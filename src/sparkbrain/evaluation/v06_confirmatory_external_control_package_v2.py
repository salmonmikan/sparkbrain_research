from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .v06_confirmatory_environment_lock_v2 import ExecutionEnvironmentLockV2
from .v06_confirmatory_external_verification_v2 import (
    IndependentFreezeVerificationV2,
)
from .v06_confirmatory_freeze_bundle_v2 import ExternalFreezeBundleV2

_CONTROL_PACKAGE_VERSION = "v06-external-control-package-2"
_REQUIRED_FILES = (
    "candidate_execution_counter.json",
    "environment_lock.json",
    "environment_lock.sha256",
    "freeze_bundle.json",
    "freeze_bundle.sha256",
    "independent_verification.json",
    "independent_verification.sha256",
)


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _payload(value: object) -> bytes:
    return (_canonical_json(value) + "\n").encode("utf-8")


def _digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _write_exclusive(path: Path, value: object) -> str:
    payload = _payload(value)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(path, 0o444)
    return _digest_bytes(payload)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@dataclass(frozen=True, slots=True)
class ExternalControlPackageV2:
    package_version: str
    bundle_hash: str
    environment_lock_hash: str
    verification_hash: str
    file_hashes: dict[str, str]
    candidate_execution_counter: int

    def validate(self) -> None:
        if self.package_version != _CONTROL_PACKAGE_VERSION:
            raise ValueError("unexpected control package version")
        if any(
            len(value) != 64
            for value in (
                self.bundle_hash,
                self.environment_lock_hash,
                self.verification_hash,
                *self.file_hashes.values(),
            )
        ):
            raise ValueError("control package contains a malformed hash")
        if self.candidate_execution_counter != 0:
            raise ValueError("control package counter must begin at zero")
        if set(self.file_hashes) != set(_REQUIRED_FILES):
            raise ValueError("control package file inventory is incomplete")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def package_hash(self) -> str:
        return _digest_bytes(_payload(self.state_dict()))


def write_external_control_package_v2(
    bundle: ExternalFreezeBundleV2,
    environment_lock: ExecutionEnvironmentLockV2,
    verification: IndependentFreezeVerificationV2,
) -> ExternalControlPackageV2:
    """Write the exact prelaunch control package into a new empty directory."""

    bundle.validate_for_execution()
    environment_lock.validate()
    if environment_lock.state_dict() != bundle.environment_lock:
        raise ValueError("environment lock differs from approved bundle")
    if not verification.verification_passed or not verification.approval_issued:
        raise ValueError("independent verification has not issued approval")
    if verification.reviewer != bundle.reviewer:
        raise ValueError("verification reviewer differs from approved bundle")
    if verification.expected_unsigned_hash != bundle.unsigned_hash():
        raise ValueError("verification does not bind approved unsigned bundle")

    control_root = Path(bundle.artifact_layout["control_root"])
    raw_root = Path(bundle.artifact_layout["raw_root"])
    analysis_root = Path(bundle.artifact_layout["analysis_root"])
    if control_root.exists() and any(control_root.iterdir()):
        raise FileExistsError("external control root must be empty")
    if raw_root.exists() and any(raw_root.iterdir()):
        raise FileExistsError("external raw root must be empty")
    if analysis_root.exists() and any(analysis_root.iterdir()):
        raise FileExistsError("external analysis root must be empty")
    control_root.mkdir(parents=True, exist_ok=True)

    file_hashes: dict[str, str] = {}
    file_hashes["freeze_bundle.json"] = _write_exclusive(
        control_root / "freeze_bundle.json",
        bundle.state_dict(),
    )
    file_hashes["freeze_bundle.sha256"] = _write_exclusive(
        control_root / "freeze_bundle.sha256",
        {"sha256": file_hashes["freeze_bundle.json"]},
    )
    file_hashes["environment_lock.json"] = _write_exclusive(
        control_root / "environment_lock.json",
        environment_lock.state_dict(),
    )
    file_hashes["environment_lock.sha256"] = _write_exclusive(
        control_root / "environment_lock.sha256",
        {"sha256": file_hashes["environment_lock.json"]},
    )
    file_hashes["independent_verification.json"] = _write_exclusive(
        control_root / "independent_verification.json",
        verification.state_dict(),
    )
    file_hashes["independent_verification.sha256"] = _write_exclusive(
        control_root / "independent_verification.sha256",
        {"sha256": file_hashes["independent_verification.json"]},
    )
    file_hashes["candidate_execution_counter.json"] = _write_exclusive(
        control_root / "candidate_execution_counter.json",
        {"bundle_hash": bundle.bundle_hash(), "count": 0},
    )
    _fsync_directory(control_root)
    package = ExternalControlPackageV2(
        package_version=_CONTROL_PACKAGE_VERSION,
        bundle_hash=bundle.bundle_hash(),
        environment_lock_hash=environment_lock.lock_hash(),
        verification_hash=_digest_bytes(_payload(verification.state_dict())),
        file_hashes=file_hashes,
        candidate_execution_counter=0,
    )
    package.validate()
    return package

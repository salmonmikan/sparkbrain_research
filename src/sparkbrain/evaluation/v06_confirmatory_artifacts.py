from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_heldout_common import result_record_state
from .v06_confirmatory_resource_accounting import MeasuredConditionExecution

ARTIFACT_CONTRACT_VERSION = "v06-atomic-raw-artifacts-1"
EXECUTION_FILE_NAMES = (
    "metadata.json",
    "results.jsonl",
    "raw_resource.json",
    "normalized_resource.json",
    "checksums.json",
    "COMPLETE",
)
RUN_FILE_NAMES = (
    "raw_manifest.json",
    "checksums.json",
    "RAW_COMPLETE",
)


def _canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _write_bytes_fsync(path: Path, value: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _make_read_only(path: Path) -> None:
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file():
            child.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif child.is_dir():
            child.chmod(
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IXOTH
            )
    path.chmod(
        stat.S_IRUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )


@dataclass(frozen=True, slots=True)
class ExecutionIdentity:
    artifact_contract_version: str
    world_generation_id: str
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    source_code_sha: str
    manifest_hash: str
    execution_id: str

    def validate(self) -> None:
        if self.artifact_contract_version != ARTIFACT_CONTRACT_VERSION:
            raise ValueError("artifact contract version mismatch")
        if not self.world_generation_id or not self.family_id or self.seed < 0:
            raise ValueError("execution identity fields must be valid")
        if len(self.source_code_sha) != 40 or any(
            char not in "0123456789abcdef" for char in self.source_code_sha
        ):
            raise ValueError("source code SHA must be 40 lowercase hex characters")
        if len(self.manifest_hash) != 64:
            raise ValueError("manifest hash must be SHA-256")
        if self.execution_id != deterministic_execution_id(
            world_generation_id=self.world_generation_id,
            family_id=self.family_id,
            seed=self.seed,
            condition=self.condition,
            source_code_sha=self.source_code_sha,
            manifest_hash=self.manifest_hash,
        ):
            raise ValueError("execution ID does not match its frozen inputs")

    @property
    def key(self) -> tuple[str, int, ConfirmatoryCondition]:
        return (self.family_id, self.seed, self.condition)

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["condition"] = self.condition.value
        return value


def deterministic_execution_id(
    *,
    world_generation_id: str,
    family_id: str,
    seed: int,
    condition: ConfirmatoryCondition,
    source_code_sha: str,
    manifest_hash: str,
) -> str:
    return "execution-" + digest(
        {
            "artifact_contract_version": ARTIFACT_CONTRACT_VERSION,
            "condition": condition.value,
            "family_id": family_id,
            "manifest_hash": manifest_hash,
            "seed": seed,
            "source_code_sha": source_code_sha,
            "world_generation_id": world_generation_id,
        }
    )[:40]


@dataclass(frozen=True, slots=True)
class ExecutionBundleVerification:
    execution_id: str
    result_record_count: int
    checksum_match: bool
    complete_marker_present: bool
    identity_match: bool
    valid: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RawRunReceipt:
    run_id: str
    final_directory: str
    execution_count: int
    result_record_count: int
    raw_resource_count: int
    normalized_resource_count: int
    raw_manifest_hash: str
    run_checksums_hash: str
    immutable_permissions_applied: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def artifact_contract_hash() -> str:
    return digest(
        {
            "atomicity": "per-execution-directory then per-run-directory rename",
            "checksum_algorithm": "sha256",
            "execution_files": list(EXECUTION_FILE_NAMES),
            "run_files": list(RUN_FILE_NAMES),
            "version": ARTIFACT_CONTRACT_VERSION,
        }
    )


def write_execution_bundle(
    run_staging_directory: Path,
    identity: ExecutionIdentity,
    measured: MeasuredConditionExecution,
) -> Path:
    """Atomically commit one complete result/resource/metadata bundle."""

    identity.validate()
    measured.validate()
    execution = measured.execution
    if execution.resource.key != identity.key:
        raise ValueError("execution payload does not match deterministic identity")
    if execution.world_specification_hash == "":
        raise ValueError("execution world hash must be present")

    executions_directory = run_staging_directory / "executions"
    temporary_directory = run_staging_directory / ".transactions"
    executions_directory.mkdir(parents=True, exist_ok=True)
    temporary_directory.mkdir(parents=True, exist_ok=True)
    final_directory = executions_directory / identity.execution_id
    if final_directory.exists():
        raise FileExistsError(f"duplicate execution: {identity.execution_id}")

    transaction = Path(
        tempfile.mkdtemp(
            prefix=f"{identity.execution_id}.",
            dir=temporary_directory,
        )
    )
    try:
        metadata = {
            "artifact_contract_version": ARTIFACT_CONTRACT_VERSION,
            "execution_identity": identity.state_dict(),
            "semantic_hash": execution.semantic_hash,
            "world_specification_hash": execution.world_specification_hash,
        }
        result_lines = b"".join(
            _canonical_json_bytes(result_record_state(row))
            for row in execution.records
        )
        payloads = {
            "metadata.json": _canonical_json_bytes(metadata),
            "results.jsonl": result_lines,
            "raw_resource.json": _canonical_json_bytes(
                execution.resource.state_dict()
            ),
            "normalized_resource.json": _canonical_json_bytes(
                measured.normalized_resource.state_dict()
            ),
        }
        for file_name, value in payloads.items():
            _write_bytes_fsync(transaction / file_name, value)
        checksums = {
            file_name: _sha256_bytes(value)
            for file_name, value in sorted(payloads.items())
        }
        _write_bytes_fsync(
            transaction / "checksums.json",
            _canonical_json_bytes(
                {
                    "algorithm": "sha256",
                    "files": checksums,
                }
            ),
        )
        _write_bytes_fsync(
            transaction / "COMPLETE",
            _canonical_json_bytes(
                {
                    "execution_id": identity.execution_id,
                    "result_record_count": len(execution.records),
                }
            ),
        )
        _fsync_directory(transaction)
        os.rename(transaction, final_directory)
        _fsync_directory(executions_directory)
    except BaseException:
        shutil.rmtree(transaction, ignore_errors=True)
        raise
    return final_directory


def verify_execution_bundle(path: Path) -> ExecutionBundleVerification:
    complete = path.joinpath("COMPLETE").is_file()
    required = set(EXECUTION_FILE_NAMES)
    present = {row.name for row in path.iterdir()} if path.is_dir() else set()
    if not required.issubset(present):
        return ExecutionBundleVerification(
            execution_id=path.name,
            result_record_count=0,
            checksum_match=False,
            complete_marker_present=complete,
            identity_match=False,
            valid=False,
        )
    try:
        checksums = json.loads(path.joinpath("checksums.json").read_text("utf-8"))
        metadata = json.loads(path.joinpath("metadata.json").read_text("utf-8"))
        marker = json.loads(path.joinpath("COMPLETE").read_text("utf-8"))
        result_rows = tuple(
            json.loads(line)
            for line in path.joinpath("results.jsonl").read_text("utf-8").splitlines()
            if line.strip()
        )
    except (OSError, json.JSONDecodeError):
        return ExecutionBundleVerification(
            execution_id=path.name,
            result_record_count=0,
            checksum_match=False,
            complete_marker_present=complete,
            identity_match=False,
            valid=False,
        )
    checksum_match = checksums.get("algorithm") == "sha256" and all(
        path.joinpath(file_name).is_file()
        and _sha256_file(path / file_name) == expected
        for file_name, expected in checksums.get("files", {}).items()
    )
    execution_id = str(
        metadata.get("execution_identity", {}).get("execution_id", "")
    )
    identity_match = (
        execution_id == path.name
        and marker.get("execution_id") == path.name
        and marker.get("result_record_count") == len(result_rows)
        and len(result_rows) == len(EvidenceDomain)
    )
    return ExecutionBundleVerification(
        execution_id=path.name,
        result_record_count=len(result_rows),
        checksum_match=checksum_match,
        complete_marker_present=complete,
        identity_match=identity_match,
        valid=complete and checksum_match and identity_match,
    )


class AtomicRawRunWriter:
    """Two-level transaction: complete executions, then one immutable raw run."""

    def __init__(
        self,
        output_root: Path,
        *,
        run_id: str,
        expected_execution_count: int,
        expected_result_record_count: int,
    ) -> None:
        if not run_id or expected_execution_count < 1:
            raise ValueError("raw run identity and expected count must be valid")
        if expected_result_record_count < expected_execution_count:
            raise ValueError("raw run result count cannot be smaller than executions")
        self.output_root = output_root
        self.run_id = run_id
        self.expected_execution_count = expected_execution_count
        self.expected_result_record_count = expected_result_record_count
        self.staging_root = output_root / ".staging"
        self.raw_root = output_root / "raw"
        self.run_staging_directory = self.staging_root / run_id
        self.final_directory = self.raw_root / run_id
        if self.final_directory.exists() or self.run_staging_directory.exists():
            raise FileExistsError(f"run already exists: {run_id}")
        self.run_staging_directory.mkdir(parents=True, exist_ok=False)
        self.raw_root.mkdir(parents=True, exist_ok=True)
        _fsync_directory(self.staging_root)

    def add(
        self,
        identity: ExecutionIdentity,
        measured: MeasuredConditionExecution,
    ) -> Path:
        return write_execution_bundle(
            self.run_staging_directory,
            identity,
            measured,
        )

    def finalize(self) -> RawRunReceipt:
        executions_directory = self.run_staging_directory / "executions"
        execution_directories = tuple(
            sorted(
                row
                for row in executions_directory.iterdir()
                if row.is_dir()
            )
        )
        verifications = tuple(
            verify_execution_bundle(path) for path in execution_directories
        )
        if len(verifications) != self.expected_execution_count:
            raise RuntimeError("raw run execution count is incomplete")
        if not all(row.valid for row in verifications):
            raise RuntimeError("raw run contains an invalid execution bundle")
        result_count = sum(row.result_record_count for row in verifications)
        if result_count != self.expected_result_record_count:
            raise RuntimeError("raw run result-record count is incomplete")
        execution_ids = tuple(row.execution_id for row in verifications)
        if len(set(execution_ids)) != len(execution_ids):
            raise RuntimeError("raw run contains duplicate execution IDs")

        raw_manifest = {
            "artifact_contract_version": ARTIFACT_CONTRACT_VERSION,
            "execution_count": len(verifications),
            "execution_ids": list(execution_ids),
            "normalized_resource_count": len(verifications),
            "raw_resource_count": len(verifications),
            "result_record_count": result_count,
            "run_id": self.run_id,
        }
        _write_bytes_fsync(
            self.run_staging_directory / "raw_manifest.json",
            _canonical_json_bytes(raw_manifest),
        )
        run_checksums = {
            "raw_manifest.json": _sha256_file(
                self.run_staging_directory / "raw_manifest.json"
            ),
            **{
                f"executions/{path.name}/checksums.json": _sha256_file(
                    path / "checksums.json"
                )
                for path in execution_directories
            },
        }
        _write_bytes_fsync(
            self.run_staging_directory / "checksums.json",
            _canonical_json_bytes(
                {
                    "algorithm": "sha256",
                    "files": run_checksums,
                }
            ),
        )
        _write_bytes_fsync(
            self.run_staging_directory / "RAW_COMPLETE",
            _canonical_json_bytes(
                {
                    "execution_count": len(verifications),
                    "result_record_count": result_count,
                    "run_id": self.run_id,
                }
            ),
        )
        _fsync_directory(self.run_staging_directory)
        os.rename(self.run_staging_directory, self.final_directory)
        _fsync_directory(self.raw_root)
        _make_read_only(self.final_directory)
        return RawRunReceipt(
            run_id=self.run_id,
            final_directory=str(self.final_directory),
            execution_count=len(verifications),
            result_record_count=result_count,
            raw_resource_count=len(verifications),
            normalized_resource_count=len(verifications),
            raw_manifest_hash=_sha256_file(
                self.final_directory / "raw_manifest.json"
            ),
            run_checksums_hash=_sha256_file(
                self.final_directory / "checksums.json"
            ),
            immutable_permissions_applied=True,
        )


def verify_raw_run(path: Path) -> RawRunReceipt:
    if not path.joinpath("RAW_COMPLETE").is_file():
        raise RuntimeError("raw run is missing RAW_COMPLETE")
    manifest = json.loads(path.joinpath("raw_manifest.json").read_text("utf-8"))
    checksums = json.loads(path.joinpath("checksums.json").read_text("utf-8"))
    if checksums.get("algorithm") != "sha256":
        raise RuntimeError("raw run checksum algorithm mismatch")
    for relative_path, expected in checksums.get("files", {}).items():
        target = path / relative_path
        if not target.is_file() or _sha256_file(target) != expected:
            raise RuntimeError(f"raw run checksum mismatch: {relative_path}")
    executions = tuple(
        sorted(row for row in path.joinpath("executions").iterdir() if row.is_dir())
    )
    verification = tuple(verify_execution_bundle(row) for row in executions)
    if not all(row.valid for row in verification):
        raise RuntimeError("raw run execution verification failed")
    result_count = sum(row.result_record_count for row in verification)
    if (
        len(executions) != manifest["execution_count"]
        or result_count != manifest["result_record_count"]
    ):
        raise RuntimeError("raw run manifest counts do not match contents")
    return RawRunReceipt(
        run_id=str(manifest["run_id"]),
        final_directory=str(path),
        execution_count=len(executions),
        result_record_count=result_count,
        raw_resource_count=int(manifest["raw_resource_count"]),
        normalized_resource_count=int(manifest["normalized_resource_count"]),
        raw_manifest_hash=_sha256_file(path / "raw_manifest.json"),
        run_checksums_hash=_sha256_file(path / "checksums.json"),
        immutable_permissions_applied=not bool(
            path.stat().st_mode & stat.S_IWUSR
        ),
    )

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory_candidate_manifest import build_candidate_manifest
from .v06_confirmatory_environment import (
    ConfirmatoryEnvironmentLock,
    environment_lock_from_state,
    verify_environment_lock,
)
from .v06_confirmatory_execution_seal import (
    ConfirmatoryFreezeRecord,
    ExecutionSealReport,
    build_freeze_record,
    freeze_record_from_state,
    validate_execution_seal,
)
from .v06_confirmatory_launch_gate import (
    GitWorkspaceState,
    inspect_git_workspace,
)

FREEZE_CANDIDATE_VERSION = "v06-independent-freeze-candidate-1"
FREEZE_VERIFICATION_VERSION = "v06-independent-freeze-verification-1"


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


def _atomic_exclusive_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_canonical_json_bytes(value))
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            raise FileExistsError(path)
        os.rename(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _unsigned_seal_components_complete(report: ExecutionSealReport) -> bool:
    values = report.state_dict()
    ignored = {"approval_present", "execution_allowed", "seal_hash"}
    return all(bool(value) for key, value in values.items() if key not in ignored)


@dataclass(frozen=True, slots=True)
class FreezeCandidateBundle:
    version: str
    builder_id: str
    source_code_sha: str
    source_workspace_state: dict[str, Any]
    manifest_state: dict[str, Any]
    manifest_hash: str
    environment_lock_state: dict[str, Any]
    environment_lock_hash: str
    unsigned_freeze_record_state: dict[str, Any]
    unsigned_seal_hash: str

    def validate_shape(self) -> None:
        if self.version != FREEZE_CANDIDATE_VERSION:
            raise ValueError("freeze candidate version mismatch")
        if not self.builder_id.strip():
            raise ValueError("freeze candidate builder identity is required")
        if len(self.source_code_sha) != 40 or any(
            character not in "0123456789abcdef"
            for character in self.source_code_sha
        ):
            raise ValueError("freeze candidate source SHA must be lowercase Git SHA")
        for name in (
            "manifest_hash",
            "environment_lock_hash",
            "unsigned_seal_hash",
        ):
            value = str(getattr(self, name))
            if len(value) != 64:
                raise ValueError(f"{name} must be SHA-256")
        if str(self.unsigned_freeze_record_state.get("approval_id", "")):
            raise ValueError("freeze candidate must remain unsigned")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def candidate_hash(self) -> str:
        self.validate_shape()
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class IndependentFreezeVerification:
    version: str
    candidate_hash: str
    builder_id: str
    reviewer_id: str
    reviewer_is_independent: bool
    source_workspace_clean: bool
    source_workspace_sha_matches: bool
    source_manifest_state_matches: bool
    source_manifest_hash_matches: bool
    environment_lock_state_matches: bool
    environment_lock_hash_matches: bool
    unsigned_freeze_record_matches: bool
    unsigned_seal_hash_matches: bool
    all_unsigned_seal_components_match: bool
    unsigned_approval_absent: bool
    ready_for_approval: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def verification_hash(self) -> str:
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ApprovedFreezePackage:
    candidate: FreezeCandidateBundle
    independent_verification: IndependentFreezeVerification
    approved_freeze_record: ConfirmatoryFreezeRecord

    def validate(self) -> None:
        self.candidate.validate_shape()
        if not self.independent_verification.ready_for_approval:
            raise ValueError("freeze package lacks independent verification")
        if not self.approved_freeze_record.approval_id.startswith("APPROVED:"):
            raise ValueError("freeze package lacks structured approval")

    def state_dict(self) -> dict[str, Any]:
        return {
            "approved_freeze_record": (
                self.approved_freeze_record.state_dict()
            ),
            "candidate": self.candidate.state_dict(),
            "independent_verification": (
                self.independent_verification.state_dict()
            ),
        }

    def package_hash(self) -> str:
        self.validate()
        return digest(self.state_dict())


def build_freeze_candidate(
    *,
    repository_root: Path,
    source_code_sha: str,
    environment_lock: ConfirmatoryEnvironmentLock,
    builder_id: str,
    workspace: GitWorkspaceState | None = None,
) -> FreezeCandidateBundle:
    """Build an unsigned freeze candidate from one clean source checkout.

    The returned object can be serialized outside Git. It intentionally has no
    approval and therefore cannot pass the execution seal.
    """

    repository_root = repository_root.resolve()
    workspace_state = workspace or inspect_git_workspace(repository_root)
    if not workspace_state.clean:
        raise RuntimeError("freeze candidate source workspace is not clean")
    if workspace_state.head_sha != source_code_sha:
        raise RuntimeError("freeze candidate source SHA does not match checkout")
    environment_lock.validate()
    manifest = build_candidate_manifest(source_code_sha=source_code_sha)
    unsigned_record = build_freeze_record(
        manifest,
        source_code_sha=source_code_sha,
        repository_root=repository_root,
        environment_lock=environment_lock,
        approval_id="",
    )
    seal_report = validate_execution_seal(
        manifest,
        unsigned_record,
        repository_root=repository_root,
        environment_lock=environment_lock,
    )
    if not _unsigned_seal_components_complete(seal_report):
        raise RuntimeError("freeze candidate contains an unfrozen protocol component")
    if seal_report.approval_present or seal_report.execution_allowed:
        raise RuntimeError("unsigned freeze candidate unexpectedly became executable")
    bundle = FreezeCandidateBundle(
        version=FREEZE_CANDIDATE_VERSION,
        builder_id=builder_id,
        source_code_sha=source_code_sha,
        source_workspace_state=workspace_state.state_dict(),
        manifest_state=manifest.state_dict(),
        manifest_hash=manifest.manifest_hash(),
        environment_lock_state=environment_lock.state_dict(),
        environment_lock_hash=environment_lock.environment_hash(),
        unsigned_freeze_record_state=unsigned_record.state_dict(),
        unsigned_seal_hash=unsigned_record.seal_hash(),
    )
    bundle.validate_shape()
    return bundle


def freeze_candidate_from_state(
    state: dict[str, Any],
) -> FreezeCandidateBundle:
    bundle = FreezeCandidateBundle(
        version=str(state["version"]),
        builder_id=str(state["builder_id"]),
        source_code_sha=str(state["source_code_sha"]),
        source_workspace_state=dict(state["source_workspace_state"]),
        manifest_state=dict(state["manifest_state"]),
        manifest_hash=str(state["manifest_hash"]),
        environment_lock_state=dict(state["environment_lock_state"]),
        environment_lock_hash=str(state["environment_lock_hash"]),
        unsigned_freeze_record_state=dict(
            state["unsigned_freeze_record_state"]
        ),
        unsigned_seal_hash=str(state["unsigned_seal_hash"]),
    )
    if set(bundle.state_dict()) != set(state):
        raise ValueError("freeze candidate contains missing or unexpected fields")
    bundle.validate_shape()
    return bundle


def independently_verify_freeze_candidate(
    candidate: FreezeCandidateBundle,
    *,
    repository_root: Path,
    reviewer_id: str,
    workspace: GitWorkspaceState | None = None,
    observed_environment: ConfirmatoryEnvironmentLock | None = None,
) -> IndependentFreezeVerification:
    """Rebuild every source-derived value before a different reviewer approves."""

    candidate.validate_shape()
    repository_root = repository_root.resolve()
    workspace_state = workspace or inspect_git_workspace(repository_root)
    manifest = build_candidate_manifest(
        source_code_sha=candidate.source_code_sha
    )
    expected_environment = environment_lock_from_state(
        candidate.environment_lock_state
    )
    environment_report = verify_environment_lock(
        expected_environment,
        observed_environment or expected_environment,
    )
    stored_record = freeze_record_from_state(
        candidate.unsigned_freeze_record_state
    )
    rebuilt_record = build_freeze_record(
        manifest,
        source_code_sha=candidate.source_code_sha,
        repository_root=repository_root,
        environment_lock=expected_environment,
        approval_id="",
    )
    seal_report = validate_execution_seal(
        manifest,
        stored_record,
        repository_root=repository_root,
        environment_lock=expected_environment,
    )
    values = {
        "reviewer_is_independent": (
            bool(reviewer_id.strip()) and reviewer_id != candidate.builder_id
        ),
        "source_workspace_clean": workspace_state.clean,
        "source_workspace_sha_matches": (
            workspace_state.head_sha == candidate.source_code_sha
        ),
        "source_manifest_state_matches": (
            manifest.state_dict() == candidate.manifest_state
        ),
        "source_manifest_hash_matches": (
            manifest.manifest_hash() == candidate.manifest_hash
        ),
        "environment_lock_state_matches": environment_report.exact_match,
        "environment_lock_hash_matches": (
            expected_environment.environment_hash()
            == candidate.environment_lock_hash
        ),
        "unsigned_freeze_record_matches": (
            stored_record == rebuilt_record
        ),
        "unsigned_seal_hash_matches": (
            stored_record.seal_hash() == candidate.unsigned_seal_hash
        ),
        "all_unsigned_seal_components_match": (
            _unsigned_seal_components_complete(seal_report)
        ),
        "unsigned_approval_absent": (
            not seal_report.approval_present
            and not seal_report.execution_allowed
            and stored_record.approval_id == ""
        ),
    }
    verification = IndependentFreezeVerification(
        version=FREEZE_VERIFICATION_VERSION,
        candidate_hash=candidate.candidate_hash(),
        builder_id=candidate.builder_id,
        reviewer_id=reviewer_id,
        **values,
        ready_for_approval=all(values.values()),
    )
    return verification


def issue_execution_seal(
    candidate: FreezeCandidateBundle,
    *,
    repository_root: Path,
    reviewer_id: str,
    workspace: GitWorkspaceState | None = None,
    observed_environment: ConfirmatoryEnvironmentLock | None = None,
) -> ApprovedFreezePackage:
    """Issue a structured external seal after independent verification."""

    verification = independently_verify_freeze_candidate(
        candidate,
        repository_root=repository_root,
        reviewer_id=reviewer_id,
        workspace=workspace,
        observed_environment=observed_environment,
    )
    if not verification.ready_for_approval:
        raise RuntimeError("freeze candidate failed independent verification")
    approval_id = (
        f"APPROVED:{reviewer_id}:{candidate.candidate_hash()[:16]}"
    )
    approved_record = replace(
        freeze_record_from_state(candidate.unsigned_freeze_record_state),
        approval_id=approval_id,
    )
    manifest = build_candidate_manifest(
        source_code_sha=candidate.source_code_sha
    )
    environment = environment_lock_from_state(candidate.environment_lock_state)
    seal_report = validate_execution_seal(
        manifest,
        approved_record,
        repository_root=repository_root,
        environment_lock=environment,
    )
    if not seal_report.execution_allowed:
        raise RuntimeError("approved freeze package did not produce a valid seal")
    package = ApprovedFreezePackage(
        candidate=candidate,
        independent_verification=verification,
        approved_freeze_record=approved_record,
    )
    package.validate()
    return package


def write_freeze_candidate(
    path: Path,
    candidate: FreezeCandidateBundle,
) -> None:
    candidate.validate_shape()
    _atomic_exclusive_json(path, candidate.state_dict())


def read_freeze_candidate(path: Path) -> FreezeCandidateBundle:
    return freeze_candidate_from_state(json.loads(path.read_text("utf-8")))


def write_approved_control_package(
    control_directory: Path,
    package: ApprovedFreezePackage,
) -> None:
    """Write seal controls externally, never into the frozen source commit."""

    package.validate()
    control_directory.mkdir(parents=True, exist_ok=True)
    _atomic_exclusive_json(
        control_directory / "freeze_record.json",
        package.approved_freeze_record.state_dict(),
    )
    _atomic_exclusive_json(
        control_directory / "environment_lock.json",
        package.candidate.environment_lock_state,
    )
    _atomic_exclusive_json(
        control_directory / "freeze_verification.json",
        {
            **package.independent_verification.state_dict(),
            "approved_package_hash": package.package_hash(),
        },
    )

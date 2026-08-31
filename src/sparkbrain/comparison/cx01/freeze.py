from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from .candidate import (
    CX01_COMPARATOR_INVENTORY,
    CandidateSpec,
    candidate_grid_hash,
    declaration_bundle_hash,
)
from .formal_policy import FormalScoringPolicy
from .privilege import privilege_profile
from .schedule import build_balanced_exposure_schedule
from .worlds import development_grid_hash


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _require_sha256(value: str, name: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value.lower()):
        raise ValueError(f"{name} must be a lowercase SHA-256 hex digest")


def _require_git_sha(value: str) -> None:
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value.lower()):
        raise ValueError("source_git_sha must be a 40-character Git SHA")


@dataclass(frozen=True, slots=True)
class FreezeManifest:
    protocol_version: str
    source_git_sha: str
    builder: str
    candidate_spec_hash: str
    candidate_grid_hash: str
    declaration_bundle_hash: str
    development_grid_hash: str
    comparator_inventory: tuple[str, ...]
    privilege_inventory_hash: str
    schedule_policy_hash: str
    scoring_policy_hash: str
    result_schema_hash: str
    resource_schema_hash: str
    execution_command: str
    artifact_root: str
    status: str = "FROZEN"

    def validate(self) -> None:
        _require_git_sha(self.source_git_sha)
        if not self.builder.strip():
            raise ValueError("freeze manifest requires a builder identity")
        for name in (
            "candidate_spec_hash",
            "candidate_grid_hash",
            "declaration_bundle_hash",
            "development_grid_hash",
            "privilege_inventory_hash",
            "schedule_policy_hash",
            "scoring_policy_hash",
            "result_schema_hash",
            "resource_schema_hash",
        ):
            _require_sha256(str(getattr(self, name)), name)
        if self.status != "FROZEN":
            raise ValueError("manifest must be frozen")
        if not self.comparator_inventory or len(set(self.comparator_inventory)) != len(
            self.comparator_inventory
        ):
            raise ValueError("comparator inventory is invalid")
        if not self.execution_command or not self.artifact_root:
            raise ValueError("execution command and artifact root are required")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["comparator_inventory"] = list(self.comparator_inventory)
        return value

    def manifest_hash(self) -> str:
        return _digest(self.state_dict())

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> FreezeManifest:
        manifest = cls(
            protocol_version=str(state["protocol_version"]),
            source_git_sha=str(state["source_git_sha"]),
            builder=str(state["builder"]),
            candidate_spec_hash=str(state["candidate_spec_hash"]),
            candidate_grid_hash=str(state["candidate_grid_hash"]),
            declaration_bundle_hash=str(state["declaration_bundle_hash"]),
            development_grid_hash=str(state["development_grid_hash"]),
            comparator_inventory=tuple(str(row) for row in state["comparator_inventory"]),
            privilege_inventory_hash=str(state["privilege_inventory_hash"]),
            schedule_policy_hash=str(state["schedule_policy_hash"]),
            scoring_policy_hash=str(state["scoring_policy_hash"]),
            result_schema_hash=str(state["result_schema_hash"]),
            resource_schema_hash=str(state["resource_schema_hash"]),
            execution_command=str(state["execution_command"]),
            artifact_root=str(state["artifact_root"]),
            status=str(state.get("status", "FROZEN")),
        )
        manifest.validate()
        return manifest


@dataclass(frozen=True, slots=True)
class ExecutionSeal:
    manifest_hash: str
    source_git_sha: str
    reviewer: str
    approval_digest: str
    approved: bool

    def validate(self) -> None:
        _require_sha256(self.manifest_hash, "manifest_hash")
        _require_sha256(self.approval_digest, "approval_digest")
        _require_git_sha(self.source_git_sha)
        if not self.approved or not self.reviewer.strip():
            raise ValueError("execution seal requires explicit independent approval")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> ExecutionSeal:
        seal = cls(
            manifest_hash=str(state["manifest_hash"]),
            source_git_sha=str(state["source_git_sha"]),
            reviewer=str(state["reviewer"]),
            approval_digest=str(state["approval_digest"]),
            approved=bool(state["approved"]),
        )
        seal.validate()
        return seal


def _privilege_inventory_hash() -> str:
    return _digest([privilege_profile(kind).state_dict() for kind in CX01_COMPARATOR_INVENTORY])


def _schedule_policy_hash() -> str:
    schedule = build_balanced_exposure_schedule((6, 5, 4))
    return _digest(
        {
            "algorithm": "interleaved-round-alternating-direction-v1",
            "representative": schedule.state_dict(),
        }
    )


def _result_schema_hash() -> str:
    return _digest(
        {
            "fields": [
                "candidate_spec_hash",
                "execution_id",
                "formal_index",
                "manifest_hash",
                "kind",
                "family",
                "seed",
                "world_hash",
                "training_transcript_hash",
                "evidence",
                "decision",
                "resource",
            ],
            "family_gates": "non-compensatory-v1",
        }
    )


def _resource_schema_hash() -> str:
    return _digest(
        {
            "fields": [
                "kind",
                "wall_clock_ns",
                "process_cpu_ns",
                "peak_traced_memory_bytes",
                "parameter_count",
                "state_entry_count",
                "observed_external_events",
                "generated_internal_events",
                "privileges",
                "decision_use",
            ],
            "decision_use": "descriptive-only",
        }
    )


def build_freeze_manifest(
    *,
    source_git_sha: str,
    builder: str,
    candidate: CandidateSpec,
    execution_command: str,
    artifact_root: str,
) -> FreezeManifest:
    candidate.validate()
    manifest = FreezeManifest(
        protocol_version=candidate.protocol_version,
        source_git_sha=source_git_sha,
        builder=builder,
        candidate_spec_hash=candidate.specification_hash(),
        candidate_grid_hash=candidate_grid_hash(candidate),
        declaration_bundle_hash=declaration_bundle_hash(candidate),
        development_grid_hash=development_grid_hash(),
        comparator_inventory=tuple(kind.value for kind in CX01_COMPARATOR_INVENTORY),
        privilege_inventory_hash=_privilege_inventory_hash(),
        schedule_policy_hash=_schedule_policy_hash(),
        scoring_policy_hash=FormalScoringPolicy().policy_hash(),
        result_schema_hash=_result_schema_hash(),
        resource_schema_hash=_resource_schema_hash(),
        execution_command=execution_command,
        artifact_root=artifact_root,
    )
    manifest.validate()
    return manifest


def issue_execution_seal(
    manifest: FreezeManifest,
    *,
    reviewer: str,
    approval_digest: str,
    approved: bool,
) -> ExecutionSeal:
    manifest.validate()
    normalized_reviewer = reviewer.strip()
    if normalized_reviewer == manifest.builder.strip():
        raise ValueError("freeze builder cannot self-approve the execution seal")
    seal = ExecutionSeal(
        manifest_hash=manifest.manifest_hash(),
        source_git_sha=manifest.source_git_sha,
        reviewer=normalized_reviewer,
        approval_digest=approval_digest,
        approved=approved,
    )
    seal.validate()
    return seal


def require_execution_seal(
    manifest: FreezeManifest,
    seal: ExecutionSeal,
    *,
    current_source_git_sha: str,
) -> None:
    manifest.validate()
    seal.validate()
    _require_git_sha(current_source_git_sha)
    if seal.reviewer.strip() == manifest.builder.strip():
        raise RuntimeError("execution seal is not independent of freeze builder")
    if manifest.source_git_sha != current_source_git_sha:
        raise RuntimeError("frozen source SHA does not match current source")
    if seal.source_git_sha != current_source_git_sha:
        raise RuntimeError("execution seal source SHA does not match current source")
    if seal.manifest_hash != manifest.manifest_hash():
        raise RuntimeError("execution seal does not bind the supplied manifest")

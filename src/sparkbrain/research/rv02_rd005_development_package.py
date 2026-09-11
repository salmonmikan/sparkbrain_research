"""Execution-disabled package contract for prospective RV02 RD005 development.

This module prepares identity, manifest, collision-registry, and no-clobber
contracts only. It deliberately does not construct a Field, build an RD005
artifact, invoke the independent verifier, run a learner/probe, score an
outcome, write an output directory, or grant held-out/formal authority.

The preregistered stage order is explicit: a construction-only D1 artifact must
be generated, retained, and reviewed before any later capability runner exists.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import PurePosixPath

from .rv02_rd005_construction_artifact import RD005_FRESH_SEED, RD005_PLAN_ID
from .rv02_rd005_gate_construction import RD005_PROTOCOL_ID

RD005_REQUIRED_SOURCE_PATHS = frozenset(
    {
        "src/sparkbrain/research/rv02_rd005_gate_construction.py",
        "src/sparkbrain/research/rv02_rd005_construction_artifact.py",
        "src/sparkbrain/research/rv02_rd005_artifact_verifier.py",
        "src/sparkbrain/research/rv02_rd003_online.py",
        "src/sparkbrain/research/rv02_recruitment.py",
        "src/sparkbrain/research/rv02_scale.py",
        "src/sparkbrain/v04/contracts.py",
        "docs/research/RV02_RD005_GATE_REACHABLE_ELIGIBILITY_PREREGISTRATION.md",
        "docs/research/RV02_RD005_GATE_CONSTRUCTION_TECHNICAL_REVIEW.md",
        "docs/research/RV02_RD005_PLANNED_MATRIX_92505_TECHNICAL_REVIEW.md",
    }
)
RD005_OUTPUT_ROOT = PurePosixPath("artifacts/rv02/rd005/development")


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_git_sha(value: str) -> None:
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError("source_git_sha must be a 40-character lowercase Git SHA")


def _require_sha256(value: str, *, label: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{label} must be a 64-character lowercase SHA-256 digest")


def _require_safe_relative_path(value: str) -> None:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError("package paths must be normalized repository-relative POSIX paths")
    if str(path) != value:
        raise ValueError("package paths must use canonical POSIX spelling")


@dataclass(frozen=True, slots=True)
class RD005SourceManifestEntry:
    path: str
    sha256: str

    def validate(self) -> None:
        _require_safe_relative_path(self.path)
        _require_sha256(self.sha256, label=f"source digest for {self.path}")

    def state_dict(self) -> dict[str, str]:
        self.validate()
        return {"path": self.path, "sha256": self.sha256}


@dataclass(frozen=True, slots=True)
class RD005SourceManifest:
    source_git_sha: str
    entries: tuple[RD005SourceManifestEntry, ...]

    def validate(self) -> None:
        _require_git_sha(self.source_git_sha)
        if not self.entries:
            raise ValueError("RD005 source manifest cannot be empty")
        paths = tuple(row.path for row in self.entries)
        if len(paths) != len(set(paths)):
            raise ValueError("RD005 source manifest paths must be unique")
        for row in self.entries:
            row.validate()
        missing = sorted(RD005_REQUIRED_SOURCE_PATHS.difference(paths))
        if missing:
            raise ValueError(f"RD005 source manifest is missing required paths: {missing}")

    def state_dict(self) -> dict[str, object]:
        self.validate()
        entries = [
            row.state_dict()
            for row in sorted(self.entries, key=lambda item: item.path)
        ]
        return {
            "source_git_sha": self.source_git_sha,
            "entries": entries,
        }

    @property
    def manifest_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


@dataclass(frozen=True, slots=True)
class RD005CollisionRegistry:
    registry_id: str
    source_paths: tuple[str, ...]
    consumed_or_reserved_seed_ids: tuple[int, ...]
    consumed_or_reserved_world_ids: tuple[str, ...]
    authoritative_complete: bool

    def validate(self) -> None:
        if not self.registry_id:
            raise ValueError("RD005 collision registry requires a stable registry_id")
        if self.authoritative_complete is not True:
            raise ValueError(
                "RD005 collision registry must be explicitly authoritative and complete"
            )
        if not self.source_paths:
            raise ValueError("RD005 collision registry requires retained source paths")
        for path in self.source_paths:
            _require_safe_relative_path(path)
        if len(set(self.source_paths)) != len(self.source_paths):
            raise ValueError("RD005 collision registry source paths must be unique")
        if not self.consumed_or_reserved_seed_ids:
            raise ValueError("RD005 collision registry requires a non-empty seed registry")
        if not self.consumed_or_reserved_world_ids:
            raise ValueError("RD005 collision registry requires a non-empty world registry")
        if any(type(seed) is not int for seed in self.consumed_or_reserved_seed_ids):
            raise TypeError("RD005 retained seed identities must be exact non-boolean ints")
        if len(set(self.consumed_or_reserved_seed_ids)) != len(self.consumed_or_reserved_seed_ids):
            raise ValueError("RD005 retained seed identities must be unique")
        if any(not world_id for world_id in self.consumed_or_reserved_world_ids):
            raise ValueError("RD005 retained world identities must be non-empty")
        if len(set(self.consumed_or_reserved_world_ids)) != len(
            self.consumed_or_reserved_world_ids
        ):
            raise ValueError("RD005 retained world identities must be unique")
        if RD005_FRESH_SEED in self.consumed_or_reserved_seed_ids:
            raise ValueError("RD005 fresh seed 92505 collides with the authoritative registry")
        token = f":{RD005_FRESH_SEED}:"
        if any(token in world_id for world_id in self.consumed_or_reserved_world_ids):
            raise ValueError("RD005 fresh world namespace collides with the authoritative registry")

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "registry_id": self.registry_id,
            "source_paths": sorted(self.source_paths),
            "consumed_or_reserved_seed_ids": sorted(self.consumed_or_reserved_seed_ids),
            "consumed_or_reserved_world_ids": sorted(self.consumed_or_reserved_world_ids),
            "authoritative_complete": True,
        }

    @property
    def registry_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


@dataclass(frozen=True, slots=True)
class RD005DevelopmentPackagePlan:
    source_manifest: RD005SourceManifest
    collision_registry: RD005CollisionRegistry

    def validate(self) -> None:
        self.source_manifest.validate()
        self.collision_registry.validate()

    @property
    def run_id(self) -> str:
        self.validate()
        return (
            "rv02-rd005-development-"
            f"{self.source_manifest.source_git_sha[:16]}-"
            f"{self.collision_registry.registry_sha256[:12]}"
        )

    @property
    def output_relpath(self) -> str:
        return str(RD005_OUTPUT_ROOT / self.run_id)

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "protocol_id": RD005_PROTOCOL_ID,
            "plan_id": RD005_PLAN_ID,
            "fresh_seed": RD005_FRESH_SEED,
            "source_git_sha": self.source_manifest.source_git_sha,
            "source_manifest_sha256": self.source_manifest.manifest_sha256,
            "collision_registry_sha256": self.collision_registry.registry_sha256,
            "run_id": self.run_id,
            "output_relpath": self.output_relpath,
            "overwrite_allowed": False,
            "retry_same_identity_allowed": False,
            "d1_construction_only_stage_required": True,
            "d1_retained_and_reviewed_before_capability_required": True,
            "construction_and_capability_same_run_allowed": False,
            "construction_verifier_required_before_capability": True,
            "construction_integrity_failure_is_terminal": True,
            "zero_ready_cells_is_terminal": True,
            "capability_output_opened": False,
            "learner_or_probe_executed": False,
            "held_out_capability_allowed": False,
            "formal_execution_allowed": False,
            "construction_wrapper_bound": False,
            "capability_wrapper_bound": False,
            "python_runtime_bound": False,
        }

    @property
    def package_plan_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


__all__ = [
    "RD005CollisionRegistry",
    "RD005DevelopmentPackagePlan",
    "RD005SourceManifest",
    "RD005SourceManifestEntry",
    "RD005_OUTPUT_ROOT",
    "RD005_REQUIRED_SOURCE_PATHS",
]

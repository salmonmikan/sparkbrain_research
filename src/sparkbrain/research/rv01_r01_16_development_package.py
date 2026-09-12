"""Execution-disabled package contract for prospective RV01 R01-16 development.

This module binds source identity, retained collision registries, and a
no-clobber construction-stage namespace only. It does not build a Field, train a
learner, run a probe, score a result, open capability output, or grant
held-out/formal authority.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import PurePosixPath

from .rv01_r01_16_identity import (
    R01_16_DEVELOPMENT_SEEDS,
    R01_16_PROTOCOL_ID,
    assert_no_seed_collisions,
    development_identity_grid,
)

R01_16_REQUIRED_SOURCE_PATHS = frozenset(
    {
        "src/sparkbrain/research/rv01_r01_16_identity.py",
        "src/sparkbrain/research/rv01_r01_16_factorization.py",
        "src/sparkbrain/research/rv01_r01_16_reachability.py",
        "src/sparkbrain/research/rv01_r01_16_development_package.py",
        "src/sparkbrain/research/rv01_r01_16_construction.py",
        "docs/research/RV01_R01_16_DEVELOPMENT_IDENTITY_BINDING.md",
        "docs/research/RV01_R01_16_PREREGISTRATION_AMENDMENT_001.md",
        "docs/research/RV01_R01_16_PROPAGATION_FACTORIZATION_PREREGISTRATION.md",
    }
)
R01_16_OUTPUT_ROOT = PurePosixPath("artifacts/rv01/r01-16/development")


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
class R0116SourceManifestEntry:
    path: str
    sha256: str

    def validate(self) -> None:
        _require_safe_relative_path(self.path)
        _require_sha256(self.sha256, label=f"source digest for {self.path}")

    def state_dict(self) -> dict[str, str]:
        self.validate()
        return {"path": self.path, "sha256": self.sha256}


@dataclass(frozen=True, slots=True)
class R0116SourceManifest:
    source_git_sha: str
    entries: tuple[R0116SourceManifestEntry, ...]

    def validate(self) -> None:
        _require_git_sha(self.source_git_sha)
        if not self.entries:
            raise ValueError("R01-16 source manifest cannot be empty")
        paths = tuple(row.path for row in self.entries)
        if len(paths) != len(set(paths)):
            raise ValueError("R01-16 source manifest paths must be unique")
        for row in self.entries:
            row.validate()
        missing = sorted(R01_16_REQUIRED_SOURCE_PATHS.difference(paths))
        if missing:
            raise ValueError(f"R01-16 source manifest is missing required paths: {missing}")

    def state_dict(self) -> dict[str, object]:
        self.validate()
        entries = [
            row.state_dict()
            for row in sorted(self.entries, key=lambda item: item.path)
        ]
        return {"source_git_sha": self.source_git_sha, "entries": entries}

    @property
    def manifest_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


@dataclass(frozen=True, slots=True)
class R0116CollisionRegistry:
    registry_id: str
    source_paths: tuple[str, ...]
    consumed_or_reserved_seed_ids: tuple[int, ...]
    consumed_or_reserved_world_ids: tuple[str, ...]
    authoritative_complete: bool

    def validate(self) -> None:
        if not self.registry_id:
            raise ValueError("R01-16 collision registry requires a stable registry_id")
        if self.authoritative_complete is not True:
            raise ValueError(
                "R01-16 collision registry must be explicitly authoritative and complete"
            )
        if not self.source_paths:
            raise ValueError("R01-16 collision registry requires retained source paths")
        for path in self.source_paths:
            _require_safe_relative_path(path)
        if len(set(self.source_paths)) != len(self.source_paths):
            raise ValueError("R01-16 collision registry source paths must be unique")
        if not self.consumed_or_reserved_seed_ids:
            raise ValueError("R01-16 collision registry requires a non-empty seed registry")
        if not self.consumed_or_reserved_world_ids:
            raise ValueError("R01-16 collision registry requires a non-empty world registry")
        if any(type(seed) is not int for seed in self.consumed_or_reserved_seed_ids):
            raise TypeError("R01-16 retained seed identities must be exact non-boolean ints")
        if len(set(self.consumed_or_reserved_seed_ids)) != len(
            self.consumed_or_reserved_seed_ids
        ):
            raise ValueError("R01-16 retained seed identities must be unique")
        if any(not world_id for world_id in self.consumed_or_reserved_world_ids):
            raise ValueError("R01-16 retained world identities must be non-empty")
        if len(set(self.consumed_or_reserved_world_ids)) != len(
            self.consumed_or_reserved_world_ids
        ):
            raise ValueError("R01-16 retained world identities must be unique")

        assert_no_seed_collisions(self.consumed_or_reserved_seed_ids)
        proposed_world_ids = {row.world_id for row in development_identity_grid()}
        world_collisions = sorted(
            proposed_world_ids.intersection(self.consumed_or_reserved_world_ids)
        )
        if world_collisions:
            raise ValueError(f"R01-16 development world collision(s): {world_collisions}")

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
class R0116DevelopmentPackagePlan:
    source_manifest: R0116SourceManifest
    collision_registry: R0116CollisionRegistry

    def validate(self) -> None:
        self.source_manifest.validate()
        self.collision_registry.validate()

    @property
    def run_id(self) -> str:
        self.validate()
        return (
            "rv01-r01-16-development-"
            f"{self.source_manifest.source_git_sha[:16]}-"
            f"{self.collision_registry.registry_sha256[:12]}"
        )

    @property
    def output_relpath(self) -> str:
        return str(R01_16_OUTPUT_ROOT / self.run_id)

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "protocol_id": R01_16_PROTOCOL_ID,
            "development_seeds": list(R01_16_DEVELOPMENT_SEEDS),
            "source_git_sha": self.source_manifest.source_git_sha,
            "source_manifest_sha256": self.source_manifest.manifest_sha256,
            "collision_registry_sha256": self.collision_registry.registry_sha256,
            "run_id": self.run_id,
            "output_relpath": self.output_relpath,
            "overwrite_allowed": False,
            "retry_same_identity_allowed": False,
            "construction_only_stage_required": True,
            "construction_retained_and_reviewed_before_capability_required": True,
            "construction_and_capability_same_run_allowed": False,
            "reachability_reconstruction_required_before_capability": True,
            "construction_integrity_failure_is_terminal": True,
            "zero_eligible_worlds_is_terminal": True,
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
    "R01_16_OUTPUT_ROOT",
    "R01_16_REQUIRED_SOURCE_PATHS",
    "R0116CollisionRegistry",
    "R0116DevelopmentPackagePlan",
    "R0116SourceManifest",
    "R0116SourceManifestEntry",
]

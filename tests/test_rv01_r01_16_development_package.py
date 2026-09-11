from __future__ import annotations

import pytest

from sparkbrain.research.rv01_r01_16_development_package import (
    R01_16_REQUIRED_SOURCE_PATHS,
    R0116CollisionRegistry,
    R0116DevelopmentPackagePlan,
    R0116SourceManifest,
    R0116SourceManifestEntry,
)
from sparkbrain.research.rv01_r01_16_identity import (
    R01_16_DEVELOPMENT_SEEDS,
    development_identity_grid,
)

SOURCE_SHA = "a" * 40
FILE_SHA = "b" * 64


def _manifest() -> R0116SourceManifest:
    return R0116SourceManifest(
        source_git_sha=SOURCE_SHA,
        entries=tuple(
            R0116SourceManifestEntry(path=path, sha256=FILE_SHA)
            for path in sorted(R01_16_REQUIRED_SOURCE_PATHS)
        ),
    )


def _registry() -> R0116CollisionRegistry:
    return R0116CollisionRegistry(
        registry_id="rv01-retained-identities-v1",
        source_paths=("docs/research/RV01_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(141500, 141600),
        consumed_or_reserved_world_ids=(
            "r01-15:development:route-a:141500",
            "r01-15:held-out:route-a:141600",
        ),
        authoritative_complete=True,
    )


def test_r01_16_package_plan_is_deterministic_and_execution_disabled() -> None:
    plan = R0116DevelopmentPackagePlan(
        source_manifest=_manifest(),
        collision_registry=_registry(),
    )
    state = plan.state_dict()

    assert state["development_seeds"] == list(R01_16_DEVELOPMENT_SEEDS)
    assert state["overwrite_allowed"] is False
    assert state["retry_same_identity_allowed"] is False
    assert state["construction_only_stage_required"] is True
    assert state["construction_retained_and_reviewed_before_capability_required"] is True
    assert state["construction_and_capability_same_run_allowed"] is False
    assert state["reachability_reconstruction_required_before_capability"] is True
    assert state["construction_integrity_failure_is_terminal"] is True
    assert state["zero_eligible_worlds_is_terminal"] is True
    assert state["capability_output_opened"] is False
    assert state["learner_or_probe_executed"] is False
    assert state["held_out_capability_allowed"] is False
    assert state["formal_execution_allowed"] is False
    assert state["construction_wrapper_bound"] is False
    assert state["capability_wrapper_bound"] is False
    assert state["python_runtime_bound"] is False
    assert plan.run_id == plan.run_id
    assert plan.package_plan_sha256 == plan.package_plan_sha256
    assert plan.output_relpath.startswith("artifacts/rv01/r01-16/development/")


def test_r01_16_source_manifest_requires_every_boundary_critical_path() -> None:
    missing = next(iter(R01_16_REQUIRED_SOURCE_PATHS))
    manifest = R0116SourceManifest(
        source_git_sha=SOURCE_SHA,
        entries=tuple(
            R0116SourceManifestEntry(path=path, sha256=FILE_SHA)
            for path in sorted(R01_16_REQUIRED_SOURCE_PATHS - {missing})
        ),
    )

    with pytest.raises(ValueError, match="missing required paths"):
        manifest.validate()


def test_r01_16_manifest_rejects_duplicate_or_unsafe_paths() -> None:
    required = sorted(R01_16_REQUIRED_SOURCE_PATHS)
    duplicate_entries = [
        R0116SourceManifestEntry(path=path, sha256=FILE_SHA) for path in required
    ]
    duplicate_entries.append(duplicate_entries[0])
    with pytest.raises(ValueError, match="paths must be unique"):
        R0116SourceManifest(
            source_git_sha=SOURCE_SHA,
            entries=tuple(duplicate_entries),
        ).validate()

    with pytest.raises(ValueError, match="normalized repository-relative"):
        R0116SourceManifestEntry(path="../escape.py", sha256=FILE_SHA).validate()


def test_r01_16_collision_registry_requires_complete_retained_identity_input() -> None:
    incomplete = R0116CollisionRegistry(
        registry_id="rv01-retained-identities-v1",
        source_paths=("docs/research/RV01_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(141500,),
        consumed_or_reserved_world_ids=("r01-15:development:route-a:141500",),
        authoritative_complete=False,
    )
    with pytest.raises(ValueError, match="authoritative and complete"):
        incomplete.validate()


def test_r01_16_collision_registry_rejects_seed_or_world_collisions() -> None:
    seed_collision = R0116CollisionRegistry(
        registry_id="rv01-retained-identities-v1",
        source_paths=("docs/research/RV01_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(R01_16_DEVELOPMENT_SEEDS[0],),
        consumed_or_reserved_world_ids=("r01-15:development:route-a:141500",),
        authoritative_complete=True,
    )
    with pytest.raises(ValueError, match="development seed collision"):
        seed_collision.validate()

    world_collision = R0116CollisionRegistry(
        registry_id="rv01-retained-identities-v1",
        source_paths=("docs/research/RV01_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(141500,),
        consumed_or_reserved_world_ids=(development_identity_grid()[0].world_id,),
        authoritative_complete=True,
    )
    with pytest.raises(ValueError, match="development world collision"):
        world_collision.validate()


def test_r01_16_collision_registry_rejects_ambiguous_seed_types() -> None:
    ambiguous = R0116CollisionRegistry(
        registry_id="rv01-retained-identities-v1",
        source_paths=("docs/research/RV01_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(141500.0,),  # type: ignore[arg-type]
        consumed_or_reserved_world_ids=("r01-15:development:route-a:141500",),
        authoritative_complete=True,
    )
    with pytest.raises(TypeError, match="exact non-boolean ints"):
        ambiguous.validate()

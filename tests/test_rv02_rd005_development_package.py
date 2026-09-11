from __future__ import annotations

import pytest

from sparkbrain.research.rv02_rd005_development_package import (
    RD005CollisionRegistry,
    RD005DevelopmentPackagePlan,
    RD005SourceManifest,
    RD005SourceManifestEntry,
    RD005_REQUIRED_SOURCE_PATHS,
)

SOURCE_SHA = "a" * 40
FILE_SHA = "b" * 64


def _manifest() -> RD005SourceManifest:
    return RD005SourceManifest(
        source_git_sha=SOURCE_SHA,
        entries=tuple(
            RD005SourceManifestEntry(path=path, sha256=FILE_SHA)
            for path in sorted(RD005_REQUIRED_SOURCE_PATHS)
        ),
    )


def _registry() -> RD005CollisionRegistry:
    return RD005CollisionRegistry(
        registry_id="rv02-retained-identities-v1",
        source_paths=("docs/research/RV02_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(92003, 92004),
        consumed_or_reserved_world_ids=(
            "rv02:rd003:92003:world-0",
            "rv02:rd004:92004:world-0",
        ),
        authoritative_complete=True,
    )


def test_rd005_package_plan_is_deterministic_and_execution_disabled() -> None:
    plan = RD005DevelopmentPackagePlan(
        source_manifest=_manifest(),
        collision_registry=_registry(),
    )
    state = plan.state_dict()

    assert state["fresh_seed"] == 92505
    assert state["overwrite_allowed"] is False
    assert state["retry_same_identity_allowed"] is False
    assert state["d1_construction_only_stage_required"] is True
    assert state["d1_retained_and_reviewed_before_capability_required"] is True
    assert state["construction_and_capability_same_run_allowed"] is False
    assert state["construction_verifier_required_before_capability"] is True
    assert state["construction_integrity_failure_is_terminal"] is True
    assert state["zero_ready_cells_is_terminal"] is True
    assert state["capability_output_opened"] is False
    assert state["learner_or_probe_executed"] is False
    assert state["held_out_capability_allowed"] is False
    assert state["formal_execution_allowed"] is False
    assert state["construction_wrapper_bound"] is False
    assert state["capability_wrapper_bound"] is False
    assert state["python_runtime_bound"] is False
    assert plan.run_id == plan.run_id
    assert plan.package_plan_sha256 == plan.package_plan_sha256
    assert plan.output_relpath.startswith("artifacts/rv02/rd005/development/")


def test_rd005_source_manifest_requires_every_boundary_critical_path() -> None:
    missing = next(iter(RD005_REQUIRED_SOURCE_PATHS))
    manifest = RD005SourceManifest(
        source_git_sha=SOURCE_SHA,
        entries=tuple(
            RD005SourceManifestEntry(path=path, sha256=FILE_SHA)
            for path in sorted(RD005_REQUIRED_SOURCE_PATHS - {missing})
        ),
    )

    with pytest.raises(ValueError, match="missing required paths"):
        manifest.validate()


def test_rd005_manifest_rejects_duplicate_or_unsafe_paths() -> None:
    required = sorted(RD005_REQUIRED_SOURCE_PATHS)
    duplicate_entries = [
        RD005SourceManifestEntry(path=path, sha256=FILE_SHA) for path in required
    ]
    duplicate_entries.append(duplicate_entries[0])
    with pytest.raises(ValueError, match="paths must be unique"):
        RD005SourceManifest(
            source_git_sha=SOURCE_SHA,
            entries=tuple(duplicate_entries),
        ).validate()

    with pytest.raises(ValueError, match="normalized repository-relative"):
        RD005SourceManifestEntry(path="../escape.py", sha256=FILE_SHA).validate()


def test_rd005_collision_registry_requires_complete_retained_identity_input() -> None:
    incomplete = RD005CollisionRegistry(
        registry_id="rv02-retained-identities-v1",
        source_paths=("docs/research/RV02_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(92003,),
        consumed_or_reserved_world_ids=("rv02:rd003:92003:world-0",),
        authoritative_complete=False,
    )
    with pytest.raises(ValueError, match="authoritative and complete"):
        incomplete.validate()


def test_rd005_collision_registry_rejects_fresh_seed_and_ambiguous_seed_types() -> None:
    colliding = RD005CollisionRegistry(
        registry_id="rv02-retained-identities-v1",
        source_paths=("docs/research/RV02_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(92505,),
        consumed_or_reserved_world_ids=("rv02:old:92004:world-0",),
        authoritative_complete=True,
    )
    with pytest.raises(ValueError, match="fresh seed 92505 collides"):
        colliding.validate()

    ambiguous = RD005CollisionRegistry(
        registry_id="rv02-retained-identities-v1",
        source_paths=("docs/research/RV02_RETAINED_IDENTITY_REGISTRY.json",),
        consumed_or_reserved_seed_ids=(92003.0,),  # type: ignore[arg-type]
        consumed_or_reserved_world_ids=("rv02:rd003:92003:world-0",),
        authoritative_complete=True,
    )
    with pytest.raises(TypeError, match="exact non-boolean ints"):
        ambiguous.validate()

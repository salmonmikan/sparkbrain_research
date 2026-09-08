from __future__ import annotations

import pytest

from sparkbrain.comparison.cx01.candidate import (
    CandidatePurpose,
    CandidateSpec,
    REJECTED_PREFORMAL_SEEDS,
    build_candidate_grid,
    candidate_structure_audit,
)
from sparkbrain.comparison.cx01.formal_worlds import (
    build_formal_world,
    development_structure_signatures,
    world_structure_signature,
)
from sparkbrain.comparison.cx01.worlds import (
    CX01Family,
    development_grid_hash,
)


EXPECTED_DEVELOPMENT_GRID_HASH = (
    "d93b362ce672fffd233973b8f27521f9d6a5fbdf4f3d4cba9369495635a33c9f"
)


def _fixture() -> CandidateSpec:
    return CandidateSpec(
        generation_id="cx01-fixture-structural-heldout-v2",
        seeds=tuple(range(5000, 5010)),
        purpose=CandidatePurpose.STRUCTURE_FIXTURE,
    )


def test_development_world_grid_is_byte_semantically_unchanged() -> None:
    assert development_grid_hash() == EXPECTED_DEVELOPMENT_GRID_HASH


def test_candidate_grid_is_structurally_disjoint_from_development() -> None:
    candidate = _fixture()
    worlds = build_candidate_grid(candidate)
    audit = candidate_structure_audit(candidate)

    assert len(worlds) == len(CX01Family) * len(candidate.seeds)
    assert audit["world_count"] == len(worlds)
    for family in CX01Family:
        row = audit["family_rows"][family.value]
        assert row["development_overlap_count"] == 0
        assert row["unique_structure_count"] >= 5


def test_formal_structure_signature_ignores_anonymous_token_identity() -> None:
    development = development_structure_signatures()
    for family in CX01Family:
        world = build_formal_world("cx01-fixture-direct-v2", family, 5300)
        assert world_structure_signature(world) not in development[family]


def test_timing_holdout_changes_topology_and_preserves_timing_only_alias() -> None:
    world = build_formal_world("cx01-fixture-direct-v2", CX01Family.TIMING, 5301)
    left, right = world.training
    left_probe, right_probe = world.probes

    assert len(left.tokens) == 5
    assert left.tokens[:-1] == right.tokens[:-1]
    assert left.tokens[-1] != right.tokens[-1]
    assert left_probe.prefix == right_probe.prefix
    assert left_probe.lags_ms != right_probe.lags_ms
    assert sum(left_probe.lags_ms) == sum(right_probe.lags_ms)


def test_branch_holdout_uses_new_prefix_topology_and_nondevelopment_ratio() -> None:
    world = build_formal_world("cx01-fixture-direct-v2", CX01Family.BRANCH, 5302)
    probe = world.probes[0]
    counts = tuple(row.exposures for row in world.training)

    assert len(probe.prefix) == 4
    assert counts != (6, 5, 4)
    assert len(set(counts)) == 3


def test_cycle_holdout_changes_contingency_schedule_shape() -> None:
    world = build_formal_world("cx01-fixture-direct-v2", CX01Family.CYCLE, 5303)
    assert len(world.cycle_phases) == 7
    assert tuple(phase.exposures for phase in world.cycle_phases) != (2, 3, 2, 3, 2, 3)


def test_rejected_candidate001_seed_band_cannot_be_reused() -> None:
    seeds = tuple(sorted(REJECTED_PREFORMAL_SEEDS))
    with pytest.raises(ValueError, match="rejected pre-start seed band"):
        CandidateSpec(
            generation_id="cx01-candidate-002",
            seeds=seeds,
            purpose=CandidatePurpose.FORMAL,
        ).validate()


def test_rejected_candidate001_generation_id_cannot_be_reused() -> None:
    with pytest.raises(ValueError, match="already exposed pre-start"):
        CandidateSpec(
            generation_id="cx01-candidate-001",
            seeds=tuple(range(700000, 700010)),
            purpose=CandidatePurpose.FORMAL,
        ).validate()

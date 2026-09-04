from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_confirmatory import EvidenceDomain
from sparkbrain.evaluation.v06_confirmatory_primary_adapter import (
    QUALIFICATION_FAMILIES,
    QUALIFICATION_SEEDS,
    PrimaryQualificationGrid,
    evaluate_primary_world,
    run_primary_qualification_grid,
    world_parameters,
)


@pytest.fixture(scope="module")
def grid() -> PrimaryQualificationGrid:
    return run_primary_qualification_grid()


def test_world_parameters_apply_real_structural_perturbations() -> None:
    identifier_rows = tuple(
        world_parameters("identifier-permutation", seed)
        for seed in QUALIFICATION_SEEDS
    )
    temporal_rows = tuple(
        world_parameters("temporal-perturbation", seed)
        for seed in QUALIFICATION_SEEDS
    )
    gain_rows = tuple(
        world_parameters("field-gain-perturbation", seed)
        for seed in QUALIFICATION_SEEDS
    )

    assert len({row.main_path for row in identifier_rows}) == 3
    assert len({row.main_port for row in identifier_rows}) == 3
    assert tuple(row.transition_lag_ms for row in temporal_rows) == (4.0, 5.0, 6.0)
    assert tuple(row.boundary_lag_ms for row in temporal_rows) == (8.0, 10.0, 12.0)
    assert tuple(row.threshold for row in gain_rows) == (0.44, 0.50, 0.56)
    assert all(
        0.5 * row.relation_reentry_gain < row.threshold
        < (7 / 11) * row.relation_reentry_gain
        for row in (*identifier_rows, *temporal_rows, *gain_rows)
    )


@pytest.mark.parametrize("family_id", QUALIFICATION_FAMILIES)
@pytest.mark.parametrize("seed", QUALIFICATION_SEEDS)
def test_every_primary_qualification_world_passes_all_evidence_domains(
    family_id: str,
    seed: int,
) -> None:
    result = evaluate_primary_world(family_id, seed)
    assert result.all_passed is True, result.state_dict()
    assert result.endogenous_origin_passed is True
    assert result.state_dependence_passed is True
    assert result.autonomous_chain_passed is True
    assert result.boundary_effect_passed is True
    assert result.relation_stabilization_passed is True
    assert result.reversal_reacquisition_passed is True
    assert result.relation_reentry_passed is True
    assert result.persistence_locus_passed is True
    assert result.taxonomy_non_interference_passed is True


def test_primary_grid_contains_three_families_three_seeds_and_nine_domains(
    grid: PrimaryQualificationGrid,
) -> None:
    assert grid.complete is True
    assert len(grid.worlds) == 9
    assert grid.passed_world_count == 9
    assert len(grid.records) == 81
    assert {row.family_id for row in grid.worlds} == set(QUALIFICATION_FAMILIES)
    assert {row.seed for row in grid.worlds} == set(QUALIFICATION_SEEDS)
    assert {row.evidence_domain for row in grid.records} == set(EvidenceDomain)
    assert all(row.passed for row in grid.records)


def test_primary_grid_is_deterministic(grid: PrimaryQualificationGrid) -> None:
    replay = run_primary_qualification_grid()
    assert replay == grid


def test_qualification_metrics_preserve_persistence_limitation(
    grid: PrimaryQualificationGrid,
) -> None:
    for world in grid.worlds:
        metrics = dict(world.metrics)
        assert metrics["persistence_local_transplant_count"] == 1.0
        assert metrics["persistence_local_reset_count"] == 0.0
        assert metrics["chain_targeted_impairment"] == 1.0
        assert metrics["chain_matched_impairment"] == 0.0


def test_invalid_family_or_seed_fails_closed() -> None:
    with pytest.raises(ValueError, match="unknown qualification world family"):
        world_parameters("unknown", 0)
    with pytest.raises(ValueError, match="unsupported qualification seed"):
        world_parameters("identifier-permutation", 9)

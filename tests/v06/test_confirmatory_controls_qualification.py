from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_controls import (
    ControlQualificationGrid,
    evaluate_no_endogenous,
    evaluate_random_matched,
    evaluate_readout_only,
    evaluate_shuffled_relation,
    expected_control_domains,
    run_control_qualification_grid,
    run_no_endogenous,
    run_random_matched,
    run_readout_only,
    run_shuffled_relation,
)
from sparkbrain.evaluation.v06_confirmatory_primary_adapter import (
    QUALIFICATION_FAMILIES,
    QUALIFICATION_SEEDS,
)


@pytest.fixture(scope="module")
def grid() -> ControlQualificationGrid:
    return run_control_qualification_grid()


def test_control_grid_has_four_conditions_three_families_three_seeds(
    grid: ControlQualificationGrid,
) -> None:
    assert grid.complete is True
    assert len(grid.worlds) == 4 * 3 * 3
    assert len(grid.records) == 4 * 3 * 3 * 9
    assert {row.family_id for row in grid.worlds} == set(QUALIFICATION_FAMILIES)
    assert {row.seed for row in grid.worlds} == set(QUALIFICATION_SEEDS)
    assert {row.condition for row in grid.worlds} == {
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }
    assert {row.evidence_domain for row in grid.records} == set(EvidenceDomain)


def test_each_control_world_satisfies_its_engineering_contract(
    grid: ControlQualificationGrid,
) -> None:
    for world in grid.worlds:
        metrics = dict(world.metrics)
        assert metrics["control_contract_passed"] == 1.0, world.state_dict()
        assert world.passed_domain_set == expected_control_domains(world.condition)
        assert metrics["taxonomy_hash_match"] == 1.0
        assert metrics["self_confirmation_violations"] == 0.0


def test_no_endogenous_control_blocks_all_internal_field_sparks() -> None:
    result = evaluate_no_endogenous("identifier-permutation", 0)
    metrics = dict(result.metrics)
    assert metrics["generated_spark_count"] == 0.0
    assert metrics["suppressed_reinjection_count"] >= 3.0
    assert result.passed_domain_set == {
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE
    }


def test_readout_only_control_keeps_proposals_out_of_the_field() -> None:
    result = evaluate_readout_only("temporal-perturbation", 1)
    metrics = dict(result.metrics)
    assert metrics["main_proposal_count"] == 1.0
    assert metrics["alternate_proposal_count"] == 1.0
    assert metrics["later_field_spark_count"] == 0.0
    assert result.passed_domain_set == {
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE
    }


def test_random_control_matches_count_time_current_and_energy_without_lineage() -> None:
    result = evaluate_random_matched("field-gain-perturbation", 2)
    metrics = dict(result.metrics)
    assert metrics["matched_event_count"] == 3.0
    assert metrics["matched_total_energy"] > 0.0
    assert metrics["random_field_spark_count"] == 3.0
    assert metrics["random_sequential_parent_count"] == 0.0
    assert result.passed_domain_set == {
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE
    }


def test_shuffled_relation_preserves_early_dynamics_but_breaks_reentry() -> None:
    result = evaluate_shuffled_relation("identifier-permutation", 2)
    assert result.passed_domain_set == {
        EvidenceDomain.ENDOGENOUS_ORIGIN,
        EvidenceDomain.STATE_DEPENDENCE,
        EvidenceDomain.AUTONOMOUS_CHAIN,
        EvidenceDomain.BOUNDARY_EFFECT,
        EvidenceDomain.RELATION_STABILIZATION,
        EvidenceDomain.REVERSAL_REACQUISITION,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE,
    }
    metrics = dict(result.metrics)
    assert metrics["relation_reentry_false_positive"] == 0.0
    assert metrics["acquired_wrong_target_count"] == 1.0
    assert metrics["reversed_wrong_target_count"] == 1.0
    assert metrics["returned_wrong_target_count"] == 1.0


@pytest.mark.parametrize(
    ("runner", "condition"),
    (
        (run_no_endogenous, ConfirmatoryCondition.NO_ENDOGENOUS),
        (run_random_matched, ConfirmatoryCondition.RANDOM_MATCHED),
        (run_readout_only, ConfirmatoryCondition.READOUT_ONLY),
        (run_shuffled_relation, ConfirmatoryCondition.SHUFFLED_RELATION),
    ),
)
def test_each_public_adapter_emits_all_nine_domains(runner, condition) -> None:
    records = runner("identifier-permutation", 0)
    assert len(records) == 9
    assert {row.condition for row in records} == {condition}
    assert {row.evidence_domain for row in records} == set(EvidenceDomain)


def test_control_grid_is_deterministic(grid: ControlQualificationGrid) -> None:
    assert run_control_qualification_grid() == grid

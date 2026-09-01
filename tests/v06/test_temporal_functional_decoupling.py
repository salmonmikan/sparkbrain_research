from __future__ import annotations

import math

import pytest

from sparkbrain.evaluation.v061_temporal_functional_decoupling import (
    BranchObservation,
    RelationLinkObservation,
    canonical_relation_counterfactuals,
    canonical_temporal_counterfactuals,
    diagnose_branch_competition,
    diagnose_relation_expression,
    g1_confidence,
    relation_reliability,
)


def test_g1_score_is_frequency_times_temporal_stability() -> None:
    value = g1_confidence(
        exposure_count=5,
        total_exposure_count=9,
        lag_variance_ms2=4.0,
        variance_scale_ms2=4.0,
    )
    assert math.isclose(value, 5.0 / 18.0)


def test_lag_variance_can_override_exposure_and_world_consistency() -> None:
    diagnosis = canonical_temporal_counterfactuals()["decoupled"]
    assert diagnosis.selected_by_exposure == "main"
    assert diagnosis.selected_by_world_consistency == "main"
    assert diagnosis.selected_by_g1 == "alternate"
    assert diagnosis.g1_matches_exposure is False
    assert diagnosis.g1_matches_world_consistency is False
    assert diagnosis.temporal_functional_decoupling is True
    assert diagnosis.selection_margin > 0.0


def test_selection_returns_to_main_when_temporal_variance_is_equalized() -> None:
    diagnosis = canonical_temporal_counterfactuals()["equal_variance"]
    assert diagnosis.selected_by_g1 == "main"
    assert diagnosis.selected_by_exposure == "main"
    assert diagnosis.selected_by_world_consistency == "main"
    assert diagnosis.temporal_functional_decoupling is False


def test_swapping_lag_structure_flips_selection_without_changing_function() -> None:
    cases = canonical_temporal_counterfactuals()
    aligned = cases["aligned"]
    decoupled = cases["decoupled"]
    assert aligned.selected_by_world_consistency == "main"
    assert decoupled.selected_by_world_consistency == "main"
    assert aligned.selected_by_g1 == "main"
    assert decoupled.selected_by_g1 == "alternate"


def test_branch_diagnosis_rejects_invalid_observation_contracts() -> None:
    with pytest.raises(ValueError, match="two competing"):
        diagnose_branch_competition(
            (BranchObservation("main", 1, (5.0,), 1.0),),
            variance_scale_ms2=4.0,
        )
    with pytest.raises(ValueError, match="unique"):
        diagnose_branch_competition(
            (
                BranchObservation("same", 1, (5.0,), 1.0),
                BranchObservation("same", 1, (6.0,), 0.0),
            ),
            variance_scale_ms2=4.0,
        )


def test_relation_reliability_uses_explicit_prior_and_counts() -> None:
    assert math.isclose(
        relation_reliability(consistent_count=4, inconsistent_count=4),
        0.5,
    )
    assert math.isclose(
        relation_reliability(consistent_count=5, inconsistent_count=2),
        2.0 / 3.0,
    )


def test_correct_relation_can_be_stored_but_not_expressed() -> None:
    diagnosis = canonical_relation_counterfactuals()["correct_but_abstains"]
    assert diagnosis.dominant_target == "current"
    assert diagnosis.storage_matches_world is True
    assert diagnosis.expressed_targets == ()
    assert diagnosis.expression_abstention is True
    assert diagnosis.storage_failure is False


def test_multiple_reliable_links_can_cross_field_threshold_together() -> None:
    diagnosis = canonical_relation_counterfactuals()["multi_link_superposition"]
    assert diagnosis.storage_matches_world is True
    assert set(diagnosis.expressed_targets) == {"current", "old"}
    assert diagnosis.multi_link_superposition is True
    assert diagnosis.exact_expression_matches_world is False


def test_hysteresis_is_a_storage_failure_not_only_an_expression_failure() -> None:
    diagnosis = canonical_relation_counterfactuals()["hysteresis"]
    assert diagnosis.dominant_target == "old"
    assert diagnosis.storage_matches_world is False
    assert diagnosis.storage_failure is True
    assert diagnosis.expressed_targets == ("old",)


def test_expression_surface_can_be_evaluated_without_runtime_taxonomy() -> None:
    diagnosis = diagnose_relation_expression(
        (
            RelationLinkObservation("unit:8", 3, 0),
            RelationLinkObservation("unit:9", 1, 2),
        ),
        expected_world_target="unit:8",
        field_threshold=0.5,
        relation_reentry_gain=0.5 / 0.60,
    )
    assert diagnosis.dominant_target == "unit:8"
    assert diagnosis.expressed_targets == ("unit:8",)
    lowered = str(diagnosis.state_dict()).lower()
    for forbidden in (
        "reward",
        "correct_action",
        "meaning_state",
        "functional_role",
        "assembly_id",
    ):
        assert forbidden not in lowered

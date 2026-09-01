from __future__ import annotations

from sparkbrain.evaluation.v061_temporal_functional_discriminators import (
    build_discriminator_report,
    run_ambiguity_experiment,
    run_consequence_permutation,
    run_lag_assignment_permutation,
    run_storage_expression_cross,
)


def test_lag_assignment_flips_selection_with_total_evidence_preserved() -> None:
    result = run_lag_assignment_permutation()
    assert result.total_lag_multiset_a == result.total_lag_multiset_b
    assert result.total_evidence_preserved is True
    assert result.world_consistency_winner_preserved is True
    assert result.assignment_a.selected_by_g1 == "alternate"
    assert result.assignment_b.selected_by_g1 == "main"
    assert result.g1_selection_flipped is True


def test_world_consequence_permutation_does_not_change_current_g1_selection() -> None:
    result = run_consequence_permutation()
    assert result.local_transition_evidence_identical is True
    assert result.original.selected_by_world_consistency == "main"
    assert result.permuted.selected_by_world_consistency == "alternate"
    assert result.original.selected_by_g1 == "alternate"
    assert result.permuted.selected_by_g1 == "alternate"
    assert result.g1_selection_unchanged is True
    assert result.world_consistency_winner_changed is True
    assert result.missing_world_to_transition_feedback is True


def test_relation_storage_can_remain_fixed_while_field_expression_changes() -> None:
    result = run_storage_expression_cross()
    assert result.stored_state_identical is True
    assert result.dominant_relation_identical is True
    assert result.high_threshold.storage_matches_world is True
    assert result.high_threshold.expression_abstention is True
    assert result.low_threshold.exact_expression_matches_world is True
    assert result.expression_changed is True
    assert result.expression_bottleneck_demonstrated is True


def test_equal_local_evidence_preserves_a_real_tie_before_evaluator_ordering() -> None:
    result = run_ambiguity_experiment()
    assert result.co_maximal_branches == ("branch-a", "branch-b")
    assert result.exact_confidence_tie is True
    assert result.diagnosis.selected_by_g1 == "branch-a"
    assert result.evaluator_singleton_is_only_tie_break is True


def test_discriminator_report_supports_only_mechanistic_inferences() -> None:
    report = build_discriminator_report()
    assert report["candidate_reexecuted"] is False
    assert report["runtime_modified"] is False
    assert all(report["supported_diagnostic_inferences"].values())
    lowered = str(report).lower()
    for forbidden in (
        "correct_action",
        "reward_value",
        "meaning_state",
        "functional_role",
        "assembly_id",
    ):
        assert forbidden not in lowered

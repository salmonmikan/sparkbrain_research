from __future__ import annotations

from sparkbrain.evaluation.v061_comparator_contrast import (
    run_comparator_contrast,
)
from sparkbrain.evaluation.v061_failure_locus_diagnostics import (
    run_failure_locus_suite,
)


def test_lag_trajectory_class_moves_with_g1_into_a_fresh_field() -> None:
    suite = run_failure_locus_suite()
    rows = {row["family_id"]: row for row in suite["transitions"]}

    alternate = rows["diagnostic-lag-resonant-shared"]
    assert alternate["baseline_units"] == (4, 5, 6)
    assert alternate["expectation_transplant_units"] == (4, 5, 6)
    assert alternate["baseline_trajectory_class"] == "alternate-only-substitution"
    assert alternate["failure_transfers_with_g1"] is True

    superposed = rows["diagnostic-lag-main-variance-2"]
    assert superposed["baseline_units"] == (1, 4, 2, 5, 3, 6)
    assert superposed["expectation_transplant_units"] == (1, 4, 2, 5, 3, 6)
    assert superposed["baseline_trajectory_class"] == (
        "dual-trajectory-superposition"
    )
    assert superposed["failure_transfers_with_g1"] is True


def test_g1_reset_and_field_only_transfer_do_not_recreate_trajectory() -> None:
    suite = run_failure_locus_suite()
    assert suite["transition_world_count"] == 3
    assert suite["transition_failure_transfers_with_g1_count"] == 3
    assert suite["transition_g1_reset_removes_expression_count"] == 3
    assert suite["transition_field_state_alone_transfer_count"] == 0
    for row in suite["transitions"]:
        assert row["expectation_reset_units"] == ()
        assert row["field_state_only_units"] == ()
        assert row["fresh_field_state_hash"] == (
            row["transplanted_fresh_field_state_hash"]
        )


def test_relation_failure_replays_from_consistency_state_on_fresh_field() -> None:
    suite = run_failure_locus_suite()
    assert suite["relation_world_count"] == 3
    assert suite["relation_failure_replays_in_fresh_field_count"] == 3
    assert suite["relation_reset_removes_expression_count"] == 3
    rows = {row["factor_value"]: row for row in suite["relations"]}

    abstention = rows["expression-abstention"]
    assert abstention["source_failure_stage"] == "relation-to-field-expression"
    assert abstention["source_expression_status"] == "abstention"
    assert abstention["source_output_units"] == ()

    hysteresis = rows["hysteresis-short-return"]
    assert hysteresis["source_failure_stage"] == "relation-storage"
    assert hysteresis["source_storage_status"] == "wrong-dominant"

    superposition = rows["parallel-link-superposition"]
    assert superposition["source_failure_stage"] == (
        "relation-to-field-expression"
    )
    assert superposition["source_expression_status"] == (
        "superposition-including-expected"
    )
    assert superposition["source_output_units"] == (14, 15)

    for row in suite["relations"]:
        assert row["source_output_units"] == row[
            "fresh_field_replay_output_units"
        ]
        assert row["reset_consistency_output_units"] == ()
        assert row["prior_field_state_required"] is False


def test_comparators_quotient_lag_order_while_primary_retains_it() -> None:
    contrast = run_comparator_contrast()
    assert contrast["candidate_003_executions"] == 0
    assert contrast["same_paths"] is True
    assert contrast["same_exposure_counts"] is True
    assert contrast["same_lag_profile_multiset"] is True
    assert contrast["lag_profile_order_equal"] is False
    assert contrast["all_comparators_quotient_lag_order"] is True
    assert contrast["primary_retains_lag_order_in_state_and_expression"] is True

    primary = contrast["primary"]
    assert primary["learned_state_equal"] is False
    assert primary["trajectory_equal"] is False
    assert primary["world_a_trajectory_class"] == "alternate-only-substitution"
    assert primary["world_b_trajectory_class"] == "main-only-exact"

    assert len(contrast["comparators"]) == 3
    for row in contrast["comparators"]:
        assert row["learned_state_equal"] is True
        assert row["output_equal"] is True
        assert row["lag_profile_values_represented_in_learned_state"] is False
        assert "time-abstracted-sequence" in row["privileged_structure"]


def test_locus_and_comparator_diagnostics_are_deterministic() -> None:
    assert run_failure_locus_suite() == run_failure_locus_suite()
    assert run_comparator_contrast() == run_comparator_contrast()

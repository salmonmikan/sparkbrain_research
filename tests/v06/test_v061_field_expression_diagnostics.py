from __future__ import annotations

from sparkbrain.evaluation.v061_field_expression_diagnostics import (
    run_field_expression_diagnosis,
)


def _transition_rows(result):
    return {row["condition"]: row for row in result["transition_conditions"]}


def _relation_rows(result):
    return {row["condition"]: row for row in result["relation_conditions"]}


def test_fixed_g1_proposals_survive_all_field_manipulations() -> None:
    result = run_field_expression_diagnosis()
    rows = _transition_rows(result)
    signatures = {
        (
            tuple(row["proposal_targets"]),
            tuple(tuple(item) for item in row["proposal_confidences"]),
        )
        for row in rows.values()
    }
    assert len(signatures) == 1
    assert result["assessment"][
        "proposal_identity_invariant_across_field_conditions"
    ] is True


def test_field_threshold_maps_one_g1_state_to_three_expression_regimes() -> None:
    result = run_field_expression_diagnosis()
    rows = _transition_rows(result)

    assert rows["low-threshold"]["trajectory_class"] == (
        "dual-trajectory-superposition"
    )
    assert rows["ordinary-field"]["trajectory_class"] == (
        "alternate-only-substitution"
    )
    assert rows["high-threshold"]["trajectory_class"] == (
        "no-endogenous-trajectory"
    )
    assert result["assessment"]["threshold_changes_trajectory_expression"] is True


def test_readout_is_not_an_actual_endogenous_spark() -> None:
    result = run_field_expression_diagnosis()
    row = _transition_rows(result)["readout-only"]
    assert row["proposal_targets"]
    assert row["generated_units"] == ()
    assert result["assessment"][
        "readout_without_reinjection_has_no_endogenous_spark"
    ] is True


def test_short_term_field_state_changes_expression_without_relearning_g1() -> None:
    result = run_field_expression_diagnosis()
    rows = _transition_rows(result)
    transition_world = result["transition_world"]

    residual = rows["residual-main-primer"]
    assert residual["primer_target"] == transition_world["main_path"][1]
    assert transition_world["main_path"][1] in residual["generated_units"]

    refractory = rows["refractory-alternate-primer"]
    assert refractory["primer_target"] == transition_world["alternate_path"][1]
    assert transition_world["alternate_path"][1] not in refractory[
        "generated_units"
    ]
    assert refractory["external_primer_spike_count"] == 1


def test_fixed_consistency_state_is_filtered_by_field_state() -> None:
    result = run_field_expression_diagnosis()
    rows = _relation_rows(result)
    target = result["relation_world"]["old_target"]

    assert rows["ordinary-field"]["endogenous_output_units"] == (target,)
    assert rows["high-threshold"]["endogenous_output_units"] == ()
    assert rows["refractory-target-primer"]["endogenous_output_units"] == ()
    assert rows["refractory-target-primer"]["external_primer_spike_count"] == 1
    assert all(
        row["consistency_state_hash_before"]
        == row["consistency_state_hash_after"]
        for row in rows.values()
    )


def test_field_role_is_expression_not_current_learned_organization() -> None:
    result = run_field_expression_diagnosis()
    assessment = result["assessment"]

    assert result["candidate_003_executions"] == 0
    assert assessment["field_active_expression_substrate_supported"] is True
    assert assessment["learned_transition_organization_moves_with_g1"] is True
    assert assessment[
        "learned_relation_organization_moves_with_consistency"
    ] is True
    assert assessment["field_learned_organizer_supported"] is False
    assert assessment["distributed_field_memory_supported"] is False


def test_field_expression_diagnosis_is_deterministic() -> None:
    assert run_field_expression_diagnosis() == run_field_expression_diagnosis()

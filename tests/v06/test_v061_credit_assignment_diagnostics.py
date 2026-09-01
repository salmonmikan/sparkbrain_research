from __future__ import annotations

from sparkbrain.evaluation.v061_credit_assignment_diagnostics import (
    run_credit_assignment_diagnosis,
)


def test_runtime_lineage_is_reconstructible_through_world_return() -> None:
    result = run_credit_assignment_diagnosis()
    assessment = result["assessment"]
    lineage = result["runtime_lineage"]

    assert result["candidate_003_executions"] == 0
    assert lineage["terminal_proposal_ids"]
    assert lineage["proposal_ancestry"]
    assert lineage["local_path_ids"]
    assert assessment["proposal_to_spark_lineage_present"] is True
    assert assessment["spark_to_boundary_proposal_ids_present"] is True
    assert assessment["boundary_to_world_parent_id_present"] is True
    assert assessment[
        "world_to_consistency_resolution_ids_present"
    ] is True
    assert assessment["complete_runtime_lineage_reconstructible"] is True
    assert assessment[
        "anonymous_credit_information_available_transiently"
    ] is True


def test_persistent_consistency_collapses_path_identity() -> None:
    result = run_credit_assignment_diagnosis()
    assessment = result["assessment"]
    persistence = result["persistence_boundary"]

    assert persistence["learned_consistency"]["links"]
    assert assessment["world_pulse_carries_local_path_ids_directly"] is False
    assert assessment["learned_consistency_retains_proposal_ids"] is False
    assert assessment["learned_consistency_retains_local_path_ids"] is False


def test_g2_eligibility_exists_but_world_consequence_does_not_commit_it() -> None:
    result = run_credit_assignment_diagnosis()
    assessment = result["assessment"]
    persistence = result["persistence_boundary"]

    assert persistence["terminal_eligibilities"]
    assert all(
        row["committed"] is False for row in persistence["terminal_eligibilities"]
    )
    assert persistence["g2_path_state"] == {}
    assert assessment["g2_eligibility_exists_for_terminal_path"] is True
    assert assessment[
        "g2_eligibility_committed_by_world_consequence"
    ] is False
    assert assessment[
        "g2_path_adaptation_updated_by_world_consequence"
    ] is False
    assert assessment["automatic_world_to_g2_resolution_present"] is False


def test_direct_g2_resolution_rejects_downstream_world_target_as_local_match() -> None:
    result = run_credit_assignment_diagnosis()
    probe = result["direct_g2_probe"]

    assert probe["proposal_target"] != probe["external_target"]
    assert probe["matched"] is False
    assert probe["confidence_after"] < probe["confidence_before"]
    assert result["assessment"][
        "direct_g2_resolution_treats_world_consequence_as_match"
    ] is False


def test_anonymous_credit_loop_is_open_not_absent() -> None:
    assessment = run_credit_assignment_diagnosis()["assessment"]

    assert assessment[
        "anonymous_credit_information_available_transiently"
    ] is True
    assert assessment["anonymous_credit_loop_closed_in_learning"] is False


def test_credit_assignment_diagnosis_is_deterministic() -> None:
    assert run_credit_assignment_diagnosis() == run_credit_assignment_diagnosis()

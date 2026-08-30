from __future__ import annotations

from sparkbrain.evaluation.v06_chain_probe import (
    build_runtime,
    pulse,
    run_canonical_chain_suite,
    run_condition,
)
from sparkbrain.v06.endogenous_chain import EndogenousChainIntervention


def test_sham_condition_builds_three_step_internal_chain_in_silence() -> None:
    result = run_condition("sham")
    assert result.main_units == (1, 2, 3)
    assert result.main_times_ms == (155.0, 160.0, 165.0)
    assert result.control_units == (5, 6, 7)
    assert result.external_observation_count == 2
    assert result.committed_positive_updates == 0


def test_each_downstream_proposal_is_created_by_a_prior_endogenous_spark() -> None:
    runtime = build_runtime()
    runtime.present_external(pulse("main-cue", 100.0, 0))
    runtime.advance_silence(120.0)
    rows = runtime.proposal_records
    assert [row.generation_depth for row in rows] == [1, 2, 3]
    assert [row.source_origin for row in rows] == [
        "external",
        "endogenous-unconfirmed",
        "endogenous-unconfirmed",
    ]
    assert [row.source_time_ms for row in rows] == [100.0, 105.0, 110.0]
    assert [row.predicted_arrival_ms for row in rows] == [105.0, 110.0, 115.0]
    assert rows[0].parent_proposal_ids == ()
    assert rows[1].parent_proposal_ids == (rows[0].proposal_id,)
    assert rows[2].parent_proposal_ids == (rows[1].proposal_id,)
    assert runtime.ledger.external_observation_count == 1
    assert runtime.ledger.committed_positive_updates == 0


def test_targeted_expansion_suppression_preserves_root_but_removes_downstream() -> None:
    result = run_condition(
        "targeted",
        EndogenousChainIntervention(suppress_expansion_unit_ids=(1,)),
    )
    assert result.main_units == (1,)
    assert result.main_downstream_count == 0
    assert result.main_root_present is True
    assert result.intervention_count == 1
    assert result.suppressed_reasons == ("suppressed_expansion_unit",)


def test_matched_random_active_path_does_not_damage_main_chain() -> None:
    result = run_condition(
        "matched-random",
        EndogenousChainIntervention(suppress_expansion_unit_ids=(5,)),
    )
    assert result.control_units == (5,)
    assert result.main_units == (1, 2, 3)
    assert result.intervention_count == 1


def test_canonical_intervention_suite_has_selective_downstream_effect() -> None:
    suite = run_canonical_chain_suite()
    assessment = suite.assessment
    assert assessment.engineering_candidate is True
    assert assessment.sham_main_downstream_count == 2
    assert assessment.targeted_main_downstream_count == 0
    assert assessment.matched_random_main_downstream_count == 2
    assert assessment.targeted_impairment == 1.0
    assert assessment.matched_random_impairment == 0.0
    assert assessment.selective_effect == 1.0
    assert assessment.root_preserved_under_targeted_intervention is True
    assert assessment.no_positive_self_confirmation is True


def test_root_reinjection_suppression_removes_entire_main_chain() -> None:
    suite = run_canonical_chain_suite()
    assert suite.root_reinjection_suppressed.main_units == ()
    assert suite.root_reinjection_suppressed.control_units == (5, 6, 7)
    assert "suppressed_reinjection_path" in (
        suite.root_reinjection_suppressed.suppressed_reasons
    )


def test_downstream_reinjection_suppression_leaves_only_main_root() -> None:
    suite = run_canonical_chain_suite()
    result = suite.downstream_reinjection_suppressed
    assert result.main_units == (1,)
    assert result.control_units == (5, 6, 7)
    assert result.intervention_count == 1
    assert result.suppressed_reasons == ("suppressed_reinjection_path",)


def test_runtime_state_is_assembly_free_and_contains_no_semantic_answer() -> None:
    result = run_condition("sham")
    lowered = str(result.runtime_state).lower()
    assert "assembly_id" not in lowered
    assert "motif_id" not in lowered
    assert "missing_target" not in lowered
    assert "correct_action" not in lowered
    assert "outcome_label" not in lowered
    assert "meaning" not in lowered


def test_internal_chain_does_not_create_external_observations_or_positive_updates() -> None:
    runtime = build_runtime()
    runtime.present_external(pulse("cue", 100.0, 0))
    before_external = runtime.ledger.external_observation_count
    before_updates = runtime.ledger.committed_positive_updates
    runtime.advance_silence(120.0)
    assert runtime.ledger.external_observation_count == before_external == 1
    assert runtime.ledger.committed_positive_updates == before_updates == 0
    assert all(
        spark.external_observation_count == 1
        and spark.committed_positive_updates == 0
        for spark in runtime.generated_sparks
    )


def test_drain_events_stops_at_last_actual_event() -> None:
    runtime = build_runtime()
    runtime.present_external(pulse("drain-cue", 100.0, 0))
    generated = runtime.drain_scheduled_events(120.0)
    assert tuple(row.unit_id for row in generated) == (1, 2, 3)
    assert runtime.field.current_time_ms == 115.0

    runtime.advance_silence(120.0)
    assert runtime.field.current_time_ms == 120.0


def test_external_time_reversal_guard_remains_strict() -> None:
    import pytest

    runtime = build_runtime()
    runtime.present_external(pulse("strict-cue", 100.0, 0))
    runtime.advance_silence(120.0)
    with pytest.raises(
        ValueError,
        match="cannot move Field time backwards",
    ):
        runtime.present_external(pulse("past-cue", 119.0, 0))

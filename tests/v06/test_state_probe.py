from __future__ import annotations

from sparkbrain.evaluation.v06_state_probe import (
    canonical_history,
    external,
    run_canonical_state_probe,
    run_state_condition,
)
from sparkbrain.v06.local_expectation import LocalExpectationConfig


def test_canonical_probe_is_deterministic_and_history_dependent() -> None:
    result = run_canonical_state_probe()
    assert result.engineering_candidate is True
    assert result.assessment.candidate is True
    assert result.assessment.deterministic_replay is True
    assert result.assessment.histories_distinct is True
    assert result.assessment.response_changed_with_history is True
    assert result.reference.response.response_trace_hash == (
        result.reference_replay.response.response_trace_hash
    )
    assert result.reference.final_state_hash == result.reference_replay.final_state_hash


def test_same_current_input_produces_different_targets_after_different_histories() -> None:
    result = run_canonical_state_probe()
    assert result.reference.response.current_input_hash == (
        result.alternate_history.response.current_input_hash
    )
    assert result.reference.response.endogenous_targets == ("unit:1",)
    assert result.alternate_history.response.endogenous_targets == ("unit:2",)
    assert result.reference.prior_state_hash != result.alternate_history.prior_state_hash


def test_probe_uses_real_field_reinjection_and_no_reinjection_control() -> None:
    result = run_canonical_state_probe()
    for condition in (result.reference, result.reference_replay, result.alternate_history):
        assert condition.queue_drained is True
        assert condition.no_reinjection_spike_count == 0
        assert condition.reinjection_accepted_count == 1
        assert condition.field_spike_count == 1
        assert condition.reinjection_decisions[0]["accepted"] is True
        assert condition.reinjection_decisions[0]["reason"] == (
            "scheduled_normal_rule_arrival"
        )
        event = condition.endogenous_events[0]
        assert event["origin"] == "endogenous-unconfirmed"
        assert event["parent_event_ids"]
        assert event["parent_event_ids"][0].startswith("endo:g1-")


def test_origin_audits_exclude_copy_echo_queue_and_target_leakage() -> None:
    result = run_canonical_state_probe()
    assert result.all_origin_audits_passed is True
    for condition in (result.reference, result.reference_replay, result.alternate_history):
        assert condition.queue_drained is True
        assert len(condition.origin_audits) == 1
        audit = condition.origin_audits[0]
        assert audit.candidate is True
        assert audit.reason_codes == ()
        assert audit.direct_copy_external_ids == ()
        assert audit.fixed_delay_echo_external_ids == ()
        assert audit.evaluator_target_supplied is False
        assert audit.origin_state_hash == condition.prior_state_hash


def test_no_history_produces_no_endogenous_response() -> None:
    result = run_canonical_state_probe()
    assert result.no_history_event_count == 0


def test_probe_uses_no_assembly_motif_or_answer_fields() -> None:
    state = run_canonical_state_probe().state_dict()
    lowered = str(state).lower()
    assert "assembly_id" not in lowered
    assert "motif_id" not in lowered
    assert "missing_target" not in lowered
    assert "correct_action" not in lowered
    assert "outcome_label" not in lowered


def test_insufficient_history_fails_to_create_a_proposal() -> None:
    current = external("current", 100.0, "unit:0")
    condition = run_state_condition(
        condition_id="insufficient",
        history=(canonical_history("unit:1")[0],),
        current_input=current,
        config=LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=20.0,
        ),
    )
    assert condition.endogenous_events == ()
    assert condition.origin_audits == ()
    assert condition.response.endogenous_targets == ()
    assert condition.reinjection_accepted_count == 0
    assert condition.field_spike_count == 0
    assert condition.no_reinjection_spike_count == 0

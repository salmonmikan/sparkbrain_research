from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_endogenous import (
    EndogenousOriginAuditConfig,
    StateConditionResponse,
    assess_persistent_state_dependence,
    audit_endogenous_origin,
)
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse


def external(
    event_id: str,
    time_ms: float,
    target: str = "unit:1",
    *,
    magnitude: float = 0.8,
    polarity: int = 1,
) -> RuntimePulse:
    return RuntimePulse(
        event_id,
        time_ms,
        target,
        magnitude,
        polarity,
        EventOrigin.EXTERNAL,
    )


def endogenous(
    event_id: str,
    time_ms: float,
    target: str = "unit:2",
    *,
    magnitude: float = 0.7,
    polarity: int = 1,
    state_hash: str = "s" * 64,
) -> RuntimePulse:
    return RuntimePulse(
        event_id,
        time_ms,
        target,
        magnitude,
        polarity,
        EventOrigin.ENDOGENOUS_UNCONFIRMED,
        metadata={"origin_state_hash": state_hash},
    )


def response(
    condition_id: str,
    *,
    current_input: object,
    prior_state_hash: str,
    final_state_hash: str,
    event_target: str,
) -> StateConditionResponse:
    return StateConditionResponse.from_events(
        condition_id=condition_id,
        current_input=current_input,
        prior_state_hash=prior_state_hash,
        final_state_hash=final_state_hash,
        events=(
            endogenous(
                f"endo:{condition_id}",
                10.0,
                event_target,
                state_hash=prior_state_hash,
            ),
        ),
    )


def test_clean_noncopy_candidate_passes_conservative_origin_audit() -> None:
    event = endogenous("endo:x", 10.0)
    result = audit_endogenous_origin(
        event,
        current_external_events=(external("ext:a", 5.0),),
        survives_queue_drained_control=True,
    )
    assert result.candidate is True
    assert result.reason_codes == ()
    assert result.origin_state_hash == "s" * 64


def test_external_event_cannot_be_reported_as_endogenous_candidate() -> None:
    event = external("ext:x", 10.0)
    result = audit_endogenous_origin(
        event,
        current_external_events=(),
        survives_queue_drained_control=True,
    )
    assert result.candidate is False
    assert "not_endogenous" in result.reason_codes


def test_direct_current_input_copy_is_rejected() -> None:
    source = external("ext:a", 10.0, target="unit:2", magnitude=0.7)
    event = endogenous("endo:x", 10.2, target="unit:2", magnitude=0.7)
    result = audit_endogenous_origin(
        event,
        current_external_events=(source,),
        survives_queue_drained_control=True,
        config=EndogenousOriginAuditConfig(direct_copy_window_ms=0.5),
    )
    assert result.candidate is False
    assert result.direct_copy_external_ids == ("ext:a",)
    assert "direct_current_input_copy" in result.reason_codes


def test_known_fixed_delay_echo_is_rejected() -> None:
    source = external("ext:a", 5.0, target="unit:2", magnitude=0.7)
    event = endogenous("endo:x", 10.0, target="unit:2", magnitude=0.7)
    result = audit_endogenous_origin(
        event,
        current_external_events=(source,),
        survives_queue_drained_control=True,
        config=EndogenousOriginAuditConfig(
            known_echo_delays_ms=(5.0,),
            echo_delay_tolerance_ms=0.1,
        ),
    )
    assert result.candidate is False
    assert result.fixed_delay_echo_external_ids == ("ext:a",)
    assert "known_fixed_delay_echo" in result.reason_codes


def test_queue_control_and_evaluator_target_are_required_boundaries() -> None:
    event = endogenous("endo:x", 10.0)
    result = audit_endogenous_origin(
        event,
        current_external_events=(),
        survives_queue_drained_control=False,
        evaluator_target_supplied=True,
    )
    assert result.candidate is False
    assert result.reason_codes == (
        "queue_replay_not_excluded",
        "evaluator_target_leakage",
    )


def test_missing_origin_state_hash_is_not_a_state_grounded_candidate() -> None:
    event = RuntimePulse(
        "endo:x",
        10.0,
        "unit:2",
        0.7,
        1,
        EventOrigin.ENDOGENOUS_UNCONFIRMED,
    )
    result = audit_endogenous_origin(
        event,
        current_external_events=(),
        survives_queue_drained_control=True,
    )
    assert result.candidate is False
    assert result.reason_codes == ("missing_origin_state_hash",)


def test_non_external_control_input_is_rejected() -> None:
    with pytest.raises(ValueError, match="external observations"):
        audit_endogenous_origin(
            endogenous("endo:x", 10.0),
            current_external_events=(endogenous("endo:control", 5.0),),
            survives_queue_drained_control=True,
        )


def test_state_dependence_candidate_requires_same_input_and_different_history() -> None:
    current_input = {"target": "unit:1", "magnitude": 0.8}
    reference = response(
        "reference",
        current_input=current_input,
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    replay = response(
        "replay",
        current_input=current_input,
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    alternate = response(
        "alternate",
        current_input=current_input,
        prior_state_hash="b" * 64,
        final_state_hash="d" * 64,
        event_target="unit:3",
    )

    result = assess_persistent_state_dependence(
        reference=reference,
        alternate_history=alternate,
        reference_replay=replay,
    )
    assert result.candidate is True
    assert result.deterministic_replay is True
    assert result.histories_distinct is True
    assert result.response_changed_with_history is True


def test_same_response_under_different_history_is_not_state_dependence() -> None:
    current_input = ["pulse-a"]
    reference = response(
        "reference",
        current_input=current_input,
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    replay = response(
        "replay",
        current_input=current_input,
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    alternate = StateConditionResponse(
        condition_id="alternate",
        current_input_hash=reference.current_input_hash,
        prior_state_hash="b" * 64,
        response_trace_hash=reference.response_trace_hash,
        final_state_hash="d" * 64,
        endogenous_event_ids=("endo:alternate",),
        endogenous_targets=("unit:2",),
    )
    result = assess_persistent_state_dependence(
        reference=reference,
        alternate_history=alternate,
        reference_replay=replay,
    )
    assert result.candidate is False
    assert "endogenous_response_not_history_dependent" in result.reason_codes


def test_nondeterministic_reference_replay_fails_candidate() -> None:
    current_input = ["pulse-a"]
    reference = response(
        "reference",
        current_input=current_input,
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    replay = response(
        "replay",
        current_input=current_input,
        prior_state_hash="a" * 64,
        final_state_hash="e" * 64,
        event_target="unit:4",
    )
    alternate = response(
        "alternate",
        current_input=current_input,
        prior_state_hash="b" * 64,
        final_state_hash="d" * 64,
        event_target="unit:3",
    )
    result = assess_persistent_state_dependence(
        reference=reference,
        alternate_history=alternate,
        reference_replay=replay,
    )
    assert result.candidate is False
    assert "reference_replay_not_deterministic" in result.reason_codes


def test_different_current_input_is_rejected_before_scoring() -> None:
    reference = response(
        "reference",
        current_input=["pulse-a"],
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    replay = response(
        "replay",
        current_input=["pulse-a"],
        prior_state_hash="a" * 64,
        final_state_hash="c" * 64,
        event_target="unit:2",
    )
    alternate = response(
        "alternate",
        current_input=["pulse-b"],
        prior_state_hash="b" * 64,
        final_state_hash="d" * 64,
        event_target="unit:3",
    )
    with pytest.raises(ValueError, match="same current input"):
        assess_persistent_state_dependence(
            reference=reference,
            alternate_history=alternate,
            reference_replay=replay,
        )


def test_state_response_rejects_external_events_and_is_assembly_free() -> None:
    with pytest.raises(ValueError, match="must be endogenous"):
        StateConditionResponse.from_events(
            condition_id="bad",
            current_input=["pulse-a"],
            prior_state_hash="a" * 64,
            final_state_hash="b" * 64,
            events=(external("ext:a", 1.0),),
        )

    row = response(
        "good",
        current_input=["pulse-a"],
        prior_state_hash="a" * 64,
        final_state_hash="b" * 64,
        event_target="unit:2",
    )
    assert "assembly_id" not in str(row.state_dict()).lower()
    assert "motif_id" not in str(row.state_dict()).lower()

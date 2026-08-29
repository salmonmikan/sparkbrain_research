from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import (
    EventOrigin,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)


@dataclass(frozen=True, slots=True)
class EndogenousOriginAuditConfig:
    """Controls for classifying an internally originated event candidate.

    The audit is deliberately conservative. Passing it does not establish a
    predictive or functional endogenous Spark; it only excludes several direct
    shortcut explanations for a Level-1 origin candidate.
    """

    direct_copy_window_ms: float = 0.5
    magnitude_tolerance: float = 1e-9
    known_echo_delays_ms: tuple[float, ...] = ()
    echo_delay_tolerance_ms: float = 0.25
    require_queue_drained_control: bool = True

    def validate(self) -> None:
        for name in (
            "direct_copy_window_ms",
            "magnitude_tolerance",
            "echo_delay_tolerance_ms",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        for delay in self.known_echo_delays_ms:
            if not math.isfinite(float(delay)) or delay < 0:
                raise ValueError("known echo delays must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class EndogenousOriginAudit:
    event_id: str
    candidate: bool
    reason_codes: tuple[str, ...]
    direct_copy_external_ids: tuple[str, ...]
    fixed_delay_echo_external_ids: tuple[str, ...]
    survives_queue_drained_control: bool
    evaluator_target_supplied: bool
    origin_state_hash: str | None

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        validate_runtime_mapping(value, path="v06.origin_audit")
        return value


def audit_endogenous_origin(
    event: RuntimePulse,
    *,
    current_external_events: tuple[RuntimePulse, ...],
    survives_queue_drained_control: bool,
    evaluator_target_supplied: bool = False,
    config: EndogenousOriginAuditConfig | None = None,
) -> EndogenousOriginAudit:
    """Exclude direct-copy, known-echo, queue, and evaluator-target shortcuts."""

    cfg = config or EndogenousOriginAuditConfig()
    cfg.validate()
    reasons: list[str] = []
    if not event.origin.is_endogenous:
        reasons.append("not_endogenous")

    direct: list[str] = []
    echoes: list[str] = []
    for external in current_external_events:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("current_external_events must contain only external observations")
        same_shape = (
            external.target == event.target
            and external.polarity == event.polarity
            and abs(external.magnitude - event.magnitude) <= cfg.magnitude_tolerance
        )
        delay = event.time_ms - external.time_ms
        if same_shape and abs(delay) <= cfg.direct_copy_window_ms:
            direct.append(external.event_id)
        if same_shape and any(
            abs(delay - known_delay) <= cfg.echo_delay_tolerance_ms
            for known_delay in cfg.known_echo_delays_ms
        ):
            echoes.append(external.event_id)

    if direct:
        reasons.append("direct_current_input_copy")
    if echoes:
        reasons.append("known_fixed_delay_echo")
    if cfg.require_queue_drained_control and not survives_queue_drained_control:
        reasons.append("queue_replay_not_excluded")
    if evaluator_target_supplied:
        reasons.append("evaluator_target_leakage")

    origin_state_hash = event.metadata.get("origin_state_hash")
    if origin_state_hash is not None and not isinstance(origin_state_hash, str):
        raise ValueError("origin_state_hash metadata must be a string")
    if event.origin.is_endogenous and not origin_state_hash:
        reasons.append("missing_origin_state_hash")

    return EndogenousOriginAudit(
        event_id=event.event_id,
        candidate=not reasons,
        reason_codes=tuple(reasons),
        direct_copy_external_ids=tuple(direct),
        fixed_delay_echo_external_ids=tuple(echoes),
        survives_queue_drained_control=survives_queue_drained_control,
        evaluator_target_supplied=evaluator_target_supplied,
        origin_state_hash=origin_state_hash,
    )


@dataclass(frozen=True, slots=True)
class StateConditionResponse:
    """One response to a matched current input under a specific prior state."""

    condition_id: str
    current_input_hash: str
    prior_state_hash: str
    response_trace_hash: str
    final_state_hash: str
    endogenous_event_ids: tuple[str, ...]
    endogenous_targets: tuple[str, ...]

    @classmethod
    def from_events(
        cls,
        *,
        condition_id: str,
        current_input: object,
        prior_state_hash: str,
        final_state_hash: str,
        events: tuple[RuntimePulse, ...],
    ) -> StateConditionResponse:
        if not condition_id or not prior_state_hash or not final_state_hash:
            raise ValueError("condition and state hashes must be non-empty")
        for event in events:
            if not event.origin.is_endogenous:
                raise ValueError("state response events must be endogenous")
        event_rows = [event.as_dict() for event in events]
        value = cls(
            condition_id=condition_id,
            current_input_hash=digest(current_input),
            prior_state_hash=prior_state_hash,
            response_trace_hash=digest(event_rows),
            final_state_hash=final_state_hash,
            endogenous_event_ids=tuple(event.event_id for event in events),
            endogenous_targets=tuple(event.target for event in events),
        )
        validate_runtime_mapping(value.state_dict(), path="v06.state_response")
        return value

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        validate_runtime_mapping(value, path="v06.state_response")
        return value


@dataclass(frozen=True, slots=True)
class StateDependenceAssessment:
    current_input_hash: str
    reference_prior_state_hash: str
    alternate_prior_state_hash: str
    deterministic_replay: bool
    histories_distinct: bool
    response_changed_with_history: bool
    final_state_changed_with_history: bool
    candidate: bool
    reason_codes: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        validate_runtime_mapping(value, path="v06.state_dependence")
        return value


def assess_persistent_state_dependence(
    *,
    reference: StateConditionResponse,
    alternate_history: StateConditionResponse,
    reference_replay: StateConditionResponse,
) -> StateDependenceAssessment:
    """Test history dependence while requiring deterministic same-state replay."""

    input_hashes = {
        reference.current_input_hash,
        alternate_history.current_input_hash,
        reference_replay.current_input_hash,
    }
    if len(input_hashes) != 1:
        raise ValueError("state-dependence runs must use the same current input")
    if reference.prior_state_hash != reference_replay.prior_state_hash:
        raise ValueError("reference replay must start from the same prior state")

    deterministic = (
        reference.response_trace_hash == reference_replay.response_trace_hash
        and reference.final_state_hash == reference_replay.final_state_hash
    )
    histories_distinct = reference.prior_state_hash != alternate_history.prior_state_hash
    response_changed = (
        reference.response_trace_hash != alternate_history.response_trace_hash
    )
    final_state_changed = reference.final_state_hash != alternate_history.final_state_hash

    reasons: list[str] = []
    if not deterministic:
        reasons.append("reference_replay_not_deterministic")
    if not histories_distinct:
        reasons.append("prior_states_not_distinct")
    if not response_changed:
        reasons.append("endogenous_response_not_history_dependent")

    return StateDependenceAssessment(
        current_input_hash=reference.current_input_hash,
        reference_prior_state_hash=reference.prior_state_hash,
        alternate_prior_state_hash=alternate_history.prior_state_hash,
        deterministic_replay=deterministic,
        histories_distinct=histories_distinct,
        response_changed_with_history=response_changed,
        final_state_changed_with_history=final_state_changed,
        candidate=not reasons,
        reason_codes=tuple(reasons),
    )

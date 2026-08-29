from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, validate_runtime_mapping
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation

from .v06_endogenous import (
    EndogenousOriginAudit,
    EndogenousOriginAuditConfig,
    StateConditionResponse,
    StateDependenceAssessment,
    assess_persistent_state_dependence,
    audit_endogenous_origin,
)


@dataclass(frozen=True, slots=True)
class StateProbeConditionResult:
    condition_id: str
    prior_state_hash: str
    final_state_hash: str
    current_input: dict[str, Any]
    endogenous_events: tuple[dict[str, Any], ...]
    origin_audits: tuple[EndogenousOriginAudit, ...]
    response: StateConditionResponse
    queue_drained: bool

    def state_dict(self) -> dict[str, Any]:
        value = {
            "condition_id": self.condition_id,
            "current_input": self.current_input,
            "endogenous_events": list(self.endogenous_events),
            "final_state_hash": self.final_state_hash,
            "origin_audits": [row.state_dict() for row in self.origin_audits],
            "prior_state_hash": self.prior_state_hash,
            "queue_drained": self.queue_drained,
            "response": self.response.state_dict(),
        }
        validate_runtime_mapping(value, path="evaluation.v06_state_probe.condition")
        return value


@dataclass(frozen=True, slots=True)
class CanonicalStateProbeResult:
    reference: StateProbeConditionResult
    reference_replay: StateProbeConditionResult
    alternate_history: StateProbeConditionResult
    no_history_event_count: int
    assessment: StateDependenceAssessment

    @property
    def all_origin_audits_passed(self) -> bool:
        return all(
            audit.candidate
            for condition in (
                self.reference,
                self.reference_replay,
                self.alternate_history,
            )
            for audit in condition.origin_audits
        )

    @property
    def engineering_candidate(self) -> bool:
        return (
            self.assessment.candidate
            and self.all_origin_audits_passed
            and self.no_history_event_count == 0
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "all_origin_audits_passed": self.all_origin_audits_passed,
            "alternate_history": self.alternate_history.state_dict(),
            "assessment": self.assessment.state_dict(),
            "engineering_candidate": self.engineering_candidate,
            "no_history_event_count": self.no_history_event_count,
            "reference": self.reference.state_dict(),
            "reference_replay": self.reference_replay.state_dict(),
        }


def external(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    magnitude: float = 0.8,
    polarity: int = 1,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=magnitude,
        polarity=polarity,
        origin=EventOrigin.EXTERNAL,
    )


def canonical_history(target: str) -> tuple[tuple[RuntimePulse, RuntimePulse], ...]:
    return tuple(
        (
            external(f"history-{target}-{index}-source", offset, "unit:0"),
            external(f"history-{target}-{index}-target", offset + 5.0, target),
        )
        for index, offset in enumerate((0.0, 20.0, 40.0))
    )


def _train(
    history: tuple[tuple[RuntimePulse, RuntimePulse], ...],
    config: LocalExpectationConfig,
) -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(config)
    for source, target in history:
        model.observe_external_transition(source, target)
    return model


def run_state_condition(
    *,
    condition_id: str,
    history: tuple[tuple[RuntimePulse, RuntimePulse], ...],
    current_input: RuntimePulse,
    config: LocalExpectationConfig | None = None,
    audit_config: EndogenousOriginAuditConfig | None = None,
) -> StateProbeConditionResult:
    if current_input.origin is not EventOrigin.EXTERNAL:
        raise ValueError("state probe current input must be external")
    model = _train(
        history,
        config
        or LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=20.0,
        ),
    )
    prior_state_hash = model.state_hash()
    proposals = model.proposals_for(
        current_input,
        origin_state_hash=prior_state_hash,
    )
    events = tuple(proposal.to_runtime_pulse() for proposal in proposals)
    final_state_hash = model.state_hash()
    audits = tuple(
        audit_endogenous_origin(
            event,
            current_external_events=(current_input,),
            survives_queue_drained_control=True,
            evaluator_target_supplied=False,
            config=audit_config
            or EndogenousOriginAuditConfig(known_echo_delays_ms=(5.0,)),
        )
        for event in events
    )
    response = StateConditionResponse.from_events(
        condition_id=condition_id,
        current_input={
            "magnitude": current_input.magnitude,
            "polarity": current_input.polarity,
            "target": current_input.target,
            "time_ms": current_input.time_ms,
        },
        prior_state_hash=prior_state_hash,
        final_state_hash=final_state_hash,
        events=events,
    )
    return StateProbeConditionResult(
        condition_id=condition_id,
        prior_state_hash=prior_state_hash,
        final_state_hash=final_state_hash,
        current_input=current_input.as_dict(),
        endogenous_events=tuple(event.as_dict() for event in events),
        origin_audits=audits,
        response=response,
        queue_drained=True,
    )


def run_canonical_state_probe() -> CanonicalStateProbeResult:
    current_input = external("current", 100.0, "unit:0")
    config = LocalExpectationConfig(
        minimum_observations=2,
        minimum_confidence=0.1,
        proposal_ttl_ms=20.0,
    )
    reference = run_state_condition(
        condition_id="reference",
        history=canonical_history("unit:1"),
        current_input=current_input,
        config=config,
    )
    replay = run_state_condition(
        condition_id="reference-replay",
        history=canonical_history("unit:1"),
        current_input=current_input,
        config=config,
    )
    alternate = run_state_condition(
        condition_id="alternate-history",
        history=canonical_history("unit:2"),
        current_input=current_input,
        config=config,
    )
    no_history = run_state_condition(
        condition_id="no-history",
        history=(),
        current_input=current_input,
        config=config,
    )
    assessment = assess_persistent_state_dependence(
        reference=reference.response,
        alternate_history=alternate.response,
        reference_replay=replay.response,
    )
    result = CanonicalStateProbeResult(
        reference=reference,
        reference_replay=replay,
        alternate_history=alternate,
        no_history_event_count=len(no_history.endogenous_events),
        assessment=assessment,
    )
    validate_runtime_mapping(
        asdict(result.assessment),
        path="evaluation.v06_state_probe.assessment",
    )
    return result

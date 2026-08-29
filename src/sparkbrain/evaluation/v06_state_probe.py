from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.foundation import (
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.reinjection import (
    FieldReinjectionGate,
    ReinjectionConfig,
    ReinjectionDecision,
)

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
    no_reinjection_spike_count: int
    reinjection_accepted_count: int
    field_spike_count: int
    reinjection_decisions: tuple[dict[str, Any], ...]

    def state_dict(self) -> dict[str, Any]:
        value = {
            "condition_id": self.condition_id,
            "current_input": self.current_input,
            "endogenous_events": list(self.endogenous_events),
            "field_spike_count": self.field_spike_count,
            "final_state_hash": self.final_state_hash,
            "no_reinjection_spike_count": self.no_reinjection_spike_count,
            "origin_audits": [row.state_dict() for row in self.origin_audits],
            "prior_state_hash": self.prior_state_hash,
            "queue_drained": self.queue_drained,
            "reinjection_accepted_count": self.reinjection_accepted_count,
            "reinjection_decisions": list(self.reinjection_decisions),
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
        conditions = (
            self.reference,
            self.reference_replay,
            self.alternate_history,
        )
        return all(condition.origin_audits for condition in conditions) and all(
            audit.candidate
            for condition in conditions
            for audit in condition.origin_audits
        )

    @property
    def engineering_candidate(self) -> bool:
        return (
            self.assessment.candidate
            and self.all_origin_audits_passed
            and self.no_history_event_count == 0
            and all(
                condition.queue_drained
                and condition.no_reinjection_spike_count == 0
                and condition.reinjection_accepted_count > 0
                and condition.field_spike_count > 0
                for condition in (
                    self.reference,
                    self.reference_replay,
                    self.alternate_history,
                )
            )
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


def _new_field() -> TemporalExcitableField:
    topology = explicit_topology(
        (
            UnitState(unit_id=0, x=0.0, y=0.0, base_threshold=0.5),
            UnitState(unit_id=1, x=1.0, y=0.0, base_threshold=0.5),
            UnitState(unit_id=2, x=2.0, y=0.0, base_threshold=0.5),
        ),
        (),
        receptor_ids=(0,),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
        ),
    )


def _schedule_external(field: TemporalExcitableField, pulse: RuntimePulse) -> None:
    target = int(pulse.target.removeprefix("unit:"))
    field.schedule_arrival(
        SynapticArrival(
            time_ms=pulse.time_ms,
            target_id=target,
            current=pulse.polarity * pulse.magnitude,
            source_id=None,
            pulse_id=pulse.event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )


def _runtime_event(
    spike: SpikeEvent,
    *,
    proposal_id: str,
    origin_state_hash: str,
    local_path_ids: tuple[str, ...],
    generation_depth: int,
) -> RuntimePulse:
    identity = {
        "proposal_id": proposal_id,
        "sources": list(spike.source_pulse_ids),
        "time_ms": spike.time_ms,
        "unit_id": spike.unit_id,
    }
    return RuntimePulse(
        event_id=f"spark:{digest(identity)[:24]}",
        time_ms=spike.time_ms,
        target=f"unit:{spike.unit_id}",
        magnitude=spike.potential_before_reset,
        polarity=1,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        generation_depth=generation_depth,
        parent_event_ids=(f"endo:{proposal_id}",),
        source_path_ids=local_path_ids,
        metadata={"origin_state_hash": origin_state_hash},
    )


def _proposal_for_spike(
    spike: SpikeEvent,
    decisions: tuple[ReinjectionDecision, ...],
    model: LocalTemporalExpectation,
) -> str:
    accepted = [
        decision.proposal_id
        for decision in decisions
        if decision.accepted
        and decision.target_unit_id == spike.unit_id
        and decision.scheduled_time_ms == spike.time_ms
        and f"endo:{decision.proposal_id}" in spike.source_pulse_ids
    ]
    if len(accepted) != 1:
        raise RuntimeError("an endogenous Spark must map to exactly one accepted proposal")
    proposal_id = accepted[0]
    if proposal_id not in {row.proposal_id for rows in model._transitions.values() for row in ()}:
        # No-op expression keeps the evaluator from depending on a hidden target table. The actual
        # proposal content is resolved from the provenance ledger by the caller.
        pass
    return proposal_id


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
    field = _new_field()
    ledger = ProvenanceLedger()
    ledger.register_external(current_input)
    _schedule_external(field, current_input)
    field.run_until(current_input.time_ms)
    if field.state_dict()["queue"]:
        raise RuntimeError("canonical state probe requires a drained queue before reinjection")

    prior_state_hash = digest(
        {
            "field": field.state_dict(),
            "local_expectation": model.state_dict(),
        }
    )
    proposals = model.proposals_for(
        current_input,
        origin_state_hash=prior_state_hash,
    )

    control = TemporalExcitableField.from_state_dict(field.state_dict())
    horizon = max(
        (proposal.predicted_arrival_ms for proposal in proposals),
        default=current_input.time_ms + 5.0,
    )
    control_spikes = control.run_until(horizon)
    queue_drained = not control_spikes and not field.state_dict()["queue"]

    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.1,
            current_gain=1.0,
            maximum_effective_current=2.0,
        ),
    )
    decisions: list[ReinjectionDecision] = []
    for proposal in proposals:
        ledger.register_proposal(proposal)
        decisions.append(gate.schedule(proposal, field))
    decision_rows = tuple(decisions)
    field_spikes = field.run_until(horizon)

    events: list[RuntimePulse] = []
    for spike in field_spikes:
        proposal_id = _proposal_for_spike(spike, decision_rows, model)
        proposal = ledger.proposals[proposal_id]
        events.append(
            _runtime_event(
                spike,
                proposal_id=proposal_id,
                origin_state_hash=prior_state_hash,
                local_path_ids=proposal.local_path_ids,
                generation_depth=proposal.generation_depth,
            )
        )
    event_rows = tuple(events)
    final_state_hash = digest(
        {
            "field": field.state_dict(),
            "gate": gate.state_dict(),
            "ledger": ledger.state_dict(),
            "local_expectation": model.state_dict(),
        }
    )
    audits = tuple(
        audit_endogenous_origin(
            event,
            current_external_events=(current_input,),
            survives_queue_drained_control=queue_drained,
            evaluator_target_supplied=False,
            config=audit_config
            or EndogenousOriginAuditConfig(known_echo_delays_ms=(5.0,)),
        )
        for event in event_rows
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
        events=event_rows,
    )
    return StateProbeConditionResult(
        condition_id=condition_id,
        prior_state_hash=prior_state_hash,
        final_state_hash=final_state_hash,
        current_input=current_input.as_dict(),
        endogenous_events=tuple(event.as_dict() for event in event_rows),
        origin_audits=audits,
        response=response,
        queue_drained=queue_drained,
        no_reinjection_spike_count=len(control_spikes),
        reinjection_accepted_count=sum(decision.accepted for decision in decision_rows),
        field_spike_count=len(field_spikes),
        reinjection_decisions=tuple(decision.state_dict() for decision in decision_rows),
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

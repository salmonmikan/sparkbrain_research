from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField

from .foundation import (
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    validate_runtime_mapping,
)
from .local_expectation import LocalTemporalExpectation
from .local_transition import PreparedLocalTransition, SparseLocalTransitionAdaptation
from .reality import RealityCorrectionEngine, RealityCorrectionResult
from .reinjection import FieldReinjectionGate, ReinjectionDecision


@dataclass(frozen=True, slots=True)
class ForwardRuntimeConfig:
    reinjection_enabled: bool = True
    expand_endogenous_sparks: bool = True
    maximum_internal_steps: int = 128

    def validate(self) -> None:
        if self.maximum_internal_steps < 1:
            raise ValueError("maximum_internal_steps must be positive")


@dataclass(frozen=True, slots=True)
class EndogenousSparkRecord:
    time_ms: float
    unit_id: int
    proposal_root_ids: tuple[str, ...]
    source_pulse_ids: tuple[str, ...]

    @property
    def target(self) -> str:
        return f"unit:{self.unit_id}"

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProposalScheduleRecord:
    source_event_id: str
    proposal_id: str
    target: str
    predicted_arrival_ms: float
    reinjection: ReinjectionDecision | None

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        if self.reinjection is not None:
            value["reinjection"] = self.reinjection.state_dict()
        return value


@dataclass(frozen=True, slots=True)
class ExternalStepRecord:
    external_event_id: str
    external_time_ms: float
    reality: RealityCorrectionResult
    field_spike_ids: tuple[int, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "external_event_id": self.external_event_id,
            "external_time_ms": self.external_time_ms,
            "field_spike_ids": list(self.field_spike_ids),
            "reality": self.reality.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class ForwardCompletionEvaluation:
    expected_target: str
    later_external_event_id: str
    later_external_time_ms: float
    endogenous_spark_time_ms: float | None
    forward_generated: bool
    temporal_compliance: bool
    later_prediction_matched: bool
    retrospective_only: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class AssemblyFreeForwardRuntime:
    """Connects G1/G2, normal Field reinjection, and external reality.

    The runtime consumes no Assembly state. External events are advanced in
    chronological order. Pending internal arrivals strictly earlier than the
    next external event are processed first; arrivals at the same timestamp are
    presented to `RealityCorrectionEngine` before the Field runs, preventing a
    prediction from being double-counted with its observation.
    """

    def __init__(
        self,
        field: TemporalExcitableField,
        expectation: LocalTemporalExpectation,
        transition: SparseLocalTransitionAdaptation,
        reinjection: FieldReinjectionGate,
        reality: RealityCorrectionEngine,
        config: ForwardRuntimeConfig | None = None,
    ) -> None:
        if transition.expectation is not expectation:
            raise ValueError("forward runtime and G2 must share one G1 model")
        if transition.ledger is not reality.ledger:
            raise ValueError("forward runtime components must share one provenance ledger")
        if reinjection.ledger is not reality.ledger:
            raise ValueError("reinjection and reality must share one provenance ledger")
        self.field = field
        self.expectation = expectation
        self.transition = transition
        self.reinjection = reinjection
        self.reality = reality
        self.ledger: ProvenanceLedger = reality.ledger
        self.config = config or ForwardRuntimeConfig()
        self.config.validate()
        self.generated_sparks: list[EndogenousSparkRecord] = []
        self.proposal_schedules: list[ProposalScheduleRecord] = []
        self.external_steps: list[ExternalStepRecord] = []
        self._expanded_proposal_roots: set[str] = set()
        self._internal_step_count = 0

    def process_external(self, external: RuntimePulse) -> ExternalStepRecord:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("forward runtime accepts only external observations")
        self.advance_internal_until(external.time_ms, include_endpoint=False)
        reality_result = self.reality.process_external(external, self.field)
        spikes = self.field.run_until(external.time_ms)
        self.reality.observe_spikes(spikes)
        self._record_endogenous_spikes(spikes)
        if self._external_caused_spike(external, spikes):
            self._prepare_and_schedule(external)
        row = ExternalStepRecord(
            external_event_id=external.event_id,
            external_time_ms=external.time_ms,
            reality=reality_result,
            field_spike_ids=tuple(spike.unit_id for spike in spikes),
        )
        self.external_steps.append(row)
        return row

    def advance_internal_until(
        self,
        end_ms: float,
        *,
        include_endpoint: bool = True,
    ) -> tuple[EndogenousSparkRecord, ...]:
        if end_ms < self.field.current_time_ms:
            raise ValueError("end_ms cannot move backwards")
        before = len(self.generated_sparks)
        while self.field._queue:  # noqa: SLF001 - retained Field event loop adapter
            next_time = self.field._queue[0][0]  # noqa: SLF001
            if next_time > end_ms or (next_time == end_ms and not include_endpoint):
                break
            self._internal_step_count += 1
            if self._internal_step_count > self.config.maximum_internal_steps:
                raise RuntimeError("maximum_internal_steps exceeded")
            spikes = self.field.run_until(next_time)
            self.reality.observe_spikes(spikes)
            self._record_endogenous_spikes(spikes)
        if include_endpoint and self.field.current_time_ms < end_ms:
            self.field.run_until(end_ms)
        return tuple(self.generated_sparks[before:])

    def _record_endogenous_spikes(self, spikes: Iterable[SpikeEvent]) -> None:
        for spike in spikes:
            roots = self._proposal_roots(spike)
            if not roots:
                continue
            self.generated_sparks.append(
                EndogenousSparkRecord(
                    time_ms=spike.time_ms,
                    unit_id=spike.unit_id,
                    proposal_root_ids=roots,
                    source_pulse_ids=spike.source_pulse_ids,
                )
            )
            if not self.config.expand_endogenous_sparks:
                continue
            for root_id in roots:
                if root_id in self._expanded_proposal_roots:
                    continue
                self._expanded_proposal_roots.add(root_id)
                self._expand_endogenous_root(root_id, spike)

    def _expand_endogenous_root(self, root_id: str, spike: SpikeEvent) -> None:
        proposal = self.ledger.proposals[root_id]
        event = self.ledger.events[f"endo:{root_id}"]
        source = RuntimePulse(
            event_id=f"endo:{root_id}",
            time_ms=spike.time_ms,
            target=f"unit:{spike.unit_id}",
            magnitude=max(proposal.magnitude, spike.dynamic_threshold),
            polarity=proposal.polarity,
            origin=event.origin,
            generation_depth=proposal.generation_depth,
            parent_event_ids=event.parent_event_ids,
            source_path_ids=event.source_path_ids,
            metadata={"derived_from_field_spark": True},
        )
        self._prepare_and_schedule(source)

    def _prepare_and_schedule(
        self,
        source: RuntimePulse,
    ) -> tuple[PreparedLocalTransition, ...]:
        prepared = self.transition.prepare(
            source,
            origin_state_hash=self.field.state_hash(),
        )
        for row in prepared:
            decision = None
            if self.config.reinjection_enabled:
                decision = self.reinjection.schedule(row.proposal, self.field)
            self.proposal_schedules.append(
                ProposalScheduleRecord(
                    source_event_id=source.event_id,
                    proposal_id=row.proposal.proposal_id,
                    target=row.proposal.target,
                    predicted_arrival_ms=row.proposal.predicted_arrival_ms,
                    reinjection=decision,
                )
            )
        return prepared

    def _proposal_roots(self, spike: SpikeEvent) -> tuple[str, ...]:
        lineage = self.reality.lineage.state_dict()
        roots: set[str] = set()
        for pulse_id in spike.source_pulse_ids:
            if pulse_id.startswith("endo:"):
                roots.add(pulse_id.removeprefix("endo:"))
            roots.update(lineage.get(pulse_id, ()))
        return tuple(sorted(roots))

    @staticmethod
    def _external_caused_spike(
        external: RuntimePulse,
        spikes: Iterable[SpikeEvent],
    ) -> bool:
        target_id = int(external.target.removeprefix("unit:"))
        return any(
            spike.unit_id == target_id and external.event_id in spike.source_pulse_ids
            for spike in spikes
        )

    def state_dict(self) -> dict[str, Any]:
        value = {
            "config": asdict(self.config),
            "expanded_proposal_roots": sorted(self._expanded_proposal_roots),
            "external_steps": [row.state_dict() for row in self.external_steps],
            "field": self.field.state_dict(),
            "generated_sparks": [row.state_dict() for row in self.generated_sparks],
            "internal_step_count": self._internal_step_count,
            "proposal_schedules": [row.state_dict() for row in self.proposal_schedules],
            "reality": self.reality.state_dict(),
            "reinjection": self.reinjection.state_dict(),
            "transition": self.transition.state_dict(),
        }
        validate_runtime_mapping(value, path="v06.forward_runtime")
        return value


def train_external_sequences(
    expectation: LocalTemporalExpectation,
    sequences: Iterable[Iterable[RuntimePulse]],
) -> None:
    for sequence in sequences:
        rows = tuple(sequence)
        for source, target in zip(rows, rows[1:], strict=False):
            expectation.observe_external_transition(source, target)


def evaluate_forward_completion(
    runtime: AssemblyFreeForwardRuntime,
    *,
    expected_target: str,
    later_external_event_id: str,
    later_external_time_ms: float,
) -> ForwardCompletionEvaluation:
    candidates = [
        row
        for row in runtime.generated_sparks
        if row.target == expected_target and row.time_ms < later_external_time_ms
    ]
    generated_time = min((row.time_ms for row in candidates), default=None)
    later_matches = [
        match
        for match in runtime.ledger.matches.values()
        if match.external_event_id == later_external_event_id
        and match.status in {"matched", "downstream-confirmed"}
    ]
    forward_generated = generated_time is not None
    return ForwardCompletionEvaluation(
        expected_target=expected_target,
        later_external_event_id=later_external_event_id,
        later_external_time_ms=later_external_time_ms,
        endogenous_spark_time_ms=generated_time,
        forward_generated=forward_generated,
        temporal_compliance=(
            generated_time is not None and generated_time < later_external_time_ms
        ),
        later_prediction_matched=bool(later_matches),
        retrospective_only=not forward_generated,
    )

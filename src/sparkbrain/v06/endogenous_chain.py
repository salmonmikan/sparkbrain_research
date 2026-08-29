from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

from .foundation import (
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    digest,
    validate_runtime_mapping,
)
from .local_expectation import LocalTemporalExpectation
from .local_transition import PreparedLocalTransition, SparseLocalTransitionAdaptation
from .reinjection import FieldReinjectionGate, ReinjectionDecision


@dataclass(frozen=True, slots=True)
class EndogenousChainIntervention:
    """Assembly-free intervention controls for endogenous-chain experiments."""

    suppress_expansion_unit_ids: tuple[int, ...] = ()
    suppress_reinjection_path_ids: tuple[str, ...] = ()
    suppress_reinjection_depths: tuple[int, ...] = ()

    def validate(self) -> None:
        if any(unit_id < 0 for unit_id in self.suppress_expansion_unit_ids):
            raise ValueError("suppressed unit IDs must be non-negative")
        if any(not path_id for path_id in self.suppress_reinjection_path_ids):
            raise ValueError("suppressed path IDs must be non-empty")
        if any(depth < 1 for depth in self.suppress_reinjection_depths):
            raise ValueError("suppressed generation depths must be positive")


@dataclass(frozen=True, slots=True)
class EndogenousChainConfig:
    maximum_internal_steps: int = 128
    maximum_recorded_sparks: int = 256
    external_current_gain: float = 1.0
    maximum_external_current: float = 4.0

    def validate(self) -> None:
        if self.maximum_internal_steps < 1 or self.maximum_recorded_sparks < 1:
            raise ValueError("chain limits must be positive")
        for name in ("external_current_gain", "maximum_external_current"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be positive and finite")


@dataclass(frozen=True, slots=True)
class EndogenousChainSpark:
    spark_id: str
    time_ms: float
    unit_id: int
    generation_depth: int
    proposal_ids: tuple[str, ...]
    parent_proposal_ids: tuple[str, ...]
    source_pulse_ids: tuple[str, ...]
    external_observation_count: int
    committed_positive_updates: int

    @property
    def target(self) -> str:
        return f"unit:{self.unit_id}"

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EndogenousProposalRecord:
    source_event_id: str
    source_origin: str
    source_target: str
    source_time_ms: float
    proposal_id: str
    parent_proposal_ids: tuple[str, ...]
    path_id: str
    target: str
    predicted_arrival_ms: float
    generation_depth: int
    reinjection: ReinjectionDecision | None
    intervention_reason: str | None

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        if self.reinjection is not None:
            value["reinjection"] = self.reinjection.state_dict()
        return value


@dataclass(frozen=True, slots=True)
class EndogenousInterventionRecord:
    stage: str
    reason: str
    source_event_id: str
    source_unit_id: int | None
    proposal_id: str | None
    path_id: str | None
    generation_depth: int | None
    time_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class AutonomousEndogenousChainRuntime:
    """Run endogenous Spark chains without explicit Assembly state.

    External cue Sparks may produce G2 proposals. A proposal is reinjected as
    ordinary Field current. Only an actual Field Spark can become the source of
    the next local prediction. No external event is synthesized during silence,
    and no endogenous-only activity can commit positive learning.
    """

    def __init__(
        self,
        field: TemporalExcitableField,
        expectation: LocalTemporalExpectation,
        transition: SparseLocalTransitionAdaptation,
        reinjection: FieldReinjectionGate,
        *,
        config: EndogenousChainConfig | None = None,
        intervention: EndogenousChainIntervention | None = None,
    ) -> None:
        if transition.expectation is not expectation:
            raise ValueError("chain runtime and G2 must share one G1 model")
        if transition.ledger is not reinjection.ledger:
            raise ValueError("chain runtime components must share one provenance ledger")
        self.field = field
        self.expectation = expectation
        self.transition = transition
        self.reinjection = reinjection
        self.ledger: ProvenanceLedger = transition.ledger
        self.config = config or EndogenousChainConfig()
        self.config.validate()
        self.intervention = intervention or EndogenousChainIntervention()
        self.intervention.validate()
        self.generated_sparks: list[EndogenousChainSpark] = []
        self.proposal_records: list[EndogenousProposalRecord] = []
        self.intervention_records: list[EndogenousInterventionRecord] = []
        self.external_event_ids: list[str] = []
        self._expanded_spike_ids: set[str] = set()
        self._pulse_proposal_roots: dict[str, frozenset[str]] = {}
        self._internal_step_count = 0

    def present_external(self, external: RuntimePulse) -> tuple[SpikeEvent, ...]:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("chain runtime accepts only external observations")
        if external.time_ms < self.field.current_time_ms:
            raise ValueError("external cue cannot move Field time backwards")
        self.advance_silence(external.time_ms, include_endpoint=False)
        target_unit_id = self._target_unit_id(external.target)
        if target_unit_id not in self.field.units:
            raise KeyError(f"unknown external target unit: {target_unit_id}")
        if external.event_id in self.ledger.events:
            raise ValueError("external event ID was already registered")
        self.ledger.register_external(external)
        self.external_event_ids.append(external.event_id)
        current = external.polarity * min(
            self.config.maximum_external_current,
            external.magnitude * self.config.external_current_gain,
        )
        self.field.schedule_arrival(
            SynapticArrival(
                time_ms=external.time_ms,
                target_id=target_unit_id,
                current=current,
                source_id=None,
                pulse_id=external.event_id,
                novelty=float(external.metadata.get("novelty", 0.0)),
                prediction_error=float(external.metadata.get("prediction_error", 0.0)),
            )
        )
        spikes = self.field.run_until(external.time_ms)
        self._observe_spikes(spikes)
        if self._external_caused_spike(external, spikes):
            self._prepare_and_maybe_reinject(external)
        return spikes

    def advance_silence(
        self,
        end_ms: float,
        *,
        include_endpoint: bool = True,
    ) -> tuple[EndogenousChainSpark, ...]:
        if end_ms < self.field.current_time_ms:
            raise ValueError("end_ms cannot move backwards")
        before = len(self.generated_sparks)
        while self.field._queue:  # noqa: SLF001 - retained Field event-loop adapter
            next_time = self.field._queue[0][0]  # noqa: SLF001
            if next_time > end_ms or (next_time == end_ms and not include_endpoint):
                break
            self._internal_step_count += 1
            if self._internal_step_count > self.config.maximum_internal_steps:
                raise RuntimeError("maximum_internal_steps exceeded")
            spikes = self.field.run_until(next_time)
            self._observe_spikes(spikes)
        if include_endpoint and self.field.current_time_ms < end_ms:
            self.field.run_until(end_ms)
        self.transition.expire_pending(end_ms)
        return tuple(self.generated_sparks[before:])

    def _observe_spikes(self, spikes: Iterable[SpikeEvent]) -> None:
        for spike in spikes:
            roots = self._proposal_roots(spike)
            spike_id = self._spike_id(spike)
            self._pulse_proposal_roots[spike_id] = frozenset(roots)
            if not roots:
                continue
            if len(self.generated_sparks) >= self.config.maximum_recorded_sparks:
                raise RuntimeError("maximum_recorded_sparks exceeded")
            proposals = tuple(self.ledger.proposals[root_id] for root_id in roots)
            parent_ids = tuple(
                sorted(
                    {
                        parent_id
                        for proposal in proposals
                        for parent_id in self._parent_ids_for(proposal.proposal_id)
                    }
                )
            )
            depth = max(proposal.generation_depth for proposal in proposals)
            self.generated_sparks.append(
                EndogenousChainSpark(
                    spark_id=spike_id,
                    time_ms=spike.time_ms,
                    unit_id=spike.unit_id,
                    generation_depth=depth,
                    proposal_ids=roots,
                    parent_proposal_ids=parent_ids,
                    source_pulse_ids=spike.source_pulse_ids,
                    external_observation_count=self.ledger.external_observation_count,
                    committed_positive_updates=self.ledger.committed_positive_updates,
                )
            )
            if spike_id in self._expanded_spike_ids:
                continue
            self._expanded_spike_ids.add(spike_id)
            if spike.unit_id in self.intervention.suppress_expansion_unit_ids:
                self.intervention_records.append(
                    EndogenousInterventionRecord(
                        stage="expansion",
                        reason="suppressed_expansion_unit",
                        source_event_id=spike_id,
                        source_unit_id=spike.unit_id,
                        proposal_id=None,
                        path_id=None,
                        generation_depth=depth,
                        time_ms=spike.time_ms,
                    )
                )
                continue
            for proposal in proposals:
                source_event = self.ledger.events[f"endo:{proposal.proposal_id}"]
                source = RuntimePulse(
                    event_id=f"endo:{proposal.proposal_id}",
                    time_ms=spike.time_ms,
                    target=f"unit:{spike.unit_id}",
                    magnitude=max(proposal.magnitude, spike.dynamic_threshold),
                    polarity=proposal.polarity,
                    origin=source_event.origin,
                    generation_depth=proposal.generation_depth,
                    parent_event_ids=source_event.parent_event_ids,
                    source_path_ids=source_event.source_path_ids,
                    metadata={
                        "derived_from_field_spark": True,
                        "origin_state_hash": proposal.origin_state_hash,
                    },
                )
                self._prepare_and_maybe_reinject(source)

    def _prepare_and_maybe_reinject(
        self,
        source: RuntimePulse,
    ) -> tuple[PreparedLocalTransition, ...]:
        prepared = self.transition.prepare(
            source,
            origin_state_hash=self.field.state_hash(),
        )
        for row in prepared:
            reason = self._reinjection_suppression_reason(row)
            decision = None
            if reason is None:
                decision = self.reinjection.schedule(row.proposal, self.field)
            else:
                self.intervention_records.append(
                    EndogenousInterventionRecord(
                        stage="reinjection",
                        reason=reason,
                        source_event_id=source.event_id,
                        source_unit_id=self._target_unit_id(source.target),
                        proposal_id=row.proposal.proposal_id,
                        path_id=row.path_id,
                        generation_depth=row.proposal.generation_depth,
                        time_ms=source.time_ms,
                    )
                )
            parent_proposal_ids = row.proposal.parent_proposal_ids
            if (
                not parent_proposal_ids
                and source.origin.is_endogenous
                and source.event_id.startswith("endo:")
            ):
                parent_proposal_ids = (source.event_id.removeprefix("endo:"),)
            self.proposal_records.append(
                EndogenousProposalRecord(
                    source_event_id=source.event_id,
                    source_origin=source.origin.value,
                    source_target=source.target,
                    source_time_ms=source.time_ms,
                    proposal_id=row.proposal.proposal_id,
                    parent_proposal_ids=parent_proposal_ids,
                    path_id=row.path_id,
                    target=row.proposal.target,
                    predicted_arrival_ms=row.proposal.predicted_arrival_ms,
                    generation_depth=row.proposal.generation_depth,
                    reinjection=decision,
                    intervention_reason=reason,
                )
            )
        return prepared

    def _reinjection_suppression_reason(
        self,
        row: PreparedLocalTransition,
    ) -> str | None:
        if row.path_id in self.intervention.suppress_reinjection_path_ids:
            return "suppressed_reinjection_path"
        if row.proposal.generation_depth in self.intervention.suppress_reinjection_depths:
            return "suppressed_reinjection_depth"
        return None

    def _parent_ids_for(self, proposal_id: str) -> tuple[str, ...]:
        for record in reversed(self.proposal_records):
            if record.proposal_id == proposal_id:
                return record.parent_proposal_ids
        return self.ledger.proposals[proposal_id].parent_proposal_ids

    def _proposal_roots(self, spike: SpikeEvent) -> tuple[str, ...]:
        roots: set[str] = set()
        for pulse_id in spike.source_pulse_ids:
            if pulse_id.startswith("endo:"):
                proposal_id = pulse_id.removeprefix("endo:")
                if proposal_id in self.ledger.proposals:
                    roots.add(proposal_id)
            roots.update(self._pulse_proposal_roots.get(pulse_id, ()))
        return tuple(sorted(roots))

    @staticmethod
    def _spike_id(spike: SpikeEvent) -> str:
        return digest(
            {
                "sources": list(spike.source_pulse_ids),
                "time_ms": spike.time_ms,
                "unit_id": spike.unit_id,
            }
        )[:20]

    @staticmethod
    def _target_unit_id(target: str) -> int:
        prefix = "unit:"
        if not target.startswith(prefix) or not target[len(prefix) :].isdigit():
            raise ValueError("target must use unit:<non-negative-int>")
        return int(target[len(prefix) :])

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
            "expanded_spike_ids": sorted(self._expanded_spike_ids),
            "external_event_ids": list(self.external_event_ids),
            "field": self.field.state_dict(),
            "generated_sparks": [row.state_dict() for row in self.generated_sparks],
            "internal_step_count": self._internal_step_count,
            "intervention": asdict(self.intervention),
            "intervention_records": [
                row.state_dict() for row in self.intervention_records
            ],
            "proposal_records": [row.state_dict() for row in self.proposal_records],
            "pulse_proposal_roots": {
                pulse_id: sorted(roots)
                for pulse_id, roots in sorted(self._pulse_proposal_roots.items())
            },
            "reinjection": self.reinjection.state_dict(),
            "transition": self.transition.state_dict(),
        }
        validate_runtime_mapping(value, path="v06.endogenous_chain")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())

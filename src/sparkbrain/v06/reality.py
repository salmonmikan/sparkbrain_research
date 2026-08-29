from __future__ import annotations

import heapq
import math
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

from .foundation import EventOrigin, ProvenanceLedger, RuntimePulse, digest, validate_runtime_mapping
from .local_transition import LocalTransitionResolution, SparseLocalTransitionAdaptation


@dataclass(frozen=True, slots=True)
class RealityCorrectionConfig:
    contradiction_window_ms: float = 8.0
    external_current_gain: float = 1.0
    maximum_external_current: float = 4.0
    cancel_competing_branches: bool = True

    def validate(self) -> None:
        for name in (
            "contradiction_window_ms",
            "external_current_gain",
            "maximum_external_current",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.contradiction_window_ms < 0:
            raise ValueError("contradiction_window_ms must be non-negative")
        if self.external_current_gain <= 0 or self.maximum_external_current <= 0:
            raise ValueError("external current limits must be positive")


@dataclass(frozen=True, slots=True)
class QueueCancellation:
    proposal_ids: tuple[str, ...]
    pulse_ids: tuple[str, ...]
    removed_arrivals: int
    field_state_hash_before: str
    field_state_hash_after: str


@dataclass(frozen=True, slots=True)
class RealityCorrectionResult:
    external_event_id: str
    matched_proposal_id: str | None
    contradicted_proposal_ids: tuple[str, ...]
    expired_proposal_ids: tuple[str, ...]
    unresolved_competing_proposal_ids: tuple[str, ...]
    cancelled_arrivals: int
    external_scheduled: bool
    field_state_hash_before: str
    field_state_hash_after: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class EndogenousLineageIndex:
    """Maps Field-generated pulse IDs back to endogenous proposal roots.

    The retained v0.4 Field hashes every emitted Spike into a new pulse ID for
    recurrent delivery. This runtime index reconstructs that hash and records
    which endogenous root proposal(s) contributed to each descendant pulse.
    It is not an Assembly observer and it participates only in provenance and
    stale-queue cancellation.
    """

    def __init__(self) -> None:
        self._pulse_roots: dict[str, frozenset[str]] = {}

    def observe_spikes(self, spikes: Iterable[SpikeEvent]) -> tuple[str, ...]:
        recorded: list[str] = []
        for spike in spikes:
            roots: set[str] = set()
            for source_pulse_id in spike.source_pulse_ids:
                if source_pulse_id.startswith("endo:"):
                    roots.add(source_pulse_id.removeprefix("endo:"))
                roots.update(self._pulse_roots.get(source_pulse_id, ()))
            spike_id = digest(
                {
                    "sources": list(spike.source_pulse_ids),
                    "time_ms": spike.time_ms,
                    "unit_id": spike.unit_id,
                }
            )[:20]
            self._pulse_roots[spike_id] = frozenset(roots)
            recorded.append(spike_id)
        return tuple(recorded)

    def pulse_ids_for(self, proposal_ids: Iterable[str]) -> frozenset[str]:
        roots = frozenset(proposal_ids)
        pulse_ids = {f"endo:{proposal_id}" for proposal_id in roots}
        for pulse_id, pulse_roots in self._pulse_roots.items():
            if roots.intersection(pulse_roots):
                pulse_ids.add(pulse_id)
        return frozenset(pulse_ids)

    def state_dict(self) -> dict[str, list[str]]:
        return {
            pulse_id: sorted(roots)
            for pulse_id, roots in sorted(self._pulse_roots.items())
        }


class RealityCorrectionEngine:
    """Makes external input authoritative over pending endogenous branches."""

    def __init__(
        self,
        transition_model: SparseLocalTransitionAdaptation,
        ledger: ProvenanceLedger,
        config: RealityCorrectionConfig | None = None,
        lineage: EndogenousLineageIndex | None = None,
    ) -> None:
        if transition_model.ledger is not ledger:
            raise ValueError("reality correction and G2 must share one provenance ledger")
        self.transition_model = transition_model
        self.ledger = ledger
        self.config = config or RealityCorrectionConfig()
        self.config.validate()
        self.lineage = lineage or EndogenousLineageIndex()
        self.external_processed_count = 0
        self.match_count = 0
        self.contradiction_count = 0
        self.expiration_count = 0
        self.cancelled_arrival_count = 0

    def observe_spikes(self, spikes: Iterable[SpikeEvent]) -> tuple[str, ...]:
        return self.lineage.observe_spikes(spikes)

    def process_external(
        self,
        external: RuntimePulse,
        field: TemporalExcitableField,
    ) -> RealityCorrectionResult:
        if external.origin is not EventOrigin.EXTERNAL:
            raise ValueError("reality correction accepts only external observations")
        if external.time_ms < field.current_time_ms:
            raise ValueError("external observation cannot arrive in the Field past")
        target_unit_id = self._target_unit_id(external.target)
        if target_unit_id not in field.units:
            raise KeyError(f"unknown external target unit: {target_unit_id}")
        existing = self.ledger.events.get(external.event_id)
        if existing is not None and existing != external:
            raise ValueError("external event ID is already registered with different content")
        if existing is not None:
            raise ValueError("external event was already processed")

        field_before = field.state_hash()
        pending_before = self._pending_proposal_ids()
        expired = self.transition_model.expire_pending(external.time_ms)
        due_ids = tuple(
            proposal_id
            for proposal_id in pending_before
            if proposal_id not in expired
            and proposal_id in self.transition_model.state_dict()["pending"]
            and abs(
                self.ledger.proposals[proposal_id].predicted_arrival_ms
                - external.time_ms
            )
            <= self.config.contradiction_window_ms
        )
        matching = tuple(
            proposal_id
            for proposal_id in due_ids
            if self._matches(self.ledger.proposals[proposal_id], external)
        )
        matched_id = min(matching, key=lambda row: self._match_score(row, external)) if matching else None

        contradicted: list[str] = []
        unresolved_competing: list[str] = []
        if matched_id is not None:
            origin_state_hash = self.ledger.proposals[matched_id].origin_state_hash
            for proposal_id in due_ids:
                if proposal_id == matched_id:
                    continue
                proposal = self.ledger.proposals[proposal_id]
                if (
                    self.config.cancel_competing_branches
                    and proposal.origin_state_hash == origin_state_hash
                ):
                    if self._matches(proposal, external):
                        unresolved_competing.append(proposal_id)
                    else:
                        contradicted.append(proposal_id)
        else:
            contradicted.extend(due_ids)

        cancellation_ids = tuple(
            dict.fromkeys((*expired, *contradicted, *unresolved_competing, *(matching or ())))
        )
        cancellation = self.cancel_proposals(cancellation_ids, field)

        if matched_id is not None:
            resolution = self.transition_model.resolve_external(matched_id, external)
            if not resolution.matched:
                raise RuntimeError("selected reality match did not satisfy G2 match contract")
            self.match_count += 1
        for proposal_id in contradicted:
            self._resolve_contradiction(proposal_id, external)
            self.contradiction_count += 1

        if external.event_id not in self.ledger.events:
            self.ledger.register_external(external)
        self._schedule_external(external, target_unit_id, field)
        self.external_processed_count += 1
        self.expiration_count += len(expired)
        self.cancelled_arrival_count += cancellation.removed_arrivals

        result = RealityCorrectionResult(
            external_event_id=external.event_id,
            matched_proposal_id=matched_id,
            contradicted_proposal_ids=tuple(contradicted),
            expired_proposal_ids=tuple(expired),
            unresolved_competing_proposal_ids=tuple(unresolved_competing),
            cancelled_arrivals=cancellation.removed_arrivals,
            external_scheduled=True,
            field_state_hash_before=field_before,
            field_state_hash_after=field.state_hash(),
        )
        validate_runtime_mapping(result.state_dict(), path="v06.reality.result")
        return result

    def cancel_proposals(
        self,
        proposal_ids: Iterable[str],
        field: TemporalExcitableField,
    ) -> QueueCancellation:
        ordered = tuple(dict.fromkeys(proposal_ids))
        before = field.state_hash()
        pulse_ids = self.lineage.pulse_ids_for(ordered)
        if not pulse_ids:
            return QueueCancellation(ordered, (), 0, before, before)
        kept = []
        removed = 0
        for item in field._queue:  # noqa: SLF001 - v0.6 adapter for retained field queue
            if item[2].pulse_id in pulse_ids:
                removed += 1
            else:
                kept.append(item)
        field._queue = kept  # noqa: SLF001 - preserve retained v0.4 state object
        heapq.heapify(field._queue)  # noqa: SLF001
        return QueueCancellation(
            proposal_ids=ordered,
            pulse_ids=tuple(sorted(pulse_ids)),
            removed_arrivals=removed,
            field_state_hash_before=before,
            field_state_hash_after=field.state_hash(),
        )

    def _pending_proposal_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self.transition_model.state_dict()["pending"]))

    def _matches(self, proposal: Any, external: RuntimePulse) -> bool:
        return (
            proposal.target == external.target
            and proposal.polarity == external.polarity
            and abs(proposal.predicted_arrival_ms - external.time_ms)
            <= self.transition_model.config.maximum_timing_error_ms
            and abs(proposal.magnitude - external.magnitude)
            <= self.transition_model.config.maximum_magnitude_error
        )

    def _match_score(self, proposal_id: str, external: RuntimePulse) -> tuple[float, float, str]:
        proposal = self.ledger.proposals[proposal_id]
        return (
            abs(proposal.predicted_arrival_ms - external.time_ms),
            abs(proposal.magnitude - external.magnitude),
            proposal_id,
        )

    def _resolve_contradiction(
        self,
        proposal_id: str,
        external: RuntimePulse,
    ) -> LocalTransitionResolution:
        proposal = self.ledger.proposals[proposal_id]
        if self._matches(proposal, external):
            raise ValueError("matching competing proposal cannot be forced into contradiction")
        return self.transition_model.resolve_external(proposal_id, external)

    def _schedule_external(
        self,
        external: RuntimePulse,
        target_unit_id: int,
        field: TemporalExcitableField,
    ) -> None:
        current = external.polarity * min(
            self.config.maximum_external_current,
            external.magnitude * self.config.external_current_gain,
        )
        field.schedule_arrival(
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

    @staticmethod
    def _target_unit_id(target: str) -> int:
        prefix = "unit:"
        if not target.startswith(prefix):
            raise ValueError("external target must use unit:<non-negative-int>")
        raw = target[len(prefix) :]
        if not raw or not raw.isdigit():
            raise ValueError("external target must use unit:<non-negative-int>")
        return int(raw)

    def state_dict(self) -> dict[str, Any]:
        value = {
            "cancelled_arrival_count": self.cancelled_arrival_count,
            "config": asdict(self.config),
            "contradiction_count": self.contradiction_count,
            "expiration_count": self.expiration_count,
            "external_processed_count": self.external_processed_count,
            "lineage": self.lineage.state_dict(),
            "match_count": self.match_count,
        }
        validate_runtime_mapping(value, path="v06.reality")
        return value

    def state_hash(self) -> str:
        return digest(self.state_dict())

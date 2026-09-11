"""Construction-only RD005 hidden-return gate reachability contract.

This module contains no model runner, task score, reward, route correctness, or
success-directed input.  It prepares the prospectively fixed E1/ES comparison
from one shared eligibility/return-event budget and certifies whether each
assigned hidden source can physically reach the inherited hidden-return commit
gate before any capability execution is opened.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Literal

RD005_PROTOCOL_ID = "rv02-rd005-gate-reachable-hidden-eligibility-v1"
INHERITED_MINIMUM_LAG_MS = 0.5
INHERITED_MAXIMUM_LAG_MS = 6.5

RD005Arm = Literal["E1", "ES"]


def _finite(value: float, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


@dataclass(frozen=True, slots=True)
class EligibilityEvent:
    event_id: str
    observed_source_id: int
    time_ms: float

    def validate(self) -> None:
        if not self.event_id:
            raise ValueError("eligibility event_id must be non-empty")
        _finite(self.time_ms, name="eligibility time_ms")


@dataclass(frozen=True, slots=True)
class ExternalReturnEvent:
    event_id: str
    eligibility_event_id: str
    target_id: int
    time_ms: float
    outcome_blind: bool = True

    def validate(self) -> None:
        if not self.event_id or not self.eligibility_event_id:
            raise ValueError("return event identities must be non-empty")
        _finite(self.time_ms, name="return time_ms")
        if self.outcome_blind is not True:
            raise ValueError("RD005 return generation must be outcome-blind")


@dataclass(frozen=True, slots=True)
class ConnectionSnapshot:
    source_id: int
    target_id: int
    plastic: bool
    initial_weight: float

    def validate(self) -> None:
        _finite(self.initial_weight, name="connection initial_weight")


@dataclass(frozen=True, slots=True)
class GateReachabilityCertificate:
    arm: RD005Arm
    eligibility_event_id: str
    return_event_id: str
    observed_source_id: int
    assigned_source_id: int
    target_id: int
    trace_time_ms: float
    return_time_ms: float
    lag_ms: float
    lag_in_window: bool
    edge_exists: bool
    edge_plastic: bool
    nonnegative_initial_weight: bool
    outcome_blind: bool

    @property
    def reachable(self) -> bool:
        return (
            self.lag_in_window
            and self.edge_exists
            and self.edge_plastic
            and self.nonnegative_initial_weight
            and self.outcome_blind
        )

    def state_dict(self) -> dict[str, object]:
        row = asdict(self)
        row["reachable"] = self.reachable
        return row


@dataclass(frozen=True, slots=True)
class GateConstructionSummary:
    protocol_id: str
    eligibility_event_count: int
    return_event_count: int
    e1_reachable_count: int
    es_reachable_count: int
    shared_budget_sha256: str

    @property
    def e1_construction_ready(self) -> bool:
        return self.e1_reachable_count > 0


class RD005GateConstruction:
    """Fail-closed, capability-free E1/ES gate construction.

    E1 and ES necessarily share the same immutable eligibility events and
    external-return events.  Their sole permitted difference is the hidden
    source assignment used while evaluating the same prospective gate.
    """

    def __init__(
        self,
        *,
        eligibility_events: tuple[EligibilityEvent, ...],
        return_events: tuple[ExternalReturnEvent, ...],
        connections: tuple[ConnectionSnapshot, ...],
        shuffled_assignment: dict[int, int],
    ) -> None:
        self.eligibility_events = tuple(eligibility_events)
        self.return_events = tuple(return_events)
        self.connections = tuple(connections)
        self.shuffled_assignment = {
            int(source): int(target)
            for source, target in shuffled_assignment.items()
        }
        self._validate()

    def _validate(self) -> None:
        if not self.eligibility_events:
            raise ValueError("RD005 requires a non-empty eligibility event budget")
        if not self.return_events:
            raise ValueError("RD005 requires a non-empty external-return event budget")

        eligibility_ids: set[str] = set()
        observed_sources: set[int] = set()
        for event in self.eligibility_events:
            event.validate()
            if event.event_id in eligibility_ids:
                raise ValueError("duplicate eligibility event_id")
            eligibility_ids.add(event.event_id)
            observed_sources.add(int(event.observed_source_id))

        return_ids: set[str] = set()
        for event in self.return_events:
            event.validate()
            if event.event_id in return_ids:
                raise ValueError("duplicate return event_id")
            if event.eligibility_event_id not in eligibility_ids:
                raise ValueError("return event references unknown eligibility event")
            return_ids.add(event.event_id)

        edge_keys: set[tuple[int, int]] = set()
        for edge in self.connections:
            edge.validate()
            key = (int(edge.source_id), int(edge.target_id))
            if key in edge_keys:
                raise ValueError("duplicate connection snapshot")
            edge_keys.add(key)

        if set(self.shuffled_assignment) != observed_sources:
            raise ValueError(
                "ES assignment keys must equal the observed hidden-source inventory"
            )
        if set(self.shuffled_assignment.values()) != observed_sources:
            raise ValueError("ES assignment must be a bijection over hidden sources")
        if any(
            source == target
            for source, target in self.shuffled_assignment.items()
        ):
            raise ValueError("ES assignment must not preserve a hidden identity")

    @property
    def shared_budget_sha256(self) -> str:
        material = {
            "protocol_id": RD005_PROTOCOL_ID,
            "eligibility_events": [asdict(row) for row in self.eligibility_events],
            "return_events": [asdict(row) for row in self.return_events],
        }
        payload = json.dumps(
            material,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def _assignment_for(self, arm: RD005Arm) -> dict[int, int]:
        if arm == "E1":
            return {
                source: source
                for source in sorted(self.shuffled_assignment)
            }
        if arm == "ES":
            return dict(self.shuffled_assignment)
        raise ValueError("RD005 arm must be E1 or ES")

    def certificates(self, arm: RD005Arm) -> tuple[GateReachabilityCertificate, ...]:
        assignment = self._assignment_for(arm)
        traces = {row.event_id: row for row in self.eligibility_events}
        edges = {
            (int(row.source_id), int(row.target_id)): row
            for row in self.connections
        }
        certificates: list[GateReachabilityCertificate] = []
        for gate in self.return_events:
            trace = traces[gate.eligibility_event_id]
            assigned_source = assignment[int(trace.observed_source_id)]
            edge = edges.get((assigned_source, int(gate.target_id)))
            lag = float(gate.time_ms) - float(trace.time_ms)
            certificates.append(
                GateReachabilityCertificate(
                    arm=arm,
                    eligibility_event_id=trace.event_id,
                    return_event_id=gate.event_id,
                    observed_source_id=int(trace.observed_source_id),
                    assigned_source_id=assigned_source,
                    target_id=int(gate.target_id),
                    trace_time_ms=float(trace.time_ms),
                    return_time_ms=float(gate.time_ms),
                    lag_ms=lag,
                    lag_in_window=(
                        INHERITED_MINIMUM_LAG_MS
                        <= lag
                        <= INHERITED_MAXIMUM_LAG_MS
                    ),
                    edge_exists=edge is not None,
                    edge_plastic=(edge is not None and bool(edge.plastic)),
                    nonnegative_initial_weight=(
                        edge is not None and float(edge.initial_weight) >= 0.0
                    ),
                    outcome_blind=gate.outcome_blind,
                )
            )
        return tuple(certificates)

    def summary(self) -> GateConstructionSummary:
        e1 = self.certificates("E1")
        es = self.certificates("ES")
        return GateConstructionSummary(
            protocol_id=RD005_PROTOCOL_ID,
            eligibility_event_count=len(self.eligibility_events),
            return_event_count=len(self.return_events),
            e1_reachable_count=sum(row.reachable for row in e1),
            es_reachable_count=sum(row.reachable for row in es),
            shared_budget_sha256=self.shared_budget_sha256,
        )

    def assert_development_matrix_reachable(self) -> GateConstructionSummary:
        """Apply preregistered D1 before any capability runner may exist."""

        summary = self.summary()
        if not summary.e1_construction_ready:
            raise RuntimeError(
                "RD005 D1 failed: no prospectively reachable E1 hidden-return gate"
            )
        return summary


__all__ = [
    "ConnectionSnapshot",
    "EligibilityEvent",
    "ExternalReturnEvent",
    "GateConstructionSummary",
    "GateReachabilityCertificate",
    "INHERITED_MAXIMUM_LAG_MS",
    "INHERITED_MINIMUM_LAG_MS",
    "RD005GateConstruction",
    "RD005_PROTOCOL_ID",
]

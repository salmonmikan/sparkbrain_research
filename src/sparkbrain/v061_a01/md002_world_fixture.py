"""Prospective anonymous world fixture for A01 MD-002 P2; execution disabled.

P2 must change the external world mapping rather than selecting a credited local
path inside the evaluator. This module fixes the smallest external contract: a
separated BoundaryEvent carries exactly one anonymous proposal ID, the world maps
that ID to an anonymous external target, and paired control/intervention responses
share one response identity and clock. The fixture never reads local path IDs,
support scores, competition outcomes, or evaluator truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sparkbrain.v06.boundary import BoundaryEvent
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, validate_runtime_mapping


@dataclass(frozen=True, slots=True)
class P2WorldResponseSchedule:
    """Arm-invariant identity and timing for one paired P2 world response."""

    event_id: str
    time_ms: float

    def validate(self, boundary: BoundaryEvent) -> None:
        if type(self.event_id) is not str or not self.event_id:
            raise ValueError("P2 external response event ID must be a non-empty string")
        if type(self.time_ms) not in (int, float):
            raise ValueError("P2 external response time must be numeric")
        if float(self.time_ms) <= boundary.time_ms:
            raise ValueError("P2 external response must occur after its BoundaryEvent")


@dataclass(frozen=True, slots=True)
class P2AnonymousWorldRelation:
    """A two-key anonymous response map used by one P2 world arm."""

    responses: tuple[tuple[str, str], ...]

    def validate(self) -> None:
        if len(self.responses) != 2:
            raise ValueError("P2 world relation requires exactly two response rows")
        for row in self.responses:
            if not isinstance(row, tuple) or len(row) != 2:
                raise ValueError("P2 world relation rows must be two-item tuples")
            key, target = row
            if type(key) is not str or type(target) is not str:
                raise ValueError("P2 world relation identifiers must be strings")
            if not key or not target:
                raise ValueError("P2 world relation identifiers must be non-empty")
        keys = tuple(key for key, _ in self.responses)
        targets = tuple(target for _, target in self.responses)
        if len(set(keys)) != 2:
            raise ValueError("P2 world relation proposal keys must be unique")
        if len(set(targets)) != 2:
            raise ValueError("P2 world relation external targets must be unique")
        if tuple(sorted(self.responses)) != self.responses:
            raise ValueError("P2 world relation rows must use canonical key order")
        validate_runtime_mapping(self.state_dict(), path="v061_a01.md002.world_relation")

    @property
    def mapping(self) -> dict[str, str]:
        self.validate()
        return dict(self.responses)

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": "v061-a01-md002-p2-anonymous-world-v1",
            "responses": [
                {"proposal_id": proposal_id, "external_target": target}
                for proposal_id, target in self.responses
            ],
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> P2AnonymousWorldRelation:
        if not isinstance(value, dict) or value.get("schema") != "v061-a01-md002-p2-anonymous-world-v1":
            raise ValueError("invalid P2 world relation schema")
        rows = value.get("responses")
        if not isinstance(rows, list):
            raise ValueError("P2 world relation responses must be a list")
        relation = cls(
            responses=tuple(
                (row.get("proposal_id"), row.get("external_target"))
                if isinstance(row, dict)
                else (None, None)
                for row in rows
            )
        )
        relation.validate()
        return relation

    def _respond(
        self,
        boundary: BoundaryEvent,
        schedule: P2WorldResponseSchedule,
    ) -> RuntimePulse:
        self.validate()
        schedule.validate(boundary)
        if len(boundary.source_proposal_ids) != 1:
            raise ValueError("P2 separated world arm requires exactly one source proposal")
        proposal_id = boundary.source_proposal_ids[0]
        if type(proposal_id) is not str or not proposal_id:
            raise ValueError("P2 BoundaryEvent proposal ID must be a non-empty string")
        try:
            target = self.mapping[proposal_id]
        except KeyError as exc:
            raise ValueError("P2 BoundaryEvent proposal is absent from the world relation") from exc
        return RuntimePulse(
            event_id=schedule.event_id,
            time_ms=float(schedule.time_ms),
            target=target,
            magnitude=float(boundary.magnitude),
            polarity=int(boundary.polarity),
            origin=EventOrigin.EXTERNAL,
            parent_event_ids=(boundary.event_id,),
        )


@dataclass(frozen=True, slots=True)
class P2AnonymousWorldPermutation:
    """Control/intervention pair with the same keys/targets and opposite assignment."""

    control: P2AnonymousWorldRelation
    intervention: P2AnonymousWorldRelation

    def validate(self) -> None:
        self.control.validate()
        self.intervention.validate()
        control = self.control.mapping
        intervention = self.intervention.mapping
        if set(control) != set(intervention):
            raise ValueError("P2 world arms must use identical anonymous proposal keys")
        if set(control.values()) != set(intervention.values()):
            raise ValueError("P2 world arms must use identical external target inventory")
        if any(control[key] == intervention[key] for key in control):
            raise ValueError("P2 intervention must reverse every registered response assignment")

    @staticmethod
    def _require_matched_boundary(control: BoundaryEvent, intervention: BoundaryEvent) -> None:
        invariant_fields = (
            "event_id",
            "time_ms",
            "port_id",
            "magnitude",
            "polarity",
            "direction",
            "source_spark_id",
            "source_unit_id",
            "source_proposal_ids",
            "generation_depth",
            "source_state_hash",
        )
        drifted = [
            name
            for name in invariant_fields
            if getattr(control, name) != getattr(intervention, name)
        ]
        if drifted:
            raise ValueError(f"P2 paired BoundaryEvents differ outside world relation: {drifted}")

    def respond_pair(
        self,
        control_boundary: BoundaryEvent,
        intervention_boundary: BoundaryEvent,
        *,
        schedule: P2WorldResponseSchedule,
    ) -> tuple[RuntimePulse, RuntimePulse]:
        """Generate both arms under one immutable event identity and response clock."""

        self.validate()
        self._require_matched_boundary(control_boundary, intervention_boundary)
        schedule.validate(control_boundary)
        return (
            self.control._respond(control_boundary, schedule),
            self.intervention._respond(intervention_boundary, schedule),
        )

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": "v061-a01-md002-p2-world-permutation-v1",
            "control": self.control.state_dict(),
            "intervention": self.intervention.state_dict(),
        }


__all__ = [
    "P2AnonymousWorldPermutation",
    "P2AnonymousWorldRelation",
    "P2WorldResponseSchedule",
]

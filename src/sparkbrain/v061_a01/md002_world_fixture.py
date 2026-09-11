"""Prospective anonymous world fixture for A01 MD-002 P2; execution disabled.

P2 must change the external world mapping rather than selecting a credited local
path inside the evaluator. This module fixes the smallest external contract: a
separated BoundaryEvent carries exactly one anonymous proposal ID, the world maps
that ID to an anonymous external target, and the generated RuntimePulse names the
BoundaryEvent as its exact external parent. The fixture never reads local path
IDs, support scores, competition outcomes, or evaluator truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sparkbrain.v06.boundary import BoundaryEvent
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, validate_runtime_mapping


@dataclass(frozen=True, slots=True)
class P2AnonymousWorldRelation:
    """A two-key anonymous response map used by one P2 world arm."""

    responses: tuple[tuple[str, str], ...]

    def validate(self) -> None:
        if len(self.responses) != 2:
            raise ValueError("P2 world relation requires exactly two response rows")
        keys = tuple(str(key) for key, _ in self.responses)
        targets = tuple(str(target) for _, target in self.responses)
        if any(not value for value in (*keys, *targets)):
            raise ValueError("P2 world relation identifiers must be non-empty")
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
        return {
            "schema": "v061-a01-md002-p2-anonymous-world-v1",
            "responses": [
                {"proposal_id": proposal_id, "external_target": target}
                for proposal_id, target in self.responses
            ],
        }

    def respond(
        self,
        boundary: BoundaryEvent,
        *,
        event_id: str,
        time_ms: float,
    ) -> RuntimePulse:
        """Generate one exact-parent external response without evaluator input."""

        self.validate()
        if not event_id:
            raise ValueError("P2 external response event ID must be non-empty")
        if time_ms <= boundary.time_ms:
            raise ValueError("P2 external response must occur after its BoundaryEvent")
        if len(boundary.source_proposal_ids) != 1:
            raise ValueError("P2 separated world arm requires exactly one source proposal")
        proposal_id = boundary.source_proposal_ids[0]
        try:
            target = self.mapping[proposal_id]
        except KeyError as exc:
            raise ValueError("P2 BoundaryEvent proposal is absent from the world relation") from exc
        return RuntimePulse(
            event_id=event_id,
            time_ms=float(time_ms),
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

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": "v061-a01-md002-p2-world-permutation-v1",
            "control": self.control.state_dict(),
            "intervention": self.intervention.state_dict(),
        }


__all__ = ["P2AnonymousWorldPermutation", "P2AnonymousWorldRelation"]

"""Execution-disabled schedule contract for A01 MD-002 P2.

The schedule fixes the cloned-attribution structure required by the prospective
MD-002 design before any capability runner exists. It deliberately contains no
local-path label or expected outcome: the anonymous world relation decides the
returned target, while the A01 bridge must recover causal paths from retained
proposal ancestry at execution time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class P2AttributionSubepisode:
    proposal_id: str
    boundary_event_id: str
    response_event_id: str
    boundary_time_ms: float
    response_time_ms: float

    def validate(self) -> None:
        for name in ("proposal_id", "boundary_event_id", "response_event_id"):
            value = getattr(self, name)
            if type(value) is not str or not value:
                raise ValueError(f"P2 {name} must be a non-empty string")
        for name in ("boundary_time_ms", "response_time_ms"):
            value = getattr(self, name)
            if type(value) not in (int, float):
                raise ValueError(f"P2 {name} must be numeric")
            if float(value) < 0.0:
                raise ValueError(f"P2 {name} must be non-negative")
        if float(self.response_time_ms) <= float(self.boundary_time_ms):
            raise ValueError("P2 response must occur after its BoundaryEvent")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "proposal_id": self.proposal_id,
            "boundary_event_id": self.boundary_event_id,
            "response_event_id": self.response_event_id,
            "boundary_time_ms": float(self.boundary_time_ms),
            "response_time_ms": float(self.response_time_ms),
        }


@dataclass(frozen=True, slots=True)
class P2SharedProbeSchedule:
    cue_event_id: str
    cue_time_ms: float
    root_target: str
    origin_state_hash: str

    def validate(self) -> None:
        for name in ("cue_event_id", "root_target", "origin_state_hash"):
            value = getattr(self, name)
            if type(value) is not str or not value:
                raise ValueError(f"P2 shared probe {name} must be non-empty")
        if type(self.cue_time_ms) not in (int, float) or float(self.cue_time_ms) < 0.0:
            raise ValueError("P2 shared probe time must be non-negative numeric")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "cue_event_id": self.cue_event_id,
            "cue_time_ms": float(self.cue_time_ms),
            "root_target": self.root_target,
            "origin_state_hash": self.origin_state_hash,
        }


@dataclass(frozen=True, slots=True)
class P2ClonedSubepisodeSchedule:
    """One outcome-blind schedule shared by W0/W1 and withheld controls."""

    subepisodes: tuple[P2AttributionSubepisode, P2AttributionSubepisode]
    shared_probe: P2SharedProbeSchedule

    def validate(self) -> None:
        if len(self.subepisodes) != 2:
            raise ValueError("P2 requires exactly two cloned attribution subepisodes")
        for row in self.subepisodes:
            row.validate()
        proposal_ids = tuple(row.proposal_id for row in self.subepisodes)
        if len(set(proposal_ids)) != 2:
            raise ValueError("P2 attribution subepisodes require distinct proposal identities")
        boundary_ids = tuple(row.boundary_event_id for row in self.subepisodes)
        response_ids = tuple(row.response_event_id for row in self.subepisodes)
        if len(set(boundary_ids)) != 2 or len(set(response_ids)) != 2:
            raise ValueError("P2 attribution subepisodes require distinct event identities")
        # Each attribution arm is restored from the same checkpoint, so their
        # relative clocks must be identical rather than serially ordered.
        boundary_times = {float(row.boundary_time_ms) for row in self.subepisodes}
        response_times = {float(row.response_time_ms) for row in self.subepisodes}
        if len(boundary_times) != 1 or len(response_times) != 1:
            raise ValueError("P2 cloned attribution subepisodes must use matched clocks")
        self.shared_probe.validate()
        if float(self.shared_probe.cue_time_ms) <= max(response_times):
            raise ValueError("P2 shared-root probe must occur after attribution response")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": "v061-a01-md002-p2-cloned-subepisode-schedule-v1",
            "subepisodes": [row.state_dict() for row in self.subepisodes],
            "shared_probe": self.shared_probe.state_dict(),
        }


def build_p2_condition_matrix(
    schedule: P2ClonedSubepisodeSchedule,
) -> tuple[dict[str, Any], ...]:
    """Return the exact four registered P2 conditions without outcome fields."""

    schedule.validate()
    schedule_state = schedule.state_dict()
    return tuple(
        {
            "condition_id": condition_id,
            "world_arm": world_arm,
            "returned_external_evidence": returned_external_evidence,
            "schedule": schedule_state,
        }
        for condition_id, world_arm, returned_external_evidence in (
            ("p2-w0-returned", "control", True),
            ("p2-w1-returned", "intervention", True),
            ("p2-w0-withheld", "control", False),
            ("p2-w1-withheld", "intervention", False),
        )
    )


__all__ = [
    "P2AttributionSubepisode",
    "P2ClonedSubepisodeSchedule",
    "P2SharedProbeSchedule",
    "build_p2_condition_matrix",
]

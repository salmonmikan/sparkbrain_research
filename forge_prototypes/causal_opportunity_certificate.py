"""Non-evidentiary treatment-to-readout causal-opportunity certificates.

This Forge prototype checks only whether a recorded, time-respecting event path
exists from a treated actor to a declared readout.  A certificate is a necessary
precondition for interpreting some null interventions; it is not an estimate or
proof of causal effect.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


class OpportunityStatus(StrEnum):
    """Result classes for a causal-opportunity check."""

    CERTIFIED = "CERTIFIED"
    NO_TREATED_ACTIVITY = "NO_TREATED_ACTIVITY"
    NO_PATH_TO_READOUT = "NO_PATH_TO_READOUT"
    INCOMPLETE_TRACE = "INCOMPLETE_TRACE"
    INVALID_TRACE = "INVALID_TRACE"


@dataclass(frozen=True, order=True)
class EventClock:
    """A deterministic event order, including events at the same timestamp."""

    time: float
    sequence: int = 0


@dataclass(frozen=True)
class TraceEvent:
    """One observed event that may carry treatment-dependent state."""

    event_id: str
    actor_id: str
    clock: EventClock
    state_bearing: bool = True


@dataclass(frozen=True)
class InfluenceEdge:
    """A directly traced influence from one event to a later event."""

    source_event_id: str
    target_event_id: str


@dataclass(frozen=True)
class Intervention:
    """The actors and earliest event order affected by an intervention."""

    target_actor_ids: frozenset[str]
    applied_at: EventClock


@dataclass(frozen=True)
class OpportunityAssessment:
    """A bounded reachability result with an optional witness path."""

    status: OpportunityStatus
    path: tuple[str, ...] = ()
    treated_seed_events: tuple[str, ...] = ()
    reason: str = ""
    establishes_causal_effect: bool = False


def certify_causal_opportunity(
    *,
    events: Iterable[TraceEvent],
    influence_edges: Iterable[InfluenceEdge],
    intervention: Intervention,
    readout_event_ids: Iterable[str],
    trace_complete: bool,
) -> OpportunityAssessment:
    """Return a deterministic treatment-to-readout event-path certificate.

    All influence edges must reference known events and move forward in the
    ``(time, sequence)`` order.  Incomplete traces fail closed because absence of
    a recorded path is not informative when the relevant edge surface is missing.
    """

    event_list = tuple(events)
    event_by_id = {event.event_id: event for event in event_list}
    if len(event_by_id) != len(event_list):
        return _invalid("duplicate event_id")
    if not intervention.target_actor_ids:
        return _invalid("intervention has no target actors")

    readouts = frozenset(readout_event_ids)
    if not readouts:
        return _invalid("no readout events declared")
    missing_readouts = sorted(readouts - event_by_id.keys())
    if missing_readouts:
        return _invalid(f"unknown readout events: {missing_readouts}")

    adjacency: dict[str, set[str]] = {event_id: set() for event_id in event_by_id}
    for edge in influence_edges:
        source = event_by_id.get(edge.source_event_id)
        target = event_by_id.get(edge.target_event_id)
        if source is None or target is None:
            return _invalid(
                "influence edge references an unknown event: "
                f"{edge.source_event_id}->{edge.target_event_id}"
            )
        if target.clock <= source.clock:
            return _invalid(
                "influence edge is not forward in event order: "
                f"{edge.source_event_id}->{edge.target_event_id}"
            )
        adjacency[source.event_id].add(target.event_id)

    if not trace_complete:
        return OpportunityAssessment(
            status=OpportunityStatus.INCOMPLETE_TRACE,
            reason="trace surface is declared incomplete; absence of a path is non-diagnostic",
        )

    seeds = tuple(
        sorted(
            event.event_id
            for event in event_list
            if event.actor_id in intervention.target_actor_ids
            and event.clock >= intervention.applied_at
            and event.state_bearing
        )
    )
    if not seeds:
        return OpportunityAssessment(
            status=OpportunityStatus.NO_TREATED_ACTIVITY,
            reason="no post-intervention state-bearing event was recorded for a treated actor",
        )

    path = _shortest_path(seeds=seeds, readouts=readouts, adjacency=adjacency)
    if path is None:
        return OpportunityAssessment(
            status=OpportunityStatus.NO_PATH_TO_READOUT,
            treated_seed_events=seeds,
            reason="treated activity exists but has no traced path to a declared readout",
        )

    return OpportunityAssessment(
        status=OpportunityStatus.CERTIFIED,
        path=path,
        treated_seed_events=seeds,
        reason="a time-respecting traced path connects treated activity to the readout",
    )


def _shortest_path(
    *,
    seeds: tuple[str, ...],
    readouts: frozenset[str],
    adjacency: dict[str, set[str]],
) -> tuple[str, ...] | None:
    queue: deque[str] = deque(seeds)
    parent: dict[str, str | None] = {seed: None for seed in seeds}

    while queue:
        current = queue.popleft()
        if current in readouts:
            return _reconstruct_path(current, parent)
        for target in sorted(adjacency[current]):
            if target not in parent:
                parent[target] = current
                queue.append(target)
    return None


def _reconstruct_path(end: str, parent: dict[str, str | None]) -> tuple[str, ...]:
    reversed_path = [end]
    cursor = parent[end]
    while cursor is not None:
        reversed_path.append(cursor)
        cursor = parent[cursor]
    return tuple(reversed(reversed_path))


def _invalid(reason: str) -> OpportunityAssessment:
    return OpportunityAssessment(status=OpportunityStatus.INVALID_TRACE, reason=reason)

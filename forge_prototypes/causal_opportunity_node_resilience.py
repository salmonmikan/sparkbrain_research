"""Internal-event resilience for causal-opportunity trace certificates.

This non-evidentiary Forge prototype counts internally event-disjoint traced
routes after the base certificate succeeds. It does not estimate causal effect
or establish that the caller-supplied trace is complete.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from forge_prototypes.causal_opportunity_certificate import (
    InfluenceEdge,
    Intervention,
    OpportunityAssessment,
    OpportunityStatus,
    TraceEvent,
    certify_causal_opportunity,
)


class NodeResilienceStatus(StrEnum):
    """Result classes for internal-event route resilience."""

    REDUNDANT_INTERNAL_EVENTS = "REDUNDANT_INTERNAL_EVENTS"
    SINGLE_INTERNAL_EVENT_FRAGILE = "SINGLE_INTERNAL_EVENT_FRAGILE"
    DIRECT_BYPASS = "DIRECT_BYPASS"
    DIRECT_READOUT = "DIRECT_READOUT"
    NOT_CERTIFIED = "NOT_CERTIFIED"


@dataclass(frozen=True)
class NodeResilienceAssessment:
    """Internally event-disjoint path count and deterministic relay-event cut."""

    status: NodeResilienceStatus
    opportunity: OpportunityAssessment
    internally_event_disjoint_path_count: int = 0
    minimum_internal_event_cut: tuple[str, ...] = ()
    reason: str = ""
    establishes_causal_effect: bool = False
    establishes_trace_completeness: bool = False


def assess_causal_opportunity_node_resilience(
    *,
    events: Iterable[TraceEvent],
    influence_edges: Iterable[InfluenceEdge],
    intervention: Intervention,
    readout_event_ids: Iterable[str],
    trace_complete: bool,
) -> NodeResilienceAssessment:
    """Measure relay-event redundancy after a base opportunity is certified.

    Each internal event is split into unit-capacity input/output nodes. Treated
    seed and readout events are terminals and therefore not eligible cut members.
    A direct seed-to-readout edge is reported separately because no internal
    event cut can block it.
    """

    event_list = tuple(events)
    edge_list = tuple(influence_edges)
    readouts = frozenset(readout_event_ids)
    opportunity = certify_causal_opportunity(
        events=event_list,
        influence_edges=edge_list,
        intervention=intervention,
        readout_event_ids=readouts,
        trace_complete=trace_complete,
    )
    if opportunity.status is not OpportunityStatus.CERTIFIED:
        return NodeResilienceAssessment(
            status=NodeResilienceStatus.NOT_CERTIFIED,
            opportunity=opportunity,
            reason="base causal-opportunity certificate was not established",
        )

    seeds = frozenset(opportunity.treated_seed_events)
    if seeds & readouts:
        return NodeResilienceAssessment(
            status=NodeResilienceStatus.DIRECT_READOUT,
            opportunity=opportunity,
            reason="a treated state-bearing event is itself a declared readout",
        )

    unique_edges = tuple(
        sorted(set(edge_list), key=lambda edge: (edge.source_event_id, edge.target_event_id))
    )
    if any(
        edge.source_event_id in seeds and edge.target_event_id in readouts
        for edge in unique_edges
    ):
        return NodeResilienceAssessment(
            status=NodeResilienceStatus.DIRECT_BYPASS,
            opportunity=opportunity,
            reason="a direct treated-seed to readout edge has no removable internal event",
        )

    path_count, reachable = _maximum_internally_event_disjoint_paths(
        event_ids=tuple(sorted(event.event_id for event in event_list)),
        edges=unique_edges,
        seeds=tuple(sorted(seeds)),
        readouts=tuple(sorted(readouts)),
    )
    terminals = seeds | readouts
    minimum_cut = tuple(
        event_id
        for event_id in sorted(event.event_id for event in event_list)
        if event_id not in terminals
        and _node(event_id, "in") in reachable
        and _node(event_id, "out") not in reachable
    )
    status = (
        NodeResilienceStatus.REDUNDANT_INTERNAL_EVENTS
        if path_count >= 2
        else NodeResilienceStatus.SINGLE_INTERNAL_EVENT_FRAGILE
    )
    return NodeResilienceAssessment(
        status=status,
        opportunity=opportunity,
        internally_event_disjoint_path_count=path_count,
        minimum_internal_event_cut=minimum_cut,
        reason=(
            "at least two internally event-disjoint traced opportunity paths exist"
            if path_count >= 2
            else "all traced opportunity paths share a one-event internal cut"
        ),
    )


def _maximum_internally_event_disjoint_paths(
    *,
    event_ids: tuple[str, ...],
    edges: tuple[InfluenceEdge, ...],
    seeds: tuple[str, ...],
    readouts: tuple[str, ...],
) -> tuple[int, frozenset[str]]:
    source = ("__forge_super_source__", "terminal")
    sink = ("__forge_super_sink__", "terminal")
    high_capacity = max(1, len(edges) + 1)
    capacity: dict[tuple[tuple[str, str], tuple[str, str]], int] = {}
    adjacency: dict[tuple[str, str], set[tuple[str, str]]] = {source: set(), sink: set()}
    terminals = frozenset((*seeds, *readouts))

    def add_arc(start: tuple[str, str], end: tuple[str, str], value: int) -> None:
        capacity[start, end] = capacity.get((start, end), 0) + value
        capacity.setdefault((end, start), 0)
        adjacency.setdefault(start, set()).add(end)
        adjacency.setdefault(end, set()).add(start)

    for event_id in event_ids:
        add_arc(
            _node(event_id, "in"),
            _node(event_id, "out"),
            high_capacity if event_id in terminals else 1,
        )
    for edge in edges:
        add_arc(
            _node(edge.source_event_id, "out"),
            _node(edge.target_event_id, "in"),
            high_capacity,
        )
    for seed in seeds:
        add_arc(source, _node(seed, "in"), high_capacity)
    for readout in readouts:
        add_arc(_node(readout, "out"), sink, high_capacity)

    residual = dict(capacity)
    flow = 0
    while True:
        parent = _augmenting_path(source=source, sink=sink, adjacency=adjacency, residual=residual)
        if sink not in parent:
            break
        bottleneck = high_capacity
        cursor = sink
        while cursor != source:
            previous = parent[cursor]
            bottleneck = min(bottleneck, residual[previous, cursor])
            cursor = previous
        cursor = sink
        while cursor != source:
            previous = parent[cursor]
            residual[previous, cursor] -= bottleneck
            residual[cursor, previous] += bottleneck
            cursor = previous
        flow += bottleneck

    reachable = _residual_reachable(source=source, adjacency=adjacency, residual=residual)
    return flow, frozenset(reachable)


def _node(event_id: str, side: str) -> tuple[str, str]:
    return event_id, side


def _augmenting_path(
    *,
    source: tuple[str, str],
    sink: tuple[str, str],
    adjacency: dict[tuple[str, str], set[tuple[str, str]]],
    residual: dict[tuple[tuple[str, str], tuple[str, str]], int],
) -> dict[tuple[str, str], tuple[str, str]]:
    parent: dict[tuple[str, str], tuple[str, str]] = {}
    seen = {source}
    queue: deque[tuple[str, str]] = deque([source])
    while queue and sink not in seen:
        current = queue.popleft()
        for target in sorted(adjacency[current]):
            if target not in seen and residual[current, target] > 0:
                seen.add(target)
                parent[target] = current
                queue.append(target)
    return parent


def _residual_reachable(
    *,
    source: tuple[str, str],
    adjacency: dict[tuple[str, str], set[tuple[str, str]]],
    residual: dict[tuple[tuple[str, str], tuple[str, str]], int],
) -> set[tuple[str, str]]:
    seen = {source}
    queue: deque[tuple[str, str]] = deque([source])
    while queue:
        current = queue.popleft()
        for target in sorted(adjacency[current]):
            if target not in seen and residual[current, target] > 0:
                seen.add(target)
                queue.append(target)
    return seen

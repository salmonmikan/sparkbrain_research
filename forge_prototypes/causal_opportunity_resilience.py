"""Bounded resilience diagnostics for causal-opportunity certificates.

This non-evidentiary Forge prototype measures how many edge-disjoint traced
routes connect treated activity to a declared readout. It does not estimate a
causal effect or establish that the supplied trace is complete.
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


class ResilienceStatus(StrEnum):
    """Result classes for certificate-path resilience."""

    REDUNDANT_PATHS = "REDUNDANT_PATHS"
    SINGLE_EDGE_FRAGILE = "SINGLE_EDGE_FRAGILE"
    DIRECT_READOUT = "DIRECT_READOUT"
    NOT_CERTIFIED = "NOT_CERTIFIED"


@dataclass(frozen=True)
class OpportunityResilienceAssessment:
    """Edge-disjoint path count and one deterministic minimum edge cut."""

    status: ResilienceStatus
    opportunity: OpportunityAssessment
    edge_disjoint_path_count: int = 0
    minimum_edge_cut: tuple[InfluenceEdge, ...] = ()
    reason: str = ""
    establishes_causal_effect: bool = False
    establishes_trace_completeness: bool = False


def assess_causal_opportunity_resilience(
    *,
    events: Iterable[TraceEvent],
    influence_edges: Iterable[InfluenceEdge],
    intervention: Intervention,
    readout_event_ids: Iterable[str],
    trace_complete: bool,
) -> OpportunityResilienceAssessment:
    """Measure edge redundancy after the base opportunity check succeeds.

    Influence edges have unit capacity. Synthetic source/target connectors have
    high capacity, so the maximum flow equals the number of edge-disjoint traced
    influence paths. The residual partition supplies one deterministic minimum
    cut. A single path is classified as fragile, not as causal evidence.
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
        return OpportunityResilienceAssessment(
            status=ResilienceStatus.NOT_CERTIFIED,
            opportunity=opportunity,
            reason="base causal-opportunity certificate was not established",
        )

    if readouts.intersection(opportunity.treated_seed_events):
        return OpportunityResilienceAssessment(
            status=ResilienceStatus.DIRECT_READOUT,
            opportunity=opportunity,
            reason="a treated state-bearing event is itself a declared readout",
        )

    unique_edges = tuple(
        sorted(
            set(edge_list),
            key=lambda edge: (edge.source_event_id, edge.target_event_id),
        )
    )
    path_count, reachable = _maximum_edge_disjoint_paths(
        event_ids=tuple(sorted(event.event_id for event in event_list)),
        edges=unique_edges,
        seeds=opportunity.treated_seed_events,
        readouts=tuple(sorted(readouts)),
    )
    minimum_cut = tuple(
        edge
        for edge in unique_edges
        if edge.source_event_id in reachable and edge.target_event_id not in reachable
    )
    status = (
        ResilienceStatus.REDUNDANT_PATHS
        if path_count >= 2
        else ResilienceStatus.SINGLE_EDGE_FRAGILE
    )
    return OpportunityResilienceAssessment(
        status=status,
        opportunity=opportunity,
        edge_disjoint_path_count=path_count,
        minimum_edge_cut=minimum_cut,
        reason=(
            "at least two edge-disjoint traced opportunity paths exist"
            if path_count >= 2
            else "all traced opportunity paths share a one-edge cut"
        ),
    )


def _maximum_edge_disjoint_paths(
    *,
    event_ids: tuple[str, ...],
    edges: tuple[InfluenceEdge, ...],
    seeds: tuple[str, ...],
    readouts: tuple[str, ...],
) -> tuple[int, frozenset[str]]:
    source = "__forge_super_source__"
    sink = "__forge_super_sink__"
    if source in event_ids or sink in event_ids:
        raise ValueError("reserved synthetic flow-node ID used as event_id")

    high_capacity = max(1, len(edges) + 1)
    capacity: dict[tuple[str, str], int] = {}
    adjacency: dict[str, set[str]] = {node: set() for node in (*event_ids, source, sink)}

    def add_arc(start: str, end: str, value: int) -> None:
        capacity[start, end] = capacity.get((start, end), 0) + value
        capacity.setdefault((end, start), 0)
        adjacency[start].add(end)
        adjacency[end].add(start)

    for edge in edges:
        add_arc(edge.source_event_id, edge.target_event_id, 1)
    for seed in seeds:
        add_arc(source, seed, high_capacity)
    for readout in readouts:
        add_arc(readout, sink, high_capacity)

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
    reachable.discard(source)
    reachable.discard(sink)
    return flow, frozenset(reachable)


def _augmenting_path(
    *,
    source: str,
    sink: str,
    adjacency: dict[str, set[str]],
    residual: dict[tuple[str, str], int],
) -> dict[str, str]:
    parent: dict[str, str] = {}
    seen = {source}
    queue: deque[str] = deque([source])
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
    source: str,
    adjacency: dict[str, set[str]],
    residual: dict[tuple[str, str], int],
) -> set[str]:
    seen = {source}
    queue: deque[str] = deque([source])
    while queue:
        current = queue.popleft()
        for target in sorted(adjacency[current]):
            if target not in seen and residual[current, target] > 0:
                seen.add(target)
                queue.append(target)
    return seen


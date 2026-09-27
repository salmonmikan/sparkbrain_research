from forge_prototypes.causal_opportunity_certificate import (
    EventClock,
    InfluenceEdge,
    Intervention,
    OpportunityStatus,
    TraceEvent,
)
from forge_prototypes.causal_opportunity_resilience import (
    ResilienceStatus,
    assess_causal_opportunity_resilience,
)


def event(event_id: str, actor_id: str, time: float, sequence: int = 0) -> TraceEvent:
    return TraceEvent(event_id, actor_id, EventClock(time, sequence))


def assess(events: tuple[TraceEvent, ...], edges: tuple[InfluenceEdge, ...], **kwargs):
    return assess_causal_opportunity_resilience(
        events=events,
        influence_edges=edges,
        intervention=Intervention(frozenset({"treated"}), EventClock(0.0)),
        readout_event_ids=kwargs.get("readouts", ("readout",)),
        trace_complete=kwargs.get("trace_complete", True),
    )


def test_single_chain_is_single_edge_fragile() -> None:
    result = assess(
        (event("seed", "treated", 1), event("relay", "relay", 2), event("readout", "r", 3)),
        (InfluenceEdge("seed", "relay"), InfluenceEdge("relay", "readout")),
    )

    assert result.status is ResilienceStatus.SINGLE_EDGE_FRAGILE
    assert result.edge_disjoint_path_count == 1
    assert result.minimum_edge_cut == (InfluenceEdge("seed", "relay"),)
    assert not result.establishes_causal_effect
    assert not result.establishes_trace_completeness


def test_diamond_has_two_edge_disjoint_paths() -> None:
    events = (
        event("seed", "treated", 1),
        event("a", "relay-a", 2),
        event("b", "relay-b", 2, 1),
        event("readout", "r", 3),
    )
    edges = (
        InfluenceEdge("seed", "a"),
        InfluenceEdge("a", "readout"),
        InfluenceEdge("seed", "b"),
        InfluenceEdge("b", "readout"),
    )

    result = assess(events, edges)

    assert result.status is ResilienceStatus.REDUNDANT_PATHS
    assert result.edge_disjoint_path_count == 2
    assert result.minimum_edge_cut == (
        InfluenceEdge("seed", "a"),
        InfluenceEdge("seed", "b"),
    )


def test_two_treated_seeds_can_supply_two_routes() -> None:
    events = (
        event("seed-a", "treated", 1),
        event("seed-b", "treated", 1, 1),
        event("readout", "r", 2),
    )
    edges = (
        InfluenceEdge("seed-a", "readout"),
        InfluenceEdge("seed-b", "readout"),
    )

    result = assess(events, edges)

    assert result.status is ResilienceStatus.REDUNDANT_PATHS
    assert result.edge_disjoint_path_count == 2


def test_incomplete_trace_propagates_without_resilience_claim() -> None:
    result = assess(
        (event("seed", "treated", 1), event("readout", "r", 2)),
        (InfluenceEdge("seed", "readout"),),
        trace_complete=False,
    )

    assert result.status is ResilienceStatus.NOT_CERTIFIED
    assert result.opportunity.status is OpportunityStatus.INCOMPLETE_TRACE
    assert result.edge_disjoint_path_count == 0


def test_disconnected_treated_activity_propagates_no_path() -> None:
    result = assess(
        (event("seed", "treated", 1), event("readout", "r", 2)),
        (),
    )

    assert result.status is ResilienceStatus.NOT_CERTIFIED
    assert result.opportunity.status is OpportunityStatus.NO_PATH_TO_READOUT


def test_reordering_does_not_change_flow_or_minimum_cut() -> None:
    events = (
        event("seed", "treated", 1),
        event("a", "relay-a", 2),
        event("b", "relay-b", 2, 1),
        event("readout", "r", 3),
    )
    edges = (
        InfluenceEdge("seed", "b"),
        InfluenceEdge("b", "readout"),
        InfluenceEdge("seed", "a"),
        InfluenceEdge("a", "readout"),
    )

    first = assess(events, edges)
    second = assess(tuple(reversed(events)), tuple(reversed(edges)))

    assert first.edge_disjoint_path_count == second.edge_disjoint_path_count == 2
    assert first.minimum_edge_cut == second.minimum_edge_cut


def test_treated_event_that_is_readout_has_no_influence_edge_cut() -> None:
    result = assess((event("readout", "treated", 1),), (), readouts=("readout",))

    assert result.status is ResilienceStatus.DIRECT_READOUT
    assert result.edge_disjoint_path_count == 0
    assert result.minimum_edge_cut == ()


def test_invalid_trace_propagates_without_flow_analysis() -> None:
    result = assess(
        (event("seed", "treated", 2), event("readout", "r", 1)),
        (InfluenceEdge("seed", "readout"),),
    )

    assert result.status is ResilienceStatus.NOT_CERTIFIED
    assert result.opportunity.status is OpportunityStatus.INVALID_TRACE


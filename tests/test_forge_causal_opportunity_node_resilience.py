from forge_prototypes.causal_opportunity_certificate import (
    EventClock,
    InfluenceEdge,
    Intervention,
    OpportunityStatus,
    TraceEvent,
)
from forge_prototypes.causal_opportunity_node_resilience import (
    NodeResilienceStatus,
    assess_causal_opportunity_node_resilience,
)


def event(event_id: str, actor_id: str, time: float, sequence: int = 0) -> TraceEvent:
    return TraceEvent(event_id, actor_id, EventClock(time, sequence))


def assess(events: tuple[TraceEvent, ...], edges: tuple[InfluenceEdge, ...], **kwargs):
    return assess_causal_opportunity_node_resilience(
        events=events,
        influence_edges=edges,
        intervention=Intervention(frozenset({"treated"}), EventClock(0.0)),
        readout_event_ids=kwargs.get("readouts", ("readout",)),
        trace_complete=kwargs.get("trace_complete", True),
    )


def test_single_chain_identifies_relay_event_cut() -> None:
    result = assess(
        (event("seed", "treated", 1), event("relay", "relay", 2), event("readout", "r", 3)),
        (InfluenceEdge("seed", "relay"), InfluenceEdge("relay", "readout")),
    )

    assert result.status is NodeResilienceStatus.SINGLE_INTERNAL_EVENT_FRAGILE
    assert result.internally_event_disjoint_path_count == 1
    assert result.minimum_internal_event_cut == ("relay",)
    assert not result.establishes_causal_effect
    assert not result.establishes_trace_completeness


def test_edge_disjoint_routes_with_shared_hub_are_node_fragile() -> None:
    events = (
        event("seed", "treated", 1),
        event("left", "left", 2),
        event("right", "right", 2, 1),
        event("hub", "hub", 3),
        event("out-a", "out-a", 4),
        event("out-b", "out-b", 4, 1),
        event("readout", "r", 5),
    )
    edges = (
        InfluenceEdge("seed", "left"),
        InfluenceEdge("seed", "right"),
        InfluenceEdge("left", "hub"),
        InfluenceEdge("right", "hub"),
        InfluenceEdge("hub", "out-a"),
        InfluenceEdge("hub", "out-b"),
        InfluenceEdge("out-a", "readout"),
        InfluenceEdge("out-b", "readout"),
    )

    result = assess(events, edges)

    assert result.status is NodeResilienceStatus.SINGLE_INTERNAL_EVENT_FRAGILE
    assert result.internally_event_disjoint_path_count == 1
    assert result.minimum_internal_event_cut == ("hub",)


def test_diamond_has_two_internally_event_disjoint_paths() -> None:
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

    assert result.status is NodeResilienceStatus.REDUNDANT_INTERNAL_EVENTS
    assert result.internally_event_disjoint_path_count == 2
    assert result.minimum_internal_event_cut == ("a", "b")


def test_direct_seed_to_readout_is_separate_from_internal_cut() -> None:
    result = assess(
        (event("seed", "treated", 1), event("readout", "r", 2)),
        (InfluenceEdge("seed", "readout"),),
    )

    assert result.status is NodeResilienceStatus.DIRECT_BYPASS
    assert result.internally_event_disjoint_path_count == 0
    assert result.minimum_internal_event_cut == ()


def test_treated_event_that_is_readout_is_direct_readout() -> None:
    result = assess((event("readout", "treated", 1),), (), readouts=("readout",))

    assert result.status is NodeResilienceStatus.DIRECT_READOUT


def test_reordering_preserves_count_and_cut() -> None:
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

    assert first.internally_event_disjoint_path_count == second.internally_event_disjoint_path_count == 2
    assert first.minimum_internal_event_cut == second.minimum_internal_event_cut


def test_incomplete_trace_produces_no_node_resilience_claim() -> None:
    result = assess(
        (event("seed", "treated", 1), event("relay", "x", 2), event("readout", "r", 3)),
        (InfluenceEdge("seed", "relay"), InfluenceEdge("relay", "readout")),
        trace_complete=False,
    )

    assert result.status is NodeResilienceStatus.NOT_CERTIFIED
    assert result.opportunity.status is OpportunityStatus.INCOMPLETE_TRACE


def test_invalid_trace_produces_no_node_resilience_claim() -> None:
    result = assess(
        (event("seed", "treated", 2), event("readout", "r", 1)),
        (InfluenceEdge("seed", "readout"),),
    )

    assert result.status is NodeResilienceStatus.NOT_CERTIFIED
    assert result.opportunity.status is OpportunityStatus.INVALID_TRACE

from forge_prototypes.causal_opportunity_certificate import (
    EventClock,
    InfluenceEdge,
    Intervention,
    OpportunityStatus,
    TraceEvent,
    certify_causal_opportunity,
)


def event(
    event_id: str,
    actor_id: str,
    time: float,
    sequence: int = 0,
    *,
    state_bearing: bool = True,
) -> TraceEvent:
    return TraceEvent(
        event_id=event_id,
        actor_id=actor_id,
        clock=EventClock(time, sequence),
        state_bearing=state_bearing,
    )


def intervention(*actor_ids: str, time: float = 0.0) -> Intervention:
    return Intervention(frozenset(actor_ids), EventClock(time))


def test_certifies_time_respecting_treated_path_to_readout() -> None:
    assessment = certify_causal_opportunity(
        events=(
            event("treated-spike", "hidden-16", 1.0),
            event("relay-spike", "hidden-22", 2.0),
            event("visible-return", "visible-3", 3.0),
        ),
        influence_edges=(
            InfluenceEdge("treated-spike", "relay-spike"),
            InfluenceEdge("relay-spike", "visible-return"),
        ),
        intervention=intervention("hidden-16"),
        readout_event_ids=("visible-return",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.CERTIFIED
    assert assessment.path == ("treated-spike", "relay-spike", "visible-return")
    assert not assessment.establishes_causal_effect


def test_untreated_direct_cue_response_does_not_count_as_opportunity() -> None:
    assessment = certify_causal_opportunity(
        events=(
            event("cue", "receptor-6", 1.0),
            event("direct-response", "receptor-7", 2.0),
        ),
        influence_edges=(InfluenceEdge("cue", "direct-response"),),
        intervention=intervention("hidden-16"),
        readout_event_ids=("direct-response",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.NO_TREATED_ACTIVITY
    assert assessment.path == ()


def test_disconnected_treated_activity_is_not_a_certificate() -> None:
    assessment = certify_causal_opportunity(
        events=(
            event("treated-state", "hidden-16", 1.0),
            event("cue", "receptor-6", 1.0, 1),
            event("readout", "receptor-7", 2.0),
        ),
        influence_edges=(InfluenceEdge("cue", "readout"),),
        intervention=intervention("hidden-16"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.NO_PATH_TO_READOUT
    assert assessment.treated_seed_events == ("treated-state",)


def test_incomplete_trace_fails_closed_before_negative_interpretation() -> None:
    assessment = certify_causal_opportunity(
        events=(event("treated-state", "hidden-16", 1.0), event("readout", "visible", 2.0)),
        influence_edges=(),
        intervention=intervention("hidden-16"),
        readout_event_ids=("readout",),
        trace_complete=False,
    )

    assert assessment.status is OpportunityStatus.INCOMPLETE_TRACE


def test_unknown_edge_endpoint_invalidates_trace() -> None:
    assessment = certify_causal_opportunity(
        events=(event("treated-state", "hidden-16", 1.0), event("readout", "visible", 2.0)),
        influence_edges=(InfluenceEdge("treated-state", "missing-event"),),
        intervention=intervention("hidden-16"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.INVALID_TRACE
    assert "unknown event" in assessment.reason


def test_backward_or_same_order_edge_invalidates_trace() -> None:
    assessment = certify_causal_opportunity(
        events=(event("treated-state", "hidden-16", 2.0), event("readout", "visible", 1.0)),
        influence_edges=(InfluenceEdge("treated-state", "readout"),),
        intervention=intervention("hidden-16"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.INVALID_TRACE
    assert "not forward" in assessment.reason


def test_same_time_sequence_can_express_a_forward_path() -> None:
    assessment = certify_causal_opportunity(
        events=(
            event("treated-state", "hidden-16", 1.0, 1),
            event("readout", "visible", 1.0, 2),
        ),
        influence_edges=(InfluenceEdge("treated-state", "readout"),),
        intervention=intervention("hidden-16"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.CERTIFIED
    assert assessment.path == ("treated-state", "readout")


def test_pre_intervention_activity_is_not_used_as_a_seed() -> None:
    assessment = certify_causal_opportunity(
        events=(
            event("old-treated-state", "hidden-16", 1.0),
            event("readout", "visible", 3.0),
        ),
        influence_edges=(InfluenceEdge("old-treated-state", "readout"),),
        intervention=intervention("hidden-16", time=2.0),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.NO_TREATED_ACTIVITY


def test_certificate_path_is_deterministic_under_edge_reordering() -> None:
    events = (
        event("seed", "treated", 1.0),
        event("a", "relay-a", 2.0),
        event("b", "relay-b", 2.0, 1),
        event("readout", "visible", 3.0),
    )
    edges = (
        InfluenceEdge("seed", "b"),
        InfluenceEdge("b", "readout"),
        InfluenceEdge("seed", "a"),
        InfluenceEdge("a", "readout"),
    )

    first = certify_causal_opportunity(
        events=events,
        influence_edges=edges,
        intervention=intervention("treated"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )
    second = certify_causal_opportunity(
        events=reversed(events),
        influence_edges=reversed(edges),
        intervention=intervention("treated"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert first.path == second.path == ("seed", "a", "readout")


def test_non_state_bearing_target_event_cannot_seed_a_certificate() -> None:
    assessment = certify_causal_opportunity(
        events=(
            event("target-log", "hidden-16", 1.0, state_bearing=False),
            event("readout", "visible", 2.0),
        ),
        influence_edges=(InfluenceEdge("target-log", "readout"),),
        intervention=intervention("hidden-16"),
        readout_event_ids=("readout",),
        trace_complete=True,
    )

    assert assessment.status is OpportunityStatus.NO_TREATED_ACTIVITY

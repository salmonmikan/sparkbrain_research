from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v061_a01.md002_p4_trace_binding import P4RetainedTraceInput
from sparkbrain.v061_a01.md002_protocol import canonical_sha256


def _event(event_id: str, proposals: tuple[str, ...]) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=1.0,
        port_id="out",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{event_id}",
        source_unit_id=1,
        source_proposal_ids=proposals,
        generation_depth=1,
        source_state_hash=f"state:{event_id}",
    )


def _trace_input(
    event: BoundaryEvent,
    *,
    before: tuple[str, ...] = ("p:a", "p:b", "p:c"),
    after: tuple[str, ...] = ("p:b", "p:c"),
) -> P4RetainedTraceInput:
    boundary = tuple(dict.fromkeys(event.source_proposal_ids))
    payload = {
        "boundary_source_proposal_ids": boundary,
        "active_lineages_before": before,
        "active_lineages_after": after,
    }
    trace = (
        {"type": "md002-p4-boundary-event", "event": event.state_dict()},
        {
            "type": "md002-p4-active-lineages",
            "phase": "before",
            "proposal_ids": list(before),
        },
        {
            "type": "md002-p4-active-lineages",
            "phase": "after",
            "proposal_ids": list(after),
        },
        {"type": "md002-merged-ancestry-measurement", "measurement": payload},
    )
    return P4RetainedTraceInput(
        boundary_events=(event,),
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )


def test_p4_trace_binding_derives_plural_ancestry_and_runtime_lineages() -> None:
    retained = _trace_input(_event("merged", ("p:a", "p:b")))

    observation = retained.observation()

    assert observation.boundary_source_proposal_ids == ("p:a", "p:b")
    assert observation.active_lineages_before == ("p:a", "p:b", "p:c")
    assert observation.active_lineages_after == ("p:b", "p:c")


def test_p4_trace_binding_rejects_boundary_event_not_retained_in_trace() -> None:
    retained = _trace_input(_event("merged", ("p:a", "p:b")))
    different = _event("different", ("p:a", "p:b"))
    forged = replace(retained, boundary_events=(different,))

    with pytest.raises(ValueError, match="do not exactly match"):
        forged.validate()


def test_p4_trace_binding_rejects_cherry_picked_boundary_subset() -> None:
    merged = _event("merged", ("p:a", "p:b"))
    omitted = _event("omitted", ("p:b", "p:c"))
    retained = _trace_input(merged)
    rows = list(retained.runtime_trace)
    rows.insert(1, {"type": "md002-p4-boundary-event", "event": omitted.state_dict()})
    trace = tuple(rows)
    cherry_picked = replace(
        retained,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )

    with pytest.raises(ValueError, match="complete retained boundary-event trace"):
        cherry_picked.validate()


def test_p4_trace_binding_rejects_separate_singleton_events_as_merged() -> None:
    a = _event("a", ("p:a",))
    b = _event("b", ("p:b",))
    trace = (
        {"type": "md002-p4-boundary-event", "event": a.state_dict()},
        {"type": "md002-p4-boundary-event", "event": b.state_dict()},
        {
            "type": "md002-p4-active-lineages",
            "phase": "before",
            "proposal_ids": ["p:a", "p:b"],
        },
        {
            "type": "md002-p4-active-lineages",
            "phase": "after",
            "proposal_ids": ["p:a"],
        },
    )
    retained = P4RetainedTraceInput(
        boundary_events=(a, b),
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )

    with pytest.raises(ValueError, match="genuinely merged"):
        retained.validate()


def test_p4_trace_binding_rejects_expected_lineage_constants_not_in_trace() -> None:
    event = _event("merged", ("p:a", "p:b"))
    retained = _trace_input(event)
    rows = list(retained.runtime_trace)
    rows[-1] = {
        "type": "md002-merged-ancestry-measurement",
        "measurement": {
            "boundary_source_proposal_ids": ("p:a", "p:b"),
            "active_lineages_before": ("p:a", "p:b", "p:c"),
            "active_lineages_after": ("p:a",),
        },
    }
    trace = tuple(rows)
    tampered = replace(
        retained,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )

    with pytest.raises(ValueError, match="derived lineage measurement"):
        tampered.validate()


def test_p4_trace_binding_rejects_duplicate_or_untyped_active_lineages() -> None:
    event = _event("merged", ("p:a", "p:b"))
    retained = _trace_input(event)
    rows = list(retained.runtime_trace)
    rows[1] = {
        "type": "md002-p4-active-lineages",
        "phase": "before",
        "proposal_ids": ["p:a", "p:a", "p:b"],
    }
    trace = tuple(rows)
    duplicate = replace(
        retained,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )
    with pytest.raises(ValueError, match="must be unique"):
        duplicate.validate()

    rows = list(retained.runtime_trace)
    rows[1] = {
        "type": "md002-p4-active-lineages",
        "phase": "before",
        "proposal_ids": ["p:a", 7],
    }
    trace = tuple(rows)
    untyped = replace(
        retained,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )
    with pytest.raises(TypeError, match="must be strings"):
        untyped.validate()

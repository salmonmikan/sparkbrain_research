from __future__ import annotations

import pytest

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.foundation import EventOrigin
from sparkbrain.v061_a01.md002_world_fixture import (
    P2AnonymousWorldPermutation,
    P2AnonymousWorldRelation,
)


def boundary(proposal_id: str, *, event_id: str = "boundary:a") -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=10.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{event_id}",
        source_unit_id=2,
        source_proposal_ids=(proposal_id,),
        generation_depth=1,
        source_state_hash="field:matched",
    )


def relation_a() -> P2AnonymousWorldRelation:
    return P2AnonymousWorldRelation(
        responses=(("proposal:a", "world:x"), ("proposal:b", "world:y"))
    )


def relation_b() -> P2AnonymousWorldRelation:
    return P2AnonymousWorldRelation(
        responses=(("proposal:a", "world:y"), ("proposal:b", "world:x"))
    )


def test_world_permutation_changes_only_assignment_inventory() -> None:
    pair = P2AnonymousWorldPermutation(relation_a(), relation_b())
    pair.validate()
    assert set(pair.control.mapping) == set(pair.intervention.mapping)
    assert set(pair.control.mapping.values()) == set(pair.intervention.mapping.values())
    assert all(
        pair.control.mapping[key] != pair.intervention.mapping[key]
        for key in pair.control.mapping
    )


def test_world_fixture_generates_exact_parent_external_response() -> None:
    control = relation_a()
    intervention = relation_b()
    source = boundary("proposal:a")

    left = control.respond(source, event_id="external:control", time_ms=12.0)
    right = intervention.respond(source, event_id="external:intervention", time_ms=12.0)

    assert left.origin is EventOrigin.EXTERNAL
    assert right.origin is EventOrigin.EXTERNAL
    assert left.parent_event_ids == right.parent_event_ids == (source.event_id,)
    assert left.target == "world:x"
    assert right.target == "world:y"
    assert left.magnitude == right.magnitude == source.magnitude
    assert left.polarity == right.polarity == source.polarity


def test_world_fixture_never_accepts_merged_or_unknown_lineage() -> None:
    source = boundary("proposal:a")
    merged = BoundaryEvent(
        event_id=source.event_id,
        time_ms=source.time_ms,
        port_id=source.port_id,
        magnitude=source.magnitude,
        polarity=source.polarity,
        direction=source.direction,
        source_spark_id=source.source_spark_id,
        source_unit_id=source.source_unit_id,
        source_proposal_ids=("proposal:a", "proposal:b"),
        generation_depth=source.generation_depth,
        source_state_hash=source.source_state_hash,
    )
    with pytest.raises(ValueError, match="exactly one source proposal"):
        relation_a().respond(merged, event_id="external:merged", time_ms=12.0)
    with pytest.raises(ValueError, match="absent from the world relation"):
        relation_a().respond(
            boundary("proposal:unknown"),
            event_id="external:unknown",
            time_ms=12.0,
        )


def test_world_permutation_fails_closed_on_non_permutation() -> None:
    unchanged = P2AnonymousWorldRelation(
        responses=(("proposal:a", "world:x"), ("proposal:b", "world:y"))
    )
    with pytest.raises(ValueError, match="reverse every registered response"):
        P2AnonymousWorldPermutation(relation_a(), unchanged).validate()

    different_target_inventory = P2AnonymousWorldRelation(
        responses=(("proposal:a", "world:y"), ("proposal:b", "world:z"))
    )
    with pytest.raises(ValueError, match="identical external target inventory"):
        P2AnonymousWorldPermutation(relation_a(), different_target_inventory).validate()

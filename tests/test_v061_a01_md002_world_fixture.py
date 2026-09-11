from __future__ import annotations

import pytest

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.foundation import EventOrigin
from sparkbrain.v061_a01.md002_world_fixture import (
    P2AnonymousWorldPermutation,
    P2AnonymousWorldRelation,
    P2WorldResponseSchedule,
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


def pair() -> P2AnonymousWorldPermutation:
    return P2AnonymousWorldPermutation(relation_a(), relation_b())


def schedule() -> P2WorldResponseSchedule:
    return P2WorldResponseSchedule(event_id="external:paired", time_ms=12.0)


def test_world_permutation_changes_only_assignment_inventory() -> None:
    permutation = pair()
    permutation.validate()
    assert set(permutation.control.mapping) == set(permutation.intervention.mapping)
    assert set(permutation.control.mapping.values()) == set(
        permutation.intervention.mapping.values()
    )
    assert all(
        permutation.control.mapping[key] != permutation.intervention.mapping[key]
        for key in permutation.control.mapping
    )


def test_world_fixture_generates_exact_parent_external_response_with_shared_identity() -> None:
    source = boundary("proposal:a")
    left, right = pair().respond_pair(source, source, schedule=schedule())

    assert left.origin is EventOrigin.EXTERNAL
    assert right.origin is EventOrigin.EXTERNAL
    assert left.event_id == right.event_id == "external:paired"
    assert left.time_ms == right.time_ms == 12.0
    assert left.parent_event_ids == right.parent_event_ids == (source.event_id,)
    assert left.target == "world:x"
    assert right.target == "world:y"
    assert left.magnitude == right.magnitude == source.magnitude
    assert left.polarity == right.polarity == source.polarity


def test_world_fixture_rejects_arm_specific_boundary_drift() -> None:
    source = boundary("proposal:a")
    drifted = boundary("proposal:a", event_id="boundary:other")
    with pytest.raises(ValueError, match="differ outside world relation"):
        pair().respond_pair(source, drifted, schedule=schedule())


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
        pair().respond_pair(merged, merged, schedule=schedule())

    unknown = boundary("proposal:unknown")
    with pytest.raises(ValueError, match="absent from the world relation"):
        pair().respond_pair(unknown, unknown, schedule=schedule())


def test_world_relation_rejects_non_string_decoded_identifiers() -> None:
    invalid = {
        "schema": "v061-a01-md002-p2-anonymous-world-v1",
        "responses": [
            {"proposal_id": 1, "external_target": "world:x"},
            {"proposal_id": "proposal:b", "external_target": "world:y"},
        ],
    }
    with pytest.raises(ValueError, match="identifiers must be strings"):
        P2AnonymousWorldRelation.from_state_dict(invalid)

    restored = P2AnonymousWorldRelation.from_state_dict(relation_a().state_dict())
    assert restored == relation_a()
    assert restored.state_dict() == relation_a().state_dict()


def test_world_response_schedule_fails_closed_on_identity_or_clock_drift() -> None:
    source = boundary("proposal:a")
    with pytest.raises(ValueError, match="non-empty string"):
        pair().respond_pair(
            source,
            source,
            schedule=P2WorldResponseSchedule(event_id="", time_ms=12.0),
        )
    with pytest.raises(ValueError, match="must occur after"):
        pair().respond_pair(
            source,
            source,
            schedule=P2WorldResponseSchedule(event_id="external:paired", time_ms=10.0),
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

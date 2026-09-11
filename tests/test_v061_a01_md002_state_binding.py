from __future__ import annotations

import json

import pytest

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import (
    EndogenousPulseProposal,
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
)
from sparkbrain.v06.local_expectation import LocalExpectationConfig
from sparkbrain.v061_a01.credit_bridge import A01LocalTemporalExpectation
from sparkbrain.v061_a01.md002_state_binding import (
    LiveReturnAddressState,
    build_bound_a01_p2_fixture,
    freeze_a01_p2_partitions,
)


def external(event_id: str, time_ms: float, target: str) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def expectation() -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0)
    )
    model.observe_external_transition(external("source", 0.0, "A"), external("target", 5.0, "B"))
    return model


def return_address() -> LiveReturnAddressState:
    proposal = EndogenousPulseProposal(
        proposal_id="proposal-a",
        created_at_ms=10.0,
        target="B",
        predicted_arrival_ms=15.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        parent_proposal_ids=(),
        local_path_ids=("local:A->B",),
        generation_depth=1,
        valid_until_ms=30.0,
        energy_cost=0.1,
    )
    boundary = BoundaryEvent(
        event_id="boundary-a",
        time_ms=16.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-a",
        source_unit_id=2,
        source_proposal_ids=(proposal.proposal_id,),
        generation_depth=1,
        source_state_hash="field-state",
    )
    return LiveReturnAddressState((proposal,), boundary)


def test_real_a01_partitions_are_canonical_and_round_trip_readable() -> None:
    model = expectation()
    consistency = UntypedBoundaryConsistency(ProvenanceLedger())
    field_state = {
        "clock_ms": 16.0,
        "units": [{"unit_id": 2, "potential": 0.25}],
        "connections": [{"source_id": 1, "target_id": 2, "weight": 0.5}],
    }
    bound = freeze_a01_p2_partitions(
        expectation=model,
        field_state=field_state,
        consistency=consistency,
        return_address=return_address(),
    )

    assert json.loads(bound.partitions.local) == model.learned_state_dict()
    assert json.loads(bound.partitions.field) == field_state
    assert json.loads(bound.partitions.consistency) == consistency.learned_state_dict()
    assert json.loads(bound.partitions.return_address or b"null") == bound.return_address_state


def test_bound_p2_fixture_varies_only_world_relation_bytes() -> None:
    model = expectation()
    consistency = UntypedBoundaryConsistency(ProvenanceLedger())
    fixture = build_bound_a01_p2_fixture(
        expectation=model,
        field_state={"clock_ms": 20.0, "field": "same"},
        consistency=consistency,
        return_address=return_address(),
        control_world_relation={"port:p": "world:x"},
        intervention_world_relation={"port:p": "world:y"},
        admissible_external_evidence=(
            external("evidence-1", 30.0, "world:z"),
            external("evidence-2", 35.0, "world:q"),
        ),
    )
    control = fixture.arm("control")
    intervention = fixture.arm("intervention")

    assert control.partitions == intervention.partitions
    assert control.admissible_external_evidence == intervention.admissible_external_evidence
    assert control.world_relation != intervention.world_relation
    fixture.prospective_contract().validate()


def test_bound_p2_rejects_nonexternal_or_unordered_evidence() -> None:
    model = expectation()
    consistency = UntypedBoundaryConsistency(ProvenanceLedger())
    endogenous = RuntimePulse(
        event_id="endo",
        time_ms=30.0,
        target="world:z",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
    )
    with pytest.raises(ValueError, match="external observations only"):
        build_bound_a01_p2_fixture(
            expectation=model,
            field_state={"field": "same"},
            consistency=consistency,
            control_world_relation={"relation": "a"},
            intervention_world_relation={"relation": "b"},
            admissible_external_evidence=(endogenous,),
        )

    with pytest.raises(ValueError, match="strictly time ordered"):
        build_bound_a01_p2_fixture(
            expectation=model,
            field_state={"field": "same"},
            consistency=consistency,
            control_world_relation={"relation": "a"},
            intervention_world_relation={"relation": "b"},
            admissible_external_evidence=(
                external("late", 40.0, "world:x"),
                external("early", 39.0, "world:y"),
            ),
        )


def test_return_address_requires_closed_proposal_ancestry() -> None:
    child = EndogenousPulseProposal(
        proposal_id="child",
        created_at_ms=10.0,
        target="B",
        predicted_arrival_ms=15.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        parent_proposal_ids=("missing-parent",),
        local_path_ids=("local:A->B",),
        generation_depth=2,
        valid_until_ms=30.0,
        energy_cost=0.1,
    )
    boundary = BoundaryEvent(
        event_id="boundary-child",
        time_ms=16.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-child",
        source_unit_id=2,
        source_proposal_ids=("child",),
        generation_depth=2,
        source_state_hash="field-state",
    )
    with pytest.raises(ValueError, match="not closed over proposal ancestry"):
        LiveReturnAddressState((child,), boundary).state_dict()

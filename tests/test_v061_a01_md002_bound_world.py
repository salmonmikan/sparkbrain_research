from __future__ import annotations

import json

import pytest

from sparkbrain.v04 import (
    Connection,
    ExcitableFieldConfig,
    TemporalExcitableField,
    UnitState,
    explicit_topology,
)
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
from sparkbrain.v061_a01.md002_bound_world import build_typed_a01_p2_world_fixture
from sparkbrain.v061_a01.md002_restore_adapter import restore_a01_p2_arm
from sparkbrain.v061_a01.md002_state_binding import LiveReturnAddressState
from sparkbrain.v061_a01.md002_world_fixture import (
    P2AnonymousWorldPermutation,
    P2AnonymousWorldRelation,
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
    model.observe_external_transition(
        external("train-source", 0.0, "A"),
        external("train-target", 5.0, "B"),
    )
    return model


def field() -> TemporalExcitableField:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
            UnitState(2, 0.5, 1.0, base_threshold=0.5),
        ),
        (
            Connection(0, 2, 0.05, 5.0, plastic=True),
            Connection(2, 1, 0.05, 5.0, plastic=True),
            Connection(0, 1, 0.05, 5.0, plastic=True),
        ),
        receptor_ids=(0, 1),
    )
    return TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))


def return_address(*, proposal_ids: tuple[str, ...] = ("child",)) -> LiveReturnAddressState:
    parent = EndogenousPulseProposal(
        proposal_id="parent",
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
    child = EndogenousPulseProposal(
        proposal_id="child",
        created_at_ms=11.0,
        target="B",
        predicted_arrival_ms=16.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        parent_proposal_ids=("parent",),
        local_path_ids=("local:A->B",),
        generation_depth=2,
        valid_until_ms=31.0,
        energy_cost=0.1,
    )
    other = EndogenousPulseProposal(
        proposal_id="other",
        created_at_ms=11.0,
        target="C",
        predicted_arrival_ms=16.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        parent_proposal_ids=(),
        local_path_ids=("local:A->C",),
        generation_depth=1,
        valid_until_ms=31.0,
        energy_cost=0.1,
    )
    boundary = BoundaryEvent(
        event_id="boundary-live",
        time_ms=17.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-live",
        source_unit_id=2,
        source_proposal_ids=proposal_ids,
        generation_depth=2,
        source_state_hash="field-state",
    )
    return LiveReturnAddressState((child, parent, other), boundary)


def permutation() -> P2AnonymousWorldPermutation:
    return P2AnonymousWorldPermutation(
        control=P2AnonymousWorldRelation(
            responses=(("child", "world:x"), ("other", "world:y"))
        ),
        intervention=P2AnonymousWorldRelation(
            responses=(("child", "world:y"), ("other", "world:x"))
        ),
    )


def build(*, address: LiveReturnAddressState | None = None):
    return build_typed_a01_p2_world_fixture(
        expectation=expectation(),
        field_state=field(),
        consistency=UntypedBoundaryConsistency(ProvenanceLedger()),
        return_address=address or return_address(),
        world_permutation=permutation(),
        admissible_external_evidence=(
            external("evidence-1", 30.0, "world:z"),
            external("evidence-2", 35.0, "world:q"),
        ),
    )


def test_typed_world_binding_preserves_checkpoint_and_exact_world_schema() -> None:
    fixture = build()
    control = fixture.arm("control")
    intervention = fixture.arm("intervention")

    assert control.partitions == intervention.partitions
    assert control.admissible_external_evidence == intervention.admissible_external_evidence
    assert control.world_relation != intervention.world_relation
    assert json.loads(control.world_relation) == permutation().control.state_dict()
    assert json.loads(intervention.world_relation) == permutation().intervention.state_dict()

    restored_control = restore_a01_p2_arm(control)
    restored_intervention = restore_a01_p2_arm(intervention)
    assert restored_control.boundary == restored_intervention.boundary
    assert restored_control.expectation.learned_state_dict() == (
        restored_intervention.expectation.learned_state_dict()
    )
    assert restored_control.world_relation == permutation().control.state_dict()
    assert restored_intervention.world_relation == permutation().intervention.state_dict()


def test_typed_world_binding_requires_live_boundary_proposal_in_both_worlds() -> None:
    absent = P2AnonymousWorldPermutation(
        control=P2AnonymousWorldRelation(
            responses=(("alpha", "world:x"), ("beta", "world:y"))
        ),
        intervention=P2AnonymousWorldRelation(
            responses=(("alpha", "world:y"), ("beta", "world:x"))
        ),
    )
    with pytest.raises(ValueError, match="control world does not contain"):
        build_typed_a01_p2_world_fixture(
            expectation=expectation(),
            field_state=field(),
            consistency=UntypedBoundaryConsistency(ProvenanceLedger()),
            return_address=return_address(),
            world_permutation=absent,
            admissible_external_evidence=(external("evidence", 30.0, "world:z"),),
        )


def test_typed_world_binding_rejects_merged_live_boundary() -> None:
    with pytest.raises(ValueError, match="exactly one live boundary proposal"):
        build(address=return_address(proposal_ids=("child", "other")))

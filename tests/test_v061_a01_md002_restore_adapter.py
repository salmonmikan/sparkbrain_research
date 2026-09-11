from __future__ import annotations

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
from sparkbrain.v061_a01.md002_restore_adapter import restore_a01_p2_arm
from sparkbrain.v061_a01.md002_state_binding import (
    LiveReturnAddressState,
    build_bound_a01_p2_fixture,
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


def live_return_address() -> LiveReturnAddressState:
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
    boundary = BoundaryEvent(
        event_id="boundary-live",
        time_ms=17.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-live",
        source_unit_id=2,
        source_proposal_ids=("child",),
        generation_depth=2,
        source_state_hash="field-state",
    )
    return LiveReturnAddressState((child, parent), boundary)


def fixture():
    model = expectation()
    consistency = UntypedBoundaryConsistency(ProvenanceLedger())
    return build_bound_a01_p2_fixture(
        expectation=model,
        field_state=field().state_dict(),
        consistency=consistency,
        return_address=live_return_address(),
        control_world_relation={"port:p": "world:x"},
        intervention_world_relation={"port:p": "world:y"},
        admissible_external_evidence=(
            external("evidence-1", 30.0, "world:z"),
            external("evidence-2", 35.0, "world:q"),
        ),
    )


def test_restore_reconstructs_both_arms_from_identical_runtime_state() -> None:
    frozen = fixture()
    control = restore_a01_p2_arm(frozen.arm("control"))
    intervention = restore_a01_p2_arm(frozen.arm("intervention"))

    assert control.expectation.learned_state_dict() == intervention.expectation.learned_state_dict()
    assert control.field.state_dict() == intervention.field.state_dict()
    assert control.consistency.learned_state_dict() == intervention.consistency.learned_state_dict()
    assert control.ledger.state_dict() == intervention.ledger.state_dict()
    assert control.boundary == intervention.boundary
    assert control.world_relation != intervention.world_relation
    assert control.admissible_external_evidence == intervention.admissible_external_evidence


def test_restore_keeps_external_evidence_unapplied_and_live_boundary_pending() -> None:
    restored = restore_a01_p2_arm(fixture().arm("control"))

    assert restored.ledger.external_observation_count == 0
    assert restored.consistency.resolutions == []
    assert restored.boundary is not None
    assert restored.boundary.event_id in restored.consistency.state_dict()["pending"]
    assert set(restored.ledger.proposals) == {"parent", "child"}
    assert restored.admissible_external_evidence[0].event_id == "evidence-1"
    assert restored.admissible_external_evidence[1].event_id == "evidence-2"

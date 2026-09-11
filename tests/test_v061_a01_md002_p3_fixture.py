from __future__ import annotations

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
from sparkbrain.v061_a01.md002_fixtures import FrozenPartitionBytes
from sparkbrain.v061_a01.md002_p3_fixture import (
    P3ReturnAddressFixture,
    restore_p3_arm,
)
from sparkbrain.v061_a01.md002_state_binding import (
    LiveReturnAddressState,
    canonical_bytes,
    freeze_a01_p2_partitions,
)


def _external(event_id: str, time_ms: float, target: str) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _expectation() -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0)
    )
    model.observe_external_transition(
        _external("train-source", 0.0, "A"),
        _external("train-target", 5.0, "B"),
    )
    return model


def _field() -> TemporalExcitableField:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ),
        (Connection(0, 1, 0.05, 5.0, plastic=True),),
        receptor_ids=(0, 1),
    )
    return TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))


def _return_address(label: str, target: str) -> LiveReturnAddressState:
    proposal = EndogenousPulseProposal(
        proposal_id=f"proposal-{label}",
        created_at_ms=20.0,
        target=target,
        predicted_arrival_ms=25.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="shared-field-state",
        local_path_ids=(f"local:A->{target}",),
        generation_depth=1,
        valid_until_ms=60.0,
        energy_cost=0.1,
    )
    boundary = BoundaryEvent(
        event_id=f"boundary-{label}",
        time_ms=30.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark-{label}",
        source_unit_id=0,
        source_proposal_ids=(proposal.proposal_id,),
        generation_depth=1,
        source_state_hash="shared-field-state",
    )
    return LiveReturnAddressState((proposal,), boundary)


def _checkpoint(return_address: LiveReturnAddressState) -> FrozenPartitionBytes:
    consistency = UntypedBoundaryConsistency(ProvenanceLedger())
    bound = freeze_a01_p2_partitions(
        expectation=_expectation(),
        field_state=_field().state_dict(),
        consistency=consistency,
        return_address=return_address,
    )
    return bound.partitions


def _evidence() -> bytes:
    rows = (
        _external("evidence-1", 70.0, "world:x"),
        _external("evidence-2", 75.0, "world:y"),
    )
    return canonical_bytes([row.as_dict() for row in rows])


def _fixture() -> P3ReturnAddressFixture:
    return P3ReturnAddressFixture(
        baseline=_checkpoint(_return_address("baseline", "B")),
        donor=_checkpoint(_return_address("donor", "C")),
        admissible_external_evidence=_evidence(),
    )


def test_p3_fixture_constructs_r_only_third_arm() -> None:
    fixture = _fixture()
    fixture.validate_isolation()

    baseline = fixture.arm("baseline")
    donor = fixture.arm("donor")
    transplanted = fixture.arm("transplanted")

    assert transplanted.partitions.local == baseline.partitions.local
    assert transplanted.partitions.field == baseline.partitions.field
    assert transplanted.partitions.consistency == baseline.partitions.consistency
    assert transplanted.partitions.return_address == donor.partitions.return_address
    assert transplanted.partitions.return_address != baseline.partitions.return_address
    assert len(
        {
            baseline.admissible_external_evidence_sha256,
            donor.admissible_external_evidence_sha256,
            transplanted.admissible_external_evidence_sha256,
        }
    ) == 1


def test_p3_all_three_arms_restore_actual_state_without_execution() -> None:
    fixture = _fixture()
    fixture.validate_isolation()

    for name in ("baseline", "donor", "transplanted"):
        arm = fixture.arm(name)
        restored = restore_p3_arm(arm)
        assert restored.expectation.learned_state_dict()
        assert restored.field.state_dict()
        assert restored.boundary is not None
        assert restored.admissible_external_evidence


def test_p3_rejects_donor_drift_outside_r() -> None:
    baseline = _checkpoint(_return_address("baseline", "B"))
    donor = _checkpoint(_return_address("donor", "C"))
    drifted = FrozenPartitionBytes(
        local=baseline.local + b" ",
        field=donor.field,
        consistency=donor.consistency,
        return_address=donor.return_address,
    )
    fixture = P3ReturnAddressFixture(
        baseline=baseline,
        donor=drifted,
        admissible_external_evidence=_evidence(),
    )
    with pytest.raises(ValueError, match="donor drifted from baseline in local"):
        fixture.validate()


def test_p3_rejects_identical_return_address() -> None:
    baseline = _checkpoint(_return_address("baseline", "B"))
    fixture = P3ReturnAddressFixture(
        baseline=baseline,
        donor=baseline.restored_copy(),
        admissible_external_evidence=_evidence(),
    )
    with pytest.raises(ValueError, match="donor R must differ"):
        fixture.validate()

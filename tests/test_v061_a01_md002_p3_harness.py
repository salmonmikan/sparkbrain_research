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
from sparkbrain.v061_a01.md002_p3_fixture import P3ReturnAddressFixture
from sparkbrain.v061_a01.md002_p3_harness import (
    prepare_p3_harness,
    prepare_p3_matrix,
    require_p3_execution_authority,
)
from sparkbrain.v061_a01.md002_protocol import MD002ExecutionGate
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


def _field_state() -> dict[str, object]:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ),
        (Connection(0, 1, 0.05, 5.0, plastic=True),),
        receptor_ids=(0, 1),
    )
    field = TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))
    return field.state_dict()


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


def _partitions(return_address: LiveReturnAddressState):
    consistency = UntypedBoundaryConsistency(ProvenanceLedger())
    return freeze_a01_p2_partitions(
        expectation=_expectation(),
        field_state=_field_state(),
        consistency=consistency,
        return_address=return_address,
    ).partitions


def _fixture(direction: str = "ab") -> P3ReturnAddressFixture:
    evidence = canonical_bytes(
        [
            _external(f"evidence-1-{direction}", 70.0, "world:x").as_dict(),
            _external(f"evidence-2-{direction}", 75.0, "world:y").as_dict(),
        ]
    )
    return P3ReturnAddressFixture(
        baseline=_partitions(_return_address(f"baseline-{direction}", "B")),
        donor=_partitions(_return_address(f"donor-{direction}", "C")),
        admissible_external_evidence=evidence,
    )


def test_p3_harness_prepares_three_actual_restorable_arms_without_capability() -> None:
    prepared = prepare_p3_harness(_fixture())

    assert tuple(row.arm for row in prepared) == ("baseline", "donor", "transplanted")
    assert len({row.fixture_sha256 for row in prepared}) == 1
    assert len({row.prospective_execution_id for row in prepared}) == 3
    assert all(row.fixture_sha256 in row.prospective_execution_id for row in prepared)
    assert len({row.admissible_external_evidence_sha256 for row in prepared}) == 1
    assert len({row.observation_schema_sha256 for row in prepared}) == 1
    assert len({row.negative_stop_schema_sha256 for row in prepared}) == 1
    assert all(row.execution_authority is False for row in prepared)
    assert all(row.runtime_trace_sha256 is None for row in prepared)
    assert all(row.capability_result is None and row.score is None for row in prepared)
    assert all(len(row.restored_state_sha256) == 64 for row in prepared)

    by_arm = {row.arm: row.pre_attribution for row in prepared}
    baseline = by_arm["baseline"]
    donor = by_arm["donor"]
    transplanted = by_arm["transplanted"]
    assert baseline.local_sha256 == donor.local_sha256 == transplanted.local_sha256
    assert baseline.field_sha256 == donor.field_sha256 == transplanted.field_sha256
    assert (
        baseline.consistency_sha256
        == donor.consistency_sha256
        == transplanted.consistency_sha256
    )
    assert baseline.return_address_sha256 != donor.return_address_sha256
    assert transplanted.return_address_sha256 == donor.return_address_sha256


def test_p3_matrix_binds_direction_specific_fixture_identity_into_all_six_ids() -> None:
    prepared = prepare_p3_matrix((_fixture("ab"), _fixture("ba")))

    assert len(prepared) == 6
    assert len({row.fixture_sha256 for row in prepared}) == 2
    assert len({row.prospective_execution_id for row in prepared}) == 6
    assert all(row.fixture_sha256 in row.prospective_execution_id for row in prepared)


def test_p3_matrix_rejects_duplicate_fixture_identity() -> None:
    fixture = _fixture("ab")
    with pytest.raises(RuntimeError, match="duplicate fixture identities"):
        prepare_p3_matrix((fixture, fixture))


def test_p3_harness_global_execution_gate_remains_fail_closed() -> None:
    prepare_p3_harness(_fixture())

    with pytest.raises(PermissionError, match="technical-review artifact digest is not pinned"):
        require_p3_execution_authority(MD002ExecutionGate())

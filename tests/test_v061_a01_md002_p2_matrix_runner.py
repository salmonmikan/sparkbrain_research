from __future__ import annotations

from dataclasses import replace

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
from sparkbrain.v061_a01.md002_p2_matrix_runner import execute_p2_development_matrix
from sparkbrain.v061_a01.md002_p2_schedule import (
    P2AttributionSubepisode,
    P2ClonedSubepisodeSchedule,
    P2SharedProbeSchedule,
)
from sparkbrain.v061_a01.md002_state_binding import LiveReturnAddressState
from sparkbrain.v061_a01.md002_world_fixture import (
    P2AnonymousWorldPermutation,
    P2AnonymousWorldRelation,
)


def _external(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    parent_event_ids: tuple[str, ...] = (),
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
        parent_event_ids=parent_event_ids,
    )


def _expectation() -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0)
    )
    model.observe_external_transition(
        _external("train-a-b-source", 0.0, "A"),
        _external("train-a-b-target", 5.0, "B"),
    )
    model.observe_external_transition(
        _external("train-a-c-source", 10.0, "A"),
        _external("train-a-c-target", 15.0, "C"),
    )
    return model


def _field() -> TemporalExcitableField:
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


def _consistency_with_unique_prior() -> UntypedBoundaryConsistency:
    ledger = ProvenanceLedger()
    model = UntypedBoundaryConsistency(ledger)
    boundary = BoundaryEvent(
        event_id="prior-boundary",
        time_ms=1.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-prior",
        source_unit_id=0,
        source_proposal_ids=(),
        generation_depth=0,
        source_state_hash="prior-state",
    )
    response = _external(
        "prior-response",
        5.0,
        "world:x",
        parent_event_ids=(boundary.event_id,),
    )
    model.register_boundary(boundary)
    ledger.register_external(response)
    resolution = model.observe_external(response)
    assert resolution.boundary_event_id == boundary.event_id
    return model


def _return_address() -> LiveReturnAddressState:
    child = EndogenousPulseProposal(
        proposal_id="child",
        created_at_ms=20.0,
        target="B",
        predicted_arrival_ms=25.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        local_path_ids=("local:A->B",),
        generation_depth=1,
        valid_until_ms=60.0,
        energy_cost=0.1,
    )
    other = EndogenousPulseProposal(
        proposal_id="other",
        created_at_ms=20.0,
        target="C",
        predicted_arrival_ms=25.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state",
        local_path_ids=("local:A->C",),
        generation_depth=1,
        valid_until_ms=60.0,
        energy_cost=0.1,
    )
    boundary = BoundaryEvent(
        event_id="boundary-live",
        time_ms=30.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-live",
        source_unit_id=2,
        source_proposal_ids=("child",),
        generation_depth=1,
        source_state_hash="field-state",
    )
    return LiveReturnAddressState((child, other), boundary)


def _permutation() -> P2AnonymousWorldPermutation:
    return P2AnonymousWorldPermutation(
        control=P2AnonymousWorldRelation(
            responses=(("child", "world:x"), ("other", "world:y"))
        ),
        intervention=P2AnonymousWorldRelation(
            responses=(("child", "world:y"), ("other", "world:x"))
        ),
    )


def _schedule() -> P2ClonedSubepisodeSchedule:
    return P2ClonedSubepisodeSchedule(
        subepisodes=(
            P2AttributionSubepisode(
                proposal_id="child",
                boundary_event_id="boundary-child",
                response_event_id="response-child",
                boundary_time_ms=40.0,
                response_time_ms=45.0,
            ),
            P2AttributionSubepisode(
                proposal_id="other",
                boundary_event_id="boundary-other",
                response_event_id="response-other",
                boundary_time_ms=40.0,
                response_time_ms=45.0,
            ),
        ),
        shared_probe=P2SharedProbeSchedule(
            cue_event_id="shared-probe",
            cue_time_ms=50.0,
            root_target="A",
            origin_state_hash="shared-root-state",
        ),
    )


def _fixture():
    return build_typed_a01_p2_world_fixture(
        expectation=_expectation(),
        field_state=_field(),
        consistency=_consistency_with_unique_prior(),
        return_address=_return_address(),
        world_permutation=_permutation(),
        admissible_external_evidence=(
            _external("evidence-1", 70.0, "world:z"),
            _external("evidence-2", 75.0, "world:q"),
        ),
    )


def test_p2_development_matrix_runs_all_registered_cloned_subepisodes() -> None:
    result = execute_p2_development_matrix(_fixture(), _schedule())

    assert tuple(row.condition_id for row in result.conditions) == (
        "p2-w0-returned",
        "p2-w1-returned",
        "p2-w0-withheld",
        "p2-w1-withheld",
    )
    assert all(len(row.subepisodes) == 2 for row in result.conditions)
    assert sum(len(row.subepisodes) for row in result.conditions) == 8
    assert result.expected_subepisode_identities == (
        ("child", "boundary-child", "response-child"),
        ("other", "boundary-other", "response-other"),
    )

    by_id = {row.condition_id: row for row in result.conditions}
    assert tuple(row.response_target for row in by_id["p2-w0-returned"].subepisodes) == (
        "world:x",
        "world:y",
    )
    assert tuple(row.response_target for row in by_id["p2-w1-returned"].subepisodes) == (
        "world:y",
        "world:x",
    )
    assert all(
        row.resolution is not None
        for condition_id in ("p2-w0-returned", "p2-w1-returned")
        for row in by_id[condition_id].subepisodes
    )
    assert all(
        row.resolution is None
        for condition_id in ("p2-w0-withheld", "p2-w1-withheld")
        for row in by_id[condition_id].subepisodes
    )


def test_p2_development_matrix_rejects_result_identity_drift() -> None:
    result = execute_p2_development_matrix(_fixture(), _schedule())
    first_condition = result.conditions[0]
    drifted_result = replace(
        first_condition.subepisodes[0],
        proposal_id="unexpected-clone",
    )
    drifted_condition = replace(
        first_condition,
        subepisodes=(drifted_result, first_condition.subepisodes[1]),
    )
    drifted_matrix = replace(
        result,
        conditions=(drifted_condition, *result.conditions[1:]),
    )

    with pytest.raises(RuntimeError, match="fixed cloned subepisode schedule"):
        drifted_matrix.validate()


def test_p2_development_matrix_rejects_event_identity_drift() -> None:
    result = execute_p2_development_matrix(_fixture(), _schedule())
    first_condition = result.conditions[0]
    drifted_result = replace(
        first_condition.subepisodes[0],
        boundary_event_id="unexpected-boundary",
    )
    drifted_condition = replace(
        first_condition,
        subepisodes=(drifted_result, first_condition.subepisodes[1]),
    )
    drifted_matrix = replace(
        result,
        conditions=(drifted_condition, *result.conditions[1:]),
    )

    with pytest.raises(RuntimeError, match="fixed cloned subepisode schedule"):
        drifted_matrix.validate()


def test_p2_development_matrix_serialization_remains_execution_disabled() -> None:
    state = execute_p2_development_matrix(_fixture(), _schedule()).state_dict()

    assert state["capability_scored"] is False
    assert state["formal_execution_opened"] is False
    assert state["expected_subepisode_identities"] == [
        {
            "proposal_id": "child",
            "boundary_event_id": "boundary-child",
            "response_event_id": "response-child",
        },
        {
            "proposal_id": "other",
            "boundary_event_id": "boundary-other",
            "response_event_id": "response-other",
        },
    ]
    assert len(state["conditions"]) == 4
    assert all(len(row["subepisodes"]) == 2 for row in state["conditions"])

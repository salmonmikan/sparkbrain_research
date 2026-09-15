from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v04 import Connection, ExcitableFieldConfig, TemporalExcitableField, UnitState, explicit_topology
from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import EndogenousPulseProposal, EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.local_expectation import LocalExpectationConfig
from sparkbrain.v061_a01.credit_bridge import A01LocalTemporalExpectation
from sparkbrain.v061_a01.md002_bound_world import build_typed_a01_p2_world_fixture
from sparkbrain.v061_a01.md002_p2_schedule import P2AttributionSubepisode, P2ClonedSubepisodeSchedule, P2SharedProbeSchedule
from sparkbrain.v061_a01.md002_p2_shared_probe import execute_p2_shared_probe
from sparkbrain.v061_a01.md002_state_binding import LiveReturnAddressState
from sparkbrain.v061_a01.md002_world_fixture import P2AnonymousWorldPermutation, P2AnonymousWorldRelation


def _external(event_id: str, time_ms: float, target: str, *, parent_event_ids: tuple[str, ...] = ()) -> RuntimePulse:
    return RuntimePulse(event_id=event_id, time_ms=time_ms, target=target, magnitude=1.0, polarity=1, origin=EventOrigin.EXTERNAL, parent_event_ids=parent_event_ids)


def _expectation() -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0))
    model.observe_external_transition(_external("train-a-b-source", 0.0, "A"), _external("train-a-b-target", 5.0, "B"))
    model.observe_external_transition(_external("train-a-c-source", 10.0, "A"), _external("train-a-c-target", 15.0, "C"))
    return model


def _field() -> TemporalExcitableField:
    topology = explicit_topology(
        (UnitState(0, 0.0, 0.0, base_threshold=0.5), UnitState(1, 1.0, 0.0, base_threshold=0.5), UnitState(2, 0.5, 1.0, base_threshold=0.5)),
        (Connection(0, 2, 0.05, 5.0, plastic=True), Connection(2, 1, 0.05, 5.0, plastic=True), Connection(0, 1, 0.05, 5.0, plastic=True)),
        receptor_ids=(0, 1),
    )
    return TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))


def _consistency() -> UntypedBoundaryConsistency:
    ledger = ProvenanceLedger()
    model = UntypedBoundaryConsistency(ledger)
    boundary = BoundaryEvent(event_id="prior-boundary", time_ms=1.0, port_id="port:p", magnitude=1.0, polarity=1, direction=BoundaryDirection.FIELD_TO_WORLD, source_spark_id="spark-prior", source_unit_id=0, source_proposal_ids=(), generation_depth=0, source_state_hash="prior-state")
    response = _external("prior-response", 5.0, "world:x", parent_event_ids=(boundary.event_id,))
    model.register_boundary(boundary)
    ledger.register_external(response)
    model.observe_external(response)
    return model


def _return_address() -> LiveReturnAddressState:
    child = EndogenousPulseProposal(proposal_id="child", created_at_ms=20.0, target="B", predicted_arrival_ms=25.0, magnitude=1.0, polarity=1, confidence=0.5, origin_state_hash="field-state", local_path_ids=("local:A->B",), generation_depth=1, valid_until_ms=60.0, energy_cost=0.1)
    other = EndogenousPulseProposal(proposal_id="other", created_at_ms=20.0, target="C", predicted_arrival_ms=25.0, magnitude=1.0, polarity=1, confidence=0.5, origin_state_hash="field-state", local_path_ids=("local:A->C",), generation_depth=1, valid_until_ms=60.0, energy_cost=0.1)
    boundary = BoundaryEvent(event_id="boundary-live", time_ms=30.0, port_id="port:p", magnitude=1.0, polarity=1, direction=BoundaryDirection.FIELD_TO_WORLD, source_spark_id="spark-live", source_unit_id=2, source_proposal_ids=("child",), generation_depth=1, source_state_hash="field-state")
    return LiveReturnAddressState((child, other), boundary)


def build_registered_fixture_and_schedule():
    permutation = P2AnonymousWorldPermutation(
        control=P2AnonymousWorldRelation(responses=(("child", "world:x"), ("other", "world:y"))),
        intervention=P2AnonymousWorldRelation(responses=(("child", "world:y"), ("other", "world:x"))),
    )
    schedule = P2ClonedSubepisodeSchedule(
        subepisodes=(
            P2AttributionSubepisode("child", "boundary-child", "response-child", 40.0, 45.0),
            P2AttributionSubepisode("other", "boundary-other", "response-other", 40.0, 45.0),
        ),
        shared_probe=P2SharedProbeSchedule("shared-probe", 50.0, "A", "shared-root-state"),
    )
    fixture = build_typed_a01_p2_world_fixture(
        expectation=_expectation(), field_state=_field(), consistency=_consistency(), return_address=_return_address(), world_permutation=permutation,
        admissible_external_evidence=(_external("evidence-1", 70.0, "world:z"), _external("evidence-2", 75.0, "world:q")),
    )
    return fixture, schedule


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    fixture, schedule = build_registered_fixture_and_schedule()
    result = execute_p2_shared_probe(fixture, schedule).state_dict()
    payload = {
        "identity": f"a01-md002-p2-shared-probe-{args.source_sha[:16]}",
        "source_sha": args.source_sha,
        "result": result,
    }
    Path(args.output).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()

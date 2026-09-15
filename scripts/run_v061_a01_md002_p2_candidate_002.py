from __future__ import annotations

import argparse
import json
from pathlib import Path

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
from sparkbrain.v061_a01.md002_p2_raw_pipeline import (
    P2SharedProbeRaw,
    acquire_p2_shared_probe,
    score_preserved_p2_shared_probe,
)
from sparkbrain.v061_a01.md002_p2_schedule import (
    P2AttributionSubepisode,
    P2ClonedSubepisodeSchedule,
    P2SharedProbeSchedule,
)
from sparkbrain.v061_a01.md002_protocol import canonical_sha256
from sparkbrain.v061_a01.md002_state_binding import LiveReturnAddressState
from sparkbrain.v061_a01.md002_world_fixture import (
    P2AnonymousWorldPermutation,
    P2AnonymousWorldRelation,
)

CANDIDATE_ID = "a01-md002-p2-shared-probe-candidate-002-v1"


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


def _candidate_expectation() -> A01LocalTemporalExpectation:
    """A prospectively distinct learned root: R -> {S,T} at a 7 ms delay."""

    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(minimum_observations=1, minimum_confidence=0.0)
    )
    for source_id, target_id, source_time, target in (
        ("c2-rs-source-1", "c2-rs-target-1", 0.0, "S"),
        ("c2-rt-source-1", "c2-rt-target-1", 20.0, "T"),
        ("c2-rs-source-2", "c2-rs-target-2", 40.0, "S"),
        ("c2-rt-source-2", "c2-rt-target-2", 60.0, "T"),
    ):
        model.observe_external_transition(
            _external(source_id, source_time, "R"),
            _external(target_id, source_time + 7.0, target),
        )
    return model


def _candidate_field() -> TemporalExcitableField:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.45),
            UnitState(1, 1.0, 0.0, base_threshold=0.45),
            UnitState(2, 0.5, 1.0, base_threshold=0.55),
        ),
        (
            Connection(0, 2, 0.06, 6.0, plastic=True),
            Connection(2, 1, 0.04, 6.0, plastic=True),
            Connection(0, 1, 0.05, 6.0, plastic=True),
        ),
        receptor_ids=(0, 1),
    )
    return TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))


def _candidate_consistency() -> UntypedBoundaryConsistency:
    ledger = ProvenanceLedger()
    model = UntypedBoundaryConsistency(ledger)
    boundary = BoundaryEvent(
        event_id="c2-prior-boundary",
        time_ms=10.0,
        port_id="port:q",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-c2-prior",
        source_unit_id=0,
        source_proposal_ids=(),
        generation_depth=0,
        source_state_hash="c2-prior-state",
    )
    response = _external(
        "c2-prior-response",
        17.0,
        "world:u",
        parent_event_ids=(boundary.event_id,),
    )
    model.register_boundary(boundary)
    ledger.register_external(response)
    model.observe_external(response)
    return model


def _candidate_return_address() -> LiveReturnAddressState:
    left = EndogenousPulseProposal(
        proposal_id="c2-left",
        created_at_ms=100.0,
        target="S",
        predicted_arrival_ms=107.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state-candidate-002",
        local_path_ids=("local:R->S",),
        generation_depth=1,
        valid_until_ms=220.0,
        energy_cost=0.12,
    )
    right = EndogenousPulseProposal(
        proposal_id="c2-right",
        created_at_ms=100.0,
        target="T",
        predicted_arrival_ms=107.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="field-state-candidate-002",
        local_path_ids=("local:R->T",),
        generation_depth=1,
        valid_until_ms=220.0,
        energy_cost=0.12,
    )
    boundary = BoundaryEvent(
        event_id="c2-boundary-live",
        time_ms=120.0,
        port_id="port:q",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-c2-live",
        source_unit_id=2,
        source_proposal_ids=("c2-left",),
        generation_depth=1,
        source_state_hash="field-state-candidate-002",
    )
    return LiveReturnAddressState((left, right), boundary)


def build_candidate_002_fixture_and_schedule() -> tuple[object, P2ClonedSubepisodeSchedule]:
    """Build candidate-002 without executing or scoring it."""

    permutation = P2AnonymousWorldPermutation(
        control=P2AnonymousWorldRelation(
            responses=(("c2-left", "world:u"), ("c2-right", "world:v"))
        ),
        intervention=P2AnonymousWorldRelation(
            responses=(("c2-left", "world:v"), ("c2-right", "world:u"))
        ),
    )
    schedule = P2ClonedSubepisodeSchedule(
        subepisodes=(
            P2AttributionSubepisode(
                "c2-left",
                "c2-boundary-left",
                "c2-response-left",
                140.0,
                147.0,
            ),
            P2AttributionSubepisode(
                "c2-right",
                "c2-boundary-right",
                "c2-response-right",
                140.0,
                147.0,
            ),
        ),
        shared_probe=P2SharedProbeSchedule(
            "c2-shared-probe",
            155.0,
            "R",
            "c2-shared-root-state",
        ),
    )
    fixture = build_typed_a01_p2_world_fixture(
        expectation=_candidate_expectation(),
        field_state=_candidate_field(),
        consistency=_candidate_consistency(),
        return_address=_candidate_return_address(),
        world_permutation=permutation,
        admissible_external_evidence=(
            _external("c2-admissible-1", 240.0, "world:m"),
            _external("c2-admissible-2", 250.0, "world:n"),
        ),
    )
    fixture.validate()
    schedule.validate()
    return fixture, schedule


def _contract_state(fixture: object) -> dict[str, object]:
    contract = fixture.prospective_contract()
    contract.validate()
    return {
        "control": contract.control.state_dict(),
        "intervention": contract.intervention.state_dict(),
        "control_world_relation_sha256": contract.control_world_relation_sha256,
        "intervention_world_relation_sha256": contract.intervention_world_relation_sha256,
        "admissible_external_evidence_sha256": contract.admissible_external_evidence_sha256,
    }


def candidate_manifest(source_sha: str) -> dict[str, object]:
    if len(source_sha) != 40:
        raise ValueError("source SHA must be an exact 40-character Git SHA")
    fixture, schedule = build_candidate_002_fixture_and_schedule()
    input_contract = {
        "candidate_id": CANDIDATE_ID,
        "world_only_contract": _contract_state(fixture),
        "schedule": schedule.state_dict(),
    }
    input_digest = canonical_sha256(input_contract)
    execution_identity = (
        "a01-md002-p2-candidate-002-"
        + canonical_sha256({"source_sha": source_sha, "input_digest": input_digest})[:24]
    )
    return {
        "schema": "v061-a01-md002-p2-candidate-manifest-v1",
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "input_digest": input_digest,
        "execution_identity": execution_identity,
        "input_contract": input_contract,
        "development_only": True,
        "held_out_execution_allowed": False,
        "formal_execution_allowed": False,
    }


def _write_json(path: str, payload: dict[str, object]) -> None:
    Path(path).write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_json(path: str) -> dict[str, object]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("expected a JSON object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("manifest", "acquire", "score"))
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-input")
    args = parser.parse_args()

    manifest = candidate_manifest(args.source_sha)
    if args.mode == "manifest":
        _write_json(args.output, manifest)
        print(json.dumps({"execution_identity": manifest["execution_identity"]}, sort_keys=True))
        return

    if args.mode == "acquire":
        if args.raw_input is not None:
            raise ValueError("acquire mode does not accept --raw-input")
        fixture, schedule = build_candidate_002_fixture_and_schedule()
        raw = acquire_p2_shared_probe(fixture, schedule)
        payload = {
            "schema": "v061-a01-md002-p2-candidate-raw-envelope-v1",
            "manifest": manifest,
            "raw": raw.state_dict(),
        }
        _write_json(args.output, payload)
        print(
            json.dumps(
                {"execution_identity": manifest["execution_identity"], "scored": False},
                sort_keys=True,
            )
        )
        return

    if args.raw_input is None:
        raise ValueError("score mode requires --raw-input")
    envelope = _read_json(args.raw_input)
    if envelope.get("schema") != "v061-a01-md002-p2-candidate-raw-envelope-v1":
        raise ValueError("unexpected P2 raw envelope schema")
    if envelope.get("manifest") != manifest:
        raise ValueError("P2 preserved raw manifest does not match frozen candidate")
    raw_value = envelope.get("raw")
    if not isinstance(raw_value, dict):
        raise TypeError("P2 preserved raw payload is missing")
    raw = P2SharedProbeRaw.from_state_dict(raw_value)
    scored = score_preserved_p2_shared_probe(raw)
    payload = {
        "schema": "v061-a01-md002-p2-candidate-scored-v1",
        "manifest": manifest,
        "raw_sha256": canonical_sha256(envelope),
        "result": scored.state_dict(),
    }
    _write_json(args.output, payload)
    print(
        json.dumps(
            {
                "execution_identity": manifest["execution_identity"],
                "verdict": scored.verdict,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

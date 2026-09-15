#!/usr/bin/env python3
"""Exactly-once development runner for A01 MD-002 P3 R-only causal-carrier probe.

This candidate is exploratory/development evidence.  It binds a fresh six-arm
counterbalanced R-only transplant matrix before execution, acquires raw runtime
observations without scoring, and applies only the prospectively encoded
deterministic classifier in ``score`` mode.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

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
from sparkbrain.v061_a01.credit_bridge import (
    A01LocalTemporalExpectation,
    A01TransientCreditBridge,
)
from sparkbrain.v061_a01.md002_p3_fixture import (
    P3ReturnAddressFixture,
    restore_p3_arm,
)
from sparkbrain.v061_a01.md002_p3_harness import (
    P3DirectionalFixture,
    prepare_p3_matrix,
)
from sparkbrain.v061_a01.md002_protocol import canonical_sha256
from sparkbrain.v061_a01.md002_state_binding import (
    LiveReturnAddressState,
    canonical_bytes,
    freeze_a01_p2_partitions,
)

CANDIDATE_ID = "a01-md002-p3-r-only-causal-carrier-candidate-001-v1"
CONTRACT_SCHEMA = "v061-a01-md002-p3-causal-carrier-candidate-v1"
RAW_SCHEMA = "v061-a01-md002-p3-causal-carrier-raw-v1"
SCORE_SCHEMA = "v061-a01-md002-p3-causal-carrier-score-v1"
CLASSIFIER_VERSION = "p3-r-only-development-classifier-v1"
DIRECTIONS = ("A-to-B", "B-to-A")
ARMS = ("baseline", "donor", "transplanted")
EXPECTED_WINNERS = {
    "A-to-B": {"baseline": "B", "donor": "C", "transplanted": "C"},
    "B-to-A": {"baseline": "C", "donor": "B", "transplanted": "B"},
}
SUPPORTED = "SUPPORTED_R_CAUSAL_CARRIER"
BASELINE_FOLLOWING = "BASELINE_FOLLOWING"
NO_DIFFERENTIAL = "NO_DIFFERENTIAL_EFFECT"
AMBIGUOUS = "AMBIGUOUS"
INVALID = "INVALID"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical(value) + b"\n")


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
    # Symmetric local competition: both routes have the same observation count
    # and timing statistics before attribution.
    model.observe_external_transition(
        _external("train-b-source", 0.0, "A"),
        _external("train-b-target", 5.0, "B"),
    )
    model.observe_external_transition(
        _external("train-c-source", 10.0, "A"),
        _external("train-c-target", 15.0, "C"),
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
    return TemporalExcitableField(
        topology, ExcitableFieldConfig(receptor_fanout=1)
    ).state_dict()


def _consistency_with_shared_prior() -> UntypedBoundaryConsistency:
    ledger = ProvenanceLedger()
    model = UntypedBoundaryConsistency(ledger)
    prior_boundary = BoundaryEvent(
        event_id="p3-prior-boundary",
        time_ms=0.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark-prior",
        source_unit_id=0,
        source_proposal_ids=(),
        generation_depth=0,
        source_state_hash="p3-shared-field-state",
    )
    model.register_boundary(prior_boundary)
    prior_external = _external(
        "p3-prior-external",
        5.0,
        "world:x",
        parent_event_ids=(prior_boundary.event_id,),
    )
    ledger.register_external(prior_external)
    resolution = model.observe_external(prior_external)
    if resolution.status != "externally-consistent":
        raise RuntimeError("failed to construct shared anonymous prior")
    return model


def _return_address(direction: str, arm_lineage: str) -> LiveReturnAddressState:
    target = {"A": "B", "B": "C"}[arm_lineage]
    # Boundary ID is deliberately identical within a direction so the exact
    # same external evidence bytes can be applied to all three arms. R differs
    # only through the retained causal proposal/path identity.
    boundary_id = f"p3-boundary-{direction}"
    proposal = EndogenousPulseProposal(
        proposal_id=f"p3-proposal-{direction}-{arm_lineage}",
        created_at_ms=20.0,
        target=target,
        predicted_arrival_ms=25.0,
        magnitude=1.0,
        polarity=1,
        confidence=0.5,
        origin_state_hash="p3-shared-field-state",
        local_path_ids=(f"local:A->{target}",),
        generation_depth=1,
        valid_until_ms=60.0,
        energy_cost=0.1,
    )
    boundary = BoundaryEvent(
        event_id=boundary_id,
        time_ms=30.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark-p3-{direction}",
        source_unit_id=0,
        source_proposal_ids=(proposal.proposal_id,),
        generation_depth=1,
        source_state_hash="p3-shared-field-state",
    )
    return LiveReturnAddressState((proposal,), boundary)


def _partitions(direction: str, lineage: str):
    return freeze_a01_p2_partitions(
        expectation=_expectation(),
        field_state=_field_state(),
        consistency=_consistency_with_shared_prior(),
        return_address=_return_address(direction, lineage),
    ).partitions


def _directional(direction: str) -> P3DirectionalFixture:
    baseline_lineage, donor_lineage = {
        "A-to-B": ("A", "B"),
        "B-to-A": ("B", "A"),
    }[direction]
    boundary_id = f"p3-boundary-{direction}"
    evidence = canonical_bytes(
        [
            _external(
                f"p3-evidence-{direction}",
                35.0,
                "world:x",
                parent_event_ids=(boundary_id,),
            ).as_dict()
        ]
    )
    fixture = P3ReturnAddressFixture(
        baseline=_partitions(direction, baseline_lineage),
        donor=_partitions(direction, donor_lineage),
        admissible_external_evidence=evidence,
    )
    fixture.validate_isolation()
    return P3DirectionalFixture(direction=direction, fixture=fixture)


def _matrix() -> tuple[P3DirectionalFixture, ...]:
    value = tuple(_directional(direction) for direction in DIRECTIONS)
    prepare_p3_matrix(value)  # fail-closed reuse of the pre-existing P3 harness
    return value


def _competition(expectation: A01LocalTemporalExpectation) -> dict[str, Any]:
    source = _external("p3-future-probe", 100.0, "A")
    rows = expectation.proposals_for(source, origin_state_hash="p3-future-probe-state")
    selected = sorted(
        (
            {
                "target": row.target,
                "confidence": row.confidence,
                "local_path_ids": list(row.local_path_ids),
            }
            for row in rows
        ),
        key=lambda row: (-float(row["confidence"]), str(row["target"])),
    )
    maximum = max(float(row["confidence"]) for row in selected)
    winners = sorted(
        str(row["target"])
        for row in selected
        if float(row["confidence"]) == maximum
    )
    return {
        "proposals": selected,
        "winner": winners[0] if len(winners) == 1 else None,
        "tied_winners": winners,
    }


def _execute_arm(
    directional: P3DirectionalFixture,
    arm_name: str,
    prospective_execution_id: str,
) -> dict[str, Any]:
    arm_input = directional.fixture.arm(arm_name)  # type: ignore[arg-type]
    restored = restore_p3_arm(arm_input)
    if restored.boundary is None:
        raise RuntimeError("P3 runtime requires a restored boundary")

    pre = {
        "local": restored.expectation.learned_state_dict(),
        "field": restored.field.state_dict(),
        "consistency": restored.consistency.learned_state_dict(),
        "return_address_sha256": arm_input.snapshot().return_address_sha256,
        "competition": _competition(restored.expectation),
    }

    evidence = restored.admissible_external_evidence
    if len(evidence) != 1:
        raise RuntimeError("candidate contract requires exactly one external evidence pulse")
    external = evidence[0]
    restored.ledger.register_external(external)
    bridge = A01TransientCreditBridge(
        restored.expectation, restored.consistency, restored.ledger
    )
    resolution = bridge.observe_external(restored.boundary, external)

    post = {
        "local": restored.expectation.learned_state_dict(),
        "field": restored.field.state_dict(),
        "consistency": restored.consistency.learned_state_dict(),
        "competition": _competition(restored.expectation),
    }
    return {
        "direction": directional.direction,
        "arm": arm_name,
        "prospective_execution_id": prospective_execution_id,
        "external_evidence": external.as_dict(),
        "credit_resolution": resolution.state_dict(),
        "pre": pre,
        "post": post,
        "hashes": {
            "pre_local": canonical_sha256(pre["local"]),
            "pre_field": canonical_sha256(pre["field"]),
            "pre_consistency": canonical_sha256(pre["consistency"]),
            "post_local": canonical_sha256(post["local"]),
            "post_field": canonical_sha256(post["field"]),
            "post_consistency": canonical_sha256(post["consistency"]),
        },
    }


def _contract(source_sha: str) -> dict[str, Any]:
    matrix = _matrix()
    prepared = prepare_p3_matrix(matrix)
    prepared_rows = [asdict(row) for row in prepared]
    fixture_rows = []
    for directional in matrix:
        fixture = directional.fixture
        fixture_rows.append(
            {
                "direction": directional.direction,
                "baseline": fixture.baseline.snapshot().state_dict(),
                "donor": fixture.donor.snapshot().state_dict(),
                "evidence_sha256": _sha256_bytes(fixture.admissible_external_evidence),
            }
        )
    classifier = {
        "version": CLASSIFIER_VERSION,
        "development_only": True,
        "supported_requires": [
            "all six arms execute exactly once under distinct prepared execution IDs",
            "within each direction pre L/F/C hashes and external evidence bytes match across arms",
            "baseline R differs from donor R and transplanted R equals donor R",
            "post Field hashes equal pre Field hashes for every arm",
            "post consistency learned state is byte-identical across all three arms "
            "in each direction",
            "each arm records exact-match credit on exactly its retained local path",
            "future competition winner is baseline target for baseline and donor target "
            "for donor/transplanted",
            "the supported pattern holds in both counterbalanced directions",
        ],
        "verdict_order": [
            INVALID,
            SUPPORTED,
            BASELINE_FOLLOWING,
            NO_DIFFERENTIAL,
            AMBIGUOUS,
        ],
        "invalid_if": [
            "binding/isolation/evidence equality fails",
            "post Field changes",
            "post consistency differs between arms within a direction",
            "credit is not exact-match or is applied to an unexpected path",
            "execution identity is missing or duplicated",
        ],
    }
    contract = {
        "schema": CONTRACT_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "development_only": True,
        "held_out_execution_allowed": False,
        "formal_execution_allowed": False,
        "same_identity_rerun_allowed": False,
        "scientific_scope": (
            "R-only causal-carrier development discriminator; final classifier was "
            "prospectively fixed for this fresh development identity after P2 and "
            "must not be represented as pre-P2 confirmatory evidence"
        ),
        "prepared_arms": prepared_rows,
        "fixtures": fixture_rows,
        "classifier": classifier,
    }
    contract["contract_sha256"] = canonical_sha256(contract)
    return contract


def _acquire(source_sha: str) -> dict[str, Any]:
    contract = _contract(source_sha)
    prepared = {
        (row["direction"], row["arm"]): row for row in contract["prepared_arms"]
    }
    observations = []
    for directional in _matrix():
        for arm_name in ARMS:
            row = prepared[(directional.direction, arm_name)]
            observations.append(
                _execute_arm(
                    directional,
                    arm_name,
                    str(row["prospective_execution_id"]),
                )
            )
    return {
        "schema": RAW_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "contract_sha256": contract["contract_sha256"],
        "contract": contract,
        "observations": observations,
    }


def _score(source_sha: str, raw: dict[str, Any]) -> dict[str, Any]:
    expected_contract = _contract(source_sha)
    if raw.get("schema") != RAW_SCHEMA or raw.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("raw envelope identity/schema mismatch")
    if raw.get("source_sha") != source_sha:
        raise ValueError("raw source SHA mismatch")
    if raw.get("contract") != expected_contract:
        raise ValueError("raw candidate contract differs from frozen scorer contract")
    if raw.get("contract_sha256") != expected_contract["contract_sha256"]:
        raise ValueError("raw contract digest mismatch")

    observations = raw.get("observations")
    if not isinstance(observations, list) or len(observations) != 6:
        raise ValueError("P3 raw evidence must contain exactly six arms")
    by_key = {(row["direction"], row["arm"]): row for row in observations}
    if len(by_key) != 6:
        raise ValueError("P3 raw evidence contains duplicate direction/arm rows")

    invalid_reasons: list[str] = []
    direction_summaries: list[dict[str, Any]] = []
    all_supported = True
    all_baseline_following = True
    all_no_differential = True

    for direction in DIRECTIONS:
        rows = {arm: by_key[(direction, arm)] for arm in ARMS}
        execution_ids = {rows[arm]["prospective_execution_id"] for arm in ARMS}
        if len(execution_ids) != 3:
            invalid_reasons.append(f"{direction}: execution IDs are not distinct")

        pre_local = {canonical_sha256(rows[a]["pre"]["local"]) for a in ARMS}
        pre_field = {canonical_sha256(rows[a]["pre"]["field"]) for a in ARMS}
        pre_consistency = {
            canonical_sha256(rows[a]["pre"]["consistency"]) for a in ARMS
        }
        evidence = {canonical_sha256(rows[a]["external_evidence"]) for a in ARMS}
        if len(pre_local) != 1:
            invalid_reasons.append(f"{direction}: pre local state drift")
        if len(pre_field) != 1:
            invalid_reasons.append(f"{direction}: pre Field state drift")
        if len(pre_consistency) != 1:
            invalid_reasons.append(f"{direction}: pre consistency state drift")
        if len(evidence) != 1:
            invalid_reasons.append(f"{direction}: external evidence drift")

        r_hash = {arm: rows[arm]["pre"]["return_address_sha256"] for arm in ARMS}
        if r_hash["baseline"] == r_hash["donor"]:
            invalid_reasons.append(f"{direction}: baseline/donor R not distinct")
        if r_hash["transplanted"] != r_hash["donor"]:
            invalid_reasons.append(f"{direction}: transplanted R does not equal donor R")

        for arm in ARMS:
            if canonical_sha256(rows[arm]["pre"]["field"]) != canonical_sha256(
                rows[arm]["post"]["field"]
            ):
                invalid_reasons.append(f"{direction}/{arm}: post Field changed")

        post_consistency = {
            canonical_sha256(rows[a]["post"]["consistency"]) for a in ARMS
        }
        if len(post_consistency) != 1:
            invalid_reasons.append(
                f"{direction}: post consistency differs across matched-evidence arms"
            )

        expected_paths = {
            "baseline": "local:A->B" if direction == "A-to-B" else "local:A->C",
            "donor": "local:A->C" if direction == "A-to-B" else "local:A->B",
            "transplanted": "local:A->C" if direction == "A-to-B" else "local:A->B",
        }
        for arm in ARMS:
            resolution = rows[arm]["credit_resolution"]
            if resolution["status"] != "exact-match":
                invalid_reasons.append(
                    f"{direction}/{arm}: credit status {resolution['status']}"
                )
            if resolution["path_ids"] != [expected_paths[arm]]:
                invalid_reasons.append(
                    f"{direction}/{arm}: unexpected credited path {resolution['path_ids']}"
                )

        winners = {arm: rows[arm]["post"]["competition"]["winner"] for arm in ARMS}
        expected = EXPECTED_WINNERS[direction]
        supported = winners == expected
        baseline_following = (
            winners["baseline"] == expected["baseline"]
            and winners["donor"] == expected["donor"]
            and winners["transplanted"] == expected["baseline"]
        )
        no_differential = len(set(winners.values())) == 1
        all_supported &= supported
        all_baseline_following &= baseline_following
        all_no_differential &= no_differential
        direction_summaries.append(
            {
                "direction": direction,
                "winners": winners,
                "expected_supported_winners": expected,
                "supported_pattern": supported,
                "baseline_following_pattern": baseline_following,
                "no_differential_pattern": no_differential,
            }
        )

    if invalid_reasons:
        verdict = INVALID
    elif all_supported:
        verdict = SUPPORTED
    elif all_baseline_following:
        verdict = BASELINE_FOLLOWING
    elif all_no_differential:
        verdict = NO_DIFFERENTIAL
    else:
        verdict = AMBIGUOUS

    return {
        "schema": SCORE_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "contract_sha256": expected_contract["contract_sha256"],
        "raw_sha256": _sha256_bytes(_canonical(raw)),
        "classifier_version": CLASSIFIER_VERSION,
        "development_only": True,
        "held_out": False,
        "formal": False,
        "verdict": verdict,
        "invalid_reasons": invalid_reasons,
        "directions": direction_summaries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("manifest", "acquire", "score"))
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-input")
    args = parser.parse_args()

    if args.mode == "manifest":
        value = _contract(args.source_sha)
    elif args.mode == "acquire":
        value = _acquire(args.source_sha)
    else:
        if not args.raw_input:
            parser.error("score requires --raw-input")
        raw = json.loads(Path(args.raw_input).read_text())
        if not isinstance(raw, dict):
            raise ValueError("raw input must be a JSON object")
        value = _score(args.source_sha, raw)
    _write_json(Path(args.output), value)


if __name__ == "__main__":
    main()

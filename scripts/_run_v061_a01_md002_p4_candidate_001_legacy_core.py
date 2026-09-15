#!/usr/bin/env python3
"""Exactly-once development runner for A01 MD-002 P4 merged-lineage resolution.

The fresh P4 identity asks whether genuinely plural historical ancestry can be
resolved selectively by later external evidence that carries an actual retained
lineage parent, without semantic labels or a caller-selected lineage field.

The acquisition path records raw observations only. Scientific classification
is applied exclusively in ``score`` mode after raw evidence has been preserved
and re-verified by the workflow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

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
    A01CausalCreditStatus,
    A01LocalTemporalExpectation,
    A01TransientCreditBridge,
)
from sparkbrain.v061_a01.md002_p4_credit_probe import probe_merged_lineage_credit
from sparkbrain.v061_a01.md002_p4_fixture import P4ProspectiveFixture
from sparkbrain.v061_a01.md002_protocol import canonical_sha256

CANDIDATE_ID = "a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1"
CONTRACT_SCHEMA = "v061-a01-md002-p4-selective-resolution-candidate-v1"
RAW_SCHEMA = "v061-a01-md002-p4-selective-resolution-raw-v1"
SCORE_SCHEMA = "v061-a01-md002-p4-selective-resolution-score-v1"
CLASSIFIER_VERSION = "p4-selective-resolution-development-classifier-v1"

SUPPORTED = "SUPPORTED_SELECTIVE_MERGED_LINEAGE_RESOLUTION"
EN_BLOC = "UNSUPPORTED_EN_BLOC_MERGED_CREDIT"
NO_EFFECT = "NO_SELECTIVE_MERGED_EFFECT"
PREMATURE_COLLAPSE = "PREMATURE_SINGLETON_COLLAPSE"
AMBIGUOUS = "AMBIGUOUS"
INVALID = "INVALID"

CONDITION_IDS = (
    "p4-separate-confirmation",
    "p4-merged-confirmation",
    "p4-merged-separating-confirmation",
    "p4-merged-separating-contradiction",
    "p4-merged-absence",
    "p4-merged-replay",
)


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


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _pulse(
    event_id: str,
    time_ms: float,
    target: str,
    *,
    polarity: int = 1,
    origin: EventOrigin = EventOrigin.EXTERNAL,
    parent_event_ids: tuple[str, ...] = (),
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=polarity,
        origin=origin,
        parent_event_ids=parent_event_ids,
    )


def _expectation() -> A01LocalTemporalExpectation:
    model = A01LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=1,
            minimum_confidence=0.0,
            proposal_ttl_ms=120.0,
        )
    )
    model.observe_external_transition(
        _pulse("p4-train-ab-source", 0.0, "A"),
        _pulse("p4-train-ab-target", 5.0, "B"),
    )
    model.observe_external_transition(
        _pulse("p4-train-ac-source", 10.0, "A"),
        _pulse("p4-train-ac-target", 15.0, "C"),
    )
    return model


def _competition(expectation: A01LocalTemporalExpectation) -> dict[str, Any]:
    source = _pulse("p4-future-probe", 100.0, "A")
    rows = expectation.proposals_for(
        source,
        origin_state_hash="p4-future-probe-state",
    )
    proposals = sorted(
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
    if not proposals:
        return {"proposals": [], "winner": None, "tied_winners": []}
    maximum = max(float(row["confidence"]) for row in proposals)
    winners = sorted(
        str(row["target"])
        for row in proposals
        if float(row["confidence"]) == maximum
    )
    return {
        "proposals": proposals,
        "winner": winners[0] if len(winners) == 1 else None,
        "tied_winners": winners,
    }


def _prior_consistency(ledger: ProvenanceLedger) -> UntypedBoundaryConsistency:
    model = UntypedBoundaryConsistency(ledger)
    boundary = BoundaryEvent(
        event_id="p4-prior-boundary",
        time_ms=0.0,
        port_id="port:p",
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id="spark:p4-prior",
        source_unit_id=0,
        source_proposal_ids=(),
        generation_depth=0,
        source_state_hash="p4-prior-state",
    )
    external = _pulse(
        "p4-prior-external",
        5.0,
        "world:x",
        parent_event_ids=(boundary.event_id,),
    )
    model.register_boundary(boundary)
    ledger.register_external(external)
    resolution = model.observe_external(external)
    if resolution.status != "externally-consistent":
        raise RuntimeError("failed to construct anonymous P4 prior relation")
    return model


def _lineage_proposals(
    expectation: A01LocalTemporalExpectation,
    ledger: ProvenanceLedger,
) -> tuple[EndogenousPulseProposal, EndogenousPulseProposal]:
    source = _pulse("p4-lineage-source", 20.0, "A")
    ledger.register_external(source)
    rows = expectation.proposals_for(source, origin_state_hash="p4-lineage-state")
    by_target = {row.target: row for row in rows}
    if set(by_target) != {"B", "C"} or len(rows) != 2:
        raise RuntimeError("P4 requires exactly the symmetric B/C proposal pair")
    first = by_target["B"]
    second = by_target["C"]
    ledger.register_proposal(first)
    ledger.register_proposal(second)
    return first, second


def _boundaries(
    proposal_a: EndogenousPulseProposal,
    proposal_b: EndogenousPulseProposal,
    *,
    merged_time_ms: float,
) -> tuple[P4ProspectiveFixture, dict[str, BoundaryEvent]]:
    fixture = P4ProspectiveFixture(
        lineage_a_proposal_id=proposal_a.proposal_id,
        lineage_b_proposal_id=proposal_b.proposal_id,
    )
    fixture.validate_matrix()
    boundaries = {
        "separate-a": BoundaryEvent(
            event_id=fixture.separate_a_boundary_id,
            time_ms=30.0,
            port_id="port:p",
            magnitude=1.0,
            polarity=1,
            direction=BoundaryDirection.FIELD_TO_WORLD,
            source_spark_id="spark:p4-separate-a",
            source_unit_id=0,
            source_proposal_ids=(proposal_a.proposal_id,),
            generation_depth=1,
            source_state_hash="p4-lineage-state",
        ),
        "separate-b": BoundaryEvent(
            event_id=fixture.separate_b_boundary_id,
            time_ms=31.0,
            port_id="port:p",
            magnitude=1.0,
            polarity=1,
            direction=BoundaryDirection.FIELD_TO_WORLD,
            source_spark_id="spark:p4-separate-b",
            source_unit_id=0,
            source_proposal_ids=(proposal_b.proposal_id,),
            generation_depth=1,
            source_state_hash="p4-lineage-state",
        ),
        "merged": BoundaryEvent(
            event_id=fixture.merged_boundary_id,
            time_ms=merged_time_ms,
            port_id="port:p",
            magnitude=1.0,
            polarity=1,
            direction=BoundaryDirection.FIELD_TO_WORLD,
            source_spark_id="spark:p4-merged",
            source_unit_id=0,
            source_proposal_ids=(proposal_a.proposal_id, proposal_b.proposal_id),
            generation_depth=1,
            source_state_hash="p4-lineage-state",
        ),
    }
    return fixture, boundaries


def _path_map(
    proposal_a: EndogenousPulseProposal,
    proposal_b: EndogenousPulseProposal,
) -> dict[str, dict[str, str]]:
    return {
        proposal_a.proposal_id: {
            "target": proposal_a.target,
            "path_id": proposal_a.local_path_ids[0],
        },
        proposal_b.proposal_id: {
            "target": proposal_b.target,
            "path_id": proposal_b.local_path_ids[0],
        },
    }


def _changed_paths(
    before: dict[str, float],
    after: dict[str, float],
) -> tuple[str, ...]:
    return tuple(
        path_id
        for path_id in sorted(set(before) | set(after))
        if before.get(path_id) != after.get(path_id)
    )


def _reliabilities(
    expectation: A01LocalTemporalExpectation,
    path_ids: tuple[str, ...],
) -> dict[str, float]:
    return {
        path_id: expectation.causal_reliability(path_id)
        for path_id in path_ids
    }


def _condition_contract(source_sha: str) -> dict[str, Any]:
    expectation = _expectation()
    ledger = ProvenanceLedger()
    _prior_consistency(ledger)
    proposal_a, proposal_b = _lineage_proposals(expectation, ledger)
    fixture, _ = _boundaries(proposal_a, proposal_b, merged_time_ms=80.0)
    conditions = [asdict(row) for row in fixture.conditions]
    return {
        "schema": CONTRACT_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "development_only": True,
        "held_out_execution_allowed": False,
        "formal_execution_allowed": False,
        "same_identity_rerun_allowed": False,
        "fixture": {
            "lineage_a_proposal_id": proposal_a.proposal_id,
            "lineage_b_proposal_id": proposal_b.proposal_id,
            "boundary_ids": {
                "separate_a": fixture.separate_a_boundary_id,
                "separate_b": fixture.separate_b_boundary_id,
                "merged": fixture.merged_boundary_id,
            },
            "path_map": _path_map(proposal_a, proposal_b),
            "conditions": conditions,
        },
        "prospective_execution_ids": {
            condition_id: f"{CANDIDATE_ID}:{condition_id}:once"
            for condition_id in CONDITION_IDS
        },
        "selection_rule": {
            "source": (
                "for requires_later_separation conditions only, derive the selected "
                "lineage from the one expired retained separate BoundaryEvent ID that "
                "the returned external event names in addition to the merged boundary"
            ),
            "forbidden": [
                "semantic outcome labels",
                "evaluator-supplied lineage identity",
                "caller-selected proposal/path singleton",
                "post-outcome tie-break",
            ],
        },
        "classifier": {
            "version": CLASSIFIER_VERSION,
            "supported_requires": [
                "all six prospective conditions execute once under distinct IDs",
                "merged conditions retain two distinct source proposal lineages before evidence",
                "separating evidence names a retained historical separate-boundary parent plus the merged boundary",
                "only the trace-derived selected lineage path changes in both separating conditions",
                "separating confirmation makes the selected lineage target the unique future winner",
                "separating contradiction makes the nonselected lineage target the unique future winner",
                "absence and internal replay produce no causal path update",
            ],
            "en_bloc_requires": [
                "all construction and control validity checks pass",
                "both separating conditions change all merged lineage paths rather than a strict selected subset",
            ],
            "verdict_order": [
                INVALID,
                PREMATURE_COLLAPSE,
                SUPPORTED,
                EN_BLOC,
                NO_EFFECT,
                AMBIGUOUS,
            ],
        },
        "scientific_scope": (
            "fresh exposed-development P4 discriminator after P3; tests selective "
            "resolution of genuinely merged historical lineage and is not formal or held out"
        ),
    }


def _contract(source_sha: str) -> dict[str, Any]:
    value = _condition_contract(source_sha)
    value["contract_sha256"] = canonical_sha256(value)
    return value


def _setup_for_condition(
    condition_id: str,
) -> tuple[
    A01LocalTemporalExpectation,
    ProvenanceLedger,
    UntypedBoundaryConsistency,
    EndogenousPulseProposal,
    EndogenousPulseProposal,
    P4ProspectiveFixture,
    dict[str, BoundaryEvent],
]:
    expectation = _expectation()
    ledger = ProvenanceLedger()
    consistency = _prior_consistency(ledger)
    proposal_a, proposal_b = _lineage_proposals(expectation, ledger)
    merged_time = 80.0 if "separating" in condition_id else 40.0
    fixture, boundaries = _boundaries(
        proposal_a,
        proposal_b,
        merged_time_ms=merged_time,
    )
    return (
        expectation,
        ledger,
        consistency,
        proposal_a,
        proposal_b,
        fixture,
        boundaries,
    )


def _historical_selection(
    external: RuntimePulse,
    boundaries: dict[str, BoundaryEvent],
) -> dict[str, str] | None:
    historical = [
        boundary
        for key, boundary in boundaries.items()
        if key.startswith("separate-")
        and boundary.event_id in external.parent_event_ids
    ]
    if not historical:
        return None
    if len(historical) != 1:
        raise RuntimeError("P4 separating evidence must identify exactly one historical lineage")
    boundary = historical[0]
    if len(boundary.source_proposal_ids) != 1:
        raise RuntimeError("historical separating boundary must have singleton ancestry")
    return {
        "parent_boundary_event_id": boundary.event_id,
        "proposal_id": boundary.source_proposal_ids[0],
    }


def _execute_condition(condition_id: str, execution_id: str) -> dict[str, Any]:
    (
        expectation,
        ledger,
        consistency,
        proposal_a,
        proposal_b,
        fixture,
        boundaries,
    ) = _setup_for_condition(condition_id)
    condition = next(row for row in fixture.conditions if row.condition_id == condition_id)
    path_map = _path_map(proposal_a, proposal_b)
    all_paths = tuple(sorted(row["path_id"] for row in path_map.values()))
    before_reliability = _reliabilities(expectation, all_paths)
    pre_competition = _competition(expectation)

    bridge = A01TransientCreditBridge(expectation, consistency, ledger)
    resolution: dict[str, Any] | None = None
    probe: dict[str, Any] | None = None
    external: RuntimePulse | None = None
    replay: RuntimePulse | None = None
    expired_history: tuple[str, ...] = ()
    active_boundary: BoundaryEvent

    if condition_id == "p4-separate-confirmation":
        active_boundary = boundaries["separate-a"]
        consistency.register_boundary(active_boundary)
        external = _pulse(
            "p4-external-separate-confirmation",
            45.0,
            "world:x",
            parent_event_ids=(active_boundary.event_id,),
        )
        ledger.register_external(external)
        resolution = bridge.observe_external(active_boundary, external).state_dict()
    elif condition_id == "p4-merged-confirmation":
        active_boundary = boundaries["merged"]
        consistency.register_boundary(active_boundary)
        external = _pulse(
            "p4-external-merged-confirmation",
            45.0,
            "world:x",
            parent_event_ids=(active_boundary.event_id,),
        )
        ledger.register_external(external)
        probe_row = probe_merged_lineage_credit(
            bridge,
            boundary=active_boundary,
            external=external,
        )
        probe = probe_row.state_dict()
        resolution = bridge.resolutions[-1].state_dict()
    elif condition_id in {
        "p4-merged-separating-confirmation",
        "p4-merged-separating-contradiction",
    }:
        history_key = (
            "separate-a"
            if condition_id.endswith("confirmation")
            else "separate-b"
        )
        historical_boundary = boundaries[history_key]
        consistency.register_boundary(historical_boundary)
        expired_history = consistency.expire(71.0)
        if expired_history != (historical_boundary.event_id,):
            raise RuntimeError("P4 historical lineage boundary did not expire exactly once")
        active_boundary = boundaries["merged"]
        consistency.register_boundary(active_boundary)
        is_confirmation = condition_id.endswith("confirmation")
        external = _pulse(
            f"p4-external-{condition_id}",
            85.0,
            "world:x" if is_confirmation else "world:y",
            parent_event_ids=(active_boundary.event_id, historical_boundary.event_id),
        )
        ledger.register_external(external)
        probe_row = probe_merged_lineage_credit(
            bridge,
            boundary=active_boundary,
            external=external,
        )
        probe = probe_row.state_dict()
        resolution = bridge.resolutions[-1].state_dict()
    elif condition_id == "p4-merged-absence":
        active_boundary = boundaries["merged"]
        consistency.register_boundary(active_boundary)
        consistency.expire(100.0)
    elif condition_id == "p4-merged-replay":
        active_boundary = boundaries["merged"]
        consistency.register_boundary(active_boundary)
        replay = _pulse(
            "p4-internal-replay",
            45.0,
            "world:x",
            origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
            parent_event_ids=(active_boundary.event_id,),
        )
        ledger.register_event(replay)
        consistency.expire(100.0)
    else:
        raise ValueError(f"unknown P4 condition: {condition_id}")

    after_reliability = _reliabilities(expectation, all_paths)
    post_competition = _competition(expectation)
    changed = _changed_paths(before_reliability, after_reliability)
    selected = _historical_selection(external, boundaries) if external else None
    if selected is not None:
        selected["path_id"] = path_map[selected["proposal_id"]]["path_id"]
        selected["target"] = path_map[selected["proposal_id"]]["target"]

    merged_ids = tuple(boundaries["merged"].source_proposal_ids)
    return {
        "condition_id": condition_id,
        "prospective_execution_id": execution_id,
        "condition_spec": asdict(condition),
        "proposal_rows": [asdict(proposal_a), asdict(proposal_b)],
        "path_map": path_map,
        "retained_boundary_events": [
            boundaries["separate-a"].state_dict(),
            boundaries["separate-b"].state_dict(),
            boundaries["merged"].state_dict(),
        ],
        "active_boundary_event_id": active_boundary.event_id,
        "merged_source_proposal_ids": list(merged_ids),
        "expired_historical_boundary_ids": list(expired_history),
        "external_evidence": external.as_dict() if external else None,
        "internal_replay": replay.as_dict() if replay else None,
        "trace_derived_selected_lineage": selected,
        "credit_resolution": resolution,
        "merged_credit_probe": probe,
        "pre": {
            "path_reliability": before_reliability,
            "competition": pre_competition,
        },
        "post": {
            "path_reliability": after_reliability,
            "competition": post_competition,
        },
        "changed_path_ids": list(changed),
        "consistency_state": consistency.state_dict(),
        "ledger_state": ledger.state_dict(),
    }


def _acquire(source_sha: str) -> dict[str, Any]:
    contract = _contract(source_sha)
    observations = [
        _execute_condition(
            condition_id,
            str(contract["prospective_execution_ids"][condition_id]),
        )
        for condition_id in CONDITION_IDS
    ]
    return {
        "schema": RAW_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "contract_sha256": contract["contract_sha256"],
        "contract": contract,
        "observations": observations,
    }


def _validate_common(
    contract: dict[str, Any],
    observations: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    reasons: list[str] = []
    if len(observations) != len(CONDITION_IDS):
        reasons.append("condition-count-mismatch")
    by_id = {str(row.get("condition_id")): row for row in observations}
    if set(by_id) != set(CONDITION_IDS):
        reasons.append("condition-id-mismatch")
    execution_ids = [row.get("prospective_execution_id") for row in observations]
    if len(execution_ids) != len(set(execution_ids)):
        reasons.append("execution-id-reuse")
    expected_ids = contract["prospective_execution_ids"]
    fixture = contract["fixture"]
    expected_path_map = fixture["path_map"]
    expected_proposals = set(expected_path_map)
    expected_merged = {
        fixture["lineage_a_proposal_id"],
        fixture["lineage_b_proposal_id"],
    }
    for condition_id, row in by_id.items():
        if row.get("prospective_execution_id") != expected_ids.get(condition_id):
            reasons.append(f"{condition_id}:execution-id-binding")
        if row.get("path_map") != expected_path_map:
            reasons.append(f"{condition_id}:path-map-binding")
        proposal_rows = row.get("proposal_rows", [])
        if {
            str(proposal.get("proposal_id"))
            for proposal in proposal_rows
            if isinstance(proposal, dict)
        } != expected_proposals:
            reasons.append(f"{condition_id}:proposal-binding")
        merged = tuple(row.get("merged_source_proposal_ids", ()))
        spec = row.get("condition_spec", {})
        if spec.get("boundary_mode") == "merged" and len(set(merged)) < 2:
            reasons.append(f"{condition_id}:premature-singleton")
        if spec.get("boundary_mode") == "merged" and set(merged) != expected_merged:
            reasons.append(f"{condition_id}:merged-ancestry-binding")
    return by_id, reasons


def _derive_selected_lineage_from_raw(
    contract: dict[str, Any],
    row: dict[str, Any],
) -> dict[str, str] | None:
    spec = row.get("condition_spec", {})
    if not spec.get("requires_later_separation"):
        return None
    external = row.get("external_evidence")
    if not isinstance(external, dict):
        return None
    parents = set(external.get("parent_event_ids", []))
    merged_id = contract["fixture"]["boundary_ids"]["merged"]
    if merged_id not in parents:
        return None
    historical = []
    for boundary in row.get("retained_boundary_events", []):
        if not isinstance(boundary, dict):
            continue
        source_ids = boundary.get("source_proposal_ids", [])
        if (
            boundary.get("event_id") in parents
            and boundary.get("event_id") != merged_id
            and isinstance(source_ids, list)
            and len(source_ids) == 1
        ):
            historical.append(boundary)
    if len(historical) != 1:
        return None
    proposal_id = str(historical[0]["source_proposal_ids"][0])
    path_row = contract["fixture"]["path_map"].get(proposal_id)
    if not isinstance(path_row, dict):
        return None
    return {
        "parent_boundary_event_id": str(historical[0]["event_id"]),
        "proposal_id": proposal_id,
        "path_id": str(path_row["path_id"]),
        "target": str(path_row["target"]),
    }


def _classify(
    contract: dict[str, Any],
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    by_id, reasons = _validate_common(contract, observations)
    if reasons:
        verdict = (
            PREMATURE_COLLAPSE
            if any("premature-singleton" in row for row in reasons)
            else INVALID
        )
        return {"verdict": verdict, "reasons": reasons}

    fixture_map = contract["fixture"]["path_map"]
    all_paths = {
        str(row["path_id"])
        for row in fixture_map.values()
    }

    separate = by_id["p4-separate-confirmation"]
    if (
        separate.get("credit_resolution", {}).get("status")
        != A01CausalCreditStatus.EXACT_MATCH.value
        or len(separate.get("changed_path_ids", [])) != 1
    ):
        reasons.append("separate-calibration-failed")

    merged_confirmation = by_id["p4-merged-confirmation"]
    if (
        merged_confirmation.get("credit_resolution", {}).get("status")
        != A01CausalCreditStatus.EXACT_MATCH.value
        or set(merged_confirmation.get("changed_path_ids", [])) != all_paths
    ):
        reasons.append("merged-calibration-failed")

    for control_id in ("p4-merged-absence", "p4-merged-replay"):
        row = by_id[control_id]
        if row.get("changed_path_ids"):
            reasons.append(f"{control_id}:causal-credit-drift")
        if row.get("credit_resolution") is not None:
            reasons.append(f"{control_id}:unexpected-external-credit")

    sep_rows = [
        by_id["p4-merged-separating-confirmation"],
        by_id["p4-merged-separating-contradiction"],
    ]
    selective_ok: list[bool] = []
    en_bloc_rows: list[bool] = []
    no_effect_rows: list[bool] = []
    for row in sep_rows:
        condition_id = str(row["condition_id"])
        selected = row.get("trace_derived_selected_lineage")
        derived = _derive_selected_lineage_from_raw(contract, row)
        if not isinstance(selected, dict) or selected != derived:
            reasons.append(f"{condition_id}:trace-selection-binding")
            selective_ok.append(False)
            en_bloc_rows.append(False)
            no_effect_rows.append(False)
            continue
        selected_path = str(selected.get("path_id"))
        if selected_path not in all_paths:
            reasons.append(f"{condition_id}:selected-path-not-merged")
        changed = set(row.get("changed_path_ids", []))
        selected_only = changed == {selected_path}
        en_bloc = changed == all_paths
        no_effect = not changed
        competition = row.get("post", {}).get("competition", {})
        selected_target = str(selected.get("target"))
        other_targets = {
            str(value["target"])
            for proposal_id, value in fixture_map.items()
            if proposal_id != selected.get("proposal_id")
        }
        expected_status = (
            A01CausalCreditStatus.EXACT_MATCH.value
            if condition_id.endswith("confirmation")
            else A01CausalCreditStatus.EXACT_CONTRADICTION.value
        )
        if len(other_targets) != 1:
            reasons.append(f"{condition_id}:nonselected-target-arity")
            winner_ok = False
        elif condition_id.endswith("confirmation"):
            winner_ok = competition.get("winner") == selected_target
        else:
            winner_ok = competition.get("winner") == next(iter(other_targets))
        status_ok = row.get("credit_resolution", {}).get("status") == expected_status
        selective_ok.append(selected_only and winner_ok and status_ok)
        en_bloc_rows.append(en_bloc and status_ok)
        no_effect_rows.append(no_effect)

    if reasons:
        return {"verdict": INVALID, "reasons": reasons}
    if all(selective_ok):
        return {
            "verdict": SUPPORTED,
            "reasons": [
                "both separating conditions changed only the trace-derived selected lineage",
                "future competition moved in the prospectively required direction",
                "absence/replay controls stayed credit-neutral",
            ],
        }
    if all(en_bloc_rows):
        return {
            "verdict": EN_BLOC,
            "reasons": [
                "valid plural merged ancestry was retained",
                "lineage-separating external evidence changed every merged causal path in both assays",
                "current bridge therefore did not selectively resolve the trace-derived causal lineage",
            ],
        }
    if all(no_effect_rows):
        return {
            "verdict": NO_EFFECT,
            "reasons": ["valid separating evidence produced no causal path update"],
        }
    return {
        "verdict": AMBIGUOUS,
        "reasons": [
            "valid controls passed but separating conditions did not form a uniform selective, en-bloc, or null pattern"
        ],
    }


def _score(source_sha: str, raw: dict[str, Any]) -> dict[str, Any]:
    expected_contract = _contract(source_sha)
    if raw.get("schema") != RAW_SCHEMA or raw.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("raw envelope identity/schema mismatch")
    if raw.get("source_sha") != source_sha:
        raise ValueError("raw source SHA mismatch")
    if raw.get("contract") != expected_contract:
        raise ValueError("raw P4 contract differs from frozen scorer contract")
    if raw.get("contract_sha256") != expected_contract["contract_sha256"]:
        raise ValueError("raw P4 contract digest mismatch")
    observations = raw.get("observations")
    if not isinstance(observations, list):
        raise ValueError("raw P4 observations must be a list")
    classification = _classify(expected_contract, observations)
    return {
        "schema": SCORE_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "contract_sha256": expected_contract["contract_sha256"],
        "classifier_version": CLASSIFIER_VERSION,
        "development_only": True,
        "held_out_executed": False,
        "formal_execution": False,
        "same_identity_rerun_allowed": False,
        "classification": classification,
        "observation_summary": [
            {
                "condition_id": row["condition_id"],
                "changed_path_ids": row["changed_path_ids"],
                "trace_derived_selected_lineage": row[
                    "trace_derived_selected_lineage"
                ],
                "credit_status": (
                    row["credit_resolution"]["status"]
                    if row["credit_resolution"] is not None
                    else None
                ),
                "future_winner": row["post"]["competition"]["winner"],
                "future_tied_winners": row["post"]["competition"]["tied_winners"],
            }
            for row in observations
        ],
    }


def _manifest(source_sha: str) -> dict[str, Any]:
    contract = _contract(source_sha)
    return {
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "contract_sha256": contract["contract_sha256"],
        "contract": contract,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    for mode in ("manifest", "acquire"):
        child = subparsers.add_parser(mode)
        child.add_argument("--source-sha", required=True)
        child.add_argument("--output", required=True)
    score = subparsers.add_parser("score")
    score.add_argument("--source-sha", required=True)
    score.add_argument("--raw-input", required=True)
    score.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    source_sha = str(args.source_sha)
    if args.mode == "manifest":
        value = _manifest(source_sha)
    elif args.mode == "acquire":
        value = _acquire(source_sha)
    elif args.mode == "score":
        raw = json.loads(Path(args.raw_input).read_text())
        value = _score(source_sha, raw)
    else:  # pragma: no cover
        raise RuntimeError(f"unexpected mode: {args.mode}")
    _write_json(Path(args.output), value)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prospective P4 runner with retained-trace and lineage counterbalancing.

This file supersedes the first candidate-001 runner before STARTED. It fixes
three pre-execution integrity defects without adding any mechanism that could
make the scientific candidate pass:

1. historical BoundaryEvents expire strictly after their configured TTL;
2. merged ancestry and lineage continuation are bound through
   ``P4RetainedTraceInput`` to the actual runtime events/state captured here;
3. separating confirmation/contradiction are crossed with both lineage IDs.

Acquisition records raw observations only. Classification remains a separate
post-preservation step in the execute-once workflow.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import run_v061_a01_md002_p4_candidate_001 as legacy

from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v061_a01.credit_bridge import A01CausalCreditStatus
from sparkbrain.v061_a01.md002_p4_credit_probe import probe_merged_lineage_credit
from sparkbrain.v061_a01.md002_p4_trace_binding import P4RetainedTraceInput
from sparkbrain.v061_a01.md002_protocol import canonical_sha256

CANDIDATE_ID = legacy.CANDIDATE_ID
CONTRACT_SCHEMA = "v061-a01-md002-p4-selective-resolution-candidate-v2"
RAW_SCHEMA = "v061-a01-md002-p4-selective-resolution-raw-v2"
SCORE_SCHEMA = "v061-a01-md002-p4-selective-resolution-score-v2"
CLASSIFIER_VERSION = "p4-selective-resolution-development-classifier-v2"

SUPPORTED = legacy.SUPPORTED
EN_BLOC = legacy.EN_BLOC
NO_EFFECT = legacy.NO_EFFECT
PREMATURE_COLLAPSE = legacy.PREMATURE_COLLAPSE
AMBIGUOUS = legacy.AMBIGUOUS
INVALID = legacy.INVALID

EXECUTION_SPECS: tuple[dict[str, str | None], ...] = (
    {
        "execution_id": "p4-separate-confirmation",
        "base_condition_id": "p4-separate-confirmation",
        "selected_lineage_arm": None,
        "evidence_sign": "confirmation",
    },
    {
        "execution_id": "p4-merged-confirmation",
        "base_condition_id": "p4-merged-confirmation",
        "selected_lineage_arm": None,
        "evidence_sign": "confirmation",
    },
    {
        "execution_id": "p4-merged-separating-confirmation-a",
        "base_condition_id": "p4-merged-separating-confirmation",
        "selected_lineage_arm": "a",
        "evidence_sign": "confirmation",
    },
    {
        "execution_id": "p4-merged-separating-confirmation-b",
        "base_condition_id": "p4-merged-separating-confirmation",
        "selected_lineage_arm": "b",
        "evidence_sign": "confirmation",
    },
    {
        "execution_id": "p4-merged-separating-contradiction-a",
        "base_condition_id": "p4-merged-separating-contradiction",
        "selected_lineage_arm": "a",
        "evidence_sign": "contradiction",
    },
    {
        "execution_id": "p4-merged-separating-contradiction-b",
        "base_condition_id": "p4-merged-separating-contradiction",
        "selected_lineage_arm": "b",
        "evidence_sign": "contradiction",
    },
    {
        "execution_id": "p4-merged-absence",
        "base_condition_id": "p4-merged-absence",
        "selected_lineage_arm": None,
        "evidence_sign": "absence",
    },
    {
        "execution_id": "p4-merged-replay",
        "base_condition_id": "p4-merged-replay",
        "selected_lineage_arm": None,
        "evidence_sign": "replay",
    },
)
EXECUTION_IDS = tuple(str(row["execution_id"]) for row in EXECUTION_SPECS)


def _write_json(path: Path, value: Any) -> None:
    legacy._write_json(path, value)


def _active_lineages_from_runtime(
    ledger: ProvenanceLedger,
    *,
    at_ms: float,
) -> tuple[str, ...]:
    """Measure proposal lineages active under their runtime validity interval."""

    active = []
    for proposal_id, proposal in sorted(ledger.proposals.items()):
        if proposal.created_at_ms <= at_ms <= proposal.valid_until_ms:
            active.append(proposal_id)
    return tuple(active)


def _boundary_from_state(row: dict[str, Any]) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=str(row["event_id"]),
        time_ms=float(row["time_ms"]),
        port_id=str(row["port_id"]),
        magnitude=float(row["magnitude"]),
        polarity=int(row["polarity"]),
        direction=BoundaryDirection(str(row["direction"])),
        source_spark_id=str(row["source_spark_id"]),
        source_unit_id=int(row["source_unit_id"]),
        source_proposal_ids=tuple(str(value) for value in row["source_proposal_ids"]),
        generation_depth=int(row["generation_depth"]),
        source_state_hash=str(row["source_state_hash"]),
    )


def _observation_state(observation: Any) -> dict[str, Any]:
    return {
        "boundary_source_proposal_ids": list(
            observation.boundary_source_proposal_ids
        ),
        "active_lineages_before": list(observation.active_lineages_before),
        "active_lineages_after": list(observation.active_lineages_after),
        "runtime_trace": list(observation.runtime_trace),
        "runtime_trace_sha256": observation.runtime_trace_sha256,
        "measurement_record_sha256": observation.measurement_record_sha256,
    }


def _retained_trace(
    *,
    boundary_events: tuple[BoundaryEvent, ...],
    ledger: ProvenanceLedger,
    merged_boundary: BoundaryEvent,
    before_time_ms: float,
    after_time_ms: float,
    expired_boundary_ids: tuple[str, ...],
) -> tuple[tuple[dict[str, Any], ...], dict[str, Any]]:
    """Capture and validate actual boundary/runtime lineage state for P4."""

    before = _active_lineages_from_runtime(ledger, at_ms=before_time_ms)
    after = _active_lineages_from_runtime(ledger, at_ms=after_time_ms)
    payload = {
        "boundary_source_proposal_ids": tuple(
            merged_boundary.source_proposal_ids
        ),
        "active_lineages_before": before,
        "active_lineages_after": after,
    }
    rows: list[dict[str, Any]] = [
        {"type": "md002-p4-boundary-event", "event": event.state_dict()}
        for event in boundary_events
    ]
    rows.extend(
        {
            "type": "md002-p4-expired-boundary",
            "event_id": event_id,
        }
        for event_id in expired_boundary_ids
    )
    rows.extend(
        (
            {
                "type": "md002-p4-active-lineages",
                "phase": "before",
                "proposal_ids": list(before),
                "measurement_time_ms": before_time_ms,
                "derivation": "ledger-proposal-temporal-validity-v1",
            },
            {
                "type": "md002-p4-active-lineages",
                "phase": "after",
                "proposal_ids": list(after),
                "measurement_time_ms": after_time_ms,
                "derivation": "ledger-proposal-temporal-validity-v1",
            },
            {
                "type": "md002-merged-ancestry-measurement",
                "measurement": payload,
            },
        )
    )
    trace = tuple(rows)
    retained = P4RetainedTraceInput(
        boundary_events=boundary_events,
        runtime_trace=trace,
        runtime_trace_sha256=canonical_sha256(trace),
    )
    observation = retained.observation()
    return trace, _observation_state(observation)


def _contract(source_sha: str) -> dict[str, Any]:
    expectation = legacy._expectation()
    ledger = ProvenanceLedger()
    legacy._prior_consistency(ledger)
    proposal_a, proposal_b = legacy._lineage_proposals(expectation, ledger)
    fixture, _ = legacy._boundaries(
        proposal_a,
        proposal_b,
        merged_time_ms=80.0,
    )
    fixture.validate_matrix()
    path_map = legacy._path_map(proposal_a, proposal_b)
    value: dict[str, Any] = {
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
            "path_map": path_map,
            "base_conditions": [asdict(row) for row in fixture.conditions],
        },
        "prospective_execution_ids": {
            execution_id: f"{CANDIDATE_ID}:{execution_id}:once"
            for execution_id in EXECUTION_IDS
        },
        "execution_matrix": [dict(row) for row in EXECUTION_SPECS],
        "retained_trace_binding": {
            "boundary_source": (
                "all BoundaryEvents actually registered for the execution are "
                "retained as md002-p4-boundary-event rows"
            ),
            "active_lineage_source": (
                "all proposals in the shared ProvenanceLedger whose runtime "
                "created_at_ms <= measurement_time_ms <= valid_until_ms"
            ),
            "digest": "canonical_sha256 over the complete retained runtime trace",
            "selection": (
                "separating selection is derived only from an expired retained "
                "singleton BoundaryEvent that is also an exact external parent"
            ),
        },
        "ttl_rule": (
            "historical selection BoundaryEvents must be expired at a time "
            "strictly greater than event.time_ms + pending_ttl_ms"
        ),
        "lineage_counterbalance": {
            "separating_cross": [
                {"evidence_sign": sign, "selected_lineage_arm": arm}
                for sign in ("confirmation", "contradiction")
                for arm in ("a", "b")
            ],
            "purpose": (
                "a fixed lineage-ID preference cannot satisfy the selective "
                "resolution classifier"
            ),
        },
        "forbidden": [
            "semantic outcome labels",
            "evaluator-supplied lineage identity",
            "caller-selected proposal/path singleton",
            "post-outcome tie-break",
            "post-outcome threshold or scorer changes",
        ],
        "classifier": {
            "version": CLASSIFIER_VERSION,
            "supported_requires": [
                "all eight prospective executions occur once under distinct IDs",
                "every merged assay has trace-bound plural ancestry",
                "all four sign-by-lineage separating assays change only the "
                "trace-derived selected lineage path",
                "confirmation makes the selected lineage target the unique winner",
                "contradiction makes the nonselected lineage target the unique winner",
                "absence and internal replay remain credit-neutral",
            ],
            "en_bloc_requires": [
                "all validity and control checks pass",
                "all four separating assays change every merged lineage path",
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
            "fresh exposed-development P4 discriminator after P3; tests "
            "selective resolution of genuinely merged historical lineage"
        ),
    }
    value["contract_sha256"] = canonical_sha256(value)
    return value


def _spec(execution_id: str) -> dict[str, str | None]:
    for row in EXECUTION_SPECS:
        if row["execution_id"] == execution_id:
            return row
    raise ValueError(f"unknown P4 execution: {execution_id}")


def _historical_selection(
    *,
    external: RuntimePulse | None,
    trace: tuple[dict[str, Any], ...],
    merged_boundary_id: str,
    path_map: dict[str, dict[str, str]],
) -> dict[str, str] | None:
    if external is None:
        return None
    parents = set(external.parent_event_ids)
    if merged_boundary_id not in parents:
        return None
    expired = {
        str(row["event_id"])
        for row in trace
        if row.get("type") == "md002-p4-expired-boundary"
    }
    candidates: list[dict[str, Any]] = []
    for row in trace:
        if row.get("type") != "md002-p4-boundary-event":
            continue
        event = row.get("event")
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("event_id"))
        source_ids = event.get("source_proposal_ids")
        if (
            event_id in parents
            and event_id in expired
            and event_id != merged_boundary_id
            and isinstance(source_ids, (list, tuple))
            and len(source_ids) == 1
        ):
            candidates.append(event)
    if not candidates:
        return None
    if len(candidates) != 1:
        raise RuntimeError(
            "P4 retained trace must identify exactly one expired historical parent"
        )
    proposal_id = str(candidates[0]["source_proposal_ids"][0])
    mapped = path_map.get(proposal_id)
    if mapped is None:
        raise RuntimeError("trace-selected proposal is not in the frozen path map")
    return {
        "parent_boundary_event_id": str(candidates[0]["event_id"]),
        "proposal_id": proposal_id,
        "path_id": str(mapped["path_id"]),
        "target": str(mapped["target"]),
    }


def _execute(execution_id: str, prospective_id: str) -> dict[str, Any]:
    spec = _spec(execution_id)
    base_condition_id = str(spec["base_condition_id"])
    (
        expectation,
        ledger,
        consistency,
        proposal_a,
        proposal_b,
        fixture,
        boundaries,
    ) = legacy._setup_for_condition(base_condition_id)
    base_condition = next(
        row
        for row in fixture.conditions
        if row.condition_id == base_condition_id
    )
    path_map = legacy._path_map(proposal_a, proposal_b)
    all_paths = tuple(sorted(row["path_id"] for row in path_map.values()))
    before_reliability = legacy._reliabilities(expectation, all_paths)
    pre_competition = legacy._competition(expectation)

    bridge = legacy.A01TransientCreditBridge(expectation, consistency, ledger)
    resolution: dict[str, Any] | None = None
    probe: dict[str, Any] | None = None
    external: RuntimePulse | None = None
    replay: RuntimePulse | None = None
    expired_history: tuple[str, ...] = ()
    trace_events: tuple[BoundaryEvent, ...]
    merged_observation: dict[str, Any] | None = None
    active_boundary: BoundaryEvent

    if base_condition_id == "p4-separate-confirmation":
        active_boundary = boundaries["separate-a"]
        trace_events = (active_boundary,)
        consistency.register_boundary(active_boundary)
        external = legacy._pulse(
            "p4-external-separate-confirmation",
            45.0,
            "world:x",
            parent_event_ids=(active_boundary.event_id,),
        )
        ledger.register_external(external)
        resolution = bridge.observe_external(active_boundary, external).state_dict()
        trace: tuple[dict[str, Any], ...] = tuple(
            {
                "type": "md002-p4-boundary-event",
                "event": event.state_dict(),
            }
            for event in trace_events
        )
    elif base_condition_id == "p4-merged-confirmation":
        active_boundary = boundaries["merged"]
        trace_events = (active_boundary,)
        consistency.register_boundary(active_boundary)
        before_time = active_boundary.time_ms
        external = legacy._pulse(
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
        trace, merged_observation = _retained_trace(
            boundary_events=trace_events,
            ledger=ledger,
            merged_boundary=active_boundary,
            before_time_ms=before_time,
            after_time_ms=external.time_ms,
            expired_boundary_ids=(),
        )
    elif base_condition_id in {
        "p4-merged-separating-confirmation",
        "p4-merged-separating-contradiction",
    }:
        selected_arm = str(spec["selected_lineage_arm"])
        historical_boundary = boundaries[f"separate-{selected_arm}"]
        consistency.register_boundary(historical_boundary)
        valid_until = (
            historical_boundary.time_ms + consistency.config.pending_ttl_ms
        )
        expired_history = consistency.expire(valid_until + 1.0)
        if expired_history != (historical_boundary.event_id,):
            raise RuntimeError(
                "P4 historical lineage boundary did not expire exactly once"
            )
        active_boundary = boundaries["merged"]
        trace_events = (historical_boundary, active_boundary)
        consistency.register_boundary(active_boundary)
        before_time = active_boundary.time_ms
        evidence_sign = str(spec["evidence_sign"])
        target = "world:x" if evidence_sign == "confirmation" else "world:y"
        external = legacy._pulse(
            f"p4-external-{execution_id}",
            85.0,
            target,
            parent_event_ids=(
                active_boundary.event_id,
                historical_boundary.event_id,
            ),
        )
        ledger.register_external(external)
        probe_row = probe_merged_lineage_credit(
            bridge,
            boundary=active_boundary,
            external=external,
        )
        probe = probe_row.state_dict()
        resolution = bridge.resolutions[-1].state_dict()
        trace, merged_observation = _retained_trace(
            boundary_events=trace_events,
            ledger=ledger,
            merged_boundary=active_boundary,
            before_time_ms=before_time,
            after_time_ms=external.time_ms,
            expired_boundary_ids=expired_history,
        )
    elif base_condition_id == "p4-merged-absence":
        active_boundary = boundaries["merged"]
        trace_events = (active_boundary,)
        consistency.register_boundary(active_boundary)
        before_time = active_boundary.time_ms
        consistency.expire(100.0)
        trace, merged_observation = _retained_trace(
            boundary_events=trace_events,
            ledger=ledger,
            merged_boundary=active_boundary,
            before_time_ms=before_time,
            after_time_ms=100.0,
            expired_boundary_ids=(active_boundary.event_id,),
        )
    elif base_condition_id == "p4-merged-replay":
        active_boundary = boundaries["merged"]
        trace_events = (active_boundary,)
        consistency.register_boundary(active_boundary)
        before_time = active_boundary.time_ms
        replay = legacy._pulse(
            "p4-internal-replay",
            45.0,
            "world:x",
            origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
            parent_event_ids=(active_boundary.event_id,),
        )
        ledger.register_event(replay)
        consistency.expire(100.0)
        trace, merged_observation = _retained_trace(
            boundary_events=trace_events,
            ledger=ledger,
            merged_boundary=active_boundary,
            before_time_ms=before_time,
            after_time_ms=100.0,
            expired_boundary_ids=(active_boundary.event_id,),
        )
    else:  # pragma: no cover
        raise ValueError(f"unknown P4 base condition: {base_condition_id}")

    after_reliability = legacy._reliabilities(expectation, all_paths)
    post_competition = legacy._competition(expectation)
    changed = legacy._changed_paths(before_reliability, after_reliability)
    selected = _historical_selection(
        external=external,
        trace=trace,
        merged_boundary_id=boundaries["merged"].event_id,
        path_map=path_map,
    )
    merged_ids = tuple(boundaries["merged"].source_proposal_ids)
    condition_spec = asdict(base_condition)
    condition_spec["base_condition_id"] = base_condition_id
    condition_spec["selected_lineage_arm"] = spec["selected_lineage_arm"]
    condition_spec["evidence_sign"] = spec["evidence_sign"]

    return {
        "condition_id": execution_id,
        "prospective_execution_id": prospective_id,
        "condition_spec": condition_spec,
        "proposal_rows": [asdict(proposal_a), asdict(proposal_b)],
        "path_map": path_map,
        "retained_boundary_events": [event.state_dict() for event in trace_events],
        "retained_runtime_trace": list(trace),
        "retained_runtime_trace_sha256": canonical_sha256(trace),
        "merged_ancestry_observation": merged_observation,
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
        _execute(
            execution_id,
            str(contract["prospective_execution_ids"][execution_id]),
        )
        for execution_id in EXECUTION_IDS
    ]
    return {
        "schema": RAW_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "contract_sha256": contract["contract_sha256"],
        "contract": contract,
        "observations": observations,
    }


def _validate_trace_binding(row: dict[str, Any]) -> str | None:
    trace_value = row.get("retained_runtime_trace")
    events_value = row.get("retained_boundary_events")
    digest_value = row.get("retained_runtime_trace_sha256")
    observation_value = row.get("merged_ancestry_observation")
    if not isinstance(trace_value, list) or not isinstance(events_value, list):
        return "missing-retained-runtime-trace"
    if not isinstance(digest_value, str):
        return "missing-retained-runtime-trace-digest"
    try:
        events = tuple(_boundary_from_state(dict(value)) for value in events_value)
        trace = tuple(dict(value) for value in trace_value)
        retained = P4RetainedTraceInput(
            boundary_events=events,
            runtime_trace=trace,
            runtime_trace_sha256=digest_value,
        )
        expected = _observation_state(retained.observation())
    except (KeyError, TypeError, ValueError) as error:
        return f"retained-trace-invalid:{type(error).__name__}"
    if observation_value != expected:
        return "retained-trace-observation-binding"
    return None


def _selected_from_raw(
    contract: dict[str, Any],
    row: dict[str, Any],
) -> dict[str, str] | None:
    spec = row.get("condition_spec", {})
    if not spec.get("requires_later_separation"):
        return None
    external_value = row.get("external_evidence")
    trace_value = row.get("retained_runtime_trace")
    if not isinstance(external_value, dict) or not isinstance(trace_value, list):
        return None
    external = RuntimePulse(
        event_id=str(external_value["event_id"]),
        time_ms=float(external_value["time_ms"]),
        target=str(external_value["target"]),
        magnitude=float(external_value["magnitude"]),
        polarity=int(external_value["polarity"]),
        origin=EventOrigin(str(external_value["origin"])),
        generation_depth=int(external_value.get("generation_depth", 0)),
        parent_event_ids=tuple(
            str(value) for value in external_value.get("parent_event_ids", [])
        ),
        source_path_ids=tuple(
            str(value) for value in external_value.get("source_path_ids", [])
        ),
        metadata=dict(external_value.get("metadata", {})),
    )
    return _historical_selection(
        external=external,
        trace=tuple(dict(value) for value in trace_value),
        merged_boundary_id=str(contract["fixture"]["boundary_ids"]["merged"]),
        path_map=dict(contract["fixture"]["path_map"]),
    )


def _validate_common(
    contract: dict[str, Any],
    observations: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    reasons: list[str] = []
    if len(observations) != len(EXECUTION_IDS):
        reasons.append("condition-count-mismatch")
    by_id = {str(row.get("condition_id")): row for row in observations}
    if set(by_id) != set(EXECUTION_IDS):
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
        observed_proposals = {
            str(proposal.get("proposal_id"))
            for proposal in proposal_rows
            if isinstance(proposal, dict)
        }
        if observed_proposals != expected_proposals:
            reasons.append(f"{condition_id}:proposal-binding")
        spec = row.get("condition_spec", {})
        if spec.get("boundary_mode") != "merged":
            continue
        merged = tuple(row.get("merged_source_proposal_ids", ()))
        if len(set(merged)) < 2:
            reasons.append(f"{condition_id}:premature-singleton")
        if set(merged) != expected_merged:
            reasons.append(f"{condition_id}:merged-ancestry-binding")
        trace_error = _validate_trace_binding(row)
        if trace_error is not None:
            reasons.append(f"{condition_id}:{trace_error}")
        observation = row.get("merged_ancestry_observation")
        if isinstance(observation, dict):
            before = observation.get("active_lineages_before", [])
            if len(set(before)) < 2:
                reasons.append(f"{condition_id}:premature-singleton")
    return by_id, reasons


def _classify(
    contract: dict[str, Any],
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    by_id, reasons = _validate_common(contract, observations)
    if reasons:
        verdict = (
            PREMATURE_COLLAPSE
            if any("premature-singleton" in reason for reason in reasons)
            else INVALID
        )
        return {"verdict": verdict, "reasons": reasons}

    fixture_map = contract["fixture"]["path_map"]
    all_paths = {str(row["path_id"]) for row in fixture_map.values()}
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

    separating_ids = tuple(
        execution_id
        for execution_id in EXECUTION_IDS
        if "p4-merged-separating-" in execution_id
    )
    selective_ok: list[bool] = []
    en_bloc_rows: list[bool] = []
    no_effect_rows: list[bool] = []
    selected_proposals_by_sign: dict[str, set[str]] = {
        "confirmation": set(),
        "contradiction": set(),
    }
    for condition_id in separating_ids:
        row = by_id[condition_id]
        selected = row.get("trace_derived_selected_lineage")
        derived = _selected_from_raw(contract, row)
        if not isinstance(selected, dict) or selected != derived:
            reasons.append(f"{condition_id}:trace-selection-binding")
            selective_ok.append(False)
            en_bloc_rows.append(False)
            no_effect_rows.append(False)
            continue
        selected_path = str(selected.get("path_id"))
        selected_proposal = str(selected.get("proposal_id"))
        if selected_path not in all_paths:
            reasons.append(f"{condition_id}:selected-path-not-merged")
        evidence_sign = str(row["condition_spec"]["evidence_sign"])
        selected_proposals_by_sign[evidence_sign].add(selected_proposal)
        changed = set(row.get("changed_path_ids", []))
        selected_only = changed == {selected_path}
        en_bloc = changed == all_paths
        no_effect = not changed
        competition = row.get("post", {}).get("competition", {})
        selected_target = str(selected.get("target"))
        other_targets = {
            str(value["target"])
            for proposal_id, value in fixture_map.items()
            if proposal_id != selected_proposal
        }
        expected_status = (
            A01CausalCreditStatus.EXACT_MATCH.value
            if evidence_sign == "confirmation"
            else A01CausalCreditStatus.EXACT_CONTRADICTION.value
        )
        if len(other_targets) != 1:
            reasons.append(f"{condition_id}:nonselected-target-arity")
            winner_ok = False
        elif evidence_sign == "confirmation":
            winner_ok = competition.get("winner") == selected_target
        else:
            winner_ok = competition.get("winner") == next(iter(other_targets))
        status_ok = row.get("credit_resolution", {}).get("status") == expected_status
        selective_ok.append(selected_only and winner_ok and status_ok)
        en_bloc_rows.append(en_bloc and status_ok)
        no_effect_rows.append(no_effect)

    expected_proposal_ids = set(fixture_map)
    for sign, proposal_ids in selected_proposals_by_sign.items():
        if proposal_ids != expected_proposal_ids:
            reasons.append(f"counterbalance-missing:{sign}")

    if reasons:
        return {"verdict": INVALID, "reasons": reasons}
    if all(selective_ok):
        return {
            "verdict": SUPPORTED,
            "reasons": [
                "all four sign-by-lineage assays changed only the trace-selected path",
                "future competition moved in the prospectively required direction",
                "absence/replay controls stayed credit-neutral",
            ],
        }
    if all(en_bloc_rows):
        return {
            "verdict": EN_BLOC,
            "reasons": [
                "valid trace-bound plural merged ancestry was retained",
                "both lineage IDs were crossed with both evidence signs",
                "every separating assay changed every merged causal path",
                "the current bridge therefore did not selectively resolve lineage",
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
            "valid controls passed but separating assays did not form a uniform "
            "selective, en-bloc, or null pattern"
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
                "future_tied_winners": row["post"]["competition"][
                    "tied_winners"
                ],
                "retained_runtime_trace_sha256": row[
                    "retained_runtime_trace_sha256"
                ],
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

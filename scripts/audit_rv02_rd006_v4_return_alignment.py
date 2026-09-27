"""Audit the preserved RD006 v4 D0 result without running dynamics."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

AUDIT_SCHEMA_VERSION = 1
AUDIT_ID = "RD006_V4_PRESERVED_OUTPUT_RETURN_ALIGNMENT_AUDIT"
ANALYST_GENERATION_ID = (
    "EVA-20260927T230711+0900-R157-RD006-V4-POSTRESULT-RECONCILIATION"
)
PRESERVED_RESULT_HEAD = "50112626ef6a4da364e3fa9268e8feb0d723ea7f"
PRESERVED_SOURCE_HEAD = "44bef35c90f24a11e27000e3c328778733da92b6"
EXPECTED_ARTIFACT_SHA256 = (
    "e40a88cd596b79d1a6b78030c8f7ea3baac5fc5c8579551b7494b37f6b89d3ba"
)
EXPECTED_ARTIFACT_FILE_SHA256 = (
    "62b3ffb6d52926b583b006799d88511c9f840b626bc776cdcaf6ee2f857faf61"
)

NO_SECOND_HIDDEN_SPIKE = "NO_SECOND_HIDDEN_SPIKE"
SPIKE_WITHOUT_EDGE = "SPIKE_WITHOUT_ELIGIBLE_EDGE_TO_CURRENT_RETURN_TARGET"
LAG_OUTSIDE = "ELIGIBLE_EDGE_BUT_LAG_OUTSIDE_0_5_TO_6_5_MS"
ADJACENT_ONLY = "ADJACENT_CLOCK_NOT_SAME_CLOCK"
CEILING_CENSORED = "CEILING_CENSORED"
NO_OTHER_CONSTRUCTION_SOURCE = "NO_OTHER_SOURCE_IN_PRESERVED_CONSTRUCTION"
CAUSES = (
    NO_SECOND_HIDDEN_SPIKE,
    SPIKE_WITHOUT_EDGE,
    LAG_OUTSIDE,
    ADJACENT_ONLY,
    CEILING_CENSORED,
    NO_OTHER_CONSTRUCTION_SOURCE,
)


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def _load_preserved_artifact(path: Path) -> dict[str, Any]:
    file_sha256 = _file_sha256(path)
    if file_sha256 != EXPECTED_ARTIFACT_FILE_SHA256:
        raise ValueError(f"preserved artifact file identity mismatch: {file_sha256}")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        artifact = json.load(handle)
    payload = dict(artifact)
    claimed = payload.pop("artifact_sha256", None)
    computed = _digest(payload)
    if claimed != computed or claimed != EXPECTED_ARTIFACT_SHA256:
        raise ValueError(
            f"preserved artifact payload identity mismatch: claimed={claimed} computed={computed}"
        )
    if artifact.get("source_git_sha") != PRESERVED_SOURCE_HEAD:
        raise ValueError("preserved source identity mismatch")
    if artifact.get("matrix_status") != "D0_INCONCLUSIVE_BOUNDED_EXPLOSION":
        raise ValueError("unexpected preserved v4 matrix status")
    return artifact


def _source_ids(rows: list[dict[str, Any]], predicate=lambda _row: True) -> set[int]:
    return {int(row["source_id"]) for row in rows if predicate(row)}


def _eligible_source_ids(clock: dict[str, Any]) -> set[int]:
    return _source_ids(
        clock["hidden_spike_diagnostics"], lambda row: bool(row["dynamically_eligible"])
    )


def _classify_clock(
    clocks: list[dict[str, Any]], index: int, required_sources: int
) -> dict[str, Any]:
    clock = clocks[index]
    diagnostics = clock["hidden_spike_diagnostics"]
    structural = _source_ids(
        clock["structurally_connected_hidden_sources"],
        lambda row: bool(row["edge_non_negative"]),
    )
    spiking = _source_ids(diagnostics)
    eligible_edge = _source_ids(
        diagnostics,
        lambda row: bool(row["edge_exists"]) and bool(row["edge_non_negative"]),
    )
    outside = _source_ids(
        diagnostics,
        lambda row: (
            bool(row["edge_exists"])
            and bool(row["edge_non_negative"])
            and not bool(row["lag_in_fixed_window"])
        ),
    )
    eligible = _eligible_source_ids(clock)
    adjacent_rows = []
    adjacent_eligible: set[int] = set()
    for adjacent_index in (index - 1, index + 1):
        if not 0 <= adjacent_index < len(clocks):
            continue
        adjacent_clock = clocks[adjacent_index]
        sources = _eligible_source_ids(adjacent_clock)
        adjacent_eligible.update(sources)
        adjacent_rows.append(
            {
                "return_event_id": adjacent_clock["return_event_id"],
                "eligible_hidden_source_ids": sorted(sources),
            }
        )

    if len(eligible) >= required_sources:
        raise ValueError("preserved v4 artifact unexpectedly contains an open gate")
    if len(structural) < required_sources:
        cause = NO_OTHER_CONSTRUCTION_SOURCE
    elif len(spiking) >= required_sources:
        cause = (
            LAG_OUTSIDE
            if len(eligible_edge) >= required_sources and outside
            else SPIKE_WITHOUT_EDGE
        )
    elif len(eligible | adjacent_eligible) >= required_sources:
        cause = ADJACENT_ONLY
    else:
        cause = NO_SECOND_HIDDEN_SPIKE

    return {
        "return_event_id": str(clock["return_event_id"]),
        "return_time_ms": float(clock["return_time_ms"]),
        "return_unit_id": int(clock["return_unit_id"]),
        "observed": True,
        "cause": cause,
        "structural_non_negative_hidden_source_ids": sorted(structural),
        "same_clock_hidden_spike_source_ids": sorted(spiking),
        "same_clock_eligible_edge_source_ids": sorted(eligible_edge),
        "same_clock_lag_outside_source_ids": sorted(outside),
        "same_clock_dynamic_eligible_source_ids": sorted(eligible),
        "dynamic_gate_deficit": required_sources - len(eligible),
        "adjacent_clock_eligible_sources": adjacent_rows,
    }


def _counter_payload(counter: Counter[str]) -> dict[str, int]:
    return {cause: int(counter.get(cause, 0)) for cause in CAUSES}


def _update_linkage(cell: dict[str, Any]) -> dict[str, Any]:
    clocks = cell["return_clocks"]
    return_times = {
        str(row["return_event_id"]): float(row["return_time_ms"]) for row in clocks
    }
    spikes: set[tuple[int, float]] = set()
    eligible_occurrences: set[tuple[int, float]] = set()
    for clock in clocks:
        for spike in clock["hidden_spikes"]:
            spikes.add((int(spike["unit_id"]), float(spike["time_ms"])))
        for row in clock["hidden_spike_diagnostics"]:
            if bool(row["dynamically_eligible"]):
                eligible_occurrences.add(
                    (int(row["source_id"]), float(row["spike_time_ms"]))
                )

    rows = []
    for update in cell["ordinary_updates"]:
        if update["edge_class"] != "PORT_TO_HIDDEN":
            continue
        source_time = return_times.get(str(update["source_event_id"]))
        if source_time is None:
            raise ValueError(
                "PORT_TO_HIDDEN source event is absent from preserved return clocks"
            )
        target_id = int(update["target_id"])
        target_time = source_time + float(update["lag_ms"])
        target_seen = (target_id, target_time) in spikes
        later = sorted(
            time
            for source, time in spikes
            if source == target_id and time > target_time
        )
        later_eligible = sorted(
            time
            for source, time in eligible_occurrences
            if source == target_id and time > target_time
        )
        rows.append(
            {
                "source_event_id": str(update["source_event_id"]),
                "target_event_id": str(update["target_event_id"]),
                "target_hidden_source_id": target_id,
                "source_return_time_ms": source_time,
                "target_hidden_spike_time_ms_inferred_from_source_plus_lag": target_time,
                "target_hidden_spike_located_by_id_and_time": target_seen,
                "later_same_source_hidden_spike_count": len(later),
                "first_later_same_source_hidden_spike_time_ms": later[0]
                if later
                else None,
                "later_same_source_dynamic_eligible_spike_count": len(later_eligible),
                "first_later_same_source_dynamic_eligible_spike_time_ms": later_eligible[
                    0
                ]
                if later_eligible
                else None,
            }
        )
    return {
        "port_to_hidden_update_count": len(rows),
        "target_hidden_spike_located_count": sum(
            row["target_hidden_spike_located_by_id_and_time"] for row in rows
        ),
        "updates_followed_by_later_same_source_hidden_spike": sum(
            bool(row["later_same_source_hidden_spike_count"]) for row in rows
        ),
        "updates_followed_by_later_same_source_dynamic_eligible_spike": sum(
            bool(row["later_same_source_dynamic_eligible_spike_count"]) for row in rows
        ),
        "rows": rows,
    }


def build_audit(preserved_artifact_path: Path) -> dict[str, Any]:
    artifact = _load_preserved_artifact(preserved_artifact_path)
    required = int(
        artifact["dynamic_gate_definition"][
            "minimum_distinct_sources_same_return_clock"
        ]
    )
    if required != 2:
        raise ValueError("preserved gate is not the fixed two-source gate")

    aggregate = Counter[str]()
    deficits = []
    cells = []
    update_aggregate = Counter[str]()
    for pair in artifact["family_pairs"]:
        family = str(pair["family"])
        execution = pair["execution_cells"]
        reference = execution["external_learning_off"]["return_clocks"]
        cell = execution["external_learning_on"]
        clocks = cell["return_clocks"]
        planned = int(cell["planned_clock_count"])
        inspected = int(cell["inspected_clock_count"])
        if planned != len(reference) or inspected != len(clocks):
            raise ValueError(f"clock cardinality mismatch for {family}")
        observed_ids = [row["return_event_id"] for row in clocks]
        reference_ids = [row["return_event_id"] for row in reference]
        if observed_ids != reference_ids[:inspected]:
            raise ValueError(
                f"ON clocks are not the paired preserved prefix for {family}"
            )

        counter = Counter[str]()
        clock_rows = []
        for index in range(inspected):
            row = _classify_clock(clocks, index, required)
            clock_rows.append(row)
            counter[row["cause"]] += 1
            aggregate[row["cause"]] += 1
            deficits.append(int(row["dynamic_gate_deficit"]))
        for reference_clock in reference[inspected:]:
            clock_rows.append(
                {
                    "return_event_id": str(reference_clock["return_event_id"]),
                    "return_time_ms": float(reference_clock["return_time_ms"]),
                    "return_unit_id": int(reference_clock["return_unit_id"]),
                    "observed": False,
                    "cause": CEILING_CENSORED,
                    "dynamic_gate_deficit": None,
                }
            )
            counter[CEILING_CENSORED] += 1
            aggregate[CEILING_CENSORED] += 1
        linkage = _update_linkage(cell)
        for key in (
            "port_to_hidden_update_count",
            "target_hidden_spike_located_count",
            "updates_followed_by_later_same_source_hidden_spike",
            "updates_followed_by_later_same_source_dynamic_eligible_spike",
        ):
            update_aggregate[key] += int(linkage[key])
        cells.append(
            {
                "family": family,
                "execution_cell_id": cell["execution_cell_id"],
                "completion_class": "COMPLETE"
                if bool(cell["complete_non_exploded"])
                else "BOUNDED",
                "planned_clock_count": planned,
                "inspected_clock_count": inspected,
                "distinct_hidden_source_count": int(
                    cell["distinct_hidden_source_count"]
                ),
                "observed_hidden_spike_count": int(cell["observed_hidden_spike_count"]),
                "cause_counts": _counter_payload(counter),
                "port_to_hidden_update_linkage": linkage,
                "clock_audit": clock_rows,
            }
        )

    planned_total = sum(cell["planned_clock_count"] for cell in cells)
    inspected_total = sum(cell["inspected_clock_count"] for cell in cells)
    if sum(aggregate.values()) != planned_total:
        raise ValueError("classification is not exhaustive")

    audit = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "audit_id": AUDIT_ID,
        "analyst_generation_id": ANALYST_GENERATION_ID,
        "object_id": artifact["object_id"],
        "protocol_id": artifact["protocol_id"],
        "development_phase": "RESULT_EXPOSED_DEVELOPMENT",
        "claim_ceiling": artifact["claim_ceiling"],
        "evidentiary_status": "DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT",
        "preserved_result_head": PRESERVED_RESULT_HEAD,
        "preserved_source_head": PRESERVED_SOURCE_HEAD,
        "preserved_artifact_sha256": artifact["artifact_sha256"],
        "preserved_artifact_file_sha256": EXPECTED_ARTIFACT_FILE_SHA256,
        "new_dynamic_execution": False,
        "artifact_mutated": False,
        "result_reclassified": False,
        "capability_scoring": False,
        "held_out_use": False,
        "fixed_gate": {
            "required_distinct_hidden_sources_same_clock": required,
            "lag_window_ms": artifact["dynamic_gate_definition"][
                "observed_spike_to_return_lag_window_ms"
            ],
            "unchanged": True,
        },
        "classification_precedence": [
            NO_OTHER_CONSTRUCTION_SOURCE,
            LAG_OUTSIDE,
            SPIKE_WITHOUT_EDGE,
            ADJACENT_ONLY,
            NO_SECOND_HIDDEN_SPIKE,
            CEILING_CENSORED,
        ],
        "planned_on_clock_count": planned_total,
        "inspected_on_clock_count": inspected_total,
        "aggregate_cause_counts": _counter_payload(aggregate),
        "minimum_deficit_to_fixed_two_source_gate": {
            "minimum_observed_clock_deficit": min(deficits),
            "maximum_observed_clock_deficit": max(deficits),
            "sum_over_inspected_on_clocks": sum(deficits),
            "unobserved_ceiling_censored_on_clocks_excluded": aggregate[
                CEILING_CENSORED
            ],
        },
        "port_to_hidden_update_linkage_aggregate": dict(update_aggregate),
        "linkage_interpretation": {
            "status": "DESCRIPTIVE_NOT_CAUSAL",
            "join_basis": "target hidden source id plus target time inferred from source return time and recorded update lag",
            "causal_effect_identified": False,
        },
        "trace_sufficiency": {
            "sufficient_for": [
                "classifying every inspected ON return clock by structural source coverage, hidden firing, current-target edge, lag window, and same-clock eligibility",
                "checking immediately adjacent clocks for split dynamic-eligible source identities",
                "describing whether a PORT_TO_HIDDEN update target source spikes again later",
            ],
            "unknown_or_not_identified": [
                "dynamic outcomes for 16 ceiling-censored opposing-reversal ON clocks",
                "direct hidden event-id join because hidden spike rows do not carry target_event_id",
                "counterfactual later spike trajectory without each PORT_TO_HIDDEN update",
                "causal contribution of a particular update to a later same-source spike or return-clock eligibility",
            ],
        },
        "cells": cells,
        "preserved_v4_result": artifact["matrix_status"],
        "preserved_v4_result_changed": False,
        "recommendation": {
            "disposition": "NO_PROPOSAL",
            "reason": "The preserved trace supports descriptive recurrence and failure classification but not a causal attribution separating learner-update effect from concurrent network state; one fresh scientific invariant is not identified by these bytes alone.",
            "implementation_or_execution_authorized": False,
        },
        "later_e0_e1_es_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "next_action": "WAIT_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    audit["audit_sha256"] = _digest(audit)
    return audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    audit = build_audit(args.artifact)
    rendered = json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()

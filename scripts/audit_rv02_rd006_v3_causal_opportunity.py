"""Audit the preserved RD006 v3 D0 result without running dynamics.

The audit reads only the exact R159 result artifact.  It classifies why each
scheduled return clock lacked a second distinct dynamically eligible hidden
source under the fixed R151 two-source gate.  Unobserved clocks in the bounded
cell are identified from the paired preserved OFF schedule and are never
assigned a dynamic outcome.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

AUDIT_SCHEMA_VERSION = 1
AUDIT_ID = "RD006_V3_PRESERVED_RESULT_CAUSAL_OPPORTUNITY_AUDIT"
ANALYST_GENERATION_ID = (
    "EVA-20260927T180100+0900-R152-RD006-V3-POSTRESULT-CAUSAL-AUDIT"
)
PRESERVED_RESULT_HEAD = "540fa54f45a8cdc467eb2695270035cb9332f2fb"
PRESERVED_SOURCE_HEAD = "8867c0565e25a0c76749c12eec7f4c03238b7aef"
EXPECTED_ARTIFACT_SHA256 = (
    "a71e324014b92ecf5680608f60f78e431c192f353d29af0633193546eec7a8da"
)
EXPECTED_ARTIFACT_FILE_SHA256 = (
    "ad7dc60af79681a30d67f1c0d2a4e39607a8984122f52bf9a65949950772b3f9"
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
        raise ValueError(
            "preserved artifact file identity mismatch: "
            f"{file_sha256} != {EXPECTED_ARTIFACT_FILE_SHA256}"
        )
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        artifact = json.load(handle)
    payload = dict(artifact)
    claimed = payload.pop("artifact_sha256", None)
    computed = _digest(payload)
    if claimed != computed or claimed != EXPECTED_ARTIFACT_SHA256:
        raise ValueError(
            "preserved artifact payload identity mismatch: "
            f"claimed={claimed} computed={computed}"
        )
    if artifact.get("source_git_sha") != PRESERVED_SOURCE_HEAD:
        raise ValueError("preserved source identity mismatch")
    if artifact.get("matrix_status") != "D0_INCONCLUSIVE_BOUNDED_EXPLOSION":
        raise ValueError("unexpected preserved v3 matrix status")
    return artifact


def _source_ids(
    rows: list[dict[str, Any]],
    predicate: Callable[[dict[str, Any]], bool] = lambda _row: True,
) -> set[int]:
    return {int(row["source_id"]) for row in rows if predicate(row)}


def _eligible_source_ids(clock: dict[str, Any]) -> set[int]:
    return _source_ids(
        clock["hidden_spike_diagnostics"],
        lambda row: bool(row["dynamically_eligible"]),
    )


def _classify_inspected_clock(
    clocks: list[dict[str, Any]], index: int, required_sources: int
) -> dict[str, Any]:
    clock = clocks[index]
    diagnostics = clock["hidden_spike_diagnostics"]
    structural_sources = _source_ids(
        clock["structurally_connected_hidden_sources"],
        lambda row: bool(row["edge_non_negative"]),
    )
    spiking_sources = _source_ids(diagnostics)
    eligible_edge_sources = _source_ids(
        diagnostics,
        lambda row: bool(row["edge_exists"]) and bool(row["edge_non_negative"]),
    )
    eligible_sources = _eligible_source_ids(clock)
    outside_window_sources = _source_ids(
        diagnostics,
        lambda row: (
            bool(row["edge_exists"])
            and bool(row["edge_non_negative"])
            and not bool(row["lag_in_fixed_window"])
        ),
    )

    adjacent_rows = []
    adjacent_eligible_sources: set[int] = set()
    for adjacent_index in (index - 1, index + 1):
        if not 0 <= adjacent_index < len(clocks):
            continue
        adjacent_clock = clocks[adjacent_index]
        sources = _eligible_source_ids(adjacent_clock)
        adjacent_eligible_sources.update(sources)
        adjacent_rows.append(
            {
                "return_event_id": adjacent_clock["return_event_id"],
                "eligible_hidden_source_ids": sorted(sources),
            }
        )

    if len(eligible_sources) >= required_sources:
        raise ValueError("preserved v3 artifact unexpectedly contains an open gate")
    if len(structural_sources) < required_sources:
        cause = NO_OTHER_CONSTRUCTION_SOURCE
    elif len(spiking_sources) >= required_sources:
        if (
            len(eligible_edge_sources) >= required_sources
            and outside_window_sources
        ):
            cause = LAG_OUTSIDE
        else:
            cause = SPIKE_WITHOUT_EDGE
    elif len(eligible_sources | adjacent_eligible_sources) >= required_sources:
        cause = ADJACENT_ONLY
    else:
        cause = NO_SECOND_HIDDEN_SPIKE

    return {
        "return_event_id": str(clock["return_event_id"]),
        "return_time_ms": float(clock["return_time_ms"]),
        "return_unit_id": int(clock["return_unit_id"]),
        "observed": True,
        "cause": cause,
        "structural_non_negative_hidden_source_ids": sorted(structural_sources),
        "same_clock_hidden_spike_source_ids": sorted(spiking_sources),
        "same_clock_eligible_edge_source_ids": sorted(eligible_edge_sources),
        "same_clock_lag_outside_source_ids": sorted(outside_window_sources),
        "same_clock_dynamic_eligible_source_ids": sorted(eligible_sources),
        "dynamic_gate_deficit": required_sources - len(eligible_sources),
        "adjacent_clock_eligible_sources": adjacent_rows,
    }


def _counter_payload(counter: Counter[str]) -> dict[str, int]:
    return {cause: int(counter.get(cause, 0)) for cause in CAUSES}


def build_audit(preserved_artifact_path: Path) -> dict[str, Any]:
    artifact = _load_preserved_artifact(preserved_artifact_path)
    required_sources = int(
        artifact["dynamic_gate_definition"][
            "minimum_distinct_sources_same_return_clock"
        ]
    )
    if required_sources != 2:
        raise ValueError("the preserved R151 gate is not the fixed two-source gate")

    aggregate = Counter[str]()
    arm_aggregate: dict[str, Counter[str]] = {}
    status_aggregate: dict[str, Counter[str]] = {}
    observed_deficits: list[int] = []
    cells = []

    for pair in artifact["family_pairs"]:
        family = str(pair["family"])
        execution_cells = pair["execution_cells"]
        reference_clocks = execution_cells["external_learning_off"][
            "inspected_clocks"
        ]
        if len(reference_clocks) != int(pair["schedule_event_count"]):
            raise ValueError(f"paired OFF schedule is incomplete for {family}")

        for arm, cell in execution_cells.items():
            clocks = cell["inspected_clocks"]
            planned_count = int(cell["planned_clock_count"])
            inspected_count = int(cell["inspected_clock_count"])
            if inspected_count != len(clocks) or planned_count != len(reference_clocks):
                raise ValueError(f"clock cardinality mismatch for {family}/{arm}")
            observed_ids = [str(row["return_event_id"]) for row in clocks]
            reference_ids = [
                str(row["return_event_id"]) for row in reference_clocks
            ]
            if observed_ids != reference_ids[:inspected_count]:
                raise ValueError(f"observed clocks are not the paired prefix for {family}/{arm}")

            completion_class = (
                "COMPLETE" if bool(cell["complete_non_exploded"]) else "BOUNDED"
            )
            cell_counter = Counter[str]()
            clock_rows = []
            for index in range(inspected_count):
                row = _classify_inspected_clock(clocks, index, required_sources)
                clock_rows.append(row)
                cause = str(row["cause"])
                cell_counter[cause] += 1
                aggregate[cause] += 1
                observed_deficits.append(int(row["dynamic_gate_deficit"]))

            for reference in reference_clocks[inspected_count:]:
                row = {
                    "return_event_id": str(reference["return_event_id"]),
                    "return_time_ms": float(reference["return_time_ms"]),
                    "return_unit_id": int(reference["return_unit_id"]),
                    "observed": False,
                    "cause": CEILING_CENSORED,
                    "dynamic_gate_deficit": None,
                }
                clock_rows.append(row)
                cell_counter[CEILING_CENSORED] += 1
                aggregate[CEILING_CENSORED] += 1

            if len(clock_rows) != planned_count:
                raise ValueError(f"audit did not classify every scheduled clock: {family}/{arm}")
            arm_aggregate.setdefault(arm, Counter()).update(cell_counter)
            status_key = f"{arm}/{completion_class}"
            status_aggregate.setdefault(status_key, Counter()).update(cell_counter)
            cells.append(
                {
                    "family": family,
                    "arm": arm,
                    "completion_class": completion_class,
                    "execution_cell_id": cell["execution_cell_id"],
                    "planned_clock_count": planned_count,
                    "inspected_clock_count": inspected_count,
                    "cause_counts": _counter_payload(cell_counter),
                    "clock_audit": clock_rows,
                }
            )

    planned_clock_count = sum(row["planned_clock_count"] for row in cells)
    inspected_clock_count = sum(row["inspected_clock_count"] for row in cells)
    if sum(aggregate.values()) != planned_clock_count:
        raise ValueError("aggregate classification is not exhaustive")

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
        "parameter_change": False,
        "capability_scoring": False,
        "held_out_use": False,
        "fixed_gate": {
            "required_distinct_hidden_sources_same_clock": required_sources,
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
        "classification_notes": {
            "adjacent_clock": (
                "immediately preceding or following scheduled return clock "
                "within the same preserved family/arm"
            ),
            "ceiling_censored": (
                "clock identity comes from the paired preserved OFF schedule; "
                "no ON-arm dynamic outcome is inferred"
            ),
        },
        "planned_clock_count": planned_clock_count,
        "inspected_clock_count": inspected_clock_count,
        "aggregate_cause_counts": _counter_payload(aggregate),
        "cause_counts_by_arm": {
            arm: _counter_payload(counter)
            for arm, counter in sorted(arm_aggregate.items())
        },
        "cause_counts_by_arm_and_completion": {
            key: _counter_payload(counter)
            for key, counter in sorted(status_aggregate.items())
        },
        "minimum_deficit_to_fixed_two_source_gate": {
            "minimum_observed_clock_deficit": min(observed_deficits),
            "maximum_observed_clock_deficit": max(observed_deficits),
            "sum_over_inspected_clocks": sum(observed_deficits),
            "unobserved_ceiling_censored_clocks_excluded": aggregate[
                CEILING_CENSORED
            ],
        },
        "cells": cells,
        "preserved_v3_result": artifact["matrix_status"],
        "preserved_v3_result_changed": False,
        "recommendation": {
            "disposition": "ONE_FRESH_PROSPECTIVE_REVISION",
            "single_changed_invariant": "ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY",
            "change": (
                "permit prospectively specified PORT_TO_HIDDEN ordinary external "
                "updates while keeping hidden-return learning disabled"
            ),
            "held_fixed": [
                "TWO_DISTINCT_ACTUAL_HIDDEN_SOURCES_SAME_RETURN_CLOCK",
                "0.5_TO_6.5_MS_LAG_WINDOW",
                "V3_STATIC_TOPOLOGY",
                "V3_SCHEDULE",
                "THRESHOLD_GAIN_STIMULUS_AND_RESOURCE_CEILINGS",
            ],
            "rationale": (
                "The preserved matrix shows that current PORT_TO_PORT-only learning "
                "occasionally creates one eligible source but never two. A fresh "
                "boundary hypothesis is more informative than another timing or "
                "topology retune."
            ),
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

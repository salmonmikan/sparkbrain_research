from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

REF = "REF_GLOBAL_SCAN"


def parse_sweep_id(point_id: str) -> tuple[str, str] | None:
    if not point_id.startswith("sweep:"):
        return None
    _, key, value = point_id.split(":", 2)
    return key, value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    raw = json.loads(Path(args.raw).read_text(encoding="utf-8"))
    sweeps: dict[str, list[dict[str, Any]]] = defaultdict(list)
    invalid: list[dict[str, str]] = []
    tradeoffs: list[dict[str, Any]] = []
    reductions_by_point: list[dict[str, Any]] = []

    for entry in raw["points"]:
        point = entry["point"]
        ref = entry["comparators"][REF]["resource_vector"]
        ref_ops = ref["primitive_operation_total"]
        reductions: list[dict[str, Any]] = []
        for comparator, result in entry["comparators"].items():
            if comparator == REF:
                continue
            if not result["equivalence"]["valid"]:
                invalid.append({"point": point["id"], "comparator": comparator})
                continue
            resource = result["resource_vector"]
            lower = resource["primitive_operation_total"] < ref_ops
            if lower:
                reduction = {
                    "comparator": comparator,
                    "reference_ops": ref_ops,
                    "comparator_ops": resource["primitive_operation_total"],
                    "operation_ratio": resource["primitive_operation_total"] / ref_ops,
                    "peak_slots": resource["peak_logical_history_timestamp_active_slots"],
                    "reference_peak_slots": ref["peak_logical_history_timestamp_active_slots"],
                    "history_manipulations": resource["history_entry_manipulation_count"],
                    "delay_buckets": resource["distinct_live_delay_buckets"],
                }
                reductions.append(reduction)
                if (
                    resource["peak_logical_history_timestamp_active_slots"]
                    > ref["peak_logical_history_timestamp_active_slots"]
                    or resource["history_entry_manipulation_count"] > 0
                ):
                    tradeoffs.append({"point": point["id"], **reduction})
        reductions_by_point.append({"point": point["id"], "reductions": reductions})
        sweep = parse_sweep_id(point["id"])
        if sweep is not None:
            sweeps[sweep[0]].append(entry)

    adjacent_signals: list[dict[str, Any]] = []
    for sweep_name, entries in sweeps.items():
        for first, second in zip(entries, entries[1:], strict=False):
            first_results = first["comparators"]
            second_results = second["comparators"]
            first_ref = first_results[REF]["resource_vector"]["primitive_operation_total"]
            second_ref = second_results[REF]["resource_vector"]["primitive_operation_total"]
            for comparator in first_results:
                if comparator == REF:
                    continue
                a = first_results[comparator]
                b = second_results[comparator]
                if not a["equivalence"]["valid"] or not b["equivalence"]["valid"]:
                    continue
                a_ops = a["resource_vector"]["primitive_operation_total"]
                b_ops = b["resource_vector"]["primitive_operation_total"]
                if a_ops < first_ref and b_ops < second_ref:
                    adjacent_signals.append(
                        {
                            "sweep": sweep_name,
                            "first": first["point"]["id"],
                            "second": second["point"]["id"],
                            "comparator": comparator,
                            "first_ratio": a_ops / first_ref,
                            "second_ratio": b_ops / second_ref,
                        }
                    )

    anchor = raw["behavioral_anchor_probe"]
    anchor_valid = bool(anchor["algebraic_match"] and anchor["target_fired_on_probe"])
    ordinary_reduction_exhaustion_signal = bool(adjacent_signals) and not invalid and anchor_valid
    no_localization_on_grid = not any(item["reductions"] for item in reductions_by_point)

    summary = {
        "schema_version": 1,
        "contract_id": raw["contract_id"],
        "candidate_id": raw["candidate_id"],
        "research_layer": "ARCHITECTURE_STUDY",
        "claim_ceiling": "SYSTEM",
        "evidentiary_status": "NON_EVIDENTIARY_SYSTEM_ARCHITECTURE_INTERPRETATION",
        "behavioral_anchor_valid": anchor_valid,
        "invalid_comparators": invalid,
        "ordinary_reduction_exhaustion_signal": ordinary_reduction_exhaustion_signal,
        "adjacent_reduction_signals": adjacent_signals,
        "tradeoff_records": tradeoffs,
        "no_localization_on_grid": no_localization_on_grid,
        "point_reductions": reductions_by_point,
        "claim_scope": (
            "Current SparkBrain reference-engine resource localization under the bound event-count "
            "eligibility semantics only; no biological mechanism, PRE_FORMAL, FORMAL, H5, "
            "continuous-time, wall-clock, cache, bandwidth, or energy claim."
        ),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

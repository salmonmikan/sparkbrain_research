"""Read-only, post-hoc diagnosis of pinned retention traces; imports no model code."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

ARTIFACT = "artifacts/research/retention_equality_diagnosis_20261002"
BINDING_SHA256 = "bb6cd04cb8dbaab46a567c7f54114bf54e79fcc5d8a087cd1a0628f3bfc73610"
COMPARISONS = (("return", "L", "Fw"), ("return", "L", "G"),
               ("novel", "L", "Fw"), ("return", "L", "C"))
FIXTURES = (910075, 910076)
FILES = ("predictions.jsonl", "receipts.jsonl", "apply.jsonl", "final-state.json")
SOURCE_FILES = (
    "src/sparkbrain/v05/brain.py", "src/sparkbrain/v04/field.py",
    "src/sparkbrain/v05/assemblies.py", "src/sparkbrain/v05/prediction.py",
    "src/sparkbrain/v05/homeostasis.py", "scripts/temporal_reuse_loop_probe.py",
    "scripts/run_plasticity_retention.py",
)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("nonfinite JSON number")
    return number


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def parse(raw: str | bytes) -> Any:
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_float=finite_float, parse_constant=reject_constant)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def required_jobs() -> list[str]:
    return sorted({f"{seed}-{condition}-{arm}" for seed in FIXTURES
                   for condition, left, right in COMPARISONS for arm in (left, right)})


def required_raw_files() -> list[str]:
    return [f"jobs/{job}/{name}" for job in required_jobs() for name in FILES]


def checked_bytes(root: Path, relative: str, digest: str) -> bytes:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("input path escapes supplied root")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError(f"input hash differs: {relative}")
    return raw


def get(row: dict, dotted: str) -> Any:
    value = row
    for key in dotted.split("."):
        value = value[key]
    return value


def spike_events(row: dict) -> list[list[int | float]]:
    return [[spike["unit_id"], spike["time_ms"]]
            for spike in row["raw_result"]["v04_result"]["spikes"]]


def first_difference(left: list, right: list) -> int | None:
    if len(left) != len(right):
        raise ValueError("comparison lengths differ")
    return next((index for index, pair in enumerate(zip(left, right, strict=True))
                 if pair[0] != pair[1]), None)


def summarize_pair(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    aa, bb = left["predictions.jsonl"], right["predictions.jsonl"]
    if len(aa) != 32 or len(bb) != 32:
        raise ValueError("expected complete 32-row branches")
    for branch in (left, right):
        receipts, applies = branch["receipts.jsonl"], branch["apply.jsonl"]
        if len(receipts) != 32 or len(applies) != 32:
            raise ValueError("incomplete receipt/apply records")
        for index, (prediction, receipt, apply) in enumerate(zip(
            branch["predictions.jsonl"], receipts, applies, strict=True
        )):
            if receipt["index"] != index or apply["index"] != index:
                raise ValueError("receipt/apply row order differs")
            if any(receipt[key] != prediction[key] for key in ("occurrence_id", "outcome")):
                raise ValueError("receipt does not bind the prediction")
    for index, (a, b) in enumerate(zip(aa, bb, strict=True)):
        if a["index"] != index or b["index"] != index:
            raise ValueError("row order differs")
        for key in ("input_sha256", "occurrence_id", "outcome", "query_time_ms"):
            if a[key] != b[key]:
                raise ValueError(f"unmatched paired input: {key}")
    paths = (
        "p1", "native", "assembly_id", "mature", "candidate_prototypes",
        "readout_counts_before_receipt", "raw_result.patterns",
        "raw_result.assembly_activations", "raw_result.prediction",
        "raw_result.emitted_pulses", "raw_result.v04_result.spikes",
        "raw_result.v04_result.cascades", "raw_result.stability",
    )
    equal = {key: sum(get(a, key) == get(b, key) for a, b in zip(aa, bb, strict=True))
             for key in paths}
    first = {key: first_difference([get(a, key) for a in aa], [get(b, key) for b in bb])
             for key in paths}
    events_a, events_b = [spike_events(a) for a in aa], [spike_events(b) for b in bb]
    equal["spike_unit_time"] = sum(a == b for a, b in zip(events_a, events_b, strict=True))
    first["spike_unit_time"] = first_difference(events_a, events_b)
    changed_fields: Counter[str] = Counter()
    changed_units: Counter[str] = Counter()
    potential_deltas = []
    aligned_rows = 0
    for a, b, event_a, event_b in zip(aa, bb, events_a, events_b, strict=True):
        if event_a != event_b:
            continue
        aligned_rows += 1
        for x, y in zip(a["raw_result"]["v04_result"]["spikes"],
                        b["raw_result"]["v04_result"]["spikes"], strict=True):
            if set(x) != set(y):
                raise ValueError("spike record schema differs")
            changed_fields.update(key for key in x if x[key] != y[key])
            if x["potential_before_reset"] != y["potential_before_reset"]:
                changed_units[str(x["unit_id"])] += 1
            potential_deltas.append(abs(x["potential_before_reset"] - y["potential_before_reset"]))
    sides = []
    for branch in (left, right):
        updates = [u for row in branch["apply.jsonl"] for u in row["updates"]]
        margins = [s["potential_before_reset"] - s["dynamic_threshold"]
                   for row in branch["predictions.jsonl"]
                   for s in row["raw_result"]["v04_result"]["spikes"]
                   if s["unit_id"] in (45, 56, 63)]
        sides.append({
            "nonzero_weight_writes": sum(u["actual_delta_weight"] != 0 for u in updates),
            "actual_absolute_weight_write_sum": math.fsum(abs(u["actual_delta_weight"])
                                                          for u in updates),
            "clipped_updates": sum(u["clipped"] for u in updates),
            "eligible_edge_post_apply_weight_range": [min(u["weight_expected"] for u in updates),
                                               max(u["weight_expected"] for u in updates)],
            "initial_readout_counts": branch["predictions.jsonl"][0][
                "readout_counts_before_receipt"],
            "final_readout_counts": branch["final-state.json"]["brain"]["predictor"]["counts"],
            "abstention_indices": [row["index"] for row in branch["predictions.jsonl"]
                                   if row["native"] is None],
            "eligible_apply_edge_ids": sorted({u["edge"] for u in updates}),
            "observed_target_firing_margins": {
                "unit_ids": [45, 56, 63], "count": len(margins),
                "selection": "Post-hoc subset: targets of the observed eligible apply edges.",
                "minimum": min(margins), "maximum": max(margins),
                "boundary": "Logged firing events only; not silent/refractory arrival margins.",
            },
        })
    final_a, final_b = left["final-state.json"]["brain"], right["final-state.json"]["brain"]
    final_equal = {key: final_a[key] == final_b[key]
                   for key in ("assemblies", "predictor", "receptors", "homeostasis")}
    units_a = final_a["base"]["payload"]["field"]["units"]
    units_b = final_b["base"]["payload"]["field"]["units"]
    unit_changes = {}
    for x, y in zip(units_a, units_b, strict=True):
        if x["unit_id"] != y["unit_id"]:
            raise ValueError("final unit order differs")
        if x != y:
            unit_changes[str(x["unit_id"])] = sorted(key for key in x if x[key] != y[key])
    receipts_a, receipts_b = left["receipts.jsonl"], right["receipts.jsonl"]
    receipt_equal = sum(a["readout_counts_after_receipt"] == b["readout_counts_after_receipt"]
                        for a, b in zip(receipts_a, receipts_b, strict=True))
    return {
        "rows_per_branch": 32, "exact_equal_row_counts": equal,
        "first_difference_zero_based_index": first,
        "aligned_spike_rows": aligned_rows,
        "aligned_spike_changed_fields": dict(sorted(changed_fields.items())),
        "aligned_spike_potential_changed_units": dict(sorted(changed_units.items())),
        "maximum_aligned_spike_potential_difference": max(potential_deltas),
        "left": sides[0], "right": sides[1],
        "final_component_exact_equality": final_equal,
        "final_unit_changed_fields": unit_changes,
        "equal_post_receipt_count_tables": receipt_equal,
    }


def analyze(run_root: Path, source_root: Path, binding: dict[str, Any]) -> dict[str, Any]:
    logical = json.dumps(binding, sort_keys=True, separators=(",", ":"), allow_nan=False)
    if hashlib.sha256(logical.encode()).hexdigest() != BINDING_SHA256:
        raise ValueError("binding differs from pinned retained-data contract")
    if set(binding["raw_files"]) != set(required_raw_files()):
        raise ValueError("raw input inventory differs")
    if set(binding["source_files"]) != set(SOURCE_FILES):
        raise ValueError("source inventory differs")
    blobs = {relative: checked_bytes(run_root, relative, digest)
             for relative, digest in binding["raw_files"].items()}
    for relative, digest in binding["source_files"].items():
        checked_bytes(source_root, relative, digest)  # Source bytes only; never execute/import.
    jobs = {}
    for job in required_jobs():
        jobs[job] = {}
        for filename in FILES:
            raw = blobs[f"jobs/{job}/{filename}"]
            jobs[job][filename] = ([parse(line) for line in raw.splitlines()]
                                   if filename.endswith(".jsonl") else parse(raw))
    comparisons = []
    for seed in FIXTURES:
        for condition, left, right in COMPARISONS:
            comparisons.append({
                "fixture": seed, "condition": condition, "left_arm": left,
                "right_arm": right,
                **summarize_pair(jobs[f"{seed}-{condition}-{left}"],
                                 jobs[f"{seed}-{condition}-{right}"]),
            })
    after = {relative: hashlib.sha256((run_root / relative).read_bytes()).hexdigest()
             for relative in binding["raw_files"]}
    if after != binding["raw_files"]:
        raise ValueError("raw files changed during read-only analysis")
    return {
        "classification": "POST_HOC_DATA_ONLY_NONCANONICAL_NON_EVIDENTIARY",
        "scientific_credit": 0, "model_calls": 0,
        "source_commit": binding["source_commit"],
        "result_publication_commit": binding["result_publication_commit"],
        "raw_files_read": len(blobs), "source_files_read": len(SOURCE_FILES),
        "raw_files_unchanged": True, "comparisons": comparisons,
        "boundary": "Descriptive retained-data diagnosis; original support gate is unchanged.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    default_binding = Path(__file__).resolve().parents[1] / ARTIFACT / "input_binding.json"
    parser.add_argument("--binding", type=Path, default=default_binding)
    args = parser.parse_args()
    result = analyze(args.run_root, args.source_root, parse(args.binding.read_bytes()))
    print(canonical(result).decode(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

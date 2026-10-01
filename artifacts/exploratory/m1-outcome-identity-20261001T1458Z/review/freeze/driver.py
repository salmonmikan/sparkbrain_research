"""Frozen, non-evidentiary M1 public-Pilot diagnostic; no runtime code changes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import traceback
from functools import partial
from pathlib import Path


def canonical(value):
    return (
        json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
    )


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        handle.write(canonical(value))


def digest_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def load_payloads(root):
    files = sorted(root.rglob("*.json"))
    payloads = {}
    for path in files:
        raw = path.read_bytes()
        value = json.loads(raw)
        if raw != canonical(value).encode():
            raise RuntimeError(f"noncanonical checkpoint: {path.name}")
        payloads[str(path.relative_to(root))] = value
    expected = {
        "predictive/reference-brain.json",
        "predictive/pilot-state.json",
        "scope/sb002-state.json",
    }
    if set(payloads) != expected:
        raise RuntimeError("checkpoint file set differs from the frozen contract")
    return payloads


def capture(pilot, directory):
    from sparkbrain.system_build.causal_scope_revision import (
        ScopeRevisionCheckpointManager,
    )
    from sparkbrain.system_build.predictive_revision import PilotCheckpointManager

    directory.mkdir()
    before = pilot.inspect()
    before_hash = pilot.state_hash()
    payload_sets = []
    for suffix in ("save1", "save2"):
        root = directory / suffix
        root.mkdir()
        PilotCheckpointManager.save(pilot.predictive, root / "predictive")
        ScopeRevisionCheckpointManager.save(pilot.scoped, root / "scope")
        payload_sets.append(load_payloads(root))
    after = pilot.inspect()
    after_hash = pilot.state_hash()
    neutral = (
        before == after
        and before_hash == after_hash
        and payload_sets[0] == payload_sets[1]
    )
    result = {
        "inspection": before,
        "inspection_hash": before_hash,
        "serialized_components": payload_sets[0],
        "repeated_save_payload_equal": payload_sets[0] == payload_sets[1],
        "serialization_state_neutral": neutral,
    }
    write_json(directory / "snapshot.json", result)
    if not neutral:
        write_json(
            directory / "serialization_failure.json",
            {
                "after_inspection": after,
                "after_hash": after_hash,
                "second_payloads": payload_sets[1],
            },
        )
        raise RuntimeError("serialization is not state-neutral")
    return result


def same_state(before, after):
    return (
        before["inspection"] == after["inspection"]
        and before["inspection_hash"] == after["inspection_hash"]
        and before["serialized_components"] == after["serialized_components"]
    )


def record_call(pilot, operation, input_row, directory, invoke, snapshot=capture):
    directory.mkdir()
    before = snapshot(pilot, directory / "before")
    output = None
    error = None
    try:
        result = invoke()
        output = result.as_dict()
    except Exception as exc:  # noqa: BLE001 - preserve every public API exception verbatim
        error = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
    after = snapshot(pilot, directory / "after")
    row = {
        "operation": operation,
        "input": input_row,
        "output": output,
        "exception": error,
        "before": before,
        "after": after,
        "complete_serialized_state_equal": same_state(before, after),
        "sequence_delta": after["inspection"]["sequence"]
        - before["inspection"]["sequence"],
    }
    write_json(directory / "record.json", row)
    if error is not None and not row["complete_serialized_state_equal"]:
        raise RuntimeError("rejected call changed complete serialized state")
    return row


def verify_freeze(root):
    manifest = json.loads((root / "FREEZE_MANIFEST.json").read_text())
    observed = {
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file()
        and p.name != "FREEZE_MANIFEST.json"
        and "__pycache__" not in p.parts
    }
    if observed != set(manifest["files"]):
        raise RuntimeError("frozen file inventory mismatch")
    for relative, expected in manifest["files"].items():
        if digest_bytes((root / relative).read_bytes()) != expected:
            raise RuntimeError(f"frozen file digest mismatch: {relative}")
    return digest_bytes((root / "FREEZE_MANIFEST.json").read_bytes())


def run(output):
    frozen = Path(__file__).resolve().parent
    freeze_hash = verify_freeze(frozen)
    output.mkdir()
    write_json(
        output / "STARTED.json",
        {
            "diagnostic_id": "exploratory-m1-outcome-identity-20261001T1458Z",
            "freeze_sha256": freeze_hash,
            "scientific_credit": 0,
        },
    )
    write_json(
        output / "environment.json",
        {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "executable": sys.executable,
            "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
            "cpu_only": True,
            "runtime_dependencies": "Python standard library; frozen local source",
            "runtime_network_calls": "none in driver",
        },
    )
    sys.path.insert(0, str(frozen / "source" / "src"))
    from sparkbrain.system_build.integrated_m1 import (
        IntegratedM1Pilot,
        M1Observation,
        M1OutcomeReceipt,
    )

    matrix = json.loads((frozen / "matrix.json").read_text())
    summaries = []
    raw_path = output / "calls.jsonl"
    with raw_path.open("x", encoding="utf-8") as raw:
        for case in matrix["cases"]:
            pilot = IntegratedM1Pilot()
            case_dir = output / case["case_id"]
            case_dir.mkdir()
            rows = []
            for index, step in enumerate(case["steps"]):
                operation = step["operation"]
                input_row = step["input"]
                if operation == "observe":
                    obj = M1Observation.from_dict(input_row)
                    invoke = partial(pilot.observe, obj)
                else:
                    obj = M1OutcomeReceipt.from_dict(input_row)
                    invoke = partial(pilot.apply_outcome, obj)
                row = record_call(
                    pilot,
                    operation,
                    input_row,
                    case_dir / f"call-{index + 1:02d}",
                    invoke,
                )
                row["case_id"] = case["case_id"]
                row["call_index"] = index + 1
                raw.write(canonical(row))
                raw.flush()
                rows.append(row)
                if (
                    case["arm"] == "exact_reversal"
                    and index == 5
                    and row["exception"] is None
                ):
                    raise RuntimeError(
                        "exact reversal committed; source reconciliation required"
                    )
            probe = rows[5]
            redelivery = rows[6]
            fourth = rows[7]
            summary = {
                "case_id": case["case_id"],
                "context": case["context"],
                "arm": case["arm"],
                "probe_action": rows[4]["output"],
                "probe_revision": probe["output"],
                "probe_exception": probe["exception"],
                "probe_complete_serialized_state_equal": probe[
                    "complete_serialized_state_equal"
                ],
                "probe_new_commits": probe["sequence_delta"],
                "redelivery_exception": redelivery["exception"],
                "redelivery_output": redelivery["output"],
                "redelivery_complete_serialized_state_equal": redelivery[
                    "complete_serialized_state_equal"
                ],
                "redelivery_new_commits": redelivery["sequence_delta"],
                "fourth_action": fourth["output"],
                "fourth_exception": fourth["exception"],
                "final_sequence": fourth["after"]["inspection"]["sequence"],
                "final_pending_event": fourth["after"]["inspection"][
                    "pending_observation"
                ],
                "observation_attempts": 4,
                "outcome_delivery_attempts": 4,
                "new_committed_outcomes": sum(row["sequence_delta"] for row in rows),
                "serialization_checks": 16,
            }
            summaries.append(summary)
            write_json(case_dir / "summary.json", summary)
    write_json(
        output / "summary.json",
        {
            "cases": summaries,
            "case_count": len(summaries),
            "observation_attempts": 32,
            "outcome_delivery_attempts": 32,
            "scientific_credit": 0,
            "session_execution": False,
        },
    )
    write_json(
        output / "COMPLETED.json",
        {
            "fixed_matrix_complete": True,
            "freeze_sha256_after": verify_freeze(frozen),
            "calls_sha256": digest_bytes(raw_path.read_bytes()),
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output)

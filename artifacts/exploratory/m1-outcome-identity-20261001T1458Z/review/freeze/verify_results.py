"""Read-only verification of the fixed diagnostic raw rows and reproducibility."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from driver import canonical, digest_bytes, same_state, write_json


def check_run(root):
    matrix = json.loads((Path(__file__).parent / "matrix.json").read_text())
    rows = [
        json.loads(line) for line in (root / "calls.jsonl").read_text().splitlines()
    ]
    checks = {
        "64_call_records": len(rows) == 64,
        "32_observations": sum(r["operation"] == "observe" for r in rows) == 32,
        "32_outcome_deliveries": sum(r["operation"] == "outcome" for r in rows) == 32,
        "all_snapshots_serialization_neutral": all(
            r[side]["serialization_state_neutral"]
            and r[side]["repeated_save_payload_equal"]
            for r in rows
            for side in ("before", "after")
        ),
        "all_failed_calls_full_rollback": all(
            same_state(r["before"], r["after"])
            for r in rows
            if r["exception"] is not None
        ),
    }
    case_findings = []
    for case in matrix["cases"]:
        group = [r for r in rows if r["case_id"] == case["case_id"]]
        checks[case["case_id"] + ":inputs_exact"] = len(group) == 8 and all(
            r["input"] == step["input"] and r["operation"] == step["operation"]
            for r, step in zip(group, case["steps"], strict=True)
        )
        if len(group) != 8:
            continue
        probe, repeat, fourth = group[5], group[6], group[7]
        after = probe["after"]["inspection"]
        predicted_route = group[4]["output"]["route_token"]
        revision = probe["output"]
        routing = None if revision is None else revision["scope_revision"]["routing"]
        scoped_revision = (
            None if revision is None else revision["scope_revision"]["revision"]
        )
        checks[case["case_id"] + ":bootstrap_two_commits"] = (
            group[1]["sequence_delta"] == group[3]["sequence_delta"] == 1
        )
        if case["arm"] == "exact_reversal":
            checks[case["case_id"] + ":exact_reversal_contract"] = (
                probe["exception"] is not None
                and probe["exception"]["message"]
                == "scope revision rejected: identical_observation_conflict"
                and same_state(probe["before"], probe["after"])
                and repeat["exception"] is not None
                and same_state(repeat["before"], repeat["after"])
                and fourth["exception"] is not None
                and fourth["exception"]["message"]
                == "later outcome must resolve the pending event before another observe"
                and after["sequence"] == 2
            )
        else:
            checks[case["case_id"] + ":probe_commit_idempotent_repeat"] = (
                probe["exception"] is None
                and probe["sequence_delta"] == 1
                and repeat["exception"] is None
                and repeat["sequence_delta"] == 0
                and repeat["output"] == probe["output"]
                and same_state(repeat["before"], repeat["after"])
            )
        finding = {
            "case_id": case["case_id"],
            "context": case["context"],
            "arm": case["arm"],
            "predicted_route": predicted_route,
            "probe_route": None if routing is None else routing["token"],
            "route_unchanged": None
            if routing is None
            else routing["token"] == predicted_route,
            "scope_after_probe": scoped_revision,
            "hypotheses_after_probe": after["predictive"]["hypotheses"],
            "probe_error": None
            if probe["exception"] is None
            else probe["exception"]["message"],
            "fourth_action": fourth["output"],
            "fourth_error": None
            if fourth["exception"] is None
            else fourth["exception"]["message"],
            "committed_outcomes": sum(r["sequence_delta"] for r in group),
        }
        case_findings.append(finding)
    return {
        "checks": checks,
        "all_expected_checks_pass": all(checks.values()),
        "case_findings": case_findings,
        "raw_sha256": digest_bytes((root / "calls.jsonl").read_bytes()),
        "scientific_credit": 0,
        "session_executed": False,
    }


def compare_runs(first, second):
    left = {str(p.relative_to(first)): p for p in first.rglob("*") if p.is_file()}
    right = {str(p.relative_to(second)): p for p in second.rglob("*") if p.is_file()}
    differences = [
        name
        for name in sorted(set(left) | set(right))
        if name not in left
        or name not in right
        or left[name].read_bytes() != right[name].read_bytes()
    ]
    env_left = json.loads((first / "environment.json").read_text())
    env_right = json.loads((second / "environment.json").read_text())
    env_changed = [
        key
        for key in sorted(set(env_left) | set(env_right))
        if env_left.get(key) != env_right.get(key)
    ]
    return {
        "files_per_run": len(left),
        "same_file_inventory": set(left) == set(right),
        "byte_different_files": differences,
        "environment_differences": env_changed,
        "expected_hashseed_pair": [
            env_left["pythonhashseed"],
            env_right["pythonhashseed"],
        ],
        "reproducible_all_runtime_records_and_checkpoints": (
            set(left) == set(right)
            and differences == ["environment.json"]
            and env_changed == ["pythonhashseed"]
            and env_left["pythonhashseed"] == "1"
            and env_right["pythonhashseed"] == "37"
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run1", type=Path, required=True)
    parser.add_argument("--run37", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"run1": check_run(args.run1)}
    if args.run37:
        result["run37"] = check_run(args.run37)
        result["reproducibility"] = compare_runs(args.run1, args.run37)
    write_json(args.output, result)
    print(canonical(result))

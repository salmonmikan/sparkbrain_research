from __future__ import annotations

import json
from pathlib import Path
import subprocess


REQUIRED_TOP_LEVEL = {
    "schema",
    "status",
    "formal_identity",
    "formal_execution_authorized",
    "evidence_analyst_authority",
    "scientific_question",
    "candidate",
    "comparators",
    "observable_envelope",
    "held_out_construction",
    "interventions",
    "resource_contract",
    "training_calibration_tuning",
    "statistics",
    "decision_rule",
    "integrity_order",
    "authoritative_source_bindings",
    "formal_boundary",
}

FORBIDDEN_PHASE_PATHS = (
    "configs/experiments/lp01/execution_authority.json",
    ".github/workflows/lp01-formal-one-way.yml",
    "scripts/run_lp01_official.py",
    "scripts/preserve_lp01_boundary.py",
)


def _git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{path}"], text=True
    ).strip()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    contract_path = root / "configs/experiments/lp01/prospective_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    missing = sorted(REQUIRED_TOP_LEVEL - set(contract))
    if missing:
        raise AssertionError(f"LP01 contract missing required keys: {missing}")
    if contract["schema"] != "lp01-prospective-contract-v1":
        raise AssertionError("unexpected LP01 contract schema")
    if contract["formal_identity"] is not None:
        raise AssertionError("formal identity must remain null before fresh Analyst acceptance")
    if contract["formal_execution_authorized"] is not False:
        raise AssertionError("formal execution must remain unauthorized")

    boundary = contract["formal_boundary"]
    for key in ("STARTED", "official_TEST", "formal_preserve", "formal_scoring", "formal_evidence"):
        if boundary.get(key) != "FORBIDDEN_IN_THIS_PHASE":
            raise AssertionError(f"{key} must remain forbidden in LP01 specification phase")

    dev_seeds = set(contract["held_out_construction"]["dev_profile"]["history_seeds"])
    formal = contract["held_out_construction"]["planned_formal_profile"]
    formal_seeds = set(
        range(formal["history_seed_start"], formal["history_seed_start"] + formal["history_seed_count"])
    )
    if dev_seeds & formal_seeds:
        raise AssertionError("DEV and planned formal seed spaces overlap")
    if not formal["must_not_run_before_fresh_analyst_go"]:
        raise AssertionError("planned formal profile must be explicitly blocked")

    bindings = contract["authoritative_source_bindings"]
    for path, expected_blob in bindings.items():
        if path == "main_commit":
            continue
        actual = _git_blob(path)
        if actual != expected_blob:
            raise AssertionError(
                f"authoritative source binding drift for {path}: expected {expected_blob}, got {actual}"
            )

    for relative in FORBIDDEN_PHASE_PATHS:
        if (root / relative).exists():
            raise AssertionError(f"formal-only LP01 path exists during specification phase: {relative}")

    comparator_names = {row["name"] for row in contract["comparators"]}
    required_comparators = {
        "ExplicitParentTable",
        "RecentWindowState",
        "ProvenanceDestroyedControl",
    }
    if not required_comparators.issubset(comparator_names):
        raise AssertionError("LP01 comparator ladder is incomplete")

    print("LP01 prospective contract: PASS — specification boundary remains fail-closed")


if __name__ == "__main__":
    main()

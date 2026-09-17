#!/usr/bin/env python3
"""Fail-closed pre-START readiness checks for the pre-formal C19-R2 object."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from sparkbrain.v03_external_validation.c19_r2_protocol import (
    CONFIG_PATH,
    PARENT_V4_PACKAGE_COMMIT,
    STATE_ALPHABET,
    load_and_validate_contract,
)
from sparkbrain.v03_external_validation.c19_r2_state_tracker import readout, transition

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DIFF_PATHS = {
    ".github/workflows/c19-r2-prestart.yml",
    "configs/external_validation/c19_r2_fsa_state_tracker.json",
    "docs/research/c19_r2_fsa_state_tracker_preregistration.md",
    "scripts/check_c19_r2_prestart.py",
    "src/sparkbrain/v03_external_validation/c19_r2_protocol.py",
    "src/sparkbrain/v03_external_validation/c19_r2_scoring.py",
    "src/sparkbrain/v03_external_validation/c19_r2_source_map.py",
    "src/sparkbrain/v03_external_validation/c19_r2_state_tracker.py",
    "tests/test_c19_r2_state_tracker.py",
}
SOURCE_BLOB_PATHS = {
    "implementation_binding_blob": "src/sparkbrain/v03_external_validation/implementation_binding.py",
    "truth_free_adapter_blob": "src/sparkbrain/v03_external_validation/truth_free_adapter.py",
    "v4_protocol_blob": "src/sparkbrain/v03_external_validation/official_protocol_v4.py",
    "v4_scoring_blob": "src/sparkbrain/v03_external_validation/official_scoring_v4.py",
    "v4_execution_blob": "src/sparkbrain/v03_external_validation/official_execution_v4.py",
    "preserver_blob": "scripts/preserve_raw_boundary.py",
}


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def _verify_parent_and_diff() -> None:
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", PARENT_V4_PACKAGE_COMMIT, "HEAD"],
        cwd=ROOT,
        check=True,
    )
    changed = {
        line
        for line in _git("diff", "--name-only", f"{PARENT_V4_PACKAGE_COMMIT}..HEAD").splitlines()
        if line
    }
    unexpected = changed - ALLOWED_DIFF_PATHS
    if unexpected:
        raise RuntimeError(f"R2 branch modifies non-R2 paths: {sorted(unexpected)}")
    missing = ALLOWED_DIFF_PATHS - changed
    if missing:
        raise RuntimeError(f"R2 readiness package is incomplete: {sorted(missing)}")


def _verify_source_blobs() -> None:
    config = json.loads((ROOT / CONFIG_PATH).read_text(encoding="utf-8"))
    source = config["source_binding"]
    for key, relative_path in SOURCE_BLOB_PATHS.items():
        actual = _git("hash-object", relative_path)
        expected = source[key]
        if actual != expected:
            raise RuntimeError(
                f"R2 source binding drift for {relative_path}: {actual} != {expected}"
            )


def _verify_golden_transition_contract() -> None:
    if len(STATE_ALPHABET) != 7 or STATE_ALPHABET[0] != "RESET":
        raise RuntimeError("R2 state alphabet drift")
    cases = (
        ("RESET", {"a": 0.5, "b": 0.3, "c": 0.2}, "A_STRONG"),
        ("A_STRONG", {"a": 0.4, "b": 0.35, "c": 0.25}, "A_STRONG"),
        ("A_STRONG", {"a": 0.3, "b": 0.4, "c": 0.3}, "A_WEAK"),
        ("A_WEAK", {"a": 0.3, "b": 0.4, "c": 0.3}, "B_WEAK"),
        ("A_WEAK", {"a": 0.2, "b": 0.6, "c": 0.2}, "B_STRONG"),
    )
    for before, probabilities, expected in cases:
        actual = transition(before, probabilities)
        if actual != expected:
            raise RuntimeError(f"R2 transition drift: {before} -> {actual}, expected {expected}")
    if readout("C_WEAK") != "c":
        raise RuntimeError("R2 readout drift")


def main() -> None:
    validated = load_and_validate_contract(ROOT / CONFIG_PATH)
    if validated["formal_identity"] is not None:
        raise RuntimeError("R2 pre-formal package must not reserve a formal identity")
    if validated["official_execution_allowed"] is not False:
        raise RuntimeError("R2 pre-formal package must not authorize execution")
    _verify_parent_and_diff()
    _verify_source_blobs()
    _verify_golden_transition_contract()
    print(
        json.dumps(
            {
                "status": "R2_PRE_START_READY_FOR_ANALYST_REVIEW",
                "formal_identity": None,
                "official_execution_allowed": False,
                "parent_v4_package_commit": PARENT_V4_PACKAGE_COMMIT,
                "state_count": len(STATE_ALPHABET),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail-closed pre-START checks for the frozen C19-R2 science plus execution authority."""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Mapping
from pathlib import Path

from sparkbrain.v03_external_validation.c19_r2_protocol import (
    CONFIG_PATH,
    PARENT_V4_PACKAGE_COMMIT,
    STATE_ALPHABET,
    load_and_validate_contract,
)
from sparkbrain.v03_external_validation.c19_r2_state_tracker import readout, transition

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "configs/external_validation/c19_r2_execution_authority.json"
AUTHORIZED_IDENTITY = "c19-r2-fsa-state-tracker-official-v1"
AUTHORIZED_ANALYST = "719b9e74063e5e10f6226fd49f1835036ed75e5b"
SCIENTIFIC_PACKAGE = "5d5d171cf872baed7a636fd246ab36f3a91a6716"
ALLOWED_DIFF_PATHS = {
    ".github/workflows/c19-r2-one-way.yml",
    ".github/workflows/c19-r2-prestart.yml",
    "configs/external_validation/c19_r2_execution_authority.json",
    "configs/external_validation/c19_r2_fsa_state_tracker.json",
    "docs/research/c19_r2_fsa_state_tracker_preregistration.md",
    "scripts/check_c19_r2_prestart.py",
    "scripts/preserve_c19_r2_boundary.py",
    "scripts/run_c19_r2_official.py",
    "src/sparkbrain/v03_external_validation/c19_r2_protocol.py",
    "src/sparkbrain/v03_external_validation/c19_r2_scoring.py",
    "src/sparkbrain/v03_external_validation/c19_r2_source_map.py",
    "src/sparkbrain/v03_external_validation/c19_r2_state_tracker.py",
    "tests/test_c19_r2_state_tracker.py",
}
SOURCE_BLOB_PATHS = {
    "implementation_binding_blob": (
        "src/sparkbrain/v03_external_validation/implementation_binding.py"
    ),
    "truth_free_adapter_blob": (
        "src/sparkbrain/v03_external_validation/truth_free_adapter.py"
    ),
    "v4_protocol_blob": "src/sparkbrain/v03_external_validation/official_protocol_v4.py",
    "v4_scoring_blob": "src/sparkbrain/v03_external_validation/official_scoring_v4.py",
    "v4_execution_blob": (
        "src/sparkbrain/v03_external_validation/official_execution_v4.py"
    ),
    "preserver_blob": "scripts/preserve_raw_boundary.py",
}


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _verify_parent_and_diff() -> None:
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", PARENT_V4_PACKAGE_COMMIT, "HEAD"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", SCIENTIFIC_PACKAGE, "HEAD"],
        cwd=ROOT,
        check=True,
    )
    changed = {
        line
        for line in _git(
            "diff", "--name-only", f"{PARENT_V4_PACKAGE_COMMIT}..HEAD"
        ).splitlines()
        if line
    }
    unexpected = changed - ALLOWED_DIFF_PATHS
    if unexpected:
        raise RuntimeError(f"R2 branch modifies non-R2 paths: {sorted(unexpected)}")
    missing = ALLOWED_DIFF_PATHS - changed
    if missing:
        raise RuntimeError(f"R2 authority package is incomplete: {sorted(missing)}")


def _verify_source_blobs() -> None:
    config = json.loads((ROOT / CONFIG_PATH).read_text(encoding="utf-8"))
    source = config["source_binding"]
    for key, relative_path in SOURCE_BLOB_PATHS.items():
        actual = _git("hash-object", relative_path)
        expected = source[key]
        if actual != expected:
            raise RuntimeError(
                f"R2 source binding drift for {relative_path}: "
                f"{actual} != {expected}"
            )


def _verify_authority() -> dict[str, object]:
    authority = json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))
    if not isinstance(authority, Mapping):
        raise RuntimeError("R2 execution authority must be a mapping")
    expected = {
        "schema_version": "1",
        "state": "EXECUTION_AUTHORIZED",
        "evidence_analyst_commit": AUTHORIZED_ANALYST,
        "run_identity": AUTHORIZED_IDENTITY,
        "execution_limit": 1,
        "no_retry_after_started": True,
        "scientific_package_commit": SCIENTIFIC_PACKAGE,
        "started_ref": "control/c19-r2-fsa-state-tracker-started-v1-20260918",
        "preserve_ref": (
            "preserve/c19-r2-fsa-state-tracker-raw-"
            "c19-r2-fsa-state-tracker-official-v1"
        ),
        "evidence_tag": (
            "evidence/c19-r2-fsa-state-tracker-"
            "c19-r2-fsa-state-tracker-official-v1"
        ),
    }
    for key, value in expected.items():
        if authority.get(key) != value:
            raise RuntimeError(f"R2 execution authority drift: {key}")
    allowed = authority.get("allowed_authority_paths")
    if not isinstance(allowed, list) or set(allowed) != {
        ".github/workflows/c19-r2-one-way.yml",
        ".github/workflows/c19-r2-prestart.yml",
        "configs/external_validation/c19_r2_execution_authority.json",
        "scripts/check_c19_r2_prestart.py",
        "scripts/preserve_c19_r2_boundary.py",
        "scripts/run_c19_r2_official.py",
    }:
        raise RuntimeError("R2 authority path budget drift")
    for key in ("scientific_contract", "preregistration"):
        binding = authority.get(key)
        if not isinstance(binding, Mapping):
            raise RuntimeError(f"R2 authority missing {key}")
        if _git("hash-object", str(binding["path"])) != binding["blob_sha"]:
            raise RuntimeError(f"R2 authority frozen blob drift: {binding['path']}")
    sources = authority.get("scientific_sources")
    if not isinstance(sources, Mapping):
        raise RuntimeError("R2 authority scientific sources missing")
    for binding in sources.values():
        if not isinstance(binding, Mapping):
            raise RuntimeError("R2 authority scientific source malformed")
        if _git("hash-object", str(binding["path"])) != binding["blob_sha"]:
            raise RuntimeError(f"R2 authority source blob drift: {binding['path']}")
    if re.fullmatch(r"[0-9a-f]{40}", AUTHORIZED_ANALYST) is None:
        raise RuntimeError("R2 Analyst authority SHA malformed")
    return dict(authority)


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
            raise RuntimeError(
                f"R2 transition drift: {before} -> {actual}, expected {expected}"
            )
    if readout("C_WEAK") != "c":
        raise RuntimeError("R2 readout drift")


def main() -> None:
    frozen = load_and_validate_contract(ROOT / CONFIG_PATH)
    if (
        frozen["formal_identity"] is not None
        or frozen["official_execution_allowed"] is not False
    ):
        raise RuntimeError(
            "R2 frozen scientific contract must remain unchanged by authority packaging"
        )
    authority = _verify_authority()
    _verify_parent_and_diff()
    _verify_source_blobs()
    _verify_golden_transition_contract()
    print(
        json.dumps(
            {
                "status": "R2_PRE_START_AUTHORITY_READY",
                "frozen_science_formal_identity": None,
                "authorized_identity": authority["run_identity"],
                "evidence_analyst_commit": authority["evidence_analyst_commit"],
                "official_execution_allowed": True,
                "parent_v4_package_commit": PARENT_V4_PACKAGE_COMMIT,
                "scientific_package_commit": SCIENTIFIC_PACKAGE,
                "state_count": len(STATE_ALPHABET),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

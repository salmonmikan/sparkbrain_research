#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs/experiments/ni01/preformal_contract.json"
AUTHORITY_PATH = ROOT / "configs/experiments/ni01/execution_authority.json"

EXPECTED_ANALYST = "d3626617c3b054afd726e468682aaa02d613bca0"
EXPECTED_SCIENCE_HEAD = "2664951b65dd18883d3d80862e80b86ac66cf24f"
EXPECTED_IDENTITY = "ni01-no-ignition-selective-prediction-official-v1"
EXPECTED_PROTOCOL = "ni01-no-ignition-selective-prediction-protocol-v1"
EXPECTED_CONTRACT_BLOB = "3dc90b08f85e0e7c459e0c17e86ab338901fd4c6"
EXPECTED_SCORER_BLOB = "d3b3565a08277e6a94ef9be1e5bd13e86265f8f2"
EXPECTED_RUNNER_BLOB = "d1602b22bacec1b4e8d2166bd0c184382e632d7e"
EXPECTED_PRESERVER_BLOB = "390816f9d69604adc0ce3fbf21be93dd916256fd"
EXPECTED_SOURCE_BLOBS = {
    "src/sparkbrain/tasks/worlds.py": "2478fba19d7276ebe30ec8f5811bf6d7b7414779",
    "src/sparkbrain/evaluation/runner.py": "90543b184c64981802560601b85edcdee4583a35",
    "src/sparkbrain/evaluation/ablations.py": (
        "caa6a1c63fedc2222aa2e6ce708b66668943e8dd"
    ),
    "configs/experiments/phase1/main.json": "0134abeaf3d0551edeeb890502ffebe2c27867b0",
    "src/sparkbrain/evaluation/ni01.py": EXPECTED_SCORER_BLOB,
}


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"expected JSON object: {path}")
    return value


def _blob(path: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    contract = _read(CONTRACT_PATH)
    authority = _read(AUTHORITY_PATH)

    if authority["status"] != "PRE_START_AUTHORIZED_CONDITIONAL":
        raise SystemExit("NI01 authority status mismatch")
    if authority["evidence_analyst_commit"] != EXPECTED_ANALYST:
        raise SystemExit("NI01 analyst authority mismatch")
    if authority["reviewed_scientific_head"] != EXPECTED_SCIENCE_HEAD:
        raise SystemExit("NI01 reviewed scientific head mismatch")
    if authority["formal_identity"] != EXPECTED_IDENTITY:
        raise SystemExit("NI01 identity mismatch")
    if authority["protocol_id"] != EXPECTED_PROTOCOL:
        raise SystemExit("NI01 protocol mismatch")
    if authority["scientific_contract_immutable"] is not True:
        raise SystemExit("NI01 scientific contract must remain immutable")
    if authority["no_retry"] is not True:
        raise SystemExit("NI01 no-retry invariant changed")
    if authority["formal_contract_git_blob"] != EXPECTED_CONTRACT_BLOB:
        raise SystemExit("NI01 contract blob authority mismatch")
    if authority["ni01_scorer_git_blob"] != EXPECTED_SCORER_BLOB:
        raise SystemExit("NI01 scorer blob authority mismatch")
    if authority["official_runner_git_blob"] != EXPECTED_RUNNER_BLOB:
        raise SystemExit("NI01 official runner blob authority mismatch")
    if authority["preserver_git_blob"] != EXPECTED_PRESERVER_BLOB:
        raise SystemExit("NI01 preserver blob authority mismatch")

    if contract["status"] != "PREFORMAL_REVIEW_ONLY":
        raise SystemExit("NI01 frozen contract status changed")
    if contract["formal_execution_authorized"] is not False:
        raise SystemExit(
            "scientific contract must not be rewritten for execution authority"
        )
    if contract["protocol_id"] != EXPECTED_PROTOCOL:
        raise SystemExit("NI01 frozen protocol changed")
    plan = contract["formal_identity_plan"]
    if plan["identity"] != EXPECTED_IDENTITY or plan["state"] != "UNRESERVED":
        raise SystemExit("NI01 frozen identity plan changed")
    contract_blob = _blob("configs/experiments/ni01/preformal_contract.json")
    if contract_blob != EXPECTED_CONTRACT_BLOB:
        raise SystemExit("NI01 formal contract blob drift")

    if _blob("scripts/run_ni01_official.py") != EXPECTED_RUNNER_BLOB:
        raise SystemExit("NI01 official runner blob drift")
    if _blob("scripts/preserve_ni01_boundary.py") != EXPECTED_PRESERVER_BLOB:
        raise SystemExit("NI01 preserver blob drift")

    actual = {path: _blob(path) for path in EXPECTED_SOURCE_BLOBS}
    if actual != EXPECTED_SOURCE_BLOBS:
        raise SystemExit(f"NI01 source binding drift: {actual}")

    if contract["source_binding"]["ni01_scorer_blob"] != EXPECTED_SCORER_BLOB:
        raise SystemExit("NI01 scorer contract binding drift")
    if contract["inputs"]["test"]["total_episodes"] != 1536:
        raise SystemExit("NI01 TEST inventory changed")
    if contract["raw_contract"]["expected_test_step_count"] != 46080:
        raise SystemExit("NI01 TEST raw cardinality changed")
    if contract["statistics"]["resamples"] != 10000:
        raise SystemExit("NI01 bootstrap count changed")
    if contract["statistics"]["bootstrap_seed"] != 74017:
        raise SystemExit("NI01 bootstrap seed changed")

    print("NI01 execution authority: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

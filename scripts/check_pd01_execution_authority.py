#!/usr/bin/env python3
"""Fail-closed admission checks for the authorized PD0.1 one-way package."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "research" / "pd01" / "execution_authority.json"
CONTRACT = ROOT / "research" / "pd01" / "formal_contract.json"
IMPLEMENTATION = ROOT / "src" / "sparkbrain" / "external_validation" / "fading_memory.py"
EXPECTED_ANALYST = "91a05bad6d130f89975e776960a1d25d764fba32"
EXPECTED_REVIEWED_HEAD = "ea2a8b4a5f244d601782ecb302760c49ee27e8c1"
EXPECTED_CONTRACT_BLOB = "0ce03b01baf41a0c77c513835b1c6063e47b2614"
EXPECTED_IMPLEMENTATION_BLOB = "16bbfb6ed57d6c9701e8437360692b62e7c36915"
EXPECTED_IDENTITY = "pd01-long-history-fading-memory-official-v1"


def _git_blob(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert authority["status"] == "PRE_START_AUTHORIZED_CONDITIONAL"
    assert authority["evidence_analyst_commit"] == EXPECTED_ANALYST
    assert authority["reviewed_scientific_head"] == EXPECTED_REVIEWED_HEAD
    assert authority["formal_contract_git_blob"] == EXPECTED_CONTRACT_BLOB
    assert authority["implementation_git_blob"] == EXPECTED_IMPLEMENTATION_BLOB
    assert authority["formal_identity"] == EXPECTED_IDENTITY
    assert authority["scientific_contract_immutable"] is True
    assert authority["no_retry"] is True
    assert _git_blob(CONTRACT) == EXPECTED_CONTRACT_BLOB
    assert _git_blob(IMPLEMENTATION) == EXPECTED_IMPLEMENTATION_BLOB

    # The reviewed science remains a review-only object. Execution permission lives only
    # in this science-invariant authority envelope so the scientific contract cannot drift.
    assert contract["status"] == "FORMAL_CONTRACT_PROPOSAL_REVIEW_ONLY"
    assert contract["formal_identity_proposed"] == EXPECTED_IDENTITY
    assert contract["formal_identity_reserved"] is False
    assert contract["started_allowed"] is False
    assert contract["official_test_access_allowed"] is False
    assert contract["official_test_target_access_allowed"] is False
    assert contract["one_way_execution_allowed"] is False
    assert contract["source_binding"]["pd01_implementation_git_blob"] == EXPECTED_IMPLEMENTATION_BLOB
    assert contract["runtime_binding"]["python"] == "3.11.16"
    assert contract["inventory"]["test_histories"] == 1024
    assert contract["inventory"]["test_raw_prediction_rows"] == 2048
    assert contract["primary_scoring"]["primary_lags"] == [64, 128]
    assert contract["primary_scoring"]["bootstrap_resamples"] == 10_000
    assert contract["primary_scoring"]["bootstrap_seed"] == 19_901

    namespaces = authority["namespaces"]
    assert namespaces["started_branch"].startswith("control/pd01-")
    assert namespaces["preserve_branch"].startswith("preserve/pd01-")
    assert namespaces["evidence_tag"].startswith("evidence/pd01-")
    print("PD0.1 execution authority: PRE_START_AUTHORIZED_CONDITIONAL")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.release import sha256_file

ROOT = Path(__file__).resolve().parents[1]

SCIENTIFIC_HASHES = {
    "artifacts/external_validation/c06-final-official/belief_r_metrics.json": (
        "2bdd0d88a48c5ed7c02dd7e3f55ceb56520ba42c0731e9c23aa416b09d0c7f43"
    ),
    "artifacts/phase3/structural-plasticity-v1/main/acceptance-matrix.json": (
        "ad6cac143f6d95ce128e982a31542c833b6acfae3e516d4987ba384271e10da6"
    ),
    "artifacts/phase3/structural-plasticity-v1/main/summary.json": (
        "8e4e689be66be55b2bdc7418e55c57120b1692cfd0f15e726fe51eeef0b84ae6"
    ),
    "artifacts/release/primary_subset.json": (
        "8c069b8d679575dc3856ee3267d356395f6be7c2da72838d2eec3af65969c391"
    ),
    "docs/CLAIMS_REGISTER.md": (
        "5562a4e04ec99ede1f4c8ea15cf1d5e4db306c6b7e71a838eaf90c14f188cc62"
    ),
}


def test_c06_c08_primary_subset_and_claim_grades_remain_frozen() -> None:
    assert {relative: sha256_file(ROOT / relative) for relative in SCIENTIFIC_HASHES} == (
        SCIENTIFIC_HASHES
    )
    subset = json.loads(
        (ROOT / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )
    assert subset["full_evaluation"] is False
    claims = (ROOT / "docs/CLAIMS_REGISTER.md").read_text(encoding="utf-8")
    assert "| CL-007 |" in claims and "| E0 |" in claims
    assert "| CL-008 |" in claims and claims.count("| E0 |") >= 2

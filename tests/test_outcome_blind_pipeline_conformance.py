from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from outcome_blind_fixed_scorer import score_preserved_raw  # noqa: E402
from outcome_blind_pipeline_conformance import run_conformance  # noqa: E402


CONTRACT_PATH = REPO_ROOT / "analysis/orchestrator/r39_pipeline_conformance/contract.json"


def test_synthetic_four_stage_pipeline_conforms(tmp_path: Path) -> None:
    result = run_conformance(
        repo_root=REPO_ROOT,
        contract_path=CONTRACT_PATH,
        output_root=tmp_path,
    )
    assert result["status"] == "PASS"

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    raw_path = Path(result["preserved_raw"])
    raw_manifest = json.loads(Path(result["raw_manifest"]).read_text(encoding="utf-8"))
    scored_manifest = json.loads(Path(result["scored_manifest"]).read_text(encoding="utf-8"))

    assert raw_manifest["stage"] == "DURABLE_RAW_ONLY_PRESERVE_DIGEST"
    assert scored_manifest["stage"] == "SCORED_PRESERVE_LINEAGE"
    assert raw_manifest["raw_sha256"] == scored_manifest["raw_sha256"]
    observed_raw_sha256 = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    assert scored_manifest["raw_sha256"] == observed_raw_sha256
    assert scored_manifest["scorer_sha256"] == contract["frozen_sha256"][contract["scorer_path"]]


def test_scorer_fails_closed_on_mutated_preserved_raw(tmp_path: Path) -> None:
    result = run_conformance(
        repo_root=REPO_ROOT,
        contract_path=CONTRACT_PATH,
        output_root=tmp_path / "clean",
    )
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    original = Path(result["preserved_raw"])
    mutated = tmp_path / "mutated-raw.json"
    shutil.copyfile(original, mutated)
    mutated.write_bytes(mutated.read_bytes() + b" ")

    with pytest.raises(ValueError, match="preserved raw digest mismatch"):
        score_preserved_raw(
            preserved_raw_path=mutated,
            expected_raw_sha256=result["raw_sha256"],
            plan_path=REPO_ROOT / contract["analysis_plan_path"],
        )

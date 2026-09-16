from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BINDING_PATH = ROOT / "docs" / "V061_A01_FAMILY_B_GEN1_EXECUTION_BINDING.json"


def _git_blob(path: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def test_execution_binding_is_exact_and_does_not_self_admit() -> None:
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    assert binding["schema"] == "v061-a01-family-b-gen1-execution-binding-v1"
    assert binding["candidate_id"] == "a01-family-b-distributed-field-trace-gen1-v1"
    assert binding["execution_admitted"] is False
    assert binding["one_way_execution_allowed"] is False
    assert binding["same_identity_rerun_allowed"] is False
    assert binding["implementation_head_sha"] == "3939df3004b61adef337c547144ffb1cdcb04f49"

    locked = binding["locked_files"]
    assert locked
    for path, expected_blob in locked.items():
        assert _git_blob(path) == expected_blob


def test_execution_binding_reserves_exact_one_way_refs_without_creating_them() -> None:
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    assert binding["expected_one_way_refs"] == {
        "source_freeze_tag": "freeze/a01-family-b-gen1-source-20260916",
        "started_ref": "control/a01-family-b-gen1-started-20260916",
        "owner_ref": "control/a01-family-b-gen1-owner-20260916",
        "acquisition_ref": "control/a01-family-b-gen1-acquire-20260916",
        "raw_recovery_ref": "preserve/a01-family-b-gen1-recovery-20260916",
        "raw_evidence_tag": "evidence/a01-family-b-gen1-raw-20260916",
        "scored_evidence_tag": "evidence/a01-family-b-gen1-scored-20260916",
        "terminal_failure_tag": "evidence/a01-family-b-gen1-terminal-failure-20260916",
    }

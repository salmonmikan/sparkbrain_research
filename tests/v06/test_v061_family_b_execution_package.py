from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import run_v061_a01_family_b_gen1 as runner
from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    BELIEF_STATE_NULL_ID,
    FAMILY_B_GEN1_PROPOSAL,
)

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "research" / "v061_a01" / "family_b_gen1_execution_input.json"
RUNTIME_PATH = ROOT / "research" / "v061_a01" / "family_b_gen1_runtime.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "v061-a01-family-b-gen1-execute-once.yml"


def test_execution_input_is_prospective_and_matches_bound_ids_without_running_it() -> None:
    payload = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    runner._validate_input(payload)
    assert payload["candidate_id"] == FAMILY_B_GEN1_PROPOSAL.proposal_id
    assert payload["required_null_ids"]["belief_state"] == BELIEF_STATE_NULL_ID
    assert payload["scientific_input_id"] == "v061-a01-family-b-gen1-scientific-input-v1"
    assert payload["lineage_swap_permutation"] == [2, 3, 0, 1]


def test_runtime_forbids_same_identity_rerun_and_requires_admission() -> None:
    runtime = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    assert runtime["same_identity_rerun_allowed"] is False
    assert runtime["execution_admission_required"] is True
    assert runtime["held_out_execution_allowed"] is False
    assert runtime["formal_execution_allowed"] is False


def test_resource_accounting_includes_null_ladder_generation_update_budget() -> None:
    assert "generation_update_budget" in runner.RESOURCE_KEYS
    assert runner.GENERATION_UPDATE_BUDGET == 9


def test_acquisition_guard_fails_closed_outside_exact_github_actions_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    with pytest.raises(RuntimeError, match="acquire requires GitHub Actions"):
        runner._claim_acquisition("0" * 40)


def test_execution_workflow_cannot_run_from_package_commits_or_manual_dispatch() -> None:
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert 'control/a01-family-b-gen1-started-20260916' in workflow
    assert "workflow_dispatch" not in workflow
    assert "Preserve raw before any scoring read" in workflow
    assert "Independently verify preserved raw bundle" in workflow
    assert "Score exactly once from independently verified preserved raw evidence" in workflow
    assert workflow.count("run_v061_a01_family_b_gen1.py score") == 1
    assert "without rescoring" in workflow

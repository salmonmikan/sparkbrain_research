from __future__ import annotations

import ast
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryPhase
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_execution_seal import (
    build_freeze_record,
    require_execution_seal,
)

_UNSEALED_CAPABILITY_PATHS = (
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_common.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_controls.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_comparators.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_matrix.py",
    "tests/v06/test_confirmatory_heldout_adapters.py",
)
_CAPABILITY_FUNCTION_NAMES = {
    "run_condition",
    "run_execution",
    "run_matrix",
    "score_confirmatory_results",
    "score_strict_confirmatory_results",
}


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def test_active_protocol_branch_contains_no_unsealed_capability_entrypoint() -> None:
    root = _repository_root()
    assert all(not (root / path).exists() for path in _UNSEALED_CAPABILITY_PATHS)


def test_active_heldout_modules_are_schema_only() -> None:
    evaluation = _repository_root() / "src" / "sparkbrain" / "evaluation"
    for path in sorted(evaluation.glob("v06_confirmatory_heldout*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        function_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        called_names = {
            name
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            for name in (_call_name(node),)
            if name is not None
        }
        assert _CAPABILITY_FUNCTION_NAMES.isdisjoint(function_names), path
        assert _CAPABILITY_FUNCTION_NAMES.isdisjoint(called_names), path
        assert "ConfirmatoryResultRecord(" not in path.read_text(encoding="utf-8")


def test_current_confirmatory_manifest_remains_fully_sealed() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    assert manifest.code_ref == "UNFROZEN"
    assert all(not row.adapter_ready for row in manifest.conditions)
    record = build_freeze_record(manifest, approval="not-yet-approved")
    with pytest.raises(RuntimeError, match="remains prohibited"):
        require_execution_seal(manifest, record)


def test_no_confirmatory_result_or_freeze_artifact_is_committed() -> None:
    root = _repository_root()
    forbidden = (
        "artifacts/v06/confirmatory/freeze_record.json",
        "artifacts/v06/confirmatory/results.jsonl",
        "artifacts/v06/confirmatory/resources.jsonl",
        "artifacts/v06/confirmatory/summary.json",
        "artifacts/v06/confirmatory/checksums.json",
    )
    assert all(not (root / path).exists() for path in forbidden)

from __future__ import annotations

import ast
from pathlib import Path

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryPhase,
    assess_confirmatory_readiness,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)

_FORBIDDEN_EXECUTION_PATHS = (
    "src/sparkbrain/evaluation/v06_confirmatory_execute.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_matrix.py",
    "tests/v06/test_confirmatory_heldout_adapters.py",
)
_SCHEMA_ONLY_MODULES = (
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_dryrun_contract.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_preflight.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary_dryrun.py",
)
_STAGING_CAPABILITY_MODULES = (
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_common.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_controls.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_comparators.py",
)
_CAPABILITY_FUNCTION_NAMES = {
    "run_condition",
    "run_execution",
    "run_matrix",
    "score_confirmatory_results",
    "score_strict_confirmatory_results",
}
_FORBIDDEN_CANDIDATE_IMPORT_NAMES = {
    "HELDOUT_SEEDS",
    "WORLD_GENERATION_ID",
    "build_heldout_world_grid",
    "heldout_world_parameters",
}


def _repository_root() -> Path:
    return Path(__file__).parents[2]


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def test_staging_branch_contains_no_dispatcher_or_candidate_execution_test() -> None:
    root = _repository_root()
    assert all(not (root / path).exists() for path in _FORBIDDEN_EXECUTION_PATHS)


def test_schema_only_modules_remain_schema_only() -> None:
    root = _repository_root()
    for relative_path in _SCHEMA_ONLY_MODULES:
        path = root / relative_path
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


def test_staging_capability_modules_cannot_construct_candidate_worlds() -> None:
    root = _repository_root()
    for relative_path in _STAGING_CAPABILITY_MODULES:
        path = root / relative_path
        assert path.exists(), path
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }
        assert _FORBIDDEN_CANDIDATE_IMPORT_NAMES.isdisjoint(imported_names), path


def test_current_confirmatory_manifest_remains_unfrozen_and_unready() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert manifest.code_ref == "UNFROZEN"
    assert all(not row.adapter_ready for row in manifest.conditions)
    assert readiness.code_ref_frozen is False
    assert readiness.ready is False


def test_no_confirmatory_result_or_freeze_artifact_is_committed() -> None:
    root = _repository_root()
    forbidden = (
        "artifacts/v06/confirmatory/control/freeze_record.json",
        "artifacts/v06/confirmatory/control/environment_lock.json",
        "artifacts/v06/confirmatory/control/STARTED.json",
        "artifacts/v06/confirmatory/raw",
        "artifacts/v06/confirmatory/analysis",
    )
    assert all(not (root / path).exists() for path in forbidden)

from __future__ import annotations

import ast
from pathlib import Path

from sparkbrain.evaluation.v06_confirmatory_normalized_resource_v2 import (
    ResourceDecisionPolicyV2,
)


def _root() -> Path:
    return Path(__file__).parents[2]


def _tree(relative_path: str) -> ast.Module:
    return ast.parse((_root() / relative_path).read_text(encoding="utf-8"))


def _top_level_import_modules(tree: ast.Module) -> set[str]:
    modules: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            modules.add(node.module or "")
        elif isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
    return modules


def _call_lines(tree: ast.AST, function_name: str) -> tuple[int, ...]:
    return tuple(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and (
            isinstance(node.func, ast.Name)
            and node.func.id == function_name
            or isinstance(node.func, ast.Attribute)
            and node.func.attr == function_name
        )
    )


def _import_lines(tree: ast.AST, suffix: str) -> tuple[int, ...]:
    return tuple(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and (node.module or "").endswith(suffix)
    )


def test_candidate_runner_has_no_top_level_capability_or_world_import() -> None:
    tree = _tree(
        "src/sparkbrain/evaluation/v06_confirmatory_execute_external_v2.py"
    )
    modules = _top_level_import_modules(tree)
    assert not any(module.endswith("v06_confirmatory_heldout_spec") for module in modules)
    assert not any(module.endswith("v06_confirmatory_adapter_registry_v2") for module in modules)
    assert not any(module.endswith("v06_confirmatory_scoring") for module in modules)


def test_gate_and_one_way_claim_precede_candidate_imports() -> None:
    tree = _tree(
        "src/sparkbrain/evaluation/v06_confirmatory_execute_external_v2.py"
    )
    gate_lines = _call_lines(tree, "require_external_launch_gate_v2")
    claim_lines = _call_lines(tree, "claim_external_one_way_execution_v2")
    world_imports = _import_lines(tree, "v06_confirmatory_heldout_spec")
    adapter_imports = _import_lines(tree, "v06_confirmatory_adapter_registry_v2")
    assert len(gate_lines) == len(claim_lines) == 1
    assert len(world_imports) == len(adapter_imports) == 1
    assert gate_lines[0] < claim_lines[0] < world_imports[0]
    assert gate_lines[0] < claim_lines[0] < adapter_imports[0]


def test_raw_writer_and_runner_do_not_import_scoring() -> None:
    for relative_path in (
        "src/sparkbrain/evaluation/v06_confirmatory_external_raw_store.py",
        "src/sparkbrain/evaluation/v06_confirmatory_execute_external_v2.py",
    ):
        source = (_root() / relative_path).read_text(encoding="utf-8")
        assert "score_strict_confirmatory_results" not in source
        assert "v06_confirmatory_scoring" not in source


def test_scorer_does_not_import_candidate_world_or_capability_adapter() -> None:
    tree = _tree(
        "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py"
    )
    modules = _top_level_import_modules(tree)
    assert not any(module.endswith("v06_confirmatory_heldout_spec") for module in modules)
    assert not any(module.endswith("v06_confirmatory_adapter_registry_v2") for module in modules)
    source = (
        _root()
        / "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py"
    ).read_text(encoding="utf-8")
    assert "run_registered_adapter_v2" not in source
    assert "build_heldout_world_grid" not in source


def test_scorer_rebuilds_the_frozen_candidate_manifest() -> None:
    source = (
        _root()
        / "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py"
    ).read_text(encoding="utf-8")
    assert "build_candidate_manifest" in source
    assert "build_current_confirmatory_manifest" not in source
    assert "candidate manifest differs from frozen bundle" in source


def test_raw_verification_precedes_strict_scoring_and_is_repeated() -> None:
    tree = _tree(
        "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py"
    )
    verification_lines = _call_lines(tree, "verify_external_raw_evidence_v2")
    scoring_lines = _call_lines(tree, "score_strict_confirmatory_results")
    assert len(verification_lines) == 3
    assert len(scoring_lines) == 1
    assert verification_lines[0] < scoring_lines[0] < verification_lines[1]
    assert scoring_lines[0] < verification_lines[2]


def test_resource_efficiency_is_descriptive_only_in_final_pipeline() -> None:
    policy = ResourceDecisionPolicyV2()
    policy.validate()
    assert policy.efficiency_affects_capability_pass_fail is False
    scorer_source = (
        _root()
        / "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py"
    ).read_text(encoding="utf-8")
    assert '"efficiency_affects_capability_pass_fail": False' in scorer_source
    assert '"decision_use": "descriptive-only"' in scorer_source

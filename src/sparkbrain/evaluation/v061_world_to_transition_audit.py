from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ModuleDependencyEvidence:
    relative_path: str
    imported_modules: tuple[str, ...]
    referenced_names: tuple[str, ...]
    defined_functions: tuple[str, ...]
    called_attributes: tuple[str, ...]
    function_calls: tuple[tuple[str, tuple[str, ...]], ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class WorldToTransitionAudit:
    modules: tuple[ModuleDependencyEvidence, ...]
    local_transition_learning_exists: bool
    relation_modules_reference_local_expectation: bool
    relation_modules_call_transition_learning: bool
    primary_relation_functions_call_transition_learning: bool
    direct_world_to_transition_dependency_present: bool
    missing_world_to_transition_path_confirmed: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "modules": [row.state_dict() for row in self.modules],
        }


def _call_attribute(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    if isinstance(node.func, ast.Name):
        return node.func.id
    return None


def _module_evidence(root: Path, relative_path: str) -> ModuleDependencyEvidence:
    path = root / relative_path
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    imports = []
    names = set()
    defined_functions = set()
    calls = set()
    function_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defined_functions.add(node.name)
        elif isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Call):
            called = _call_attribute(node)
            if called is not None:
                calls.add(called)
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        row_calls = {
            called
            for child in ast.walk(node)
            if isinstance(child, ast.Call)
            for called in (_call_attribute(child),)
            if called is not None
        }
        function_calls.append((node.name, tuple(sorted(row_calls))))
    return ModuleDependencyEvidence(
        relative_path=relative_path,
        imported_modules=tuple(sorted(set(imports))),
        referenced_names=tuple(sorted(names)),
        defined_functions=tuple(sorted(defined_functions)),
        called_attributes=tuple(sorted(calls)),
        function_calls=tuple(sorted(function_calls)),
    )


def _calls_in_functions(
    evidence: ModuleDependencyEvidence,
    *,
    name_fragments: tuple[str, ...],
) -> set[str]:
    return {
        called
        for function_name, calls in evidence.function_calls
        if any(fragment in function_name for fragment in name_fragments)
        for called in calls
    }


def audit_world_to_transition_dependency(
    repository_root: Path,
) -> WorldToTransitionAudit:
    """Inspect architecture dependencies without executing a candidate world."""

    paths = (
        "src/sparkbrain/v06/local_expectation.py",
        "src/sparkbrain/v06/consistency.py",
        "src/sparkbrain/v06/relation_reentry.py",
        "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py",
    )
    modules = tuple(_module_evidence(repository_root, path) for path in paths)
    by_path = {row.relative_path: row for row in modules}
    local = by_path["src/sparkbrain/v06/local_expectation.py"]
    consistency = by_path["src/sparkbrain/v06/consistency.py"]
    reentry = by_path["src/sparkbrain/v06/relation_reentry.py"]
    primary = by_path[
        "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py"
    ]

    transition_learning_call = "observe_external_transition"
    local_learning_exists = transition_learning_call in local.defined_functions
    relation_rows = (consistency, reentry)
    relation_references_local = any(
        any("local_expectation" in module for module in row.imported_modules)
        or "LocalTemporalExpectation" in row.referenced_names
        for row in relation_rows
    )
    relation_calls_learning = any(
        transition_learning_call in row.called_attributes for row in relation_rows
    )
    primary_relation_calls = _calls_in_functions(
        primary,
        name_fragments=("relation", "reentry", "boundary_episode"),
    )
    primary_relation_learning = transition_learning_call in primary_relation_calls
    direct_dependency = (
        relation_references_local
        or relation_calls_learning
        or primary_relation_learning
    )
    return WorldToTransitionAudit(
        modules=modules,
        local_transition_learning_exists=local_learning_exists,
        relation_modules_reference_local_expectation=relation_references_local,
        relation_modules_call_transition_learning=relation_calls_learning,
        primary_relation_functions_call_transition_learning=(
            primary_relation_learning
        ),
        direct_world_to_transition_dependency_present=direct_dependency,
        missing_world_to_transition_path_confirmed=(
            local_learning_exists and not direct_dependency
        ),
    )

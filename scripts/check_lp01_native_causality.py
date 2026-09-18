from __future__ import annotations

import ast
import textwrap
from pathlib import Path


FORBIDDEN_CAUSAL_TOKENS = {"identities", "parents", "tombstones", "lineage"}


def _function_source(path: Path, class_name: str, function_name: str) -> str:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if (
                    isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and child.name == function_name
                ):
                    return ast.get_source_segment(text, child) or ""
    raise AssertionError(f"missing {class_name}.{function_name} in {path}")


def _referenced_identifiers(source: str) -> set[str]:
    tree = ast.parse(textwrap.dedent(source))
    names = {node.id.lower() for node in ast.walk(tree) if isinstance(node, ast.Name)}
    attrs = {node.attr.lower() for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    return names | attrs


def _assert_no_lineage_dependency(path: Path, class_name: str, function_name: str) -> None:
    source = _function_source(path, class_name, function_name)
    identifiers = _referenced_identifiers(source)
    found = sorted(FORBIDDEN_CAUSAL_TOKENS & identifiers)
    if found:
        raise AssertionError(
            f"{class_name}.{function_name} unexpectedly depends on lineage metadata: {found}"
        )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    model = root / "src/sparkbrain/structural/model.py"
    backend = root / "src/sparkbrain/structural/backend.py"
    controller = root / "src/sparkbrain/structural/controller.py"

    _assert_no_lineage_dependency(model, "StructuralSparseModel", "forward_step")
    _assert_no_lineage_dependency(backend, "StructuralBrainBackend", "run")
    _assert_no_lineage_dependency(backend, "StructuralBrainBackend", "_consume_structural")
    _assert_no_lineage_dependency(backend, "StructuralBrainBackend", "apply_reward_eligibility")
    _assert_no_lineage_dependency(controller, "StructuralController", "discover")
    _assert_no_lineage_dependency(controller, "StructuralController", "candidate_group")

    inspect_source = _function_source(backend, "StructuralBrainBackend", "inspect_snapshot")
    if "controller.identities" not in inspect_source:
        raise AssertionError("lineage identity metadata is no longer exposed by inspect_snapshot")

    state_source = _function_source(controller, "StructuralController", "state_dict")
    if '"identities"' not in state_source or '"tombstones"' not in state_source:
        raise AssertionError("controller no longer persists identity/tombstone provenance")

    print(
        "LP01 native source audit: PASS — current lineage metadata is persisted/inspectable "
        "but is not read by forward decision, structural consumption, reward eligibility, "
        "discovery, or candidate-group selection paths."
    )


if __name__ == "__main__":
    main()

"""Reserved-fixture regression; no comparator or formal package execution."""
from __future__ import annotations

import ast
import hashlib
import json
import unittest
from pathlib import Path
from typing import Any

from sparkbrain.comparison.cx01.formal_identifiability import audit_formal_grid_identifiability
from sparkbrain.comparison.cx01.formal_revision import build_revised_formal_world
from sparkbrain.comparison.cx01.formal_worlds import audit_formal_grid_structure
from sparkbrain.comparison.cx01.structural_components import audit_formal_grid_components
from sparkbrain.comparison.cx01.worlds import CX01Family


def _namespace() -> tuple[dict[str, Any], list[ast.stmt]]:
    # Execute only the helper and audit assignment/guard, never package code.
    path = Path(__file__).resolve().parents[2] / "src/sparkbrain/comparison/cx01/prepare.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_audit_envelope")
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "prepare_outcome_blind_bundle")
    index = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "audits" for t in n.targets))
    namespace: dict[str, Any] = {"Any": Any}
    exec(compile(ast.Module(body=[helper], type_ignores=[]), str(path), "exec"), namespace)
    return namespace, function.body[index:index + 2]


def test_envelope_rejects_explicit_non_success() -> None:
    namespace, _ = _namespace()
    for report in [{"passed": False}, {"passed": None}, {"passed": 1}]:
        with unittest.TestCase().assertRaisesRegex(RuntimeError, "explicitly did not pass"):
            namespace["_audit_envelope"](report)


def test_reserved_sixty_world_audits_pass_without_report_mutation() -> None:
    namespace, statements = _namespace()
    worlds = tuple(build_revised_formal_world("cx01-fixture-prepare-001", family, seed)
                   for family in CX01Family for seed in range(5000, 5010))
    auditors = {
        "audit_formal_grid_structure": audit_formal_grid_structure,
        "audit_formal_grid_components": audit_formal_grid_components,
        "audit_formal_grid_identifiability": audit_formal_grid_identifiability,
    }
    reports = [fn(worlds) for fn in auditors.values()]
    before = [hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest() for r in reports]
    namespace.update(worlds=worlds, **auditors)
    exec(compile(ast.Module(body=statements, type_ignores=[]), "audit-guard", "exec"), namespace)
    assert len(worlds) == 60
    assert all(row["passed"] is True for row in namespace["audits"].values())
    for envelope, report, digest in zip(namespace["audits"].values(), reports, before, strict=True):
        assert envelope["report"] == report
        assert hashlib.sha256(json.dumps(envelope["report"], sort_keys=True).encode()).hexdigest() == digest
    path = Path(__file__).resolve().parents[2] / "src/sparkbrain/comparison/cx01/prepare.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    verifier = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "verify_outcome_blind_bundle")
    guard = next(n for n in verifier.body if isinstance(n, ast.If) and "packaged structural audit does not pass" in ast.unparse(n))
    compiled = compile(ast.Module(body=[guard], type_ignores=[]), "verify-audit-guard", "exec")
    exec(compiled, namespace)
    namespace["audits"]["component_structure"]["passed"] = False
    with unittest.TestCase().assertRaisesRegex(RuntimeError, "packaged structural audit does not pass"):
        exec(compiled, namespace)


def test_auditor_exception_is_not_converted_to_success() -> None:
    namespace, statements = _namespace()
    def fail(_: object) -> dict[str, Any]:
        raise RuntimeError("audit sentinel failure")
    namespace.update(worlds=(), audit_formal_grid_structure=fail)
    with unittest.TestCase().assertRaisesRegex(RuntimeError, "audit sentinel failure"):
        exec(compile(ast.Module(body=statements, type_ignores=[]), "audit-guard", "exec"), namespace)


class AuditEnvelopeTests(unittest.TestCase):
    def test_explicit_non_success(self) -> None:
        test_envelope_rejects_explicit_non_success()

    def test_sixty_reserved_worlds(self) -> None:
        test_reserved_sixty_world_audits_pass_without_report_mutation()

    def test_exception_propagation(self) -> None:
        test_auditor_exception_is_not_converted_to_success()


if __name__ == "__main__":
    unittest.main()

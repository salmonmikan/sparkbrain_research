"""Reproduce an audit-shape blocker without importing any comparator runtime.

Supply src/sparkbrain/comparison/cx01 from observed commit 10490ee3.
Only the already-reserved structure-fixture 5000..5009 is constructed.
No formal candidate, manifest, package, seal or STARTED is constructed.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path


def run(source: Path) -> dict:
    expected = {
        "formal_identifiability.py": "1d2d8ede56d479baaa79d6bad4c224780a0788b2fdec6e44d77ecbf7f0dcf9a4",
        "formal_revision.py": "4e76a265a8f501f21cad7bd73660602d78ecf487357102429be60155c4701436",
        "formal_worlds.py": "7e54a2909ea487bd2ac109846ec4164ff37ca8f17e3d4e83677272cc6a1eb044",
        "prepare.py": "2b78cb045139a1f910eed6935ebffa3a919b28128810d1429314a7d48172a5b0",
        "structural_components.py": "5aa5ae1192e5744d110777505fb5ad58800f0d6d2928cf22274f3182b43634cc",
        "worlds.py": "34f6063773eec1fd8d21646ecc3131d273ae2d2073053e7c3ac53bb58c047e0a",
    }
    for name, digest in expected.items():
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"observed source snapshot hash mismatch: {name}")
    package = types.ModuleType("cx01_audit_snapshot")
    package.__path__ = [str(source)]
    sys.modules[package.__name__] = package
    modules = {}
    hashes = {}
    for name in (
        "worlds", "formal_worlds", "formal_revision",
        "structural_components", "formal_identifiability",
    ):
        path = source / f"{name}.py"
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        spec = importlib.util.spec_from_file_location(f"{package.__name__}.{name}", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        modules[name] = module

    worlds = tuple(
        modules["formal_revision"].build_revised_formal_world(
            "cx01-fixture-prepare-001", family, seed
        )
        for family in modules["worlds"].CX01Family
        for seed in range(5000, 5010)
    )
    namespace = {
        "worlds": worlds,
        "audit_formal_grid_structure": modules["formal_worlds"].audit_formal_grid_structure,
        "audit_formal_grid_components": modules["structural_components"].audit_formal_grid_components,
        "audit_formal_grid_identifiability": modules["formal_identifiability"].audit_formal_grid_identifiability,
    }
    path = source / "prepare.py"
    hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    tree = ast.parse(path.read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "prepare_outcome_blind_bundle")
    index = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "audits" for t in n.targets))
    statements = function.body[index:index + 2]
    assert isinstance(statements[1], ast.If), "audited source guard changed"
    error = None
    try:
        exec(compile(ast.Module(body=statements, type_ignores=[]), str(path), "exec"), namespace)
    except RuntimeError as exc:
        error = str(exc)
    assert error == "candidate structural audits must pass before packaging", error
    audits = namespace["audits"]
    assert audits["component_structure"]["passed"] is True
    assert "passed" not in audits["canonical_structure"]
    assert "passed" not in audits["family_identifiability"]
    assert all(row["development_overlap_count"] == 0 for row in audits["canonical_structure"]["family_rows"].values())
    ident = audits["family_identifiability"]
    assert ident["family_pass_counts"] == ident["family_world_counts"]
    return {
        "status": "BLOCKER_REPRODUCED",
        "source_git_sha": "10490ee302d3e6c540a5acc886d530250745143e",
        "source_sha256": hashes,
        "fixture": "cx01-fixture-prepare-001",
        "fixture_seeds": list(range(5000, 5010)),
        "world_count": len(worlds),
        "all_auditors_returned_without_exception": True,
        "passed_key_present": {key: "passed" in value for key, value in audits.items()},
        "observed_error": error,
        "comparator_imports": 0,
        "formal_capability_calls": 0,
        "package_writes": 0,
        "limitations": "Executes original AST audit assignment and guard only, not full package preparation.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source), indent=2, sort_keys=True))

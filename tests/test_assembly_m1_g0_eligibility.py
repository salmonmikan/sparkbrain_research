"""Model-free source auditor checks; no fixture, backend or model imports."""
from __future__ import annotations

import ast
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/verify_assembly_m1_g0_eligibility.py"
SPEC = importlib.util.spec_from_file_location("g0_source_auditor", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)


def contract():
    return json.loads((ROOT / AUDITOR.PROTOCOL).read_text())


def test_success_is_source_binding_not_g0_pass():
    before = {name for name in sys.modules if name.startswith("sparkbrain")}
    result = AUDITOR.verify(ROOT)
    assert result["source_binding_verified"] is True
    assert result["g0_status"] == "BLOCKED_SOURCE_CONTRACT_GAP"
    assert result["runtime_execution_authorized"] is False
    assert result["scientific_credit"] == 0
    assert len(result["facts"]) == 9
    assert before == {name for name in sys.modules if name.startswith("sparkbrain")}


@pytest.mark.parametrize("key,value", [
    ("schema", True), ("schema", 2), ("classification", "PASS"),
    ("scientific_credit", True), ("scientific_credit", 1),
    ("runtime_execution_authorized", True), ("runtime_execution_authorized", 0),
    ("blockers", {}),
])
def test_rejects_boundary_upgrade(key, value):
    data = contract()
    data[key] = value
    with pytest.raises(ValueError):
        AUDITOR.verify(ROOT, data)


@pytest.mark.parametrize("path", sorted(contract()["files"]))
def test_rejects_source_digest_drift(path):
    data = contract()
    data["files"][path] = "0" * 64
    with pytest.raises(ValueError, match="source drift"):
        AUDITOR.verify(ROOT, data)


@pytest.mark.parametrize("key,value", [
    ("symbol", "Missing.method"), ("required_tokens", ["NEVER_PRESENT_TOKEN"]),
    ("path", "src/absent.py"),
])
def test_rejects_source_fact_drift(key, value):
    data = contract()
    data["facts"][0][key] = value
    with pytest.raises(ValueError):
        AUDITOR.verify(ROOT, data)


def test_rejects_duplicate_and_missing_facts():
    for facts in ([], [contract()["facts"][0]] * 2):
        data = contract()
        data["facts"] = facts
        with pytest.raises(ValueError):
            AUDITOR.verify(ROOT, data)


def test_rejects_paths_outside_checkout():
    data = contract()
    data["files"]["../outside.py"] = "0" * 64
    with pytest.raises(ValueError, match="escapes checkout"):
        AUDITOR.verify(ROOT, data)


def test_contract_is_not_mutated():
    data = contract()
    original = copy.deepcopy(data)
    AUDITOR.verify(ROOT, data)
    assert data == original


def test_symbol_resolution_rejects_ambiguity():
    tree = ast.parse("def a(): pass\ndef a(): pass\n")
    with pytest.raises(ValueError, match="ambiguous"):
        AUDITOR.resolve_symbol(tree, "a")


def test_cli_with_import_guard():
    # Install the guard before importing the audit script, not after a model could run.
    program = '''
import importlib.abc, runpy, sys
class DenySparkBrain(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise RuntimeError("SparkBrain import forbidden in source-only audit")
sys.meta_path.insert(0, DenySparkBrain())
sys.argv = [sys.argv[1]]
runpy.run_path(sys.argv[0], run_name="__main__")
assert not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules)
'''
    result = subprocess.run(
        [sys.executable, "-B", "-c", program, str(SCRIPT)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    assert report["g0_status"] == "BLOCKED_SOURCE_CONTRACT_GAP"
    assert report["real_dynamics_calls_by_this_auditor"] == 0


@pytest.mark.parametrize("mutation", ["commit", "cases", "subset", "empty_tokens", "metadata"])
def test_rejects_reduced_or_relabelled_contract(mutation):
    data = contract()
    if mutation == "commit":
        data["source_commit"] = "0" * 40
    elif mutation == "cases":
        data["future_case_ids"] = []
    elif mutation == "subset":
        data["facts"] = data["facts"][:1]
    elif mutation == "empty_tokens":
        data["facts"][0]["required_tokens"] = []
    else:
        data["facts"][0]["interpretation"] = "G0 passed"
    with pytest.raises(ValueError, match="complete pinned inventory"):
        AUDITOR.verify(ROOT, data)


@pytest.mark.parametrize("mutation", ["authorization", "facts", "nested", "identical"])
def test_rejects_duplicate_json_keys_before_source_access(tmp_path, mutation):
    raw = (ROOT / AUDITOR.PROTOCOL).read_text()
    if mutation == "authorization":
        raw = '{"runtime_execution_authorized":true,' + raw[1:]
    elif mutation == "facts":
        raw = '{"facts":[],' + raw[1:]
    elif mutation == "nested":
        raw = raw.replace('"required_tokens": [', '"required_tokens": [], "required_tokens": [', 1)
    else:
        raw = '{"schema":1,' + raw[1:]
    path = tmp_path / AUDITOR.PROTOCOL
    path.parent.mkdir(parents=True)
    path.write_text(raw)
    # Source files are deliberately absent: malformed contract must reject first.
    with pytest.raises(ValueError, match="duplicate JSON key"):
        AUDITOR.verify(tmp_path)


def test_rejects_nonfinite_json_before_hashing(tmp_path):
    path = tmp_path / AUDITOR.PROTOCOL
    path.parent.mkdir(parents=True)
    path.write_text('{"unknown":NaN}')
    with pytest.raises(ValueError, match="nonfinite JSON constant"):
        AUDITOR.verify(tmp_path)

"""Static new-source binding checks only; no native import or construction."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.verify_m1_path_source import CONTRACT, verify

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def copied(tmp_path):
    root = tmp_path / "source"
    contract = json.loads((ROOT / CONTRACT).read_text())
    files = {CONTRACT, *contract["runtime_sources_sha256"], *contract["runtime_schema_sha256"],
             *contract["preparation_sources_sha256"]}
    for relative in files:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, path)
    return root


def test_new_repaired_source_is_static_only_and_does_not_inherit_g0():
    result = verify(ROOT)
    assert result["status"] == "SOURCE_ONLY_CANDIDATE_VERIFIED_NATIVE_BLOCKED"
    assert result["runtime_execution_authorized"] is False
    assert result["class_witnesses"] == 101
    assert result["allocation_type_witnesses"] > 101
    contract = json.loads((ROOT / CONTRACT).read_text())
    assert contract["historical_delta"]["g0_eligibility_inherited"] is False
    assert set(contract["historical_delta"]["changed_runtime_sources"]) == {
        "src/sparkbrain/v032/checkpoint.py"}
    assert "exact_repaired_three_observation_graph_and_checkpoint_eligibility" in (
        result["unresolved_gates"])


def test_old_contract_keeps_rejecting_new_repaired_runtime():
    from scripts.verify_g0_joint_source_contract import verify as historical_verify
    with pytest.raises(ValueError, match="runtime dependency inventory"):
        historical_verify(ROOT)


@pytest.mark.parametrize("kind", ["runtime", "extra", "input", "script", "manifest"])
def test_source_input_and_scope_drift_fail_closed(copied, kind):
    relative = {
        "runtime": "src/sparkbrain/v032/checkpoint.py",
        "extra": "src/sparkbrain/unreviewed.py",
        "input": "artifacts/research/assembly_m1_path_v1_20261002/inputs.jsonl",
        "script": "scripts/m1_path_pilot.py", "manifest": CONTRACT,
    }[kind]
    path = copied / relative
    with path.open("a") as stream:
        stream.write("\n")
    with pytest.raises(ValueError, match="changed"):
        verify(copied)


def test_contract_alias_rejected(copied, tmp_path):
    path = copied / CONTRACT
    external = tmp_path / "contract.json"
    path.rename(external)
    path.symlink_to(external)
    with pytest.raises(ValueError, match="symlink"):
        verify(copied)


def test_static_verification_import_guard():
    program = '''
import importlib.abc, sys
class Deny(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name == 'sparkbrain' or name.startswith('sparkbrain.'):
            raise AssertionError('model import forbidden')
sys.meta_path.insert(0, Deny())
from scripts.verify_m1_path_source import verify
assert verify()['runtime_execution_authorized'] is False
assert not any(n == 'sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules)
'''
    subprocess.run([sys.executable, "-B", "-c", program], cwd=ROOT, check=True)


def test_transient_allocations_have_separate_source_witnesses():
    contract = json.loads((ROOT / CONTRACT).read_text())
    for name in ("sparkbrain.v032.contracts:SensoryChannelDecision",
                 "sparkbrain.v032.contracts:V032StepResult",
                 "sparkbrain.v03_seed.sensory_field:SensoryChannelTrace",
                 "sparkbrain.v03_seed.sensory_field:SensoryObservation",
                 "sparkbrain.v03_seed.contracts:ConceptCandidate"):
        assert name in contract["allocation_type_sources"]

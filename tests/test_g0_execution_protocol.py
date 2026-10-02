"""Literal/source-only checks; this file never imports the native SparkBrain package."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from scripts import g0_execution_support as support
from scripts import run_g0_joint_eligibility as runner

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / runner.ARTIFACT_ROOT


def load(name):
    return json.loads((ARTIFACT / name).read_text())


def test_protocol_inputs_and_budget_bindings():
    protocol = load('protocol.json')
    assert protocol['identity'] == support.IDENTITY == runner.IDENTITY
    assert protocol['call_caps'] == support.protocol_call_caps()
    assert protocol['limits'] == support.LIMITS
    assert protocol['reserves'] == support.RESERVES
    assert protocol['status'] == 'PROSPECTIVE_UNEXECUTED'
    assert protocol['ownership_contract_sha256'] == support.CONTRACT_SHA256
    assert protocol['source_base_commit'] == runner.SOURCE_PIN
    assert len(protocol['cases']) == 14
    assert [case['candidate'] for case in protocol['cases']] == list(range(1, 15))
    binding = protocol['inputs']
    assert hashlib.sha256((ROOT / binding['path']).read_bytes()).hexdigest() == binding['sha256']
    unique_hash = hashlib.sha256((ROOT / binding['unique_rows_path']).read_bytes()).hexdigest()
    assert unique_hash == binding['unique_rows_sha256']
    rows, receipts = runner.normalize_plan(load('inputs.json'))
    assert len(rows) == 66 and len(receipts) == 3
    assert len({row['observation']['occurrence_id'] for row in rows}) == 66


def test_literal_recipe_exposure_and_only_declared_changes():
    protocol = load('protocol.json')
    provenance = protocol['input_provenance']
    raw = (ROOT / provenance['source']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == provenance['sha256']
    rows = [json.loads(line) for line in raw.splitlines()]
    # Historical exposed A32/B32 plus the first A query; neither selection nor
    # adaptation is permitted at runtime. The primary literal schema is checked
    # independently of importing any historical producer script.
    selected = [row for row in rows if row.get('seed') == provenance['seed']]
    assert selected
    primary = load('inputs.json')
    assert len(primary['acquisition']) == 64
    for index, observation in enumerate(primary['acquisition']):
        assert observation['occurrence_id'] == f'g0-20261002-{index:06d}'
        original = copy.deepcopy(selected[index]['observation'])
        original['occurrence_id'] = observation['occurrence_id']
        assert observation == original
    bootstrap = primary['queries']['bootstrap']
    later = primary['queries']['publish_observe']
    original = copy.deepcopy(selected[64]['observation'])
    original['occurrence_id'] = bootstrap['occurrence_id']
    assert bootstrap == original
    shifted = copy.deepcopy(bootstrap)
    shifted['occurrence_id'] = later['occurrence_id']
    shifted['start_ms'] += 200.0
    for pulse in shifted['pulses']:
        pulse['time_ms'] += 200.0
    assert later == shifted
    assert later['start_ms'] == bootstrap['start_ms'] + 200.0
    assert later['occurrence_id'] != bootstrap['occurrence_id']
    assert primary['receipts']['teach']['event_id'] == later['occurrence_id']
    assert (primary['receipts']['conflict']['receipt_id']
            == primary['receipts']['teach']['receipt_id'])


def test_preparation_imports_cannot_load_native_runtime():
    code = '''
import importlib.abc, sys
class BlockNative(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("native runtime import during preparation: " + fullname)
sys.meta_path.insert(0, BlockNative())
from scripts import g0_execution_support
from scripts import run_g0_joint_eligibility
assert not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules)
'''
    result = subprocess.run([sys.executable, '-B', '-s', '-c', code], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr

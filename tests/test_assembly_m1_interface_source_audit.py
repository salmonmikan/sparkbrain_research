"""Model-free corruption checks for the design auditor; no SparkBrain imports."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "assembly_m1_design_audit", ROOT / "scripts/verify_assembly_m1_interface_design.py"
)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def inputs():
    sources = {path: (ROOT / path).read_bytes() for path in AUDIT.SYMBOLS}
    record = json.loads((ROOT / AUDIT.ARTIFACT / "source_audit.json").read_text())
    return sources, record, copy.deepcopy(AUDIT.EXPECTED_CONTRACT)


def test_current_source_audit():
    sources, record, contract = inputs()
    AUDIT.verify_audit(record, sources, contract)


@pytest.mark.parametrize("field", ["sha256", "symbols"])
def test_rejects_changed_source_record(field):
    sources, record, contract = inputs()
    first = next(iter(record["files"]))
    record["files"][first][field] = "corrupted"
    with pytest.raises(ValueError, match="source audit"):
        AUDIT.verify_audit(record, sources, contract)


def test_rejects_missing_file():
    sources, record, contract = inputs()
    sources.pop(next(iter(sources)))
    with pytest.raises(ValueError, match="inventory"):
        AUDIT.verify_audit(record, sources, contract)


def test_rejects_added_source_bytes():
    sources, record, contract = inputs()
    first = next(iter(sources))
    sources[first] += b"\n# source mutation\n"
    with pytest.raises(ValueError, match="source audit"):
        AUDIT.verify_audit(record, sources, contract)


@pytest.mark.parametrize("field,value", [
    ("feature_dimensions", 3),
    ("model_execution_authorized", 0),
    ("scientific_credit", False),
    ("native_v05_checkpoint_sufficient", True),
    ("maximum_pending_occurrences", 2),
])
def test_rejects_contract_changes(field, value):
    sources, record, contract = inputs()
    contract[field] = value
    with pytest.raises(ValueError, match="contract"):
        AUDIT.verify_audit(record, sources, contract)


def test_rejects_reference_action_read_added_to_observe():
    sources, _, _ = inputs()
    path = "src/sparkbrain/system_build/integrated_m1.py"
    sources[path] = sources[path].replace(
        b"prediction = self.predictive.observe(self._sensory_sample(observation))",
        b"prediction = self.predictive.observe(self._sensory_sample(observation))\n"
        b"                unused = prediction.reference_action",
    )
    with pytest.raises(ValueError, match="source facts"):
        AUDIT.build_audit(sources)

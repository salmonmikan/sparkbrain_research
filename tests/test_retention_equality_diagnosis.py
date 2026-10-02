"""Data-only checks against the already-preserved retention archive; never run models."""
from __future__ import annotations

import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/analyze_retention_equality.py"
SPEC = importlib.util.spec_from_file_location("retention_equality_data_only", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ARTIFACT = ROOT / MODULE.ARTIFACT


def binding():
    return MODULE.parse((ARTIFACT / "input_binding.json").read_bytes())


def guarded_command(script, *args):
    program = '''
import importlib.abc,runpy,sys
class BlockModels(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise RuntimeError("model import prohibited in retained-data diagnosis")
sys.meta_path.insert(0,BlockModels())
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0],run_name="__main__")
assert not any(x == "sparkbrain" or x.startswith("sparkbrain.") for x in sys.modules)
'''
    return subprocess.run([sys.executable, "-S", "-P", "-B", "-c", program,
                           str(script), *map(str, args)],
                          check=True, capture_output=True)


@pytest.fixture(scope="module")
def extracted(tmp_path_factory):
    path = tmp_path_factory.mktemp("retained-data") / "extracted"
    result = guarded_command(ROOT / "scripts/verify_retention_v5_evidence.py", "--extract", path)
    assert MODULE.parse(result.stdout)["runtime_model_method_calls"] == 0
    return path


def test_exact_reproduction_with_model_imports_denied(extracted):
    result = guarded_command(SCRIPT, "--run-root", extracted / "run",
                             "--source-root", extracted / "frozen-sources")
    assert result.stdout == (ARTIFACT / "diagnosis.json").read_bytes()
    data = MODULE.parse(result.stdout)
    assert data["model_calls"] == 0
    assert data["scientific_credit"] == 0
    assert data["raw_files_unchanged"] is True
    assert data["raw_files_read"] == 48
    assert len(data["comparisons"]) == 8


def test_summarized_raw_comparisons_and_boundaries(extracted):
    result = MODULE.analyze(extracted / "run", extracted / "frozen-sources", binding())
    for row in result["comparisons"]:
        if row["right_arm"] in ("Fw", "G"):
            assert row["exact_equal_row_counts"]["spike_unit_time"] == 32
            assert row["exact_equal_row_counts"]["raw_result.patterns"] == 32
            assert row["exact_equal_row_counts"]["p1"] == 32
            assert row["first_difference_zero_based_index"]["raw_result.v04_result.spikes"] == 1
            assert row["left"]["nonzero_weight_writes"] == 224
            assert row["left"]["clipped_updates"] == 0
            assert row["aligned_spike_potential_changed_units"] == {"45": 31, "56": 31, "63": 31}
        else:
            assert row["first_difference_zero_based_index"]["spike_unit_time"] == 10
            assert row["first_difference_zero_based_index"]["p1"] == 14
        if row["right_arm"] == "Fw":
            assert row["right"]["nonzero_weight_writes"] == 0
            assert all(row["final_component_exact_equality"].values())
            assert row["equal_post_receipt_count_tables"] == 32


@pytest.mark.parametrize("key", ["raw_files", "source_files", "source_commit",
                                 "result_publication_commit", "archive_sha256"])
def test_modified_binding_rejected_before_data_reads(tmp_path, key):
    value = binding()
    value[key] = {} if key.endswith("files") else "changed"
    with pytest.raises(ValueError, match="pinned retained-data contract"):
        MODULE.analyze(tmp_path, tmp_path, value)


@pytest.mark.parametrize("raw", ['{"a":1,"a":1}', '{"a":1,"a":2}',
                                 '{"a":{"b":0,"b":1}}'])
def test_duplicate_json_rejected(raw):
    with pytest.raises(ValueError, match="duplicate"):
        MODULE.parse(raw)


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity", "1e400", "-1e400"])
def test_nonfinite_json_rejected(literal):
    with pytest.raises(ValueError, match="nonfinite"):
        MODULE.parse('{"x":' + literal + '}')


def test_changed_raw_bytes_rejected(tmp_path):
    (tmp_path / "record.json").write_text('{}')
    with pytest.raises(ValueError, match="input hash differs"):
        MODULE.checked_bytes(tmp_path, "record.json", "0" * 64)


def test_path_escape_rejected(tmp_path):
    with pytest.raises(ValueError, match="escapes"):
        MODULE.checked_bytes(tmp_path, "../outside.json", "0" * 64)


def branches(extracted):
    result = []
    for arm in ("L", "Fw"):
        root = extracted / "run/jobs" / f"910075-return-{arm}"
        branch = {}
        for name in MODULE.FILES:
            raw = (root / name).read_bytes()
            branch[name] = ([MODULE.parse(line) for line in raw.splitlines()]
                            if name.endswith(".jsonl") else MODULE.parse(raw))
        result.append(branch)
    return result


@pytest.mark.parametrize("mutation", [
    "short", "index", "input_sha256", "outcome", "receipt_short", "receipt_index",
    "receipt_identity", "receipt_outcome", "apply_short", "apply_index",
])
def test_unpaired_or_incomplete_rows_rejected(extracted, mutation):
    a, b = branches(extracted)
    if mutation == "receipt_short":
        b["receipts.jsonl"].pop()
    elif mutation == "receipt_index":
        b["receipts.jsonl"][0]["index"] = 99
    elif mutation == "receipt_identity":
        b["receipts.jsonl"][0]["occurrence_id"] = "wrong"
    elif mutation == "receipt_outcome":
        b["receipts.jsonl"][0]["outcome"] = "wrong"
    elif mutation == "apply_short":
        b["apply.jsonl"].pop()
    elif mutation == "apply_index":
        b["apply.jsonl"][0]["index"] = 99
    elif mutation == "short":
        b["predictions.jsonl"].pop()
    elif mutation == "index":
        b["predictions.jsonl"][0]["index"] = 99
    else:
        b["predictions.jsonl"][0][mutation] = "different"
    with pytest.raises(ValueError):
        MODULE.summarize_pair(a, b)


def test_analysis_does_not_mutate_decoded_inputs(extracted):
    a, b = branches(extracted)
    before = copy.deepcopy([a, b])
    MODULE.summarize_pair(a, b)
    assert [a, b] == before


def test_first_difference_preserves_row_position():
    assert MODULE.first_difference([1, 2, 3], [1, 4, 3]) == 1
    assert MODULE.first_difference([1, 2], [1, 2]) is None
    with pytest.raises(ValueError):
        MODULE.first_difference([1], [1, 2])
    with pytest.raises(ValueError):
        MODULE.first_difference([1], [2, 3])

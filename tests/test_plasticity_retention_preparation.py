"""Only JSON/source preparation; importing a SparkBrain runtime is forbidden."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/prepare_plasticity_retention_inputs.py"
SPEC = importlib.util.spec_from_file_location("retention_prepare", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)
P = json.loads(TOOL.PROTOCOL.read_bytes())


@pytest.fixture(scope="module")
def prepared():
    return TOOL.build()


def test_exact_preparation_recalculates(prepared) -> None:
    assert set(prepared) == {
        "inputs.json",
        "jobs.json",
        "prefix_sources.json",
        "preparation_manifest.json",
    }
    for name, raw in prepared.items():
        assert (TOOL.DEFAULT / name).read_bytes() == raw
    m = json.loads(prepared["preparation_manifest.json"])
    assert m["model_calls"] == 0
    assert m["execution_authorized"] is False
    assert m["execution_runner_present"] is False
    assert m["execution_dependency_freeze_complete"] is False


def test_novel_each_half_has_eight_of_each_class(prepared) -> None:
    streams = json.loads(prepared["inputs.json"])["streams"]
    for seed in (910075, 910076):
        rows = streams[f"{seed}-novel"]
        for start in (0, 16):
            targets = [r["outcome"] for r in rows[start : start + 16]]
            assert targets.count(0) == targets.count(1) == 8


def test_complete_information_and_timing_contract(prepared) -> None:
    inputs = json.loads(prepared["inputs.json"])["streams"]
    assert len(inputs) == 6 and sum(map(len, inputs.values())) == 160
    for key, rows in inputs.items():
        condition = key.split("-")[1]
        for i, row in enumerate(rows):
            assert set(row) == {"occurrence_id", "start_ms", "pulses", "outcome", "receipt_time_ms"}
            assert row["occurrence_id"] == f"occ-{64 + i:06d}"
            assert row["start_ms"] == float((64 + i) * 200)
            assert row["receipt_time_ms"] == row["start_ms"] + 80
            assert len(row["pulses"]) == 6
            cue = [x for x in row["pulses"] if x["channel"] in "ACF"]
            expected = {
                "return": "AFC",
                "stationary": "CFA",
                "novel": ("ACF", "CAF")[row["outcome"]],
            }[condition]
            assert "".join(x["channel"] for x in cue) == expected
            for x in row["pulses"]:
                assert x["metadata"] == {} and x["source_id"] == "probe-input"
                assert x["novelty"] == x["prediction_error"] == 0.0
                assert 0 <= x["time_ms"] - row["start_ms"] <= 40
            q = next(x for x in row["pulses"] if x["channel"] == "Q")
            assert q["time_ms"] == row["start_ms"] + 40 and q["magnitude"] == 1.18


def test_jobs_share_exact_inputs_and_prefixes(prepared) -> None:
    jobs = json.loads(prepared["jobs.json"])["jobs"]
    streams = json.loads(prepared["inputs.json"])["streams"]
    assert len(jobs) == 26 and sum(x["pairs"] for x in jobs) == 768
    assert sum(x["pairs"] for x in jobs if x["family"] == "v05") == 512
    assert sum(x["family"] == "v05" for x in jobs) == 18
    for job in jobs:
        assert job["input_sha256"] == TOOL.sha(TOOL.encoded(streams[job["stream"]]))
        assert job["prefix"].endswith("-S" if job["family"] == "v05" else "-" + job["arm"])
    for stream in streams:
        hashes = {x["input_sha256"] for x in jobs if x["stream"] == stream}
        assert len(hashes) == 1


def test_failure_allowance_is_inside_total_budget() -> None:
    r = P["resources"]
    assert r["ordinary_output_bytes"] + r["reserved_failure_metadata_bytes"] == 256 * 1024**2
    assert (
        26 * r["max_worker_terminal_metadata_bytes"] + r["max_driver_terminal_metadata_bytes"]
        <= (r["reserved_failure_metadata_bytes"])
    )


@pytest.mark.parametrize(
    "key,value",
    [("execution_authorized", True), ("execution_authorized", 0), ("schema_version", True)],
)
def test_preparation_cannot_misstate_authority_or_schema(key: str, value) -> None:
    p = copy.deepcopy(P)
    p[key] = value
    with pytest.raises(ValueError):
        TOOL.make_inputs(p)


@pytest.mark.parametrize("kind", ["budget", "arm", "mapping", "model_keys", "delay", "reserve"])
def test_changed_control_contract_rejected(kind: str) -> None:
    p = copy.deepcopy(P)
    if kind == "budget":
        p["budget"]["total_pairs"] = 769
    elif kind == "arm":
        p["arms"]["L"]["enable_weight_learning"] = False
    elif kind == "mapping":
        p["conditions"]["novel"]["outcomes"] = [1, 0]
    elif kind == "model_keys":
        p["input_contract"]["model_keys"].append("outcome")
    elif kind == "delay":
        p["common_v05"]["enable_delay_learning"] = True
    else:
        p["resources"]["max_driver_terminal_metadata_bytes"] *= 10
    with pytest.raises(ValueError):
        TOOL.make_inputs(p)


def test_no_clobber_or_input_overlap(tmp_path: Path, prepared) -> None:
    with pytest.raises(ValueError, match="absent"):
        TOOL.write_new(tmp_path, prepared)
    old = ROOT / P["public_prefix_source"]["transport_directory"]
    with pytest.raises(ValueError, match="overlap"):
        TOOL.write_new(old / "forbidden-new-output", prepared)
    assert not (old / "forbidden-new-output").exists()
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path / "absent")
    with pytest.raises(ValueError, match="absent"):
        TOOL.write_new(alias, prepared)


def test_preparer_readback_cli_never_imports_runtime() -> None:
    code = (
        "import builtins,runpy,sys; original=builtins.__import__; "
        'exec("def guard(name,*a,**k):\\n'
        " if name.startswith('sparkbrain'): raise AssertionError(name)\\n"
        ' return original(name,*a,**k)"); '
        "builtins.__import__=guard;sys.argv=" + repr([str(SOURCE), "--check"]) + ";"
        "runpy.run_path(" + repr(str(SOURCE)) + ",run_name='__main__')"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["model_calls"] == 0


def test_documented_novel_block_counts_cannot_drift() -> None:
    p = copy.deepcopy(P)
    p["conditions"]["novel"]["balanced_blocks"][0]["counts"] = {"0": 9, "1": 7}
    with pytest.raises(ValueError, match="balanced novel blocks"):
        TOOL.make_inputs(p)

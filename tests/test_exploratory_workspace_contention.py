"""Adverse and reproducibility checks for a non-evidentiary diagnostic."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "workspace_contention", ROOT / "scripts/exploratory_workspace_contention.py"
)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_exact_frozen_grid_and_runtime():
    protocol = runner.load_protocol()
    assert len(runner.cells(protocol)) == 216
    assert len({runner.canonical(cell) for cell in runner.cells(protocol)}) == 216
    assert len(runner.verify_runtime(protocol)) == 3


@pytest.mark.parametrize("mutation", ["extra", "value", "type", "order", "missing"])
def test_rejects_protocol_mutations(tmp_path, mutation):
    protocol = runner.load_protocol()
    if mutation == "extra":
        protocol["undeclared"] = True
    elif mutation == "value":
        protocol["rounds"] += 1
    elif mutation == "type":
        protocol["schema_version"] = True
    elif mutation == "order":
        protocol["seeds"].reverse()
    else:
        del protocol["claims"]
    path = tmp_path / "changed.json"
    path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(ValueError, match="Frozen protocol"):
        runner.load_protocol(path)


def test_rejects_changed_runtime(tmp_path, monkeypatch):
    protocol = runner.load_protocol()
    path = tmp_path / "src/sparkbrain/engine.py"
    path.parent.mkdir(parents=True)
    path.write_text("# changed\n", encoding="utf-8")
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="Pinned runtime"):
        runner.verify_runtime(protocol)


def test_capacity_changes_retention_not_ignition():
    protocol = runner.load_protocol()
    cell = runner.cells(protocol)[0] | {"task_count": 4}
    low = runner.run_episode(cell | {"slots": 1}, protocol)
    high = runner.run_episode(cell | {"slots": 4}, protocol)
    assert low["inputs"] == high["inputs"]
    assert low["ignitions"] == high["ignitions"]
    assert low["counters"] == high["counters"]
    assert len(low["final_workspace"]) <= 1
    assert len(high["final_workspace"]) <= 4


def test_single_task_shared_equals_isolation():
    protocol = runner.load_protocol()
    cell = runner.cells(protocol)[0]
    shared = runner.run_episode(cell, protocol)
    isolated = runner.run_episode(cell | {"variant": "isolated_reference"}, protocol)
    for key in ("inputs", "ignitions", "final_workspace", "metrics", "counters"):
        assert shared[key] == isolated[key]


def test_controls_preserve_input_and_isolated_subsequences():
    protocol = runner.load_protocol()
    cell = runner.cells(protocol)[0] | {"task_count": 4}
    rows = [runner.run_episode(cell | {"variant": variant}, protocol)
            for variant in protocol["variants"]]
    assert len({row["input_sha256"] for row in rows}) == 1
    for row in rows:
        assert row["counters"]["events_processed"] == len(row["inputs"])
        assert row["counters"]["fires"] == 0
        assert row["counters"]["edge_evaluations"] == 0
        assert all(item["task"] in range(4) for item in row["ignitions"])
    assert rows[-1]["engine_count"] == 4


def test_artifact_reproduction_and_no_clobber(tmp_path):
    left, right = tmp_path / "left", tmp_path / "right"
    runner.produce(left, "a" * 40)
    runner.produce(right, "a" * 40)
    assert sorted(p.name for p in left.iterdir()) == [
        "manifest.json", "raw_episodes.jsonl", "summary.json"
    ]
    for path in left.iterdir():
        assert path.read_bytes() == (right / path.name).read_bytes()
    rows = [json.loads(line) for line in (left / "raw_episodes.jsonl").read_text().splitlines()]
    protocol = runner.load_protocol()
    for row in rows:
        declared = set(protocol["primary_metrics"] + protocol["secondary_metrics"])
        assert declared <= row["metrics"].keys() | row["counters"].keys()
        assert row["metrics"]["ignition_count"] == len(row["ignitions"])
        assert row["metrics"]["ignition_count"] == row["counters"]["ignitions"]
    assert json.loads((left / "summary.json").read_text()) == runner.summarize(rows)
    manifest = json.loads((left / "manifest.json").read_text())
    for name, expected in manifest["files"].items():
        assert runner.sha256((left / name).read_bytes()) == expected
    with pytest.raises(FileExistsError):
        runner.produce(left, "a" * 40)
    with pytest.raises(ValueError):
        runner.produce(tmp_path / "bad", "unknown")

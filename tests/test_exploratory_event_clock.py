from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "event_clock", ROOT / "scripts/exploratory_event_clock.py"
)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def condition(**changes):
    return {"strength": 0.6, "sources": 2, "stability": 4, "bonus": 0.0, "gap": 0.0,
            "padding_count": 2, "padding_kind": "hypothesis", **changes}


def episode(**changes):
    return runner.run_episode(condition(**changes), runner.load_protocol())


def test_exact_unique_grid_and_metrics():
    protocol = runner.load_protocol()
    cells = runner.cells(protocol)
    assert len(cells) == 1080
    assert len({runner.canonical(cell) for cell in cells}) == 1080
    assert sum(cell["padding_count"] == 0 for cell in cells) == 108
    required = set(protocol["primary_metrics"] + protocol["secondary_metrics"])
    assert required <= episode()["metrics"].keys()


@pytest.mark.parametrize("mutation", ["value", "type", "extra", "format"])
def test_protocol_mutation_rejected(tmp_path, mutation):
    protocol = runner.load_protocol()
    if mutation == "value":
        protocol["evidence_strengths"][0] = 0.2
    elif mutation == "type":
        protocol["random_seed"] = "7"
    elif mutation == "extra":
        protocol["unexpected"] = True
    path = tmp_path / "protocol.json"
    path.write_text(json.dumps(protocol))
    with pytest.raises(ValueError, match="Frozen protocol"):
        runner.load_protocol(path)


def test_runtime_source_pin_rejects_changes(tmp_path, monkeypatch):
    protocol = runner.load_protocol()
    for name in protocol["runtime_git_blobs"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    runner.verify_runtime(protocol)
    with (tmp_path / "src/sparkbrain/engine.py").open("ab") as stream:
        stream.write(b"\n")
    with pytest.raises(ValueError, match="Pinned runtime"):
        runner.verify_runtime(protocol)


def test_primary_stability_gate_and_matched_nulls():
    for count in (0, 1, 2, 4):
        kinds = ("none",) if count == 0 else ("hypothesis", "sensory", "reward")
        for kind in kinds:
            result = episode(padding_count=count, padding_kind=kind)
            expected = kind == "hypothesis" and count >= 2
            assert result["metrics"]["post_padding_first_ignition"] is expected
            assert result["metrics"]["target_stability_at_end"] == (
                2 + count if kind == "hypothesis" else 2
            )
            assert result["metrics"]["pre_padding_ignition_count"] == 0


def test_genuine_evidence_event_budget_and_horizon_are_matched():
    protocol = runner.load_protocol()
    rows = [runner.run_episode(condition(gap=1.0, padding_kind=kind), protocol)
            for kind in ("hypothesis", "sensory", "reward")]
    assert len({row["genuine_input_sha256"] for row in rows}) == 1
    assert {row["metrics"]["events_processed"] for row in rows} == {5}
    assert {row["observations"][-1]["time"] for row in rows} == {4.01}
    for row in rows:
        assert row["metrics"]["fires"] == row["metrics"]["edge_evaluations"] == 0
        assert row["metrics"]["target_support_count"] == 2


def test_one_source_changes_only_sensor_metadata_and_blocks_diversity():
    protocol = runner.load_protocol()
    streams = [runner.input_stream(condition(sources=sources), protocol) for sources in (1, 2)]
    streams[0][1]["metadata"]["sensor"] = streams[1][1]["metadata"]["sensor"]
    assert streams[0] == streams[1]
    result = episode(sources=1)
    coalition = result["final_coalitions"][0]
    assert coalition["score"] > result["config"]["ignition_threshold"]
    assert coalition["stability"] == 4
    assert coalition["diversity"] == 1
    assert result["ignitions"] == []


def test_weak_evidence_remains_no_ignition():
    for sources in (1, 2):
        result = episode(strength=0.1, bonus=0.06, stability=1,
                         sources=sources, padding_count=4)
        assert result["ignitions"] == []


def test_bonus_crossing_is_separate_from_hard_stability():
    with_bonus = episode(strength=0.43, bonus=0.06, stability=2, padding_count=1)
    no_bonus = episode(strength=0.43, bonus=0.0, stability=2, padding_count=4)
    assert with_bonus["metrics"]["pre_padding_ignition_count"] == 0
    assert with_bonus["metrics"]["post_padding_first_ignition"] is True
    assert no_bonus["ignitions"] == []
    final = episode(strength=0.43, bonus=0.06, stability=2, padding_count=4)
    observations = final["observations"]
    assert observations[3]["target_stability"] == 4
    assert observations[5]["target_stability"] == 6
    assert observations[3]["stored_coalitions"][0]["score"] == (
        observations[5]["stored_coalitions"][0]["score"]
    )


def test_early_and_repeat_ignitions_are_not_padding_onset():
    result = episode(stability=2, bonus=0.06, gap=1.0, padding_count=1)
    metrics = result["metrics"]
    assert metrics["pre_padding_ignition_count"] == 1
    assert metrics["first_ignition_phase"] == "evidence"
    assert metrics["first_ignition_time"] == 0.01
    assert metrics["post_padding_first_ignition"] is False
    assert metrics["post_padding_repeat_ignition_count"] == 1


def test_same_time_and_elapsed_time_have_distinct_outcomes():
    assert episode(gap=0.0)["metrics"]["post_padding_first_ignition"] is True
    assert episode(gap=1.0)["ignitions"] == []


def test_stored_coalition_time_and_horizon_projection_are_explicit():
    result = episode(padding_kind="reward", gap=1.0)
    final = result["observations"][-1]
    assert final["time"] == 4.01
    assert final["last_coalition_evaluation_time"] == 0.01
    expected = (0.6 * math.exp(-0.01 / 2.5) + 0.6) * math.exp(-4.0 / 2.5)
    assert final["observer_only_projection"]["target_activation"] == pytest.approx(expected)
    assert final["stored_target_activation"] > expected


def test_observer_noninterference_and_empty_evidence_null():
    protocol = runner.load_protocol()
    brain = runner.make_brain(condition(), protocol)
    for _ in range(4):
        brain.schedule(time=0.01, kind=runner.EventKind.PROPAGATION,
                       source="padding", target="padding:hypothesis", strength=0.0,
                       metadata={"origin_kind": "internal"})
        brain.run()
    before = runner.canonical(brain.state_dict())
    for _ in range(3):
        observed = runner.observe(brain, 0.01)
    assert runner.canonical(brain.state_dict()) == before
    assert observed["target_stability"] == 0
    assert brain.ignitions == brain.last_coalitions == []


def test_deterministic_artifacts_and_no_clobber(tmp_path, monkeypatch):
    selected = runner.cells(runner.load_protocol())[:10]
    monkeypatch.setattr(runner, "cells", lambda protocol: selected)
    first, second = tmp_path / "a", tmp_path / "b"
    runner.produce(first, "1" * 40)
    runner.produce(second, "1" * 40)
    for path in first.iterdir():
        assert path.read_bytes() == (second / path.name).read_bytes()
    manifest = json.loads((first / "manifest.json").read_bytes())
    assert manifest["episodes"] == 10
    for name, digest in manifest["files"].items():
        assert runner.sha256((first / name).read_bytes()) == digest
    with pytest.raises(FileExistsError):
        runner.produce(first, "1" * 40)
    with pytest.raises(ValueError, match="source_commit"):
        runner.produce(tmp_path / "c", "not-a-commit")


def test_implementation_failure_is_retained(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "cells", lambda protocol: [condition()])
    monkeypatch.setattr(runner, "run_episode", lambda *args: 1 / 0)
    output = tmp_path / "failure"
    with pytest.raises(ZeroDivisionError):
        runner.produce(output, "1" * 40)
    failure = json.loads((output / "failure.json").read_bytes())
    assert failure["status"] == "IMPLEMENTATION_FAILURE"
    assert failure["completed_rows"] == 0
    assert failure["declared_source_checkpoint"] == "1" * 40
    assert failure["protocol_sha256"] == runner.PROTOCOL_SHA256
    assert failure["runner_sha256"] == runner.sha256(Path(runner.__file__).read_bytes())
    assert failure["runtime_git_blobs"] == runner.load_protocol()["runtime_git_blobs"]
    assert failure["runtime_sha256"] == runner.verify_runtime(runner.load_protocol())
    assert failure["failing_cell"] == condition()
    assert failure["failure_stage"] == "run_cell"
    assert failure["retained_files"]["raw_episodes.jsonl"]["sha256"] == runner.sha256(b"")
    assert (output / "raw_episodes.jsonl").read_bytes() == b""


def test_partial_failure_binds_retained_rows_and_failing_cell(tmp_path, monkeypatch):
    first = condition(padding_kind="sensory")
    second = condition(padding_kind="reward")
    monkeypatch.setattr(runner, "cells", lambda protocol: [first, second])
    original = runner.run_episode

    def fail_second(cell, protocol):
        if cell == second:
            raise RuntimeError("synthetic failure in second cell")
        return original(cell, protocol)

    monkeypatch.setattr(runner, "run_episode", fail_second)
    output = tmp_path / "partial"
    with pytest.raises(RuntimeError, match="synthetic failure"):
        runner.produce(output, "2" * 40)
    raw = (output / "raw_episodes.jsonl").read_bytes()
    failure = json.loads((output / "failure.json").read_bytes())
    assert failure["completed_rows"] == 1
    assert failure["failing_cell"] == second
    assert failure["retained_files"]["raw_episodes.jsonl"] == {
        "sha256": runner.sha256(raw), "bytes": len(raw)
    }
    assert raw == runner.canonical(original(first, runner.load_protocol()))

from __future__ import annotations

import json

import pytest

from sparkbrain.replay import load_trace
from sparkbrain.serialization import dump_state, load_state, state_hash
from sparkbrain.visualizer import write_trace
from sparkbrain.worlds import SwitchWorld, run_scenario


def test_state_round_trip_has_identical_canonical_hash(tmp_path) -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:3])
    before = state_hash(brain)
    path = dump_state(brain, tmp_path / "checkpoint.json")
    restored = load_state(path)
    assert state_hash(restored) == before
    assert restored.prediction == brain.prediction


def test_checkpoint_continuation_is_deterministic(tmp_path) -> None:
    events = SwitchWorld.canonical_scenario()
    original, _ = run_scenario(events[:3])
    restored = load_state(dump_state(original, tmp_path / "checkpoint.json"))

    original, original_frames = run_scenario(events[3:], brain=original)
    restored, restored_frames = run_scenario(events[3:], brain=restored)

    assert [frame.prediction for frame in restored_frames] == [
        frame.prediction for frame in original_frames
    ]
    assert state_hash(restored) == state_hash(original)


def test_json_checkpoint_contains_no_infinity(tmp_path) -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:1])
    path = dump_state(brain, tmp_path / "checkpoint.json")
    text = path.read_text(encoding="utf-8")
    assert "Infinity" not in text
    json.loads(text, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def test_unsupported_state_schema_is_rejected(tmp_path) -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:1])
    payload = brain.state_dict()
    payload["schema_version"] = "999"
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported state schema"):
        load_state(path)


def test_trace_replay_is_dynamics_free(tmp_path) -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario())
    path = write_trace(brain, tmp_path / "trace.json")
    replay = load_trace(path)
    assert len(replay.frames) == 7
    assert replay.final_prediction == "cat"
    assert replay.frame(0)["prediction"] is None


def test_unsupported_trace_schema_is_rejected(tmp_path) -> None:
    path = tmp_path / "trace.json"
    path.write_text(
        json.dumps({"schema_version": "999", "graph": {}, "frames": []}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Unsupported trace schema"):
        load_trace(path)

from __future__ import annotations

import json
from dataclasses import asdict

import pytest

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, Spark, SparkKind
from sparkbrain.protocols import BrainBackend
from sparkbrain.replay import load_trace
from sparkbrain.serialization import (
    canonical_json,
    dump_config,
    dump_state,
    load_config,
    load_state,
    state_hash,
)
from sparkbrain.visualizer import write_trace
from sparkbrain.worlds import SwitchWorld, build_reference_brain, run_scenario


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


def test_fresh_runs_have_identical_normalized_trace() -> None:
    first, _ = run_scenario(SwitchWorld.canonical_scenario())
    second, _ = run_scenario(SwitchWorld.canonical_scenario())

    assert canonical_json([asdict(frame) for frame in first.trace]) == canonical_json(
        [asdict(frame) for frame in second.trace]
    )
    assert state_hash(first) == state_hash(second)


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


def test_config_json_round_trip_is_versioned(tmp_path) -> None:
    config = BrainConfig(ignition_threshold=1.4, random_seed=23)
    path = dump_config(config, tmp_path / "config.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "0.2"
    assert load_config(path) == config


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda payload: payload.pop("schema_version"), "schema_version"),
        (lambda payload: payload.__setitem__("graph", {}), "nodes and edges"),
        (lambda payload: payload.__setitem__("extra", True), "unsupported fields"),
        (lambda payload: payload["frames"][0].pop("stats"), "missing required fields"),
    ],
)
def test_trace_replay_rejects_incomplete_or_unknown_payloads(tmp_path, mutation, message) -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:1])
    path = write_trace(brain, tmp_path / "trace.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutation(payload)
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        load_trace(path)


def test_checkpoint_rejects_missing_or_unknown_control_state() -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:1])
    missing = brain.state_dict()
    missing.pop("stability")
    with pytest.raises(ValueError, match="missing required fields"):
        SparkBrain.from_state_dict(missing)

    unknown = brain.state_dict()
    unknown["untracked_control"] = {}
    with pytest.raises(ValueError, match="unsupported fields"):
        SparkBrain.from_state_dict(unknown)


def test_checkpoint_rejects_invalid_pending_queue_contract() -> None:
    brain = build_reference_brain()
    brain.inject_stimulus(target="sensory:fur", label="fur", time=1.0)
    brain.inject_stimulus(target="sound_meow", label="meow", time=2.0)
    duplicate_sequence = brain.state_dict()
    duplicate_sequence["queue"][1]["sequence"] = duplicate_sequence["queue"][0]["sequence"]
    with pytest.raises(ValueError, match="duplicate sequence"):
        SparkBrain.from_state_dict(duplicate_sequence)

    past_event = brain.state_dict()
    past_event["time"] = 1.5
    with pytest.raises(ValueError, match="must be >="):
        SparkBrain.from_state_dict(past_event)


def test_checkpoint_continuation_preserves_pending_queue_and_rng() -> None:
    brain = build_reference_brain()
    brain.inject_stimulus(target="sensory:fur", label="fur", time=1.0)
    brain.random.random()
    restored = SparkBrain.from_state_dict(brain.state_dict())
    assert restored.random.random() == brain.random.random()

    brain.run()
    restored.run()
    original_frame = brain.snapshot(external_event="queued", truth="cat")
    restored_frame = restored.snapshot(external_event="queued", truth="cat")
    assert asdict(restored_frame) == asdict(original_frame)
    assert state_hash(restored) == state_hash(brain)


def test_reset_preserves_graph_but_clears_episode_state() -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:2])
    weights_before = [(edge.source, edge.target, edge.weight) for edge in brain.connections]
    brain.reset(seed=19)
    assert isinstance(brain, BrainBackend)
    assert [(edge.source, edge.target, edge.weight) for edge in brain.connections] == weights_before
    assert brain.time == 0.0
    assert brain.stats.events_processed == 0
    assert brain.workspace == []
    assert brain.ignitions == []
    assert brain.trace == []
    assert all(spark.activation == 0.0 for spark in brain.sparks.values())
    assert brain.random.random() == SparkBrain(BrainConfig(random_seed=19)).random.random()


def test_load_state_dict_replaces_an_existing_engine_instance() -> None:
    source, _ = run_scenario(SwitchWorld.canonical_scenario()[:2])
    target = SparkBrain()
    target.add_spark(Spark("other", "other", SparkKind.SENSORY, "perception"))
    target.load_state_dict(source.state_dict())
    assert state_hash(target) == state_hash(source)


def test_state_dict_and_snapshot_do_not_change_future_dynamics() -> None:
    events = SwitchWorld.canonical_scenario()
    reference, _ = run_scenario(events[:2])
    inspected, _ = run_scenario(events[:2])
    before = state_hash(inspected)
    inspected.state_dict()
    assert state_hash(inspected) == before
    inspected.snapshot(external_event="inspection", truth="cat")

    reference, reference_frames = run_scenario(events[2:], brain=reference)
    inspected, inspected_frames = run_scenario(events[2:], brain=inspected)
    assert [asdict(frame) for frame in inspected_frames] == [
        asdict(frame) for frame in reference_frames
    ]
    assert inspected.ignitions == reference.ignitions
    assert inspected.stats == reference.stats

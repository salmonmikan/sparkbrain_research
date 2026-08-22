# ruff: noqa: E402 -- skip the optional learned suite before importing its modules.
from __future__ import annotations

import json
import math
from dataclasses import asdict, replace

import pytest

torch = pytest.importorskip("torch")

from sparkbrain.learned.backend import LearnedBrainBackend
from sparkbrain.learned.checkpoint import load_checkpoint, save_checkpoint
from sparkbrain.learned.config import LearnedConfig
from sparkbrain.learned.experiment import ABLATIONS
from sparkbrain.learned.model import SparseRoutingModel, stable_bucket
from sparkbrain.learned.training import (
    calibrate_ignition,
    episode_examples,
    evaluate_model,
    train_model,
)
from sparkbrain.model import EventKind
from sparkbrain.protocols import BrainBackend
from sparkbrain.tasks import generate_episode


def small_config(**changes) -> LearnedConfig:
    values = {
        "event_dim": 12,
        "hidden_dim": 10,
        "module_count": 6,
        "active_k": 2,
        "epochs": 1,
        "train_episodes": 2,
        "calibration_episodes": 1,
        "test_episodes": 2,
        "steps": 6,
        **changes,
    }
    return replace(LearnedConfig(), **values)


def inject(backend: LearnedBrainBackend, evidence: str = "meow") -> None:
    backend.schedule(
        time=1.0,
        kind=EventKind.STIMULUS,
        source="sensor:test",
        target=None,
        strength=1.0,
        evidence_id="e:1",
        evidence_label=evidence,
        metadata={"channel": "evidence", "delivery_delay": 0.0},
    )
    backend.run()


def test_optional_backend_satisfies_c01_protocol_and_separates_action() -> None:
    backend = LearnedBrainBackend(small_config(confidence_threshold=0.0, margin_threshold=0.0))
    assert isinstance(backend, BrainBackend)
    inject(backend)
    assert backend.prediction in backend.learned_config.labels
    assert backend.action in backend.learned_config.labels
    assert backend.model.belief_head is not backend.model.action_head


def test_top_k_is_bounded_and_sparse_work_is_counted() -> None:
    config = small_config(active_k=2, module_count=7)
    backend = LearnedBrainBackend(config)
    inject(backend)
    record = backend.prediction_record()
    assert len(record.selected_modules) == 2
    assert len(record.evidence_path) == 4
    assert backend.work.state_updates == 2
    assert backend.work.evaluated_edges == 4
    assert backend.work.conceptual_candidates == 7
    assert backend.work.dense_tensor_ops == 2


def test_dense_ablation_is_labeled_and_executes_more_edges() -> None:
    config = small_config(condition="dense_recurrent")
    backend = LearnedBrainBackend(config)
    inject(backend)
    assert backend.work.selected_modules == config.module_count
    assert backend.work.evaluated_edges == config.module_count**2


def test_trace_explains_modules_paths_coalition_and_no_ignition() -> None:
    config = small_config(confidence_threshold=1.0, margin_threshold=1.0)
    backend = LearnedBrainBackend(config)
    inject(backend)
    frame = backend.snapshot(external_event="meow", truth="cat")
    assert frame.prediction is None
    assert sum(bool(row["selected"]) for row in frame.sparks) == config.active_k
    assert len(frame.active_edges) == config.active_k**2
    assert {"support", "diversity", "stability", "contradiction", "score"} <= set(
        frame.coalitions[0]
    )


def test_runtime_state_round_trip_preserves_continuation() -> None:
    config = small_config(confidence_threshold=0.0, margin_threshold=0.0)
    original = LearnedBrainBackend(config)
    inject(original, "fur")
    payload = json.loads(json.dumps(original.state_dict()))
    restored = LearnedBrainBackend(config)
    restored.load_state_dict(payload)
    for backend in (original, restored):
        backend.schedule(
            time=2.0,
            kind=EventKind.STIMULUS,
            source="sensor:test",
            target=None,
            evidence_id="e:2",
            evidence_label="bark",
            strength=1.0,
        )
        backend.run()
    assert restored.prediction_record().probabilities == pytest.approx(
        original.prediction_record().probabilities
    )


def test_pending_queue_and_trace_survive_runtime_checkpoint() -> None:
    config = small_config(confidence_threshold=0.0, margin_threshold=0.0)
    original = LearnedBrainBackend(config)
    inject(original, "fur")
    original.snapshot(external_event="fur", truth="cat")
    original.schedule(
        time=2.0,
        kind=EventKind.STIMULUS,
        source="sensor:test",
        target=None,
        evidence_id="e:pending",
        evidence_label="bark",
        strength=1.0,
    )
    original.schedule(
        time=2.0,
        kind=EventKind.STIMULUS,
        source="sensor:second",
        target=None,
        evidence_id="e:pending:second",
        evidence_label="plastic_seam",
        strength=1.0,
    )
    payload = json.loads(json.dumps(original.state_dict()))
    restored = LearnedBrainBackend(config)
    restored.load_state_dict(payload)
    assert restored.prediction_record().probabilities == pytest.approx(
        original.prediction_record().probabilities
    )
    assert len(restored.trace) == 1
    for backend in (original, restored):
        backend.schedule(
            time=2.0,
            kind=EventKind.STIMULUS,
            source="sensor:third",
            target=None,
            evidence_id="e:pending:third",
            evidence_label="meow",
            strength=1.0,
        )
    assert [item.sequence for item in sorted(restored._queue)] == [1, 2, 3]
    original.run()
    restored.run()
    assert restored.prediction_record().probabilities == pytest.approx(
        original.prediction_record().probabilities
    )
    assert restored.prediction_record() == original.prediction_record()
    original_work = original.work.to_dict()
    restored_work = restored.work.to_dict()
    original_work.pop("wall_clock_seconds")
    restored_work.pop("wall_clock_seconds")
    assert restored_work == original_work
    original_frame = asdict(original.inspect_snapshot(external_event="same", truth="cat"))
    restored_frame = asdict(restored.inspect_snapshot(external_event="same", truth="cat"))
    original_frame["stats"].pop("wall_clock_seconds")
    restored_frame["stats"].pop("wall_clock_seconds")
    assert restored_frame == original_frame


@pytest.mark.parametrize(
    ("field", "value"),
    (("time", math.inf), ("time", math.nan), ("strength", math.inf), ("priority", True)),
)
def test_schedule_rejects_invalid_event_fields(field, value) -> None:
    backend = LearnedBrainBackend(small_config())
    values = {
        "time": 1.0,
        "kind": EventKind.STIMULUS,
        "source": "sensor:test",
        "target": None,
        "strength": 1.0,
        "priority": 10,
    }
    values[field] = value
    with pytest.raises(ValueError):
        backend.schedule(**values)


def test_schedule_rejects_past_and_load_rejects_duplicate_sequence() -> None:
    backend = LearnedBrainBackend(small_config())
    inject(backend)
    with pytest.raises(ValueError, match="past"):
        backend.schedule(
            time=0.5,
            kind=EventKind.STIMULUS,
            source="sensor:test",
            target=None,
        )
    backend.schedule(
        time=2.0,
        kind=EventKind.STIMULUS,
        source="sensor:a",
        target=None,
    )
    backend.schedule(
        time=2.0,
        kind=EventKind.STIMULUS,
        source="sensor:b",
        target=None,
    )
    payload = backend.state_dict()
    payload["queue"][1]["sequence"] = payload["queue"][0]["sequence"]
    with pytest.raises(ValueError, match="unique"):
        LearnedBrainBackend(small_config()).load_state_dict(payload)


def test_checkpoint_inference_round_trip(tmp_path) -> None:
    config = small_config()
    model = SparseRoutingModel(config)
    path = tmp_path / "learned.pt"
    save_checkpoint(path, config=config, model=model, metadata={"seed": config.seed})
    loaded_config, loaded_model, metadata = load_checkpoint(path)
    assert loaded_config == config
    assert metadata == {"seed": config.seed}
    assert set(model.state_dict()) == set(loaded_model.state_dict())


def test_training_seed_is_reproducible_and_does_not_use_hand_authored_weights() -> None:
    config = small_config()
    episodes = [
        generate_episode("switchworld", seed=100000 + index, split="dev", steps=6)
        for index in range(2)
    ]
    first, history_a = train_model(config, episodes)
    second, history_b = train_model(config, episodes)
    assert history_a == history_b
    for key, value in first.state_dict().items():
        assert torch.equal(value, second.state_dict()[key])
    import sparkbrain.learned.training as training_module

    assert "EVIDENCE_WEIGHTS" not in training_module.__dict__


def test_dev_calibration_is_noncollapsed_and_evaluation_reports_load() -> None:
    config = small_config(epochs=2)
    train = [generate_episode("switchworld", seed=100000, split="dev", steps=8)]
    calibration = [generate_episode("goal_conflict_world", seed=100010, split="dev", steps=8)]
    test = [generate_episode("delayed_evidence_world", seed=200000, split="test", steps=8)]
    model, _ = train_model(config, train)
    calibrated = calibrate_ignition(config, model, calibration)
    summary, rows, _ = evaluate_model(calibrated, model, test)
    assert 0.0 < summary.coverage < 1.0
    assert len(summary.module_loads) == config.module_count
    assert all(len(row["selected_modules"]) == config.active_k for row in rows)


def test_required_ablation_names_are_complete() -> None:
    assert set(ABLATIONS) == {
        "full",
        "dense_recurrent",
        "no_persistent_state",
        "no_residual",
        "no_coalition_score",
        "forced_prediction",
        "random_router",
        "learned_router_no_load_balance",
        "no_workspace_broadcast",
        "detached_coalition",
        "end_to_end_coalition",
    }


def test_stable_hash_encoder_is_process_independent() -> None:
    assert stable_bucket("meow", 128) == stable_bucket("meow", 128)
    assert 0 <= stable_bucket("sensor:test", 128) < 128


def test_shared_example_contract_preserves_multi_object_identity() -> None:
    episode = generate_episode("multi_object_world", seed=100000, split="dev", steps=6)
    examples = episode_examples(episode)
    assert [item.object_id for item in examples] == [
        step.observation.object_id for step in episode.steps
    ]

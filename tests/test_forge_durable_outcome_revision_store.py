import inspect
import json

import pytest

from forge_prototypes.durable_outcome_revision_store import (
    DurableCheckpointConflictError,
    DurableCheckpointCorruptError,
    DurableOutcomeRevisionStore,
)
from forge_prototypes.idempotent_outcome_revision_stream import (
    StreamEventConflictError,
)
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)


def base(*rows: tuple[str, float]) -> PredictionPoolSnapshot:
    hypotheses = tuple(
        WeightedHypothesis(value, 5, probability) for value, probability in rows
    )
    probabilities = sorted((row.probability for row in hypotheses), reverse=True)
    confidence = probabilities[0] if probabilities else 0.0
    second = probabilities[1] if len(probabilities) > 1 else 0.0
    return PredictionPoolSnapshot(
        "assembly-1",
        hypotheses,
        None,
        confidence,
        confidence - second,
        True,
        "low_confidence",
    )


def frozen(path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def process_first(store: DurableOutcomeRevisionStore):
    return store.process(
        "evt-000",
        0,
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.0],
        observed_value="later-b",
    )


def test_public_api_adds_only_transport_and_local_store_identity(tmp_path) -> None:
    parameters = set(inspect.signature(DurableOutcomeRevisionStore.process).parameters)
    assert {"event_id", "sequence"} <= parameters
    forbidden = {
        "prediction_error",
        "scope",
        "episode",
        "regime",
        "observed_probability",
        "tail_assignment",
        "truth",
        "evaluator",
    }
    assert not parameters & forbidden
    assert not (tmp_path / "checkpoint.json").exists()


def test_commit_reopen_and_exact_redelivery_are_durable_and_idempotent(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    first = process_first(DurableOutcomeRevisionStore.open(path))
    before_replay = frozen(path)
    stat_before_replay = path.stat()

    reopened = DurableOutcomeRevisionStore.open(path)
    duplicate = process_first(reopened)

    assert first.delivery_action == "processed"
    assert duplicate.delivery_action == "duplicate_replay"
    assert duplicate.duplicate
    assert not duplicate.state_changed
    assert frozen(path) == before_replay
    assert path.stat().st_mtime_ns == stat_before_replay.st_mtime_ns


def test_same_identifier_different_content_after_reopen_fails_closed(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    process_first(DurableOutcomeRevisionStore.open(path))
    before = frozen(path)
    reopened = DurableOutcomeRevisionStore.open(path)

    with pytest.raises(StreamEventConflictError, match="different content"):
        reopened.process(
            "evt-000",
            0,
            base(("later-a", 0.8), ("later-b", 0.2)),
            observation=[0.0],
            observed_value="later-a",
        )

    assert frozen(path) == before
    assert reopened.state_dict()["next_sequence"] == 1


def test_failure_before_replace_preserves_old_checkpoint_and_live_state(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    process_first(DurableOutcomeRevisionStore.open(path))
    before = frozen(path)

    def fail(stage: str) -> None:
        if stage == "after_temp_fsync":
            raise RuntimeError("simulated pre-replace crash")

    store = DurableOutcomeRevisionStore.open(path, fault_hook=fail)
    with pytest.raises(RuntimeError, match="pre-replace"):
        store.process(
            "evt-001",
            1,
            base(("later-a", 0.8), ("later-b", 0.2)),
            observation=[0.05],
            observed_value="later-a",
        )

    assert frozen(path) == before
    assert store.state_dict()["next_sequence"] == 1
    assert not list(tmp_path.glob(".checkpoint.json.*.tmp"))


def test_crash_after_replace_recovers_committed_event_and_safe_redelivery(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    process_first(DurableOutcomeRevisionStore.open(path))

    def fail(stage: str) -> None:
        if stage == "after_replace":
            raise RuntimeError("simulated post-replace crash")

    crashed = DurableOutcomeRevisionStore.open(path, fault_hook=fail)
    with pytest.raises(RuntimeError, match="post-replace"):
        crashed.process(
            "evt-001",
            1,
            base(("later-a", 0.8), ("later-b", 0.2)),
            observation=[0.05],
            observed_value="later-a",
        )

    assert crashed.state_dict()["next_sequence"] == 1
    recovered = DurableOutcomeRevisionStore.open(path)
    assert recovered.state_dict()["next_sequence"] == 2
    duplicate = recovered.process(
        "evt-001",
        1,
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.05],
        observed_value="later-a",
    )
    assert duplicate.duplicate
    assert not duplicate.state_changed


def test_stale_local_writer_cannot_overwrite_newer_checkpoint(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    first_writer = DurableOutcomeRevisionStore.open(path)
    stale_writer = DurableOutcomeRevisionStore.open(path)
    process_first(first_writer)
    after_first = frozen(path)

    with pytest.raises(DurableCheckpointConflictError, match="changed"):
        process_first(stale_writer)

    assert frozen(path) == after_first
    assert stale_writer.state_dict()["next_sequence"] == 0


def test_corrupt_or_torn_checkpoint_fails_closed(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    process_first(DurableOutcomeRevisionStore.open(path))
    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["stream_state"]["next_sequence"] = 99
    path.write_text(json.dumps(envelope), encoding="utf-8")

    with pytest.raises(DurableCheckpointCorruptError, match="digest mismatch"):
        DurableOutcomeRevisionStore.open(path)

    path.write_text("{torn", encoding="utf-8")
    with pytest.raises(DurableCheckpointCorruptError, match="valid JSON"):
        DurableOutcomeRevisionStore.open(path)

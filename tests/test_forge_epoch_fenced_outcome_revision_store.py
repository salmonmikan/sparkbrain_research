import inspect
import json

import pytest

from forge_prototypes.epoch_fenced_outcome_revision_store import (
    EpochCheckpointCorruptError,
    EpochFencedOutcomeRevisionStream,
    EpochRotationConflictError,
    FutureStreamEpochError,
    LockedEpochFencedOutcomeRevisionStore,
    RetiredStreamEpochError,
)
from forge_prototypes.idempotent_outcome_revision_stream import (
    IdempotentOutcomeRevisionStream,
)
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)


def base() -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        "assembly-1",
        (
            WeightedHypothesis("later-a", 5, 0.8),
            WeightedHypothesis("later-b", 5, 0.2),
        ),
        None,
        0.8,
        0.6,
        True,
        "low_confidence",
    )


def process_event(
    store,
    epoch: int,
    sequence: int,
    *,
    event_id: str | None = None,
):
    return store.process(
        epoch,
        event_id or f"evt-{sequence:03d}",
        sequence,
        base(),
        observation=[epoch + sequence * 0.05],
        observed_value="later-b" if sequence % 2 == 0 else "later-a",
    )


def frozen_state(store) -> str:
    return json.dumps(store.state_dict(), sort_keys=True)


def test_public_epoch_is_transport_only_and_semantic_shortcuts_stay_absent() -> None:
    parameters = set(
        inspect.signature(LockedEpochFencedOutcomeRevisionStore.process).parameters
    )
    assert "stream_epoch" in parameters
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


def test_rotation_resets_delivery_filter_but_preserves_revision_state() -> None:
    stream = EpochFencedOutcomeRevisionStream(
        IdempotentOutcomeRevisionStream(receipt_capacity=2)
    )
    for sequence in range(4):
        process_event(stream, 0, sequence)

    before = stream.state_dict()
    assert int(before["stream"]["compacted_event_filter_hex"], 16) != 0
    coordinator_before = before["stream"]["coordinator"]

    digest = stream.rotate_epoch(1, expected_next_sequence=4)
    after = stream.state_dict()
    assert after["current_epoch"] == after["retired_before_epoch"] == 1
    assert after["retired_epoch_chain_sha256"] == digest
    assert len(digest) == 64
    assert after["stream"]["next_sequence"] == 0
    assert after["stream"]["receipts"] == []
    assert after["stream"]["retained_from_sequence"] == 0
    assert after["stream"]["compacted_prefix_sha256"] is None
    assert int(after["stream"]["compacted_event_filter_hex"], 16) == 0
    assert after["stream"]["coordinator"] == coordinator_before

    receipt = process_event(stream, 1, 0, event_id="evt-000")
    assert not receipt.duplicate


def test_retired_and_future_delivery_fail_without_state_change() -> None:
    stream = EpochFencedOutcomeRevisionStream(
        IdempotentOutcomeRevisionStream(receipt_capacity=2)
    )
    process_event(stream, 0, 0)
    stream.rotate_epoch(1, expected_next_sequence=1)
    before = frozen_state(stream)

    with pytest.raises(RetiredStreamEpochError, match="retired"):
        process_event(stream, 0, 0)
    assert frozen_state(stream) == before

    with pytest.raises(FutureStreamEpochError, match="not open"):
        process_event(stream, 2, 0)
    assert frozen_state(stream) == before


def test_rotation_requires_contiguous_epoch_and_fresh_sequence_fence() -> None:
    stream = EpochFencedOutcomeRevisionStream(
        IdempotentOutcomeRevisionStream(receipt_capacity=2)
    )
    process_event(stream, 0, 0)
    before = frozen_state(stream)

    with pytest.raises(EpochRotationConflictError, match="exactly one"):
        stream.rotate_epoch(2, expected_next_sequence=1)
    assert frozen_state(stream) == before

    with pytest.raises(EpochRotationConflictError, match="stream fence"):
        stream.rotate_epoch(1, expected_next_sequence=0)
    assert frozen_state(stream) == before


def test_epoch_state_roundtrip_preserves_fence_and_exact_duplicate() -> None:
    stream = EpochFencedOutcomeRevisionStream(
        IdempotentOutcomeRevisionStream(receipt_capacity=2)
    )
    process_event(stream, 0, 0)
    stream.rotate_epoch(1, expected_next_sequence=1)
    process_event(stream, 1, 0)

    restored = EpochFencedOutcomeRevisionStream.from_state_dict(
        json.loads(json.dumps(stream.state_dict()))
    )
    assert restored.state_dict() == stream.state_dict()
    duplicate = process_event(restored, 1, 0)
    assert duplicate.duplicate
    with pytest.raises(RetiredStreamEpochError):
        process_event(restored, 0, 0)


def test_locked_store_rotation_is_durable_and_visible_to_stale_handle(tmp_path) -> None:
    path = tmp_path / "epoch-checkpoint.json"
    first = LockedEpochFencedOutcomeRevisionStore.open(path, receipt_capacity=2)
    second = LockedEpochFencedOutcomeRevisionStore.open(path, receipt_capacity=2)
    for sequence in range(3):
        process_event(first, 0, sequence)

    first.rotate_epoch(1, expected_next_sequence=3)
    with pytest.raises(RetiredStreamEpochError):
        process_event(second, 0, 0)

    receipt = process_event(second, 1, 0, event_id="evt-000")
    assert not receipt.duplicate
    reopened = LockedEpochFencedOutcomeRevisionStore.open(path)
    state = reopened.state_dict()
    assert state["current_epoch"] == 1
    assert state["stream"]["next_sequence"] == 1
    assert process_event(reopened, 1, 0, event_id="evt-000").duplicate


def test_checkpoint_digest_corruption_fails_closed(tmp_path) -> None:
    path = tmp_path / "epoch-checkpoint.json"
    store = LockedEpochFencedOutcomeRevisionStore.open(path, receipt_capacity=2)
    process_event(store, 0, 0)
    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["checkpoint_sha256"] = "0" * 64
    path.write_text(json.dumps(envelope), encoding="utf-8")

    with pytest.raises(EpochCheckpointCorruptError, match="digest mismatch"):
        store.state_dict()


def test_repeated_rotation_builds_chain_and_keeps_checkpoint_bounded(tmp_path) -> None:
    path = tmp_path / "epoch-checkpoint.json"
    store = LockedEpochFencedOutcomeRevisionStore.open(path, receipt_capacity=2)
    digests = []
    for epoch in range(3):
        for sequence in range(3):
            process_event(store, epoch, sequence)
        digests.append(
            store.rotate_epoch(epoch + 1, expected_next_sequence=3)
        )

    state = store.state_dict()
    assert len(set(digests)) == 3
    assert state["current_epoch"] == 3
    assert state["retired_epoch_chain_sha256"] == digests[-1]
    assert state["stream"]["receipts"] == []
    assert state["stream"]["receipt_capacity"] == 2
    assert path.stat().st_size < 100_000

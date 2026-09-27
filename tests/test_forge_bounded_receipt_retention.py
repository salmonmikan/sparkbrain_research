import inspect
import json

import pytest

from forge_prototypes.durable_outcome_revision_store import (
    DurableOutcomeRevisionStore,
    ReceiptCapacityMismatchError,
)
from forge_prototypes.idempotent_outcome_revision_stream import (
    CompactedEventIdentityError,
    CompactedReceiptUnavailableError,
    IdempotentOutcomeRevisionStream,
)
from forge_prototypes.locked_outcome_revision_store import LockedOutcomeRevisionStore
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)


def base() -> PredictionPoolSnapshot:
    hypotheses = (
        WeightedHypothesis("later-a", 5, 0.8),
        WeightedHypothesis("later-b", 5, 0.2),
    )
    return PredictionPoolSnapshot(
        "assembly-1", hypotheses, None, 0.8, 0.6, True, "low_confidence"
    )


def process_event(store, sequence: int, *, event_id: str | None = None):
    return store.process(
        event_id or f"evt-{sequence:03d}",
        sequence,
        base(),
        observation=[sequence * 0.05],
        observed_value="later-b" if sequence % 2 == 0 else "later-a",
    )


def frozen_state(store) -> str:
    return json.dumps(store.state_dict(), sort_keys=True)


def test_public_api_exposes_only_storage_retention_not_science_inputs() -> None:
    open_parameters = set(inspect.signature(LockedOutcomeRevisionStore.open).parameters)
    process_parameters = set(
        inspect.signature(LockedOutcomeRevisionStore.process).parameters
    )
    assert "receipt_capacity" in open_parameters
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
    assert not process_parameters & forbidden


def test_receipt_ledger_is_bounded_and_retained_replay_remains_exact() -> None:
    stream = IdempotentOutcomeRevisionStream(receipt_capacity=2)
    for sequence in range(5):
        process_event(stream, sequence)

    state = stream.state_dict()
    assert state["next_sequence"] == 5
    assert state["retained_from_sequence"] == 3
    assert [row["sequence"] for row in state["receipts"]] == [3, 4]
    assert len(state["receipts"]) == state["receipt_capacity"] == 2
    assert len(state["compacted_prefix_sha256"]) == 64
    assert int(state["compacted_event_filter_hex"], 16) != 0

    duplicate = process_event(stream, 4)
    assert duplicate.duplicate
    assert duplicate.delivery_action == "duplicate_replay"


def test_compacted_replay_and_identifier_reuse_fail_without_mutation() -> None:
    stream = IdempotentOutcomeRevisionStream(receipt_capacity=2)
    for sequence in range(4):
        process_event(stream, sequence)
    before = frozen_state(stream)

    with pytest.raises(CompactedReceiptUnavailableError, match="predates"):
        process_event(stream, 0)
    assert frozen_state(stream) == before

    with pytest.raises(CompactedEventIdentityError, match="compacted history"):
        process_event(stream, 4, event_id="evt-000")
    assert frozen_state(stream) == before


def test_roundtrip_preserves_retention_horizon_and_conservative_filter() -> None:
    stream = IdempotentOutcomeRevisionStream(receipt_capacity=2)
    for sequence in range(4):
        process_event(stream, sequence)

    restored = IdempotentOutcomeRevisionStream.from_state_dict(
        json.loads(json.dumps(stream.state_dict()))
    )
    assert restored.state_dict() == stream.state_dict()
    with pytest.raises(CompactedReceiptUnavailableError):
        process_event(restored, 1)
    with pytest.raises(CompactedEventIdentityError):
        process_event(restored, 4, event_id="evt-001")
    process_event(restored, 4)
    assert restored.state_dict()["retained_from_sequence"] == 3


def test_locked_store_reopens_with_bounded_ledger_and_rejects_reconfiguration(
    tmp_path,
) -> None:
    path = tmp_path / "checkpoint.json"
    store = LockedOutcomeRevisionStore.open(path, receipt_capacity=2)
    for sequence in range(4):
        process_event(store, sequence)

    reopened = LockedOutcomeRevisionStore.open(path)
    state = reopened.state_dict()
    assert state["receipt_capacity"] == 2
    assert state["retained_from_sequence"] == 2
    assert [row["sequence"] for row in state["receipts"]] == [2, 3]
    assert process_event(reopened, 3).duplicate
    with pytest.raises(CompactedReceiptUnavailableError):
        process_event(reopened, 0)

    with pytest.raises(ReceiptCapacityMismatchError, match="does not match"):
        DurableOutcomeRevisionStore.open(path, receipt_capacity=3)


def test_legacy_unbounded_checkpoint_migrates_without_implicit_compaction() -> None:
    stream = IdempotentOutcomeRevisionStream()
    process_event(stream, 0)
    legacy = stream.state_dict()
    legacy["schema_version"] = 1
    for field in (
        "receipt_capacity",
        "retained_from_sequence",
        "compacted_prefix_sha256",
        "compacted_event_filter_hex",
    ):
        legacy.pop(field)

    restored = IdempotentOutcomeRevisionStream.from_state_dict(legacy)
    state = restored.state_dict()
    assert state["receipt_capacity"] is None
    assert state["retained_from_sequence"] == 0
    assert process_event(restored, 0).duplicate

import inspect
import json

import pytest

from forge_prototypes.idempotent_outcome_revision_stream import (
    IdempotentOutcomeRevisionStream,
    StreamEventConflictError,
    StreamSequenceError,
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


def frozen_state(stream: IdempotentOutcomeRevisionStream) -> str:
    return json.dumps(stream.state_dict(), sort_keys=True)


def test_public_api_adds_delivery_identity_without_privileged_science_inputs() -> None:
    parameters = set(inspect.signature(IdempotentOutcomeRevisionStream.process).parameters)
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


def test_contiguous_events_advance_stream_and_coordinator_state() -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))

    first = stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    second = stream.process(
        "evt-001", 1, prediction, observation=[0.05], observed_value="later-a"
    )

    assert first.delivery_action == "processed"
    assert first.committed and first.state_changed
    assert second.delivery_action == "processed"
    assert stream.state_dict()["next_sequence"] == 2
    assert [row["event_id"] for row in stream.state_dict()["receipts"]] == [
        "evt-000",
        "evt-001",
    ]


def test_exact_redelivery_returns_receipt_without_second_mutation() -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))
    first = stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    after_first = frozen_state(stream)

    duplicate = stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )

    assert duplicate.payload_sha256 == first.payload_sha256
    assert duplicate.outcome_action == first.outcome_action
    assert duplicate.committed == first.committed
    assert duplicate.duplicate
    assert not duplicate.state_changed
    assert duplicate.delivery_action == "duplicate_replay"
    assert frozen_state(stream) == after_first


def test_same_event_id_with_different_content_fails_closed() -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))
    stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    before = frozen_state(stream)

    with pytest.raises(StreamEventConflictError, match="different content"):
        stream.process(
            "evt-000", 0, prediction, observation=[0.0], observed_value="later-a"
        )

    assert frozen_state(stream) == before


@pytest.mark.parametrize("sequence", [0, 2])
def test_new_stale_or_gapped_event_fails_without_mutation(sequence: int) -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))
    stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    before = frozen_state(stream)

    with pytest.raises(StreamSequenceError, match="does not match next 1"):
        stream.process(
            f"evt-{sequence}",
            sequence,
            prediction,
            observation=[0.05],
            observed_value="later-a",
        )

    assert frozen_state(stream) == before


def test_no_write_event_is_ledgered_and_never_re_evaluated_after_state_changes() -> None:
    stream = IdempotentOutcomeRevisionStream()
    omitted = base(("later-a", 0.6), ("later-b", 0.3))
    no_write = stream.process(
        "evt-000", 0, omitted, observation=[0.0], observed_value="later-c"
    )
    assert not no_write.committed
    assert not no_write.state_changed

    stream.process(
        "evt-001",
        1,
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.0],
        observed_value="later-b",
    )
    before_replay = frozen_state(stream)

    replay = stream.process(
        "evt-000", 0, omitted, observation=[0.0], observed_value="later-c"
    )

    assert replay.duplicate
    assert replay.outcome_action == no_write.outcome_action
    assert frozen_state(stream) == before_replay


def test_failed_payload_does_not_consume_sequence_or_event_id() -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))
    before = frozen_state(stream)

    with pytest.raises(ValueError, match="strength must be finite"):
        stream.process(
            "evt-000",
            0,
            prediction,
            observation=[0.0],
            observed_value="later-a",
            strength=float("nan"),
        )

    assert frozen_state(stream) == before
    accepted = stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-a"
    )
    assert accepted.delivery_action == "processed"
    assert stream.state_dict()["next_sequence"] == 1


def test_checkpoint_roundtrip_preserves_deduplication_and_next_event() -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))
    stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    state = json.loads(json.dumps(stream.state_dict()))
    restored = IdempotentOutcomeRevisionStream.from_state_dict(state)

    duplicate = restored.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    next_event = restored.process(
        "evt-001", 1, prediction, observation=[0.05], observed_value="later-a"
    )

    assert duplicate.duplicate
    assert not duplicate.state_changed
    assert next_event.delivery_action == "processed"
    assert restored.state_dict()["next_sequence"] == 2


def test_checkpoint_rejects_non_contiguous_receipt_ledger() -> None:
    stream = IdempotentOutcomeRevisionStream()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))
    stream.process(
        "evt-000", 0, prediction, observation=[0.0], observed_value="later-b"
    )
    state = stream.state_dict()
    state["receipts"][0]["sequence"] = 2

    with pytest.raises(ValueError, match="not contiguous"):
        IdempotentOutcomeRevisionStream.from_state_dict(state)

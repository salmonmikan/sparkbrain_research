import fcntl
import inspect
import multiprocessing
import os

import pytest

from forge_prototypes.locked_outcome_revision_store import (
    LocalStoreLockTimeoutError,
    LockedOutcomeRevisionStore,
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


def process_event(store, event_id: str, sequence: int, observed_value: str):
    return store.process(
        event_id,
        sequence,
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[sequence * 0.05],
        observed_value=observed_value,
    )


def concurrent_redelivery_worker(path: str, start, results) -> None:
    store = LockedOutcomeRevisionStore.open(path)
    start.wait()
    try:
        receipt = process_event(store, "evt-000", 0, "later-b")
        results.put(("ok", receipt.delivery_action, receipt.duplicate))
    except Exception as exc:  # pragma: no cover - surfaced to parent assertion
        results.put(("error", type(exc).__name__, str(exc)))


def test_public_api_adds_only_transport_and_local_store_identity(tmp_path) -> None:
    parameters = set(inspect.signature(LockedOutcomeRevisionStore.process).parameters)
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


def test_instances_opened_before_first_write_reload_under_lock(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    first = LockedOutcomeRevisionStore.open(path)
    second = LockedOutcomeRevisionStore.open(path)

    receipt_0 = process_event(first, "evt-000", 0, "later-b")
    receipt_1 = process_event(second, "evt-001", 1, "later-a")

    assert receipt_0.delivery_action == "processed"
    assert receipt_1.delivery_action == "processed"
    assert second.state_dict()["next_sequence"] == 2


def test_two_process_exact_redelivery_is_applied_once(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    context = multiprocessing.get_context("spawn")
    start = context.Event()
    results = context.Queue()
    workers = [
        context.Process(
            target=concurrent_redelivery_worker,
            args=(str(path), start, results),
        )
        for _ in range(2)
    ]
    for worker in workers:
        worker.start()
    start.set()
    observed = [results.get(timeout=10) for _ in workers]
    for worker in workers:
        worker.join(timeout=10)
        assert worker.exitcode == 0

    assert sorted(observed) == [
        ("ok", "duplicate_replay", True),
        ("ok", "processed", False),
    ]
    assert LockedOutcomeRevisionStore.open(path).state_dict()["next_sequence"] == 1


def test_lock_timeout_fails_without_creating_checkpoint(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"
    lock_path = tmp_path / ".checkpoint.json.lock"
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(descriptor, fcntl.LOCK_EX)
    try:
        store = LockedOutcomeRevisionStore.open(path, lock_timeout_seconds=0.02)
        with pytest.raises(LocalStoreLockTimeoutError, match="timed out"):
            process_event(store, "evt-000", 0, "later-b")
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)

    assert not path.exists()


def test_post_replace_uncertain_commit_recovers_with_locked_redelivery(tmp_path) -> None:
    path = tmp_path / "checkpoint.json"

    def fail(stage: str) -> None:
        if stage == "after_replace":
            raise RuntimeError("simulated post-replace crash")

    crashed = LockedOutcomeRevisionStore.open(path, fault_hook=fail)
    with pytest.raises(RuntimeError, match="post-replace"):
        process_event(crashed, "evt-000", 0, "later-b")

    recovered = LockedOutcomeRevisionStore.open(path)
    duplicate = process_event(recovered, "evt-000", 0, "later-b")
    assert duplicate.delivery_action == "duplicate_replay"
    assert duplicate.duplicate
    assert recovered.state_dict()["next_sequence"] == 1

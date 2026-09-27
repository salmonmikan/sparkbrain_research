from __future__ import annotations

import errno
import fcntl
import os
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from forge_prototypes.durable_outcome_revision_store import (
    DurableOutcomeRevisionStore,
    FaultHook,
)
from forge_prototypes.idempotent_outcome_revision_stream import StreamEventReceipt
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


class LocalStoreLockTimeoutError(TimeoutError):
    """Raised when the local writer lock is not acquired in the allowed time."""


class LockedOutcomeRevisionStore:
    """Serialize cooperating local processes around a durable outcome store.

    The lock file has a stable path and is never replaced.  Each operation takes
    an exclusive POSIX advisory lock, reloads the checkpoint while holding that
    lock, applies at most one event, and releases the lock only after the durable
    store has completed its atomic replacement and directory flush.

    Reloading inside the critical section is important: two instances may have
    been opened from the same old checkpoint, but the second writer still sees
    the first writer's receipt ledger before evaluating its event.

    This is ordinary single-host file locking around an atomic snapshot.  It is
    not distributed consensus, a remote-store transaction, a learning
    mechanism, or scientific evidence.  Every writer must cooperate by using
    the same lock path.
    """

    def __init__(
        self,
        path: Path,
        *,
        receipt_capacity: int | None,
        lock_timeout_seconds: float | None,
        fault_hook: FaultHook | None,
    ) -> None:
        self._path = path
        self._lock_path = path.with_name(f".{path.name}.lock")
        self._lock_timeout_seconds = self._validate_timeout(lock_timeout_seconds)
        self._receipt_capacity = receipt_capacity
        self._fault_hook = fault_hook

    @classmethod
    def open(
        cls,
        path: str | os.PathLike[str],
        *,
        receipt_capacity: int | None = None,
        lock_timeout_seconds: float | None = 5.0,
        fault_hook: FaultHook | None = None,
    ) -> LockedOutcomeRevisionStore:
        return cls(
            Path(path),
            receipt_capacity=receipt_capacity,
            lock_timeout_seconds=lock_timeout_seconds,
            fault_hook=fault_hook,
        )

    @staticmethod
    def _validate_timeout(value: float | None) -> float | None:
        if value is None:
            return None
        timeout = float(value)
        if timeout < 0:
            raise ValueError("lock_timeout_seconds must be non-negative or None")
        return timeout

    def _acquire_lock(self) -> int:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(self._lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        if self._lock_timeout_seconds is None:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            return descriptor

        deadline = time.monotonic() + self._lock_timeout_seconds
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return descriptor
            except OSError as exc:
                if exc.errno not in (errno.EACCES, errno.EAGAIN):
                    os.close(descriptor)
                    raise
                if time.monotonic() >= deadline:
                    os.close(descriptor)
                    raise LocalStoreLockTimeoutError(
                        "timed out waiting for the local outcome-store writer lock"
                    ) from exc
                time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))

    @staticmethod
    def _release_lock(descriptor: int) -> None:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)

    def process(
        self,
        event_id: str,
        sequence: int,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        observed_value: str,
        strength: float = 1.0,
    ) -> StreamEventReceipt:
        descriptor = self._acquire_lock()
        try:
            fresh = DurableOutcomeRevisionStore.open(
                self._path,
                receipt_capacity=self._receipt_capacity,
                fault_hook=self._fault_hook,
            )
            return fresh.process(
                event_id,
                sequence,
                base,
                observation=observation,
                observed_value=observed_value,
                strength=strength,
            )
        finally:
            self._release_lock(descriptor)

    def state_dict(self) -> dict[str, Any]:
        descriptor = self._acquire_lock()
        try:
            return DurableOutcomeRevisionStore.open(
                self._path,
                receipt_capacity=self._receipt_capacity,
            ).state_dict()
        finally:
            self._release_lock(descriptor)


__all__ = [
    "LocalStoreLockTimeoutError",
    "LockedOutcomeRevisionStore",
]

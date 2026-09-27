from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import os
import tempfile
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from forge_prototypes.idempotent_outcome_revision_stream import (
    IdempotentOutcomeRevisionStream,
    StreamEventReceipt,
)
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


class RetiredStreamEpochError(ValueError):
    """Raised when delivery targets an epoch that has already been fenced."""


class FutureStreamEpochError(ValueError):
    """Raised when delivery targets an epoch that has not been opened."""


class EpochRotationConflictError(ValueError):
    """Raised when an epoch rotation does not match the observed stream fence."""


class EpochCheckpointCorruptError(ValueError):
    """Raised when the epoch checkpoint or its digest is invalid."""


class EpochStoreLockTimeoutError(TimeoutError):
    """Raised when the cooperating local-writer lock cannot be acquired."""


class EpochFencedOutcomeRevisionStream:
    """Fence compacted delivery history behind explicit transport epochs.

    Rotation preserves the revision coordinator but starts a new delivery
    namespace with sequence zero, an empty exact-receipt window, and a fresh
    conservative identity filter.  Every earlier epoch is rejected wholesale,
    so old delivery cannot be mistaken for a new event after the filter reset.

    ``stream_epoch`` is transport metadata only.  It must not encode scope,
    regime, episode, target, truth, or evaluator identity.  This is ordinary
    epoch fencing and log rotation, not a learning or memory mechanism.
    """

    _SCHEMA_VERSION = 1
    _FILTER_HEX_LENGTH = 2048 // 4

    def __init__(
        self,
        stream: IdempotentOutcomeRevisionStream | None = None,
        *,
        current_epoch: int = 0,
        retired_epoch_chain_sha256: str | None = None,
    ) -> None:
        self._validate_epoch(current_epoch, "current_epoch")
        if current_epoch == 0:
            if retired_epoch_chain_sha256 is not None:
                raise ValueError("epoch zero cannot have retired epoch history")
        elif not self._valid_digest(retired_epoch_chain_sha256):
            raise ValueError("rotated stream requires a retired epoch chain digest")
        self._stream = stream or IdempotentOutcomeRevisionStream()
        self._current_epoch = current_epoch
        self._retired_epoch_chain_sha256 = retired_epoch_chain_sha256

    @staticmethod
    def _validate_epoch(value: int, name: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")

    @staticmethod
    def _valid_digest(value: object) -> bool:
        return bool(
            isinstance(value, str)
            and len(value) == 64
            and all(character in "0123456789abcdef" for character in value)
        )

    @staticmethod
    def _canonical_bytes(value: dict[str, Any]) -> bytes:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    def _require_current_epoch(self, stream_epoch: int) -> None:
        self._validate_epoch(stream_epoch, "stream_epoch")
        if stream_epoch < self._current_epoch:
            raise RetiredStreamEpochError(
                f"stream epoch {stream_epoch} is retired; current epoch is "
                f"{self._current_epoch}"
            )
        if stream_epoch > self._current_epoch:
            raise FutureStreamEpochError(
                f"stream epoch {stream_epoch} is not open; current epoch is "
                f"{self._current_epoch}"
            )

    def process(
        self,
        stream_epoch: int,
        event_id: str,
        sequence: int,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        observed_value: str,
        strength: float = 1.0,
    ) -> StreamEventReceipt:
        self._require_current_epoch(stream_epoch)
        return self._stream.process(
            event_id,
            sequence,
            base,
            observation=observation,
            observed_value=observed_value,
            strength=strength,
        )

    def rotate_epoch(
        self,
        next_epoch: int,
        *,
        expected_next_sequence: int,
    ) -> str:
        self._validate_epoch(next_epoch, "next_epoch")
        if next_epoch != self._current_epoch + 1:
            raise EpochRotationConflictError(
                "next_epoch must advance the current epoch by exactly one"
            )
        stream_state = self._stream.state_dict()
        if expected_next_sequence != stream_state["next_sequence"]:
            raise EpochRotationConflictError(
                "expected_next_sequence does not match the current stream fence"
            )

        retirement_record = {
            "epoch": self._current_epoch,
            "stream_state": stream_state,
        }
        previous = bytes.fromhex(self._retired_epoch_chain_sha256 or "00" * 32)
        retired_digest = hashlib.sha256(
            previous + b"\n" + self._canonical_bytes(retirement_record)
        ).hexdigest()

        reset_state = {
            "schema_version": stream_state["schema_version"],
            "next_sequence": 0,
            "coordinator": stream_state["coordinator"],
            "receipts": [],
            "receipt_capacity": stream_state["receipt_capacity"],
            "retained_from_sequence": 0,
            "compacted_prefix_sha256": None,
            "compacted_event_filter_hex": "0" * self._FILTER_HEX_LENGTH,
        }
        self._stream = IdempotentOutcomeRevisionStream.from_state_dict(reset_state)
        self._current_epoch = next_epoch
        self._retired_epoch_chain_sha256 = retired_digest
        return retired_digest

    def state_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self._SCHEMA_VERSION,
            "current_epoch": self._current_epoch,
            "retired_before_epoch": self._current_epoch,
            "retired_epoch_chain_sha256": self._retired_epoch_chain_sha256,
            "stream": self._stream.state_dict(),
        }

    @classmethod
    def from_state_dict(
        cls, state: dict[str, Any]
    ) -> EpochFencedOutcomeRevisionStream:
        if state.get("schema_version") != cls._SCHEMA_VERSION:
            raise ValueError("unsupported epoch stream checkpoint schema_version")
        current_epoch = state.get("current_epoch")
        cls._validate_epoch(current_epoch, "current_epoch")
        if state.get("retired_before_epoch") != current_epoch:
            raise ValueError("retired epoch fence does not match current_epoch")
        stream_state = state.get("stream")
        if not isinstance(stream_state, dict):
            raise ValueError("epoch stream checkpoint is missing stream state")
        return cls(
            IdempotentOutcomeRevisionStream.from_state_dict(stream_state),
            current_epoch=current_epoch,
            retired_epoch_chain_sha256=state.get("retired_epoch_chain_sha256"),
        )


class LockedEpochFencedOutcomeRevisionStore:
    """Persist an epoch-fenced stream with one cooperating POSIX writer lock."""

    _CHECKPOINT_SCHEMA_VERSION = 1

    def __init__(
        self,
        path: Path,
        *,
        receipt_capacity: int | None,
        lock_timeout_seconds: float | None,
    ) -> None:
        self._path = path
        self._lock_path = path.with_name(f".{path.name}.lock")
        self._receipt_capacity = receipt_capacity
        self._lock_timeout_seconds = self._validate_timeout(lock_timeout_seconds)

    @classmethod
    def open(
        cls,
        path: str | os.PathLike[str],
        *,
        receipt_capacity: int | None = None,
        lock_timeout_seconds: float | None = 5.0,
    ) -> LockedEpochFencedOutcomeRevisionStore:
        if receipt_capacity is not None and (
            isinstance(receipt_capacity, bool)
            or not isinstance(receipt_capacity, int)
            or receipt_capacity < 1
        ):
            raise ValueError("receipt_capacity must be a positive integer or None")
        return cls(
            Path(path),
            receipt_capacity=receipt_capacity,
            lock_timeout_seconds=lock_timeout_seconds,
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
                    raise EpochStoreLockTimeoutError(
                        "timed out waiting for the epoch-store writer lock"
                    ) from exc
                time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))

    @staticmethod
    def _release_lock(descriptor: int) -> None:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)

    @staticmethod
    def _canonical_bytes(state: dict[str, Any]) -> bytes:
        return json.dumps(
            state,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    @classmethod
    def _envelope(cls, state: dict[str, Any]) -> bytes:
        digest = hashlib.sha256(cls._canonical_bytes(state)).hexdigest()
        return (
            json.dumps(
                {
                    "schema_version": cls._CHECKPOINT_SCHEMA_VERSION,
                    "checkpoint_sha256": digest,
                    "epoch_stream_state": state,
                },
                allow_nan=False,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )

    @classmethod
    def _read_checkpoint(cls, path: Path) -> EpochFencedOutcomeRevisionStream:
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise EpochCheckpointCorruptError("checkpoint is not valid JSON") from exc
        if envelope.get("schema_version") != cls._CHECKPOINT_SCHEMA_VERSION:
            raise EpochCheckpointCorruptError(
                "unsupported epoch checkpoint schema_version"
            )
        state = envelope.get("epoch_stream_state")
        if not isinstance(state, dict):
            raise EpochCheckpointCorruptError("epoch_stream_state is missing")
        expected = envelope.get("checkpoint_sha256")
        actual = hashlib.sha256(cls._canonical_bytes(state)).hexdigest()
        if expected != actual:
            raise EpochCheckpointCorruptError("epoch checkpoint digest mismatch")
        try:
            return EpochFencedOutcomeRevisionStream.from_state_dict(state)
        except (KeyError, TypeError, ValueError) as exc:
            raise EpochCheckpointCorruptError(
                "epoch stream state is invalid"
            ) from exc

    def _load_locked(self) -> EpochFencedOutcomeRevisionStream:
        if not self._path.exists():
            return EpochFencedOutcomeRevisionStream(
                IdempotentOutcomeRevisionStream(
                    receipt_capacity=self._receipt_capacity
                )
            )
        stream = self._read_checkpoint(self._path)
        stored_capacity = stream.state_dict()["stream"]["receipt_capacity"]
        if (
            self._receipt_capacity is not None
            and self._receipt_capacity != stored_capacity
        ):
            raise ValueError(
                "receipt_capacity does not match the existing epoch checkpoint"
            )
        return stream

    def _replace_checkpoint(self, state: dict[str, Any]) -> None:
        payload = self._envelope(state)
        descriptor, temporary_name = tempfile.mkstemp(
            dir=self._path.parent,
            prefix=f".{self._path.name}.",
            suffix=".tmp",
        )
        temporary_path = Path(temporary_name)
        replaced = False
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, self._path)
            replaced = True
            directory_fd = os.open(self._path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if not replaced:
                temporary_path.unlink(missing_ok=True)

    def process(
        self,
        stream_epoch: int,
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
            stream = self._load_locked()
            before = stream.state_dict()
            receipt = stream.process(
                stream_epoch,
                event_id,
                sequence,
                base,
                observation=observation,
                observed_value=observed_value,
                strength=strength,
            )
            after = stream.state_dict()
            if after != before:
                self._replace_checkpoint(after)
            return receipt
        finally:
            self._release_lock(descriptor)

    def rotate_epoch(
        self,
        next_epoch: int,
        *,
        expected_next_sequence: int,
    ) -> str:
        descriptor = self._acquire_lock()
        try:
            stream = self._load_locked()
            digest = stream.rotate_epoch(
                next_epoch,
                expected_next_sequence=expected_next_sequence,
            )
            self._replace_checkpoint(stream.state_dict())
            return digest
        finally:
            self._release_lock(descriptor)

    def state_dict(self) -> dict[str, Any]:
        descriptor = self._acquire_lock()
        try:
            return self._load_locked().state_dict()
        finally:
            self._release_lock(descriptor)


__all__ = [
    "EpochCheckpointCorruptError",
    "EpochFencedOutcomeRevisionStream",
    "EpochRotationConflictError",
    "EpochStoreLockTimeoutError",
    "FutureStreamEpochError",
    "LockedEpochFencedOutcomeRevisionStore",
    "RetiredStreamEpochError",
]

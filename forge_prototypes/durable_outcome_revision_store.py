from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from forge_prototypes.idempotent_outcome_revision_stream import (
    IdempotentOutcomeRevisionStream,
    StreamEventReceipt,
)
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


class DurableCheckpointConflictError(RuntimeError):
    """Raised when another writer replaced the checkpoint after it was opened."""


class DurableCheckpointCorruptError(ValueError):
    """Raised when a checkpoint is malformed or fails its content digest."""


FaultHook = Callable[[str], None]


class DurableOutcomeRevisionStore:
    """Persist an idempotent revision stream through atomic local snapshots.

    Each event is first evaluated on a checkpoint copy.  The complete candidate
    stream is written to a same-directory temporary file, flushed, atomically
    replaced, and only then installed as the live in-memory stream.  A digest
    comparison against the checkpoint opened by this instance provides a small
    optimistic-concurrency boundary for multiple local writers.

    A process crash after ``os.replace`` may leave the caller uncertain whether
    the event committed.  Reopening the store and redelivering the same event is
    safe because the underlying stream binds event identity to payload content.

    This is ordinary local checkpoint/WAL-style engineering.  It is not a
    distributed transaction, consensus protocol, learning mechanism, or
    scientific result.
    """

    _SCHEMA_VERSION = 1

    def __init__(
        self,
        path: Path,
        stream: IdempotentOutcomeRevisionStream,
        *,
        checkpoint_sha256: str | None,
        fault_hook: FaultHook | None = None,
    ) -> None:
        self._path = path
        self._stream = stream
        self._checkpoint_sha256 = checkpoint_sha256
        self._fault_hook = fault_hook

    @classmethod
    def open(
        cls,
        path: str | os.PathLike[str],
        *,
        fault_hook: FaultHook | None = None,
    ) -> DurableOutcomeRevisionStore:
        checkpoint_path = Path(path)
        if not checkpoint_path.exists():
            return cls(
                checkpoint_path,
                IdempotentOutcomeRevisionStream(),
                checkpoint_sha256=None,
                fault_hook=fault_hook,
            )
        state, digest = cls._read_checkpoint(checkpoint_path)
        return cls(
            checkpoint_path,
            IdempotentOutcomeRevisionStream.from_state_dict(state),
            checkpoint_sha256=digest,
            fault_hook=fault_hook,
        )

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
    def _envelope(cls, state: dict[str, Any]) -> tuple[bytes, str]:
        canonical_state = cls._canonical_bytes(state)
        digest = hashlib.sha256(canonical_state).hexdigest()
        envelope = {
            "schema_version": cls._SCHEMA_VERSION,
            "checkpoint_sha256": digest,
            "stream_state": state,
        }
        payload = json.dumps(
            envelope,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ).encode("utf-8") + b"\n"
        return payload, digest

    @classmethod
    def _read_checkpoint(cls, path: Path) -> tuple[dict[str, Any], str]:
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DurableCheckpointCorruptError("checkpoint is not valid JSON") from exc
        if envelope.get("schema_version") != cls._SCHEMA_VERSION:
            raise DurableCheckpointCorruptError(
                "unsupported durable checkpoint schema_version"
            )
        state = envelope.get("stream_state")
        if not isinstance(state, dict):
            raise DurableCheckpointCorruptError("checkpoint stream_state is missing")
        expected = envelope.get("checkpoint_sha256")
        actual = hashlib.sha256(cls._canonical_bytes(state)).hexdigest()
        if expected != actual:
            raise DurableCheckpointCorruptError("checkpoint digest mismatch")
        try:
            IdempotentOutcomeRevisionStream.from_state_dict(state)
        except (KeyError, TypeError, ValueError) as exc:
            raise DurableCheckpointCorruptError(
                "checkpoint stream_state is invalid"
            ) from exc
        return state, actual

    def _call_fault_hook(self, stage: str) -> None:
        if self._fault_hook is not None:
            self._fault_hook(stage)

    def _assert_current_checkpoint(self) -> None:
        if self._path.exists():
            _, current_digest = self._read_checkpoint(self._path)
        else:
            current_digest = None
        if current_digest != self._checkpoint_sha256:
            raise DurableCheckpointConflictError(
                "durable checkpoint changed after this store was opened"
            )

    def _replace_checkpoint(self, payload: bytes) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
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
            self._call_fault_hook("after_temp_fsync")
            os.replace(temporary_path, self._path)
            replaced = True
            self._call_fault_hook("after_replace")
            directory_fd = os.open(self._path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            self._call_fault_hook("after_directory_fsync")
        finally:
            if not replaced:
                temporary_path.unlink(missing_ok=True)

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
        self._assert_current_checkpoint()
        candidate = IdempotentOutcomeRevisionStream.from_state_dict(
            self._stream.state_dict()
        )
        receipt = candidate.process(
            event_id,
            sequence,
            base,
            observation=observation,
            observed_value=observed_value,
            strength=strength,
        )
        candidate_state = candidate.state_dict()
        if candidate_state == self._stream.state_dict():
            return receipt
        payload, digest = self._envelope(candidate_state)
        self._replace_checkpoint(payload)
        self._stream = candidate
        self._checkpoint_sha256 = digest
        return receipt

    def state_dict(self) -> dict[str, Any]:
        return self._stream.state_dict()


__all__ = [
    "DurableCheckpointConflictError",
    "DurableCheckpointCorruptError",
    "DurableOutcomeRevisionStore",
]

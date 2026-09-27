from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass, replace
from math import isfinite
from typing import Any

from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot
from forge_prototypes.transactional_outcome_revision_coordinator import (
    TransactionalOutcomeRevisionCoordinator,
)


class StreamEventConflictError(ValueError):
    """Raised when an event identifier is reused for different public inputs."""


class StreamSequenceError(ValueError):
    """Raised when a new event is delivered outside the declared stream order."""


@dataclass(frozen=True, slots=True)
class StreamEventReceipt:
    event_id: str
    sequence: int
    payload_sha256: str
    outcome_action: str
    committed: bool
    state_changed: bool
    duplicate: bool
    delivery_action: str


class IdempotentOutcomeRevisionStream:
    """Add ordered, idempotent delivery around transactional revision steps.

    A new event must use the next contiguous sequence number.  Once an event is
    accepted, its identifier is bound to a digest of the complete public input.
    Exact redelivery returns the stored semantic receipt without re-evaluating
    the event.  Identifier reuse with different content and out-of-order new
    delivery both fail without changing coordinator or receipt state.

    This is an ordinary idempotent-consumer ledger.  It supplies no event-time
    inference, distributed exactly-once guarantee, learning rule or scientific
    evidence.
    """

    _SCHEMA_VERSION = 1

    def __init__(
        self,
        coordinator: TransactionalOutcomeRevisionCoordinator | None = None,
        *,
        next_sequence: int = 0,
        receipts: dict[str, StreamEventReceipt] | None = None,
    ) -> None:
        if next_sequence < 0:
            raise ValueError("next_sequence must be non-negative")
        self._coordinator = coordinator or TransactionalOutcomeRevisionCoordinator()
        self._next_sequence = next_sequence
        self._receipts = dict(receipts or {})

    @staticmethod
    def _payload_digest(
        event_id: str,
        sequence: int,
        base: PredictionPoolSnapshot,
        observation: Sequence[float],
        observed_value: str,
        strength: float,
    ) -> str:
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event_id must be a non-empty string")
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
            raise ValueError("sequence must be a non-negative integer")

        normalized_observation = [float(value) for value in observation]
        if not all(isfinite(value) for value in normalized_observation):
            raise ValueError("observation values must be finite")
        normalized_strength = float(strength)
        if not isfinite(normalized_strength):
            raise ValueError("strength must be finite")

        payload = {
            "base": base.as_dict(),
            "event_id": event_id,
            "observation": normalized_observation,
            "observed_value": observed_value,
            "sequence": sequence,
            "strength": normalized_strength,
        }
        serialized = json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

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
        digest = self._payload_digest(
            event_id,
            sequence,
            base,
            observation,
            observed_value,
            strength,
        )
        previous = self._receipts.get(event_id)
        if previous is not None:
            if previous.payload_sha256 != digest:
                raise StreamEventConflictError(
                    f"event_id {event_id!r} is already bound to different content"
                )
            return replace(
                previous,
                state_changed=False,
                duplicate=True,
                delivery_action="duplicate_replay",
            )

        if sequence != self._next_sequence:
            raise StreamSequenceError(
                f"new event sequence {sequence} does not match next {self._next_sequence}"
            )

        # Apply to a checkpoint copy so coordinator and receipt state advance as
        # one in-memory transaction.  Exceptions leave both live objects alone.
        candidate = TransactionalOutcomeRevisionCoordinator.from_state_dict(
            self._coordinator.state_dict()
        )
        result = candidate.apply_step(
            base,
            observation=observation,
            observed_value=observed_value,
            strength=strength,
        )
        receipt = StreamEventReceipt(
            event_id=event_id,
            sequence=sequence,
            payload_sha256=digest,
            outcome_action=result.action,
            committed=result.committed,
            state_changed=result.state_changed,
            duplicate=False,
            delivery_action="processed",
        )

        self._coordinator = candidate
        self._receipts[event_id] = receipt
        self._next_sequence += 1
        return receipt

    def state_dict(self) -> dict[str, Any]:
        ordered_receipts = sorted(
            self._receipts.values(), key=lambda receipt: (receipt.sequence, receipt.event_id)
        )
        return {
            "schema_version": self._SCHEMA_VERSION,
            "next_sequence": self._next_sequence,
            "coordinator": self._coordinator.state_dict(),
            "receipts": [asdict(receipt) for receipt in ordered_receipts],
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> IdempotentOutcomeRevisionStream:
        if state.get("schema_version") != cls._SCHEMA_VERSION:
            raise ValueError("unsupported stream checkpoint schema_version")
        receipts = {
            row["event_id"]: StreamEventReceipt(**row)
            for row in state.get("receipts", [])
        }
        if len(receipts) != len(state.get("receipts", [])):
            raise ValueError("stream checkpoint contains duplicate event_id entries")
        next_sequence = int(state["next_sequence"])
        expected_sequences = list(range(next_sequence))
        actual_sequences = sorted(receipt.sequence for receipt in receipts.values())
        if actual_sequences != expected_sequences:
            raise ValueError("stream checkpoint receipt sequences are not contiguous")
        return cls(
            TransactionalOutcomeRevisionCoordinator.from_state_dict(
                state["coordinator"]
            ),
            next_sequence=next_sequence,
            receipts=receipts,
        )


__all__ = [
    "IdempotentOutcomeRevisionStream",
    "StreamEventConflictError",
    "StreamEventReceipt",
    "StreamSequenceError",
]

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


class CompactedReceiptUnavailableError(ValueError):
    """Raised when a replay predates the retained exact-receipt window."""


class CompactedEventIdentityError(ValueError):
    """Raised when an identifier may already exist in the compacted prefix."""


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
    Exact redelivery in the retained window returns the stored semantic receipt
    without re-evaluating the event.  With a configured receipt capacity, older
    receipts are replaced by a rolling digest and conservative fixed-size event
    identity filter.  Old replay and possible compacted identifier reuse fail
    closed rather than silently re-applying an event.

    This is an ordinary idempotent-consumer ledger.  It supplies no event-time
    inference, distributed exactly-once guarantee, learning rule or scientific
    evidence.
    """

    _SCHEMA_VERSION = 2
    _COMPACTED_FILTER_BITS = 2048
    _COMPACTED_FILTER_HASHES = 4

    def __init__(
        self,
        coordinator: TransactionalOutcomeRevisionCoordinator | None = None,
        *,
        next_sequence: int = 0,
        receipts: dict[str, StreamEventReceipt] | None = None,
        receipt_capacity: int | None = None,
        retained_from_sequence: int = 0,
        compacted_prefix_sha256: str | None = None,
        compacted_event_filter: int = 0,
    ) -> None:
        if next_sequence < 0:
            raise ValueError("next_sequence must be non-negative")
        if receipt_capacity is not None and (
            isinstance(receipt_capacity, bool)
            or not isinstance(receipt_capacity, int)
            or receipt_capacity < 1
        ):
            raise ValueError("receipt_capacity must be a positive integer or None")
        if retained_from_sequence < 0 or retained_from_sequence > next_sequence:
            raise ValueError("retained_from_sequence is outside the stream")
        self._coordinator = coordinator or TransactionalOutcomeRevisionCoordinator()
        self._next_sequence = next_sequence
        self._receipts = dict(receipts or {})
        self._receipt_capacity = receipt_capacity
        self._retained_from_sequence = retained_from_sequence
        self._compacted_prefix_sha256 = compacted_prefix_sha256
        self._compacted_event_filter = compacted_event_filter

    @classmethod
    def _filter_positions(cls, event_id: str) -> tuple[int, ...]:
        digest = hashlib.sha256(event_id.encode("utf-8")).digest()
        return tuple(
            int.from_bytes(digest[index * 2 : index * 2 + 2], "big")
            % cls._COMPACTED_FILTER_BITS
            for index in range(cls._COMPACTED_FILTER_HASHES)
        )

    def _might_have_compacted(self, event_id: str) -> bool:
        if self._retained_from_sequence == 0:
            return False
        return all(
            self._compacted_event_filter & (1 << position)
            for position in self._filter_positions(event_id)
        )

    @staticmethod
    def _canonical_receipt(receipt: StreamEventReceipt) -> bytes:
        return json.dumps(
            asdict(receipt),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")

    def _compact_receipts(self) -> None:
        if self._receipt_capacity is None:
            return
        while len(self._receipts) > self._receipt_capacity:
            receipt = min(
                self._receipts.values(), key=lambda row: (row.sequence, row.event_id)
            )
            previous = bytes.fromhex(self._compacted_prefix_sha256 or "00" * 32)
            self._compacted_prefix_sha256 = hashlib.sha256(
                previous + b"\n" + self._canonical_receipt(receipt)
            ).hexdigest()
            for position in self._filter_positions(receipt.event_id):
                self._compacted_event_filter |= 1 << position
            del self._receipts[receipt.event_id]
            self._retained_from_sequence = receipt.sequence + 1

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

        if sequence < self._retained_from_sequence:
            raise CompactedReceiptUnavailableError(
                f"event sequence {sequence} predates retained receipt window "
                f"starting at {self._retained_from_sequence}"
            )
        if self._might_have_compacted(event_id):
            raise CompactedEventIdentityError(
                f"event_id {event_id!r} may already exist in compacted history"
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
        self._compact_receipts()
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
            "receipt_capacity": self._receipt_capacity,
            "retained_from_sequence": self._retained_from_sequence,
            "compacted_prefix_sha256": self._compacted_prefix_sha256,
            "compacted_event_filter_hex": format(
                self._compacted_event_filter,
                f"0{self._COMPACTED_FILTER_BITS // 4}x",
            ),
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> IdempotentOutcomeRevisionStream:
        version = state.get("schema_version")
        if version not in (1, cls._SCHEMA_VERSION):
            raise ValueError("unsupported stream checkpoint schema_version")
        receipts = {
            row["event_id"]: StreamEventReceipt(**row)
            for row in state.get("receipts", [])
        }
        if len(receipts) != len(state.get("receipts", [])):
            raise ValueError("stream checkpoint contains duplicate event_id entries")
        next_sequence = int(state["next_sequence"])
        retained_from_sequence = (
            0 if version == 1 else int(state.get("retained_from_sequence", 0))
        )
        receipt_capacity = None if version == 1 else state.get("receipt_capacity")
        if receipt_capacity is not None:
            if (
                isinstance(receipt_capacity, bool)
                or not isinstance(receipt_capacity, int)
                or receipt_capacity < 1
            ):
                raise ValueError("invalid receipt_capacity")
            if len(receipts) > receipt_capacity:
                raise ValueError("receipt ledger exceeds receipt_capacity")
        if retained_from_sequence < 0 or retained_from_sequence > next_sequence:
            raise ValueError("invalid retained_from_sequence")
        expected_sequences = list(range(retained_from_sequence, next_sequence))
        actual_sequences = sorted(receipt.sequence for receipt in receipts.values())
        if actual_sequences != expected_sequences:
            raise ValueError("stream checkpoint receipt sequences are not contiguous")
        compacted_prefix_sha256 = (
            None if version == 1 else state.get("compacted_prefix_sha256")
        )
        if retained_from_sequence == 0:
            if compacted_prefix_sha256 is not None:
                raise ValueError("uncompacted stream has a compacted prefix digest")
        elif not (
            isinstance(compacted_prefix_sha256, str)
            and len(compacted_prefix_sha256) == 64
            and all(ch in "0123456789abcdef" for ch in compacted_prefix_sha256)
        ):
            raise ValueError("compacted stream lacks a valid prefix digest")
        filter_hex = (
            "0" * (cls._COMPACTED_FILTER_BITS // 4)
            if version == 1
            else state.get("compacted_event_filter_hex", "")
        )
        if not (
            isinstance(filter_hex, str)
            and len(filter_hex) == cls._COMPACTED_FILTER_BITS // 4
            and all(ch in "0123456789abcdef" for ch in filter_hex)
        ):
            raise ValueError("invalid compacted event filter")
        compacted_event_filter = int(filter_hex, 16)
        if retained_from_sequence > 0 and compacted_event_filter == 0:
            raise ValueError("compacted stream lacks event identity filter entries")
        return cls(
            TransactionalOutcomeRevisionCoordinator.from_state_dict(
                state["coordinator"]
            ),
            next_sequence=next_sequence,
            receipts=receipts,
            receipt_capacity=receipt_capacity,
            retained_from_sequence=retained_from_sequence,
            compacted_prefix_sha256=compacted_prefix_sha256,
            compacted_event_filter=compacted_event_filter,
        )


__all__ = [
    "CompactedEventIdentityError",
    "CompactedReceiptUnavailableError",
    "IdempotentOutcomeRevisionStream",
    "StreamEventConflictError",
    "StreamEventReceipt",
    "StreamSequenceError",
]

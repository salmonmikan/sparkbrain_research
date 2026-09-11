"""Construction-only R01-16 propagation factorization.

This module binds exact pre/post training connection inventories and constructs
F0/FW/FD/FWD intervention states without running a probe.  It deliberately
contains no task endpoint, scorer, held-out path, or execution authority.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Literal

R01_16_PROTOCOL_ID = "rv01-r01-16-propagation-factorization-v1"
R01_16_ARM = Literal["F0", "FW", "FD", "FWD"]


def _finite(value: float, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real numeric value")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


@dataclass(frozen=True, slots=True)
class ConnectionState:
    """One physical edge at a fixed construction boundary."""

    source_id: int
    target_id: int
    weight: float
    delay_ms: float
    plastic: bool

    def validate(self) -> None:
        if type(self.source_id) is not int or type(self.target_id) is not int:
            raise TypeError("connection unit IDs must be integers")
        _finite(self.weight, name="connection weight")
        delay = _finite(self.delay_ms, name="connection delay_ms")
        if delay <= 0.0:
            raise ValueError("connection delay_ms must be positive")
        if type(self.plastic) is not bool:
            raise TypeError("connection plastic flag must be boolean")

    @property
    def key(self) -> tuple[int, int]:
        return (self.source_id, self.target_id)

    def state_dict(self) -> dict[str, int | float | bool]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True, slots=True)
class QueuedPropagationSnapshot:
    """Queued arrival already derived from a physical connection."""

    event_id: str
    source_id: int
    target_id: int
    queued_weight: float
    queued_delay_ms: float

    def validate(self) -> None:
        if not self.event_id:
            raise ValueError("queued propagation event_id must be non-empty")
        if type(self.source_id) is not int or type(self.target_id) is not int:
            raise TypeError("queued propagation unit IDs must be integers")
        _finite(self.queued_weight, name="queued weight")
        delay = _finite(self.queued_delay_ms, name="queued delay_ms")
        if delay <= 0.0:
            raise ValueError("queued delay_ms must be positive")

    @property
    def key(self) -> tuple[int, int]:
        return (self.source_id, self.target_id)

    def state_dict(self) -> dict[str, str | int | float]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FactorizationConstructionSummary:
    protocol_id: str
    pre_training_sha256: str
    post_training_sha256: str
    queue_sha256: str
    weight_changed_edges: tuple[tuple[int, int], ...]
    delay_changed_edges: tuple[tuple[int, int], ...]
    arm_sha256: dict[str, str]

    @property
    def weight_contrast_ready(self) -> bool:
        return bool(self.weight_changed_edges)

    @property
    def delay_contrast_ready(self) -> bool:
        return bool(self.delay_changed_edges)

    @property
    def any_contrast_ready(self) -> bool:
        return self.weight_contrast_ready or self.delay_contrast_ready


class R01_16FactorizationConstruction:
    """Build exact expression-time reset arms before capability exists."""

    def __init__(
        self,
        *,
        pre_training: tuple[ConnectionState, ...],
        post_training: tuple[ConnectionState, ...],
        queued_propagation: tuple[QueuedPropagationSnapshot, ...] = (),
    ) -> None:
        self.pre_training = tuple(pre_training)
        self.post_training = tuple(post_training)
        self.queued_propagation = tuple(queued_propagation)
        self._pre = self._index(self.pre_training, label="pre-training")
        self._post = self._index(self.post_training, label="post-training")
        self._validate()

    @staticmethod
    def _index(
        rows: tuple[ConnectionState, ...],
        *,
        label: str,
    ) -> dict[tuple[int, int], ConnectionState]:
        if not rows:
            raise ValueError(f"R01-16 requires non-empty {label} connections")
        result: dict[tuple[int, int], ConnectionState] = {}
        for row in rows:
            row.validate()
            if row.key in result:
                raise ValueError(f"duplicate {label} connection edge")
            result[row.key] = row
        return result

    def _validate(self) -> None:
        if set(self._pre) != set(self._post):
            raise ValueError("R01-16 pre/post connection topology drifted")
        for key in self._pre:
            if self._pre[key].plastic != self._post[key].plastic:
                raise ValueError("R01-16 connection plastic flag drifted")

        queued_ids: set[str] = set()
        for queued in self.queued_propagation:
            queued.validate()
            if queued.event_id in queued_ids:
                raise ValueError("duplicate queued propagation event_id")
            queued_ids.add(queued.event_id)
            if queued.key not in self._post:
                raise ValueError("queued propagation references missing connection")
            post = self._post[queued.key]
            if queued.queued_weight != post.weight or queued.queued_delay_ms != post.delay_ms:
                raise ValueError(
                    "queued propagation does not match common post-training checkpoint"
                )
            pre = self._pre[queued.key]
            if pre.weight != post.weight or pre.delay_ms != post.delay_ms:
                raise RuntimeError(
                    "R01-16 queue-integrity gate failed: changed connection already "
                    "has queued propagation"
                )

    @property
    def weight_changed_edges(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            key
            for key in sorted(self._pre)
            if self._pre[key].weight != self._post[key].weight
        )

    @property
    def delay_changed_edges(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            key
            for key in sorted(self._pre)
            if self._pre[key].delay_ms != self._post[key].delay_ms
        )

    def arm_inventory(self, arm: R01_16_ARM) -> tuple[ConnectionState, ...]:
        if arm not in ("F0", "FW", "FD", "FWD"):
            raise ValueError("R01-16 arm must be F0, FW, FD, or FWD")
        rows: list[ConnectionState] = []
        for key in sorted(self._post):
            pre = self._pre[key]
            post = self._post[key]
            weight = pre.weight if arm in ("FW", "FWD") else post.weight
            delay_ms = pre.delay_ms if arm in ("FD", "FWD") else post.delay_ms
            rows.append(
                ConnectionState(
                    source_id=post.source_id,
                    target_id=post.target_id,
                    weight=weight,
                    delay_ms=delay_ms,
                    plastic=post.plastic,
                )
            )
        result = tuple(rows)
        for row in result:
            row.validate()
        return result

    @staticmethod
    def inventory_sha256(rows: tuple[ConnectionState, ...]) -> str:
        ordered = tuple(sorted(rows, key=lambda row: row.key))
        return _sha256([row.state_dict() for row in ordered])

    def summary(self) -> FactorizationConstructionSummary:
        arms = {
            arm: self.inventory_sha256(self.arm_inventory(arm))
            for arm in ("F0", "FW", "FD", "FWD")
        }
        return FactorizationConstructionSummary(
            protocol_id=R01_16_PROTOCOL_ID,
            pre_training_sha256=self.inventory_sha256(self.pre_training),
            post_training_sha256=self.inventory_sha256(self.post_training),
            queue_sha256=_sha256(
                [row.state_dict() for row in self.queued_propagation]
            ),
            weight_changed_edges=self.weight_changed_edges,
            delay_changed_edges=self.delay_changed_edges,
            arm_sha256=arms,
        )

    def require_any_prospective_contrast(self) -> FactorizationConstructionSummary:
        summary = self.summary()
        if not summary.any_contrast_ready:
            raise RuntimeError(
                "R01-16 construction stopped: no learned weight or delay contrast exists"
            )
        return summary


__all__ = [
    "ConnectionState",
    "FactorizationConstructionSummary",
    "QueuedPropagationSnapshot",
    "R01_16FactorizationConstruction",
    "R01_16_PROTOCOL_ID",
]

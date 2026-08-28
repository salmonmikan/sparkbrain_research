from __future__ import annotations

import hashlib
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable

from .contracts import (
    BurstEvent,
    CascadeEvent,
    IgnitionEvent,
    SpikeEvent,
    canonical_json,
)


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _spatial_spread(spikes: Iterable[SpikeEvent]) -> float:
    rows = list(spikes)
    if len(rows) < 2:
        return 0.0
    return max(
        math.hypot(a.x - b.x, a.y - b.y)
        for index, a in enumerate(rows)
        for b in rows[index + 1 :]
    )


@dataclass(frozen=True, slots=True)
class BurstDetectorConfig:
    window_ms: float = 8.0
    min_spikes: int = 4
    min_units: int = 3


class BurstDetector:
    def __init__(self, config: BurstDetectorConfig | None = None) -> None:
        self.config = config or BurstDetectorConfig()
        self._window: deque[SpikeEvent] = deque()
        self._emitted_keys: set[tuple[int, int]] = set()

    def update(self, spikes: Iterable[SpikeEvent]) -> tuple[BurstEvent, ...]:
        output: list[BurstEvent] = []
        for spike in sorted(spikes, key=lambda row: (row.time_ms, row.unit_id)):
            self._window.append(spike)
            cutoff = spike.time_ms - self.config.window_ms
            while self._window and self._window[0].time_ms < cutoff:
                self._window.popleft()
            units = sorted({row.unit_id for row in self._window})
            if len(self._window) < self.config.min_spikes or len(units) < self.config.min_units:
                continue
            key = (int(round(self._window[0].time_ms * 1000)), int(round(spike.time_ms * 1000)))
            if key in self._emitted_keys:
                continue
            self._emitted_keys.add(key)
            payload = {
                "end_ms": spike.time_ms,
                "start_ms": self._window[0].time_ms,
                "unit_ids": units,
            }
            output.append(
                BurstEvent(
                    burst_id=f"burst-{_digest(payload)[:12]}",
                    start_ms=self._window[0].time_ms,
                    end_ms=spike.time_ms,
                    spike_count=len(self._window),
                    unit_ids=tuple(units),
                    spatial_spread=_spatial_spread(self._window),
                )
            )
        return tuple(output)


@dataclass(frozen=True, slots=True)
class CascadeTrackerConfig:
    max_gap_ms: float = 6.0
    temporal_bin_ms: float = 2.0
    min_spikes: int = 2


@dataclass(slots=True)
class AssemblyMemory:
    """Track repeated spatiotemporal cascade signatures without semantic labels."""

    counts: dict[str, int] = field(default_factory=dict)
    last_seen_ms: dict[str, float] = field(default_factory=dict)

    def recurrence_before_update(self, signature: str) -> float:
        count = self.counts.get(signature, 0)
        return 1.0 - math.exp(-count / 2.0)

    def update(self, signature: str, *, time_ms: float) -> None:
        self.counts[signature] = self.counts.get(signature, 0) + 1
        self.last_seen_ms[signature] = time_ms

    def state_dict(self) -> dict[str, object]:
        return {
            "counts": dict(sorted(self.counts.items())),
            "last_seen_ms": dict(sorted(self.last_seen_ms.items())),
        }


class CascadeTracker:
    def __init__(
        self,
        config: CascadeTrackerConfig | None = None,
        *,
        memory: AssemblyMemory | None = None,
    ) -> None:
        self.config = config or CascadeTrackerConfig()
        self.memory = memory or AssemblyMemory()
        self._pending: list[SpikeEvent] = []

    def _signature(self, spikes: list[SpikeEvent]) -> str:
        if not spikes:
            return "empty"
        start = spikes[0].time_ms
        sequence = [
            [
                row.unit_id,
                int(round((row.time_ms - start) / self.config.temporal_bin_ms)),
            ]
            for row in spikes
        ]
        return _digest({"sequence": sequence})[:24]

    def _finalize(self) -> CascadeEvent | None:
        if len(self._pending) < self.config.min_spikes:
            self._pending.clear()
            return None
        spikes = list(self._pending)
        self._pending.clear()
        signature = self._signature(spikes)
        recurrence = self.memory.recurrence_before_update(signature)
        self.memory.update(signature, time_ms=spikes[-1].time_ms)
        units = tuple(sorted({row.unit_id for row in spikes}))
        payload = {
            "end_ms": spikes[-1].time_ms,
            "signature": signature,
            "start_ms": spikes[0].time_ms,
        }
        return CascadeEvent(
            cascade_id=f"cascade-{_digest(payload)[:12]}",
            start_ms=spikes[0].time_ms,
            end_ms=spikes[-1].time_ms,
            spike_count=len(spikes),
            unit_ids=units,
            ordered_units=tuple(row.unit_id for row in spikes),
            spatial_spread=_spatial_spread(spikes),
            novelty=sum(row.novelty for row in spikes) / len(spikes),
            prediction_error=sum(row.prediction_error for row in spikes) / len(spikes),
            recurrence=recurrence,
            signature=signature,
        )

    def update(
        self,
        spikes: Iterable[SpikeEvent],
        *,
        flush_until_ms: float | None = None,
    ) -> tuple[CascadeEvent, ...]:
        output: list[CascadeEvent] = []
        for spike in sorted(spikes, key=lambda row: (row.time_ms, row.unit_id)):
            if self._pending and spike.time_ms - self._pending[-1].time_ms > self.config.max_gap_ms:
                row = self._finalize()
                if row is not None:
                    output.append(row)
            self._pending.append(spike)
        if (
            flush_until_ms is not None
            and self._pending
            and flush_until_ms - self._pending[-1].time_ms > self.config.max_gap_ms
        ):
            row = self._finalize()
            if row is not None:
                output.append(row)
        return tuple(output)

    def flush(self) -> tuple[CascadeEvent, ...]:
        row = self._finalize()
        return () if row is None else (row,)

    def state_dict(self) -> dict[str, object]:
        return {
            "memory": self.memory.state_dict(),
            "pending": [row.as_dict() for row in self._pending],
        }


@dataclass(frozen=True, slots=True)
class IgnitionGateConfig:
    threshold: float = 4.2
    min_spikes: int = 5
    min_units: int = 4
    size_weight: float = 1.25
    diversity_weight: float = 1.0
    spread_weight: float = 0.25
    recurrence_weight: float = 0.8
    novelty_weight: float = 0.55
    prediction_error_weight: float = 0.9


class IgnitionGate:
    def __init__(self, config: IgnitionGateConfig | None = None) -> None:
        self.config = config or IgnitionGateConfig()

    def score(self, cascade: CascadeEvent) -> float:
        return (
            self.config.size_weight * math.log1p(cascade.spike_count)
            + self.config.diversity_weight * math.log1p(len(cascade.unit_ids))
            + self.config.spread_weight * cascade.spatial_spread
            + self.config.recurrence_weight * cascade.recurrence
            + self.config.novelty_weight * cascade.novelty
            + self.config.prediction_error_weight * cascade.prediction_error
        )

    def evaluate(self, cascades: Iterable[CascadeEvent]) -> tuple[IgnitionEvent, ...]:
        rows: list[IgnitionEvent] = []
        for cascade in cascades:
            score = self.score(cascade)
            if cascade.spike_count < self.config.min_spikes:
                continue
            if len(cascade.unit_ids) < self.config.min_units:
                continue
            if score < self.config.threshold:
                continue
            payload = {
                "cascade_id": cascade.cascade_id,
                "score": round(score, 12),
                "signature": cascade.signature,
            }
            rows.append(
                IgnitionEvent(
                    ignition_id=f"ignition-{_digest(payload)[:12]}",
                    cascade_id=cascade.cascade_id,
                    time_ms=cascade.end_ms,
                    score=score,
                    threshold=self.config.threshold,
                    reason="cascade_threshold_crossed",
                    unit_ids=cascade.unit_ids,
                    signature=cascade.signature,
                )
            )
        return tuple(rows)

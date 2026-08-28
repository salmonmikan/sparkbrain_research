from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

from .contracts import SpikeEvent
from .field import TemporalExcitableField


@dataclass(frozen=True, slots=True)
class TimingPlasticityConfig:
    learning_rate: float = 0.012
    tau_plus_ms: float = 18.0
    tau_minus_ms: float = 24.0
    depression_ratio: float = 0.75
    reward_decay: float = 0.85
    min_weight: float = -1.5
    max_weight: float = 1.5
    delay_learning_rate: float = 0.02
    min_delay_ms: float = 0.5
    max_delay_ms: float = 30.0


class TimingPlasticityRule:
    """A bounded STDP-like engineering rule with optional reward modulation."""

    def __init__(self, config: TimingPlasticityConfig | None = None) -> None:
        self.config = config or TimingPlasticityConfig()
        self.reward_trace = 1.0
        self.update_count = 0

    def reward(self, value: float) -> None:
        self.reward_trace = max(-2.0, min(2.0, float(value)))

    def apply(
        self,
        field: TemporalExcitableField,
        spikes: Iterable[SpikeEvent],
    ) -> int:
        rows = sorted(spikes, key=lambda row: (row.time_ms, row.unit_id))
        by_unit: dict[int, list[float]] = {}
        for row in rows:
            by_unit.setdefault(row.unit_id, []).append(row.time_ms)
        updates = 0
        for edge in field.connections.values():
            if not edge.plastic:
                continue
            pre_times = by_unit.get(edge.source_id, [])
            post_times = by_unit.get(edge.target_id, [])
            if not pre_times or not post_times:
                continue
            delta = 0.0
            delay_delta = 0.0
            pairs = 0
            for pre in pre_times:
                for post in post_times:
                    lag = post - pre
                    if lag > 0:
                        delta += math.exp(-lag / self.config.tau_plus_ms)
                        desired_delay = max(self.config.min_delay_ms, lag)
                        delay_delta += desired_delay - edge.delay_ms
                        pairs += 1
                    elif lag < 0:
                        delta -= self.config.depression_ratio * math.exp(
                            lag / self.config.tau_minus_ms
                        )
            if delta == 0.0:
                continue
            edge.weight = max(
                self.config.min_weight,
                min(
                    self.config.max_weight,
                    edge.weight + self.config.learning_rate * self.reward_trace * delta,
                ),
            )
            if pairs and edge.weight > 0:
                edge.delay_ms = max(
                    self.config.min_delay_ms,
                    min(
                        self.config.max_delay_ms,
                        edge.delay_ms + self.config.delay_learning_rate * (delay_delta / pairs),
                    ),
                )
            updates += 1
        self.reward_trace = 1.0 + (self.reward_trace - 1.0) * self.config.reward_decay
        self.update_count += updates
        return updates

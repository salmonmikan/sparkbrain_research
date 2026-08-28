from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField


@dataclass(frozen=True, slots=True)
class V05PlasticityConfig:
    enable_weight_learning: bool = True
    enable_delay_learning: bool = True
    learning_rate: float = 0.001
    delay_learning_rate: float = 0.004
    tau_plus_ms: float = 18.0
    tau_minus_ms: float = 24.0
    depression_ratio: float = 0.75
    min_weight: float = -1.4
    max_weight: float = 1.4
    min_delay_ms: float = 0.5
    max_delay_ms: float = 30.0
    max_updates_per_step: int = 2_000
    eligibility_decay: float = 0.90


@dataclass(slots=True)
class V05PlasticityController:
    config: V05PlasticityConfig = field(default_factory=V05PlasticityConfig)
    reward_trace: float = 1.0
    eligibility: dict[str, float] = field(default_factory=dict)
    update_count: int = 0

    @staticmethod
    def _key(source_id: int, target_id: int) -> str:
        return f"{source_id}:{target_id}"

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
        for key in list(self.eligibility):
            self.eligibility[key] *= self.config.eligibility_decay
            if abs(self.eligibility[key]) < 1e-8:
                del self.eligibility[key]
        updates = 0
        for edge_key in sorted(field.connections):
            if updates >= self.config.max_updates_per_step:
                break
            edge = field.connections[edge_key]
            if not edge.plastic:
                continue
            pre_times = by_unit.get(edge.source_id, ())
            post_times = by_unit.get(edge.target_id, ())
            if not pre_times or not post_times:
                continue
            delta = 0.0
            causal_lags: list[float] = []
            for pre in pre_times:
                for post in post_times:
                    lag = post - pre
                    if lag > 0:
                        delta += math.exp(-lag / self.config.tau_plus_ms)
                        causal_lags.append(lag)
                    elif lag < 0:
                        delta -= self.config.depression_ratio * math.exp(
                            lag / self.config.tau_minus_ms
                        )
            if delta == 0.0:
                continue
            key = self._key(edge.source_id, edge.target_id)
            eligibility = self.eligibility.get(key, 0.0) + delta
            self.eligibility[key] = eligibility
            if self.config.enable_weight_learning:
                edge.weight = max(
                    self.config.min_weight,
                    min(
                        self.config.max_weight,
                        edge.weight + self.config.learning_rate * self.reward_trace * eligibility,
                    ),
                )
            if self.config.enable_delay_learning and causal_lags and edge.weight > 0:
                desired = sum(causal_lags) / len(causal_lags)
                edge.delay_ms = max(
                    self.config.min_delay_ms,
                    min(
                        self.config.max_delay_ms,
                        edge.delay_ms + self.config.delay_learning_rate * (desired - edge.delay_ms),
                    ),
                )
            updates += 1
        self.reward_trace = 1.0 + (self.reward_trace - 1.0) * 0.85
        self.update_count += updates
        return updates

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "eligibility": dict(sorted(self.eligibility.items())),
            "reward_trace": self.reward_trace,
            "update_count": self.update_count,
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> V05PlasticityController:
        row = cls(V05PlasticityConfig(**value["config"]))
        row.eligibility = {str(k): float(v) for k, v in value["eligibility"].items()}
        row.reward_trace = float(value["reward_trace"])
        row.update_count = int(value["update_count"])
        return row

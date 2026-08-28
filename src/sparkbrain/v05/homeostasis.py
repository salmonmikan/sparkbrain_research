from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField

from .contracts import StabilitySnapshot


@dataclass(frozen=True, slots=True)
class HomeostasisConfig:
    target_spikes_per_window: float = 0.35
    learning_rate: float = 0.004
    min_threshold: float = 0.35
    max_threshold: float = 2.8
    rate_decay: float = 0.88
    runaway_spikes_per_window: int = 800
    dead_windows_before_flag: int = 6


@dataclass(slots=True)
class HomeostaticController:
    config: HomeostasisConfig = field(default_factory=HomeostasisConfig)
    rate_ema: dict[int, float] = field(default_factory=dict)
    dead_streak: int = 0
    windows: int = 0

    def observe(
        self,
        field: TemporalExcitableField,
        spikes: Iterable[SpikeEvent],
        *,
        time_ms: float,
    ) -> StabilitySnapshot:
        rows = tuple(spikes)
        counts: dict[int, int] = {}
        for spike in rows:
            counts[spike.unit_id] = counts.get(spike.unit_id, 0) + 1
        for unit_id, unit in field.units.items():
            previous = self.rate_ema.get(unit_id, 0.0)
            current = float(counts.get(unit_id, 0))
            rate = self.config.rate_decay * previous + (1.0 - self.config.rate_decay) * current
            self.rate_ema[unit_id] = rate
            delta = self.config.learning_rate * (rate - self.config.target_spikes_per_window)
            unit.base_threshold = max(
                self.config.min_threshold,
                min(self.config.max_threshold, unit.base_threshold + delta),
            )
        self.windows += 1
        if rows:
            self.dead_streak = 0
        else:
            self.dead_streak += 1
        active_fraction = len(counts) / max(1, len(field.units))
        mean_threshold = sum(unit.base_threshold for unit in field.units.values()) / max(
            1, len(field.units)
        )
        return StabilitySnapshot(
            time_ms=time_ms,
            spike_count=len(rows),
            active_unit_fraction=active_fraction,
            runaway=len(rows) > self.config.runaway_spikes_per_window,
            dead=self.dead_streak >= self.config.dead_windows_before_flag,
            mean_threshold=mean_threshold,
        )

    def snapshot(
        self,
        field: TemporalExcitableField,
        spikes: Iterable[SpikeEvent],
        *,
        time_ms: float,
    ) -> StabilitySnapshot:
        rows = tuple(spikes)
        active_ids = {row.unit_id for row in rows}
        mean_threshold = sum(unit.base_threshold for unit in field.units.values()) / max(
            1, len(field.units)
        )
        return StabilitySnapshot(
            time_ms=time_ms,
            spike_count=len(rows),
            active_unit_fraction=len(active_ids) / max(1, len(field.units)),
            runaway=len(rows) > self.config.runaway_spikes_per_window,
            dead=False,
            mean_threshold=mean_threshold,
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "dead_streak": self.dead_streak,
            "rate_ema": {str(k): v for k, v in sorted(self.rate_ema.items())},
            "windows": self.windows,
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> HomeostaticController:
        row = cls(HomeostasisConfig(**value["config"]))
        row.dead_streak = int(value["dead_streak"])
        row.rate_ema = {int(k): float(v) for k, v in value["rate_ema"].items()}
        row.windows = int(value["windows"])
        return row

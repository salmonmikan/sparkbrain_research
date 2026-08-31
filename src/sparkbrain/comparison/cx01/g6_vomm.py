from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from .contract import ComparatorKind
from .events import ComparatorEvent, EventOrigin, PredictionDistribution


@dataclass(frozen=True, slots=True)
class VariableOrderConfig:
    max_order: int = 8
    retention: float = 0.8
    maximum_rollout_steps: int = 8

    def validate(self) -> None:
        if self.max_order < 1:
            raise ValueError("max_order must be positive")
        if not 0.0 < self.retention <= 1.0:
            raise ValueError("retention must be in (0, 1]")
        if self.maximum_rollout_steps < 1:
            raise ValueError("maximum_rollout_steps must be positive")


class VariableOrderMarkovPredictor:
    """External-only variable-order suffix predictor with deterministic backoff.

    Every external transition updates all available suffix contexts up to
    `max_order`. Generated events are never fed back into the learned tables.
    """

    kind = ComparatorKind.G6_VARIABLE_ORDER

    def __init__(self, config: VariableOrderConfig | None = None) -> None:
        self.config = config or VariableOrderConfig()
        self.config.validate()
        self._scores: dict[tuple[str, ...], dict[str, float]] = {}
        self._history: list[str] = []
        self._time_ms = 0.0
        self._suppressed: set[str] = set()
        self._observed_events = 0
        self._generated_events = 0

    def _update_row(self, context: tuple[str, ...], target: str) -> None:
        row = self._scores.setdefault(context, {})
        for candidate in tuple(row):
            row[candidate] *= self.config.retention
        row[target] = row.get(target, 0.0) + 1.0

    def observe_external(self, event: ComparatorEvent) -> None:
        event.validate()
        if event.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G6 accepts external observations only")
        if event.timestamp_ms < self._time_ms:
            raise ValueError("events must be chronological")
        if event.episode_start:
            self._history.clear()
        if self._history:
            upper = min(self.config.max_order, len(self._history))
            for order in range(1, upper + 1):
                self._update_row(tuple(self._history[-order:]), event.token)
        self._history.append(event.token)
        if len(self._history) > self.config.max_order:
            del self._history[: len(self._history) - self.config.max_order]
        self._time_ms = event.timestamp_ms
        self._observed_events += 1

    def advance(self, timestamp_ms: float) -> None:
        if not math.isfinite(timestamp_ms) or timestamp_ms < self._time_ms:
            raise ValueError("time must be finite and monotonic")
        self._time_ms = timestamp_ms

    def _scores_for(self, history: list[str]) -> dict[str, float]:
        if not history or history[-1] in self._suppressed:
            return {}
        upper = min(self.config.max_order, len(history))
        for order in range(upper, 0, -1):
            row = self._scores.get(tuple(history[-order:]))
            if row and sum(row.values()) > 0:
                return row
        return {}

    def _distribution_for(self, history: list[str]) -> PredictionDistribution:
        return PredictionDistribution.from_scores(self._scores_for(history))

    def distribution(self) -> PredictionDistribution:
        return self._distribution_for(list(self._history))

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]:
        if max_steps < 0 or max_steps > self.config.maximum_rollout_steps:
            raise ValueError("rollout steps exceed configured bound")
        virtual_history = list(self._history)
        events: list[ComparatorEvent] = []
        for index in range(max_steps):
            distribution = self._distribution_for(virtual_history).as_dict()
            if not distribution:
                break
            token = min(distribution, key=lambda candidate: (-distribution[candidate], candidate))
            events.append(
                ComparatorEvent(
                    token=token,
                    timestamp_ms=self._time_ms + float(index + 1),
                    origin=EventOrigin.GENERATED,
                )
            )
            virtual_history.append(token)
            if len(virtual_history) > self.config.max_order:
                del virtual_history[: len(virtual_history) - self.config.max_order]
        self._generated_events += len(events)
        return tuple(events)

    def suppress(self, token: str) -> None:
        if not token:
            raise ValueError("suppressed token must be non-empty")
        self._suppressed.add(token)

    def clear_suppression(self) -> None:
        self._suppressed.clear()

    def snapshot(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "generated_events": self._generated_events,
            "history": list(self._history),
            "kind": self.kind.value,
            "observed_events": self._observed_events,
            "scores": [
                {
                    "context": list(context),
                    "targets": dict(sorted(row.items())),
                }
                for context, row in sorted(self._scores.items())
            ],
            "suppressed": sorted(self._suppressed),
            "time_ms": self._time_ms,
        }

    def restore(self, state: dict[str, Any]) -> None:
        if state.get("kind") != self.kind.value:
            raise ValueError("snapshot kind mismatch")
        self.config = VariableOrderConfig(**state["config"])
        self.config.validate()
        self._scores = {
            tuple(row["context"]): {
                str(token): float(score) for token, score in row["targets"].items()
            }
            for row in state["scores"]
        }
        self._history = [str(token) for token in state["history"]]
        self._time_ms = float(state["time_ms"])
        self._suppressed = set(str(token) for token in state["suppressed"])
        self._observed_events = int(state["observed_events"])
        self._generated_events = int(state["generated_events"])

    @property
    def parameter_count(self) -> int:
        return sum(len(row) for row in self._scores.values())

    @property
    def state_entry_count(self) -> int:
        return self.parameter_count + len(self._history)

    @property
    def observed_external_events(self) -> int:
        return self._observed_events

    @property
    def generated_internal_events(self) -> int:
        return self._generated_events

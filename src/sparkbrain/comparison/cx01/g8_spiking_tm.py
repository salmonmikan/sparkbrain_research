from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from typing import Any

from .contract import ComparatorKind
from .events import ComparatorEvent, EventOrigin, PredictionDistribution


@dataclass(frozen=True, slots=True)
class SpikingTemporalMemoryConfig:
    population_size: int = 24
    max_context: int = 4
    lag_tolerance_ms: float = 2.0
    membrane_decay_ms: float = 20.0
    prediction_threshold: float = 2.0
    replay_threshold: float = 1.0
    replay_excitability_gain: float = 1.5
    maximum_rollout_steps: int = 8

    def validate(self) -> None:
        if self.population_size < 2 or self.max_context < 1:
            raise ValueError("spiking population/context configuration is invalid")
        for value in (
            self.lag_tolerance_ms,
            self.membrane_decay_ms,
            self.prediction_threshold,
            self.replay_threshold,
            self.replay_excitability_gain,
        ):
            if not math.isfinite(value) or value <= 0:
                raise ValueError("spiking temporal-memory values must be positive and finite")
        if self.maximum_rollout_steps < 1:
            raise ValueError("maximum_rollout_steps must be positive")


@dataclass(slots=True)
class _Association:
    context_tokens: tuple[str, ...]
    lag_signature: tuple[int, ...]
    target_token: str
    observations: int
    target_lag_sum_ms: float

    @property
    def mean_target_lag_ms(self) -> float:
        return self.target_lag_sum_ms / max(1, self.observations)


class SpikingTemporalMemoryComparator:
    """Small timing-sensitive recurrent spiking comparator for CX01.

    Anonymous tokens map to deterministic neuron populations. Learned recurrent
    associations are indexed by population history and quantized inter-spike
    timing. G8-P exposes the next predictive population only. G8-R uses the same
    learned state with an explicit global replay/excitability mode and may chain
    generated populations without training on them.

    This is a local reference comparator for the CX01 contract, not a claim of
    bit-for-bit reproduction of the published NEST/NESTML sTM implementation.
    """

    def __init__(
        self,
        *,
        replay_mode: bool = False,
        config: SpikingTemporalMemoryConfig | None = None,
    ) -> None:
        self.config = config or SpikingTemporalMemoryConfig()
        self.config.validate()
        self.replay_mode = bool(replay_mode)
        self.kind = ComparatorKind.G8_REPLAY if replay_mode else ComparatorKind.G8_PREDICTION
        self._associations: dict[tuple[tuple[str, ...], tuple[int, ...], str], _Association] = {}
        self._history_tokens: list[str] = []
        self._history_times: list[float] = []
        self._known_tokens: set[str] = set()
        self._suppressed: set[str] = set()
        self._time_ms = 0.0
        self._observed_events = 0
        self._generated_events = 0
        self._membrane: dict[int, tuple[float, float]] = {}

    @staticmethod
    def _hash_int(*parts: object) -> int:
        payload = "|".join(str(part) for part in parts).encode("utf-8")
        return int(hashlib.sha256(payload).hexdigest()[:16], 16)

    def population(self, token: str) -> tuple[int, ...]:
        if not token:
            raise ValueError("token must be non-empty")
        base = self._hash_int("population", token) % 10_000_019
        return tuple(
            base * self.config.population_size + index
            for index in range(self.config.population_size)
        )

    def _activate_population(self, token: str, timestamp_ms: float) -> None:
        for neuron in self.population(token):
            previous_v, previous_t = self._membrane.get(neuron, (0.0, timestamp_ms))
            elapsed = max(0.0, timestamp_ms - previous_t)
            decayed = previous_v * math.exp(-elapsed / self.config.membrane_decay_ms)
            self._membrane[neuron] = (decayed + 1.0, timestamp_ms)

    def _lag_signature(self, times: list[float]) -> tuple[int, ...]:
        if len(times) < 2:
            return ()
        tolerance = self.config.lag_tolerance_ms
        return tuple(
            round((right - left) / tolerance) for left, right in zip(times, times[1:], strict=False)
        )

    def _context(
        self, tokens: list[str], times: list[float]
    ) -> tuple[tuple[str, ...], tuple[int, ...]]:
        width = min(self.config.max_context, len(tokens))
        context_tokens = tuple(tokens[-width:])
        context_times = times[-width:]
        return context_tokens, self._lag_signature(context_times)

    def _learn_target(self, token: str, timestamp_ms: float) -> None:
        if not self._history_tokens:
            return
        context_tokens, lag_signature = self._context(self._history_tokens, self._history_times)
        target_lag = timestamp_ms - self._history_times[-1]
        key = (context_tokens, lag_signature, token)
        association = self._associations.get(key)
        if association is None:
            self._associations[key] = _Association(
                context_tokens=context_tokens,
                lag_signature=lag_signature,
                target_token=token,
                observations=1,
                target_lag_sum_ms=target_lag,
            )
        else:
            association.observations += 1
            association.target_lag_sum_ms += target_lag

    def observe_external(self, event: ComparatorEvent) -> None:
        event.validate()
        if event.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G8 accepts external observations only")
        if event.timestamp_ms < self._time_ms:
            raise ValueError("events must be chronological")
        if event.episode_start:
            self._history_tokens.clear()
            self._history_times.clear()
        self._learn_target(event.token, event.timestamp_ms)
        self._activate_population(event.token, event.timestamp_ms)
        self._history_tokens.append(event.token)
        self._history_times.append(event.timestamp_ms)
        if len(self._history_tokens) > self.config.max_context:
            excess = len(self._history_tokens) - self.config.max_context
            del self._history_tokens[:excess]
            del self._history_times[:excess]
        self._known_tokens.add(event.token)
        self._time_ms = event.timestamp_ms
        self._observed_events += 1

    def advance(self, timestamp_ms: float) -> None:
        if not math.isfinite(timestamp_ms) or timestamp_ms < self._time_ms:
            raise ValueError("time must be finite and monotonic")
        self._time_ms = timestamp_ms

    def _matching(self, tokens: list[str], times: list[float]) -> list[_Association]:
        if not tokens or tokens[-1] in self._suppressed:
            return []
        for width in range(min(self.config.max_context, len(tokens)), 0, -1):
            context_tokens = tuple(tokens[-width:])
            context_times = times[-width:]
            signature = self._lag_signature(context_times)
            rows = [
                row
                for row in self._associations.values()
                if row.context_tokens == context_tokens and row.lag_signature == signature
            ]
            if rows:
                return rows
        return []

    def _scores_for(self, tokens: list[str], times: list[float]) -> dict[str, float]:
        threshold = (
            self.config.replay_threshold if self.replay_mode else self.config.prediction_threshold
        )
        gain = self.config.replay_excitability_gain if self.replay_mode else 1.0
        scores: dict[str, float] = {}
        for row in self._matching(tokens, times):
            effective = row.observations * gain
            if effective < threshold:
                continue
            scores[row.target_token] = scores.get(row.target_token, 0.0) + effective
        return scores

    def distribution(self) -> PredictionDistribution:
        return PredictionDistribution.from_scores(
            self._scores_for(list(self._history_tokens), list(self._history_times))
        )

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]:
        if max_steps < 0 or max_steps > self.config.maximum_rollout_steps:
            raise ValueError("rollout steps exceed configured bound")
        if not self.replay_mode:
            max_steps = min(max_steps, 1)
        tokens = list(self._history_tokens)
        times = list(self._history_times)
        generated: list[ComparatorEvent] = []
        for _ in range(max_steps):
            rows = self._matching(tokens, times)
            scores = self._scores_for(tokens, times)
            if not scores:
                break
            target = min(scores, key=lambda candidate: (-scores[candidate], candidate))
            candidate_rows = [row for row in rows if row.target_token == target]
            lag = sum(row.mean_target_lag_ms * row.observations for row in candidate_rows) / max(
                1, sum(row.observations for row in candidate_rows)
            )
            timestamp = (times[-1] if times else self._time_ms) + max(0.001, lag)
            generated.append(ComparatorEvent(target, timestamp, EventOrigin.GENERATED))
            self._activate_population(target, timestamp)
            tokens.append(target)
            times.append(timestamp)
            if len(tokens) > self.config.max_context:
                excess = len(tokens) - self.config.max_context
                del tokens[:excess]
                del times[:excess]
        self._generated_events += len(generated)
        return tuple(generated)

    def suppress(self, token: str) -> None:
        if not token:
            raise ValueError("suppressed token must be non-empty")
        self._suppressed.add(token)

    def clear_suppression(self) -> None:
        self._suppressed.clear()

    def snapshot(self) -> dict[str, Any]:
        return {
            "associations": [
                {
                    "context_tokens": list(row.context_tokens),
                    "lag_signature": list(row.lag_signature),
                    "observations": row.observations,
                    "target_lag_sum_ms": row.target_lag_sum_ms,
                    "target_token": row.target_token,
                }
                for _, row in sorted(self._associations.items())
            ],
            "config": asdict(self.config),
            "generated_events": self._generated_events,
            "history_times": list(self._history_times),
            "history_tokens": list(self._history_tokens),
            "kind": self.kind.value,
            "known_tokens": sorted(self._known_tokens),
            "observed_events": self._observed_events,
            "replay_mode": self.replay_mode,
            "suppressed": sorted(self._suppressed),
            "time_ms": self._time_ms,
        }

    def restore(self, state: dict[str, Any]) -> None:
        expected = (
            ComparatorKind.G8_REPLAY if state["replay_mode"] else ComparatorKind.G8_PREDICTION
        )
        if state.get("kind") != expected.value:
            raise ValueError("snapshot kind mismatch")
        self.config = SpikingTemporalMemoryConfig(**state["config"])
        self.config.validate()
        self.replay_mode = bool(state["replay_mode"])
        self.kind = expected
        self._associations = {}
        for value in state["associations"]:
            row = _Association(
                context_tokens=tuple(str(token) for token in value["context_tokens"]),
                lag_signature=tuple(int(item) for item in value["lag_signature"]),
                target_token=str(value["target_token"]),
                observations=int(value["observations"]),
                target_lag_sum_ms=float(value["target_lag_sum_ms"]),
            )
            self._associations[(row.context_tokens, row.lag_signature, row.target_token)] = row
        self._history_tokens = [str(token) for token in state["history_tokens"]]
        self._history_times = [float(value) for value in state["history_times"]]
        self._known_tokens = set(str(token) for token in state["known_tokens"])
        self._suppressed = set(str(token) for token in state["suppressed"])
        self._time_ms = float(state["time_ms"])
        self._observed_events = int(state["observed_events"])
        self._generated_events = int(state["generated_events"])
        self._membrane = {}

    @property
    def parameter_count(self) -> int:
        return len(self._associations) * (self.config.population_size + 2)

    @property
    def state_entry_count(self) -> int:
        return self.parameter_count + len(self._history_tokens) + len(self._membrane)

    @property
    def observed_external_events(self) -> int:
        return self._observed_events

    @property
    def generated_internal_events(self) -> int:
        return self._generated_events

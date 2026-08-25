from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, fields

from .contracts import PerceptualSpark, SensorySample


@dataclass(frozen=True, slots=True)
class SensoryFieldConfig:
    prediction_rate: float = 0.25
    variability_rate: float = 0.15
    habituation_rate: float = 0.22
    habituation_release: float = 0.55
    habituation_penalty: float = 1.25
    novelty_gain: float = 1.0
    goal_gain: float = 0.9
    onset_bonus: float = 1.25
    base_threshold: float = 1.0
    threshold_increment: float = 0.20
    threshold_relaxation: float = 0.12
    minimum_scale: float = 0.10
    stable_error_ratio: float = 0.35
    max_active: int = 8

    def validate(self) -> None:
        if self.max_active < 1:
            raise ValueError("max_active must be >= 1")
        for item in fields(self):
            name = item.name
            value = getattr(self, name)
            if name == "max_active":
                continue
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")


@dataclass(slots=True)
class _FeatureState:
    prediction: float = 0.0
    variability: float = 1.0
    habituation: float = 0.0
    threshold: float = 1.0
    initialized: bool = False
    last_value: float = 0.0
    last_time: float = 0.0


class AdaptiveSensoryField:
    """A small, deterministic reference for active input selection.

    It is not a biological retinal model.  It instantiates four testable ideas:

    * input is continuous rather than pre-decoded into an answer;
    * predictable repetition is progressively suppressed;
    * unexpected change produces prediction-error salience;
    * a top-down goal can bias which low-level channel crosses threshold.
    """

    def __init__(self, config: SensoryFieldConfig | None = None) -> None:
        self.config = config or SensoryFieldConfig()
        self.config.validate()
        self._states: dict[str, _FeatureState] = {}
        self._sequence = 0

    def reset(self) -> None:
        self._states.clear()
        self._sequence = 0

    def feature_state(self, feature_id: str) -> dict[str, float | bool]:
        state = self._states[feature_id]
        return {
            "prediction": state.prediction,
            "variability": state.variability,
            "habituation": state.habituation,
            "threshold": state.threshold,
            "initialized": state.initialized,
            "last_value": state.last_value,
            "last_time": state.last_time,
        }

    def observe(
        self,
        sample: SensorySample,
        *,
        goal_bias: dict[str, float] | None = None,
    ) -> tuple[PerceptualSpark, ...]:
        sample.validate()
        bias = goal_bias or {}
        candidates: list[tuple[float, str, PerceptualSpark]] = []

        for local_name, raw_value in sorted(sample.values.items()):
            value = float(raw_value)
            feature_id = f"{sample.modality}:{local_name}"
            state = self._states.setdefault(
                feature_id,
                _FeatureState(threshold=self.config.base_threshold),
            )
            if sample.time < state.last_time:
                raise ValueError("sensory samples must not move a feature backward in time")

            onset = 0.0 if state.initialized else 1.0
            prediction_error = abs(value - state.prediction) if state.initialized else abs(value)
            scale = max(self.config.minimum_scale, state.variability)
            normalized_error = prediction_error / scale
            stable = state.initialized and prediction_error <= (
                self.config.stable_error_ratio * scale
            )

            if stable:
                state.habituation += self.config.habituation_rate * (1.0 - state.habituation)
            else:
                state.habituation *= max(0.0, 1.0 - self.config.habituation_release)

            top_down = max(0.0, float(bias.get(feature_id, bias.get(local_name, 0.0))))
            salience = (
                self.config.onset_bonus * onset
                + self.config.novelty_gain * normalized_error
                + self.config.goal_gain * top_down
                - self.config.habituation_penalty * state.habituation
            )
            salience = max(0.0, salience)
            fired = salience >= state.threshold

            if fired:
                digest = hashlib.sha256(
                    f"{sample.sample_id}:{feature_id}:{self._sequence}".encode()
                ).hexdigest()[:16]
                candidates.append(
                    (
                        salience,
                        feature_id,
                        PerceptualSpark(
                            spark_id=f"percept:{digest}",
                            feature_id=feature_id,
                            time=sample.time,
                            activation=value,
                            salience=salience,
                            prediction_error=prediction_error,
                            threshold=state.threshold,
                            evidence_id=f"percept:{digest}",
                            source_id=sample.source_id,
                            correlation_group=(
                                sample.correlation_group or f"sample:{sample.sample_id}"
                            ),
                            entity_slot=sample.entity_hint,
                            parents=(sample.sample_id,),
                        ),
                    )
                )
                state.threshold += self.config.threshold_increment
            else:
                state.threshold += self.config.threshold_relaxation * (
                    self.config.base_threshold - state.threshold
                )

            if not state.initialized:
                state.prediction = value
                state.variability = max(self.config.minimum_scale, abs(value))
                state.initialized = True
            else:
                state.prediction += self.config.prediction_rate * (value - state.prediction)
                state.variability += self.config.variability_rate * (
                    prediction_error - state.variability
                )
                state.variability = max(self.config.minimum_scale, state.variability)
            state.last_value = value
            state.last_time = sample.time
            self._sequence += 1

        candidates.sort(key=lambda row: (-row[0], row[1]))
        return tuple(row[2] for row in candidates[: self.config.max_active])

from __future__ import annotations

import copy
import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import asdict, dataclass, fields
from types import MappingProxyType
from typing import Any

from .contracts import PerceptualSpark, SensorySample

SENSORY_STATE_SCHEMA_VERSION = "0.3"
_ALLOWED_ABLATIONS = {
    "no_goal",
    "no_habituation",
    "no_magnitude",
    "no_novelty",
    "no_prediction_error",
}
_FORBIDDEN_GOAL_FIELDS = {
    "answer",
    "contradiction",
    "evaluator",
    "gold",
    "label",
    "split",
    "target",
    "test_only",
    "truth",
}


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _hash_payload(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _normalized_name(value: object) -> str:
    return str(value).strip().lower().replace("-", "_")


@dataclass(frozen=True, slots=True)
class SensoryFieldConfig:
    prediction_rate: float = 0.25
    variability_rate: float = 0.15
    habituation_rate: float = 0.22
    habituation_release: float = 0.55
    habituation_penalty: float = 1.25
    magnitude_gain: float = 0.15
    magnitude_cap: float = 2.0
    novelty_gain: float = 1.20
    goal_gain: float = 0.90
    max_goal_bias: float = 0.35
    onset_bonus: float = 1.25
    base_threshold: float = 0.90
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
    threshold: float = 0.90
    initialized: bool = False
    last_value: float = 0.0
    last_time: float = 0.0


@dataclass(frozen=True, slots=True)
class SensoryWorkCounters:
    channels_inspected: int = 0
    features_scored: int = 0
    state_updates: int = 0
    candidate_channels: int = 0
    sparks_emitted: int = 0
    suppressed_channels: int = 0
    downstream_active_work: int = 0

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SensoryChannelTrace:
    sample_id: str
    feature_id: str
    omission: bool
    accepted: bool
    suppression_reason: str | None
    activation: float
    magnitude: float
    magnitude_contribution: float
    prediction_error: float
    normalized_novelty: float
    prediction_error_contribution: float
    novelty_contribution: float
    habituation: float
    habituation_contribution: float
    goal_bias_requested: float
    goal_bias_applied: float
    goal_contribution: float
    onset: float
    onset_contribution: float
    threshold: float
    final_salience: float
    ablations: tuple[str, ...]
    spark_id: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SensoryObservation:
    sparks: tuple[PerceptualSpark, ...]
    channel_trace: tuple[SensoryChannelTrace, ...]
    work_delta: SensoryWorkCounters
    work_total: SensoryWorkCounters
    state_hash_before: str
    state_hash_after: str


class AdaptiveSensoryField:
    """Deterministic, inspectable computational sensory gate.

    This is not a biological sensory-system reproduction. Dense channel scoring is
    reported separately from emitted downstream active work.
    """

    def __init__(self, config: SensoryFieldConfig | None = None) -> None:
        self.config = config or SensoryFieldConfig()
        self.config.validate()
        self._states: dict[str, _FeatureState] = {}
        self._sequence = 0
        self._counters = SensoryWorkCounters()

    def reset(self) -> None:
        self._states.clear()
        self._sequence = 0
        self._counters = SensoryWorkCounters()

    def feature_state(self, feature_id: str) -> Mapping[str, float | bool]:
        return MappingProxyType(asdict(self._states[feature_id]))

    def inspect_state(self) -> Mapping[str, Any]:
        return MappingProxyType(copy.deepcopy(self._state_payload()))

    def state_hash(self) -> str:
        return _hash_payload(self._state_payload())

    def serialize_state(self) -> str:
        return _canonical_json(self._state_payload())

    @classmethod
    def from_serialized_state(cls, payload: str) -> AdaptiveSensoryField:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("sensory state must be valid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError("sensory state must be a JSON object")
        expected = {"config", "counters", "features", "schema_version", "sequence"}
        if set(value) != expected:
            raise ValueError("sensory state has unexpected fields")
        if value["schema_version"] != SENSORY_STATE_SCHEMA_VERSION:
            raise ValueError("unsupported sensory state schema version")
        try:
            field = cls(SensoryFieldConfig(**value["config"]))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid serialized sensory config") from exc
        feature_fields = {item.name for item in fields(_FeatureState)}
        if not isinstance(value["features"], dict):
            raise ValueError("sensory state features must be an object")
        parsed_states: dict[str, _FeatureState] = {}
        for feature_id, state_value in value["features"].items():
            if (
                not feature_id
                or not isinstance(state_value, dict)
                or set(state_value) != feature_fields
            ):
                raise ValueError("invalid serialized feature state")
            try:
                state = _FeatureState(**state_value)
                field._validate_feature_state(state)
            except (TypeError, ValueError) as exc:
                raise ValueError("invalid serialized feature state") from exc
            parsed_states[feature_id] = state
        counter_fields = {item.name for item in fields(SensoryWorkCounters)}
        if not isinstance(value["counters"], dict) or set(value["counters"]) != counter_fields:
            raise ValueError("invalid serialized sensory counters")
        try:
            counters = SensoryWorkCounters(**value["counters"])
        except TypeError as exc:
            raise ValueError("invalid serialized sensory counters") from exc
        if any(count < 0 or not isinstance(count, int) for count in counters.as_dict().values()):
            raise ValueError("sensory counters must be non-negative integers")
        sequence = value["sequence"]
        if not isinstance(sequence, int) or sequence < 0:
            raise ValueError("sensory sequence must be a non-negative integer")
        field._states = parsed_states
        field._counters = counters
        field._sequence = sequence
        if field.serialize_state() != payload:
            raise ValueError("sensory state payload is not strict canonical JSON")
        return field

    def observe(
        self,
        sample: SensorySample,
        *,
        goal_bias: Mapping[str, float] | None = None,
        ablations: frozenset[str] | None = None,
        bypass: bool = False,
    ) -> tuple[PerceptualSpark, ...]:
        return self.observe_with_trace(
            sample, goal_bias=goal_bias, ablations=ablations, bypass=bypass
        ).sparks

    def observe_with_trace(
        self,
        sample: SensorySample,
        *,
        goal_bias: Mapping[str, float] | None = None,
        ablations: frozenset[str] | None = None,
        bypass: bool = False,
    ) -> SensoryObservation:
        sample.validate()
        bias = self._validated_goal_bias(goal_bias or {})
        disabled = frozenset(ablations or ())
        unknown_ablations = disabled - _ALLOWED_ABLATIONS
        if unknown_ablations:
            raise ValueError(f"unknown sensory ablation: {sorted(unknown_ablations)}")

        working_states = copy.deepcopy(self._states)
        working_sequence = self._sequence
        state_hash_before = self.state_hash()
        rows: list[dict[str, Any]] = []
        channel_names = sorted(set(sample.values) | set(sample.omitted_channels))
        for local_name in channel_names:
            feature_id = f"{sample.modality}:{local_name}"
            omission = local_name in sample.omitted_channels
            if omission and (
                feature_id not in working_states or not working_states[feature_id].initialized
            ):
                raise ValueError("explicit omission requires a previously observed channel")
            value = 0.0 if omission else float(sample.values[local_name])
            state = working_states.setdefault(
                feature_id, _FeatureState(threshold=self.config.base_threshold)
            )
            self._validate_feature_state(state)
            if sample.time < state.last_time:
                raise ValueError("sensory samples must not move a feature backward in time")

            onset = 0.0 if state.initialized or omission else 1.0
            prediction_error = abs(value - state.prediction) if state.initialized else abs(value)
            scale = max(self.config.minimum_scale, state.variability)
            normalized_novelty = prediction_error / scale
            stable = state.initialized and not omission and prediction_error <= (
                self.config.stable_error_ratio * scale
            )
            if stable:
                state.habituation += self.config.habituation_rate * (1.0 - state.habituation)
            else:
                state.habituation *= max(0.0, 1.0 - self.config.habituation_release)

            requested = float(bias.get(feature_id, bias.get(local_name, 0.0)))
            applied = min(self.config.max_goal_bias, max(0.0, requested))
            magnitude = abs(value)
            magnitude_contribution = (
                0.0
                if "no_magnitude" in disabled
                else self.config.magnitude_gain * min(magnitude, self.config.magnitude_cap)
            )
            half_novelty = 0.5 * self.config.novelty_gain * normalized_novelty
            prediction_error_contribution = (
                0.0 if "no_prediction_error" in disabled else half_novelty
            )
            novelty_contribution = 0.0 if "no_novelty" in disabled else half_novelty
            habituation_contribution = (
                0.0
                if "no_habituation" in disabled
                else -self.config.habituation_penalty * state.habituation
            )
            goal_contribution = (
                0.0 if "no_goal" in disabled else self.config.goal_gain * applied
            )
            onset_contribution = self.config.onset_bonus * onset
            final_salience = max(
                0.0,
                magnitude_contribution
                + prediction_error_contribution
                + novelty_contribution
                + habituation_contribution
                + goal_contribution
                + onset_contribution,
            )
            candidate = (bypass and not omission) or final_salience >= state.threshold
            digest = hashlib.sha256(
                f"{sample.sample_id}:{feature_id}:{working_sequence}".encode()
            ).hexdigest()[:16]
            rows.append(
                {
                    "feature_id": feature_id,
                    "omission": omission,
                    "value": value,
                    "magnitude": magnitude,
                    "magnitude_contribution": magnitude_contribution,
                    "prediction_error": prediction_error,
                    "normalized_novelty": normalized_novelty,
                    "prediction_error_contribution": prediction_error_contribution,
                    "novelty_contribution": novelty_contribution,
                    "habituation": state.habituation,
                    "habituation_contribution": habituation_contribution,
                    "goal_bias_requested": requested,
                    "goal_bias_applied": applied,
                    "goal_contribution": goal_contribution,
                    "onset": onset,
                    "onset_contribution": onset_contribution,
                    "threshold": state.threshold,
                    "final_salience": final_salience,
                    "candidate": candidate,
                    "spark_id": f"percept:{digest}",
                    "state": state,
                }
            )
            working_sequence += 1

        candidates = sorted(
            (row for row in rows if row["candidate"]),
            key=lambda row: (-row["final_salience"], row["feature_id"]),
        )
        selected = candidates if bypass else candidates[: self.config.max_active]
        accepted_ids = {id(row) for row in selected}
        sparks: list[PerceptualSpark] = []
        trace: list[SensoryChannelTrace] = []
        for row in rows:
            accepted = id(row) in accepted_ids
            state = row["state"]
            if accepted:
                state.threshold += self.config.threshold_increment
                spark = PerceptualSpark(
                    spark_id=row["spark_id"],
                    feature_id=row["feature_id"],
                    time=sample.time,
                    activation=row["value"],
                    salience=row["final_salience"],
                    prediction_error=row["prediction_error"],
                    threshold=row["threshold"],
                    evidence_id=row["spark_id"],
                    source_id=sample.source_id,
                    correlation_group=sample.correlation_group or f"sample:{sample.sample_id}",
                    entity_slot=sample.entity_hint,
                    parents=(sample.sample_id,),
                )
                spark.validate()
                sparks.append(spark)
                suppression_reason = None
            else:
                state.threshold += self.config.threshold_relaxation * (
                    self.config.base_threshold - state.threshold
                )
                suppression_reason = "top_k_budget" if row["candidate"] else "below_threshold"

            value = row["value"]
            prediction_error = row["prediction_error"]
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
            self._validate_feature_state(state)
            trace.append(
                SensoryChannelTrace(
                    sample_id=sample.sample_id,
                    feature_id=row["feature_id"],
                    omission=row["omission"],
                    accepted=accepted,
                    suppression_reason=suppression_reason,
                    activation=value,
                    magnitude=row["magnitude"],
                    magnitude_contribution=row["magnitude_contribution"],
                    prediction_error=prediction_error,
                    normalized_novelty=row["normalized_novelty"],
                    prediction_error_contribution=row["prediction_error_contribution"],
                    novelty_contribution=row["novelty_contribution"],
                    habituation=row["habituation"],
                    habituation_contribution=row["habituation_contribution"],
                    goal_bias_requested=row["goal_bias_requested"],
                    goal_bias_applied=row["goal_bias_applied"],
                    goal_contribution=row["goal_contribution"],
                    onset=row["onset"],
                    onset_contribution=row["onset_contribution"],
                    threshold=row["threshold"],
                    final_salience=row["final_salience"],
                    ablations=tuple(sorted(disabled)),
                    spark_id=row["spark_id"] if accepted else None,
                )
            )

        delta = SensoryWorkCounters(
            channels_inspected=len(rows),
            features_scored=len(rows),
            state_updates=len(rows),
            candidate_channels=len(candidates),
            sparks_emitted=len(sparks),
            suppressed_channels=len(rows) - len(sparks),
            downstream_active_work=len(sparks),
        )
        totals = SensoryWorkCounters(
            **{
                name: getattr(self._counters, name) + getattr(delta, name)
                for name in delta.as_dict()
            }
        )
        self._states = working_states
        self._sequence = working_sequence
        self._counters = totals
        return SensoryObservation(
            sparks=tuple(sparks),
            channel_trace=tuple(trace),
            work_delta=delta,
            work_total=totals,
            state_hash_before=state_hash_before,
            state_hash_after=self.state_hash(),
        )

    def _validated_goal_bias(self, bias: Mapping[str, float]) -> dict[str, float]:
        if not isinstance(bias, Mapping):
            raise ValueError("goal bias must be a mapping")
        result: dict[str, float] = {}
        for key, value in bias.items():
            if not isinstance(key, str) or not key:
                raise ValueError("goal bias channel names must be non-empty strings")
            if _normalized_name(key) in _FORBIDDEN_GOAL_FIELDS:
                raise ValueError(f"forbidden goal field: {key}")
            try:
                numeric = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError("goal bias values must be numeric") from exc
            if not math.isfinite(numeric):
                raise ValueError("goal bias values must be finite")
            result[key] = numeric
        return result

    def _state_payload(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "counters": self._counters.as_dict(),
            "features": {
                feature_id: asdict(self._states[feature_id])
                for feature_id in sorted(self._states)
            },
            "schema_version": SENSORY_STATE_SCHEMA_VERSION,
            "sequence": self._sequence,
        }

    @staticmethod
    def _validate_feature_state(state: _FeatureState) -> None:
        for name in (
            "prediction",
            "variability",
            "habituation",
            "threshold",
            "last_value",
            "last_time",
        ):
            if not math.isfinite(getattr(state, name)):
                raise ValueError(f"sensory feature state {name} must be finite")
        if state.variability < 0 or state.habituation < 0 or state.threshold < 0:
            raise ValueError(
                "sensory feature scales, habituation, and threshold must be non-negative"
            )

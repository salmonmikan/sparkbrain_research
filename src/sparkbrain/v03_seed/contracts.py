from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

SENSORY_CONTRACT_VERSION = "0.3"
_FORBIDDEN_SENSORY_FIELDS = {
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


def _normalized_field_name(value: object) -> str:
    return str(value).strip().lower().replace("-", "_")


def _reject_forbidden_sensory_fields(value: object, *, path: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if _normalized_field_name(key) in _FORBIDDEN_SENSORY_FIELDS:
                raise ValueError(f"forbidden sensory field at {path}.{key}")
            _reject_forbidden_sensory_fields(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_forbidden_sensory_fields(child, path=f"{path}[{index}]")


@dataclass(frozen=True, slots=True)
class SensorySample:
    """A local-only, low-level observation used by the v0.3 seed sensory field.

    ``values`` deliberately contains continuous named channels rather than a
    pre-decoded answer.  A real modality adapter may produce these channels from
    pixels, audio samples, text fragments, or simulator state, but the cognitive
    core must not receive evaluator-owned truth labels.
    """

    sample_id: str
    time: float
    source_id: str
    modality: str
    values: Mapping[str, float]
    correlation_group: str | None = None
    entity_hint: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    omitted_channels: tuple[str, ...] = ()
    schema_version: str = SENSORY_CONTRACT_VERSION

    def validate(self) -> None:
        if self.schema_version != SENSORY_CONTRACT_VERSION:
            raise ValueError(f"unsupported sensory schema version: {self.schema_version}")
        if not self.sample_id or not self.source_id or not self.modality:
            raise ValueError("sample_id, source_id, and modality must not be empty")
        if not math.isfinite(self.time) or self.time < 0:
            raise ValueError("sample time must be finite and >= 0")
        if not self.values and not self.omitted_channels:
            raise ValueError("a sensory sample requires a value or explicit omission")
        for feature, value in self.values.items():
            if not feature:
                raise ValueError("sensory feature names must not be empty")
            if not math.isfinite(float(value)):
                raise ValueError(f"sensory value for {feature!r} must be finite")
        if len(set(self.omitted_channels)) != len(self.omitted_channels):
            raise ValueError("explicit omission channels must be unique")
        for feature in self.omitted_channels:
            if not feature:
                raise ValueError("explicit omission channel names must not be empty")
            if feature in self.values:
                raise ValueError("a channel cannot contain a value and an explicit omission")
        _reject_forbidden_sensory_fields(self.metadata, path="metadata")
        try:
            json.dumps(self.metadata, allow_nan=False, ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("sensory metadata must be finite JSON data") from exc

    def to_canonical_json(self) -> str:
        self.validate()
        payload = {
            "correlation_group": self.correlation_group,
            "entity_hint": self.entity_hint,
            "metadata": self.metadata,
            "modality": self.modality,
            "omitted_channels": list(self.omitted_channels),
            "sample_id": self.sample_id,
            "schema_version": self.schema_version,
            "source_id": self.source_id,
            "time": self.time,
            "values": dict(sorted(self.values.items())),
        }
        return json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_canonical_json(cls, payload: str) -> SensorySample:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("sensory sample must be valid JSON") from exc
        expected = {
            "correlation_group",
            "entity_hint",
            "metadata",
            "modality",
            "omitted_channels",
            "sample_id",
            "schema_version",
            "source_id",
            "time",
            "values",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("sensory sample canonical payload has unexpected fields")
        sample = cls(
            sample_id=value["sample_id"],
            time=value["time"],
            source_id=value["source_id"],
            modality=value["modality"],
            values=value["values"],
            correlation_group=value["correlation_group"],
            entity_hint=value["entity_hint"],
            metadata=value["metadata"],
            omitted_channels=tuple(value["omitted_channels"]),
            schema_version=value["schema_version"],
        )
        if sample.to_canonical_json() != payload:
            raise ValueError("sensory sample payload is not strict canonical JSON")
        return sample


@dataclass(frozen=True, slots=True)
class PerceptualSpark:
    """A sparse event emitted by the adaptive sensory field."""

    spark_id: str
    feature_id: str
    time: float
    activation: float
    salience: float
    prediction_error: float
    threshold: float
    evidence_id: str
    source_id: str
    correlation_group: str | None = None
    entity_slot: str | None = None
    parents: tuple[str, ...] = ()
    schema_version: str = SENSORY_CONTRACT_VERSION

    def validate(self) -> None:
        if self.schema_version != SENSORY_CONTRACT_VERSION:
            raise ValueError(f"unsupported sensory schema version: {self.schema_version}")
        for name, value in (
            ("spark_id", self.spark_id),
            ("feature_id", self.feature_id),
            ("evidence_id", self.evidence_id),
            ("source_id", self.source_id),
        ):
            if not value:
                raise ValueError(f"{name} must not be empty")
        for name, value in (
            ("time", self.time),
            ("activation", self.activation),
            ("salience", self.salience),
            ("prediction_error", self.prediction_error),
            ("threshold", self.threshold),
        ):
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.time < 0 or self.salience < 0 or self.prediction_error < 0 or self.threshold < 0:
            raise ValueError("time, salience, prediction_error, and threshold must be non-negative")
        if len(set(self.parents)) != len(self.parents) or any(
            not parent for parent in self.parents
        ):
            raise ValueError("parents must contain unique non-empty IDs")

    def to_canonical_json(self) -> str:
        self.validate()
        payload = {
            "activation": self.activation,
            "correlation_group": self.correlation_group,
            "entity_slot": self.entity_slot,
            "evidence_id": self.evidence_id,
            "feature_id": self.feature_id,
            "parents": list(self.parents),
            "prediction_error": self.prediction_error,
            "salience": self.salience,
            "schema_version": self.schema_version,
            "source_id": self.source_id,
            "spark_id": self.spark_id,
            "threshold": self.threshold,
            "time": self.time,
        }
        return json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_canonical_json(cls, payload: str) -> PerceptualSpark:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("PerceptualSpark must be valid JSON") from exc
        expected = {
            "activation",
            "correlation_group",
            "entity_slot",
            "evidence_id",
            "feature_id",
            "parents",
            "prediction_error",
            "salience",
            "schema_version",
            "source_id",
            "spark_id",
            "threshold",
            "time",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("PerceptualSpark canonical payload has unexpected fields")
        spark = cls(
            spark_id=value["spark_id"],
            feature_id=value["feature_id"],
            time=value["time"],
            activation=value["activation"],
            salience=value["salience"],
            prediction_error=value["prediction_error"],
            threshold=value["threshold"],
            evidence_id=value["evidence_id"],
            source_id=value["source_id"],
            correlation_group=value["correlation_group"],
            entity_slot=value["entity_slot"],
            parents=tuple(value["parents"]),
            schema_version=value["schema_version"],
        )
        if spark.to_canonical_json() != payload:
            raise ValueError("PerceptualSpark payload is not strict canonical JSON")
        return spark


@dataclass(frozen=True, slots=True)
class EvidenceContribution:
    """One attributable contribution to one candidate belief.

    Evidence identity and correlation group are first-class.  Repeated delivery
    of the same evidence ID is not independent evidence, and multiple evidence
    IDs in one correlation group are discounted by the ledger.
    """

    evidence_id: str
    source_id: str
    belief_key: str
    time: float
    support: float = 0.0
    contradiction: float = 0.0
    correlation_group: str | None = None
    object_key: str | None = None
    parent_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.evidence_id or not self.source_id or not self.belief_key:
            raise ValueError("evidence_id, source_id, and belief_key must not be empty")
        for name, value in (
            ("time", self.time),
            ("support", self.support),
            ("contradiction", self.contradiction),
        ):
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.time < 0 or self.support < 0 or self.contradiction < 0:
            raise ValueError("time, support, and contradiction must be non-negative")
        if self.support > 0 and self.contradiction > 0:
            raise ValueError("one contribution cannot support and contradict simultaneously")


@dataclass(frozen=True, slots=True)
class EvidenceSummary:
    belief_key: str
    object_key: str | None
    effective_support: float
    effective_contradiction: float
    redundancy: float
    unique_evidence_count: int
    source_count: int
    independent_group_count: int
    support_ids: tuple[str, ...]
    contradiction_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ConceptCandidate:
    concept_id: str
    members: tuple[str, ...]
    strength: float
    observations: int
    reuse_count: int
    first_seen: float
    last_seen: float


@dataclass(frozen=True, slots=True)
class CoalitionState:
    belief_key: str
    object_key: str | None
    score: float
    activation: float
    effective_support: float
    effective_contradiction: float
    redundancy: float
    source_count: int
    independent_group_count: int
    evidence_count: int
    stability: int
    support_ids: tuple[str, ...]
    contradiction_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IgnitionDecision:
    ignited: bool
    belief_key: str | None
    object_key: str | None
    score: float
    margin: float
    reason: str
    coalitions: tuple[CoalitionState, ...]


@dataclass(slots=True)
class BeliefActivation:
    object_key: str | None
    belief_key: str
    activation: float = 0.0
    last_score: float = 0.0
    last_update_time: float = 0.0
    ignition_count: int = 0
    cited_evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class OrganEvidence:
    candidate_id: str
    seed_consistency: int
    structural_cohesion: float
    functional_selectivity: float
    held_out_reuse: float
    targeted_impairment: float
    matched_random_impairment: float
    unrelated_collateral: float


@dataclass(frozen=True, slots=True)
class OrganAssessment:
    accepted: bool
    passed_gates: tuple[str, ...]
    failed_gates: tuple[str, ...]
    reason: str

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
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
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
class EvidenceRecord:
    """Immutable v0.3 evidence identity and lineage contract."""

    evidence_id: str
    source_id: str
    entity_key: str
    hypothesis_id: str
    time: float
    polarity: str
    strength: float
    correlation_group: str | None = None
    parent_evidence_ids: tuple[str, ...] = ()
    parent_spark_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    schema_version: str = SENSORY_CONTRACT_VERSION

    def validate(self) -> None:
        if self.schema_version != SENSORY_CONTRACT_VERSION:
            raise ValueError(f"unsupported evidence schema version: {self.schema_version}")
        for name, value in (
            ("evidence_id", self.evidence_id),
            ("source_id", self.source_id),
            ("entity_key", self.entity_key),
            ("hypothesis_id", self.hypothesis_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if self.polarity not in {"support", "contradict", "neutral"}:
            raise ValueError("polarity must be support, contradict, or neutral")
        if (
            isinstance(self.time, bool)
            or not isinstance(self.time, (int, float))
            or not math.isfinite(self.time)
            or self.time < 0
        ):
            raise ValueError("evidence time must be finite and non-negative")
        if (
            isinstance(self.strength, bool)
            or not isinstance(self.strength, (int, float))
            or not math.isfinite(self.strength)
            or self.strength < 0
        ):
            raise ValueError("evidence strength must be finite and non-negative")
        if self.correlation_group is not None and (
            not isinstance(self.correlation_group, str)
            or not self.correlation_group.strip()
        ):
            raise ValueError("correlation_group must be a non-empty string when present")
        for name, values in (
            ("parent_evidence_ids", self.parent_evidence_ids),
            ("parent_spark_ids", self.parent_spark_ids),
        ):
            if not isinstance(values, tuple) or any(
                not isinstance(value, str) for value in values
            ):
                raise ValueError(f"{name} must be a tuple of strings")
            if tuple(sorted(values)) != values or len(set(values)) != len(values):
                raise ValueError(f"{name} must be sorted and unique")
            if any(not value.strip() for value in values):
                raise ValueError(f"{name} must not contain empty IDs")
        if not self.parent_spark_ids:
            raise ValueError("parent_spark_ids requires at least one resolvable Spark")
        if not isinstance(self.metadata, Mapping):
            raise ValueError("evidence metadata must be a mapping")
        _reject_forbidden_sensory_fields(self.metadata, path="metadata")
        try:
            json.dumps(self.metadata, allow_nan=False, ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("evidence metadata must be finite JSON data") from exc

    def to_canonical_json(self) -> str:
        self.validate()
        return json.dumps(
            {
                "correlation_group": self.correlation_group,
                "entity_key": self.entity_key,
                "evidence_id": self.evidence_id,
                "hypothesis_id": self.hypothesis_id,
                "metadata": self.metadata,
                "parent_evidence_ids": list(self.parent_evidence_ids),
                "parent_spark_ids": list(self.parent_spark_ids),
                "polarity": self.polarity,
                "schema_version": self.schema_version,
                "source_id": self.source_id,
                "strength": self.strength,
                "time": self.time,
            },
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_canonical_json(cls, payload: str) -> EvidenceRecord:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("EvidenceRecord must be valid JSON") from exc
        expected = {
            "correlation_group",
            "entity_key",
            "evidence_id",
            "hypothesis_id",
            "metadata",
            "parent_evidence_ids",
            "parent_spark_ids",
            "polarity",
            "schema_version",
            "source_id",
            "strength",
            "time",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("EvidenceRecord canonical payload has unexpected fields")
        record = cls(
            evidence_id=value["evidence_id"],
            source_id=value["source_id"],
            entity_key=value["entity_key"],
            hypothesis_id=value["hypothesis_id"],
            time=value["time"],
            polarity=value["polarity"],
            strength=value["strength"],
            correlation_group=value["correlation_group"],
            parent_evidence_ids=tuple(value["parent_evidence_ids"]),
            parent_spark_ids=tuple(value["parent_spark_ids"]),
            metadata=value["metadata"],
            schema_version=value["schema_version"],
        )
        if record.to_canonical_json() != payload:
            raise ValueError("EvidenceRecord payload is not strict canonical JSON")
        return record

    def to_contribution(self) -> EvidenceContribution:
        return EvidenceContribution(
            evidence_id=self.evidence_id,
            source_id=self.source_id,
            belief_key=self.hypothesis_id,
            time=self.time,
            support=self.strength if self.polarity == "support" else 0.0,
            contradiction=self.strength if self.polarity == "contradict" else 0.0,
            correlation_group=self.correlation_group,
            object_key=None if self.entity_key == "__global__" else self.entity_key,
            parent_ids=self.parent_evidence_ids,
        )


@dataclass(frozen=True, slots=True)
class EvidenceAuditRow:
    schema_version: str
    audit_id: str
    sequence: int
    branch_id: str
    action: str
    evidence_id: str
    event_time: float
    reason: str
    before_active: bool | None
    after_active: bool | None
    payload_hash: str
    active_state_hash_before: str
    active_state_hash_after: str
    previous_audit_hash: str
    audit_hash: str

    def validate(self) -> None:
        if self.schema_version != SENSORY_CONTRACT_VERSION:
            raise ValueError(f"unsupported evidence audit schema: {self.schema_version}")
        if (
            isinstance(self.sequence, bool)
            or not isinstance(self.sequence, int)
            or self.sequence < 0
            or self.audit_id != f"audit:{self.sequence:08d}"
        ):
            raise ValueError("audit sequence and audit_id must match")
        if self.action not in {"add", "redelivery_noop", "rejection", "deactivate", "restore"}:
            raise ValueError("invalid evidence audit action")
        if any(
            not isinstance(value, str) or not value.strip()
            for value in (self.branch_id, self.evidence_id, self.reason)
        ):
            raise ValueError("audit branch, evidence, and reason must not be empty")
        if (
            isinstance(self.event_time, bool)
            or not isinstance(self.event_time, (int, float))
            or not math.isfinite(self.event_time)
            or self.event_time < 0
        ):
            raise ValueError("audit event_time must be finite and non-negative")
        for name, value in (
            ("payload_hash", self.payload_hash),
            ("active_state_hash_before", self.active_state_hash_before),
            ("active_state_hash_after", self.active_state_hash_after),
            ("previous_audit_hash", self.previous_audit_hash),
            ("audit_hash", self.audit_hash),
        ):
            if not isinstance(value, str) or len(value) != 64 or any(
                character not in "0123456789abcdef" for character in value
            ):
                raise ValueError(f"{name} must be a lowercase SHA-256")

    def to_canonical_json(self) -> str:
        self.validate()
        return json.dumps(
            {
                "action": self.action,
                "active_state_hash_after": self.active_state_hash_after,
                "active_state_hash_before": self.active_state_hash_before,
                "after_active": self.after_active,
                "audit_hash": self.audit_hash,
                "audit_id": self.audit_id,
                "before_active": self.before_active,
                "branch_id": self.branch_id,
                "event_time": self.event_time,
                "evidence_id": self.evidence_id,
                "payload_hash": self.payload_hash,
                "previous_audit_hash": self.previous_audit_hash,
                "reason": self.reason,
                "schema_version": self.schema_version,
                "sequence": self.sequence,
            },
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_canonical_json(cls, payload: str) -> EvidenceAuditRow:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("EvidenceAuditRow must be valid JSON") from exc
        expected = {
            "action",
            "active_state_hash_after",
            "active_state_hash_before",
            "after_active",
            "audit_hash",
            "audit_id",
            "before_active",
            "branch_id",
            "event_time",
            "evidence_id",
            "payload_hash",
            "previous_audit_hash",
            "reason",
            "schema_version",
            "sequence",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("EvidenceAuditRow canonical payload has unexpected fields")
        row = cls(**value)
        if row.to_canonical_json() != payload:
            raise ValueError("EvidenceAuditRow payload is not strict canonical JSON")
        return row


@dataclass(frozen=True, slots=True)
class EntityBinding:
    """Traceable transition from diagnostic hint to perceptual slot and evidence scope."""

    binding_id: str
    entity_hint: str | None
    entity_slot: str | None
    entity_key: str | None
    assignment_status: str
    confidence: float
    time: float
    parent_spark_id: str
    schema_version: str = SENSORY_CONTRACT_VERSION

    def validate(self) -> None:
        if self.schema_version != SENSORY_CONTRACT_VERSION:
            raise ValueError(f"unsupported entity schema version: {self.schema_version}")
        if any(
            not isinstance(value, str) or not value.strip()
            for value in (self.binding_id, self.parent_spark_id)
        ):
            raise ValueError("binding_id and parent_spark_id must not be empty")
        for name, value in (
            ("entity_hint", self.entity_hint),
            ("entity_slot", self.entity_slot),
            ("entity_key", self.entity_key),
        ):
            if value is not None and (
                not isinstance(value, str) or not value.strip()
            ):
                raise ValueError(f"{name} must be a non-empty string when present")
        if self.assignment_status not in {"assigned", "unassigned", "uncertain"}:
            raise ValueError("invalid entity assignment status")
        if (
            isinstance(self.confidence, bool)
            or not isinstance(self.confidence, (int, float))
            or not math.isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("entity confidence must be finite and in [0, 1]")
        if (
            isinstance(self.time, bool)
            or not isinstance(self.time, (int, float))
            or not math.isfinite(self.time)
            or self.time < 0
        ):
            raise ValueError("entity binding time must be finite and non-negative")
        if self.assignment_status == "assigned" and not self.entity_key:
            raise ValueError("assigned entity binding requires entity_key")
        if self.assignment_status != "assigned" and self.entity_key is not None:
            raise ValueError("unassigned or uncertain binding cannot set entity_key")

    def to_canonical_json(self) -> str:
        self.validate()
        return json.dumps(
            {
                "assignment_status": self.assignment_status,
                "binding_id": self.binding_id,
                "confidence": self.confidence,
                "entity_hint": self.entity_hint,
                "entity_key": self.entity_key,
                "entity_slot": self.entity_slot,
                "parent_spark_id": self.parent_spark_id,
                "schema_version": self.schema_version,
                "time": self.time,
            },
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_canonical_json(cls, payload: str) -> EntityBinding:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("EntityBinding must be valid JSON") from exc
        expected = {
            "assignment_status",
            "binding_id",
            "confidence",
            "entity_hint",
            "entity_key",
            "entity_slot",
            "parent_spark_id",
            "schema_version",
            "time",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("EntityBinding canonical payload has unexpected fields")
        binding = cls(**value)
        if binding.to_canonical_json() != payload:
            raise ValueError("EntityBinding payload is not strict canonical JSON")
        return binding


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

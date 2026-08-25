from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


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

    def validate(self) -> None:
        if not self.sample_id or not self.source_id or not self.modality:
            raise ValueError("sample_id, source_id, and modality must not be empty")
        if not math.isfinite(self.time) or self.time < 0:
            raise ValueError("sample time must be finite and >= 0")
        if not self.values:
            raise ValueError("a sensory sample requires at least one channel")
        for feature, value in self.values.items():
            if not feature:
                raise ValueError("sensory feature names must not be empty")
            if not math.isfinite(float(value)):
                raise ValueError(f"sensory value for {feature!r} must be finite")


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

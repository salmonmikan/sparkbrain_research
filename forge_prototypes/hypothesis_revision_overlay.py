from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


@dataclass(frozen=True, slots=True)
class RevisionOverlayConfig:
    evidence_gain: float = 1.0
    min_confidence: float = 0.60
    min_margin: float = 0.20
    max_abs_support: float = 4.0

    def __post_init__(self) -> None:
        if self.evidence_gain <= 0.0:
            raise ValueError("evidence_gain must be positive")
        if not 0.0 <= self.min_confidence <= 1.0:
            raise ValueError("min_confidence must be in [0, 1]")
        if not 0.0 <= self.min_margin <= 1.0:
            raise ValueError("min_margin must be in [0, 1]")
        if self.max_abs_support <= 0.0:
            raise ValueError("max_abs_support must be positive")


@dataclass(frozen=True, slots=True)
class EvidenceUpdate:
    value: str
    strength: float

    def as_dict(self) -> dict[str, Any]:
        return {"strength": self.strength, "value": self.value}


@dataclass(frozen=True, slots=True)
class RevisedHypothesis:
    value: str
    base_probability: float
    cumulative_support: float
    revised_probability: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "base_probability": self.base_probability,
            "cumulative_support": self.cumulative_support,
            "revised_probability": self.revised_probability,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class RevisionSnapshot:
    assembly_id: str | None
    hypotheses: tuple[RevisedHypothesis, ...]
    selected_value: str | None
    confidence: float
    margin: float
    abstained: bool
    reason: str
    base_reason: str
    evidence_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "abstained": self.abstained,
            "assembly_id": self.assembly_id,
            "base_reason": self.base_reason,
            "confidence": self.confidence,
            "evidence_count": self.evidence_count,
            "hypotheses": [row.as_dict() for row in self.hypotheses],
            "margin": self.margin,
            "reason": self.reason,
            "selected_value": self.selected_value,
        }


class HypothesisRevisionOverlay:
    """Forge-only late-evidence overlay; never mutates the underlying predictor."""

    def __init__(self, config: RevisionOverlayConfig | None = None) -> None:
        self.config = config or RevisionOverlayConfig()
        self.events: list[EvidenceUpdate] = []

    def apply_evidence(
        self,
        base: PredictionPoolSnapshot,
        *,
        value: str,
        strength: float = 1.0,
    ) -> RevisionSnapshot:
        values = {row.value for row in base.hypotheses}
        if value not in values:
            raise ValueError("evidence value must already exist in the exposed hypothesis pool")
        resolved_strength = float(strength)
        if not math.isfinite(resolved_strength) or not -1.0 <= resolved_strength <= 1.0:
            raise ValueError("strength must be finite and in [-1, 1]")
        self.events.append(EvidenceUpdate(value=value, strength=resolved_strength))
        return self.evaluate(base)

    def evaluate(self, base: PredictionPoolSnapshot) -> RevisionSnapshot:
        if not base.hypotheses:
            return RevisionSnapshot(
                assembly_id=base.assembly_id,
                hypotheses=(),
                selected_value=None,
                confidence=0.0,
                margin=0.0,
                abstained=True,
                reason="no_exposed_hypotheses",
                base_reason=base.reason,
                evidence_count=len(self.events),
            )

        # Late evidence may resolve ambiguity, but it must not manufacture
        # confidence from a pool that was already rejected for insufficient data.
        if base.reason == "insufficient_observations":
            hypotheses = tuple(
                RevisedHypothesis(
                    value=row.value,
                    base_probability=row.probability,
                    cumulative_support=0.0,
                    revised_probability=row.probability,
                )
                for row in base.hypotheses
            )
            return RevisionSnapshot(
                assembly_id=base.assembly_id,
                hypotheses=hypotheses,
                selected_value=None,
                confidence=max(row.probability for row in base.hypotheses),
                margin=0.0,
                abstained=True,
                reason="base_insufficient_observations",
                base_reason=base.reason,
                evidence_count=len(self.events),
            )

        support_by_value = {row.value: 0.0 for row in base.hypotheses}
        for event in self.events:
            if event.value not in support_by_value:
                continue
            support_by_value[event.value] += event.strength

        logits: list[tuple[str, float, float, float]] = []
        for row in base.hypotheses:
            support = max(
                -self.config.max_abs_support,
                min(self.config.max_abs_support, support_by_value[row.value]),
            )
            logit = math.log(max(row.probability, 1e-12)) + self.config.evidence_gain * support
            logits.append((row.value, row.probability, support, logit))

        max_logit = max(row[3] for row in logits)
        weights = [math.exp(row[3] - max_logit) for row in logits]
        normalizer = sum(weights)
        revised = [
            RevisedHypothesis(
                value=row[0],
                base_probability=row[1],
                cumulative_support=row[2],
                revised_probability=weight / normalizer,
            )
            for row, weight in zip(logits, weights, strict=True)
        ]
        revised.sort(key=lambda row: (-row.revised_probability, row.value))

        confidence = revised[0].revised_probability
        second = revised[1].revised_probability if len(revised) > 1 else 0.0
        margin = confidence - second
        ambiguous = confidence < self.config.min_confidence or (
            len(revised) > 1 and margin < self.config.min_margin
        )

        return RevisionSnapshot(
            assembly_id=base.assembly_id,
            hypotheses=tuple(revised),
            selected_value=None if ambiguous else revised[0].value,
            confidence=confidence,
            margin=margin,
            abstained=ambiguous,
            reason="ambiguous_after_revision" if ambiguous else "selected_after_revision",
            base_reason=base.reason,
            evidence_count=len(self.events),
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "events": [event.as_dict() for event in self.events],
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> HypothesisRevisionOverlay:
        overlay = cls(RevisionOverlayConfig(**state["config"]))
        overlay.events = [EvidenceUpdate(**row) for row in state.get("events", [])]
        return overlay

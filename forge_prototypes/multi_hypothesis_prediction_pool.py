from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sparkbrain.v05.contracts import AssemblyActivation
from sparkbrain.v05.prediction import AssemblyPredictor


@dataclass(frozen=True, slots=True)
class PredictionPoolConfig:
    max_hypotheses: int = 3
    min_observations: int = 3
    min_confidence: float = 0.60
    min_margin: float = 0.20

    def __post_init__(self) -> None:
        if self.max_hypotheses < 1:
            raise ValueError("max_hypotheses must be positive")
        if self.min_observations < 1:
            raise ValueError("min_observations must be positive")
        if not 0.0 <= self.min_confidence <= 1.0:
            raise ValueError("min_confidence must be in [0, 1]")
        if not 0.0 <= self.min_margin <= 1.0:
            raise ValueError("min_margin must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class WeightedHypothesis:
    value: str
    count: int
    probability: float

    def as_dict(self) -> dict[str, Any]:
        return {"count": self.count, "probability": self.probability, "value": self.value}


@dataclass(frozen=True, slots=True)
class PredictionPoolSnapshot:
    assembly_id: str | None
    hypotheses: tuple[WeightedHypothesis, ...]
    selected_value: str | None
    confidence: float
    margin: float
    abstained: bool
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "abstained": self.abstained,
            "assembly_id": self.assembly_id,
            "confidence": self.confidence,
            "hypotheses": [row.as_dict() for row in self.hypotheses],
            "margin": self.margin,
            "reason": self.reason,
            "selected_value": self.selected_value,
        }


class MultiHypothesisPredictionPool:
    """Forge-only read-only view over the stable v0.5 predictor histogram."""

    def __init__(
        self,
        predictor: AssemblyPredictor,
        config: PredictionPoolConfig | None = None,
    ) -> None:
        self.predictor = predictor
        self.config = config or PredictionPoolConfig()

    def inspect(self, activation: AssemblyActivation | None) -> PredictionPoolSnapshot:
        if activation is None or activation.suppressed or not activation.mature:
            return self._abstain(
                None if activation is None else activation.assembly_id,
                reason="inactive_or_immature",
            )

        table = self.predictor.counts.get(activation.assembly_id, {})
        total = sum(table.values())
        if total <= 0:
            return self._abstain(activation.assembly_id, reason="no_observations")

        ranked = sorted(table.items(), key=lambda row: (-row[1], row[0]))
        hypotheses = tuple(
            WeightedHypothesis(value=value, count=count, probability=count / total)
            for value, count in ranked[: self.config.max_hypotheses]
        )
        confidence = hypotheses[0].probability
        second = hypotheses[1].probability if len(hypotheses) > 1 else 0.0
        margin = confidence - second

        if total < self.config.min_observations:
            return self._abstain(
                activation.assembly_id,
                reason="insufficient_observations",
                hypotheses=hypotheses,
                confidence=confidence,
                margin=margin,
            )
        if confidence < self.config.min_confidence:
            return self._abstain(
                activation.assembly_id,
                reason="low_confidence",
                hypotheses=hypotheses,
                confidence=confidence,
                margin=margin,
            )
        if len(hypotheses) > 1 and margin < self.config.min_margin:
            return self._abstain(
                activation.assembly_id,
                reason="ambiguous_hypotheses",
                hypotheses=hypotheses,
                confidence=confidence,
                margin=margin,
            )
        return PredictionPoolSnapshot(
            assembly_id=activation.assembly_id,
            hypotheses=hypotheses,
            selected_value=hypotheses[0].value,
            confidence=confidence,
            margin=margin,
            abstained=False,
            reason="selected",
        )

    @staticmethod
    def _abstain(
        assembly_id: str | None,
        *,
        reason: str,
        hypotheses: tuple[WeightedHypothesis, ...] = (),
        confidence: float = 0.0,
        margin: float = 0.0,
    ) -> PredictionPoolSnapshot:
        return PredictionPoolSnapshot(
            assembly_id=assembly_id,
            hypotheses=hypotheses,
            selected_value=None,
            confidence=confidence,
            margin=margin,
            abstained=True,
            reason=reason,
        )

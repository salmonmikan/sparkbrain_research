from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class EventOrigin(StrEnum):
    EXTERNAL = "external"
    GENERATED = "generated"


@dataclass(frozen=True, slots=True)
class ComparatorEvent:
    """Anonymous event visible at the CX01 evaluator boundary.

    `episode_start` is structural segmentation metadata only. It must never
    encode a hidden context, target, semantic class, correct branch, or reward.
    """

    token: str
    timestamp_ms: float
    origin: EventOrigin
    episode_start: bool = False

    def validate(self) -> None:
        if not self.token:
            raise ValueError("event token must be non-empty")
        if not math.isfinite(self.timestamp_ms) or self.timestamp_ms < 0:
            raise ValueError("event timestamp must be finite and non-negative")
        if self.origin is EventOrigin.GENERATED and self.episode_start:
            raise ValueError("generated events cannot open externally declared episodes")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value = asdict(self)
        value["origin"] = self.origin.value
        return value


@dataclass(frozen=True, slots=True)
class CandidateProbability:
    token: str
    probability: float

    def validate(self) -> None:
        if not self.token:
            raise ValueError("candidate token must be non-empty")
        if not math.isfinite(self.probability):
            raise ValueError("candidate probability must be finite")
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("candidate probability must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class PredictionDistribution:
    rows: tuple[CandidateProbability, ...]

    def validate(self) -> None:
        if not self.rows:
            return
        for row in self.rows:
            row.validate()
        if len({row.token for row in self.rows}) != len(self.rows):
            raise ValueError("prediction distribution tokens must be unique")
        total = sum(row.probability for row in self.rows)
        if not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("prediction distribution must sum to one")

    @classmethod
    def from_scores(cls, scores: dict[str, float]) -> PredictionDistribution:
        positive = {
            str(token): max(0.0, float(score))
            for token, score in scores.items()
            if math.isfinite(float(score)) and float(score) > 0.0
        }
        total = sum(positive.values())
        if total <= 0.0:
            return cls(())
        rows = tuple(
            CandidateProbability(token, score / total)
            for token, score in sorted(positive.items())
        )
        distribution = cls(rows)
        distribution.validate()
        return distribution

    def as_dict(self) -> dict[str, float]:
        self.validate()
        return {row.token: row.probability for row in self.rows}

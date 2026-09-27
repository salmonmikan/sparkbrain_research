from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import exp, isfinite, sqrt

from forge_prototypes.internal_scope_allocator import InternalScopeAllocator

NEW_SCOPE = "__new_scope__"


@dataclass(frozen=True)
class ScopePosteriorConfig:
    temperature: float = 0.35
    new_scope_error_scale: float = 0.5
    top_k: int = 3
    min_margin: float = 0.15
    min_selected_mass: float = 0.55

    def __post_init__(self) -> None:
        if not isfinite(self.temperature) or self.temperature <= 0.0:
            raise ValueError("temperature must be finite and positive")
        if not isfinite(self.new_scope_error_scale) or self.new_scope_error_scale <= 0.0:
            raise ValueError("new_scope_error_scale must be finite and positive")
        if self.top_k < 2:
            raise ValueError("top_k must retain at least two alternatives")
        if not isfinite(self.min_margin) or not 0.0 <= self.min_margin <= 1.0:
            raise ValueError("min_margin must be in [0, 1]")
        if not isfinite(self.min_selected_mass) or not 0.0 <= self.min_selected_mass <= 1.0:
            raise ValueError("min_selected_mass must be in [0, 1]")


@dataclass(frozen=True)
class ScopeHypothesis:
    scope_token: str
    mass: float
    distance: float | None


@dataclass(frozen=True)
class ScopePosterior:
    hypotheses: tuple[ScopeHypothesis, ...]
    selected_scope: str | None
    abstained: bool
    reason: str


class PluralScopePosteriorRouter:
    """Rank existing internally allocated scopes plus a NEW_SCOPE alternative.

    This is an ordinary normalized radial-score + reject-option prototype.  It
    does not claim calibrated Bayesian posterior semantics or latent-cause
    discovery.
    """

    def __init__(self, config: ScopePosteriorConfig | None = None) -> None:
        self.config = config or ScopePosteriorConfig()

    @staticmethod
    def _vector(observation: Sequence[float]) -> list[float]:
        if isinstance(observation, (str, bytes)):
            raise ValueError("observation must be a non-empty numeric vector")
        vector = [float(value) for value in observation]
        if not vector or not all(isfinite(value) for value in vector):
            raise ValueError("observation must be a non-empty finite numeric vector")
        return vector

    @staticmethod
    def _distance(left: Sequence[float], right: Sequence[float]) -> float:
        return sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))

    def route(
        self,
        allocator: InternalScopeAllocator,
        observation: Sequence[float],
        *,
        prediction_error: float,
    ) -> ScopePosterior:
        vector = self._vector(observation)
        error = float(prediction_error)
        if not isfinite(error) or error < 0.0:
            raise ValueError("prediction_error must be finite and non-negative")

        state = allocator.state_dict()
        dimension = state["dimension"]
        if dimension is not None and len(vector) != int(dimension):
            raise ValueError("observation dimension changed")

        raw: list[tuple[str, float, float | None]] = []
        for row in state["scopes"]:
            distance = self._distance(vector, row["centroid"])
            score = exp(-distance / self.config.temperature)
            raw.append((str(row["scope_token"]), score, distance))

        new_score = exp(min(error / self.config.new_scope_error_scale, 20.0)) - 1.0
        raw.append((NEW_SCOPE, max(new_score, 1e-12), None))
        total = sum(score for _, score, _ in raw)
        ranked = sorted(
            (
                ScopeHypothesis(token, score / total, distance)
                for token, score, distance in raw
            ),
            key=lambda row: (-row.mass, row.scope_token),
        )[: self.config.top_k]

        first = ranked[0]
        second_mass = ranked[1].mass if len(ranked) > 1 else 0.0
        margin = first.mass - second_mass
        if first.mass < self.config.min_selected_mass:
            return ScopePosterior(tuple(ranked), None, True, "insufficient_mass")
        if margin < self.config.min_margin:
            return ScopePosterior(tuple(ranked), None, True, "ambiguous_margin")
        return ScopePosterior(tuple(ranked), first.scope_token, False, "separated")


__all__ = [
    "NEW_SCOPE",
    "PluralScopePosteriorRouter",
    "ScopeHypothesis",
    "ScopePosterior",
    "ScopePosteriorConfig",
]

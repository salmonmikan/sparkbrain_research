from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import isfinite, sqrt
from typing import Any

from forge_prototypes.hypothesis_revision_overlay import RevisionOverlayConfig, RevisionSnapshot
from forge_prototypes.managed_scope_hypothesis_revision import (
    ManagedScopeHypothesisRevisionOverlay,
)
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


class ScopeBudgetExceeded(RuntimeError):
    """Raised instead of silently evicting a learned scope."""


@dataclass(frozen=True)
class InternalScopeAllocatorConfig:
    reuse_radius: float = 0.35
    create_error_threshold: float = 0.5
    centroid_learning_rate: float = 0.1
    max_scopes: int = 8

    def __post_init__(self) -> None:
        if not isfinite(self.reuse_radius) or self.reuse_radius < 0.0:
            raise ValueError("reuse_radius must be finite and non-negative")
        if not isfinite(self.create_error_threshold) or self.create_error_threshold < 0.0:
            raise ValueError("create_error_threshold must be finite and non-negative")
        if not isfinite(self.centroid_learning_rate) or not (
            0.0 <= self.centroid_learning_rate <= 1.0
        ):
            raise ValueError("centroid_learning_rate must be finite and in [0, 1]")
        if self.max_scopes < 1:
            raise ValueError("max_scopes must be positive")


@dataclass(frozen=True)
class ScopeAllocation:
    scope_token: str | None
    action: str
    nearest_distance: float | None
    reason: str

    @property
    def allocated(self) -> bool:
        return self.scope_token is not None


@dataclass
class _ScopePrototype:
    scope_token: str
    centroid: list[float]
    observations: int = 1


class InternalScopeAllocator:
    """Issue opaque scope IDs from observations and predictive mismatch only.

    This is a deterministic nearest-centroid/change-threshold prototype.  It is
    ordinary cache/session allocation engineering, not a learned scientific
    mechanism.  The API deliberately accepts no caller-provided scope, episode,
    regime, entity, target, truth, or evaluator identifier.
    """

    def __init__(self, config: InternalScopeAllocatorConfig | None = None) -> None:
        self.config = config or InternalScopeAllocatorConfig()
        self._dimension: int | None = None
        self._next_scope_index = 1
        self._scopes: list[_ScopePrototype] = []

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

    def _create_scope(self, vector: list[float]) -> ScopeAllocation:
        if len(self._scopes) >= self.config.max_scopes:
            raise ScopeBudgetExceeded(
                "scope budget exhausted; allocator will not silently evict prior scopes"
            )
        token = f"scope-{self._next_scope_index:08d}"
        self._next_scope_index += 1
        self._scopes.append(_ScopePrototype(token, list(vector)))
        reason = "bootstrap" if len(self._scopes) == 1 else "mismatch"
        return ScopeAllocation(token, "created", None, reason)

    def observe(
        self,
        observation: Sequence[float],
        *,
        prediction_error: float,
    ) -> ScopeAllocation:
        vector = self._vector(observation)
        error = float(prediction_error)
        if not isfinite(error) or error < 0.0:
            raise ValueError("prediction_error must be finite and non-negative")
        if self._dimension is None:
            self._dimension = len(vector)
        elif len(vector) != self._dimension:
            raise ValueError("observation dimension changed")

        if not self._scopes:
            return self._create_scope(vector)

        nearest = min(self._scopes, key=lambda row: self._distance(vector, row.centroid))
        distance = self._distance(vector, nearest.centroid)
        if distance <= self.config.reuse_radius:
            rate = self.config.centroid_learning_rate
            nearest.centroid = [
                current + rate * (observed - current)
                for current, observed in zip(nearest.centroid, vector, strict=True)
            ]
            nearest.observations += 1
            return ScopeAllocation(nearest.scope_token, "reused", distance, "within_reuse_radius")

        if error < self.config.create_error_threshold:
            return ScopeAllocation(None, "abstained", distance, "insufficient_change_evidence")

        created = self._create_scope(vector)
        return ScopeAllocation(created.scope_token, created.action, distance, created.reason)

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "dimension": self._dimension,
            "next_scope_index": self._next_scope_index,
            "scopes": [
                {
                    "scope_token": row.scope_token,
                    "centroid": list(row.centroid),
                    "observations": row.observations,
                }
                for row in self._scopes
            ],
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> InternalScopeAllocator:
        result = cls(InternalScopeAllocatorConfig(**state["config"]))
        dimension = state.get("dimension")
        result._dimension = None if dimension is None else int(dimension)
        result._next_scope_index = int(state["next_scope_index"])
        for row in state.get("scopes", []):
            token = str(row["scope_token"])
            centroid = cls._vector(row["centroid"])
            observations = int(row["observations"])
            if not token or observations < 1:
                raise ValueError("invalid persisted scope")
            if result._dimension != len(centroid):
                raise ValueError("persisted scope dimension mismatch")
            result._scopes.append(_ScopePrototype(token, centroid, observations))
        if len(result._scopes) > result.config.max_scopes:
            raise ValueError("persisted scopes exceed configured budget")
        expected_tokens = {f"scope-{index:08d}" for index in range(1, result._next_scope_index)}
        actual_tokens = {row.scope_token for row in result._scopes}
        if len(actual_tokens) != len(result._scopes) or not actual_tokens <= expected_tokens:
            raise ValueError("invalid persisted scope token sequence")
        return result


@dataclass(frozen=True)
class ScopedRevisionSnapshot:
    allocation: ScopeAllocation
    revision: RevisionSnapshot | None


class InternallyScopedHypothesisRevision:
    """Bridge internally allocated scopes into the existing revision overlay."""

    def __init__(
        self,
        allocator_config: InternalScopeAllocatorConfig | None = None,
        revision_config: RevisionOverlayConfig | None = None,
    ) -> None:
        self.allocator_config = allocator_config or InternalScopeAllocatorConfig()
        self._allocators: dict[str, InternalScopeAllocator] = {}
        self._revision = ManagedScopeHypothesisRevisionOverlay(revision_config)

    @staticmethod
    def _assembly_id(base: PredictionPoolSnapshot) -> str:
        if base.assembly_id is None:
            raise ValueError("internal scope allocation requires a concrete Assembly")
        return base.assembly_id

    def _allocate(
        self,
        base: PredictionPoolSnapshot,
        observation: Sequence[float],
        prediction_error: float,
    ) -> ScopeAllocation:
        assembly_id = self._assembly_id(base)
        allocator = self._allocators.setdefault(
            assembly_id, InternalScopeAllocator(self.allocator_config)
        )
        return allocator.observe(observation, prediction_error=prediction_error)

    def evaluate(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        prediction_error: float,
    ) -> ScopedRevisionSnapshot:
        allocation = self._allocate(base, observation, prediction_error)
        if allocation.scope_token is None:
            return ScopedRevisionSnapshot(allocation, None)
        revision = self._revision.evaluate(base, scope_token=allocation.scope_token)
        return ScopedRevisionSnapshot(allocation, revision)

    def apply_evidence(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        prediction_error: float,
        value: str,
        strength: float = 1.0,
    ) -> ScopedRevisionSnapshot:
        allocation = self._allocate(base, observation, prediction_error)
        if allocation.scope_token is None:
            return ScopedRevisionSnapshot(allocation, None)
        revision = self._revision.apply_evidence(
            base,
            scope_token=allocation.scope_token,
            value=value,
            strength=strength,
        )
        return ScopedRevisionSnapshot(allocation, revision)

    def state_dict(self) -> dict[str, Any]:
        return {
            "allocator_config": asdict(self.allocator_config),
            "allocators": {
                assembly_id: allocator.state_dict()
                for assembly_id, allocator in sorted(self._allocators.items())
            },
            "revision": self._revision.state_dict(),
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> InternallyScopedHypothesisRevision:
        revision_state = state["revision"]
        result = cls(
            InternalScopeAllocatorConfig(**state["allocator_config"]),
            RevisionOverlayConfig(**revision_state["overlay"]["config"]),
        )
        result._allocators = {
            str(assembly_id): InternalScopeAllocator.from_state_dict(allocator_state)
            for assembly_id, allocator_state in state.get("allocators", {}).items()
        }
        result._revision = ManagedScopeHypothesisRevisionOverlay.from_state_dict(revision_state)
        return result

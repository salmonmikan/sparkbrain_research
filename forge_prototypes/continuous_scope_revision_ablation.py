from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any

from forge_prototypes.coverage_aware_outcome_guard import CoverageAwareOutcomeGuard
from forge_prototypes.hypothesis_revision_overlay import (
    HypothesisRevisionOverlay,
    RevisionOverlayConfig,
    RevisionSnapshot,
)
from forge_prototypes.internal_scope_allocator import InternalScopeAllocatorConfig
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot
from forge_prototypes.plural_scope_posterior import ScopePosteriorConfig
from forge_prototypes.plural_scope_revision_bridge import PluralScopeRevisionBridge
from forge_prototypes.transactional_outcome_revision_coordinator import (
    TransactionalOutcomeRevisionCoordinator,
    TransactionalOutcomeRevisionSnapshot,
)


@dataclass(frozen=True, slots=True)
class AblationEvent:
    label: str
    observation: tuple[float, ...]
    observed_value: str
    strength: float = 1.0


@dataclass(frozen=True, slots=True)
class AblationStep:
    label: str
    observed_value: str
    full_action: str
    cut_action: str
    full_scope_token: str | None
    cut_scope_token: str | None
    full_selected_value: str | None
    cut_selected_value: str | None
    full_committed: bool
    cut_committed: bool


@dataclass(frozen=True, slots=True)
class AblationQuery:
    label: str
    full_action: str
    cut_action: str
    full_scope_token: str | None
    cut_scope_token: str | None
    full_selected_value: str | None
    cut_selected_value: str | None
    full_abstained: bool
    cut_abstained: bool


@dataclass(frozen=True, slots=True)
class ContinuousRevisionAblationReport:
    steps: tuple[AblationStep, ...]
    queries: tuple[AblationQuery, ...]
    full_commits: int
    cut_commits: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "steps": [asdict(row) for row in self.steps],
            "queries": [asdict(row) for row in self.queries],
            "full_commits": self.full_commits,
            "cut_commits": self.cut_commits,
        }


class ContinuousScopeRevisionAblation:
    """Compare the connected scope->revision loop with only that connection cut.

    Both arms execute the same internal scope router, allocator, coverage guard,
    and transaction boundary.  The connected arm sends evidence strength into
    the selected scope.  The cut arm commits the same routing step with zero
    scope-local strength, then sends the original evidence to one assembly-wide
    overlay.  This preserves component execution while removing scope-specific
    revision state.

    The harness is a noncanonical development diagnostic.  It cannot establish
    comparative superiority, composition contribution outside this fixture, or
    scientific novelty.
    """

    def __init__(
        self,
        allocator_config: InternalScopeAllocatorConfig | None = None,
        router_config: ScopePosteriorConfig | None = None,
        revision_config: RevisionOverlayConfig | None = None,
    ) -> None:
        self.allocator_config = allocator_config or InternalScopeAllocatorConfig()
        self.router_config = router_config or ScopePosteriorConfig()
        self.revision_config = revision_config or RevisionOverlayConfig()
        self._full = self._new_coordinator()
        self._cut = self._new_coordinator()
        self._cut_global: dict[str, HypothesisRevisionOverlay] = {}

    def _new_coordinator(self) -> TransactionalOutcomeRevisionCoordinator:
        bridge = PluralScopeRevisionBridge(
            self.allocator_config,
            self.router_config,
            self.revision_config,
        )
        return TransactionalOutcomeRevisionCoordinator(CoverageAwareOutcomeGuard(bridge))

    @staticmethod
    def _assembly_id(base: PredictionPoolSnapshot) -> str:
        if base.assembly_id is None:
            raise ValueError("continuous ablation requires a concrete Assembly")
        return base.assembly_id

    @staticmethod
    def _scope_token(snapshot: TransactionalOutcomeRevisionSnapshot) -> str | None:
        applied = snapshot.outcome.applied
        if applied is None:
            return None
        allocation = applied.bridge.allocation
        if allocation is not None and allocation.scope_token is not None:
            return allocation.scope_token
        selected = applied.bridge.routing.selected_scope
        return None if selected == "__new_scope__" else selected

    @staticmethod
    def _revision(snapshot: TransactionalOutcomeRevisionSnapshot) -> RevisionSnapshot | None:
        applied = snapshot.outcome.applied
        return None if applied is None else applied.bridge.revision

    def _cut_revision(
        self,
        base: PredictionPoolSnapshot,
        *,
        event: AblationEvent,
        route_committed: bool,
    ) -> RevisionSnapshot:
        assembly_id = self._assembly_id(base)
        overlay = self._cut_global.get(assembly_id)
        if route_committed:
            overlay = self._cut_global.setdefault(
                assembly_id, HypothesisRevisionOverlay(self.revision_config)
            )
            return overlay.apply_evidence(
                base,
                value=event.observed_value,
                strength=event.strength,
            )
        return (overlay or HypothesisRevisionOverlay(self.revision_config)).evaluate(base)

    def apply_event(
        self,
        base: PredictionPoolSnapshot,
        event: AblationEvent,
    ) -> AblationStep:
        full = self._full.apply_step(
            base,
            observation=event.observation,
            observed_value=event.observed_value,
            strength=event.strength,
        )
        cut = self._cut.apply_step(
            base,
            observation=event.observation,
            observed_value=event.observed_value,
            strength=0.0,
        )
        cut_revision = self._cut_revision(base, event=event, route_committed=cut.committed)
        full_revision = self._revision(full)
        return AblationStep(
            label=event.label,
            observed_value=event.observed_value,
            full_action=full.action,
            cut_action=cut.action,
            full_scope_token=self._scope_token(full),
            cut_scope_token=self._scope_token(cut),
            full_selected_value=(
                None if full_revision is None else full_revision.selected_value
            ),
            cut_selected_value=cut_revision.selected_value,
            full_committed=full.committed,
            cut_committed=cut.committed,
        )

    @staticmethod
    def _validated_error(base: PredictionPoolSnapshot, observed_value: str) -> float:
        probabilities = {row.value: float(row.probability) for row in base.hypotheses}
        if observed_value not in probabilities:
            raise ValueError("query value must exist in the exposed hypothesis pool")
        probability = probabilities[observed_value]
        if not isfinite(probability) or not 0.0 <= probability <= 1.0:
            raise ValueError("hypothesis probability must be finite and in [0, 1]")
        return 1.0 - probability

    @staticmethod
    def _query_bridge(
        coordinator: TransactionalOutcomeRevisionCoordinator,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        prediction_error: float,
    ):
        state = coordinator.state_dict()["guard"]["bridge"]
        probe = PluralScopeRevisionBridge.from_state_dict(state)
        return probe.evaluate(
            base,
            observation=observation,
            prediction_error=prediction_error,
        )

    def query(
        self,
        base: PredictionPoolSnapshot,
        *,
        label: str,
        observation: Sequence[float],
        reference_value: str,
    ) -> AblationQuery:
        error = self._validated_error(base, reference_value)
        full = self._query_bridge(
            self._full, base, observation=observation, prediction_error=error
        )
        cut = self._query_bridge(
            self._cut, base, observation=observation, prediction_error=error
        )
        global_overlay = self._cut_global.get(self._assembly_id(base))
        cut_revision = (
            global_overlay or HypothesisRevisionOverlay(self.revision_config)
        ).evaluate(base)
        return AblationQuery(
            label=label,
            full_action=full.action,
            cut_action=cut.action,
            full_scope_token=full.routing.selected_scope,
            cut_scope_token=cut.routing.selected_scope,
            full_selected_value=(
                None if full.revision is None else full.revision.selected_value
            ),
            cut_selected_value=cut_revision.selected_value,
            full_abstained=(
                True if full.revision is None else full.revision.abstained
            ),
            cut_abstained=cut_revision.abstained,
        )

    def run(
        self,
        base: PredictionPoolSnapshot,
        events: Sequence[AblationEvent],
        queries: Sequence[tuple[str, Sequence[float], str]],
    ) -> ContinuousRevisionAblationReport:
        steps = tuple(self.apply_event(base, event) for event in events)
        query_rows = tuple(
            self.query(
                base,
                label=label,
                observation=observation,
                reference_value=reference_value,
            )
            for label, observation, reference_value in queries
        )
        return ContinuousRevisionAblationReport(
            steps=steps,
            queries=query_rows,
            full_commits=sum(row.full_committed for row in steps),
            cut_commits=sum(row.cut_committed for row in steps),
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "allocator_config": asdict(self.allocator_config),
            "router_config": asdict(self.router_config),
            "revision_config": asdict(self.revision_config),
            "full": self._full.state_dict(),
            "cut": self._cut.state_dict(),
            "cut_global": {
                assembly_id: overlay.state_dict()
                for assembly_id, overlay in sorted(self._cut_global.items())
            },
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> ContinuousScopeRevisionAblation:
        result = cls(
            InternalScopeAllocatorConfig(**state["allocator_config"]),
            ScopePosteriorConfig(**state["router_config"]),
            RevisionOverlayConfig(**state["revision_config"]),
        )
        result._full = TransactionalOutcomeRevisionCoordinator.from_state_dict(
            state["full"]
        )
        result._cut = TransactionalOutcomeRevisionCoordinator.from_state_dict(
            state["cut"]
        )
        result._cut_global = {
            str(assembly_id): HypothesisRevisionOverlay.from_state_dict(overlay_state)
            for assembly_id, overlay_state in state.get("cut_global", {}).items()
        }
        return result


__all__ = [
    "AblationEvent",
    "AblationQuery",
    "AblationStep",
    "ContinuousRevisionAblationReport",
    "ContinuousScopeRevisionAblation",
]


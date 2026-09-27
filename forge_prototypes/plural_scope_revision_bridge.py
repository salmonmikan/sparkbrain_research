from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any

from forge_prototypes.hypothesis_revision_overlay import RevisionOverlayConfig, RevisionSnapshot
from forge_prototypes.internal_scope_allocator import (
    InternalScopeAllocator,
    InternalScopeAllocatorConfig,
    ScopeAllocation,
)
from forge_prototypes.managed_scope_hypothesis_revision import (
    ManagedScopeHypothesisRevisionOverlay,
)
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot
from forge_prototypes.plural_scope_posterior import (
    NEW_SCOPE,
    PluralScopePosteriorRouter,
    ScopePosterior,
    ScopePosteriorConfig,
)


@dataclass(frozen=True)
class PluralScopeRevisionSnapshot:
    routing: ScopePosterior
    allocation: ScopeAllocation | None
    revision: RevisionSnapshot | None
    action: str


class PluralScopeRevisionBridge:
    """Route plural internal scopes before committing late evidence.

    Ambiguous routing is read-only.  A separated route is committed through the
    allocator, and any disagreement between the read-only route and allocator
    mutation is rolled back before revision support can change.  This remains
    ordinary transactional cache/mixture engineering, not a scientific
    mechanism.
    """

    def __init__(
        self,
        allocator_config: InternalScopeAllocatorConfig | None = None,
        router_config: ScopePosteriorConfig | None = None,
        revision_config: RevisionOverlayConfig | None = None,
    ) -> None:
        self.allocator_config = allocator_config or InternalScopeAllocatorConfig()
        self.router_config = router_config or ScopePosteriorConfig()
        self._allocators: dict[str, InternalScopeAllocator] = {}
        self._router = PluralScopePosteriorRouter(self.router_config)
        self._revision = ManagedScopeHypothesisRevisionOverlay(revision_config)

    @staticmethod
    def _assembly_id(base: PredictionPoolSnapshot) -> str:
        if base.assembly_id is None:
            raise ValueError("plural scope revision requires a concrete Assembly")
        return base.assembly_id

    def _allocator(self, base: PredictionPoolSnapshot) -> InternalScopeAllocator:
        assembly_id = self._assembly_id(base)
        return self._allocators.setdefault(
            assembly_id, InternalScopeAllocator(self.allocator_config)
        )

    def evaluate(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        prediction_error: float,
    ) -> PluralScopeRevisionSnapshot:
        allocator = self._allocator(base)
        routing = self._router.route(
            allocator, observation, prediction_error=prediction_error
        )
        if routing.abstained or routing.selected_scope is None:
            return PluralScopeRevisionSnapshot(routing, None, None, "routing_abstained")
        if routing.selected_scope == NEW_SCOPE:
            return PluralScopeRevisionSnapshot(
                routing, None, None, "new_scope_uncommitted"
            )
        revision = self._revision.evaluate(
            base, scope_token=routing.selected_scope
        )
        return PluralScopeRevisionSnapshot(
            routing, None, revision, "evaluated_existing"
        )

    def apply_evidence(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        prediction_error: float,
        value: str,
        strength: float = 1.0,
    ) -> PluralScopeRevisionSnapshot:
        assembly_id = self._assembly_id(base)
        allocator = self._allocator(base)
        routing = self._router.route(
            allocator, observation, prediction_error=prediction_error
        )
        if routing.abstained or routing.selected_scope is None:
            return PluralScopeRevisionSnapshot(routing, None, None, "routing_abstained")

        allocator_before = allocator.state_dict()
        allocation = allocator.observe(
            observation, prediction_error=prediction_error
        )
        selected = routing.selected_scope
        if selected == NEW_SCOPE:
            compatible = allocation.action in {"created", "pending"}
        else:
            compatible = (
                allocation.action == "reused"
                and allocation.scope_token == selected
            )

        if not compatible:
            self._allocators[assembly_id] = InternalScopeAllocator.from_state_dict(
                allocator_before
            )
            return PluralScopeRevisionSnapshot(
                routing, allocation, None, "routing_commit_conflict"
            )

        if allocation.scope_token is None:
            return PluralScopeRevisionSnapshot(
                routing, allocation, None, allocation.action
            )

        revision = self._revision.apply_evidence(
            base,
            scope_token=allocation.scope_token,
            value=value,
            strength=strength,
        )
        action = (
            "applied_created"
            if allocation.action == "created"
            else "applied_existing"
        )
        return PluralScopeRevisionSnapshot(routing, allocation, revision, action)

    def state_dict(self) -> dict[str, Any]:
        return {
            "allocator_config": asdict(self.allocator_config),
            "router_config": asdict(self.router_config),
            "allocators": {
                assembly_id: allocator.state_dict()
                for assembly_id, allocator in sorted(self._allocators.items())
            },
            "revision": self._revision.state_dict(),
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> PluralScopeRevisionBridge:
        revision_state = state["revision"]
        result = cls(
            InternalScopeAllocatorConfig(**state["allocator_config"]),
            ScopePosteriorConfig(**state["router_config"]),
            RevisionOverlayConfig(**revision_state["overlay"]["config"]),
        )
        result._allocators = {
            str(assembly_id): InternalScopeAllocator.from_state_dict(allocator_state)
            for assembly_id, allocator_state in state.get("allocators", {}).items()
        }
        result._revision = ManagedScopeHypothesisRevisionOverlay.from_state_dict(
            revision_state
        )
        return result


__all__ = [
    "PluralScopeRevisionBridge",
    "PluralScopeRevisionSnapshot",
]

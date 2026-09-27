from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from forge_prototypes.coverage_aware_outcome_guard import (
    CoverageAwareOutcomeGuard,
    CoverageAwareOutcomeSnapshot,
)
from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot


@dataclass(frozen=True, slots=True)
class TransactionalOutcomeRevisionSnapshot:
    outcome: CoverageAwareOutcomeSnapshot
    committed: bool
    state_changed: bool
    action: str


class TransactionalOutcomeRevisionCoordinator:
    """Commit a complete observed-outcome step or preserve the prior checkpoint.

    The underlying Forge bridge validates revision evidence after routing and
    allocation.  A late validation failure can therefore leave allocator state
    behind even though no revision was accepted.  This coordinator evaluates a
    step on an isolated checkpoint and publishes the candidate state only for
    actions whose contract intentionally changes state.

    This is ordinary transaction/checkpoint engineering.  It is not a learning
    mechanism, a scientific result, or evidence of composition contribution.
    """

    _COMMIT_BRIDGE_ACTIONS = frozenset(
        {
            "applied_created",
            "applied_existing",
            # Pending confirmation is intentional allocator state, but no
            # revision support is written until a scope is confirmed.
            "pending",
        }
    )

    def __init__(self, guard: CoverageAwareOutcomeGuard | None = None) -> None:
        self._guard = guard or CoverageAwareOutcomeGuard()

    def apply_step(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        observed_value: str,
        strength: float = 1.0,
    ) -> TransactionalOutcomeRevisionSnapshot:
        before = self._guard.state_dict()
        candidate = CoverageAwareOutcomeGuard.from_state_dict(before)

        # Any exception is confined to the candidate.  The live guard is not
        # replaced until the complete step has returned a commit-bearing action.
        outcome = candidate.apply_observed_outcome(
            base,
            observation=observation,
            observed_value=observed_value,
            strength=strength,
        )

        bridge_action = (
            outcome.applied.bridge.action if outcome.applied is not None else None
        )
        committed = bool(
            outcome.outcome_exposed
            and bridge_action in self._COMMIT_BRIDGE_ACTIONS
        )
        if committed:
            candidate_state = candidate.state_dict()
            # Restore through the public checkpoint contract so the live state
            # cannot retain object aliases from the speculative candidate.
            self._guard = CoverageAwareOutcomeGuard.from_state_dict(candidate_state)
            state_changed = candidate_state != before
            action = f"committed_{outcome.action}"
        else:
            state_changed = False
            action = f"preserved_{outcome.action}"

        return TransactionalOutcomeRevisionSnapshot(
            outcome=outcome,
            committed=committed,
            state_changed=state_changed,
            action=action,
        )

    def state_dict(self) -> dict[str, Any]:
        return {"guard": self._guard.state_dict()}

    @classmethod
    def from_state_dict(
        cls, state: dict[str, Any]
    ) -> TransactionalOutcomeRevisionCoordinator:
        return cls(CoverageAwareOutcomeGuard.from_state_dict(state["guard"]))


__all__ = [
    "TransactionalOutcomeRevisionCoordinator",
    "TransactionalOutcomeRevisionSnapshot",
]

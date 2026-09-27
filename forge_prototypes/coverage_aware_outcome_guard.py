from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Any

from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot
from forge_prototypes.observed_outcome_revision_loop import (
    ObservedOutcomeRevisionLoop,
    ObservedOutcomeRevisionSnapshot,
)
from forge_prototypes.plural_scope_revision_bridge import (
    PluralScopeRevisionBridge,
    PluralScopeRevisionSnapshot,
)


@dataclass(frozen=True, slots=True)
class CoverageAwareOutcomeSnapshot:
    observed_value: str
    outcome_exposed: bool
    exposed_probability_mass: float
    tail_probability_mass: float
    observed_probability_lower: float
    observed_probability_upper: float
    prediction_error_lower: float
    prediction_error_upper: float
    lower_route: PluralScopeRevisionSnapshot
    upper_route: PluralScopeRevisionSnapshot
    applied: ObservedOutcomeRevisionSnapshot | None
    action: str


class CoverageAwareOutcomeGuard:
    """Keep top-k omissions set-valued instead of inventing a probability.

    An exposed outcome has an exact probability and may use the existing
    observed-outcome revision loop.  For an omitted outcome, only the total
    tail mass is known: the outcome probability lies in ``[0, tail_mass]``.
    The guard evaluates both resulting error endpoints and never mutates state.
    This is ordinary interval/coverage validation, not calibrated uncertainty
    or a scientific mechanism.
    """

    def __init__(self, bridge: PluralScopeRevisionBridge | None = None) -> None:
        self._bridge = bridge or PluralScopeRevisionBridge()
        self._loop = ObservedOutcomeRevisionLoop(self._bridge)

    @staticmethod
    def _bounds(
        base: PredictionPoolSnapshot, observed_value: str
    ) -> tuple[bool, float, float, float, float, float, float]:
        if not isinstance(observed_value, str) or not observed_value:
            raise ValueError("observed_value must be a non-empty string")

        probabilities: dict[str, float] = {}
        for row in base.hypotheses:
            probability = float(row.probability)
            if not isfinite(probability) or not 0.0 <= probability <= 1.0:
                raise ValueError("hypothesis probabilities must be finite and in [0, 1]")
            if row.value in probabilities:
                raise ValueError("hypothesis values must be unique")
            probabilities[row.value] = probability

        exposed_mass = sum(probabilities.values())
        if exposed_mass > 1.0 + 1e-9:
            raise ValueError("exposed hypothesis probability mass must not exceed 1")
        exposed_mass = min(exposed_mass, 1.0)
        tail_mass = max(0.0, 1.0 - exposed_mass)

        if observed_value in probabilities:
            probability = probabilities[observed_value]
            error = 1.0 - probability
            return True, exposed_mass, tail_mass, probability, probability, error, error

        return False, exposed_mass, tail_mass, 0.0, tail_mass, exposed_mass, 1.0

    @staticmethod
    def _route_identity(snapshot: PluralScopeRevisionSnapshot) -> tuple[Any, ...]:
        return (
            snapshot.routing.selected_scope,
            snapshot.routing.abstained,
            snapshot.action,
        )

    def apply_observed_outcome(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        observed_value: str,
        strength: float = 1.0,
    ) -> CoverageAwareOutcomeSnapshot:
        (
            exposed,
            exposed_mass,
            tail_mass,
            probability_lower,
            probability_upper,
            error_lower,
            error_upper,
        ) = self._bounds(base, observed_value)

        if exposed:
            applied = self._loop.apply_observed_outcome(
                base,
                observation=observation,
                observed_value=observed_value,
                strength=strength,
            )
            return CoverageAwareOutcomeSnapshot(
                observed_value,
                True,
                exposed_mass,
                tail_mass,
                probability_lower,
                probability_upper,
                error_lower,
                error_upper,
                applied.bridge,
                applied.bridge,
                applied,
                f"exposed_{applied.action}",
            )

        # Evaluate omissions against an isolated copy.  Even read-only routing
        # lazily creates an empty per-Assembly allocator cache, which must not
        # leak into the live checkpoint on a no-write path.
        probe = PluralScopeRevisionBridge.from_state_dict(self._bridge.state_dict())
        lower_route = probe.evaluate(
            base, observation=observation, prediction_error=error_lower
        )
        upper_route = probe.evaluate(
            base, observation=observation, prediction_error=error_upper
        )
        stable = self._route_identity(lower_route) == self._route_identity(upper_route)
        action = (
            "unexposed_route_stable_no_revision"
            if stable
            else "unexposed_tail_ambiguous_no_write"
        )
        return CoverageAwareOutcomeSnapshot(
            observed_value,
            False,
            exposed_mass,
            tail_mass,
            probability_lower,
            probability_upper,
            error_lower,
            error_upper,
            lower_route,
            upper_route,
            None,
            action,
        )

    def state_dict(self) -> dict[str, Any]:
        return {"bridge": self._bridge.state_dict()}

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> CoverageAwareOutcomeGuard:
        return cls(PluralScopeRevisionBridge.from_state_dict(state["bridge"]))


__all__ = ["CoverageAwareOutcomeGuard", "CoverageAwareOutcomeSnapshot"]

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Any

from forge_prototypes.multi_hypothesis_prediction_pool import PredictionPoolSnapshot
from forge_prototypes.plural_scope_revision_bridge import (
    PluralScopeRevisionBridge,
    PluralScopeRevisionSnapshot,
)


@dataclass(frozen=True, slots=True)
class ObservedOutcomeRevisionSnapshot:
    observed_value: str
    observed_probability: float
    exposed_probability_mass: float
    prediction_error: float
    outcome_exposed: bool
    bridge: PluralScopeRevisionSnapshot
    action: str


class ObservedOutcomeRevisionLoop:
    """Derive routing error from an exposed prediction and observed outcome.

    The caller supplies the actual later outcome, not a precomputed error or
    scope identity.  A missing outcome remains a no-write diagnostic because
    the current revision overlay may only update already exposed hypotheses.
    This is ordinary bounded scoring/adapter engineering.
    """

    def __init__(self, bridge: PluralScopeRevisionBridge | None = None) -> None:
        self._bridge = bridge or PluralScopeRevisionBridge()

    @staticmethod
    def _outcome_error(
        base: PredictionPoolSnapshot, observed_value: str
    ) -> tuple[float, float, float, bool]:
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
        probability = probabilities.get(observed_value, 0.0)
        return probability, exposed_mass, 1.0 - probability, observed_value in probabilities

    def inspect(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        observed_value: str,
    ) -> ObservedOutcomeRevisionSnapshot:
        probability, mass, error, exposed = self._outcome_error(base, observed_value)
        bridge = self._bridge.evaluate(
            base, observation=observation, prediction_error=error
        )
        return ObservedOutcomeRevisionSnapshot(
            observed_value,
            probability,
            mass,
            error,
            exposed,
            bridge,
            "inspected" if exposed else "outcome_not_exposed_no_write",
        )

    def apply_observed_outcome(
        self,
        base: PredictionPoolSnapshot,
        *,
        observation: Sequence[float],
        observed_value: str,
        strength: float = 1.0,
    ) -> ObservedOutcomeRevisionSnapshot:
        probability, mass, error, exposed = self._outcome_error(base, observed_value)
        if not exposed:
            bridge = self._bridge.evaluate(
                base, observation=observation, prediction_error=error
            )
            return ObservedOutcomeRevisionSnapshot(
                observed_value,
                probability,
                mass,
                error,
                False,
                bridge,
                "outcome_not_exposed_no_write",
            )

        bridge = self._bridge.apply_evidence(
            base,
            observation=observation,
            prediction_error=error,
            value=observed_value,
            strength=strength,
        )
        return ObservedOutcomeRevisionSnapshot(
            observed_value,
            probability,
            mass,
            error,
            True,
            bridge,
            f"observed_{bridge.action}",
        )

    def state_dict(self) -> dict[str, Any]:
        return {"bridge": self._bridge.state_dict()}

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> ObservedOutcomeRevisionLoop:
        return cls(PluralScopeRevisionBridge.from_state_dict(state["bridge"]))


__all__ = ["ObservedOutcomeRevisionLoop", "ObservedOutcomeRevisionSnapshot"]

from __future__ import annotations

from typing import Any

from ..worlds import LABELS


class ChanceBound:
    name = "chance"

    def __init__(self, priors: dict[str, float] | None = None) -> None:
        self._priors = priors or {label: 1.0 / len(LABELS) for label in LABELS}
        self.reset()

    def reset(self) -> None:
        self._steps = 0

    def step(self, observation: Any) -> str:
        self._steps += 1
        return max(self._priors, key=self._priors.get)

    def predict_proba(self) -> dict[str, float]:
        return dict(self._priors)

    def state_trace(self) -> dict[str, Any]:
        return {"priors": dict(self._priors), "steps": self._steps}

    def work_counters(self) -> dict[str, int]:
        return {"state_updates": 0, "messages": 0}


class OracleBound:
    """Evaluator-only upper bound; truth is never passed through the observation API."""

    name = "oracle"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._truth: str | None = None
        self._steps = 0

    def step(self, observation: Any) -> None:
        raise RuntimeError("OracleBound is evaluator-only; call evaluator_step with held-out truth")

    def evaluator_step(self, truth: str) -> str:
        self._truth = truth
        self._steps += 1
        return truth

    def predict_proba(self) -> dict[str, float]:
        return {label: float(label == self._truth) for label in LABELS}

    def state_trace(self) -> dict[str, Any]:
        return {"truth_visible_to_model": True, "steps": self._steps}

    def work_counters(self) -> dict[str, int]:
        return {"state_updates": 0, "messages": 0}

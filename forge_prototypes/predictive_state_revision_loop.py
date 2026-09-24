from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from math import sqrt
from typing import Any, Iterable


@dataclass(slots=True)
class PredictiveState:
    state_id: str
    context_mean: tuple[float, ...]
    outcome_mean: float
    count: int = 1
    last_used_step: int = 0


@dataclass(frozen=True, slots=True)
class RevisionDecision:
    action: str
    state_id: str
    context_distance: float
    prediction_error_before: float
    state_count: int


class PredictiveStateBank:
    """Noncanonical update/split/reuse prototype using ordinary memory mechanisms."""

    def __init__(self, *, context_gate: float = 0.35, reuse_error: float = 0.35) -> None:
        self.context_gate = float(context_gate)
        self.reuse_error = float(reuse_error)
        self.states: list[PredictiveState] = []
        self.active_state_id: str | None = None
        self.step = 0

    @staticmethod
    def _distance(left: tuple[float, ...], right: tuple[float, ...]) -> float:
        if len(left) != len(right):
            raise ValueError("context dimensions must match")
        return sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))

    def _new_state(self, context: tuple[float, ...], outcome: float) -> PredictiveState:
        state = PredictiveState(
            state_id=f"state-{len(self.states) + 1:03d}",
            context_mean=context,
            outcome_mean=outcome,
            count=1,
            last_used_step=self.step,
        )
        self.states.append(state)
        return state

    def _update(
        self,
        state: PredictiveState,
        context: tuple[float, ...],
        outcome: float,
    ) -> None:
        new_count = state.count + 1
        state.context_mean = tuple(
            (state.context_mean[index] * state.count + context[index]) / new_count
            for index in range(len(context))
        )
        state.outcome_mean = (state.outcome_mean * state.count + outcome) / new_count
        state.count = new_count
        state.last_used_step = self.step

    def observe(self, context: Iterable[float], outcome: float) -> RevisionDecision:
        self.step += 1
        resolved_context = tuple(float(value) for value in context)
        resolved_outcome = float(outcome)
        if not resolved_context:
            raise ValueError("context must be non-empty")

        compatible: list[tuple[float, float, PredictiveState]] = []
        for state in self.states:
            distance = self._distance(state.context_mean, resolved_context)
            if distance <= self.context_gate:
                compatible.append(
                    (abs(resolved_outcome - state.outcome_mean), distance, state)
                )

        if not self.states or not compatible:
            state = self._new_state(resolved_context, resolved_outcome)
            self.active_state_id = state.state_id
            return RevisionDecision("create", state.state_id, 0.0, 0.0, len(self.states))

        error, distance, state = min(
            compatible,
            key=lambda row: (row[0], row[1], row[2].state_id),
        )
        if error <= self.reuse_error:
            prior_active = self.active_state_id
            action = (
                "reuse"
                if prior_active is not None and prior_active != state.state_id
                else "update"
            )
            self._update(state, resolved_context, resolved_outcome)
            self.active_state_id = state.state_id
            return RevisionDecision(action, state.state_id, distance, error, len(self.states))

        state = self._new_state(resolved_context, resolved_outcome)
        self.active_state_id = state.state_id
        return RevisionDecision("split", state.state_id, 0.0, error, len(self.states))

    def snapshot(self) -> list[dict[str, Any]]:
        return [asdict(state) for state in self.states]


@dataclass(slots=True)
class SingleStateEWMA:
    """Overwrite baseline with no persistent alternative hypotheses."""

    alpha: float = 0.5
    prediction: float | None = None

    def observe(self, outcome: float) -> float:
        resolved = float(outcome)
        error = 0.0 if self.prediction is None else abs(resolved - self.prediction)
        if self.prediction is None:
            self.prediction = resolved
        else:
            self.prediction = self.alpha * resolved + (1.0 - self.alpha) * self.prediction
        return error


DEMO_SEQUENCE: tuple[tuple[tuple[float, float], float], ...] = (
    ((0.00, 0.00), 1.00),
    ((0.05, -0.03), 1.10),
    ((-0.04, 0.02), 0.90),
    ((0.02, 0.01), -1.00),
    ((-0.03, -0.02), -0.90),
    ((0.01, 0.03), 1.05),
    ((2.00, 2.00), 1.00),
)


def run_demo() -> dict[str, Any]:
    bank = PredictiveStateBank(context_gate=0.35, reuse_error=0.35)
    baseline = SingleStateEWMA(alpha=0.5)

    decisions: list[dict[str, Any]] = []
    baseline_errors: list[float] = []
    for context, outcome in DEMO_SEQUENCE:
        decisions.append(asdict(bank.observe(context, outcome)))
        baseline_errors.append(baseline.observe(outcome))

    return {
        "decisions": decisions,
        "states": bank.snapshot(),
        "single_state_ewma_errors": baseline_errors,
        "return_to_prior_state_bank_error": decisions[5]["prediction_error_before"],
        "return_to_prior_state_single_state_error": baseline_errors[5],
        "claim_boundary": (
            "Development diagnostic only. Demonstrates an ordinary persistent "
            "multi-hypothesis control loop; establishes no scientific novelty."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, sort_keys=True))

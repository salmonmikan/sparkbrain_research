from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sparkbrain.v05 import ActionDecision, AssemblyActionPolicy


@dataclass(frozen=True, slots=True)
class EligibilityCreditConfig:
    decay: float = 0.80
    learning_rate: float = 0.30
    min_trace: float = 1e-6
    clear_on_reward: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= self.decay <= 1.0:
            raise ValueError("decay must be in [0, 1]")
        if self.learning_rate < 0.0:
            raise ValueError("learning_rate must be non-negative")
        if self.min_trace < 0.0:
            raise ValueError("min_trace must be non-negative")


@dataclass(slots=True)
class EligibilityActionCreditRouter:
    """Forge-only delayed-credit adapter over recent assembly/action pairs."""

    policy: AssemblyActionPolicy
    config: EligibilityCreditConfig = field(default_factory=EligibilityCreditConfig)
    traces: dict[tuple[str, str], float] = field(default_factory=dict)

    def observe_action(self, decision: ActionDecision) -> None:
        self._decay()
        if decision.assembly_id is None or decision.action is None:
            return
        self.traces[(decision.assembly_id, decision.action)] = 1.0

    def reward(self, value: float) -> dict[str, float]:
        reward_value = float(value)
        applied: dict[str, float] = {}
        for (assembly_id, action), eligibility in sorted(self.traces.items()):
            table = self.policy.scores.get(assembly_id)
            if table is None or action not in table:
                continue
            delta = self.config.learning_rate * reward_value * eligibility
            table[action] += delta
            applied[f"{assembly_id}:{action}"] = delta
        if self.config.clear_on_reward:
            self.traces.clear()
        return applied

    def _decay(self) -> None:
        next_traces: dict[tuple[str, str], float] = {}
        for key, value in self.traces.items():
            decayed = value * self.config.decay
            if decayed >= self.config.min_trace:
                next_traces[key] = decayed
        self.traces = next_traces

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": {
                "clear_on_reward": self.config.clear_on_reward,
                "decay": self.config.decay,
                "learning_rate": self.config.learning_rate,
                "min_trace": self.config.min_trace,
            },
            "traces": [
                {
                    "action": action,
                    "assembly_id": assembly_id,
                    "eligibility": eligibility,
                }
                for (assembly_id, action), eligibility in sorted(self.traces.items())
            ],
        }

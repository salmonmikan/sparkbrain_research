from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .contracts import ActionDecision, AssemblyActivation


@dataclass(frozen=True, slots=True)
class ActionPolicyConfig:
    actions: tuple[str, ...] = ("action-0", "action-1", "withhold")
    learning_rate: float = 0.30
    exploration_visits: int = 6


@dataclass(slots=True)
class AssemblyActionPolicy:
    config: ActionPolicyConfig = field(default_factory=ActionPolicyConfig)
    scores: dict[str, dict[str, float]] = field(default_factory=dict)
    visits: dict[str, int] = field(default_factory=dict)
    pending: tuple[str, str] | None = None

    def choose(
        self,
        activation: AssemblyActivation | None,
        *,
        explore: bool = True,
    ) -> ActionDecision:
        if activation is None or activation.suppressed or not activation.mature:
            self.pending = None
            return ActionDecision(None, "withhold", 1.0)
        assembly_id = activation.assembly_id
        table = self.scores.setdefault(
            assembly_id,
            {action: 0.0 for action in self.config.actions},
        )
        visits = self.visits.get(assembly_id, 0)
        if explore and visits < self.config.exploration_visits:
            action = self.config.actions[visits % len(self.config.actions)]
        else:
            action = max(
                self.config.actions,
                key=lambda item: (table[item], -self.config.actions.index(item)),
            )
        self.visits[assembly_id] = visits + 1
        self.pending = (assembly_id, action)
        values = sorted(table.values(), reverse=True)
        margin = values[0] - values[1] if len(values) > 1 else abs(values[0])
        return ActionDecision(assembly_id, action, max(0.0, min(1.0, 0.5 + margin)))

    def reward(self, value: float) -> None:
        if self.pending is None:
            return
        assembly_id, action = self.pending
        self.scores[assembly_id][action] += self.config.learning_rate * float(value)

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": {
                "actions": list(self.config.actions),
                "exploration_visits": self.config.exploration_visits,
                "learning_rate": self.config.learning_rate,
            },
            "pending": list(self.pending) if self.pending is not None else None,
            "scores": {
                key: dict(sorted(value.items())) for key, value in sorted(self.scores.items())
            },
            "visits": dict(sorted(self.visits.items())),
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> AssemblyActionPolicy:
        config_row = value["config"]
        row = cls(
            ActionPolicyConfig(
                actions=tuple(config_row["actions"]),
                learning_rate=float(config_row["learning_rate"]),
                exploration_visits=int(config_row["exploration_visits"]),
            )
        )
        row.pending = tuple(value["pending"]) if value["pending"] is not None else None
        row.scores = {
            str(key): {str(k): float(v) for k, v in table.items()}
            for key, table in value["scores"].items()
        }
        row.visits = {str(k): int(v) for k, v in value["visits"].items()}
        return row

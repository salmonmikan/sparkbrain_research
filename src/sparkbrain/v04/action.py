from __future__ import annotations

from dataclasses import dataclass, field

from .contracts import IgnitionEvent


@dataclass(slots=True)
class ActionAssociator:
    actions: tuple[str, ...] = ("observe", "inspect", "act_a", "act_b")
    learning_rate: float = 0.25
    scores: dict[str, dict[str, float]] = field(default_factory=dict)
    last_signature: str | None = None
    last_action: str | None = None

    def choose(self, ignitions: tuple[IgnitionEvent, ...]) -> str | None:
        if not ignitions:
            self.last_signature = None
            self.last_action = None
            return None
        signature = ignitions[-1].signature
        table = self.scores.setdefault(signature, {action: 0.0 for action in self.actions})
        action = max(self.actions, key=lambda item: (table[item], -self.actions.index(item)))
        self.last_signature = signature
        self.last_action = action
        return action

    def reward(self, value: float) -> None:
        if self.last_signature is None or self.last_action is None:
            return
        table = self.scores[self.last_signature]
        table[self.last_action] += self.learning_rate * float(value)

    def state_dict(self) -> dict[str, object]:
        return {
            "actions": list(self.actions),
            "last_action": self.last_action,
            "last_signature": self.last_signature,
            "learning_rate": self.learning_rate,
            "scores": {
                signature: dict(sorted(table.items()))
                for signature, table in sorted(self.scores.items())
            },
        }

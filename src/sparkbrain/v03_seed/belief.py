from __future__ import annotations

from dataclasses import dataclass

from .contracts import BeliefActivation, IgnitionDecision


@dataclass(frozen=True, slots=True)
class BeliefFieldConfig:
    """Reference dynamics for persistent, entity-scoped belief candidates."""

    decay: float = 0.88
    loser_retention: float = 0.92
    winner_gain: float = 0.55
    winner_threshold: float = 0.60
    winner_margin: float = 0.08

    def validate(self) -> None:
        for name in ("decay", "loser_retention"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.winner_gain < 0 or self.winner_threshold < 0 or self.winner_margin < 0:
            raise ValueError("gain and winner thresholds must be non-negative")


class PersistentBeliefField:
    """Residual loser states, no-ignition, and entity isolation.

    This class is deliberately simple.  It exists to make v0.3's intended state
    contract executable before learned dynamics replace the hand-set update rule.
    """

    def __init__(self, config: BeliefFieldConfig | None = None) -> None:
        self.config = config or BeliefFieldConfig()
        self.config.validate()
        self._states: dict[tuple[str, str], BeliefActivation] = {}

    @staticmethod
    def entity_key(object_key: str | None) -> str:
        return object_key or "__global__"

    def reset(self) -> None:
        self._states.clear()

    def seed(
        self,
        object_key: str | None,
        belief_key: str,
        *,
        activation: float = 0.0,
    ) -> None:
        key = (self.entity_key(object_key), belief_key)
        state = self._states.get(key)
        if state is None:
            self._states[key] = BeliefActivation(
                object_key=object_key,
                belief_key=belief_key,
                activation=max(0.0, activation),
            )
        else:
            state.activation = max(state.activation, activation)

    def update(self, decision: IgnitionDecision, *, time: float) -> None:
        object_key = decision.object_key
        entity = self.entity_key(object_key)
        for (candidate_entity, _), state in self._states.items():
            if candidate_entity != entity:
                continue
            state.activation *= self.config.decay * self.config.loser_retention
            state.last_update_time = time

        if not decision.ignited or decision.belief_key is None:
            return
        self.seed(object_key, decision.belief_key)
        winner = self._states[(entity, decision.belief_key)]
        winner.activation = min(
            2.0,
            winner.activation + self.config.winner_gain * max(0.0, decision.score),
        )
        winner.last_score = decision.score
        winner.last_update_time = time
        winner.ignition_count += 1
        winner.cited_evidence_ids = (
            decision.coalitions[0].support_ids if decision.coalitions else ()
        )

    def activation(self, object_key: str | None, belief_key: str) -> float:
        state = self._states.get((self.entity_key(object_key), belief_key))
        return state.activation if state is not None else 0.0

    def ranked(self, object_key: str | None) -> tuple[BeliefActivation, ...]:
        entity = self.entity_key(object_key)
        return tuple(
            sorted(
                (state for (key, _), state in self._states.items() if key == entity),
                key=lambda row: (-row.activation, row.belief_key),
            )
        )

    def winner(self, object_key: str | None) -> str | None:
        ranked = self.ranked(object_key)
        if not ranked or ranked[0].activation < self.config.winner_threshold:
            return None
        second = ranked[1].activation if len(ranked) > 1 else 0.0
        if ranked[0].activation - second < self.config.winner_margin:
            return None
        return ranked[0].belief_key

from __future__ import annotations

import math
from dataclasses import dataclass

from ..worlds import EVIDENCE_WEIGHTS, LABELS, SwitchEvent


@dataclass(slots=True)
class BaselineStep:
    time: float
    evidence: str
    truth: str
    prediction: str | None
    scores: dict[str, float]


class EvidenceAccumulator:
    """Dense scalar evidence accumulator used as the minimum baseline."""

    name = "accumulator"

    def __init__(
        self, *, decay_tau: float = 4.0, threshold: float = 1.0, margin: float = 0.18
    ) -> None:
        self.decay_tau = decay_tau
        self.threshold = threshold
        self.margin = margin
        self.reset()

    def reset(self) -> None:
        self.scores = {label: 0.0 for label in LABELS}
        self.last_time = 0.0
        self.prediction: str | None = None
        self._updates = 0

    def update(self, event: SwitchEvent) -> BaselineStep:
        dt = max(0.0, event.time - self.last_time)
        decay = math.exp(-dt / self.decay_tau)
        for label in self.scores:
            self.scores[label] *= decay
            self.scores[label] += EVIDENCE_WEIGHTS.get(event.evidence, {}).get(label, 0.0)
        ranked = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        top_label, top_score = ranked[0]
        second_score = ranked[1][1]
        if top_score >= self.threshold and top_score - second_score >= self.margin:
            self.prediction = top_label
        self.last_time = event.time
        self._updates += len(self.scores)
        return BaselineStep(
            event.time,
            event.evidence,
            event.truth,
            self.prediction,
            {label: round(score, 6) for label, score in self.scores.items()},
        )

    def step(self, event: SwitchEvent) -> BaselineStep:
        return self.update(event)

    def predict_proba(self) -> dict[str, float]:
        values = {
            label: math.exp(max(-20.0, min(20.0, score))) for label, score in self.scores.items()
        }
        total = sum(values.values())
        return {label: value / total for label, value in values.items()}

    def state_trace(self) -> dict[str, object]:
        return {"scores": dict(self.scores), "prediction": self.prediction, "time": self.last_time}

    def work_counters(self) -> dict[str, int]:
        return {"state_updates": self._updates, "messages": self._updates}


class HardWinnerTakeAll(EvidenceAccumulator):
    """Ablation baseline that erases all losing hypotheses after selection."""

    name = "hard_wta"

    def update(self, event: SwitchEvent) -> BaselineStep:
        step = super().update(event)
        if self.prediction is not None:
            winner_score = self.scores[self.prediction]
            for label in self.scores:
                self.scores[label] = winner_score if label == self.prediction else 0.0
            step.scores = {label: round(score, 6) for label, score in self.scores.items()}
        return step


class InstantClassifier(EvidenceAccumulator):
    """Chooses from only the current event; deliberately over-reactive."""

    name = "instant"

    def update(self, event: SwitchEvent) -> BaselineStep:
        self.scores = dict(EVIDENCE_WEIGHTS[event.evidence])
        ranked = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        self.prediction = ranked[0][0]
        self.last_time = event.time
        self._updates += len(self.scores)
        return BaselineStep(
            event.time,
            event.evidence,
            event.truth,
            self.prediction,
            {label: round(score, 6) for label, score in self.scores.items()},
        )


def run_baseline(model: EvidenceAccumulator, events: list[SwitchEvent]) -> list[BaselineStep]:
    return [model.update(event) for event in events]

from __future__ import annotations

import math
from dataclasses import dataclass

from .worlds import EVIDENCE_WEIGHTS, LABELS, SwitchEvent


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
        self,
        *,
        decay_tau: float = 4.0,
        threshold: float = 1.0,
        margin: float = 0.18,
    ) -> None:
        self.decay_tau = decay_tau
        self.threshold = threshold
        self.margin = margin
        self.scores = {label: 0.0 for label in LABELS}
        self.last_time = 0.0
        self.prediction: str | None = None

    def update(self, event: SwitchEvent) -> BaselineStep:
        dt = max(0.0, event.time - self.last_time)
        decay = math.exp(-dt / self.decay_tau)
        for label in self.scores:
            self.scores[label] *= decay
            self.scores[label] += EVIDENCE_WEIGHTS[event.evidence][label]

        ranked = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        top_label, top_score = ranked[0]
        second_score = ranked[1][1]
        if top_score >= self.threshold and top_score - second_score >= self.margin:
            self.prediction = top_label
        self.last_time = event.time
        return BaselineStep(
            time=event.time,
            evidence=event.evidence,
            truth=event.truth,
            prediction=self.prediction,
            scores={label: round(score, 6) for label, score in self.scores.items()},
        )


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
        return BaselineStep(
            time=event.time,
            evidence=event.evidence,
            truth=event.truth,
            prediction=self.prediction,
            scores={label: round(score, 6) for label, score in self.scores.items()},
        )


def run_baseline(model: EvidenceAccumulator, events: list[SwitchEvent]) -> list[BaselineStep]:
    return [model.update(event) for event in events]

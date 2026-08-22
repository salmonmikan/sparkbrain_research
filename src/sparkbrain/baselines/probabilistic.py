from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any

from ..tasks.schema import Episode, Observation
from ..worlds import EVIDENCE_WEIGHTS, LABELS


def _normalize(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values())
    if total <= 0:
        return {label: 1.0 / len(values) for label in values}
    return {label: value / total for label, value in values.items()}


class PrivilegedBayesFilter:
    """Bayes-style filter with the repository's declared evidence weights.

    It is explicitly privileged and must not be placed in information-matched rankings.
    """

    name = "privileged_bayes"

    def __init__(self, *, stay_probability: float = 0.84) -> None:
        self.stay_probability = stay_probability
        self.reset()

    def reset(self) -> None:
        self._posterior = {label: 1.0 / len(LABELS) for label in LABELS}
        self._trace: list[dict[str, Any]] = []
        self._updates = 0

    def step(self, observation: Observation) -> str:
        switch = (1.0 - self.stay_probability) / (len(LABELS) - 1)
        prior = {
            label: sum(
                probability * (self.stay_probability if source == label else switch)
                for source, probability in self._posterior.items()
            )
            for label in LABELS
        }
        weights = EVIDENCE_WEIGHTS.get(observation.evidence_label, {})
        likelihood = {label: math.exp(float(weights.get(label, 0.0))) for label in LABELS}
        self._posterior = _normalize({label: prior[label] * likelihood[label] for label in LABELS})
        self._updates += len(LABELS) ** 2 + len(LABELS)
        prediction = max(self._posterior, key=self._posterior.get)
        self._trace.append(
            {"step_index": observation.step_index, "posterior": dict(self._posterior)}
        )
        return prediction

    def predict_proba(self) -> dict[str, float]:
        return dict(self._posterior)

    def state_trace(self) -> dict[str, Any]:
        return {"posterior": dict(self._posterior), "steps": list(self._trace)}

    def work_counters(self) -> dict[str, int]:
        return {"state_updates": self._updates, "messages": self._updates}


class LaplaceHMM:
    """Causal discrete HMM estimated only from supplied training episodes."""

    name = "laplace_hmm"

    def __init__(self, *, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self._transition: dict[str, dict[str, float]] = {}
        self._emission: dict[str, dict[str, float]] = {}
        self._vocabulary: set[str] = set()
        self.fitted_split: str | None = None
        self.reset()

    def fit(self, episodes: list[Episode]) -> None:
        if not episodes or any(episode.split not in {"dev", "smoke"} for episode in episodes):
            raise ValueError(
                "HMM fitting accepts local train/dev-like episodes only; frozen test is forbidden"
            )
        transitions: dict[str, Counter[str]] = defaultdict(Counter)
        emissions: dict[str, Counter[str]] = defaultdict(Counter)
        for episode in episodes:
            previous: str | None = None
            for step in episode.steps:
                truth = step.target.belief_truth_by_object.get(
                    step.observation.object_id or "object"
                )
                if truth is None:
                    truth = step.target.belief_truth_by_object[
                        sorted(step.target.belief_truth_by_object)[0]
                    ]
                token = step.observation.evidence_label
                self._vocabulary.add(token)
                emissions[truth][token] += 1
                if previous is not None:
                    transitions[previous][truth] += 1
                previous = truth
        labels = tuple(LABELS)
        vocab = tuple(sorted(self._vocabulary | {"<UNK>"}))
        self._transition = {
            source: _normalize(
                {target: transitions[source][target] + self.alpha for target in labels}
            )
            for source in labels
        }
        self._emission = {
            label: _normalize({token: emissions[label][token] + self.alpha for token in vocab})
            for label in labels
        }
        self.fitted_split = episodes[0].split
        self.reset()

    def reset(self) -> None:
        self._posterior = {label: 1.0 / len(LABELS) for label in LABELS}
        self._trace: list[dict[str, Any]] = []
        self._updates = 0

    def step(self, observation: Observation) -> str:
        if not self._transition:
            raise RuntimeError("fit must be called before step")
        token = (
            observation.evidence_label
            if observation.evidence_label in self._vocabulary
            else "<UNK>"
        )
        prior = {
            label: sum(
                self._posterior[source] * self._transition[source][label] for source in LABELS
            )
            for label in LABELS
        }
        self._posterior = _normalize(
            {label: prior[label] * self._emission[label][token] for label in LABELS}
        )
        self._updates += len(LABELS) ** 2 + len(LABELS)
        prediction = max(self._posterior, key=self._posterior.get)
        self._trace.append(
            {"step_index": observation.step_index, "posterior": dict(self._posterior)}
        )
        return prediction

    def predict_proba(self) -> dict[str, float]:
        return dict(self._posterior)

    def state_trace(self) -> dict[str, Any]:
        return {"posterior": dict(self._posterior), "steps": list(self._trace)}

    def work_counters(self) -> dict[str, int]:
        return {"state_updates": self._updates, "messages": self._updates}

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

from ...tasks.schema import Episode, Observation
from ...worlds import LABELS


def require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("learned baselines require the optional 'learned' extra") from exc
    return torch


def configure_determinism(seed: int, *, threads: int = 1) -> dict[str, Any]:
    torch = require_torch()
    random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(threads)
    torch.use_deterministic_algorithms(True)
    return {
        "seed": seed,
        "torch_version": torch.__version__,
        "threads": threads,
        "deterministic_algorithms": True,
    }


@dataclass(frozen=True, slots=True)
class EncodedEpisode:
    episode_id: str
    features: tuple[tuple[float, ...], ...]
    targets: tuple[int, ...]
    justified: tuple[bool, ...]


class FeatureEncoder:
    """Train/dev-fitted observation-only encoder with a stable UNK path."""

    def __init__(self) -> None:
        self.vocabulary: dict[str, int] = {"<UNK>": 0}
        self.fitted_split: str | None = None

    @staticmethod
    def _tokens(observation: Observation) -> tuple[str, ...]:
        object_id = observation.object_id or "<NONE>"
        reliability = observation.metadata.get("reliability_band", "<NONE>")
        return (
            f"channel:{observation.channel}",
            f"source:{observation.source_id}",
            f"object:{object_id}",
            f"evidence:{observation.evidence_label}",
            f"reliability:{reliability}",
        )

    def fit(self, episodes: list[Episode]) -> None:
        if not episodes or any(episode.split == "test" for episode in episodes):
            raise ValueError("Feature vocabulary must be fit without frozen test episodes")
        tokens = sorted(
            {
                token
                for episode in episodes
                for step in episode.steps
                for token in self._tokens(step.observation)
            }
        )
        self.vocabulary = {"<UNK>": 0, **{token: index + 1 for index, token in enumerate(tokens)}}
        self.fitted_split = episodes[0].split

    @property
    def input_size(self) -> int:
        return len(self.vocabulary) + 3

    def encode_observation(
        self, observation: Observation, *, previous_time: float
    ) -> tuple[float, ...]:
        if self.fitted_split is None:
            raise RuntimeError("FeatureEncoder.fit must be called first")
        values = [0.0] * self.input_size
        for token in self._tokens(observation):
            values[self.vocabulary.get(token, 0)] += 1.0
        values[-3] = float(observation.strength)
        values[-2] = max(0.0, observation.delivery_time - previous_time)
        values[-1] = float(observation.emitted_time <= observation.delivery_time)
        return tuple(values)

    def encode_episode(self, episode: Episode) -> EncodedEpisode:
        previous_time = 0.0
        features: list[tuple[float, ...]] = []
        targets: list[int] = []
        justified: list[bool] = []
        for step in episode.steps:
            observation = step.observation
            features.append(self.encode_observation(observation, previous_time=previous_time))
            previous_time = observation.delivery_time
            object_id = observation.object_id or sorted(step.target.belief_truth_by_object)[0]
            if object_id not in step.target.belief_truth_by_object:
                object_id = sorted(step.target.belief_truth_by_object)[0]
            targets.append(LABELS.index(step.target.belief_truth_by_object[object_id]))
            justified.append(step.target.decision_justified_by_object[object_id])
        return EncodedEpisode(episode.episode_id, tuple(features), tuple(targets), tuple(justified))

    def input_hash(self, episodes: list[Episode]) -> str:
        encoded = [self.encode_episode(episode) for episode in episodes]
        payload = [{"episode_id": row.episode_id, "features": row.features} for row in encoded]
        return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


class TorchStreamingBaseline:
    def __init__(
        self,
        name: str,
        module: Any,
        encoder: FeatureEncoder,
        *,
        context_limit: int = 64,
        confidence_threshold: float = 0.0,
    ) -> None:
        self.name = name
        self.module = module
        self.encoder = encoder
        self.context_limit = context_limit
        self.confidence_threshold = confidence_threshold
        self.reset()

    def reset(self) -> None:
        self._features: list[tuple[float, ...]] = []
        self._probabilities = {label: 1.0 / len(LABELS) for label in LABELS}
        self._trace: list[dict[str, Any]] = []
        self._previous_time = 0.0
        self._updates = 0

    def step(self, observation: Observation) -> str:
        torch = require_torch()
        feature = self.encoder.encode_observation(observation, previous_time=self._previous_time)
        self._previous_time = observation.delivery_time
        self._features.append(feature)
        visible = self._features[-self.context_limit :]
        tensor = torch.tensor([visible], dtype=torch.float32)
        self.module.eval()
        with torch.no_grad():
            logits = self.module(tensor)[0, -1]
            probabilities = torch.softmax(logits, dim=-1).tolist()
        self._probabilities = dict(zip(LABELS, probabilities, strict=True))
        self._updates += int(getattr(self.module, "last_work", len(visible)))
        prediction = max(self._probabilities, key=self._probabilities.get)
        if self._probabilities[prediction] < self.confidence_threshold:
            prediction = None
        self._trace.append(
            {"step_index": observation.step_index, "probabilities": dict(self._probabilities)}
        )
        return prediction

    def predict_proba(self) -> dict[str, float]:
        return dict(self._probabilities)

    def state_trace(self) -> dict[str, Any]:
        return {
            "context_length": len(self._features[-self.context_limit :]),
            "steps": list(self._trace),
        }

    def work_counters(self) -> dict[str, int]:
        return {"state_updates": self._updates, "messages": self._updates}

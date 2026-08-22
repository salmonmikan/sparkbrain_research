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

    @staticmethod
    def _state_digest(
        *, ordered_vocabulary: list[str], fitted_split: str, input_size: int
    ) -> str:
        payload = {
            "schema_version": "0.1",
            "kind": "c05-feature-encoder",
            "ordered_vocabulary": ordered_vocabulary,
            "fitted_split": fitted_split,
            "input_size": input_size,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def state_dict(self) -> dict[str, Any]:
        """Return a strict, portable encoder state without evaluator targets."""

        if self.fitted_split is None:
            raise RuntimeError("FeatureEncoder.fit must be called before serialization")
        if self.fitted_split == "test":
            raise ValueError("FeatureEncoder state cannot originate from test episodes")
        ordered = [
            token for token, _ in sorted(self.vocabulary.items(), key=lambda item: item[1])
        ]
        digest = self._state_digest(
            ordered_vocabulary=ordered,
            fitted_split=self.fitted_split,
            input_size=self.input_size,
        )
        return {
            "schema_version": "0.1",
            "kind": "c05-feature-encoder",
            "ordered_vocabulary": ordered,
            "fitted_split": self.fitted_split,
            "input_size": self.input_size,
            "state_sha256": digest,
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> FeatureEncoder:
        required = {
            "schema_version",
            "kind",
            "ordered_vocabulary",
            "fitted_split",
            "input_size",
            "state_sha256",
        }
        if set(state) != required:
            raise ValueError("FeatureEncoder state fields do not match schema 0.1")
        if state["schema_version"] != "0.1" or state["kind"] != "c05-feature-encoder":
            raise ValueError("Unsupported FeatureEncoder state schema")
        fitted_split = state["fitted_split"]
        if fitted_split not in {"train", "dev", "smoke"}:
            raise ValueError("FeatureEncoder state must originate from train/dev-like data")
        ordered = state["ordered_vocabulary"]
        if (
            not isinstance(ordered, list)
            or not ordered
            or ordered[0] != "<UNK>"
            or any(not isinstance(token, str) or not token for token in ordered)
            or len(set(ordered)) != len(ordered)
        ):
            raise ValueError("FeatureEncoder ordered vocabulary is invalid")
        input_size = state["input_size"]
        if isinstance(input_size, bool) or input_size != len(ordered) + 3:
            raise ValueError("FeatureEncoder input_size does not match its vocabulary")
        digest = cls._state_digest(
            ordered_vocabulary=ordered,
            fitted_split=fitted_split,
            input_size=input_size,
        )
        if state["state_sha256"] != digest:
            raise ValueError("FeatureEncoder state hash mismatch")
        result = cls()
        result.vocabulary = {token: index for index, token in enumerate(ordered)}
        result.fitted_split = fitted_split
        return result

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

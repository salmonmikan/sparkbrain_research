from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from typing import Any

SCHEMA_VERSION = "0.2"
RESERVED_OBSERVATION_KEYS = frozenset({"truth", "answer", "target", "label_truth"})


def reserved_observation_paths(value: Any, *, path: str = "metadata") -> tuple[str, ...]:
    """Return nested metadata paths that expose evaluator-owned field names."""

    leaked: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if str(key).casefold() in RESERVED_OBSERVATION_KEYS:
                leaked.append(child_path)
            leaked.extend(reserved_observation_paths(child, path=child_path))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            leaked.extend(reserved_observation_paths(child, path=f"{path}[{index}]"))
    return tuple(leaked)


@dataclass(frozen=True, slots=True)
class Observation:
    observation_id: str
    step_index: int
    emitted_time: float
    delivery_time: float
    channel: str
    source_id: str
    evidence_id: str
    evidence_label: str
    strength: float = 1.0
    object_id: str | None = None
    metadata: dict[str, str | int | float | bool | None] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.observation_id or not self.source_id or not self.evidence_id:
            raise ValueError("Observation identifiers must not be empty")
        if self.step_index < 0:
            raise ValueError("Observation step_index must be >= 0")
        if self.channel not in {"evidence", "goal", "value"}:
            raise ValueError(f"Unsupported observation channel: {self.channel!r}")
        for name, value in (
            ("emitted_time", self.emitted_time),
            ("delivery_time", self.delivery_time),
            ("strength", self.strength),
        ):
            if not math.isfinite(value):
                raise ValueError(f"Observation {name} must be finite")
        if self.emitted_time < 0 or self.delivery_time < 0:
            raise ValueError("Observation times must be >= 0")
        leaked = reserved_observation_paths(self.metadata)
        if leaked:
            raise ValueError(f"Observation metadata leaks evaluator fields: {list(leaked)}")


@dataclass(frozen=True, slots=True)
class Target:
    belief_truth_by_object: dict[str, str]
    decision_justified_by_object: dict[str, bool]
    optimal_action: str | None = None
    update_required: bool = False
    scenario_tags: tuple[str, ...] = ()
    annotations: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.belief_truth_by_object:
            raise ValueError("Target requires at least one belief truth")
        if set(self.belief_truth_by_object) != set(self.decision_justified_by_object):
            raise ValueError("Target truth and decision-justified objects must match")


@dataclass(frozen=True, slots=True)
class EpisodeStep:
    observation: Observation
    target: Target


@dataclass(frozen=True, slots=True)
class Episode:
    episode_id: str
    world_id: str
    world_version: str
    split: str
    seed: int
    generator_config_hash: str
    steps: tuple[EpisodeStep, ...]
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"Unsupported Episode schema: {self.schema_version!r}")
        if self.split not in {"train", "dev", "test", "smoke"}:
            raise ValueError(f"Unsupported Episode split: {self.split!r}")
        if not self.episode_id or not self.world_id or not self.steps:
            raise ValueError("Episode identifiers and steps must not be empty")
        indices: set[int] = set()
        last_delivery = -math.inf
        for step in self.steps:
            step.observation.validate()
            step.target.validate()
            index = step.observation.step_index
            if index in indices:
                raise ValueError(f"Duplicate Episode step_index: {index}")
            if step.observation.delivery_time < last_delivery:
                raise ValueError("Episode steps must be ordered by delivery_time")
            indices.add(index)
            last_delivery = step.observation.delivery_time

    def to_dict(self) -> dict[str, Any]:
        # Round-trip through JSON so tuple-backed immutable fields implement
        # the array representation required by the persisted schema.
        return json.loads(json.dumps(asdict(self), ensure_ascii=False))

    def canonical_json(self) -> str:
        self.validate()
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def config_hash(config: dict[str, Any]) -> str:
    encoded = json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def episode_id(world_id: str, split: str, seed: int, digest: str) -> str:
    return f"{world_id}:{split}:{seed}:{digest[:12]}"

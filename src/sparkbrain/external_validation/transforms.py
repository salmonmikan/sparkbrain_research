from __future__ import annotations

import random
from dataclasses import dataclass, replace

from ..tasks.schema import Observation


@dataclass(frozen=True, slots=True)
class TransformResult:
    """Target-blind observation transform plus evaluator-side source mapping."""

    observations: tuple[Observation, ...]
    source_indices: tuple[int, ...]
    transform_id: str


def _reindex(
    rows: list[tuple[int, Observation]], *, transform_id: str
) -> TransformResult:
    observations = tuple(
        replace(observation, step_index=index, delivery_time=float(index))
        for index, (_, observation) in enumerate(rows)
    )
    for observation in observations:
        observation.validate()
    return TransformResult(observations, tuple(source for source, _ in rows), transform_id)


def permute_order(observations: tuple[Observation, ...], *, seed: int) -> TransformResult:
    rows = list(enumerate(observations))
    random.Random(seed).shuffle(rows)
    return _reindex(rows, transform_id=f"order_permutation:{seed}")


def delay_observation(
    observations: tuple[Observation, ...], *, source_index: int, delay_steps: int
) -> TransformResult:
    if delay_steps < 1:
        raise ValueError("delay_steps must be >= 1")
    rows = list(enumerate(observations))
    try:
        selected = rows.pop(source_index)
    except IndexError as exc:
        raise ValueError(f"source_index out of range: {source_index}") from exc
    rows.insert(min(len(rows), source_index + delay_steps), selected)
    return _reindex(rows, transform_id=f"delay:{source_index}:{delay_steps}")


def _restatement(text: str) -> str:
    old = "What necessarily had to follow assuming that the above premises were true?"
    new = "Given only the premises above, which conclusion necessarily follows?"
    return text.replace(old, new)


def duplicate_restatement(
    observations: tuple[Observation, ...], *, source_index: int
) -> TransformResult:
    try:
        original = observations[source_index]
    except IndexError as exc:
        raise ValueError(f"source_index out of range: {source_index}") from exc
    metadata = dict(original.metadata)
    metadata["track_c_transform"] = {
        "kind": "duplicate_restatement",
        "original_observation_id": original.observation_id,
    }
    duplicate = replace(
        original,
        observation_id=f"{original.observation_id}:restatement",
        evidence_label=_restatement(original.evidence_label),
        metadata=metadata,
    )
    rows = list(enumerate(observations))
    rows.insert(source_index + 1, (source_index, duplicate))
    return _reindex(rows, transform_id=f"duplicate_restatement:{source_index}")


def correlated_source_variants(
    observations: tuple[Observation, ...], *, source_index: int, count: int = 2
) -> TransformResult:
    if count < 1:
        raise ValueError("count must be >= 1")
    try:
        original = observations[source_index]
    except IndexError as exc:
        raise ValueError(f"source_index out of range: {source_index}") from exc
    rows = list(enumerate(observations))
    inserts: list[tuple[int, Observation]] = []
    for variant in range(count):
        metadata = dict(original.metadata)
        metadata["track_c_transform"] = {
            "kind": "correlated_source_variant",
            "correlation_group": original.evidence_id,
            "variant": variant,
        }
        inserts.append(
            (
                source_index,
                replace(
                    original,
                    observation_id=f"{original.observation_id}:correlated:{variant}",
                    source_id=f"{original.source_id}:correlated:{variant}",
                    metadata=metadata,
                ),
            )
        )
    rows[source_index + 1 : source_index + 1] = inserts
    return _reindex(rows, transform_id=f"correlated_sources:{source_index}:{count}")


def inject_irrelevant_distractor(
    observations: tuple[Observation, ...], *, after_index: int, seed: int
) -> TransformResult:
    if after_index < -1 or after_index >= len(observations):
        raise ValueError(f"after_index out of range: {after_index}")
    rng = random.Random(seed)
    token = rng.randrange(1_000_000)
    distractor = Observation(
        observation_id=f"track_c:distractor:{seed}:{token}",
        step_index=0,
        emitted_time=0.0,
        delivery_time=0.0,
        channel="evidence",
        source_id="track_c:irrelevant",
        evidence_id=f"track_c:distractor:{seed}:{token}",
        evidence_label=f"Irrelevant fact: item-{token} has property-{token % 97}.",
        object_id=f"distractor:{token}",
        metadata={
            "track_c_transform": {
                "kind": "irrelevant_distractor",
                "seed": seed,
            }
        },
    )
    rows = list(enumerate(observations))
    rows.insert(after_index + 1, (-1, distractor))
    return _reindex(rows, transform_id=f"irrelevant_distractor:{after_index}:{seed}")

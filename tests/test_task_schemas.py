from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import jsonschema
import pytest

from sparkbrain.tasks import generate_episode


def test_all_worlds_are_seed_deterministic_and_diverge() -> None:
    worlds = (
        "switchworld",
        "reliability_world",
        "delayed_evidence_world",
        "contradiction_world",
        "multi_object_world",
        "goal_conflict_world",
    )
    for world in worlds:
        first = generate_episode(world, seed=17, split="test", steps=20)
        assert (
            first.canonical_json()
            == generate_episode(world, seed=17, split="test", steps=20).canonical_json()
        )
        assert (
            first.canonical_json()
            != generate_episode(world, seed=18, split="test", steps=20).canonical_json()
        )


def test_episode_schema_validates_generated_payload() -> None:
    root = Path(__file__).parents[1]
    schema = json.loads((root / "schemas/episode-v0.2.schema.json").read_text(encoding="utf-8"))
    payload = generate_episode("switchworld", seed=2, split="smoke", steps=5).to_dict()
    jsonschema.validate(payload, schema)


def test_observation_rejects_truth_leakage() -> None:
    episode = generate_episode("switchworld", seed=2, split="smoke", steps=5)
    observation = replace(episode.steps[0].observation, metadata={"truth": "cat"})
    with pytest.raises(ValueError, match="leaks evaluator"):
        observation.validate()


def test_delayed_world_is_delivery_ordered() -> None:
    episode = generate_episode("delayed_evidence_world", seed=4, steps=50)
    deliveries = [step.observation.delivery_time for step in episode.steps]
    assert deliveries == sorted(deliveries)
    assert any(
        step.observation.delivery_time > step.observation.emitted_time for step in episode.steps
    )


def test_multi_object_ids_are_explicit() -> None:
    episode = generate_episode("multi_object_world", seed=3, steps=12)
    assert {step.observation.object_id for step in episode.steps} == {"a", "b"}
    assert all(set(step.target.belief_truth_by_object) == {"a", "b"} for step in episode.steps)

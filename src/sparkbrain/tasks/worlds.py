from __future__ import annotations

import random
from collections.abc import Callable
from typing import Any

from ..worlds import EVIDENCE_BY_STATE, EVIDENCE_WEIGHTS, LABELS
from .schema import Episode, EpisodeStep, Observation, Target, config_hash, episode_id

WorldFactory = Callable[..., Episode]


def _finalize(
    world_id: str,
    seed: int,
    split: str,
    config: dict[str, Any],
    rows: list[tuple[Observation, Target]],
) -> Episode:
    digest = config_hash(config)
    rows.sort(key=lambda row: (row[0].delivery_time, row[0].step_index))
    normalized = tuple(
        EpisodeStep(
            Observation(
                observation_id=obs.observation_id,
                step_index=index,
                emitted_time=obs.emitted_time,
                delivery_time=obs.delivery_time,
                channel=obs.channel,
                source_id=obs.source_id,
                evidence_id=obs.evidence_id,
                evidence_label=obs.evidence_label,
                strength=obs.strength,
                object_id=obs.object_id,
                metadata=obs.metadata,
            ),
            target,
        )
        for index, (obs, target) in enumerate(rows)
    )
    result = Episode(
        episode_id(world_id, split, seed, digest), world_id, "0.2", split, seed, digest, normalized
    )
    result.validate()
    return result


def switchworld(*, seed: int, split: str = "test", steps: int = 30, **_: Any) -> Episode:
    rng = random.Random(seed)
    truth = rng.choice(LABELS)
    rows: list[tuple[Observation, Target]] = []
    config = {"steps": steps, "switch_probability": 0.16, "noise_probability": 0.22}
    for index in range(steps):
        switched = index > 0 and rng.random() < config["switch_probability"]
        if switched:
            truth = rng.choice([label for label in LABELS if label != truth])
        noise = rng.random() < config["noise_probability"]
        evidence = rng.choice(tuple(EVIDENCE_WEIGHTS) if noise else EVIDENCE_BY_STATE[truth])
        tags = tuple(
            tag for tag, active in (("state_switch", switched), ("noise", noise)) if active
        )
        obs = Observation(
            f"obs:{index}",
            index,
            float(index + 1),
            float(index + 1),
            "evidence",
            f"sensor:{evidence}",
            f"e:{seed}:{index}",
            evidence,
        )
        target = Target(
            {"object": truth}, {"object": True}, update_required=switched, scenario_tags=tags
        )
        rows.append((obs, target))
    return _finalize("switchworld", seed, split, config, rows)


def reliability_world(*, seed: int, split: str = "test", steps: int = 30, **_: Any) -> Episode:
    rng = random.Random(seed)
    truth = rng.choice(LABELS)
    reliabilities = {
        "sensor:high": 0.90,
        "sensor:low": 0.58,
        "sensor:corr-a": 0.74,
        "sensor:corr-b": 0.74,
    }
    rows: list[tuple[Observation, Target]] = []
    config = {"steps": steps, "reliabilities": reliabilities}
    previous_id = ""
    for index in range(steps):
        source = rng.choice(tuple(reliabilities))
        reliability = reliabilities[source]
        correct = rng.random() < reliability
        evidence = rng.choice(EVIDENCE_BY_STATE[truth] if correct else tuple(EVIDENCE_WEIGHTS))
        duplicate = index > 0 and index % 9 == 0
        evidence_id = previous_id if duplicate else f"e:{seed}:{index}"
        previous_id = evidence_id
        tags = (
            ("duplicate",)
            if duplicate
            else (("correlated",) if source.startswith("sensor:corr") else ())
        )
        obs = Observation(
            f"obs:{index}",
            index,
            float(index + 1),
            float(index + 1),
            "evidence",
            source,
            evidence_id,
            evidence,
            reliability,
            metadata={"reliability_band": "high" if reliability >= 0.8 else "low"},
        )
        target = Target(
            {"object": truth},
            {"object": True},
            scenario_tags=tags,
            annotations={
                "source_reliability": reliability,
                "correlation_group": "corr" if source.startswith("sensor:corr") else None,
            },
        )
        rows.append((obs, target))
    return _finalize("reliability_world", seed, split, config, rows)


def delayed_evidence_world(*, seed: int, split: str = "test", steps: int = 30, **_: Any) -> Episode:
    rng = random.Random(seed)
    truth = rng.choice(LABELS)
    rows: list[tuple[Observation, Target]] = []
    config = {"steps": steps, "max_delay": 3}
    for index in range(steps):
        switched = index > 0 and index % 10 == 0
        if switched:
            truth = rng.choice([label for label in LABELS if label != truth])
        delay = rng.randint(0, 3)
        emitted = float(index + 1)
        evidence = rng.choice(EVIDENCE_BY_STATE[truth])
        obs = Observation(
            f"obs:{index}",
            index,
            emitted,
            emitted + delay,
            "evidence",
            f"sensor:{evidence}",
            f"e:{seed}:{index}",
            evidence,
        )
        target = Target(
            {"object": truth},
            {"object": delay == 0 or index > 1},
            update_required=switched,
            scenario_tags=("delayed",) if delay else (),
        )
        rows.append((obs, target))
    return _finalize("delayed_evidence_world", seed, split, config, rows)


def contradiction_world(*, seed: int, split: str = "test", steps: int = 30, **_: Any) -> Episode:
    rng = random.Random(seed)
    truth = rng.choice(LABELS)
    rows: list[tuple[Observation, Target]] = []
    config = {"steps": steps, "contradiction_probability": 0.35}
    for index in range(steps):
        contradictory = rng.random() < config["contradiction_probability"]
        evidence = rng.choice(
            tuple(EVIDENCE_WEIGHTS) if contradictory else EVIDENCE_BY_STATE[truth]
        )
        source = "sensor:shared" if index % 2 else f"sensor:independent:{index}"
        obs = Observation(
            f"obs:{index}",
            index,
            float(index + 1),
            float(index + 1),
            "evidence",
            source,
            f"e:{seed}:{index}",
            evidence,
        )
        target = Target(
            {"object": truth},
            {"object": True},
            scenario_tags=("contradiction",) if contradictory else (),
        )
        rows.append((obs, target))
    return _finalize("contradiction_world", seed, split, config, rows)


def multi_object_world(*, seed: int, split: str = "test", steps: int = 30, **_: Any) -> Episode:
    rng = random.Random(seed)
    truths = {"a": rng.choice(LABELS), "b": rng.choice(LABELS)}
    rows: list[tuple[Observation, Target]] = []
    config = {"steps": steps, "objects": ["a", "b"]}
    for index in range(steps):
        object_id = "a" if index % 3 else "b"
        if index and index % 11 == 0:
            truths[object_id] = rng.choice(
                [label for label in LABELS if label != truths[object_id]]
            )
        evidence = rng.choice(EVIDENCE_BY_STATE[truths[object_id]])
        obs = Observation(
            f"obs:{index}",
            index,
            float(index + 1),
            float(index + 1),
            "evidence",
            f"sensor:{object_id}",
            f"e:{seed}:{object_id}:{index}",
            evidence,
            object_id=object_id,
        )
        target = Target(dict(truths), {"a": True, "b": True}, scenario_tags=("multi_object",))
        rows.append((obs, target))
    return _finalize("multi_object_world", seed, split, config, rows)


def goal_conflict_world(*, seed: int, split: str = "test", steps: int = 30, **_: Any) -> Episode:
    rng = random.Random(seed)
    truth = rng.choice(LABELS)
    rows: list[tuple[Observation, Target]] = []
    config = {"steps": steps, "goals": ["report", "avoid"]}
    for index in range(steps):
        goal = "report" if (index // 5) % 2 == 0 else "avoid"
        if index % 5 == 0:
            obs = Observation(
                f"obs:{index}",
                index,
                float(index + 1),
                float(index + 1),
                "goal",
                "goal-controller",
                f"goal:{seed}:{index}",
                goal,
            )
        else:
            evidence = rng.choice(EVIDENCE_BY_STATE[truth])
            obs = Observation(
                f"obs:{index}",
                index,
                float(index + 1),
                float(index + 1),
                "evidence",
                f"sensor:{evidence}",
                f"e:{seed}:{index}",
                evidence,
            )
        action = f"{goal}:{truth}"
        target = Target(
            {"object": truth},
            {"object": obs.channel == "evidence"},
            optimal_action=action,
            scenario_tags=("goal_change",) if index % 5 == 0 else (),
        )
        rows.append((obs, target))
    return _finalize("goal_conflict_world", seed, split, config, rows)


WORLD_FACTORIES: dict[str, WorldFactory] = {
    "switchworld": switchworld,
    "reliability_world": reliability_world,
    "delayed_evidence_world": delayed_evidence_world,
    "contradiction_world": contradiction_world,
    "multi_object_world": multi_object_world,
    "goal_conflict_world": goal_conflict_world,
}


def generate_episode(world_id: str, *, seed: int, split: str = "test", steps: int = 30) -> Episode:
    try:
        factory = WORLD_FACTORIES[world_id]
    except KeyError as exc:
        raise ValueError(f"Unknown world: {world_id!r}") from exc
    return factory(seed=seed, split=split, steps=steps)

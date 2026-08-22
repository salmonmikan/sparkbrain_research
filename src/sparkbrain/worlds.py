from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass

from .engine import SparkBrain
from .model import BrainConfig, Spark, SparkKind, TraceFrame

LABELS = ("cat", "dog", "toy")

# Hand-authored evidence model for Phase 0/1.  Learned routing is deliberately
# deferred so the dynamic cognition hypothesis can be tested independently.
EVIDENCE_WEIGHTS: dict[str, dict[str, float]] = {
    "fur": {"cat": 0.48, "dog": 0.38, "toy": 0.06},
    "meow": {"cat": 0.82, "dog": -0.18, "toy": -0.05},
    "purr": {"cat": 0.78, "dog": -0.12, "toy": -0.05},
    "bark": {"dog": 0.85, "cat": -0.18, "toy": -0.05},
    "tail_wag": {"dog": 0.55, "cat": 0.10, "toy": 0.00},
    "motionless": {"toy": 0.66, "cat": -0.22, "dog": -0.22},
    "plastic_seam": {"toy": 0.92, "cat": -0.15, "dog": -0.15},
    "warm_body": {"cat": 0.25, "dog": 0.25, "toy": -0.45},
    "four_legs": {"cat": 0.25, "dog": 0.28, "toy": 0.05},
    "whiskers": {"cat": 0.64, "dog": -0.08, "toy": 0.02},
    "collar": {"dog": 0.36, "cat": 0.18, "toy": 0.02},
}

EVIDENCE_BY_STATE: dict[str, tuple[str, ...]] = {
    "cat": ("fur", "meow", "purr", "warm_body", "four_legs", "whiskers"),
    "dog": ("fur", "bark", "tail_wag", "warm_body", "four_legs", "collar"),
    "toy": ("motionless", "plastic_seam", "fur", "four_legs"),
}


@dataclass(frozen=True, slots=True)
class SwitchEvent:
    time: float
    evidence: str
    truth: str
    note: str = ""


class SwitchWorld:
    """Small controlled world for stability/revision experiments."""

    @staticmethod
    def canonical_scenario() -> list[SwitchEvent]:
        return [
            SwitchEvent(1.0, "fur", "cat", "ambiguous weak evidence"),
            SwitchEvent(2.0, "meow", "cat", "independent evidence should ignite CAT"),
            SwitchEvent(3.0, "bark", "cat", "irrelevant/noisy observation; avoid needless switch"),
            SwitchEvent(4.0, "motionless", "toy", "world changes; old belief should weaken"),
            SwitchEvent(5.0, "plastic_seam", "toy", "decisive evidence should ignite TOY"),
            SwitchEvent(6.0, "warm_body", "cat", "world changes back; loser state may recover"),
            SwitchEvent(7.0, "purr", "cat", "independent evidence should restore CAT"),
        ]

    @staticmethod
    def random_episode(
        *,
        seed: int,
        steps: int = 30,
        switch_probability: float = 0.16,
        noise_probability: float = 0.22,
    ) -> list[SwitchEvent]:
        rng = random.Random(seed)
        truth = rng.choice(LABELS)
        events: list[SwitchEvent] = []
        all_evidence = tuple(EVIDENCE_WEIGHTS)

        for step in range(1, steps + 1):
            if step > 1 and rng.random() < switch_probability:
                truth = rng.choice([label for label in LABELS if label != truth])
                note = "state_switch"
            else:
                note = ""

            if rng.random() < noise_probability:
                evidence = rng.choice(all_evidence)
                note = f"{note}|noise" if note else "noise"
            else:
                evidence = rng.choice(EVIDENCE_BY_STATE[truth])

            events.append(SwitchEvent(float(step), evidence, truth, note))
        return events


def build_reference_brain(config: BrainConfig | None = None) -> SparkBrain:
    brain = SparkBrain(config)

    for evidence in EVIDENCE_WEIGHTS:
        brain.add_spark(
            Spark(
                id=f"sensory:{evidence}",
                label=evidence,
                kind=SparkKind.SENSORY,
                organ="perception",
                threshold=0.55,
                base_threshold=0.55,
                decay_tau=0.45,
                metadata={"post_fire_residual": 0.05},
            )
        )

    for label in LABELS:
        brain.add_spark(
            Spark(
                id=f"hypothesis:{label}",
                label=label,
                kind=SparkKind.HYPOTHESIS,
                organ="hypothesis",
                threshold=0.78,
                base_threshold=0.78,
                decay_tau=4.0,
                competition_group="object_identity",
                metadata={"post_fire_residual": 0.84},
            )
        )

    brain.add_spark(
        Spark(
            id="memory:workspace",
            label="working memory",
            kind=SparkKind.MEMORY,
            organ="memory",
            threshold=0.70,
            base_threshold=0.70,
            decay_tau=8.0,
            metadata={"post_fire_residual": 0.70},
        )
    )
    brain.add_spark(
        Spark(
            id="action:report",
            label="report belief",
            kind=SparkKind.ACTION,
            organ="action",
            threshold=0.70,
            base_threshold=0.70,
            decay_tau=1.0,
            metadata={"post_fire_residual": 0.05},
        )
    )

    for evidence, mapping in EVIDENCE_WEIGHTS.items():
        for label, weight in mapping.items():
            brain.connect(
                f"sensory:{evidence}",
                f"hypothesis:{label}",
                weight,
                plastic=False,
                label="evidence",
            )

    brain.add_soft_competition(
        [f"hypothesis:{label}" for label in LABELS],
        weight=-0.16,
    )
    brain.register_broadcast_listener("memory:workspace")
    brain.register_broadcast_listener("action:report")
    return brain


def run_scenario(
    events: Iterable[SwitchEvent],
    *,
    brain: SparkBrain | None = None,
    reward_correct_beliefs: bool = False,
) -> tuple[SparkBrain, list[TraceFrame]]:
    brain = brain or build_reference_brain()
    frames: list[TraceFrame] = []

    for index, item in enumerate(events):
        brain.inject_stimulus(
            target=f"sensory:{item.evidence}",
            label=item.evidence,
            time=item.time,
            source=f"sensor:{item.evidence}",
            evidence_id=f"event:{index}:{item.evidence}",
            metadata={"sensor": item.evidence, "truth": item.truth, "note": item.note},
        )
        brain.run()

        if reward_correct_beliefs and brain.prediction is not None:
            reward = 1.0 if brain.prediction == item.truth else -1.0
            brain.inject_reward(reward=reward, time=brain.time + 0.001)
            brain.run()

        frames.append(brain.snapshot(external_event=item.evidence, truth=item.truth))

    return brain, frames

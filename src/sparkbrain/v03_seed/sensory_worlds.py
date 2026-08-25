from __future__ import annotations

import random
from dataclasses import dataclass

from .contracts import SensorySample


@dataclass(frozen=True, slots=True)
class SensoryWorldStep:
    world: str
    episode_id: str
    event_kind: str
    expected_salient: bool
    sample: SensorySample
    goal_bias: dict[str, float]


def _sample(
    *,
    seed: int,
    episode: str,
    step: int,
    values: dict[str, float],
    omitted_channels: tuple[str, ...] = (),
) -> SensorySample:
    return SensorySample(
        sample_id=f"{episode}:{seed}:{step}",
        time=float(step),
        source_id=f"synthetic:{episode}",
        modality="vision",
        values=values,
        correlation_group=f"{episode}:{seed}:{step}",
        omitted_channels=omitted_channels,
    )


class HabituationWorld:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def steps(self) -> tuple[SensoryWorldStep, ...]:
        values = {"tone": 1.0, "context": 0.5, "background": -0.25}
        return tuple(
            SensoryWorldStep(
                "HabituationWorld",
                f"habituation:{self.seed}",
                "onset" if step == 0 else "predictable_repetition",
                step == 0,
                _sample(
                    seed=self.seed,
                    episode="habituation",
                    step=step,
                    values=values,
                ),
                {},
            )
            for step in range(6)
        )


class UnexpectedChangeWorld:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def episodes(self) -> tuple[tuple[SensoryWorldStep, ...], ...]:
        generator = random.Random(self.seed)
        context = round(generator.uniform(0.15, 0.25), 6)
        episodes: list[tuple[SensoryWorldStep, ...]] = []
        for kind in ("change", "omission"):
            steps: list[SensoryWorldStep] = []
            for step in range(4):
                steps.append(
                    SensoryWorldStep(
                        "UnexpectedChangeWorld",
                        f"{kind}:{self.seed}",
                        "onset" if step == 0 else "predictable_repetition",
                        step == 0,
                        _sample(
                            seed=self.seed,
                            episode=kind,
                            step=step,
                            values={"tone": 1.0, "context": context},
                        ),
                        {},
                    )
                )
            sample = (
                _sample(
                    seed=self.seed,
                    episode=kind,
                    step=4,
                    values={"tone": -1.0, "context": context},
                )
                if kind == "change"
                else _sample(
                    seed=self.seed,
                    episode=kind,
                    step=4,
                    values={"context": context},
                    omitted_channels=("tone",),
                )
            )
            steps.append(
                SensoryWorldStep(
                    "UnexpectedChangeWorld",
                    f"{kind}:{self.seed}",
                    f"unexpected_{kind}",
                    True,
                    sample,
                    {},
                )
            )
            episodes.append(tuple(steps))
        return tuple(episodes)


class GoalTargetWorld:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def steps(self, *, with_goal: bool) -> tuple[SensoryWorldStep, ...]:
        episode = "goal" if with_goal else "no_goal"
        values = (1.0, 1.0, 0.4)
        return tuple(
            SensoryWorldStep(
                "GoalTargetWorld",
                f"{episode}:{self.seed}",
                "weak_goal_target" if step == 2 else ("onset" if step == 0 else "repeat"),
                step in {0, 2},
                _sample(
                    seed=self.seed,
                    episode=episode,
                    step=step,
                    values={"weak": value},
                ),
                {"vision:weak": 999.0} if with_goal and step == 2 else {},
            )
            for step, value in enumerate(values)
        )


class DistractorNoiseWorld:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def steps(self, *, with_goal: bool) -> tuple[SensoryWorldStep, ...]:
        episode = "noise_goal" if with_goal else "noise_no_goal"
        return tuple(
            SensoryWorldStep(
                "DistractorNoiseWorld",
                f"{episode}:{self.seed}",
                "noise_probe" if step >= 2 else ("onset" if step == 0 else "repeat"),
                step == 0,
                _sample(
                    seed=self.seed,
                    episode=episode,
                    step=step,
                    values={"noise": 0.0},
                ),
                {"vision:noise": 999.0} if with_goal and step >= 2 else {},
            )
            for step in range(12)
        )


class StimulusSpecificityWorld:
    def __init__(self, seed: int) -> None:
        self.seed = seed

    def steps(self) -> tuple[SensoryWorldStep, ...]:
        steps = [
            SensoryWorldStep(
                "StimulusSpecificityWorld",
                f"specificity:{self.seed}",
                "onset" if step == 0 else "predictable_repetition",
                step == 0,
                _sample(
                    seed=self.seed,
                    episode="specificity",
                    step=step,
                    values={"adapted": 1.0},
                ),
                {},
            )
            for step in range(4)
        ]
        steps.append(
            SensoryWorldStep(
                "StimulusSpecificityWorld",
                f"specificity:{self.seed}",
                "novel_channel",
                True,
                _sample(
                    seed=self.seed,
                    episode="specificity",
                    step=4,
                    values={"adapted": 1.0, "novel": 0.2},
                ),
                {},
            )
        )
        return tuple(steps)

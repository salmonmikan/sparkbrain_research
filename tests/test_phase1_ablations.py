from __future__ import annotations

import pytest

from sparkbrain.engine import SparkBrain
from sparkbrain.evaluation.ablations import ABLATION_NAMES
from sparkbrain.evaluation.runner import run_episode
from sparkbrain.model import Spark, SparkKind
from sparkbrain.tasks import generate_episode


@pytest.mark.parametrize("condition", ABLATION_NAMES)
def test_every_ablation_runs_shared_harness(condition: str) -> None:
    episode = generate_episode("switchworld", seed=5, split="smoke", steps=8)
    result = run_episode(episode, condition=condition)
    assert result.status == "complete"
    assert result.condition == condition
    assert len(result.steps) == 8


def test_hard_wta_hook_erases_only_same_group_losers() -> None:
    brain = SparkBrain()
    for spark_id, group in (("winner", "g"), ("loser", "g"), ("other", "h")):
        brain.add_spark(
            Spark(
                spark_id,
                spark_id,
                SparkKind.HYPOTHESIS,
                "hyp",
                activation=0.5,
                competition_group=group,
            )
        )
    brain.erase_losing_hypotheses("winner")
    assert brain.sparks["loser"].activation == 0.0
    assert brain.sparks["other"].activation == 0.5


def test_multi_object_runner_keeps_object_predictions_separate() -> None:
    result = run_episode(generate_episode("multi_object_world", seed=9, split="smoke", steps=18))
    assert all(set(row["prediction"]) == {"a", "b"} for row in result.steps)
    assert "object_cross_talk" in result.metrics


def test_reliability_runner_reports_source_sensitivity() -> None:
    result = run_episode(generate_episode("reliability_world", seed=19, steps=30))
    assert result.metrics["source_reliability_sensitivity"] is not None

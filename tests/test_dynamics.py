from __future__ import annotations

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, Spark, SparkKind
from sparkbrain.worlds import SwitchEvent, SwitchWorld, build_reference_brain, run_scenario


def test_single_ambiguous_evidence_does_not_ignite() -> None:
    _, frames = run_scenario([SwitchEvent(1.0, "fur", "cat")])
    assert frames[-1].prediction is None


def test_canonical_scenario_supports_revision_and_recovery() -> None:
    brain, frames = run_scenario(SwitchWorld.canonical_scenario())
    assert [frame.prediction for frame in frames] == [
        None,
        "cat",
        "cat",
        "cat",
        "toy",
        "toy",
        "cat",
    ]
    assert {ignition.label for ignition in brain.ignitions} >= {"cat", "toy"}


def test_event_activity_is_sparse_by_node_count() -> None:
    brain, frames = run_scenario(SwitchWorld.canonical_scenario())
    fractions = [float(frame.stats["active_spark_fraction"]) for frame in frames]
    assert max(fractions) < 1.0
    assert sum(fractions) / len(fractions) < 0.65
    assert brain.stats.edge_evaluations > 0


def test_reward_modulates_plastic_connection() -> None:
    config = BrainConfig(learning_rate=0.2, eligibility_decay=1.0)
    brain = SparkBrain(config)
    brain.add_spark(
        Spark("source", "source", SparkKind.SENSORY, "perception", threshold=0.5, base_threshold=0.5)
    )
    brain.add_spark(
        Spark("target", "target", SparkKind.HYPOTHESIS, "hypothesis", threshold=0.5, base_threshold=0.5)
    )
    edge = brain.connect("source", "target", 0.6, plastic=True)
    before = edge.weight
    brain.inject_stimulus(target="source", label="signal", time=1.0)
    brain.run()
    brain.inject_reward(reward=1.0, time=1.1)
    brain.run()
    assert edge.weight > before


def test_no_residual_ablation_can_still_execute() -> None:
    brain = build_reference_brain()
    for spark in brain.sparks.values():
        if spark.kind is SparkKind.HYPOTHESIS:
            spark.metadata["post_fire_residual"] = 0.02
    brain, frames = run_scenario(SwitchWorld.canonical_scenario(), brain=brain)
    assert len(frames) == 7
    assert brain.stats.events_processed > 0

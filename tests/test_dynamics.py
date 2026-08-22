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
        Spark(
            "source",
            "source",
            SparkKind.SENSORY,
            "perception",
            threshold=0.5,
            base_threshold=0.5,
        )
    )
    brain.add_spark(
        Spark(
            "target",
            "target",
            SparkKind.HYPOTHESIS,
            "hypothesis",
            threshold=0.5,
            base_threshold=0.5,
        )
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


def test_hard_zero_residual_prevents_canonical_loser_recovery() -> None:
    _, recovered_frames = run_scenario(SwitchWorld.canonical_scenario())
    zeroed = build_reference_brain()
    for spark in zeroed.sparks.values():
        if spark.kind is SparkKind.HYPOTHESIS:
            spark.metadata["post_fire_residual"] = 0.0
    zeroed, zeroed_frames = run_scenario(SwitchWorld.canonical_scenario(), brain=zeroed)
    assert recovered_frames[-1].prediction == "cat"
    assert zeroed_frames[-1].prediction is None
    assert zeroed.ignitions == []


def test_cooldown_blocks_repeat_ignition_until_elapsed() -> None:
    brain = SparkBrain(
        BrainConfig(
            ignition_threshold=0.05,
            ignition_margin=0.0,
            min_support_sources=1,
            stability_evaluations=1,
            ignition_cooldown=1.0,
            refractory_period=0.01,
            homeostatic_increment=0.0,
        )
    )
    brain.add_spark(
        Spark(
            "h",
            "h",
            SparkKind.HYPOTHESIS,
            "hypothesis",
            threshold=0.5,
            base_threshold=0.5,
            metadata={"post_fire_residual": 0.0},
        )
    )
    for time, evidence_id in ((1.0, "one"), (1.5, "two"), (2.1, "three")):
        brain.inject_stimulus(target="h", label="h", time=time, evidence_id=evidence_id)
        brain.run()
    assert [ignition.time for ignition in brain.ignitions] == [1.0, 2.1]


def test_stability_resets_when_winner_changes() -> None:
    brain = SparkBrain(
        BrainConfig(ignition_threshold=100.0, min_support_sources=1, stability_evaluations=1)
    )
    for identifier in ("cat", "toy"):
        brain.add_spark(
            Spark(
                identifier,
                identifier,
                SparkKind.HYPOTHESIS,
                "hypothesis",
                threshold=0.5,
                base_threshold=0.5,
            )
        )
    for time, target, strength in ((1.0, "cat", 1.0), (1.1, "cat", 1.0), (2.0, "toy", 3.0)):
        brain.inject_stimulus(target=target, label=target, time=time, strength=strength)
        brain.run()
    assert brain.last_coalitions[0].hypothesis_id == "toy"
    assert brain._stability["toy"] == 1
    assert brain._stability["cat"] < 2


def test_refractory_period_blocks_then_allows_refiring() -> None:
    brain = SparkBrain(BrainConfig(refractory_period=0.5, homeostatic_increment=0.0))
    brain.add_spark(
        Spark(
            "s",
            "s",
            SparkKind.SENSORY,
            "perception",
            threshold=0.5,
            base_threshold=0.5,
            metadata={"post_fire_residual": 0.0},
        )
    )
    for time in (1.0, 1.2, 1.6):
        brain.inject_stimulus(target="s", label="s", time=time)
    brain.run()
    assert brain.sparks["s"].fired_count == 2


def test_workspace_replaces_previous_ignition_when_capacity_is_one() -> None:
    brain = SparkBrain(
        BrainConfig(
            ignition_threshold=0.05,
            ignition_margin=0.0,
            min_support_sources=1,
            stability_evaluations=1,
            workspace_slots=1,
            refractory_period=0.01,
            homeostatic_increment=0.0,
        )
    )
    for identifier in ("cat", "toy"):
        brain.add_spark(
            Spark(
                identifier,
                identifier,
                SparkKind.HYPOTHESIS,
                "hypothesis",
                threshold=0.5,
                base_threshold=0.5,
                metadata={"post_fire_residual": 0.0},
            )
        )
    brain.inject_stimulus(target="cat", label="cat", time=1.0)
    brain.run()
    brain.inject_stimulus(target="toy", label="toy", time=2.0, strength=3.0)
    brain.run()
    assert [item.label for item in brain.workspace] == ["toy"]

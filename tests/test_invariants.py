from __future__ import annotations

from dataclasses import asdict

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, Spark, SparkKind
from sparkbrain.serialization import state_hash
from sparkbrain.worlds import SwitchWorld, build_reference_brain, run_scenario


def test_snapshot_does_not_change_engine_counters_or_core_activation() -> None:
    brain, _ = run_scenario(SwitchWorld.canonical_scenario()[:2])
    counters_before = asdict(brain.stats)
    activation_before = {key: spark.activation for key, spark in brain.sparks.items()}
    brain.snapshot(external_event="inspection", truth="cat")
    assert asdict(brain.stats) == counters_before
    assert {key: spark.activation for key, spark in brain.sparks.items()} == activation_before


def test_inspect_snapshot_does_not_change_any_serialized_state() -> None:
    brain = build_reference_brain()
    brain.inject_stimulus(target="sensory:fur", label="fur", time=1.0)
    brain.run()
    before = state_hash(brain)

    frame = brain.inspect_snapshot(external_event="inspection", truth="cat")

    assert frame.external_event == "inspection"
    assert state_hash(brain) == before


def test_duplicate_evidence_id_is_not_independent_source_diversity() -> None:
    config = BrainConfig(
        ignition_threshold=10.0,
        stability_evaluations=1,
        min_support_sources=1,
    )
    brain = SparkBrain(config)
    for source in ("s1", "s2"):
        brain.add_spark(
            Spark(
                source,
                source,
                SparkKind.SENSORY,
                "perception",
                threshold=0.5,
                base_threshold=0.5,
            )
        )
    brain.add_spark(
        Spark(
            "h",
            "hypothesis",
            SparkKind.HYPOTHESIS,
            "hypothesis",
            threshold=0.5,
            base_threshold=0.5,
        )
    )
    brain.connect("s1", "h", 0.6)
    brain.connect("s2", "h", 0.6)
    for source in ("s1", "s2"):
        brain.inject_stimulus(
            target=source,
            label="same",
            time=1.0,
            evidence_id="same-evidence-id",
            metadata={"sensor": source},
        )
    brain.run()
    coalition = next(item for item in brain.last_coalitions if item.hypothesis_id == "h")
    assert coalition.diversity == 1
    assert len(brain.sparks["h"].supports) == 1


def test_lateral_inhibition_is_not_external_contradiction() -> None:
    brain = SparkBrain(
        BrainConfig(
            ignition_threshold=10.0,
            stability_evaluations=1,
            min_support_sources=1,
        )
    )
    brain.add_spark(
        Spark("s", "signal", SparkKind.SENSORY, "perception", threshold=0.5, base_threshold=0.5)
    )
    for label in ("a", "b"):
        brain.add_spark(
            Spark(
                label,
                label,
                SparkKind.HYPOTHESIS,
                "hypothesis",
                threshold=0.5,
                base_threshold=0.5,
            )
        )
    brain.connect("s", "a", 0.8)
    brain.add_soft_competition(["a", "b"], weight=-0.3)
    brain.inject_stimulus(target="s", label="signal", time=1.0, metadata={"sensor": "s"})
    brain.run()
    assert brain.sparks["b"].contradictions == {}


def test_workspace_respects_capacity() -> None:
    brain = build_reference_brain(BrainConfig(workspace_slots=1))
    brain, _ = run_scenario(SwitchWorld.canonical_scenario(), brain=brain)
    assert len(brain.workspace) == 1
    assert brain.workspace[0].label == "cat"


def test_threshold_relaxes_toward_base() -> None:
    brain = SparkBrain(
        BrainConfig(
            homeostatic_increment=0.2,
            threshold_relaxation_tau=1.0,
            refractory_period=0.1,
        )
    )
    brain.add_spark(
        Spark(
            "s",
            "s",
            SparkKind.SENSORY,
            "perception",
            threshold=0.5,
            base_threshold=0.5,
            decay_tau=1.0,
            metadata={"post_fire_residual": 0.0},
        )
    )
    brain.inject_stimulus(target="s", label="first", time=1.0)
    brain.run()
    elevated = brain.sparks["s"].threshold
    brain.inject_stimulus(target="s", label="touch", time=4.0, strength=0.0)
    brain.run()
    assert elevated > 0.5
    assert 0.5 < brain.sparks["s"].threshold < elevated


def test_reward_does_not_change_nonplastic_edge() -> None:
    brain = SparkBrain(BrainConfig(learning_rate=1.0, eligibility_decay=1.0))
    brain.add_spark(
        Spark("s", "s", SparkKind.SENSORY, "perception", threshold=0.5, base_threshold=0.5)
    )
    brain.add_spark(
        Spark("h", "h", SparkKind.HYPOTHESIS, "hypothesis", threshold=0.5, base_threshold=0.5)
    )
    edge = brain.connect("s", "h", 0.6, plastic=False)
    brain.inject_stimulus(target="s", label="signal", time=1.0)
    brain.run()
    before = edge.weight
    brain.inject_reward(reward=1.0, time=2.0)
    brain.run()
    assert edge.weight == before

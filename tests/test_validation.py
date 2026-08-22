from __future__ import annotations

import math

import pytest

from sparkbrain.engine import SparkBrain
from sparkbrain.model import BrainConfig, EventKind, Spark, SparkKind
from sparkbrain.validation import validate_config, validate_graph


def test_config_rejects_invalid_workspace_capacity() -> None:
    with pytest.raises(ValueError, match="workspace_slots"):
        SparkBrain(BrainConfig(workspace_slots=0))


def test_config_rejects_nonfinite_value() -> None:
    config = BrainConfig(ignition_threshold=math.inf)
    with pytest.raises(ValueError, match="finite"):
        validate_config(config)


def test_config_rejects_invalid_residual() -> None:
    with pytest.raises(ValueError, match="post_fire_residual"):
        SparkBrain(BrainConfig(post_fire_residual=1.1))


def test_duplicate_spark_id_is_rejected() -> None:
    brain = SparkBrain()
    spark = Spark("x", "x", SparkKind.SENSORY, "perception")
    brain.add_spark(spark)
    with pytest.raises(ValueError, match="Duplicate"):
        brain.add_spark(Spark("x", "again", SparkKind.SENSORY, "perception"))


def test_dangling_edge_is_rejected_by_graph_validation() -> None:
    spark = Spark("x", "x", SparkKind.SENSORY, "perception")
    from sparkbrain.model import Connection

    with pytest.raises(ValueError, match="Dangling"):
        validate_graph([spark], [Connection("x", "missing", 1.0)])


def test_nonfinite_event_is_rejected() -> None:
    brain = SparkBrain()
    brain.add_spark(Spark("x", "x", SparkKind.SENSORY, "perception"))
    with pytest.raises(ValueError, match="finite"):
        brain.schedule(
            time=1.0,
            kind=EventKind.STIMULUS,
            source="world",
            target="x",
            strength=math.nan,
        )


def test_event_insertion_order_breaks_equal_time_priority_ties() -> None:
    def run(first: float, second: float) -> int:
        brain = SparkBrain(BrainConfig(homeostatic_increment=0.0))
        brain.add_spark(
            Spark(
                "x",
                "x",
                SparkKind.SENSORY,
                "perception",
                threshold=0.5,
                base_threshold=0.5,
                metadata={"post_fire_residual": 0.0},
            )
        )
        for strength in (first, second):
            brain.schedule(
                time=1.0,
                kind=EventKind.STIMULUS,
                source="world",
                target="x",
                strength=strength,
                priority=0,
            )
        brain.run()
        return brain.sparks["x"].fired_count

    assert run(0.8, -0.8) == 1
    assert run(-0.8, 0.8) == 0


def test_event_limit_error_contains_queue_diagnostics() -> None:
    brain = SparkBrain(BrainConfig(propagation_delay=0.001, refractory_period=0.0001, homeostatic_increment=0.0))
    brain.add_spark(
        Spark(
            "loop",
            "loop",
            SparkKind.SENSORY,
            "perception",
            threshold=0.5,
            base_threshold=0.5,
            metadata={"post_fire_residual": 1.0},
        )
    )
    brain.connect("loop", "loop", 1.0, delay=0.001)
    brain.inject_stimulus(target="loop", label="loop", time=1.0)
    with pytest.raises(RuntimeError, match="remaining=.*next="):
        brain.run(max_events=8)

from __future__ import annotations

import math
from dataclasses import fields
from typing import Any, Iterable

from .model import BrainConfig, Connection, Spark

SCHEMA_VERSION = "0.2"


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")


def validate_config(config: BrainConfig) -> None:
    for field in fields(config):
        value = getattr(config, field.name)
        if isinstance(value, float):
            _require_finite(field.name, value)

    positive = {
        "ignition_threshold": config.ignition_threshold,
        "workspace_slots": float(config.workspace_slots),
        "support_tau": config.support_tau,
        "refractory_period": config.refractory_period,
        "threshold_relaxation_tau": config.threshold_relaxation_tau,
        "max_abs_weight": config.max_abs_weight,
        "propagation_delay": config.propagation_delay,
    }
    for name, value in positive.items():
        if value <= 0:
            raise ValueError(f"{name} must be > 0, got {value!r}")

    nonnegative = {
        "ignition_margin": config.ignition_margin,
        "min_support_sources": float(config.min_support_sources),
        "stability_evaluations": float(config.stability_evaluations),
        "diversity_bonus": config.diversity_bonus,
        "temporal_coherence_bonus": config.temporal_coherence_bonus,
        "contradiction_penalty": config.contradiction_penalty,
        "post_fire_residual": config.post_fire_residual,
        "active_epsilon": config.active_epsilon,
        "homeostatic_increment": config.homeostatic_increment,
        "learning_rate": config.learning_rate,
    }
    for name, value in nonnegative.items():
        if value < 0:
            raise ValueError(f"{name} must be >= 0, got {value!r}")

    if config.min_support_sources < 1:
        raise ValueError("min_support_sources must be >= 1")
    if config.stability_evaluations < 1:
        raise ValueError("stability_evaluations must be >= 1")
    if not 0 <= config.post_fire_residual <= 1:
        raise ValueError("post_fire_residual must be in [0, 1]")
    if not 0 <= config.eligibility_decay <= 1:
        raise ValueError("eligibility_decay must be in [0, 1]")


def validate_spark(spark: Spark) -> None:
    if not spark.id:
        raise ValueError("Spark id must not be empty")
    if spark.threshold <= 0 or spark.base_threshold <= 0:
        raise ValueError(f"Spark thresholds must be > 0: {spark.id}")
    if spark.decay_tau <= 0:
        raise ValueError(f"Spark decay_tau must be > 0: {spark.id}")
    for name in (
        "threshold",
        "base_threshold",
        "decay_tau",
        "activation",
        "last_update",
        "refractory_until",
    ):
        _require_finite(f"{spark.id}.{name}", float(getattr(spark, name)))


def validate_graph(
    sparks: Iterable[Spark],
    connections: Iterable[Connection],
    listeners: Iterable[str] = (),
) -> None:
    spark_rows = list(sparks)
    ids = [spark.id for spark in spark_rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate Spark ids in graph")
    for spark in spark_rows:
        validate_spark(spark)
    id_set = set(ids)
    for edge in connections:
        if edge.source not in id_set or edge.target not in id_set:
            raise ValueError(f"Dangling edge: {edge.source!r} -> {edge.target!r}")
        _require_finite(f"edge {edge.source}->{edge.target} weight", edge.weight)
        _require_finite(f"edge {edge.source}->{edge.target} delay", edge.delay)
        if edge.delay < 0:
            raise ValueError(f"Edge delay must be >= 0: {edge.source}->{edge.target}")
    unknown = set(listeners) - id_set
    if unknown:
        raise ValueError(f"Unknown broadcast listeners: {sorted(unknown)}")


def assert_json_finite(value: Any, location: str = "root") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"Non-finite number at {location}: {value!r}")
    if isinstance(value, dict):
        for key, child in value.items():
            assert_json_finite(child, f"{location}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            assert_json_finite(child, f"{location}[{index}]")

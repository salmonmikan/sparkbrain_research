from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import fields
from typing import Any

from .model import BrainConfig, Connection, EventKind, Spark

SCHEMA_VERSION = "0.2"

REQUIRED_STATE_FIELDS = frozenset(
    {
        "schema_version",
        "config",
        "time",
        "sparks",
        "connections",
        "broadcast_listeners",
        "queue",
        "next_sequence",
        "active_hypotheses",
        "stability",
        "last_top_hypothesis",
        "last_ignition_time",
        "last_ignition_hypothesis",
        "workspace",
        "ignitions",
        "last_coalitions",
        "belief_label",
        "stats",
        "trace",
        "fired_since_frame",
        "active_edges_since_frame",
        "updated_since_frame",
        "random_state",
    }
)
ALLOWED_STATE_FIELDS = REQUIRED_STATE_FIELDS
CONFIG_FIELDS = frozenset(field.name for field in fields(BrainConfig))
REQUIRED_EVENT_FIELDS = frozenset(
    {
        "time",
        "priority",
        "sequence",
        "kind",
        "source",
        "target",
        "strength",
        "evidence_id",
        "evidence_label",
        "metadata",
    }
)
REQUIRED_TRACE_FIELDS = frozenset({"schema_version", "graph", "frames", "ignitions"})


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
        "support_tau": config.support_tau,
        "threshold_relaxation_tau": config.threshold_relaxation_tau,
        "max_abs_weight": config.max_abs_weight,
        "propagation_delay": config.propagation_delay,
    }
    for name, value in positive.items():
        if value <= 0:
            raise ValueError(f"{name} must be > 0, got {value!r}")

    nonnegative = {
        "ignition_margin": config.ignition_margin,
        "ignition_cooldown": config.ignition_cooldown,
        "refractory_period": config.refractory_period,
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

    for name, value in {
        "min_support_sources": config.min_support_sources,
        "stability_evaluations": config.stability_evaluations,
        "workspace_slots": config.workspace_slots,
    }.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be an integer >= 1, got {value!r}")
    if isinstance(config.random_seed, bool) or not isinstance(config.random_seed, int):
        raise ValueError(f"random_seed must be an integer, got {config.random_seed!r}")
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


def _require_int(name: str, value: Any, *, minimum: int | None = None) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {value!r}")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value!r}")


def _require_number(name: str, value: Any, *, minimum: float | None = None) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number, got {value!r}")
    _require_finite(name, float(value))
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value!r}")


def validate_config_payload(config: Any) -> None:
    """Validate the exact JSON representation of ``BrainConfig``."""

    if not isinstance(config, dict):
        raise ValueError("Config payload must be a JSON object")
    missing = sorted(CONFIG_FIELDS - set(config))
    if missing:
        raise ValueError(f"Config payload is missing required fields: {missing}")
    unknown = sorted(set(config) - CONFIG_FIELDS)
    if unknown:
        raise ValueError(f"Config payload has unsupported fields: {unknown}")
    try:
        validate_config(BrainConfig(**config))
    except TypeError as exc:
        raise ValueError("Config payload cannot construct BrainConfig") from exc


def validate_trace_payload(payload: Any) -> None:
    """Validate the shape required for dynamics-free trace replay."""

    if not isinstance(payload, dict):
        raise ValueError("Trace payload must be a JSON object")
    if "schema_version" not in payload:
        raise ValueError("Trace payload is missing required field: schema_version")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Unsupported trace schema: {payload['schema_version']!r}")
    missing = sorted(REQUIRED_TRACE_FIELDS - set(payload))
    if missing:
        raise ValueError(f"Trace payload is missing required fields: {missing}")
    unknown = sorted(set(payload) - REQUIRED_TRACE_FIELDS)
    if unknown:
        raise ValueError(f"Trace payload has unsupported fields: {unknown}")
    graph = payload["graph"]
    if not isinstance(graph, dict) or set(graph) != {"nodes", "edges"}:
        raise ValueError("Trace graph must contain exactly nodes and edges")
    if not isinstance(graph["nodes"], list) or not isinstance(graph["edges"], list):
        raise ValueError("Trace graph nodes and edges must be lists")
    for index, node in enumerate(graph["nodes"]):
        if not isinstance(node, dict) or not {"id", "label", "kind", "organ"} <= set(node):
            raise ValueError(f"Trace graph node {index} is malformed")
    if not isinstance(payload["frames"], list):
        raise ValueError("Trace frames must be a list")
    for index, frame in enumerate(payload["frames"]):
        if not isinstance(frame, dict):
            raise ValueError(f"Trace frame {index} must be an object")
        missing_frame = {
            "time",
            "external_event",
            "prediction",
            "sparks",
            "coalitions",
            "workspace",
            "fired",
            "active_edges",
            "stats",
        } - set(frame)
        if missing_frame:
            raise ValueError(
                f"Trace frame {index} is missing required fields: {sorted(missing_frame)}"
            )
    if not isinstance(payload["ignitions"], list):
        raise ValueError("Trace ignitions must be a list")
    assert_json_finite(payload)


def validate_state_payload(state: Any) -> None:
    """Reject incomplete checkpoint payloads before reconstruction.

    The enclosing checkpoint identifies the version of its embedded config.
    All engine state needed for deterministic replay is required here instead
    of silently defaulting.
    """

    if not isinstance(state, dict):
        raise ValueError("State payload must be a JSON object")
    schema_version = state.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        raise ValueError(f"Unsupported state schema: {schema_version!r}")
    missing = sorted(REQUIRED_STATE_FIELDS - set(state))
    if missing:
        raise ValueError(f"State payload is missing required fields: {missing}")
    unknown = sorted(set(state) - ALLOWED_STATE_FIELDS)
    if unknown:
        raise ValueError(f"State payload has unsupported fields: {unknown}")
    validate_config_payload(state["config"])
    _require_number("State time", state["time"], minimum=0.0)
    _require_int("State next_sequence", state["next_sequence"], minimum=0)
    if not isinstance(state["queue"], list):
        raise ValueError("State queue must be a list")
    if not isinstance(state["sparks"], list):
        raise ValueError("State sparks must be a list")
    if not isinstance(state["connections"], list):
        raise ValueError("State connections must be a list")
    if not isinstance(state["broadcast_listeners"], list):
        raise ValueError("State broadcast_listeners must be a list")
    if not isinstance(state["active_hypotheses"], list):
        raise ValueError("State active_hypotheses must be a list")
    if not isinstance(state["stability"], dict):
        raise ValueError("State stability must be an object")
    if not isinstance(state["workspace"], list):
        raise ValueError("State workspace must be a list")
    if not isinstance(state["ignitions"], list):
        raise ValueError("State ignitions must be a list")
    if not isinstance(state["last_coalitions"], list):
        raise ValueError("State last_coalitions must be a list")
    if not isinstance(state["stats"], dict):
        raise ValueError("State stats must be an object")
    if not isinstance(state["trace"], list):
        raise ValueError("State trace must be a list")
    if not isinstance(state["fired_since_frame"], list):
        raise ValueError("State fired_since_frame must be a list")
    if not isinstance(state["active_edges_since_frame"], list):
        raise ValueError("State active_edges_since_frame must be a list")
    if not isinstance(state["updated_since_frame"], list):
        raise ValueError("State updated_since_frame must be a list")
    if not isinstance(state["random_state"], list):
        raise ValueError("State random_state must be a list")

    sequences: set[int] = set()
    for index, event in enumerate(state["queue"]):
        if not isinstance(event, dict):
            raise ValueError(f"State queue event {index} must be an object")
        event_missing = sorted(REQUIRED_EVENT_FIELDS - set(event))
        event_unknown = sorted(set(event) - REQUIRED_EVENT_FIELDS)
        if event_missing or event_unknown:
            raise ValueError(
                f"State queue event {index} has incompatible fields: "
                f"missing={event_missing}, unsupported={event_unknown}"
            )
        _require_number(f"State queue event {index}.time", event["time"], minimum=state["time"])
        _require_number(f"State queue event {index}.strength", event["strength"])
        _require_int(f"State queue event {index}.priority", event["priority"])
        _require_int(f"State queue event {index}.sequence", event["sequence"], minimum=0)
        if event["sequence"] in sequences:
            raise ValueError(f"State queue event {index} has duplicate sequence")
        sequences.add(event["sequence"])
        if event["kind"] not in {kind.value for kind in EventKind}:
            raise ValueError(f"State queue event {index} has unsupported kind: {event['kind']!r}")
        if not isinstance(event["source"], str):
            raise ValueError(f"State queue event {index}.source must be a string")
        if event["target"] is not None and not isinstance(event["target"], str):
            raise ValueError(f"State queue event {index}.target must be a string or null")
        if event["evidence_id"] is not None and not isinstance(event["evidence_id"], str):
            raise ValueError(f"State queue event {index}.evidence_id must be a string or null")
        if event["evidence_label"] is not None and not isinstance(event["evidence_label"], str):
            raise ValueError(f"State queue event {index}.evidence_label must be a string or null")
        if not isinstance(event["metadata"], dict):
            raise ValueError(f"State queue event {index}.metadata must be an object")
    if sequences and state["next_sequence"] <= max(sequences):
        raise ValueError("State next_sequence must exceed every queued event sequence")
    for hypothesis_id, stability in state["stability"].items():
        if not isinstance(hypothesis_id, str):
            raise ValueError("State stability keys must be strings")
        _require_int(f"State stability[{hypothesis_id!r}]", stability, minimum=0)
    assert_json_finite(state)

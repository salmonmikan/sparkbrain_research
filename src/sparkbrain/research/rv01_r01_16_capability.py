"""Prospective exposed-development capability runner for RV01 R01-16.

This module implements the already-preregistered F0/FW/FD/FWD propagation
factorization without granting execution authority.  It contains no held-out or
formal path and performs no I/O.  A future frozen wrapper must bind the exact
source/runtime/package identity and acquire an atomic remote STARTED claim before
calling ``run_development_capability_suite`` exactly once.
"""

from __future__ import annotations

import copy
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import digest

from .rv01.interference_contract import InterferencePhase
from .rv01.interference_runner import (
    _INITIAL_WEIGHT,
    _MAXIMUM_PROBE_SPIKES,
    _directed_edges,
    _ordered_coverage,
    _train_route,
)
from .rv01.physical_learner_bridge import build_physical_field, connection_state_hash
from .rv01_r01_16_factorization import (
    R01_16_ARM,
    R01_16_PROTOCOL_ID,
    ConnectionState,
    R01_16FactorizationConstruction,
)
from .rv01_r01_16_worlds import (
    R0116DevelopmentWorldSpec,
    development_world_grid,
    development_world_grid_hash,
)

_ARMS: tuple[R01_16_ARM, ...] = ("F0", "FW", "FD", "FWD")


def _connection_inventory(field: TemporalExcitableField) -> tuple[ConnectionState, ...]:
    rows = tuple(
        ConnectionState(
            source_id=int(connection.source_id),
            target_id=int(connection.target_id),
            weight=float(connection.weight),
            delay_ms=float(connection.delay_ms),
            plastic=bool(connection.plastic),
        )
        for connection in sorted(
            field.connections.values(),
            key=lambda row: (row.source_id, row.target_id),
        )
    )
    for row in rows:
        row.validate()
    return rows


def _queue_size(field: TemporalExcitableField) -> int:
    return len(field.state_dict().get("queue", ()))


def _traversal_metrics(trace: tuple[int, ...]) -> dict[str, Any]:
    seen: set[int] = set()
    first_visit_positions: list[int] = []
    for index, unit_id in enumerate(trace, start=1):
        if unit_id not in seen:
            seen.add(unit_id)
            first_visit_positions.append(index)
    event_count = len(trace)
    distinct_count = len(seen)
    revisit_count = event_count - distinct_count
    return {
        "event_count": event_count,
        "distinct_unit_count": distinct_count,
        "revisit_count": revisit_count,
        "revisit_rate": revisit_count / event_count if event_count else 0.0,
        "new_state_yield": distinct_count / event_count if event_count else 0.0,
        "first_visit_positions": first_visit_positions,
    }


def _prefix_to_distinct_budget(trace: tuple[int, ...], budget: int) -> tuple[int, ...] | None:
    if budget < 0:
        raise ValueError("distinct budget must be non-negative")
    if budget == 0:
        return ()
    seen: set[int] = set()
    prefix: list[int] = []
    for unit_id in trace:
        prefix.append(unit_id)
        seen.add(unit_id)
        if len(seen) == budget:
            return tuple(prefix)
    return None


def _train_shared_field(
    world: R0116DevelopmentWorldSpec,
) -> tuple[TemporalExcitableField, tuple[ConnectionState, ...]]:
    world.validate()
    field = build_physical_field(
        unit_count=world.unit_count,
        directed_edges=_directed_edges(world),
        threshold=world.threshold,
        initial_weight=_INITIAL_WEIGHT,
        initial_delay_ms=world.lag_ms,
    )
    if _queue_size(field) != 0:
        raise RuntimeError("R01-16 fresh field unexpectedly contains queued propagation")
    pre_training = _connection_inventory(field)
    route_by_id = {route.route_id: route for route in world.routes}
    api_hashes: set[str] = set()
    for phase_index, route_id in enumerate(world.training_order, start=1):
        _, _, api = _train_route(
            world,
            field,
            route_by_id[route_id],
            phase_index=phase_index,
        )
        api_hashes.add(api.api_hash)
    if len(api_hashes) != 1:
        raise RuntimeError("R01-16 learner API changed inside one capability world")
    if _queue_size(field) != 0:
        raise RuntimeError("R01-16 queue-integrity gate failed after training")
    return field, pre_training


def _checkpoint_with_arm(
    checkpoint: dict[str, Any],
    arm_inventory: tuple[ConnectionState, ...],
) -> dict[str, Any]:
    value = copy.deepcopy(checkpoint)
    existing = value.get("connections")
    if not isinstance(existing, list):
        raise TypeError("R01-16 checkpoint connection inventory must be a list")
    existing_keys = {
        (int(row["source_id"]), int(row["target_id"]))
        for row in existing
        if isinstance(row, dict)
    }
    arm_keys = {row.key for row in arm_inventory}
    if existing_keys != arm_keys or len(existing_keys) != len(existing):
        raise RuntimeError("R01-16 arm rewrite would change checkpoint topology")
    value["connections"] = [row.state_dict() for row in arm_inventory]
    return value


def _run_arm(
    world: R0116DevelopmentWorldSpec,
    checkpoint: dict[str, Any],
    route: Any,
    *,
    arm: R01_16_ARM,
    arm_inventory: tuple[ConnectionState, ...],
) -> dict[str, Any]:
    arm_checkpoint = _checkpoint_with_arm(checkpoint, arm_inventory)
    field = TemporalExcitableField.from_state_dict(arm_checkpoint)
    if _queue_size(field) != 0:
        raise RuntimeError("R01-16 arm checkpoint unexpectedly contains queued propagation")
    checkpoint_hash = digest(arm_checkpoint)
    connection_hash_before = connection_state_hash(field)

    cue_time = 100.0
    if field.current_time_ms > cue_time:
        raise RuntimeError("R01-16 common checkpoint has advanced beyond registered cue time")
    field.schedule_arrival(
        SynapticArrival(
            time_ms=cue_time,
            target_id=route.units[0],
            current=world.cue_magnitude,
            source_id=None,
            pulse_id=f"r01-16:{world.world_id}:{route.route_id}:{arm}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    horizon = cue_time + world.probe_horizon_ms(route)
    slice_ms = max(0.25, world.lag_ms / 4.0)
    current = cue_time
    spikes: list[Any] = []
    maximum_queue_size = _queue_size(field)
    halt_reason = "horizon_reached"
    while current < horizon:
        target = min(horizon, current + slice_ms)
        spikes.extend(field.run_until(target))
        current = target
        maximum_queue_size = max(maximum_queue_size, _queue_size(field))
        if len(spikes) > _MAXIMUM_PROBE_SPIKES:
            halt_reason = "spike_budget_exceeded"
            break
        if _queue_size(field) == 0 and current > cue_time:
            halt_reason = "queue_drained"
            break

    later = tuple(row for row in spikes if row.time_ms > cue_time)
    trace = tuple(int(row.unit_id) for row in later)
    expected = route.units[1:]
    connection_hash_after = connection_state_hash(field)
    if connection_hash_after != connection_hash_before:
        raise RuntimeError("R01-16 probe changed frozen connection state")
    contamination = sum(unit_id not in route.units for unit_id in trace)
    coverage = _ordered_coverage(expected, trace)
    return {
        "arm": arm,
        "arm_checkpoint_hash": checkpoint_hash,
        "connection_hash_before": connection_hash_before,
        "connection_hash_after": connection_hash_after,
        "generated_units": list(trace),
        "generated_times_ms": [float(row.time_ms) for row in later],
        "raw_metrics": _traversal_metrics(trace),
        "ordered_retention_fraction": coverage,
        "exact_route_recovered": coverage == 1.0 and contamination == 0,
        "contamination_count": contamination,
        "maximum_queue_size": maximum_queue_size,
        "final_queue_size": _queue_size(field),
        "halt_reason": halt_reason,
    }


def _behavior_signature(row: dict[str, Any]) -> tuple[object, ...]:
    return (
        tuple(row["generated_units"]),
        tuple(row["generated_times_ms"]),
        row["ordered_retention_fraction"],
        row["exact_route_recovered"],
        row["contamination_count"],
        row["common_breadth_reached"],
        tuple(row["common_breadth_units"] or ()),
        digest(row["common_breadth_metrics"]),
    )


def run_capability_world(world: R0116DevelopmentWorldSpec) -> dict[str, Any]:
    """Run one fixed R01-16 exposed-development world exactly as registered."""

    world.validate()
    trained, pre_training = _train_shared_field(world)
    post_training = _connection_inventory(trained)
    checkpoint = trained.state_dict()
    if _queue_size(trained) != 0:
        raise RuntimeError("R01-16 common capability checkpoint queue is not empty")
    construction = R01_16FactorizationConstruction(
        pre_training=pre_training,
        post_training=post_training,
        queued_propagation=(),
    )
    summary = construction.require_any_prospective_contrast()
    route_by_id = {route.route_id: route for route in world.routes}

    probes: list[dict[str, Any]] = []
    for route_id in world.probe_order:
        route = route_by_id[route_id]
        arms = {
            arm: _run_arm(
                world,
                checkpoint,
                route,
                arm=arm,
                arm_inventory=construction.arm_inventory(arm),
            )
            for arm in _ARMS
        }
        common_breadth = min(
            int(row["raw_metrics"]["distinct_unit_count"])
            for row in arms.values()
        )
        for row in arms.values():
            trace = tuple(int(unit) for unit in row["generated_units"])
            prefix = _prefix_to_distinct_budget(trace, common_breadth)
            row["common_breadth_budget"] = common_breadth
            row["common_breadth_reached"] = prefix is not None
            row["common_breadth_units"] = list(prefix) if prefix is not None else None
            row["common_breadth_metrics"] = (
                _traversal_metrics(prefix) if prefix is not None else None
            )
        signatures = {arm: _behavior_signature(arms[arm]) for arm in _ARMS}
        probes.append(
            {
                "probe_route_id": route_id,
                "expected_units": list(route.units[1:]),
                "common_breadth_budget": common_breadth,
                "field_arms": [arms[arm] for arm in _ARMS],
                "contrasts": {
                    "F0_vs_FW_different": signatures["F0"] != signatures["FW"],
                    "F0_vs_FD_different": signatures["F0"] != signatures["FD"],
                    "F0_vs_FWD_different": signatures["F0"] != signatures["FWD"],
                    "FW_vs_FWD_different": signatures["FW"] != signatures["FWD"],
                    "FD_vs_FWD_different": signatures["FD"] != signatures["FWD"],
                },
            }
        )

    return {
        "protocol_id": R01_16_PROTOCOL_ID,
        "phase": "development",
        "world": world.state_dict(),
        "world_specification_hash": world.specification_hash(),
        "common_checkpoint_hash": digest(checkpoint),
        "pre_training": [row.state_dict() for row in pre_training],
        "post_training": [row.state_dict() for row in post_training],
        "factorization_summary": {
            "pre_training_sha256": summary.pre_training_sha256,
            "post_training_sha256": summary.post_training_sha256,
            "queue_sha256": summary.queue_sha256,
            "weight_changed_edges": [list(edge) for edge in summary.weight_changed_edges],
            "delay_changed_edges": [list(edge) for edge in summary.delay_changed_edges],
            "arm_sha256": dict(summary.arm_sha256),
        },
        "queue_integrity": {
            "common_checkpoint_queue_empty": True,
            "queued_propagation_count": 0,
            "disposition": "PASS_EMPTY_COMMON_CHECKPOINT_QUEUE",
        },
        "probes": probes,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
    }


def run_development_capability_suite() -> dict[str, Any]:
    """Run the fixed 25-world R01-16 development capability matrix.

    This function deliberately contains no retry logic and no execution authority.
    The one-way wrapper is responsible for exactly-once control state.
    """

    worlds = [run_capability_world(world) for world in development_world_grid()]
    contrast_counts = {
        key: sum(
            int(probe["contrasts"][key])
            for world in worlds
            for probe in world["probes"]
        )
        for key in (
            "F0_vs_FW_different",
            "F0_vs_FD_different",
            "F0_vs_FWD_different",
            "FW_vs_FWD_different",
            "FD_vs_FWD_different",
        )
    }
    payload = {
        "protocol_id": R01_16_PROTOCOL_ID,
        "phase": "development",
        "world_grid_hash": development_world_grid_hash(),
        "world_count": len(worlds),
        "probe_count": sum(len(world["probes"]) for world in worlds),
        "contrast_difference_counts": contrast_counts,
        "all_physically_effective_arms_behaviorally_identical_to_F0": (
            contrast_counts["F0_vs_FW_different"] == 0
            and contrast_counts["F0_vs_FD_different"] == 0
            and contrast_counts["F0_vs_FWD_different"] == 0
        ),
        "worlds": worlds,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
    }
    payload["suite_hash"] = digest(payload)
    return payload


__all__ = ["run_capability_world", "run_development_capability_suite"]

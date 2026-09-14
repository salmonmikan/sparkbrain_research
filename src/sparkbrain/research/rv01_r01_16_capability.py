"""Prospective exposed-development capability runner for RV01 R01-16.

This module implements the already-preregistered F0/FW/FD/FWD propagation
factorization without granting execution authority. It contains no held-out or
formal path and performs no I/O. A future frozen wrapper must bind the exact
source/runtime/package identity, the preserved construction reachability hashes,
and the prospectively bound exactly-once STARTED claim before calling
``run_development_capability_suite`` exactly once.
"""

from __future__ import annotations

import copy
from collections import Counter
from collections.abc import Mapping
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import digest

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
from .rv01_r01_16_reachability import build_factor_reachability_certificate
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


def _prefix_to_distinct_budget(
    trace: tuple[int, ...], budget: int
) -> tuple[int, ...] | None:
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


def _registered_cue_pulse_id(world: R0116DevelopmentWorldSpec, route: Any) -> str:
    """Return the one cue identity shared by all factorization arms."""

    return f"r01-16:{world.world_id}:{route.route_id}:fixed-cue"


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
    cue_pulse_id = _registered_cue_pulse_id(world, route)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=cue_time,
            target_id=route.units[0],
            current=world.cue_magnitude,
            source_id=None,
            pulse_id=cue_pulse_id,
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
        "registered_cue_pulse_id": cue_pulse_id,
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


def _behavior_signature(row: dict[str, Any]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return exactly the preregistered primary sequence pair."""

    common_breadth_units = row.get("common_breadth_units")
    if common_breadth_units is None:
        raise RuntimeError("R01-16 primary endpoint lacks common-breadth sequence")
    return (
        tuple(int(unit_id) for unit_id in row["generated_units"]),
        tuple(int(unit_id) for unit_id in common_breadth_units),
    )


def _replicated_classification(
    rows: list[tuple[str, str]],
    *,
    support_cell: str,
    negative_cell: str,
    supported: str,
    unsupported: str,
    mixed: str,
) -> dict[str, object]:
    """Apply the fixed >=2-world, all-cell non-compensatory decision rule."""

    world_count = len({world_id for world_id, _ in rows})
    dispositions = Counter(disposition for _, disposition in rows)
    if world_count < 2:
        classification = "INSUFFICIENT_REACHABLE_REPLICATION"
    elif rows and all(disposition == support_cell for _, disposition in rows):
        classification = supported
    elif rows and all(disposition == negative_cell for _, disposition in rows):
        classification = unsupported
    else:
        classification = mixed
    return {
        "classification": classification,
        "eligible_world_count": world_count,
        "eligible_cell_count": len(rows),
        "cell_disposition_counts": dict(sorted(dispositions.items())),
    }


def _require_retained_route_bindings(
    world: R0116DevelopmentWorldSpec,
    retained_reachability_sha256: Mapping[str, str],
) -> None:
    registered = set(world.probe_order)
    retained = set(retained_reachability_sha256)
    if retained != registered:
        missing = sorted(registered - retained)
        extra = sorted(retained - registered)
        raise RuntimeError(
            "R01-16 retained reachability binding does not match fixed probe grid: "
            f"missing={missing}, extra={extra}"
        )
    for route_id, value in retained_reachability_sha256.items():
        if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise ValueError(
                f"R01-16 retained certificate hash for {route_id} is not SHA-256"
            )


def run_capability_world(
    world: R0116DevelopmentWorldSpec,
    *,
    retained_reachability_sha256: Mapping[str, str],
) -> dict[str, Any]:
    """Run one fixed R01-16 exposed-development world exactly as registered."""

    world.validate()
    _require_retained_route_bindings(world, retained_reachability_sha256)
    trained, pre_training = _train_shared_field(world)
    post_training = _connection_inventory(trained)
    checkpoint = trained.state_dict()
    common_checkpoint_hash = digest(checkpoint)
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
        certificate = build_factor_reachability_certificate(
            construction,
            registered_unit_ids=tuple(range(world.unit_count)),
            cue_source_ids=(route.units[0],),
            probe_horizon_ms=world.probe_horizon_ms(route),
        )
        expected_certificate_sha256 = retained_reachability_sha256[route_id]
        if certificate.sha256 != expected_certificate_sha256:
            raise RuntimeError(
                "R01-16 capability reachability reconstruction diverged from retained "
                f"construction evidence for {world.world_id}/{route_id}"
            )
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
        if arms["F0"]["arm_checkpoint_hash"] != common_checkpoint_hash:
            raise RuntimeError("R01-16 F0 did not restore the exact common checkpoint")
        cue_ids = {str(row["registered_cue_pulse_id"]) for row in arms.values()}
        if len(cue_ids) != 1:
            raise RuntimeError("R01-16 factor arms changed the registered cue identity")
        common_breadth = min(
            int(row["raw_metrics"]["distinct_unit_count"])
            for row in arms.values()
        )
        for row in arms.values():
            trace = tuple(int(unit) for unit in row["generated_units"])
            prefix = _prefix_to_distinct_budget(trace, common_breadth)
            if prefix is None:
                raise RuntimeError("R01-16 arm failed its fixed common-breadth budget")
            row["common_breadth_budget"] = common_breadth
            row["common_breadth_reached"] = True
            row["common_breadth_units"] = list(prefix)
            row["common_breadth_metrics"] = _traversal_metrics(prefix)
        signatures = {arm: _behavior_signature(arms[arm]) for arm in _ARMS}
        contrasts = {
            "F0_vs_FW_different": signatures["F0"] != signatures["FW"],
            "F0_vs_FD_different": signatures["F0"] != signatures["FD"],
            "F0_vs_FWD_different": signatures["F0"] != signatures["FWD"],
            "FW_vs_FWD_different": signatures["FW"] != signatures["FWD"],
            "FD_vs_FWD_different": signatures["FD"] != signatures["FWD"],
        }
        if certificate.weight_eligible:
            weight_pair = (
                contrasts["F0_vs_FW_different"],
                contrasts["FD_vs_FWD_different"],
            )
            if all(weight_pair):
                weight_cell = "WEIGHT_SUPPORT_CELL"
            elif not any(weight_pair):
                weight_cell = "WEIGHT_NEGATIVE_CELL"
            else:
                weight_cell = "WEIGHT_DISCORDANT"
        else:
            weight_cell = "WEIGHT_INELIGIBLE_UNREACHABLE"

        if certificate.delay_eligible:
            delay_pair = (
                contrasts["F0_vs_FD_different"],
                contrasts["FW_vs_FWD_different"],
            )
            if all(delay_pair):
                delay_cell = "DELAY_SUPPORT_CELL"
            elif not any(delay_pair):
                delay_cell = "DELAY_NEGATIVE_CELL"
            else:
                delay_cell = "DELAY_DISCORDANT"
        else:
            delay_cell = "DELAY_INELIGIBLE_UNREACHABLE"

        if certificate.combined_eligible:
            combined_cell = (
                "COMBINED_SUPPORT_CELL"
                if contrasts["F0_vs_FWD_different"]
                else "COMBINED_NEGATIVE_CELL"
            )
        else:
            combined_cell = "COMBINED_INELIGIBLE_UNREACHABLE"

        probes.append(
            {
                "probe_route_id": route_id,
                "expected_units": list(route.units[1:]),
                "common_breadth_budget": common_breadth,
                "registered_cue_pulse_id": next(iter(cue_ids)),
                "retained_reachability_certificate_sha256": (
                    expected_certificate_sha256
                ),
                "reachability_certificate_sha256": certificate.sha256,
                "retained_reachability_verified": True,
                "reachability_certificate": certificate.state_dict(),
                "factor_eligibility": {
                    "weight_eligible": certificate.weight_eligible,
                    "delay_eligible": certificate.delay_eligible,
                    "combined_eligible": certificate.combined_eligible,
                },
                "field_arms": [arms[arm] for arm in _ARMS],
                "contrasts": contrasts,
                "primary_cell_classification": {
                    "weight": weight_cell,
                    "delay": delay_cell,
                    "combined": combined_cell,
                },
            }
        )

    return {
        "protocol_id": R01_16_PROTOCOL_ID,
        "phase": "development",
        "world": world.state_dict(),
        "world_specification_hash": world.specification_hash(),
        "common_checkpoint_hash": common_checkpoint_hash,
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
        "retained_reachability_verified": True,
        "probes": probes,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
    }


def _require_world_bindings(
    worlds: tuple[R0116DevelopmentWorldSpec, ...],
    retained_reachability_sha256: Mapping[str, Mapping[str, str]],
) -> None:
    expected_world_ids = {world.world_id for world in worlds}
    retained_world_ids = set(retained_reachability_sha256)
    if retained_world_ids != expected_world_ids:
        missing = sorted(expected_world_ids - retained_world_ids)
        extra = sorted(retained_world_ids - expected_world_ids)
        raise RuntimeError(
            "R01-16 retained reachability world binding does not match fixed grid: "
            f"missing={missing}, extra={extra}"
        )


def run_development_capability_suite(
    *,
    retained_reachability_sha256: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
    """Run the fixed 25-world R01-16 development capability matrix.

    The caller must supply the exact per-world/per-route certificate hashes from
    the preserved construction census. This function deliberately contains no
    retry logic and no execution authority; the one-way wrapper is responsible
    for exactly-once control state.
    """

    fixed_worlds = development_world_grid()
    _require_world_bindings(fixed_worlds, retained_reachability_sha256)
    worlds = [
        run_capability_world(
            world,
            retained_reachability_sha256=retained_reachability_sha256[world.world_id],
        )
        for world in fixed_worlds
    ]
    contrast_keys = (
        "F0_vs_FW_different",
        "F0_vs_FD_different",
        "F0_vs_FWD_different",
        "FW_vs_FWD_different",
        "FD_vs_FWD_different",
    )
    contrast_counts = {
        key: sum(
            int(probe["contrasts"][key])
            for world in worlds
            for probe in world["probes"]
        )
        for key in contrast_keys
    }

    weight_rows: list[tuple[str, str]] = []
    delay_rows: list[tuple[str, str]] = []
    combined_rows: list[tuple[str, str]] = []
    for world in worlds:
        world_id = str(world["world"]["world_id"])
        for probe in world["probes"]:
            eligibility = probe["factor_eligibility"]
            classification = probe["primary_cell_classification"]
            if eligibility["weight_eligible"]:
                weight_rows.append((world_id, str(classification["weight"])))
            if eligibility["delay_eligible"]:
                delay_rows.append((world_id, str(classification["delay"])))
            if eligibility["combined_eligible"]:
                combined_rows.append((world_id, str(classification["combined"])))

    factor_classification = {
        "weight": _replicated_classification(
            weight_rows,
            support_cell="WEIGHT_SUPPORT_CELL",
            negative_cell="WEIGHT_NEGATIVE_CELL",
            supported="WEIGHT_SUPPORTED",
            unsupported="WEIGHT_UNSUPPORTED",
            mixed="WEIGHT_MIXED",
        ),
        "delay": _replicated_classification(
            delay_rows,
            support_cell="DELAY_SUPPORT_CELL",
            negative_cell="DELAY_NEGATIVE_CELL",
            supported="DELAY_SUPPORTED",
            unsupported="DELAY_UNSUPPORTED",
            mixed="DELAY_MIXED",
        ),
        "combined": _replicated_classification(
            combined_rows,
            support_cell="COMBINED_SUPPORT_CELL",
            negative_cell="COMBINED_NEGATIVE_CELL",
            supported="COMBINED_SUPPORTED",
            unsupported="COMBINED_UNSUPPORTED",
            mixed="COMBINED_MIXED",
        ),
    }
    payload = {
        "protocol_id": R01_16_PROTOCOL_ID,
        "phase": "development",
        "world_grid_hash": development_world_grid_hash(),
        "world_count": len(worlds),
        "probe_count": sum(len(world["probes"]) for world in worlds),
        "primary_endpoint": [
            "generated_unit_sequence",
            "common_breadth_unit_sequence",
        ],
        "retained_reachability_verified": True,
        "contrast_difference_counts": contrast_counts,
        "factor_classification": factor_classification,
        "worlds": worlds,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
    }
    payload["suite_hash"] = digest(payload)
    return payload


__all__ = ["run_capability_world", "run_development_capability_suite"]

"""RD006 v2 lag-alignment development revision.

This module preserves the v1 D0 implementation and changes exactly one
science-affecting field: within-route external-event spacing from 5.0 ms to
5.5 ms.  The v1 source, protocol, result, and audit remain immutable history.
"""

from __future__ import annotations

from typing import Any

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1

PROTOCOL_ID = "rv02-rd006-external-learning-reachability-a-v2-lag-alignment"
OBJECT_ID = v1.OBJECT_ID
PARENT_AUDIT_HEAD = "2e4b27b620c7fdd2d4d1803df0f11f13b5ed28e8"
PRIOR_REVISION_PROTOCOL_ID = v1.PROTOCOL_ID
WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS = 5.5

ARMS = v1.ARMS
FAMILIES = v1.FAMILIES
PORTS = v1.PORTS
RD006Config = v1.RD006Config
development_worlds = v1.development_worlds
digest = v1.digest


def training_schedule(world: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    """Build the prospectively fixed v2 schedule with 5.5 ms spacing."""

    rows: list[dict[str, Any]] = []
    ordinal = 0
    for route_index, (route, exposures) in enumerate(
        zip(world["routes"], world["exposures"], strict=True)
    ):
        for episode in range(exposures):
            for position, unit_id in enumerate(route):
                rows.append(
                    {
                        "ordinal": ordinal,
                        "route_index": route_index,
                        "episode": episode,
                        "position": position,
                        "unit_id": unit_id,
                        "time_ms": float(
                            route_index * 10000
                            + episode * 100
                            + position
                            * WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS
                        ),
                        "event_id": f"rd006-v2-ext-{ordinal:06d}",
                    }
                )
                ordinal += 1
    return tuple(rows)


def run_cell(config: RD006Config, world: dict[str, Any]) -> dict[str, Any]:
    config.validate()
    if world["family"] not in FAMILIES or world["ports"] != PORTS:
        raise ValueError("world is outside the fixed RD006 v2 exposed fixture")
    initial = v1.build_initial_field(config, world)
    initial_state = initial.state_dict()
    initial_state_sha256 = digest(initial_state)
    schedule = training_schedule(world)
    schedule_sha256 = digest(schedule)
    arms = {
        arm: v1.run_arm(initial_state, schedule, arm=arm, config=config)
        for arm in ARMS
    }
    if len({result["initial_connection_sha256"] for result in arms.values()}) != 1:
        raise RuntimeError("paired arms do not share identical initial connections")
    ready_arms = tuple(
        arm for arm in ARMS if arms[arm]["status"].startswith("D0_REACHABLE")
    )
    bounded_arms = tuple(
        arm for arm in ARMS if arms[arm]["bounded_failure"] is not None
    )
    measured_clock_ids = {
        arm: tuple(row["return_event_id"] for row in arms[arm]["inspected_clocks"])
        for arm in ARMS
    }
    return {
        "cell_id": f"rv02-rd006-v2-{world['family']}-scale-1",
        "family": world["family"],
        "scale": config.scale,
        "unit_count": config.unit_count,
        "world_id": world["world_id"],
        "world_sha256": world["world_sha256"],
        "topology_sha256": digest(v1.build_topology(config, world)),
        "initial_state_sha256": initial_state_sha256,
        "schedule_sha256": schedule_sha256,
        "schedule_event_count": len(schedule),
        "within_route_external_event_position_interval_ms": (
            WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS
        ),
        "paired_contract": {
            "same_topology": True,
            "same_schedule": True,
            "same_initial_state": True,
            "same_measurement_clocks": len(set(measured_clock_ids.values())) == 1,
            "identical_requested_measurement_clocks": True,
            "only_factor": "ordinary_external_learning_on_vs_off",
        },
        "arms": arms,
        "ready_arms": ready_arms,
        "bounded_arms": bounded_arms,
        "status": (
            "D0_REACHABLE"
            if ready_arms
            else "D0_INCONCLUSIVE_BOUNDED_EXPLOSION"
            if bounded_arms
            else "D0_UNREACHABLE"
        ),
    }


def run_matrix(source_git_sha: str) -> dict[str, Any]:
    v1.require_git_sha(source_git_sha)
    config = RD006Config()
    cells = tuple(run_cell(config, world) for world in development_worlds(config))
    ready_cells = tuple(
        cell["cell_id"] for cell in cells if cell["status"] == "D0_REACHABLE"
    )
    bounded_cells = tuple(
        cell["cell_id"]
        for cell in cells
        if cell["status"] == "D0_INCONCLUSIVE_BOUNDED_EXPLOSION"
    )
    artifact = {
        "schema_version": 1,
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "prior_revision_protocol_id": PRIOR_REVISION_PROTOCOL_ID,
        "parent_audit_head": PARENT_AUDIT_HEAD,
        "phase": "OPEN_DEVELOPMENT",
        "claim_ceiling": "SYSTEM",
        "source_git_sha": source_git_sha,
        "formal_execution": False,
        "held_out_execution": False,
        "capability_scoring": False,
        "configuration": config.state_dict(),
        "only_science_affecting_change": {
            "field": "WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS",
            "from": 5.0,
            "to": WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS,
            "formula": "route_index*10000 + episode*100 + position*5.5",
        },
        "fixed_from_v1": [
            "seed_worlds_routes_exposures_all_six_families",
            "unit_count_degree_scale_topology",
            "threshold_initial_weight_initial_delay_5ms_boundary_gain_input_magnitude",
            "return_lag_window_0.5_to_6.5ms",
            "required_distinct_hidden_sources",
            "event_and_spike_ceilings",
            "ordinary_external_learning_off_vs_on",
            "hidden_return_learning_off",
            "no_capability_scoring_or_heldout",
        ],
        "cells": cells,
        "ready_cell_ids": ready_cells,
        "bounded_explosion_cell_ids": bounded_cells,
        "matrix_status": (
            "D0_REACHABLE_FOR_LATER_ANALYST_REVIEW_WITH_BOUNDED_EXPLOSIONS"
            if ready_cells and bounded_cells
            else "D0_REACHABLE_FOR_LATER_ANALYST_REVIEW"
            if ready_cells
            else "D0_INCONCLUSIVE_BOUNDED_EXPLOSION"
            if bounded_cells
            else "D0_ZERO_REACHABLE_STOP"
        ),
        "later_e0_e1_es_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "scientific_interpretation": (
            "development reachability only; zero confirmatory credit; fresh Analyst "
            "authority required before any later stage"
        ),
    }
    artifact["artifact_sha256"] = digest(artifact)
    return artifact


__all__ = [
    "ARMS",
    "FAMILIES",
    "OBJECT_ID",
    "PARENT_AUDIT_HEAD",
    "PORTS",
    "PRIOR_REVISION_PROTOCOL_ID",
    "PROTOCOL_ID",
    "RD006Config",
    "WITHIN_ROUTE_EXTERNAL_EVENT_POSITION_INTERVAL_MS",
    "development_worlds",
    "digest",
    "run_cell",
    "run_matrix",
    "training_schedule",
]

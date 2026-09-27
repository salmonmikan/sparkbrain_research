"""RD006 v4 one-shot bounded D0 result-bearing execution adapter.

This module is intentionally separate from the v4 synthetic-preflight module,
whose result-bearing entrypoints remain fail-closed.  It connects the already
preflighted v4 ordinary learner to the preserved v3 topology and schedule
without changing either surface.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v3 as v3
from sparkbrain.research import rv02_rd006_external_learning_reachability_v3_d0 as v3d0
from sparkbrain.research import rv02_rd006_external_learning_reachability_v4 as v4
from sparkbrain.v04.field import TemporalExcitableField

PROTOCOL_ID = (
    "rv02-rd006-external-learning-reachability-a-"
    "v4-port-to-hidden-trace-boundary-d0-execution"
)
OBJECT_ID = v4.OBJECT_ID
PARENT_PREFLIGHT_HEAD = "78594102ea03fe3ffc0f6e1e0b8b94dd66351005"
PARENT_PREFLIGHT_TREE = "f41b9bd97630e4822584f3994692eec5d82c66fa"
ANALYST_ALLOCATION_ID = (
    "EVA-20260927T200051+0900-R154-RD006-V4-D0-MATRIX-AUTHORIZATION"
)
ANALYST_ATTRIBUTION_ID = (
    "EVA-20260927T210004+0900-R156-RD006-V4-ATTRIBUTION-CLARIFICATION"
)
DEVELOPMENT_PHASE_BEFORE_OUTPUT = "OPEN_DEVELOPMENT"
DEVELOPMENT_PHASE_AFTER_OUTPUT = "RESULT_EXPOSED_DEVELOPMENT"
EVIDENTIARY_STATUS = "DEVELOPMENT_ZERO_CONFIRMATORY_CREDIT"
ARMS = v1.ARMS
FAMILIES = v1.FAMILIES
PORTS = v1.PORTS
RD006Config = v1.RD006Config
development_worlds = v1.development_worlds
digest = v1.digest

CELL_MEASUREMENT_FIELDS = (
    "completion_status",
    "event_count",
    "spike_count",
    "hidden_spike_count",
    "return_clocks",
    "dynamic_eligible_hidden_sources",
    "maximum_same_clock_source_count",
    "ready_gate_events",
    "ordinary_update_edge_class_counts",
    "prohibited_update_count",
    "new_edge_count",
)


def _assert_fixed_config(config: RD006Config) -> None:
    config.validate()
    if config.state_dict() != RD006Config().state_dict():
        raise ValueError("RD006 v4 D0 configuration differs from frozen surface")
    surface = v4.fixed_future_evaluation_surface()
    expected_surface = {
        "topology": "V3_FIXED",
        "seed": 92701,
        "families": 6,
        "unit_count": 48,
        "edge_count": 384,
        "degree": 8,
        "event_spacing_ms": 5.5,
        "minimum_return_lag_ms": 0.5,
        "maximum_return_lag_ms": 6.5,
        "threshold": 0.5,
        "initial_weight": 0.05,
        "initial_delay_ms": 5.0,
        "boundary_gain": 4.0,
        "input_magnitude": 1.0,
        "max_events_per_run": 4096,
        "max_spikes_per_run": 512,
    }
    if surface != expected_surface:
        raise ValueError("RD006 v4 preflight surface differs from allocation")


def _edge_class(source_id: int, target_id: int) -> str:
    source_role = "PORT" if source_id in PORTS else "HIDDEN"
    target_role = "PORT" if target_id in PORTS else "HIDDEN"
    return f"{source_role}_TO_{target_role}"


def _classified_update(update: v1.PhysicalConnectionUpdate) -> dict[str, Any]:
    row = update.state_dict()
    row["source_role"] = "PORT" if update.source_id in PORTS else "HIDDEN"
    row["target_role"] = "PORT" if update.target_id in PORTS else "HIDDEN"
    row["edge_class"] = _edge_class(update.source_id, update.target_id)
    return row


def build_execution_field(
    config: RD006Config, world: dict[str, Any], preflight: dict[str, Any]
) -> TemporalExcitableField:
    """Reuse the exact v3 execution topology builder after fixed-config checks."""

    _assert_fixed_config(config)
    return v3d0.build_execution_field(config, world, preflight)


def clock_diagnostics(
    field: TemporalExcitableField,
    spikes: tuple[Any, ...],
    *,
    return_unit_id: int,
    return_time_ms: float,
    config: RD006Config,
) -> dict[str, Any]:
    return v3d0.clock_diagnostics(
        field,
        spikes,
        return_unit_id=return_unit_id,
        return_time_ms=return_time_ms,
        config=config,
    )


def run_execution_cell(
    initial_state: dict[str, Any],
    schedule: tuple[dict[str, Any], ...],
    *,
    family: str,
    arm: str,
    config: RD006Config,
    progress_hook: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run one fixed cell; ON observes actual hidden spikes before each pulse."""

    _assert_fixed_config(config)
    if family not in FAMILIES:
        raise ValueError(f"unsupported RD006 family: {family}")
    if arm not in ARMS:
        raise ValueError(f"unsupported RD006 arm: {arm}")
    field = TemporalExcitableField.from_state_dict(initial_state)
    learner = (
        v4.PortToHiddenExternalPlasticity(field)
        if arm == "external_learning_on"
        else None
    )
    initial_connection_rows = v1.connection_rows(field)
    initial_connection_keys = tuple(sorted(field.connections))
    clocks: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []
    bounded_failure: dict[str, Any] | None = None
    if progress_hook is not None:
        progress_hook(
            {
                "event": "CELL_STARTED",
                "family": family,
                "arm": arm,
                "planned_clock_count": len(schedule),
                "initial_connection_sha256": digest(initial_connection_rows),
            }
        )

    for clock_index, row in enumerate(schedule):
        time_ms = float(row["time_ms"])
        try:
            spikes = field.run_until(time_ms)
        except RuntimeError as exc:
            if str(exc) not in {
                "max_events_per_run exceeded",
                "max_spikes_per_run exceeded",
            }:
                raise
            bounded_failure = {
                "error_class": type(exc).__name__,
                "error": str(exc),
                "return_event_id": row["event_id"],
                "return_time_ms": time_ms,
                "return_unit_id": row["unit_id"],
                "last_run_arrivals": field.last_run_arrivals,
                "last_run_spikes": field.last_run_spikes,
                "total_arrivals": field.total_arrivals,
                "total_spikes": field.total_spikes,
            }
            if progress_hook is not None:
                progress_hook(
                    {
                        "event": "CELL_BOUNDED",
                        "family": family,
                        "arm": arm,
                        "clock_index": clock_index,
                        "bounded_failure": bounded_failure,
                    }
                )
            break

        diagnostics = clock_diagnostics(
            field,
            spikes,
            return_unit_id=int(row["unit_id"]),
            return_time_ms=time_ms,
            config=config,
        )
        clocks.append(
            {
                "return_event_id": row["event_id"],
                "return_time_ms": time_ms,
                "return_unit_id": row["unit_id"],
                "raw_spikes": tuple(spike.as_dict() for spike in spikes),
                "hidden_spikes": tuple(
                    spike.as_dict() for spike in spikes if spike.unit_id not in PORTS
                ),
                **diagnostics,
            }
        )
        pulse = v1.RuntimePulse(
            event_id=str(row["event_id"]),
            time_ms=time_ms,
            target=f"unit:{row['unit_id']}",
            magnitude=config.input_magnitude,
        )
        if learner is not None:
            updates.extend(
                _classified_update(update)
                for update in learner.observe_clock(spikes, pulse)
            )
        v1.schedule_external(
            field,
            event_id=str(row["event_id"]),
            time_ms=time_ms,
            unit_id=int(row["unit_id"]),
            magnitude=config.input_magnitude,
        )
        if progress_hook is not None:
            progress_hook(
                {
                    "event": "CLOCK_PRESERVED",
                    "family": family,
                    "arm": arm,
                    "clock_index": clock_index,
                    "clock": clocks[-1],
                    "ordinary_update_count_so_far": len(updates),
                    "ordinary_update_edge_class_counts_so_far": {
                        edge_class: sum(
                            update["edge_class"] == edge_class
                            for update in updates
                        )
                        for edge_class in ("PORT_TO_PORT", "PORT_TO_HIDDEN")
                    },
                    "total_arrivals": field.total_arrivals,
                    "total_spikes": field.total_spikes,
                }
            )

    complete = bounded_failure is None and len(clocks) == len(schedule)
    ready_clocks = tuple(clock for clock in clocks if clock["dynamic_gate_ready"])
    gate_open = complete and bool(ready_clocks) and arm == "external_learning_on"
    final_connection_rows = v1.connection_rows(field)
    final_connection_keys = tuple(sorted(field.connections))
    allowed_classes = {"PORT_TO_PORT", "PORT_TO_HIDDEN"}
    prohibited_updates = tuple(
        update for update in updates if update["edge_class"] not in allowed_classes
    )
    new_edges = tuple(sorted(set(final_connection_keys) - set(initial_connection_keys)))
    if prohibited_updates or new_edges:
        raise RuntimeError("RD006 v4 learner violated the frozen edge-class boundary")
    edge_class_counts = {
        edge_class: sum(update["edge_class"] == edge_class for update in updates)
        for edge_class in ("PORT_TO_PORT", "PORT_TO_HIDDEN")
    }
    result = {
        "execution_cell_id": f"rv02-rd006-v4-{family}-{arm}-scale-1",
        "family": family,
        "arm": arm,
        "ordinary_external_learning_enabled": learner is not None,
        "ordinary_learning_package": (
            "PORT_TO_PORT_PLUS_PORT_TO_HIDDEN" if learner is not None else "NONE"
        ),
        "hidden_return_learning_enabled": False,
        "planned_clock_count": len(schedule),
        "inspected_clock_count": len(clocks),
        "complete_non_exploded": complete,
        "completion_status": (
            "COMPLETED" if complete else "BOUNDED_INCOMPLETE"
        ),
        "bounded_failure": bounded_failure,
        "event_count": field.total_arrivals,
        "spike_count": field.total_spikes,
        "initial_connection_sha256": digest(initial_connection_rows),
        "final_connection_sha256": digest(final_connection_rows),
        "final_connection_rows": final_connection_rows,
        "external_observation_count": (
            learner.external_observation_count if learner is not None else 0
        ),
        "observed_hidden_spike_count": (
            learner.observed_hidden_spike_count if learner is not None else 0
        ),
        "ordinary_update_count": len(updates),
        "ordinary_update_edge_class_counts": edge_class_counts,
        "ordinary_updates": tuple(updates),
        "hidden_return_update_count": 0,
        "return_clocks": tuple(clocks),
        "dynamic_eligible_hidden_sources": tuple(
            {
                "return_event_id": clock["return_event_id"],
                "sources": clock["dynamic_eligible_hidden_sources"],
            }
            for clock in clocks
        ),
        "ready_gate_events": tuple(
            clock["return_event_id"] for clock in ready_clocks
        ),
        "hidden_spike_count": sum(len(clock["hidden_spikes"]) for clock in clocks),
        "distinct_hidden_source_count": len(
            {
                spike["unit_id"]
                for clock in clocks
                for spike in clock["hidden_spikes"]
            }
        ),
        "maximum_structurally_connected_hidden_sources_at_return": max(
            (clock["structurally_connected_hidden_source_count"] for clock in clocks),
            default=0,
        ),
        "maximum_same_clock_source_count": max(
            (clock["dynamic_eligible_hidden_source_count"] for clock in clocks),
            default=0,
        ),
        "selected_dynamic_gate_clock": ready_clocks[0] if ready_clocks else None,
        "dynamic_gate_open": gate_open,
        "prohibited_update_count": len(prohibited_updates),
        "new_edge_count": len(new_edges),
        "status": (
            "D0_REACHABLE_FOR_LATER_ANALYST_REVIEW"
            if gate_open
            else "D0_BOUNDED_INCOMPLETE"
            if bounded_failure is not None
            else "D0_COMPLETE_ZERO_DYNAMIC_ELIGIBLE_CLOCK"
        ),
    }
    if progress_hook is not None:
        progress_hook(
            {
                "event": "CELL_COMPLETED",
                "family": family,
                "arm": arm,
                "cell": result,
            }
        )
    return result


def run_family_pair(
    config: RD006Config,
    world: dict[str, Any],
    *,
    progress_hook: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    _assert_fixed_config(config)
    if world["family"] not in FAMILIES or tuple(world["ports"]) != PORTS:
        raise ValueError("world is outside the fixed RD006 v4 fixture")
    preflight = v3.build_family_preflight(config, world)
    field = build_execution_field(config, world, preflight)
    initial_state = field.state_dict()
    initial_connection_rows = v1.connection_rows(field)
    schedule = v3.declared_schedule(world)
    cells = {
        arm: run_execution_cell(
            initial_state,
            schedule,
            family=str(world["family"]),
            arm=arm,
            config=config,
            progress_hook=progress_hook,
        )
        for arm in ARMS
    }
    if len({cell["initial_connection_sha256"] for cell in cells.values()}) != 1:
        raise RuntimeError("paired cells do not share identical initial connections")
    measured_clock_ids = {
        arm: tuple(
            clock["return_event_id"] for clock in cells[arm]["return_clocks"]
        )
        for arm in ARMS
    }
    return {
        "family": world["family"],
        "world_id": world["world_id"],
        "world_sha256": world["world_sha256"],
        "planned_topology_sha256": preflight["planned_topology_sha256"],
        "static_declared_return_clock": preflight["declared_return_clock"],
        "static_hidden_source_paths": preflight["static_hidden_source_paths"],
        "initial_state_sha256": digest(initial_state),
        "initial_connection_rows": initial_connection_rows,
        "schedule_sha256": digest(schedule),
        "schedule_event_count": len(schedule),
        "paired_contract": {
            "same_topology": True,
            "same_schedule": True,
            "same_initial_state": True,
            "same_requested_measurement_clocks": True,
            "same_completed_measurement_clocks": len(set(measured_clock_ids.values()))
            == 1,
            "only_factor": "complete_ordinary_external_learning_package_on_vs_off",
            "incremental_port_to_hidden_effect_identified": False,
        },
        "execution_cells": cells,
    }


def run_matrix(
    source_git_sha: str,
    *,
    progress_hook: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Execute the single prospectively fixed six-family/two-arm matrix."""

    v1.require_git_sha(source_git_sha)
    config = RD006Config()
    _assert_fixed_config(config)
    family_pairs = tuple(
        run_family_pair(config, world, progress_hook=progress_hook)
        for world in development_worlds(config)
    )
    execution_cells = tuple(
        pair["execution_cells"][arm]
        for pair in family_pairs
        for arm in ARMS
    )
    gate_open_cell_ids = tuple(
        cell["execution_cell_id"]
        for cell in execution_cells
        if cell["dynamic_gate_open"]
    )
    bounded_cell_ids = tuple(
        cell["execution_cell_id"]
        for cell in execution_cells
        if cell["bounded_failure"] is not None
    )
    complete_cell_ids = tuple(
        cell["execution_cell_id"]
        for cell in execution_cells
        if cell["complete_non_exploded"]
    )
    artifact = {
        "schema_version": 1,
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "parent_preflight_head": PARENT_PREFLIGHT_HEAD,
        "parent_preflight_tree": PARENT_PREFLIGHT_TREE,
        "analyst_allocation_id": ANALYST_ALLOCATION_ID,
        "analyst_attribution_id": ANALYST_ATTRIBUTION_ID,
        "development_phase_before_output": DEVELOPMENT_PHASE_BEFORE_OUTPUT,
        "development_phase_after_output": DEVELOPMENT_PHASE_AFTER_OUTPUT,
        "claim_ceiling": "SYSTEM",
        "evidentiary_status": EVIDENTIARY_STATUS,
        "scientific_credit": 0,
        "source_git_sha": source_git_sha,
        "formal_execution": False,
        "held_out_execution": False,
        "capability_scoring": False,
        "configuration": config.state_dict(),
        "construction_rule_id": v3.CONSTRUCTION_RULE_ID,
        "within_route_external_event_position_interval_ms": 5.5,
        "factors": {
            "ordinary_external_learning": ["OFF", "ON"],
            "off_package": "NONE",
            "on_package": "PORT_TO_PORT_PLUS_PORT_TO_HIDDEN",
            "incremental_port_to_hidden_effect_identified": False,
            "hidden_return_learning": "OFF_ALL_CELLS",
            "topology_schedule_initial_state_resources": "FIXED_WITHIN_FAMILY_PAIR",
        },
        "dynamic_gate_definition": {
            "actual_hidden_spike_required": True,
            "distinct_source_id_required": True,
            "eligible_non_negative_edge_to_current_scheduled_visible_return_target_required": True,
            "observed_spike_to_return_lag_window_ms": [0.5, 6.5],
            "minimum_distinct_sources_same_return_clock": 2,
            "on_cell_must_complete_without_ceiling": True,
            "static_connectivity_or_nominal_time_alone_sufficient": False,
        },
        "measurement_schema": CELL_MEASUREMENT_FIELDS,
        "family_pairs": family_pairs,
        "family_count": len(family_pairs),
        "execution_cell_count": len(execution_cells),
        "complete_cell_ids": complete_cell_ids,
        "bounded_cell_ids": bounded_cell_ids,
        "gate_open_cell_ids": gate_open_cell_ids,
        "prohibited_update_count": sum(
            cell["prohibited_update_count"] for cell in execution_cells
        ),
        "new_edge_count": sum(cell["new_edge_count"] for cell in execution_cells),
        "matrix_status": (
            "REACHABLE_FOR_LATER_ANALYST_REVIEW"
            if gate_open_cell_ids
            else "D0_INCONCLUSIVE_BOUNDED_EXPLOSION"
            if bounded_cell_ids
            else "D0_COMPLETE_ZERO_DYNAMIC_ELIGIBLE_CLOCK"
        ),
        "later_e0_e1_es_authorized": False,
        "second_matrix_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "learner_boundary_change_authorized": False,
        "scientific_interpretation": (
            "development reachability diagnostic only; OFF/ON estimates the "
            "complete ordinary-learning package effect, not incremental "
            "PORT-to-hidden contribution; zero confirmatory credit; stop for "
            "fresh Analyst reconciliation"
        ),
        "next_action": "STOP_FOR_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    artifact["artifact_sha256"] = digest(artifact)
    return artifact


def score_capability(*args: object, **kwargs: object) -> None:
    raise v4.PreflightExecutionForbidden("capability scoring is not authorized")


def load_held_out(*args: object, **kwargs: object) -> None:
    raise v4.PreflightExecutionForbidden("held-out access is not authorized")


__all__ = [
    "ANALYST_ALLOCATION_ID",
    "ANALYST_ATTRIBUTION_ID",
    "ARMS",
    "CELL_MEASUREMENT_FIELDS",
    "FAMILIES",
    "OBJECT_ID",
    "PARENT_PREFLIGHT_HEAD",
    "PARENT_PREFLIGHT_TREE",
    "PORTS",
    "PROTOCOL_ID",
    "RD006Config",
    "build_execution_field",
    "clock_diagnostics",
    "development_worlds",
    "digest",
    "load_held_out",
    "run_execution_cell",
    "run_family_pair",
    "run_matrix",
    "score_capability",
]

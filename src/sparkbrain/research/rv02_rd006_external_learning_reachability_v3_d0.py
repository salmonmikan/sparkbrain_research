"""RD006 v3 bounded D0 result-bearing executor.

This module is intentionally separate from the v3 static-preflight module so
its fail-closed dynamic sentinels remain intact.  It implements only the
single 12-cell OFF/ON matrix authorized by Evidence Analyst R150 and the
actual-spike gate clarification in R151.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v3 as v3
from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology

PROTOCOL_ID = "rv02-rd006-external-learning-reachability-a-v3-d0-execution"
OBJECT_ID = v3.OBJECT_ID
PARENT_STATIC_PREFLIGHT_HEAD = "6b273e531c22729759cacabcced9df3319227a8e"
ANALYST_ALLOCATION_ID = "EVA-20260927T160005+0900-R150-RD006-V3-D0-MATRIX-ALLOCATION"
ANALYST_GATE_CLARIFICATION_ID = (
    "EVA-20260927T170004+0900-R151-RD006-V3-D0-DYNAMIC-GATE-CLARIFIED"
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


def _planned_edges(
    config: RD006Config, world: dict[str, Any], preflight: dict[str, Any]
) -> tuple[tuple[int, int], ...]:
    baseline = set(v1.build_topology(config, world))
    removed = {tuple(int(value) for value in edge) for edge in preflight["removed_edges"]}
    added = {tuple(int(value) for value in edge) for edge in preflight["added_edges"]}
    if not removed <= baseline:
        raise ValueError("v3 preflight removes an edge absent from the baseline")
    planned = tuple(sorted((baseline - removed) | added))
    if digest(planned) != preflight["planned_topology_sha256"]:
        raise ValueError("v3 planned topology does not match the static preflight")
    return planned


def build_execution_field(
    config: RD006Config, world: dict[str, Any], preflight: dict[str, Any]
) -> TemporalExcitableField:
    """Build the exact static-preflight topology without calling v3 sentinels."""

    config.validate()
    planned = _planned_edges(config, world, preflight)
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=config.threshold,
            )
            for unit_id in range(config.unit_count)
        ),
        tuple(
            Connection(
                source_id=source,
                target_id=target,
                weight=config.initial_weight,
                delay_ms=config.initial_delay_ms,
            )
            for source, target in planned
        ),
        receptor_ids=PORTS,
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=max(1.0, config.initial_delay_ms * 0.25),
        ),
    )
    field.config = replace(
        field.config,
        max_events_per_run=config.max_events_per_run,
        max_spikes_per_run=config.max_spikes_per_run,
    )
    for edge in field.connections.values():
        if edge.source_id in PORTS and edge.target_id not in PORTS:
            edge.weight *= config.boundary_gain
    return field


def _edge_class(source_id: int, target_id: int) -> str:
    source_role = "PORT" if source_id in PORTS else "HIDDEN"
    target_role = "PORT" if target_id in PORTS else "HIDDEN"
    return f"{source_role}_TO_{target_role}"


def clock_diagnostics(
    field: TemporalExcitableField,
    spikes: tuple[SpikeEvent, ...],
    *,
    return_unit_id: int,
    return_time_ms: float,
    config: RD006Config,
) -> dict[str, Any]:
    """Separate static connectivity from the R151 actual-spike dynamic gate."""

    structural_sources = []
    for source_id in sorted(set(range(config.unit_count)) - set(PORTS)):
        edge = field.connections.get((source_id, return_unit_id))
        if edge is None:
            continue
        structural_sources.append(
            {
                "source_id": source_id,
                "target_id": return_unit_id,
                "edge_weight": edge.weight,
                "edge_delay_ms": edge.delay_ms,
                "edge_plastic": edge.plastic,
                "edge_non_negative": edge.weight >= 0.0,
            }
        )

    spike_rows = []
    latest_eligible_by_source: dict[int, dict[str, Any]] = {}
    for spike in spikes:
        if spike.unit_id in PORTS:
            continue
        edge = field.connections.get((spike.unit_id, return_unit_id))
        lag_ms = return_time_ms - spike.time_ms
        lag_in_window = (
            config.minimum_return_lag_ms
            <= lag_ms
            <= config.maximum_return_lag_ms
        )
        edge_non_negative = edge is not None and edge.weight >= 0.0
        dynamically_eligible = edge_non_negative and lag_in_window
        row = {
            "source_id": spike.unit_id,
            "target_id": return_unit_id,
            "spike_time_ms": spike.time_ms,
            "return_time_ms": return_time_ms,
            "lag_ms": lag_ms,
            "lag_in_fixed_window": lag_in_window,
            "edge_exists": edge is not None,
            "edge_weight": edge.weight if edge is not None else None,
            "edge_delay_ms": edge.delay_ms if edge is not None else None,
            "edge_plastic": edge.plastic if edge is not None else None,
            "edge_non_negative": edge_non_negative,
            "dynamically_eligible": dynamically_eligible,
        }
        spike_rows.append(row)
        if dynamically_eligible:
            previous = latest_eligible_by_source.get(spike.unit_id)
            if previous is None or row["spike_time_ms"] > previous["spike_time_ms"]:
                latest_eligible_by_source[spike.unit_id] = row

    eligible = tuple(
        latest_eligible_by_source[source_id]
        for source_id in sorted(latest_eligible_by_source)
    )
    return {
        "structurally_connected_hidden_sources": tuple(structural_sources),
        "structurally_connected_hidden_source_count": len(structural_sources),
        "hidden_spike_diagnostics": tuple(spike_rows),
        "dynamic_eligible_hidden_sources": eligible,
        "dynamic_eligible_hidden_source_count": len(eligible),
        "dynamic_gate_ready": len(eligible) >= config.required_distinct_hidden_sources,
    }


def _classified_update(update: v1.PhysicalConnectionUpdate) -> dict[str, Any]:
    row = update.state_dict()
    row["source_role"] = "PORT" if update.source_id in PORTS else "HIDDEN"
    row["target_role"] = "PORT" if update.target_id in PORTS else "HIDDEN"
    row["edge_class"] = _edge_class(update.source_id, update.target_id)
    return row


def run_execution_cell(
    initial_state: dict[str, Any],
    schedule: tuple[dict[str, Any], ...],
    *,
    family: str,
    arm: str,
    config: RD006Config,
) -> dict[str, Any]:
    """Run one of the 12 fixed family/learning cells exactly once."""

    if arm not in ARMS:
        raise ValueError(f"unsupported RD006 arm: {arm}")
    field = TemporalExcitableField.from_state_dict(initial_state)
    learner = v1.ExternalOnlyPhysicalPlasticity(field) if arm == "external_learning_on" else None
    initial_connection_rows = v1.connection_rows(field)
    clocks: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []
    bounded_failure: dict[str, Any] | None = None

    for row in schedule:
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
                _classified_update(update) for update in learner.observe_external(pulse)
            )
        v1.schedule_external(
            field,
            event_id=str(row["event_id"]),
            time_ms=time_ms,
            unit_id=int(row["unit_id"]),
            magnitude=config.input_magnitude,
        )

    complete = bounded_failure is None and len(clocks) == len(schedule)
    selected_clock = next(
        (clock for clock in clocks if clock["dynamic_gate_ready"]),
        None,
    )
    gate_open = complete and selected_clock is not None
    final_connection_rows = v1.connection_rows(field)
    return {
        "execution_cell_id": f"rv02-rd006-v3-{family}-{arm}-scale-1",
        "family": family,
        "arm": arm,
        "ordinary_external_learning_enabled": learner is not None,
        "hidden_return_learning_enabled": False,
        "planned_clock_count": len(schedule),
        "inspected_clock_count": len(clocks),
        "complete_non_exploded": complete,
        "bounded_failure": bounded_failure,
        "initial_connection_sha256": digest(initial_connection_rows),
        "final_connection_sha256": digest(final_connection_rows),
        "final_connection_rows": final_connection_rows,
        "external_observation_count": (
            learner.external_observation_count if learner is not None else 0
        ),
        "ordinary_update_count": len(updates),
        "ordinary_update_edge_class_counts": {
            edge_class: sum(update["edge_class"] == edge_class for update in updates)
            for edge_class in sorted({update["edge_class"] for update in updates})
        },
        "ordinary_updates": tuple(updates),
        "hidden_return_update_count": 0,
        "inspected_clocks": tuple(clocks),
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
        "maximum_dynamic_eligible_hidden_sources_at_return": max(
            (clock["dynamic_eligible_hidden_source_count"] for clock in clocks),
            default=0,
        ),
        "selected_dynamic_gate_clock": selected_clock,
        "dynamic_gate_open": gate_open,
        "status": (
            "D0_REACHABLE_FOR_LATER_ANALYST_REVIEW"
            if gate_open
            else "D0_BOUNDED_INCOMPLETE"
            if bounded_failure is not None
            else "D0_COMPLETE_ZERO_DYNAMIC_ELIGIBLE_CLOCK"
        ),
    }


def run_family_pair(config: RD006Config, world: dict[str, Any]) -> dict[str, Any]:
    config.validate()
    if world["family"] not in FAMILIES or tuple(world["ports"]) != PORTS:
        raise ValueError("world is outside the fixed RD006 v3 fixture")
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
        )
        for arm in ARMS
    }
    if len({cell["initial_connection_sha256"] for cell in cells.values()}) != 1:
        raise RuntimeError("paired cells do not share identical initial connections")
    measured_clock_ids = {
        arm: tuple(
            clock["return_event_id"] for clock in cells[arm]["inspected_clocks"]
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
            "same_completed_measurement_clocks": len(set(measured_clock_ids.values())) == 1,
            "only_factor": "ordinary_external_learning_on_vs_off",
        },
        "execution_cells": cells,
    }


def run_matrix(source_git_sha: str) -> dict[str, Any]:
    """Execute the single prospectively fixed six-family/two-arm matrix."""

    v1.require_git_sha(source_git_sha)
    config = RD006Config()
    family_pairs = tuple(
        run_family_pair(config, world) for world in development_worlds(config)
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
        "parent_static_preflight_head": PARENT_STATIC_PREFLIGHT_HEAD,
        "analyst_allocation_id": ANALYST_ALLOCATION_ID,
        "analyst_gate_clarification_id": ANALYST_GATE_CLARIFICATION_ID,
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
            "hidden_return_learning": "OFF_ALL_CELLS",
            "topology_schedule_initial_state_resources": "FIXED_WITHIN_FAMILY_PAIR",
        },
        "dynamic_gate_definition": {
            "actual_hidden_spike_required": True,
            "distinct_source_id_required": True,
            "eligible_non_negative_edge_to_current_scheduled_visible_return_target_required": True,
            "observed_spike_to_return_lag_window_ms": [0.5, 6.5],
            "minimum_distinct_sources_same_return_clock": 2,
            "cell_must_complete_without_ceiling": True,
            "static_connectivity_or_nominal_time_alone_sufficient": False,
        },
        "family_pairs": family_pairs,
        "family_count": len(family_pairs),
        "execution_cell_count": len(execution_cells),
        "complete_cell_ids": complete_cell_ids,
        "bounded_cell_ids": bounded_cell_ids,
        "gate_open_cell_ids": gate_open_cell_ids,
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
            "development reachability diagnostic only; OFF/ON differences are "
            "diagnostic; zero confirmatory credit; stop for fresh Analyst reconciliation"
        ),
        "next_action": "STOP_FOR_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    artifact["artifact_sha256"] = digest(artifact)
    return artifact


__all__ = [
    "ANALYST_ALLOCATION_ID",
    "ANALYST_GATE_CLARIFICATION_ID",
    "ARMS",
    "FAMILIES",
    "OBJECT_ID",
    "PARENT_STATIC_PREFLIGHT_HEAD",
    "PORTS",
    "PROTOCOL_ID",
    "RD006Config",
    "build_execution_field",
    "clock_diagnostics",
    "development_worlds",
    "digest",
    "run_execution_cell",
    "run_family_pair",
    "run_matrix",
]

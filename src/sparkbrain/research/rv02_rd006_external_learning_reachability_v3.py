"""RD006 v3 structural-temporal role static preflight.

This revision is construction-only.  It builds and verifies a deterministic
topology/schedule contract without instantiating or running a Field.  Dynamic
entrypoints intentionally fail closed until fresh Evidence Analyst authority.
"""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v2 as v2

PROTOCOL_ID = (
    "rv02-rd006-external-learning-reachability-a-"
    "v3-structural-temporal-role-preflight"
)
OBJECT_ID = v1.OBJECT_ID
ANALYST_GENERATION_ID = "EVA-20260927T135700+0900-R149-RD006-V3-STATIC-PREFLIGHT"
PARENT_STATIC_AUDIT_HEAD = "cdb985e16dda2b38f7a0713e51992fa16f128ad5"
CONSTRUCTION_RULE_ID = "STATIC_PORT_HIDDEN_RETURN_CLOCK_V1"
DEVELOPMENT_PHASE = "OPEN_DEVELOPMENT"
EVIDENTIARY_STATUS = "DEVELOPMENT_CONSTRUCTION_ZERO_CONFIRMATORY_CREDIT"

FAMILIES = v1.FAMILIES
PORTS = v1.PORTS
RD006Config = v1.RD006Config
development_worlds = v1.development_worlds
digest = v1.digest


class DynamicsExecutionForbidden(RuntimeError):
    """Raised when a result-bearing entrypoint is invoked before authorization."""


def _forbid_dynamics(entrypoint: str) -> None:
    raise DynamicsExecutionForbidden(
        f"{entrypoint} is forbidden by the RD006 v3 static-preflight contract"
    )


def run_arm(*args: object, **kwargs: object) -> None:
    _forbid_dynamics("run_arm")


def run_cell(*args: object, **kwargs: object) -> None:
    _forbid_dynamics("run_cell")


def run_matrix(*args: object, **kwargs: object) -> None:
    _forbid_dynamics("run_matrix")


def build_initial_field(*args: object, **kwargs: object) -> None:
    _forbid_dynamics("build_initial_field")


def execute_topology(*args: object, **kwargs: object) -> None:
    _forbid_dynamics("execute_topology")


def declared_schedule(world: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    """Return the unchanged, prospectively declared v2 5.5 ms schedule."""

    return v2.training_schedule(world)


def _hidden_units(config: RD006Config) -> tuple[int, ...]:
    return tuple(sorted(set(range(config.unit_count)) - set(PORTS)))


def _ordered_transition_pairs(
    schedule: tuple[dict[str, Any], ...],
) -> tuple[tuple[dict[str, Any], dict[str, Any]], ...]:
    pairs = []
    for predecessor, return_row in zip(schedule, schedule[1:], strict=False):
        same_route_episode = (
            predecessor["route_index"],
            predecessor["episode"],
        ) == (return_row["route_index"], return_row["episode"])
        consecutive_position = (
            int(return_row["position"]) == int(predecessor["position"]) + 1
        )
        if same_route_episode and consecutive_position:
            pairs.append((predecessor, return_row))
    return tuple(
        sorted(
            pairs,
            key=lambda pair: (
                int(pair[1]["route_index"]),
                int(pair[1]["episode"]),
                int(pair[1]["position"]),
                int(pair[0]["unit_id"]),
                int(pair[1]["unit_id"]),
                str(pair[1]["event_id"]),
            ),
        )
    )


def _ordered_hidden_neighbors(
    *,
    predecessor_unit_id: int,
    baseline_edges: set[tuple[int, int]],
    hidden_units: tuple[int, ...],
    seed: int,
    family: str,
    return_unit_id: int,
) -> tuple[int, ...]:
    candidates = tuple(
        unit_id
        for unit_id in hidden_units
        if (predecessor_unit_id, unit_id) in baseline_edges
    )

    def role_key(unit_id: int) -> tuple[str, int]:
        return (
            digest(
                {
                    "construction_rule_id": CONSTRUCTION_RULE_ID,
                    "seed": seed,
                    "family": family,
                    "predecessor_unit_id": predecessor_unit_id,
                    "return_unit_id": return_unit_id,
                    "hidden_source_id": unit_id,
                }
            ),
            unit_id,
        )

    return tuple(sorted(candidates, key=role_key))


def _select_declared_clock(
    *,
    config: RD006Config,
    world: dict[str, Any],
    baseline_edges: set[tuple[int, int]],
    schedule: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    hidden_units = _hidden_units(config)
    for predecessor, return_row in _ordered_transition_pairs(schedule):
        predecessor_unit = int(predecessor["unit_id"])
        return_unit = int(return_row["unit_id"])
        sources = _ordered_hidden_neighbors(
            predecessor_unit_id=predecessor_unit,
            baseline_edges=baseline_edges,
            hidden_units=hidden_units,
            seed=config.seed,
            family=str(world["family"]),
            return_unit_id=return_unit,
        )
        nominal_hidden_time = float(predecessor["time_ms"]) + config.initial_delay_ms
        lag_ms = float(return_row["time_ms"]) - nominal_hidden_time
        if (
            len(sources) >= config.required_distinct_hidden_sources
            and config.minimum_return_lag_ms
            <= lag_ms
            <= config.maximum_return_lag_ms
        ):
            selected_sources = sources[: config.required_distinct_hidden_sources]
            return {
                "predecessor_event_id": str(predecessor["event_id"]),
                "predecessor_time_ms": float(predecessor["time_ms"]),
                "predecessor_unit_id": predecessor_unit,
                "return_event_id": str(return_row["event_id"]),
                "return_time_ms": float(return_row["time_ms"]),
                "return_unit_id": return_unit,
                "nominal_hidden_time_ms": nominal_hidden_time,
                "schedule_relation_lag_ms": lag_ms,
                "hidden_source_ids": list(selected_sources),
            }
    raise ValueError(
        f"no static two-source clock can be constructed for {world['family']}"
    )


def _build_planned_topology(
    *,
    config: RD006Config,
    world: dict[str, Any],
    baseline: tuple[tuple[int, int], ...],
    declared_clock: dict[str, Any],
) -> tuple[tuple[int, int], ...]:
    baseline_outgoing = {
        source: {target for edge_source, target in baseline if edge_source == source}
        for source in range(config.unit_count)
    }
    return_unit = int(declared_clock["return_unit_id"])
    assigned_sources = {int(source) for source in declared_clock["hidden_source_ids"]}
    hidden_units = set(_hidden_units(config))
    planned: list[tuple[int, int]] = []

    for source in range(config.unit_count):
        if source in PORTS:
            targets = set(baseline_outgoing[source])
        else:
            targets = {(source + 1) % config.unit_count}
            if source in assigned_sources:
                targets.add(return_unit)
            for target in sorted(baseline_outgoing[source]):
                if target != source and len(targets) < config.degree:
                    targets.add(target)
            for target in range(config.unit_count):
                if target != source and len(targets) < config.degree:
                    targets.add(target)
        if source not in hidden_units and targets != baseline_outgoing[source]:
            raise ValueError("port-source edges must remain unchanged")
        if len(targets) != config.degree:
            raise ValueError("v3 topology must preserve exact per-source out-degree")
        planned.extend((source, target) for target in sorted(targets))
    return tuple(planned)


def build_family_preflight(
    config: RD006Config, world: dict[str, Any]
) -> dict[str, Any]:
    """Construct and verify one family without executing Field dynamics."""

    config.validate()
    if world["family"] not in FAMILIES or tuple(world["ports"]) != PORTS:
        raise ValueError("world is outside the fixed RD006 family fixture")
    baseline = v1.build_topology(config, world)
    baseline_edges = set(baseline)
    schedule = declared_schedule(world)
    declared_clock = _select_declared_clock(
        config=config,
        world=world,
        baseline_edges=baseline_edges,
        schedule=schedule,
    )
    planned = _build_planned_topology(
        config=config,
        world=world,
        baseline=baseline,
        declared_clock=declared_clock,
    )
    planned_edges = set(planned)
    required_route_edges = {
        edge
        for route in world["routes"]
        for edge in zip(route, route[1:], strict=False)
    }
    hidden_ring_edges = {
        (source, (source + 1) % config.unit_count) for source in _hidden_units(config)
    }
    baseline_port_edges = {edge for edge in baseline_edges if edge[0] in PORTS}
    planned_port_edges = {edge for edge in planned_edges if edge[0] in PORTS}
    outdegree = Counter(source for source, _ in planned)
    source_paths = []
    for source in declared_clock["hidden_source_ids"]:
        source = int(source)
        first_edge = (int(declared_clock["predecessor_unit_id"]), source)
        second_edge = (source, int(declared_clock["return_unit_id"]))
        source_paths.append(
            {
                "hidden_source_id": source,
                "predecessor_to_hidden_edge": list(first_edge),
                "hidden_to_return_edge": list(second_edge),
                "predecessor_to_hidden_delay_ms": config.initial_delay_ms,
                "hidden_to_return_delay_ms": config.initial_delay_ms,
                "nominal_hidden_time_ms": declared_clock["nominal_hidden_time_ms"],
                "return_clock_lag_ms": declared_clock["schedule_relation_lag_ms"],
                "first_edge_present": first_edge in planned_edges,
                "second_edge_present": second_edge in planned_edges,
            }
        )

    invariants = {
        "unit_count": config.unit_count,
        "total_edge_count": len(planned),
        "mean_out_degree": len(planned) / config.unit_count,
        "all_source_outdegrees_exact": all(
            outdegree[source] == config.degree for source in range(config.unit_count)
        ),
        "port_source_edges_preserved": baseline_port_edges == planned_port_edges,
        "route_edges_preserved": required_route_edges <= planned_edges,
        "hidden_ring_edges_preserved": hidden_ring_edges <= planned_edges,
        "no_self_edges": all(source != target for source, target in planned),
        "distinct_hidden_source_count": len(
            set(int(source) for source in declared_clock["hidden_source_ids"])
        ),
        "all_static_path_edges_present": all(
            row["first_edge_present"] and row["second_edge_present"]
            for row in source_paths
        ),
        "all_declared_lags_in_fixed_window": all(
            config.minimum_return_lag_ms
            <= float(row["return_clock_lag_ms"])
            <= config.maximum_return_lag_ms
            for row in source_paths
        ),
        "all_hidden_to_return_edge_delays_in_fixed_window": all(
            config.minimum_return_lag_ms
            <= float(row["hidden_to_return_delay_ms"])
            <= config.maximum_return_lag_ms
            for row in source_paths
        ),
    }
    accepted = (
        invariants["total_edge_count"] == config.unit_count * config.degree
        and invariants["mean_out_degree"] == float(config.degree)
        and invariants["all_source_outdegrees_exact"]
        and invariants["port_source_edges_preserved"]
        and invariants["route_edges_preserved"]
        and invariants["hidden_ring_edges_preserved"]
        and invariants["no_self_edges"]
        and invariants["distinct_hidden_source_count"]
        >= config.required_distinct_hidden_sources
        and invariants["all_static_path_edges_present"]
        and invariants["all_declared_lags_in_fixed_window"]
        and invariants["all_hidden_to_return_edge_delays_in_fixed_window"]
    )
    if not accepted:
        raise ValueError(f"v3 static acceptance failed for {world['family']}")
    return {
        "family": str(world["family"]),
        "world_sha256": str(world["world_sha256"]),
        "baseline_topology_sha256": digest(baseline),
        "planned_topology_sha256": digest(planned),
        "declared_schedule_sha256": digest(schedule),
        "schedule_event_count": len(schedule),
        "declared_return_clock": declared_clock,
        "static_hidden_source_paths": source_paths,
        "added_edges": [list(edge) for edge in sorted(planned_edges - baseline_edges)],
        "removed_edges": [list(edge) for edge in sorted(baseline_edges - planned_edges)],
        "invariants": invariants,
        "static_acceptance": "PASS",
        "dynamic_reachability_claimed": False,
    }


def build_static_preflight() -> dict[str, Any]:
    """Build the complete six-family deterministic, non-result-bearing report."""

    config = RD006Config()
    families = [
        build_family_preflight(config, world) for world in development_worlds(config)
    ]
    report = {
        "schema_version": 1,
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "analyst_generation_id": ANALYST_GENERATION_ID,
        "parent_static_audit_head": PARENT_STATIC_AUDIT_HEAD,
        "construction_rule_id": CONSTRUCTION_RULE_ID,
        "development_phase": DEVELOPMENT_PHASE,
        "claim_ceiling": "SYSTEM",
        "evidentiary_status": EVIDENTIARY_STATUS,
        "configuration": config.state_dict(),
        "construction_inputs": [
            "fixed_seed",
            "family",
            "sorted_static_unit_roles",
            "declared_5.5ms_schedule",
            "fixed_5.0ms_edge_delay",
            "fixed_0.5_to_6.5ms_return_lag_window",
        ],
        "observed_spike_or_artifact_outcome_used": False,
        "new_dynamic_execution": False,
        "new_result_bearing_matrix": False,
        "capability_scoring": False,
        "held_out_use": False,
        "families": families,
        "family_count": len(families),
        "families_passing": sum(
            row["static_acceptance"] == "PASS" for row in families
        ),
        "static_preflight_status": "PASS",
        "v3_result_bearing_execution_authorized": False,
        "later_e0_e1_es_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "scientific_credit": 0,
        "interpretation": (
            "Construction reachability only: each family has one declared clock "
            "with two static hidden-source paths in the fixed lag window. This does "
            "not show that either source fires, returns visibly, learns, or improves "
            "capability."
        ),
        "next_action": "STOP_FOR_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    report["report_sha256"] = digest(report)
    return report


def serialize_static_preflight(report: dict[str, Any]) -> bytes:
    return (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def replay_static_preflight(payload: bytes) -> dict[str, Any]:
    report = json.loads(payload.decode("utf-8"))
    claimed = report.pop("report_sha256", None)
    computed = digest(report)
    if claimed != computed:
        raise ValueError("static preflight report digest mismatch")
    report["report_sha256"] = claimed
    if serialize_static_preflight(report) != payload:
        raise ValueError("static preflight serialization is not canonical")
    return report


__all__ = [
    "ANALYST_GENERATION_ID",
    "CONSTRUCTION_RULE_ID",
    "DEVELOPMENT_PHASE",
    "DynamicsExecutionForbidden",
    "EVIDENTIARY_STATUS",
    "FAMILIES",
    "OBJECT_ID",
    "PARENT_STATIC_AUDIT_HEAD",
    "PORTS",
    "PROTOCOL_ID",
    "RD006Config",
    "build_family_preflight",
    "build_initial_field",
    "build_static_preflight",
    "declared_schedule",
    "development_worlds",
    "execute_topology",
    "replay_static_preflight",
    "run_arm",
    "run_cell",
    "run_matrix",
    "serialize_static_preflight",
]

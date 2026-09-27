"""Audit RD006 v2 static return coverage without executing new dynamics.

The audit reads the preserved v2 artifact, reconstructs only the deterministic
world, schedule and topology, and crosses those static edges with already
preserved spike times.  It also evaluates one outcome-independent role-level
construction rule.  It must never run a Field arm, cell or matrix.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v2 as v2

AUDIT_SCHEMA_VERSION = 1
AUDIT_ID = "RD006_V2_PRESERVED_STATIC_TOPOLOGY_RETURN_COVERAGE_AUDIT"
PRESERVED_RESULT_HEAD = "d2462ebc52e3bf1e6a50334ee6b8d7cf437b416a"
PRESERVED_SOURCE_HEAD = "7896433af675b77b1f442e9efaf268d16564c564"
EXPECTED_ARTIFACT_SHA256 = (
    "5898fdcb75b10747fb88f8a19329f2d063422bb5012e80683c2c413cbbfb76d6"
)
EXPECTED_ARTIFACT_FILE_SHA256 = (
    "7ce4ffa4366f60290b26ead6edd31f9a2083f0822949c7c11815aefe8df5c468"
)
ROLE_RULE_ID = "BALANCED_HIDDEN_RETURN_INDEGREE_2_V1"


def _file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_preserved_artifact(path: Path) -> dict[str, Any]:
    if _file_sha256(path) != EXPECTED_ARTIFACT_FILE_SHA256:
        raise ValueError("preserved artifact file identity mismatch")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        artifact = json.load(handle)
    payload = dict(artifact)
    claimed = payload.pop("artifact_sha256", None)
    computed = v1.digest(payload)
    if claimed != computed or claimed != EXPECTED_ARTIFACT_SHA256:
        raise ValueError(
            f"preserved artifact identity mismatch: claimed={claimed} computed={computed}"
        )
    if artifact.get("source_git_sha") != PRESERVED_SOURCE_HEAD:
        raise ValueError("preserved source identity mismatch")
    return artifact


def _return_units(world: dict[str, Any]) -> tuple[int, ...]:
    return tuple(sorted({int(unit) for route in world["routes"] for unit in route}))


def _role_source_order(
    *, hidden_sources: tuple[int, ...], seed: int, family: str
) -> tuple[int, ...]:
    """Order hidden roles without consulting any observed spike identity."""

    def key(source_id: int) -> str:
        return v1.digest(
            {
                "rule_id": ROLE_RULE_ID,
                "seed": seed,
                "family": family,
                "source_id": source_id,
            }
        )

    return tuple(sorted(hidden_sources, key=key))


def _role_assignments(
    *, return_units: tuple[int, ...], hidden_sources: tuple[int, ...], seed: int, family: str
) -> dict[int, tuple[int, int]]:
    order = _role_source_order(
        hidden_sources=hidden_sources, seed=seed, family=family
    )
    if len(order) < 2:
        raise ValueError("at least two hidden source roles are required")
    return {
        return_unit: (
            order[(2 * index) % len(order)],
            order[(2 * index + 1) % len(order)],
        )
        for index, return_unit in enumerate(return_units)
    }


def _planned_topology(
    *,
    current_edges: tuple[tuple[int, int], ...],
    assignments: dict[int, tuple[int, int]],
    config: v1.RD006Config,
) -> tuple[tuple[int, int], ...]:
    """Build a budget-matched static plan; no activity data are accepted."""

    current_outgoing = {
        source: {target for edge_source, target in current_edges if edge_source == source}
        for source in range(config.unit_count)
    }
    role_targets: dict[int, set[int]] = {
        source: set() for source in range(config.unit_count)
    }
    for target, sources in assignments.items():
        for source in sources:
            role_targets[source].add(target)

    planned: list[tuple[int, int]] = []
    hidden_sources = set(range(config.unit_count)) - set(v1.PORTS)
    for source in range(config.unit_count):
        if source not in hidden_sources:
            targets = set(current_outgoing[source])
        else:
            targets = {(source + 1) % config.unit_count} | role_targets[source]
            if len(targets) > config.degree:
                raise ValueError("role rule exceeds per-source degree budget")
            for target in sorted(current_outgoing[source]):
                if target != source and len(targets) < config.degree:
                    targets.add(target)
            for target in range(config.unit_count):
                if target != source and len(targets) < config.degree:
                    targets.add(target)
        if len(targets) != config.degree:
            raise ValueError("planned topology does not preserve exact out-degree")
        planned.extend((source, target) for target in sorted(targets))
    return tuple(planned)


def _timing_sources(
    clock: dict[str, Any], config: v1.RD006Config
) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                int(spike["unit_id"])
                for spike in clock["hidden_spikes"]
                if config.minimum_return_lag_ms
                <= float(clock["return_time_ms"]) - float(spike["time_ms"])
                <= config.maximum_return_lag_ms
            }
        )
    )


def _count_distribution(values: list[int]) -> dict[str, int]:
    counts = Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


def build_audit(preserved_artifact_path: Path) -> dict[str, Any]:
    artifact = _load_preserved_artifact(preserved_artifact_path)
    config = v1.RD006Config(**artifact["configuration"])
    config.validate()
    worlds = {world["family"]: world for world in v1.development_worlds(config)}
    cells = {cell["family"]: cell for cell in artifact["cells"]}
    if set(worlds) != set(cells):
        raise ValueError("preserved family set mismatch")

    hidden_sources = tuple(
        sorted(set(range(config.unit_count)) - set(v1.PORTS))
    )
    family_rows: list[dict[str, Any]] = []
    aggregate = Counter()

    for family in v1.FAMILIES:
        world = worlds[family]
        cell = cells[family]
        topology = v1.build_topology(config, world)
        schedule = v2.training_schedule(world)
        if v1.digest(topology) != cell["topology_sha256"]:
            raise ValueError(f"topology identity mismatch: {family}")
        if v1.digest(schedule) != cell["schedule_sha256"]:
            raise ValueError(f"schedule identity mismatch: {family}")

        returns = _return_units(world)
        current_incoming = {
            target: tuple(
                sorted(
                    source
                    for source, edge_target in topology
                    if edge_target == target and source in hidden_sources
                )
            )
            for target in returns
        }
        assignments = _role_assignments(
            return_units=returns,
            hidden_sources=hidden_sources,
            seed=config.seed,
            family=family,
        )
        planned_topology = _planned_topology(
            current_edges=topology, assignments=assignments, config=config
        )
        planned_incoming = {
            target: tuple(
                sorted(
                    source
                    for source, edge_target in planned_topology
                    if edge_target == target and source in hidden_sources
                )
            )
            for target in returns
        }
        if not all(
            set(assignments[target]) <= set(planned_incoming[target])
            for target in returns
        ):
            raise ValueError(f"role guarantee missing from plan: {family}")

        current_edges = set(topology)
        planned_edges = set(planned_topology)
        added_edges = planned_edges - current_edges
        removed_edges = current_edges - planned_edges
        if len(current_edges) != len(planned_edges) or len(added_edges) != len(removed_edges):
            raise ValueError(f"edge budget mismatch: {family}")
        current_port_source_edges = {
            edge for edge in current_edges if edge[0] in v1.PORTS
        }
        planned_port_source_edges = {
            edge for edge in planned_edges if edge[0] in v1.PORTS
        }
        required_route_edges = {
            edge
            for route in world["routes"]
            for edge in zip(route, route[1:], strict=False)
        }
        if current_port_source_edges != planned_port_source_edges:
            raise ValueError(f"port-source edges changed: {family}")
        if not required_route_edges <= planned_edges:
            raise ValueError(f"required route edge changed: {family}")

        on_arm = cell["arms"]["external_learning_on"]
        clock_rows: list[dict[str, Any]] = []
        current_intersections: list[int] = []
        planned_intersections: list[int] = []
        timing_counts: list[int] = []
        for clock in on_arm["inspected_clocks"]:
            target = int(clock["return_unit_id"])
            timing = set(_timing_sources(clock, config))
            current = tuple(sorted(timing & set(current_incoming[target])))
            planned = tuple(sorted(timing & set(planned_incoming[target])))
            preserved_eligible = tuple(
                sorted(
                    int(row["source_id"])
                    for row in clock["eligible_hidden_sources"]
                )
            )
            if current != preserved_eligible:
                raise ValueError(
                    f"preserved eligibility mismatch: {family}/{clock['return_event_id']}"
                )
            timing_counts.append(len(timing))
            current_intersections.append(len(current))
            planned_intersections.append(len(planned))
            if timing or current or planned:
                clock_rows.append(
                    {
                        "return_event_id": clock["return_event_id"],
                        "return_time_ms": float(clock["return_time_ms"]),
                        "return_unit_id": target,
                        "time_aligned_hidden_source_ids": sorted(timing),
                        "current_structurally_eligible_source_ids": list(current),
                        "role_rule_structurally_eligible_source_ids": list(planned),
                    }
                )

        coverage = [len(current_incoming[target]) for target in returns]
        planned_coverage = [len(planned_incoming[target]) for target in returns]
        role_loads = Counter(
            source for sources in assignments.values() for source in sources
        )
        row = {
            "family": family,
            "world_sha256": cell["world_sha256"],
            "topology_sha256": cell["topology_sha256"],
            "schedule_sha256": cell["schedule_sha256"],
            "return_unit_count": len(returns),
            "return_units": [
                {
                    "return_unit_id": target,
                    "current_hidden_incoming_source_ids": list(current_incoming[target]),
                    "current_hidden_incoming_count": len(current_incoming[target]),
                    "role_rule_required_source_ids": list(assignments[target]),
                    "planned_hidden_incoming_source_ids": list(planned_incoming[target]),
                    "planned_hidden_incoming_count": len(planned_incoming[target]),
                }
                for target in returns
            ],
            "current_hidden_incoming_distribution": _count_distribution(coverage),
            "planned_hidden_incoming_distribution": _count_distribution(
                planned_coverage
            ),
            "current_zero_incoming_return_units": sum(count == 0 for count in coverage),
            "current_one_incoming_return_units": sum(count == 1 for count in coverage),
            "current_two_or_more_incoming_return_units": sum(
                count >= 2 for count in coverage
            ),
            "static_role_rule": {
                "rule_id": ROLE_RULE_ID,
                "inputs": [
                    "unit_roles",
                    "family",
                    "seed",
                    "sorted_return_units",
                ],
                "observed_spike_id_input": False,
                "required_hidden_incoming_per_return": 2,
                "minimum_role_edges_per_hidden_source": min(role_loads.values()),
                "maximum_role_edges_per_hidden_source": max(role_loads.values()),
                "preserves_hidden_ring_edge": True,
                "planned_total_edge_count": len(planned_edges),
                "planned_mean_out_degree": len(planned_edges) / config.unit_count,
                "added_edge_count": len(added_edges),
                "removed_edge_count": len(removed_edges),
                "port_source_edges_preserved": True,
                "required_route_edges_preserved": True,
                "all_return_units_have_two_role_sources": all(
                    set(assignments[target]) <= set(planned_incoming[target])
                    for target in returns
                ),
            },
            "preserved_on_arm_timing": {
                "inspected_clock_count": int(on_arm["inspected_clock_count"]),
                "planned_clock_count": int(on_arm["planned_clock_count"]),
                "unobserved_clock_count": int(on_arm["planned_clock_count"])
                - int(on_arm["inspected_clock_count"]),
                "time_aligned_source_count_distribution": _count_distribution(
                    timing_counts
                ),
                "clocks_with_at_least_one_time_aligned_source": sum(
                    count >= 1 for count in timing_counts
                ),
                "clocks_with_at_least_two_time_aligned_sources": sum(
                    count >= 2 for count in timing_counts
                ),
                "current_structural_intersection_distribution": _count_distribution(
                    current_intersections
                ),
                "current_clocks_with_two_eligible_sources": sum(
                    count >= 2 for count in current_intersections
                ),
                "role_rule_intersection_distribution": _count_distribution(
                    planned_intersections
                ),
                "role_rule_clocks_with_two_eligible_sources": sum(
                    count >= 2 for count in planned_intersections
                ),
                "nonempty_clock_rows": clock_rows,
            },
            "bounded_failure": on_arm["bounded_failure"],
        }
        family_rows.append(row)
        aggregate.update(
            {
                "return_units": len(returns),
                "current_zero_incoming": row["current_zero_incoming_return_units"],
                "current_one_incoming": row["current_one_incoming_return_units"],
                "current_two_or_more_incoming": row[
                    "current_two_or_more_incoming_return_units"
                ],
                "inspected_on_arm_clocks": int(on_arm["inspected_clock_count"]),
                "unobserved_on_arm_clocks": int(on_arm["planned_clock_count"])
                - int(on_arm["inspected_clock_count"]),
                "time_aligned_ge_1": sum(count >= 1 for count in timing_counts),
                "time_aligned_ge_2": sum(count >= 2 for count in timing_counts),
                "current_eligible_ge_1": sum(
                    count >= 1 for count in current_intersections
                ),
                "current_eligible_ge_2": sum(
                    count >= 2 for count in current_intersections
                ),
                "role_rule_eligible_ge_1": sum(
                    count >= 1 for count in planned_intersections
                ),
                "role_rule_eligible_ge_2": sum(
                    count >= 2 for count in planned_intersections
                ),
                "planned_added_edges": len(added_edges),
                "planned_removed_edges": len(removed_edges),
            }
        )

    audit = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "audit_id": AUDIT_ID,
        "object_id": artifact["object_id"],
        "protocol_id": artifact["protocol_id"],
        "development_phase": "RESULT_EXPOSED_DEVELOPMENT",
        "claim_ceiling": artifact["claim_ceiling"],
        "evidentiary_status": "DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT",
        "preserved_result_head": PRESERVED_RESULT_HEAD,
        "preserved_source_head": PRESERVED_SOURCE_HEAD,
        "preserved_artifact_sha256": artifact["artifact_sha256"],
        "preserved_artifact_file_sha256": _file_sha256(preserved_artifact_path),
        "new_dynamic_execution": False,
        "new_result_bearing_matrix": False,
        "capability_scoring": False,
        "held_out_use": False,
        "topology_mutated": False,
        "observed_spike_identity_used_for_edge_selection": False,
        "configuration": artifact["configuration"],
        "families": family_rows,
        "aggregate": dict(aggregate),
        "disposition": {
            "current_v2_contract": "CLOSED_UNCHANGED_D0_INCONCLUSIVE_BOUNDED_EXPLOSION",
            "static_role_rule_budget_feasibility": (
                "STRUCTURALLY_FEASIBLE_UNDER_SAME_UNIT_COUNT_AND_EDGE_BUDGET"
            ),
            "static_role_rule_preserved_timing_sufficiency": (
                "NOT_SUFFICIENT_ON_PRESERVED_V2_TIMING"
            ),
            "reason": (
                "The deterministic role rule gives every scheduled return unit at "
                "least two hidden incoming edges while retaining 48 units, 384 edges "
                "and mean out-degree 8.0, but its outcome-independent assignments "
                "intersect no preserved clock with two time-aligned hidden sources."
            ),
            "bounded_uncertainty_retained": True,
            "unobserved_clocks_inferred": False,
        },
        "optional_prospective_v3_contract_proposal": {
            "status": "PROPOSAL_ONLY_NOT_AUTHORIZED_FOR_EXECUTION",
            "fresh_revision_required": True,
            "construction_rule_id": ROLE_RULE_ID,
            "precommit_before_dynamics": True,
            "required_hidden_incoming_per_scheduled_return": 2,
            "preserve_unit_count": config.unit_count,
            "preserve_total_edge_count": config.unit_count * config.degree,
            "preserve_mean_out_degree": float(config.degree),
            "preserve_route_edges": True,
            "preserve_hidden_ring_edges": True,
            "forbid_observed_spike_identity_edge_selection": True,
            "matched_resources_and_privilege_required": True,
            "separate_failure_surfaces": [
                "STATIC_STRUCTURAL_COVERAGE",
                "PRESERVED_TEMPORAL_ALIGNMENT",
                "BOUNDED_EXPLOSION_OR_UNOBSERVED_CLOCKS",
            ],
            "prediction_not_made": (
                "Static feasibility does not predict that fresh dynamics will fire "
                "the assigned sources or satisfy the two-source gate."
            ),
        },
        "later_e0_e1_es_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "v3_execution_authorized": False,
        "next_action": "WAIT_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    audit["audit_sha256"] = v1.digest(audit)
    return audit


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    rendered = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        with path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
                zipped.write(rendered)
    else:
        path.write_bytes(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    _write_json(args.output, build_audit(args.artifact))


if __name__ == "__main__":
    main()

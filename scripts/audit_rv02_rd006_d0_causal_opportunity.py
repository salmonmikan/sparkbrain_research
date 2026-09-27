"""Audit preserved RD006 D0 bytes without executing new dynamics.

The audit reconstructs only the deterministic v1 topology/schedule and combines
them with the already-preserved attempt-002 clocks.  It must never call the D0
runtime, rescore capability, or infer clocks hidden by a bounded explosion.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
from typing import Any

from sparkbrain.research.rv02_rd006_external_learning_reachability import (
    ARMS,
    PORTS,
    RD006Config,
    build_topology,
    development_worlds,
    digest,
    training_schedule,
)

AUDIT_SCHEMA_VERSION = 1
AUDIT_ID = "RD006_D0_PRESERVED_CAUSAL_OPPORTUNITY_AUDIT"
PRESERVED_RESULT_HEAD = "49b91ca801522f3d6685ebd22097a1e64f9234c9"
PRESERVED_SOURCE_HEAD = "b4fbd9cc92f9e9d02f4ec1ff69084ab31f924b0c"
EXPECTED_ARTIFACT_SHA256 = (
    "c27951973b25a83ea3a23ce16b97e6634ac513929aee605c8af417410e12209c"
)


def _edge_class(source_id: int, target_id: int) -> str:
    source_port = source_id in PORTS
    target_port = target_id in PORTS
    if source_port and target_port:
        return "PORT_TO_PORT"
    if source_port:
        return "PORT_TO_HIDDEN"
    if target_port:
        return "HIDDEN_TO_PORT"
    return "HIDDEN_TO_HIDDEN"


def _distance_to_window(lag_ms: float, minimum_ms: float, maximum_ms: float) -> float:
    if lag_ms < minimum_ms:
        return minimum_ms - lag_ms
    if lag_ms > maximum_ms:
        return lag_ms - maximum_ms
    return 0.0


def _load_preserved_artifact(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        artifact = json.load(handle)
    claimed = artifact.get("artifact_sha256")
    payload = dict(artifact)
    payload.pop("artifact_sha256", None)
    computed = digest(payload)
    if claimed != computed or claimed != EXPECTED_ARTIFACT_SHA256:
        raise ValueError(
            f"preserved artifact identity mismatch: claimed={claimed} computed={computed}"
        )
    return artifact


def _audit_clock(
    clock: dict[str, Any],
    *,
    structural_sources: tuple[int, ...],
    config: RD006Config,
) -> dict[str, Any]:
    structural_spikes = [
        spike
        for spike in clock["hidden_spikes"]
        if int(spike["unit_id"]) in structural_sources
    ]
    timing_rows = []
    for spike in structural_spikes:
        lag_ms = float(clock["return_time_ms"]) - float(spike["time_ms"])
        timing_rows.append(
            {
                "source_id": int(spike["unit_id"]),
                "spike_time_ms": float(spike["time_ms"]),
                "lag_ms": lag_ms,
                "distance_to_fixed_window_ms": _distance_to_window(
                    lag_ms,
                    config.minimum_return_lag_ms,
                    config.maximum_return_lag_ms,
                ),
            }
        )
    timing_rows.sort(
        key=lambda row: (
            row["distance_to_fixed_window_ms"],
            abs(row["lag_ms"]),
            row["source_id"],
            row["spike_time_ms"],
        )
    )
    eligible_sources = sorted(
        {
            int(row["source_id"])
            for row in timing_rows
            if row["distance_to_fixed_window_ms"] == 0.0
        }
    )
    if not structural_sources:
        failure_class = "NO_STRUCTURAL_RETURN_EDGE"
    elif not structural_spikes:
        failure_class = "STRUCTURAL_EDGE_NO_HIDDEN_SPIKE"
    elif not eligible_sources:
        failure_class = "HIDDEN_SPIKE_OUTSIDE_LAG"
    elif len(eligible_sources) == 1:
        failure_class = "ELIGIBLE_SINGLE_SOURCE_ONLY"
    else:
        failure_class = "ELIGIBLE_MULTI_SOURCE"
    return {
        "return_event_id": clock["return_event_id"],
        "return_time_ms": float(clock["return_time_ms"]),
        "return_unit_id": int(clock["return_unit_id"]),
        "structural_hidden_return_source_ids": list(structural_sources),
        "structural_hidden_return_edge_count": len(structural_sources),
        "observed_structurally_connected_hidden_spike_count": len(structural_spikes),
        "eligible_structural_hidden_source_ids": eligible_sources,
        "nearest_structurally_connected_hidden_spike": (
            timing_rows[0] if timing_rows else None
        ),
        "failure_class": failure_class,
    }


def build_audit(preserved_artifact_path: Path) -> dict[str, Any]:
    artifact = _load_preserved_artifact(preserved_artifact_path)
    if artifact.get("source_git_sha") != PRESERVED_SOURCE_HEAD:
        raise ValueError(
            "preserved source identity mismatch: "
            f"{artifact.get('source_git_sha')} != {PRESERVED_SOURCE_HEAD}"
        )
    config = RD006Config(**artifact["configuration"])
    config.validate()
    worlds = {world["family"]: world for world in development_worlds(config)}
    cells_by_family = {cell["family"]: cell for cell in artifact["cells"]}
    if set(worlds) != set(cells_by_family):
        raise ValueError("preserved artifact family set does not match v1 source")
    cell_audits = []
    aggregate_failure_classes: dict[str, int] = {}
    global_nearest: dict[str, Any] | None = None

    for family in worlds:
        world = worlds[family]
        cell = cells_by_family[family]
        topology = build_topology(config, world)
        if digest(topology) != cell["topology_sha256"]:
            raise ValueError(f"topology identity mismatch for {family}")
        schedule = training_schedule(world)
        if digest(schedule) != cell["schedule_sha256"]:
            raise ValueError(f"schedule identity mismatch for {family}")

        hidden_sources_by_target = {
            target: tuple(
                sorted(
                    source
                    for source, edge_target in topology
                    if edge_target == target and source not in PORTS
                )
            )
            for target in PORTS
        }
        scheduled_units = {int(row["unit_id"]) for row in schedule}
        if not scheduled_units <= set(PORTS):
            raise ValueError(f"non-port external target in preserved schedule: {family}")
        topology_class_counts = {
            name: 0
            for name in (
                "PORT_TO_PORT",
                "PORT_TO_HIDDEN",
                "HIDDEN_TO_PORT",
                "HIDDEN_TO_HIDDEN",
            )
        }
        directly_updatable_class_counts = dict.fromkeys(topology_class_counts, 0)
        for source, target in topology:
            name = _edge_class(source, target)
            topology_class_counts[name] += 1
            if source in scheduled_units and target in scheduled_units:
                directly_updatable_class_counts[name] += 1

        arms = []
        for arm_name in ARMS:
            arm = cell["arms"][arm_name]
            clock_rows = []
            class_counts: dict[str, int] = {}
            nearest: dict[str, Any] | None = None
            for clock in arm["inspected_clocks"]:
                target = int(clock["return_unit_id"])
                audited = _audit_clock(
                    clock,
                    structural_sources=hidden_sources_by_target[target],
                    config=config,
                )
                clock_rows.append(audited)
                name = audited["failure_class"]
                class_counts[name] = class_counts.get(name, 0) + 1
                aggregate_failure_classes[name] = (
                    aggregate_failure_classes.get(name, 0) + 1
                )
                candidate = audited["nearest_structurally_connected_hidden_spike"]
                if candidate is not None:
                    enriched = {
                        "family": family,
                        "arm": arm_name,
                        "return_event_id": audited["return_event_id"],
                        "return_time_ms": audited["return_time_ms"],
                        "return_unit_id": audited["return_unit_id"],
                        **candidate,
                    }
                    order = (
                        enriched["distance_to_fixed_window_ms"],
                        abs(enriched["lag_ms"]),
                        enriched["source_id"],
                        enriched["return_time_ms"],
                    )
                    if nearest is None or order < nearest["_order"]:
                        nearest = {"_order": order, **enriched}
                    if global_nearest is None or order < global_nearest["_order"]:
                        global_nearest = {"_order": order, **enriched}

            bounded = arm["bounded_failure"]
            bounded_row = None
            if bounded is not None:
                target = int(bounded["return_unit_id"])
                bounded_row = {
                    "return_event_id": bounded["return_event_id"],
                    "return_time_ms": float(bounded["return_time_ms"]),
                    "return_unit_id": target,
                    "structural_hidden_return_source_ids": list(
                        hidden_sources_by_target[target]
                    ),
                    "structural_hidden_return_edge_count": len(
                        hidden_sources_by_target[target]
                    ),
                    "failure_class": "BOUNDED_EXPLOSION_BEFORE_DECISION",
                    "unobserved_clock_count": (
                        int(arm["planned_clock_count"])
                        - int(arm["inspected_clock_count"])
                    ),
                }
                aggregate_failure_classes["BOUNDED_EXPLOSION_BEFORE_DECISION"] = (
                    aggregate_failure_classes.get(
                        "BOUNDED_EXPLOSION_BEFORE_DECISION", 0
                    )
                    + 1
                )
            actual_update_class_counts: dict[str, int] = {}
            for update in arm["ordinary_updates"]:
                name = _edge_class(
                    int(update["source_id"]), int(update["target_id"])
                )
                actual_update_class_counts[name] = (
                    actual_update_class_counts.get(name, 0) + 1
                )
            if nearest is not None:
                nearest.pop("_order")
            arms.append(
                {
                    "arm": arm_name,
                    "inspected_clock_count": int(arm["inspected_clock_count"]),
                    "planned_clock_count": int(arm["planned_clock_count"]),
                    "failure_class_counts": class_counts,
                    "nearest_structurally_connected_hidden_spike": nearest,
                    "bounded_failure_clock": bounded_row,
                    "pre_ceiling_causal_opportunity": {
                        "structural_return_edge_observed": any(
                            row["structural_hidden_return_edge_count"] > 0
                            for row in clock_rows
                        ),
                        "eligible_single_or_multi_source_observed": any(
                            row["failure_class"]
                            in {
                                "ELIGIBLE_SINGLE_SOURCE_ONLY",
                                "ELIGIBLE_MULTI_SOURCE",
                            }
                            for row in clock_rows
                        ),
                        "eligible_multi_source_observed": any(
                            row["failure_class"] == "ELIGIBLE_MULTI_SOURCE"
                            for row in clock_rows
                        ),
                    },
                    "actual_ordinary_update_class_counts": actual_update_class_counts,
                    "clock_audit": clock_rows,
                }
            )

        cell_audits.append(
            {
                "family": family,
                "world_sha256": cell["world_sha256"],
                "topology_sha256": cell["topology_sha256"],
                "schedule_sha256": cell["schedule_sha256"],
                "topology_edge_class_counts": topology_class_counts,
                "ordinary_external_learner_directly_updatable_edge_class_counts": (
                    directly_updatable_class_counts
                ),
                "arms": arms,
            }
        )

    if global_nearest is not None:
        global_nearest.pop("_order")
    audit = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "audit_id": AUDIT_ID,
        "object_id": artifact["object_id"],
        "protocol_id": artifact["protocol_id"],
        "development_phase": "RESULT_EXPOSED_DEVELOPMENT",
        "claim_ceiling": artifact["claim_ceiling"],
        "evidentiary_status": "DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT",
        "preserved_result_head": PRESERVED_RESULT_HEAD,
        "preserved_source_git_sha": artifact["source_git_sha"],
        "preserved_artifact_sha256": artifact["artifact_sha256"],
        "new_dynamic_execution": False,
        "execution_procedure_nonconformance": {
            "observed": True,
            "class": "NON_PERSISTED_LOCAL_DYNAMIC_UNIT_TEST_INVOCATION",
            "command_scope": (
                "tests/test_rv02_rd006_external_learning_reachability.py"
            ),
            "used_for_audit": False,
            "persisted_as_scientific_output": False,
            "preserved_v1_mutated": False,
            "follow_up": "DISCLOSE_TO_EVIDENCE_ANALYST_AND_DO_NOT_REPEAT",
        },
        "new_seed": False,
        "parameter_change": False,
        "capability_scoring": False,
        "held_out_use": False,
        "fixed_lag_window_ms": [
            config.minimum_return_lag_ms,
            config.maximum_return_lag_ms,
        ],
        "aggregate_failure_class_counts": aggregate_failure_classes,
        "global_nearest_structurally_connected_hidden_spike": global_nearest,
        "ordinary_external_learner_contract": {
            "trace_population": "EXTERNALLY_SCHEDULED_PORTS_ONLY",
            "directly_updatable_edge_classes": ["PORT_TO_PORT"],
            "port_to_hidden_direct_update_possible": False,
            "hidden_to_port_direct_update_possible": False,
            "hidden_to_hidden_direct_update_possible": False,
        },
        "cells": cell_audits,
        "v1_result_changed": False,
        "v1_result": artifact["matrix_status"],
        "later_e0_e1_es_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "prospective_revision_authorized": False,
        "next_action": "WAIT_FRESH_EVIDENCE_ANALYST_RECONCILIATION",
    }
    audit["audit_sha256"] = digest(audit)
    return audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    audit = build_audit(args.artifact)
    rendered = json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()

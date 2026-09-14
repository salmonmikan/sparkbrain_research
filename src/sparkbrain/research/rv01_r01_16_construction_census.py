"""One-shot construction-only contrast census for prospective RV01 R01-16.

This stage trains the fixed fresh development worlds only far enough to retain
pre/post physical connection inventories and outcome-blind reachability
certificates.  It never schedules a capability cue, runs a probe, emits a task
trace, scores an endpoint, or opens held-out/formal authority.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .rv01.interference_runner import _INITIAL_WEIGHT, _directed_edges, _train_route
from .rv01.physical_learner_bridge import build_physical_field
from .rv01_r01_16_development_package import (
    R0116DevelopmentPackagePlan,
    R0116SourceManifest,
)
from .rv01_r01_16_factorization import ConnectionState, R01_16FactorizationConstruction
from .rv01_r01_16_reachability import build_factor_reachability_certificate
from .rv01_r01_16_retained_history import build_retained_history_snapshot
from .rv01_r01_16_source_binding import verify_r01_16_source_checkout
from .rv01_r01_16_worlds import development_world_grid, development_world_grid_hash

_CENSUS_SCHEMA = "rv01-r01-16-construction-census-v1"


def _connection_inventory(field: Any) -> tuple[ConnectionState, ...]:
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


def _queue_is_empty(field: Any) -> bool:
    queue = field.state_dict().get("queue", ())
    return len(queue) == 0


def _world_construction_record(world: Any) -> dict[str, object]:
    route_by_id = {route.route_id: route for route in world.routes}
    field = build_physical_field(
        unit_count=world.unit_count,
        directed_edges=_directed_edges(world),
        threshold=world.threshold,
        initial_weight=_INITIAL_WEIGHT,
        initial_delay_ms=world.lag_ms,
    )
    if not _queue_is_empty(field):
        raise RuntimeError("R01-16 fresh field unexpectedly contains queued propagation")
    pre_training = _connection_inventory(field)

    training_rows: list[dict[str, object]] = []
    api_hashes: set[str] = set()
    for phase_index, route_id in enumerate(world.training_order, start=1):
        accepted, ignored, api = _train_route(
            world,
            field,
            route_by_id[route_id],
            phase_index=phase_index,
        )
        api_hashes.add(api.api_hash)
        training_rows.append(
            {
                "phase_index": phase_index,
                "route_id": route_id,
                "accepted_observation_count": accepted,
                "ignored_observation_count": ignored,
                "learner_api_hash": api.api_hash,
            }
        )
    if len(api_hashes) != 1:
        raise RuntimeError("R01-16 learner API changed inside one construction world")
    if not _queue_is_empty(field):
        raise RuntimeError(
            "R01-16 queue-integrity gate failed: training left queued propagation"
        )

    post_training = _connection_inventory(field)
    construction = R01_16FactorizationConstruction(
        pre_training=pre_training,
        post_training=post_training,
        queued_propagation=(),
    )
    summary = construction.summary()

    cells: list[dict[str, object]] = []
    for route_id in world.probe_order:
        route = route_by_id[route_id]
        certificate = build_factor_reachability_certificate(
            construction,
            registered_unit_ids=tuple(range(world.unit_count)),
            cue_source_ids=(route.units[0],),
            probe_horizon_ms=world.probe_horizon_ms(route),
        )
        cells.append(
            {
                "probe_route_id": route_id,
                "cue_source_ids": [route.units[0]],
                "probe_horizon_ms": world.probe_horizon_ms(route),
                "reachability_certificate_sha256": certificate.sha256,
                "reachability_certificate": certificate.state_dict(),
            }
        )

    return {
        "world": world.state_dict(),
        "world_specification_sha256": world.specification_hash(),
        "learner_api_hash": next(iter(api_hashes)),
        "training": training_rows,
        "pre_training": [row.state_dict() for row in pre_training],
        "post_training": [row.state_dict() for row in post_training],
        "factorization_summary": {
            "protocol_id": summary.protocol_id,
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
        "cells": cells,
        "capability_output_opened": False,
        "probe_executed": False,
        "held_out_capability_executed": False,
        "formal_execution_allowed": False,
    }


def _summarize(worlds: list[dict[str, object]]) -> dict[str, object]:
    weight_worlds: set[str] = set()
    delay_worlds: set[str] = set()
    combined_worlds: set[str] = set()
    weight_cells = 0
    delay_cells = 0
    combined_cells = 0
    zero_contrast_worlds = 0

    for row in worlds:
        world = row["world"]
        if not isinstance(world, dict):
            raise TypeError("R01-16 retained world record must be an object")
        world_id = str(world["world_id"])
        factorization = row["factorization_summary"]
        if not isinstance(factorization, dict):
            raise TypeError("R01-16 factorization summary must be an object")
        if not factorization["weight_changed_edges"] and not factorization["delay_changed_edges"]:
            zero_contrast_worlds += 1
        cells = row["cells"]
        if not isinstance(cells, list):
            raise TypeError("R01-16 construction cells must be a list")
        for cell in cells:
            if not isinstance(cell, dict):
                raise TypeError("R01-16 construction cell must be an object")
            certificate = cell["reachability_certificate"]
            if not isinstance(certificate, dict):
                raise TypeError("R01-16 reachability certificate must be an object")
            if certificate["weight_eligible"]:
                weight_cells += 1
                weight_worlds.add(world_id)
            if certificate["delay_eligible"]:
                delay_cells += 1
                delay_worlds.add(world_id)
            if certificate["combined_eligible"]:
                combined_cells += 1
                combined_worlds.add(world_id)

    return {
        "world_count": len(worlds),
        "planned_cell_count": sum(len(row["cells"]) for row in worlds),
        "zero_contrast_world_count": zero_contrast_worlds,
        "weight_eligible_cell_count": weight_cells,
        "delay_eligible_cell_count": delay_cells,
        "combined_eligible_cell_count": combined_cells,
        "weight_eligible_world_count": len(weight_worlds),
        "delay_eligible_world_count": len(delay_worlds),
        "combined_eligible_world_count": len(combined_worlds),
        "weight_reachability_replication_ready": len(weight_worlds) >= 2,
        "delay_reachability_replication_ready": len(delay_worlds) >= 2,
        "combined_reachability_replication_ready": len(combined_worlds) >= 2,
    }


def run_construction_census(
    *,
    repo_root: Path,
    source_manifest: R0116SourceManifest,
) -> Path:
    """Consume one construction-only package identity and retain its full census."""

    root = repo_root.resolve(strict=True)
    source_manifest.validate()
    verified_source = verify_r01_16_source_checkout(root, source_manifest)
    retained = build_retained_history_snapshot(root)
    registry = retained.to_collision_registry()
    plan = R0116DevelopmentPackagePlan(
        source_manifest=source_manifest,
        collision_registry=registry,
    )
    plan.validate()
    world_grid_sha256 = development_world_grid_hash()
    worlds = development_world_grid()

    output_dir = root / plan.output_relpath
    if output_dir.exists():
        raise FileExistsError(
            f"refusing to reuse consumed R01-16 construction identity: {output_dir}"
        )
    output_dir.mkdir(parents=True, exist_ok=False)
    started = {
        "schema": _CENSUS_SCHEMA,
        "status": "STARTED_CONSTRUCTION_ONLY",
        "protocol_id": "rv01-r01-16-propagation-factorization-v1",
        "run_id": plan.run_id,
        "package_plan_sha256": plan.package_plan_sha256,
        "source_git_sha": source_manifest.source_git_sha,
        "source_manifest_sha256": source_manifest.manifest_sha256,
        "collision_registry_sha256": registry.registry_sha256,
        "world_grid_sha256": world_grid_sha256,
        "python_version": sys.version,
        "capability_output_opened": False,
        "probe_executed": False,
        "same_identity_rerun_allowed": False,
    }
    (output_dir / "STARTED.json").write_text(
        json.dumps(started, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    try:
        world_rows = [_world_construction_record(world) for world in worlds]
        summary = _summarize(world_rows)
        status = (
            "CONSTRUCTION_CENSUS_COMPLETE_CAPABILITY_UNOPENED"
            if summary["combined_eligible_world_count"]
            else "CONSTRUCTION_CENSUS_TERMINAL_ZERO_ELIGIBLE_WORLDS"
        )
        payload = {
            "schema": _CENSUS_SCHEMA,
            "status": status,
            "protocol_id": "rv01-r01-16-propagation-factorization-v1",
            "run_id": plan.run_id,
            "package_plan": plan.state_dict(),
            "package_plan_sha256": plan.package_plan_sha256,
            "source_binding": verified_source.state_dict(),
            "source_manifest": source_manifest.state_dict(),
            "retained_history": retained.state_dict(),
            "collision_registry": registry.state_dict(),
            "world_grid_sha256": world_grid_sha256,
            "summary": summary,
            "worlds": world_rows,
            "python_executable": sys.executable,
            "python_version": sys.version,
            "capability_output_opened": False,
            "probe_executed": False,
            "held_out_capability_executed": False,
            "formal_execution_allowed": False,
            "same_identity_rerun_allowed": False,
        }
        (output_dir / "construction_census.json").write_text(
            json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "COMPLETE.json").write_text(
            json.dumps(
                {
                    "schema": _CENSUS_SCHEMA,
                    "status": status,
                    "run_id": plan.run_id,
                    "summary": summary,
                    "capability_output_opened": False,
                    "probe_executed": False,
                    "same_identity_rerun_allowed": False,
                },
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        (output_dir / "FAILED.json").write_text(
            json.dumps(
                {
                    "schema": _CENSUS_SCHEMA,
                    "status": "CONSTRUCTION_CENSUS_FAILED_TERMINAL_FOR_THIS_IDENTITY",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "same_identity_rerun_allowed": False,
                    "capability_output_opened": False,
                    "probe_executed": False,
                },
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        raise

    return output_dir


__all__ = ["run_construction_census"]

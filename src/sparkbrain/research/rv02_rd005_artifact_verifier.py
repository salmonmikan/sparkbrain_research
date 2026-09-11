"""Independent fail-closed verifier for RD005 construction artifacts.

This module is deliberately separate from construction. It reconstructs the
prospective hidden-return gate from retained artifact rows and refuses future
capability eligibility unless every D1_READY cell contains the complete,
mutually consistent gate evidence fixed by the preregistration.

It additionally regenerates the fixed topology and initial gained connection
state from the registered world/scale identity. A retained self-hash is never
accepted as topology/connection provenance by itself.

It runs no learner or probe and grants no formal/held-out authority.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict
from typing import Any

from .rv02_rd003_online import _new_gained_field
from .rv02_rd005_construction_artifact import (
    RD005_FRESH_SEED,
    RD005_RETURN_OFFSET_MS,
    InspectedClock,
    RD005ConstructionArtifact,
    RD005ConstructionCell,
)
from .rv02_rd005_gate_construction import (
    ConnectionSnapshot,
    EligibilityEvent,
    ExternalReturnEvent,
    RD005GateConstruction,
)
from .rv02_recruitment import PORTS
from .rv02_scale import ScaleStudyConfig, audit_scale, development_worlds, digest


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _connection_snapshots(cell: RD005ConstructionCell) -> tuple[ConnectionSnapshot, ...]:
    rows: list[ConnectionSnapshot] = []
    for row in cell.connection_rows:
        required = {"source_id", "target_id", "plastic", "weight"}
        if not required.issubset(row):
            raise ValueError("RD005 retained connection row is incomplete")
        if type(row["source_id"]) is not int or type(row["target_id"]) is not int:
            raise TypeError("RD005 retained connection IDs must be integers")
        if type(row["plastic"]) is not bool:
            raise TypeError("RD005 retained connection plastic flag must be boolean")
        weight = row["weight"]
        if isinstance(weight, bool) or not isinstance(weight, int | float):
            raise TypeError("RD005 retained connection weight must be numeric")
        if not math.isfinite(float(weight)):
            raise ValueError("RD005 retained connection weight must be finite")
        rows.append(
            ConnectionSnapshot(
                source_id=row["source_id"],
                target_id=row["target_id"],
                plastic=row["plastic"],
                initial_weight=float(weight),
            )
        )
    if not rows:
        raise ValueError("RD005 non-failure cell requires retained connection rows")
    return tuple(rows)


def _authoritative_connection_rows(
    config: ScaleStudyConfig,
    world: dict[str, Any],
    scale: int,
) -> tuple[dict[str, Any], ...]:
    """Regenerate the pre-training gained connection state without running dynamics."""

    field = _new_gained_field(config, world, scale)
    return tuple(asdict(edge) for _, edge in sorted(field.connections.items()))


def _certificate_states(rows: tuple[object, ...]) -> tuple[dict[str, object], ...]:
    states: list[dict[str, object]] = []
    for row in rows:
        state_dict = getattr(row, "state_dict", None)
        if not callable(state_dict):
            raise TypeError("RD005 certificate does not expose state_dict")
        states.append(state_dict())
    return tuple(states)


def _spike_identity(spike: dict[str, Any]) -> str:
    return _canonical_sha256(spike)


def _selected_batch_from_retained_clock(
    *,
    clock: InspectedClock,
    connections: tuple[ConnectionSnapshot, ...],
) -> tuple[tuple[dict[str, Any], int], ...]:
    return_time_ms = float(clock.time_ms) + RD005_RETURN_OFFSET_MS
    visible_targets: dict[int, tuple[int, ...]] = {}
    for edge in connections:
        if edge.target_id not in PORTS or not edge.plastic or edge.initial_weight < 0.0:
            continue
        visible_targets.setdefault(edge.source_id, tuple())
        visible_targets[edge.source_id] = tuple(
            sorted({*visible_targets[edge.source_id], edge.target_id})
        )

    by_source: dict[int, list[dict[str, Any]]] = {}
    for spike in clock.spikes:
        if "unit_id" not in spike or "time_ms" not in spike:
            raise ValueError("RD005 retained spike is missing unit/time identity")
        if type(spike["unit_id"]) is not int:
            raise TypeError("RD005 retained spike unit_id must be an integer")
        source_id = spike["unit_id"]
        if source_id in PORTS or source_id not in visible_targets:
            continue
        time_ms = spike["time_ms"]
        if isinstance(time_ms, bool) or not isinstance(time_ms, int | float):
            raise TypeError("RD005 retained spike time_ms must be numeric")
        if not math.isfinite(float(time_ms)):
            raise ValueError("RD005 retained spike time_ms must be finite")
        lag = return_time_ms - float(time_ms)
        if 0.5 <= lag <= 6.5:
            by_source.setdefault(source_id, []).append(spike)

    selected: list[tuple[dict[str, Any], int]] = []
    for source_id in sorted(by_source):
        spike = max(
            by_source[source_id],
            key=lambda row: (float(row["time_ms"]), _spike_identity(row)),
        )
        selected.append((spike, min(visible_targets[source_id])))
    if len(selected) < 2:
        return ()
    return tuple(selected)


def _derive_gate_from_retained_trace(
    cell: RD005ConstructionCell,
    connections: tuple[ConnectionSnapshot, ...],
) -> tuple[
    float | None,
    tuple[EligibilityEvent, ...],
    tuple[ExternalReturnEvent, ...],
    tuple[tuple[int, int], ...],
]:
    schedule_times = tuple(float(row["time_ms"]) for row in cell.ordinary_schedule)
    inspected_times = tuple(float(row.time_ms) for row in cell.inspected_clocks)
    if inspected_times != schedule_times[: len(inspected_times)]:
        raise ValueError("RD005 inspected clocks are not the retained schedule prefix")

    for index, clock in enumerate(cell.inspected_clocks):
        selected = _selected_batch_from_retained_clock(
            clock=clock,
            connections=connections,
        )
        if not selected:
            continue
        if index != len(cell.inspected_clocks) - 1:
            raise ValueError("RD005 retained trace continued after the first qualifying batch")
        return_time_ms = float(clock.time_ms) + RD005_RETURN_OFFSET_MS
        eligibility: list[EligibilityEvent] = []
        returns: list[ExternalReturnEvent] = []
        for ordinal, (spike, target_id) in enumerate(selected):
            suffix = _spike_identity(spike)[:16]
            eligibility_id = (
                f"rd005-eligibility:{cell.family}:{cell.scale}:{ordinal}:{suffix}"
            )
            eligibility.append(
                EligibilityEvent(
                    event_id=eligibility_id,
                    observed_source_id=int(spike["unit_id"]),
                    time_ms=float(spike["time_ms"]),
                )
            )
            returns.append(
                ExternalReturnEvent(
                    event_id=(
                        f"rd005-return:{cell.family}:{cell.scale}:{ordinal}:{suffix}"
                    ),
                    eligibility_event_id=eligibility_id,
                    target_id=int(target_id),
                    time_ms=return_time_ms,
                    outcome_blind=True,
                )
            )
        sources = tuple(sorted(row.observed_source_id for row in eligibility))
        mapping = tuple(
            (source, sources[(ordinal + 1) % len(sources)])
            for ordinal, source in enumerate(sources)
        )
        return (
            float(clock.time_ms),
            tuple(eligibility),
            tuple(returns),
            mapping,
        )

    if len(cell.inspected_clocks) != len(cell.ordinary_schedule):
        raise ValueError("RD005 no-gate trace does not cover the complete retained schedule")
    return None, (), (), ()


def _event_states(rows: tuple[object, ...]) -> tuple[dict[str, object], ...]:
    return tuple(asdict(row) for row in rows)


def verify_rd005_construction_cell(cell: RD005ConstructionCell) -> None:
    """Verify one retained cell as future-capability input, without executing it."""

    cell.validate()
    if cell.status == "CONSTRUCTION_INTEGRITY_FAILURE":
        return

    connections = _connection_snapshots(cell)
    selected_clock, eligibility, returns, mapping = _derive_gate_from_retained_trace(
        cell,
        connections,
    )
    expected_status = "D1_READY" if selected_clock is not None else "D1_UNREACHABLE"
    if cell.status != expected_status:
        raise ValueError("RD005 cell status does not match retained deterministic gate trace")
    if cell.error is not None:
        raise ValueError("RD005 non-failure cell must not carry an integrity error")

    if expected_status == "D1_UNREACHABLE":
        if cell.selected_clock_ms is not None:
            raise ValueError("RD005 unreachable cell cannot select a gate clock")
        if any(
            (
                cell.eligibility_events,
                cell.return_events,
                cell.es_assignment,
                cell.e1_certificates,
                cell.es_certificates,
            )
        ):
            raise ValueError("RD005 unreachable cell cannot retain ready-only gate evidence")
        return

    if cell.selected_clock_ms != selected_clock:
        raise ValueError("RD005 selected clock does not match retained deterministic trace")
    if _event_states(cell.eligibility_events) != _event_states(eligibility):
        raise ValueError("RD005 eligibility events do not reconstruct from retained spikes")
    if _event_states(cell.return_events) != _event_states(returns):
        raise ValueError("RD005 return events do not reconstruct from retained spikes")
    if cell.es_assignment != mapping:
        raise ValueError("RD005 ES assignment does not reconstruct from retained spikes")
    if not cell.e1_certificates or not cell.es_certificates:
        raise ValueError("RD005 D1_READY cell requires retained E1/ES certificates")

    gate = RD005GateConstruction(
        eligibility_events=eligibility,
        return_events=returns,
        connections=connections,
        shuffled_assignment=dict(mapping),
    )
    gate.assert_development_matrix_reachable()

    expected_e1 = _certificate_states(gate.certificates("E1"))
    expected_es = _certificate_states(gate.certificates("ES"))
    actual_e1 = _certificate_states(cell.e1_certificates)
    actual_es = _certificate_states(cell.es_certificates)
    if actual_e1 != expected_e1:
        raise ValueError("RD005 retained E1 certificates do not reconstruct from artifact inputs")
    if actual_es != expected_es:
        raise ValueError("RD005 retained ES certificates do not reconstruct from artifact inputs")


def _verify_fixed_matrix_identity(artifact: RD005ConstructionArtifact) -> None:
    config = ScaleStudyConfig(seed=RD005_FRESH_SEED)
    config.validate()
    expected_rows: list[
        tuple[str, str, int, str, str, str, str, str]
    ] = []
    for world in development_worlds(config):
        for scale in config.scales:
            world_id = str(world["world_id"])
            audit = audit_scale(config, world, scale)
            authoritative_connections = _authoritative_connection_rows(config, world, scale)
            expected_rows.append(
                (
                    f"{world_id}|scale={scale}",
                    str(world["family"]),
                    int(scale),
                    world_id,
                    digest(world),
                    str(world["evidence_hash"]),
                    str(audit["topology_hash"]),
                    digest(authoritative_connections),
                )
            )

    if len(artifact.cells) != len(expected_rows):
        raise ValueError("RD005 artifact does not match the exact preregistered 18-cell matrix")

    for cell, expected in zip(artifact.cells, expected_rows, strict=True):
        base_actual = (
            cell.cell_id,
            cell.family,
            cell.scale,
            cell.world_id,
            cell.world_sha256,
            cell.evidence_sha256,
        )
        if base_actual != expected[:6]:
            raise ValueError("RD005 artifact does not match the exact preregistered 18-cell matrix")
        if cell.status == "CONSTRUCTION_INTEGRITY_FAILURE":
            continue
        if cell.topology_sha256 != expected[6]:
            raise ValueError("RD005 topology hash does not match authoritative regeneration")
        if cell.connection_rows_sha256 != expected[7]:
            raise ValueError("RD005 connection state does not match authoritative regeneration")


def verify_rd005_artifact_for_future_capability(
    artifact: RD005ConstructionArtifact,
) -> tuple[str, ...]:
    """Return the exact capability-cell inventory only after independent verification."""

    artifact.validate()
    _verify_fixed_matrix_identity(artifact)
    for cell in artifact.cells:
        verify_rd005_construction_cell(cell)
    if any(cell.status == "CONSTRUCTION_INTEGRITY_FAILURE" for cell in artifact.cells):
        return ()
    ready = tuple(cell.cell_id for cell in artifact.cells if cell.status == "D1_READY")
    if not ready:
        return ()
    return ready


__all__ = [
    "verify_rd005_artifact_for_future_capability",
    "verify_rd005_construction_cell",
]

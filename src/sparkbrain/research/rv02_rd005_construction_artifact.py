"""Construction-only RD005 fresh D1 artifact builder.

The builder regenerates the fixed 18-cell fresh matrix at seed 92505 and inspects
only ordinary pre-capability Field dynamics. It never instantiates the RD005
learner, runs a probe, computes route correctness, or opens formal/held-out
authority.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Literal

from sparkbrain.research.rv02_rd003_online import (
    _new_gained_field,
    _schedule_external,
    _training_schedule,
)
from sparkbrain.research.rv02_rd005_gate_construction import (
    ConnectionSnapshot,
    EligibilityEvent,
    ExternalReturnEvent,
    GateReachabilityCertificate,
    RD005GateConstruction,
    RD005_PROTOCOL_ID,
)
from sparkbrain.research.rv02_recruitment import PORTS
from sparkbrain.research.rv02_scale import (
    ScaleStudyConfig,
    audit_scale,
    development_worlds,
    digest,
)
from sparkbrain.v04.contracts import SpikeEvent

RD005_PLAN_ID = "rv02-rd005-planned-matrix-92505-v1"
RD005_FRESH_SEED = 92505
RD005_RETURN_OFFSET_MS = 1.0
RD005CellStatus = Literal[
    "D1_READY",
    "D1_UNREACHABLE",
    "CONSTRUCTION_INTEGRITY_FAILURE",
]


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_git_sha(value: str) -> None:
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError("source_git_sha must be a 40-character lowercase Git SHA")


@dataclass(frozen=True, slots=True)
class SeedCollisionRecord:
    """Explicit pre-D1 fresh-identity collision search record."""

    seed: int
    searched_seed_ids: tuple[int, ...]
    searched_world_ids: tuple[str, ...]

    def validate(self) -> None:
        if self.seed != RD005_FRESH_SEED:
            raise ValueError("RD005 collision record is bound to seed 92505")
        if not self.searched_seed_ids or not self.searched_world_ids:
            raise ValueError("RD005 requires an explicit non-empty collision search record")
        if self.seed in self.searched_seed_ids:
            raise ValueError("RD005 fresh seed collides with a prior registered seed")
        token = f":{self.seed}:"
        if any(token in world_id for world_id in self.searched_world_ids):
            raise ValueError("RD005 fresh world namespace collides with a prior world identity")

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "seed": self.seed,
            "searched_seed_ids": list(self.searched_seed_ids),
            "searched_world_ids": list(self.searched_world_ids),
            "collision_found": False,
            "search_record_sha256": _canonical_sha256(
                {
                    "seed": self.seed,
                    "searched_seed_ids": list(self.searched_seed_ids),
                    "searched_world_ids": list(self.searched_world_ids),
                }
            ),
        }


@dataclass(frozen=True, slots=True)
class InspectedClock:
    time_ms: float
    spikes: tuple[dict[str, Any], ...]

    def state_dict(self) -> dict[str, object]:
        if not math.isfinite(float(self.time_ms)):
            raise ValueError("inspected clock must be finite")
        return {"time_ms": float(self.time_ms), "spikes": list(self.spikes)}


@dataclass(frozen=True, slots=True)
class RD005ConstructionCell:
    cell_id: str
    family: str
    scale: int
    world_id: str
    world_sha256: str
    evidence_sha256: str
    topology_sha256: str
    ordinary_schedule_sha256: str
    connection_rows_sha256: str
    inspected_clocks: tuple[InspectedClock, ...]
    selected_clock_ms: float | None
    eligibility_events: tuple[EligibilityEvent, ...]
    return_events: tuple[ExternalReturnEvent, ...]
    es_assignment: tuple[tuple[int, int], ...]
    e1_certificates: tuple[GateReachabilityCertificate, ...]
    es_certificates: tuple[GateReachabilityCertificate, ...]
    status: RD005CellStatus
    error: str | None = None

    def state_dict(self) -> dict[str, object]:
        return {
            "cell_id": self.cell_id,
            "family": self.family,
            "scale": self.scale,
            "world_id": self.world_id,
            "world_sha256": self.world_sha256,
            "evidence_sha256": self.evidence_sha256,
            "topology_sha256": self.topology_sha256,
            "ordinary_schedule_sha256": self.ordinary_schedule_sha256,
            "connection_rows_sha256": self.connection_rows_sha256,
            "inspected_clocks": [row.state_dict() for row in self.inspected_clocks],
            "selected_clock_ms": self.selected_clock_ms,
            "eligibility_events": [asdict(row) for row in self.eligibility_events],
            "return_events": [asdict(row) for row in self.return_events],
            "es_assignment": [list(row) for row in self.es_assignment],
            "e1_certificates": [row.state_dict() for row in self.e1_certificates],
            "es_certificates": [row.state_dict() for row in self.es_certificates],
            "status": self.status,
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class RD005ConstructionArtifact:
    source_git_sha: str
    collision_search: SeedCollisionRecord
    cells: tuple[RD005ConstructionCell, ...]

    def validate(self) -> None:
        _require_git_sha(self.source_git_sha)
        self.collision_search.validate()
        if len(self.cells) != 18:
            raise ValueError("RD005 construction artifact must retain exactly 18 cells")
        identities = tuple(row.cell_id for row in self.cells)
        if len(set(identities)) != 18:
            raise ValueError("RD005 construction cell identities must be unique")

    @property
    def matrix_status(self) -> str:
        self.validate()
        if any(row.status == "CONSTRUCTION_INTEGRITY_FAILURE" for row in self.cells):
            return "CONSTRUCTION_INTEGRITY_FAILURE"
        if not any(row.status == "D1_READY" for row in self.cells):
            return "D1_ZERO_READY_STOP"
        return "D1_CONSTRUCTION_READY"

    @property
    def future_capability_cell_ids(self) -> tuple[str, ...]:
        if self.matrix_status != "D1_CONSTRUCTION_READY":
            return ()
        return tuple(row.cell_id for row in self.cells if row.status == "D1_READY")

    def state_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "protocol_id": RD005_PROTOCOL_ID,
            "plan_id": RD005_PLAN_ID,
            "source_git_sha": self.source_git_sha,
            "fresh_seed": RD005_FRESH_SEED,
            "formal_execution_allowed": False,
            "held_out_capability_allowed": False,
            "collision_search": self.collision_search.state_dict(),
            "cells": [row.state_dict() for row in self.cells],
            "matrix_status": self.matrix_status,
            "future_capability_cell_ids": list(self.future_capability_cell_ids),
        }

    @property
    def artifact_sha256(self) -> str:
        return _canonical_sha256(self.state_dict())


def _connection_rows(field: Any) -> tuple[dict[str, Any], ...]:
    return tuple(asdict(edge) for _, edge in sorted(field.connections.items()))


def _connection_snapshots(field: Any) -> tuple[ConnectionSnapshot, ...]:
    return tuple(
        ConnectionSnapshot(
            source_id=int(edge.source_id),
            target_id=int(edge.target_id),
            plastic=bool(edge.plastic),
            initial_weight=float(edge.weight),
        )
        for _, edge in sorted(field.connections.items())
    )


def _spike_identity(spike: SpikeEvent) -> str:
    return _canonical_sha256(spike.as_dict())


def _selected_batch(
    *,
    spikes: tuple[SpikeEvent, ...],
    return_time_ms: float,
    connections: tuple[ConnectionSnapshot, ...],
) -> tuple[tuple[SpikeEvent, int], ...]:
    visible_targets: dict[int, tuple[int, ...]] = {}
    for edge in connections:
        if edge.target_id not in PORTS or not edge.plastic or edge.initial_weight < 0.0:
            continue
        visible_targets.setdefault(edge.source_id, tuple())
        visible_targets[edge.source_id] = tuple(
            sorted({*visible_targets[edge.source_id], edge.target_id})
        )

    by_source: dict[int, list[SpikeEvent]] = {}
    for spike in spikes:
        if spike.unit_id in PORTS or spike.unit_id not in visible_targets:
            continue
        lag = return_time_ms - float(spike.time_ms)
        if 0.5 <= lag <= 6.5:
            by_source.setdefault(int(spike.unit_id), []).append(spike)

    selected: list[tuple[SpikeEvent, int]] = []
    for source in sorted(by_source):
        spike = max(
            by_source[source],
            key=lambda row: (float(row.time_ms), _spike_identity(row)),
        )
        selected.append((spike, min(visible_targets[source])))
    if len(selected) < 2:
        return ()
    return tuple(selected)


def _rotation(sources: tuple[int, ...]) -> dict[int, int]:
    if len(sources) < 2:
        raise ValueError("RD005 ES rotation requires at least two hidden sources")
    return {
        source: sources[(index + 1) % len(sources)]
        for index, source in enumerate(sources)
    }


def _construct_cell(
    config: ScaleStudyConfig,
    world: dict[str, Any],
    scale: int,
) -> RD005ConstructionCell:
    audit = audit_scale(config, world, scale)
    field = _new_gained_field(config, world, scale)
    connections = _connection_snapshots(field)
    connection_rows = _connection_rows(field)
    schedule = _training_schedule(world)
    inspected: list[InspectedClock] = []

    for row in schedule:
        clock = float(row["time_ms"])
        spikes = tuple(field.run_until(clock))
        inspected.append(
            InspectedClock(
                time_ms=clock,
                spikes=tuple(spike.as_dict() for spike in spikes if spike.unit_id not in PORTS),
            )
        )
        return_time = clock + RD005_RETURN_OFFSET_MS
        selected = _selected_batch(
            spikes=spikes,
            return_time_ms=return_time,
            connections=connections,
        )
        if selected:
            eligibility: list[EligibilityEvent] = []
            returns: list[ExternalReturnEvent] = []
            for ordinal, (spike, target_id) in enumerate(selected):
                suffix = _spike_identity(spike)[:16]
                eligibility_id = (
                    f"rd005-eligibility:{world['family']}:{scale}:{ordinal}:{suffix}"
                )
                eligibility.append(
                    EligibilityEvent(
                        event_id=eligibility_id,
                        observed_source_id=int(spike.unit_id),
                        time_ms=float(spike.time_ms),
                    )
                )
                returns.append(
                    ExternalReturnEvent(
                        event_id=(
                            f"rd005-return:{world['family']}:{scale}:{ordinal}:{suffix}"
                        ),
                        eligibility_event_id=eligibility_id,
                        target_id=int(target_id),
                        time_ms=return_time,
                        outcome_blind=True,
                    )
                )
            sources = tuple(sorted(row.observed_source_id for row in eligibility))
            mapping = _rotation(sources)
            gate = RD005GateConstruction(
                eligibility_events=tuple(eligibility),
                return_events=tuple(returns),
                connections=connections,
                shuffled_assignment=mapping,
            )
            gate.assert_development_matrix_reachable()
            return RD005ConstructionCell(
                cell_id=f"{world['world_id']}|scale={scale}",
                family=str(world["family"]),
                scale=scale,
                world_id=str(world["world_id"]),
                world_sha256=digest(world),
                evidence_sha256=str(world["evidence_hash"]),
                topology_sha256=str(audit["topology_hash"]),
                ordinary_schedule_sha256=digest(schedule),
                connection_rows_sha256=digest(connection_rows),
                inspected_clocks=tuple(inspected),
                selected_clock_ms=clock,
                eligibility_events=tuple(eligibility),
                return_events=tuple(returns),
                es_assignment=tuple(sorted(mapping.items())),
                e1_certificates=gate.certificates("E1"),
                es_certificates=gate.certificates("ES"),
                status="D1_READY",
            )

        _schedule_external(
            field,
            event_id=f"rd005-plan-{int(row['ordinal']):06d}",
            time_ms=clock,
            unit_id=int(row["unit_id"]),
        )

    return RD005ConstructionCell(
        cell_id=f"{world['world_id']}|scale={scale}",
        family=str(world["family"]),
        scale=scale,
        world_id=str(world["world_id"]),
        world_sha256=digest(world),
        evidence_sha256=str(world["evidence_hash"]),
        topology_sha256=str(audit["topology_hash"]),
        ordinary_schedule_sha256=digest(schedule),
        connection_rows_sha256=digest(connection_rows),
        inspected_clocks=tuple(inspected),
        selected_clock_ms=None,
        eligibility_events=(),
        return_events=(),
        es_assignment=(),
        e1_certificates=(),
        es_certificates=(),
        status="D1_UNREACHABLE",
    )


def build_rd005_construction_artifact(
    *,
    source_git_sha: str,
    collision_search: SeedCollisionRecord,
) -> RD005ConstructionArtifact:
    """Construct all 18 fresh D1 cells without opening RD005 capability."""

    _require_git_sha(source_git_sha)
    collision_search.validate()
    config = ScaleStudyConfig(seed=RD005_FRESH_SEED)
    config.validate()
    cells: list[RD005ConstructionCell] = []
    for world in development_worlds(config):
        for scale in config.scales:
            try:
                cell = _construct_cell(config, world, scale)
            except Exception as exc:  # preserve integrity failures as data
                audit = audit_scale(config, world, scale)
                field = _new_gained_field(config, world, scale)
                schedule = _training_schedule(world)
                connection_rows = _connection_rows(field)
                cell = RD005ConstructionCell(
                    cell_id=f"{world['world_id']}|scale={scale}",
                    family=str(world["family"]),
                    scale=scale,
                    world_id=str(world["world_id"]),
                    world_sha256=digest(world),
                    evidence_sha256=str(world["evidence_hash"]),
                    topology_sha256=str(audit["topology_hash"]),
                    ordinary_schedule_sha256=digest(schedule),
                    connection_rows_sha256=digest(connection_rows),
                    inspected_clocks=(),
                    selected_clock_ms=None,
                    eligibility_events=(),
                    return_events=(),
                    es_assignment=(),
                    e1_certificates=(),
                    es_certificates=(),
                    status="CONSTRUCTION_INTEGRITY_FAILURE",
                    error=f"{type(exc).__name__}: {exc}",
                )
            cells.append(cell)
    artifact = RD005ConstructionArtifact(
        source_git_sha=source_git_sha,
        collision_search=collision_search,
        cells=tuple(cells),
    )
    artifact.validate()
    return artifact


__all__ = [
    "InspectedClock",
    "RD005ConstructionArtifact",
    "RD005ConstructionCell",
    "RD005_FRESH_SEED",
    "RD005_PLAN_ID",
    "SeedCollisionRecord",
    "build_rd005_construction_artifact",
]

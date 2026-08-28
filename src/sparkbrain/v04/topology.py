from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class UnitState:
    unit_id: int
    x: float
    y: float
    excitatory: bool = True
    potential: float = 0.0
    base_threshold: float = 1.0
    adaptation: float = 0.0
    refractory_until_ms: float = 0.0
    last_update_ms: float = 0.0
    last_spike_ms: float | None = None
    spike_count: int = 0
    source_pulse_ids: tuple[str, ...] = ()
    novelty_trace: float = 0.0
    prediction_error_trace: float = 0.0
    excitatory_drive: float = 0.0
    inhibitory_drive: float = 0.0


@dataclass(slots=True)
class Connection:
    source_id: int
    target_id: int
    weight: float
    delay_ms: float
    plastic: bool = True


@dataclass(frozen=True, slots=True)
class FieldTopology:
    units: tuple[UnitState, ...]
    connections: tuple[Connection, ...]
    receptor_ids: tuple[int, ...]


def _distance(a: UnitState, b: UnitState) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def grid_topology(
    *,
    width: int = 8,
    height: int = 8,
    receptor_rows: int = 1,
    local_radius: float = 1.5,
    excitatory_fraction: float = 0.8,
    base_weight: float = 0.34,
    inhibitory_weight: float = -0.72,
    base_delay_ms: float = 1.0,
    conduction_ms_per_unit: float = 1.4,
    long_range_edges_per_unit: int = 1,
    seed: int = 41,
) -> FieldTopology:
    if width < 2 or height < 2:
        raise ValueError("width and height must be at least 2")
    if not 0 < excitatory_fraction <= 1:
        raise ValueError("excitatory_fraction must be in (0, 1]")
    rng = random.Random(seed)
    units: list[UnitState] = []
    for y in range(height):
        for x in range(width):
            unit_id = y * width + x
            excitatory = rng.random() < excitatory_fraction
            threshold = 0.52 if y < receptor_rows else 0.80
            units.append(
                UnitState(
                    unit_id=unit_id,
                    x=float(x),
                    y=float(y),
                    excitatory=excitatory,
                    base_threshold=threshold,
                )
            )

    connections: dict[tuple[int, int], Connection] = {}
    for source in units:
        neighbors = [
            target
            for target in units
            if target.unit_id != source.unit_id and _distance(source, target) <= local_radius
        ]
        for target in neighbors:
            distance = max(_distance(source, target), 0.1)
            sign_weight = base_weight if source.excitatory else inhibitory_weight
            weight = sign_weight / max(1.0, distance)
            delay = base_delay_ms + conduction_ms_per_unit * distance
            connections[(source.unit_id, target.unit_id)] = Connection(
                source_id=source.unit_id,
                target_id=target.unit_id,
                weight=weight,
                delay_ms=delay,
            )

        candidates = [target for target in units if target.unit_id != source.unit_id]
        rng.shuffle(candidates)
        for target in candidates[:long_range_edges_per_unit]:
            distance = max(_distance(source, target), 0.1)
            sign_weight = 0.65 * (base_weight if source.excitatory else inhibitory_weight)
            connections[(source.unit_id, target.unit_id)] = Connection(
                source_id=source.unit_id,
                target_id=target.unit_id,
                weight=sign_weight,
                delay_ms=base_delay_ms + conduction_ms_per_unit * distance,
            )

    receptor_ids = tuple(
        unit.unit_id for unit in units if int(unit.y) < min(receptor_rows, height)
    )
    return FieldTopology(
        units=tuple(units),
        connections=tuple(connections.values()),
        receptor_ids=receptor_ids,
    )


def explicit_topology(
    units: Iterable[UnitState],
    connections: Iterable[Connection],
    *,
    receptor_ids: Iterable[int],
) -> FieldTopology:
    unit_rows = tuple(units)
    ids = {unit.unit_id for unit in unit_rows}
    if len(ids) != len(unit_rows):
        raise ValueError("unit IDs must be unique")
    connection_rows = tuple(connections)
    for edge in connection_rows:
        if edge.source_id not in ids or edge.target_id not in ids:
            raise ValueError("connection references an unknown unit")
        if edge.delay_ms <= 0:
            raise ValueError("connection delay must be positive")
    receptors = tuple(receptor_ids)
    if not set(receptors).issubset(ids):
        raise ValueError("receptor_ids must reference known units")
    return FieldTopology(unit_rows, connection_rows, receptors)

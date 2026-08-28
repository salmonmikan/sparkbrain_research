from __future__ import annotations

import math
import random

from sparkbrain.v04.topology import Connection, FieldTopology, UnitState, explicit_topology


def layered_reservoir_topology(
    *,
    receptor_count: int = 16,
    reservoir_width: int = 8,
    reservoir_height: int = 6,
    seed: int = 505,
) -> FieldTopology:
    """Generic receptor-to-reservoir topology with no semantic wiring.

    Receptors receive no recurrent input, so an external pulse has a stable
    first Spark representation.  Reservoir connectivity is local and seeded;
    channel identities are still mapped by the v0.4 stable hash router.
    """

    if receptor_count < 4:
        raise ValueError("receptor_count must be at least 4")
    if reservoir_width < 2 or reservoir_height < 2:
        raise ValueError("reservoir dimensions must be at least 2")
    rng = random.Random(seed)
    units: list[UnitState] = []
    for index in range(receptor_count):
        units.append(
            UnitState(
                unit_id=index,
                x=float(index),
                y=0.0,
                excitatory=True,
                base_threshold=0.46,
            )
        )
    reservoir_start = receptor_count
    reservoir_ids: list[int] = []
    for y in range(reservoir_height):
        for x in range(reservoir_width):
            unit_id = reservoir_start + y * reservoir_width + x
            reservoir_ids.append(unit_id)
            units.append(
                UnitState(
                    unit_id=unit_id,
                    x=float(x) * 1.7,
                    y=float(y) + 2.0,
                    excitatory=rng.random() < 0.82,
                    base_threshold=0.76,
                )
            )

    connections: list[Connection] = []
    # Every receptor projects to a generic, deterministic fanout in the reservoir.
    for receptor_id in range(receptor_count):
        for offset in (0, 7, 19):
            target = reservoir_ids[(receptor_id * 11 + offset) % len(reservoir_ids)]
            connections.append(
                Connection(
                    receptor_id,
                    target,
                    0.47,
                    1.0 + (offset % 5) * 0.8,
                    plastic=True,
                )
            )

    coords = {
        unit.unit_id: (unit.x, unit.y)
        for unit in units
        if unit.unit_id >= reservoir_start
    }
    for source_id in reservoir_ids:
        sx, sy = coords[source_id]
        source = units[source_id]
        candidates = []
        for target_id in reservoir_ids:
            if source_id == target_id:
                continue
            tx, ty = coords[target_id]
            distance = math.hypot(sx - tx, sy - ty)
            if distance <= 2.5:
                candidates.append((distance, target_id))
        candidates.sort(key=lambda row: (row[0], row[1]))
        for distance, target_id in candidates[:5]:
            weight = 0.24 / max(1.0, distance) if source.excitatory else -0.56 / max(1.0, distance)
            connections.append(
                Connection(
                    source_id,
                    target_id,
                    weight,
                    1.0 + 0.9 * distance,
                    plastic=True,
                )
            )
        # One long-range seeded edge per reservoir unit.
        target_id = reservoir_ids[rng.randrange(len(reservoir_ids))]
        if target_id != source_id:
            weight = 0.16 if source.excitatory else -0.38
            connections.append(
                Connection(
                    source_id,
                    target_id,
                    weight,
                    4.0 + rng.random() * 6.0,
                    plastic=True,
                )
            )

    return explicit_topology(
        units,
        connections,
        receptor_ids=tuple(range(receptor_count)),
    )

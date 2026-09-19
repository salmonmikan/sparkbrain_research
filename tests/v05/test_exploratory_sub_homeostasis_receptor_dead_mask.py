from __future__ import annotations

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v05 import HomeostaticController


def _spike(time_ms: float, unit_id: int) -> SpikeEvent:
    return SpikeEvent(
        time_ms,
        unit_id,
        1.0,
        0.5,
        float(unit_id),
        0.0,
        (),
        0.0,
        0.0,
        1.0,
        0.0,
    )


def _field() -> TemporalExcitableField:
    topology = explicit_topology(
        [
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ],
        [],
        receptor_ids=(0,),
    )
    return TemporalExcitableField(topology)


def test_receptor_only_activity_masks_internal_dead_state() -> None:
    production_field = _field()
    production = HomeostaticController()
    empty_field = _field()
    empty = HomeostaticController()
    shadow_field = _field()
    shadow = HomeostaticController()

    production_snapshots = []
    empty_snapshots = []
    shadow_snapshots = []

    for window in range(6):
        time_ms = float(window + 1)
        rows = (_spike(time_ms, 0),)
        production_snapshots.append(
            production.observe(production_field, rows, time_ms=time_ms)
        )
        empty_snapshots.append(empty.observe(empty_field, (), time_ms=time_ms))
        shadow_rows = tuple(
            spike for spike in rows if spike.unit_id not in shadow_field.receptor_ids
        )
        shadow_snapshots.append(shadow.observe(shadow_field, shadow_rows, time_ms=time_ms))

    production_final = production_snapshots[-1]
    empty_final = empty_snapshots[-1]
    shadow_final = shadow_snapshots[-1]

    assert production_final.dead is False
    assert production.dead_streak == 0
    assert production_final.active_unit_fraction == 0.5
    assert production.rate_ema[1] == 0.0

    assert empty_final.dead is True
    assert empty.dead_streak == 6
    assert empty_final.active_unit_fraction == 0.0

    assert shadow_final.dead is True
    assert shadow.dead_streak == 6
    assert shadow_final.active_unit_fraction == 0.0

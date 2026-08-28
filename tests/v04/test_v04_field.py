from __future__ import annotations

from sparkbrain.v04 import (
    Connection,
    ExcitableFieldConfig,
    SignalPulse,
    TemporalExcitableField,
    UnitState,
    explicit_topology,
)


def test_delayed_propagation_respects_arrival_time() -> None:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ),
        (Connection(0, 1, 0.8, 5.0, plastic=False),),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))
    field.schedule_pulse(SignalPulse(0.0, "A", 0.7, location=(0.0, 0.0)))
    before = field.run_until(4.9)
    assert [row.unit_id for row in before] == [0]
    after = field.run_until(5.0)
    assert [row.unit_id for row in after] == [1]


def test_coincident_subthreshold_arrivals_can_trigger_target() -> None:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
            UnitState(2, 0.5, 1.0, base_threshold=0.9),
        ),
        (
            Connection(0, 2, 0.46, 5.0, plastic=False),
            Connection(1, 2, 0.46, 2.0, plastic=False),
        ),
        receptor_ids=(0, 1),
    )
    field = TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))
    field.schedule_pulse(SignalPulse(0.0, "A", 0.7, location=(0.0, 0.0)))
    field.schedule_pulse(SignalPulse(3.0, "B", 0.7, location=(1.0, 0.0)))
    spikes = field.run_until(6.0)
    assert [row.unit_id for row in spikes].count(2) == 1


def test_field_state_round_trip_preserves_future_dynamics() -> None:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ),
        (Connection(0, 1, 0.8, 5.0, plastic=False),),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))
    field.schedule_pulse(SignalPulse(0.0, "A", 0.7, location=(0.0, 0.0)))
    first = field.run_until(1.0)
    assert [row.unit_id for row in first] == [0]
    restored = TemporalExcitableField.from_json(field.to_json())
    assert restored.state_hash() == field.state_hash()
    assert [row.as_dict() for row in restored.run_until(6.0)] == [
        row.as_dict() for row in field.run_until(6.0)
    ]

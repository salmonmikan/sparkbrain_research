from __future__ import annotations

import pytest

from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology


def _two_unit_field(*, edge_weight: float) -> TemporalExcitableField:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.50),
            UnitState(1, 1.0, 0.0, base_threshold=0.80),
        ),
        (Connection(0, 1, weight=edge_weight, delay_ms=1.0),),
        receptor_ids=(0,),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(input_gain=1.0, receptor_fanout=1),
    )


def _pulse_receptor(field: TemporalExcitableField) -> tuple[int, ...]:
    field.schedule_pulse(SignalPulse(time_ms=0.0, channel="forge-probe", magnitude=0.60))
    spikes = field.run_until(1.0)
    return tuple(spike.unit_id for spike in spikes)


def test_natural_history_can_reach_zero_potential_with_positive_adaptation() -> None:
    field = _two_unit_field(edge_weight=0.90)

    spike_units = _pulse_receptor(field)
    target = field.units[1]

    assert spike_units == (0, 1)
    assert target.potential == pytest.approx(0.0)
    assert target.adaptation == pytest.approx(field.config.adaptation_increment)

    # This is a real post-spike state, not a coordinate splice: other state
    # variables carry the history that produced the same qualitative pair.
    assert target.spike_count == 1
    assert target.last_spike_ms == pytest.approx(1.0)
    assert target.refractory_until_ms == pytest.approx(4.0)
    assert target.excitatory_drive == pytest.approx(0.90)


def test_natural_history_can_reach_zero_adaptation_with_nonzero_potential() -> None:
    field = _two_unit_field(edge_weight=0.40)

    spike_units = _pulse_receptor(field)
    target = field.units[1]

    assert spike_units == (0,)
    assert target.potential == pytest.approx(0.40)
    assert target.adaptation == pytest.approx(0.0)

    # Again the coordinate pair has a natural witness, while the full state
    # records the causal history and therefore is not interchangeable with an
    # arbitrary anchor whose adaptation alone was set to zero.
    assert target.spike_count == 0
    assert target.last_spike_ms is None
    assert target.excitatory_drive == pytest.approx(0.40)
    assert target.source_pulse_ids


def test_quiescent_history_reaches_joint_zero_pair() -> None:
    field = _two_unit_field(edge_weight=0.40)
    target = field.units[1]

    assert target.potential == pytest.approx(0.0)
    assert target.adaptation == pytest.approx(0.0)
    assert target.spike_count == 0
    assert target.last_spike_ms is None

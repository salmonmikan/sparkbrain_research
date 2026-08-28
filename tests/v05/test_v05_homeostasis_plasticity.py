from __future__ import annotations

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v05 import HomeostaticController, V05PlasticityConfig, V05PlasticityController


def spike(t: float, unit: int) -> SpikeEvent:
    return SpikeEvent(t, unit, 1.0, 0.5, float(unit), 0.0, (), 0.0, 0.0, 1.0, 0.0)


def field() -> TemporalExcitableField:
    topology = explicit_topology(
        [UnitState(0, 0.0, 0.0, base_threshold=0.5), UnitState(1, 1.0, 0.0, base_threshold=0.5)],
        [Connection(0, 1, 0.4, 5.0, plastic=True)],
        receptor_ids=(0,),
    )
    return TemporalExcitableField(topology)


def test_homeostasis_raises_frequently_active_threshold() -> None:
    f = field()
    controller = HomeostaticController()
    before = f.units[0].base_threshold
    controller.observe(f, [spike(1.0, 0)] * 5, time_ms=2.0)
    assert f.units[0].base_threshold > before


def test_plasticity_separates_weight_and_delay_modes() -> None:
    weight_field = field()
    weight_only = V05PlasticityController(V05PlasticityConfig(enable_weight_learning=True, enable_delay_learning=False))
    before_weight = weight_field.connections[(0, 1)].weight
    before_delay = weight_field.connections[(0, 1)].delay_ms
    weight_only.apply(weight_field, [spike(0.0, 0), spike(3.0, 1)])
    assert weight_field.connections[(0, 1)].weight != before_weight
    assert weight_field.connections[(0, 1)].delay_ms == before_delay

    delay_field = field()
    delay_only = V05PlasticityController(V05PlasticityConfig(enable_weight_learning=False, enable_delay_learning=True))
    before_weight = delay_field.connections[(0, 1)].weight
    before_delay = delay_field.connections[(0, 1)].delay_ms
    delay_only.apply(delay_field, [spike(0.0, 0), spike(3.0, 1)])
    assert delay_field.connections[(0, 1)].weight == before_weight
    assert delay_field.connections[(0, 1)].delay_ms != before_delay

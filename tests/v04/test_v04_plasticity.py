from __future__ import annotations

from sparkbrain.v04 import (
    Connection,
    ExcitableFieldConfig,
    TemporalExcitableField,
    TimingPlasticityRule,
    UnitState,
    explicit_topology,
)
from sparkbrain.v04.contracts import SpikeEvent


def _spike(time_ms: float, unit_id: int) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.8,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=("p",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def test_pre_before_post_strengthens_bounded_connection() -> None:
    topology = explicit_topology(
        (UnitState(0, 0.0, 0.0), UnitState(1, 1.0, 0.0)),
        (Connection(0, 1, 0.2, 5.0),),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(topology, ExcitableFieldConfig(receptor_fanout=1))
    rule = TimingPlasticityRule()
    before = field.connection(0, 1).weight
    assert rule.apply(field, (_spike(0.0, 0), _spike(5.0, 1))) == 1
    assert field.connection(0, 1).weight > before


def test_negative_reward_reverses_causal_update_direction() -> None:
    topology = explicit_topology(
        (UnitState(0, 0.0, 0.0), UnitState(1, 1.0, 0.0)),
        (Connection(0, 1, 0.2, 5.0),),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(topology)
    rule = TimingPlasticityRule()
    before = field.connection(0, 1).weight
    rule.reward(-1.0)
    rule.apply(field, (_spike(0.0, 0), _spike(5.0, 1)))
    assert field.connection(0, 1).weight < before

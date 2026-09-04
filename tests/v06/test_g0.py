from __future__ import annotations

from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v06.g0 import (
    classify_g0_support,
    compare_queue_controls,
    field_with_queue_mode,
    run_queue_condition,
)


def prefix_field() -> TemporalExcitableField:
    topology = explicit_topology(
        units=(
            UnitState(unit_id=0, x=0, y=0, base_threshold=0.5),
            UnitState(unit_id=1, x=1, y=0, base_threshold=0.5),
            UnitState(unit_id=2, x=2, y=0, base_threshold=0.5),
        ),
        connections=(
            Connection(source_id=0, target_id=1, weight=0.8, delay_ms=4.0),
            Connection(source_id=1, target_id=2, weight=0.8, delay_ms=4.0),
        ),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            receptor_fanout=1,
            adaptation_increment=0.0,
            refractory_ms=1.0,
        ),
    )
    field.schedule_pulse(
        SignalPulse(
            time_ms=0,
            channel="prefix-A",
            magnitude=1.0,
            source_id="external-A",
        )
    )
    assert tuple(row.unit_id for row in field.run_until(0.1)) == (0,)
    assert len(field.state_dict()["queue"]) == 1
    return field


def test_queue_modes_do_not_mutate_prefix() -> None:
    field = prefix_field()
    before = field.state_hash()
    for mode in ("intact", "drained", "shuffled"):
        field_with_queue_mode(field, mode)
    assert field.state_hash() == before


def test_intact_queue_continues_scheduled_propagation() -> None:
    result = run_queue_condition(prefix_field(), mode="intact", end_ms=10)
    assert result.spike_unit_ids == (1, 2)
    assert result.initial_queue_count == 1
    assert result.final_queue_count == 0


def test_drained_queue_has_no_spontaneous_continuation_in_v04_field() -> None:
    result = run_queue_condition(prefix_field(), mode="drained", end_ms=10)
    assert result.spike_count == 0
    assert result.initial_queue_count == 0
    assert result.final_queue_count == 0


def test_comparison_uses_identical_prefix_state() -> None:
    field = prefix_field()
    before = field.state_hash()
    comparison = compare_queue_controls(field, end_ms=10)
    rows = comparison.by_mode()
    assert comparison.prefix_state_hash == before
    assert field.state_hash() == before
    assert rows["intact"].spike_count == 2
    assert rows["drained"].spike_count == 0


def test_canonical_g0_probe_reports_pending_queue_dependency() -> None:
    report = classify_g0_support(compare_queue_controls(prefix_field(), end_ms=10))
    assert report == {
        "drained_spikes": 0,
        "intact_spikes": 2,
        "pending_queue_dependency": True,
        "status": "not_observed_after_queue_drain",
    }


def test_queue_mode_rejects_unknown_value() -> None:
    try:
        field_with_queue_mode(prefix_field(), "invalid")  # type: ignore[arg-type]
    except ValueError as exc:
        assert "unsupported queue mode" in str(exc)
    else:
        raise AssertionError("invalid queue mode was accepted")

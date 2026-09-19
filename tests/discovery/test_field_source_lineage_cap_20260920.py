from __future__ import annotations

from dataclasses import asdict

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import FieldTopology, UnitState


def _run(order: tuple[str, ...]) -> tuple[TemporalExcitableField, object]:
    topology = FieldTopology(
        units=(UnitState(unit_id=0, x=0.0, y=0.0, base_threshold=1.0),),
        connections=(),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(max_sources_per_unit=16),
    )
    for pulse_id in order:
        field.schedule_arrival(
            SynapticArrival(
                time_ms=1.0,
                target_id=0,
                current=0.06,
                source_id=None,
                pulse_id=pulse_id,
            )
        )
    spikes = field.run_until(1.0)
    assert len(spikes) == 1
    return field, spikes[0]


def _physical_unit_state(field: TemporalExcitableField) -> dict[str, object]:
    row = asdict(field.units[0])
    row.pop("source_pulse_ids")
    return row


def test_same_simultaneous_arrival_multiset_changes_only_bounded_lineage_by_enqueue_order() -> None:
    """EXPLORATORY / NON_EVIDENTIARY.

    The two arms have the same target, timestamp, currents, and set of pulse IDs.
    Only insertion order changes. This characterizes bounded provenance retention;
    it is not a regression contract for desired future semantics.
    """

    pulse_ids = tuple(f"p{index:02d}" for index in range(20))
    forward_field, forward_spike = _run(pulse_ids)
    reverse_field, reverse_spike = _run(tuple(reversed(pulse_ids)))

    assert forward_spike.source_pulse_ids == tuple(f"p{index:02d}" for index in range(4, 20))
    assert reverse_spike.source_pulse_ids == tuple(f"p{index:02d}" for index in range(15, -1, -1))
    assert set(forward_spike.source_pulse_ids) != set(reverse_spike.source_pulse_ids)

    # Physical dynamics are invariant because pulse IDs never enter current,
    # threshold, refractory, or adaptation calculations.
    assert forward_spike.potential_before_reset == reverse_spike.potential_before_reset
    assert forward_spike.dynamic_threshold == reverse_spike.dynamic_threshold
    assert forward_spike.excitatory_drive == reverse_spike.excitatory_drive
    assert forward_spike.inhibitory_drive == reverse_spike.inhibitory_drive
    assert _physical_unit_state(forward_field) == _physical_unit_state(reverse_field)

    # The serialized state hash still changes because source_pulse_ids is part of
    # UnitState. Thus hash/provenance reproducibility is order-sensitive even
    # when the physical state projection is identical.
    assert forward_field.state_hash() != reverse_field.state_hash()

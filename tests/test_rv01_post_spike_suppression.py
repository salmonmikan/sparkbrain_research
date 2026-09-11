from __future__ import annotations

from sparkbrain.research.rv01_post_spike_suppression import PostSpikeSuppressionField
from sparkbrain.v04 import (
    Connection,
    ExcitableFieldConfig,
    SynapticArrival,
    TemporalExcitableField,
    UnitState,
    explicit_topology,
)


def checkpoint() -> dict:
    topology = explicit_topology(
        (
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ),
        (Connection(0, 1, 0.2, 5.0, plastic=True),),
        receptor_ids=(0,),
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            receptor_fanout=1,
            adaptation_increment=0.16,
            refractory_ms=3.0,
        ),
    )
    return field.state_dict()


def run_arm(mode: str) -> PostSpikeSuppressionField:
    field = PostSpikeSuppressionField.from_state_dict(checkpoint(), mode=mode)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=10.0,
            target_id=0,
            current=1.0,
            source_id=None,
            pulse_id="cue",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    spikes = field.run_until(10.0)
    assert len(spikes) == 1
    return field


def test_all_arms_restore_from_exact_same_checkpoint_before_probe() -> None:
    state = checkpoint()
    for mode in ("intact", "adaptation_zero", "refractory_zero", "both_zero"):
        restored = PostSpikeSuppressionField.from_state_dict(state, mode=mode)
        assert restored.state_dict() == state
        assert restored.intervention_records == []


def test_post_spike_interventions_change_only_registered_unit_fields() -> None:
    intact = run_arm("intact")
    adaptation = run_arm("adaptation_zero")
    refractory = run_arm("refractory_zero")
    both = run_arm("both_zero")

    # All arms emit/schedule the ordinary spike consequences before any edit.
    assert intact.state_dict()["queue"] == adaptation.state_dict()["queue"]
    assert intact.state_dict()["queue"] == refractory.state_dict()["queue"]
    assert intact.state_dict()["queue"] == both.state_dict()["queue"]
    assert intact.connection_state() == adaptation.connection_state()
    assert intact.connection_state() == refractory.connection_state()
    assert intact.connection_state() == both.connection_state()

    intact_unit = intact.units[0]
    adaptation_unit = adaptation.units[0]
    refractory_unit = refractory.units[0]
    both_unit = both.units[0]

    assert intact_unit.adaptation == 0.16
    assert intact_unit.refractory_until_ms == 13.0
    assert adaptation_unit.adaptation == 0.0
    assert adaptation_unit.refractory_until_ms == 13.0
    assert refractory_unit.adaptation == 0.16
    assert refractory_unit.refractory_until_ms == 10.0
    assert both_unit.adaptation == 0.0
    assert both_unit.refractory_until_ms == 10.0

    ignored = {"adaptation", "refractory_until_ms"}
    intact_state = intact.state_dict()["units"][0]
    for arm in (adaptation, refractory, both):
        arm_state = arm.state_dict()["units"][0]
        assert {k: v for k, v in arm_state.items() if k not in ignored} == {
            k: v for k, v in intact_state.items() if k not in ignored
        }


def test_intervention_records_are_exactly_mode_scoped() -> None:
    intact = run_arm("intact")
    adaptation = run_arm("adaptation_zero")
    refractory = run_arm("refractory_zero")
    both = run_arm("both_zero")

    assert intact.intervention_records == []
    assert [row["field"] for row in adaptation.intervention_records] == ["adaptation"]
    assert [row["field"] for row in refractory.intervention_records] == [
        "refractory_until_ms"
    ]
    assert [row["field"] for row in both.intervention_records] == [
        "adaptation",
        "refractory_until_ms",
    ]
    assert all(row["spike_time_ms"] == 10.0 for row in both.intervention_records)


def test_refractory_neutralization_affects_later_arrival_without_changing_queue() -> None:
    intact = run_arm("intact")
    refractory = run_arm("refractory_zero")

    for field in (intact, refractory):
        field.schedule_arrival(
            SynapticArrival(
                time_ms=11.0,
                target_id=0,
                current=0.7,
                source_id=None,
                pulse_id="second",
                novelty=0.0,
                prediction_error=0.0,
            )
        )

    assert intact.run_until(11.0) == ()
    later = refractory.run_until(11.0)
    assert len(later) == 1
    assert later[0].unit_id == 0

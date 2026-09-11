from __future__ import annotations

from sparkbrain.research.rv01.physical_learner_bridge import (
    build_physical_field,
    runtime_pulse,
)
from sparkbrain.research.rv02_hidden_eligibility import (
    OnlineHiddenEligibilityPlasticity,
    deterministic_hidden_permutation,
)
from sparkbrain.v04.contracts import SpikeEvent


def hidden_spike(unit_id: int, time_ms: float, *, magnitude: float = 1.0) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=magnitude,
        dynamic_threshold=0.5,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=(f"source-{unit_id}-{time_ms}",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=magnitude,
        inhibitory_drive=0.0,
    )


def test_hidden_spike_cannot_commit_without_later_external_gate() -> None:
    field = build_physical_field(
        unit_count=3,
        directed_edges=((0, 2), (2, 1), (0, 1)),
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    learner = OnlineHiddenEligibilityPlasticity(
        field,
        visible_units=(0, 1),
        mode="causal",
    )
    before = learner.connection_state_hash()
    recorded = learner.record_hidden_spikes((hidden_spike(2, 5.0),))
    assert len(recorded) == 1
    assert learner.connection_state_hash() == before
    assert learner.hidden_return_updates == []

    updates = learner.observe_external(
        runtime_pulse(
            event_id="external-visible-1",
            time_ms=10.0,
            unit_id=1,
            magnitude=1.0,
        )
    )
    hidden_updates = [row for row in updates if row.mode == "hidden_return_potentiation"]
    assert len(hidden_updates) == 1
    assert hidden_updates[0].source_id == 2
    assert hidden_updates[0].target_id == 1
    assert hidden_updates[0].weight_after > hidden_updates[0].weight_before
    assert learner.connection_state_hash() != before


def test_hidden_trace_outside_lag_window_expires_without_update() -> None:
    field = build_physical_field(
        unit_count=3,
        directed_edges=((0, 2), (2, 1)),
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    learner = OnlineHiddenEligibilityPlasticity(
        field,
        visible_units=(0, 1),
        mode="causal",
    )
    before = learner.connection_state_hash()
    learner.record_hidden_spikes((hidden_spike(2, 1.0),))
    updates = learner.observe_external(
        runtime_pulse(
            event_id="too-late",
            time_ms=8.0,
            unit_id=1,
            magnitude=1.0,
        )
    )
    assert not [row for row in updates if row.mode == "hidden_return_potentiation"]
    assert learner.connection_state_hash() == before
    assert len(learner.hidden_trace_expiry_records) == 1


def test_shuffled_control_preserves_hidden_event_budget() -> None:
    causal_field = build_physical_field(
        unit_count=4,
        directed_edges=((0, 2), (0, 3), (2, 1), (3, 1)),
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    shuffled_field = build_physical_field(
        unit_count=4,
        directed_edges=((0, 2), (0, 3), (2, 1), (3, 1)),
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    mapping = deterministic_hidden_permutation((2, 3), namespace="unit-test")
    assert mapping == {2: 3, 3: 2}

    causal = OnlineHiddenEligibilityPlasticity(
        causal_field,
        visible_units=(0, 1),
        mode="causal",
    )
    shuffled = OnlineHiddenEligibilityPlasticity(
        shuffled_field,
        visible_units=(0, 1),
        mode="shuffled",
        shuffled_mapping=mapping,
    )
    spikes = (
        hidden_spike(2, 5.0, magnitude=0.8),
        hidden_spike(3, 6.0, magnitude=1.1),
    )
    causal_rows = causal.record_hidden_spikes(spikes)
    shuffled_rows = shuffled.record_hidden_spikes(spikes)

    assert len(causal_rows) == len(shuffled_rows) == 2
    assert [row.time_ms for row in causal_rows] == [row.time_ms for row in shuffled_rows]
    assert [row.magnitude for row in causal_rows] == [row.magnitude for row in shuffled_rows]
    assert [row.observed_unit_id for row in causal_rows] == [
        row.observed_unit_id for row in shuffled_rows
    ]
    assert [row.assigned_source_id for row in causal_rows] == [2, 3]
    assert [row.assigned_source_id for row in shuffled_rows] == [3, 2]


def test_disabled_arm_records_no_hidden_eligibility() -> None:
    field = build_physical_field(
        unit_count=3,
        directed_edges=((0, 2), (2, 1)),
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    learner = OnlineHiddenEligibilityPlasticity(
        field,
        visible_units=(0, 1),
        mode="disabled",
    )
    before = learner.connection_state_hash()
    assert learner.record_hidden_spikes((hidden_spike(2, 5.0),)) == ()
    learner.observe_external(
        runtime_pulse(
            event_id="external-visible-1",
            time_ms=10.0,
            unit_id=1,
            magnitude=1.0,
        )
    )
    assert learner.hidden_trace_records == []
    assert learner.hidden_return_updates == []
    assert learner.connection_state_hash() == before

"""EXPLORATORY / NON_EVIDENTIARY delayed-reward eligibility discriminator."""

from __future__ import annotations

import pytest

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v05.brain import IntegratedV05Brain
from sparkbrain.v05.plasticity import V05PlasticityConfig, V05PlasticityController


def _spike(time_ms: float, unit_id: int) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.8,
        x=0.0,
        y=0.0,
        source_pulse_ids=("synthetic-dev",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def _setup() -> tuple[V05PlasticityController, object, tuple[int, int]]:
    brain = IntegratedV05Brain()
    field = brain.base.field
    edge_key = min(key for key, edge in field.connections.items() if edge.plastic)
    controller = V05PlasticityController(
        V05PlasticityConfig(enable_weight_learning=True, enable_delay_learning=False)
    )
    return controller, field, edge_key


def _causal_pair(edge_key: tuple[int, int], offset_ms: float) -> tuple[SpikeEvent, SpikeEvent]:
    source_id, target_id = edge_key
    return (_spike(offset_ms + 1.0, source_id), _spike(offset_ms + 2.0, target_id))


def test_delayed_reward_requires_edge_reactivation_for_weight_effect() -> None:
    no_activity_controller, no_activity_field, edge_key = _setup()
    rewarded_controller, rewarded_field, rewarded_edge_key = _setup()
    neutral_controller, neutral_field, neutral_edge_key = _setup()
    assert rewarded_edge_key == edge_key == neutral_edge_key

    first_pair = _causal_pair(edge_key, 0.0)
    for controller, field in (
        (no_activity_controller, no_activity_field),
        (rewarded_controller, rewarded_field),
        (neutral_controller, neutral_field),
    ):
        assert controller.apply(field, first_pair) == 1

    eligibility_key = f"{edge_key[0]}:{edge_key[1]}"
    initial_weight = no_activity_field.connections[edge_key].weight
    initial_eligibility = no_activity_controller.eligibility[eligibility_key]
    assert rewarded_field.connections[edge_key].weight == pytest.approx(initial_weight)
    assert neutral_field.connections[edge_key].weight == pytest.approx(initial_weight)
    assert rewarded_controller.eligibility[eligibility_key] == pytest.approx(initial_eligibility)
    assert neutral_controller.eligibility[eligibility_key] == pytest.approx(initial_eligibility)

    # Delayed scalar reward after the causal event does not by itself apply the stored
    # local eligibility to the edge when the next plasticity step has no activity.
    no_activity_controller.reward(-2.0)
    assert no_activity_controller.apply(no_activity_field, ()) == 0
    assert no_activity_field.connections[edge_key].weight == pytest.approx(initial_weight)
    assert no_activity_controller.eligibility[eligibility_key] == pytest.approx(
        initial_eligibility * no_activity_controller.config.eligibility_decay
    )

    # The same delayed reward has an effect only once that same edge is active again.
    second_pair = _causal_pair(edge_key, 10.0)
    rewarded_controller.reward(-2.0)
    assert rewarded_controller.apply(rewarded_field, second_pair) == 1
    assert neutral_controller.apply(neutral_field, second_pair) == 1

    rewarded_weight = rewarded_field.connections[edge_key].weight
    neutral_weight = neutral_field.connections[edge_key].weight
    assert rewarded_weight < initial_weight
    assert neutral_weight > initial_weight
    assert rewarded_weight < neutral_weight

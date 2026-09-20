"""EXPLORATORY / NON_EVIDENTIARY eligibility-history specificity discriminator."""

from __future__ import annotations

import math

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


def _causal_pair(edge_key: tuple[int, int], offset_ms: float) -> tuple[SpikeEvent, SpikeEvent]:
    source_id, target_id = edge_key
    return (_spike(offset_ms + 1.0, source_id), _spike(offset_ms + 2.0, target_id))


def _two_disjoint_plastic_edges() -> tuple[IntegratedV05Brain, tuple[int, int], tuple[int, int]]:
    brain = IntegratedV05Brain()
    field = brain.base.field
    bounds = V05PlasticityConfig()
    candidates = [
        key
        for key in sorted(field.connections)
        if field.connections[key].plastic
        and bounds.min_weight + 0.05 < field.connections[key].weight < bounds.max_weight - 0.05
    ]
    for index, edge_a in enumerate(candidates):
        units_a = set(edge_a)
        for edge_b in candidates[index + 1 :]:
            if units_a.isdisjoint(edge_b):
                return brain, edge_a, edge_b
    raise AssertionError("default v0.5 field did not expose two disjoint interior plastic edges")


def test_history_specific_reward_credit_reduces_to_per_edge_eligibility_trace() -> None:
    brain, edge_a, edge_b = _two_disjoint_plastic_edges()
    field = brain.base.field

    priming_config = V05PlasticityConfig(
        enable_weight_learning=False,
        enable_delay_learning=False,
    )
    controller = V05PlasticityController(priming_config)

    key_a = f"{edge_a[0]}:{edge_a[1]}"
    key_b = f"{edge_b[0]}:{edge_b[1]}"

    # Prime only A. The two target edges have disjoint endpoint units, so B has
    # no target-edge eligibility history after this synthetic causal event.
    assert controller.apply(field, _causal_pair(edge_a, 0.0)) >= 1
    primed_a = controller.eligibility[key_a]
    assert primed_a > 0.0
    assert key_b not in controller.eligibility

    controller.config = V05PlasticityConfig(
        enable_weight_learning=True,
        enable_delay_learning=False,
    )
    config = controller.config

    weight_a_before = field.connections[edge_a].weight
    weight_b_before = field.connections[edge_b].weight

    lag_ms = 1.0
    current_delta = math.exp(-lag_ms / config.tau_plus_ms)
    expected_eligibility_a = config.eligibility_decay * primed_a + current_delta
    expected_eligibility_b = current_delta
    reward = -2.0
    expected_weight_a = max(
        config.min_weight,
        min(
            config.max_weight,
            weight_a_before + config.learning_rate * reward * expected_eligibility_a,
        ),
    )
    expected_weight_b = max(
        config.min_weight,
        min(
            config.max_weight,
            weight_b_before + config.learning_rate * reward * expected_eligibility_b,
        ),
    )

    # Matched current activity: both target edges receive exactly one +1 ms causal
    # pair in the same plasticity step under the same scalar reward. Only A differs
    # by having stored eligibility from the prospectively fixed priming event.
    controller.reward(reward)
    current_spikes = _causal_pair(edge_a, 10.0) + _causal_pair(edge_b, 20.0)
    assert controller.apply(field, current_spikes) >= 2

    assert controller.eligibility[key_a] == pytest.approx(expected_eligibility_a)
    assert controller.eligibility[key_b] == pytest.approx(expected_eligibility_b)
    assert field.connections[edge_a].weight == pytest.approx(expected_weight_a)
    assert field.connections[edge_b].weight == pytest.approx(expected_weight_b)

    delta_a = field.connections[edge_a].weight - weight_a_before
    delta_b = field.connections[edge_b].weight - weight_b_before
    assert abs(delta_a) > abs(delta_b)
    assert delta_a == pytest.approx(config.learning_rate * reward * expected_eligibility_a)
    assert delta_b == pytest.approx(config.learning_rate * reward * expected_eligibility_b)

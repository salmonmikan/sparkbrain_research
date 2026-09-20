from __future__ import annotations

import copy
import math

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v05 import V05PlasticityConfig, V05PlasticityController


def _spike(time_ms: float, unit_id: int) -> SpikeEvent:
    return SpikeEvent(time_ms, unit_id, 1.0, 0.5, float(unit_id), 0.0, (), 0.0, 0.0, 1.0, 0.0)


def _field() -> TemporalExcitableField:
    topology = explicit_topology(
        [
            UnitState(0, 0.0, 0.0, base_threshold=0.5),
            UnitState(1, 1.0, 0.0, base_threshold=0.5),
        ],
        [Connection(0, 1, 0.4, 5.0, plastic=True)],
        receptor_ids=(0,),
    )
    return TemporalExcitableField(topology)


def test_dev_eligibility_timebase_partition_invariance_fixed_contract() -> None:
    config = V05PlasticityConfig(
        enable_weight_learning=True,
        enable_delay_learning=False,
        learning_rate=0.001,
        eligibility_decay=0.90,
    )
    controller = V05PlasticityController(config)
    field = _field()

    initial_event = [_spike(0.0, 0), _spike(18.0, 1)]
    final_event = [_spike(100.0, 0), _spike(118.0, 1)]

    assert controller.reward_trace == 1.0
    assert controller.apply(field, initial_event) == 1

    arm_one_controller = copy.deepcopy(controller)
    arm_two_controller = copy.deepcopy(controller)
    arm_one_field = copy.deepcopy(field)
    arm_two_field = copy.deepcopy(field)

    # Prospective matched-contract validity: exact clones before the partition-only difference.
    assert arm_one_controller.state_dict() == arm_two_controller.state_dict()
    assert arm_one_field.connections[(0, 1)].weight == arm_two_field.connections[(0, 1)].weight
    assert arm_one_field.connections[(0, 1)].delay_ms == arm_two_field.connections[(0, 1)].delay_ms
    assert arm_one_controller.reward_trace == arm_two_controller.reward_trace == 1.0

    # The only arm difference is one additional empty apply() partition in Arm B.
    assert arm_one_controller.apply(arm_one_field, []) == 0
    assert arm_two_controller.apply(arm_two_field, []) == 0
    assert arm_two_controller.apply(arm_two_field, []) == 0

    # Same source/target IDs and absolute timestamps in the fixed final causal event.
    assert arm_one_controller.apply(arm_one_field, final_event) == 1
    assert arm_two_controller.apply(arm_two_field, final_event) == 1

    delta = math.exp(-18.0 / config.tau_plus_ms)
    decay = config.eligibility_decay
    key = "0:1"
    shared_post_initial_weight = 0.4 + config.learning_rate * delta

    expected_one_eligibility = delta * decay**2 + delta
    expected_two_eligibility = delta * decay**3 + delta
    expected_one_weight = (
        shared_post_initial_weight + config.learning_rate * expected_one_eligibility
    )
    expected_two_weight = (
        shared_post_initial_weight + config.learning_rate * expected_two_eligibility
    )

    actual_one_eligibility = arm_one_controller.eligibility[key]
    actual_two_eligibility = arm_two_controller.eligibility[key]
    actual_one_weight = arm_one_field.connections[(0, 1)].weight
    actual_two_weight = arm_two_field.connections[(0, 1)].weight

    # Prospectively fixed CALL_COUNT_PARTITION_DEPENDENT_EXACT terminal.
    assert actual_one_eligibility != actual_two_eligibility
    assert actual_one_weight != actual_two_weight
    assert math.isclose(
        actual_one_eligibility,
        expected_one_eligibility,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert math.isclose(
        actual_two_eligibility,
        expected_two_eligibility,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert math.isclose(actual_one_weight, expected_one_weight, rel_tol=1e-12, abs_tol=1e-12)
    assert math.isclose(actual_two_weight, expected_two_weight, rel_tol=1e-12, abs_tol=1e-12)
    assert arm_one_controller.update_count == arm_two_controller.update_count == 2

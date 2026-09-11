from __future__ import annotations

import math

import pytest

from sparkbrain.research.rv01.interference_contract import (
    InterferenceFamily,
    InterferencePhase,
)
from sparkbrain.research.rv01.traversal_dynamics import (
    _prefix_for_distinct_budget,
    _traversal_metrics,
    run_traversal_dynamics_world,
)
from sparkbrain.research.rv01.traversal_dynamics_contract import (
    R01_14_DEVELOPMENT_SEEDS,
    R01_14_HELD_OUT_SEEDS,
    development_traversal_dynamics_worlds,
    held_out_traversal_dynamics_worlds,
    traversal_dynamics_world,
    traversal_dynamics_world_grid_hash,
)


def test_r01_14_world_contract_uses_fresh_fixed_seed_namespaces() -> None:
    development = development_traversal_dynamics_worlds()
    held_out = held_out_traversal_dynamics_worlds()

    assert R01_14_DEVELOPMENT_SEEDS == (400, 401, 402, 403, 404)
    assert R01_14_HELD_OUT_SEEDS == tuple(range(500, 510))
    assert len(development) == 25
    assert len(held_out) == 50
    assert {world.seed for world in development} == set(R01_14_DEVELOPMENT_SEEDS)
    assert {world.seed for world in held_out} == set(R01_14_HELD_OUT_SEEDS)
    assert {world.family for world in development} == set(InterferenceFamily)
    assert {world.family for world in held_out} == set(InterferenceFamily)
    assert all(world.unit_count == 96 for world in development + held_out)


def test_r01_14_world_grid_is_deterministic_and_phase_disjoint() -> None:
    development_a = development_traversal_dynamics_worlds()
    development_b = development_traversal_dynamics_worlds()
    held_out = held_out_traversal_dynamics_worlds()

    assert traversal_dynamics_world_grid_hash(development_a) == (
        traversal_dynamics_world_grid_hash(development_b)
    )
    assert traversal_dynamics_world_grid_hash(development_a) != (
        traversal_dynamics_world_grid_hash(held_out)
    )
    assert not set(R01_14_DEVELOPMENT_SEEDS).intersection(R01_14_HELD_OUT_SEEDS)


def test_traversal_metrics_measure_revisits_and_discovery_without_route_labels() -> None:
    metrics = _traversal_metrics((7, 7, 3, 7, 9))

    assert metrics.event_count == 5
    assert metrics.distinct_unit_count == 3
    assert metrics.revisit_count == 2
    assert math.isclose(metrics.revisit_rate, 0.4)
    assert math.isclose(metrics.new_state_yield, 0.6)
    assert metrics.first_visit_positions == (1, 3, 5)
    assert 0.0 < metrics.normalized_discovery_auc < 1.0


def test_common_breadth_prefix_preserves_original_event_order() -> None:
    assert _prefix_for_distinct_budget((1, 1, 2, 3, 2), 3) == (1, 1, 2, 3)
    assert _prefix_for_distinct_budget((4, 5, 4), 0) == ()
    with pytest.raises(ValueError):
        _prefix_for_distinct_budget((1, 2), 3)


def test_r01_14_held_out_capability_is_closed() -> None:
    world = traversal_dynamics_world(
        InterferencePhase.HELD_OUT,
        InterferenceFamily.DISJOINT_ROUTES,
        R01_14_HELD_OUT_SEEDS[0],
    )
    with pytest.raises(RuntimeError, match="held-out capability execution is not open"):
        run_traversal_dynamics_world(world)


def test_r01_14_development_probe_preserves_fixed_resource_comparator() -> None:
    world = traversal_dynamics_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.DISJOINT_ROUTES,
        R01_14_DEVELOPMENT_SEEDS[0],
    )
    result = run_traversal_dynamics_world(world)

    assert result.resource_match_passed
    assert result.field_reexecution_consistent
    assert result.deterministic_replay_state_hash
    assert result.deterministic_replay_probe_hash
    assert len(result.probes) == world.route_count
    for probe in result.probes:
        assert probe.common_distinct_budget == min(
            probe.field_raw.distinct_unit_count,
            probe.reservoir_raw.distinct_unit_count,
        )
        assert probe.field_common_breadth.distinct_unit_count == (
            probe.common_distinct_budget
        )
        assert probe.reservoir_common_breadth.distinct_unit_count == (
            probe.common_distinct_budget
        )

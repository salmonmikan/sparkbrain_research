from __future__ import annotations

from sparkbrain.research.rv01.activity_matched_contract import (
    R01_13_DEVELOPMENT_SEEDS,
    R01_13_HELD_OUT_SEEDS,
    activity_matched_world,
    activity_matched_world_grid_hash,
    development_activity_matched_worlds,
    held_out_activity_matched_worlds,
)
from sparkbrain.research.rv01.activity_matched_discrimination import (
    _prefix_for_distinct_budget,
    _trace_metrics,
    run_activity_matched_world,
)
from sparkbrain.research.rv01.interference_contract import (
    DEVELOPMENT_SEEDS,
    HELD_OUT_SEEDS,
    InterferenceFamily,
    InterferencePhase,
)


def test_r01_13_seed_space_is_fresh_and_disjoint_from_r01_12() -> None:
    old = set(DEVELOPMENT_SEEDS).union(HELD_OUT_SEEDS)
    assert not old.intersection(R01_13_DEVELOPMENT_SEEDS)
    assert not old.intersection(R01_13_HELD_OUT_SEEDS)
    assert not set(R01_13_DEVELOPMENT_SEEDS).intersection(R01_13_HELD_OUT_SEEDS)


def test_r01_13_world_grids_are_deterministic_and_phase_separated() -> None:
    development = development_activity_matched_worlds()
    held_out = held_out_activity_matched_worlds()
    assert len(development) == 25
    assert len(held_out) == 50
    assert all(world.phase is InterferencePhase.DEVELOPMENT for world in development)
    assert all(world.phase is InterferencePhase.HELD_OUT for world in held_out)
    assert all(world.unit_count == 96 for world in development + held_out)
    assert activity_matched_world_grid_hash(
        development
    ) == activity_matched_world_grid_hash(development_activity_matched_worlds())
    assert activity_matched_world_grid_hash(
        held_out
    ) == activity_matched_world_grid_hash(held_out_activity_matched_worlds())
    assert activity_matched_world_grid_hash(
        development
    ) != activity_matched_world_grid_hash(held_out)


def test_event_and_candidate_breadth_matching_are_prefix_only() -> None:
    trace = (4, 4, 8, 4, 9, 10)
    assert trace[:4] == (4, 4, 8, 4)
    assert _prefix_for_distinct_budget(trace, 0) == ()
    assert _prefix_for_distinct_budget(trace, 1) == (4,)
    assert _prefix_for_distinct_budget(trace, 2) == (4, 4, 8)
    assert _prefix_for_distinct_budget(trace, 3) == (4, 4, 8, 4, 9)


def test_trace_metrics_keep_retention_and_contamination_separate() -> None:
    metrics = _trace_metrics(
        expected=(1, 2, 3),
        route_units=(0, 1, 2, 3),
        trace=(1, 7, 2, 8, 3),
    )
    assert metrics.ordered_retention_fraction == 1.0
    assert metrics.ordered_match_count == 3
    assert metrics.contamination_count == 2
    assert metrics.contamination_rate == 0.4
    assert metrics.exact_route_recovered is False


def test_single_world_integration_preserves_resource_matched_reservoir() -> None:
    world = activity_matched_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.SHARED_PREFIX_BRANCHES,
        R01_13_DEVELOPMENT_SEEDS[0],
    )
    result = run_activity_matched_world(world)
    assert result.resource_match_passed is True
    assert result.field_reexecution_consistent is True
    assert result.deterministic_replay_state_hash is True
    assert result.deterministic_replay_probe_hash is True
    assert len(result.probes) == world.route_count
    for probe in result.probes:
        assert len(probe.field_event_units) == probe.common_event_budget
        assert len(probe.reservoir_event_units) == probe.common_event_budget
        assert len(set(probe.field_breadth_units)) == probe.common_distinct_budget
        assert len(set(probe.reservoir_breadth_units)) == probe.common_distinct_budget


def test_held_out_world_is_not_executable_through_r01_13_runner() -> None:
    world = activity_matched_world(
        InterferencePhase.HELD_OUT,
        InterferenceFamily.DENSE_ROUTE_LOAD,
        R01_13_HELD_OUT_SEEDS[0],
    )
    try:
        run_activity_matched_world(world)
    except RuntimeError as error:
        assert "held-out capability execution is not open" in str(error)
    else:
        raise AssertionError("R01-13 held-out execution must remain closed")

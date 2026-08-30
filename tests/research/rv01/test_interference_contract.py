from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.research.rv01.interference_contract import (
    DEVELOPMENT_SEEDS,
    HELD_OUT_SEEDS,
    InterferenceFamily,
    InterferencePhase,
    development_worlds,
    held_out_worlds,
    interference_world,
    world_grid_hash,
)


def test_development_grid_is_complete_deterministic_and_hashable() -> None:
    first = development_worlds()
    second = development_worlds()
    assert len(first) == len(InterferenceFamily) * len(DEVELOPMENT_SEEDS) == 15
    assert first == second
    assert world_grid_hash(first) == world_grid_hash(second)
    assert len(world_grid_hash(first)) == 64
    assert len({world.specification_hash() for world in first}) == len(first)
    assert all(world.phase is InterferencePhase.DEVELOPMENT for world in first)


def test_held_out_grid_is_defined_but_not_executed_by_the_contract() -> None:
    first = held_out_worlds()
    second = held_out_worlds()
    assert len(first) == len(InterferenceFamily) * len(HELD_OUT_SEEDS) == 50
    assert first == second
    assert world_grid_hash(first) == world_grid_hash(second)
    assert len({world.specification_hash() for world in first}) == len(first)
    assert all(world.phase is InterferencePhase.HELD_OUT for world in first)
    lowered = str([world.state_dict() for world in first]).lower()
    for forbidden in (
        "passed",
        "success_fraction",
        "correct_action",
        "scalar_reward",
        "meaning_state",
        "assembly_id",
    ):
        assert forbidden not in lowered


def test_development_and_held_out_seed_sets_are_disjoint() -> None:
    assert set(DEVELOPMENT_SEEDS).isdisjoint(HELD_OUT_SEEDS)


@pytest.mark.parametrize("seed", DEVELOPMENT_SEEDS)
def test_disjoint_routes_share_no_units(seed: int) -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.DISJOINT_ROUTES,
        seed,
    )
    for index, left in enumerate(world.routes):
        for right in world.routes[index + 1 :]:
            assert set(left.units).isdisjoint(right.units)


@pytest.mark.parametrize("seed", DEVELOPMENT_SEEDS)
def test_shared_cue_family_has_three_real_competing_branches(seed: int) -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.SHARED_CUE_BRANCHES,
        seed,
    )
    assert world.route_count == 3
    assert len({route.units[0] for route in world.routes}) == 1
    assert len({route.units for route in world.routes}) == 3
    assert all(route.exposure_count > 0 for route in world.routes)
    assert max(route.exposure_count for route in world.routes) - min(
        route.exposure_count for route in world.routes
    ) == 2


@pytest.mark.parametrize("seed", DEVELOPMENT_SEEDS)
def test_shared_prefix_family_diverges_only_after_two_units(seed: int) -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.SHARED_PREFIX_BRANCHES,
        seed,
    )
    assert len({route.units[:2] for route in world.routes}) == 1
    suffixes = tuple(route.units[2:] for route in world.routes)
    assert len(set(suffixes)) == 3
    for index, left in enumerate(suffixes):
        for right in suffixes[index + 1 :]:
            assert set(left).isdisjoint(right)


@pytest.mark.parametrize("seed", DEVELOPMENT_SEEDS)
def test_edge_reversal_family_contains_opposing_directed_edges(seed: int) -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.EDGE_REVERSAL,
        seed,
    )
    edges = {
        (route.units[index], route.units[index + 1])
        for route in world.routes
        for index in range(len(route.units) - 1)
    }
    assert any((target, source) in edges for source, target in edges)
    assert set(world.reversal_route_ids) == {
        "route:forward",
        "route:reverse",
    }


@pytest.mark.parametrize("seed", DEVELOPMENT_SEEDS)
def test_dense_route_family_exceeds_frozen_edge_budget(seed: int) -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.DENSE_ROUTE_LOAD,
        seed,
    )
    structural_edges = sum(len(route.units) - 1 for route in world.routes)
    assert world.route_count == 8
    assert structural_edges > world.maximum_total_active_edges
    assert world.maximum_active_outgoing_edges == 3


def test_training_and_probe_order_cover_each_route_once() -> None:
    for world in (*development_worlds(), *held_out_worlds()):
        route_ids = {route.route_id for route in world.routes}
        assert set(world.training_order) == route_ids
        assert len(world.training_order) == len(route_ids)
        assert set(world.probe_order) == route_ids
        assert len(world.probe_order) == len(route_ids)


def test_invalid_family_shapes_fail_closed() -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.DISJOINT_ROUTES,
        0,
    )
    overlapping = replace(
        world.routes[1],
        units=(world.routes[0].units[0], *world.routes[1].units[1:]),
    )
    invalid = replace(world, routes=(world.routes[0], overlapping, world.routes[2]))
    with pytest.raises(ValueError, match="overlapping"):
        invalid.validate()

    dense = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.DENSE_ROUTE_LOAD,
        0,
    )
    with pytest.raises(ValueError, match="must exceed"):
        replace(dense, maximum_total_active_edges=999).validate()


def test_contract_contains_no_runtime_transition_or_functional_taxonomy() -> None:
    lowered = str(
        [
            world.state_dict()
            for world in (*development_worlds(), *held_out_worlds())
        ]
    ).lower()
    for forbidden in (
        "localtemporalexpectation",
        "sparselocaltransitionadaptation",
        "endogenouspulseproposal",
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "correct_action",
        "scalar_reward",
        "meaning_state",
    ):
        assert forbidden not in lowered

from sparkbrain.research.rv01.interference_contract import InterferenceFamily
from sparkbrain.research.rv01_r01_16_identity import R01_16_DEVELOPMENT_SEEDS
from sparkbrain.research.rv01_r01_16_worlds import (
    development_world_grid,
    development_world_grid_hash,
)


def test_r01_16_development_world_grid_is_exact_and_deterministic() -> None:
    worlds = development_world_grid()

    assert len(worlds) == 25
    assert {world.seed for world in worlds} == set(R01_16_DEVELOPMENT_SEEDS)
    assert {world.family for world in worlds} == set(InterferenceFamily)
    assert len({world.world_id for world in worlds}) == 25
    assert len({world.specification_hash() for world in worlds}) == 25
    assert all(world.unit_count == 96 for world in worlds)
    assert development_world_grid_hash() == (
        "b334ab63b12ec967acc60d75242c8518fadc93a0eeb3de8f9c4a9d38d663c432"
    )


def test_r01_16_world_grid_registers_every_future_probe_cell_without_running_it() -> None:
    worlds = development_world_grid()

    for world in worlds:
        route_ids = {route.route_id for route in world.routes}
        assert set(world.probe_order) == route_ids
        assert set(world.training_order) == route_ids
        assert all(
            world.probe_horizon_ms(route) > world.lag_ms
            for route in world.routes
        )
        assert world.state_dict()["phase"] == "development"
        assert "capability" not in world.state_dict()

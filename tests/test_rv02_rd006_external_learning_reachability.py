from __future__ import annotations

from sparkbrain.research.rv02_rd006_external_learning_reachability import (
    ARMS,
    FAMILIES,
    RD006Config,
    development_worlds,
    run_cell,
)


def test_rd006_contract_is_fixed_and_fresh() -> None:
    config = RD006Config()
    worlds = development_worlds(config)
    assert tuple(world["family"] for world in worlds) == FAMILIES
    assert config.seed == 92701
    assert config.scale == 1
    assert config.unit_count == 48
    assert config.degree == 8


def test_paired_arms_isolate_ordinary_external_learning() -> None:
    config = RD006Config()
    cell = run_cell(config, development_worlds(config)[0])
    assert tuple(cell["arms"]) == ARMS
    assert cell["paired_contract"] == {
        "same_topology": True,
        "same_schedule": True,
        "same_initial_state": True,
        "same_measurement_clocks": True,
        "only_factor": "ordinary_external_learning_on_vs_off",
    }
    off = cell["arms"]["external_learning_off"]
    on = cell["arms"]["external_learning_on"]
    assert off["initial_connection_sha256"] == on["initial_connection_sha256"]
    assert off["ordinary_update_count"] == 0
    assert on["external_observation_count"] == cell["schedule_event_count"]
    assert on["ordinary_update_count"] > 0
    assert off["hidden_return_learning_enabled"] is False
    assert on["hidden_return_learning_enabled"] is False
    assert off["hidden_return_update_count"] == 0
    assert on["hidden_return_update_count"] == 0


def test_rd006_is_deterministic() -> None:
    config = RD006Config()
    world = development_worlds(config)[1]
    assert run_cell(config, world) == run_cell(config, world)


def test_all_measurement_clocks_retain_raw_activity() -> None:
    config = RD006Config()
    cell = run_cell(config, development_worlds(config)[0])
    for arm in cell["arms"].values():
        assert len(arm["inspected_clocks"]) == cell["schedule_event_count"]
        assert all("raw_spikes" in row for row in arm["inspected_clocks"])

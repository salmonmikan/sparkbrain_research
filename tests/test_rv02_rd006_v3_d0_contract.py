from __future__ import annotations

from sparkbrain.research import rv02_rd006_external_learning_reachability_v3 as v3
from sparkbrain.research import rv02_rd006_external_learning_reachability_v3_d0 as d0
from sparkbrain.v04.contracts import SpikeEvent


def _spike(unit_id: int, time_ms: float) -> SpikeEvent:
    return SpikeEvent(
        time_ms=time_ms,
        unit_id=unit_id,
        potential_before_reset=1.0,
        dynamic_threshold=0.5,
        x=float(unit_id),
        y=0.0,
        source_pulse_ids=("test",),
        novelty=0.0,
        prediction_error=0.0,
        excitatory_drive=1.0,
        inhibitory_drive=0.0,
    )


def test_execution_field_matches_static_preflight_without_running_dynamics() -> None:
    config = d0.RD006Config()
    for world in d0.development_worlds(config):
        preflight = v3.build_family_preflight(config, world)
        field = d0.build_execution_field(config, world, preflight)
        assert d0.digest(tuple(sorted(field.connections))) == preflight["planned_topology_sha256"]
        assert len(field.connections) == config.unit_count * config.degree


def test_static_paths_without_actual_spikes_cannot_open_dynamic_gate() -> None:
    config = d0.RD006Config()
    world = d0.development_worlds(config)[0]
    preflight = v3.build_family_preflight(config, world)
    field = d0.build_execution_field(config, world, preflight)
    clock = preflight["declared_return_clock"]
    diagnostics = d0.clock_diagnostics(
        field,
        (),
        return_unit_id=int(clock["return_unit_id"]),
        return_time_ms=float(clock["return_time_ms"]),
        config=config,
    )
    assert diagnostics["structurally_connected_hidden_source_count"] >= 2
    assert diagnostics["dynamic_eligible_hidden_source_count"] == 0
    assert diagnostics["dynamic_gate_ready"] is False


def test_two_distinct_actual_spikes_with_edges_and_fixed_lag_open_clock_gate() -> None:
    config = d0.RD006Config()
    world = d0.development_worlds(config)[0]
    preflight = v3.build_family_preflight(config, world)
    field = d0.build_execution_field(config, world, preflight)
    clock = preflight["declared_return_clock"]
    return_time = float(clock["return_time_ms"])
    sources = tuple(int(value) for value in clock["hidden_source_ids"])
    diagnostics = d0.clock_diagnostics(
        field,
        tuple(_spike(source, return_time - 0.5) for source in sources),
        return_unit_id=int(clock["return_unit_id"]),
        return_time_ms=return_time,
        config=config,
    )
    assert diagnostics["dynamic_eligible_hidden_source_count"] == 2
    assert diagnostics["dynamic_gate_ready"] is True
    assert {
        row["source_id"] for row in diagnostics["dynamic_eligible_hidden_sources"]
    } == set(sources)


def test_duplicate_spikes_from_one_source_count_once() -> None:
    config = d0.RD006Config()
    world = d0.development_worlds(config)[0]
    preflight = v3.build_family_preflight(config, world)
    field = d0.build_execution_field(config, world, preflight)
    clock = preflight["declared_return_clock"]
    return_time = float(clock["return_time_ms"])
    source = int(clock["hidden_source_ids"][0])
    diagnostics = d0.clock_diagnostics(
        field,
        (_spike(source, return_time - 1.0), _spike(source, return_time - 0.5)),
        return_unit_id=int(clock["return_unit_id"]),
        return_time_ms=return_time,
        config=config,
    )
    assert diagnostics["dynamic_eligible_hidden_source_count"] == 1
    assert diagnostics["dynamic_gate_ready"] is False


def test_out_of_window_actual_spikes_do_not_open_dynamic_gate() -> None:
    config = d0.RD006Config()
    world = d0.development_worlds(config)[0]
    preflight = v3.build_family_preflight(config, world)
    field = d0.build_execution_field(config, world, preflight)
    clock = preflight["declared_return_clock"]
    return_time = float(clock["return_time_ms"])
    sources = tuple(int(value) for value in clock["hidden_source_ids"])
    diagnostics = d0.clock_diagnostics(
        field,
        tuple(_spike(source, return_time) for source in sources),
        return_unit_id=int(clock["return_unit_id"]),
        return_time_ms=return_time,
        config=config,
    )
    assert diagnostics["dynamic_eligible_hidden_source_count"] == 0
    assert diagnostics["dynamic_gate_ready"] is False

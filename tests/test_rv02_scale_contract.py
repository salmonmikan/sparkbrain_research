"""Independent construction invariants; no formal-world execution."""

import copy
import json
from collections import Counter, defaultdict

import unittest

from sparkbrain.research.rv02_scale import (
    ScaleStudyConfig,
    audit_scale,
    build_topology,
    development_worlds,
    digest,
    geometry,
    project_behavior,
    run_development_cell,
)


def test_config_round_trip_is_json_safe():
    config = ScaleStudyConfig()
    config.validate()
    restored = ScaleStudyConfig.from_state_dict(json.loads(json.dumps(config.state_dict())))
    assert restored == config


def test_invalid_or_incomplete_scale_matrix_is_rejected():
    for scales in [(True, 3, 10), (1.0, 3, 10), (1, 1, 10), (1, 3), (0, 3, 10)]:
        with unittest.TestCase().assertRaises((TypeError, ValueError)):
            ScaleStudyConfig(scales=scales).validate()


def test_invalid_resource_bounds_are_rejected():
    for field, value in [
        ("base_units", True), ("base_units", 0), ("degree", 0),
        ("degree", 48), ("probe_steps", 0), ("max_events", 0),
    ]:
        with unittest.TestCase().assertRaises((TypeError, ValueError)):
            ScaleStudyConfig(**{field: value}).validate()


def test_topology_growth_is_linear_not_density_preserving():
    config = ScaleStudyConfig()
    counts = []
    for scale in config.scales:
        edges = build_topology(config, scale)
        units = config.base_units * scale
        assert len(edges) == len(set(edges)) == units * config.degree
        assert all(type(a) is int and type(b) is int for a, b in edges)
        assert all(0 <= a < units and 0 <= b < units and a != b for a, b in edges)
        assert Counter(a for a, _ in edges) == dict.fromkeys(range(units), config.degree)
        assert sum(Counter(b for _, b in edges).values()) / units == config.degree
        counts.append(len(edges))
    assert counts == [counts[0] * scale for scale in config.scales]


def test_every_added_unit_is_reachable_not_disconnected_padding():
    config = ScaleStudyConfig()
    for scale in config.scales:
        graph = defaultdict(list)
        for source, target in build_topology(config, scale):
            graph[source].append(target)
        seen, pending = {0}, [0]
        while pending:
            for target in graph[pending.pop()]:
                if target not in seen:
                    seen.add(target)
                    pending.append(target)
        assert len(seen) == config.base_units * scale


def test_topology_is_deterministic_and_preserves_required_edges():
    config = ScaleStudyConfig()
    required = ((0, 2), (2, 5), (5, 7))
    for scale in config.scales:
        edges = build_topology(config, scale, required_edges=required)
        assert set(required) <= set(edges)
        assert edges == build_topology(config, scale, required_edges=required)
        assert len(edges) == config.base_units * scale * config.degree


def test_overfull_required_degree_fails_instead_of_growing_connectivity():
    config = ScaleStudyConfig()
    required = tuple((0, destination) for destination in range(1, config.degree + 2))
    with unittest.TestCase().assertRaises((TypeError, ValueError)):
        build_topology(config, 1, required_edges=required)


def test_world_evidence_ports_and_readout_are_identical_across_scales():
    config = ScaleStudyConfig()
    worlds = development_worlds(config)
    assert worlds == development_worlds(config)
    assert len(worlds) >= 5
    for world in worlds:
        before = json.dumps(world, sort_keys=True)
        rows = [audit_scale(config, world, scale) for scale in config.scales]
        assert len({row["evidence_hash"] for row in rows}) == 1
        assert all(row["input_ports"] == rows[0]["input_ports"] for row in rows)
        assert all(row["readout_ports"] == rows[0]["readout_ports"] for row in rows)
        assert all(row["formal_execution_allowed"] is False for row in rows)
        assert all(row["comparative_capability_claim_allowed"] is False for row in rows)
        assert all(row["resource_match_passed"] is False for row in rows)
        assert [row["unit_count"] for row in rows] == [config.base_units * s for s in config.scales]
        assert all(row["reachable_unit_count"] == row["unit_count"] for row in rows)
        assert json.dumps(world, sort_keys=True) == before


def test_raw_and_normalized_contamination_are_reconstructible():
    generated, ports, route = (1, 2, 7, 50, 2), tuple(range(10)), (0, 1, 2)
    row = project_behavior(generated, ports, route, 100)
    assert row["generated_units"] == (1, 2, 7, 2)
    assert row["raw_contamination"] == 1
    assert row["contamination_per_active_unit"] == 1 / 4
    assert row["contamination_per_total_unit"] == 1 / 100
    assert row["contamination_per_recovered_route_unit"] == 1 / 2
    assert row["contamination_per_candidate_activity"] == 1 / 4
    assert row["exact_sequence_recovered"] is False


def test_no_output_preserves_undefined_denominators_and_fails_recovery():
    row = project_behavior((), (0, 1, 2), (0, 1, 2), 48)
    assert row["raw_contamination"] == 0
    assert row["contamination_per_active_unit"] is None
    assert row["contamination_per_recovered_route_unit"] is None
    assert row["contamination_per_candidate_activity"] is None
    assert row["ordered_retention"] == 0
    assert row["exact_sequence_recovered"] is False


def test_hidden_activity_does_not_invent_wrong_external_symbols():
    row = project_behavior((47, 45), (0, 1, 2), (0, 1, 2), 48)
    assert row["generated_units"] == ()
    assert row["raw_contamination"] == 0
    assert row["contamination_per_candidate_activity"] is None
    assert row["ordered_retention"] == 0
    assert row["exact_sequence_recovered"] is False


def test_geometry_counts_actual_occupied_units_not_declared_capacity():
    active = ((1, 1, 2), (2, 3), ())
    small = geometry(active, 48)
    large = geometry(active, 480)
    assert small["active_counts"] == large["active_counts"] == (2, 2, 0)
    assert small["unique_occupied_units"] == large["unique_occupied_units"] == 3
    assert small["unique_occupied_fraction"] == 3 / 48
    assert large["unique_occupied_fraction"] == 3 / 480
    assert small["state_reuse_count"] == 1
    assert small["activation_entropy_nats"] == large["activation_entropy_nats"]


def test_unobserved_future_route_cannot_change_topology_silently():
    config = ScaleStudyConfig()
    world = copy.deepcopy(development_worlds(config)[0])
    world["routes"] = world["routes"] + ((35, 34, 33, 32),)
    world["exposures"] = world["exposures"] + (0,)
    # A foreign world with a stale identity must fail before any topology or runtime.
    with unittest.TestCase().assertRaises((TypeError, ValueError)):
        audit_scale(config, world, 1)


def test_tampered_external_schedule_cannot_reuse_evidence_hash():
    config = ScaleStudyConfig()
    world = copy.deepcopy(development_worlds(config)[0])
    world["exposures"] = (world["exposures"][0] + 1,) + world["exposures"][1:]
    with unittest.TestCase().assertRaises((TypeError, ValueError)):
        audit_scale(config, world, 1)


def test_zero_exposure_probe_cannot_add_an_unseen_transition_edge():
    config = ScaleStudyConfig()
    world = copy.deepcopy(development_worlds(config)[0])
    expected = audit_scale(config, world, 1)["topology_hash"]
    world["routes"] = world["routes"] + ((35, 34, 33, 32),)
    world["exposures"] = world["exposures"] + (0,)
    world["evidence_hash"] = digest({k: v for k, v in world.items() if k != "evidence_hash"})
    try:
        actual = audit_scale(config, world, 1)
    except (ValueError, TypeError):
        return  # Current development schema may forbid unseen probes entirely.
    assert actual["topology_hash"] == expected


def test_all_six_cells_are_deterministic_and_probe_learning_is_absent():
    config = ScaleStudyConfig(probe_steps=2)
    world = development_worlds(config)[0]
    rows = []
    for scale in config.scales:
        for architecture in ("field", "reservoir"):
            row = run_development_cell(config, world, scale, architecture)
            assert row == run_development_cell(config, world, scale, architecture)
            assert row["scientific_status"] == "not_evaluated_development_feasibility"
            assert row["audit"]["comparative_capability_claim_allowed"] is False
            for probe in row["probes"]:
                prefix = "connection" if architecture == "field" else "readout"
                assert probe[prefix + "_hash_before_probe"] == probe[prefix + "_hash_after_probe"]
            if architecture == "field":
                assert row["resource"]["changed_hidden_connections"] == 0
                observed = row["resource"]["learning_observe_calls"]
            else:
                observed = row["resource"]["observed_external_event_count"]
            assert observed == row["audit"]["external_observation_count"]
            rows.append(row)
    assert len(rows) == 6
    assert len({row["audit"]["evidence_hash"] for row in rows}) == 1
    for scale in config.scales:
        pair = [row for row in rows if row["audit"]["scale"] == scale]
        assert pair[0]["audit"]["topology_hash"] == pair[1]["audit"]["topology_hash"]


def test_one_event_ceiling_fails_closed_or_reports_budget_exhaustion():
    config = ScaleStudyConfig(max_events=1)
    world = development_worlds(config)[0]
    for architecture in ("field", "reservoir"):
        try:
            row = run_development_cell(config, world, 1, architecture)
        except RuntimeError as error:
            assert "max_events" in str(error) or "max_spikes" in str(error)
            continue
        assert row["complete"] is False
        assert row["audit"]["comparative_capability_claim_allowed"] is False
        for probe in row["probes"]:
            assert probe["halt_reason"] == "event_budget_reached"
            assert len(probe["behavior"]["generated_units"]) <= 1


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(
        unittest.FunctionTestCase(value)
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    )


if __name__ == "__main__":
    unittest.main()

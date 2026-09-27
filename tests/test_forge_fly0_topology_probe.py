from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_topology_probe import (
    Edge,
    Topology,
    build_degree_preserving_rewire,
    build_random_sparse,
    build_structured_topology,
    compare_topologies,
    run_scenario,
)


def test_three_topologies_share_exact_resource_envelope() -> None:
    structured = build_structured_topology()
    rewired = build_degree_preserving_rewire(structured)
    random_sparse = build_random_sparse(structured)

    assert structured.node_count == 128
    assert len(structured.edges) == 512
    assert rewired.resource_signature() == structured.resource_signature()
    assert random_sparse.resource_signature() == structured.resource_signature()


def test_rewired_control_preserves_every_node_degree_but_changes_edges() -> None:
    structured = build_structured_topology()
    rewired = build_degree_preserving_rewire(structured)

    assert rewired.degree_signature() == structured.degree_signature()
    assert set(rewired.edges) != set(structured.edges)


def test_fixed_seeds_produce_deterministic_topology_fingerprints() -> None:
    structured = build_structured_topology()

    assert build_degree_preserving_rewire(structured).fingerprint() == (
        build_degree_preserving_rewire(structured).fingerprint()
    )
    assert build_random_sparse(structured).fingerprint() == build_random_sparse(
        structured
    ).fingerprint()


@pytest.mark.parametrize("side", ["left", "right"])
def test_structured_sensorimotor_pulse_remains_side_specific(side: str) -> None:
    result = run_scenario(build_structured_topology(), side=side)

    assert result.matched_motor_events > 0
    assert result.opposite_motor_events == 0
    assert result.first_matched_motor_time is not None
    assert any(event.role == "modulation" for event in result.trace)
    assert any(event.role == "local" for event in result.trace)


def test_comparison_is_bounded_and_exposes_matched_controls() -> None:
    result = compare_topologies()
    summary = result.summary()

    assert result.degree_preservation is True
    assert len(result.scenarios) == 6
    assert set(summary["topologies"]) == {
        "fly_like_structured",
        "degree_preserving_rewired",
        "random_sparse",
    }
    assert all(scenario.fired_events <= 4096 for scenario in result.scenarios)


def test_topology_rejects_duplicate_and_invalid_edges() -> None:
    topology = build_structured_topology()
    duplicate = topology.edges[0]
    with pytest.raises(ValueError, match="duplicate"):
        replace(topology, edges=topology.edges + (duplicate,))
    with pytest.raises(ValueError, match="self"):
        Topology("invalid", topology.roles, (Edge(0, 0, 1, 1),))


def test_probe_rejects_unbounded_horizon_and_tiny_budget() -> None:
    topology = build_structured_topology()
    with pytest.raises(ValueError, match="horizon"):
        run_scenario(topology, side="left", horizon=33)
    with pytest.raises(ValueError, match="event"):
        run_scenario(topology, side="left", max_fired_events=32)

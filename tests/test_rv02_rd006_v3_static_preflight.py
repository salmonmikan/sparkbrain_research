from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v2 as v2
from sparkbrain.research import rv02_rd006_external_learning_reachability_v3 as v3

ARTIFACT = Path(
    "artifacts/rv02_rd006/"
    "external_learning_reachability_a_v3_structural_temporal_role_preflight/"
    "static_preflight.json"
)


def test_preflight_is_static_only_and_uses_no_observed_artifact(monkeypatch) -> None:
    def forbidden(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("dynamic entrypoint invoked by static preflight")

    for module, names in (
        (v1, ("build_initial_field", "run_arm", "run_cell", "run_matrix")),
        (v2, ("run_cell", "run_matrix")),
    ):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)

    report = v3.build_static_preflight()
    assert report["observed_spike_or_artifact_outcome_used"] is False
    assert report["new_dynamic_execution"] is False
    assert report["new_result_bearing_matrix"] is False
    assert report["capability_scoring"] is False
    assert report["held_out_use"] is False


def test_every_family_has_two_static_paths_at_a_declared_clock() -> None:
    report = v3.build_static_preflight()
    assert report["family_count"] == len(v3.FAMILIES) == 6
    assert report["families_passing"] == 6
    assert report["static_preflight_status"] == "PASS"
    for family in report["families"]:
        assert family["static_acceptance"] == "PASS"
        assert len(family["static_hidden_source_paths"]) >= 2
        assert family["invariants"]["distinct_hidden_source_count"] >= 2
        assert family["invariants"]["all_static_path_edges_present"] is True
        assert family["invariants"]["all_declared_lags_in_fixed_window"] is True
        assert (
            family["invariants"][
                "all_hidden_to_return_edge_delays_in_fixed_window"
            ]
            is True
        )
        assert family["dynamic_reachability_claimed"] is False


def test_resource_route_and_ring_invariants_are_exact() -> None:
    report = v3.build_static_preflight()
    for family in report["families"]:
        invariants = family["invariants"]
        assert invariants["unit_count"] == 48
        assert invariants["total_edge_count"] == 384
        assert invariants["mean_out_degree"] == 8.0
        assert invariants["all_source_outdegrees_exact"] is True
        assert invariants["port_source_edges_preserved"] is True
        assert invariants["route_edges_preserved"] is True
        assert invariants["hidden_ring_edges_preserved"] is True
        assert invariants["no_self_edges"] is True
        assert len(family["added_edges"]) == len(family["removed_edges"])


def test_serialization_and_replay_are_deterministic() -> None:
    first = v3.build_static_preflight()
    second = v3.build_static_preflight()
    first_payload = v3.serialize_static_preflight(first)
    second_payload = v3.serialize_static_preflight(second)
    assert first == second
    assert first_payload == second_payload
    assert v3.replay_static_preflight(first_payload) == first


def test_committed_static_report_matches_the_deterministic_builder() -> None:
    payload = ARTIFACT.read_bytes()
    assert payload == v3.serialize_static_preflight(v3.build_static_preflight())
    assert v3.replay_static_preflight(payload)["static_preflight_status"] == "PASS"


@pytest.mark.parametrize(
    "entrypoint",
    [
        v3.build_initial_field,
        v3.execute_topology,
        v3.run_arm,
        v3.run_cell,
        v3.run_matrix,
    ],
)
def test_dynamic_entrypoints_fail_closed(entrypoint) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(v3.DynamicsExecutionForbidden):
        entrypoint()

from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.research import rv02_rd006_external_learning_reachability_v3 as v3
from sparkbrain.research import rv02_rd006_external_learning_reachability_v4 as v4
from sparkbrain.research import rv02_rd006_external_learning_reachability_v4_d0 as d0


def test_execution_field_matches_frozen_v3_topology_without_dynamics() -> None:
    config = d0.RD006Config()
    for world in d0.development_worlds(config):
        preflight = v3.build_family_preflight(config, world)
        field = d0.build_execution_field(config, world, preflight)
        assert (
            d0.digest(tuple(sorted(field.connections)))
            == preflight["planned_topology_sha256"]
        )
        assert len(field.connections) == 384


def test_fixed_surface_and_config_guard_reject_drift() -> None:
    config = d0.RD006Config()
    d0._assert_fixed_config(config)
    with pytest.raises(ValueError):
        d0._assert_fixed_config(replace(config, threshold=0.51))


def test_on_learner_is_preflighted_v4_implementation() -> None:
    config = d0.RD006Config()
    world = d0.development_worlds(config)[0]
    preflight = v3.build_family_preflight(config, world)
    field = d0.build_execution_field(config, world, preflight)
    learner = v4.PortToHiddenExternalPlasticity(field)
    assert learner.config == d0.v1.DirectFieldPlasticityConfig()
    assert learner.port_to_hidden_update_count == 0


def test_measurement_schema_and_attribution_are_frozen() -> None:
    assert d0.CELL_MEASUREMENT_FIELDS == (
        "completion_status",
        "event_count",
        "spike_count",
        "hidden_spike_count",
        "return_clocks",
        "dynamic_eligible_hidden_sources",
        "maximum_same_clock_source_count",
        "ready_gate_events",
        "ordinary_update_edge_class_counts",
        "prohibited_update_count",
        "new_edge_count",
    )
    assert d0.ANALYST_ALLOCATION_ID.startswith(
        "EVA-20260927T200051+0900-R154"
    )
    assert d0.ANALYST_ATTRIBUTION_ID.startswith(
        "EVA-20260927T210004+0900-R156"
    )


def test_protected_entrypoints_remain_closed() -> None:
    with pytest.raises(v4.PreflightExecutionForbidden):
        d0.score_capability()
    with pytest.raises(v4.PreflightExecutionForbidden):
        d0.load_held_out()


def test_parent_identity_is_exact() -> None:
    assert d0.PARENT_PREFLIGHT_HEAD == (
        "78594102ea03fe3ffc0f6e1e0b8b94dd66351005"
    )
    assert d0.PARENT_PREFLIGHT_TREE == (
        "f41b9bd97630e4822584f3994692eec5d82c66fa"
    )
    assert d0.PROTOCOL_ID.endswith("v4-port-to-hidden-trace-boundary-d0-execution")

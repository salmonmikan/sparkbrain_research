from __future__ import annotations

from types import SimpleNamespace

import pytest

from sparkbrain.research.rv01_r01_16_capability import (
    _behavior_signature,
    _checkpoint_with_arm,
    _prefix_to_distinct_budget,
    _registered_cue_pulse_id,
    _replicated_classification,
    _traversal_metrics,
)
from sparkbrain.research.rv01_r01_16_factorization import ConnectionState


def _checkpoint() -> dict[str, object]:
    return {
        "config": {"sentinel": "unchanged"},
        "connections": [
            {
                "source_id": 0,
                "target_id": 1,
                "weight": 0.5,
                "delay_ms": 4.0,
                "plastic": True,
            },
            {
                "source_id": 1,
                "target_id": 2,
                "weight": 0.6,
                "delay_ms": 5.0,
                "plastic": False,
            },
        ],
        "units": [{"sentinel": 1}],
        "queue": [],
    }


def test_checkpoint_arm_rewrite_changes_only_bound_connection_inventory() -> None:
    checkpoint = _checkpoint()
    arm = (
        ConnectionState(0, 1, 0.1, 7.0, True),
        ConnectionState(1, 2, 0.2, 8.0, False),
    )

    rewritten = _checkpoint_with_arm(checkpoint, arm)

    assert rewritten is not checkpoint
    assert rewritten["config"] == checkpoint["config"]
    assert rewritten["units"] == checkpoint["units"]
    assert rewritten["queue"] == checkpoint["queue"]
    assert rewritten["connections"] == [row.state_dict() for row in arm]
    assert checkpoint["connections"][0]["weight"] == 0.5


def test_checkpoint_arm_rewrite_fails_closed_on_topology_drift() -> None:
    checkpoint = _checkpoint()
    arm = (ConnectionState(0, 1, 0.1, 7.0, True),)

    with pytest.raises(RuntimeError, match="topology"):
        _checkpoint_with_arm(checkpoint, arm)


def test_common_breadth_prefix_uses_distinct_unit_budget() -> None:
    trace = (1, 1, 2, 1, 3, 4)
    assert _prefix_to_distinct_budget(trace, 3) == (1, 1, 2, 1, 3)
    assert _prefix_to_distinct_budget(trace, 0) == ()
    assert _prefix_to_distinct_budget(trace, 5) is None


def test_traversal_metrics_preserve_registered_revisit_definition() -> None:
    metrics = _traversal_metrics((1, 1, 2, 1, 3))
    assert metrics == {
        "event_count": 5,
        "distinct_unit_count": 3,
        "revisit_count": 2,
        "revisit_rate": 0.4,
        "new_state_yield": 0.6,
        "first_visit_positions": [1, 3, 5],
    }


def test_primary_signature_ignores_all_registered_secondary_fields() -> None:
    left = {
        "generated_units": [1, 2, 3],
        "common_breadth_units": [1, 2],
        "generated_times_ms": [101.0, 105.0, 109.0],
        "ordered_retention_fraction": 1.0,
        "exact_route_recovered": True,
        "contamination_count": 0,
        "common_breadth_reached": True,
        "common_breadth_metrics": {"event_count": 2},
    }
    right = {
        **left,
        "generated_times_ms": [101.0, 105.000000000001, 109.0],
        "ordered_retention_fraction": 0.5,
        "exact_route_recovered": False,
        "contamination_count": 4,
        "common_breadth_metrics": {"event_count": 999},
    }

    assert _behavior_signature(left) == _behavior_signature(right)


def test_primary_signature_changes_only_when_registered_sequence_pair_changes() -> None:
    baseline = {
        "generated_units": [1, 2, 3],
        "common_breadth_units": [1, 2],
    }
    changed_full = {**baseline, "generated_units": [1, 3, 2]}
    changed_common = {**baseline, "common_breadth_units": [1, 3]}

    assert _behavior_signature(baseline) != _behavior_signature(changed_full)
    assert _behavior_signature(baseline) != _behavior_signature(changed_common)


def test_registered_cue_identity_is_independent_of_factor_arm() -> None:
    world = SimpleNamespace(world_id="world:test")
    route = SimpleNamespace(route_id="route:test")

    first = _registered_cue_pulse_id(world, route)
    second = _registered_cue_pulse_id(world, route)

    assert first == second == "r01-16:world:test:route:test:fixed-cue"


def test_replicated_classification_requires_two_independent_worlds() -> None:
    result = _replicated_classification(
        [("world:a", "WEIGHT_SUPPORT_CELL"), ("world:a", "WEIGHT_SUPPORT_CELL")],
        support_cell="WEIGHT_SUPPORT_CELL",
        negative_cell="WEIGHT_NEGATIVE_CELL",
        supported="WEIGHT_SUPPORTED",
        unsupported="WEIGHT_UNSUPPORTED",
        mixed="WEIGHT_MIXED",
    )

    assert result["classification"] == "INSUFFICIENT_REACHABLE_REPLICATION"
    assert result["eligible_world_count"] == 1


def test_replicated_classification_is_non_compensatory() -> None:
    result = _replicated_classification(
        [("world:a", "WEIGHT_SUPPORT_CELL"), ("world:b", "WEIGHT_DISCORDANT")],
        support_cell="WEIGHT_SUPPORT_CELL",
        negative_cell="WEIGHT_NEGATIVE_CELL",
        supported="WEIGHT_SUPPORTED",
        unsupported="WEIGHT_UNSUPPORTED",
        mixed="WEIGHT_MIXED",
    )

    assert result["classification"] == "WEIGHT_MIXED"

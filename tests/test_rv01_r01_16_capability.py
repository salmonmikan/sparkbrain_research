from __future__ import annotations

import pytest

from sparkbrain.research.rv01_r01_16_capability import (
    _checkpoint_with_arm,
    _prefix_to_distinct_budget,
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

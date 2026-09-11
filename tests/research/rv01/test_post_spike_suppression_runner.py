from __future__ import annotations

import pytest

from sparkbrain.research.rv01.interference_contract import InterferenceFamily, InterferencePhase
from sparkbrain.research.rv01.post_spike_suppression_contract import (
    R01_15_DEVELOPMENT_SEEDS,
    R01_15_HELD_OUT_SEEDS,
    development_post_spike_suppression_worlds,
    post_spike_suppression_world,
    post_spike_suppression_world_grid_hash,
)
from sparkbrain.research.rv01.post_spike_suppression_runner import (
    run_post_spike_suppression_world,
)


def test_r01_15_world_grid_is_fresh_fixed_and_deterministic() -> None:
    assert R01_15_DEVELOPMENT_SEEDS == (141500, 141501, 141502, 141503, 141504)
    assert R01_15_HELD_OUT_SEEDS == tuple(range(141600, 141610))
    left = development_post_spike_suppression_worlds()
    right = development_post_spike_suppression_worlds()
    assert len(left) == len(tuple(InterferenceFamily)) * 5
    assert [row.state_dict() for row in left] == [row.state_dict() for row in right]
    assert post_spike_suppression_world_grid_hash(left) == (
        post_spike_suppression_world_grid_hash(right)
    )
    assert all(row.phase is InterferencePhase.DEVELOPMENT for row in left)
    assert all(row.unit_count == 96 for row in left)


def test_r01_15_runner_refuses_reserved_held_out_world() -> None:
    world = post_spike_suppression_world(
        InterferencePhase.HELD_OUT,
        InterferenceFamily.DISJOINT_ROUTES,
        R01_15_HELD_OUT_SEEDS[0],
    )
    with pytest.raises(RuntimeError, match="held-out capability execution is sealed"):
        run_post_spike_suppression_world(world)


def test_r01_15_one_development_world_preserves_arm_isolation() -> None:
    world = post_spike_suppression_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.DISJOINT_ROUTES,
        R01_15_DEVELOPMENT_SEEDS[0],
    )
    result = run_post_spike_suppression_world(world)
    assert result["phase"] == "development"
    assert result["held_out_capability_executed"] is False
    assert result["resource_match"]["resource_match_passed"] is True
    assert len(result["probes"]) == world.route_count

    for probe in result["probes"]:
        arms = {row["mode"]: row for row in probe["field_arms"]}
        assert set(arms) == {
            "intact",
            "adaptation_zero",
            "refractory_zero",
            "both_zero",
        }
        assert len({row["checkpoint_hash"] for row in arms.values()}) == 1
        assert len({row["connection_hash_before"] for row in arms.values()}) == 1
        assert all(
            row["connection_hash_before"] == row["connection_hash_after"]
            for row in arms.values()
        )
        assert arms["intact"]["intervention_records"] == []
        assert {
            row["field"] for row in arms["adaptation_zero"]["intervention_records"]
        }.issubset({"adaptation"})
        assert {
            row["field"] for row in arms["refractory_zero"]["intervention_records"]
        }.issubset({"refractory_until_ms"})
        assert {
            row["field"] for row in arms["both_zero"]["intervention_records"]
        }.issubset({"adaptation", "refractory_until_ms"})

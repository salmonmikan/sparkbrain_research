from __future__ import annotations

import pytest

from sparkbrain.research.rv01_r01_17_real_delay import (
    R01_17_DEVELOPMENT_SEEDS,
    R01_17_MIN_CAUSAL_SHIFT_MS,
    R01_17_MIN_DELAY_DISPLACEMENT_MS,
    R01_17_TIMING_TOLERANCE_MS,
    _rewrite_checkpoint_delays,
    build_world_spec,
    prospective_world_specs,
    score_raw_suite,
)


def test_prospective_worlds_are_fixed_distinct_and_nontrivial() -> None:
    rows = prospective_world_specs()

    assert tuple(row.seed for row in rows) == R01_17_DEVELOPMENT_SEEDS
    assert len({row.world_id for row in rows}) == 5
    assert len({row.identity_sha256 for row in rows}) == 5
    assert all(row.initial_delay_ms - row.training_lag_ms >= 1.5 for row in rows)
    assert all(row.initial_delay_ms - row.training_lag_ms <= 2.25 for row in rows)
    assert R01_17_MIN_DELAY_DISPLACEMENT_MS == 0.5
    assert R01_17_MIN_CAUSAL_SHIFT_MS == 0.5
    assert R01_17_TIMING_TOLERANCE_MS == 0.05


def test_world_builder_rejects_unregistered_seed() -> None:
    with pytest.raises(ValueError, match="fixed development namespace"):
        build_world_spec(999999)


def test_delay_rewrite_changes_only_registered_delays() -> None:
    checkpoint = {
        "sentinel": {"unchanged": True},
        "connections": [
            {
                "source_id": 0,
                "target_id": 1,
                "weight": 0.9,
                "delay_ms": 4.0,
                "plastic": True,
            },
            {
                "source_id": 1,
                "target_id": 2,
                "weight": 0.8,
                "delay_ms": 4.1,
                "plastic": True,
            },
        ],
    }

    rewritten = _rewrite_checkpoint_delays(
        checkpoint,
        {(0, 1): 6.0, (1, 2): 6.1},
    )

    assert rewritten is not checkpoint
    assert rewritten["sentinel"] == checkpoint["sentinel"]
    assert rewritten["connections"][0]["weight"] == 0.9
    assert rewritten["connections"][1]["weight"] == 0.8
    assert rewritten["connections"][0]["delay_ms"] == 6.0
    assert rewritten["connections"][1]["delay_ms"] == 6.1
    assert checkpoint["connections"][0]["delay_ms"] == 4.0


def test_delay_rewrite_fails_closed_on_topology_mismatch() -> None:
    checkpoint = {
        "connections": [
            {
                "source_id": 0,
                "target_id": 1,
                "weight": 0.9,
                "delay_ms": 4.0,
                "plastic": True,
            }
        ]
    }

    with pytest.raises(RuntimeError, match="omitted"):
        _rewrite_checkpoint_delays(
            checkpoint,
            {(0, 1): 6.0, (1, 2): 6.1},
        )


def test_scorer_refuses_incomplete_real_grid_without_running_candidate() -> None:
    with pytest.raises(ValueError, match="complete fixed five-cell"):
        score_raw_suite(
            {
                "protocol_id": "rv01-r01-17-real-delay-causal-timing-v1",
                "worlds": [],
            }
        )

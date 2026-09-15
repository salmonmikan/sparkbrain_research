from __future__ import annotations

import pytest

from sparkbrain.research.rv01_r01_17_real_delay import (
    R01_17_DEVELOPMENT_SEEDS,
    R01_17_INITIAL_WEIGHT,
    R01_17_MIN_CAUSAL_SHIFT_MS,
    R01_17_MIN_DELAY_DISPLACEMENT_MS,
    R01_17_TIMING_TOLERANCE_MS,
    _digest,
    _rewrite_checkpoint_delays,
    build_world_spec,
    prospective_world_grid_hash,
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


def _connection_row(
    source: int, target: int, *, weight: float, delay_ms: float
) -> dict[str, object]:
    return {
        "source_id": source,
        "target_id": target,
        "weight": weight,
        "delay_ms": delay_ms,
    }


def _synthetic_complete_raw(
    *,
    disposition_mode: str,
    boundary: bool = False,
) -> dict[str, object]:
    worlds: list[dict[str, object]] = []
    for index, spec in enumerate(prospective_world_specs()):
        eligible = not (disposition_mode == "ineligible" and index == 0)
        support = disposition_mode == "support" or (disposition_mode == "mixed" and index == 0)
        displacement = 0.5 if boundary else (0.75 if eligible else 0.49)
        shift = 0.5 if boundary else (0.75 if support else 0.49)
        pre_rows = [
            _connection_row(
                source,
                target,
                weight=R01_17_INITIAL_WEIGHT,
                delay_ms=spec.initial_delay_ms,
            )
            for source, target in ((0, 1), (1, 2), (2, 3))
        ]
        post_rows = [
            _connection_row(
                source,
                target,
                weight=0.9,
                delay_ms=spec.initial_delay_ms - displacement,
            )
            for source, target in ((0, 1), (1, 2), (2, 3))
        ]
        f0_times = [104.0, 108.0, 112.0]
        fd_times = [value + shift for value in f0_times]

        def arm(
            *,
            source_rows: list[dict[str, object]],
            times: list[float],
            state_hash: str,
        ) -> dict[str, object]:
            connections = [
                _connection_row(
                    int(row["source_id"]),
                    int(row["target_id"]),
                    weight=0.9,
                    delay_ms=float(row["delay_ms"]),
                )
                for row in source_rows
            ]
            return {
                "connection_hash_after": state_hash,
                "connection_hash_before": state_hash,
                "connections": connections,
                "generated_times_ms": times,
                "generated_units": [1, 2, 3],
            }

        worlds.append(
            {
                "arms": {
                    "F0": arm(source_rows=post_rows, times=f0_times, state_hash="post"),
                    "FD": arm(source_rows=pre_rows, times=fd_times, state_hash="pre"),
                    "SHAM": arm(source_rows=post_rows, times=f0_times, state_hash="post"),
                },
                "learner_api_hash": "synthetic-api",
                "post_training_connections": post_rows,
                "pre_training_connections": pre_rows,
                "spec": spec.state_dict(),
                "training_exposures": [],
            }
        )
    payload: dict[str, object] = {
        "formal_authority": False,
        "held_out_authority": False,
        "phase": "development",
        "protocol_id": "rv01-r01-17-real-delay-causal-timing-v1",
        "python_runtime": "synthetic-test",
        "source_git_sha": "0" * 40,
        "world_grid_sha256": prospective_world_grid_hash(),
        "worlds": worlds,
    }
    payload["raw_suite_sha256"] = _digest(worlds)
    return payload


@pytest.mark.parametrize(
    ("mode", "expected"),
    (
        ("support", "SUPPORTED_REAL_DELAY_CAUSAL_TIMING"),
        ("negative", "UNSUPPORTED_REAL_DELAY_CAUSAL_TIMING"),
        ("mixed", "MIXED_REAL_DELAY_CAUSAL_TIMING"),
        ("ineligible", "INSUFFICIENT_REAL_DELAY_CONSTRUCTION"),
    ),
)
def test_frozen_scorer_covers_all_aggregate_outcomes(mode: str, expected: str) -> None:
    scored = score_raw_suite(_synthetic_complete_raw(disposition_mode=mode))
    assert scored["classification"] == expected


def test_frozen_scorer_accepts_exact_preregistered_half_ms_boundaries() -> None:
    scored = score_raw_suite(_synthetic_complete_raw(disposition_mode="support", boundary=True))
    assert scored["classification"] == "SUPPORTED_REAL_DELAY_CAUSAL_TIMING"
    assert all(row["disposition"] == "REAL_DELAY_SUPPORT_CELL" for row in scored["scored_worlds"])

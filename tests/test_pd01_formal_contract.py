from __future__ import annotations

import pytest

from sparkbrain.external_validation.fading_memory import (
    DeterministicReservoir,
    PD01ScoreRow,
    PD01WorldConfig,
    ReservoirConfig,
    build_pd01_inputs,
    build_pd01_targets,
    classify_pd01_terminal,
    fit_ridge_readout,
    pd01_primary_statistics,
    predict_ridge,
    run_reservoir_probe_features,
    run_v04_probe_features,
)


def test_reservoir_is_deterministic_contractive_and_reset_per_history() -> None:
    config = ReservoirConfig()
    first = DeterministicReservoir(config)
    second = DeterministicReservoir(config)
    history = ((1.0, 0.0), (0.4, 0.4), (0.75, 0.75))

    assert first.run(history) == second.run(history)
    assert first.run(history) == first.run(history)
    assert len(first.run(history)) == 64
    assert first.recurrent_row_l1_sums == pytest.approx((0.90,) * 64)


def test_world_inventory_targets_and_recent_matching_are_fixed() -> None:
    config = PD01WorldConfig(dev_worlds=2, test_worlds=3)
    inputs = build_pd01_inputs("TEST", config)
    targets = build_pd01_targets("TEST", config)

    assert len(inputs) == 3 * 4 * 2
    assert len(targets) == len(inputs)
    assert {row.history_id for row in inputs} == {row.history_id for row in targets}

    world_zero = [row for row in inputs if row.base_world_id == 0]
    by_lag_member = {
        (row.lag, row.history_id.rsplit("m", 1)[1]): row for row in world_zero
    }
    for lag in config.lag_grid:
        left = by_lag_member[(lag, "0")]
        right = by_lag_member[(lag, "1")]
        assert left.observations[1:] == right.observations[1:]
        assert left.observations[-9:-1] == right.observations[-9:-1]
    assert by_lag_member[(16, "0")].observations[-17:-1] == (
        by_lag_member[(128, "0")].observations[-17:-1]
    )


def test_equal_probe_feature_width_and_v04_determinism() -> None:
    history = ((1.0, 0.0), (0.3, 0.3), (0.4, 0.4), (0.75, 0.75))
    v04_a = run_v04_probe_features(history)
    v04_b = run_v04_probe_features(history)
    reservoir = run_reservoir_probe_features(history)

    assert len(v04_a) == len(v04_b) == len(reservoir) == 64
    assert v04_a == v04_b


def test_fixed_ridge_readout_has_no_selection_loop() -> None:
    features = ((-2.0,), (-1.0,), (1.0,), (2.0,))
    labels = (-1, -1, 1, 1)
    weights = fit_ridge_readout(features, labels)

    assert predict_ridge((-1.5,), weights) < 0.0
    assert predict_ridge((1.5,), weights) > 0.0


def test_cluster_bootstrap_and_terminal_rules_are_deterministic() -> None:
    rows = []
    for base_world_id in range(6):
        for lag in (64, 128):
            for target in (-1, 1):
                rows.append(
                    PD01ScoreRow(
                        base_world_id=base_world_id,
                        lag=lag,
                        candidate_score=float(target),
                        comparator_score=float(-target),
                        target=target,
                    )
                )
    stats = pd01_primary_statistics(rows, resamples=100, seed=19901)

    assert stats["candidate_accuracy"] == 1.0
    assert stats["comparator_accuracy"] == 0.0
    assert stats["effect"] == 1.0
    assert classify_pd01_terminal(stats) == "PASS_SURVIVES_FADING_MEMORY_REDUCTION"

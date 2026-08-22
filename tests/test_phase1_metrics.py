from __future__ import annotations

import pytest

from sparkbrain.evaluation.bootstrap import percentile_interval
from sparkbrain.evaluation.metrics import (
    brier_score,
    expected_calibration_error,
    pareto_rows,
    quantiles,
)


def test_brier_score_hand_computed() -> None:
    # (0.2-0)^2 + (0.8-1)^2 = 0.08
    assert brier_score([{"cat": 0.8, "dog": 0.2}], ["cat"]) == pytest.approx(0.08)
    assert brier_score([], []) is None


def test_ece_hand_computed_single_bin() -> None:
    # accuracy=.5, confidence=.75 => .25
    assert expected_calibration_error([0.75, 0.75], [True, False], bins=1) == pytest.approx(0.25)
    assert expected_calibration_error([], []) is None


def test_quantiles_hand_computed_nearest_rank() -> None:
    result = quantiles([1.0, 2.0, 3.0, 4.0])
    assert result == {"mean": 2.5, "p50": 2.0, "p95": 4.0, "p99": 4.0, "max": 4.0}


def test_bootstrap_is_seed_deterministic() -> None:
    assert percentile_interval([1.0, 2.0, 3.0], seed=7, samples=100) == percentile_interval(
        [1.0, 2.0, 3.0], seed=7, samples=100
    )


def test_pareto_marks_known_dominated_row() -> None:
    rows = [
        {
            "condition": "strong",
            "unnecessary_revision_rate": 0.1,
            "revision_recall": 0.9,
            "mean_switch_latency": 1.0,
        },
        {
            "condition": "weak",
            "unnecessary_revision_rate": 0.2,
            "revision_recall": 0.8,
            "mean_switch_latency": 2.0,
        },
    ]
    result = {row["condition"]: row for row in pareto_rows(rows)}
    assert result["strong"]["dominated"] is False
    assert result["weak"]["dominated_by"] == ["strong"]

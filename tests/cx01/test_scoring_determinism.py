from __future__ import annotations

from sparkbrain.comparison.cx01.scoring import brier_score, cross_entropy


def test_distribution_metrics_ignore_mapping_insertion_order() -> None:
    expected_a = {"z": 0.2, "a": 0.5, "m": 0.3}
    expected_b = {"m": 0.3, "z": 0.2, "a": 0.5}
    observed_a = {"a": 0.45, "m": 0.35, "z": 0.20}
    observed_b = {"z": 0.20, "a": 0.45, "m": 0.35}

    assert brier_score(expected_a, observed_a) == brier_score(expected_b, observed_b)
    assert cross_entropy(expected_a, observed_a) == cross_entropy(expected_b, observed_b)

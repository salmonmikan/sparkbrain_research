from __future__ import annotations

import math

import pytest

from sparkbrain.evaluation.ni01 import (
    ScoredStep,
    comparator_decision,
    coverage_matched_threshold,
    selective_decision_loss,
    summarize_effect,
    type7_quantile,
)


def test_coverage_matched_threshold_is_target_free_and_conservative_on_ties() -> None:
    threshold = coverage_matched_threshold([True, False], [0.8, 0.6])
    assert threshold == 0.8


def test_comparator_decision_uses_canonical_label_order_for_exact_ties() -> None:
    assert comparator_decision([0.5, 0.5, 0.0], ["CAT", "TOY", "OTHER"], 0.4) == "CAT"
    assert comparator_decision([0.5, 0.5, 0.0], ["CAT", "TOY", "OTHER"], 0.6) is None


def test_selective_decision_loss_matches_frozen_contract() -> None:
    assert selective_decision_loss(None, truth="CAT", decision_justified=False) == 0.0
    assert selective_decision_loss("CAT", truth="CAT", decision_justified=False) == 1.0
    assert selective_decision_loss("CAT", truth="CAT", decision_justified=True) == 0.0
    assert selective_decision_loss(None, truth="CAT", decision_justified=True) == 0.5
    assert selective_decision_loss("TOY", truth="CAT", decision_justified=True) == 1.0


def test_type7_quantile_uses_linear_interpolation() -> None:
    assert type7_quantile([0.0, 10.0], 0.25) == pytest.approx(2.5)


def test_summarize_effect_clusters_by_episode_and_equal_weights_worlds() -> None:
    rows = [
        ScoredStep("w1", "a", 0.0, 0.2),
        ScoredStep("w1", "a", 0.0, 0.2),
        ScoredStep("w1", "b", 0.2, 0.4),
        ScoredStep("w1", "b", 0.2, 0.4),
        ScoredStep("w2", "c", 0.4, 0.5),
        ScoredStep("w2", "c", 0.4, 0.5),
        ScoredStep("w2", "d", 0.6, 0.7),
        ScoredStep("w2", "d", 0.6, 0.7),
    ]
    summary = summarize_effect(
        rows,
        worlds=["w1", "w2"],
        episodes_per_world=2,
        steps_per_episode=2,
        resamples=100,
        seed=7,
    )
    assert summary.candidate_loss == pytest.approx(0.3)
    assert summary.comparator_loss == pytest.approx(0.45)
    assert summary.effect == pytest.approx(0.15)
    assert summary.world_effects == pytest.approx({"w1": 0.2, "w2": 0.1})
    assert math.isfinite(summary.ci95_lower)
    assert math.isfinite(summary.ci95_upper)
    assert summary.ci95_lower <= summary.ci95_upper

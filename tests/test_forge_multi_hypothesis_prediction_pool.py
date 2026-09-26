import pytest

from forge_prototypes.multi_hypothesis_prediction_pool import (
    MultiHypothesisPredictionPool,
    PredictionPoolConfig,
)
from sparkbrain.v05.contracts import AssemblyActivation
from sparkbrain.v05.prediction import AssemblyPredictor


def _activation(*, mature: bool = True) -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id="assembly-0001",
        pattern_id="pattern-a",
        time_ms=10.0,
        similarity=0.9,
        occurrences=4,
        episode_count=4,
        mature=mature,
        unit_ids=(1, 2, 3),
    )


def test_ambiguous_predictions_are_retained_but_abstain() -> None:
    predictor = AssemblyPredictor(counts={"assembly-0001": {"later-a": 5, "later-b": 5}})
    snapshot = MultiHypothesisPredictionPool(predictor).inspect(_activation())
    assert snapshot.abstained is True
    assert snapshot.reason == "low_confidence"
    assert snapshot.selected_value is None
    assert [row.value for row in snapshot.hypotheses] == ["later-a", "later-b"]
    assert [row.probability for row in snapshot.hypotheses] == [0.5, 0.5]
    assert snapshot.margin == 0.0


def test_clear_prediction_can_be_selected_without_mutating_predictor() -> None:
    predictor = AssemblyPredictor(counts={"assembly-0001": {"later-a": 8, "later-b": 2}})
    before = predictor.state_dict()
    probe = MultiHypothesisPredictionPool(
        predictor,
        PredictionPoolConfig(min_confidence=0.6, min_margin=0.2),
    )
    snapshot = probe.inspect(_activation())
    assert snapshot.abstained is False
    assert snapshot.reason == "selected"
    assert snapshot.selected_value == "later-a"
    assert snapshot.confidence == 0.8
    assert snapshot.margin == pytest.approx(0.6)
    assert predictor.state_dict() == before


def test_sparse_prediction_abstains_for_insufficient_observations() -> None:
    predictor = AssemblyPredictor(counts={"assembly-0001": {"later-a": 1}})
    snapshot = MultiHypothesisPredictionPool(predictor).inspect(_activation())
    assert snapshot.abstained is True
    assert snapshot.reason == "insufficient_observations"
    assert snapshot.hypotheses[0].value == "later-a"
    assert snapshot.confidence == 1.0


def test_immature_activation_never_exposes_prediction_pool() -> None:
    predictor = AssemblyPredictor(counts={"assembly-0001": {"later-a": 9, "later-b": 1}})
    snapshot = MultiHypothesisPredictionPool(predictor).inspect(_activation(mature=False))
    assert snapshot.abstained is True
    assert snapshot.reason == "inactive_or_immature"
    assert snapshot.hypotheses == ()

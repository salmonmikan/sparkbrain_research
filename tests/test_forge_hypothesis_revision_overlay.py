import json

import pytest

from forge_prototypes.hypothesis_revision_overlay import HypothesisRevisionOverlay
from forge_prototypes.multi_hypothesis_prediction_pool import MultiHypothesisPredictionPool
from sparkbrain.v05.contracts import AssemblyActivation
from sparkbrain.v05.prediction import AssemblyPredictor


def _activation() -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id="assembly-0001",
        pattern_id="pattern-a",
        time_ms=10.0,
        similarity=0.9,
        occurrences=4,
        episode_count=4,
        mature=True,
        unit_ids=(1, 2, 3),
    )


def _snapshot(counts: dict[str, int]):
    predictor = AssemblyPredictor(counts={"assembly-0001": counts})
    before = predictor.state_dict()
    snapshot = MultiHypothesisPredictionPool(predictor).inspect(_activation())
    assert predictor.state_dict() == before
    return predictor, snapshot


def test_late_evidence_can_resolve_a_retained_tie_without_mutating_predictor() -> None:
    predictor, base = _snapshot({"later-a": 5, "later-b": 5})
    before = predictor.state_dict()
    assert base.abstained is True
    assert base.selected_value is None

    overlay = HypothesisRevisionOverlay()
    revised = overlay.apply_evidence(base, value="later-a", strength=1.0)

    assert revised.abstained is False
    assert revised.selected_value == "later-a"
    assert revised.confidence > 0.73
    assert revised.margin > 0.46
    assert predictor.state_dict() == before
    assert [row.base_probability for row in revised.hypotheses] == [0.5, 0.5]


def test_balanced_late_evidence_restores_abstention_instead_of_overwriting_history() -> None:
    _, base = _snapshot({"later-a": 5, "later-b": 5})
    overlay = HypothesisRevisionOverlay()
    overlay.apply_evidence(base, value="later-a", strength=1.0)
    revised = overlay.apply_evidence(base, value="later-b", strength=1.0)

    assert revised.abstained is True
    assert revised.selected_value is None
    assert revised.reason == "ambiguous_after_revision"
    assert revised.evidence_count == 2
    assert {row.cumulative_support for row in revised.hypotheses} == {1.0}


def test_overlay_state_is_json_serializable_and_replayable() -> None:
    _, base = _snapshot({"later-a": 5, "later-b": 5})
    overlay = HypothesisRevisionOverlay()
    expected = overlay.apply_evidence(base, value="later-a", strength=0.75)

    payload = json.loads(json.dumps(overlay.state_dict()))
    restored = HypothesisRevisionOverlay.from_state_dict(payload)

    assert restored.evaluate(base).as_dict() == expected.as_dict()


def test_late_evidence_does_not_override_insufficient_base_observations() -> None:
    _, base = _snapshot({"later-a": 1})
    assert base.reason == "insufficient_observations"

    overlay = HypothesisRevisionOverlay()
    revised = overlay.apply_evidence(base, value="later-a", strength=1.0)

    assert revised.abstained is True
    assert revised.reason == "base_insufficient_observations"
    assert revised.selected_value is None


def test_unknown_evidence_value_fails_closed() -> None:
    _, base = _snapshot({"later-a": 5, "later-b": 5})
    with pytest.raises(ValueError, match="must already exist"):
        HypothesisRevisionOverlay().apply_evidence(
            base,
            value="hidden-answer",
            strength=1.0,
        )

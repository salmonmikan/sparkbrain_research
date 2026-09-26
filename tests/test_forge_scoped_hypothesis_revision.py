import json

from forge_prototypes.hypothesis_revision_overlay import HypothesisRevisionOverlay
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.scoped_hypothesis_revision import ScopedHypothesisRevisionOverlay


def base(assembly_id: str, second: str = "later-b") -> PredictionPoolSnapshot:
    rows = (
        WeightedHypothesis("later-a", 5, 0.5),
        WeightedHypothesis(second, 5, 0.5),
    )
    return PredictionPoolSnapshot(
        assembly_id, rows, None, 0.5, 0.0, True, "low_confidence"
    )


def test_unscoped_state_leaks_between_assemblies_with_same_labels() -> None:
    overlay = HypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), value="later-a")
    leaked = overlay.evaluate(base("assembly-2"))
    assert leaked.selected_value == "later-a"


def test_scoped_state_blocks_cross_assembly_leakage() -> None:
    overlay = ScopedHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), value="later-a")
    untouched = overlay.evaluate(base("assembly-2"))
    assert untouched.abstained is True
    assert untouched.selected_value is None


def test_changed_hypothesis_set_does_not_reactivate_old_support() -> None:
    overlay = ScopedHypothesisRevisionOverlay()
    original = base("assembly-1")
    changed = base("assembly-1", "later-c")
    overlay.apply_evidence(original, value="later-a")
    assert overlay.evaluate(changed).abstained is True
    assert overlay.evaluate(changed).selected_value is None


def test_scope_state_is_json_replayable() -> None:
    overlay = ScopedHypothesisRevisionOverlay()
    original = base("assembly-1")
    expected = overlay.apply_evidence(original, value="later-a", strength=0.75)
    restored = ScopedHypothesisRevisionOverlay.from_state_dict(
        json.loads(json.dumps(overlay.state_dict()))
    )
    assert restored.evaluate(original).as_dict() == expected.as_dict()
    assert restored.evaluate(base("assembly-2")).abstained is True

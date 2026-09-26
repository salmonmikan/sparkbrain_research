import json

from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.scoped_hypothesis_revision import ScopedHypothesisRevisionOverlay
from forge_prototypes.stable_scope_hypothesis_revision import (
    StableScopeHypothesisRevisionOverlay,
)


def base(assembly_id: str, second: str = "later-b") -> PredictionPoolSnapshot:
    rows = (
        WeightedHypothesis("later-a", 5, 0.5),
        WeightedHypothesis(second, 5, 0.5),
    )
    return PredictionPoolSnapshot(
        assembly_id, rows, None, 0.5, 0.0, True, "low_confidence"
    )


def test_hypothesis_set_scope_fragments_support_when_pool_changes() -> None:
    overlay = ScopedHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), value="later-a")
    changed = overlay.evaluate(base("assembly-1", "later-c"))
    assert changed.abstained is True
    assert changed.selected_value is None


def test_stable_scope_preserves_common_hypothesis_support_across_pool_change() -> None:
    overlay = StableScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    changed = overlay.evaluate(base("assembly-1", "later-c"), scope_token="ctx-1")
    assert changed.abstained is False
    assert changed.selected_value == "later-a"


def test_stable_scope_isolates_new_context_on_same_assembly() -> None:
    overlay = StableScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    untouched = overlay.evaluate(base("assembly-1"), scope_token="ctx-2")
    assert untouched.abstained is True
    assert untouched.selected_value is None


def test_stable_scope_isolates_same_context_token_across_assemblies() -> None:
    overlay = StableScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    untouched = overlay.evaluate(base("assembly-2"), scope_token="ctx-1")
    assert untouched.abstained is True
    assert untouched.selected_value is None


def test_scope_token_defines_evidence_lifetime_across_temporary_absence() -> None:
    overlay = StableScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    no_a = PredictionPoolSnapshot(
        "assembly-1",
        (WeightedHypothesis("later-c", 5, 0.5), WeightedHypothesis("later-d", 5, 0.5)),
        None,
        0.5,
        0.0,
        True,
        "low_confidence",
    )
    assert overlay.evaluate(no_a, scope_token="ctx-1").abstained is True
    restored = overlay.evaluate(base("assembly-1"), scope_token="ctx-1")
    assert restored.selected_value == "later-a"


def test_stable_scope_state_is_json_replayable() -> None:
    overlay = StableScopeHypothesisRevisionOverlay()
    expected = overlay.apply_evidence(
        base("assembly-1"), scope_token="ctx-1", value="later-a", strength=0.75
    )
    restored = StableScopeHypothesisRevisionOverlay.from_state_dict(
        json.loads(json.dumps(overlay.state_dict()))
    )
    assert (
        restored.evaluate(base("assembly-1"), scope_token="ctx-1").as_dict()
        == expected.as_dict()
    )
    assert restored.evaluate(base("assembly-1"), scope_token="ctx-2").abstained is True

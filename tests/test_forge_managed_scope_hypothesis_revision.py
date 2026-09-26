import json

import pytest

from forge_prototypes.managed_scope_hypothesis_revision import (
    ManagedScopeHypothesisRevisionOverlay,
)
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)


def base(assembly_id: str) -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        assembly_id,
        (
            WeightedHypothesis("later-a", 5, 0.5),
            WeightedHypothesis("later-b", 5, 0.5),
        ),
        None,
        0.5,
        0.0,
        True,
        "low_confidence",
    )


def test_close_scope_discards_support_and_tombstones_token() -> None:
    overlay = ManagedScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    assert overlay.close_scope(assembly_id="assembly-1", scope_token="ctx-1") is True

    with pytest.raises(ValueError, match="scope token is closed"):
        overlay.evaluate(base("assembly-1"), scope_token="ctx-1")


def test_fresh_token_after_close_starts_clean_then_can_learn() -> None:
    overlay = ManagedScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    overlay.close_scope(assembly_id="assembly-1", scope_token="ctx-1")

    clean = overlay.evaluate(base("assembly-1"), scope_token="ctx-2")
    assert clean.abstained is True

    learned = overlay.apply_evidence(
        base("assembly-1"), scope_token="ctx-2", value="later-b"
    )
    assert learned.selected_value == "later-b"


def test_close_is_scoped_by_assembly_even_for_same_token() -> None:
    overlay = ManagedScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    other = overlay.apply_evidence(
        base("assembly-2"), scope_token="ctx-1", value="later-b"
    )

    overlay.close_scope(assembly_id="assembly-1", scope_token="ctx-1")

    with pytest.raises(ValueError):
        overlay.evaluate(base("assembly-1"), scope_token="ctx-1")
    assert (
        overlay.evaluate(base("assembly-2"), scope_token="ctx-1").as_dict()
        == other.as_dict()
    )


def test_closed_scope_tombstone_is_json_replayable() -> None:
    overlay = ManagedScopeHypothesisRevisionOverlay()
    overlay.apply_evidence(base("assembly-1"), scope_token="ctx-1", value="later-a")
    overlay.close_scope(assembly_id="assembly-1", scope_token="ctx-1")

    restored = ManagedScopeHypothesisRevisionOverlay.from_state_dict(
        json.loads(json.dumps(overlay.state_dict()))
    )

    with pytest.raises(ValueError, match="scope token is closed"):
        restored.evaluate(base("assembly-1"), scope_token="ctx-1")
    assert restored.evaluate(base("assembly-1"), scope_token="ctx-2").abstained is True

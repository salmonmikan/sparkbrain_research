import inspect
import json

import pytest

from forge_prototypes.internal_scope_allocator import (
    InternallyScopedHypothesisRevision,
    InternalScopeAllocator,
    InternalScopeAllocatorConfig,
    ScopeBudgetExceeded,
)
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)


def base() -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        "assembly-1",
        (
            WeightedHypothesis("later-a", 5, 1 / 3),
            WeightedHypothesis("later-b", 5, 1 / 3),
            WeightedHypothesis("later-c", 5, 1 / 3),
        ),
        None,
        1 / 3,
        0.0,
        True,
        "low_confidence",
    )


def test_api_has_no_caller_supplied_scope_or_privileged_label() -> None:
    parameters = set(inspect.signature(InternalScopeAllocator.observe).parameters)
    assert parameters == {"self", "observation", "prediction_error"}
    forbidden = {"scope", "episode", "regime", "entity", "target", "truth", "evaluator"}
    assert not parameters & forbidden


def test_appearance_only_change_reuses_scope() -> None:
    allocator = InternalScopeAllocator()
    first = allocator.observe([0.0, 0.0], prediction_error=0.8)
    shifted = allocator.observe([0.1, -0.1], prediction_error=0.1)

    assert first.action == "created"
    assert shifted.action == "reused"
    assert shifted.scope_token == first.scope_token


def test_identifiable_change_creates_scope_and_return_reuses_prior_scope() -> None:
    allocator = InternalScopeAllocator()
    original = allocator.observe([0.0, 0.0], prediction_error=0.7)
    changed = allocator.observe([2.0, 2.0], prediction_error=0.9)
    returned = allocator.observe([0.05, -0.05], prediction_error=0.2)

    assert changed.action == "created"
    assert changed.scope_token != original.scope_token
    assert returned.action == "reused"
    assert returned.scope_token == original.scope_token


def test_non_identifiable_change_abstains_without_creating_scope() -> None:
    allocator = InternalScopeAllocator()
    first = allocator.observe([0.0, 0.0], prediction_error=0.8)
    ambiguous = allocator.observe([2.0, 2.0], prediction_error=0.1)
    returned = allocator.observe([0.0, 0.0], prediction_error=0.0)

    assert ambiguous.action == "abstained"
    assert ambiguous.scope_token is None
    assert returned.scope_token == first.scope_token
    assert len(allocator.state_dict()["scopes"]) == 1


def test_scope_budget_fails_explicitly_without_eviction() -> None:
    allocator = InternalScopeAllocator(InternalScopeAllocatorConfig(max_scopes=2))
    allocator.observe([0.0], prediction_error=1.0)
    allocator.observe([2.0], prediction_error=1.0)

    with pytest.raises(ScopeBudgetExceeded, match="will not silently evict"):
        allocator.observe([4.0], prediction_error=1.0)

    assert [row["scope_token"] for row in allocator.state_dict()["scopes"]] == [
        "scope-00000001",
        "scope-00000002",
    ]


def test_internal_scope_revision_keeps_three_hypotheses_and_abstains_cleanly() -> None:
    revision = InternallyScopedHypothesisRevision()
    first = revision.apply_evidence(
        base(),
        observation=[0.0, 0.0],
        prediction_error=0.8,
        value="later-b",
    )
    learned = revision.apply_evidence(
        base(),
        observation=[0.05, 0.05],
        prediction_error=0.2,
        value="later-b",
    )
    ambiguous = revision.evaluate(
        base(),
        observation=[2.0, 2.0],
        prediction_error=0.1,
    )

    assert learned.revision is not None
    assert learned.revision.selected_value == "later-b"
    assert learned.allocation.scope_token == first.allocation.scope_token
    assert len(learned.revision.hypotheses) == 3
    assert ambiguous.allocation.action == "abstained"
    assert ambiguous.revision is None


def test_checkpoint_roundtrip_preserves_allocator_and_revision_state() -> None:
    revision = InternallyScopedHypothesisRevision()
    first = revision.apply_evidence(
        base(),
        observation=[0.0, 0.0],
        prediction_error=0.8,
        value="later-c",
    )
    revision.apply_evidence(
        base(),
        observation=[0.05, 0.05],
        prediction_error=0.2,
        value="later-c",
    )
    revision.evaluate(base(), observation=[2.0, 2.0], prediction_error=0.9)

    restored = InternallyScopedHypothesisRevision.from_state_dict(
        json.loads(json.dumps(revision.state_dict()))
    )
    returned = restored.evaluate(
        base(),
        observation=[0.05, 0.05],
        prediction_error=0.2,
    )

    assert returned.allocation.scope_token == first.allocation.scope_token
    assert returned.revision is not None
    assert returned.revision.selected_value == "later-c"
    assert restored.state_dict() == json.loads(json.dumps(restored.state_dict()))

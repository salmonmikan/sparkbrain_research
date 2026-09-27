import inspect
import json

from forge_prototypes.hypothesis_revision_overlay import RevisionOverlayConfig
from forge_prototypes.internal_scope_allocator import InternalScopeAllocatorConfig
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.plural_scope_posterior import NEW_SCOPE, ScopePosteriorConfig
from forge_prototypes.plural_scope_revision_bridge import PluralScopeRevisionBridge


def base() -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        "assembly-1",
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


def test_api_has_no_privileged_scope_identity_inputs() -> None:
    parameters = set(inspect.signature(PluralScopeRevisionBridge.apply_evidence).parameters)
    forbidden = {"scope", "episode", "regime", "entity", "target", "truth", "evaluator"}
    assert not parameters & forbidden


def test_bootstrap_mints_scope_and_applies_late_evidence() -> None:
    bridge = PluralScopeRevisionBridge()
    result = bridge.apply_evidence(
        base(), observation=[0.0], prediction_error=1.0, value="later-b"
    )

    assert result.routing.selected_scope == NEW_SCOPE
    assert result.allocation is not None
    assert result.allocation.action == "created"
    assert result.action == "applied_created"
    assert result.revision is not None
    assert result.revision.selected_value == "later-b"


def test_ambiguous_scope_route_does_not_mutate_any_state() -> None:
    bridge = PluralScopeRevisionBridge(
        router_config=ScopePosteriorConfig(min_selected_mass=0.4, min_margin=0.2)
    )
    bridge.apply_evidence(
        base(), observation=[0.0], prediction_error=1.0, value="later-a"
    )
    bridge.apply_evidence(
        base(), observation=[2.0], prediction_error=1.0, value="later-b"
    )
    before = json.loads(json.dumps(bridge.state_dict()))

    result = bridge.apply_evidence(
        base(), observation=[1.0], prediction_error=0.0, value="later-a"
    )

    assert result.action == "routing_abstained"
    assert result.revision is None
    assert bridge.state_dict() == before


def test_clear_return_reuses_existing_scope_and_revises_it() -> None:
    bridge = PluralScopeRevisionBridge()
    first = bridge.apply_evidence(
        base(), observation=[0.0], prediction_error=1.0, value="later-a"
    )
    bridge.apply_evidence(
        base(), observation=[2.0], prediction_error=1.0, value="later-b"
    )

    returned = bridge.apply_evidence(
        base(), observation=[0.05], prediction_error=0.05, value="later-a"
    )

    assert returned.routing.selected_scope == first.allocation.scope_token
    assert returned.allocation is not None
    assert returned.allocation.action == "reused"
    assert returned.action == "applied_existing"
    assert returned.revision is not None
    assert returned.revision.selected_value == "later-a"


def test_new_scope_confirmation_delays_revision_until_commit() -> None:
    bridge = PluralScopeRevisionBridge(
        allocator_config=InternalScopeAllocatorConfig(create_confirmation_count=2)
    )
    bridge.apply_evidence(
        base(), observation=[0.0], prediction_error=1.0, value="later-a"
    )

    pending = bridge.apply_evidence(
        base(), observation=[2.0], prediction_error=1.0, value="later-b"
    )
    committed = bridge.apply_evidence(
        base(), observation=[2.1], prediction_error=1.0, value="later-b"
    )

    assert pending.action == "pending"
    assert pending.revision is None
    assert committed.action == "applied_created"
    assert committed.allocation is not None
    assert committed.allocation.reason == "confirmed_mismatch"
    assert committed.revision is not None
    assert committed.revision.selected_value == "later-b"


def test_router_allocator_disagreement_rolls_back_before_revision() -> None:
    bridge = PluralScopeRevisionBridge()
    bridge.apply_evidence(
        base(), observation=[0.0], prediction_error=1.0, value="later-a"
    )
    before = json.loads(json.dumps(bridge.state_dict()))

    conflict = bridge.apply_evidence(
        base(), observation=[0.05], prediction_error=1.0, value="later-b"
    )

    assert conflict.routing.selected_scope == NEW_SCOPE
    assert conflict.allocation is not None
    assert conflict.allocation.action == "reused"
    assert conflict.action == "routing_commit_conflict"
    assert conflict.revision is None
    assert bridge.state_dict() == before


def test_checkpoint_roundtrip_preserves_routing_and_revision() -> None:
    bridge = PluralScopeRevisionBridge(
        revision_config=RevisionOverlayConfig(min_confidence=0.6, min_margin=0.2)
    )
    bridge.apply_evidence(
        base(), observation=[0.0], prediction_error=1.0, value="later-b"
    )
    state = json.loads(json.dumps(bridge.state_dict()))
    restored = PluralScopeRevisionBridge.from_state_dict(state)

    left = bridge.evaluate(base(), observation=[0.05], prediction_error=0.05)
    right = restored.evaluate(base(), observation=[0.05], prediction_error=0.05)

    assert left == right
    assert restored.state_dict() == state

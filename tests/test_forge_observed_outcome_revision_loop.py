import inspect
import json

import pytest

from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.observed_outcome_revision_loop import ObservedOutcomeRevisionLoop


def base(
    first_probability: float = 0.5, second_probability: float = 0.5
) -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        "assembly-1",
        (
            WeightedHypothesis("later-a", 5, first_probability),
            WeightedHypothesis("later-b", 5, second_probability),
        ),
        None,
        max(first_probability, second_probability),
        abs(first_probability - second_probability),
        True,
        "low_confidence",
    )


def test_public_mutation_api_has_no_caller_error_or_scope_identity() -> None:
    parameters = set(
        inspect.signature(ObservedOutcomeRevisionLoop.apply_observed_outcome).parameters
    )
    forbidden = {
        "prediction_error",
        "scope",
        "episode",
        "regime",
        "entity",
        "target",
        "truth",
        "evaluator",
    }
    assert not parameters & forbidden


def test_observed_probability_derives_bounded_error_and_commits_scope() -> None:
    loop = ObservedOutcomeRevisionLoop()

    result = loop.apply_observed_outcome(
        base(0.8, 0.2), observation=[0.0], observed_value="later-b"
    )

    assert result.observed_probability == pytest.approx(0.2)
    assert result.prediction_error == pytest.approx(0.8)
    assert result.outcome_exposed
    assert result.bridge.allocation is not None
    assert result.bridge.allocation.action == "created"
    assert result.action == "observed_applied_created"


def test_returning_high_probability_outcome_reuses_internal_scope() -> None:
    loop = ObservedOutcomeRevisionLoop()
    created = loop.apply_observed_outcome(
        base(0.8, 0.2), observation=[0.0], observed_value="later-b"
    )

    returned = loop.apply_observed_outcome(
        base(0.8, 0.2), observation=[0.05], observed_value="later-a"
    )

    assert returned.prediction_error == pytest.approx(0.2)
    assert returned.bridge.routing.selected_scope == created.bridge.allocation.scope_token
    assert returned.bridge.allocation is not None
    assert returned.bridge.allocation.action == "reused"
    assert returned.action == "observed_applied_existing"


def test_unexposed_outcome_is_explicit_no_write() -> None:
    loop = ObservedOutcomeRevisionLoop()
    loop.apply_observed_outcome(
        base(), observation=[0.0], observed_value="later-a"
    )
    before = json.loads(json.dumps(loop.state_dict()))

    missing = loop.apply_observed_outcome(
        base(), observation=[3.0], observed_value="later-c"
    )

    assert missing.observed_probability == 0.0
    assert missing.prediction_error == 1.0
    assert not missing.outcome_exposed
    assert missing.action == "outcome_not_exposed_no_write"
    assert loop.state_dict() == before


def test_invalid_exposed_probability_mass_fails_closed() -> None:
    loop = ObservedOutcomeRevisionLoop()

    with pytest.raises(ValueError, match="probability mass"):
        loop.inspect(
            base(0.8, 0.8), observation=[0.0], observed_value="later-a"
        )


def test_checkpoint_roundtrip_preserves_derived_routing_and_revision() -> None:
    loop = ObservedOutcomeRevisionLoop()
    loop.apply_observed_outcome(
        base(), observation=[0.0], observed_value="later-b"
    )
    state = json.loads(json.dumps(loop.state_dict()))
    restored = ObservedOutcomeRevisionLoop.from_state_dict(state)

    left = loop.inspect(base(), observation=[0.05], observed_value="later-a")
    right = restored.inspect(base(), observation=[0.05], observed_value="later-a")

    assert left == right
    assert restored.state_dict() == state

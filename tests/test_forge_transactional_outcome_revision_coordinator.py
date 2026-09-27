import inspect
import json

import pytest

from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.transactional_outcome_revision_coordinator import (
    TransactionalOutcomeRevisionCoordinator,
)


def base(*rows: tuple[str, float]) -> PredictionPoolSnapshot:
    hypotheses = tuple(
        WeightedHypothesis(value, 5, probability) for value, probability in rows
    )
    probabilities = sorted((row.probability for row in hypotheses), reverse=True)
    confidence = probabilities[0] if probabilities else 0.0
    second = probabilities[1] if len(probabilities) > 1 else 0.0
    return PredictionPoolSnapshot(
        "assembly-1",
        hypotheses,
        None,
        confidence,
        confidence - second,
        True,
        "low_confidence",
    )


def frozen_state(coordinator: TransactionalOutcomeRevisionCoordinator) -> str:
    return json.dumps(coordinator.state_dict(), sort_keys=True)


def test_public_api_has_no_privileged_identity_error_or_tail_inputs() -> None:
    parameters = set(
        inspect.signature(TransactionalOutcomeRevisionCoordinator.apply_step).parameters
    )
    forbidden = {
        "prediction_error",
        "scope",
        "episode",
        "regime",
        "observed_probability",
        "tail_assignment",
        "truth",
        "evaluator",
    }
    assert not parameters & forbidden


def test_successful_exposed_outcome_commits_complete_candidate_state() -> None:
    coordinator = TransactionalOutcomeRevisionCoordinator()

    result = coordinator.apply_step(
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.0],
        observed_value="later-b",
    )

    assert result.committed
    assert result.state_changed
    assert result.action == "committed_exposed_observed_applied_created"
    state = coordinator.state_dict()["guard"]["bridge"]
    assert "assembly-1" in state["allocators"]
    assert state["revision"]["overlay"]["scopes"]


def test_late_strength_validation_failure_preserves_exact_checkpoint() -> None:
    coordinator = TransactionalOutcomeRevisionCoordinator()
    before = frozen_state(coordinator)

    with pytest.raises(ValueError, match="strength must be finite"):
        coordinator.apply_step(
            base(("later-a", 0.8), ("later-b", 0.2)),
            observation=[0.0],
            observed_value="later-a",
            strength=2.0,
        )

    assert frozen_state(coordinator) == before


def test_failed_step_cannot_change_following_valid_result() -> None:
    left = TransactionalOutcomeRevisionCoordinator()
    right = TransactionalOutcomeRevisionCoordinator()
    prediction = base(("later-a", 0.8), ("later-b", 0.2))

    with pytest.raises(ValueError):
        left.apply_step(
            prediction,
            observation=[0.0],
            observed_value="later-a",
            strength=float("nan"),
        )

    left_result = left.apply_step(
        prediction,
        observation=[0.0],
        observed_value="later-b",
    )
    right_result = right.apply_step(
        prediction,
        observation=[0.0],
        observed_value="later-b",
    )

    assert left_result == right_result
    assert left.state_dict() == right.state_dict()


def test_unexposed_tail_diagnostic_preserves_state() -> None:
    coordinator = TransactionalOutcomeRevisionCoordinator()
    coordinator.apply_step(
        base(("later-a", 0.6), ("later-b", 0.3)),
        observation=[0.0],
        observed_value="later-a",
    )
    before = frozen_state(coordinator)

    result = coordinator.apply_step(
        base(("later-a", 0.1)),
        observation=[0.4],
        observed_value="later-c",
    )

    assert not result.committed
    assert not result.state_changed
    assert result.action == "preserved_unexposed_tail_ambiguous_no_write"
    assert frozen_state(coordinator) == before


def test_checkpoint_roundtrip_preserves_next_transaction() -> None:
    coordinator = TransactionalOutcomeRevisionCoordinator()
    coordinator.apply_step(
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.0],
        observed_value="later-b",
    )
    state = json.loads(json.dumps(coordinator.state_dict()))
    restored = TransactionalOutcomeRevisionCoordinator.from_state_dict(state)

    left = coordinator.apply_step(
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.05],
        observed_value="later-a",
    )
    right = restored.apply_step(
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.05],
        observed_value="later-a",
    )

    assert left == right
    assert coordinator.state_dict() == restored.state_dict()

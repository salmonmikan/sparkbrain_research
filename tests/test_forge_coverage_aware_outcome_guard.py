import inspect
import json

import pytest

from forge_prototypes.coverage_aware_outcome_guard import CoverageAwareOutcomeGuard
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
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


def test_public_mutation_api_has_no_caller_error_scope_or_tail_assignment() -> None:
    parameters = set(
        inspect.signature(CoverageAwareOutcomeGuard.apply_observed_outcome).parameters
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


def test_exposed_outcome_delegates_to_exact_revision_loop() -> None:
    guard = CoverageAwareOutcomeGuard()

    result = guard.apply_observed_outcome(
        base(("later-a", 0.8), ("later-b", 0.2)),
        observation=[0.0],
        observed_value="later-b",
    )

    assert result.outcome_exposed
    assert result.observed_probability_lower == pytest.approx(0.2)
    assert result.observed_probability_upper == pytest.approx(0.2)
    assert result.prediction_error_lower == pytest.approx(0.8)
    assert result.prediction_error_upper == pytest.approx(0.8)
    assert result.applied is not None
    assert result.applied.bridge.allocation is not None
    assert result.action == "exposed_observed_applied_created"


def test_unexposed_outcome_uses_tail_interval_without_mutation() -> None:
    guard = CoverageAwareOutcomeGuard()
    guard.apply_observed_outcome(
        base(("later-a", 0.6), ("later-b", 0.3)),
        observation=[0.0],
        observed_value="later-a",
    )
    before = json.loads(json.dumps(guard.state_dict()))

    result = guard.apply_observed_outcome(
        base(("later-a", 0.6), ("later-b", 0.3)),
        observation=[3.0],
        observed_value="later-c",
    )

    assert not result.outcome_exposed
    assert result.exposed_probability_mass == pytest.approx(0.9)
    assert result.tail_probability_mass == pytest.approx(0.1)
    assert result.observed_probability_lower == pytest.approx(0.0)
    assert result.observed_probability_upper == pytest.approx(0.1)
    assert result.prediction_error_lower == pytest.approx(0.9)
    assert result.prediction_error_upper == pytest.approx(1.0)
    assert result.action == "unexposed_route_stable_no_revision"
    assert guard.state_dict() == before


def test_tail_interval_that_changes_route_abstains_without_mutation() -> None:
    guard = CoverageAwareOutcomeGuard()
    guard.apply_observed_outcome(
        base(("later-a", 0.6), ("later-b", 0.3)),
        observation=[0.0],
        observed_value="later-a",
    )
    before = json.loads(json.dumps(guard.state_dict()))

    result = guard.apply_observed_outcome(
        base(("later-a", 0.1)),
        observation=[0.4],
        observed_value="later-c",
    )

    assert result.prediction_error_lower == pytest.approx(0.1)
    assert result.prediction_error_upper == pytest.approx(1.0)
    assert result.lower_route.routing.selected_scope != result.upper_route.routing.selected_scope
    assert result.action == "unexposed_tail_ambiguous_no_write"
    assert guard.state_dict() == before


def test_invalid_probability_mass_fails_closed() -> None:
    guard = CoverageAwareOutcomeGuard()

    with pytest.raises(ValueError, match="probability mass"):
        guard.apply_observed_outcome(
            base(("later-a", 0.8), ("later-b", 0.8)),
            observation=[0.0],
            observed_value="later-c",
        )


def test_checkpoint_roundtrip_preserves_interval_routing() -> None:
    guard = CoverageAwareOutcomeGuard()
    guard.apply_observed_outcome(
        base(("later-a", 0.6), ("later-b", 0.3)),
        observation=[0.0],
        observed_value="later-a",
    )
    state = json.loads(json.dumps(guard.state_dict()))
    restored = CoverageAwareOutcomeGuard.from_state_dict(state)

    left = guard.apply_observed_outcome(
        base(("later-a", 0.1)),
        observation=[0.4],
        observed_value="later-c",
    )
    right = restored.apply_observed_outcome(
        base(("later-a", 0.1)),
        observation=[0.4],
        observed_value="later-c",
    )

    assert left == right
    assert restored.state_dict() == state

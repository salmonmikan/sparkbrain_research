from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.reservoir_baseline import (
    FixedEchoStateAutoregressor,
    ReservoirConfig,
)
from sparkbrain.research.rv01.reservoir_comparison import (
    run_reservoir_comparison_suite,
)


def test_echo_state_reservoir_reproduces_basic_continuation() -> None:
    suite = run_reservoir_comparison_suite()
    row = suite.continuation
    assert row.training_sequences == ((0, 1, 2, 3),)
    assert row.prefix == (0,)
    assert row.generated == (1, 2, 3)
    assert row.fixed_parameter_count == 720
    assert row.learned_parameter_count == 150
    assert row.observation_count == 15
    assert row.generated_token_count == 3
    assert suite.rv01_physical_output == (1, 2, 3)
    assert suite.assessment.same_basic_capability_is_non_unique is True


def test_reservoir_state_distinguishes_same_current_token_by_prior_context() -> None:
    suite = run_reservoir_comparison_suite()
    row = suite.context
    assert row.left_prefix == (0, 1, 2)
    assert row.right_prefix == (0, 3, 2)
    assert row.left_prediction.predicted_token == 4
    assert row.right_prediction.predicted_token == 5
    assert (
        row.left_prediction.hidden_state_hash
        != row.right_prediction.hidden_state_hash
    )
    assert suite.assessment.reservoir_context_changes_prediction is True


def test_context_ablation_collapses_context_specific_prediction() -> None:
    suite = run_reservoir_comparison_suite()
    row = suite.context
    assert (
        row.left_ablated_prediction.predicted_token
        == row.right_ablated_prediction.predicted_token
    )
    assert (
        row.left_ablated_prediction.hidden_state_hash
        == row.right_ablated_prediction.hidden_state_hash
    )
    assert row.left_ablated_prediction.context_ablated is True
    assert row.right_ablated_prediction.context_ablated is True
    assert suite.assessment.context_state_intervention_collapses_difference is True


def test_equal_branch_training_retains_two_top_probability_candidates() -> None:
    suite = run_reservoir_comparison_suite()
    row = suite.ambiguity
    left, right = row.branch_probabilities
    assert row.prefix == (0, 1)
    assert row.branch_tokens == (2, 3)
    assert row.top_two_tokens == (2, 3)
    assert left == pytest.approx(right, abs=1e-9)
    assert left > 0.20
    assert right > 0.20
    assert suite.assessment.equal_branch_readout_retains_probability_mass is True


def test_supervised_readout_refit_reverses_and_reacquires() -> None:
    suite = run_reservoir_comparison_suite()
    row = suite.revision
    assert row.acquired_output == (1, 2, 3)
    assert row.reversed_output == (1, 4, 5)
    assert row.returned_output == (1, 2, 3)
    assert row.acquired_readout_hash != row.reversed_readout_hash
    assert row.returned_readout_hash == row.acquired_readout_hash
    assert suite.assessment.reservoir_refit_reverses_and_reacquires is True


def test_readout_state_transplant_reproduces_acquired_behavior() -> None:
    suite = run_reservoir_comparison_suite()
    assert suite.transplanted_output == suite.revision.acquired_output
    assert suite.transplanted_output == (1, 2, 3)
    assert suite.assessment.readout_transplant_reproduces_behavior is True


def test_generated_tokens_do_not_train_the_reservoir_readout() -> None:
    model = FixedEchoStateAutoregressor(
        ReservoirConfig(token_count=6, reservoir_size=24, seed=17)
    )
    model.fit_sequences(((0, 1, 2, 3),), repetitions=5)
    before = model.learned_state_dict()
    assert model.rollout((0,), steps=3) == (1, 2, 3)
    assert model.learned_state_dict() == before
    assert model.generated_token_count == 3


def test_invalid_reservoir_contracts_fail_closed() -> None:
    with pytest.raises(ValueError, match="token_count"):
        ReservoirConfig(token_count=1).validate()
    with pytest.raises(ValueError, match="recurrent_density"):
        ReservoirConfig(token_count=4, recurrent_density=1.1).validate()
    with pytest.raises(ValueError, match="leak_rate"):
        ReservoirConfig(token_count=4, leak_rate=1.1).validate()

    model = FixedEchoStateAutoregressor(ReservoirConfig(token_count=4))
    with pytest.raises(RuntimeError, match="fit_sequences"):
        model.predict_next((0,))
    with pytest.raises(ValueError, match="prefix"):
        model.encode_prefix(())
    with pytest.raises(ValueError, match="outside"):
        model.advance(model.zero_state(), 99)


def test_r01_09b_keeps_generic_recurrent_explanation_open() -> None:
    assessment = run_reservoir_comparison_suite().assessment
    assert assessment.echo_state_continuation_supported is True
    assert assessment.rv01_physical_continuation_supported is True
    assert assessment.reservoir_context_changes_prediction is True
    assert assessment.context_state_intervention_collapses_difference is True
    assert assessment.equal_branch_readout_retains_probability_mass is True
    assert assessment.reservoir_refit_reverses_and_reacquires is True
    assert assessment.generation_does_not_self_train is True
    assert assessment.recurrent_weights_are_fixed is True
    assert assessment.reservoir_is_not_resource_matched is True
    assert assessment.passive_output_only_explanation_rejected is True
    assert assessment.generic_recurrent_explanation_remains_viable is True
    assert assessment.architectural_uniqueness_established is False
    assert assessment.engineering_candidate is True


def test_reservoir_comparison_is_deterministic() -> None:
    first = run_reservoir_comparison_suite()
    second = run_reservoir_comparison_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash


def test_reservoir_comparator_does_not_import_rv01_physical_runtime() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "reservoir_baseline.py"
    )
    source = path.read_text(encoding="utf-8")
    for forbidden in (
        "TemporalExcitableField",
        "ExternalGatedDirectFieldPlasticity",
        "LocalTemporalExpectation",
        "SparseLocalTransitionAdaptation",
        "EndogenousPulseProposal",
    ):
        assert forbidden not in source

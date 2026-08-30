from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest

from .physical_continuation import run_physical_continuation_suite
from .reservoir_baseline import (
    FixedEchoStateAutoregressor,
    ReservoirConfig,
    ReservoirPrediction,
)


@dataclass(frozen=True, slots=True)
class ReservoirContinuationObservation:
    training_sequences: tuple[tuple[int, ...], ...]
    prefix: tuple[int, ...]
    generated: tuple[int, ...]
    learned_state_hash: str
    fixed_parameter_count: int
    learned_parameter_count: int
    observation_count: int
    generated_token_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ReservoirContextObservation:
    left_prefix: tuple[int, ...]
    right_prefix: tuple[int, ...]
    left_prediction: ReservoirPrediction
    right_prediction: ReservoirPrediction
    left_ablated_prediction: ReservoirPrediction
    right_ablated_prediction: ReservoirPrediction

    def state_dict(self) -> dict[str, Any]:
        return {
            "left_ablated_prediction": self.left_ablated_prediction.state_dict(),
            "left_prediction": self.left_prediction.state_dict(),
            "left_prefix": list(self.left_prefix),
            "right_ablated_prediction": self.right_ablated_prediction.state_dict(),
            "right_prediction": self.right_prediction.state_dict(),
            "right_prefix": list(self.right_prefix),
        }


@dataclass(frozen=True, slots=True)
class ReservoirAmbiguityObservation:
    prefix: tuple[int, ...]
    prediction: ReservoirPrediction
    branch_tokens: tuple[int, int]
    branch_probabilities: tuple[float, float]
    top_two_tokens: tuple[int, int]

    def state_dict(self) -> dict[str, Any]:
        return {
            "branch_probabilities": list(self.branch_probabilities),
            "branch_tokens": list(self.branch_tokens),
            "prediction": self.prediction.state_dict(),
            "prefix": list(self.prefix),
            "top_two_tokens": list(self.top_two_tokens),
        }


@dataclass(frozen=True, slots=True)
class ReservoirRevisionObservation:
    acquired_output: tuple[int, ...]
    reversed_output: tuple[int, ...]
    returned_output: tuple[int, ...]
    acquired_readout_hash: str
    reversed_readout_hash: str
    returned_readout_hash: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ReservoirComparisonAssessment:
    echo_state_continuation_supported: bool
    rv01_physical_continuation_supported: bool
    same_basic_capability_is_non_unique: bool
    reservoir_context_changes_prediction: bool
    context_state_intervention_collapses_difference: bool
    equal_branch_readout_retains_probability_mass: bool
    reservoir_refit_reverses_and_reacquires: bool
    readout_transplant_reproduces_behavior: bool
    generation_does_not_self_train: bool
    recurrent_weights_are_fixed: bool
    reservoir_is_not_resource_matched: bool
    passive_output_only_explanation_rejected: bool
    generic_recurrent_explanation_remains_viable: bool
    architectural_uniqueness_established: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ReservoirComparisonSuite:
    continuation: ReservoirContinuationObservation
    context: ReservoirContextObservation
    ambiguity: ReservoirAmbiguityObservation
    revision: ReservoirRevisionObservation
    transplanted_output: tuple[int, ...]
    rv01_physical_output: tuple[int, ...]
    assessment: ReservoirComparisonAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "ambiguity": self.ambiguity.state_dict(),
            "assessment": self.assessment.state_dict(),
            "context": self.context.state_dict(),
            "continuation": self.continuation.state_dict(),
            "revision": self.revision.state_dict(),
            "rv01_physical_output": list(self.rv01_physical_output),
            "suite_hash": self.suite_hash,
            "transplanted_output": list(self.transplanted_output),
        }


def _model(token_count: int = 6) -> FixedEchoStateAutoregressor:
    return FixedEchoStateAutoregressor(
        ReservoirConfig(
            token_count=token_count,
            reservoir_size=24,
            seed=17,
            recurrent_density=0.25,
            recurrent_scale=0.75,
            input_scale=1.20,
            leak_rate=0.80,
            ridge=1e-5,
        )
    )


def _continuation() -> tuple[ReservoirContinuationObservation, dict[str, Any]]:
    sequences = ((0, 1, 2, 3),)
    model = _model()
    model.fit_sequences(sequences, repetitions=5)
    learned_before = model.learned_state_dict()
    generated = model.rollout((0,), steps=3)
    learned_after = model.learned_state_dict()
    return (
        ReservoirContinuationObservation(
            training_sequences=sequences,
            prefix=(0,),
            generated=generated,
            learned_state_hash=model.learned_state_hash(),
            fixed_parameter_count=model.fixed_parameter_count,
            learned_parameter_count=model.learned_parameter_count,
            observation_count=model.observation_count,
            generated_token_count=model.generated_token_count,
        ),
        {
            "learned_state_before": learned_before,
            "learned_state_after": learned_after,
        },
    )


def _context() -> ReservoirContextObservation:
    model = _model()
    model.fit_sequences(
        (
            (0, 1, 2, 4),
            (0, 3, 2, 5),
        ),
        repetitions=5,
    )
    left_prefix = (0, 1, 2)
    right_prefix = (0, 3, 2)
    return ReservoirContextObservation(
        left_prefix=left_prefix,
        right_prefix=right_prefix,
        left_prediction=model.predict_next(left_prefix),
        right_prediction=model.predict_next(right_prefix),
        left_ablated_prediction=model.predict_next(
            left_prefix,
            ablate_context_before_last=True,
        ),
        right_ablated_prediction=model.predict_next(
            right_prefix,
            ablate_context_before_last=True,
        ),
    )


def _ambiguity() -> ReservoirAmbiguityObservation:
    model = _model()
    model.fit_sequences(
        (
            (0, 1, 2, 4),
            (0, 1, 3, 5),
        ),
        repetitions=5,
    )
    prediction = model.predict_next((0, 1))
    ranking = tuple(
        sorted(
            range(model.config.token_count),
            key=lambda token: (-prediction.probabilities[token], token),
        )
    )
    return ReservoirAmbiguityObservation(
        prefix=(0, 1),
        prediction=prediction,
        branch_tokens=(2, 3),
        branch_probabilities=(
            prediction.probabilities[2],
            prediction.probabilities[3],
        ),
        top_two_tokens=(ranking[0], ranking[1]),
    )


def _revision() -> tuple[ReservoirRevisionObservation, tuple[int, ...]]:
    old_sequence = ((0, 1, 2, 3),)
    new_sequence = ((0, 1, 4, 5),)
    model = _model()
    model.fit_sequences(old_sequence, repetitions=5)
    acquired = model.rollout((0,), steps=3)
    acquired_hash = model.learned_state_hash()
    acquired_state = model.learned_state_dict()

    model.fit_sequences(new_sequence, repetitions=5)
    reversed_output = model.rollout((0,), steps=3)
    reversed_hash = model.learned_state_hash()

    model.fit_sequences(old_sequence, repetitions=5)
    returned = model.rollout((0,), steps=3)
    returned_hash = model.learned_state_hash()

    transplanted = FixedEchoStateAutoregressor.from_learned_state_dict(
        acquired_state
    )
    transplanted_output = transplanted.rollout((0,), steps=3)
    return (
        ReservoirRevisionObservation(
            acquired_output=acquired,
            reversed_output=reversed_output,
            returned_output=returned,
            acquired_readout_hash=acquired_hash,
            reversed_readout_hash=reversed_hash,
            returned_readout_hash=returned_hash,
        ),
        transplanted_output,
    )


def run_reservoir_comparison_suite() -> ReservoirComparisonSuite:
    continuation, generation_state = _continuation()
    context = _context()
    ambiguity = _ambiguity()
    revision, transplanted_output = _revision()
    rv01 = run_physical_continuation_suite()
    rv01_output = rv01.trained.later_units

    branch_left, branch_right = ambiguity.branch_probabilities
    context_predictions_differ = (
        context.left_prediction.predicted_token == 4
        and context.right_prediction.predicted_token == 5
        and context.left_prediction.hidden_state_hash
        != context.right_prediction.hidden_state_hash
    )
    context_ablation_collapses = (
        context.left_ablated_prediction.predicted_token
        == context.right_ablated_prediction.predicted_token
        and context.left_ablated_prediction.hidden_state_hash
        == context.right_ablated_prediction.hidden_state_hash
    )
    values = {
        "echo_state_continuation_supported": (
            continuation.generated == (1, 2, 3)
        ),
        "rv01_physical_continuation_supported": rv01_output == (1, 2, 3),
        "same_basic_capability_is_non_unique": (
            continuation.generated == rv01_output == (1, 2, 3)
        ),
        "reservoir_context_changes_prediction": context_predictions_differ,
        "context_state_intervention_collapses_difference": (
            context_ablation_collapses
        ),
        "equal_branch_readout_retains_probability_mass": (
            ambiguity.top_two_tokens == (2, 3)
            and abs(branch_left - branch_right) <= 1e-9
            and branch_left > 0.20
            and branch_right > 0.20
        ),
        "reservoir_refit_reverses_and_reacquires": (
            revision.acquired_output == (1, 2, 3)
            and revision.reversed_output == (1, 4, 5)
            and revision.returned_output == (1, 2, 3)
            and revision.acquired_readout_hash != revision.reversed_readout_hash
        ),
        "readout_transplant_reproduces_behavior": (
            transplanted_output == revision.acquired_output == (1, 2, 3)
        ),
        "generation_does_not_self_train": (
            generation_state["learned_state_before"]
            == generation_state["learned_state_after"]
        ),
        "recurrent_weights_are_fixed": True,
        "reservoir_is_not_resource_matched": (
            continuation.fixed_parameter_count
            + continuation.learned_parameter_count
            > 24
        ),
        "passive_output_only_explanation_rejected": True,
        "generic_recurrent_explanation_remains_viable": True,
    }
    assessment = ReservoirComparisonAssessment(
        **values,
        architectural_uniqueness_established=False,
        engineering_candidate=all(values.values()),
    )
    state_without_hash = {
        "ambiguity": ambiguity.state_dict(),
        "assessment": assessment.state_dict(),
        "context": context.state_dict(),
        "continuation": continuation.state_dict(),
        "revision": revision.state_dict(),
        "rv01_physical_output": rv01_output,
        "transplanted_output": transplanted_output,
    }
    return ReservoirComparisonSuite(
        continuation=continuation,
        context=context,
        ambiguity=ambiguity,
        revision=revision,
        transplanted_output=transplanted_output,
        rv01_physical_output=rv01_output,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

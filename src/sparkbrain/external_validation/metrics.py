from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Any

from .schema import PredictionStep, RevisionTarget


@dataclass(frozen=True, slots=True)
class ExternalMetrics:
    final_answer_accuracy: float
    revision_precision: float | None
    revision_recall: float | None
    no_update_retention_accuracy: float | None
    false_revision_rate: float | None
    mean_switch_latency_steps: float | None
    coverage: float
    abstention_utility: float
    contradiction_sensitivity: float | None
    evidence_attribution_fidelity: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_revision_sequence(
    predictions: tuple[PredictionStep, ...], targets: tuple[RevisionTarget, ...]
) -> ExternalMetrics:
    if not predictions or len(predictions) != len(targets):
        raise ValueError("Predictions and targets must be non-empty and aligned")
    for prediction in predictions:
        prediction.validate()
    for target in targets:
        target.validate()
    correct = [
        prediction.prediction == target.truth
        for prediction, target in zip(predictions, targets, strict=True)
    ]
    prediction_changes = [
        index
        for index in range(1, len(predictions))
        if predictions[index].prediction != predictions[index - 1].prediction
    ]
    correct_changes = sum(correct[index] for index in prediction_changes)
    update_indices = [index for index, target in enumerate(targets) if target.update_required]
    recovered = 0
    latencies: list[float] = []
    for update_index in update_indices:
        resolved = next(
            (index for index in range(update_index, len(predictions)) if correct[index]), None
        )
        if resolved is not None:
            recovered += 1
            latencies.append(float(resolved - update_index))
    no_update_indices = [
        index for index in range(1, len(targets)) if not targets[index].update_required
    ]
    retained = sum(
        predictions[index].prediction == predictions[index - 1].prediction
        and correct[index]
        for index in no_update_indices
    )
    false_revisions = sum(index in no_update_indices for index in prediction_changes)
    justified_indices = [index for index, target in enumerate(targets) if target.decision_justified]
    unjustified_indices = [
        index for index, target in enumerate(targets) if not target.decision_justified
    ]
    justified_correct = sum(correct[index] for index in justified_indices)
    appropriate_abstentions = sum(
        predictions[index].prediction is None for index in unjustified_indices
    )
    abstention_utility = (
        justified_correct + appropriate_abstentions
    ) / (len(justified_indices) + len(unjustified_indices))
    contradiction_indices = [
        index for index, target in enumerate(targets) if "contradiction" in target.scenario_tags
    ]
    attribution_rows = [
        (set(prediction.cited_evidence_ids), set(target.required_evidence_ids))
        for prediction, target in zip(predictions, targets, strict=True)
        if target.required_evidence_ids
    ]
    attribution = mean(
        len(cited & required) / len(cited | required) if cited | required else 1.0
        for cited, required in attribution_rows
    ) if attribution_rows else None
    return ExternalMetrics(
        final_answer_accuracy=float(correct[-1]),
        revision_precision=(
            correct_changes / len(prediction_changes) if prediction_changes else None
        ),
        revision_recall=recovered / len(update_indices) if update_indices else None,
        no_update_retention_accuracy=retained / len(no_update_indices)
        if no_update_indices
        else None,
        false_revision_rate=false_revisions / len(no_update_indices) if no_update_indices else None,
        mean_switch_latency_steps=mean(latencies) if latencies else None,
        coverage=(
            sum(prediction.prediction is not None for prediction in predictions)
            / len(predictions)
        ),
        abstention_utility=abstention_utility,
        contradiction_sensitivity=mean(float(correct[index]) for index in contradiction_indices)
        if contradiction_indices
        else None,
        evidence_attribution_fidelity=attribution,
    )


def context_length_degradation(*, short_accuracy: float, long_accuracy: float) -> float:
    return short_accuracy - long_accuracy


def entity_cross_talk_rate(*, unaffected_changes: int, intervention_count: int) -> float | None:
    if intervention_count < 0 or unaffected_changes < 0:
        raise ValueError("Cross-talk counts must be non-negative")
    if intervention_count == 0:
        return None
    return unaffected_changes / intervention_count


def categorize_errors(
    predictions: tuple[PredictionStep, ...], targets: tuple[RevisionTarget, ...]
) -> tuple[tuple[str, ...], ...]:
    if len(predictions) != len(targets):
        raise ValueError("Predictions and targets must be aligned")
    result: list[tuple[str, ...]] = []
    for index, (prediction, target) in enumerate(zip(predictions, targets, strict=True)):
        labels: list[str] = []
        correct = prediction.prediction == target.truth
        if index == 0 and not correct:
            labels.append("initial_error")
        if target.update_required and not correct:
            labels.append("missed_revision")
        if (
            index > 0
            and not target.update_required
            and prediction.prediction != predictions[index - 1].prediction
        ):
            labels.append("false_revision")
        if prediction.prediction is None and target.decision_justified:
            labels.append("inappropriate_abstention")
        if not correct and prediction.confidence is not None and prediction.confidence >= 0.8:
            labels.append("overconfident_wrong")
        if target.required_evidence_ids and not (
            set(prediction.cited_evidence_ids) & set(target.required_evidence_ids)
        ):
            labels.append("unsupported_attribution")
        result.append(tuple(labels))
    return tuple(result)

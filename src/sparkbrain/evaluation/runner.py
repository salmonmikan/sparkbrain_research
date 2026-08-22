from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from ..engine import SparkBrain
from ..metrics import SequencePoint, evaluate_sequence
from ..model import BrainConfig, Spark, SparkKind
from ..tasks.schema import Episode
from ..worlds import EVIDENCE_WEIGHTS, LABELS, build_reference_brain
from .ablations import get_ablation
from .metrics import brier_score, expected_calibration_error, quantiles


@dataclass(slots=True)
class EpisodeResult:
    episode_id: str
    world: str
    split: str
    condition: str
    seed: int
    status: str
    metrics: dict[str, Any]
    counters: dict[str, Any]
    steps: list[dict[str, Any]]
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _build_multi_object_brain(config: BrainConfig, object_ids: tuple[str, ...]) -> SparkBrain:
    brain = SparkBrain(config)
    for object_id in object_ids:
        for evidence in EVIDENCE_WEIGHTS:
            brain.add_spark(
                Spark(
                    id=f"sensory:{object_id}:{evidence}",
                    label=evidence,
                    kind=SparkKind.SENSORY,
                    organ=f"perception:{object_id}",
                    threshold=0.55,
                    base_threshold=0.55,
                    decay_tau=0.45,
                    metadata={"post_fire_residual": 0.05},
                )
            )
        hypothesis_ids: list[str] = []
        for label in LABELS:
            spark_id = f"hypothesis:{object_id}:{label}"
            hypothesis_ids.append(spark_id)
            brain.add_spark(
                Spark(
                    id=spark_id,
                    label=label,
                    kind=SparkKind.HYPOTHESIS,
                    organ=f"hypothesis:{object_id}",
                    threshold=0.78,
                    base_threshold=0.78,
                    decay_tau=4.0,
                    competition_group=f"object_identity:{object_id}",
                    metadata={"post_fire_residual": 0.84},
                )
            )
        for evidence, mapping in EVIDENCE_WEIGHTS.items():
            for label, weight in mapping.items():
                brain.connect(
                    f"sensory:{object_id}:{evidence}",
                    f"hypothesis:{object_id}:{label}",
                    weight,
                    label="evidence",
                )
        brain.add_soft_competition(hypothesis_ids, weight=-0.16)
    brain.add_spark(
        Spark(
            id="memory:workspace",
            label="working memory",
            kind=SparkKind.MEMORY,
            organ="memory",
            threshold=0.70,
            base_threshold=0.70,
            decay_tau=8.0,
            metadata={"post_fire_residual": 0.70},
        )
    )
    brain.register_broadcast_listener("memory:workspace")
    return brain


def _object_predictions(brain: SparkBrain, object_ids: tuple[str, ...]) -> dict[str, str | None]:
    if object_ids == ("object",):
        return {"object": brain.prediction}
    predictions: dict[str, str | None] = {object_id: None for object_id in object_ids}
    for item in reversed(brain.workspace):
        parts = item.hypothesis_id.split(":")
        if len(parts) == 3 and parts[1] in predictions:
            predictions[parts[1]] = item.label
    return predictions


def _probabilities(brain: SparkBrain) -> dict[str, float]:
    scores = {label: 0.0 for label in LABELS}
    for coalition in brain.last_coalitions:
        scores[coalition.label] = coalition.score
    exponentials = {
        label: math.exp(max(-20.0, min(20.0, score))) for label, score in scores.items()
    }
    total = sum(exponentials.values())
    return {label: value / total for label, value in exponentials.items()}


def run_episode(
    episode: Episode, *, condition: str = "full", retain_trace: bool = False
) -> EpisodeResult:
    episode.validate()
    ablation = get_ablation(condition)
    config = ablation.configure(BrainConfig(random_seed=episode.seed))
    object_ids = tuple(sorted(episode.steps[0].target.belief_truth_by_object))
    brain = (
        _build_multi_object_brain(config, object_ids)
        if len(object_ids) > 1
        else build_reference_brain(config)
    )
    ablation.transform(brain)
    rows: list[dict[str, Any]] = []
    points: list[SequencePoint] = []
    probabilities: list[dict[str, float]] = []
    truths: list[str] = []
    confidences: list[float] = []
    correct: list[bool] = []
    update_counts: list[float] = []
    edge_counts: list[float] = []
    previous_stats = (0, 0)
    previous_predictions = {object_id: None for object_id in object_ids}
    previous_score = 0.0
    current_goal = "report"
    duplicate_inflation: list[float] = []
    reliability_scores: dict[str, list[float]] = {"high": [], "low": []}
    cross_talk = 0
    belief_goal_flips = 0
    action_correct = 0
    action_total = 0
    appropriate_abstentions = missed_decisions = unjustified = justified = 0
    false_certainty = 0

    for step in episode.steps:
        obs, target = step.observation, step.target
        before_ignitions = len(brain.ignitions)
        if obs.channel == "goal":
            before = dict(previous_predictions)
            current_goal = obs.evidence_label
            predictions = _object_predictions(brain, object_ids)
            belief_goal_flips += int(predictions != before)
        else:
            object_id = obs.object_id or "object"
            sensory_id = (
                f"sensory:{object_id}:{obs.evidence_label}"
                if len(object_ids) > 1
                else f"sensory:{obs.evidence_label}"
            )
            brain.inject_stimulus(
                target=sensory_id,
                label=obs.evidence_label,
                time=max(brain.time, obs.delivery_time),
                strength=obs.strength,
                source=obs.source_id,
                evidence_id=obs.evidence_id,
                metadata={
                    "sensor": obs.source_id,
                    "object_id": obs.object_id,
                    "scenario_tags": list(target.scenario_tags),
                },
            )
            brain.run()
            if ablation.hard_wta and len(brain.ignitions) > before_ignitions:
                brain.erase_losing_hypotheses(brain.ignitions[-1].hypothesis_id)
            predictions = _object_predictions(brain, object_ids)

        forced = False
        primary_object = "a" if "a" in object_ids else object_ids[0]
        prediction = predictions[primary_object]
        if prediction is None and ablation.forced_prediction and brain.last_coalitions:
            prediction = brain.last_coalitions[0].label
            predictions[primary_object] = prediction
            forced = True
        truth = target.belief_truth_by_object[primary_object]
        probs = _probabilities(brain)
        confidence = max(probs.values())
        decision_justified = target.decision_justified_by_object[primary_object]
        if decision_justified:
            justified += 1
            missed_decisions += int(prediction is None)
        else:
            unjustified += 1
            appropriate_abstentions += int(prediction is None)
        false_certainty += int(
            confidence >= 0.80 and (prediction != truth or not decision_justified)
        )
        if obs.object_id:
            for other in object_ids:
                if other != obs.object_id and predictions[other] != previous_predictions[other]:
                    cross_talk += 1
        action_prediction = f"{current_goal}:{prediction or 'none'}"
        if target.optimal_action is not None:
            action_total += 1
            action_correct += int(action_prediction == target.optimal_action)
        score = brain.last_coalitions[0].score if brain.last_coalitions else 0.0
        if "duplicate" in target.scenario_tags:
            duplicate_inflation.append(score - previous_score)
        reliability = target.annotations.get("source_reliability")
        if isinstance(reliability, (int, float)):
            band = "high" if reliability >= 0.8 else "low"
            reliability_scores[band].append(probs.get(truth, 0.0))
        previous_score = score
        stats = (brain.stats.spark_updates, brain.stats.edge_evaluations)
        update_counts.append(float(stats[0] - previous_stats[0]))
        edge_counts.append(float(stats[1] - previous_stats[1]))
        previous_stats = stats
        rows.append(
            {
                "step_index": obs.step_index,
                "time": obs.delivery_time,
                "observation_id": obs.observation_id,
                "object_id": obs.object_id,
                "truth": target.belief_truth_by_object,
                "prediction": predictions,
                "forced": forced,
                "confidence": confidence,
                "probabilities": probs,
                "action_prediction": action_prediction,
                "scenario_tags": list(target.scenario_tags),
                "coalition_score": score,
            }
        )
        points.append(
            SequencePoint(obs.delivery_time, truth, prediction, "|".join(target.scenario_tags))
        )
        probabilities.append(probs)
        truths.append(truth)
        confidences.append(confidence)
        correct.append(prediction == truth)
        previous_predictions = dict(predictions)
        if retain_trace:
            brain.snapshot(external_event=obs.evidence_label, truth=truth)

    base = evaluate_sequence(points).to_dict()
    base.update(
        {
            "brier_score": brier_score(probabilities, truths),
            "expected_calibration_error": expected_calibration_error(confidences, correct),
            "appropriate_abstention_rate": appropriate_abstentions / unjustified
            if unjustified
            else None,
            "missed_decision_rate": missed_decisions / justified if justified else None,
            "false_certainty_rate": false_certainty / len(rows),
            "duplicate_evidence_inflation": sum(duplicate_inflation) / len(duplicate_inflation)
            if duplicate_inflation
            else None,
            "source_reliability_sensitivity": (
                sum(reliability_scores["high"]) / len(reliability_scores["high"])
                - sum(reliability_scores["low"]) / len(reliability_scores["low"])
                if reliability_scores["high"] and reliability_scores["low"]
                else None
            ),
            "object_cross_talk": cross_talk,
            "belief_goal_flip_rate": belief_goal_flips
            / max(1, sum(step.observation.channel == "goal" for step in episode.steps)),
            "action_accuracy": action_correct / action_total if action_total else None,
            "false_ignition_rate": sum(
                ign.label
                != points[
                    min(range(len(points)), key=lambda i: abs(points[i].time - ign.time))
                ].truth
                for ign in brain.ignitions
            )
            / len(brain.ignitions)
            if brain.ignitions
            else 0.0,
        }
    )
    counters = {
        "spark_updates": brain.stats.spark_updates,
        "edge_evaluations": brain.stats.edge_evaluations,
        "events_processed": brain.stats.events_processed,
        "spark_update_distribution": quantiles(update_counts),
        "edge_evaluation_distribution": quantiles(edge_counts),
        "counterfactual_dense_spark_updates": len(brain.sparks) * len(rows),
        "counterfactual_dense_edge_evaluations": len(brain.connections) * len(rows),
    }
    return EpisodeResult(
        episode.episode_id,
        episode.world_id,
        episode.split,
        condition,
        episode.seed,
        "complete",
        base,
        counters,
        rows,
    )

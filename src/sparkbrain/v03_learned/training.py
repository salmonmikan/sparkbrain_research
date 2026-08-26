from __future__ import annotations

import hashlib
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

import torch
from torch import Tensor, nn

from .model import C15RevisionModel, RevisionModelConfig, RevisionModelOutput
from .objectives import (
    CONDITION_ORDER,
    ObjectiveGradientRow,
    ObjectiveTarget,
    ObjectiveWeights,
    WeightedCETarget,
    compute_objective_losses,
    objective_gradient_statistics,
    total_gradient_l2,
)

CHECKPOINT_EPOCHS = (2, 4, 6)
MODEL_SEEDS = (2951, 2952, 2953, 2954, 2955)
TEMPERATURE_GRID = (0.75, 1.0, 1.25)
ABSTENTION_THRESHOLD_GRID = (0.4, 0.5, 0.6)


@dataclass(frozen=True, slots=True)
class TrainingTarget:
    belief_index: int
    previous_belief_index: int
    transition_target: str
    sufficient_information: bool
    attribution_target_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TrainingEpisode:
    episode_id: str
    variant_id: str
    input_track: str
    entity_condition: str
    model_calls: tuple[Mapping[str, object], ...]
    assessment_index: int
    target: TrainingTarget | WeightedCETarget

    @classmethod
    def from_fixture(cls, fixture: Mapping[str, object]) -> TrainingEpisode:
        expected = {
            "episode_id",
            "variant_id",
            "input_track",
            "entity_condition",
            "model_calls",
            "assessment_index",
            "target",
        }
        if set(fixture) != expected:
            raise ValueError("training fixture has missing or unknown fields")
        raw_calls = fixture["model_calls"]
        if not isinstance(raw_calls, Sequence) or isinstance(raw_calls, (str, bytes)):
            raise ValueError("model_calls must be a sequence")
        calls = tuple(raw_calls)
        if not calls or any(not isinstance(call, Mapping) for call in calls):
            raise ValueError("model_calls must contain visible fixture mappings")
        assessment_index = fixture["assessment_index"]
        if (
            isinstance(assessment_index, bool)
            or not isinstance(assessment_index, int)
            or assessment_index <= 0
            or assessment_index >= len(calls)
        ):
            raise ValueError("assessment_index must follow at least one context call")
        raw_target = fixture["target"]
        if not isinstance(raw_target, Mapping):
            raise ValueError("target must be an evaluator-side mapping")
        separated_target_fields = {
            "belief_index",
            "previous_belief_index",
            "transition_target",
            "sufficient_information",
            "attribution_target_ids",
        }
        weighted_ce_target_fields = {"belief_index", "sufficient_information"}
        if frozenset(raw_target) not in {
            frozenset(separated_target_fields),
            frozenset(weighted_ce_target_fields),
        }:
            raise ValueError("training target has missing or unknown fields")
        if set(raw_target) == weighted_ce_target_fields:
            target: TrainingTarget | WeightedCETarget = WeightedCETarget(
                belief_index=raw_target["belief_index"],
                sufficient_information=raw_target["sufficient_information"],
            )
            target.validate()
        else:
            raw_ids = raw_target["attribution_target_ids"]
            if not isinstance(raw_ids, Sequence) or isinstance(raw_ids, (str, bytes)):
                raise ValueError("attribution_target_ids must be a sequence")
            target = TrainingTarget(
                belief_index=raw_target["belief_index"],
                previous_belief_index=raw_target["previous_belief_index"],
                transition_target=str(raw_target["transition_target"]),
                sufficient_information=raw_target["sufficient_information"],
                attribution_target_ids=tuple(raw_ids),
            )
        episode = cls(
            episode_id=str(fixture["episode_id"]),
            variant_id=str(fixture["variant_id"]),
            input_track=str(fixture["input_track"]),
            entity_condition=str(fixture["entity_condition"]),
            model_calls=calls,
            assessment_index=assessment_index,
            target=target,
        )
        episode.validate()
        return episode

    def validate(self) -> None:
        if not self.episode_id:
            raise ValueError("episode_id must be non-empty")
        if self.variant_id != "base":
            raise ValueError("C15 training uses the base variant only")
        if (self.input_track, self.entity_condition) != (
            "I1_local_compositional",
            "E1_oracle_entity",
        ):
            raise ValueError("C15 training cell must be I1/E1")


@dataclass(frozen=True, slots=True)
class EpisodeOutputs:
    outputs: tuple[RevisionModelOutput, ...]
    assessment: RevisionModelOutput
    previous_probabilities: Tensor


@dataclass(frozen=True, slots=True)
class TrainingStepRow:
    condition_id: str
    model_seed: int
    epoch: int
    optimizer_step: int
    episode_id: str
    objectives: dict[str, ObjectiveGradientRow]
    total_loss: float
    pre_clip_total_gradient_l2: float
    post_clip_total_gradient_l2: float

    def as_artifact_row(self) -> dict[str, object]:
        return {
            "condition_id": self.condition_id,
            "model_seed": self.model_seed,
            "epoch": self.epoch,
            "optimizer_step": self.optimizer_step,
            "episode_id": self.episode_id,
            "objectives": {
                objective_id: {
                    "eligible_count": row.eligible_count,
                    "raw_loss": row.raw_loss,
                    "weight": row.weight,
                    "weighted_contribution": row.weighted_contribution,
                    "unweighted_gradient_l2": row.unweighted_gradient_l2,
                    "weighted_gradient_l2": row.weighted_gradient_l2,
                }
                for objective_id, row in self.objectives.items()
            },
            "total_loss": self.total_loss,
            "pre_clip_total_gradient_l2": self.pre_clip_total_gradient_l2,
            "post_clip_total_gradient_l2": self.post_clip_total_gradient_l2,
        }


@dataclass(frozen=True, slots=True)
class CheckpointSnapshot:
    epoch: int
    state_dict: dict[str, Tensor]
    sha256: str


@dataclass(frozen=True, slots=True)
class TrainingResult:
    condition_id: str
    model_seed: int
    model: C15RevisionModel
    checkpoints: dict[int, CheckpointSnapshot]
    training_step_rows: tuple[TrainingStepRow, ...]
    parameter_count: int


@dataclass(frozen=True, slots=True)
class CheckpointScore:
    epoch: int
    weighted_objective_total: float


@dataclass(frozen=True, slots=True)
class CalibrationScore:
    temperature: float
    abstention_threshold: float
    belief_brier: float
    abstention_brier: float

    @property
    def total(self) -> float:
        return self.belief_brier + self.abstention_brier


def run_visible_episode(model: C15RevisionModel, episode: TrainingEpisode) -> EpisodeOutputs:
    episode.validate()
    model.reset_runtime()
    outputs = tuple(model.forward_fixture(call) for call in episode.model_calls)
    previous = outputs[episode.assessment_index - 1].conditional_belief_probabilities().detach()
    return EpisodeOutputs(
        outputs=outputs,
        assessment=outputs[episode.assessment_index],
        previous_probabilities=previous,
    )


def objective_target_with_state(
    episode: TrainingEpisode,
    outputs: EpisodeOutputs,
    *,
    restored_prior_activation: float,
) -> ObjectiveTarget:
    """Join evaluator labels with the controller state captured before assessment."""

    if not isinstance(episode.target, TrainingTarget):
        raise ValueError("weighted CE does not receive transition or recovery targets")
    if not math.isfinite(restored_prior_activation) or restored_prior_activation < 0.0:
        raise ValueError("restored_prior_activation must be finite and non-negative")
    return ObjectiveTarget(
        belief_index=episode.target.belief_index,
        previous_belief_index=episode.target.previous_belief_index,
        transition_target=episode.target.transition_target,
        sufficient_information=episode.target.sufficient_information,
        previous_probabilities=outputs.previous_probabilities,
        restored_prior_activation=restored_prior_activation,
        attribution_target_ids=episode.target.attribution_target_ids,
    )


def _checkpoint_hash(state_dict: Mapping[str, Tensor]) -> str:
    digest = hashlib.sha256()
    for name, tensor in sorted(state_dict.items()):
        value = tensor.detach().cpu().contiguous()
        digest.update(name.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(str(tuple(value.shape)).encode("ascii"))
        digest.update(value.numpy().tobytes(order="C"))
    return digest.hexdigest()


def _snapshot(model: C15RevisionModel, epoch: int) -> CheckpointSnapshot:
    state = {
        name: value.detach().cpu().clone() for name, value in sorted(model.state_dict().items())
    }
    return CheckpointSnapshot(epoch=epoch, state_dict=state, sha256=_checkpoint_hash(state))


def train_condition(
    fixtures: Sequence[TrainingEpisode | Mapping[str, object]],
    *,
    condition_id: str,
    model_seed: int,
    target_builder: Callable[[TrainingEpisode, EpisodeOutputs], ObjectiveTarget],
) -> TrainingResult:
    if condition_id not in CONDITION_ORDER:
        raise ValueError("condition_id is not preregistered")
    if model_seed not in MODEL_SEEDS:
        raise ValueError("model_seed is not preregistered")
    episodes = tuple(
        fixture if isinstance(fixture, TrainingEpisode) else TrainingEpisode.from_fixture(fixture)
        for fixture in fixtures
    )
    if len(episodes) != 64 or len({episode.episode_id for episode in episodes}) != 64:
        raise ValueError("C15 training requires exactly 64 unique ordered episodes")
    for episode in episodes:
        episode.validate()
        if condition_id == "one_weighted_ce":
            if not isinstance(episode.target, WeightedCETarget):
                raise ValueError("one_weighted_ce fixtures must expose only the final class target")
        elif not isinstance(episode.target, TrainingTarget):
            raise ValueError("separated-objective fixtures require transition targets")

    torch.manual_seed(model_seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    model = C15RevisionModel(RevisionModelConfig())
    model.train()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.01,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0.0,
        amsgrad=False,
    )
    weights = ObjectiveWeights.for_condition(condition_id)
    rows: list[TrainingStepRow] = []
    checkpoints: dict[int, CheckpointSnapshot] = {}
    optimizer_step = 0
    for epoch in range(1, 7):
        for episode in episodes:
            optimizer_step += 1
            optimizer.zero_grad(set_to_none=True)
            outputs = run_visible_episode(model, episode)
            if condition_id == "one_weighted_ce":
                if not isinstance(episode.target, WeightedCETarget):
                    raise RuntimeError("weighted CE target validation was bypassed")
                objective_target: ObjectiveTarget | WeightedCETarget = episode.target
            else:
                if not isinstance(episode.target, TrainingTarget):
                    raise RuntimeError("separated target validation was bypassed")
                objective_target = target_builder(episode, outputs)
                objective_target.validate()
                if (
                    objective_target.belief_index != episode.target.belief_index
                    or objective_target.previous_belief_index
                    != episode.target.previous_belief_index
                    or objective_target.transition_target != episode.target.transition_target
                    or objective_target.sufficient_information
                    != episode.target.sufficient_information
                    or objective_target.attribution_target_ids
                    != episode.target.attribution_target_ids
                    or not torch.equal(
                        objective_target.previous_probabilities,
                        outputs.previous_probabilities,
                    )
                ):
                    raise ValueError(
                        "target_builder changed frozen labels or model-derived history"
                    )
            bundle = compute_objective_losses(
                model=model,
                assessment=outputs.assessment,
                episode_outputs=outputs.outputs,
                target=objective_target,
                weights=weights,
                one_weighted_ce=condition_id == "one_weighted_ce",
            )
            objective_rows = objective_gradient_statistics(model, bundle)
            bundle.total_loss.backward()
            pre_clip = total_gradient_l2(model)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
            post_clip = total_gradient_l2(model)
            optimizer.step()
            model.detach_runtime()
            rows.append(
                TrainingStepRow(
                    condition_id=condition_id,
                    model_seed=model_seed,
                    epoch=epoch,
                    optimizer_step=optimizer_step,
                    episode_id=episode.episode_id,
                    objectives=objective_rows,
                    total_loss=float(bundle.total_loss.detach().cpu()),
                    pre_clip_total_gradient_l2=pre_clip,
                    post_clip_total_gradient_l2=post_clip,
                )
            )
        if epoch in CHECKPOINT_EPOCHS:
            checkpoints[epoch] = _snapshot(model, epoch)
    if optimizer_step != 384 or len(rows) != 384:
        raise RuntimeError("C15 optimizer-step contract violated")
    model.eval()
    model.reset_runtime()
    return TrainingResult(
        condition_id=condition_id,
        model_seed=model_seed,
        model=model,
        checkpoints=checkpoints,
        training_step_rows=tuple(rows),
        parameter_count=sum(parameter.numel() for parameter in model.parameters()),
    )


def select_checkpoint(scores: Sequence[CheckpointScore]) -> CheckpointScore:
    if {score.epoch for score in scores} != set(CHECKPOINT_EPOCHS) or len(scores) != 3:
        raise ValueError("checkpoint scores must contain epochs 2, 4, and 6 exactly once")
    if any(not math.isfinite(score.weighted_objective_total) for score in scores):
        raise ValueError("checkpoint scores must be finite")
    return min(scores, key=lambda score: (score.weighted_objective_total, score.epoch))


def select_calibration(scores: Sequence[CalibrationScore]) -> CalibrationScore:
    expected = {
        (temperature, threshold)
        for temperature in TEMPERATURE_GRID
        for threshold in ABSTENTION_THRESHOLD_GRID
    }
    actual = {(score.temperature, score.abstention_threshold) for score in scores}
    if actual != expected or len(scores) != len(expected):
        raise ValueError("calibration scores must contain the exact frozen 3x3 grid")
    if any(
        not math.isfinite(value)
        for score in scores
        for value in (score.belief_brier, score.abstention_brier)
    ):
        raise ValueError("calibration scores must be finite")
    return min(
        scores,
        key=lambda score: (score.total, score.temperature, score.abstention_threshold),
    )

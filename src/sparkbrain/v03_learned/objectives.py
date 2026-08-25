from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import Tensor, nn

from .model import C15RevisionModel, RevisionModelOutput

OBJECTIVE_ORDER = (
    "belief",
    "maintain",
    "update",
    "recovery",
    "no_ignition",
    "calibration",
    "attribution",
    "sparsity",
    "load_balance",
)
TRANSITION_ORDER = ("maintain", "update", "recover", "insufficient_information")
CONDITION_ORDER = (
    "full_separated",
    "no_belief",
    "no_maintain",
    "no_update",
    "no_recovery",
    "no_no_ignition",
    "no_calibration",
    "no_attribution",
    "no_sparsity",
    "no_load_balance",
    "one_weighted_ce",
    "no_residual",
)


@dataclass(frozen=True, slots=True)
class ObjectiveWeights:
    belief: float = 1.0
    maintain: float = 0.4
    update: float = 0.6
    recovery: float = 0.8
    no_ignition: float = 0.5
    calibration: float = 0.2
    attribution: float = 0.3
    sparsity: float = 0.02
    load_balance: float = 0.05

    def __post_init__(self) -> None:
        for objective_id in OBJECTIVE_ORDER:
            value = getattr(self, objective_id)
            if not math.isfinite(value) or value < 0.0:
                raise ValueError("objective weights must be finite and non-negative")

    def as_dict(self) -> dict[str, float]:
        return {objective_id: getattr(self, objective_id) for objective_id in OBJECTIVE_ORDER}

    @classmethod
    def for_condition(cls, condition_id: str) -> ObjectiveWeights:
        if condition_id not in CONDITION_ORDER:
            raise ValueError(f"unknown C15 condition: {condition_id}")
        values = cls().as_dict()
        if condition_id.startswith("no_") and condition_id != "no_residual":
            objective_id = condition_id.removeprefix("no_")
            values[objective_id] = 0.0
        elif condition_id == "one_weighted_ce":
            values = {objective_id: 0.0 for objective_id in OBJECTIVE_ORDER}
        return cls(**values)


@dataclass(frozen=True, slots=True)
class ObjectiveTarget:
    belief_index: int
    previous_belief_index: int
    transition_target: str
    sufficient_information: bool
    previous_probabilities: Tensor
    restored_prior_activation: float
    attribution_target_ids: tuple[str, ...]

    def validate(self) -> None:
        for name in ("belief_index", "previous_belief_index"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value not in range(3):
                raise ValueError(f"{name} must be an integer in [0, 2]")
        if self.transition_target not in TRANSITION_ORDER:
            raise ValueError("transition_target is invalid")
        if not isinstance(self.sufficient_information, bool):
            raise ValueError("sufficient_information must be bool")
        if self.previous_probabilities.shape != (3,) or not bool(
            torch.isfinite(self.previous_probabilities).all()
        ):
            raise ValueError("previous_probabilities must be a finite three-vector")
        if not math.isfinite(self.restored_prior_activation) or self.restored_prior_activation < 0:
            raise ValueError("restored_prior_activation must be finite and non-negative")
        if len(set(self.attribution_target_ids)) != len(self.attribution_target_ids):
            raise ValueError("attribution_target_ids must be unique")
        if len(self.attribution_target_ids) > 2 or any(
            not isinstance(value, str) or not value for value in self.attribution_target_ids
        ):
            raise ValueError("attribution_target_ids must contain zero to two opaque IDs")


@dataclass(frozen=True, slots=True)
class WeightedCETarget:
    """Evaluator target exposed to the matched four-class CE baseline only."""

    belief_index: int
    sufficient_information: bool

    def validate(self) -> None:
        if (
            isinstance(self.belief_index, bool)
            or not isinstance(self.belief_index, int)
            or self.belief_index not in range(3)
        ):
            raise ValueError("belief_index must be an integer in [0, 2]")
        if not isinstance(self.sufficient_information, bool):
            raise ValueError("sufficient_information must be bool")


@dataclass(frozen=True, slots=True)
class ObjectiveLossTerm:
    raw_loss: Tensor
    weight: float
    eligible_count: int

    @property
    def weighted_contribution(self) -> Tensor:
        if self.weight == 0.0:
            return self.raw_loss.detach() * 0.0
        return self.raw_loss * self.weight

    @property
    def ablated(self) -> bool:
        return self.weight == 0.0


@dataclass(frozen=True, slots=True)
class ObjectiveLossBundle:
    terms: dict[str, ObjectiveLossTerm]
    total_loss: Tensor
    baseline_loss: Tensor | None


@dataclass(frozen=True, slots=True)
class ObjectiveGradientRow:
    eligible_count: int
    raw_loss: float
    weight: float
    weighted_contribution: float
    unweighted_gradient_l2: float
    weighted_gradient_l2: float


def _connected_zero(model: C15RevisionModel) -> Tensor:
    return sum((parameter.sum() * 0.0 for parameter in model.parameters()), torch.tensor(0.0))


def _router_rows(outputs: tuple[RevisionModelOutput, ...]) -> Tensor:
    rows = [output.router_probabilities[output.attribution_mask] for output in outputs]
    if not rows or not any(row.numel() for row in rows):
        raise ValueError("episode outputs must contain visible evidence")
    return torch.cat(rows, dim=0)


def compute_objective_losses(
    *,
    model: C15RevisionModel,
    assessment: RevisionModelOutput,
    episode_outputs: tuple[RevisionModelOutput, ...],
    target: ObjectiveTarget | WeightedCETarget,
    weights: ObjectiveWeights,
    one_weighted_ce: bool = False,
) -> ObjectiveLossBundle:
    """Compute the nine preregistered objectives after model prediction."""

    target.validate()
    zero = _connected_zero(model)
    sufficient = target.sufficient_information
    truth = torch.tensor(
        target.belief_index, dtype=torch.long, device=assessment.belief_logits.device
    )

    if one_weighted_ce:
        if not isinstance(target, WeightedCETarget):
            raise ValueError("one_weighted_ce must not receive transition objectives")
        if any(value != 0.0 for value in weights.as_dict().values()):
            raise ValueError("one_weighted_ce requires every auxiliary weight to be zero")
        logits = torch.cat((assessment.belief_logits, assessment.abstention_logit.reshape(1)))
        baseline_target = target.belief_index if sufficient else 3
        baseline_loss = nn.functional.cross_entropy(
            logits.unsqueeze(0),
            torch.tensor([baseline_target], dtype=torch.long, device=logits.device),
            weight=torch.ones(4, device=logits.device),
        )
        terms = {
            objective_id: ObjectiveLossTerm(raw_loss=zero, weight=0.0, eligible_count=0)
            for objective_id in OBJECTIVE_ORDER
        }
        return ObjectiveLossBundle(
            terms=terms,
            total_loss=baseline_loss,
            baseline_loss=baseline_loss,
        )
    if not isinstance(target, ObjectiveTarget):
        raise ValueError("separated objectives require the frozen transition target")

    def transition_is(value: str) -> float:
        return float(target.transition_target == value)

    if sufficient:
        belief = nn.functional.cross_entropy(
            assessment.belief_logits.unsqueeze(0),
            truth.unsqueeze(0),
            weight=torch.ones(3, device=assessment.belief_logits.device),
        )
        probabilities = torch.softmax(assessment.belief_logits, dim=-1)
        one_hot = nn.functional.one_hot(truth, num_classes=3).to(probabilities.dtype)
        calibration = torch.sum((probabilities - one_hot) ** 2)
        maintain = nn.functional.binary_cross_entropy_with_logits(
            assessment.maintain_logit,
            torch.tensor(transition_is("maintain"), device=assessment.maintain_logit.device),
        )
        if target.transition_target == "maintain":
            maintain = maintain + torch.mean(
                torch.abs(probabilities - target.previous_probabilities.detach().to(probabilities))
            )
        update = nn.functional.binary_cross_entropy_with_logits(
            assessment.update_logit,
            torch.tensor(transition_is("update"), device=assessment.update_logit.device),
        )
        if target.transition_target == "update":
            update = update + nn.functional.softplus(
                -(
                    assessment.belief_logits[target.belief_index]
                    - assessment.belief_logits[target.previous_belief_index]
                )
            )
        recovery = nn.functional.binary_cross_entropy_with_logits(
            assessment.recovery_logit,
            torch.tensor(transition_is("recover"), device=assessment.recovery_logit.device),
        )
        if target.transition_target == "recover":
            recovery = recovery + torch.relu(
                torch.tensor(
                    0.15 - target.restored_prior_activation,
                    dtype=assessment.belief_logits.dtype,
                    device=assessment.belief_logits.device,
                )
            )
    else:
        belief = calibration = maintain = update = recovery = zero

    no_ignition = nn.functional.binary_cross_entropy_with_logits(
        assessment.abstention_logit,
        torch.tensor(
            float(not sufficient),
            dtype=assessment.abstention_logit.dtype,
            device=assessment.abstention_logit.device,
        ),
    )
    attribution_target_set = set(target.attribution_target_ids)
    attribution_targets = torch.tensor(
        [
            float(evidence_id in attribution_target_set) if evidence_id is not None else 0.0
            for evidence_id in assessment.evidence_ids
        ],
        dtype=assessment.attribution_logits.dtype,
        device=assessment.attribution_logits.device,
    )
    visible = assessment.attribution_mask
    attribution = (
        nn.functional.binary_cross_entropy_with_logits(
            assessment.attribution_logits[visible], attribution_targets[visible]
        )
        if bool(visible.any())
        else zero
    )
    router_rows = _router_rows(episode_outputs)
    sparsity = torch.mean(
        -torch.sum(router_rows * torch.log(torch.clamp(router_rows, min=1e-12)), dim=-1)
        / math.log(model.config.module_count)
    )
    mean_load = router_rows.mean(dim=0)
    load_balance = torch.mean((mean_load - 1.0 / model.config.module_count) ** 2)

    raw_losses = {
        "belief": belief,
        "maintain": maintain,
        "update": update,
        "recovery": recovery,
        "no_ignition": no_ignition,
        "calibration": calibration,
        "attribution": attribution,
        "sparsity": sparsity,
        "load_balance": load_balance,
    }
    eligible = {
        "belief": int(sufficient),
        "maintain": int(sufficient),
        "update": int(sufficient),
        "recovery": int(sufficient),
        "no_ignition": 1,
        "calibration": int(sufficient),
        "attribution": int(visible.sum().item()),
        "sparsity": int(router_rows.shape[0]),
        "load_balance": int(router_rows.shape[0]),
    }
    terms = {
        objective_id: ObjectiveLossTerm(
            raw_loss=raw_losses[objective_id],
            weight=getattr(weights, objective_id),
            eligible_count=eligible[objective_id],
        )
        for objective_id in OBJECTIVE_ORDER
    }
    total = sum((term.weighted_contribution for term in terms.values()), zero)
    return ObjectiveLossBundle(terms=terms, total_loss=total, baseline_loss=None)


def _gradient_l2(
    loss: Tensor,
    parameters: tuple[Tensor, ...],
    *,
    retain_graph: bool,
) -> float:
    gradients = torch.autograd.grad(
        loss,
        parameters,
        allow_unused=True,
        retain_graph=retain_graph,
    )
    squares = [torch.sum(gradient.detach() ** 2) for gradient in gradients if gradient is not None]
    if not squares:
        return 0.0
    return float(torch.sqrt(torch.stack(squares).sum()).cpu())


def objective_gradient_statistics(
    model: C15RevisionModel,
    bundle: ObjectiveLossBundle,
) -> dict[str, ObjectiveGradientRow]:
    named = sorted(
        (
            (name, parameter)
            for name, parameter in model.named_parameters()
            if parameter.requires_grad
        ),
        key=lambda item: item[0],
    )
    parameters = tuple(parameter for _, parameter in named)
    rows: dict[str, ObjectiveGradientRow] = {}
    for objective_id in OBJECTIVE_ORDER:
        term = bundle.terms[objective_id]
        raw_norm = (
            0.0
            if term.eligible_count == 0
            else _gradient_l2(term.raw_loss, parameters, retain_graph=True)
        )
        weighted_norm = (
            0.0
            if term.weight == 0.0 or term.eligible_count == 0
            else _gradient_l2(term.raw_loss * term.weight, parameters, retain_graph=True)
        )
        rows[objective_id] = ObjectiveGradientRow(
            eligible_count=term.eligible_count,
            raw_loss=0.0 if term.eligible_count == 0 else float(term.raw_loss.detach().cpu()),
            weight=term.weight,
            weighted_contribution=(
                0.0
                if term.weight == 0.0 or term.eligible_count == 0
                else float((term.raw_loss * term.weight).detach().cpu())
            ),
            unweighted_gradient_l2=raw_norm,
            weighted_gradient_l2=weighted_norm,
        )
    return rows


def total_gradient_l2(model: C15RevisionModel) -> float:
    squares = [
        torch.sum(parameter.grad.detach() ** 2)
        for _, parameter in sorted(model.named_parameters(), key=lambda item: item[0])
        if parameter.requires_grad and parameter.grad is not None
    ]
    return 0.0 if not squares else float(torch.sqrt(torch.stack(squares).sum()).cpu())

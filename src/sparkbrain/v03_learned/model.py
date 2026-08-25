from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import torch
from torch import Tensor, nn

_FORBIDDEN_MODEL_KEYS = {
    "answer",
    "decision_justified",
    "evaluator",
    "expected",
    "label",
    "belief_index",
    "episode_seed",
    "previous_belief_index",
    "previous_truth_belief",
    "recovery_opportunity",
    "scenario_tags",
    "split",
    "sufficient_information",
    "target",
    "test_only",
    "transition_target",
    "truth",
    "truth_belief",
    "update_required",
}


def _normalized_key(value: object) -> str:
    return str(value).strip().lower().replace("-", "_")


def _reject_evaluator_fields(value: object, *, path: str = "fixture") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if _normalized_key(key) in _FORBIDDEN_MODEL_KEYS:
                raise ValueError(f"forbidden evaluator field at {path}.{key}")
            _reject_evaluator_fields(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_evaluator_fields(child, path=f"{path}[{index}]")


@dataclass(frozen=True, slots=True)
class RevisionModelConfig:
    feature_dimension: int = 12
    hidden_dimension: int = 16
    module_count: int = 4
    active_k: int = 2
    candidate_slots: int = 5

    def validate(self) -> None:
        if self.feature_dimension != 12:
            raise ValueError("C15 feature_dimension must be 12")
        if self.hidden_dimension != 16:
            raise ValueError("C15 hidden_dimension must be 16")
        if self.module_count != 4:
            raise ValueError("C15 module_count must be 4")
        if self.active_k != 2:
            raise ValueError("C15 active_k must be 2")
        if self.candidate_slots != 5:
            raise ValueError("C15 candidate_slots must be 5")


@dataclass(frozen=True, slots=True)
class RevisionModelOutput:
    entity_key: str
    belief_logits: Tensor
    maintain_logit: Tensor
    update_logit: Tensor
    recovery_logit: Tensor
    abstention_logit: Tensor
    attribution_logits: Tensor
    attribution_mask: Tensor
    evidence_ids: tuple[str | None, ...]
    router_probabilities: Tensor
    selected_modules: Tensor
    hidden_state: Tensor

    def conditional_belief_probabilities(self, *, temperature: float = 1.0) -> Tensor:
        if not math.isfinite(temperature) or temperature <= 0.0:
            raise ValueError("temperature must be finite and positive")
        return torch.softmax(self.belief_logits / temperature, dim=-1)

    def transition_probabilities(self) -> Tensor:
        logits = torch.stack(
            (
                self.abstention_logit,
                self.maintain_logit,
                self.recovery_logit,
                self.update_logit,
            )
        )
        return torch.softmax(logits, dim=-1)


class C15RevisionModel(nn.Module):
    """Deterministic CPU reference model frozen by the C15 preregistration."""

    def __init__(self, config: RevisionModelConfig | None = None) -> None:
        super().__init__()
        self.config = config or RevisionModelConfig()
        self.config.validate()
        hidden = self.config.hidden_dimension
        self.evidence_encoder = nn.Linear(self.config.feature_dimension, hidden)
        self.router = nn.Linear(hidden, self.config.module_count)
        self.module_transforms = nn.ModuleList(
            nn.Linear(hidden, hidden) for _ in range(self.config.module_count)
        )
        self.entity_gru = nn.GRUCell(hidden, hidden)
        self.belief_head = nn.Linear(hidden, 3)
        self.maintain_head = nn.Linear(hidden, 1)
        self.update_head = nn.Linear(hidden, 1)
        self.recovery_head = nn.Linear(hidden, 1)
        self.abstention_head = nn.Linear(hidden, 1)
        self.attribution_head = nn.Linear(hidden, 1)
        self._entity_states: dict[str, Tensor] = {}

    def reset_runtime(self) -> None:
        self._entity_states.clear()

    def detach_runtime(self) -> None:
        self._entity_states = {
            key: value.detach() for key, value in sorted(self._entity_states.items())
        }

    def runtime_state(self, entity_key: str) -> Tensor | None:
        value = self._entity_states.get(entity_key)
        return None if value is None else value.detach().clone()

    @staticmethod
    def _selected_indices(probabilities: Tensor, active_k: int) -> Tensor:
        rows: list[list[int]] = []
        for row in probabilities.detach().cpu().tolist():
            rows.append(sorted(range(len(row)), key=lambda index: (-row[index], index))[:active_k])
        return torch.tensor(rows, dtype=torch.long, device=probabilities.device)

    def forward_visible(
        self,
        *,
        entity_key: str,
        features: Tensor,
        evidence_ids: Sequence[str | None],
        padding_mask: Tensor,
    ) -> RevisionModelOutput:
        if not isinstance(entity_key, str) or not entity_key.strip():
            raise ValueError("entity_key must be a non-empty opaque string")
        if features.shape != (self.config.candidate_slots, self.config.feature_dimension):
            raise ValueError("features must have shape [5, 12]")
        if features.dtype not in (torch.float32, torch.float64):
            raise ValueError("features must use a floating dtype")
        if not bool(torch.isfinite(features).all()):
            raise ValueError("features must be finite")
        if padding_mask.shape != (self.config.candidate_slots,) or padding_mask.dtype != torch.bool:
            raise ValueError("padding_mask must be a bool tensor with shape [5]")
        if len(evidence_ids) != self.config.candidate_slots:
            raise ValueError("evidence_ids must have exactly five entries")
        if not bool(padding_mask.any()):
            raise ValueError("at least one non-padding evidence slot is required")
        for index, evidence_id in enumerate(evidence_ids):
            if bool(padding_mask[index]):
                if not isinstance(evidence_id, str) or not evidence_id:
                    raise ValueError("non-padding evidence slots require opaque IDs")
            elif evidence_id is not None:
                raise ValueError("padding evidence IDs must be null")

        encoded = torch.tanh(self.evidence_encoder(features))
        router_probabilities = torch.softmax(self.router(encoded), dim=-1)
        selected = self._selected_indices(router_probabilities, self.config.active_k)
        transformed: list[Tensor] = []
        for row_index in range(self.config.candidate_slots):
            module_rows = [
                torch.tanh(self.module_transforms[module_index](encoded[row_index]))
                for module_index in selected[row_index].tolist()
            ]
            transformed.append(torch.stack(module_rows).mean(dim=0))
        transformed_rows = torch.stack(transformed)
        episode_input = transformed_rows[padding_mask].mean(dim=0)
        previous = self._entity_states.get(entity_key)
        if previous is None:
            previous = torch.zeros(
                self.config.hidden_dimension,
                dtype=episode_input.dtype,
                device=episode_input.device,
            )
        hidden = self.entity_gru(episode_input, previous)
        self._entity_states[entity_key] = hidden
        attribution_logits = self.attribution_head(encoded).squeeze(-1)
        return RevisionModelOutput(
            entity_key=entity_key,
            belief_logits=self.belief_head(hidden),
            maintain_logit=self.maintain_head(hidden).squeeze(-1),
            update_logit=self.update_head(hidden).squeeze(-1),
            recovery_logit=self.recovery_head(hidden).squeeze(-1),
            abstention_logit=self.abstention_head(hidden).squeeze(-1),
            attribution_logits=attribution_logits,
            attribution_mask=padding_mask.clone(),
            evidence_ids=tuple(evidence_ids),
            router_probabilities=router_probabilities,
            selected_modules=selected,
            hidden_state=hidden,
        )

    def forward_fixture(self, fixture: Mapping[str, object]) -> RevisionModelOutput:
        """Run one production-visible call without accepting evaluator-owned targets."""

        _reject_evaluator_fields(fixture)
        expected = {"entity_key", "features", "evidence_ids", "padding_mask"}
        if set(fixture) != expected:
            raise ValueError("model fixture has missing or unknown fields")
        features = torch.as_tensor(fixture["features"], dtype=torch.float32)
        padding_mask = torch.as_tensor(fixture["padding_mask"], dtype=torch.bool)
        raw_evidence_ids = fixture["evidence_ids"]
        if not isinstance(raw_evidence_ids, Sequence) or isinstance(raw_evidence_ids, str):
            raise ValueError("evidence_ids must be a sequence")
        entity_key = fixture["entity_key"]
        if not isinstance(entity_key, str):
            raise ValueError("entity_key must be a string")
        return self.forward_visible(
            entity_key=entity_key,
            features=features,
            evidence_ids=tuple(raw_evidence_ids),
            padding_mask=padding_mask,
        )

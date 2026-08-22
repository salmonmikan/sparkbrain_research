from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn

from ..learned.config import LearnedConfig
from ..learned.model import EventEncoder
from .config import StructuralConfig


@dataclass(slots=True)
class StructuralStep:
    logits: Tensor
    action_logits: Tensor
    probabilities: Tensor
    router_probabilities: Tensor
    selected: Tensor
    selected_edges: Tensor
    support: Tensor
    diversity: Tensor
    stability: Tensor
    contradiction: Tensor
    coalition_score: Tensor


class StructuralSparseModel(nn.Module):
    def __init__(self, learned: LearnedConfig, structural: StructuralConfig) -> None:
        super().__init__()
        structural.validate()
        self.learned_config = LearnedConfig.from_dict(
            {**learned.to_dict(), "module_count": structural.max_modules}
        )
        self.structural_config = structural
        config = self.learned_config
        self.encoder = EventEncoder(config)
        self.router = nn.Linear(config.event_dim, config.module_count)
        self.event_to_state = nn.Linear(config.event_dim, config.hidden_dim)
        self.update = nn.GRUCell(config.hidden_dim, config.hidden_dim)
        self.edge_weights = nn.Parameter(torch.empty(config.module_count, config.module_count))
        self.belief_head = nn.Linear(config.hidden_dim, len(config.labels))
        self.residual_head = nn.Linear(config.event_dim, len(config.labels), bias=False)
        self.action_head = nn.Linear(config.hidden_dim, len(config.labels))
        self.coalition_head = nn.Linear(4, 1, bias=False)
        nn.init.normal_(self.edge_weights, std=0.08)
        active_modules = torch.zeros(config.module_count, dtype=torch.bool)
        active_modules[: structural.source_modules] = True
        active_edges = torch.zeros(config.module_count, config.module_count, dtype=torch.bool)
        for index in range(structural.source_modules):
            active_edges[index, index] = True
            active_edges[index, (index + 1) % structural.source_modules] = True
        self.register_buffer("active_module_mask", active_modules)
        self.register_buffer("active_edge_mask", active_edges)
        self.register_buffer(
            "module_state", torch.zeros(config.module_count, config.hidden_dim), persistent=False
        )
        self.register_buffer(
            "previous_probabilities",
            torch.full((len(config.labels),), 1 / len(config.labels)),
            persistent=False,
        )

    def import_source(self, source_state: dict[str, Tensor], source_modules: int) -> None:
        current = self.state_dict()
        copied: dict[str, Tensor] = {}
        for key, target in current.items():
            if key not in source_state:
                continue
            source = source_state[key]
            if source.shape == target.shape:
                copied[key] = source
            elif key == "router.weight":
                value = target.clone()
                value[:source_modules] = source[:source_modules]
                copied[key] = value
            elif key == "router.bias":
                value = target.clone()
                value[:source_modules] = source[:source_modules]
                copied[key] = value
            elif key == "edge_weights":
                value = target.clone()
                value[:source_modules, :source_modules] = source[
                    :source_modules, :source_modules
                ]
                copied[key] = value
        self.load_state_dict(copied, strict=False)

    def reset_runtime(self) -> None:
        self.module_state = torch.zeros_like(self.module_state)
        self.previous_probabilities = torch.full_like(
            self.previous_probabilities, 1 / len(self.learned_config.labels)
        )

    def forward_step(
        self, *, evidence: str, source: str, channel: str, strength: float, delay: float
    ) -> StructuralStep:
        encoded = self.encoder(evidence, source, channel, strength, delay)
        router_logits = self.router(encoded).masked_fill(~self.active_module_mask, -torch.inf)
        router_probabilities = torch.softmax(router_logits, dim=-1)
        selected = torch.topk(
            router_logits, k=self.structural_config.active_k, sorted=True
        ).indices
        previous = self.module_state.index_select(0, selected)
        selected_edge_mask = self.active_edge_mask.index_select(0, selected).index_select(
            1, selected
        )
        local_sources, local_targets = torch.where(selected_edge_mask)
        if local_sources.numel():
            global_sources = selected.index_select(0, local_sources)
            global_targets = selected.index_select(0, local_targets)
            weights = self.edge_weights[global_sources, global_targets].tanh().unsqueeze(1)
            contributions = weights * previous.index_select(0, local_sources)
            messages = torch.zeros_like(previous).index_add(0, local_targets, contributions)
            counts = torch.zeros(len(selected), device=encoded.device).index_add(
                0, local_targets, torch.ones_like(local_targets, dtype=torch.float32)
            )
            messages = messages / counts.clamp_min(1).unsqueeze(1)
            selected_edges = torch.stack((global_sources, global_targets), dim=1)
        else:
            messages = torch.zeros_like(previous)
            selected_edges = torch.empty((0, 2), dtype=torch.long, device=encoded.device)
        event_state = torch.tanh(self.event_to_state(encoded)).expand(len(selected), -1)
        updated = self.update(event_state + messages, previous)
        updated = (
            self.learned_config.persistence * updated
            + (1 - self.learned_config.persistence) * previous
        )
        self.module_state = self.module_state.clone().index_copy(0, selected, updated)
        pooled = updated.mean(0)
        logits = self.belief_head(pooled) + self.learned_config.residual_scale * self.residual_head(
            encoded
        )
        probabilities = torch.softmax(logits, dim=-1)
        action_logits = self.action_head(pooled)
        support = probabilities.max()
        diversity = router_probabilities.gather(0, selected).sum() / len(selected)
        stability = 1 - torch.abs(probabilities - self.previous_probabilities).mean()
        contradiction = 1 - torch.dot(probabilities, self.previous_probabilities)
        components = torch.stack((support, diversity, stability, -contradiction))
        coalition_score = self.coalition_head(components).squeeze()
        self.previous_probabilities = probabilities
        return StructuralStep(
            logits,
            action_logits,
            probabilities,
            router_probabilities,
            selected,
            selected_edges,
            support,
            diversity,
            stability,
            contradiction,
            coalition_score,
        )

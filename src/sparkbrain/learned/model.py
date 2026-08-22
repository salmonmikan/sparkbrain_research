from __future__ import annotations

import hashlib
from dataclasses import dataclass

import torch
from torch import Tensor, nn

from .config import LearnedConfig


def stable_bucket(value: str, buckets: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % buckets


@dataclass(slots=True)
class StepOutput:
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


class EventEncoder(nn.Module):
    def __init__(self, config: LearnedConfig) -> None:
        super().__init__()
        self.config = config
        part = (config.event_dim - 2) // 3
        self.evidence = nn.Embedding(config.hash_buckets, part)
        self.source = nn.Embedding(config.hash_buckets, part)
        self.channel = nn.Embedding(config.hash_buckets, part)
        self.numeric = nn.Linear(2, config.event_dim - 3 * part)

    def forward(
        self, evidence: str, source: str, channel: str, strength: float, delay: float
    ) -> Tensor:
        device = self.evidence.weight.device
        indices = [
            torch.tensor(stable_bucket(value, self.config.hash_buckets), device=device)
            for value in (evidence, source, channel)
        ]
        numeric = torch.tensor([strength, delay], dtype=torch.float32, device=device)
        return torch.cat(
            (
                self.evidence(indices[0]),
                self.source(indices[1]),
                self.channel(indices[2]),
                torch.tanh(self.numeric(numeric)),
            )
        )


class SparseRoutingModel(nn.Module):
    """Rate backend whose local recurrent work is restricted to selected nodes."""

    def __init__(self, config: LearnedConfig) -> None:
        super().__init__()
        config.validate()
        self.config = config
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
        self.register_buffer(
            "module_state", torch.zeros(config.module_count, config.hidden_dim), persistent=False
        )
        self.register_buffer(
            "previous_probabilities", torch.full((len(config.labels),), 1 / len(config.labels)),
            persistent=False,
        )

    def reset_runtime(self) -> None:
        self.module_state = torch.zeros_like(self.module_state)
        self.previous_probabilities = torch.full_like(
            self.previous_probabilities, 1 / len(self.config.labels)
        )

    def forward_step(
        self,
        *,
        evidence: str,
        source: str,
        channel: str,
        strength: float,
        delay: float,
        condition: str | None = None,
        generator: torch.Generator | None = None,
    ) -> StepOutput:
        condition = condition or self.config.condition
        encoded = self.encoder(evidence, source, channel, strength, delay)
        router_logits = self.router(encoded)
        router_probabilities = torch.softmax(router_logits, dim=-1)
        k = self.config.module_count if condition == "dense_recurrent" else self.config.active_k
        if condition == "random_router":
            selected = torch.randperm(
                self.config.module_count, generator=generator, device=encoded.device
            )[:k]
        else:
            selected = torch.topk(router_logits, k=k, sorted=True).indices

        previous = self.module_state.index_select(0, selected)
        local_edges = self.edge_weights.index_select(0, selected).index_select(1, selected)
        normalizer = max(1, k - 1)
        messages = torch.tanh(local_edges) @ previous / normalizer
        event_state = torch.tanh(self.event_to_state(encoded)).expand(k, -1)
        updated = self.update(event_state + messages, previous)
        if condition != "no_persistent_state":
            updated = self.config.persistence * updated + (1 - self.config.persistence) * previous
        new_state = self.module_state.clone()
        new_state = new_state.index_copy(0, selected, updated)
        self.module_state = (
            new_state if condition != "no_persistent_state" else torch.zeros_like(new_state)
        )

        pooled = updated.mean(dim=0)
        logits = self.belief_head(pooled)
        if condition != "no_residual":
            logits = logits + self.config.residual_scale * self.residual_head(encoded)
        probabilities = torch.softmax(logits, dim=-1)
        action_logits = self.action_head(pooled)

        support = probabilities.max()
        diversity = router_probabilities.gather(0, selected).sum() / k
        stability = 1.0 - torch.abs(probabilities - self.previous_probabilities).mean()
        contradiction = 1.0 - torch.dot(probabilities, self.previous_probabilities)
        components = torch.stack((support, diversity, stability, -contradiction))
        if condition == "detached_coalition" or not self.config.coalition_end_to_end:
            components = components.detach()
        coalition_score = (
            support
            if condition == "no_coalition_score"
            else self.coalition_head(components).squeeze()
        )
        self.previous_probabilities = probabilities

        edge_pairs = torch.cartesian_prod(selected, selected)
        return StepOutput(
            logits,
            action_logits,
            probabilities,
            router_probabilities,
            selected,
            edge_pairs,
            support,
            diversity,
            stability,
            contradiction,
            coalition_score,
        )

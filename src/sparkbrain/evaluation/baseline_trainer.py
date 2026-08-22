from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..baselines.neural import FeatureEncoder
from ..baselines.neural.common import EncodedEpisode, require_torch


@dataclass(frozen=True, slots=True)
class TrainingResult:
    steps_completed: int
    examples_seen: int
    final_loss: float
    failed: bool
    error: str | None = None


def train_module(
    module: Any,
    encoder: FeatureEncoder,
    episodes: list[Any],
    *,
    optimizer_steps: int,
    learning_rate: float,
) -> TrainingResult:
    torch = require_torch()
    encoded = [encoder.encode_episode(episode) for episode in episodes]
    optimizer = torch.optim.Adam(module.parameters(), lr=learning_rate)
    module.train()
    completed = 0
    examples = 0
    loss_value = float("nan")
    try:
        for index in range(optimizer_steps):
            row: EncodedEpisode = encoded[index % len(encoded)]
            features = torch.tensor([row.features], dtype=torch.float32)
            targets = torch.tensor([row.targets], dtype=torch.long)
            optimizer.zero_grad(set_to_none=True)
            logits = module(features)
            loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, logits.shape[-1]), targets.reshape(-1)
            )
            loss.backward()
            optimizer.step()
            completed += 1
            examples += len(row.targets)
            loss_value = float(loss.detach())
    except (RuntimeError, ValueError) as exc:
        return TrainingResult(completed, examples, loss_value, True, str(exc))
    return TrainingResult(completed, examples, loss_value, False)

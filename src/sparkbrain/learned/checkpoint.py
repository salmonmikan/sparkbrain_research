from __future__ import annotations

from pathlib import Path
from typing import Any

import torch

from .config import LearnedConfig
from .model import SparseRoutingModel


def save_checkpoint(
    path: str | Path,
    *,
    config: LearnedConfig,
    model: SparseRoutingModel,
    metadata: dict[str, Any] | None = None,
) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "schema_version": "0.2",
            "backend": "learned-sparse-rate",
            "config": config.to_dict(),
            "model": model.state_dict(),
            "metadata": metadata or {},
        },
        target,
    )


def load_checkpoint(path: str | Path) -> tuple[LearnedConfig, SparseRoutingModel, dict[str, Any]]:
    payload = torch.load(Path(path), map_location="cpu", weights_only=True)
    if payload.get("schema_version") != "0.2" or payload.get("backend") != "learned-sparse-rate":
        raise ValueError("Unsupported learned checkpoint")
    config = LearnedConfig.from_dict(payload["config"])
    model = SparseRoutingModel(config)
    model.load_state_dict(payload["model"])
    model.eval()
    return config, model, dict(payload.get("metadata", {}))

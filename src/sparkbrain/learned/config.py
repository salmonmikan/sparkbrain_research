from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any


@dataclass(frozen=True, slots=True)
class LearnedConfig:
    schema_version: str = "0.2"
    seed: int = 41
    labels: tuple[str, ...] = ("cat", "dog", "toy")
    hash_buckets: int = 128
    event_dim: int = 24
    hidden_dim: int = 24
    module_count: int = 12
    active_k: int = 4
    learning_rate: float = 0.012
    epochs: int = 4
    train_episodes: int = 48
    calibration_episodes: int = 12
    test_episodes: int = 60
    steps: int = 24
    confidence_threshold: float = 0.48
    margin_threshold: float = 0.08
    residual_scale: float = 1.0
    persistence: float = 0.75
    belief_loss: float = 1.0
    revision_loss: float = 0.15
    ignition_loss: float = 0.10
    load_balance_loss: float = 0.02
    sparsity_loss: float = 0.005
    provenance_loss: float = 0.02
    recovery_loss: float = 0.10
    trace_consistency_loss: float = 0.02
    workspace_broadcast: bool = True
    coalition_end_to_end: bool = True
    condition: str = "full"
    device: str = "cpu"

    def validate(self) -> None:
        if self.schema_version != "0.2":
            raise ValueError("Learned config must preserve schema version 0.2")
        if not 1 <= self.active_k <= self.module_count:
            raise ValueError("active_k must be between one and module_count")
        if self.device != "cpu":
            raise ValueError("C04 reference configuration is CPU-only")
        for name in ("hash_buckets", "event_dim", "hidden_dim", "module_count", "epochs"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> LearnedConfig:
        allowed = {item.name for item in fields(cls)}
        values = {key: value for key, value in row.items() if key in allowed}
        if "labels" in values:
            values["labels"] = tuple(values["labels"])
        result = cls(**values)
        result.validate()
        return result

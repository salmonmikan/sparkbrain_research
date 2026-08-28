from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SensoryChannelDecision:
    channel: str
    accepted: bool
    reason: str | None = None
    activation: float | None = None
    threshold: float | None = None
    novelty: float | None = None
    prediction_error: float | None = None
    goal_contribution: float | None = None
    habituation: float | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class V032StepResult:
    base_result: Any
    sensory_channel_trace: tuple[SensoryChannelDecision, ...]
    accepted_channels: tuple[str, ...]
    suppressed_channels: tuple[str, ...]
    suppression_reasons: Mapping[str, int]
    dense_inspection_count: int

    def to_dict(self) -> dict[str, Any]:
        from .jsonsafe import json_safe
        return {
            'base_result': json_safe(self.base_result),
            'sensory_channel_trace': [json_safe(item) for item in self.sensory_channel_trace],
            'accepted_channels': list(self.accepted_channels),
            'suppressed_channels': list(self.suppressed_channels),
            'suppression_reasons': dict(self.suppression_reasons),
            'dense_inspection_count': self.dense_inspection_count,
        }

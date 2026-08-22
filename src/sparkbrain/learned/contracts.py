from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

LEARNED_CONTRACT_VERSION = "0.2"


@dataclass(frozen=True, slots=True)
class LearnedExample:
    """Additive C04/C05 example contract backed by a C02 observation."""

    episode_id: str
    world_id: str
    split: str
    step_index: int
    evidence_label: str
    source_id: str
    channel: str
    strength: float
    delivery_delay: float
    belief_truth: str
    optimal_action: str | None
    update_required: bool
    scenario_tags: tuple[str, ...] = ()
    object_id: str | None = None


@dataclass(frozen=True, slots=True)
class PredictionRecord:
    belief: str | None
    action: str | None
    probabilities: dict[str, float]
    selected_modules: tuple[int, ...]
    evidence_path: tuple[tuple[int, int], ...]
    coalition: dict[str, float]


@dataclass(slots=True)
class WorkCounters:
    observations: int = 0
    conceptual_candidates: int = 0
    selected_modules: int = 0
    state_updates: int = 0
    evaluated_edges: int = 0
    evaluated_messages: int = 0
    dense_tensor_ops: int = 0
    kernel_launch_estimate: int = 0
    wall_clock_seconds: float = 0.0
    peak_memory_bytes: int = 0

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    condition: str
    split: str
    examples: int
    accuracy: float
    covered_accuracy: float | None
    coverage: float
    chance_accuracy: float
    nonlearning_accuracy: float
    recovery_count: int
    routing_entropy: float
    module_loads: tuple[int, ...]
    counters: dict[str, int | float]
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

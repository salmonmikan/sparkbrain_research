from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class SparkKind(StrEnum):
    """Functional role of a Spark.

    The categories are deliberately functional rather than anatomical.  A future
    implementation may allow these roles to emerge instead of assigning them.
    """

    SENSORY = "sensory"
    FEATURE = "feature"
    HYPOTHESIS = "hypothesis"
    MEMORY = "memory"
    GOAL = "goal"
    ACTION = "action"
    WORKSPACE = "workspace"


class EventKind(StrEnum):
    STIMULUS = "stimulus"
    PROPAGATION = "propagation"
    INHIBITION = "inhibition"
    BROADCAST = "broadcast"
    REWARD = "reward"


@dataclass(slots=True)
class BrainConfig:
    """Configuration for the rate-based reference engine.

    The reference implementation aims to expose every important theoretical
    parameter.  Defaults are chosen for the included SwitchWorld experiment;
    they are not claimed to be biologically accurate.
    """

    ignition_threshold: float = 1.18
    ignition_margin: float = 0.20
    min_support_sources: int = 2
    stability_evaluations: int = 2
    workspace_slots: int = 4
    ignition_cooldown: float = 0.35

    diversity_bonus: float = 0.12
    temporal_coherence_bonus: float = 0.06
    contradiction_penalty: float = 0.16
    support_tau: float = 5.0

    refractory_period: float = 0.15
    post_fire_residual: float = 0.32
    active_epsilon: float = 0.01

    homeostatic_increment: float = 0.015
    threshold_relaxation_tau: float = 10.0

    eligibility_decay: float = 0.90
    learning_rate: float = 0.025
    max_abs_weight: float = 1.50

    propagation_delay: float = 0.01
    random_seed: int = 7


@dataclass(slots=True)
class EvidenceRecord:
    evidence_id: str
    source: str
    label: str
    time: float
    strength: float


@dataclass(slots=True)
class Spark:
    id: str
    label: str
    kind: SparkKind
    organ: str
    threshold: float = 1.0
    base_threshold: float = 1.0
    decay_tau: float = 2.5
    competition_group: str | None = None
    activation: float = 0.0
    last_update: float = 0.0
    refractory_until: float = 0.0
    last_fire: float | None = None
    fired_count: int = 0
    supports: dict[str, EvidenceRecord] = field(default_factory=dict)
    contradictions: dict[str, EvidenceRecord] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Connection:
    source: str
    target: str
    weight: float
    delay: float = 0.01
    plastic: bool = False
    eligibility: float = 0.0
    label: str = ""


@dataclass(order=True, slots=True)
class Event:
    time: float
    priority: int
    sequence: int
    kind: EventKind = field(compare=False)
    source: str = field(compare=False)
    target: str | None = field(compare=False, default=None)
    strength: float = field(compare=False, default=0.0)
    evidence_id: str | None = field(compare=False, default=None)
    evidence_label: str | None = field(compare=False, default=None)
    metadata: dict[str, Any] = field(compare=False, default_factory=dict)


@dataclass(slots=True)
class Coalition:
    id: str
    hypothesis_id: str
    label: str
    members: tuple[str, ...]
    score: float
    activation: float
    evidence_strength: float
    diversity: int
    stability: int
    contradiction: float


@dataclass(slots=True)
class WorkspaceItem:
    coalition_id: str
    hypothesis_id: str
    label: str
    score: float
    ignition_time: float
    supports: tuple[str, ...]


@dataclass(slots=True)
class Ignition:
    time: float
    label: str
    hypothesis_id: str
    coalition_id: str
    score: float
    margin: float
    supports: tuple[str, ...]


@dataclass(slots=True)
class EngineStats:
    events_processed: int = 0
    spark_updates: int = 0
    edge_evaluations: int = 0
    fires: int = 0
    ignitions: int = 0
    broadcasts: int = 0


@dataclass(slots=True)
class TraceFrame:
    time: float
    external_event: str
    truth: str | None
    prediction: str | None
    sparks: list[dict[str, Any]]
    coalitions: list[dict[str, Any]]
    workspace: list[dict[str, Any]]
    fired: list[str]
    active_edges: list[tuple[str, str, float]]
    stats: dict[str, int | float]

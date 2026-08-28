from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from sparkbrain.v04.contracts import SignalPulse, V04StepResult


@dataclass(frozen=True, slots=True)
class ReceptorTrace:
    time_ms: float
    channel: str
    signed_input: float
    fast_trace: float
    medium_trace: float
    slow_trace: float
    derivative: float
    novelty: float
    gain: float
    emitted_magnitude: float
    emitted: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ActivityPattern:
    pattern_id: str
    start_ms: float
    end_ms: float
    ordered_units: tuple[int, ...]
    relative_bins: tuple[int, ...]
    unit_ids: tuple[int, ...]
    spike_count: int
    source_cascade_id: str | None = None
    source_kind: str = "internal_reservoir"

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        for key in ("ordered_units", "relative_bins", "unit_ids"):
            row[key] = list(row[key])
        return row


@dataclass(frozen=True, slots=True)
class AssemblyActivation:
    assembly_id: str
    pattern_id: str
    time_ms: float
    similarity: float
    occurrences: int
    episode_count: int
    mature: bool
    unit_ids: tuple[int, ...]
    suppressed: bool = False

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["unit_ids"] = list(self.unit_ids)
        return row


@dataclass(frozen=True, slots=True)
class PredictionDecision:
    assembly_id: str | None
    value: str | None
    confidence: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ActionDecision:
    assembly_id: str | None
    action: str | None
    confidence: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StabilitySnapshot:
    time_ms: float
    spike_count: int
    active_unit_fraction: float
    runaway: bool
    dead: bool
    mean_threshold: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class V05StepResult:
    start_ms: float
    end_ms: float
    raw_pulses: tuple[SignalPulse, ...]
    emitted_pulses: tuple[SignalPulse, ...]
    receptor_traces: tuple[ReceptorTrace, ...]
    v04_result: V04StepResult
    patterns: tuple[ActivityPattern, ...]
    assembly_activations: tuple[AssemblyActivation, ...]
    prediction: PredictionDecision
    action: ActionDecision
    stability: StabilitySnapshot
    state_hash: str
    trace_hash: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.as_dict(),
            "assembly_activations": [row.as_dict() for row in self.assembly_activations],
            "emitted_pulses": [row.as_dict() for row in self.emitted_pulses],
            "end_ms": self.end_ms,
            "metadata": dict(self.metadata),
            "patterns": [row.as_dict() for row in self.patterns],
            "prediction": self.prediction.as_dict(),
            "raw_pulses": [row.as_dict() for row in self.raw_pulses],
            "receptor_traces": [row.as_dict() for row in self.receptor_traces],
            "stability": self.stability.as_dict(),
            "start_ms": self.start_ms,
            "state_hash": self.state_hash,
            "trace_hash": self.trace_hash,
            "v04_result": self.v04_result.as_dict(),
        }

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


@dataclass(frozen=True, slots=True)
class SignalPulse:
    """A local, time-stamped perturbation before semantic interpretation.

    ``channel`` identifies a receptor path, not a human-readable concept.  The
    field only consumes timing, magnitude, polarity, location, and modulation
    terms.  Metadata is observational and must not affect core dynamics.
    """

    time_ms: float
    channel: str
    magnitude: float
    polarity: int = 1
    location: tuple[float, float] | None = None
    novelty: float = 0.0
    prediction_error: float = 0.0
    source_id: str = "input"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "time_ms", _finite("time_ms", self.time_ms))
        object.__setattr__(self, "magnitude", _finite("magnitude", self.magnitude))
        object.__setattr__(self, "novelty", _finite("novelty", self.novelty))
        object.__setattr__(
            self,
            "prediction_error",
            _finite("prediction_error", self.prediction_error),
        )
        if self.time_ms < 0:
            raise ValueError("time_ms must be non-negative")
        if not self.channel:
            raise ValueError("channel must be non-empty")
        if self.magnitude < 0:
            raise ValueError("magnitude must be non-negative")
        if self.polarity not in (-1, 1):
            raise ValueError("polarity must be -1 or 1")
        if self.location is not None:
            if len(self.location) != 2:
                raise ValueError("location must contain x and y")
            object.__setattr__(
                self,
                "location",
                (_finite("location.x", self.location[0]), _finite("location.y", self.location[1])),
            )
        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")
        object.__setattr__(self, "metadata", dict(self.metadata))

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        if self.location is not None:
            row["location"] = list(self.location)
        return row


@dataclass(frozen=True, slots=True)
class SynapticArrival:
    time_ms: float
    target_id: int
    current: float
    source_id: int | None
    pulse_id: str
    novelty: float = 0.0
    prediction_error: float = 0.0


@dataclass(frozen=True, slots=True)
class SpikeEvent:
    time_ms: float
    unit_id: int
    potential_before_reset: float
    dynamic_threshold: float
    x: float
    y: float
    source_pulse_ids: tuple[str, ...]
    novelty: float
    prediction_error: float
    excitatory_drive: float
    inhibitory_drive: float

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["source_pulse_ids"] = list(self.source_pulse_ids)
        return row


@dataclass(frozen=True, slots=True)
class BurstEvent:
    burst_id: str
    start_ms: float
    end_ms: float
    spike_count: int
    unit_ids: tuple[int, ...]
    spatial_spread: float

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["unit_ids"] = list(self.unit_ids)
        return row


@dataclass(frozen=True, slots=True)
class CascadeEvent:
    cascade_id: str
    start_ms: float
    end_ms: float
    spike_count: int
    unit_ids: tuple[int, ...]
    ordered_units: tuple[int, ...]
    spatial_spread: float
    novelty: float
    prediction_error: float
    recurrence: float
    signature: str

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["unit_ids"] = list(self.unit_ids)
        row["ordered_units"] = list(self.ordered_units)
        return row


@dataclass(frozen=True, slots=True)
class IgnitionEvent:
    ignition_id: str
    cascade_id: str
    time_ms: float
    score: float
    threshold: float
    reason: str
    unit_ids: tuple[int, ...]
    signature: str

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["unit_ids"] = list(self.unit_ids)
        return row


@dataclass(frozen=True, slots=True)
class V04StepResult:
    start_ms: float
    end_ms: float
    input_pulses: tuple[SignalPulse, ...]
    spikes: tuple[SpikeEvent, ...]
    bursts: tuple[BurstEvent, ...]
    cascades: tuple[CascadeEvent, ...]
    ignitions: tuple[IgnitionEvent, ...]
    action: str | None
    field_state_hash: str
    trace_hash: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "bursts": [item.as_dict() for item in self.bursts],
            "cascades": [item.as_dict() for item in self.cascades],
            "end_ms": self.end_ms,
            "field_state_hash": self.field_state_hash,
            "ignitions": [item.as_dict() for item in self.ignitions],
            "input_pulses": [item.as_dict() for item in self.input_pulses],
            "spikes": [item.as_dict() for item in self.spikes],
            "start_ms": self.start_ms,
            "trace_hash": self.trace_hash,
        }

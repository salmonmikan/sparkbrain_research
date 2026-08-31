from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest


@dataclass(frozen=True, slots=True)
class DirectFieldPlasticityConfig:
    """Bounded local rule that writes only to ordinary Field connections."""

    minimum_lag_ms: float = 0.5
    maximum_lag_ms: float = 6.5
    potentiation_tau_ms: float = 10.0
    depression_tau_ms: float = 10.0
    potentiation_rate: float = 0.50
    depression_rate: float = 0.15
    delay_learning_rate: float = 0.50
    minimum_weight: float = 0.0
    maximum_weight: float = 1.25
    minimum_delay_ms: float = 0.5
    maximum_delay_ms: float = 20.0
    maximum_modulation: float = 2.0
    maximum_updates_per_event: int = 256

    def validate(self) -> None:
        positive = (
            "minimum_lag_ms",
            "maximum_lag_ms",
            "potentiation_tau_ms",
            "depression_tau_ms",
            "potentiation_rate",
            "depression_rate",
            "delay_learning_rate",
            "maximum_weight",
            "minimum_delay_ms",
            "maximum_delay_ms",
            "maximum_modulation",
        )
        for name in positive:
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if not math.isfinite(float(self.minimum_weight)) or self.minimum_weight < 0.0:
            raise ValueError("minimum_weight must be finite and non-negative")
        if self.maximum_lag_ms < self.minimum_lag_ms:
            raise ValueError("maximum_lag_ms must be at least minimum_lag_ms")
        if self.maximum_weight < self.minimum_weight:
            raise ValueError("maximum_weight must be at least minimum_weight")
        if self.maximum_delay_ms < self.minimum_delay_ms:
            raise ValueError("maximum_delay_ms must be at least minimum_delay_ms")
        if self.maximum_updates_per_event < 1:
            raise ValueError("maximum_updates_per_event must be positive")


@dataclass(frozen=True, slots=True)
class UnitExternalTrace:
    unit_id: int
    time_ms: float
    magnitude: float
    event_id: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalConnectionUpdate:
    source_id: int
    target_id: int
    mode: str
    lag_ms: float
    source_event_id: str
    target_event_id: str
    weight_before: float
    weight_after: float
    delay_before_ms: float
    delay_after_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExternalGatedDirectFieldPlasticity:
    """Update existing physical edges from short-lived unit-local external traces.

    The object owns no learned source-target proposal table, no confirmed or
    contradicted path counters, and no reward state. Long-lived acquired state
    resides in the ordinary ``Connection.weight`` and ``Connection.delay_ms``
    values already owned by ``TemporalExcitableField``. Controller traces are
    unit-local, short-lived, and may be cleared without removing learned edges.
    """

    def __init__(
        self,
        field: TemporalExcitableField,
        config: DirectFieldPlasticityConfig | None = None,
    ) -> None:
        self.field = field
        self.config = config or DirectFieldPlasticityConfig()
        self.config.validate()
        self._unit_traces: dict[int, UnitExternalTrace] = {}
        self.current_time_ms = 0.0
        self.external_observation_count = 0
        self.ignored_endogenous_count = 0
        self.update_count = 0

    def observe(self, pulse: RuntimePulse) -> tuple[PhysicalConnectionUpdate, ...]:
        """Apply one local physical update from an externally originated pulse.

        Endogenous pulses are explicitly ignored. They may participate in later
        Field execution, but cannot strengthen their own physical route.
        """

        if pulse.origin is not EventOrigin.EXTERNAL:
            self.ignored_endogenous_count += 1
            return ()
        if pulse.time_ms < self.current_time_ms:
            raise ValueError("external plasticity observations cannot move backwards")
        unit_id = self._unit_id(pulse.target)
        if unit_id not in self.field.units:
            raise KeyError(f"unknown external target unit: {unit_id}")
        self._expire_traces(pulse.time_ms)

        updates: list[PhysicalConnectionUpdate] = []
        for edge in sorted(
            self.field.incoming[unit_id],
            key=lambda row: (row.source_id, row.target_id),
        ):
            trace = self._unit_traces.get(edge.source_id)
            if trace is None or not edge.plastic or edge.weight < 0.0:
                continue
            lag = pulse.time_ms - trace.time_ms
            if not self._eligible_lag(lag):
                continue
            modulation = self._modulation(trace.magnitude, pulse.magnitude)
            factor = math.exp(-lag / self.config.potentiation_tau_ms)
            weight_delta = self.config.potentiation_rate * modulation * factor
            updates.append(
                self._update_edge(
                    edge.source_id,
                    edge.target_id,
                    mode="causal_potentiation",
                    lag_ms=lag,
                    source_event_id=trace.event_id,
                    target_event_id=pulse.event_id,
                    weight_delta=weight_delta,
                    desired_delay_ms=lag,
                )
            )
            if len(updates) >= self.config.maximum_updates_per_event:
                raise RuntimeError("maximum_updates_per_event exceeded")

        for edge in sorted(
            self.field.outgoing[unit_id],
            key=lambda row: (row.target_id, row.source_id),
        ):
            prior_post = self._unit_traces.get(edge.target_id)
            if prior_post is None or not edge.plastic or edge.weight < 0.0:
                continue
            lag = pulse.time_ms - prior_post.time_ms
            if not self._eligible_lag(lag):
                continue
            modulation = self._modulation(pulse.magnitude, prior_post.magnitude)
            factor = math.exp(-lag / self.config.depression_tau_ms)
            weight_delta = -self.config.depression_rate * modulation * factor
            updates.append(
                self._update_edge(
                    edge.source_id,
                    edge.target_id,
                    mode="anti_causal_depression",
                    lag_ms=lag,
                    source_event_id=pulse.event_id,
                    target_event_id=prior_post.event_id,
                    weight_delta=weight_delta,
                    desired_delay_ms=None,
                )
            )
            if len(updates) >= self.config.maximum_updates_per_event:
                raise RuntimeError("maximum_updates_per_event exceeded")

        self._unit_traces[unit_id] = UnitExternalTrace(
            unit_id=unit_id,
            time_ms=pulse.time_ms,
            magnitude=pulse.magnitude,
            event_id=pulse.event_id,
        )
        self.current_time_ms = pulse.time_ms
        self.external_observation_count += 1
        self.update_count += len(updates)
        return tuple(updates)

    def observe_external(
        self,
        pulse: RuntimePulse,
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        """Compatibility entry point for callers that explicitly name the boundary."""

        return self.observe(pulse)

    def clear_traces(self) -> None:
        self._unit_traces.clear()

    def connection_state_hash(self) -> str:
        return digest(
            [
                {
                    "delay_ms": edge.delay_ms,
                    "plastic": edge.plastic,
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "weight": edge.weight,
                }
                for _, edge in sorted(self.field.connections.items())
            ]
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "current_time_ms": self.current_time_ms,
            "external_observation_count": self.external_observation_count,
            "ignored_endogenous_count": self.ignored_endogenous_count,
            "unit_traces": {
                str(unit_id): trace.state_dict()
                for unit_id, trace in sorted(self._unit_traces.items())
            },
            "update_count": self.update_count,
        }

    @staticmethod
    def _unit_id(target: str) -> int:
        if not target.startswith("unit:"):
            raise ValueError("direct Field plasticity requires a unit target")
        return int(target.removeprefix("unit:"))

    def _expire_traces(self, now_ms: float) -> None:
        expired = tuple(
            unit_id
            for unit_id, trace in self._unit_traces.items()
            if now_ms - trace.time_ms > self.config.maximum_lag_ms
        )
        for unit_id in expired:
            del self._unit_traces[unit_id]

    def _eligible_lag(self, lag_ms: float) -> bool:
        return self.config.minimum_lag_ms <= lag_ms <= self.config.maximum_lag_ms

    def _modulation(self, left: float, right: float) -> float:
        value = math.sqrt(max(0.0, left) * max(0.0, right))
        return min(self.config.maximum_modulation, value)

    def _update_edge(
        self,
        source_id: int,
        target_id: int,
        *,
        mode: str,
        lag_ms: float,
        source_event_id: str,
        target_event_id: str,
        weight_delta: float,
        desired_delay_ms: float | None,
    ) -> PhysicalConnectionUpdate:
        edge = self.field.connection(source_id, target_id)
        weight_before = edge.weight
        delay_before = edge.delay_ms
        edge.weight = min(
            self.config.maximum_weight,
            max(self.config.minimum_weight, edge.weight + weight_delta),
        )
        if desired_delay_ms is not None and edge.weight > 0.0:
            edge.delay_ms = min(
                self.config.maximum_delay_ms,
                max(
                    self.config.minimum_delay_ms,
                    edge.delay_ms
                    + self.config.delay_learning_rate
                    * (desired_delay_ms - edge.delay_ms),
                ),
            )
        return PhysicalConnectionUpdate(
            source_id=source_id,
            target_id=target_id,
            mode=mode,
            lag_ms=lag_ms,
            source_event_id=source_event_id,
            target_event_id=target_event_id,
            weight_before=weight_before,
            weight_after=edge.weight,
            delay_before_ms=delay_before,
            delay_after_ms=edge.delay_ms,
        )

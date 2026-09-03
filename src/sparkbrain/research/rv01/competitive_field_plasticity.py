from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse

from .direct_field_plasticity import (
    DirectFieldPlasticityConfig,
    ExternalGatedDirectFieldPlasticity,
    PhysicalConnectionUpdate,
)


@dataclass(frozen=True, slots=True)
class CompetitiveFieldPlasticityConfig:
    base: DirectFieldPlasticityConfig = field(
        default_factory=DirectFieldPlasticityConfig
    )
    competing_depression_rate: float = 0.35
    competing_depression_tau_ms: float = 10.0

    def validate(self) -> None:
        self.base.validate()
        for name in (
            "competing_depression_rate",
            "competing_depression_tau_ms",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")


class ExternalGatedCompetitiveFieldPlasticity(
    ExternalGatedDirectFieldPlasticity
):
    """Direct Field plasticity with local heterosynaptic competition.

    When an external post-unit follows a short-lived external pre-unit trace,
    the observed physical pre->post edge is potentiated by the base rule. Other
    currently positive outgoing edges of that same pre-unit are depressed. The
    controller stores no confirmed/contradicted counts and no source-target
    transition table; durable state remains ordinary Field connections.
    """

    def __init__(
        self,
        field: TemporalExcitableField,
        config: CompetitiveFieldPlasticityConfig | None = None,
    ) -> None:
        self.competition_config = config or CompetitiveFieldPlasticityConfig()
        self.competition_config.validate()
        super().__init__(field, self.competition_config.base)
        self.competitive_update_count = 0

    def observe(self, pulse: RuntimePulse) -> tuple[PhysicalConnectionUpdate, ...]:
        if pulse.origin is not EventOrigin.EXTERNAL:
            return super().observe(pulse)
        target_id = self._unit_id(pulse.target)
        eligible_sources = tuple(
            trace
            for edge in self.field.incoming[target_id]
            if (trace := self._unit_traces.get(edge.source_id)) is not None
            and edge.plastic
            and edge.weight >= 0.0
            and self._eligible_lag(pulse.time_ms - trace.time_ms)
        )
        base_updates = list(super().observe(pulse))
        competing_updates: list[PhysicalConnectionUpdate] = []
        for trace in eligible_sources:
            lag = pulse.time_ms - trace.time_ms
            modulation = self._modulation(trace.magnitude, pulse.magnitude)
            delta = (
                -self.competition_config.competing_depression_rate
                * modulation
                * math.exp(
                    -lag
                    / self.competition_config.competing_depression_tau_ms
                )
            )
            for edge in sorted(
                self.field.outgoing[trace.unit_id],
                key=lambda row: (row.target_id, row.source_id),
            ):
                if (
                    edge.target_id == target_id
                    or not edge.plastic
                    or edge.weight <= self.config.minimum_weight
                ):
                    continue
                competing_updates.append(
                    self._update_edge(
                        edge.source_id,
                        edge.target_id,
                        mode="local_competing_depression",
                        lag_ms=lag,
                        source_event_id=trace.event_id,
                        target_event_id=pulse.event_id,
                        weight_delta=delta,
                        desired_delay_ms=None,
                    )
                )
                if (
                    len(base_updates) + len(competing_updates)
                    > self.config.maximum_updates_per_event
                ):
                    raise RuntimeError("maximum_updates_per_event exceeded")
        self.competitive_update_count += len(competing_updates)
        self.update_count += len(competing_updates)
        return tuple((*base_updates, *competing_updates))

    def state_dict(self) -> dict[str, Any]:
        state = super().state_dict()
        return {
            **state,
            "competition_config": asdict(self.competition_config),
            "competitive_update_count": self.competitive_update_count,
            "ignored_endogenous_observations": state["ignored_endogenous_count"],
        }

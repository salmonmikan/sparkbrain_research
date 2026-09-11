"""R01-15 expression-only post-spike suppression interventions.

The intervention is applied only after the ordinary Field runtime has emitted a
spike and scheduled its outgoing consequences. It changes no topology,
connection, cue, training, or queued event. This module is development-only and
contains no world generator, scorer, held-out path, or experiment runner.
"""

from __future__ import annotations

import heapq
from dataclasses import asdict
from typing import Any, Literal

from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, FieldTopology, UnitState

PostSpikeSuppressionMode = Literal[
    "intact",
    "adaptation_zero",
    "refractory_zero",
    "both_zero",
]

_ALLOWED_MODES = {
    "intact",
    "adaptation_zero",
    "refractory_zero",
    "both_zero",
}


class PostSpikeSuppressionField(TemporalExcitableField):
    """Temporal Field with one fixed R01-15 post-spike expression intervention."""

    def __init__(
        self,
        topology: FieldTopology,
        config: ExcitableFieldConfig | None = None,
        *,
        mode: PostSpikeSuppressionMode = "intact",
    ) -> None:
        if mode not in _ALLOWED_MODES:
            raise ValueError("invalid R01-15 post-spike suppression mode")
        super().__init__(topology, config)
        self.intervention_mode: PostSpikeSuppressionMode = mode
        self.intervention_records: list[dict[str, Any]] = []

    def _deliver_group(
        self,
        time_ms: float,
        arrivals: list[SynapticArrival],
    ) -> list[SpikeEvent]:
        spikes = super()._deliver_group(time_ms, arrivals)
        if self.intervention_mode == "intact":
            return spikes

        for spike in spikes:
            unit = self.units[spike.unit_id]
            if self.intervention_mode in ("adaptation_zero", "both_zero"):
                before = float(unit.adaptation)
                unit.adaptation = 0.0
                self.intervention_records.append(
                    {
                        "type": "r01-15-post-spike-intervention",
                        "mode": self.intervention_mode,
                        "unit_id": spike.unit_id,
                        "spike_time_ms": float(spike.time_ms),
                        "field": "adaptation",
                        "before": before,
                        "after": 0.0,
                    }
                )
            if self.intervention_mode in ("refractory_zero", "both_zero"):
                before = float(unit.refractory_until_ms)
                unit.refractory_until_ms = float(spike.time_ms)
                self.intervention_records.append(
                    {
                        "type": "r01-15-post-spike-intervention",
                        "mode": self.intervention_mode,
                        "unit_id": spike.unit_id,
                        "spike_time_ms": float(spike.time_ms),
                        "field": "refractory_until_ms",
                        "before": before,
                        "after": float(spike.time_ms),
                    }
                )
        return spikes

    @classmethod
    def from_state_dict(
        cls,
        value: dict[str, Any],
        *,
        mode: PostSpikeSuppressionMode = "intact",
    ) -> PostSpikeSuppressionField:
        """Restore every arm from the exact same serialized pre-probe state."""

        config = ExcitableFieldConfig(**value["config"])
        topology = FieldTopology(
            units=tuple(UnitState(**row) for row in value["units"]),
            connections=tuple(Connection(**row) for row in value["connections"]),
            receptor_ids=tuple(value["receptor_ids"]),
        )
        field = cls(topology, config, mode=mode)
        field.current_time_ms = float(value["current_time_ms"])
        field._counter = int(value["counter"])
        field.total_arrivals = int(value["totals"]["arrivals"])
        field.total_spikes = int(value["totals"]["spikes"])
        field._queue.clear()
        for row in value["queue"]:
            arrival = SynapticArrival(**row["arrival"])
            heapq.heappush(
                field._queue,
                (float(row["time_ms"]), int(row["counter"]), arrival),
            )
        # The intervention is probe-expression state only and must not affect
        # the restored checkpoint before the first spike.
        if field.state_dict() != value:
            raise ValueError("R01-15 restored Field is not byte-semantically identical")
        return field

    def intervention_state_dict(self) -> dict[str, Any]:
        return {
            "mode": self.intervention_mode,
            "records": [dict(row) for row in self.intervention_records],
        }

    def connection_state(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            asdict(self.connections[key]) for key in sorted(self.connections)
        )


__all__ = [
    "PostSpikeSuppressionField",
    "PostSpikeSuppressionMode",
]

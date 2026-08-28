from __future__ import annotations

import hashlib
import heapq
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .contracts import SignalPulse, SpikeEvent, SynapticArrival, canonical_json
from .topology import Connection, FieldTopology, UnitState


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _stable_index(value: str, size: int) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % size


@dataclass(frozen=True, slots=True)
class ExcitableFieldConfig:
    membrane_tau_ms: float = 18.0
    adaptation_tau_ms: float = 90.0
    refractory_ms: float = 3.0
    reset_potential: float = 0.0
    adaptation_increment: float = 0.16
    input_gain: float = 1.0
    novelty_gain: float = 0.20
    prediction_error_gain: float = 0.34
    receptor_fanout: int = 2
    max_events_per_run: int = 200_000
    max_spikes_per_run: int = 50_000
    max_sources_per_unit: int = 16

    def validate(self) -> None:
        positive = (
            "membrane_tau_ms",
            "adaptation_tau_ms",
            "refractory_ms",
            "input_gain",
            "receptor_fanout",
            "max_events_per_run",
            "max_spikes_per_run",
            "max_sources_per_unit",
        )
        for name in positive:
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"{name} must be positive")
        for name in (
            "reset_potential",
            "adaptation_increment",
            "novelty_gain",
            "prediction_error_gain",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
            if not math.isfinite(float(value)):
                raise ValueError(f"{name} must be finite")


class TemporalExcitableField:
    """Deterministic event-driven field with delayed recurrent propagation.

    This is an engineering abstraction of an excitable medium, not a claim of
    biological neuron equivalence.  Only touched units are integrated; dormant
    units are decayed lazily when an event reaches them or during inspection.
    """

    def __init__(
        self,
        topology: FieldTopology,
        config: ExcitableFieldConfig | None = None,
    ) -> None:
        self.config = config or ExcitableFieldConfig()
        self.config.validate()
        self.units: dict[int, UnitState] = {
            row.unit_id: UnitState(**asdict(row)) for row in topology.units
        }
        self.connections: dict[tuple[int, int], Connection] = {
            (row.source_id, row.target_id): Connection(**asdict(row))
            for row in topology.connections
        }
        self.receptor_ids = tuple(topology.receptor_ids)
        self.outgoing: dict[int, list[Connection]] = {unit_id: [] for unit_id in self.units}
        self.incoming: dict[int, list[Connection]] = {unit_id: [] for unit_id in self.units}
        for edge in self.connections.values():
            self.outgoing[edge.source_id].append(edge)
            self.incoming[edge.target_id].append(edge)
        for rows in self.outgoing.values():
            rows.sort(key=lambda edge: (edge.delay_ms, edge.target_id))
        self._queue: list[tuple[float, int, SynapticArrival]] = []
        self._counter = 0
        self.current_time_ms = 0.0
        self.total_arrivals = 0
        self.total_spikes = 0
        self.last_run_arrivals = 0
        self.last_run_spikes = 0
        self.last_input_routes: list[dict[str, Any]] = []

    def _decay_unit(self, unit: UnitState, time_ms: float) -> None:
        if time_ms < unit.last_update_ms:
            raise ValueError("field time cannot move backwards")
        elapsed = time_ms - unit.last_update_ms
        if elapsed <= 0:
            return
        unit.potential *= math.exp(-elapsed / self.config.membrane_tau_ms)
        unit.adaptation *= math.exp(-elapsed / self.config.adaptation_tau_ms)
        unit.novelty_trace *= math.exp(-elapsed / self.config.membrane_tau_ms)
        unit.prediction_error_trace *= math.exp(-elapsed / self.config.membrane_tau_ms)
        unit.excitatory_drive *= math.exp(-elapsed / self.config.membrane_tau_ms)
        unit.inhibitory_drive *= math.exp(-elapsed / self.config.membrane_tau_ms)
        unit.last_update_ms = time_ms

    @staticmethod
    def dynamic_threshold(unit: UnitState) -> float:
        return unit.base_threshold + max(0.0, unit.adaptation)

    def route_pulse(self, pulse: SignalPulse) -> tuple[int, ...]:
        if not self.receptor_ids:
            raise RuntimeError("field has no receptor units")
        fanout = min(int(self.config.receptor_fanout), len(self.receptor_ids))
        if pulse.location is not None:
            x, y = pulse.location
            ranked = sorted(
                self.receptor_ids,
                key=lambda unit_id: (
                    math.hypot(self.units[unit_id].x - x, self.units[unit_id].y - y),
                    unit_id,
                ),
            )
            return tuple(ranked[:fanout])
        key = f"{pulse.channel}|polarity={pulse.polarity}"
        start = _stable_index(key, len(self.receptor_ids))
        return tuple(
            self.receptor_ids[(start + offset) % len(self.receptor_ids)]
            for offset in range(fanout)
        )

    def schedule_pulse(self, pulse: SignalPulse) -> tuple[int, ...]:
        targets = self.route_pulse(pulse)
        pulse_id = _digest(pulse.as_dict())[:20]
        current = (
            pulse.magnitude * self.config.input_gain
            + pulse.novelty * self.config.novelty_gain
            + pulse.prediction_error * self.config.prediction_error_gain
        ) / math.sqrt(len(targets))
        self.last_input_routes.append(
            {
                "channel": pulse.channel,
                "polarity": pulse.polarity,
                "pulse_id": pulse_id,
                "targets": list(targets),
                "time_ms": pulse.time_ms,
            }
        )
        for target_id in targets:
            self.schedule_arrival(
                SynapticArrival(
                    time_ms=pulse.time_ms,
                    target_id=target_id,
                    current=current,
                    source_id=None,
                    pulse_id=pulse_id,
                    novelty=pulse.novelty,
                    prediction_error=pulse.prediction_error,
                )
            )
        return targets

    def schedule_arrival(self, arrival: SynapticArrival) -> None:
        if arrival.target_id not in self.units:
            raise KeyError(f"unknown target unit: {arrival.target_id}")
        if arrival.time_ms < self.current_time_ms:
            raise ValueError("cannot schedule an arrival in the past")
        self._counter += 1
        heapq.heappush(self._queue, (arrival.time_ms, self._counter, arrival))

    def _source_tuple(self, unit: UnitState, pulse_ids: Iterable[str]) -> tuple[str, ...]:
        merged = list(unit.source_pulse_ids)
        for pulse_id in pulse_ids:
            if pulse_id not in merged:
                merged.append(pulse_id)
        return tuple(merged[-int(self.config.max_sources_per_unit) :])

    def _deliver_group(
        self,
        time_ms: float,
        arrivals: list[SynapticArrival],
    ) -> list[SpikeEvent]:
        by_target: dict[int, list[SynapticArrival]] = {}
        for row in arrivals:
            by_target.setdefault(row.target_id, []).append(row)
        spikes: list[SpikeEvent] = []
        for target_id in sorted(by_target):
            unit = self.units[target_id]
            self._decay_unit(unit, time_ms)
            rows = by_target[target_id]
            positive = sum(max(0.0, row.current) for row in rows)
            negative = sum(max(0.0, -row.current) for row in rows)
            unit.excitatory_drive += positive
            unit.inhibitory_drive += negative
            unit.novelty_trace = max(
                unit.novelty_trace,
                max((row.novelty for row in rows), default=0.0),
            )
            unit.prediction_error_trace = max(
                unit.prediction_error_trace,
                max((row.prediction_error for row in rows), default=0.0),
            )
            unit.source_pulse_ids = self._source_tuple(
                unit,
                (row.pulse_id for row in rows),
            )
            net_current = positive - negative
            if time_ms < unit.refractory_until_ms:
                # Inhibition can still shorten the post-spike residual; positive
                # drive is ignored during the absolute refractory window.
                unit.potential += min(0.0, net_current)
                continue
            unit.potential += net_current
            threshold = self.dynamic_threshold(unit)
            if unit.potential + 1e-12 < threshold:
                continue
            potential_before_reset = unit.potential
            spike = SpikeEvent(
                time_ms=time_ms,
                unit_id=unit.unit_id,
                potential_before_reset=potential_before_reset,
                dynamic_threshold=threshold,
                x=unit.x,
                y=unit.y,
                source_pulse_ids=unit.source_pulse_ids,
                novelty=unit.novelty_trace,
                prediction_error=unit.prediction_error_trace,
                excitatory_drive=unit.excitatory_drive,
                inhibitory_drive=unit.inhibitory_drive,
            )
            spikes.append(spike)
            unit.potential = float(self.config.reset_potential)
            unit.adaptation += self.config.adaptation_increment
            unit.refractory_until_ms = time_ms + self.config.refractory_ms
            unit.last_spike_ms = time_ms
            unit.spike_count += 1
            spike_id = _digest(
                {
                    "sources": list(spike.source_pulse_ids),
                    "time_ms": time_ms,
                    "unit_id": unit.unit_id,
                }
            )[:20]
            for edge in self.outgoing[unit.unit_id]:
                self.schedule_arrival(
                    SynapticArrival(
                        time_ms=time_ms + edge.delay_ms,
                        target_id=edge.target_id,
                        current=edge.weight,
                        source_id=unit.unit_id,
                        pulse_id=spike_id,
                        novelty=spike.novelty * 0.92,
                        prediction_error=spike.prediction_error * 0.92,
                    )
                )
        return spikes

    def run_until(self, end_ms: float) -> tuple[SpikeEvent, ...]:
        if end_ms < self.current_time_ms:
            raise ValueError("end_ms cannot move backwards")
        self.last_run_arrivals = 0
        self.last_run_spikes = 0
        spikes: list[SpikeEvent] = []
        while self._queue and self._queue[0][0] <= end_ms:
            time_ms = self._queue[0][0]
            group: list[SynapticArrival] = []
            while self._queue and self._queue[0][0] == time_ms:
                _, _, arrival = heapq.heappop(self._queue)
                group.append(arrival)
                self.last_run_arrivals += 1
                self.total_arrivals += 1
                if self.last_run_arrivals > self.config.max_events_per_run:
                    raise RuntimeError("max_events_per_run exceeded")
            new_spikes = self._deliver_group(time_ms, group)
            spikes.extend(new_spikes)
            self.last_run_spikes += len(new_spikes)
            self.total_spikes += len(new_spikes)
            if self.last_run_spikes > self.config.max_spikes_per_run:
                raise RuntimeError("max_spikes_per_run exceeded")
            self.current_time_ms = time_ms
        self.current_time_ms = end_ms
        return tuple(spikes)

    def connection(self, source_id: int, target_id: int) -> Connection:
        return self.connections[(source_id, target_id)]

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "connections": [
                asdict(self.connections[key]) for key in sorted(self.connections)
            ],
            "counter": self._counter,
            "current_time_ms": self.current_time_ms,
            "queue": [
                {
                    "arrival": asdict(arrival),
                    "counter": counter,
                    "time_ms": time_ms,
                }
                for time_ms, counter, arrival in sorted(self._queue)
            ],
            "receptor_ids": list(self.receptor_ids),
            "totals": {
                "arrivals": self.total_arrivals,
                "spikes": self.total_spikes,
            },
            "units": [asdict(self.units[unit_id]) for unit_id in sorted(self.units)],
        }

    def state_hash(self) -> str:
        return _digest(self.state_dict())

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> TemporalExcitableField:
        config = ExcitableFieldConfig(**value["config"])
        topology = FieldTopology(
            units=tuple(UnitState(**row) for row in value["units"]),
            connections=tuple(Connection(**row) for row in value["connections"]),
            receptor_ids=tuple(value["receptor_ids"]),
        )
        field = cls(topology, config)
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
        return field

    def to_json(self) -> str:
        return canonical_json(self.state_dict())

    @classmethod
    def from_json(cls, payload: str) -> TemporalExcitableField:
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise ValueError("field payload must be an object")
        return cls.from_state_dict(value)

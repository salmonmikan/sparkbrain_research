"""RV02-RD006 Stage D0 external-learning reachability diagnostic.

This is a fresh, non-formal development object.  It compares the ordinary
external-only Field learner ON versus OFF while holding topology, schedule,
initial state, clocks, threshold, gain, stimulus, and hidden-return learning
fixed.  It emits mechanism-reachability diagnostics only: no route score,
capability score, held-out evaluation, E0/E1/ES learner, or reservoir arm.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass, replace
from enum import StrEnum
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology

PROTOCOL_ID = "rv02-rd006-external-learning-reachability-a-v1"
OBJECT_ID = "RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A"
PRIOR_SOURCE_SHA = "c60b7fd8d3889ee969f505d921e7d31c990871e6"
PORTS = tuple(range(36))
FAMILIES = (
    "disjoint-routes",
    "shared-cue",
    "shared-prefix",
    "opposing-reversal",
    "dense-load",
    "capacity-pressure",
)
ARMS = ("external_learning_off", "external_learning_on")


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def require_git_sha(value: str) -> None:
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError("source_git_sha must be a lowercase 40-character Git SHA")


class EventOrigin(StrEnum):
    EXTERNAL = "external"
    ENDOGENOUS = "endogenous"


@dataclass(frozen=True, slots=True)
class RuntimePulse:
    event_id: str
    time_ms: float
    target: str
    magnitude: float
    origin: EventOrigin = EventOrigin.EXTERNAL

    def __post_init__(self) -> None:
        if not self.event_id or not self.target:
            raise ValueError("pulse identifiers must be non-empty")
        if not math.isfinite(self.time_ms) or self.time_ms < 0.0:
            raise ValueError("pulse time must be finite and non-negative")
        if not math.isfinite(self.magnitude) or self.magnitude < 0.0:
            raise ValueError("pulse magnitude must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class RD006Config:
    seed: int = 92701
    unit_count: int = 48
    degree: int = 8
    scale: int = 1
    threshold: float = 0.5
    initial_weight: float = 0.05
    initial_delay_ms: float = 5.0
    boundary_gain: float = 4.0
    input_magnitude: float = 1.0
    minimum_return_lag_ms: float = 0.5
    maximum_return_lag_ms: float = 6.5
    required_distinct_hidden_sources: int = 2
    max_events_per_run: int = 4096
    max_spikes_per_run: int = 512

    def validate(self) -> None:
        if self != RD006Config():
            raise ValueError("RD006 Stage D0 configuration is fixed")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DirectFieldPlasticityConfig:
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


@dataclass(frozen=True, slots=True)
class UnitExternalTrace:
    unit_id: int
    time_ms: float
    magnitude: float
    event_id: str


class ExternalOnlyPhysicalPlasticity:
    """Ordinary external-only local learner retained from the RV01 path.

    This is intentionally the prior direct-Field rule, isolated here so the
    fresh main-based object does not import a consumed RD005 branch identity.
    It never consumes hidden spikes, task outcomes, or capability scores.
    """

    def __init__(
        self,
        field: TemporalExcitableField,
        config: DirectFieldPlasticityConfig | None = None,
    ) -> None:
        self.field = field
        self.config = config or DirectFieldPlasticityConfig()
        self._unit_traces: dict[int, UnitExternalTrace] = {}
        self.current_time_ms = 0.0
        self.external_observation_count = 0
        self.ignored_endogenous_count = 0
        self.update_count = 0

    def observe_external(
        self, pulse: RuntimePulse
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        if pulse.origin is not EventOrigin.EXTERNAL:
            self.ignored_endogenous_count += 1
            return ()
        if pulse.time_ms < self.current_time_ms:
            raise ValueError("external observations cannot move backwards")
        if not pulse.target.startswith("unit:"):
            raise ValueError("ordinary Field plasticity requires a unit target")
        unit_id = int(pulse.target.removeprefix("unit:"))
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
            delta = (
                self.config.potentiation_rate
                * modulation
                * math.exp(-lag / self.config.potentiation_tau_ms)
            )
            updates.append(
                self._update_edge(
                    edge,
                    mode="causal_potentiation",
                    lag_ms=lag,
                    source_event_id=trace.event_id,
                    target_event_id=pulse.event_id,
                    weight_delta=delta,
                    desired_delay_ms=lag,
                )
            )
            if len(updates) >= self.config.maximum_updates_per_event:
                raise RuntimeError("maximum_updates_per_event exceeded")

        for edge in sorted(
            self.field.outgoing[unit_id],
            key=lambda row: (row.target_id, row.source_id),
        ):
            trace = self._unit_traces.get(edge.target_id)
            if trace is None or not edge.plastic or edge.weight < 0.0:
                continue
            lag = pulse.time_ms - trace.time_ms
            if not self._eligible_lag(lag):
                continue
            modulation = self._modulation(pulse.magnitude, trace.magnitude)
            delta = (
                -self.config.depression_rate
                * modulation
                * math.exp(-lag / self.config.depression_tau_ms)
            )
            updates.append(
                self._update_edge(
                    edge,
                    mode="anti_causal_depression",
                    lag_ms=lag,
                    source_event_id=pulse.event_id,
                    target_event_id=trace.event_id,
                    weight_delta=delta,
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

    def _expire_traces(self, now_ms: float) -> None:
        for unit_id in tuple(self._unit_traces):
            if now_ms - self._unit_traces[unit_id].time_ms > self.config.maximum_lag_ms:
                del self._unit_traces[unit_id]

    def _eligible_lag(self, lag_ms: float) -> bool:
        return self.config.minimum_lag_ms <= lag_ms <= self.config.maximum_lag_ms

    def _modulation(self, left: float, right: float) -> float:
        return min(self.config.maximum_modulation, math.sqrt(max(0.0, left * right)))

    def _update_edge(
        self,
        edge: Connection,
        *,
        mode: str,
        lag_ms: float,
        source_event_id: str,
        target_event_id: str,
        weight_delta: float,
        desired_delay_ms: float | None,
    ) -> PhysicalConnectionUpdate:
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
                    + self.config.delay_learning_rate * (desired_delay_ms - edge.delay_ms),
                ),
            )
        return PhysicalConnectionUpdate(
            source_id=edge.source_id,
            target_id=edge.target_id,
            mode=mode,
            lag_ms=lag_ms,
            source_event_id=source_event_id,
            target_event_id=target_event_id,
            weight_before=weight_before,
            weight_after=edge.weight,
            delay_before_ms=delay_before,
            delay_after_ms=edge.delay_ms,
        )


def development_worlds(config: RD006Config) -> tuple[dict[str, Any], ...]:
    config.validate()
    templates: dict[str, tuple[tuple[int, ...], ...]] = {
        "disjoint-routes": ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11)),
        "shared-cue": ((0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9)),
        "shared-prefix": ((0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7)),
        "opposing-reversal": ((0, 1, 2, 3), (4, 2, 1, 5), (6, 7, 8, 9)),
        "dense-load": tuple(
            (0 if index < 4 else index, 10 + 3 * index, 11 + 3 * index, 12 + 3 * index)
            for index in range(8)
        ),
        "capacity-pressure": tuple(
            (0, 1 + 3 * index, 2 + 3 * index, 3 + 3 * index) for index in range(6)
        ),
    }
    rng = random.Random(config.seed)
    mapping = list(PORTS)
    rng.shuffle(mapping)
    worlds = []
    for family in FAMILIES:
        routes = tuple(tuple(mapping[unit] for unit in route) for route in templates[family])
        world = {
            "world_id": f"rv02-rd006:{config.seed}:{family}",
            "family": family,
            "routes": routes,
            "exposures": tuple(4 for _ in routes),
            "ports": PORTS,
        }
        world["world_sha256"] = digest(world)
        worlds.append(world)
    return tuple(worlds)


def build_topology(
    config: RD006Config, world: dict[str, Any]
) -> tuple[tuple[int, int], ...]:
    required = {
        edge
        for route in world["routes"]
        for edge in zip(route, route[1:], strict=False)
    }
    outgoing = [{(unit + 1) % config.unit_count} for unit in range(config.unit_count)]
    for source, target in required:
        outgoing[source].add(target)
    rng = random.Random(config.seed)
    for source, targets in enumerate(outgoing):
        choices = [
            target
            for target in range(config.unit_count)
            if target != source and target not in targets
        ]
        targets.update(rng.sample(choices, config.degree - len(targets)))
    return tuple(
        (source, target)
        for source, targets in enumerate(outgoing)
        for target in sorted(targets)
    )


def build_initial_field(config: RD006Config, world: dict[str, Any]) -> TemporalExcitableField:
    edges = build_topology(config, world)
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=config.threshold,
            )
            for unit_id in range(config.unit_count)
        ),
        tuple(
            Connection(
                source_id=source,
                target_id=target,
                weight=config.initial_weight,
                delay_ms=config.initial_delay_ms,
            )
            for source, target in edges
        ),
        receptor_ids=PORTS,
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=max(1.0, config.initial_delay_ms * 0.25),
        ),
    )
    field.config = replace(
        field.config,
        max_events_per_run=config.max_events_per_run,
        max_spikes_per_run=config.max_spikes_per_run,
    )
    for edge in field.connections.values():
        if edge.source_id in PORTS and edge.target_id not in PORTS:
            edge.weight *= config.boundary_gain
    return field


def training_schedule(world: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    ordinal = 0
    for route_index, (route, exposures) in enumerate(
        zip(world["routes"], world["exposures"], strict=True)
    ):
        for episode in range(exposures):
            for position, unit_id in enumerate(route):
                rows.append(
                    {
                        "ordinal": ordinal,
                        "route_index": route_index,
                        "episode": episode,
                        "position": position,
                        "unit_id": unit_id,
                        "time_ms": float(route_index * 10000 + episode * 100 + position * 5),
                        "event_id": f"rd006-ext-{ordinal:06d}",
                    }
                )
                ordinal += 1
    return tuple(rows)


def connection_rows(field: TemporalExcitableField) -> tuple[dict[str, Any], ...]:
    return tuple(asdict(edge) for _, edge in sorted(field.connections.items()))


def schedule_external(
    field: TemporalExcitableField,
    *,
    event_id: str,
    time_ms: float,
    unit_id: int,
    magnitude: float,
) -> None:
    field.schedule_arrival(
        SynapticArrival(
            time_ms=time_ms,
            target_id=unit_id,
            current=magnitude,
            source_id=None,
            pulse_id=event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )


def _hidden_spike_rows(spikes: tuple[SpikeEvent, ...]) -> tuple[dict[str, Any], ...]:
    return tuple(spike.as_dict() for spike in spikes if spike.unit_id not in PORTS)


def _spike_rows(spikes: tuple[SpikeEvent, ...]) -> tuple[dict[str, Any], ...]:
    """Retain the complete driven activity needed for silence/explosion audits."""

    return tuple(spike.as_dict() for spike in spikes)


def eligible_hidden_sources(
    field: TemporalExcitableField,
    spikes: tuple[SpikeEvent, ...],
    *,
    return_unit_id: int,
    return_time_ms: float,
    config: RD006Config,
) -> tuple[dict[str, Any], ...]:
    by_source: dict[int, dict[str, Any]] = {}
    for spike in spikes:
        if spike.unit_id in PORTS:
            continue
        edge = field.connections.get((spike.unit_id, return_unit_id))
        if edge is None or not edge.plastic or edge.weight < 0.0:
            continue
        lag = return_time_ms - spike.time_ms
        if not config.minimum_return_lag_ms <= lag <= config.maximum_return_lag_ms:
            continue
        row = {
            "source_id": spike.unit_id,
            "target_id": return_unit_id,
            "spike_time_ms": spike.time_ms,
            "return_time_ms": return_time_ms,
            "lag_ms": lag,
            "edge_weight": edge.weight,
            "edge_delay_ms": edge.delay_ms,
        }
        previous = by_source.get(spike.unit_id)
        if previous is None or row["spike_time_ms"] > previous["spike_time_ms"]:
            by_source[spike.unit_id] = row
    return tuple(by_source[source] for source in sorted(by_source))


def run_arm(
    initial_state: dict[str, Any],
    schedule: tuple[dict[str, Any], ...],
    *,
    arm: str,
    config: RD006Config,
) -> dict[str, Any]:
    if arm not in ARMS:
        raise ValueError(f"unsupported RD006 arm: {arm}")
    field = TemporalExcitableField.from_state_dict(initial_state)
    learner = ExternalOnlyPhysicalPlasticity(field) if arm == "external_learning_on" else None
    initial_connection_sha256 = digest(connection_rows(field))
    clocks: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []

    for row in schedule:
        time_ms = float(row["time_ms"])
        spikes = field.run_until(time_ms)
        eligible = eligible_hidden_sources(
            field,
            spikes,
            return_unit_id=int(row["unit_id"]),
            return_time_ms=time_ms,
            config=config,
        )
        raw_spikes = _spike_rows(spikes)
        hidden_spikes = _hidden_spike_rows(spikes)
        clocks.append(
            {
                "return_event_id": row["event_id"],
                "return_time_ms": time_ms,
                "return_unit_id": row["unit_id"],
                "raw_spikes": raw_spikes,
                "hidden_spikes": hidden_spikes,
                "eligible_hidden_sources": eligible,
            }
        )
        pulse = RuntimePulse(
            event_id=str(row["event_id"]),
            time_ms=time_ms,
            target=f"unit:{row['unit_id']}",
            magnitude=config.input_magnitude,
        )
        if learner is not None:
            updates.extend(update.state_dict() for update in learner.observe_external(pulse))
        schedule_external(
            field,
            event_id=str(row["event_id"]),
            time_ms=time_ms,
            unit_id=int(row["unit_id"]),
            magnitude=config.input_magnitude,
        )

    maximum_eligible = max(
        (len(clock["eligible_hidden_sources"]) for clock in clocks),
        default=0,
    )
    selected = next(
        (
            clock
            for clock in clocks
            if len(clock["eligible_hidden_sources"])
            >= config.required_distinct_hidden_sources
        ),
        None,
    )
    return {
        "arm": arm,
        "ordinary_external_learning_enabled": learner is not None,
        "hidden_return_learning_enabled": False,
        "initial_connection_sha256": initial_connection_sha256,
        "final_connection_sha256": digest(connection_rows(field)),
        "external_observation_count": (
            learner.external_observation_count if learner is not None else 0
        ),
        "ordinary_update_count": len(updates),
        "hidden_return_update_count": 0,
        "ordinary_updates": updates,
        "inspected_clocks": clocks,
        "hidden_spike_count": sum(len(clock["hidden_spikes"]) for clock in clocks),
        "distinct_hidden_source_count": len(
            {
                spike["unit_id"]
                for clock in clocks
                for spike in clock["hidden_spikes"]
            }
        ),
        "maximum_eligible_hidden_sources_at_return": maximum_eligible,
        "selected_reachable_clock": selected,
        "status": "D0_REACHABLE" if selected is not None else "D0_UNREACHABLE",
    }


def run_cell(config: RD006Config, world: dict[str, Any]) -> dict[str, Any]:
    config.validate()
    if world["family"] not in FAMILIES or world["ports"] != PORTS:
        raise ValueError("world is outside the fixed RD006 exposed fixture")
    initial = build_initial_field(config, world)
    initial_state = initial.state_dict()
    initial_state_sha256 = digest(initial_state)
    schedule = training_schedule(world)
    schedule_sha256 = digest(schedule)
    arms = {
        arm: run_arm(initial_state, schedule, arm=arm, config=config) for arm in ARMS
    }
    if len({result["initial_connection_sha256"] for result in arms.values()}) != 1:
        raise RuntimeError("paired arms do not share identical initial connections")
    ready_arms = tuple(arm for arm in ARMS if arms[arm]["status"] == "D0_REACHABLE")
    return {
        "cell_id": f"rv02-rd006-{world['family']}-scale-1",
        "family": world["family"],
        "scale": config.scale,
        "unit_count": config.unit_count,
        "world_id": world["world_id"],
        "world_sha256": world["world_sha256"],
        "topology_sha256": digest(build_topology(config, world)),
        "initial_state_sha256": initial_state_sha256,
        "schedule_sha256": schedule_sha256,
        "schedule_event_count": len(schedule),
        "paired_contract": {
            "same_topology": True,
            "same_schedule": True,
            "same_initial_state": True,
            "same_measurement_clocks": True,
            "only_factor": "ordinary_external_learning_on_vs_off",
        },
        "arms": arms,
        "ready_arms": ready_arms,
        "status": "D0_REACHABLE" if ready_arms else "D0_UNREACHABLE",
    }


def run_matrix(source_git_sha: str) -> dict[str, Any]:
    require_git_sha(source_git_sha)
    config = RD006Config()
    cells = tuple(run_cell(config, world) for world in development_worlds(config))
    ready_cells = tuple(cell["cell_id"] for cell in cells if cell["status"] == "D0_REACHABLE")
    artifact = {
        "schema_version": 1,
        "object_id": OBJECT_ID,
        "protocol_id": PROTOCOL_ID,
        "phase": "OPEN_DEVELOPMENT",
        "claim_ceiling": "SYSTEM",
        "source_git_sha": source_git_sha,
        "prior_generic_mechanism_source_sha": PRIOR_SOURCE_SHA,
        "fresh_identity": True,
        "reuses_rd005_identity": False,
        "formal_execution": False,
        "held_out_execution": False,
        "capability_scoring": False,
        "configuration": config.state_dict(),
        "factors": {
            "ordinary_external_learning": ["OFF", "ON"],
            "hidden_return_learning": "OFF_BOTH_ARMS",
            "threshold_gain_stimulus": "FIXED_BOTH_ARMS",
        },
        "cells": cells,
        "ready_cell_ids": ready_cells,
        "matrix_status": (
            "D0_MECHANISM_SURFACE_EVALUABLE" if ready_cells else "D0_ZERO_REACHABLE_STOP"
        ),
        "later_e0_e1_es_authorized": False,
        "scale_expansion_authorized": False,
        "reservoir_comparison_authorized": False,
        "scientific_interpretation": (
            "development reachability only; prior/build/development observations receive "
            "zero inherited confirmatory credit"
        ),
    }
    artifact["artifact_sha256"] = digest(artifact)
    return artifact


__all__ = [
    "ARMS",
    "FAMILIES",
    "OBJECT_ID",
    "PORTS",
    "PROTOCOL_ID",
    "RD006Config",
    "development_worlds",
    "digest",
    "run_cell",
    "run_matrix",
]

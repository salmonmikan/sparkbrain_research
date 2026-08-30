from __future__ import annotations

import hashlib
import json
import math
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin

from .interference_contract import (
    InterferenceFamily,
    InterferencePhase,
    InterferenceWorldSpec,
    RouteExposure,
    development_worlds,
    world_grid_hash,
)
from .physical_learner_bridge import (
    CurrentPhysicalLearnerBridge,
    PhysicalConnectionSnapshot,
    ResolvedPhysicalLearnerApi,
    build_physical_field,
    connection_snapshots,
    connection_state_hash,
    runtime_pulse,
)

_INITIAL_WEIGHT = 0.05
_MAXIMUM_PROBE_SPIKES = 512


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class RouteProbeRecord:
    world_id: str
    training_phase_index: int
    last_trained_route_id: str
    probe_route_id: str
    cue_unit_id: int
    expected_units: tuple[int, ...]
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    ordered_retention_fraction: float
    exact_route_recovered: bool
    contamination_count: int
    first_hop_targets_generated: tuple[int, ...]
    structural_first_hop_targets: tuple[int, ...]
    first_hop_coverage_fraction: float
    total_spike_count: int
    maximum_queue_size: int
    final_queue_size: int
    halt_reason: str
    connection_state_hash: str

    def validate(self) -> None:
        if self.training_phase_index < 1:
            raise ValueError("training_phase_index must be positive")
        if not self.last_trained_route_id or not self.probe_route_id:
            raise ValueError("route identities must be non-empty")
        if not 0.0 <= self.ordered_retention_fraction <= 1.0:
            raise ValueError("ordered_retention_fraction must be in [0, 1]")
        if not 0.0 <= self.first_hop_coverage_fraction <= 1.0:
            raise ValueError("first_hop_coverage_fraction must be in [0, 1]")
        if self.contamination_count < 0 or self.total_spike_count < 0:
            raise ValueError("probe counts must be non-negative")
        if self.maximum_queue_size < self.final_queue_size:
            raise ValueError("maximum queue size cannot be below final queue size")
        if len(self.connection_state_hash) != 64:
            raise ValueError("connection_state_hash must be a sha256 digest")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TrainingPhaseRecord:
    world_id: str
    phase_index: int
    route_id: str
    exposure_count: int
    accepted_observation_count: int
    ignored_observation_count: int
    connection_hash_before: str
    connection_hash_after: str
    changed_connection_count: int
    suprathreshold_connection_count: int
    active_outgoing_edge_maximum: int
    total_edge_budget_exceeded: bool
    outgoing_edge_budget_exceeded: bool
    observed_minimum_weight: float
    observed_maximum_weight: float
    observed_minimum_delay_ms: float
    observed_maximum_delay_ms: float

    def validate(self) -> None:
        if self.phase_index < 1 or self.exposure_count < 1:
            raise ValueError("training phase and exposure count must be positive")
        if self.accepted_observation_count < 0 or self.ignored_observation_count < 0:
            raise ValueError("observation counts must be non-negative")
        if self.changed_connection_count < 0:
            raise ValueError("changed_connection_count must be non-negative")
        if self.suprathreshold_connection_count < 0:
            raise ValueError("suprathreshold_connection_count must be non-negative")
        if self.active_outgoing_edge_maximum < 0:
            raise ValueError("active_outgoing_edge_maximum must be non-negative")
        if self.observed_minimum_weight > self.observed_maximum_weight:
            raise ValueError("weight bounds are inverted")
        if self.observed_minimum_delay_ms > self.observed_maximum_delay_ms:
            raise ValueError("delay bounds are inverted")
        if self.observed_minimum_delay_ms <= 0.0:
            raise ValueError("physical delays must remain positive")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class InterferenceResourceRecord:
    world_id: str
    route_count: int
    directed_edge_count: int
    external_transition_observation_count: int
    ignored_endogenous_observation_count: int
    generated_probe_spike_count: int
    probe_count: int
    training_phase_count: int
    persistent_connection_entry_count: int
    maximum_queue_size: int
    safety_halt_count: int
    wall_clock_ms: float

    def validate(self) -> None:
        integer_fields = (
            "route_count",
            "directed_edge_count",
            "external_transition_observation_count",
            "ignored_endogenous_observation_count",
            "generated_probe_spike_count",
            "probe_count",
            "training_phase_count",
            "persistent_connection_entry_count",
            "maximum_queue_size",
            "safety_halt_count",
        )
        if any(getattr(self, name) < 0 for name in integer_fields):
            raise ValueError("resource counts must be non-negative")
        if not math.isfinite(self.wall_clock_ms) or self.wall_clock_ms < 0.0:
            raise ValueError("wall_clock_ms must be finite and non-negative")
        if self.route_count < 2:
            raise ValueError("interference resource record requires multiple routes")
        if self.persistent_connection_entry_count != self.directed_edge_count:
            raise ValueError("persistent physical state must equal directed edge count")

    def semantic_state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value.pop("wall_clock_ms")
        return value

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class InterferenceWorldAssessment:
    any_connection_learning_detected: bool
    all_disjoint_routes_retained: bool | None
    shared_branch_coverage_fraction: float | None
    shared_branch_collapse_detected: bool | None
    shared_prefix_retained: bool | None
    reversal_routes_retained: bool | None
    dense_edge_budget_exceeded: bool | None
    endogenous_activity_cannot_write_connections: bool
    no_g1_g2_runtime_state: bool
    development_diagnostic_complete: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class InterferenceWorldResult:
    world_id: str
    world_specification_hash: str
    learner_api: ResolvedPhysicalLearnerApi
    training_phases: tuple[TrainingPhaseRecord, ...]
    probes: tuple[RouteProbeRecord, ...]
    final_connections: tuple[PhysicalConnectionSnapshot, ...]
    resource: InterferenceResourceRecord
    assessment: InterferenceWorldAssessment
    semantic_hash: str

    def validate(self, world: InterferenceWorldSpec) -> None:
        if self.world_id != world.world_id:
            raise ValueError("world result identity mismatch")
        if self.world_specification_hash != world.specification_hash():
            raise ValueError("world result specification hash mismatch")
        if len(self.training_phases) != world.route_count:
            raise ValueError("world result must contain every training phase")
        expected_probe_count = world.route_count * world.route_count
        if len(self.probes) != expected_probe_count:
            raise ValueError("world result probe matrix is incomplete")
        if len({row.phase_index for row in self.training_phases}) != world.route_count:
            raise ValueError("training phase identities are incomplete")
        expected_probe_keys = {
            (phase_index, route.route_id)
            for phase_index in range(1, world.route_count + 1)
            for route in world.routes
        }
        observed_probe_keys = {
            (row.training_phase_index, row.probe_route_id) for row in self.probes
        }
        if observed_probe_keys != expected_probe_keys:
            raise ValueError("probe phase/route coverage is incomplete")
        for row in self.training_phases:
            row.validate()
        for row in self.probes:
            row.validate()
        for row in self.final_connections:
            row.validate()
        self.resource.validate()
        if len(self.semantic_hash) != 64:
            raise ValueError("semantic_hash must be a sha256 digest")

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "final_connections": [row.state_dict() for row in self.final_connections],
            "learner_api": self.learner_api.state_dict(),
            "probes": [row.state_dict() for row in self.probes],
            "resource": self.resource.state_dict(),
            "semantic_hash": self.semantic_hash,
            "training_phases": [row.state_dict() for row in self.training_phases],
            "world_id": self.world_id,
            "world_specification_hash": self.world_specification_hash,
        }


@dataclass(frozen=True, slots=True)
class DevelopmentInterferenceSuite:
    world_grid_hash: str
    worlds: tuple[InterferenceWorldResult, ...]
    suite_hash: str

    @property
    def world_count(self) -> int:
        return len(self.worlds)

    @property
    def total_probe_count(self) -> int:
        return sum(len(world.probes) for world in self.worlds)

    @property
    def total_resource_count(self) -> int:
        return len(self.worlds)

    def state_dict(self) -> dict[str, Any]:
        return {
            "suite_hash": self.suite_hash,
            "total_probe_count": self.total_probe_count,
            "total_resource_count": self.total_resource_count,
            "world_count": self.world_count,
            "world_grid_hash": self.world_grid_hash,
            "worlds": [world.state_dict() for world in self.worlds],
        }


def _directed_edges(world: InterferenceWorldSpec) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            {
                (route.units[index], route.units[index + 1])
                for route in world.routes
                for index in range(len(route.units) - 1)
            }
        )
    )


def _route_map(world: InterferenceWorldSpec) -> dict[str, RouteExposure]:
    return {route.route_id: route for route in world.routes}


def _ordered_coverage(expected: tuple[int, ...], observed: tuple[int, ...]) -> float:
    if not expected:
        return 1.0
    position = 0
    matched = 0
    for value in observed:
        if position < len(expected) and value == expected[position]:
            matched += 1
            position += 1
    return matched / len(expected)


def _queue_size(field: TemporalExcitableField) -> int:
    state = field.state_dict()
    queue = state.get("queue", ())
    return len(queue)


def _probe_route(
    world: InterferenceWorldSpec,
    field: TemporalExcitableField,
    *,
    phase_index: int,
    last_trained_route_id: str,
    route: RouteExposure,
) -> RouteProbeRecord:
    probe = TemporalExcitableField.from_state_dict(field.state_dict())
    cue_time = 100.0
    cue_id = f"probe:{world.world_id}:{phase_index}:{route.route_id}"
    probe.schedule_arrival(
        SynapticArrival(
            time_ms=cue_time,
            target_id=route.units[0],
            current=world.cue_magnitude,
            source_id=None,
            pulse_id=cue_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    horizon = cue_time + world.lag_ms * (len(route.units) + 3)
    slice_ms = max(0.25, world.lag_ms / 4.0)
    current = cue_time
    spikes = []
    maximum_queue = _queue_size(probe)
    halt_reason = "horizon_reached"
    while current < horizon:
        target = min(horizon, current + slice_ms)
        spikes.extend(probe.run_until(target))
        current = target
        maximum_queue = max(maximum_queue, _queue_size(probe))
        if len(spikes) > _MAXIMUM_PROBE_SPIKES:
            halt_reason = "spike_budget_exceeded"
            break
        if _queue_size(probe) == 0 and current > cue_time:
            halt_reason = "queue_drained"
            break
    later = tuple(row for row in spikes if row.time_ms > cue_time)
    generated_units = tuple(row.unit_id for row in later)
    expected = route.units[1:]
    contamination = sum(unit_id not in route.units for unit_id in generated_units)
    structural_first_hops = tuple(
        sorted(
            {
                candidate.units[1]
                for candidate in world.routes
                if candidate.units[0] == route.units[0]
            }
        )
    )
    generated_first_hops = tuple(
        sorted(set(generated_units).intersection(structural_first_hops))
    )
    first_hop_coverage = (
        len(generated_first_hops) / len(structural_first_hops)
        if structural_first_hops
        else 1.0
    )
    coverage = _ordered_coverage(expected, generated_units)
    row = RouteProbeRecord(
        world_id=world.world_id,
        training_phase_index=phase_index,
        last_trained_route_id=last_trained_route_id,
        probe_route_id=route.route_id,
        cue_unit_id=route.units[0],
        expected_units=expected,
        generated_units=generated_units,
        generated_times_ms=tuple(row.time_ms for row in later),
        ordered_retention_fraction=coverage,
        exact_route_recovered=(coverage == 1.0 and contamination == 0),
        contamination_count=contamination,
        first_hop_targets_generated=generated_first_hops,
        structural_first_hop_targets=structural_first_hops,
        first_hop_coverage_fraction=first_hop_coverage,
        total_spike_count=len(spikes),
        maximum_queue_size=maximum_queue,
        final_queue_size=_queue_size(probe),
        halt_reason=halt_reason,
        connection_state_hash=connection_state_hash(probe),
    )
    row.validate()
    return row


def _connection_phase_metrics(
    world: InterferenceWorldSpec,
    rows: tuple[PhysicalConnectionSnapshot, ...],
) -> dict[str, Any]:
    changed = tuple(row for row in rows if not math.isclose(row.weight, _INITIAL_WEIGHT))
    suprathreshold = tuple(
        row
        for row in rows
        if abs(row.weight) * world.cue_magnitude >= world.threshold
    )
    outgoing: defaultdict[int, int] = defaultdict(int)
    for row in suprathreshold:
        outgoing[row.source_id] += 1
    maximum_outgoing = max(outgoing.values(), default=0)
    return {
        "active_outgoing_edge_maximum": maximum_outgoing,
        "changed_connection_count": len(changed),
        "observed_maximum_delay_ms": max(row.delay_ms for row in rows),
        "observed_maximum_weight": max(row.weight for row in rows),
        "observed_minimum_delay_ms": min(row.delay_ms for row in rows),
        "observed_minimum_weight": min(row.weight for row in rows),
        "outgoing_edge_budget_exceeded": (
            maximum_outgoing > world.maximum_active_outgoing_edges
        ),
        "suprathreshold_connection_count": len(suprathreshold),
        "total_edge_budget_exceeded": (
            len(suprathreshold) > world.maximum_total_active_edges
        ),
    }


def _train_route(
    world: InterferenceWorldSpec,
    field: TemporalExcitableField,
    route: RouteExposure,
    *,
    phase_index: int,
) -> tuple[int, int, ResolvedPhysicalLearnerApi]:
    accepted = 0
    ignored = 0
    api: ResolvedPhysicalLearnerApi | None = None
    for episode in range(route.exposure_count):
        bridge = CurrentPhysicalLearnerBridge(field)
        api = bridge.api
        start = float(phase_index * 10000 + episode * 100)
        pulses = tuple(
            runtime_pulse(
                event_id=(
                    f"train:{world.world_id}:{phase_index}:"
                    f"{episode}:{index}"
                ),
                time_ms=start + index * world.lag_ms,
                unit_id=unit_id,
                magnitude=world.cue_magnitude,
                origin=EventOrigin.EXTERNAL,
            )
            for index, unit_id in enumerate(route.units)
        )
        results = bridge.observe_sequence(pulses)
        accepted += sum(row.accepted for row in results)
        ignored += sum(row.ignored_or_rejected for row in results)
    if api is None:
        raise RuntimeError("route training did not resolve a physical learner")
    return accepted, ignored, api


def _endogenous_write_stress(
    world: InterferenceWorldSpec,
    field: TemporalExcitableField,
) -> tuple[int, bool]:
    route = world.routes[0]
    bridge = CurrentPhysicalLearnerBridge(field)
    before = connection_state_hash(field)
    source = runtime_pulse(
        event_id=f"endo-stress:{world.world_id}:source",
        time_ms=500000.0,
        unit_id=route.units[0],
        magnitude=world.cue_magnitude,
        origin=EventOrigin.ENDOGENOUS,
    )
    target = runtime_pulse(
        event_id=f"endo-stress:{world.world_id}:target",
        time_ms=500000.0 + world.lag_ms,
        unit_id=route.units[1],
        magnitude=world.cue_magnitude,
        origin=EventOrigin.ENDOGENOUS,
    )
    rows = bridge.observe_pair(source, target)
    after = connection_state_hash(field)
    ignored = int(rows.ignored_or_rejected or before == after)
    return ignored, before == after


def _assessment(
    world: InterferenceWorldSpec,
    phases: tuple[TrainingPhaseRecord, ...],
    probes: tuple[RouteProbeRecord, ...],
    endogenous_safe: bool,
) -> InterferenceWorldAssessment:
    final_phase = world.route_count
    final_rows = tuple(
        row for row in probes if row.training_phase_index == final_phase
    )
    all_exact = all(row.exact_route_recovered for row in final_rows)
    branch_coverage = None
    branch_collapse = None
    shared_prefix_retained = None
    reversal_retained = None
    dense_budget = None
    disjoint_retained = None
    if world.family is InterferenceFamily.DISJOINT_ROUTES:
        disjoint_retained = all_exact
    elif world.family is InterferenceFamily.SHARED_CUE_BRANCHES:
        branch_coverage = sum(
            row.first_hop_coverage_fraction for row in final_rows
        ) / len(final_rows)
        branch_collapse = branch_coverage < 1.0
    elif world.family is InterferenceFamily.SHARED_PREFIX_BRANCHES:
        shared_prefix_retained = all(
            row.ordered_retention_fraction >= (1.0 / 3.0)
            for row in final_rows
        )
    elif world.family is InterferenceFamily.EDGE_REVERSAL:
        reversal_ids = set(world.reversal_route_ids)
        reversal_retained = all(
            row.ordered_retention_fraction == 1.0
            for row in final_rows
            if row.probe_route_id in reversal_ids
        )
    else:
        dense_budget = phases[-1].total_edge_budget_exceeded
    return InterferenceWorldAssessment(
        any_connection_learning_detected=any(
            row.connection_hash_before != row.connection_hash_after
            for row in phases
        ),
        all_disjoint_routes_retained=disjoint_retained,
        shared_branch_coverage_fraction=branch_coverage,
        shared_branch_collapse_detected=branch_collapse,
        shared_prefix_retained=shared_prefix_retained,
        reversal_routes_retained=reversal_retained,
        dense_edge_budget_exceeded=dense_budget,
        endogenous_activity_cannot_write_connections=endogenous_safe,
        no_g1_g2_runtime_state=True,
        development_diagnostic_complete=(
            len(phases) == world.route_count
            and len(probes) == world.route_count * world.route_count
        ),
    )


def run_interference_world(
    world: InterferenceWorldSpec,
) -> InterferenceWorldResult:
    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError(
            "held-out interference capability execution is sealed before freeze"
        )
    world.validate()
    started = time.perf_counter()
    edges = _directed_edges(world)
    field = build_physical_field(
        unit_count=world.unit_count,
        directed_edges=edges,
        threshold=world.threshold,
        initial_weight=_INITIAL_WEIGHT,
        initial_delay_ms=world.lag_ms,
    )
    route_by_id = _route_map(world)
    phases: list[TrainingPhaseRecord] = []
    probes: list[RouteProbeRecord] = []
    learner_api: ResolvedPhysicalLearnerApi | None = None
    accepted_total = 0
    ignored_total = 0
    for phase_index, route_id in enumerate(world.training_order, start=1):
        route = route_by_id[route_id]
        before = connection_state_hash(field)
        accepted, ignored, api = _train_route(
            world,
            field,
            route,
            phase_index=phase_index,
        )
        learner_api = api
        accepted_total += accepted
        ignored_total += ignored
        after = connection_state_hash(field)
        connections = connection_snapshots(field)
        metrics = _connection_phase_metrics(world, connections)
        phase = TrainingPhaseRecord(
            world_id=world.world_id,
            phase_index=phase_index,
            route_id=route.route_id,
            exposure_count=route.exposure_count,
            accepted_observation_count=accepted,
            ignored_observation_count=ignored,
            connection_hash_before=before,
            connection_hash_after=after,
            **metrics,
        )
        phase.validate()
        phases.append(phase)
        for probe_id in world.probe_order:
            probes.append(
                _probe_route(
                    world,
                    field,
                    phase_index=phase_index,
                    last_trained_route_id=route.route_id,
                    route=route_by_id[probe_id],
                )
            )
    if learner_api is None:
        raise RuntimeError("interference world did not resolve a physical learner")
    endogenous_ignored, endogenous_safe = _endogenous_write_stress(world, field)
    ignored_total += endogenous_ignored
    final_connections = connection_snapshots(field)
    resource = InterferenceResourceRecord(
        world_id=world.world_id,
        route_count=world.route_count,
        directed_edge_count=len(edges),
        external_transition_observation_count=accepted_total,
        ignored_endogenous_observation_count=endogenous_ignored,
        generated_probe_spike_count=sum(row.total_spike_count for row in probes),
        probe_count=len(probes),
        training_phase_count=len(phases),
        persistent_connection_entry_count=len(final_connections),
        maximum_queue_size=max(
            (row.maximum_queue_size for row in probes),
            default=0,
        ),
        safety_halt_count=sum(
            row.halt_reason == "spike_budget_exceeded" for row in probes
        ),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
    )
    resource.validate()
    phase_rows = tuple(phases)
    probe_rows = tuple(probes)
    assessment = _assessment(
        world,
        phase_rows,
        probe_rows,
        endogenous_safe,
    )
    semantic_payload = {
        "assessment": assessment.state_dict(),
        "final_connections": [row.state_dict() for row in final_connections],
        "learner_api": learner_api.state_dict(),
        "probes": [row.state_dict() for row in probe_rows],
        "resource": resource.semantic_state_dict(),
        "training_phases": [row.state_dict() for row in phase_rows],
        "world_id": world.world_id,
        "world_specification_hash": world.specification_hash(),
    }
    result = InterferenceWorldResult(
        world_id=world.world_id,
        world_specification_hash=world.specification_hash(),
        learner_api=learner_api,
        training_phases=phase_rows,
        probes=probe_rows,
        final_connections=final_connections,
        resource=resource,
        assessment=assessment,
        semantic_hash=_digest(semantic_payload),
    )
    result.validate(world)
    return result


def run_development_interference_suite() -> DevelopmentInterferenceSuite:
    specs = development_worlds()
    worlds = tuple(run_interference_world(world) for world in specs)
    payload = {
        "world_grid_hash": world_grid_hash(specs),
        "worlds": [
            {
                "semantic_hash": world.semantic_hash,
                "world_id": world.world_id,
            }
            for world in worlds
        ],
    }
    return DevelopmentInterferenceSuite(
        world_grid_hash=world_grid_hash(specs),
        worlds=worlds,
        suite_hash=_digest(payload),
    )

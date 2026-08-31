from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin

from .interference_contract import (
    InterferenceFamily,
    InterferencePhase,
    InterferenceWorldSpec,
    development_worlds,
    world_grid_hash,
)
from .interference_runner import (
    _INITIAL_WEIGHT,
    _directed_edges,
    _endogenous_write_stress,
    _probe_route,
    _route_map,
    _train_route,
)
from .physical_learner_bridge import (
    CurrentPhysicalLearnerBridge,
    build_physical_field,
    connection_snapshots,
    connection_state_hash,
    runtime_pulse,
)


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
class InterventionEdgeSelection:
    target_route_id: str
    matched_route_id: str
    target_edge: tuple[int, int]
    matched_edge: tuple[int, int]

    def validate(self) -> None:
        if not self.target_route_id or not self.matched_route_id:
            raise ValueError("intervention route identities must be non-empty")
        if self.target_route_id == self.matched_route_id:
            raise ValueError("target and matched routes must differ")
        if self.target_edge == self.matched_edge:
            raise ValueError("target and matched edges must differ")
        if set(self.target_edge).intersection(self.matched_edge):
            raise ValueError("matched edge must be endpoint-disjoint from target edge")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ControlConditionSummary:
    condition_id: str
    connection_state_hash: str
    probe_signature_hash: str
    mean_ordered_retention_fraction: float
    exact_route_count: int
    contamination_count: int
    mean_first_hop_coverage_fraction: float
    target_route_retention_fraction: float
    matched_route_retention_fraction: float

    def validate(self, *, route_count: int) -> None:
        if not self.condition_id:
            raise ValueError("condition_id must be non-empty")
        if len(self.connection_state_hash) != 64 or len(self.probe_signature_hash) != 64:
            raise ValueError("condition hashes must be sha256 digests")
        for value in (
            self.mean_ordered_retention_fraction,
            self.mean_first_hop_coverage_fraction,
            self.target_route_retention_fraction,
            self.matched_route_retention_fraction,
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError("control fractions must be in [0, 1]")
        if not 0 <= self.exact_route_count <= route_count:
            raise ValueError("exact_route_count outside route count")
        if self.contamination_count < 0:
            raise ValueError("contamination_count must be non-negative")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PlasticityFreezeAssessment:
    phase_count: int
    probe_equivalent_phase_count: int
    blocked_external_write_phase_count: int
    all_phase_probes_equivalent: bool
    all_external_writes_blocked: bool

    def validate(self) -> None:
        if self.phase_count < 1:
            raise ValueError("phase_count must be positive")
        for value in (
            self.probe_equivalent_phase_count,
            self.blocked_external_write_phase_count,
        ):
            if not 0 <= value <= self.phase_count:
                raise ValueError("freeze phase count outside phase_count")
        if self.all_phase_probes_equivalent != (
            self.probe_equivalent_phase_count == self.phase_count
        ):
            raise ValueError("probe-equivalence aggregate is inconsistent")
        if self.all_external_writes_blocked != (
            self.blocked_external_write_phase_count == self.phase_count
        ):
            raise ValueError("external-write aggregate is inconsistent")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class InterferenceControlAssessment:
    deterministic_replay_connection_hash: bool
    deterministic_replay_probe_hash: bool
    probe_order_invariant: bool
    plasticity_disable_preserves_execution: bool
    plasticity_disable_blocks_external_learning: bool
    endogenous_activity_cannot_write_connections: bool
    target_edge_retention_delta: float
    matched_ablation_target_retention_delta: float
    target_edge_selective_delta: float
    reversed_order_retention_delta: float

    def validate(self) -> None:
        for value in (
            self.target_edge_retention_delta,
            self.matched_ablation_target_retention_delta,
            self.target_edge_selective_delta,
            self.reversed_order_retention_delta,
        ):
            if not math.isfinite(value) or not -1.0 <= value <= 1.0:
                raise ValueError("intervention delta must be finite and in [-1, 1]")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class InterferenceControlWorldResult:
    world_id: str
    world_specification_hash: str
    edge_selection: InterventionEdgeSelection
    baseline: ControlConditionSummary
    reset_all_connections: ControlConditionSummary
    weights_only_transplant: ControlConditionSummary
    delays_only_transplant: ControlConditionSummary
    target_edge_removed: ControlConditionSummary
    matched_edge_removed: ControlConditionSummary
    reversed_training_order: ControlConditionSummary
    permuted_probe_order: ControlConditionSummary
    deterministic_replay: ControlConditionSummary
    plasticity_freeze: PlasticityFreezeAssessment
    assessment: InterferenceControlAssessment
    semantic_hash: str

    def validate(self, world: InterferenceWorldSpec) -> None:
        if self.world_id != world.world_id:
            raise ValueError("control result world identity mismatch")
        if self.world_specification_hash != world.specification_hash():
            raise ValueError("control result world specification mismatch")
        self.edge_selection.validate()
        for row in (
            self.baseline,
            self.reset_all_connections,
            self.weights_only_transplant,
            self.delays_only_transplant,
            self.target_edge_removed,
            self.matched_edge_removed,
            self.reversed_training_order,
            self.permuted_probe_order,
            self.deterministic_replay,
        ):
            row.validate(route_count=world.route_count)
        self.plasticity_freeze.validate()
        self.assessment.validate()
        if len(self.semantic_hash) != 64:
            raise ValueError("semantic_hash must be a sha256 digest")

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "baseline": self.baseline.state_dict(),
            "delays_only_transplant": self.delays_only_transplant.state_dict(),
            "deterministic_replay": self.deterministic_replay.state_dict(),
            "edge_selection": self.edge_selection.state_dict(),
            "matched_edge_removed": self.matched_edge_removed.state_dict(),
            "permuted_probe_order": self.permuted_probe_order.state_dict(),
            "plasticity_freeze": self.plasticity_freeze.state_dict(),
            "reset_all_connections": self.reset_all_connections.state_dict(),
            "reversed_training_order": self.reversed_training_order.state_dict(),
            "semantic_hash": self.semantic_hash,
            "target_edge_removed": self.target_edge_removed.state_dict(),
            "weights_only_transplant": self.weights_only_transplant.state_dict(),
            "world_id": self.world_id,
            "world_specification_hash": self.world_specification_hash,
        }


@dataclass(frozen=True, slots=True)
class DevelopmentInterferenceControlSuite:
    world_grid_hash: str
    worlds: tuple[InterferenceControlWorldResult, ...]
    suite_hash: str

    @property
    def world_count(self) -> int:
        return len(self.worlds)

    def state_dict(self) -> dict[str, Any]:
        return {
            "suite_hash": self.suite_hash,
            "world_count": self.world_count,
            "world_grid_hash": self.world_grid_hash,
            "worlds": [row.state_dict() for row in self.worlds],
        }


def _new_field(
    world: InterferenceWorldSpec,
    *,
    excluded_edge: tuple[int, int] | None = None,
) -> TemporalExcitableField:
    edges = _directed_edges(world)
    if excluded_edge is not None:
        if excluded_edge not in edges:
            raise ValueError("excluded intervention edge is absent from world topology")
        edges = tuple(edge for edge in edges if edge != excluded_edge)
    return build_physical_field(
        unit_count=world.unit_count,
        directed_edges=edges,
        threshold=world.threshold,
        initial_weight=_INITIAL_WEIGHT,
        initial_delay_ms=world.lag_ms,
    )


def _train_field(
    world: InterferenceWorldSpec,
    order: tuple[str, ...],
) -> TemporalExcitableField:
    if set(order) != {row.route_id for row in world.routes} or len(order) != world.route_count:
        raise ValueError("control training order must contain every route exactly once")
    field = _new_field(world)
    route_by_id = _route_map(world)
    for phase_index, route_id in enumerate(order, start=1):
        _train_route(
            world,
            field,
            route_by_id[route_id],
            phase_index=phase_index,
        )
    return field


def _transplant_connections(
    donor: TemporalExcitableField,
    recipient: TemporalExcitableField,
    *,
    weights: bool,
    delays: bool,
) -> None:
    snapshots = {
        (row.source_id, row.target_id): row for row in connection_snapshots(donor)
    }
    for key, edge in sorted(recipient.connections.items()):
        source = snapshots.get(key)
        if source is None:
            raise ValueError("recipient contains an edge absent from donor")
        if weights:
            edge.weight = source.weight
        if delays:
            edge.delay_ms = source.delay_ms


def _probe_rows(
    world: InterferenceWorldSpec,
    field: TemporalExcitableField,
    *,
    training_order: tuple[str, ...],
    probe_order: tuple[str, ...],
) -> tuple[Any, ...]:
    if set(probe_order) != {row.route_id for row in world.routes} or len(probe_order) != world.route_count:
        raise ValueError("control probe order must contain every route exactly once")
    route_by_id = _route_map(world)
    return tuple(
        _probe_route(
            world,
            field,
            phase_index=world.route_count,
            last_trained_route_id=training_order[-1],
            route=route_by_id[route_id],
        )
        for route_id in probe_order
    )


def _probe_signature(rows: tuple[Any, ...]) -> str:
    payload = []
    for row in sorted(rows, key=lambda item: item.probe_route_id):
        payload.append(
            {
                "contamination_count": row.contamination_count,
                "exact_route_recovered": row.exact_route_recovered,
                "first_hop_coverage_fraction": row.first_hop_coverage_fraction,
                "first_hop_targets_generated": list(row.first_hop_targets_generated),
                "generated_times_ms": list(row.generated_times_ms),
                "generated_units": list(row.generated_units),
                "ordered_retention_fraction": row.ordered_retention_fraction,
                "probe_route_id": row.probe_route_id,
            }
        )
    return _digest(payload)


def _summarize(
    condition_id: str,
    world: InterferenceWorldSpec,
    field: TemporalExcitableField,
    *,
    selection: InterventionEdgeSelection,
    training_order: tuple[str, ...],
    probe_order: tuple[str, ...] | None = None,
) -> ControlConditionSummary:
    rows = _probe_rows(
        world,
        field,
        training_order=training_order,
        probe_order=probe_order or world.probe_order,
    )
    by_route = {row.probe_route_id: row for row in rows}
    result = ControlConditionSummary(
        condition_id=condition_id,
        connection_state_hash=connection_state_hash(field),
        probe_signature_hash=_probe_signature(rows),
        mean_ordered_retention_fraction=(
            sum(row.ordered_retention_fraction for row in rows) / len(rows)
        ),
        exact_route_count=sum(row.exact_route_recovered for row in rows),
        contamination_count=sum(row.contamination_count for row in rows),
        mean_first_hop_coverage_fraction=(
            sum(row.first_hop_coverage_fraction for row in rows) / len(rows)
        ),
        target_route_retention_fraction=(
            by_route[selection.target_route_id].ordered_retention_fraction
        ),
        matched_route_retention_fraction=(
            by_route[selection.matched_route_id].ordered_retention_fraction
        ),
    )
    result.validate(route_count=world.route_count)
    return result


def _select_intervention_edges(
    world: InterferenceWorldSpec,
) -> InterventionEdgeSelection:
    routes = _route_map(world)
    if world.family is InterferenceFamily.EDGE_REVERSAL:
        target_route_id = "route:forward"
        matched_route_id = "route:control"
        target_units = routes[target_route_id].units
        matched_units = routes[matched_route_id].units
        selection = InterventionEdgeSelection(
            target_route_id=target_route_id,
            matched_route_id=matched_route_id,
            target_edge=(target_units[1], target_units[2]),
            matched_edge=(matched_units[1], matched_units[2]),
        )
        selection.validate()
        return selection

    target_route_id = world.training_order[0]
    target_units = routes[target_route_id].units
    target_edge = (target_units[-2], target_units[-1])
    matched_route_id = ""
    matched_edge: tuple[int, int] | None = None
    for route_id in world.training_order[1:]:
        units = routes[route_id].units
        candidate = (units[-2], units[-1])
        if not set(target_edge).intersection(candidate):
            matched_route_id = route_id
            matched_edge = candidate
            break
    if matched_edge is None:
        raise RuntimeError("no endpoint-disjoint matched edge exists for intervention")
    selection = InterventionEdgeSelection(
        target_route_id=target_route_id,
        matched_route_id=matched_route_id,
        target_edge=target_edge,
        matched_edge=matched_edge,
    )
    selection.validate()
    return selection


def _ablated_field(
    world: InterferenceWorldSpec,
    donor: TemporalExcitableField,
    edge: tuple[int, int],
) -> TemporalExcitableField:
    result = _new_field(world, excluded_edge=edge)
    _transplant_connections(donor, result, weights=True, delays=True)
    return result


def _plasticity_freeze_assessment(
    world: InterferenceWorldSpec,
) -> PlasticityFreezeAssessment:
    field = _new_field(world)
    route_by_id = _route_map(world)
    equivalent = 0
    blocked = 0
    for phase_index, route_id in enumerate(world.training_order, start=1):
        _train_route(
            world,
            field,
            route_by_id[route_id],
            phase_index=phase_index,
        )
        normal_rows = tuple(
            _probe_route(
                world,
                field,
                phase_index=phase_index,
                last_trained_route_id=route_id,
                route=route_by_id[probe_id],
            )
            for probe_id in world.probe_order
        )
        frozen = TemporalExcitableField.from_state_dict(field.state_dict())
        for edge in frozen.connections.values():
            edge.plastic = False
        frozen_rows = tuple(
            _probe_route(
                world,
                frozen,
                phase_index=phase_index,
                last_trained_route_id=route_id,
                route=route_by_id[probe_id],
            )
            for probe_id in world.probe_order
        )
        if _probe_signature(normal_rows) == _probe_signature(frozen_rows):
            equivalent += 1

        bridge = CurrentPhysicalLearnerBridge(frozen)
        first = world.routes[0]
        before = connection_state_hash(frozen)
        start = 900000.0 + phase_index * 100.0
        bridge.observe_pair(
            runtime_pulse(
                event_id=f"freeze:{world.world_id}:{phase_index}:source",
                time_ms=start,
                unit_id=first.units[0],
                magnitude=world.cue_magnitude,
                origin=EventOrigin.EXTERNAL,
            ),
            runtime_pulse(
                event_id=f"freeze:{world.world_id}:{phase_index}:target",
                time_ms=start + world.lag_ms,
                unit_id=first.units[1],
                magnitude=world.cue_magnitude,
                origin=EventOrigin.EXTERNAL,
            ),
        )
        if connection_state_hash(frozen) == before:
            blocked += 1

    result = PlasticityFreezeAssessment(
        phase_count=world.route_count,
        probe_equivalent_phase_count=equivalent,
        blocked_external_write_phase_count=blocked,
        all_phase_probes_equivalent=(equivalent == world.route_count),
        all_external_writes_blocked=(blocked == world.route_count),
    )
    result.validate()
    return result


def run_interference_control_world(
    world: InterferenceWorldSpec,
) -> InterferenceControlWorldResult:
    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError(
            "held-out interference controls are sealed before R01-12E freeze"
        )
    world.validate()
    selection = _select_intervention_edges(world)

    donor = _train_field(world, world.training_order)
    baseline = _summarize(
        "baseline",
        world,
        donor,
        selection=selection,
        training_order=world.training_order,
    )

    reset_field = _new_field(world)
    reset = _summarize(
        "reset-all-connections",
        world,
        reset_field,
        selection=selection,
        training_order=world.training_order,
    )

    weights_field = _new_field(world)
    _transplant_connections(donor, weights_field, weights=True, delays=False)
    weights_only = _summarize(
        "weights-only-transplant",
        world,
        weights_field,
        selection=selection,
        training_order=world.training_order,
    )

    delays_field = _new_field(world)
    _transplant_connections(donor, delays_field, weights=False, delays=True)
    delays_only = _summarize(
        "delays-only-transplant",
        world,
        delays_field,
        selection=selection,
        training_order=world.training_order,
    )

    target_removed = _summarize(
        "target-edge-removed",
        world,
        _ablated_field(world, donor, selection.target_edge),
        selection=selection,
        training_order=world.training_order,
    )
    matched_removed = _summarize(
        "matched-edge-removed",
        world,
        _ablated_field(world, donor, selection.matched_edge),
        selection=selection,
        training_order=world.training_order,
    )

    reversed_order = tuple(reversed(world.training_order))
    reversed_field = _train_field(world, reversed_order)
    reversed_summary = _summarize(
        "reversed-training-order",
        world,
        reversed_field,
        selection=selection,
        training_order=reversed_order,
    )

    permuted_probe_order = tuple(reversed(world.probe_order))
    permuted_probe = _summarize(
        "permuted-probe-order",
        world,
        donor,
        selection=selection,
        training_order=world.training_order,
        probe_order=permuted_probe_order,
    )

    replay_field = _train_field(world, world.training_order)
    replay = _summarize(
        "deterministic-replay",
        world,
        replay_field,
        selection=selection,
        training_order=world.training_order,
    )

    freeze = _plasticity_freeze_assessment(world)
    _, endogenous_safe = _endogenous_write_stress(world, donor)

    target_delta = (
        baseline.target_route_retention_fraction
        - target_removed.target_route_retention_fraction
    )
    matched_target_delta = (
        baseline.target_route_retention_fraction
        - matched_removed.target_route_retention_fraction
    )
    assessment = InterferenceControlAssessment(
        deterministic_replay_connection_hash=(
            replay.connection_state_hash == baseline.connection_state_hash
        ),
        deterministic_replay_probe_hash=(
            replay.probe_signature_hash == baseline.probe_signature_hash
        ),
        probe_order_invariant=(
            permuted_probe.probe_signature_hash == baseline.probe_signature_hash
        ),
        plasticity_disable_preserves_execution=freeze.all_phase_probes_equivalent,
        plasticity_disable_blocks_external_learning=freeze.all_external_writes_blocked,
        endogenous_activity_cannot_write_connections=endogenous_safe,
        target_edge_retention_delta=target_delta,
        matched_ablation_target_retention_delta=matched_target_delta,
        target_edge_selective_delta=(target_delta - matched_target_delta),
        reversed_order_retention_delta=(
            reversed_summary.mean_ordered_retention_fraction
            - baseline.mean_ordered_retention_fraction
        ),
    )
    assessment.validate()

    semantic_payload = {
        "assessment": assessment.state_dict(),
        "baseline": baseline.state_dict(),
        "delays_only_transplant": delays_only.state_dict(),
        "deterministic_replay": replay.state_dict(),
        "edge_selection": selection.state_dict(),
        "matched_edge_removed": matched_removed.state_dict(),
        "permuted_probe_order": permuted_probe.state_dict(),
        "plasticity_freeze": freeze.state_dict(),
        "reset_all_connections": reset.state_dict(),
        "reversed_training_order": reversed_summary.state_dict(),
        "target_edge_removed": target_removed.state_dict(),
        "weights_only_transplant": weights_only.state_dict(),
        "world_id": world.world_id,
        "world_specification_hash": world.specification_hash(),
    }
    result = InterferenceControlWorldResult(
        world_id=world.world_id,
        world_specification_hash=world.specification_hash(),
        edge_selection=selection,
        baseline=baseline,
        reset_all_connections=reset,
        weights_only_transplant=weights_only,
        delays_only_transplant=delays_only,
        target_edge_removed=target_removed,
        matched_edge_removed=matched_removed,
        reversed_training_order=reversed_summary,
        permuted_probe_order=permuted_probe,
        deterministic_replay=replay,
        plasticity_freeze=freeze,
        assessment=assessment,
        semantic_hash=_digest(semantic_payload),
    )
    result.validate(world)
    return result


def run_development_interference_control_suite() -> DevelopmentInterferenceControlSuite:
    specs = development_worlds()
    worlds = tuple(run_interference_control_world(world) for world in specs)
    payload = {
        "world_grid_hash": world_grid_hash(specs),
        "worlds": [
            {"semantic_hash": row.semantic_hash, "world_id": row.world_id}
            for row in worlds
        ],
    }
    return DevelopmentInterferenceControlSuite(
        world_grid_hash=world_grid_hash(specs),
        worlds=worlds,
        suite_hash=_digest(payload),
    )

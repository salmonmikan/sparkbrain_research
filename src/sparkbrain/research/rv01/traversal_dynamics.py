from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest

from .interference_contract import InterferenceFamily, InterferencePhase
from .interference_runner import run_interference_world
from .resource_matched_reservoir import run_resource_matched_reservoir_world
from .traversal_dynamics_contract import (
    TraversalDynamicsWorldSpec,
    development_traversal_dynamics_worlds,
    traversal_dynamics_world_grid_hash,
)


@dataclass(frozen=True, slots=True)
class TraversalMetrics:
    event_count: int
    distinct_unit_count: int
    revisit_count: int
    revisit_rate: float
    new_state_yield: float
    first_visit_positions: tuple[int, ...]
    normalized_discovery_auc: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TraversalProbeComparison:
    world_id: str
    family: str
    probe_route_id: str
    field_raw_units: tuple[int, ...]
    reservoir_raw_units: tuple[int, ...]
    common_distinct_budget: int
    field_common_breadth_units: tuple[int, ...]
    reservoir_common_breadth_units: tuple[int, ...]
    field_raw: TraversalMetrics
    reservoir_raw: TraversalMetrics
    field_common_breadth: TraversalMetrics
    reservoir_common_breadth: TraversalMetrics
    field_ordered_retention: float
    reservoir_ordered_retention: float
    field_exact_route_recovered: bool
    reservoir_exact_route_recovered: bool
    field_contamination_count: int
    reservoir_contamination_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TraversalDynamicsWorldResult:
    world_id: str
    family: str
    seed: int
    world_specification_hash: str
    field_semantic_hash: str
    comparator_semantic_hash: str
    resource_match_passed: bool
    field_reexecution_consistent: bool
    deterministic_replay_state_hash: bool
    deterministic_replay_probe_hash: bool
    probes: tuple[TraversalProbeComparison, ...]
    summary: dict[str, float | int]
    semantic_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "comparator_semantic_hash": self.comparator_semantic_hash,
            "deterministic_replay_probe_hash": self.deterministic_replay_probe_hash,
            "deterministic_replay_state_hash": self.deterministic_replay_state_hash,
            "family": self.family,
            "field_reexecution_consistent": self.field_reexecution_consistent,
            "field_semantic_hash": self.field_semantic_hash,
            "probes": [probe.state_dict() for probe in self.probes],
            "resource_match_passed": self.resource_match_passed,
            "seed": self.seed,
            "semantic_hash": self.semantic_hash,
            "summary": self.summary,
            "world_id": self.world_id,
            "world_specification_hash": self.world_specification_hash,
        }


def _traversal_metrics(trace: tuple[int, ...]) -> TraversalMetrics:
    if not trace:
        return TraversalMetrics(
            event_count=0,
            distinct_unit_count=0,
            revisit_count=0,
            revisit_rate=0.0,
            new_state_yield=0.0,
            first_visit_positions=(),
            normalized_discovery_auc=0.0,
        )

    seen: set[int] = set()
    first_positions: list[int] = []
    cumulative_distinct: list[int] = []
    for index, unit in enumerate(trace, start=1):
        if unit not in seen:
            seen.add(unit)
            first_positions.append(index)
        cumulative_distinct.append(len(seen))

    events = len(trace)
    distinct = len(seen)
    revisits = events - distinct
    observed_area = sum(cumulative_distinct)
    ideal_area = (
        distinct * (distinct + 1) / 2
        + distinct * (events - distinct)
    )
    normalized_auc = observed_area / ideal_area if ideal_area else 0.0
    return TraversalMetrics(
        event_count=events,
        distinct_unit_count=distinct,
        revisit_count=revisits,
        revisit_rate=revisits / events,
        new_state_yield=distinct / events,
        first_visit_positions=tuple(first_positions),
        normalized_discovery_auc=normalized_auc,
    )


def _prefix_for_distinct_budget(
    trace: tuple[int, ...],
    distinct_budget: int,
) -> tuple[int, ...]:
    if distinct_budget < 0 or distinct_budget > len(set(trace)):
        raise ValueError("invalid distinct budget")
    if distinct_budget == 0:
        return ()
    seen: set[int] = set()
    prefix: list[int] = []
    for unit in trace:
        prefix.append(unit)
        seen.add(unit)
        if len(seen) == distinct_budget:
            return tuple(prefix)
    raise RuntimeError("distinct prefix construction failed")


def _field_consistent(field_result: Any, comparator_result: Any) -> bool:
    phase = len(field_result.training_phases)
    rows = tuple(
        row
        for row in field_result.probes
        if row.training_phase_index == phase
    )
    assessment = comparator_result.assessment
    return all(
        (
            math.isclose(
                sum(row.ordered_retention_fraction for row in rows) / len(rows),
                assessment.field_mean_ordered_retention,
            ),
            sum(row.exact_route_recovered for row in rows)
            == assessment.field_exact_route_count,
            sum(row.contamination_count for row in rows)
            == assessment.field_contamination_count,
            math.isclose(
                sum(row.first_hop_coverage_fraction for row in rows) / len(rows),
                assessment.field_mean_first_hop_coverage,
            ),
        )
    )


def _mean(values: Iterable[float | int]) -> float:
    rows = tuple(float(value) for value in values)
    if not rows:
        raise ValueError("mean requires values")
    return sum(rows) / len(rows)


def _summary(
    probes: Iterable[TraversalProbeComparison],
) -> dict[str, float | int]:
    rows = tuple(probes)
    if not rows:
        raise ValueError("summary requires probes")

    field_raw = tuple(row.field_raw for row in rows)
    reservoir_raw = tuple(row.reservoir_raw for row in rows)
    field_common = tuple(row.field_common_breadth for row in rows)
    reservoir_common = tuple(row.reservoir_common_breadth for row in rows)
    deltas = tuple(
        field.event_count - reservoir.event_count
        for field, reservoir in zip(field_common, reservoir_common, strict=True)
    )

    return {
        "probe_count": len(rows),
        "raw_field_mean_event_count": _mean(x.event_count for x in field_raw),
        "raw_reservoir_mean_event_count": _mean(
            x.event_count for x in reservoir_raw
        ),
        "raw_field_mean_distinct_count": _mean(
            x.distinct_unit_count for x in field_raw
        ),
        "raw_reservoir_mean_distinct_count": _mean(
            x.distinct_unit_count for x in reservoir_raw
        ),
        "raw_field_mean_revisit_rate": _mean(x.revisit_rate for x in field_raw),
        "raw_reservoir_mean_revisit_rate": _mean(
            x.revisit_rate for x in reservoir_raw
        ),
        "raw_field_mean_new_state_yield": _mean(
            x.new_state_yield for x in field_raw
        ),
        "raw_reservoir_mean_new_state_yield": _mean(
            x.new_state_yield for x in reservoir_raw
        ),
        "raw_field_mean_discovery_auc": _mean(
            x.normalized_discovery_auc for x in field_raw
        ),
        "raw_reservoir_mean_discovery_auc": _mean(
            x.normalized_discovery_auc for x in reservoir_raw
        ),
        "common_breadth_mean": _mean(row.common_distinct_budget for row in rows),
        "common_field_mean_event_count": _mean(
            x.event_count for x in field_common
        ),
        "common_reservoir_mean_event_count": _mean(
            x.event_count for x in reservoir_common
        ),
        "common_field_minus_reservoir_mean_events": _mean(deltas),
        "common_field_mean_revisit_count": _mean(
            x.revisit_count for x in field_common
        ),
        "common_reservoir_mean_revisit_count": _mean(
            x.revisit_count for x in reservoir_common
        ),
        "common_field_mean_revisit_rate": _mean(
            x.revisit_rate for x in field_common
        ),
        "common_reservoir_mean_revisit_rate": _mean(
            x.revisit_rate for x in reservoir_common
        ),
        "common_field_mean_new_state_yield": _mean(
            x.new_state_yield for x in field_common
        ),
        "common_reservoir_mean_new_state_yield": _mean(
            x.new_state_yield for x in reservoir_common
        ),
        "common_field_mean_discovery_auc": _mean(
            x.normalized_discovery_auc for x in field_common
        ),
        "common_reservoir_mean_discovery_auc": _mean(
            x.normalized_discovery_auc for x in reservoir_common
        ),
        "common_field_faster_probe_count": sum(delta < 0 for delta in deltas),
        "common_tied_probe_count": sum(delta == 0 for delta in deltas),
        "common_field_slower_probe_count": sum(delta > 0 for delta in deltas),
        "context_field_mean_ordered_retention": _mean(
            row.field_ordered_retention for row in rows
        ),
        "context_reservoir_mean_ordered_retention": _mean(
            row.reservoir_ordered_retention for row in rows
        ),
        "context_field_exact_route_count": sum(
            row.field_exact_route_recovered for row in rows
        ),
        "context_reservoir_exact_route_count": sum(
            row.reservoir_exact_route_recovered for row in rows
        ),
        "context_field_contamination_count": sum(
            row.field_contamination_count for row in rows
        ),
        "context_reservoir_contamination_count": sum(
            row.reservoir_contamination_count for row in rows
        ),
    }


def run_traversal_dynamics_world(
    world: TraversalDynamicsWorldSpec,
) -> TraversalDynamicsWorldResult:
    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError("R01-14 held-out capability execution is not open")
    world.validate()

    field_result = run_interference_world(world)
    comparator = run_resource_matched_reservoir_world(world)
    consistent = _field_consistent(field_result, comparator)
    if not consistent:
        raise RuntimeError("Field rerun diverged from comparator-embedded Field run")

    phase = world.route_count
    field = {
        row.probe_route_id: row
        for row in field_result.probes
        if row.training_phase_index == phase
    }
    reservoir = {row.probe_route_id: row for row in comparator.probes}
    probes: list[TraversalProbeComparison] = []

    for route_id in world.probe_order:
        field_probe = field[route_id]
        reservoir_probe = reservoir[route_id]
        field_raw = tuple(field_probe.generated_units)
        reservoir_raw = tuple(reservoir_probe.generated_units)
        common_distinct = min(len(set(field_raw)), len(set(reservoir_raw)))
        field_common = _prefix_for_distinct_budget(field_raw, common_distinct)
        reservoir_common = _prefix_for_distinct_budget(
            reservoir_raw,
            common_distinct,
        )
        probes.append(
            TraversalProbeComparison(
                world_id=world.world_id,
                family=world.family.value,
                probe_route_id=route_id,
                field_raw_units=field_raw,
                reservoir_raw_units=reservoir_raw,
                common_distinct_budget=common_distinct,
                field_common_breadth_units=field_common,
                reservoir_common_breadth_units=reservoir_common,
                field_raw=_traversal_metrics(field_raw),
                reservoir_raw=_traversal_metrics(reservoir_raw),
                field_common_breadth=_traversal_metrics(field_common),
                reservoir_common_breadth=_traversal_metrics(reservoir_common),
                field_ordered_retention=field_probe.ordered_retention_fraction,
                reservoir_ordered_retention=(
                    reservoir_probe.ordered_retention_fraction
                ),
                field_exact_route_recovered=field_probe.exact_route_recovered,
                reservoir_exact_route_recovered=(
                    reservoir_probe.exact_route_recovered
                ),
                field_contamination_count=field_probe.contamination_count,
                reservoir_contamination_count=reservoir_probe.contamination_count,
            )
        )

    probe_rows = tuple(probes)
    summary = _summary(probe_rows)
    payload = {
        "comparator_semantic_hash": comparator.semantic_hash,
        "field_semantic_hash": field_result.semantic_hash,
        "probes": [probe.state_dict() for probe in probe_rows],
        "summary": summary,
        "world": world.state_dict(),
    }
    return TraversalDynamicsWorldResult(
        world_id=world.world_id,
        family=world.family.value,
        seed=world.seed,
        world_specification_hash=world.specification_hash(),
        field_semantic_hash=field_result.semantic_hash,
        comparator_semantic_hash=comparator.semantic_hash,
        resource_match_passed=comparator.resources.resource_match_passed,
        field_reexecution_consistent=consistent,
        deterministic_replay_state_hash=(
            comparator.assessment.deterministic_replay_state_hash
        ),
        deterministic_replay_probe_hash=(
            comparator.assessment.deterministic_replay_probe_hash
        ),
        probes=probe_rows,
        summary=summary,
        semantic_hash=digest(payload),
    )


def _suite_summary(
    worlds: tuple[TraversalDynamicsWorldResult, ...],
) -> dict[str, float | int]:
    summary = _summary(tuple(probe for world in worlds for probe in world.probes))
    summary["world_count"] = len(worlds)
    key = "common_field_minus_reservoir_mean_events"
    deltas = tuple(float(world.summary[key]) for world in worlds)
    summary["common_field_faster_world_count"] = sum(delta < 0.0 for delta in deltas)
    summary["common_tied_world_count"] = sum(
        math.isclose(delta, 0.0) for delta in deltas
    )
    summary["common_field_slower_world_count"] = sum(delta > 0.0 for delta in deltas)
    return summary


def run_development_traversal_dynamics_suite() -> dict[str, Any]:
    specs = development_traversal_dynamics_worlds()
    worlds = tuple(run_traversal_dynamics_world(world) for world in specs)
    family_summaries = {
        family.value: _suite_summary(
            tuple(world for world in worlds if world.family == family.value)
        )
        for family in InterferenceFamily
    }
    grid_hash = traversal_dynamics_world_grid_hash(specs)
    overall = _suite_summary(worlds)
    payload = {
        "family_summaries": family_summaries,
        "overall_summary": overall,
        "world_grid_hash": grid_hash,
        "worlds": [
            {"world_id": world.world_id, "semantic_hash": world.semantic_hash}
            for world in worlds
        ],
    }
    return {
        "family_summaries": family_summaries,
        "overall_summary": overall,
        "probe_count": sum(len(world.probes) for world in worlds),
        "suite_hash": digest(payload),
        "world_count": len(worlds),
        "world_grid_hash": grid_hash,
        "worlds": [world.state_dict() for world in worlds],
    }

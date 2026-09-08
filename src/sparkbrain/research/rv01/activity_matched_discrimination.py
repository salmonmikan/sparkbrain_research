from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from sparkbrain.v06.foundation import digest

from .activity_matched_contract import (
    ActivityMatchedWorldSpec,
    activity_matched_world_grid_hash,
    development_activity_matched_worlds,
)
from .interference_contract import InterferenceFamily, InterferencePhase
from .interference_runner import _ordered_coverage, run_interference_world
from .resource_matched_reservoir import run_resource_matched_reservoir_world


@dataclass(frozen=True, slots=True)
class TraceMetrics:
    event_count: int
    distinct_unit_count: int
    ordered_match_count: int
    ordered_retention_fraction: float
    contamination_count: int
    contamination_rate: float
    ordered_match_yield: float
    exact_route_recovered: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProbeComparison:
    world_id: str
    family: str
    probe_route_id: str
    expected_units: tuple[int, ...]
    route_units: tuple[int, ...]
    field_raw_units: tuple[int, ...]
    reservoir_raw_units: tuple[int, ...]
    common_event_budget: int
    field_event_units: tuple[int, ...]
    reservoir_event_units: tuple[int, ...]
    common_distinct_budget: int
    field_breadth_units: tuple[int, ...]
    reservoir_breadth_units: tuple[int, ...]
    field_raw: TraceMetrics
    reservoir_raw: TraceMetrics
    field_event: TraceMetrics
    reservoir_event: TraceMetrics
    field_breadth: TraceMetrics
    reservoir_breadth: TraceMetrics
    field_first_hop_coverage: float
    reservoir_first_hop_coverage: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ActivityMatchedWorldResult:
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
    probes: tuple[ProbeComparison, ...]
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
            "probes": [row.state_dict() for row in self.probes],
            "resource_match_passed": self.resource_match_passed,
            "seed": self.seed,
            "semantic_hash": self.semantic_hash,
            "summary": self.summary,
            "world_id": self.world_id,
            "world_specification_hash": self.world_specification_hash,
        }


def _trace_metrics(
    expected: tuple[int, ...],
    route_units: tuple[int, ...],
    trace: tuple[int, ...],
) -> TraceMetrics:
    retention = _ordered_coverage(expected, trace)
    matches = int(round(retention * len(expected)))
    contamination = sum(unit not in route_units for unit in trace)
    events = len(trace)
    return TraceMetrics(
        event_count=events,
        distinct_unit_count=len(set(trace)),
        ordered_match_count=matches,
        ordered_retention_fraction=retention,
        contamination_count=contamination,
        contamination_rate=contamination / events if events else 0.0,
        ordered_match_yield=matches / events if events else 0.0,
        exact_route_recovered=(retention == 1.0 and contamination == 0),
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


def _summary(rows: Iterable[ProbeComparison]) -> dict[str, float | int]:
    probes = tuple(rows)
    if not probes:
        raise ValueError("summary requires probes")
    out: dict[str, float | int] = {"route_count": len(probes)}
    for view, field_name, reservoir_name in (
        ("raw", "field_raw", "reservoir_raw"),
        ("event_matched", "field_event", "reservoir_event"),
        ("breadth_matched", "field_breadth", "reservoir_breadth"),
    ):
        field = tuple(getattr(row, field_name) for row in probes)
        reservoir = tuple(getattr(row, reservoir_name) for row in probes)
        field_retention = sum(x.ordered_retention_fraction for x in field) / len(field)
        reservoir_retention = (
            sum(x.ordered_retention_fraction for x in reservoir) / len(reservoir)
        )
        field_events = sum(x.event_count for x in field)
        reservoir_events = sum(x.event_count for x in reservoir)
        field_contamination = sum(x.contamination_count for x in field)
        reservoir_contamination = sum(x.contamination_count for x in reservoir)
        field_matches = sum(x.ordered_match_count for x in field)
        reservoir_matches = sum(x.ordered_match_count for x in reservoir)
        out.update(
            {
                f"{view}_field_mean_ordered_retention": field_retention,
                f"{view}_reservoir_mean_ordered_retention": reservoir_retention,
                f"{view}_field_minus_reservoir_retention": (
                    field_retention - reservoir_retention
                ),
                f"{view}_field_exact_route_count": sum(
                    x.exact_route_recovered for x in field
                ),
                f"{view}_reservoir_exact_route_count": sum(
                    x.exact_route_recovered for x in reservoir
                ),
                f"{view}_field_contamination_count": field_contamination,
                f"{view}_reservoir_contamination_count": reservoir_contamination,
                f"{view}_field_event_count": field_events,
                f"{view}_reservoir_event_count": reservoir_events,
                f"{view}_field_contamination_rate": (
                    field_contamination / field_events if field_events else 0.0
                ),
                f"{view}_reservoir_contamination_rate": (
                    reservoir_contamination / reservoir_events
                    if reservoir_events
                    else 0.0
                ),
                f"{view}_field_ordered_match_yield": (
                    field_matches / field_events if field_events else 0.0
                ),
                f"{view}_reservoir_ordered_match_yield": (
                    reservoir_matches / reservoir_events if reservoir_events else 0.0
                ),
            }
        )
    out["raw_field_mean_first_hop_coverage"] = sum(
        row.field_first_hop_coverage for row in probes
    ) / len(probes)
    out["raw_reservoir_mean_first_hop_coverage"] = sum(
        row.reservoir_first_hop_coverage for row in probes
    ) / len(probes)
    return out


def _field_consistent(field_result: Any, comparator_result: Any) -> bool:
    phase = len(field_result.training_phases)
    rows = tuple(x for x in field_result.probes if x.training_phase_index == phase)
    assessment = comparator_result.assessment
    return all(
        (
            math.isclose(
                sum(x.ordered_retention_fraction for x in rows) / len(rows),
                assessment.field_mean_ordered_retention,
            ),
            sum(x.exact_route_recovered for x in rows)
            == assessment.field_exact_route_count,
            sum(x.contamination_count for x in rows)
            == assessment.field_contamination_count,
            math.isclose(
                sum(x.first_hop_coverage_fraction for x in rows) / len(rows),
                assessment.field_mean_first_hop_coverage,
            ),
        )
    )


def run_activity_matched_world(
    world: ActivityMatchedWorldSpec,
) -> ActivityMatchedWorldResult:
    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError("R01-13 held-out capability execution is not open")
    world.validate()
    field_result = run_interference_world(world)
    comparator = run_resource_matched_reservoir_world(world)
    consistent = _field_consistent(field_result, comparator)
    if not consistent:
        raise RuntimeError("Field rerun diverged from comparator-embedded Field run")

    phase = world.route_count
    field = {
        x.probe_route_id: x
        for x in field_result.probes
        if x.training_phase_index == phase
    }
    reservoir = {x.probe_route_id: x for x in comparator.probes}
    routes = {x.route_id: x for x in world.routes}
    probes: list[ProbeComparison] = []

    for route_id in world.probe_order:
        route = routes[route_id]
        field_probe = field[route_id]
        reservoir_probe = reservoir[route_id]
        field_raw = tuple(field_probe.generated_units)
        reservoir_raw = tuple(reservoir_probe.generated_units)
        event_budget = min(len(field_raw), len(reservoir_raw))
        distinct_budget = min(len(set(field_raw)), len(set(reservoir_raw)))
        field_event = field_raw[:event_budget]
        reservoir_event = reservoir_raw[:event_budget]
        field_breadth = _prefix_for_distinct_budget(field_raw, distinct_budget)
        reservoir_breadth = _prefix_for_distinct_budget(
            reservoir_raw,
            distinct_budget,
        )
        expected = tuple(route.units[1:])
        route_units = tuple(route.units)
        probes.append(
            ProbeComparison(
                world_id=world.world_id,
                family=world.family.value,
                probe_route_id=route_id,
                expected_units=expected,
                route_units=route_units,
                field_raw_units=field_raw,
                reservoir_raw_units=reservoir_raw,
                common_event_budget=event_budget,
                field_event_units=field_event,
                reservoir_event_units=reservoir_event,
                common_distinct_budget=distinct_budget,
                field_breadth_units=field_breadth,
                reservoir_breadth_units=reservoir_breadth,
                field_raw=_trace_metrics(expected, route_units, field_raw),
                reservoir_raw=_trace_metrics(expected, route_units, reservoir_raw),
                field_event=_trace_metrics(expected, route_units, field_event),
                reservoir_event=_trace_metrics(expected, route_units, reservoir_event),
                field_breadth=_trace_metrics(expected, route_units, field_breadth),
                reservoir_breadth=_trace_metrics(
                    expected,
                    route_units,
                    reservoir_breadth,
                ),
                field_first_hop_coverage=field_probe.first_hop_coverage_fraction,
                reservoir_first_hop_coverage=(
                    reservoir_probe.first_hop_coverage_fraction
                ),
            )
        )

    probe_rows = tuple(probes)
    summary = _summary(probe_rows)
    payload = {
        "comparator_semantic_hash": comparator.semantic_hash,
        "field_semantic_hash": field_result.semantic_hash,
        "probes": [row.state_dict() for row in probe_rows],
        "summary": summary,
        "world": world.state_dict(),
    }
    return ActivityMatchedWorldResult(
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
    worlds: tuple[ActivityMatchedWorldResult, ...],
) -> dict[str, float | int]:
    summary = _summary(tuple(row for world in worlds for row in world.probes))
    summary["world_count"] = len(worlds)
    for view in ("raw", "event_matched", "breadth_matched"):
        key = f"{view}_field_minus_reservoir_retention"
        summary[f"{view}_field_positive_world_count"] = sum(
            float(world.summary[key]) > 0.0 for world in worlds
        )
        summary[f"{view}_field_tied_world_count"] = sum(
            math.isclose(float(world.summary[key]), 0.0) for world in worlds
        )
        summary[f"{view}_field_negative_world_count"] = sum(
            float(world.summary[key]) < 0.0 for world in worlds
        )
    return summary


def run_development_activity_matched_suite() -> dict[str, Any]:
    specs = development_activity_matched_worlds()
    worlds = tuple(run_activity_matched_world(world) for world in specs)
    family_summaries = {
        family.value: _suite_summary(
            tuple(world for world in worlds if world.family == family.value)
        )
        for family in InterferenceFamily
    }
    grid_hash = activity_matched_world_grid_hash(specs)
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

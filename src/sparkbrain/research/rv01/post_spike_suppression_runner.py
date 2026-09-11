from __future__ import annotations

from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v06.foundation import digest

from .interference_contract import InterferenceFamily, InterferencePhase, RouteExposure
from .interference_runner import (
    _INITIAL_WEIGHT,
    _MAXIMUM_PROBE_SPIKES,
    _directed_edges,
    _ordered_coverage,
    _route_map,
    _train_route,
)
from .physical_learner_bridge import build_physical_field, connection_state_hash
from .post_spike_suppression_contract import (
    PostSpikeSuppressionWorldSpec,
    R01_15_PROTOCOL_ID,
    development_post_spike_suppression_worlds,
    post_spike_suppression_world_grid_hash,
)
from .resource_matched_reservoir import run_resource_matched_reservoir_world
from sparkbrain.research.rv01_post_spike_suppression import (
    PostSpikeSuppressionField,
    PostSpikeSuppressionMode,
)

_FIELD_MODES: tuple[PostSpikeSuppressionMode, ...] = (
    "intact",
    "adaptation_zero",
    "refractory_zero",
    "both_zero",
)


def _traversal_metrics(trace: tuple[int, ...]) -> dict[str, Any]:
    seen: set[int] = set()
    first_visit_positions: list[int] = []
    for index, unit_id in enumerate(trace, start=1):
        if unit_id not in seen:
            seen.add(unit_id)
            first_visit_positions.append(index)
    event_count = len(trace)
    distinct_count = len(seen)
    revisit_count = event_count - distinct_count
    return {
        "event_count": event_count,
        "distinct_unit_count": distinct_count,
        "revisit_count": revisit_count,
        "revisit_rate": revisit_count / event_count if event_count else 0.0,
        "new_state_yield": distinct_count / event_count if event_count else 0.0,
        "first_visit_positions": first_visit_positions,
    }


def _prefix_to_distinct_budget(
    trace: tuple[int, ...],
    budget: int,
) -> tuple[int, ...] | None:
    if budget < 0:
        raise ValueError("distinct budget must be non-negative")
    if budget == 0:
        return ()
    seen: set[int] = set()
    prefix: list[int] = []
    for unit_id in trace:
        prefix.append(unit_id)
        seen.add(unit_id)
        if len(seen) == budget:
            return tuple(prefix)
    return None


def _train_shared_field(world: PostSpikeSuppressionWorldSpec) -> Any:
    """Train one ordinary Field checkpoint using the accepted RV01 learner path."""

    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError("R01-15 held-out capability execution is sealed")
    world.validate()
    field = build_physical_field(
        unit_count=world.unit_count,
        directed_edges=_directed_edges(world),
        threshold=world.threshold,
        initial_weight=_INITIAL_WEIGHT,
        initial_delay_ms=world.lag_ms,
    )
    route_by_id = _route_map(world)
    for phase_index, route_id in enumerate(world.training_order, start=1):
        _train_route(
            world,
            field,
            route_by_id[route_id],
            phase_index=phase_index,
        )
    return field


def _queue_size(field: PostSpikeSuppressionField) -> int:
    return len(field.state_dict().get("queue", ()))


def _run_field_arm(
    world: PostSpikeSuppressionWorldSpec,
    checkpoint: dict[str, Any],
    route: RouteExposure,
    *,
    mode: PostSpikeSuppressionMode,
) -> dict[str, Any]:
    field = PostSpikeSuppressionField.from_state_dict(checkpoint, mode=mode)
    checkpoint_hash = digest(checkpoint)
    if digest(field.state_dict()) != checkpoint_hash:
        raise RuntimeError("R01-15 arm did not restore from the shared checkpoint")
    connection_hash_before = connection_state_hash(field)

    cue_time = 100.0
    field.schedule_arrival(
        SynapticArrival(
            time_ms=cue_time,
            target_id=route.units[0],
            current=world.cue_magnitude,
            source_id=None,
            pulse_id=f"r01-15:{world.world_id}:{route.route_id}:{mode}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    horizon = cue_time + world.lag_ms * (len(route.units) + 3)
    slice_ms = max(0.25, world.lag_ms / 4.0)
    current = cue_time
    spikes = []
    maximum_queue_size = _queue_size(field)
    halt_reason = "horizon_reached"
    while current < horizon:
        target = min(horizon, current + slice_ms)
        spikes.extend(field.run_until(target))
        current = target
        maximum_queue_size = max(maximum_queue_size, _queue_size(field))
        if len(spikes) > _MAXIMUM_PROBE_SPIKES:
            halt_reason = "spike_budget_exceeded"
            break
        if _queue_size(field) == 0 and current > cue_time:
            halt_reason = "queue_drained"
            break

    later = tuple(row for row in spikes if row.time_ms > cue_time)
    trace = tuple(row.unit_id for row in later)
    expected = route.units[1:]
    connection_hash_after = connection_state_hash(field)
    if connection_hash_after != connection_hash_before:
        raise RuntimeError("R01-15 probe changed learned connection state")

    allowed_fields = {
        "intact": set(),
        "adaptation_zero": {"adaptation"},
        "refractory_zero": {"refractory_until_ms"},
        "both_zero": {"adaptation", "refractory_until_ms"},
    }[mode]
    observed_fields = {str(row["field"]) for row in field.intervention_records}
    if not observed_fields.issubset(allowed_fields):
        raise RuntimeError("R01-15 intervention escaped its preregistered field scope")
    if mode != "intact" and field.intervention_records and observed_fields != allowed_fields:
        raise RuntimeError("R01-15 intervention record is incomplete for emitted spikes")

    coverage = _ordered_coverage(expected, trace)
    contamination = sum(unit_id not in route.units for unit_id in trace)
    return {
        "mode": mode,
        "checkpoint_hash": checkpoint_hash,
        "connection_hash_before": connection_hash_before,
        "connection_hash_after": connection_hash_after,
        "cue_unit_id": route.units[0],
        "generated_units": list(trace),
        "generated_times_ms": [float(row.time_ms) for row in later],
        "raw_metrics": _traversal_metrics(trace),
        "ordered_retention_fraction": coverage,
        "exact_route_recovered": coverage == 1.0 and contamination == 0,
        "contamination_count": contamination,
        "intervention_records": [dict(row) for row in field.intervention_records],
        "maximum_queue_size": maximum_queue_size,
        "final_queue_size": _queue_size(field),
        "halt_reason": halt_reason,
    }


def run_post_spike_suppression_world(
    world: PostSpikeSuppressionWorldSpec,
) -> dict[str, Any]:
    """Run one fixed exposed-development R01-15 world.

    All four Field arms restore from one post-training checkpoint. The reservoir is
    the unchanged accepted RV01 external reference and is generated once per world.
    """

    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError("R01-15 held-out capability execution is sealed")
    world.validate()

    trained = _train_shared_field(world)
    checkpoint = trained.state_dict()
    checkpoint_hash = digest(checkpoint)
    comparator = run_resource_matched_reservoir_world(world)
    if not comparator.resources.resource_match_passed:
        raise RuntimeError("R01-15 resource-matched reservoir contract failed")
    reservoir_by_route = {row.probe_route_id: row for row in comparator.probes}
    route_by_id = _route_map(world)

    probes: list[dict[str, Any]] = []
    for route_id in world.probe_order:
        route = route_by_id[route_id]
        arms = {
            mode: _run_field_arm(world, checkpoint, route, mode=mode)
            for mode in _FIELD_MODES
        }
        if {row["checkpoint_hash"] for row in arms.values()} != {checkpoint_hash}:
            raise RuntimeError("R01-15 arm checkpoint hashes diverged")
        if len({row["connection_hash_before"] for row in arms.values()}) != 1:
            raise RuntimeError("R01-15 arms did not share learned connection state")

        reservoir = reservoir_by_route[route_id]
        intact_trace = tuple(arms["intact"]["generated_units"])
        reservoir_trace = tuple(reservoir.generated_units)
        common_breadth = min(len(set(intact_trace)), len(set(reservoir_trace)))
        for row in arms.values():
            trace = tuple(row["generated_units"])
            prefix = _prefix_to_distinct_budget(trace, common_breadth)
            row["common_breadth_budget"] = common_breadth
            row["common_breadth_reached"] = prefix is not None
            row["common_breadth_metrics"] = (
                _traversal_metrics(prefix) if prefix is not None else None
            )
            row["common_breadth_units"] = list(prefix) if prefix is not None else None

        reservoir_prefix = _prefix_to_distinct_budget(reservoir_trace, common_breadth)
        if reservoir_prefix is None:
            raise RuntimeError("reservoir failed its own registered common breadth")
        probes.append(
            {
                "probe_route_id": route_id,
                "expected_units": list(route.units[1:]),
                "common_breadth_budget": common_breadth,
                "field_arms": [arms[mode] for mode in _FIELD_MODES],
                "reservoir": {
                    "generated_units": list(reservoir.generated_units),
                    "common_breadth_units": list(reservoir_prefix),
                    "common_breadth_metrics": _traversal_metrics(reservoir_prefix),
                    "ordered_retention_fraction": reservoir.ordered_retention_fraction,
                    "exact_route_recovered": reservoir.exact_route_recovered,
                    "contamination_count": reservoir.contamination_count,
                    "halt_reason": reservoir.halt_reason,
                },
            }
        )

    payload = {
        "protocol_id": R01_15_PROTOCOL_ID,
        "phase": "development",
        "held_out_capability_executed": False,
        "world": world.state_dict(),
        "world_specification_hash": world.specification_hash(),
        "checkpoint_hash": checkpoint_hash,
        "resource_match": comparator.resources.state_dict(),
        "probes": probes,
    }
    payload["semantic_hash"] = digest(payload)
    return payload


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _suite_summary(worlds: list[dict[str, Any]]) -> dict[str, Any]:
    mode_events: dict[str, list[float]] = {mode: [] for mode in _FIELD_MODES}
    mode_revisits: dict[str, list[float]] = {mode: [] for mode in _FIELD_MODES}
    mode_exact: dict[str, int] = {mode: 0 for mode in _FIELD_MODES}
    mode_unreached: dict[str, int] = {mode: 0 for mode in _FIELD_MODES}
    intact_vs_reservoir_event_delta: list[float] = []

    for world in worlds:
        for probe in world["probes"]:
            reservoir_metrics = probe["reservoir"]["common_breadth_metrics"]
            for arm in probe["field_arms"]:
                mode = arm["mode"]
                mode_exact[mode] += int(arm["exact_route_recovered"])
                metrics = arm["common_breadth_metrics"]
                if metrics is None:
                    mode_unreached[mode] += 1
                    continue
                mode_events[mode].append(float(metrics["event_count"]))
                mode_revisits[mode].append(float(metrics["revisit_count"]))
                if mode == "intact":
                    intact_vs_reservoir_event_delta.append(
                        float(metrics["event_count"])
                        - float(reservoir_metrics["event_count"])
                    )

    return {
        "mean_common_breadth_event_count": {
            mode: _mean(mode_events[mode]) for mode in _FIELD_MODES
        },
        "mean_common_breadth_revisit_count": {
            mode: _mean(mode_revisits[mode]) for mode in _FIELD_MODES
        },
        "exact_route_recovered_count": mode_exact,
        "common_breadth_unreached_count": mode_unreached,
        "intact_minus_reservoir_mean_common_breadth_events": _mean(
            intact_vs_reservoir_event_delta
        ),
    }


def run_development_post_spike_suppression_suite() -> dict[str, Any]:
    specs = development_post_spike_suppression_worlds()
    worlds = [run_post_spike_suppression_world(world) for world in specs]
    family_summaries = {
        family.value: _suite_summary(
            [row for row in worlds if row["world"]["family"] == family.value]
        )
        for family in InterferenceFamily
    }
    payload = {
        "protocol_id": R01_15_PROTOCOL_ID,
        "phase": "development",
        "held_out_capability_executed": False,
        "world_grid_hash": post_spike_suppression_world_grid_hash(specs),
        "world_count": len(worlds),
        "probe_count": sum(len(world["probes"]) for world in worlds),
        "family_summaries": family_summaries,
        "overall_summary": _suite_summary(worlds),
        "worlds": worlds,
    }
    payload["suite_hash"] = digest(payload)
    return payload


__all__ = [
    "run_development_post_spike_suppression_suite",
    "run_post_spike_suppression_world",
]

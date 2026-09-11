"""Prospective RV02-RD004 relative-clock probe implementation.

RD003 attempt-001 is consumed and remains untouched. This module implements only
the new RD004 probe-time contract: finish the inherited eligibility tail, apply a
fixed no-input washout, clone one shared snapshot, and anchor the cue to that
snapshot's current Field clock. It contains no RD004 matrix runner.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import asdict
from typing import Any

from sparkbrain.research.rv02_boundary_recruitment import (
    PartialObservedField,
    PartialReferenceField,
)
from sparkbrain.research.rv02_recruitment import PORTS, connection_hash
from sparkbrain.research.rv02_scale import digest, project_behavior
from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

RD004_ELIGIBILITY_TAIL_MS = 6.5
RD004_WASHOUT_MS = 100.0
RD004_HORIZON_MS = 40.0


def prepare_rd004_probe_snapshot(
    field: TemporalExcitableField,
    *,
    eligibility_tail_ms: float = RD004_ELIGIBILITY_TAIL_MS,
    washout_ms: float = RD004_WASHOUT_MS,
) -> dict[str, Any]:
    """Advance a clone through the fixed tail/washout and return one shared snapshot."""

    if eligibility_tail_ms != RD004_ELIGIBILITY_TAIL_MS:
        raise ValueError("RD004 eligibility tail is fixed at 6.5 ms")
    if washout_ms != RD004_WASHOUT_MS:
        raise ValueError("RD004 washout is fixed at 100 ms")

    clone = TemporalExcitableField.from_state_dict(field.state_dict())
    source_clock = clone.current_time_ms
    tail_end = source_clock + eligibility_tail_ms
    clone.run_until(tail_end)
    washout_end = tail_end + washout_ms
    clone.run_until(washout_end)
    state = clone.state_dict()
    return {
        "source_clock_ms": source_clock,
        "eligibility_tail_ms": eligibility_tail_ms,
        "tail_end_ms": tail_end,
        "washout_ms": washout_ms,
        "cue_time_ms": washout_end,
        "snapshot_state": state,
        "snapshot_state_hash": clone.state_hash(),
        "connection_hash": connection_hash(clone),
    }


def score_rd004_probe(
    spikes: list[dict[str, Any]],
    route: tuple[int, ...],
    unit_count: int,
    *,
    cue_time_ms: float,
) -> dict[str, Any]:
    """Score only post-cue continuation; the forced cue is never a symbol."""

    generated = tuple(
        int(row["unit_id"])
        for row in spikes
        if float(row["time_ms"]) > cue_time_ms
    )
    result = project_behavior(generated, PORTS, route, unit_count)
    visible = tuple(unit_id for unit_id in generated if unit_id in PORTS)
    counts = Counter(visible)
    result["missing_expected_count"] = len(route[1:]) - round(
        result["ordered_retention"] * len(route[1:])
    )
    expected = Counter(route[1:])
    result["excess_route_event_count"] = sum(
        max(0, counts[unit_id] - expected[unit_id]) for unit_id in set(route)
    )
    result["repeated_expected_unit_spikes"] = sum(
        max(0, counts[unit_id] - 1) for unit_id in set(route[1:])
    )
    result["cue_recurrence_spikes"] = counts[route[0]]
    return result


def run_rd004_probe(
    snapshot_state: dict[str, Any],
    cue_unit: int,
    *,
    cut_hidden_boundary: bool = False,
    horizon_ms: float = RD004_HORIZON_MS,
    ports: tuple[int, ...] = PORTS,
) -> dict[str, Any]:
    """Run one natural/cut probe from the already shared post-washout snapshot."""

    if horizon_ms != RD004_HORIZON_MS:
        raise ValueError("RD004 probe horizon is fixed at 40 ms")
    if ports != PORTS:
        raise ValueError("RD004 ports are fixed to the RV02 visible inventory")

    base = TemporalExcitableField.from_state_dict(snapshot_state)
    if type(cue_unit) is not int or cue_unit not in base.units:
        raise ValueError("invalid RD004 cue unit")
    cue_time = base.current_time_ms
    shared_snapshot_hash = base.state_hash()
    shared_connection_hash = connection_hash(base)

    observed = PartialObservedField.from_state_dict(snapshot_state)
    interventions: list[dict[str, Any]] = []
    if cut_hidden_boundary:
        for key, edge in observed.connections.items():
            if (edge.source_id in ports) != (edge.target_id in ports):
                interventions.append(
                    {"edge": list(key), "old_weight": edge.weight}
                )
                edge.weight = 0.0
    reference = PartialReferenceField.from_state_dict(observed.state_dict())
    probe_connection_hash = connection_hash(observed)

    cue = SynapticArrival(
        time_ms=cue_time,
        target_id=cue_unit,
        current=1.0,
        source_id=None,
        pulse_id="rv02-rd004-cue",
        novelty=0.0,
        prediction_error=0.0,
    )
    observed.schedule_arrival(cue)
    reference.schedule_arrival(cue)

    errors: list[str | None] = []
    for runner in (observed, reference):
        try:
            runner.run_until(cue_time + horizon_ms)
            errors.append(None)
        except RuntimeError as exc:
            if str(exc) not in (
                "max_events_per_run exceeded",
                "max_spikes_per_run exceeded",
            ):
                raise
            errors.append(str(exc))
    if errors[0] != errors[1]:
        raise RuntimeError("RD004 observer/reference native-guard mismatch")

    if errors[0] is not None:
        return {
            "status": "incomplete_native_guard_probe",
            "error": errors[0],
            "metrics_available": False,
            "cue_time_ms": cue_time,
            "horizon_ms": horizon_ms,
            "cut_hidden_boundary": cut_hidden_boundary,
            "shared_snapshot_hash": shared_snapshot_hash,
            "shared_connection_hash": shared_connection_hash,
            "probe_connection_hash_before": probe_connection_hash,
            "probe_connection_hash_after": connection_hash(observed),
            "boundary_interventions": interventions,
            "actual_arrivals": observed.total_arrivals,
            "actual_spikes": observed.total_spikes,
            "final_clock_ms": observed.current_time_ms,
        }

    spikes = tuple(observed.delivered_objects)
    reference_spikes = tuple(reference.delivered_objects)
    observer_equivalence = (
        observed.state_hash() == reference.state_hash()
        and spikes == reference_spikes
    )
    if not observer_equivalence or connection_hash(observed) != probe_connection_hash:
        raise RuntimeError("RD004 observer noninterference/probe nonlearning failure")

    hidden = sorted(set(observed.units) - set(ports))
    by_unit: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in observed.arrival_observations:
        by_unit[int(row["target_id"])].append(row)
    hidden_rows: list[dict[str, Any]] = []
    for unit_id in hidden:
        rows = by_unit[unit_id]
        unit = observed.units[unit_id]
        projected = unit.potential * math.exp(
            -(observed.current_time_ms - unit.last_update_ms)
            / observed.config.membrane_tau_ms
        )
        hidden_rows.append(
            {
                "unit_id": unit_id,
                "arrival_count": sum(row["arrival_count"] for row in rows),
                "positive_current_arrival_count": sum(
                    row["positive_current_arrival_count"] for row in rows
                ),
                "positive_current": sum(row["positive_current"] for row in rows),
                "negative_current": sum(row["negative_current"] for row in rows),
                "integrated_net_current": sum(
                    row["integrated_net_current"] for row in rows
                ),
                "refractory_suppressed_net_positive": sum(
                    row["refractory_suppressed_net_positive"] for row in rows
                ),
                "maximum_potential_threshold_ratio": max(
                    (
                        row["potential_before_reset"] / row["threshold"]
                        for row in rows
                    ),
                    default=None,
                ),
                "spike_count": sum(row["spiked"] for row in rows),
                "stored_final_potential": unit.potential,
                "last_update_ms": unit.last_update_ms,
                "projected_final_potential": projected,
            }
        )

    visible_state = [asdict(observed.units[unit_id]) for unit_id in ports]
    spike_rows = [asdict(spike) for spike in spikes]
    return {
        "status": "complete",
        "metrics_available": True,
        "cue_unit": cue_unit,
        "cue_time_ms": cue_time,
        "horizon_ms": horizon_ms,
        "cut_hidden_boundary": cut_hidden_boundary,
        "shared_snapshot_hash": shared_snapshot_hash,
        "shared_connection_hash": shared_connection_hash,
        "boundary_interventions": interventions,
        "probe_connection_hash_before": probe_connection_hash,
        "probe_connection_hash_after": connection_hash(observed),
        "observer_equivalence": observer_equivalence,
        "observed_state_hash": observed.state_hash(),
        "reference_state_hash": reference.state_hash(),
        "arrival_observations": observed.arrival_observations,
        "spikes": spike_rows,
        "hidden_units": hidden_rows,
        "visible_trace": [
            (spike.time_ms, spike.unit_id)
            for spike in spikes
            if spike.time_ms > cue_time and spike.unit_id in ports
        ],
        "visible_final_state": visible_state,
        "visible_final_state_hash": digest(visible_state),
        "final_queue_size": len(observed.state_dict()["queue"]),
        "queue_drained": not observed.state_dict()["queue"],
        "actual_arrivals": observed.total_arrivals,
        "actual_spikes": observed.total_spikes,
        "final_clock_ms": observed.current_time_ms,
    }


__all__ = [
    "RD004_ELIGIBILITY_TAIL_MS",
    "RD004_HORIZON_MS",
    "RD004_WASHOUT_MS",
    "prepare_rd004_probe_snapshot",
    "run_rd004_probe",
    "score_rd004_probe",
]

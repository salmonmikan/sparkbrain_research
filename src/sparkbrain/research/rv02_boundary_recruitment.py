"""RD002 fixed post-training boundary-input gain diagnosis; development only."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from typing import Any

from sparkbrain.research.rv01.physical_learner_bridge import build_physical_field, runtime_pulse
from sparkbrain.research.rv01.physical_plasticity import ExternalOnlyPhysicalPlasticity
from sparkbrain.research.rv02_recruitment import PORTS, ArrivalObservedField, connection_hash
from sparkbrain.research.rv02_scale import ScaleStudyConfig, audit_scale, digest, project_behavior
from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

GAINS = (1.0, 2.0, 4.0)


def apply_boundary_gain(
    field: TemporalExcitableField, gain: float
) -> tuple[TemporalExcitableField, list[dict[str, Any]]]:
    """Clone trained state and multiply only visible-to-hidden weights."""
    if type(gain) not in (int, float) or gain not in GAINS:
        raise ValueError("RD002 gain must be one of 1, 2, 4")
    clone = TemporalExcitableField.from_state_dict(field.state_dict())
    changes = []
    for key, edge in sorted(clone.connections.items()):
        if edge.source_id in PORTS and edge.target_id not in PORTS:
            old = edge.weight
            edge.weight *= gain
            if not math.isfinite(edge.weight):
                raise ValueError("nonfinite gained weight")
            changes.append({"edge": list(key), "old_weight": old, "new_weight": edge.weight})
    return clone, changes


def score_probe(
    spikes: list[dict[str, Any]], route: tuple[int, ...], unit_count: int
) -> dict[str, Any]:
    """Score continuation only; forced cue and hidden spikes are not symbols."""
    generated = tuple(s["unit_id"] for s in spikes if s["time_ms"] > 100.0)
    result = project_behavior(generated, PORTS, route, unit_count)
    visible = tuple(u for u in generated if u in PORTS)
    counts = Counter(visible)
    result["missing_expected_count"] = len(route[1:]) - round(
        result["ordered_retention"] * len(route[1:])
    )
    expected = Counter(route[1:])
    result["excess_route_event_count"] = sum(max(0, counts[u] - expected[u]) for u in set(route))
    result["repeated_expected_unit_spikes"] = sum(max(0, counts[u] - 1) for u in set(route[1:]))
    result["cue_recurrence_spikes"] = counts[route[0]]
    return result


class PartialReferenceField(TemporalExcitableField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.delivered_objects: list = []

    def _deliver_group(self, time_ms: float, arrivals: list[SynapticArrival]) -> list:
        spikes = super()._deliver_group(time_ms, arrivals)
        self.delivered_objects.extend(spikes)
        return spikes


class PartialObservedField(ArrivalObservedField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.delivered_objects: list = []
        self.delivered_spikes: list = []

    def _deliver_group(self, time_ms: float, arrivals: list[SynapticArrival]) -> list:
        spikes = super()._deliver_group(time_ms, arrivals)
        self.delivered_objects.extend(spikes)
        self.delivered_spikes.extend(asdict(s) for s in spikes)
        return spikes


def run_probe(
    field: TemporalExcitableField,
    cue_unit: int,
    *,
    horizon_ms: float = 40.0,
    cut_hidden_boundary: bool = False,
    ports: tuple[int, ...] = PORTS,
) -> dict[str, Any]:
    if horizon_ms != 40.0:
        raise ValueError("RD002 permits only the predeclared 40ms horizon")
    if ports != PORTS or type(cue_unit) is not int or cue_unit not in field.units:
        raise ValueError("invalid probe ports/cue")
    initial_hash = connection_hash(field)
    observed = PartialObservedField.from_state_dict(field.state_dict())
    changed = []
    if cut_hidden_boundary:
        for key, edge in observed.connections.items():
            if (edge.source_id in ports) != (edge.target_id in ports):
                changed.append({"edge": key, "old_weight": edge.weight})
                edge.weight = 0.0
    reference = PartialReferenceField.from_state_dict(observed.state_dict())
    probe_connection_hash = connection_hash(observed)
    cue = SynapticArrival(
        time_ms=100.0,
        target_id=cue_unit,
        current=1.0,
        source_id=None,
        pulse_id="rv02-rd001-cue",
        novelty=0.0,
        prediction_error=0.0,
    )
    observed.schedule_arrival(cue)
    reference.schedule_arrival(cue)
    # One native bounded call covers the whole horizon, not separately reset bin budgets.
    errors = []
    for runner in (observed, reference):
        try:
            runner.run_until(100.0 + horizon_ms)
            errors.append(None)
        except RuntimeError as exc:
            if str(exc) not in ("max_events_per_run exceeded", "max_spikes_per_run exceeded"):
                raise
            errors.append(str(exc))
    if (
        errors[0] != errors[1]
        or observed.state_hash() != reference.state_hash()
        or observed.delivered_objects != reference.delivered_objects
        or connection_hash(observed) != probe_connection_hash
    ):
        raise RuntimeError("observer noninterference/probe nonlearning failure")
    if errors[0] is not None or observed.total_arrivals >= 4096 or observed.total_spikes >= 512:
        return {
            "status": "incomplete_native_guard",
            "error": errors[0] or "native limit reached",
            "metrics_available": False,
            "actual_arrivals": observed.total_arrivals,
            "actual_spikes": observed.total_spikes,
            "final_clock_ms": observed.current_time_ms,
            "final_queue_size": len(observed.state_dict()["queue"]),
            "partial_state": observed.state_dict(),
            "spikes": observed.delivered_spikes,
            "arrival_observations": observed.arrival_observations,
            "reference_error": errors[1],
            "reference_spikes": [asdict(s) for s in reference.delivered_objects],
            "probe_connection_hash_before": probe_connection_hash,
            "probe_connection_hash_after": connection_hash(observed),
            "observed_state_hash": observed.state_hash(),
            "reference_state_hash": reference.state_hash(),
            "observer_equivalence": observed.state_hash() == reference.state_hash(),
        }
    spikes = tuple(observed.delivered_objects)
    # Reconstruct the reference generated events captured by its passive wrapper.
    reference_spikes = tuple(reference.delivered_objects)
    observer_equivalence = (
        observed.state_hash() == reference.state_hash() and spikes == reference_spikes
    )
    if not observer_equivalence or connection_hash(observed) != probe_connection_hash:
        raise RuntimeError("observer noninterference/probe nonlearning failure")
    hidden = sorted(set(field.units) - set(ports))
    by_unit: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in observed.arrival_observations:
        by_unit[row["target_id"]].append(row)
    hidden_rows = []
    for unit_id in hidden:
        rows, unit = by_unit[unit_id], observed.units[unit_id]
        final_projected = unit.potential * math.exp(
            -(observed.current_time_ms - unit.last_update_ms) / observed.config.membrane_tau_ms
        )
        hidden_rows.append(
            {
                "unit_id": unit_id,
                "arrival_count": sum(r["arrival_count"] for r in rows),
                "positive_current_arrival_count": sum(
                    r["positive_current_arrival_count"] for r in rows
                ),
                "positive_current": sum(r["positive_current"] for r in rows),
                "negative_current": sum(r["negative_current"] for r in rows),
                "integrated_net_current": sum(r["integrated_net_current"] for r in rows),
                "refractory_suppressed_net_positive": sum(
                    r["refractory_suppressed_net_positive"] for r in rows
                ),
                "maximum_potential_threshold_ratio": max(
                    (r["potential_before_reset"] / r["threshold"] for r in rows), default=None
                ),
                "spike_count": sum(r["spiked"] for r in rows),
                "stored_final_potential": unit.potential,
                "last_update_ms": unit.last_update_ms,
                "projected_final_potential": final_projected,
            }
        )
    visible_state = [asdict(observed.units[unit_id]) for unit_id in ports]
    return {
        "cue_unit": cue_unit,
        "horizon_ms": horizon_ms,
        "cut_hidden_boundary": cut_hidden_boundary,
        "boundary_interventions": changed,
        "initial_connection_hash": initial_hash,
        "probe_connection_hash_before": probe_connection_hash,
        "probe_connection_hash_after": connection_hash(observed),
        "observer_equivalence": observer_equivalence,
        "observed_state_hash": observed.state_hash(),
        "reference_state_hash": reference.state_hash(),
        "arrival_observations": observed.arrival_observations,
        "spikes": [asdict(spike) for spike in spikes],
        "hidden_units": hidden_rows,
        "visible_trace": [
            (spike.time_ms, spike.unit_id) for spike in spikes if spike.unit_id in ports
        ],
        "visible_final_state": visible_state,
        "visible_final_state_hash": digest(visible_state),
        "final_queue_size": len(observed.state_dict()["queue"]),
        "queue_drained": not observed.state_dict()["queue"],
        "actual_arrivals": observed.total_arrivals,
        "actual_spikes": observed.total_spikes,
        "final_clock_ms": observed.current_time_ms,
    }


def run_boundary_cell(
    config: ScaleStudyConfig, world: dict[str, Any], scale: int
) -> dict[str, Any]:
    if config != ScaleStudyConfig():
        raise ValueError("RD002 baseline configuration is fixed")
    audit = audit_scale(config, world, scale)
    field = build_physical_field(
        unit_count=audit["unit_count"],
        directed_edges=audit["edges"],
        threshold=0.5,
        initial_weight=0.05,
        initial_delay_ms=5.0,
    )
    field.receptor_ids = PORTS
    field.config = replace(field.config, max_events_per_run=4096, max_spikes_per_run=512)
    before = {key: asdict(edge) for key, edge in field.connections.items()}
    training_rows = []
    for route_index, (route, exposures) in enumerate(
        zip(world["routes"], world["exposures"], strict=True)
    ):
        for episode in range(exposures):
            learner = ExternalOnlyPhysicalPlasticity(field)
            for index, unit in enumerate(route):
                updates = learner.observe_external(
                    runtime_pulse(
                        event_id=f"{world['world_id']}:{route_index}:{episode}:{index}",
                        time_ms=float(route_index * 10000 + episode * 100 + index * 5),
                        unit_id=unit,
                        magnitude=1.0,
                    )
                )
                training_rows.append(
                    {
                        "route_index": route_index,
                        "episode": episode,
                        "position": index,
                        "external_unit": unit,
                        "external_trace_units": sorted(
                            map(int, learner.state_dict()["unit_traces"])
                        ),
                        "updates": [asdict(update) for update in updates],
                    }
                )
    changed_hidden = [
        list(key)
        for key, edge in field.connections.items()
        if (key[0] not in PORTS or key[1] not in PORTS) and before[key] != asdict(edge)
    ]
    probes = []
    for gain in GAINS:
        gained, interventions = apply_boundary_gain(field, gain)
        for index, route in enumerate(world["routes"]):
            pair = {"gain": gain, "route_index": index, "gain_interventions": interventions}
            for name, cut in (("natural", False), ("boundary_zero", True)):
                try:
                    probe = run_probe(gained, route[0], cut_hidden_boundary=cut)
                    if probe.get("status") != "incomplete_native_guard":
                        probe["behavior"] = score_probe(probe["spikes"], route, audit["unit_count"])
                        probe["status"] = "complete"
                    pair[name] = probe
                except RuntimeError as exc:
                    if str(exc) not in (
                        "max_events_per_run exceeded",
                        "max_spikes_per_run exceeded",
                    ):
                        raise
                    pair[name] = {
                        "status": "incomplete_native_guard",
                        "error": str(exc),
                        "metrics_available": False,
                    }
            complete = all(pair[k]["status"] == "complete" for k in ("natural", "boundary_zero"))
            pair["complete"] = complete
            pair["boundary_visible_trace_equal"] = (
                pair["natural"]["visible_trace"] == pair["boundary_zero"]["visible_trace"]
                if complete
                else None
            )
            pair["boundary_visible_final_state_equal"] = (
                pair["natural"]["visible_final_state_hash"]
                == pair["boundary_zero"]["visible_final_state_hash"]
                if complete
                else None
            )
            probes.append(pair)
    return {
        "diagnosis": "rv02-rd002-development",
        "audit": audit,
        "training_rows": training_rows,
        "changed_hidden_edges": changed_hidden,
        "hidden_external_trace_count": sum(
            u not in PORTS for row in training_rows for u in row["external_trace_units"]
        ),
        "trained_state": field.state_dict(),
        "trained_connection_hash": connection_hash(field),
        "route_probes": probes,
        "complete": all(p["complete"] for p in probes),
        "scientific_status": "not_evaluated_development_diagnosis",
    }

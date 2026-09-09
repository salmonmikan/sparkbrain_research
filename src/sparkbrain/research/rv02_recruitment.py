"""Passive recruitment diagnosis of the fixed RV02 development Field."""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import asdict, replace
from typing import Any

from sparkbrain.research.rv01.physical_learner_bridge import (
    build_physical_field,
    runtime_pulse,
)
from sparkbrain.research.rv01.physical_plasticity import ExternalOnlyPhysicalPlasticity
from sparkbrain.research.rv02_scale import ScaleStudyConfig, audit_scale, digest
from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField

PORTS = tuple(range(36))


def connection_hash(field: TemporalExcitableField) -> str:
    return digest([asdict(edge) for _, edge in sorted(field.connections.items())])


class ArrivalObservedField(TemporalExcitableField):
    """Observe complete event groups without mutating their delivery semantics."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.arrival_observations: list[dict[str, Any]] = []

    def _deliver_group(self, time_ms: float, arrivals: list[SynapticArrival]) -> list:
        grouped: dict[int, list[SynapticArrival]] = defaultdict(list)
        for arrival in arrivals:
            grouped[arrival.target_id].append(arrival)
        pending = []
        for target, rows in sorted(grouped.items()):
            unit = self.units[target]
            elapsed = time_ms - unit.last_update_ms
            potential = unit.potential * math.exp(-elapsed / self.config.membrane_tau_ms)
            adaptation = unit.adaptation * math.exp(-elapsed / self.config.adaptation_tau_ms)
            positive = sum(max(0., row.current) for row in rows)
            negative = sum(max(0., -row.current) for row in rows)
            refractory = time_ms < unit.refractory_until_ms
            net = positive-negative
            effective = min(0., net) if refractory else net
            threshold = unit.base_threshold + max(0., adaptation)
            pending.append({"time_ms": time_ms, "target_id": target,
                            "arrival_count": len(rows), "positive_current": positive,
                            "positive_current_arrival_count": sum(row.current > 0. for row in rows),
                            "negative_current": negative, "decayed_potential": potential,
                            "integrated_net_current": effective,
                            "refractory_suppressed_net_positive": (
                                max(0., net) if refractory else 0.),
                            "potential_before_reset": potential+effective,
                            "threshold": threshold, "refractory": refractory})
        spikes = super()._deliver_group(time_ms, arrivals)
        spiked = {spike.unit_id for spike in spikes}
        for row in pending:
            row["spiked"] = row["target_id"] in spiked
            row["potential_after_event"] = self.units[row["target_id"]].potential
        self.arrival_observations.extend(pending)
        return spikes


def run_probe(field: TemporalExcitableField, cue_unit: int, *, horizon_ms: float = 40.,
              cut_hidden_boundary: bool = False, ports: tuple[int, ...] = PORTS) -> dict[str, Any]:
    if horizon_ms not in (40., 160.):
        raise ValueError("RD001 permits only predeclared 40/160ms horizons")
    if ports != PORTS or type(cue_unit) is not int or cue_unit not in field.units:
        raise ValueError("invalid probe ports/cue")
    initial_hash = connection_hash(field)
    observed = ArrivalObservedField.from_state_dict(field.state_dict())
    changed = []
    if cut_hidden_boundary:
        for key, edge in observed.connections.items():
            if (edge.source_id in ports) != (edge.target_id in ports):
                changed.append({"edge": key, "old_weight": edge.weight})
                edge.weight = 0.
    reference = TemporalExcitableField.from_state_dict(observed.state_dict())
    probe_connection_hash = connection_hash(observed)
    cue = SynapticArrival(time_ms=100., target_id=cue_unit, current=1., source_id=None,
                          pulse_id="rv02-rd001-cue", novelty=0., prediction_error=0.)
    observed.schedule_arrival(cue)
    reference.schedule_arrival(cue)
    # One native bounded call covers the whole horizon, not separately reset bin budgets.
    spikes = observed.run_until(100.+horizon_ms)
    reference_spikes = reference.run_until(100.+horizon_ms)
    observer_equivalence = (observed.state_hash() == reference.state_hash()
                            and spikes == reference_spikes)
    if not observer_equivalence or connection_hash(observed) != probe_connection_hash:
        raise RuntimeError("observer noninterference/probe nonlearning failure")
    hidden = sorted(set(field.units)-set(ports))
    by_unit: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in observed.arrival_observations:
        by_unit[row["target_id"]].append(row)
    hidden_rows = []
    for unit_id in hidden:
        rows, unit = by_unit[unit_id], observed.units[unit_id]
        final_projected = unit.potential * math.exp(
            -(observed.current_time_ms-unit.last_update_ms)/observed.config.membrane_tau_ms)
        hidden_rows.append({
            "unit_id": unit_id, "arrival_count": sum(r["arrival_count"] for r in rows),
            "positive_current_arrival_count": sum(
                r["positive_current_arrival_count"] for r in rows),
            "positive_current": sum(r["positive_current"] for r in rows),
            "negative_current": sum(r["negative_current"] for r in rows),
            "integrated_net_current": sum(r["integrated_net_current"] for r in rows),
            "refractory_suppressed_net_positive": sum(
                r["refractory_suppressed_net_positive"] for r in rows),
            "maximum_potential_threshold_ratio": max(
                (r["potential_before_reset"]/r["threshold"] for r in rows), default=None),
            "spike_count": sum(r["spiked"] for r in rows),
            "stored_final_potential": unit.potential, "last_update_ms": unit.last_update_ms,
            "projected_final_potential": final_projected,
        })
    visible_state = [asdict(observed.units[unit_id]) for unit_id in ports]
    return {
        "cue_unit": cue_unit, "horizon_ms": horizon_ms,
        "cut_hidden_boundary": cut_hidden_boundary, "boundary_interventions": changed,
        "initial_connection_hash": initial_hash,
        "probe_connection_hash_before": probe_connection_hash,
        "probe_connection_hash_after": connection_hash(observed),
        "observer_equivalence": observer_equivalence,
        "observed_state_hash": observed.state_hash(),
        "reference_state_hash": reference.state_hash(),
        "arrival_observations": observed.arrival_observations,
        "spikes": [asdict(spike) for spike in spikes], "hidden_units": hidden_rows,
        "visible_trace": [(spike.time_ms, spike.unit_id) for spike in spikes
                          if spike.unit_id in ports],
        "visible_final_state": visible_state,
        "visible_final_state_hash": digest(visible_state),
        "final_queue_size": len(observed.state_dict()["queue"]),
        "queue_drained": not observed.state_dict()["queue"],
        "actual_arrivals": observed.total_arrivals, "actual_spikes": observed.total_spikes,
        "final_clock_ms": observed.current_time_ms,
    }


def run_recruitment_cell(config: ScaleStudyConfig, world: dict[str, Any],
                         scale: int) -> dict[str, Any]:
    if config != ScaleStudyConfig():
        raise ValueError("RD001 baseline configuration is fixed")
    audit = audit_scale(config, world, scale)
    field = build_physical_field(unit_count=audit["unit_count"], directed_edges=audit["edges"],
                                 threshold=.5, initial_weight=.05, initial_delay_ms=5.)
    field.receptor_ids = PORTS
    field.config = replace(field.config, max_events_per_run=4096, max_spikes_per_run=512)
    before = {key: asdict(edge) for key, edge in field.connections.items()}
    training_rows = []
    for route_index, (route, exposures) in enumerate(
            zip(world["routes"], world["exposures"], strict=True)):
        for episode in range(exposures):
            learner = ExternalOnlyPhysicalPlasticity(field)
            for index, unit in enumerate(route):
                updates = learner.observe_external(runtime_pulse(
                    event_id=f"{world['world_id']}:{route_index}:{episode}:{index}",
                    time_ms=float(route_index*10000+episode*100+index*5),
                    unit_id=unit, magnitude=1.))
                traces = learner.state_dict()["unit_traces"]
                training_rows.append({
                    "route_index": route_index, "episode": episode, "position": index,
                    "external_unit": unit, "external_trace_units": sorted(map(int, traces)),
                    "updates": [asdict(update) for update in updates],
                })
    changed_hidden = [key for key, edge in field.connections.items()
                      if (key[0] not in PORTS or key[1] not in PORTS)
                      and before[key] != asdict(edge)]
    hidden_external_trace_count = sum(
        u not in PORTS for row in training_rows for u in row["external_trace_units"])
    probes = []
    for index, route in enumerate(world["routes"]):
        natural = run_probe(field, route[0])
        extended = run_probe(field, route[0], horizon_ms=160.)
        cut = run_probe(field, route[0], cut_hidden_boundary=True)
        probes.append({
            "route_index": index, "natural": natural, "extended": extended, "boundary_zero": cut,
            "extended_40ms_prefix_matches": (
                [s for s in extended["spikes"] if s["time_ms"] <= 140.] == natural["spikes"]),
            "boundary_visible_trace_equal": cut["visible_trace"] == natural["visible_trace"],
            "boundary_visible_final_state_equal": (
                cut["visible_final_state_hash"] == natural["visible_final_state_hash"]),
        })
    positive = run_probe(field, min(set(field.units)-set(PORTS)))
    positive_passed = any(spike["unit_id"] == positive["cue_unit"]
                          and spike["time_ms"] == 100. for spike in positive["spikes"])
    if not positive_passed or not all(p["extended_40ms_prefix_matches"] for p in probes):
        raise RuntimeError("positive control or extended-prefix check failed")
    return {"diagnosis": "rv02-rd001-development", "audit": audit,
            "training_rows": training_rows, "changed_hidden_edges": changed_hidden,
            "hidden_external_trace_count": hidden_external_trace_count,
            "route_probes": probes, "positive_control": positive,
            "positive_control_passed": positive_passed, "complete": True,
            "scientific_status": "not_evaluated_development_diagnosis"}

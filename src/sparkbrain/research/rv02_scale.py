"""RV02 development feasibility; not a formal capability evaluator.

No RV01 source or learning rule is modified. Expanded connectivity, fixed external
ports and residual resource mismatches are explicit development adaptations.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from collections import Counter, deque
from dataclasses import asdict, dataclass, replace
from typing import Any


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


@dataclass(frozen=True)
class ScaleStudyConfig:
    base_units: int = 48
    scales: tuple[int, ...] = (1, 3, 10)
    degree: int = 8
    seed: int = 92001
    probe_steps: int = 8
    max_events: int = 512

    def validate(self) -> None:
        for name in ("base_units", "degree", "seed", "probe_steps", "max_events"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.base_units < 48 or self.base_units > 256:
            raise ValueError("development base_units must be in [48,256]")
        if self.scales != (1, 3, 10) or any(type(s) is not int for s in self.scales):
            raise ValueError("development scales must be exactly (1,3,10)")
        if not 8 <= self.degree < self.base_units:
            raise ValueError("degree must be at least 8 and less than base_units")
        if self.probe_steps > 16 or self.max_events > 512:
            raise ValueError("development probe ceiling exceeded")

    def state_dict(self) -> dict[str, Any]:
        return {**asdict(self), "scales": list(self.scales)}

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> ScaleStudyConfig:
        if set(value) != set(cls.__dataclass_fields__):
            raise ValueError("config fields must match exactly")
        config = cls(**{**value, "scales": tuple(value["scales"])})
        config.validate()
        return config


def build_topology(
    config: ScaleStudyConfig,
    scale: int,
    required_edges: tuple[tuple[int, int], ...] = (),
) -> tuple[tuple[int, int], ...]:
    """A ring plus exposed transitions, filled to fixed outgoing degree.

    The mean incoming degree is exact; its dispersion is not assumed constant.
    The exposed-edge privilege is inherited from RV01 and shared by both models.
    """
    config.validate()
    if type(scale) is not int or scale not in config.scales:
        raise ValueError("unsupported development scale")
    n = config.base_units * scale
    outgoing = [{(i + 1) % n} for i in range(n)]
    for source, target in required_edges:
        if any(type(x) is not int or not 0 <= x < n for x in (source, target)):
            raise ValueError("invalid required edge endpoint")
        if source == target:
            raise ValueError("self edges are prohibited")
        outgoing[source].add(target)
    rng = random.Random(config.seed)
    for source, targets in enumerate(outgoing):
        if len(targets) > config.degree:
            raise ValueError("required topology exceeds fixed degree")
        choices = [target for target in range(n) if target != source and target not in targets]
        targets.update(rng.sample(choices, config.degree - len(targets)))
    return tuple(
        (source, target) for source, targets in enumerate(outgoing) for target in sorted(targets)
    )


def development_worlds(config: ScaleStudyConfig) -> tuple[dict[str, Any], ...]:
    config.validate()
    templates = {
        "disjoint-routes": ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11)),
        "shared-cue": ((0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9)),
        "shared-prefix": ((0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7)),
        "opposing-reversal": ((0, 1, 2, 3), (4, 2, 1, 5), (6, 7, 8, 9)),
        "dense-load": tuple(
            (0 if i < 4 else i, 10 + 3 * i, 11 + 3 * i, 12 + 3 * i) for i in range(8)
        ),
        "capacity-pressure": tuple((0, 1 + 3 * i, 2 + 3 * i, 3 + 3 * i) for i in range(6)),
    }
    rng = random.Random(config.seed)
    mapping = list(range(36))
    rng.shuffle(mapping)
    worlds = []
    for family, templates_for_family in templates.items():
        routes = tuple(tuple(mapping[u] for u in route) for route in templates_for_family)
        # Per-world evidence is fixed across scales, not necessarily across families.
        world = {
            "world_id": f"rv02-development:{config.seed}:{family}",
            "family": family,
            "routes": routes,
            "exposures": tuple(4 for _ in routes),
            "ports": tuple(range(36)),
        }
        world["evidence_hash"] = digest(world)
        worlds.append(world)
    return tuple(worlds)


def audit_scale(config: ScaleStudyConfig, world: dict[str, Any], scale: int) -> dict[str, Any]:
    # Only this development fixture namespace can execute. No caller-provided
    # unseen route, stale digest or zero-exposure probe may seed the topology.
    if digest(world) not in {digest(w) for w in development_worlds(config)}:
        raise ValueError("world must match an unmodified RV02 development fixture")
    required = tuple(
        sorted({edge for route in world["routes"] for edge in zip(route, route[1:], strict=True)})
    )
    edges = build_topology(config, scale, required)
    n = config.base_units * scale
    outgoing: dict[int, list[int]] = {i: [] for i in range(n)}
    incoming = Counter(target for _, target in edges)
    for source, target in edges:
        outgoing[source].append(target)
    distance = {port: 0 for port in world["ports"]}
    queue = deque(distance)
    while queue:
        source = queue.popleft()
        for target in outgoing[source]:
            if target not in distance:
                distance[target] = distance[source] + 1
                queue.append(target)
    return {
        "world_id": world["world_id"],
        "scale": scale,
        "unit_count": n,
        "connection_count": len(edges),
        "average_out_degree": len(edges) / n,
        "average_in_degree": len(edges) / n,
        "minimum_in_degree": min(incoming.values()),
        "maximum_in_degree": max(incoming.values()),
        "evidence_hash": world["evidence_hash"],
        "input_ports": world["ports"],
        "readout_ports": world["ports"],
        "input_fanout": 1,
        "external_observation_count": sum(
            len(r) * e for r, e in zip(world["routes"], world["exposures"], strict=True)
        ),
        "probe_count": len(world["routes"]),
        "reachable_unit_count": len(distance),
        "maximum_port_distance": max(distance.values()),
        "reachable_within_probe_steps": sum(d <= config.probe_steps for d in distance.values()),
        "topology_hash": digest(edges),
        "edges": edges,
        "topology_privilege": "observed_transition_edges_present_before_training",
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "resource_match_passed": False,
        "resource_match_reason": (
            "units_edges_evidence_paired_but_adaptive_state_and_work_not_matched"
        ),
    }


def project_behavior(
    generated: tuple[int, ...], ports: tuple[int, ...], route: tuple[int, ...], unit_count: int
) -> dict[str, Any]:
    """Hidden activity is never counted as a wrong external symbol."""
    visible = tuple(u for u in generated if u in ports)
    expected = route[1:]
    position = 0
    for unit in visible:
        if position < len(expected) and unit == expected[position]:
            position += 1
    contamination = sum(u not in route for u in visible)
    return {
        "generated_units": visible,
        "ordered_retention": position / len(expected),
        "exact_sequence_recovered": visible == expected,
        "rv01_compatible_exact_route": position == len(expected) and contamination == 0,
        "raw_contamination": contamination,
        "contamination_per_active_unit": (
            contamination / len(set(generated)) if generated else None
        ),
        "contamination_per_total_unit": contamination / unit_count,
        "contamination_per_recovered_route_unit": contamination / position if position else None,
        "contamination_per_candidate_activity": contamination / len(visible) if visible else None,
    }


def geometry(active_sets: tuple[tuple[int, ...], ...], unit_count: int) -> dict[str, Any]:
    counts = Counter(u for active in active_sets for u in set(active))
    total = sum(counts.values())
    entropy = -sum((c / total) * math.log(c / total) for c in counts.values()) if total else 0.0
    return {
        "active_sets": active_sets,
        "active_counts": tuple(len(set(a)) for a in active_sets),
        "active_fractions": tuple(len(set(a)) / unit_count for a in active_sets),
        "unique_occupied_units": len(counts),
        "unique_occupied_fraction": len(counts) / unit_count,
        "state_reuse_count": total - len(counts),
        "activation_entropy_nats": entropy,
    }


def run_development_cell(
    config: ScaleStudyConfig, world: dict[str, Any], scale: int, architecture: str
) -> dict[str, Any]:
    """Execute unchanged learning rules on a new connected development substrate.

    Reservoir fixed-port readout is an explicit adapter, not an RV01 reproduction.
    Resource mismatches prohibit inference that either architecture is superior.
    """
    if architecture not in ("field", "reservoir"):
        raise ValueError("architecture must be field or reservoir")
    audit = audit_scale(config, world, scale)
    from sparkbrain.research.rv01.physical_learner_bridge import (
        build_physical_field,
        connection_snapshots,
        runtime_pulse,
    )
    from sparkbrain.research.rv01.physical_plasticity import ExternalOnlyPhysicalPlasticity
    from sparkbrain.research.rv01.resource_matched_reservoir import ResourceMatchedSparseReservoir
    from sparkbrain.v04.contracts import SynapticArrival
    from sparkbrain.v04.field import TemporalExcitableField

    n, edges, ports = audit["unit_count"], audit["edges"], world["ports"]
    probes = []
    if architecture == "field":
        field = build_physical_field(
            unit_count=n,
            directed_edges=edges,
            threshold=0.5,
            initial_weight=0.05,
            initial_delay_ms=5.0,
        )
        field.receptor_ids = ports
        field.config = replace(
            field.config,
            max_events_per_run=config.max_events * config.degree,
            max_spikes_per_run=config.max_events,
        )
        before = connection_snapshots(field)
        updates = 0
        parameter_updates = 0
        training = zip(world["routes"], world["exposures"], strict=True)
        for route_index, (route, exposures) in enumerate(training):
            for episode in range(exposures):
                learner = ExternalOnlyPhysicalPlasticity(field)
                for index, unit in enumerate(route):
                    changed = learner.observe_external(
                        runtime_pulse(
                            event_id=f"{world['world_id']}:{route_index}:{episode}:{index}",
                            time_ms=float(route_index * 10000 + episode * 100 + index * 5),
                            unit_id=unit,
                            magnitude=1.0,
                        )
                    )
                    updates += 1
                    parameter_updates += len(changed)
        after = connection_snapshots(field)
        changed_hidden = sum(
            a.weight != b.weight or a.delay_ms != b.delay_ms
            for a, b in zip(before, after, strict=True)
            if a.source_id not in ports or a.target_id not in ports
        )
        for route in world["routes"]:
            probe = TemporalExcitableField.from_state_dict(field.state_dict())
            connection_hash_before_probe = digest([asdict(c) for c in connection_snapshots(probe)])
            probe.schedule_arrival(
                SynapticArrival(
                    time_ms=100.0,
                    target_id=route[0],
                    current=1.0,
                    source_id=None,
                    pulse_id="rv02-cue",
                    novelty=0.0,
                    prediction_error=0.0,
                )
            )
            spikes, active_sets = [], []
            halt = "horizon_reached"
            for step in range(config.probe_steps):
                # Native guards enforce remaining aggregate limits inside run_until.
                probe.config = replace(
                    probe.config,
                    max_events_per_run=max(
                        1, config.max_events * config.degree - probe.total_arrivals
                    ),
                    max_spikes_per_run=max(1, config.max_events - probe.total_spikes),
                )
                rows = probe.run_until(100.0 + 5 * (step + 1))
                spikes.extend(row for row in rows if row.time_ms > 100.0)
                active_sets.append(tuple(row.unit_id for row in rows))
                if (
                    probe.total_spikes >= config.max_events
                    or probe.total_arrivals >= config.max_events * config.degree
                ):
                    halt = "event_budget_reached"
                    break
                if not probe.state_dict()["queue"]:
                    halt = "queue_drained"
                    break
            generated = tuple(row.unit_id for row in spikes)
            probes.append(
                {
                    "route": route,
                    "behavior": project_behavior(generated, ports, route, n),
                    "geometry": geometry(tuple(active_sets), n),
                    "halt_reason": halt,
                    "geometry_definition": "spiking_units_per_5ms_bin",
                    "final_queue_size": len(probe.state_dict()["queue"]),
                    "actual_arrival_count": probe.total_arrivals,
                    "actual_spike_count": probe.total_spikes,
                    "connection_hash_before_probe": connection_hash_before_probe,
                    "connection_hash_after_probe": digest(
                        [asdict(c) for c in connection_snapshots(probe)]
                    ),
                }
            )
        resource = {
            "learning_observe_calls": updates,
            "changed_hidden_connections": changed_hidden,
            "parameter_update_count": parameter_updates,
            "adaptive_connection_scalar_slots": 2 * len(edges),
            "serialized_state_bytes": len(json.dumps(field.state_dict()).encode()),
        }
    else:
        reservoir = ResourceMatchedSparseReservoir(
            unit_count=n,
            directed_edges=edges,
            maximum_active_outputs=config.degree,
            seed=config.seed,
        )
        # Separate visible target interface; never silently train hidden output labels.
        visible_edges = tuple(edge for edge in edges if edge[1] in ports)
        reservoir._readout_sources = {
            target: sources
            for target, sources in reservoir._readout_sources.items()
            if target in ports
        }
        for route, exposures in zip(world["routes"], world["exposures"], strict=True):
            for _ in range(exposures):
                state = reservoir.zero_state()
                for index, unit in enumerate(route):
                    state = reservoir.advance_many(state, (unit,))
                    reservoir.observed_external_event_count += 1
                    if index + 1 < len(route):
                        # Same update rule, over explicit fixed-port readout edges only.
                        original_edges = reservoir.directed_edges
                        reservoir.directed_edges = visible_edges
                        try:
                            reservoir._update_readout(state, route[index + 1])
                        finally:
                            reservoir.directed_edges = original_edges
        for route in world["routes"]:
            readout_hash_before_probe = digest(sorted(reservoir._readout_weights.items()))
            state, active = reservoir.zero_state(), (route[0],)
            generated, active_sets, halt = [], [], "horizon_reached"
            for _ in range(config.probe_steps):
                state = reservoir.advance_many(state, active)
                active_sets.append(tuple(i for i, value in enumerate(state) if abs(value) > 1e-9))
                ranked = sorted(
                    ((score, u) for u, score in reservoir._scores(state).items() if score > 0),
                    key=lambda row: (-row[0], row[1]),
                )
                remaining = config.max_events - len(generated)
                if remaining <= 0:
                    halt = "event_budget_reached"
                    break
                active = tuple(u for _, u in ranked[: min(config.degree, remaining)])
                if not active:
                    halt = "no_positive_output"
                    break
                generated.extend(active)
            probes.append(
                {
                    "route": route,
                    "behavior": project_behavior(tuple(generated), ports, route, n),
                    "geometry": geometry(tuple(active_sets), n),
                    "halt_reason": halt,
                    "geometry_definition": "abs_recurrent_state_gt_1e-9_per_step",
                    "readout_hash_before_probe": readout_hash_before_probe,
                    "readout_hash_after_probe": digest(sorted(reservoir._readout_weights.items())),
                }
            )
        resource = {
            "parameter_update_count": reservoir.parameter_update_count,
            "observed_external_event_count": reservoir.observed_external_event_count,
            "fixed_recurrent_scalar_slots": len(edges),
            "allocated_readout_scalar_slots": len(edges),
            "trainable_visible_readout_scalar_slots": len(visible_edges),
            "hidden_readout_scalar_slots_unused": len(edges) - len(visible_edges),
        }
    complete = all(p["halt_reason"] != "event_budget_reached" for p in probes)
    for probe in probes:
        probe["complete"] = probe["halt_reason"] != "event_budget_reached"
    return {
        "architecture": architecture,
        "audit": audit,
        "probes": probes,
        "complete": complete,
        "resource": resource,
        "scientific_status": "not_evaluated_development_feasibility",
    }

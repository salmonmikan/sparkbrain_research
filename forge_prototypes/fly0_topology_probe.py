"""Bounded, non-evidentiary FLY-0 topology comparison.

This module deliberately models only a small deterministic engineering probe.  It is
not a fly connectome, a biological simulation, or a scientific evaluator.
"""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
from typing import Literal

Role = Literal["sensory", "local", "motor", "modulation"]


@dataclass(frozen=True, order=True)
class Edge:
    source: int
    target: int
    sign: int
    delay: int

    def __post_init__(self) -> None:
        if self.sign not in {-1, 1}:
            raise ValueError("edge sign must be -1 or 1")
        if not 1 <= self.delay <= 3:
            raise ValueError("edge delay must be in [1, 3]")


@dataclass(frozen=True)
class Topology:
    name: str
    roles: tuple[Role, ...]
    edges: tuple[Edge, ...]

    def __post_init__(self) -> None:
        node_count = len(self.roles)
        if node_count == 0:
            raise ValueError("topology must contain nodes")
        pairs: set[tuple[int, int]] = set()
        for edge in self.edges:
            if not 0 <= edge.source < node_count or not 0 <= edge.target < node_count:
                raise ValueError("edge endpoint outside topology")
            if edge.source == edge.target:
                raise ValueError("self edges are not allowed")
            pair = (edge.source, edge.target)
            if pair in pairs:
                raise ValueError("duplicate directed edge")
            pairs.add(pair)

    @property
    def node_count(self) -> int:
        return len(self.roles)

    def fingerprint(self) -> str:
        payload = {
            "roles": self.roles,
            "edges": [edge.__dict__ for edge in sorted(self.edges)],
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return sha256(encoded).hexdigest()

    def resource_signature(self) -> dict[str, object]:
        return {
            "node_count": self.node_count,
            "edge_count": len(self.edges),
            "role_counts": dict(sorted(Counter(self.roles).items())),
            "sign_counts": dict(sorted(Counter(edge.sign for edge in self.edges).items())),
            "delay_counts": dict(sorted(Counter(edge.delay for edge in self.edges).items())),
            "role_pair_counts": dict(
                sorted(
                    Counter(
                        f"{self.roles[edge.source]}->{self.roles[edge.target]}"
                        for edge in self.edges
                    ).items()
                )
            ),
        }

    def degree_signature(self) -> tuple[tuple[int, int], ...]:
        incoming = Counter(edge.target for edge in self.edges)
        outgoing = Counter(edge.source for edge in self.edges)
        return tuple((outgoing[node], incoming[node]) for node in range(self.node_count))


@dataclass(frozen=True)
class TraceEvent:
    time: int
    node: int
    role: Role


@dataclass(frozen=True)
class ScenarioResult:
    topology: str
    side: Literal["left", "right"]
    fired_events: int
    active_nodes: int
    motor_events: tuple[tuple[int, int], ...]
    matched_motor_events: int
    opposite_motor_events: int
    first_matched_motor_time: int | None
    trace: tuple[TraceEvent, ...]


@dataclass(frozen=True)
class ComparisonResult:
    resource_signature: dict[str, object]
    fingerprints: dict[str, str]
    degree_preservation: bool
    scenarios: tuple[ScenarioResult, ...]

    def summary(self) -> dict[str, object]:
        by_topology: dict[str, dict[str, object]] = {}
        for scenario in self.scenarios:
            row = by_topology.setdefault(
                scenario.topology,
                {
                    "matched_motor_events": 0,
                    "opposite_motor_events": 0,
                    "fired_events": 0,
                    "first_matched_motor_times": [],
                },
            )
            row["matched_motor_events"] += scenario.matched_motor_events
            row["opposite_motor_events"] += scenario.opposite_motor_events
            row["fired_events"] += scenario.fired_events
            if scenario.first_matched_motor_time is not None:
                row["first_matched_motor_times"].append(scenario.first_matched_motor_time)
        for row in by_topology.values():
            matched = int(row["matched_motor_events"])
            opposite = int(row["opposite_motor_events"])
            total = matched + opposite
            row["motor_side_selectivity"] = (matched - opposite) / total if total else 0.0
        return {
            "resource_signature": self.resource_signature,
            "degree_preservation": self.degree_preservation,
            "fingerprints": self.fingerprints,
            "topologies": by_topology,
        }


SENSORY = tuple(range(0, 16))
LOCAL = tuple(range(16, 112))
MOTOR = tuple(range(112, 120))
MODULATION = tuple(range(120, 128))
LEFT_SENSORY = SENSORY[:8]
RIGHT_SENSORY = SENSORY[8:]
LEFT_LOCAL = LOCAL[:48]
RIGHT_LOCAL = LOCAL[48:]
LEFT_MOTOR = MOTOR[:4]
RIGHT_MOTOR = MOTOR[4:]
LEFT_MODULATION = MODULATION[:4]
RIGHT_MODULATION = MODULATION[4:]


def _roles() -> tuple[Role, ...]:
    return (
        ("sensory",) * len(SENSORY)
        + ("local",) * len(LOCAL)
        + ("motor",) * len(MOTOR)
        + ("modulation",) * len(MODULATION)
    )


def _local_sign(node: int) -> int:
    return -1 if (node - LOCAL[0]) % 5 == 0 else 1


def build_structured_topology() -> Topology:
    """Build a reduced bilateral sensorimotor motif with bounded local recurrence."""

    edges: list[Edge] = []
    for sensory_group, local_group in (
        (LEFT_SENSORY, LEFT_LOCAL),
        (RIGHT_SENSORY, RIGHT_LOCAL),
    ):
        for index, source in enumerate(sensory_group):
            for offset in range(4):
                target = local_group[(index * 5 + offset * 7) % len(local_group)]
                edges.append(Edge(source, target, 1, 1))

    for local_group in (LEFT_LOCAL, RIGHT_LOCAL):
        for index, source in enumerate(local_group):
            sign = _local_sign(source)
            for offset, delay in ((1, 1), (7, 1), (17, 2)):
                target = local_group[(index + offset) % len(local_group)]
                edges.append(Edge(source, target, sign, delay))

    for local_group, motor_group in (
        (LEFT_LOCAL, LEFT_MOTOR),
        (RIGHT_LOCAL, RIGHT_MOTOR),
    ):
        for index, source in enumerate(local_group):
            target = motor_group[index % len(motor_group)]
            edges.append(Edge(source, target, _local_sign(source), 1))

    for motor_group, local_group in (
        (LEFT_MOTOR, LEFT_LOCAL),
        (RIGHT_MOTOR, RIGHT_LOCAL),
    ):
        for index, source in enumerate(motor_group):
            for offset in range(4):
                target = local_group[(index * 11 + offset * 9) % len(local_group)]
                edges.append(Edge(source, target, 1, 2))

    for modulation_group, local_group in (
        (LEFT_MODULATION, LEFT_LOCAL),
        (RIGHT_MODULATION, RIGHT_LOCAL),
    ):
        for index, source in enumerate(modulation_group):
            for offset in range(4):
                target = local_group[(index * 13 + offset * 5) % len(local_group)]
                edges.append(Edge(source, target, 1, 1))

    return Topology("fly_like_structured", _roles(), tuple(edges))


def _role_pair(topology: Topology, edge: Edge) -> tuple[Role, Role]:
    return topology.roles[edge.source], topology.roles[edge.target]


def build_degree_preserving_rewire(
    structured: Topology, *, seed: int = 2801, swap_factor: int = 24
) -> Topology:
    """Rewire targets within role-pair strata while preserving each node's degrees."""

    rng = random.Random(seed)
    edges = list(structured.edges)
    buckets: dict[tuple[Role, Role], list[int]] = defaultdict(list)
    for index, edge in enumerate(edges):
        buckets[_role_pair(structured, edge)].append(index)
    pairs = {(edge.source, edge.target) for edge in edges}
    attempts = max(1, len(edges) * swap_factor)
    swaps = 0
    bucket_values = [indices for indices in buckets.values() if len(indices) >= 2]
    for _ in range(attempts):
        indices = rng.choice(bucket_values)
        first_index, second_index = rng.sample(indices, 2)
        first = edges[first_index]
        second = edges[second_index]
        if first.source == second.source or first.target == second.target:
            continue
        first_pair = (first.source, second.target)
        second_pair = (second.source, first.target)
        if first_pair[0] == first_pair[1] or second_pair[0] == second_pair[1]:
            continue
        old_pairs = {(first.source, first.target), (second.source, second.target)}
        if (first_pair in pairs and first_pair not in old_pairs) or (
            second_pair in pairs and second_pair not in old_pairs
        ):
            continue
        pairs.difference_update(old_pairs)
        pairs.update((first_pair, second_pair))
        edges[first_index] = Edge(first.source, second.target, first.sign, first.delay)
        edges[second_index] = Edge(second.source, first.target, second.sign, second.delay)
        swaps += 1
    if swaps < len(edges):
        raise RuntimeError("insufficient valid degree-preserving swaps")
    return Topology("degree_preserving_rewired", structured.roles, tuple(edges))


def build_random_sparse(structured: Topology, *, seed: int = 2802) -> Topology:
    """Build a random sparse control matched on role pairs, signs and delays."""

    rng = random.Random(seed)
    nodes_by_role: dict[Role, tuple[int, ...]] = {
        role: tuple(index for index, value in enumerate(structured.roles) if value == role)
        for role in ("sensory", "local", "motor", "modulation")
    }
    edges: list[Edge] = []
    used: set[tuple[int, int]] = set()
    template_edges = list(structured.edges)
    rng.shuffle(template_edges)
    for template in template_edges:
        source_role, target_role = _role_pair(structured, template)
        candidates = [
            (source, target)
            for source in nodes_by_role[source_role]
            for target in nodes_by_role[target_role]
            if source != target and (source, target) not in used
        ]
        if not candidates:
            raise RuntimeError("random sparse role-pair stratum exhausted")
        source, target = rng.choice(candidates)
        used.add((source, target))
        edges.append(Edge(source, target, template.sign, template.delay))
    return Topology("random_sparse", structured.roles, tuple(edges))


def _threshold(role: Role) -> float:
    return 2.0 if role == "motor" else 1.0


def run_scenario(
    topology: Topology,
    *,
    side: Literal["left", "right"],
    horizon: int = 8,
    max_fired_events: int = 4096,
) -> ScenarioResult:
    """Run one deterministic event-like pulse with descending modulation."""

    if horizon < 1 or horizon > 32:
        raise ValueError("horizon must be in [1, 32]")
    if max_fired_events < topology.node_count:
        raise ValueError("max_fired_events is too small for a useful bounded probe")
    outgoing: dict[int, list[Edge]] = defaultdict(list)
    for edge in topology.edges:
        outgoing[edge.source].append(edge)
    for edges in outgoing.values():
        edges.sort()

    sensory = LEFT_SENSORY if side == "left" else RIGHT_SENSORY
    modulation = LEFT_MODULATION if side == "left" else RIGHT_MODULATION
    matched_motors = set(LEFT_MOTOR if side == "left" else RIGHT_MOTOR)
    pending: dict[int, dict[int, float]] = defaultdict(lambda: defaultdict(float))
    for node in sensory:
        pending[0][node] += 1.5
    for node in modulation:
        pending[0][node] += 1.5

    trace: list[TraceEvent] = []
    motor_events: list[tuple[int, int]] = []
    last_fired: dict[int, int] = {}
    for time in range(horizon + 1):
        for node, amplitude in sorted(pending.pop(time, {}).items()):
            if amplitude < _threshold(topology.roles[node]):
                continue
            if last_fired.get(node) == time:
                continue
            last_fired[node] = time
            event = TraceEvent(time, node, topology.roles[node])
            trace.append(event)
            if len(trace) > max_fired_events:
                raise RuntimeError("bounded event budget exceeded")
            if topology.roles[node] == "motor":
                motor_events.append((time, node))
            for edge in outgoing.get(node, ()):
                arrival = time + edge.delay
                if arrival <= horizon:
                    pending[arrival][edge.target] += float(edge.sign)

    matched = sum(node in matched_motors for _, node in motor_events)
    opposite = len(motor_events) - matched
    matched_times = [time for time, node in motor_events if node in matched_motors]
    return ScenarioResult(
        topology=topology.name,
        side=side,
        fired_events=len(trace),
        active_nodes=len({event.node for event in trace}),
        motor_events=tuple(motor_events),
        matched_motor_events=matched,
        opposite_motor_events=opposite,
        first_matched_motor_time=min(matched_times) if matched_times else None,
        trace=tuple(trace),
    )


def compare_topologies() -> ComparisonResult:
    structured = build_structured_topology()
    rewired = build_degree_preserving_rewire(structured)
    random_sparse = build_random_sparse(structured)
    topologies = (structured, rewired, random_sparse)
    signature = structured.resource_signature()
    if any(topology.resource_signature() != signature for topology in topologies[1:]):
        raise AssertionError("topology resource envelopes diverged")
    degree_preservation = structured.degree_signature() == rewired.degree_signature()
    if not degree_preservation:
        raise AssertionError("degree-preserving control changed a node degree")
    scenarios = tuple(
        run_scenario(topology, side=side)
        for topology in topologies
        for side in ("left", "right")
    )
    return ComparisonResult(
        resource_signature=signature,
        fingerprints={topology.name: topology.fingerprint() for topology in topologies},
        degree_preservation=degree_preservation,
        scenarios=scenarios,
    )


def render_summary(result: ComparisonResult) -> str:
    return json.dumps(result.summary(), indent=2, sort_keys=True)


if __name__ == "__main__":
    print(render_summary(compare_topologies()))

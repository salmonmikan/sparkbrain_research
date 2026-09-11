"""Construction-only causal-reachability certificates for R01-16.

The certificate answers only whether preregistered propagation-factor reset
edges are structurally reachable from the fixed cue source(s) within the fixed
probe horizon. It does not run the Field, inspect behavioral output, score a
probe, or grant execution authority.
"""

from __future__ import annotations

import hashlib
import heapq
import json
import math
from dataclasses import asdict, dataclass

from .rv01_r01_16_factorization import (
    ConnectionState,
    R01_16FactorizationConstruction,
)

R01_16_REACHABILITY_AMENDMENT_ID = (
    "rv01-r01-16-propagation-factorization-amendment-001"
)


def _sha256(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _finite_positive(value: float, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a real numeric value")
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


@dataclass(frozen=True, slots=True)
class ReachableEdge:
    source_id: int
    target_id: int
    earliest_source_arrival_ms: float
    conservative_edge_delay_ms: float
    earliest_target_arrival_ms: float

    @property
    def key(self) -> tuple[int, int]:
        return (self.source_id, self.target_id)

    def state_dict(self) -> dict[str, int | float]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FactorReachabilityCertificate:
    amendment_id: str
    cue_source_ids: tuple[int, ...]
    probe_horizon_ms: float
    pre_training_sha256: str
    post_training_sha256: str
    earliest_arrival_sha256: str
    weight_changed_edges: tuple[tuple[int, int], ...]
    delay_changed_edges: tuple[tuple[int, int], ...]
    reachable_weight_edges: tuple[ReachableEdge, ...]
    reachable_delay_edges: tuple[ReachableEdge, ...]

    @property
    def weight_eligible(self) -> bool:
        return bool(self.reachable_weight_edges)

    @property
    def delay_eligible(self) -> bool:
        return bool(self.reachable_delay_edges)

    @property
    def combined_eligible(self) -> bool:
        return self.weight_eligible or self.delay_eligible

    def state_dict(self) -> dict[str, object]:
        return {
            "amendment_id": self.amendment_id,
            "cue_source_ids": list(self.cue_source_ids),
            "probe_horizon_ms": self.probe_horizon_ms,
            "pre_training_sha256": self.pre_training_sha256,
            "post_training_sha256": self.post_training_sha256,
            "earliest_arrival_sha256": self.earliest_arrival_sha256,
            "weight_changed_edges": [list(edge) for edge in self.weight_changed_edges],
            "delay_changed_edges": [list(edge) for edge in self.delay_changed_edges],
            "reachable_weight_edges": [
                edge.state_dict() for edge in self.reachable_weight_edges
            ],
            "reachable_delay_edges": [
                edge.state_dict() for edge in self.reachable_delay_edges
            ],
            "weight_eligible": self.weight_eligible,
            "delay_eligible": self.delay_eligible,
            "combined_eligible": self.combined_eligible,
        }

    @property
    def sha256(self) -> str:
        return _sha256(self.state_dict())


def _conservative_delay(
    pre: ConnectionState,
    post: ConnectionState,
) -> float:
    """Use the slower registered value so reachability is true in both reset states."""

    return max(pre.delay_ms, post.delay_ms)


def _earliest_arrivals(
    construction: R01_16FactorizationConstruction,
    *,
    cue_source_ids: tuple[int, ...],
    probe_horizon_ms: float,
) -> dict[int, float]:
    if not cue_source_ids:
        raise ValueError("R01-16 reachability requires at least one cue source")
    if any(type(unit_id) is not int for unit_id in cue_source_ids):
        raise TypeError("cue source IDs must be integers")
    if len(set(cue_source_ids)) != len(cue_source_ids):
        raise ValueError("cue source IDs must be unique")
    horizon = _finite_positive(probe_horizon_ms, name="probe_horizon_ms")

    pre = {row.key: row for row in construction.pre_training}
    post = {row.key: row for row in construction.post_training}
    unit_ids = {unit_id for edge in pre for unit_id in edge}
    missing = set(cue_source_ids) - unit_ids
    if missing:
        raise ValueError("cue source is not present in the fixed connection topology")

    outgoing: dict[int, list[tuple[int, float]]] = {}
    for key in sorted(post):
        source_id, target_id = key
        delay = _conservative_delay(pre[key], post[key])
        outgoing.setdefault(source_id, []).append((target_id, delay))

    arrivals: dict[int, float] = {unit_id: 0.0 for unit_id in cue_source_ids}
    queue: list[tuple[float, int]] = [(0.0, unit_id) for unit_id in cue_source_ids]
    heapq.heapify(queue)
    while queue:
        time_ms, source_id = heapq.heappop(queue)
        if time_ms != arrivals.get(source_id):
            continue
        for target_id, delay_ms in outgoing.get(source_id, ()):
            arrival_ms = time_ms + delay_ms
            if arrival_ms > horizon:
                continue
            previous = arrivals.get(target_id)
            if previous is None or arrival_ms < previous:
                arrivals[target_id] = arrival_ms
                heapq.heappush(queue, (arrival_ms, target_id))
    return arrivals


def build_factor_reachability_certificate(
    construction: R01_16FactorizationConstruction,
    *,
    cue_source_ids: tuple[int, ...],
    probe_horizon_ms: float,
) -> FactorReachabilityCertificate:
    """Bind reachable learned-factor edges without running any capability."""

    horizon = _finite_positive(probe_horizon_ms, name="probe_horizon_ms")
    arrivals = _earliest_arrivals(
        construction,
        cue_source_ids=cue_source_ids,
        probe_horizon_ms=horizon,
    )
    pre = {row.key: row for row in construction.pre_training}
    post = {row.key: row for row in construction.post_training}

    def reachable(edges: tuple[tuple[int, int], ...]) -> tuple[ReachableEdge, ...]:
        rows: list[ReachableEdge] = []
        for source_id, target_id in edges:
            source_arrival = arrivals.get(source_id)
            if source_arrival is None:
                continue
            edge_key = (source_id, target_id)
            edge_delay = _conservative_delay(pre[edge_key], post[edge_key])
            target_arrival = source_arrival + edge_delay
            if target_arrival > horizon:
                continue
            rows.append(
                ReachableEdge(
                    source_id=source_id,
                    target_id=target_id,
                    earliest_source_arrival_ms=source_arrival,
                    conservative_edge_delay_ms=edge_delay,
                    earliest_target_arrival_ms=target_arrival,
                )
            )
        return tuple(rows)

    summary = construction.summary()
    arrival_rows = [
        {"unit_id": unit_id, "earliest_arrival_ms": arrivals[unit_id]}
        for unit_id in sorted(arrivals)
    ]
    return FactorReachabilityCertificate(
        amendment_id=R01_16_REACHABILITY_AMENDMENT_ID,
        cue_source_ids=tuple(cue_source_ids),
        probe_horizon_ms=horizon,
        pre_training_sha256=summary.pre_training_sha256,
        post_training_sha256=summary.post_training_sha256,
        earliest_arrival_sha256=_sha256(arrival_rows),
        weight_changed_edges=summary.weight_changed_edges,
        delay_changed_edges=summary.delay_changed_edges,
        reachable_weight_edges=reachable(summary.weight_changed_edges),
        reachable_delay_edges=reachable(summary.delay_changed_edges),
    )


__all__ = [
    "FactorReachabilityCertificate",
    "R01_16_REACHABILITY_AMENDMENT_ID",
    "ReachableEdge",
    "build_factor_reachability_certificate",
]

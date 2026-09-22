from __future__ import annotations

import copy
import hashlib
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from typing import Any, Literal

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v04.field import TemporalExcitableField

from .brain import IntegratedV05Brain


MAX_CANDIDATE_EDGES = 12
QUIESCENCE_INCREMENT_MS = 32.0
QUIESCENCE_MAX_STEPS = 8
QUIESCENCE_CAP_MS = QUIESCENCE_INCREMENT_MS * QUIESCENCE_MAX_STEPS
DELAY_PERTURBATION_MS = 1.0

InterventionKind = Literal["transmission_null", "delay_plus_1ms", "sham"]


class RouteArchitectureUnreachable(RuntimeError):
    """The prospectively fixed Architecture construction cannot be reached."""


@dataclass(frozen=True, slots=True)
class RouteEdge:
    source_id: int
    target_id: int
    weight: float
    delay_ms: float
    plastic: bool
    internal: bool

    @property
    def key(self) -> tuple[int, int]:
        return (self.source_id, self.target_id)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EdgeControlPair:
    target: RouteEdge
    control: RouteEdge

    def as_dict(self) -> dict[str, Any]:
        return {"control": self.control.as_dict(), "target": self.target.as_dict()}


@dataclass(frozen=True, slots=True)
class OpportunityArc:
    source_id: int
    source_time_ms: float
    target_id: int
    target_time_ms: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class QuiescenceReport:
    source_field_hash: str
    clone_field_hash: str
    start_time_ms: float
    end_time_ms: float
    steps: int
    pending_counts: tuple[int, ...]
    quiescent: bool

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["pending_counts"] = list(self.pending_counts)
        return row


@dataclass(frozen=True, slots=True)
class FrozenResponseSignature:
    payload_json: str
    sha256: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def pending_arrival_count(field: TemporalExcitableField) -> int:
    """Read pending-arrival count without exposing or mutating the private heap."""
    return len(field.state_dict()["queue"])


def clone_at_quiescent_anchor(
    brain: IntegratedV05Brain,
) -> tuple[IntegratedV05Brain, QuiescenceReport]:
    """Clone and settle within the prospectively fixed 8 x 32 ms boundary.

    The source brain is never advanced.  Failure to empty the pending queue by
    256 ms is reported rather than extending the cap.
    """
    source_hash = brain.base.field.state_hash()
    clone = copy.deepcopy(brain)
    start_time = clone.current_time_ms
    pending_counts = [pending_arrival_count(clone.base.field)]
    steps = 0

    while pending_counts[-1] and steps < QUIESCENCE_MAX_STEPS:
        clone.base.advance(clone.current_time_ms + QUIESCENCE_INCREMENT_MS)
        steps += 1
        pending_counts.append(pending_arrival_count(clone.base.field))

    if brain.base.field.state_hash() != source_hash:
        raise AssertionError("quiescent-anchor construction mutated the source brain")

    report = QuiescenceReport(
        source_field_hash=source_hash,
        clone_field_hash=clone.base.field.state_hash(),
        start_time_ms=start_time,
        end_time_ms=clone.current_time_ms,
        steps=steps,
        pending_counts=tuple(pending_counts),
        quiescent=pending_counts[-1] == 0,
    )
    return clone, report


def _route_edge(field: TemporalExcitableField, source_id: int, target_id: int) -> RouteEdge:
    edge = field.connection(source_id, target_id)
    return RouteEdge(
        source_id=edge.source_id,
        target_id=edge.target_id,
        weight=float(edge.weight),
        delay_ms=float(edge.delay_ms),
        plastic=bool(edge.plastic),
        internal=False,
    )


def select_candidate_edges(
    field: TemporalExcitableField,
    prototype_unit_ids: Iterable[int],
    *,
    limit: int = MAX_CANDIDATE_EDGES,
) -> tuple[RouteEdge, ...]:
    """Select the checkpoint-only bounded edge family for one Assembly prototype."""
    if limit < 1 or limit > MAX_CANDIDATE_EDGES:
        raise ValueError(f"limit must be in [1, {MAX_CANDIDATE_EDGES}]")
    prototype = frozenset(int(unit_id) for unit_id in prototype_unit_ids)
    if not prototype:
        raise ValueError("prototype_unit_ids must be non-empty")
    receptors = frozenset(field.receptor_ids)
    rows: list[RouteEdge] = []
    for edge in field.connections.values():
        if edge.target_id not in prototype or edge.source_id in receptors:
            continue
        rows.append(
            RouteEdge(
                source_id=edge.source_id,
                target_id=edge.target_id,
                weight=float(edge.weight),
                delay_ms=float(edge.delay_ms),
                plastic=bool(edge.plastic),
                internal=edge.source_id in prototype,
            )
        )
    rows.sort(
        key=lambda edge: (
            0 if edge.internal else 1,
            -abs(edge.weight),
            edge.delay_ms,
            edge.source_id,
            edge.target_id,
        )
    )
    return tuple(rows[:limit])


def _sign_class(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def match_non_target_controls(
    field: TemporalExcitableField,
    prototype_unit_ids: Iterable[int],
    targets: Iterable[RouteEdge],
) -> tuple[EdgeControlPair, ...]:
    """Match controls deterministically using checkpoint-only edge metadata.

    Controls are reservoir edges with neither endpoint in the target prototype.
    Matching is without replacement and never consults response outcomes.
    """
    prototype = frozenset(int(unit_id) for unit_id in prototype_unit_ids)
    receptors = frozenset(field.receptor_ids)
    target_rows = tuple(targets)
    target_keys = {row.key for row in target_rows}
    pool: list[RouteEdge] = []
    for edge in field.connections.values():
        key = (edge.source_id, edge.target_id)
        if key in target_keys:
            continue
        if edge.source_id in receptors or edge.target_id in receptors:
            continue
        if edge.source_id in prototype or edge.target_id in prototype:
            continue
        pool.append(
            RouteEdge(
                source_id=edge.source_id,
                target_id=edge.target_id,
                weight=float(edge.weight),
                delay_ms=float(edge.delay_ms),
                plastic=bool(edge.plastic),
                internal=False,
            )
        )

    available = {row.key: row for row in pool}
    pairs: list[EdgeControlPair] = []
    for target in target_rows:
        ranked = sorted(
            available.values(),
            key=lambda control: (
                0 if _sign_class(control.weight) == _sign_class(target.weight) else 1,
                0 if control.plastic == target.plastic else 1,
                abs(abs(control.weight) - abs(target.weight)),
                abs(control.delay_ms - target.delay_ms),
                control.source_id,
                control.target_id,
            ),
        )
        if not ranked:
            raise RouteArchitectureUnreachable(
                "prospective matched non-target control pool is exhausted"
            )
        control = ranked[0]
        pairs.append(EdgeControlPair(target=target, control=control))
        del available[control.key]
    return tuple(pairs)


def opportunity_arc(edge: RouteEdge, source_time_ms: float) -> OpportunityArc:
    return OpportunityArc(
        source_id=edge.source_id,
        source_time_ms=float(source_time_ms),
        target_id=edge.target_id,
        target_time_ms=float(source_time_ms) + edge.delay_ms,
    )


def apply_edge_intervention(
    field: TemporalExcitableField,
    edge: RouteEdge,
    kind: InterventionKind,
) -> RouteEdge:
    """Apply one fixed Architecture perturbation to a cloned field only."""
    current = field.connection(edge.source_id, edge.target_id)
    if float(current.weight) != edge.weight or float(current.delay_ms) != edge.delay_ms:
        raise RouteArchitectureUnreachable("edge drifted after prospective selection")
    if kind == "transmission_null":
        current.weight = 0.0
    elif kind == "delay_plus_1ms":
        current.delay_ms += DELAY_PERTURBATION_MS
    elif kind != "sham":
        raise ValueError(f"unknown intervention kind: {kind}")
    updated = _route_edge(field, edge.source_id, edge.target_id)
    return RouteEdge(**{**updated.as_dict(), "internal": edge.internal})


def freeze_response_signature(observables: Mapping[str, object]) -> FrozenResponseSignature:
    """Serialize a complete response signature deterministically for equivalence checks."""
    payload = canonical_json(dict(observables))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return FrozenResponseSignature(payload_json=payload, sha256=digest)

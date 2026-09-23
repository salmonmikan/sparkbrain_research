from __future__ import annotations

import copy
import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import canonical_json

from .brain import IntegratedV05Brain


class SubthresholdArchitectureUnreachable(RuntimeError):
    """The prospectively bounded non-result Architecture construction is unreachable."""


@dataclass(frozen=True, slots=True)
class QueueCapReport:
    pending_arrivals: int
    max_pending_arrivals: int
    within_cap: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SubthresholdUnitSnapshot:
    unit_id: int
    potential: float
    adaptation: float
    base_threshold: float
    dynamic_threshold: float
    refractory_until_ms: float
    last_update_ms: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class QueueFreeAnchor:
    source_state_hash: str
    clone_state_hash: str
    current_time_ms: float
    pending_arrivals: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FrozenSubthresholdSignature:
    payload_json: str
    sha256: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def pending_arrival_count(brain: IntegratedV05Brain) -> int:
    """Return the serialized queue size without inspecting candidate responses."""
    return len(brain.base.field.state_dict()["queue"])


def enforce_queue_cap(
    brain: IntegratedV05Brain,
    *,
    max_pending_arrivals: int,
) -> QueueCapReport:
    """Fail closed when a caller-supplied prospective queue cap is exceeded.

    This helper intentionally does not choose a scientific cap. The caller must
    supply an already-authorized bound. Candidate #35's queue-free anchor uses
    a cap of zero.
    """
    if isinstance(max_pending_arrivals, bool) or not isinstance(max_pending_arrivals, int):
        raise TypeError("max_pending_arrivals must be an integer")
    if max_pending_arrivals < 0:
        raise ValueError("max_pending_arrivals must be non-negative")
    pending = pending_arrival_count(brain)
    report = QueueCapReport(
        pending_arrivals=pending,
        max_pending_arrivals=max_pending_arrivals,
        within_cap=pending <= max_pending_arrivals,
    )
    if not report.within_cap:
        raise SubthresholdArchitectureUnreachable(
            "pending-arrival queue exceeds the prospectively supplied cap"
        )
    return report


def clone_at_queue_free_anchor(brain: IntegratedV05Brain) -> tuple[IntegratedV05Brain, QueueFreeAnchor]:
    """Clone only an already queue-free state, without advancing the source.

    No settling, cue, candidate response, or adaptive waiting is performed.
    """
    source_hash = brain.state_hash()
    cap = enforce_queue_cap(brain, max_pending_arrivals=0)
    clone = copy.deepcopy(brain)
    clone_hash = clone.state_hash()
    if brain.state_hash() != source_hash:
        raise AssertionError("queue-free anchor construction mutated the source brain")
    if clone_hash != source_hash:
        raise AssertionError("queue-free anchor clone is not state-identical to source")
    return clone, QueueFreeAnchor(
        source_state_hash=source_hash,
        clone_state_hash=clone_hash,
        current_time_ms=float(brain.current_time_ms),
        pending_arrivals=cap.pending_arrivals,
    )


def snapshot_subthreshold_units(
    brain: IntegratedV05Brain,
    unit_ids: tuple[int, ...] | list[int],
) -> tuple[SubthresholdUnitSnapshot, ...]:
    """Serialize only local physical state needed for the ordinary reduction panel."""
    resolved = tuple(sorted({int(unit_id) for unit_id in unit_ids}))
    if not resolved:
        raise ValueError("unit_ids must be non-empty")
    rows: list[SubthresholdUnitSnapshot] = []
    for unit_id in resolved:
        if unit_id not in brain.base.field.units:
            raise KeyError(f"unknown unit_id: {unit_id}")
        unit = brain.base.field.units[unit_id]
        rows.append(
            SubthresholdUnitSnapshot(
                unit_id=unit_id,
                potential=float(unit.potential),
                adaptation=float(unit.adaptation),
                base_threshold=float(unit.base_threshold),
                dynamic_threshold=float(brain.base.field.dynamic_threshold(unit)),
                refractory_until_ms=float(unit.refractory_until_ms),
                last_update_ms=float(unit.last_update_ms),
            )
        )
    return tuple(rows)


def clone_with_subthreshold_reset(
    brain: IntegratedV05Brain,
    unit_ids: tuple[int, ...] | list[int],
) -> IntegratedV05Brain:
    """Return a queue-free clone with only potential/adaptation reset to zero.

    This is non-result Architecture tooling. It does not choose candidate units,
    cue bytes, timing, response criteria, or any SYSTEM-to-MECHANISM uplift.
    """
    clone, _ = clone_at_queue_free_anchor(brain)
    resolved = tuple(sorted({int(unit_id) for unit_id in unit_ids}))
    if not resolved:
        raise ValueError("unit_ids must be non-empty")
    for unit_id in resolved:
        if unit_id not in clone.base.field.units:
            raise KeyError(f"unknown unit_id: {unit_id}")
        unit = clone.base.field.units[unit_id]
        unit.potential = 0.0
        unit.adaptation = 0.0
    enforce_queue_cap(clone, max_pending_arrivals=0)
    return clone


def freeze_subthreshold_signature(
    brain: IntegratedV05Brain,
    unit_ids: tuple[int, ...] | list[int],
) -> FrozenSubthresholdSignature:
    """Create a deterministic, non-evidentiary local-state signature."""
    payload = {
        "candidate_id": "CAND-35-QUEUE-FREE-SUBTHRESHOLD-STATE-CAUSAL-PRIMING",
        "evidentiary_status": "NON_EVIDENTIARY_ARCHITECTURE_ONLY",
        "current_time_ms": float(brain.current_time_ms),
        "pending_arrivals": pending_arrival_count(brain),
        "units": [row.as_dict() for row in snapshot_subthreshold_units(brain, unit_ids)],
        "candidate_response_execution_allowed": False,
        "preformal_execution_allowed": False,
        "formal_action_allowed": False,
    }
    payload_json = canonical_json(payload)
    return FrozenSubthresholdSignature(
        payload_json=payload_json,
        sha256=hashlib.sha256(payload_json.encode("utf-8")).hexdigest(),
    )

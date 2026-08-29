from __future__ import annotations

import copy
import random
from dataclasses import asdict, dataclass
from typing import Any, Literal

from sparkbrain.v04.contracts import SpikeEvent
from sparkbrain.v04.field import TemporalExcitableField

from .foundation import canonical_json, digest, validate_runtime_mapping

QueueMode = Literal["intact", "drained", "shuffled"]


@dataclass(frozen=True, slots=True)
class QueueControlResult:
    """One Field-only continuation condition after the same prefix state."""

    mode: QueueMode
    start_ms: float
    end_ms: float
    initial_queue_count: int
    final_queue_count: int
    spike_count: int
    spike_unit_ids: tuple[int, ...]
    field_state_hash: str
    trace_hash: str

    def as_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["spike_unit_ids"] = list(self.spike_unit_ids)
        return row


@dataclass(frozen=True, slots=True)
class G0Comparison:
    """Matched queue controls for a single immutable prefix Field state."""

    prefix_state_hash: str
    horizon_ms: float
    results: tuple[QueueControlResult, ...]

    def by_mode(self) -> dict[QueueMode, QueueControlResult]:
        return {row.mode: row for row in self.results}

    def as_dict(self) -> dict[str, Any]:
        return {
            "horizon_ms": self.horizon_ms,
            "prefix_state_hash": self.prefix_state_hash,
            "results": [row.as_dict() for row in self.results],
        }

    def state_hash(self) -> str:
        return digest(self.as_dict())


def _queue_count(state: dict[str, Any]) -> int:
    queue = state.get("queue")
    if not isinstance(queue, list):
        raise ValueError("Field state queue must be a list")
    return len(queue)


def field_with_queue_mode(
    field: TemporalExcitableField,
    mode: QueueMode,
    *,
    shuffle_seed: int = 6003,
) -> TemporalExcitableField:
    """Clone a Field while changing only its already-scheduled arrival queue."""

    if mode not in {"intact", "drained", "shuffled"}:
        raise ValueError(f"unsupported queue mode: {mode}")
    state = copy.deepcopy(field.state_dict())
    queue = state["queue"]
    if mode == "drained":
        state["queue"] = []
    elif mode == "shuffled":
        rng = random.Random(shuffle_seed)
        arrivals = [row["arrival"] for row in queue]
        targets = [int(row["target_id"]) for row in arrivals]
        currents = [float(row["current"]) for row in arrivals]
        rng.shuffle(targets)
        rng.shuffle(currents)
        for row, target_id, current in zip(arrivals, targets, currents, strict=True):
            row["target_id"] = target_id
            row["current"] = current
    validate_runtime_mapping(
        {
            "current_time_ms": state["current_time_ms"],
            "queue": state["queue"],
            "units": state["units"],
        },
        path="g0.field_state",
    )
    return TemporalExcitableField.from_state_dict(state)


def run_queue_condition(
    field: TemporalExcitableField,
    *,
    mode: QueueMode,
    end_ms: float,
    shuffle_seed: int = 6003,
) -> QueueControlResult:
    if end_ms < field.current_time_ms:
        raise ValueError("end_ms cannot precede the prefix state")
    candidate = field_with_queue_mode(field, mode, shuffle_seed=shuffle_seed)
    initial_queue_count = _queue_count(candidate.state_dict())
    spikes = candidate.run_until(end_ms)
    trace = _spike_trace(spikes)
    final_state = candidate.state_dict()
    return QueueControlResult(
        mode=mode,
        start_ms=field.current_time_ms,
        end_ms=end_ms,
        initial_queue_count=initial_queue_count,
        final_queue_count=_queue_count(final_state),
        spike_count=len(spikes),
        spike_unit_ids=tuple(row.unit_id for row in spikes),
        field_state_hash=candidate.state_hash(),
        trace_hash=digest(trace),
    )


def compare_queue_controls(
    field: TemporalExcitableField,
    *,
    end_ms: float,
    shuffle_seed: int = 6003,
) -> G0Comparison:
    """Run intact, drained, and shuffled controls from the exact same state."""

    prefix_hash = field.state_hash()
    results = tuple(
        run_queue_condition(
            field,
            mode=mode,
            end_ms=end_ms,
            shuffle_seed=shuffle_seed,
        )
        for mode in ("intact", "drained", "shuffled")
    )
    if field.state_hash() != prefix_hash:
        raise RuntimeError("G0 comparison mutated the prefix Field")
    return G0Comparison(
        prefix_state_hash=prefix_hash,
        horizon_ms=end_ms,
        results=results,
    )


def classify_g0_support(comparison: G0Comparison) -> dict[str, Any]:
    """Engineering interpretation; it is not a scientific acceptance gate."""

    rows = comparison.by_mode()
    intact = rows["intact"].spike_count
    drained = rows["drained"].spike_count
    status = "candidate" if drained > 0 else "not_observed_after_queue_drain"
    return {
        "drained_spikes": drained,
        "intact_spikes": intact,
        "pending_queue_dependency": intact > drained,
        "status": status,
    }


def _spike_trace(spikes: tuple[SpikeEvent, ...]) -> list[dict[str, Any]]:
    # Round-trip through canonical JSON so the returned trace contains only
    # plain JSON values and cannot expose mutable Field objects.
    return [
        __import__("json").loads(canonical_json(row.as_dict()))
        for row in spikes
    ]

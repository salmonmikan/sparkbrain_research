"""Target-free deterministic fading-memory primitives for PD0.1 pre-formal work.

This module deliberately contains no formal experiment identity, task selection, lag grid,
metric, threshold, target access, fitting, or learned recurrent training. Scientific values that
remain under Evidence Analyst authority must be supplied only after prospective authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping, Sequence


_TARGET_LIKE_KEYS = frozenset({"answer", "gold", "label", "outcome", "target", "truth"})


@dataclass(frozen=True)
class FadingMemoryConfig:
    """Configuration for the single deterministic exponential-memory comparator family."""

    decay: float

    def __post_init__(self) -> None:
        if not isfinite(self.decay) or not 0.0 < self.decay < 1.0:
            raise ValueError("decay must be finite and strictly between 0 and 1")


class FadingMemoryComparator:
    """Stateless-across-histories exponential memory with no fitting or target access.

    Within one history, the state transition is ``state = decay * state + observation``.
    A new ``run`` starts from an all-zero state, so no information crosses history boundaries.
    """

    def __init__(self, config: FadingMemoryConfig) -> None:
        self.config = config

    def run(self, observations: Iterable[Sequence[float]]) -> tuple[float, ...]:
        state: list[float] | None = None
        for observation in observations:
            vector = _validated_vector(observation)
            if state is None:
                state = [0.0] * len(vector)
            elif len(vector) != len(state):
                raise ValueError("all observations in one history must have equal dimensions")
            decay = self.config.decay
            state = [decay * previous + current for previous, current in zip(state, vector)]
        if state is None:
            raise ValueError("history must contain at least one observation")
        return tuple(state)


def assert_target_free_record(record: Mapping[str, object]) -> None:
    """Fail closed on obvious target-bearing fields before history/scorability processing."""

    forbidden = sorted(key for key in record if key.casefold() in _TARGET_LIKE_KEYS)
    if forbidden:
        raise ValueError(f"target-like fields are forbidden in pre-target records: {forbidden}")


def stable_history_order(
    records: Iterable[Mapping[str, object]], *, order_field: str
) -> tuple[Mapping[str, object], ...]:
    """Deterministically order target-free records by a caller-selected unique stable field.

    The formal order field is intentionally *not* selected here; that choice remains blocked on
    prospective Evidence Analyst authorization. This utility only enforces deterministic behavior
    after a field is supplied by an authorized protocol or by a clearly synthetic/dev fixture.
    """

    materialized = tuple(records)
    for record in materialized:
        assert_target_free_record(record)
        if order_field not in record:
            raise ValueError(f"missing order field: {order_field}")

    keys = [record[order_field] for record in materialized]
    if len(set(keys)) != len(keys):
        raise ValueError("order field values must be unique within one history")
    try:
        return tuple(sorted(materialized, key=lambda record: record[order_field]))
    except TypeError as exc:
        raise ValueError("order field values must be mutually orderable") from exc


@dataclass(frozen=True)
class TargetFreeInventory:
    """Target-free cardinality accounting for a proposed history universe."""

    history_count: int
    observation_count: int


def inventory_histories(
    histories: Iterable[Sequence[Mapping[str, object]]],
) -> TargetFreeInventory:
    """Count histories/observations without reading targets or defining a scientific score."""

    history_count = 0
    observation_count = 0
    for history in histories:
        history_count += 1
        observation_count += len(history)
        for record in history:
            assert_target_free_record(record)
    return TargetFreeInventory(
        history_count=history_count,
        observation_count=observation_count,
    )


def _validated_vector(values: Sequence[float]) -> tuple[float, ...]:
    if not values:
        raise ValueError("observation vectors must be non-empty")
    vector = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in vector):
        raise ValueError("observation vectors must contain only finite values")
    return vector

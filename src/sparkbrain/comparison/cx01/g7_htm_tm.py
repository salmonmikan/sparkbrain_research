from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from typing import Any

from .contract import ComparatorKind
from .events import ComparatorEvent, EventOrigin, PredictionDistribution


@dataclass(frozen=True, slots=True)
class HTMTemporalMemoryConfig:
    active_columns_per_token: int = 16
    cells_per_column: int = 32
    activation_threshold: int = 12
    max_new_synapse_count: int = 16
    initial_permanence: float = 0.21
    connected_permanence: float = 0.50
    permanence_increment: float = 0.10
    maximum_rollout_steps: int = 8

    def validate(self) -> None:
        if self.active_columns_per_token < 1 or self.cells_per_column < 2:
            raise ValueError("HTM token SDR geometry is invalid")
        if not 1 <= self.activation_threshold <= self.active_columns_per_token:
            raise ValueError("HTM activation threshold must fit the token SDR width")
        if self.max_new_synapse_count < self.activation_threshold:
            raise ValueError("max_new_synapse_count cannot undercut activation threshold")
        for value in (
            self.initial_permanence,
            self.connected_permanence,
            self.permanence_increment,
        ):
            if not math.isfinite(value) or value < 0:
                raise ValueError("permanence values must be finite and non-negative")
        if self.maximum_rollout_steps < 1:
            raise ValueError("maximum_rollout_steps must be positive")


@dataclass(slots=True)
class _Segment:
    presynaptic_cells: tuple[int, ...]
    target_token: str
    permanence: float
    observations: int

    def connected_overlap(self, active_cells: tuple[int, ...], threshold: float) -> int:
        if self.permanence < threshold:
            return 0
        return len(set(self.presynaptic_cells).intersection(active_cells))


class HTMTemporalMemoryComparator:
    """Minimal independent Temporal-Memory capability reference for CX01.

    This is not `htm.core` and does not implement Spatial Pooling. Anonymous
    tokens map deterministically to fixed sparse columns. Context-dependent
    winner cells and distal-like segments provide high-order sequence state.
    Evaluation observations may advance sparse context without changing learned
    segment state.

    Only parameters that are actually active in this compact implementation are
    exposed. Full HTM bursting/matching-segment punishment and predicted-segment
    decrement mechanisms are outside this comparator's fidelity claim.
    """

    kind = ComparatorKind.G7_HTM_TEMPORAL_MEMORY

    def __init__(self, config: HTMTemporalMemoryConfig | None = None) -> None:
        self.config = config or HTMTemporalMemoryConfig()
        self.config.validate()
        self._segments: dict[tuple[tuple[int, ...], str], _Segment] = {}
        self._active_cells: tuple[int, ...] = ()
        self._last_token: str | None = None
        self._known_tokens: set[str] = set()
        self._time_ms = 0.0
        self._suppressed: set[str] = set()
        self._observed_events = 0
        self._generated_events = 0

    @staticmethod
    def _hash_int(*parts: object) -> int:
        text = "|".join(str(part) for part in parts).encode("utf-8")
        return int(hashlib.sha256(text).hexdigest()[:16], 16)

    def token_columns(self, token: str) -> tuple[int, ...]:
        if not token:
            raise ValueError("token must be non-empty")
        columns: list[int] = []
        nonce = 0
        while len(columns) < self.config.active_columns_per_token:
            column = self._hash_int("column", token, nonce) % 1_000_003
            if column not in columns:
                columns.append(column)
            nonce += 1
        return tuple(sorted(columns))

    def _context_fingerprint(self, cells: tuple[int, ...]) -> str:
        if not cells:
            return "ROOT"
        payload = ",".join(str(cell) for cell in cells).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:24]

    def _winner_cells(self, token: str, previous_cells: tuple[int, ...]) -> tuple[int, ...]:
        fingerprint = self._context_fingerprint(previous_cells)
        winners = []
        for column in self.token_columns(token):
            cell_index = (
                self._hash_int("cell", token, column, fingerprint) % self.config.cells_per_column
            )
            winners.append(column * self.config.cells_per_column + cell_index)
        return tuple(sorted(winners))

    def _learn(self, previous_cells: tuple[int, ...], target: str) -> None:
        if not previous_cells:
            return
        key = (previous_cells, target)
        segment = self._segments.get(key)
        if segment is None:
            segment = _Segment(
                presynaptic_cells=previous_cells[: self.config.max_new_synapse_count],
                target_token=target,
                permanence=min(
                    1.0, self.config.initial_permanence + self.config.permanence_increment
                ),
                observations=1,
            )
            self._segments[key] = segment
        else:
            segment.permanence = min(1.0, segment.permanence + self.config.permanence_increment)
            segment.observations += 1

    def observe_external(self, event: ComparatorEvent, *, learn: bool = True) -> None:
        event.validate()
        if event.origin is not EventOrigin.EXTERNAL:
            raise ValueError("G7 accepts external observations only")
        if event.timestamp_ms < self._time_ms:
            raise ValueError("events must be chronological")
        if event.episode_start:
            self._active_cells = ()
            self._last_token = None
        previous = self._active_cells
        if learn:
            self._learn(previous, event.token)
        self._active_cells = self._winner_cells(event.token, previous)
        self._last_token = event.token
        self._known_tokens.add(event.token)
        self._time_ms = event.timestamp_ms
        self._observed_events += 1

    def finalize_episode(self) -> None:
        self._active_cells = ()
        self._last_token = None

    def advance(self, timestamp_ms: float) -> None:
        if not math.isfinite(timestamp_ms) or timestamp_ms < self._time_ms:
            raise ValueError("time must be finite and monotonic")
        self._time_ms = timestamp_ms

    def _scores_for(
        self, active_cells: tuple[int, ...], last_token: str | None
    ) -> dict[str, float]:
        if not active_cells or last_token in self._suppressed:
            return {}
        scores: dict[str, float] = {}
        for segment in self._segments.values():
            overlap = segment.connected_overlap(active_cells, self.config.connected_permanence)
            if overlap < self.config.activation_threshold:
                continue
            scores[segment.target_token] = scores.get(segment.target_token, 0.0) + (
                float(overlap) * segment.permanence * segment.observations
            )
        return scores

    def distribution(self) -> PredictionDistribution:
        return PredictionDistribution.from_scores(
            self._scores_for(self._active_cells, self._last_token)
        )

    def generate(self, *, max_steps: int = 1) -> tuple[ComparatorEvent, ...]:
        if max_steps < 0 or max_steps > self.config.maximum_rollout_steps:
            raise ValueError("rollout steps exceed configured bound")
        virtual_cells = self._active_cells
        virtual_last = self._last_token
        events: list[ComparatorEvent] = []
        for index in range(max_steps):
            distribution = PredictionDistribution.from_scores(
                self._scores_for(virtual_cells, virtual_last)
            ).as_dict()
            if not distribution:
                break
            token = min(distribution, key=lambda candidate: (-distribution[candidate], candidate))
            events.append(
                ComparatorEvent(
                    token=token,
                    timestamp_ms=self._time_ms + float(index + 1),
                    origin=EventOrigin.GENERATED,
                )
            )
            virtual_cells = self._winner_cells(token, virtual_cells)
            virtual_last = token
        self._generated_events += len(events)
        return tuple(events)

    def suppress(self, token: str) -> None:
        if not token:
            raise ValueError("suppressed token must be non-empty")
        self._suppressed.add(token)

    def clear_suppression(self) -> None:
        self._suppressed.clear()

    def _segment_rows(self) -> list[dict[str, Any]]:
        return [
            {
                "observations": segment.observations,
                "permanence": segment.permanence,
                "presynaptic_cells": list(segment.presynaptic_cells),
                "target_token": segment.target_token,
            }
            for _, segment in sorted(self._segments.items())
        ]

    def learned_state_dict(self) -> dict[str, Any]:
        return {"segments": self._segment_rows()}

    def snapshot(self) -> dict[str, Any]:
        return {
            "active_cells": list(self._active_cells),
            "config": asdict(self.config),
            "generated_events": self._generated_events,
            "kind": self.kind.value,
            "known_tokens": sorted(self._known_tokens),
            "last_token": self._last_token,
            "observed_events": self._observed_events,
            "segments": self._segment_rows(),
            "suppressed": sorted(self._suppressed),
            "time_ms": self._time_ms,
        }

    def restore(self, state: dict[str, Any]) -> None:
        if state.get("kind") != self.kind.value:
            raise ValueError("snapshot kind mismatch")
        self.config = HTMTemporalMemoryConfig(**state["config"])
        self.config.validate()
        self._segments = {}
        for row in state["segments"]:
            segment = _Segment(
                presynaptic_cells=tuple(int(cell) for cell in row["presynaptic_cells"]),
                target_token=str(row["target_token"]),
                permanence=float(row["permanence"]),
                observations=int(row["observations"]),
            )
            self._segments[(segment.presynaptic_cells, segment.target_token)] = segment
        self._active_cells = tuple(int(cell) for cell in state["active_cells"])
        self._known_tokens = set(str(token) for token in state["known_tokens"])
        self._last_token = state["last_token"]
        self._suppressed = set(str(token) for token in state["suppressed"])
        self._time_ms = float(state["time_ms"])
        self._observed_events = int(state["observed_events"])
        self._generated_events = int(state["generated_events"])

    @property
    def parameter_count(self) -> int:
        return len(self._segments) * self.config.max_new_synapse_count

    @property
    def state_entry_count(self) -> int:
        return self.parameter_count + len(self._active_cells)

    @property
    def observed_external_events(self) -> int:
        return self._observed_events

    @property
    def generated_internal_events(self) -> int:
        return self._generated_events

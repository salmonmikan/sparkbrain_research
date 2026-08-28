from __future__ import annotations

import hashlib
import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from typing import Any

from sparkbrain.v04.contracts import CascadeEvent, SpikeEvent, canonical_json

from .contracts import ActivityPattern, AssemblyActivation


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _edit_similarity(left: tuple[int, ...], right: tuple[int, ...]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, start=1):
        current = [i]
        for j, b in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (a != b),
                )
            )
        previous = current
    return 1.0 - previous[-1] / max(len(left), len(right))


def _jaccard(left: tuple[int, ...], right: tuple[int, ...]) -> float:
    a, b = set(left), set(right)
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def _timing_similarity(left: ActivityPattern, right: ActivityPattern) -> float:
    """Compare relative timing, allowing one-event partial observations.

    When lengths differ, the shorter unit sequence must be an ordered
    subsequence of the longer sequence.  This permits bounded pattern
    completion without treating an unordered subset as equivalent.
    """
    if not left.relative_bins and not right.relative_bins:
        return 1.0
    if not left.relative_bins or not right.relative_bins:
        return 0.0
    if len(left.relative_bins) == len(right.relative_bins):
        error = sum(
            abs(a - b) for a, b in zip(left.relative_bins, right.relative_bins, strict=True)
        ) / len(left.relative_bins)
        return math.exp(-error / 2.0)

    short, long = (
        (left, right) if len(left.ordered_units) < len(right.ordered_units) else (right, left)
    )
    if len(short.ordered_units) < 2:
        return 0.0
    from itertools import combinations

    best = 0.0
    for indices in combinations(range(len(long.ordered_units)), len(short.ordered_units)):
        if tuple(long.ordered_units[i] for i in indices) != short.ordered_units:
            continue
        selected = tuple(long.relative_bins[i] for i in indices)
        selected = tuple(value - selected[0] for value in selected)
        short_bins = tuple(value - short.relative_bins[0] for value in short.relative_bins)
        error = sum(abs(a - b) for a, b in zip(selected, short_bins, strict=True)) / len(short_bins)
        best = max(best, math.exp(-error / 4.0))
    return best


def pattern_similarity(left: ActivityPattern, right: ActivityPattern) -> float:
    """Compare internal spatiotemporal Spark sequences without semantic labels."""
    return (
        0.55 * _edit_similarity(left.ordered_units, right.ordered_units)
        + 0.25 * _jaccard(left.unit_ids, right.unit_ids)
        + 0.20 * _timing_similarity(left, right)
    )


def pattern_from_spikes(
    spikes: Iterable[SpikeEvent],
    *,
    source_cascade_id: str | None = None,
    temporal_bin_ms: float = 2.0,
    source_kind: str = "internal_reservoir",
) -> ActivityPattern | None:
    rows = sorted(spikes, key=lambda row: (row.time_ms, row.unit_id))
    if len(rows) < 2:
        return None
    start = rows[0].time_ms
    sequence = [[row.unit_id, int(round((row.time_ms - start) / temporal_bin_ms))] for row in rows]
    payload = {
        "sequence": sequence,
        "source_cascade_id": source_cascade_id,
        "source_kind": source_kind,
    }
    return ActivityPattern(
        pattern_id=f"pattern-{_digest(payload)[:16]}",
        start_ms=start,
        end_ms=rows[-1].time_ms,
        ordered_units=tuple(row.unit_id for row in rows),
        relative_bins=tuple(item[1] for item in sequence),
        unit_ids=tuple(sorted({row.unit_id for row in rows})),
        spike_count=len(rows),
        source_cascade_id=source_cascade_id,
        source_kind=source_kind,
    )


def patterns_from_step(
    cascades: Iterable[CascadeEvent],
    spikes: Iterable[SpikeEvent],
    *,
    temporal_bin_ms: float = 2.0,
    excluded_unit_ids: Iterable[int] = (),
    source_kind: str = "internal_reservoir",
) -> tuple[ActivityPattern, ...]:
    """Extract Assembly candidates from internal Sparks, never direct receptors.

    Receptor rows are intentionally excluded from the primary v0.5 Assembly
    track.  Otherwise the detector can merely memorize the presented input
    sequence instead of discovering a recurrent internal response.
    """
    excluded = set(excluded_unit_ids)
    spike_rows = tuple(row for row in spikes if row.unit_id not in excluded)
    patterns: list[ActivityPattern] = []
    for cascade in cascades:
        rows = [
            spike
            for spike in spike_rows
            if cascade.start_ms - 1e-9 <= spike.time_ms <= cascade.end_ms + 1e-9
            and spike.unit_id in cascade.unit_ids
        ]
        pattern = pattern_from_spikes(
            rows,
            source_cascade_id=cascade.cascade_id,
            temporal_bin_ms=temporal_bin_ms,
            source_kind=source_kind,
        )
        if pattern is not None:
            patterns.append(pattern)
    if not patterns:
        fallback = pattern_from_spikes(
            spike_rows,
            temporal_bin_ms=temporal_bin_ms,
            source_kind=source_kind,
        )
        if fallback is not None:
            patterns.append(fallback)
    return tuple(patterns)


@dataclass(frozen=True, slots=True)
class AssemblyConfig:
    similarity_threshold: float = 0.66
    mature_episodes: int = 3
    max_candidates: int = 256
    stale_after_ms: float = 50_000.0
    immature_stale_episodes: int = 2


@dataclass(slots=True)
class AssemblyCandidate:
    assembly_id: str
    prototype: ActivityPattern
    occurrences: int
    episode_ids: set[str]
    first_seen_ms: float
    last_seen_ms: float
    similarity_sum: float = 1.0

    @property
    def episode_count(self) -> int:
        return len(self.episode_ids)

    @property
    def mean_similarity(self) -> float:
        return self.similarity_sum / max(1, self.occurrences)

    def as_dict(self) -> dict[str, Any]:
        return {
            "assembly_id": self.assembly_id,
            "episode_count": self.episode_count,
            "episode_ids": sorted(self.episode_ids),
            "first_seen_ms": self.first_seen_ms,
            "last_seen_ms": self.last_seen_ms,
            "mean_similarity": self.mean_similarity,
            "occurrences": self.occurrences,
            "prototype": self.prototype.as_dict(),
            "similarity_sum": self.similarity_sum,
        }


@dataclass(slots=True)
class TemporalAssemblyMemory:
    config: AssemblyConfig = field(default_factory=AssemblyConfig)
    candidates: dict[str, AssemblyCandidate] = field(default_factory=dict)
    suppressed: set[str] = field(default_factory=set)
    next_id: int = 1

    def _new_candidate(
        self,
        pattern: ActivityPattern,
        time_ms: float,
        episode_id: str,
    ) -> AssemblyCandidate:
        assembly_id = f"assembly-{self.next_id:04d}"
        self.next_id += 1
        candidate = AssemblyCandidate(
            assembly_id=assembly_id,
            prototype=pattern,
            occurrences=1,
            episode_ids={episode_id},
            first_seen_ms=time_ms,
            last_seen_ms=time_ms,
        )
        self.candidates[assembly_id] = candidate
        return candidate

    def best_match(self, pattern: ActivityPattern) -> tuple[AssemblyCandidate | None, float]:
        best: AssemblyCandidate | None = None
        best_score = -1.0
        for candidate in self.candidates.values():
            score = pattern_similarity(candidate.prototype, pattern)
            if score > best_score or (
                score == best_score
                and best is not None
                and candidate.assembly_id < best.assembly_id
            ):
                best = candidate
                best_score = score
        return best, max(0.0, best_score)

    def observe(
        self,
        pattern: ActivityPattern,
        *,
        time_ms: float,
        episode_id: str,
        learn: bool = True,
    ) -> AssemblyActivation | None:
        if not episode_id:
            raise ValueError("episode_id must be non-empty")
        candidate, similarity = self.best_match(pattern)
        if candidate is None or similarity < self.config.similarity_threshold:
            if not learn:
                return None
            if len(self.candidates) >= self.config.max_candidates:
                self.prune(time_ms)
            if len(self.candidates) >= self.config.max_candidates:
                return None
            candidate = self._new_candidate(pattern, time_ms, episode_id)
            similarity = 1.0
        elif learn:
            candidate.occurrences += 1
            candidate.episode_ids.add(episode_id)
            candidate.last_seen_ms = time_ms
            candidate.similarity_sum += similarity
        mature = candidate.episode_count >= self.config.mature_episodes
        return AssemblyActivation(
            assembly_id=candidate.assembly_id,
            pattern_id=pattern.pattern_id,
            time_ms=time_ms,
            similarity=similarity,
            occurrences=candidate.occurrences,
            episode_count=candidate.episode_count,
            mature=mature,
            unit_ids=candidate.prototype.unit_ids,
            suppressed=candidate.assembly_id in self.suppressed,
        )

    def prune(self, time_ms: float) -> None:
        removable = [
            candidate.assembly_id
            for candidate in self.candidates.values()
            if candidate.episode_count <= self.config.immature_stale_episodes
            and time_ms - candidate.last_seen_ms > self.config.stale_after_ms
        ]
        for assembly_id in removable:
            del self.candidates[assembly_id]
            self.suppressed.discard(assembly_id)

    def suppress(self, assembly_id: str) -> None:
        if assembly_id not in self.candidates:
            raise KeyError(assembly_id)
        self.suppressed.add(assembly_id)

    def unsuppress(self, assembly_id: str) -> None:
        self.suppressed.discard(assembly_id)

    def state_dict(self) -> dict[str, Any]:
        return {
            "candidates": {key: value.as_dict() for key, value in sorted(self.candidates.items())},
            "config": asdict(self.config),
            "next_id": self.next_id,
            "suppressed": sorted(self.suppressed),
        }

    @classmethod
    def from_state_dict(cls, value: dict[str, Any]) -> TemporalAssemblyMemory:
        config = dict(value["config"])
        # Development checkpoint compatibility for the first v0.5 draft.
        if "mature_occurrences" in config:
            config["mature_episodes"] = config.pop("mature_occurrences")
        if "immature_stale_occurrences" in config:
            config["immature_stale_episodes"] = config.pop("immature_stale_occurrences")
        row = cls(AssemblyConfig(**config))
        row.next_id = int(value["next_id"])
        row.suppressed = set(value["suppressed"])
        for key, candidate in value["candidates"].items():
            pattern_row = dict(candidate["prototype"])
            for name in ("ordered_units", "relative_bins", "unit_ids"):
                pattern_row[name] = tuple(pattern_row[name])
            row.candidates[key] = AssemblyCandidate(
                assembly_id=str(candidate["assembly_id"]),
                prototype=ActivityPattern(**pattern_row),
                occurrences=int(candidate["occurrences"]),
                episode_ids=set(candidate.get("episode_ids", [])),
                first_seen_ms=float(candidate["first_seen_ms"]),
                last_seen_ms=float(candidate["last_seen_ms"]),
                similarity_sum=float(candidate["similarity_sum"]),
            )
        return row

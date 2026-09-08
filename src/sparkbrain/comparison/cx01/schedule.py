from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ScheduledEpisode:
    episode_index: int
    sequence_index: int
    exposure_index: int

    def state_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BalancedExposureSchedule:
    exposure_counts: tuple[int, ...]
    episodes: tuple[ScheduledEpisode, ...]

    def validate(self) -> None:
        if not self.exposure_counts:
            raise ValueError("schedule requires at least one sequence")
        if any(count < 1 for count in self.exposure_counts):
            raise ValueError("schedule exposure counts must be positive")
        if len(self.episodes) != sum(self.exposure_counts):
            raise ValueError("schedule is incomplete")
        observed = [0] * len(self.exposure_counts)
        for index, episode in enumerate(self.episodes):
            if episode.episode_index != index:
                raise ValueError("episode indices must be contiguous")
            if not 0 <= episode.sequence_index < len(self.exposure_counts):
                raise ValueError("sequence index is invalid")
            if episode.exposure_index != observed[episode.sequence_index]:
                raise ValueError("per-sequence exposure indices must be contiguous")
            observed[episode.sequence_index] += 1
        if tuple(observed) != self.exposure_counts:
            raise ValueError("observed exposure counts do not match declaration")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "episodes": [episode.state_dict() for episode in self.episodes],
            "exposure_counts": list(self.exposure_counts),
        }

    def schedule_hash(self) -> str:
        encoded = json.dumps(
            self.state_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def build_balanced_exposure_schedule(
    exposure_counts: tuple[int, ...],
) -> BalancedExposureSchedule:
    """Interleave exposures by round and alternate traversal direction.

    This preserves the fairness repair learned during v0.6 development while
    remaining independent of any comparator implementation.
    """

    if not exposure_counts or any(count < 1 for count in exposure_counts):
        raise ValueError("positive exposure counts are required")
    observed = [0] * len(exposure_counts)
    episodes: list[ScheduledEpisode] = []
    for round_index in range(max(exposure_counts)):
        order = tuple(range(len(exposure_counts)))
        if round_index % 2:
            order = tuple(reversed(order))
        for sequence_index in order:
            if observed[sequence_index] >= exposure_counts[sequence_index]:
                continue
            episodes.append(
                ScheduledEpisode(
                    episode_index=len(episodes),
                    sequence_index=sequence_index,
                    exposure_index=observed[sequence_index],
                )
            )
            observed[sequence_index] += 1
    schedule = BalancedExposureSchedule(exposure_counts, tuple(episodes))
    schedule.validate()
    return schedule

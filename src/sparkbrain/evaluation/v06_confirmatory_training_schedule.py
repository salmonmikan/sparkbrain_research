from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest


@dataclass(frozen=True, slots=True)
class TrainingEpisode:
    episode_index: int
    path_index: int
    exposure_index: int
    lag_profile_index: int

    def state_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BalancedTrainingSchedule:
    """Architecture-independent chronological exposure schedule.

    Paths are interleaved by exposure round. Traversal direction alternates on
    each round to reduce path-order recency bias. If one path has more total
    exposures, its remaining episodes appear only after all competitors have
    exhausted their preregistered counts.
    """

    path_count: int
    exposure_counts: tuple[int, ...]
    lag_profile_count: int
    episodes: tuple[TrainingEpisode, ...]

    def validate(self) -> None:
        if self.path_count < 1:
            raise ValueError("training schedule requires at least one path")
        if len(self.exposure_counts) != self.path_count:
            raise ValueError("one exposure count is required per path")
        if any(count < 1 for count in self.exposure_counts):
            raise ValueError("exposure counts must be positive")
        if self.lag_profile_count < 1:
            raise ValueError("at least one lag profile is required")
        if len(self.episodes) != sum(self.exposure_counts):
            raise ValueError("training schedule episode count is incomplete")
        if tuple(row.episode_index for row in self.episodes) != tuple(
            range(len(self.episodes))
        ):
            raise ValueError("episode indices must be contiguous")
        observed = [0] * self.path_count
        for row in self.episodes:
            if not 0 <= row.path_index < self.path_count:
                raise ValueError("training schedule path index is invalid")
            if row.exposure_index != observed[row.path_index]:
                raise ValueError("per-path exposure indices must be contiguous")
            if row.lag_profile_index != row.episode_index % self.lag_profile_count:
                raise ValueError("lag profile assignment must be deterministic")
            observed[row.path_index] += 1
        if tuple(observed) != self.exposure_counts:
            raise ValueError("training schedule exposure counts do not match")

    def state_dict(self) -> dict[str, Any]:
        return {
            "episodes": [row.state_dict() for row in self.episodes],
            "exposure_counts": list(self.exposure_counts),
            "lag_profile_count": self.lag_profile_count,
            "path_count": self.path_count,
        }

    def schedule_hash(self) -> str:
        return digest(self.state_dict())


def build_balanced_training_schedule(
    exposure_counts: tuple[int, ...],
    *,
    lag_profile_count: int,
) -> BalancedTrainingSchedule:
    if not exposure_counts:
        raise ValueError("training schedule requires exposure counts")
    if any(count < 1 for count in exposure_counts):
        raise ValueError("training exposure counts must be positive")
    if lag_profile_count < 1:
        raise ValueError("training schedule requires a lag profile")

    observed = [0] * len(exposure_counts)
    episodes: list[TrainingEpisode] = []
    for round_index in range(max(exposure_counts)):
        path_indices = tuple(range(len(exposure_counts)))
        if round_index % 2 == 1:
            path_indices = tuple(reversed(path_indices))
        for path_index in path_indices:
            if observed[path_index] >= exposure_counts[path_index]:
                continue
            episode_index = len(episodes)
            episodes.append(
                TrainingEpisode(
                    episode_index=episode_index,
                    path_index=path_index,
                    exposure_index=observed[path_index],
                    lag_profile_index=episode_index % lag_profile_count,
                )
            )
            observed[path_index] += 1

    schedule = BalancedTrainingSchedule(
        path_count=len(exposure_counts),
        exposure_counts=exposure_counts,
        lag_profile_count=lag_profile_count,
        episodes=tuple(episodes),
    )
    schedule.validate()
    return schedule

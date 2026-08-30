from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory_heldout_spec import (
    HeldoutWorldParameters,
    build_heldout_world_grid,
)
from .v06_confirmatory_training_schedule import (
    BalancedTrainingSchedule,
    build_balanced_training_schedule,
)

SCHEDULE_CONTRACT_VERSION = "v06-balanced-chronological-schedule-1"


@dataclass(frozen=True, slots=True)
class ContingencyEpisode:
    episode_index: int
    phase_index: int
    phase_episode_index: int
    target: int
    spacing_index: int
    spacing_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class WorldScheduleContract:
    version: str
    family_id: str
    seed: int
    world_specification_hash: str
    branch_paths: tuple[tuple[int, int, int, int], ...]
    branch_and_control_paths: tuple[tuple[int, int, int, int], ...]
    branch_and_control_exposure_counts: tuple[int, ...]
    branch_training_schedule: BalancedTrainingSchedule
    main_single_path_schedule: BalancedTrainingSchedule
    alternate_single_path_schedule: BalancedTrainingSchedule
    control_single_path_schedule: BalancedTrainingSchedule
    contingency_episodes: tuple[ContingencyEpisode, ...]

    def validate(self) -> None:
        if self.version != SCHEDULE_CONTRACT_VERSION:
            raise ValueError("schedule contract version mismatch")
        if not self.family_id or self.seed < 0:
            raise ValueError("schedule identity must be valid")
        if len(self.world_specification_hash) != 64:
            raise ValueError("world specification hash must be SHA-256")
        if not self.branch_paths:
            raise ValueError("schedule requires at least one branch")
        if self.branch_and_control_paths != (*self.branch_paths, self.branch_and_control_paths[-1]):
            raise ValueError("branch/control schedule path ordering is malformed")
        if len(self.branch_and_control_exposure_counts) != len(
            self.branch_and_control_paths
        ):
            raise ValueError("schedule exposure counts must align with paths")
        for schedule in (
            self.branch_training_schedule,
            self.main_single_path_schedule,
            self.alternate_single_path_schedule,
            self.control_single_path_schedule,
        ):
            schedule.validate()
        if self.branch_training_schedule.exposure_counts != (
            self.branch_and_control_exposure_counts
        ):
            raise ValueError("branch schedule exposure counts changed")
        if tuple(row.episode_index for row in self.contingency_episodes) != tuple(
            range(len(self.contingency_episodes))
        ):
            raise ValueError("contingency episode indices must be contiguous")
        if any(row.spacing_ms <= 0 for row in self.contingency_episodes):
            raise ValueError("contingency spacing must be positive")

    def state_dict(self) -> dict[str, Any]:
        return {
            "alternate_single_path_schedule": (
                self.alternate_single_path_schedule.state_dict()
            ),
            "branch_and_control_exposure_counts": list(
                self.branch_and_control_exposure_counts
            ),
            "branch_and_control_paths": [
                list(path) for path in self.branch_and_control_paths
            ],
            "branch_paths": [list(path) for path in self.branch_paths],
            "branch_training_schedule": self.branch_training_schedule.state_dict(),
            "contingency_episodes": [
                row.state_dict() for row in self.contingency_episodes
            ],
            "control_single_path_schedule": self.control_single_path_schedule.state_dict(),
            "family_id": self.family_id,
            "main_single_path_schedule": self.main_single_path_schedule.state_dict(),
            "seed": self.seed,
            "version": self.version,
            "world_specification_hash": self.world_specification_hash,
        }

    def contract_hash(self) -> str:
        self.validate()
        return digest(self.state_dict())


def _default_single_path_exposure_count(
    parameters: HeldoutWorldParameters,
) -> int:
    return max(3, len(parameters.training_lag_profiles_ms))


def _contingency_episodes(
    parameters: HeldoutWorldParameters,
) -> tuple[ContingencyEpisode, ...]:
    rows: list[ContingencyEpisode] = []
    for phase_index, (target, phase_length) in enumerate(
        zip(
            parameters.contingency_cycle_targets,
            parameters.contingency_phase_lengths,
            strict=True,
        )
    ):
        for phase_episode_index in range(phase_length):
            episode_index = len(rows)
            spacing_index = episode_index % len(parameters.episode_spacings_ms)
            rows.append(
                ContingencyEpisode(
                    episode_index=episode_index,
                    phase_index=phase_index,
                    phase_episode_index=phase_episode_index,
                    target=target,
                    spacing_index=spacing_index,
                    spacing_ms=parameters.episode_spacings_ms[spacing_index],
                )
            )
    return tuple(rows)


def build_world_schedule_contract(
    parameters: HeldoutWorldParameters,
) -> WorldScheduleContract:
    parameters.validate()
    default_count = _default_single_path_exposure_count(parameters)
    branch_paths = tuple(parameters.competition_paths)
    branch_and_control_paths = (*branch_paths, parameters.control_path)
    branch_and_control_counts = (
        *parameters.branch_exposure_counts,
        default_count,
    )
    contract = WorldScheduleContract(
        version=SCHEDULE_CONTRACT_VERSION,
        family_id=parameters.family_id,
        seed=parameters.seed,
        world_specification_hash=parameters.specification_hash(),
        branch_paths=branch_paths,
        branch_and_control_paths=branch_and_control_paths,
        branch_and_control_exposure_counts=branch_and_control_counts,
        branch_training_schedule=build_balanced_training_schedule(
            branch_and_control_counts,
            lag_profile_count=len(parameters.training_lag_profiles_ms),
        ),
        main_single_path_schedule=build_balanced_training_schedule(
            (default_count,),
            lag_profile_count=len(parameters.training_lag_profiles_ms),
        ),
        alternate_single_path_schedule=build_balanced_training_schedule(
            (default_count,),
            lag_profile_count=len(parameters.training_lag_profiles_ms),
        ),
        control_single_path_schedule=build_balanced_training_schedule(
            (default_count,),
            lag_profile_count=len(parameters.training_lag_profiles_ms),
        ),
        contingency_episodes=_contingency_episodes(parameters),
    )
    contract.validate()
    return contract


def build_schedule_contract_grid() -> tuple[WorldScheduleContract, ...]:
    return tuple(
        build_world_schedule_contract(parameters)
        for parameters in build_heldout_world_grid()
    )


def training_schedule_grid_hash() -> str:
    return digest(
        {
            "version": SCHEDULE_CONTRACT_VERSION,
            "worlds": [row.state_dict() for row in build_schedule_contract_grid()],
        }
    )

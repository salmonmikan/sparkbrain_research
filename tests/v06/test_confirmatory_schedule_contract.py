from __future__ import annotations

from collections import Counter

from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELDOUT_FAMILIES,
    HELDOUT_SEEDS,
    build_heldout_world_grid,
)
from sparkbrain.evaluation.v06_confirmatory_schedule_contract import (
    SCHEDULE_CONTRACT_VERSION,
    build_schedule_contract_grid,
    build_world_schedule_contract,
    training_schedule_grid_hash,
)


def test_schedule_grid_covers_all_fifty_candidate_worlds_without_capability() -> None:
    worlds = build_heldout_world_grid()
    schedules = build_schedule_contract_grid()
    assert len(worlds) == len(schedules) == 50
    assert {(row.family_id, row.seed) for row in schedules} == {
        (family_id, seed)
        for family_id in HELDOUT_FAMILIES
        for seed in HELDOUT_SEEDS
    }
    assert all(row.version == SCHEDULE_CONTRACT_VERSION for row in schedules)
    assert all(len(row.contract_hash()) == 64 for row in schedules)


def test_concrete_chronological_order_is_deterministic_and_hashed() -> None:
    first = build_schedule_contract_grid()
    second = build_schedule_contract_grid()
    assert first == second
    assert training_schedule_grid_hash() == training_schedule_grid_hash()
    assert len(training_schedule_grid_hash()) == 64
    assert len({row.contract_hash() for row in first}) == 50


def test_branch_schedule_preserves_exact_exposure_counts_and_control_path() -> None:
    for world in build_heldout_world_grid():
        contract = build_world_schedule_contract(world)
        expected_counts = (
            *world.branch_exposure_counts,
            max(3, len(world.training_lag_profiles_ms)),
        )
        assert contract.branch_paths == world.competition_paths
        assert contract.branch_and_control_paths == (
            *world.competition_paths,
            world.control_path,
        )
        assert contract.branch_and_control_exposure_counts == expected_counts
        assert Counter(
            row.path_index for row in contract.branch_training_schedule.episodes
        ) == {
            index: count for index, count in enumerate(expected_counts)
        }


def test_schedule_freezes_lag_assignment_and_contingency_order() -> None:
    for world in build_heldout_world_grid():
        contract = build_world_schedule_contract(world)
        assert tuple(
            row.lag_profile_index
            for row in contract.branch_training_schedule.episodes
        ) == tuple(
            index % len(world.training_lag_profiles_ms)
            for index in range(len(contract.branch_training_schedule.episodes))
        )
        assert tuple(row.target for row in contract.contingency_episodes) == tuple(
            target
            for target, phase_length in zip(
                world.contingency_cycle_targets,
                world.contingency_phase_lengths,
                strict=True,
            )
            for _ in range(phase_length)
        )
        assert tuple(row.spacing_index for row in contract.contingency_episodes) == tuple(
            index % len(world.episode_spacings_ms)
            for index in range(len(contract.contingency_episodes))
        )


def test_branch_competition_schedule_interleaves_before_residual_exposures() -> None:
    worlds = tuple(
        world
        for world in build_heldout_world_grid()
        if world.family_id == "heldout-branch-competition"
    )
    for world in worlds:
        schedule = build_world_schedule_contract(world).branch_training_schedule
        shared_rounds = min(world.branch_exposure_counts)
        branch_only_prefix = tuple(
            row
            for row in schedule.episodes
            if row.path_index < len(world.competition_paths)
        )[: shared_rounds * len(world.competition_paths)]
        counts = Counter(row.path_index for row in branch_only_prefix)
        assert counts == {
            index: shared_rounds for index in range(len(world.competition_paths))
        }

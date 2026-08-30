from __future__ import annotations

import inspect
from collections import Counter

import pytest

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_heldout_comparators import (
    _FACADE_FACTORIES,
    _context,
    _train_paths,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_primary import (
    _train_expectation,
)
from sparkbrain.evaluation.v06_confirmatory_training_schedule import (
    build_balanced_training_schedule,
)

from test_capability_staging_development_fixture import DevelopmentCapabilityWorld
from test_capability_staging_development_variants import development_variants

_COMPARATORS = (
    ConfirmatoryCondition.G3_RECURRENT,
    ConfirmatoryCondition.G4_ASSEMBLY,
    ConfirmatoryCondition.G5_TYPED,
)


def test_654_schedule_preserves_counts_and_balances_shared_rounds() -> None:
    schedule = build_balanced_training_schedule(
        (6, 5, 4),
        lag_profile_count=4,
    )
    assert len(schedule.episodes) == 15
    assert Counter(row.path_index for row in schedule.episodes) == {
        0: 6,
        1: 5,
        2: 4,
    }
    assert tuple(row.path_index for row in schedule.episodes[:12]) == (
        0,
        1,
        2,
        2,
        1,
        0,
        0,
        1,
        2,
        2,
        1,
        0,
    )
    assert tuple(row.path_index for row in schedule.episodes[12:]) == (0, 1, 0)
    assert Counter(row.path_index for row in schedule.episodes[:12]) == {
        0: 4,
        1: 4,
        2: 4,
    }


def test_schedule_is_deterministic_hashable_and_assigns_lags_globally() -> None:
    first = build_balanced_training_schedule((6, 5, 4), lag_profile_count=3)
    second = build_balanced_training_schedule((6, 5, 4), lag_profile_count=3)
    assert first == second
    assert first.schedule_hash() == second.schedule_hash()
    assert len(first.schedule_hash()) == 64
    assert tuple(row.lag_profile_index for row in first.episodes) == tuple(
        index % 3 for index in range(len(first.episodes))
    )
    for path_index in range(3):
        assert tuple(
            row.exposure_index
            for row in first.episodes
            if row.path_index == path_index
        ) == tuple(range((6, 5, 4)[path_index]))


def test_invalid_schedule_contracts_fail_closed() -> None:
    with pytest.raises(ValueError, match="requires exposure counts"):
        build_balanced_training_schedule((), lag_profile_count=3)
    with pytest.raises(ValueError, match="positive"):
        build_balanced_training_schedule((3, 0), lag_profile_count=3)
    with pytest.raises(ValueError, match="lag profile"):
        build_balanced_training_schedule((3, 2), lag_profile_count=0)


def test_primary_and_comparator_training_use_the_same_schedule_builder() -> None:
    assert "build_balanced_training_schedule" in inspect.getsource(_train_expectation)
    assert "build_balanced_training_schedule" in inspect.getsource(_train_paths)


@pytest.mark.parametrize(
    "world",
    (DevelopmentCapabilityWorld(), *development_variants()),
    ids=lambda row: row.family_id,
)
@pytest.mark.parametrize("condition", _COMPARATORS, ids=lambda row: row.value)
def test_balanced_schedule_makes_most_exposed_main_branch_the_sham_chain(
    world,
    condition: ConfirmatoryCondition,
) -> None:
    factory = _FACADE_FACTORIES[condition]
    paths = (*world.competition_paths, world.control_path)
    model = factory.create()
    _train_paths(model, world, paths)
    assert model.rollout(
        _context("sequence", world.main_path),
        world.main_path[0],
    ) == world.main_path[1:]
    assert model.rollout(
        _context("sequence", world.control_path),
        world.control_path[0],
    ) == world.control_path[1:]


@pytest.mark.parametrize(
    "world",
    (DevelopmentCapabilityWorld(), *development_variants()),
    ids=lambda row: row.family_id,
)
@pytest.mark.parametrize("condition", _COMPARATORS, ids=lambda row: row.value)
def test_balanced_schedule_preserves_targeted_and_matched_intervention_contract(
    world,
    condition: ConfirmatoryCondition,
) -> None:
    factory = _FACADE_FACTORIES[condition]
    paths = (*world.competition_paths, world.control_path)
    main_context = _context("sequence", world.main_path)
    control_context = _context("sequence", world.control_path)

    targeted = factory.create()
    _train_paths(targeted, world, paths)
    assert targeted.rollout(
        main_context,
        world.main_path[0],
        suppressed_sources=(world.main_path[1],),
    ) == (world.main_path[1],)

    matched = factory.create()
    _train_paths(matched, world, paths)
    assert matched.rollout(
        control_context,
        world.control_path[0],
        suppressed_sources=(world.control_path[1],),
    ) == (world.control_path[1],)
    assert matched.rollout(
        main_context,
        world.main_path[0],
    ) == world.main_path[1:]

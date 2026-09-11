from __future__ import annotations

import pytest

from sparkbrain.research.rv01.interference_contract import InterferenceFamily
from sparkbrain.research.rv01_r01_16_identity import (
    R01_16_DEVELOPMENT_SEEDS,
    R01_16_FIXED_EXCLUSIONS,
    R01_16_FORMAL_AUTHORITY,
    R01_16_HELD_OUT_AUTHORITY,
    R01_16_UNIT_COUNT,
    R0116DevelopmentIdentity,
    assert_no_seed_collisions,
    development_identity_grid,
)


def test_r01_16_identity_grid_is_complete_deterministic_and_development_only() -> None:
    left = development_identity_grid()
    right = development_identity_grid()

    assert left == right
    assert len(left) == len(tuple(InterferenceFamily)) * len(R01_16_DEVELOPMENT_SEEDS)
    assert len(left) == 25
    assert {row.seed for row in left} == set(R01_16_DEVELOPMENT_SEEDS)
    assert {row.family for row in left} == {family.value for family in InterferenceFamily}
    assert {row.unit_count for row in left} == {R01_16_UNIT_COUNT}
    assert len({row.world_id for row in left}) == 25
    assert len({row.identity_sha256 for row in left}) == 25
    assert R01_16_FORMAL_AUTHORITY is False
    assert R01_16_HELD_OUT_AUTHORITY is False
    assert all(row.state_dict()["phase"] == "development" for row in left)


def test_r01_16_seed_namespace_is_disjoint_from_r01_15_fixed_ranges() -> None:
    assert set(R01_16_DEVELOPMENT_SEEDS).isdisjoint(R01_16_FIXED_EXCLUSIONS)
    assert_no_seed_collisions(R01_16_FIXED_EXCLUSIONS)


def test_r01_16_collision_check_fails_closed_on_any_retained_collision() -> None:
    with pytest.raises(ValueError, match="141702"):
        assert_no_seed_collisions({141702, 999999})


def test_r01_16_identity_rejects_unregistered_seed_or_family() -> None:
    with pytest.raises(ValueError, match="outside the fixed development namespace"):
        R0116DevelopmentIdentity(
            family=next(iter(InterferenceFamily)).value,
            seed=141799,
        ).validate()

    with pytest.raises(ValueError, match="inherited fixed family set"):
        R0116DevelopmentIdentity(family="invented-family", seed=141700).validate()

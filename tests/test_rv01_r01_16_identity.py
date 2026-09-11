from __future__ import annotations

import pytest

from sparkbrain.research.rv01_r01_16_identity import (
    R01_16_DEVELOPMENT_SEEDS,
    R01_16_FAMILIES,
    R01_16_FIXED_EXCLUSIONS,
    R01_16_FORMAL_AUTHORITY,
    R01_16_HELD_OUT_AUTHORITY,
    R01_16_UNIT_COUNT,
    R0116DevelopmentIdentity,
    assert_no_seed_collisions,
    development_identity_grid,
)

EXPECTED_FAMILIES = (
    "disjoint-routes",
    "shared-cue-branches",
    "shared-prefix-branches",
    "edge-reversal",
    "dense-route-load",
)


def test_r01_16_identity_grid_is_complete_deterministic_and_development_only() -> None:
    left = development_identity_grid()
    right = development_identity_grid()

    assert R01_16_FAMILIES == EXPECTED_FAMILIES
    assert left == right
    assert len(left) == len(R01_16_FAMILIES) * len(R01_16_DEVELOPMENT_SEEDS)
    assert len(left) == 25
    assert {row.seed for row in left} == set(R01_16_DEVELOPMENT_SEEDS)
    assert {row.family for row in left} == set(EXPECTED_FAMILIES)
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


def test_r01_16_collision_registry_rejects_ambiguous_numeric_identity() -> None:
    with pytest.raises(TypeError, match="exact non-boolean ints"):
        assert_no_seed_collisions({141700.0})
    with pytest.raises(TypeError, match="exact non-boolean ints"):
        assert_no_seed_collisions({True})


def test_r01_16_identity_rejects_unregistered_seed_or_family() -> None:
    with pytest.raises(ValueError, match="outside the fixed development namespace"):
        R0116DevelopmentIdentity(family=R01_16_FAMILIES[0], seed=141799).validate()

    with pytest.raises(ValueError, match="fixed registered family set"):
        R0116DevelopmentIdentity(family="invented-family", seed=141700).validate()


@pytest.mark.parametrize("bad_seed", [141700.0, True])
def test_r01_16_identity_rejects_non_exact_integer_seed(bad_seed: object) -> None:
    with pytest.raises(TypeError, match="seed must be an exact non-boolean int"):
        R0116DevelopmentIdentity(family=R01_16_FAMILIES[0], seed=bad_seed).validate()  # type: ignore[arg-type]


@pytest.mark.parametrize("bad_unit_count", [96.0, True])
def test_r01_16_identity_rejects_non_exact_integer_unit_count(bad_unit_count: object) -> None:
    with pytest.raises(TypeError, match="unit_count must be an exact non-boolean int"):
        R0116DevelopmentIdentity(
            family=R01_16_FAMILIES[0],
            seed=R01_16_DEVELOPMENT_SEEDS[0],
            unit_count=bad_unit_count,  # type: ignore[arg-type]
        ).validate()

from __future__ import annotations

import pytest

from sparkbrain.comparison.cx01.privilege import privilege_profile
from sparkbrain.comparison.cx01.contract import ComparatorKind
from sparkbrain.comparison.cx01.worlds import (
    CX01Family,
    DEVELOPMENT_SEEDS,
    HISTORICALLY_EXPOSED_SEEDS,
    build_development_grid,
    build_world,
    development_grid_hash,
)


def test_development_grid_is_complete_and_deterministic() -> None:
    first = build_development_grid()
    second = build_development_grid()
    assert len(first) == len(CX01Family) * len(DEVELOPMENT_SEEDS)
    assert tuple(row.specification_hash() for row in first) == tuple(
        row.specification_hash() for row in second
    )
    assert len(development_grid_hash()) == 64


def test_historical_confirmatory_seeds_are_rejected() -> None:
    for seed in HISTORICALLY_EXPOSED_SEEDS:
        with pytest.raises(ValueError):
            build_world("cx01-illegal", CX01Family.HIGH_ORDER, seed)


def test_timing_family_is_token_aliased_by_design() -> None:
    world = build_world("cx01-test", CX01Family.TIMING, 3999)
    left, right = world.training
    assert left.tokens[:-1] == right.tokens[:-1]
    assert left.tokens[-1] != right.tokens[-1]
    assert left.lags_ms[:-1] != right.lags_ms[:-1]


def test_high_order_family_has_shared_suffix_and_different_history() -> None:
    world = build_world("cx01-test", CX01Family.HIGH_ORDER, 3998)
    left, right = world.training
    assert left.tokens[1:3] == right.tokens[1:3]
    assert left.tokens[0] != right.tokens[0]
    assert left.tokens[-1] != right.tokens[-1]


def test_privilege_profiles_forbid_target_and_context_leakage() -> None:
    for kind in ComparatorKind:
        profile = privilege_profile(kind)
        profile.validate()
        assert not profile.generated_events_may_train
        assert not profile.correct_target_visible
        assert not profile.evaluator_context_id_visible

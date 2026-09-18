from __future__ import annotations

import pytest

from sparkbrain.external_validation.fading_memory import (
    FadingMemoryComparator,
    FadingMemoryConfig,
    assert_target_free_record,
    inventory_histories,
    stable_history_order,
)

DEV_CONFIG = FadingMemoryConfig(decay=0.5)


def test_dev_fixture_exhibits_fading_memory_without_training() -> None:
    comparator = FadingMemoryComparator(DEV_CONFIG)

    state = comparator.run([(1.0,), (0.0,), (0.0,)])

    assert state == (0.25,)
    assert comparator.run([(1.0,), (0.0,), (0.0,)]) == state


def test_histories_reset_and_do_not_share_state() -> None:
    comparator = FadingMemoryComparator(DEV_CONFIG)

    first = comparator.run([(1.0, 2.0), (0.0, 0.0)])
    second = comparator.run([(0.0, 0.0)])

    assert first == (0.5, 1.0)
    assert second == (0.0, 0.0)


def test_target_free_order_and_inventory_are_deterministic() -> None:
    unordered = (
        {"seq": 2, "feature": "later"},
        {"seq": 1, "feature": "earlier"},
    )

    ordered = stable_history_order(unordered, order_field="seq")
    inventory = inventory_histories((ordered,))

    assert tuple(record["seq"] for record in ordered) == (1, 2)
    assert inventory.history_count == 1
    assert inventory.observation_count == 2


def test_target_like_fields_fail_closed() -> None:
    with pytest.raises(ValueError, match="target-like fields"):
        assert_target_free_record({"seq": 1, "label": "must-not-enter-preformal-history"})


def test_invalid_decay_is_rejected() -> None:
    with pytest.raises(ValueError, match="decay"):
        FadingMemoryConfig(decay=1.0)

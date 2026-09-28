from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_modulation_supersession_guard import (
    ModulationSupersessionGuard,
    build_supersession_guard_report,
)

_ALL_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_superseded_high_level_frame_fails_closed_without_local_advance(
    variant: str,
) -> None:
    guard = ModulationSupersessionGuard(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    old = guard.make_frame(
        frame_sequence=0,
        mode="permit_side",
        target_side="left",
    )
    local_before = guard.snapshot
    bridge_sequence_before = guard.bridge_sequence

    guard.supersede("intent-b")
    result = guard.step(old)

    assert result.accepted is False
    assert result.reason == "SUPERSEDED_HIGH_LEVEL_AUTHORITY"
    assert result.before == local_before
    assert result.after == local_before
    assert guard.snapshot == local_before
    assert guard.bridge_sequence == bridge_sequence_before


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_fresh_frame_after_supersession_uses_existing_v2_contract(
    variant: str,
) -> None:
    guard = ModulationSupersessionGuard(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    guard.supersede("intent-b")

    result = guard.step(
        guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
    )

    assert result.accepted is True
    assert result.bridge_result is not None
    assert result.bridge_result.reason == (
        "HIGH_LEVEL_SIDE_MATCH_LOCAL_STEP_COMMITTED"
    )
    assert result.bridge_result.local_step_committed is True
    assert guard.snapshot.world.position == 1


def test_checkpoint_restore_recovers_authority_and_exact_frame_replay() -> None:
    guard = ModulationSupersessionGuard(
        WorldState(position=2, target=-1),
        variant="rewired",
        authority_token="intent-a",
    )
    checkpoint = guard.checkpoint()
    frame = guard.make_frame(
        frame_sequence=0,
        mode="permit_side",
        target_side="left",
    )

    first = guard.step(frame)
    first_token = guard.snapshot.token()

    guard.restore(checkpoint)
    assert guard.authority_epoch == 0
    assert guard.authority_token == "intent-a"

    second = guard.step(frame)

    assert first.accepted is True
    assert second.accepted is True
    assert guard.snapshot.token() == first_token


def test_invalid_checkpoint_restore_is_transactional() -> None:
    guard = ModulationSupersessionGuard(
        WorldState(position=2, target=-1),
        variant="structured",
        authority_token="intent-a",
    )
    stable = guard.checkpoint()
    payload = json.loads(stable)
    payload["authority_epoch"] = -1

    with pytest.raises(ValueError, match="authority epoch invalid"):
        guard.restore(json.dumps(payload, sort_keys=True))

    assert guard.checkpoint() == stable


def test_report_is_four_way_green_without_expanding_modulation_vocabulary() -> None:
    report = build_supersession_guard_report()

    assert report["status"] == "NON_EVIDENTIARY_NONCANONICAL_FORGE"
    assert report["modulation_vocabulary_expanded"] is False
    assert report["all_variants_reject_superseded_authority"] is True
    assert report["all_variants_accept_fresh_authority"] is True
    assert set(report["rows"]) == set(_ALL_VARIANTS)

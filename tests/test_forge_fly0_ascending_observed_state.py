from __future__ import annotations

import pytest

from forge_prototypes.fly0_ascending_observed_state import (
    AscendingObservedStateBridge,
    build_observed_state_report,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState

_ALL_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_fresh_step_reports_committed_world_outcome(variant: str) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
    )
    observed = result.observed
    assert result.guarded_result.accepted is True
    assert observed.accepted is True
    assert observed.reason == "HIGH_LEVEL_SIDE_MATCH_LOCAL_STEP_COMMITTED"
    assert observed.authority_epoch == 0
    assert observed.authority_token == "intent-a"
    assert observed.local_sequence_before == 0
    assert observed.local_sequence_after == 1
    assert observed.bridge_sequence_before == 0
    assert observed.bridge_sequence_after == 1
    assert observed.world_position_before == 2
    assert observed.world_position_after == 1
    assert observed.world_target == -1
    assert observed.position_delta == -1
    assert observed.remaining_signed_error == -2
    assert observed.local_step_committed is True


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_superseded_frame_reports_no_false_state_advance(variant: str) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    stale_frame = bridge.guard.make_frame(
        frame_sequence=0,
        mode="permit_side",
        target_side="left",
    )
    snapshot_before = bridge.snapshot
    bridge_sequence_before = bridge.guard.bridge_sequence
    bridge.guard.supersede("intent-b")

    result = bridge.step(stale_frame)
    observed = result.observed
    assert result.guarded_result.accepted is False
    assert observed.accepted is False
    assert observed.reason == "SUPERSEDED_HIGH_LEVEL_AUTHORITY"
    assert observed.authority_epoch == 1
    assert observed.authority_token == "intent-b"
    assert observed.local_sequence_before == snapshot_before.sequence
    assert observed.local_sequence_after == snapshot_before.sequence
    assert observed.bridge_sequence_before == bridge_sequence_before
    assert observed.bridge_sequence_after == bridge_sequence_before
    assert observed.world_position_before == snapshot_before.world.position
    assert observed.world_position_after == snapshot_before.world.position
    assert observed.position_delta == 0
    assert observed.local_step_committed is False
    assert observed.feedback_fired_events == 0
    assert observed.feedback_matched_motor_events == 0
    assert observed.feedback_opposite_motor_events == 0
    assert bridge.snapshot == snapshot_before
    assert bridge.guard.bridge_sequence == bridge_sequence_before


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_descending_cut_reports_actual_outcome_not_issued_hold(
    variant: str,
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    hold = bridge.guard.make_frame(frame_sequence=0, mode="hold")
    result = bridge.step(hold, descending_cut=True)
    observed = result.observed
    assert result.guarded_result.accepted is True
    assert observed.reason == "DESCENDING_CUT_LOCAL_BASELINE"
    assert observed.local_step_committed is True
    assert observed.world_position_before == 2
    assert observed.world_position_after == 1
    assert observed.position_delta == -1
    assert observed.remaining_signed_error == -2


def test_checkpoint_restore_replays_observed_summary_exactly() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="rewired",
        authority_token="intent-a",
    )
    checkpoint = bridge.checkpoint()
    frame = bridge.guard.make_frame(
        frame_sequence=0,
        mode="permit_side",
        target_side="left",
    )
    first = bridge.step(frame)
    first_snapshot_token = bridge.snapshot.token()
    bridge.restore(checkpoint)
    second = bridge.step(frame)
    assert second.observed.token() == first.observed.token()
    assert bridge.snapshot.token() == first_snapshot_token


def test_report_is_four_way_green_without_expanding_control_surface() -> None:
    report = build_observed_state_report()
    assert report["status"] == "NON_EVIDENTIARY_NONCANONICAL_FORGE"
    assert report["design"] == "ASCENDING_OBSERVED_STATE_SUMMARY"
    assert report["control_surface_expanded"] is False
    assert report["modulation_vocabulary_expanded"] is False
    assert report["all_variants_report_committed_outcome"] is True
    assert report["all_variants_reject_stale_without_false_observation"] is True
    assert set(report["rows"]) == set(_ALL_VARIANTS)

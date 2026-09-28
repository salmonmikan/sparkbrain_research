from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_descending_modulation import (
    DescendingModulationBridge,
    ModulationFrame,
    build_descending_modulation_report,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState

_ALL_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_neutral_frame_reproduces_local_baseline(variant: str) -> None:
    bridge = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant=variant,
    )

    trace = [bridge.snapshot.world.position]
    for sequence in range(3):
        result = bridge.step(
            bridge.make_frame(
                frame_sequence=sequence,
                mode="neutral",
            )
        )
        assert result.accepted is True
        assert result.local_step_committed is True
        trace.append(bridge.snapshot.world.position)

    assert tuple(trace) == (2, 1, 0, -1)


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_hold_and_descending_cut_separate_high_level_influence(
    variant: str,
) -> None:
    held = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant=variant,
    )
    frame = held.make_frame(frame_sequence=0, mode="hold")

    hold_result = held.step(frame)

    assert hold_result.accepted is True
    assert hold_result.reason == "HIGH_LEVEL_HOLD_COMMITTED"
    assert hold_result.local_step_committed is False
    assert held.snapshot.world.position == 2

    cut = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant=variant,
    )
    cut_result = cut.step(
        cut.make_frame(frame_sequence=0, mode="hold"),
        descending_cut=True,
    )

    assert cut_result.accepted is True
    assert cut_result.reason == "DESCENDING_CUT_LOCAL_BASELINE"
    assert cut_result.local_step_committed is True
    assert cut.snapshot.world.position == 1


@pytest.mark.parametrize("variant", _ALL_VARIANTS)
def test_local_feedback_cut_blocks_dependent_continuation(
    variant: str,
) -> None:
    bridge = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        mask_feedback=True,
    )

    first = bridge.step(
        bridge.make_frame(frame_sequence=0, mode="neutral")
    )
    before_second = bridge.snapshot
    second = bridge.step(
        bridge.make_frame(frame_sequence=1, mode="neutral")
    )

    assert first.accepted is True
    assert second.accepted is False
    assert second.reason == "ascending feedback insufficient for modulation"
    assert second.after == before_second
    assert bridge.snapshot == before_second
    assert bridge.last_frame_sequence == 0


def test_checkpoint_replay_is_exact_and_binds_modulation_contract() -> None:
    bridge = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant="rewired",
    )
    checkpoint = bridge.checkpoint()
    frame = bridge.make_frame(frame_sequence=0, mode="neutral")

    first = bridge.step(frame)
    first_after = bridge.snapshot.token()

    bridge.restore(checkpoint)
    second = bridge.step(frame)

    assert first.accepted is True
    assert second.accepted is True
    assert bridge.snapshot.token() == first_after

    payload = json.loads(checkpoint)
    payload["modulation_contract"]["version"] = "tampered"
    before = bridge.checkpoint()
    with pytest.raises(ValueError, match="modulation contract"):
        bridge.restore(json.dumps(payload, sort_keys=True))
    assert bridge.checkpoint() == before


def test_stale_expired_and_wrong_provenance_frames_fail_closed() -> None:
    bridge = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant="reactive",
    )
    first = bridge.make_frame(frame_sequence=0, mode="neutral")
    assert bridge.step(first).accepted is True
    stable = bridge.checkpoint()

    stale = ModulationFrame(
        schema_version=first.schema_version,
        frame_sequence=0,
        mode="neutral",
        issued_at_local_sequence=bridge.snapshot.sequence,
        ttl_steps=1,
        source_checkpoint_token=bridge.snapshot.token(),
    )
    assert bridge.step(stale).reason == "stale modulation frame sequence"
    assert bridge.checkpoint() == stable

    expired = ModulationFrame(
        schema_version=first.schema_version,
        frame_sequence=1,
        mode="neutral",
        issued_at_local_sequence=0,
        ttl_steps=1,
        source_checkpoint_token=bridge.snapshot.token(),
    )
    assert bridge.step(expired).reason == "expired modulation frame"
    assert bridge.checkpoint() == stable

    wrong_source = ModulationFrame(
        schema_version=first.schema_version,
        frame_sequence=1,
        mode="neutral",
        issued_at_local_sequence=bridge.snapshot.sequence,
        ttl_steps=1,
        source_checkpoint_token="0" * 64,
    )
    assert (
        bridge.step(wrong_source).reason
        == "modulation frame provenance token mismatch"
    )
    assert bridge.checkpoint() == stable


def test_local_failure_rolls_back_bridge_and_local_state() -> None:
    bridge = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant="structured",
        event_budget=1,
    )
    before = bridge.checkpoint()
    result = bridge.step(
        bridge.make_frame(frame_sequence=0, mode="neutral")
    )

    assert result.accepted is False
    assert result.reason == "local event budget exceeded"
    assert bridge.checkpoint() == before


def test_report_is_four_way_green_without_overclaim() -> None:
    report = build_descending_modulation_report()

    assert report["all_variants_same_interface"] is True
    assert report["all_neutral_baselines_green"] is True
    assert report["all_descending_cuts_green"] is True
    assert report["all_local_feedback_cuts_green"] is True
    assert len(report["modulation_contract_fingerprint"]) == 64
    assert set(report["rows"]) == set(_ALL_VARIANTS)
    assert report["status"] == "NON_EVIDENTIARY_NONCANONICAL_FORGE"

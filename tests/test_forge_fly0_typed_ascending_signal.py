from __future__ import annotations

import pytest

from forge_prototypes.fly0_ascending_observed_state import (
    AscendingObservedStateBridge,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_typed_ascending_signal import (
    build_typed_ascending_report,
    make_typed_signal,
)

_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


@pytest.mark.parametrize("variant", _VARIANTS)
def test_semantic_lanes_do_not_alias_world_outcome(variant: str) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=0, mode="permit_side", target_side="left"
        )
    )
    reafferent = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    local = make_typed_signal(
        semantic_kind="REALIZED_LOCAL_STATE",
        availability="OBSERVED",
        observed=result.observed,
    )
    predictive = make_typed_signal(
        semantic_kind="PREDICTIVE_MOTOR_COPY",
        availability="OBSERVED",
        source_token=f"{variant}-prediction",
    )

    assert reafferent.world_position_after == 1
    assert reafferent.position_delta == -1
    assert reafferent.world_reconciliation_candidate is True
    assert reafferent.requires_full_r22_receipt_validation is True
    assert local.local_sequence_after == 1
    assert local.world_position_after is None
    assert local.world_reconciliation_candidate is False
    assert predictive.provisional_only is True
    assert predictive.world_position_after is None
    assert predictive.world_reconciliation_candidate is False


@pytest.mark.parametrize(
    ("availability", "delay_steps"),
    (("GATED", 0), ("MASKED", 0), ("DELAYED", 2), ("MISSING", 0)),
)
def test_unavailable_reafference_is_not_zero_outcome(
    availability: str,
    delay_steps: int,
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="structured",
        authority_token="intent-a",
    )
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=0, mode="permit_side", target_side="left"
        )
    )
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability=availability,
        observed=None if availability == "MISSING" else result.observed,
        source_token="missing" if availability == "MISSING" else None,
        delay_steps=delay_steps,
    )
    assert signal.world_position_after is None
    assert signal.position_delta is None
    assert signal.remaining_signed_error is None
    assert signal.world_reconciliation_candidate is False


@pytest.mark.parametrize("variant", _VARIANTS)
def test_rejected_step_is_not_realized_world_outcome(variant: str) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    stale = bridge.guard.make_frame(
        frame_sequence=0, mode="permit_side", target_side="left"
    )
    bridge.guard.supersede("intent-b")
    result = bridge.step(stale)
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    assert signal.accepted is False
    assert signal.local_step_committed is False
    assert signal.world_position_after is None
    assert signal.position_delta is None
    assert signal.world_reconciliation_candidate is False


def test_predictive_lane_rejects_realized_payload() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="rewired",
        authority_token="intent-a",
    )
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=0, mode="permit_side", target_side="left"
        )
    )
    with pytest.raises(ValueError, match="predictive signal"):
        make_typed_signal(
            semantic_kind="PREDICTIVE_MOTOR_COPY",
            availability="OBSERVED",
            observed=result.observed,
        )


def test_report_is_four_way_green_and_narrow() -> None:
    report = build_typed_ascending_report()
    assert report["status"] == "NON_EVIDENTIARY_NONCANONICAL_FORGE"
    assert report["design"] == "TYPED_ASCENDING_SEMANTIC_RECONCILIATION"
    assert report["control_surface_expanded"] is False
    assert report["full_r22_receipt_contract_implemented"] is False
    assert report["all_variants_green"] is True
    assert set(report["rows"]) == set(_VARIANTS)

from __future__ import annotations

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_bounded_reconciliation_horizon import (
    BoundedReconciliationHorizon,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal
from forge_prototypes.fly0_upstream_receipt_validator import (
    record_execution,
    record_source_frame,
)

_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


def _record(
    bridge: AscendingObservedStateBridge,
    *,
    frame_sequence: int,
    outcome_sequence: int,
    transaction_id: str,
    availability: str = "OBSERVED",
):
    frame = bridge.guard.make_frame(
        frame_sequence=frame_sequence,
        mode="permit_side",
        target_side="left",
    )
    result = bridge.step(frame)
    source = record_source_frame(frame)
    journal = record_execution(
        result,
        transaction_id=transaction_id,
        outcome_sequence=outcome_sequence,
    )
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability=availability,
        observed=result.observed,
    )
    return result, signal, source, journal


def _submit(
    horizon: BoundedReconciliationHorizon,
    bridge: AscendingObservedStateBridge,
    signal,
    source,
    journal,
):
    return horizon.submit(
        signal,
        source_frame=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )


@pytest.mark.parametrize("variant", _VARIANTS)
def test_four_variants_compose_validator_gate_and_bounded_horizon(
    variant: str,
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant=variant,
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=3, max_pending=3)
    _, signal, source, journal = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id=f"{variant}-tx-1",
    )

    decision = _submit(horizon, bridge, signal, source, journal)

    assert decision.status == "RECONCILED"
    assert decision.world_position == 3
    assert decision.outcome_watermark == 1
    assert decision.observer_certainty == "EXACT_WITHIN_HORIZON"
    assert decision.pending_count == 0
    assert decision.retained_exact_count == 1


def test_horizon_blocks_pending_lineage_until_explicit_expiry() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=3, max_pending=3)
    _, masked, source, journal = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="pending-1",
        availability="MASKED",
    )

    pending = _submit(horizon, bridge, masked, source, journal)
    blocked = horizon.advance_horizon(2, expire_pending=False)

    assert pending.status == "PENDING"
    assert blocked.status == "HORIZON_ADVANCE_BLOCKED"
    assert blocked.reconciliation_horizon_floor == 0
    assert blocked.pending_count == 1
    assert blocked.observer_certainty == "EXACT_WITHIN_HORIZON"

    expired = horizon.advance_horizon(2, expire_pending=True)

    assert expired.status == "HORIZON_ADVANCED"
    assert expired.reconciliation_horizon_floor == 2
    assert expired.pending_count == 0
    assert expired.unresolved_gap_events == 1
    assert expired.observer_certainty == "DEGRADED_CAUSAL_GAP"


def test_checkpoint_restore_preserves_pending_then_accepts_same_lineage() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="rewired",
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=4, max_pending=3)

    _, first, first_source, first_journal = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="tx-1",
    )
    assert _submit(
        horizon, bridge, first, first_source, first_journal
    ).status == "RECONCILED"

    result, delayed, source, journal = _record(
        bridge,
        frame_sequence=1,
        outcome_sequence=2,
        transaction_id="tx-2",
        availability="DELAYED",
    )
    assert _submit(horizon, bridge, delayed, source, journal).status == "PENDING"

    checkpoint = horizon.checkpoint()
    restored = BoundedReconciliationHorizon(exact_window=4, max_pending=3)
    restored.restore(checkpoint)

    assert restored.checkpoint() == checkpoint
    assert restored.pending_count == 1
    assert restored.outcome_watermark == 1

    observed = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    resolved = _submit(restored, bridge, observed, source, journal)

    assert resolved.status == "RECONCILED"
    assert resolved.pending_count == 0
    assert resolved.outcome_watermark == 2
    assert resolved.world_position == 2


def test_outside_horizon_is_unresolved_and_never_rolls_back_world() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="random_sparse",
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=3, max_pending=3)
    first = None

    for index in range(5):
        item = _record(
            bridge,
            frame_sequence=index,
            outcome_sequence=index + 1,
            transaction_id=f"tx-{index + 1}",
        )
        if index == 0:
            first = item
        decision = _submit(horizon, bridge, item[1], item[2], item[3])
        assert decision.status == "RECONCILED"

    assert first is not None
    before_position = horizon.world_position
    before_watermark = horizon.outcome_watermark
    assert horizon.reconciliation_horizon_floor == 3
    assert horizon.retained_exact_count == 3

    late = _submit(horizon, bridge, first[1], first[2], first[3])

    assert late.status == "OUTSIDE_RETENTION_HORIZON"
    assert late.state_advanced is False
    assert late.world_position == before_position
    assert late.outcome_watermark == before_watermark
    assert late.observer_certainty == "DEGRADED_CAUSAL_GAP"
    assert late.unresolved_gap_events == 1


def test_ordinary_new_receipt_does_not_clear_gap_only_resync_does() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="reactive",
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=2, max_pending=2)
    records = []

    for index in range(4):
        item = _record(
            bridge,
            frame_sequence=index,
            outcome_sequence=index + 1,
            transaction_id=f"tx-{index + 1}",
        )
        records.append(item)
        assert _submit(
            horizon, bridge, item[1], item[2], item[3]
        ).status == "RECONCILED"

    assert horizon.reconciliation_horizon_floor == 3
    old = records[0]
    assert _submit(horizon, bridge, old[1], old[2], old[3]).status == (
        "OUTSIDE_RETENTION_HORIZON"
    )
    assert horizon.observer_certainty == "DEGRADED_CAUSAL_GAP"

    fresh = _record(
        bridge,
        frame_sequence=4,
        outcome_sequence=5,
        transaction_id="tx-5",
    )
    accepted = _submit(horizon, bridge, fresh[1], fresh[2], fresh[3])
    assert accepted.status == "RECONCILED"
    assert accepted.observer_certainty == "DEGRADED_CAUSAL_GAP"

    resynced = horizon.resynchronize(
        authoritative_world_position=horizon.world_position or 0,
        outcome_sequence=horizon.outcome_watermark,
    )
    assert resynced.status == "RESYNCHRONIZED"
    assert resynced.observer_certainty == "EXACT_WITHIN_HORIZON"
    assert resynced.unresolved_gap_events == 0


def test_long_run_exact_identity_state_is_bounded_by_window() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=4, max_pending=3)

    for index in range(20):
        _, signal, source, journal = _record(
            bridge,
            frame_sequence=index,
            outcome_sequence=index + 1,
            transaction_id=f"tx-{index + 1}",
        )
        decision = _submit(horizon, bridge, signal, source, journal)
        assert decision.status == "RECONCILED"
        assert decision.retained_exact_count <= 4

    assert horizon.outcome_watermark == 20
    assert horizon.reconciliation_horizon_floor == 17
    assert horizon.retained_exact_count == 4
    assert horizon.pending_count == 0
    assert horizon.observer_certainty == "EXACT_WITHIN_HORIZON"


def test_checkpoint_restore_preserves_horizon_gap_and_exact_replay_state() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    horizon = BoundedReconciliationHorizon(exact_window=2, max_pending=2)
    records = []
    for index in range(4):
        item = _record(
            bridge,
            frame_sequence=index,
            outcome_sequence=index + 1,
            transaction_id=f"checkpoint-tx-{index + 1}",
        )
        records.append(item)
        assert _submit(horizon, bridge, item[1], item[2], item[3]).status == "RECONCILED"

    assert horizon.reconciliation_horizon_floor == 3
    old = records[0]
    assert _submit(horizon, bridge, old[1], old[2], old[3]).status == "OUTSIDE_RETENTION_HORIZON"
    checkpoint = horizon.checkpoint()

    restored = BoundedReconciliationHorizon(exact_window=2, max_pending=2)
    restored.restore(checkpoint)
    assert restored.checkpoint() == checkpoint
    assert restored.reconciliation_horizon_floor == 3
    assert restored.outcome_watermark == 4
    assert restored.retained_exact_count == 2
    assert restored.observer_certainty == "DEGRADED_CAUSAL_GAP"
    assert restored.pending_count == 0

    latest = records[-1]
    duplicate = _submit(restored, bridge, latest[1], latest[2], latest[3])
    assert duplicate.status == "DUPLICATE_NOOP"
    assert duplicate.outcome_watermark == 4
    assert duplicate.observer_certainty == "DEGRADED_CAUSAL_GAP"

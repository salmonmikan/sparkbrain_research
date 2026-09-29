from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_recovery_epoch_fence import (
    RecoveryEpochFencedReconciliation,
)
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
    return signal, source, journal


def _bind(
    fence: RecoveryEpochFencedReconciliation,
    source,
    journal,
):
    bound_source = fence.bind_source_frame(source)
    bound_journal = fence.bind_execution(bound_source, journal)
    return bound_source, bound_journal


def _submit(
    fence: RecoveryEpochFencedReconciliation,
    bridge: AscendingObservedStateBridge,
    signal,
    source,
    journal,
):
    return fence.submit(
        signal,
        source=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )


@pytest.mark.parametrize("variant", _VARIANTS)
def test_four_variants_compose_with_recovery_epoch_fence(variant: str) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant=variant,
        authority_token="intent-a",
    )
    fence = RecoveryEpochFencedReconciliation(exact_window=4, max_pending=3)
    signal, source, journal = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id=f"{variant}-tx-1",
    )
    bound_source, bound_journal = _bind(fence, source, journal)

    decision = _submit(
        fence,
        bridge,
        signal,
        bound_source,
        bound_journal,
    )

    assert decision.status == "RECONCILIATION_RESULT"
    assert decision.reconciliation_status == "RECONCILED"
    assert decision.world_position == 3
    assert decision.outcome_watermark == 1
    assert decision.recovery_epoch == 0


def test_pre_resync_newer_sequence_cannot_overwrite_authoritative_world() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    fence = RecoveryEpochFencedReconciliation(exact_window=4, max_pending=3)

    first = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="tx-1",
    )
    first_source, first_journal = _bind(fence, first[1], first[2])
    assert _submit(
        fence,
        bridge,
        first[0],
        first_source,
        first_journal,
    ).reconciliation_status == "RECONCILED"

    delayed_old = _record(
        bridge,
        frame_sequence=1,
        outcome_sequence=6,
        transaction_id="tx-old-delayed",
    )
    old_source, old_journal = _bind(fence, delayed_old[1], delayed_old[2])

    resync = fence.resynchronize(
        authoritative_world_position=4,
        outcome_sequence=5,
    )
    assert resync.status == "RESYNCHRONIZED"
    assert resync.recovery_epoch == 1
    assert resync.world_position == 4
    assert resync.outcome_watermark == 5

    rejected = _submit(
        fence,
        bridge,
        delayed_old[0],
        old_source,
        old_journal,
    )
    assert rejected.status == "RETIRED_RECOVERY_EPOCH"
    assert rejected.state_advanced is False
    assert rejected.world_position == 4
    assert rejected.outcome_watermark == 5

    current = _record(
        bridge,
        frame_sequence=2,
        outcome_sequence=7,
        transaction_id="tx-current",
    )
    current_source, current_journal = _bind(fence, current[1], current[2])
    accepted = _submit(
        fence,
        bridge,
        current[0],
        current_source,
        current_journal,
    )
    assert accepted.reconciliation_status == "RECONCILED"
    assert accepted.outcome_watermark == 7
    assert accepted.recovery_epoch == 1


def test_resync_retires_all_pre_resync_pending_receipts() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="rewired",
        authority_token="intent-a",
    )
    fence = RecoveryEpochFencedReconciliation(exact_window=4, max_pending=2)
    pending = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=9,
        transaction_id="pending-old",
        availability="DELAYED",
    )
    pending_source, pending_journal = _bind(fence, pending[1], pending[2])

    unresolved = _submit(
        fence,
        bridge,
        pending[0],
        pending_source,
        pending_journal,
    )
    assert unresolved.reconciliation_status == "PENDING"
    assert unresolved.pending_count == 1

    resync = fence.resynchronize(
        authoritative_world_position=2,
        outcome_sequence=5,
    )

    assert resync.pending_count == 0
    assert resync.recovery_epoch == 1
    assert resync.world_position == 2
    assert resync.outcome_watermark == 5


def test_checkpoint_restore_preserves_epoch_fence() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="random_sparse",
        authority_token="intent-a",
    )
    fence = RecoveryEpochFencedReconciliation(exact_window=3, max_pending=2)
    old = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=6,
        transaction_id="old-after-restore",
    )
    old_source, old_journal = _bind(fence, old[1], old[2])
    fence.resynchronize(authoritative_world_position=3, outcome_sequence=5)

    checkpoint = fence.checkpoint()
    restored = RecoveryEpochFencedReconciliation(exact_window=3, max_pending=2)
    restored.restore(checkpoint)

    assert restored.checkpoint() == checkpoint
    assert restored.recovery_epoch == 1
    rejected = _submit(
        restored,
        bridge,
        old[0],
        old_source,
        old_journal,
    )
    assert rejected.status == "RETIRED_RECOVERY_EPOCH"
    assert rejected.world_position == 3
    assert rejected.outcome_watermark == 5


def test_future_or_mismatched_epoch_is_fail_closed() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="reactive",
        authority_token="intent-a",
    )
    fence = RecoveryEpochFencedReconciliation(exact_window=3, max_pending=2)
    item = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="future",
    )
    source, journal = _bind(fence, item[1], item[2])

    future_source = replace(source, recovery_epoch=1)
    future = _submit(
        fence,
        bridge,
        item[0],
        future_source,
        journal,
    )
    assert future.status == "FUTURE_RECOVERY_EPOCH"
    assert future.state_advanced is False

    mismatched_journal = replace(journal, bound_source_token="not-the-source-token")
    mismatch = _submit(
        fence,
        bridge,
        item[0],
        source,
        mismatched_journal,
    )
    assert mismatch.status == "RECOVERY_LINEAGE_BINDING_REJECTED"
    assert mismatch.state_advanced is False

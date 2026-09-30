from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_issue_time_provenance_binding import IssueTimeProvenanceBinding
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal
from forge_prototypes.fly0_upstream_receipt_validator import (
    record_execution,
    record_source_frame,
)

_VARIANTS = ("structured", "rewired", "random_sparse")


def _stack(variant="structured", session="world-a", issue_window=4):
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant=variant,
        authority_token="intent-a",
    )
    ledger = WorldSessionLedger(
        world_session_id=session,
        initial_world_position=4,
        cut_window=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=4,
        max_pending=3,
        anchor_window=3,
    )
    provenance = IssueTimeProvenanceBinding(
        ledger=ledger,
        reconciler=reconciler,
        issue_window=issue_window,
    )
    return bridge, ledger, reconciler, provenance


def _record(bridge, frame_sequence, outcome_sequence, transaction_id):
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
        availability="OBSERVED",
        observed=result.observed,
    )
    return result, signal, source, journal


def _commit_world(ledger, result, journal, action_id):
    ticket = ledger.issue_action(action_id)
    committed = ledger.commit_action(
        ticket,
        world_position=result.observed.world_position_after,
        outcome_sequence=journal.outcome_sequence,
    )
    assert committed.status == "COMMITTED"


def _submit(provenance, bridge, item, issued):
    execution = provenance.bind_execution(issued, item[3])
    return provenance.submit(
        item[1],
        source=issued,
        execution=execution,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )


@pytest.mark.parametrize("variant", _VARIANTS)
def test_old_issue_cannot_be_restamped_after_resync(variant):
    bridge, ledger, reconciler, provenance = _stack(
        variant=variant,
        session=f"world-{variant}",
    )
    old = _record(bridge, 0, 1, f"{variant}-old")
    _commit_world(ledger, old[0], old[3], f"{variant}-action-1")
    issued_old = provenance.issue_source(old[2], issue_id=f"{variant}-old-issue")

    rebased = reconciler.atomic_rebase(anchor_id=f"{variant}-anchor")
    assert rebased.status == "ANCHOR_REBASE_APPLIED"

    before = reconciler.checkpoint()
    rejected = _submit(provenance, bridge, old, issued_old)
    assert rejected.status == "RETIRED_WORLD_CUT"
    assert reconciler.checkpoint() == before

    forged = replace(
        issued_old,
        stamp=replace(
            issued_old.stamp,
            world_cut_generation=ledger.world_cut_generation,
            recovery_epoch=reconciler.recovery_epoch,
        ),
    )
    conflict = _submit(provenance, bridge, old, forged)
    assert conflict.status == "ISSUE_IDENTITY_CONFLICT"
    assert reconciler.checkpoint() == before

    current = _record(bridge, 1, 2, f"{variant}-current")
    _commit_world(ledger, current[0], current[3], f"{variant}-action-2")
    issued_current = provenance.issue_source(
        current[2],
        issue_id=f"{variant}-current-issue",
    )
    accepted = _submit(provenance, bridge, current, issued_current)
    assert accepted.status == "RECONCILIATION_RESULT"
    assert accepted.reconciliation_status == "RECONCILED"
    assert accepted.outcome_watermark == 2


def test_checkpoint_restores_issue_created_before_execution():
    bridge, ledger, reconciler, provenance = _stack()
    item = _record(bridge, 0, 1, "crash-boundary")
    _commit_world(ledger, item[0], item[3], "action-1")
    issued = provenance.issue_source(item[2], issue_id="durable-issue")
    checkpoint = provenance.checkpoint()

    restored = IssueTimeProvenanceBinding(
        ledger=ledger,
        reconciler=reconciler,
        issue_window=4,
    )
    restored.restore(checkpoint)
    recovered = restored.lookup_issue("durable-issue")
    assert recovered == issued
    assert restored.checkpoint() == checkpoint
    assert recovered is not None
    accepted = _submit(restored, bridge, item, recovered)
    assert accepted.reconciliation_status == "RECONCILED"


def test_issue_retention_is_bounded_and_expiry_fails_closed():
    bridge, _, reconciler, provenance = _stack(issue_window=2)
    first = None
    for index in range(3):
        item = _record(bridge, index, index + 1, f"tx-{index}")
        issued = provenance.issue_source(item[2], issue_id=f"issue-{index}")
        first = first or (item, issued)

    assert provenance.issue_count == 2
    assert provenance.issue_replay_floor == 1
    before = reconciler.checkpoint()
    rejected = _submit(provenance, bridge, first[0], first[1])
    assert rejected.status == "ISSUE_OUTSIDE_REPLAY_HORIZON"
    assert reconciler.checkpoint() == before


def test_old_issue_cannot_cross_new_world_session():
    old_bridge, _, _, old_provenance = _stack(session="world-old")
    item = _record(old_bridge, 0, 1, "old-session")
    issued = old_provenance.issue_source(item[2], issue_id="old-issue")

    new_bridge, _, new_reconciler, new_provenance = _stack(session="world-new")
    before = new_reconciler.checkpoint()
    rejected = _submit(new_provenance, new_bridge, item, issued)
    assert rejected.status == "WRONG_WORLD_SESSION"
    assert new_reconciler.checkpoint() == before


def test_wrapper_preserves_r14_same_session_monotonicity():
    bridge, ledger, reconciler, provenance = _stack()
    item = _record(bridge, 0, 1, "observer-ahead")
    issued = provenance.issue_source(item[2], issue_id="observer-ahead")
    assert _submit(provenance, bridge, item, issued).reconciliation_status == "RECONCILED"
    assert reconciler.outcome_watermark == 1
    assert ledger.outcome_sequence == 0

    before = reconciler.checkpoint()
    ledger_before = ledger.checkpoint()
    rejected = reconciler.atomic_rebase(anchor_id="backward-anchor")
    assert rejected.status == "ANCHOR_VALIDATION_REJECTED"
    assert rejected.reason == "ANCHOR_DOES_NOT_COVER_CURRENT_OBSERVER_WATERMARK"
    assert reconciler.checkpoint() == before
    assert ledger.checkpoint() == ledger_before

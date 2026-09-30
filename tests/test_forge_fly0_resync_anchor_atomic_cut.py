from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    ValidatedResyncAnchor,
    WorldAnchorSnapshot,
    WorldSessionLedger,
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
    return result, signal, source, journal


def _commit_world(ledger: WorldSessionLedger, result, journal, *, action_id: str) -> None:
    ticket = ledger.issue_action(action_id)
    committed = ledger.commit_action(
        ticket,
        world_position=result.observed.world_position_after,
        outcome_sequence=journal.outcome_sequence,
    )
    assert committed.status == "COMMITTED"


def _bind(reconciler: AnchoredRecoveryReconciler, source, journal):
    bound_source = reconciler.bind_source_frame(source)
    bound_journal = reconciler.bind_execution(bound_source, journal)
    return bound_source, bound_journal


def _submit(
    reconciler: AnchoredRecoveryReconciler,
    bridge: AscendingObservedStateBridge,
    signal,
    source,
    journal,
):
    return reconciler.submit(
        signal,
        source=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )


def _advance_to_gap(
    bridge: AscendingObservedStateBridge,
    ledger: WorldSessionLedger,
    reconciler: AnchoredRecoveryReconciler,
):
    records = []
    for index in range(4):
        result, signal, source, journal = _record(
            bridge,
            frame_sequence=index,
            outcome_sequence=index + 1,
            transaction_id=f"tx-{index + 1}",
        )
        _commit_world(ledger, result, journal, action_id=f"action-{index + 1}")
        bound_source, bound_journal = _bind(reconciler, source, journal)
        decision = _submit(
            reconciler,
            bridge,
            signal,
            bound_source,
            bound_journal,
        )
        assert decision.reconciliation_status == "RECONCILED"
        records.append((result, signal, bound_source, bound_journal))

    first = records[0]
    outside = _submit(
        reconciler,
        bridge,
        first[1],
        first[2],
        first[3],
    )
    assert outside.reconciliation_status == "OUTSIDE_RETENTION_HORIZON"
    assert reconciler.observer_certainty == "DEGRADED_CAUSAL_GAP"
    return records


@pytest.mark.parametrize("variant", _VARIANTS)
def test_four_variants_restore_certainty_only_from_validated_world_anchor(
    variant: str,
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant=variant,
        authority_token="intent-a",
    )
    ledger = WorldSessionLedger(
        world_session_id=f"world-{variant}",
        initial_world_position=4,
        cut_window=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=2,
        max_pending=3,
        anchor_window=3,
    )
    _advance_to_gap(bridge, ledger, reconciler)

    rebased = reconciler.atomic_rebase(anchor_id=f"{variant}-anchor-1")

    assert rebased.status == "ANCHOR_REBASE_APPLIED"
    assert rebased.anchor is not None
    assert rebased.recovery_epoch == 1
    assert rebased.world_position == ledger.world_position
    assert rebased.outcome_watermark == ledger.outcome_sequence
    assert rebased.observer_certainty == "EXACT_WITHIN_HORIZON"
    assert ledger.cut_pending is False

    result, signal, source, journal = _record(
        bridge,
        frame_sequence=4,
        outcome_sequence=5,
        transaction_id=f"{variant}-post-anchor",
    )
    _commit_world(ledger, result, journal, action_id=f"{variant}-action-5")
    bound_source, bound_journal = _bind(reconciler, source, journal)
    accepted = _submit(
        reconciler,
        bridge,
        signal,
        bound_source,
        bound_journal,
    )

    assert accepted.status == "RECONCILIATION_RESULT"
    assert accepted.reconciliation_status == "RECONCILED"
    assert accepted.recovery_epoch == 1
    assert accepted.outcome_watermark == 5


def test_self_attested_or_tampered_snapshot_cannot_restore_certainty() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    ledger = WorldSessionLedger(
        world_session_id="world-a",
        initial_world_position=4,
        cut_window=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=2,
        max_pending=3,
    )
    _advance_to_gap(bridge, ledger, reconciler)
    before = reconciler.checkpoint()

    self_attested = WorldAnchorSnapshot(
        world_session_id="world-a",
        anchor_id="forged",
        world_cut_generation=ledger.world_cut_generation,
        source_checkpoint_token="caller-claim",
        causal_cut_id="not-in-world-ledger",
        covered_through_outcome_sequence=ledger.outcome_sequence,
        world_position=999,
        old_recovery_epoch=reconciler.recovery_epoch,
        proposed_recovery_epoch=reconciler.recovery_epoch + 1,
        snapshot_digest="caller-digest",
    )
    rejected = reconciler.validate_external_snapshot(self_attested)

    assert rejected.status == "UNKNOWN_CAUSAL_CUT"
    assert reconciler.checkpoint() == before
    assert reconciler.observer_certainty == "DEGRADED_CAUSAL_GAP"

    ledger_before = ledger.checkpoint()
    canonical = ledger.snapshot_and_cut(
        anchor_id="canonical-but-tampered",
        old_recovery_epoch=reconciler.recovery_epoch,
    )
    tampered = replace(canonical, world_position=canonical.world_position + 100)
    tampered_decision = reconciler.validate_external_snapshot(tampered)

    assert tampered_decision.status == "CUT_RECORD_MISMATCH"
    assert reconciler.checkpoint() == before
    ledger.restore(ledger_before)


def test_stale_independent_world_anchor_cannot_roll_observer_back() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="rewired",
        authority_token="intent-a",
    )
    ledger = WorldSessionLedger(
        world_session_id="lagging-world",
        initial_world_position=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=3,
        max_pending=2,
    )
    result, signal, source, journal = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="observer-ahead",
    )
    del result
    bound_source, bound_journal = _bind(reconciler, source, journal)
    assert _submit(
        reconciler,
        bridge,
        signal,
        bound_source,
        bound_journal,
    ).reconciliation_status == "RECONCILED"

    ledger_before = ledger.checkpoint()
    observer_before = reconciler.checkpoint()
    rejected = reconciler.atomic_rebase(anchor_id="stale-world-anchor")

    assert rejected.status == "ANCHOR_VALIDATION_REJECTED"
    assert rejected.reason == "ANCHOR_DOES_NOT_COVER_CURRENT_OBSERVER_WATERMARK"
    assert reconciler.checkpoint() == observer_before
    assert ledger.checkpoint() == ledger_before
    assert reconciler.outcome_watermark == 1
    assert reconciler.recovery_epoch == 0


def test_world_cut_fences_old_action_and_includes_pre_cut_commit() -> None:
    ledger = WorldSessionLedger(
        world_session_id="race-world",
        initial_world_position=4,
        cut_window=4,
    )
    ledger_before = ledger.checkpoint()
    old_ticket = ledger.issue_action("late-old-action")
    snapshot = ledger.snapshot_and_cut(anchor_id="cut-a", old_recovery_epoch=0)

    rejected = ledger.commit_action(
        old_ticket,
        world_position=3,
        outcome_sequence=1,
    )

    assert rejected.status == "WORLD_CUT_PENDING_REBASE"
    assert rejected.state_advanced is False
    assert snapshot.covered_through_outcome_sequence == 0
    assert snapshot.world_position == 4

    ledger.restore(ledger_before)
    before_cut = ledger.issue_action("pre-cut-action")
    committed = ledger.commit_action(
        before_cut,
        world_position=3,
        outcome_sequence=1,
    )
    assert committed.status == "COMMITTED"

    included = ledger.snapshot_and_cut(anchor_id="cut-b", old_recovery_epoch=0)
    assert included.covered_through_outcome_sequence == 1
    assert included.world_position == 3


def test_pending_lineage_is_classified_and_old_receipt_is_fenced() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="random_sparse",
        authority_token="intent-a",
    )
    ledger = WorldSessionLedger(
        world_session_id="pending-world",
        initial_world_position=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=4,
        max_pending=3,
    )

    first = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="tx-1",
    )
    _commit_world(ledger, first[0], first[3], action_id="action-1")
    first_source, first_journal = _bind(reconciler, first[2], first[3])
    assert _submit(
        reconciler,
        bridge,
        first[1],
        first_source,
        first_journal,
    ).reconciliation_status == "RECONCILED"

    delayed = _record(
        bridge,
        frame_sequence=1,
        outcome_sequence=2,
        transaction_id="tx-delayed",
        availability="DELAYED",
    )
    _commit_world(ledger, delayed[0], delayed[3], action_id="action-2")
    delayed_source, delayed_journal = _bind(reconciler, delayed[2], delayed[3])
    pending = _submit(
        reconciler,
        bridge,
        delayed[1],
        delayed_source,
        delayed_journal,
    )
    assert pending.reconciliation_status == "PENDING"
    assert reconciler.pending_count == 1

    rebased = reconciler.atomic_rebase(anchor_id="pending-anchor")
    assert rebased.status == "ANCHOR_REBASE_APPLIED"
    assert len(rebased.pending_classifications) == 1
    classification = rebased.pending_classifications[0]
    assert classification.transaction_id == "tx-delayed"
    assert classification.outcome_sequence == 2
    assert classification.disposition == "COVERED_BY_ANCHOR"
    assert reconciler.pending_count == 0

    observed = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=delayed[0].observed,
    )
    before_position = reconciler.world_position
    before_watermark = reconciler.outcome_watermark
    old = _submit(
        reconciler,
        bridge,
        observed,
        delayed_source,
        delayed_journal,
    )
    assert old.status == "RETIRED_RECOVERY_EPOCH"
    assert old.state_advanced is False
    assert reconciler.world_position == before_position
    assert reconciler.outcome_watermark == before_watermark


@pytest.mark.parametrize("fail_at", ("BEFORE_FENCE", "AFTER_FENCE", "AFTER_REGISTRY"))
def test_atomic_rebase_failure_restores_complete_pre_anchor_state(fail_at: str) -> None:
    ledger = WorldSessionLedger(
        world_session_id=f"crash-world-{fail_at}",
        initial_world_position=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=3,
        max_pending=2,
        anchor_window=2,
    )
    ledger_before = ledger.checkpoint()
    observer_before = reconciler.checkpoint()

    failed = reconciler.atomic_rebase(
        anchor_id=f"crash-{fail_at}",
        fail_at=fail_at,
    )

    assert failed.status == "ATOMIC_REBASE_ROLLED_BACK"
    assert ledger.checkpoint() == ledger_before
    assert reconciler.checkpoint() == observer_before
    assert reconciler.recovery_epoch == 0
    assert reconciler.consumed_anchor_count == 0

    retried = reconciler.atomic_rebase(anchor_id=f"crash-{fail_at}")
    assert retried.status == "ANCHOR_REBASE_APPLIED"
    assert retried.recovery_epoch == 1
    assert ledger.cut_pending is False


def test_anchor_replay_conflict_and_checkpoint_restore() -> None:
    ledger = WorldSessionLedger(
        world_session_id="replay-world",
        initial_world_position=4,
        cut_window=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=3,
        max_pending=2,
        anchor_window=3,
    )
    applied = reconciler.atomic_rebase(anchor_id="anchor-1")
    assert applied.status == "ANCHOR_REBASE_APPLIED"
    assert applied.anchor is not None
    anchor = applied.anchor

    duplicate = reconciler.replay_anchor(anchor)
    assert duplicate.status == "DUPLICATE_ANCHOR_NOOP"
    assert duplicate.state_advanced is False

    forged = ValidatedResyncAnchor(
        snapshot=replace(
            anchor.snapshot,
            world_position=anchor.snapshot.world_position + 1,
        ),
        validation_token=anchor.validation_token,
    )
    conflict = reconciler.replay_anchor(forged)
    assert conflict.status == "ANCHOR_IDENTITY_CONFLICT"
    assert conflict.state_advanced is False

    ledger_checkpoint = ledger.checkpoint()
    reconciler_checkpoint = reconciler.checkpoint()
    restored_ledger = WorldSessionLedger(
        world_session_id="replay-world",
        initial_world_position=999,
        cut_window=4,
    )
    restored_ledger.restore(ledger_checkpoint)
    restored = AnchoredRecoveryReconciler(
        ledger=restored_ledger,
        exact_window=3,
        max_pending=2,
        anchor_window=3,
    )
    restored.restore(reconciler_checkpoint)

    assert restored.checkpoint() == reconciler_checkpoint
    assert restored_ledger.checkpoint() == ledger_checkpoint
    assert restored.replay_anchor(anchor).status == "DUPLICATE_ANCHOR_NOOP"
    assert restored.recovery_epoch == 1
    assert restored.observer_certainty == "EXACT_WITHIN_HORIZON"


def test_anchor_and_world_cut_identity_are_bounded_over_long_run() -> None:
    ledger = WorldSessionLedger(
        world_session_id="bounded-world",
        initial_world_position=4,
        cut_window=4,
    )
    reconciler = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=2,
        max_pending=2,
        anchor_window=3,
    )
    first_anchor = None

    for index in range(10):
        applied = reconciler.atomic_rebase(anchor_id=f"anchor-{index}")
        assert applied.status == "ANCHOR_REBASE_APPLIED"
        assert applied.anchor is not None
        if first_anchor is None:
            first_anchor = applied.anchor
        assert reconciler.consumed_anchor_count <= 3
        assert ledger.cut_count <= 4
        assert reconciler.retained_exact_count <= 2

    assert first_anchor is not None
    assert reconciler.recovery_epoch == 10
    assert reconciler.consumed_anchor_count == 3
    assert ledger.cut_count == 4
    assert reconciler.anchor_replay_floor > 0
    assert reconciler.replay_anchor(first_anchor).status == (
        "ANCHOR_OUTSIDE_REPLAY_HORIZON"
    )

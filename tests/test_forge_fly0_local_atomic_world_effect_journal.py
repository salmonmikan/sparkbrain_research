from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_issue_time_provenance_binding import (
    IssueBoundExecution,
    IssueTimeProvenanceBinding,
)
from forge_prototypes.fly0_local_atomic_world_effect_journal import (
    LocalAtomicWorldEffectJournal,
)
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldSessionLedger,
)
from forge_prototypes.fly0_upstream_receipt_validator import (
    record_execution,
    record_source_frame,
)

_VARIANTS = ("structured", "rewired", "random_sparse")


def _provenance(*, session: str = "world-a"):
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
    return IssueTimeProvenanceBinding(
        ledger=ledger,
        reconciler=reconciler,
        issue_window=8,
    )


def _record_issue(
    bridge: AscendingObservedStateBridge,
    provenance: IssueTimeProvenanceBinding,
    *,
    frame_sequence: int,
    outcome_sequence: int,
    issue_id: str,
):
    frame = bridge.guard.make_frame(
        frame_sequence=frame_sequence,
        mode="permit_side",
        target_side="left",
    )
    result = bridge.step(frame)
    assert result.observed.accepted is True
    assert result.observed.local_step_committed is True
    source = record_source_frame(frame)
    journal = record_execution(
        result,
        transaction_id=f"tx-{issue_id}",
        outcome_sequence=outcome_sequence,
    )
    issued = provenance.issue_source(source, issue_id=issue_id)
    execution = provenance.bind_execution(issued, journal)
    return issued, execution


@pytest.mark.parametrize("variant", _VARIANTS)
@pytest.mark.parametrize(
    "fail_at",
    ("AFTER_WORLD_UPDATE", "AFTER_EFFECT_INSERT"),
)
def test_atomic_failure_rolls_back_world_and_effect(
    tmp_path, variant: str, fail_at: str
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant=variant,
        authority_token="intent-a",
    )
    provenance = _provenance()
    issued, execution = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id=f"{variant}-{fail_at}",
    )
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / f"{variant}-{fail_at}.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
    )
    intent = journal.issue_action(issued, action_id="move-left")
    before = journal.snapshot()

    decision = journal.commit_effect(
        source=issued,
        execution=execution,
        intent=intent,
        fail_at=fail_at,
    )

    assert decision.status == "ATOMIC_ROLLBACK"
    assert decision.state_advanced is False
    assert journal.snapshot() == before
    assert journal.lookup_effect(issued.stamp.issue_id) is None
    journal.close()


def test_missing_effect_fails_closed_without_world_advance(tmp_path) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    issued, execution = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="missing-effect",
    )
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / "missing.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
    )
    intent = journal.issue_action(issued, action_id="move-left")
    before = journal.snapshot()

    joined = journal.verify_join(
        source=issued,
        execution=execution,
        intent=intent,
        effect=None,
    )

    assert joined.status == "MISSING_EFFECT"
    assert joined.accepted is False
    assert journal.snapshot() == before
    journal.close()


def test_committed_effect_survives_reopen_and_exact_replay_is_idempotent(
    tmp_path,
) -> None:
    db_path = tmp_path / "reopen.sqlite"
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    issued, execution = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="reopen-effect",
    )
    journal = LocalAtomicWorldEffectJournal(
        db_path,
        world_session_id="world-a",
        initial_world_position=4,
    )
    intent = journal.issue_action(issued, action_id="move-left")
    committed = journal.commit_effect(
        source=issued,
        execution=execution,
        intent=intent,
    )
    assert committed.status == "COMMITTED"
    assert committed.state_advanced is True
    assert committed.effect is not None
    committed_snapshot = journal.snapshot()
    effect_token = committed.effect.token()
    journal.close()

    reopened = LocalAtomicWorldEffectJournal(
        db_path,
        world_session_id="world-a",
        initial_world_position=999,
    )
    restored = reopened.lookup_effect(issued.stamp.issue_id)
    assert restored is not None
    assert restored.token() == effect_token
    assert reopened.snapshot() == committed_snapshot

    joined = reopened.verify_join(
        source=issued,
        execution=execution,
        intent=intent,
        effect=restored,
    )
    assert joined.status == "EXACT_MATCH"
    assert joined.accepted is True
    assert joined.effect_token == effect_token

    replay = reopened.commit_effect(
        source=issued,
        execution=execution,
        intent=intent,
    )
    assert replay.status == "EXACT_REPLAY"
    assert replay.state_advanced is False
    assert reopened.snapshot() == committed_snapshot
    assert reopened.lookup_effect(issued.stamp.issue_id).token() == effect_token
    reopened.close()


def test_cross_wire_and_effect_tamper_fail_closed(tmp_path) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / "cross-wire.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
    )

    issued_a, execution_a = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="issue-a",
    )
    intent_a = journal.issue_action(issued_a, action_id="move-left-a")
    committed_a = journal.commit_effect(
        source=issued_a,
        execution=execution_a,
        intent=intent_a,
    )
    assert committed_a.status == "COMMITTED"
    assert committed_a.effect is not None

    issued_b, execution_b = _record_issue(
        bridge,
        provenance,
        frame_sequence=1,
        outcome_sequence=2,
        issue_id="issue-b",
    )
    intent_b = journal.issue_action(issued_b, action_id="move-left-b")
    committed_b = journal.commit_effect(
        source=issued_b,
        execution=execution_b,
        intent=intent_b,
    )
    assert committed_b.status == "COMMITTED"
    assert committed_b.effect is not None

    cross_wire = journal.verify_join(
        source=issued_a,
        execution=execution_a,
        intent=intent_a,
        effect=committed_b.effect,
    )
    assert cross_wire.status == "ISSUE_EFFECT_CROSS_WIRE"
    assert cross_wire.accepted is False

    tampered = replace(committed_a.effect, observed_token="tampered")
    conflict = journal.verify_join(
        source=issued_a,
        execution=execution_a,
        intent=intent_a,
        effect=tampered,
    )
    assert conflict.status == "EFFECT_IDENTITY_CONFLICT"
    assert conflict.accepted is False
    journal.close()


def test_same_issue_with_changed_execution_conflicts_after_commit(tmp_path) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    issued, execution = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="conflict",
    )
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / "conflict.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
    )
    intent = journal.issue_action(issued, action_id="move-left")
    committed = journal.commit_effect(
        source=issued,
        execution=execution,
        intent=intent,
    )
    assert committed.status == "COMMITTED"

    changed_execution = IssueBoundExecution(
        issue_token=execution.issue_token,
        journal=replace(execution.journal, transaction_id="different-tx"),
    )
    conflict = journal.commit_effect(
        source=issued,
        execution=changed_execution,
        intent=intent,
    )

    assert conflict.status == "ISSUE_IDENTITY_CONFLICT"
    assert conflict.state_advanced is False
    journal.close()


def test_stale_world_base_is_rejected_without_advancing_state(tmp_path) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / "stale-base.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
    )

    issued_a, execution_a = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="base-a",
    )
    issued_b, execution_b = _record_issue(
        bridge,
        provenance,
        frame_sequence=1,
        outcome_sequence=2,
        issue_id="base-b",
    )
    intent_a = journal.issue_action(issued_a, action_id="move-left-a")
    stale_intent_b = journal.issue_action(issued_b, action_id="move-left-b")

    first = journal.commit_effect(
        source=issued_a,
        execution=execution_a,
        intent=intent_a,
    )
    assert first.status == "COMMITTED"
    before_stale = journal.snapshot()

    stale = journal.commit_effect(
        source=issued_b,
        execution=execution_b,
        intent=stale_intent_b,
    )
    assert stale.status == "STALE_WORLD_BASE"
    assert stale.state_advanced is False
    assert journal.snapshot() == before_stale
    assert journal.lookup_effect(issued_b.stamp.issue_id) is None
    journal.close()


def test_effect_retention_expires_to_outside_horizon(tmp_path) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / "retention.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
        effect_window=1,
    )

    issued_a, execution_a = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="retained-a",
    )
    intent_a = journal.issue_action(issued_a, action_id="move-left-a")
    first = journal.commit_effect(
        source=issued_a,
        execution=execution_a,
        intent=intent_a,
    )
    assert first.status == "COMMITTED"
    assert first.effect is not None

    issued_b, execution_b = _record_issue(
        bridge,
        provenance,
        frame_sequence=1,
        outcome_sequence=2,
        issue_id="retained-b",
    )
    intent_b = journal.issue_action(issued_b, action_id="move-left-b")
    second = journal.commit_effect(
        source=issued_b,
        execution=execution_b,
        intent=intent_b,
    )
    assert second.status == "COMMITTED"

    assert journal.lookup_effect(issued_a.stamp.issue_id) is None
    expired = journal.verify_join(
        source=issued_a,
        execution=execution_a,
        intent=intent_a,
        effect=first.effect,
    )
    assert expired.status == "EFFECT_OUTSIDE_REPLAY_HORIZON"
    assert expired.accepted is False
    journal.close()


def test_retired_issue_lineage_cannot_issue_current_world_effect(tmp_path) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant="structured",
        authority_token="intent-a",
    )
    provenance = _provenance()
    issued, _ = _record_issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="old-lineage",
    )
    journal = LocalAtomicWorldEffectJournal(
        tmp_path / "retired-lineage.sqlite",
        world_session_id="world-a",
        initial_world_position=4,
        world_cut_generation=1,
        recovery_epoch=1,
    )

    with pytest.raises(
        ValueError,
        match="issued source does not match current local WORLD lineage",
    ):
        journal.issue_action(issued, action_id="move-left")
    journal.close()

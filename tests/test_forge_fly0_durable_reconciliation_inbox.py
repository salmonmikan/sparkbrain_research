from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_durable_reconciliation_inbox import (
    DurableReconciliationInbox,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_issue_time_provenance_binding import IssueTimeProvenanceBinding
from forge_prototypes.fly0_local_atomic_world_effect_journal import (
    LocalAtomicWorldEffectJournal,
)
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import (
    TypedAscendingSignal,
    make_typed_signal,
)
from forge_prototypes.fly0_upstream_receipt_validator import (
    record_execution,
    record_source_frame,
)

_VARIANTS = ("structured", "rewired", "random_sparse")


def _runtime(*, variant: str = "structured", session: str = "world-a"):
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4),
        variant=variant,
        authority_token="intent-a",
    )
    ledger = WorldSessionLedger(world_session_id=session, initial_world_position=4)
    inner = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=4,
        max_pending=3,
        anchor_window=3,
    )
    provenance = IssueTimeProvenanceBinding(
        ledger=ledger,
        reconciler=inner,
        issue_window=8,
    )
    return bridge, provenance


def _issue(
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
    source = record_source_frame(frame)
    journal = record_execution(
        result,
        transaction_id=f"tx-{issue_id}",
        outcome_sequence=outcome_sequence,
    )
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    issued = provenance.issue_source(source, issue_id=issue_id)
    execution = provenance.bind_execution(issued, journal)
    return signal, issued, execution


def _prepare(tmp_path: Path, *, commit_effect: bool = True):
    db_path = tmp_path / "durable.sqlite"
    bridge, provenance = _runtime()
    effects = LocalAtomicWorldEffectJournal(
        db_path,
        world_session_id="world-a",
        initial_world_position=4,
    )
    durable = DurableReconciliationInbox(db_path)
    signal, issued, execution = _issue(
        bridge,
        provenance,
        frame_sequence=0,
        outcome_sequence=1,
        issue_id="issue-0",
    )
    durable.persist_source(issued)
    durable.persist_execution(execution, issue_id=issued.stamp.issue_id)
    intent = effects.issue_action(issued, action_id="move-left-0")
    if commit_effect:
        committed = effects.commit_effect(
            source=issued,
            execution=execution,
            intent=intent,
        )
        assert committed.status == "COMMITTED"
    return db_path, bridge, provenance, effects, durable, signal, issued


def _accept(durable, bridge, signal, issue_id, *, fail_at=None):
    return durable.accept_receipt(
        signal,
        issue_id=issue_id,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
        fail_at=fail_at,
    )


_PHASE_A = r"""
import json
import sys
from dataclasses import asdict
from pathlib import Path

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_durable_reconciliation_inbox import DurableReconciliationInbox
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_issue_time_provenance_binding import IssueTimeProvenanceBinding
from forge_prototypes.fly0_local_atomic_world_effect_journal import (
    LocalAtomicWorldEffectJournal,
)
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal
from forge_prototypes.fly0_upstream_receipt_validator import (
    record_execution,
    record_source_frame,
)

db_path = Path(sys.argv[1])
receipt_path = Path(sys.argv[2])
variant = sys.argv[3]
session = f"world-{variant}"

bridge = AscendingObservedStateBridge(
    WorldState(position=4, target=-4),
    variant=variant,
    authority_token="intent-a",
)
ledger = WorldSessionLedger(world_session_id=session, initial_world_position=4)
inner = AnchoredRecoveryReconciler(
    ledger=ledger,
    exact_window=4,
    max_pending=3,
    anchor_window=3,
)
provenance = IssueTimeProvenanceBinding(
    ledger=ledger,
    reconciler=inner,
    issue_window=8,
)
effects = LocalAtomicWorldEffectJournal(
    db_path,
    world_session_id=session,
    initial_world_position=4,
)
durable = DurableReconciliationInbox(db_path)

frame = bridge.guard.make_frame(
    frame_sequence=0,
    mode="permit_side",
    target_side="left",
)
result = bridge.step(frame)
source = record_source_frame(frame)
journal = record_execution(
    result,
    transaction_id=f"tx-{variant}-cold",
    outcome_sequence=1,
)
issued = provenance.issue_source(source, issue_id=f"{variant}-cold")
execution = provenance.bind_execution(issued, journal)
durable.persist_source(issued)
durable.persist_execution(execution, issue_id=issued.stamp.issue_id)
intent = effects.issue_action(issued, action_id="move-left-cold")
committed = effects.commit_effect(
    source=issued,
    execution=execution,
    intent=intent,
)
assert committed.status == "COMMITTED"
signal = make_typed_signal(
    semantic_kind="REAFFERENT_WORLD_OUTCOME",
    availability="OBSERVED",
    observed=result.observed,
)
receipt_path.write_text(
    json.dumps(
        {
            "signal": asdict(signal),
            "issue_id": issued.stamp.issue_id,
            "authority_epoch": bridge.guard.authority_epoch,
            "authority_token": bridge.guard.authority_token,
        },
        sort_keys=True,
    ),
    encoding="utf-8",
)
durable.close()
effects.close()
"""


@pytest.mark.parametrize("variant", _VARIANTS)
def test_true_process_loss_reconstructs_from_durable_rows(tmp_path, variant):
    db_path = tmp_path / f"{variant}-cold.sqlite"
    receipt_path = tmp_path / f"{variant}-receipt.json"
    subprocess.run(
        [sys.executable, "-c", _PHASE_A, str(db_path), str(receipt_path), variant],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    signal = TypedAscendingSignal(**receipt["signal"])

    restarted = DurableReconciliationInbox(db_path)
    context = restarted.reconstruct(receipt["issue_id"])
    assert context.source.stamp.issue_id == receipt["issue_id"]
    assert context.execution.issue_token == context.source.token()
    assert context.effect.issue_token == context.source.token()

    accepted = restarted.accept_receipt(
        signal,
        issue_id=receipt["issue_id"],
        current_authority_epoch=receipt["authority_epoch"],
        current_authority_token=receipt["authority_token"],
    )
    assert accepted.status == "ACCEPTED"
    assert accepted.frontier.outcome_watermark == 1
    committed_frontier = accepted.frontier
    restarted.close()

    reopened = DurableReconciliationInbox(db_path)
    assert reopened.snapshot() == committed_frontier
    replay = reopened.accept_receipt(
        signal,
        issue_id=receipt["issue_id"],
        current_authority_epoch=receipt["authority_epoch"],
        current_authority_token=receipt["authority_token"],
    )
    assert replay.status == "EXACT_REPLAY"
    assert replay.state_advanced is False
    assert replay.frontier == committed_frontier
    reopened.close()


@pytest.mark.parametrize("fail_at", ("AFTER_INBOX", "AFTER_FRONTIER"))
def test_inbox_and_frontier_rollback_together(tmp_path, fail_at):
    stack = _prepare(tmp_path)
    _, bridge, _, effects, durable, signal, issued = stack
    before = durable.snapshot()

    rolled_back = _accept(
        durable,
        bridge,
        signal,
        issued.stamp.issue_id,
        fail_at=fail_at,
    )

    assert rolled_back.status == "ATOMIC_ROLLBACK"
    assert rolled_back.state_advanced is False
    assert durable.snapshot() == before
    accepted = _accept(durable, bridge, signal, issued.stamp.issue_id)
    assert accepted.status == "ACCEPTED"
    durable.close()
    effects.close()


def test_missing_execution_fails_closed_after_restart(tmp_path):
    stack = _prepare(tmp_path)
    db_path, bridge, _, effects, durable, signal, issued = stack
    before = durable.snapshot()
    durable.close()
    with sqlite3.connect(db_path) as db:
        db.execute(
            """
            UPDATE reconciliation_provenance
            SET execution_token=NULL, execution_payload=NULL
            WHERE issue_id=?
            """,
            (issued.stamp.issue_id,),
        )

    restarted = DurableReconciliationInbox(db_path)
    rejected = _accept(restarted, bridge, signal, issued.stamp.issue_id)

    assert rejected.status == "MISSING_PROVENANCE"
    assert rejected.state_advanced is False
    assert restarted.snapshot() == before
    restarted.close()
    effects.close()


def test_source_tamper_fails_closed_after_restart(tmp_path):
    stack = _prepare(tmp_path)
    db_path, bridge, _, effects, durable, signal, issued = stack
    before = durable.snapshot()
    durable.close()
    with sqlite3.connect(db_path) as db:
        row = db.execute(
            "SELECT source_payload FROM reconciliation_provenance WHERE issue_id=?",
            (issued.stamp.issue_id,),
        ).fetchone()
        assert row is not None
        payload = json.loads(row[0])
        payload["stamp"]["issue_id"] = "tampered"
        db.execute(
            "UPDATE reconciliation_provenance SET source_payload=? WHERE issue_id=?",
            (
                json.dumps(payload, sort_keys=True, separators=(",", ":")),
                issued.stamp.issue_id,
            ),
        )

    restarted = DurableReconciliationInbox(db_path)
    rejected = _accept(restarted, bridge, signal, issued.stamp.issue_id)

    assert rejected.status == "PROVENANCE_TAMPERED"
    assert rejected.state_advanced is False
    assert restarted.snapshot() == before
    restarted.close()
    effects.close()


def test_missing_world_effect_fails_closed(tmp_path):
    stack = _prepare(tmp_path, commit_effect=False)
    _, bridge, _, effects, durable, signal, issued = stack
    before = durable.snapshot()

    rejected = _accept(durable, bridge, signal, issued.stamp.issue_id)

    assert rejected.status == "MISSING_EFFECT"
    assert rejected.state_advanced is False
    assert durable.snapshot() == before
    durable.close()
    effects.close()


def test_receipt_cross_wire_is_rejected(tmp_path):
    stack = _prepare(tmp_path)
    _, bridge, provenance, effects, durable, signal_a, _ = stack
    signal_b, issued_b, execution_b = _issue(
        bridge,
        provenance,
        frame_sequence=1,
        outcome_sequence=2,
        issue_id="issue-1",
    )
    durable.persist_source(issued_b)
    durable.persist_execution(execution_b, issue_id=issued_b.stamp.issue_id)
    intent_b = effects.issue_action(issued_b, action_id="move-left-1")
    committed_b = effects.commit_effect(
        source=issued_b,
        execution=execution_b,
        intent=intent_b,
    )
    assert committed_b.status == "COMMITTED"
    before = durable.snapshot()

    rejected = _accept(durable, bridge, signal_a, issued_b.stamp.issue_id)

    assert rejected.status == "RECEIPT_REJECTED"
    assert rejected.state_advanced is False
    assert durable.snapshot() == before
    assert signal_b.world_reconciliation_candidate is True
    durable.close()
    effects.close()


def test_outcome_gap_cannot_skip_unresolved_receipt(tmp_path):
    stack = _prepare(tmp_path)
    _, bridge, provenance, effects, durable, _, _ = stack
    signal_b, issued_b, execution_b = _issue(
        bridge,
        provenance,
        frame_sequence=1,
        outcome_sequence=2,
        issue_id="gap-issue",
    )
    durable.persist_source(issued_b)
    durable.persist_execution(execution_b, issue_id=issued_b.stamp.issue_id)
    intent_b = effects.issue_action(issued_b, action_id="move-left-gap")
    committed_b = effects.commit_effect(
        source=issued_b,
        execution=execution_b,
        intent=intent_b,
    )
    assert committed_b.status == "COMMITTED"

    rejected = _accept(durable, bridge, signal_b, issued_b.stamp.issue_id)

    assert rejected.status == "OUTCOME_GAP"
    assert rejected.state_advanced is False
    assert rejected.frontier.outcome_watermark == 0
    durable.close()
    effects.close()


def test_world_lineage_divergence_fails_closed(tmp_path):
    stack = _prepare(tmp_path)
    db_path, bridge, _, effects, durable, signal, issued = stack
    before = durable.snapshot()
    durable.close()
    effects.close()
    with sqlite3.connect(db_path) as db:
        db.execute("UPDATE world_state SET epoch=epoch+1 WHERE id=1")

    restarted = DurableReconciliationInbox(db_path)
    rejected = _accept(restarted, bridge, signal, issued.stamp.issue_id)

    assert rejected.status == "WORLD_AUTHORITY_DIVERGED"
    assert rejected.state_advanced is False
    assert rejected.frontier == before
    restarted.close()


def test_exact_duplicate_is_idempotent_across_store_instances(tmp_path):
    stack = _prepare(tmp_path)
    db_path, bridge, _, effects, durable, signal, issued = stack
    peer = DurableReconciliationInbox(db_path)

    accepted = _accept(durable, bridge, signal, issued.stamp.issue_id)
    replay = _accept(peer, bridge, signal, issued.stamp.issue_id)

    assert accepted.status == "ACCEPTED"
    assert accepted.state_advanced is True
    assert replay.status == "EXACT_REPLAY"
    assert replay.state_advanced is False
    assert peer.snapshot() == durable.snapshot()
    peer.close()
    durable.close()
    effects.close()



def test_old_issue_lineage_is_rejected_after_world_and_frontier_advance(tmp_path):
    stack = _prepare(tmp_path)
    db_path, bridge, _, effects, durable, signal, issued = stack
    before = durable.snapshot()
    durable.close()
    effects.close()

    with sqlite3.connect(db_path) as db:
        db.execute("UPDATE world_state SET cut=cut+1, epoch=epoch+1 WHERE id=1")
        db.execute(
            """
            UPDATE reconciliation_frontier
            SET cut=cut+1, epoch=epoch+1
            WHERE id=1
            """
        )

    restarted = DurableReconciliationInbox(db_path)
    rejected = _accept(restarted, bridge, signal, issued.stamp.issue_id)

    assert rejected.status == "LINEAGE_RETIRED_OR_FUTURE"
    assert rejected.state_advanced is False
    assert rejected.frontier.world_cut_generation == before.world_cut_generation + 1
    assert rejected.frontier.recovery_epoch == before.recovery_epoch + 1
    assert rejected.frontier.outcome_watermark == before.outcome_watermark
    assert rejected.frontier.accepted_receipts == before.accepted_receipts
    restarted.close()


def test_exact_duplicate_race_advances_frontier_once(tmp_path):
    stack = _prepare(tmp_path)
    db_path, bridge, _, effects, durable, signal, issued = stack
    issue_id = issued.stamp.issue_id
    authority_epoch = bridge.guard.authority_epoch
    authority_token = bridge.guard.authority_token
    durable.close()
    effects.close()
    barrier = Barrier(2)

    def submit_once():
        inbox = DurableReconciliationInbox(db_path)
        try:
            barrier.wait(timeout=5)
            return inbox.accept_receipt(
                signal,
                issue_id=issue_id,
                current_authority_epoch=authority_epoch,
                current_authority_token=authority_token,
            )
        finally:
            inbox.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(submit_once) for _ in range(2)]
        results = [future.result(timeout=10) for future in futures]

    assert sorted(result.status for result in results) == ["ACCEPTED", "EXACT_REPLAY"]
    assert sum(result.state_advanced for result in results) == 1

    inspector = DurableReconciliationInbox(db_path)
    frontier = inspector.snapshot()
    assert frontier.outcome_watermark == 1
    assert frontier.accepted_receipts == 1
    inspector.close()

from __future__ import annotations

import json
import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_causal_frontier import SessionCausalFrontierGuard
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_issue_time_provenance_binding import IssueTimeProvenanceBinding
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldAnchorSnapshot,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal
from forge_prototypes.fly0_upstream_receipt_validator import (
    record_execution,
    record_source_frame,
)

_VARIANTS = ("structured", "rewired", "random_sparse")


def _stack(*, variant: str = "structured", session: str = "world-a"):
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
        issue_window=4,
    )
    frontier = SessionCausalFrontierGuard(
        ledger=ledger,
        reconciler=reconciler,
    )
    return bridge, ledger, reconciler, provenance, frontier


def _record(
    bridge: AscendingObservedStateBridge,
    *,
    frame_sequence: int,
    outcome_sequence: int,
    transaction_id: str,
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
        availability="OBSERVED",
        observed=result.observed,
    )
    return result, signal, source, journal


def _submit(
    reconciler: AnchoredRecoveryReconciler,
    bridge: AscendingObservedStateBridge,
    item,
):
    bound_source = reconciler.bind_source_frame(item[2])
    bound_journal = reconciler.bind_execution(bound_source, item[3])
    return reconciler.submit(
        item[1],
        source=bound_source,
        journal=bound_journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )


@pytest.mark.parametrize("variant", _VARIANTS)
def test_recreated_inner_cannot_reset_durable_outcome_watermark(variant: str) -> None:
    bridge, ledger, reconciler, _, frontier = _stack(
        variant=variant,
        session=f"world-{variant}",
    )
    for index in range(2):
        item = _record(
            bridge,
            frame_sequence=index,
            outcome_sequence=index + 1,
            transaction_id=f"{variant}-tx-{index + 1}",
        )
        assert _submit(reconciler, bridge, item).reconciliation_status == "RECONCILED"

    refreshed = frontier.refresh_from_inner()
    assert refreshed.accepted is True
    assert frontier.frontier.outcome_watermark == 2

    recreated = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=4,
        max_pending=3,
        anchor_window=3,
    )
    before = frontier.checkpoint()
    rejected = frontier.validate_inner(recreated)

    assert rejected.status == "OUTCOME_WATERMARK_ROLLBACK"
    assert rejected.accepted is False
    assert frontier.checkpoint() == before


def test_inner_from_different_world_session_is_rejected() -> None:
    _, _, _, _, frontier = _stack(session="world-current")
    other_ledger = WorldSessionLedger(
        world_session_id="world-other",
        initial_world_position=4,
    )
    other_inner = AnchoredRecoveryReconciler(
        ledger=other_ledger,
        exact_window=4,
        max_pending=3,
        anchor_window=3,
    )

    rejected = frontier.validate_inner(other_inner)

    assert rejected.status == "WRONG_WORLD_SESSION"
    assert rejected.accepted is False


def test_atomic_rebase_advances_frontier_and_retires_old_issue_lineage() -> None:
    bridge, ledger, reconciler, provenance, frontier = _stack()
    item = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="pre-rebase",
    )
    issued = provenance.issue_source(item[2], issue_id="pre-rebase-issue")

    rebased = reconciler.atomic_rebase(anchor_id="anchor-1")
    assert rebased.status == "ANCHOR_REBASE_APPLIED"
    advanced = frontier.reconcile_after_rebase()
    assert advanced.accepted is True
    assert frontier.frontier.world_cut_generation == 1
    assert frontier.frontier.recovery_epoch == 1

    old_issue = frontier.admit_issue_stamp(issued.stamp)
    assert old_issue.status == "RETIRED_ISSUE_LINEAGE"

    stale_ledger = WorldSessionLedger(
        world_session_id=ledger.world_session_id,
        initial_world_position=4,
    )
    stale_inner = AnchoredRecoveryReconciler(
        ledger=stale_ledger,
        exact_window=4,
        max_pending=3,
        anchor_window=3,
    )
    stale = frontier.validate_inner(stale_inner)
    assert stale.status == "WORLD_CUT_ROLLBACK"


def test_stale_anchor_coverage_cannot_move_frontier_backward() -> None:
    bridge, _, reconciler, _, frontier = _stack()
    item = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="observer-ahead",
    )
    assert _submit(reconciler, bridge, item).reconciliation_status == "RECONCILED"
    assert frontier.refresh_from_inner().accepted is True
    assert frontier.frontier.outcome_watermark == 1

    current = frontier.frontier
    stale = WorldAnchorSnapshot(
        world_session_id=current.world_session_id,
        anchor_id="stale-anchor",
        world_cut_generation=current.world_cut_generation,
        source_checkpoint_token="checkpoint-token",
        causal_cut_id="causal-cut",
        covered_through_outcome_sequence=0,
        world_position=4,
        old_recovery_epoch=current.recovery_epoch,
        proposed_recovery_epoch=current.recovery_epoch + 1,
        snapshot_digest="not-used-by-frontier-preflight",
    )
    before = frontier.checkpoint()
    rejected = frontier.preflight_anchor(stale)

    assert rejected.status == "STALE_ANCHOR_COVERAGE"
    assert rejected.accepted is False
    assert frontier.checkpoint() == before


def test_checkpoint_rejects_tamper_and_inner_behind_durable_frontier() -> None:
    bridge, ledger, reconciler, _, frontier = _stack()
    item = _record(
        bridge,
        frame_sequence=0,
        outcome_sequence=1,
        transaction_id="durable-frontier",
    )
    assert _submit(reconciler, bridge, item).reconciliation_status == "RECONCILED"
    assert frontier.refresh_from_inner().accepted is True
    checkpoint = frontier.checkpoint()

    tampered = json.loads(checkpoint)
    tampered["frontier"]["outcome_watermark"] = 0
    with pytest.raises(ValueError, match="checkpoint token mismatch"):
        frontier.restore(json.dumps(tampered, sort_keys=True, separators=(",", ":")))

    behind_inner = AnchoredRecoveryReconciler(
        ledger=ledger,
        exact_window=4,
        max_pending=3,
        anchor_window=3,
    )
    behind_guard = SessionCausalFrontierGuard(
        ledger=ledger,
        reconciler=behind_inner,
    )
    with pytest.raises(ValueError, match="inner outcome watermark behind durable frontier"):
        behind_guard.restore(checkpoint)


def test_repeated_rebases_keep_frontier_checkpoint_fixed_shape() -> None:
    _, _, reconciler, _, frontier = _stack()
    for index in range(5):
        rebased = reconciler.atomic_rebase(anchor_id=f"anchor-{index}")
        assert rebased.status == "ANCHOR_REBASE_APPLIED"
        assert frontier.reconcile_after_rebase().accepted is True

    payload = json.loads(frontier.checkpoint())
    assert set(payload) == {"schema_version", "frontier", "frontier_token"}
    assert set(payload["frontier"]) == {
        "world_session_id",
        "world_cut_generation",
        "recovery_epoch",
        "outcome_watermark",
        "horizon_floor",
        "observer_certainty",
    }
    assert payload["frontier"]["world_cut_generation"] == 5
    assert payload["frontier"]["recovery_epoch"] == 5

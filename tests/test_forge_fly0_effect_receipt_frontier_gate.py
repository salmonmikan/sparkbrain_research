from __future__ import annotations

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_causal_frontier import SessionCausalFrontierGuard
from forge_prototypes.fly0_effect_receipt_frontier_gate import EffectReceiptFrontierGate
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_issue_time_provenance_binding import IssueTimeProvenanceBinding
from forge_prototypes.fly0_local_atomic_world_effect_journal import LocalAtomicWorldEffectJournal
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal
from forge_prototypes.fly0_upstream_receipt_validator import record_execution, record_source_frame

_VARIANTS = ("structured", "rewired", "random_sparse")


def _fixture(tmp_path, variant="structured", session="world-a"):
    bridge = AscendingObservedStateBridge(
        WorldState(position=4, target=-4), variant=variant, authority_token="intent-a"
    )
    ledger = WorldSessionLedger(world_session_id=session, initial_world_position=4)
    inner = AnchoredRecoveryReconciler(
        ledger=ledger, exact_window=4, max_pending=3, anchor_window=3
    )
    provenance = IssueTimeProvenanceBinding(
        ledger=ledger, reconciler=inner, issue_window=8
    )
    frontier = SessionCausalFrontierGuard(ledger=ledger, reconciler=inner)
    effects = LocalAtomicWorldEffectJournal(
        tmp_path / f"{variant}.sqlite",
        world_session_id=session,
        initial_world_position=4,
    )
    gate = EffectReceiptFrontierGate(
        effect_journal=effects, provenance=provenance, frontier=frontier
    )
    return bridge, inner, provenance, frontier, effects, gate


def _issue(bridge, provenance, effects, seq, outcome, issue_id):
    frame = bridge.guard.make_frame(
        frame_sequence=seq, mode="permit_side", target_side="left"
    )
    result = bridge.step(frame)
    source = record_source_frame(frame)
    journal = record_execution(
        result, transaction_id=f"tx-{issue_id}", outcome_sequence=outcome
    )
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    issued = provenance.issue_source(source, issue_id=issue_id)
    execution = provenance.bind_execution(issued, journal)
    intent = effects.issue_action(issued, action_id=f"action-{issue_id}")
    return signal, issued, execution, intent


def _commit(effects, item):
    decision = effects.commit_effect(
        source=item[1], execution=item[2], intent=item[3]
    )
    assert decision.status == "COMMITTED"
    assert decision.effect is not None
    return decision.effect


def _submit(gate, bridge, item, effect):
    return gate.submit(
        item[0],
        source=item[1],
        execution=item[2],
        intent=item[3],
        effect=effect,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )


@pytest.mark.parametrize("variant", _VARIANTS)
def test_exact_effect_allows_frontier_advance(tmp_path, variant):
    stack = _fixture(tmp_path, variant, f"world-{variant}")
    bridge, inner, _, frontier, effects, gate = stack
    item = _issue(bridge, stack[2], effects, 0, 1, f"{variant}-issue")
    effect = _commit(effects, item)

    accepted = _submit(gate, bridge, item, effect)

    assert accepted.status == "ACCEPTED"
    assert accepted.state_advanced is True
    assert accepted.binding is not None
    assert accepted.binding.effect_token == effect.token()
    assert accepted.binding.frontier_token == frontier.frontier.token()
    assert inner.outcome_watermark == 1
    assert frontier.frontier.outcome_watermark == 1

    checkpoint = gate.checkpoint()
    restored = EffectReceiptFrontierGate(
        effect_journal=effects, provenance=stack[2], frontier=frontier
    )
    restored.restore_bindings(checkpoint)
    replay = _submit(restored, bridge, item, effect)
    assert replay.status == "EXACT_REPLAY"
    assert replay.state_advanced is False
    effects.close()


def test_missing_effect_does_not_advance_frontier(tmp_path):
    bridge, inner, provenance, frontier, effects, gate = _fixture(tmp_path)
    item = _issue(bridge, provenance, effects, 0, 1, "missing")
    before_frontier = frontier.checkpoint()
    before_inner = inner.checkpoint()

    rejected = _submit(gate, bridge, item, None)

    assert rejected.status == "EFFECT_JOIN_REJECTED"
    assert rejected.state_advanced is False
    assert frontier.checkpoint() == before_frontier
    assert inner.checkpoint() == before_inner
    effects.close()


def test_effect_identity_from_other_issue_is_rejected(tmp_path):
    bridge, inner, provenance, frontier, effects, gate = _fixture(tmp_path)
    first = _issue(bridge, provenance, effects, 0, 1, "first")
    _commit(effects, first)
    second = _issue(bridge, provenance, effects, 1, 2, "second")
    other_effect = _commit(effects, second)
    before_frontier = frontier.checkpoint()
    before_inner = inner.checkpoint()

    rejected = _submit(gate, bridge, first, other_effect)

    assert rejected.status == "EFFECT_JOIN_REJECTED"
    assert rejected.state_advanced is False
    assert frontier.checkpoint() == before_frontier
    assert inner.checkpoint() == before_inner
    effects.close()


def test_frontier_advanced_without_binding_cannot_be_bound_later(tmp_path):
    bridge, _, provenance, frontier, effects, gate = _fixture(tmp_path)
    item = _issue(bridge, provenance, effects, 0, 1, "early-frontier")
    effect = _commit(effects, item)

    direct = provenance.submit(
        item[0],
        source=item[1],
        execution=item[2],
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    assert direct.reconciliation_status == "RECONCILED"
    assert frontier.refresh_from_inner().accepted is True
    before = frontier.checkpoint()

    rejected = _submit(gate, bridge, item, effect)

    assert rejected.status == "UNBOUND_FRONTIER_AHEAD"
    assert rejected.state_advanced is False
    assert rejected.binding is None
    assert frontier.checkpoint() == before
    effects.close()

from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_ascending_observed_state import (
    AscendingObservedStateBridge,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_reconciliation_admission_gate import (
    ReconciliationAdmissionGate,
    make_validation_proof,
)
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal

_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


def _world_signal(
    bridge: AscendingObservedStateBridge,
    *,
    frame_sequence: int,
):
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=frame_sequence,
            mode="permit_side",
            target_side="left",
        )
    )
    return make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )


@pytest.mark.parametrize("variant", _VARIANTS)
def test_committed_stale_control_outcome_reconciles_once_without_control_restore(
    variant: str,
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    signal = _world_signal(bridge, frame_sequence=0)
    proof = make_validation_proof(
        signal,
        transaction_id=f"{variant}-tx-1",
        outcome_sequence=1,
        source_control_current=False,
    )
    gate = ReconciliationAdmissionGate()

    first = gate.admit(signal, proof)
    duplicate = gate.admit(signal, proof)

    assert first.status == "RECONCILED"
    assert first.reason == (
        "COMMITTED_OUTCOME_RECONCILED_WITHOUT_CONTROL_RESTORATION"
    )
    assert first.state_advanced is True
    assert first.world_position == 1
    assert duplicate.status == "DUPLICATE_NOOP"
    assert duplicate.state_advanced is False
    assert gate.world_position == 1


def test_non_world_and_unavailable_signals_never_reconcile() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="structured",
        authority_token="intent-a",
    )
    result = bridge.step(
        bridge.guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
    )
    predictive = make_typed_signal(
        semantic_kind="PREDICTIVE_MOTOR_COPY",
        availability="OBSERVED",
        source_token="prediction",
    )
    local = make_typed_signal(
        semantic_kind="REALIZED_LOCAL_STATE",
        availability="OBSERVED",
        observed=result.observed,
    )
    masked = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="MASKED",
        observed=result.observed,
    )
    gate = ReconciliationAdmissionGate()

    assert gate.admit(predictive).status == "NON_WORLD_SIGNAL"
    assert gate.admit(local).status == "NON_WORLD_SIGNAL"
    assert gate.admit(masked).status == "NOT_RECONCILABLE"
    assert gate.world_position is None


def test_reafferent_candidate_requires_receipt_and_exact_signal_binding() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="rewired",
        authority_token="intent-a",
    )
    signal = _world_signal(bridge, frame_sequence=0)
    gate = ReconciliationAdmissionGate()

    missing = gate.admit(signal)
    proof = make_validation_proof(
        signal,
        transaction_id="tx-1",
        outcome_sequence=1,
    )
    mismatched = gate.admit(
        signal,
        replace(proof, signal_token="not-the-signal-token"),
    )

    assert missing.status == "RECEIPT_REQUIRED"
    assert mismatched.status == "REJECTED_RECEIPT"
    assert mismatched.reason == "SIGNAL_RECEIPT_BINDING_MISMATCH"
    assert gate.world_position is None


@pytest.mark.parametrize(
    ("field", "reason"),
    (
        ("provenance_valid", "SOURCE_PROVENANCE_INVALID"),
        ("transaction_valid", "TRANSACTION_INVALID"),
    ),
)
def test_invalid_upstream_receipt_proof_fails_closed(
    field: str,
    reason: str,
) -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="random_sparse",
        authority_token="intent-a",
    )
    signal = _world_signal(bridge, frame_sequence=0)
    proof = make_validation_proof(
        signal,
        transaction_id="tx-invalid",
        outcome_sequence=1,
    )
    gate = ReconciliationAdmissionGate()

    rejected = gate.admit(signal, replace(proof, **{field: False}))

    assert rejected.status == "REJECTED_RECEIPT"
    assert rejected.reason == reason
    assert gate.world_position is None


def test_out_of_order_committed_outcome_is_recorded_without_rollback() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="structured",
        authority_token="intent-a",
    )
    older = _world_signal(bridge, frame_sequence=0)
    newer = _world_signal(bridge, frame_sequence=1)
    gate = ReconciliationAdmissionGate()

    newest_first = gate.admit(
        newer,
        make_validation_proof(
            newer,
            transaction_id="tx-2",
            outcome_sequence=2,
        ),
    )
    old_late = gate.admit(
        older,
        make_validation_proof(
            older,
            transaction_id="tx-1",
            outcome_sequence=1,
            source_control_current=False,
        ),
    )

    assert newest_first.status == "RECONCILED"
    assert newest_first.world_position == 0
    assert old_late.status == "OUT_OF_ORDER_NO_ROLLBACK"
    assert old_late.state_advanced is False
    assert gate.world_position == 0
    assert gate.last_outcome_sequence == 2


def test_transaction_id_collision_fails_closed() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="reactive",
        authority_token="intent-a",
    )
    first = _world_signal(bridge, frame_sequence=0)
    second = _world_signal(bridge, frame_sequence=1)
    gate = ReconciliationAdmissionGate()

    accepted = gate.admit(
        first,
        make_validation_proof(
            first,
            transaction_id="same-tx",
            outcome_sequence=1,
        ),
    )
    collision = gate.admit(
        second,
        make_validation_proof(
            second,
            transaction_id="same-tx",
            outcome_sequence=2,
        ),
    )

    assert accepted.status == "RECONCILED"
    assert collision.status == "REJECTED_RECEIPT"
    assert collision.reason == "TRANSACTION_ID_COLLISION"
    assert gate.world_position == 1


def test_checkpoint_restore_preserves_exactly_once_state() -> None:
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant="structured",
        authority_token="intent-a",
    )
    signal = _world_signal(bridge, frame_sequence=0)
    proof = make_validation_proof(
        signal,
        transaction_id="tx-checkpoint",
        outcome_sequence=1,
    )
    gate = ReconciliationAdmissionGate()
    assert gate.admit(signal, proof).status == "RECONCILED"

    checkpoint = gate.checkpoint()
    restored = ReconciliationAdmissionGate()
    restored.restore(checkpoint)
    duplicate = restored.admit(signal, proof)

    assert duplicate.status == "DUPLICATE_NOOP"
    assert restored.world_position == 1
    assert restored.last_outcome_sequence == 1


@pytest.mark.parametrize("variant", _VARIANTS)
def test_cross_transaction_signal_replay_is_rejected_without_poisoning_next_outcome(variant: str) -> None:
    bridge = AscendingObservedStateBridge(WorldState(position=2, target=-1), variant=variant, authority_token="intent-a")
    first = _world_signal(bridge, frame_sequence=0)
    second = _world_signal(bridge, frame_sequence=1)
    gate = ReconciliationAdmissionGate()
    assert gate.admit(first, make_validation_proof(first, transaction_id=f"{variant}-tx-1", outcome_sequence=1)).status == "RECONCILED"
    replay = gate.admit(first, make_validation_proof(first, transaction_id=f"{variant}-replay", outcome_sequence=2))
    assert replay.status == "REJECTED_RECEIPT"
    assert replay.reason == "SIGNAL_REPLAY_ACROSS_TRANSACTION"
    assert gate.last_outcome_sequence == 1
    next_outcome = gate.admit(second, make_validation_proof(second, transaction_id=f"{variant}-tx-2", outcome_sequence=2))
    assert next_outcome.status == "RECONCILED"
    assert gate.last_outcome_sequence == 2


def test_same_transaction_signal_with_conflicting_sequence_is_rejected() -> None:
    bridge = AscendingObservedStateBridge(WorldState(position=2, target=-1), variant="structured", authority_token="intent-a")
    signal = _world_signal(bridge, frame_sequence=0)
    gate = ReconciliationAdmissionGate()
    assert gate.admit(signal, make_validation_proof(signal, transaction_id="tx-sequence", outcome_sequence=1)).status == "RECONCILED"
    conflict = gate.admit(signal, make_validation_proof(signal, transaction_id="tx-sequence", outcome_sequence=2))
    assert conflict.status == "REJECTED_RECEIPT"
    assert conflict.reason == "TRANSACTION_PROOF_SEQUENCE_CONFLICT"
    assert gate.last_outcome_sequence == 1

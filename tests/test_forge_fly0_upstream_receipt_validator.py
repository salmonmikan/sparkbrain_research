from __future__ import annotations

from dataclasses import replace

import pytest

from forge_prototypes.fly0_ascending_observed_state import AscendingObservedStateBridge
from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_reconciliation_admission_gate import ReconciliationAdmissionGate
from forge_prototypes.fly0_typed_ascending_signal import make_typed_signal
from forge_prototypes.fly0_upstream_receipt_validator import (
    UpstreamReceiptValidator,
    record_execution,
    record_source_frame,
)

_VARIANTS = ("structured", "rewired", "random_sparse", "reactive")


def _fixture(variant: str):
    bridge = AscendingObservedStateBridge(
        WorldState(position=2, target=-1),
        variant=variant,
        authority_token="intent-a",
    )
    frame = bridge.guard.make_frame(
        frame_sequence=0, mode="permit_side", target_side="left"
    )
    result = bridge.step(frame)
    source = record_source_frame(frame)
    journal = record_execution(
        result, transaction_id=f"{variant}-tx-1", outcome_sequence=1
    )
    signal = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="OBSERVED",
        observed=result.observed,
    )
    return bridge, result, signal, source, journal


@pytest.mark.parametrize("variant", _VARIANTS)
def test_exact_receipt_validates_and_composes_with_gate(variant: str) -> None:
    bridge, _, signal, source, journal = _fixture(variant)
    decision = UpstreamReceiptValidator().validate(
        signal,
        source_frame=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    assert decision.status == "VALIDATED"
    assert decision.proof is not None
    reconciled = ReconciliationAdmissionGate().admit(signal, decision.proof)
    assert reconciled.status == "RECONCILED"
    assert reconciled.world_position == 1


@pytest.mark.parametrize("variant", _VARIANTS)
def test_committed_stale_authority_does_not_restore_control(variant: str) -> None:
    bridge, _, signal, source, journal = _fixture(variant)
    bridge.guard.supersede("intent-b")
    decision = UpstreamReceiptValidator().validate(
        signal,
        source_frame=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    assert decision.status == "VALIDATED"
    assert decision.proof is not None
    assert decision.proof.source_control_current is False
    reconciled = ReconciliationAdmissionGate().admit(signal, decision.proof)
    assert reconciled.reason == "COMMITTED_OUTCOME_RECONCILED_WITHOUT_CONTROL_RESTORATION"


def test_adversarial_receipt_boundaries() -> None:
    bridge, result, signal, source, journal = _fixture("structured")
    validator = UpstreamReceiptValidator()
    wrong_source = validator.validate(
        signal,
        source_frame=replace(source, frame_sequence=source.frame_sequence + 1),
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    assert signal.world_position_after is not None
    wrong_payload = validator.validate(
        replace(signal, world_position_after=signal.world_position_after + 1),
        source_frame=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    rolled_back = record_execution(
        result, transaction_id="rollback-tx", outcome_sequence=2, rolled_back=True
    )
    rollback = validator.validate(
        signal,
        source_frame=source,
        journal=rolled_back,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    masked = make_typed_signal(
        semantic_kind="REAFFERENT_WORLD_OUTCOME",
        availability="MASKED",
        observed=result.observed,
    )
    unavailable = validator.validate(
        masked,
        source_frame=source,
        journal=journal,
        current_authority_epoch=bridge.guard.authority_epoch,
        current_authority_token=bridge.guard.authority_token,
    )
    assert wrong_source.reason == "SOURCE_FRAME_JOURNAL_MISMATCH"
    assert wrong_payload.reason == "SIGNAL_JOURNAL_PAYLOAD_MISMATCH"
    assert rollback.reason == "TRANSACTION_NOT_COMMITTED"
    assert unavailable.status == "UNRESOLVED"
    assert unavailable.reason == "FEEDBACK_NOT_OBSERVED"

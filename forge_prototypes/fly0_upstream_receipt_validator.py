"""Forge-only source-frame and execution-journal validation for FLY-0.

NON_EVIDENTIARY / NONCANONICAL.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_ascending_observed_state import ObservedStepResult
from forge_prototypes.fly0_modulation_supersession_guard import GuardedModulationFrame
from forge_prototypes.fly0_reconciliation_admission_gate import ValidatedReceiptProof
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal

TransactionState = Literal["COMMITTED", "REJECTED", "ROLLED_BACK"]
ValidationStatus = Literal["VALIDATED", "REJECTED", "UNRESOLVED"]


@dataclass(frozen=True)
class SourceFrameRecord:
    authority_epoch: int
    authority_token: str
    frame_sequence: int
    schema_version: str
    mode: str
    target_side: str | None
    issued_at_local_sequence: int
    ttl_steps: int
    source_checkpoint_token: str

    def token(self) -> str:
        raw = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return sha256(raw.encode()).hexdigest()


@dataclass(frozen=True)
class ExecutionJournalEntry:
    transaction_id: str
    outcome_sequence: int
    transaction_state: TransactionState
    source_frame_token: str
    source_authority_epoch: int
    source_authority_token: str
    observed_token: str
    accepted: bool
    local_step_committed: bool
    local_sequence_after: int
    world_position_after: int
    position_delta: int
    remaining_signed_error: int

    def __post_init__(self) -> None:
        if not self.transaction_id:
            raise ValueError("transaction_id must be non-empty")
        if self.outcome_sequence < 0:
            raise ValueError("outcome_sequence must be non-negative")


@dataclass(frozen=True)
class ReceiptValidationDecision:
    status: ValidationStatus
    reason: str
    proof: ValidatedReceiptProof | None = None


def record_source_frame(frame: GuardedModulationFrame) -> SourceFrameRecord:
    inner = frame.frame
    return SourceFrameRecord(
        authority_epoch=frame.authority_epoch,
        authority_token=frame.authority_token,
        frame_sequence=inner.frame_sequence,
        schema_version=inner.schema_version,
        mode=inner.mode,
        target_side=inner.target_side,
        issued_at_local_sequence=inner.issued_at_local_sequence,
        ttl_steps=inner.ttl_steps,
        source_checkpoint_token=inner.source_checkpoint_token,
    )


def record_execution(
    result: ObservedStepResult,
    *,
    transaction_id: str,
    outcome_sequence: int,
    rolled_back: bool = False,
) -> ExecutionJournalEntry:
    observed = result.observed
    source = record_source_frame(result.guarded_result.guarded_frame)
    state: TransactionState
    if rolled_back:
        state = "ROLLED_BACK"
    elif observed.accepted and observed.local_step_committed:
        state = "COMMITTED"
    else:
        state = "REJECTED"
    return ExecutionJournalEntry(
        transaction_id=transaction_id,
        outcome_sequence=outcome_sequence,
        transaction_state=state,
        source_frame_token=source.token(),
        source_authority_epoch=source.authority_epoch,
        source_authority_token=source.authority_token,
        observed_token=observed.token(),
        accepted=observed.accepted,
        local_step_committed=observed.local_step_committed,
        local_sequence_after=observed.local_sequence_after,
        world_position_after=observed.world_position_after,
        position_delta=observed.position_delta,
        remaining_signed_error=observed.remaining_signed_error,
    )


class UpstreamReceiptValidator:
    def validate(
        self,
        signal: TypedAscendingSignal,
        *,
        source_frame: SourceFrameRecord,
        journal: ExecutionJournalEntry,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> ReceiptValidationDecision:
        if signal.semantic_kind != "REAFFERENT_WORLD_OUTCOME":
            return ReceiptValidationDecision(
                "REJECTED", "SEMANTIC_KIND_NOT_REAFFERENT_WORLD_OUTCOME"
            )
        if signal.availability != "OBSERVED":
            return ReceiptValidationDecision("UNRESOLVED", "FEEDBACK_NOT_OBSERVED")
        if not signal.world_reconciliation_candidate:
            return ReceiptValidationDecision(
                "REJECTED", "SIGNAL_NOT_COMMITTED_WORLD_OUTCOME"
            )
        if source_frame.token() != journal.source_frame_token:
            return ReceiptValidationDecision(
                "REJECTED", "SOURCE_FRAME_JOURNAL_MISMATCH"
            )
        if (
            source_frame.authority_epoch != journal.source_authority_epoch
            or source_frame.authority_token != journal.source_authority_token
        ):
            return ReceiptValidationDecision(
                "REJECTED", "SOURCE_AUTHORITY_JOURNAL_MISMATCH"
            )
        if journal.transaction_state != "COMMITTED":
            return ReceiptValidationDecision("REJECTED", "TRANSACTION_NOT_COMMITTED")
        if not journal.accepted or not journal.local_step_committed:
            return ReceiptValidationDecision(
                "REJECTED", "JOURNAL_NOT_COMMITTED_OUTCOME"
            )
        expected_source_token = sha256(journal.observed_token.encode()).hexdigest()
        if signal.source_token != expected_source_token:
            return ReceiptValidationDecision(
                "REJECTED", "SIGNAL_JOURNAL_SOURCE_TOKEN_MISMATCH"
            )
        signal_payload = (
            signal.accepted,
            signal.local_step_committed,
            signal.local_sequence_after,
            signal.world_position_after,
            signal.position_delta,
            signal.remaining_signed_error,
        )
        journal_payload = (
            journal.accepted,
            journal.local_step_committed,
            journal.local_sequence_after,
            journal.world_position_after,
            journal.position_delta,
            journal.remaining_signed_error,
        )
        if signal_payload != journal_payload:
            return ReceiptValidationDecision(
                "REJECTED", "SIGNAL_JOURNAL_PAYLOAD_MISMATCH"
            )
        source_control_current = (
            source_frame.authority_epoch == current_authority_epoch
            and source_frame.authority_token == current_authority_token
        )
        proof = ValidatedReceiptProof(
            signal_token=signal.token(),
            transaction_id=journal.transaction_id,
            outcome_sequence=journal.outcome_sequence,
            provenance_valid=True,
            transaction_valid=True,
            source_control_current=source_control_current,
        )
        return ReceiptValidationDecision("VALIDATED", "RECEIPT_VALIDATED", proof)

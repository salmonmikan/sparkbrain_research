"""Bounded reconciliation horizon for FLY-0 receipt composition.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. This layer bounds retained
receipt state while keeping expiry as explicit uncertainty rather than a
zero/no-event WORLD claim.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Literal

from forge_prototypes.fly0_reconciliation_admission_gate import ReconciliationAdmissionGate
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal
from forge_prototypes.fly0_upstream_receipt_validator import (
    ExecutionJournalEntry,
    SourceFrameRecord,
    UpstreamReceiptValidator,
)

ObserverCertainty = Literal["EXACT_WITHIN_HORIZON", "DEGRADED_CAUSAL_GAP"]
HorizonStatus = Literal[
    "PENDING",
    "PENDING_CAPACITY_EXCEEDED",
    "VALIDATION_REJECTED",
    "RECONCILED",
    "DUPLICATE_NOOP",
    "OUT_OF_ORDER_NO_ROLLBACK",
    "OUTSIDE_RETENTION_HORIZON",
    "HORIZON_ADVANCED",
    "HORIZON_ADVANCE_BLOCKED",
    "RESYNCHRONIZED",
]


@dataclass(frozen=True)
class PendingReceipt:
    transaction_id: str
    outcome_sequence: int
    source_frame_token: str
    signal_source_token: str


@dataclass(frozen=True)
class HorizonDecision:
    status: HorizonStatus
    reason: str
    state_advanced: bool
    world_position: int | None
    outcome_watermark: int
    reconciliation_horizon_floor: int
    observer_certainty: ObserverCertainty
    pending_count: int
    retained_exact_count: int
    unresolved_gap_events: int


class BoundedReconciliationHorizon:
    def __init__(self, *, exact_window: int = 8, max_pending: int = 8) -> None:
        if exact_window < 1 or max_pending < 1:
            raise ValueError("exact_window and max_pending must be >= 1")
        self._exact_window = exact_window
        self._max_pending = max_pending
        self._floor = 0
        self._validator = UpstreamReceiptValidator()
        self._gate = ReconciliationAdmissionGate()
        self._pending: dict[str, PendingReceipt] = {}
        self._unresolved_gap_events = 0

    @property
    def world_position(self) -> int | None:
        return self._gate.world_position

    @property
    def outcome_watermark(self) -> int:
        return self._gate.last_outcome_sequence

    @property
    def reconciliation_horizon_floor(self) -> int:
        return self._floor

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    @property
    def observer_certainty(self) -> ObserverCertainty:
        return (
            "DEGRADED_CAUSAL_GAP"
            if self._unresolved_gap_events
            else "EXACT_WITHIN_HORIZON"
        )

    @property
    def retained_exact_count(self) -> int:
        return len(json.loads(self._gate.checkpoint())["consumed_transactions"])

    def _decision(
        self,
        status: HorizonStatus,
        reason: str,
        *,
        state_advanced: bool = False,
    ) -> HorizonDecision:
        return HorizonDecision(
            status=status,
            reason=reason,
            state_advanced=state_advanced,
            world_position=self.world_position,
            outcome_watermark=self.outcome_watermark,
            reconciliation_horizon_floor=self._floor,
            observer_certainty=self.observer_certainty,
            pending_count=len(self._pending),
            retained_exact_count=self.retained_exact_count,
            unresolved_gap_events=self._unresolved_gap_events,
        )

    def _record_gap(self) -> None:
        self._unresolved_gap_events += 1

    def _compact_gate(self, new_floor: int) -> None:
        payload = json.loads(self._gate.checkpoint())
        payload["consumed_transactions"] = {
            tx: entry
            for tx, entry in payload["consumed_transactions"].items()
            if entry["outcome_sequence"] >= new_floor
        }
        self._gate.restore(json.dumps(payload, sort_keys=True, separators=(",", ":")))

    def advance_horizon(
        self,
        new_floor: int,
        *,
        expire_pending: bool,
    ) -> HorizonDecision:
        if new_floor < self._floor:
            raise ValueError("reconciliation horizon must be monotonic")
        blocking = [
            p for p in self._pending.values() if p.outcome_sequence < new_floor
        ]
        if blocking and not expire_pending:
            return self._decision(
                "HORIZON_ADVANCE_BLOCKED",
                "PENDING_VALIDATOR_LINEAGE_STILL_ELIGIBLE",
            )
        if expire_pending:
            for pending in blocking:
                self._pending.pop(pending.transaction_id, None)
                self._record_gap()
        self._compact_gate(new_floor)
        self._floor = new_floor
        return self._decision(
            "HORIZON_ADVANCED",
            (
                "HORIZON_ADVANCED_WITH_EXPLICIT_UNRESOLVED_EXPIRY"
                if blocking
                else "HORIZON_ADVANCED_WITHOUT_CAUSAL_LOSS"
            ),
        )

    def _apply_window(self) -> None:
        if self.outcome_watermark < 0:
            return
        floor = max(0, self.outcome_watermark - self._exact_window + 1)
        if floor > self._floor:
            self.advance_horizon(floor, expire_pending=True)

    def submit(
        self,
        signal: TypedAscendingSignal,
        *,
        source_frame: SourceFrameRecord,
        journal: ExecutionJournalEntry,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> HorizonDecision:
        sequence = journal.outcome_sequence
        if sequence < self._floor:
            self._record_gap()
            return self._decision(
                "OUTSIDE_RETENTION_HORIZON",
                "CAUSAL_ITEM_OUTSIDE_EXACT_RETENTION_HORIZON",
            )

        pending = self._pending.get(journal.transaction_id)
        if signal.availability != "OBSERVED":
            candidate = PendingReceipt(
                transaction_id=journal.transaction_id,
                outcome_sequence=sequence,
                source_frame_token=source_frame.token(),
                signal_source_token=signal.source_token,
            )
            if pending is None:
                if len(self._pending) >= self._max_pending:
                    self._record_gap()
                    return self._decision(
                        "PENDING_CAPACITY_EXCEEDED",
                        "PENDING_BOUND_EXCEEDED_CAUSAL_ITEM_UNTRACKED",
                    )
                self._pending[journal.transaction_id] = candidate
            elif pending != candidate:
                return self._decision(
                    "VALIDATION_REJECTED",
                    "PENDING_CAUSAL_LINEAGE_CONFLICT",
                )
            return self._decision(
                "PENDING",
                "FEEDBACK_UNRESOLVED_WITHIN_RETENTION_HORIZON",
            )

        if pending is not None and (
            pending.outcome_sequence != sequence
            or pending.source_frame_token != source_frame.token()
            or pending.signal_source_token != signal.source_token
        ):
            return self._decision(
                "VALIDATION_REJECTED",
                "OBSERVED_FEEDBACK_DOES_NOT_MATCH_PENDING_CAUSAL_LINEAGE",
            )

        validation = self._validator.validate(
            signal,
            source_frame=source_frame,
            journal=journal,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        if validation.status != "VALIDATED" or validation.proof is None:
            return self._decision("VALIDATION_REJECTED", validation.reason)

        admitted = self._gate.admit(signal, validation.proof)
        if admitted.status in {
            "RECONCILED",
            "DUPLICATE_NOOP",
            "OUT_OF_ORDER_NO_ROLLBACK",
        }:
            self._pending.pop(journal.transaction_id, None)
            self._apply_window()
            return self._decision(
                admitted.status,
                admitted.reason,
                state_advanced=admitted.state_advanced,
            )
        return self._decision("VALIDATION_REJECTED", admitted.reason)

    def resynchronize(
        self,
        *,
        authoritative_world_position: int,
        outcome_sequence: int,
    ) -> HorizonDecision:
        if outcome_sequence < self.outcome_watermark:
            raise ValueError("resynchronization cannot move watermark backward")
        payload = json.loads(self._gate.checkpoint())
        payload["last_outcome_sequence"] = outcome_sequence
        payload["world_position"] = authoritative_world_position
        payload["consumed_transactions"] = {}
        self._gate.restore(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self._pending = {
            tx: pending
            for tx, pending in self._pending.items()
            if pending.outcome_sequence > outcome_sequence
        }
        self._unresolved_gap_events = 0
        self._floor = max(
            self._floor,
            max(0, outcome_sequence - self._exact_window + 1),
        )
        return self._decision(
            "RESYNCHRONIZED",
            "EXPLICIT_AUTHORITATIVE_WORLD_RESYNCHRONIZATION",
            state_advanced=True,
        )

    def checkpoint(self) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "exact_window": self._exact_window,
                "max_pending": self._max_pending,
                "reconciliation_horizon_floor": self._floor,
                "gate": self._gate.checkpoint(),
                "pending": {
                    tx: asdict(pending)
                    for tx, pending in sorted(self._pending.items())
                },
                "unresolved_gap_events": self._unresolved_gap_events,
                "observer_certainty": self.observer_certainty,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid checkpoint schema")
        if payload.get("exact_window") != self._exact_window:
            raise ValueError("exact_window mismatch")
        if payload.get("max_pending") != self._max_pending:
            raise ValueError("max_pending mismatch")
        floor = payload.get("reconciliation_horizon_floor")
        pending_raw = payload.get("pending")
        gaps = payload.get("unresolved_gap_events")
        gate_checkpoint = payload.get("gate")
        if not isinstance(floor, int) or floor < 0:
            raise ValueError("invalid reconciliation_horizon_floor")
        if not isinstance(pending_raw, dict):
            raise ValueError("invalid pending receipt state")
        if not isinstance(gaps, int) or gaps < 0:
            raise ValueError("invalid unresolved gap count")
        if not isinstance(gate_checkpoint, str):
            raise ValueError("invalid gate checkpoint")

        restored: dict[str, PendingReceipt] = {}
        for transaction_id, raw in pending_raw.items():
            if not isinstance(raw, dict):
                raise ValueError("invalid pending receipt")
            pending = PendingReceipt(**raw)
            if transaction_id != pending.transaction_id:
                raise ValueError("pending transaction identity mismatch")
            if pending.outcome_sequence < floor:
                raise ValueError("pending item below reconciliation horizon")
            restored[transaction_id] = pending
        if len(restored) > self._max_pending:
            raise ValueError("pending receipt bound exceeded")

        self._gate.restore(gate_checkpoint)
        self._floor = floor
        self._pending = restored
        self._unresolved_gap_events = gaps
        if payload.get("observer_certainty") != self.observer_certainty:
            raise ValueError("observer certainty does not match gap state")


def build_bounded_horizon_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "BOUNDED_RECONCILIATION_HORIZON_AND_UNRESOLVED_GAPS",
        "out_of_horizon_implies_zero_world_change": False,
        "expired_unresolved_is_explicit": True,
        "checkpoint_preserves_pending_horizon_and_gap_state": True,
        "ordinary_reduction": (
            "bounded event log / execution journal / idempotent consumer / checkpoint"
        ),
        "claim_boundary": (
            "Useful bounded systems engineering is not biological fidelity, topology "
            "superiority, efficiency, composition contribution, whole-system "
            "superiority, external validity, or scientific novelty."
        ),
    }

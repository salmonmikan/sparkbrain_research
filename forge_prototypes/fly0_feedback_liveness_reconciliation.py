"""Forge-only lifecycle coordinator for typed FLY-0 reafferent feedback.

This prototype tracks unavailable/delayed reafferent feedback without inventing a
zero/no-change WORLD outcome. A liveness timeout is operational metadata only:
a later transaction-valid committed outcome may still reconcile through the
separate admission gate exactly once.

This is noncanonical, non-evidentiary engineering work.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

from forge_prototypes.fly0_reconciliation_admission_gate import (
    ReconciliationAdmissionGate,
    ValidatedReceiptProof,
)
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal

FeedbackStatus = Literal[
    "IGNORED_NON_REAFFERENT",
    "PENDING",
    "PENDING_UPDATED",
    "TIMEOUT_NO_WORLD_ASSUMPTION",
    "LINEAGE_REJECTED",
    "RECEIPT_REQUIRED",
    "REJECTED_RECEIPT",
    "RECONCILED",
    "DUPLICATE_NOOP",
    "OUT_OF_ORDER_NO_ROLLBACK",
    "NOT_RECONCILABLE",
]


@dataclass
class _PendingFeedback:
    source_token: str
    deadline_step: int
    last_availability: str
    timed_out: bool = False


@dataclass(frozen=True)
class FeedbackDecision:
    status: FeedbackStatus
    reason: str
    feedback_id: str
    arrived_after_timeout: bool
    state_advanced: bool
    world_position: int | None
    pending_count: int
    reconciliation_status: str | None = None


class FeedbackLivenessReconciler:
    """Track feedback liveness separately from causal reconciliation validity."""

    def __init__(self) -> None:
        self._gate = ReconciliationAdmissionGate()
        self._pending: dict[str, _PendingFeedback] = {}
        self._clock_step = 0

    @property
    def world_position(self) -> int | None:
        return self._gate.world_position

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    @property
    def clock_step(self) -> int:
        return self._clock_step

    def _decision(
        self,
        *,
        status: FeedbackStatus,
        reason: str,
        feedback_id: str,
        arrived_after_timeout: bool = False,
        state_advanced: bool = False,
        reconciliation_status: str | None = None,
    ) -> FeedbackDecision:
        return FeedbackDecision(
            status=status,
            reason=reason,
            feedback_id=feedback_id,
            arrived_after_timeout=arrived_after_timeout,
            state_advanced=state_advanced,
            world_position=self._gate.world_position,
            pending_count=len(self._pending),
            reconciliation_status=reconciliation_status,
        )

    def advance_clock(self, current_step: int) -> tuple[FeedbackDecision, ...]:
        if current_step < self._clock_step:
            raise ValueError("current_step must be monotonic")
        self._clock_step = current_step
        decisions: list[FeedbackDecision] = []
        for feedback_id in sorted(self._pending):
            pending = self._pending[feedback_id]
            if not pending.timed_out and current_step >= pending.deadline_step:
                pending.timed_out = True
                decisions.append(
                    self._decision(
                        status="TIMEOUT_NO_WORLD_ASSUMPTION",
                        reason="FEEDBACK_DEADLINE_ELAPSED_WITHOUT_WORLD_INFERENCE",
                        feedback_id=feedback_id,
                        arrived_after_timeout=True,
                    )
                )
        return tuple(decisions)

    def submit(
        self,
        feedback_id: str,
        signal: TypedAscendingSignal,
        *,
        current_step: int,
        max_wait_steps: int | None = None,
        proof: ValidatedReceiptProof | None = None,
    ) -> FeedbackDecision:
        if not feedback_id:
            raise ValueError("feedback_id must be non-empty")
        if current_step < self._clock_step:
            raise ValueError("current_step must be monotonic")
        self.advance_clock(current_step)

        if signal.semantic_kind != "REAFFERENT_WORLD_OUTCOME":
            return self._decision(
                status="IGNORED_NON_REAFFERENT",
                reason="ONLY_REAFFERENT_FEEDBACK_HAS_LIVENESS_STATE",
                feedback_id=feedback_id,
            )

        pending = self._pending.get(feedback_id)

        if signal.availability != "OBSERVED":
            if max_wait_steps is None or max_wait_steps < 1:
                raise ValueError(
                    "unavailable feedback requires max_wait_steps >= 1"
                )
            if proof is not None:
                return self._decision(
                    status="NOT_RECONCILABLE",
                    reason="UNAVAILABLE_FEEDBACK_CANNOT_CONSUME_RECEIPT_PROOF",
                    feedback_id=feedback_id,
                )
            if pending is not None and pending.source_token != signal.source_token:
                return self._decision(
                    status="LINEAGE_REJECTED",
                    reason="FEEDBACK_SOURCE_TOKEN_CHANGED_WHILE_PENDING",
                    feedback_id=feedback_id,
                    arrived_after_timeout=pending.timed_out,
                )
            if pending is None:
                pending = _PendingFeedback(
                    source_token=signal.source_token,
                    deadline_step=current_step + max_wait_steps,
                    last_availability=signal.availability,
                )
                self._pending[feedback_id] = pending
                return self._decision(
                    status="PENDING",
                    reason="UNAVAILABLE_FEEDBACK_TRACKED_WITHOUT_WORLD_INFERENCE",
                    feedback_id=feedback_id,
                )

            pending.last_availability = signal.availability
            status: FeedbackStatus = (
                "TIMEOUT_NO_WORLD_ASSUMPTION"
                if pending.timed_out
                else "PENDING_UPDATED"
            )
            reason = (
                "FEEDBACK_REMAINS_UNAVAILABLE_AFTER_DEADLINE"
                if pending.timed_out
                else "FEEDBACK_AVAILABILITY_UPDATED_WITHOUT_DEADLINE_EXTENSION"
            )
            return self._decision(
                status=status,
                reason=reason,
                feedback_id=feedback_id,
                arrived_after_timeout=pending.timed_out,
            )

        if pending is not None and pending.source_token != signal.source_token:
            return self._decision(
                status="LINEAGE_REJECTED",
                reason="OBSERVED_FEEDBACK_DOES_NOT_MATCH_PENDING_SOURCE",
                feedback_id=feedback_id,
                arrived_after_timeout=pending.timed_out,
            )

        gate_decision = self._gate.admit(signal, proof)
        arrived_after_timeout = pending.timed_out if pending is not None else False
        gate_status = gate_decision.status

        if gate_status in {
            "RECONCILED",
            "DUPLICATE_NOOP",
            "OUT_OF_ORDER_NO_ROLLBACK",
        }:
            self._pending.pop(feedback_id, None)

        status_map: dict[str, FeedbackStatus] = {
            "RECEIPT_REQUIRED": "RECEIPT_REQUIRED",
            "REJECTED_RECEIPT": "REJECTED_RECEIPT",
            "RECONCILED": "RECONCILED",
            "DUPLICATE_NOOP": "DUPLICATE_NOOP",
            "OUT_OF_ORDER_NO_ROLLBACK": "OUT_OF_ORDER_NO_ROLLBACK",
            "NOT_RECONCILABLE": "NOT_RECONCILABLE",
            "NON_WORLD_SIGNAL": "NOT_RECONCILABLE",
        }
        return self._decision(
            status=status_map[gate_status],
            reason=gate_decision.reason,
            feedback_id=feedback_id,
            arrived_after_timeout=arrived_after_timeout,
            state_advanced=gate_decision.state_advanced,
            reconciliation_status=gate_status,
        )

    def checkpoint(self) -> str:
        payload = {
            "clock_step": self._clock_step,
            "gate": self._gate.checkpoint(),
            "pending": {
                feedback_id: {
                    "source_token": pending.source_token,
                    "deadline_step": pending.deadline_step,
                    "last_availability": pending.last_availability,
                    "timed_out": pending.timed_out,
                }
                for feedback_id, pending in sorted(self._pending.items())
            },
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        clock_step = payload["clock_step"]
        pending_payload = payload["pending"]
        gate_checkpoint = payload["gate"]
        if not isinstance(clock_step, int) or clock_step < 0:
            raise ValueError("invalid clock_step")
        if not isinstance(pending_payload, dict):
            raise ValueError("invalid pending feedback")
        if not isinstance(gate_checkpoint, str):
            raise ValueError("invalid gate checkpoint")

        restored: dict[str, _PendingFeedback] = {}
        for feedback_id, raw in pending_payload.items():
            if not isinstance(feedback_id, str) or not feedback_id:
                raise ValueError("invalid feedback_id")
            if not isinstance(raw, dict):
                raise ValueError("invalid pending entry")
            source_token = raw.get("source_token")
            deadline_step = raw.get("deadline_step")
            last_availability = raw.get("last_availability")
            timed_out = raw.get("timed_out")
            if not isinstance(source_token, str) or not source_token:
                raise ValueError("invalid source_token")
            if not isinstance(deadline_step, int) or deadline_step < 0:
                raise ValueError("invalid deadline_step")
            if not isinstance(last_availability, str):
                raise ValueError("invalid last_availability")
            if not isinstance(timed_out, bool):
                raise ValueError("invalid timed_out")
            restored[feedback_id] = _PendingFeedback(
                source_token=source_token,
                deadline_step=deadline_step,
                last_availability=last_availability,
                timed_out=timed_out,
            )

        self._gate.restore(gate_checkpoint)
        self._clock_step = clock_step
        self._pending = restored


def build_feedback_liveness_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "FEEDBACK_LIVENESS_RECONCILIATION",
        "timeout_implies_zero_world_change": False,
        "late_valid_committed_outcome_may_reconcile": True,
        "deadline_extension_on_repeat_unavailable_signal": False,
        "full_r22_receipt_contract_implemented": False,
        "ordinary_reduction": (
            "asynchronous event liveness tracker / idempotent transaction consumer"
        ),
        "claim_boundary": (
            "This coordinator adds liveness bookkeeping around typed feedback and "
            "an existing consumer admission gate. It does not validate source-command "
            "provenance, establish biological fidelity, topology superiority, "
            "efficiency, composition contribution, external validity, scientific "
            "novelty, scientific credit, or SYSTEM_BUILD completion."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_feedback_liveness_report(), indent=2, sort_keys=True))

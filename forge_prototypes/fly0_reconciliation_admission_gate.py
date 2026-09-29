"""Forge-only admission gate between typed FLY-0 feedback and WORLD reconciliation.

The gate does not validate the full R22 receipt contract. It consumes an
explicit upstream validation proof and prevents typed ascending signals from
being committed as WORLD facts unless that proof binds the exact signal to a
transaction-valid, provenance-valid receipt.

This is noncanonical, non-evidentiary engineering work.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal

DecisionStatus = Literal[
    "NON_WORLD_SIGNAL",
    "NOT_RECONCILABLE",
    "RECEIPT_REQUIRED",
    "REJECTED_RECEIPT",
    "RECONCILED",
    "DUPLICATE_NOOP",
    "OUT_OF_ORDER_NO_ROLLBACK",
]


@dataclass(frozen=True)
class ValidatedReceiptProof:
    """Narrow proof emitted by a separate full receipt validator."""

    signal_token: str
    transaction_id: str
    outcome_sequence: int
    provenance_valid: bool
    transaction_valid: bool
    source_control_current: bool

    def __post_init__(self) -> None:
        if not self.transaction_id:
            raise ValueError("transaction_id must be non-empty")
        if self.outcome_sequence < 0:
            raise ValueError("outcome_sequence must be non-negative")

    def identity(self) -> str:
        raw = json.dumps(
            {
                "signal_token": self.signal_token,
                "transaction_id": self.transaction_id,
                "outcome_sequence": self.outcome_sequence,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        return sha256(raw).hexdigest()


@dataclass(frozen=True)
class ReconciliationDecision:
    status: DecisionStatus
    reason: str
    state_advanced: bool
    world_position: int | None
    last_outcome_sequence: int


class ReconciliationAdmissionGate:
    """Bound replay of validated proofs without restoring stale control."""

    def __init__(self) -> None:
        self._last_outcome_sequence = -1
        self._world_position: int | None = None
        self._consumed_transactions: dict[str, tuple[str, int]] = {}
        self._consumed_signals: dict[str, str] = {}

    @property
    def world_position(self) -> int | None:
        return self._world_position

    @property
    def last_outcome_sequence(self) -> int:
        return self._last_outcome_sequence

    def _decision(
        self,
        status: DecisionStatus,
        reason: str,
        *,
        state_advanced: bool = False,
    ) -> ReconciliationDecision:
        return ReconciliationDecision(
            status=status,
            reason=reason,
            state_advanced=state_advanced,
            world_position=self._world_position,
            last_outcome_sequence=self._last_outcome_sequence,
        )

    def admit(
        self,
        signal: TypedAscendingSignal,
        proof: ValidatedReceiptProof | None = None,
    ) -> ReconciliationDecision:
        if signal.semantic_kind != "REAFFERENT_WORLD_OUTCOME":
            return self._decision(
                "NON_WORLD_SIGNAL",
                "ASCENDING_SEMANTICS_NOT_REAFFERENT_WORLD_OUTCOME",
            )
        if not signal.world_reconciliation_candidate:
            return self._decision(
                "NOT_RECONCILABLE",
                "REAFFERENT_SIGNAL_NOT_OBSERVED_COMMITTED_OUTCOME",
            )
        if proof is None:
            return self._decision(
                "RECEIPT_REQUIRED",
                "FULL_R22_VALIDATION_PROOF_REQUIRED",
            )
        if proof.signal_token != signal.token():
            return self._decision(
                "REJECTED_RECEIPT",
                "SIGNAL_RECEIPT_BINDING_MISMATCH",
            )
        if not proof.provenance_valid:
            return self._decision(
                "REJECTED_RECEIPT",
                "SOURCE_PROVENANCE_INVALID",
            )
        if not proof.transaction_valid:
            return self._decision(
                "REJECTED_RECEIPT",
                "TRANSACTION_INVALID",
            )

        prior_proof = self._consumed_transactions.get(proof.transaction_id)
        if prior_proof is not None:
            prior_signal, prior_sequence = prior_proof
            if (
                prior_signal == proof.signal_token
                and prior_sequence == proof.outcome_sequence
            ):
                return self._decision(
                    "DUPLICATE_NOOP",
                    "TRANSACTION_ALREADY_RECONCILED",
                )
            if prior_signal == proof.signal_token:
                return self._decision(
                    "REJECTED_RECEIPT",
                    "TRANSACTION_PROOF_SEQUENCE_CONFLICT",
                )
            return self._decision(
                "REJECTED_RECEIPT",
                "TRANSACTION_ID_COLLISION",
            )

        if proof.signal_token in self._consumed_signals:
            return self._decision(
                "REJECTED_RECEIPT",
                "SIGNAL_REPLAY_ACROSS_TRANSACTION",
            )

        self._consumed_transactions[proof.transaction_id] = (
            proof.signal_token,
            proof.outcome_sequence,
        )
        self._consumed_signals[proof.signal_token] = proof.transaction_id
        if proof.outcome_sequence <= self._last_outcome_sequence:
            return self._decision(
                "OUT_OF_ORDER_NO_ROLLBACK",
                "OLDER_COMMITTED_OUTCOME_RECORDED_WITHOUT_STATE_ROLLBACK",
            )

        self._last_outcome_sequence = proof.outcome_sequence
        self._world_position = signal.world_position_after
        return self._decision(
            "RECONCILED",
            (
                "COMMITTED_OUTCOME_RECONCILED"
                if proof.source_control_current
                else "COMMITTED_OUTCOME_RECONCILED_WITHOUT_CONTROL_RESTORATION"
            ),
            state_advanced=True,
        )

    def checkpoint(self) -> str:
        payload = {
            "schema_version": 2,
            "last_outcome_sequence": self._last_outcome_sequence,
            "world_position": self._world_position,
            "consumed_transactions": {
                transaction_id: {
                    "signal_token": signal_token,
                    "outcome_sequence": outcome_sequence,
                }
                for transaction_id, (
                    signal_token,
                    outcome_sequence,
                ) in sorted(self._consumed_transactions.items())
            },
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        last = payload["last_outcome_sequence"]
        world_position = payload["world_position"]
        consumed = payload["consumed_transactions"]
        if not isinstance(last, int) or last < -1:
            raise ValueError("invalid last_outcome_sequence")
        if world_position is not None and not isinstance(world_position, int):
            raise ValueError("invalid world_position")
        if payload.get("schema_version") != 2 or not isinstance(consumed, dict):
            raise ValueError("invalid checkpoint schema")
        restored_transactions: dict[str, tuple[str, int]] = {}
        restored_signals: dict[str, str] = {}
        for transaction_id, entry in consumed.items():
            if (
                not isinstance(transaction_id, str)
                or not transaction_id
                or not isinstance(entry, dict)
            ):
                raise ValueError("invalid consumed transaction proof")
            signal_token = entry.get("signal_token")
            outcome_sequence = entry.get("outcome_sequence")
            if not isinstance(signal_token, str) or not signal_token:
                raise ValueError("invalid consumed signal token")
            if not isinstance(outcome_sequence, int) or outcome_sequence < 0:
                raise ValueError("invalid consumed outcome sequence")
            if signal_token in restored_signals:
                raise ValueError("duplicate consumed signal token")
            restored_transactions[transaction_id] = (signal_token, outcome_sequence)
            restored_signals[signal_token] = transaction_id
        self._last_outcome_sequence = last
        self._world_position = world_position
        self._consumed_transactions = restored_transactions
        self._consumed_signals = restored_signals


def make_validation_proof(
    signal: TypedAscendingSignal,
    *,
    transaction_id: str,
    outcome_sequence: int,
    provenance_valid: bool = True,
    transaction_valid: bool = True,
    source_control_current: bool = True,
) -> ValidatedReceiptProof:
    return ValidatedReceiptProof(
        signal_token=signal.token(),
        transaction_id=transaction_id,
        outcome_sequence=outcome_sequence,
        provenance_valid=provenance_valid,
        transaction_valid=transaction_valid,
        source_control_current=source_control_current,
    )


def build_reconciliation_gate_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "TYPED_RECONCILIATION_ADMISSION_GATE",
        "full_r22_receipt_contract_implemented": False,
        "consumer_side_exactly_once_guard": False,
        "bounded_proof_replay_guard": True,
        "cross_transaction_signal_dedupe": True,
        "full_r24_receipt_validator_implemented": False,
        "stale_source_control_may_restore_control": False,
        "ordinary_reduction": "idempotent event consumer / transaction admission gate",
        "claim_boundary": (
            "This gate consumes an upstream receipt-validation proof. It does not "
            "itself establish source-command provenance, biological fidelity, "
            "topology superiority, efficiency, composition contribution, "
            "whole-system superiority, external validity, scientific novelty, "
            "scientific credit, or SYSTEM_BUILD completion."
        ),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            build_reconciliation_gate_report(),
            indent=2,
            sort_keys=True,
        )
    )

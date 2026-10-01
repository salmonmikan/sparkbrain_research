"""Effect-token-gated receipt/frontier composition for FLY-0.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. This wrapper requires an exact
local WORLD effect, a validated typed receipt, and current issue lineage before
the R27 causal frontier may advance. It records the exact effect token that
authorized each accepted frontier advance.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_causal_frontier import SessionCausalFrontierGuard
from forge_prototypes.fly0_issue_time_provenance_binding import (
    IssueBoundExecution,
    IssueTimeProvenanceBinding,
    IssuedSourceFrame,
)
from forge_prototypes.fly0_local_atomic_world_effect_journal import (
    LocalAtomicWorldEffectJournal,
    WorldEffectIntent,
    WorldEffectRecord,
)
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal
from forge_prototypes.fly0_upstream_receipt_validator import UpstreamReceiptValidator

GateStatus = Literal[
    "ACCEPTED",
    "EXACT_REPLAY",
    "RETIRED_ISSUE_LINEAGE",
    "FUTURE_ISSUE_LINEAGE",
    "EFFECT_JOIN_REJECTED",
    "RECEIPT_REJECTED",
    "EFFECT_RECEIPT_MISMATCH",
    "UNBOUND_FRONTIER_AHEAD",
    "RECONCILIATION_REJECTED",
    "FRONTIER_ADVANCE_REJECTED",
]


def _digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class EffectReceiptFrontierBinding:
    issue_id: str
    issue_token: str
    effect_token: str
    transaction_id: str
    outcome_sequence: int
    signal_token: str
    frontier_token: str

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class EffectGateDecision:
    status: GateStatus
    reason: str
    accepted: bool
    state_advanced: bool
    effect_token: str | None
    frontier_token: str
    binding: EffectReceiptFrontierBinding | None = None


class EffectReceiptFrontierGate:
    """Require one exact WORLD-effect token before causal-frontier advance."""

    def __init__(
        self,
        *,
        effect_journal: LocalAtomicWorldEffectJournal,
        provenance: IssueTimeProvenanceBinding,
        frontier: SessionCausalFrontierGuard,
        binding_window: int = 8,
    ) -> None:
        if binding_window < 1:
            raise ValueError("binding_window must be >= 1")
        self._effects = effect_journal
        self._provenance = provenance
        self._frontier = frontier
        self._validator = UpstreamReceiptValidator()
        self._binding_window = binding_window
        self._bindings: dict[str, EffectReceiptFrontierBinding] = {}
        self._binding_order: list[str] = []

    def _decision(
        self,
        status: GateStatus,
        reason: str,
        *,
        accepted: bool = False,
        advanced: bool = False,
        effect_token: str | None = None,
        binding: EffectReceiptFrontierBinding | None = None,
    ) -> EffectGateDecision:
        return EffectGateDecision(
            status=status,
            reason=reason,
            accepted=accepted,
            state_advanced=advanced,
            effect_token=effect_token,
            frontier_token=self._frontier.frontier.token(),
            binding=binding,
        )

    @staticmethod
    def _binding_matches(
        binding: EffectReceiptFrontierBinding,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        signal: TypedAscendingSignal,
        effect: WorldEffectRecord,
    ) -> bool:
        return (
            binding.issue_id == source.stamp.issue_id
            and binding.issue_token == source.token()
            and binding.effect_token == effect.token()
            and binding.transaction_id == execution.journal.transaction_id
            and binding.outcome_sequence == execution.journal.outcome_sequence
            and binding.signal_token == signal.token()
        )

    def _remember(self, binding: EffectReceiptFrontierBinding) -> None:
        self._bindings[binding.effect_token] = binding
        self._binding_order.append(binding.effect_token)
        while len(self._binding_order) > self._binding_window:
            retired = self._binding_order.pop(0)
            self._bindings.pop(retired, None)

    def submit(
        self,
        signal: TypedAscendingSignal,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        intent: WorldEffectIntent,
        effect: WorldEffectRecord | None,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> EffectGateDecision:
        if effect is not None:
            prior = self._bindings.get(effect.token())
            if prior is not None:
                if self._binding_matches(
                    prior,
                    source=source,
                    execution=execution,
                    signal=signal,
                    effect=effect,
                ):
                    return self._decision(
                        "EXACT_REPLAY",
                        "exact effect/receipt/frontier binding already accepted",
                        accepted=True,
                        effect_token=effect.token(),
                        binding=prior,
                    )
                return self._decision(
                    "EFFECT_RECEIPT_MISMATCH",
                    "effect token was previously bound to different receipt identity",
                    effect_token=effect.token(),
                )

        lineage = self._frontier.admit_issue_stamp(source.stamp)
        if not lineage.accepted:
            status: GateStatus = (
                "RETIRED_ISSUE_LINEAGE"
                if lineage.status == "RETIRED_ISSUE_LINEAGE"
                else "FUTURE_ISSUE_LINEAGE"
            )
            return self._decision(status, lineage.reason)

        joined = self._effects.verify_join(
            source=source,
            execution=execution,
            intent=intent,
            effect=effect,
        )
        if not joined.accepted or effect is None or joined.effect_token is None:
            return self._decision(
                "EFFECT_JOIN_REJECTED",
                joined.reason,
                effect_token=None if effect is None else effect.token(),
            )

        receipt = self._validator.validate(
            signal,
            source_frame=source.source_frame,
            journal=execution.journal,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        if receipt.status != "VALIDATED" or receipt.proof is None:
            return self._decision(
                "RECEIPT_REJECTED",
                receipt.reason,
                effect_token=effect.token(),
            )

        proof = receipt.proof
        expected_signal_source = sha256(effect.observed_token.encode()).hexdigest()
        if (
            joined.effect_token != effect.token()
            or proof.transaction_id != effect.transaction_id
            or proof.outcome_sequence != effect.outcome_sequence
            or proof.signal_token != signal.token()
            or signal.source_token != expected_signal_source
        ):
            return self._decision(
                "EFFECT_RECEIPT_MISMATCH",
                "validated receipt does not exactly reference committed effect identity",
                effect_token=effect.token(),
            )

        before = self._frontier.frontier.outcome_watermark
        if before >= effect.outcome_sequence:
            return self._decision(
                "UNBOUND_FRONTIER_AHEAD",
                "frontier already covers effect without retained exact binding",
                effect_token=effect.token(),
            )

        reconciled = self._provenance.submit(
            signal,
            source=source,
            execution=execution,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        if (
            reconciled.reconciliation_status != "RECONCILED"
            or not reconciled.state_advanced
        ):
            return self._decision(
                "RECONCILIATION_REJECTED",
                reconciled.reason,
                effect_token=effect.token(),
            )

        advanced = self._frontier.refresh_from_inner()
        if (
            not advanced.accepted
            or advanced.frontier.outcome_watermark < effect.outcome_sequence
        ):
            return self._decision(
                "FRONTIER_ADVANCE_REJECTED",
                advanced.reason,
                effect_token=effect.token(),
            )

        binding = EffectReceiptFrontierBinding(
            issue_id=source.stamp.issue_id,
            issue_token=source.token(),
            effect_token=effect.token(),
            transaction_id=effect.transaction_id,
            outcome_sequence=effect.outcome_sequence,
            signal_token=signal.token(),
            frontier_token=advanced.frontier.token(),
        )
        self._remember(binding)
        return self._decision(
            "ACCEPTED",
            "exact WORLD effect and receipt authorized causal-frontier advance",
            accepted=True,
            advanced=True,
            effect_token=effect.token(),
            binding=binding,
        )

    def checkpoint(self) -> str:
        payload = {
            "schema_version": 1,
            "frontier_checkpoint_digest": sha256(
                self._frontier.checkpoint().encode()
            ).hexdigest(),
            "bindings": [
                {
                    "record": asdict(self._bindings[token]),
                    "binding_token": self._bindings[token].token(),
                }
                for token in self._binding_order
                if token in self._bindings
            ],
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore_bindings(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid effect/frontier checkpoint schema")
        expected_frontier = sha256(self._frontier.checkpoint().encode()).hexdigest()
        if payload.get("frontier_checkpoint_digest") != expected_frontier:
            raise ValueError("frontier checkpoint mismatch")

        raw_bindings = payload.get("bindings")
        if not isinstance(raw_bindings, list):
            raise ValueError("invalid effect/frontier bindings")
        restored: list[EffectReceiptFrontierBinding] = []
        for item in raw_bindings:
            if not isinstance(item, dict) or not isinstance(item.get("record"), dict):
                raise ValueError("invalid effect/frontier binding")
            record = EffectReceiptFrontierBinding(**item["record"])
            if item.get("binding_token") != record.token():
                raise ValueError("effect/frontier binding token mismatch")
            restored.append(record)

        if len(restored) > self._binding_window:
            raise ValueError("binding checkpoint exceeds configured window")
        self._bindings = {record.effect_token: record for record in restored}
        self._binding_order = [record.effect_token for record in restored]


def build_effect_receipt_frontier_gate_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "EXACT_LOCAL_WORLD_EFFECT_TO_TYPED_RECEIPT_TO_R27_FRONTIER_GATE",
        "missing_effect_can_advance_frontier": False,
        "cross_wired_effect_can_advance_frontier": False,
        "frontier_advance_records_exact_effect_token": True,
        "ordinary_reduction": (
            "transactional outbox identity + receipt validation + monotonic frontier"
        ),
        "scientific_credit": 0,
    }

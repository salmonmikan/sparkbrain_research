"""Recovery-epoch fence for FLY-0 authoritative resynchronization.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. This layer prevents receipts
issued under a pre-resynchronization lineage from mutating WORLD state after an
authoritative resynchronization, even when their outcome sequence is newer
than the resynchronization watermark.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_bounded_reconciliation_horizon import (
    BoundedReconciliationHorizon,
    HorizonDecision,
)
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal
from forge_prototypes.fly0_upstream_receipt_validator import (
    ExecutionJournalEntry,
    SourceFrameRecord,
)

FenceStatus = Literal[
    "RECONCILIATION_RESULT",
    "RESYNCHRONIZED",
    "RETIRED_RECOVERY_EPOCH",
    "FUTURE_RECOVERY_EPOCH",
    "RECOVERY_LINEAGE_BINDING_REJECTED",
]


@dataclass(frozen=True)
class EpochBoundSourceFrame:
    recovery_epoch: int
    source_frame: SourceFrameRecord

    def __post_init__(self) -> None:
        if self.recovery_epoch < 0:
            raise ValueError("recovery_epoch must be non-negative")

    def token(self) -> str:
        raw = json.dumps(
            {
                "recovery_epoch": self.recovery_epoch,
                "source_frame": asdict(self.source_frame),
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        return sha256(raw).hexdigest()


@dataclass(frozen=True)
class EpochBoundExecutionJournal:
    recovery_epoch: int
    bound_source_token: str
    journal: ExecutionJournalEntry

    def __post_init__(self) -> None:
        if self.recovery_epoch < 0:
            raise ValueError("recovery_epoch must be non-negative")
        if not self.bound_source_token:
            raise ValueError("bound_source_token must be non-empty")


@dataclass(frozen=True)
class RecoveryFenceDecision:
    status: FenceStatus
    reason: str
    recovery_epoch: int
    state_advanced: bool
    world_position: int | None
    outcome_watermark: int
    pending_count: int
    reconciliation_status: str | None = None


class RecoveryEpochFencedReconciliation:
    """Fence pre-resynchronization receipt lineage behind recovery epochs.

    The recovery epoch is issue-time metadata. A bound source frame and its
    execution journal must retain the same epoch until reconciliation. An
    authoritative resynchronization advances the epoch and starts a fresh
    bounded reconciliation horizon, retiring all old pending/dedupe lineage.
    """

    def __init__(self, *, exact_window: int = 8, max_pending: int = 8) -> None:
        if exact_window < 1 or max_pending < 1:
            raise ValueError("exact_window and max_pending must be >= 1")
        self._exact_window = exact_window
        self._max_pending = max_pending
        self._recovery_epoch = 0
        self._horizon = BoundedReconciliationHorizon(
            exact_window=exact_window,
            max_pending=max_pending,
        )

    @property
    def recovery_epoch(self) -> int:
        return self._recovery_epoch

    @property
    def world_position(self) -> int | None:
        return self._horizon.world_position

    @property
    def outcome_watermark(self) -> int:
        return self._horizon.outcome_watermark

    @property
    def pending_count(self) -> int:
        return self._horizon.pending_count

    @property
    def reconciliation_horizon_floor(self) -> int:
        return self._horizon.reconciliation_horizon_floor

    def bind_source_frame(self, source_frame: SourceFrameRecord) -> EpochBoundSourceFrame:
        return EpochBoundSourceFrame(
            recovery_epoch=self._recovery_epoch,
            source_frame=source_frame,
        )

    def bind_execution(
        self,
        source: EpochBoundSourceFrame,
        journal: ExecutionJournalEntry,
    ) -> EpochBoundExecutionJournal:
        if source.recovery_epoch != self._recovery_epoch:
            raise ValueError("cannot bind execution for a retired recovery epoch")
        if journal.source_frame_token != source.source_frame.token():
            raise ValueError("execution journal does not match bound source frame")
        return EpochBoundExecutionJournal(
            recovery_epoch=source.recovery_epoch,
            bound_source_token=source.token(),
            journal=journal,
        )

    def _decision(
        self,
        status: FenceStatus,
        reason: str,
        *,
        state_advanced: bool = False,
        reconciliation_status: str | None = None,
    ) -> RecoveryFenceDecision:
        return RecoveryFenceDecision(
            status=status,
            reason=reason,
            recovery_epoch=self._recovery_epoch,
            state_advanced=state_advanced,
            world_position=self.world_position,
            outcome_watermark=self.outcome_watermark,
            pending_count=self.pending_count,
            reconciliation_status=reconciliation_status,
        )

    def _epoch_status(
        self,
        source: EpochBoundSourceFrame,
        journal: EpochBoundExecutionJournal,
    ) -> RecoveryFenceDecision | None:
        observed_epoch = min(source.recovery_epoch, journal.recovery_epoch)
        if observed_epoch < self._recovery_epoch:
            return self._decision(
                "RETIRED_RECOVERY_EPOCH",
                "PRE_RESYNCHRONIZATION_LINEAGE_RETIRED",
            )
        if (
            source.recovery_epoch > self._recovery_epoch
            or journal.recovery_epoch > self._recovery_epoch
        ):
            return self._decision(
                "FUTURE_RECOVERY_EPOCH",
                "RECOVERY_EPOCH_NOT_YET_OPEN",
            )
        return None

    def submit(
        self,
        signal: TypedAscendingSignal,
        *,
        source: EpochBoundSourceFrame,
        journal: EpochBoundExecutionJournal,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> RecoveryFenceDecision:
        epoch_rejection = self._epoch_status(source, journal)
        if epoch_rejection is not None:
            return epoch_rejection
        if source.recovery_epoch != journal.recovery_epoch:
            return self._decision(
                "RECOVERY_LINEAGE_BINDING_REJECTED",
                "SOURCE_AND_EXECUTION_RECOVERY_EPOCH_MISMATCH",
            )
        if journal.bound_source_token != source.token():
            return self._decision(
                "RECOVERY_LINEAGE_BINDING_REJECTED",
                "RECOVERY_SOURCE_ENVELOPE_TOKEN_MISMATCH",
            )
        if journal.journal.source_frame_token != source.source_frame.token():
            return self._decision(
                "RECOVERY_LINEAGE_BINDING_REJECTED",
                "BASE_SOURCE_FRAME_JOURNAL_MISMATCH",
            )

        decision = self._horizon.submit(
            signal,
            source_frame=source.source_frame,
            journal=journal.journal,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        return self._from_horizon(decision)

    def _from_horizon(self, decision: HorizonDecision) -> RecoveryFenceDecision:
        return self._decision(
            "RECONCILIATION_RESULT",
            decision.reason,
            state_advanced=decision.state_advanced,
            reconciliation_status=decision.status,
        )

    def resynchronize(
        self,
        *,
        authoritative_world_position: int,
        outcome_sequence: int,
    ) -> RecoveryFenceDecision:
        next_epoch = self._recovery_epoch + 1
        fresh = BoundedReconciliationHorizon(
            exact_window=self._exact_window,
            max_pending=self._max_pending,
        )
        decision = fresh.resynchronize(
            authoritative_world_position=authoritative_world_position,
            outcome_sequence=outcome_sequence,
        )
        self._horizon = fresh
        self._recovery_epoch = next_epoch
        return self._decision(
            "RESYNCHRONIZED",
            "AUTHORITATIVE_RESYNC_ADVANCED_RECOVERY_EPOCH",
            state_advanced=decision.state_advanced,
            reconciliation_status=decision.status,
        )

    def checkpoint(self) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "exact_window": self._exact_window,
                "max_pending": self._max_pending,
                "recovery_epoch": self._recovery_epoch,
                "horizon": self._horizon.checkpoint(),
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
        recovery_epoch = payload.get("recovery_epoch")
        horizon_checkpoint = payload.get("horizon")
        if not isinstance(recovery_epoch, int) or recovery_epoch < 0:
            raise ValueError("invalid recovery_epoch")
        if not isinstance(horizon_checkpoint, str):
            raise ValueError("invalid horizon checkpoint")
        restored = BoundedReconciliationHorizon(
            exact_window=self._exact_window,
            max_pending=self._max_pending,
        )
        restored.restore(horizon_checkpoint)
        self._recovery_epoch = recovery_epoch
        self._horizon = restored


def build_recovery_epoch_fence_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "AUTHORITATIVE_RESYNC_RECOVERY_EPOCH_FENCE",
        "pre_resync_receipt_may_mutate_post_resync_world": False,
        "resync_retires_old_pending_and_dedupe_lineage": True,
        "checkpoint_preserves_recovery_epoch": True,
        "ordinary_reduction": "epoch fencing / generation fencing / log rotation",
        "limitation": (
            "The recovery epoch must be stamped at source-frame issue time and "
            "carried by the execution journal; this prototype does not prove a "
            "non-cooperating producer cannot forge or restamp lineage metadata."
        ),
        "claim_boundary": (
            "Useful recovery fencing does not establish biological fidelity, "
            "topology superiority, efficiency, composition contribution, "
            "whole-system superiority, external validity, or scientific novelty."
        ),
    }

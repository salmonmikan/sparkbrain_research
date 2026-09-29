"""Forge-only CAS guard for authoritative FLY-0 resynchronization."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_recovery_epoch_fence import (
    EpochBoundExecutionJournal,
    EpochBoundSourceFrame,
    RecoveryEpochFencedReconciliation,
    RecoveryFenceDecision,
)
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal
from forge_prototypes.fly0_upstream_receipt_validator import (
    ExecutionJournalEntry,
    SourceFrameRecord,
)

ResyncCASStatus = Literal[
    "RESYNCHRONIZED",
    "DUPLICATE_RESYNC_NOOP",
    "RESYNC_IDENTITY_CONFLICT",
    "STALE_RESYNC_BASE",
    "FUTURE_RESYNC_BASE",
    "RESYNC_BASE_STATE_MISMATCH",
    "RESYNC_WATERMARK_ROLLBACK",
]


@dataclass(frozen=True)
class ResyncRequest:
    request_id: str
    base_recovery_epoch: int
    base_checkpoint_digest: str
    authoritative_world_position: int
    outcome_sequence: int

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must be non-empty")
        if self.base_recovery_epoch < 0:
            raise ValueError("base_recovery_epoch must be non-negative")
        if not self.base_checkpoint_digest:
            raise ValueError("base_checkpoint_digest must be non-empty")
        if self.outcome_sequence < 0:
            raise ValueError("outcome_sequence must be non-negative")

    def token(self) -> str:
        raw = json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode()
        return sha256(raw).hexdigest()


@dataclass(frozen=True)
class ResyncCASDecision:
    status: ResyncCASStatus
    reason: str
    recovery_epoch: int
    state_advanced: bool
    world_position: int | None
    outcome_watermark: int
    consumed_request_count: int


class RecoveryResyncCASGuard:
    def __init__(self, *, exact_window: int = 8, max_pending: int = 8) -> None:
        if exact_window < 1 or max_pending < 1:
            raise ValueError("exact_window and max_pending must be >= 1")
        self._exact_window = exact_window
        self._max_pending = max_pending
        self._fence = RecoveryEpochFencedReconciliation(
            exact_window=exact_window, max_pending=max_pending
        )
        self._consumed: dict[str, str] = {}

    @property
    def recovery_epoch(self) -> int:
        return self._fence.recovery_epoch

    @property
    def world_position(self) -> int | None:
        return self._fence.world_position

    @property
    def outcome_watermark(self) -> int:
        return self._fence.outcome_watermark

    @property
    def pending_count(self) -> int:
        return self._fence.pending_count

    @property
    def consumed_request_count(self) -> int:
        return len(self._consumed)

    def _digest(self) -> str:
        return sha256(self._fence.checkpoint().encode()).hexdigest()

    def _decision(
        self, status: ResyncCASStatus, reason: str, *, advanced: bool = False
    ) -> ResyncCASDecision:
        return ResyncCASDecision(
            status=status,
            reason=reason,
            recovery_epoch=self.recovery_epoch,
            state_advanced=advanced,
            world_position=self.world_position,
            outcome_watermark=self.outcome_watermark,
            consumed_request_count=len(self._consumed),
        )

    def issue_resync_request(
        self,
        *,
        request_id: str,
        authoritative_world_position: int,
        outcome_sequence: int,
    ) -> ResyncRequest:
        return ResyncRequest(
            request_id=request_id,
            base_recovery_epoch=self.recovery_epoch,
            base_checkpoint_digest=self._digest(),
            authoritative_world_position=authoritative_world_position,
            outcome_sequence=outcome_sequence,
        )

    def apply_resync(self, request: ResyncRequest) -> ResyncCASDecision:
        token = request.token()
        prior = self._consumed.get(request.request_id)
        if prior is not None:
            if prior == token:
                return self._decision(
                    "DUPLICATE_RESYNC_NOOP", "EXACT_RESYNC_REQUEST_ALREADY_CONSUMED"
                )
            return self._decision(
                "RESYNC_IDENTITY_CONFLICT",
                "RESYNC_REQUEST_ID_REUSED_WITH_DIFFERENT_CONTENT",
            )
        if request.base_recovery_epoch < self.recovery_epoch:
            return self._decision(
                "STALE_RESYNC_BASE", "RESYNC_REQUEST_BASE_EPOCH_RETIRED"
            )
        if request.base_recovery_epoch > self.recovery_epoch:
            return self._decision(
                "FUTURE_RESYNC_BASE", "RESYNC_REQUEST_BASE_EPOCH_NOT_YET_OPEN"
            )
        if request.base_checkpoint_digest != self._digest():
            return self._decision(
                "RESYNC_BASE_STATE_MISMATCH",
                "RESYNC_REQUEST_BASE_CHECKPOINT_CHANGED",
            )
        if request.outcome_sequence < self.outcome_watermark:
            return self._decision(
                "RESYNC_WATERMARK_ROLLBACK",
                "RESYNC_CANNOT_MOVE_OUTCOME_WATERMARK_BACKWARD",
            )
        applied = self._fence.resynchronize(
            authoritative_world_position=request.authoritative_world_position,
            outcome_sequence=request.outcome_sequence,
        )
        self._consumed[request.request_id] = token
        return self._decision(
            "RESYNCHRONIZED",
            "CAS_BOUND_AUTHORITATIVE_RESYNC_APPLIED",
            advanced=applied.state_advanced,
        )

    def bind_source_frame(self, source_frame: SourceFrameRecord) -> EpochBoundSourceFrame:
        return self._fence.bind_source_frame(source_frame)

    def bind_execution(
        self, source: EpochBoundSourceFrame, journal: ExecutionJournalEntry
    ) -> EpochBoundExecutionJournal:
        return self._fence.bind_execution(source, journal)

    def submit(
        self,
        signal: TypedAscendingSignal,
        *,
        source: EpochBoundSourceFrame,
        journal: EpochBoundExecutionJournal,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> RecoveryFenceDecision:
        return self._fence.submit(
            signal,
            source=source,
            journal=journal,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )

    def checkpoint(self) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "exact_window": self._exact_window,
                "max_pending": self._max_pending,
                "fence": self._fence.checkpoint(),
                "consumed_resync_requests": dict(sorted(self._consumed.items())),
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
        fence_checkpoint = payload.get("fence")
        consumed = payload.get("consumed_resync_requests")
        if not isinstance(fence_checkpoint, str) or not isinstance(consumed, dict):
            raise ValueError("invalid checkpoint payload")
        registry: dict[str, str] = {}
        for request_id, token in consumed.items():
            if not isinstance(request_id, str) or not request_id:
                raise ValueError("invalid consumed request id")
            if not isinstance(token, str) or not token:
                raise ValueError("invalid consumed request token")
            registry[request_id] = token
        fence = RecoveryEpochFencedReconciliation(
            exact_window=self._exact_window, max_pending=self._max_pending
        )
        fence.restore(fence_checkpoint)
        self._fence = fence
        self._consumed = registry


def build_resync_cas_guard_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "AUTHORITATIVE_RESYNC_COMPARE_AND_SWAP_IDEMPOTENCY_GUARD",
        "same_request_replay_advances_epoch": False,
        "same_id_conflict_can_overwrite_world": False,
        "stale_base_can_overwrite_newer_state": False,
        "ordinary_reduction": "compare-and-swap / idempotency key / replay protection",
        "limitation": (
            "The guard does not authenticate who is entitled to declare a snapshot "
            "authoritative; it only binds, deduplicates, and fences requests."
        ),
        "scientific_credit": 0,
    }

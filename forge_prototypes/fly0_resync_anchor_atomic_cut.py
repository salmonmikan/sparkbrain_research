"""Validated resynchronization anchor and atomic recovery cut for FLY-0.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. This prototype separates
WORLD/session truth from observer authority: certainty can be restored only
from a snapshot registered by an independent local WORLD ledger at an explicit
causal cut. The rebase is transactional across the WORLD cut and the bounded
reconciliation observer.
"""

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

WorldCommitStatus = Literal[
    "COMMITTED",
    "WRONG_WORLD_SESSION",
    "WORLD_CUT_PENDING_REBASE",
    "STALE_WORLD_ACTION_TICKET",
    "FUTURE_WORLD_ACTION_TICKET",
    "STALE_WORLD_ACTION_BASE",
    "OUTCOME_SEQUENCE_NOT_MONOTONIC",
]
AnchorValidationStatus = Literal[
    "VALIDATED",
    "WRONG_WORLD_SESSION",
    "UNKNOWN_CAUSAL_CUT",
    "CUT_RECORD_MISMATCH",
    "SNAPSHOT_DIGEST_MISMATCH",
    "STALE_ANCHOR_COVERAGE",
    "STALE_RECOVERY_EPOCH",
    "FUTURE_RECOVERY_EPOCH",
    "INVALID_RECOVERY_EPOCH_TRANSITION",
]
PendingDisposition = Literal["COVERED_BY_ANCHOR", "RETIRED_BY_REBASE"]
AtomicRebaseStatus = Literal[
    "ANCHOR_REBASE_APPLIED",
    "DUPLICATE_ANCHOR_NOOP",
    "ANCHOR_IDENTITY_CONFLICT",
    "ANCHOR_OUTSIDE_REPLAY_HORIZON",
    "UNCONSUMED_ANCHOR_REPLAY_REJECTED",
    "ANCHOR_VALIDATION_REJECTED",
    "ATOMIC_REBASE_ROLLED_BACK",
]


def _digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class WorldActionTicket:
    world_session_id: str
    world_cut_generation: int
    action_id: str
    base_outcome_sequence: int

    def __post_init__(self) -> None:
        if not self.world_session_id:
            raise ValueError("world_session_id must be non-empty")
        if self.world_cut_generation < 0:
            raise ValueError("world_cut_generation must be non-negative")
        if not self.action_id:
            raise ValueError("action_id must be non-empty")
        if self.base_outcome_sequence < 0:
            raise ValueError("base_outcome_sequence must be non-negative")


@dataclass(frozen=True)
class WorldCommitDecision:
    status: WorldCommitStatus
    reason: str
    state_advanced: bool
    world_position: int
    outcome_sequence: int
    world_cut_generation: int


@dataclass(frozen=True)
class WorldAnchorSnapshot:
    world_session_id: str
    anchor_id: str
    world_cut_generation: int
    source_checkpoint_token: str
    causal_cut_id: str
    covered_through_outcome_sequence: int
    world_position: int
    old_recovery_epoch: int
    proposed_recovery_epoch: int
    snapshot_digest: str

    def __post_init__(self) -> None:
        if not self.world_session_id:
            raise ValueError("world_session_id must be non-empty")
        if not self.anchor_id:
            raise ValueError("anchor_id must be non-empty")
        if self.world_cut_generation < 0:
            raise ValueError("world_cut_generation must be non-negative")
        if not self.source_checkpoint_token:
            raise ValueError("source_checkpoint_token must be non-empty")
        if not self.causal_cut_id:
            raise ValueError("causal_cut_id must be non-empty")
        if self.covered_through_outcome_sequence < 0:
            raise ValueError("covered sequence must be non-negative")
        if self.old_recovery_epoch < 0 or self.proposed_recovery_epoch < 0:
            raise ValueError("recovery epochs must be non-negative")
        if not self.snapshot_digest:
            raise ValueError("snapshot_digest must be non-empty")

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class ValidatedResyncAnchor:
    snapshot: WorldAnchorSnapshot
    validation_token: str

    def token(self) -> str:
        return _digest(
            {
                "snapshot_token": self.snapshot.token(),
                "validation_token": self.validation_token,
            }
        )


@dataclass(frozen=True)
class AnchorValidationDecision:
    status: AnchorValidationStatus
    reason: str
    anchor: ValidatedResyncAnchor | None = None


@dataclass(frozen=True)
class PendingClassification:
    transaction_id: str
    outcome_sequence: int
    disposition: PendingDisposition


@dataclass(frozen=True)
class ConsumedAnchor:
    anchor_token: str
    world_cut_generation: int


@dataclass(frozen=True)
class AtomicRebaseDecision:
    status: AtomicRebaseStatus
    reason: str
    state_advanced: bool
    recovery_epoch: int
    world_position: int | None
    outcome_watermark: int
    observer_certainty: str
    pending_classifications: tuple[PendingClassification, ...]
    consumed_anchor_count: int
    anchor_replay_floor: int
    anchor: ValidatedResyncAnchor | None = None


class WorldSessionLedger:
    """Independent local WORLD/session commit ledger used as anchor authority."""

    def __init__(
        self,
        *,
        world_session_id: str,
        initial_world_position: int,
        initial_outcome_sequence: int = 0,
        cut_window: int = 8,
    ) -> None:
        if not world_session_id:
            raise ValueError("world_session_id must be non-empty")
        if initial_outcome_sequence < 0:
            raise ValueError("initial_outcome_sequence must be non-negative")
        if cut_window < 1:
            raise ValueError("cut_window must be >= 1")
        self._world_session_id = world_session_id
        self._world_position = initial_world_position
        self._outcome_sequence = initial_outcome_sequence
        self._world_cut_generation = 0
        self._cut_window = cut_window
        self._cuts: dict[str, WorldAnchorSnapshot] = {}
        self._cut_order: list[str] = []
        self._cut_floor_generation = 0
        self._pending_anchor_id: str | None = None

    @property
    def world_session_id(self) -> str:
        return self._world_session_id

    @property
    def world_position(self) -> int:
        return self._world_position

    @property
    def outcome_sequence(self) -> int:
        return self._outcome_sequence

    @property
    def world_cut_generation(self) -> int:
        return self._world_cut_generation

    @property
    def cut_count(self) -> int:
        return len(self._cuts)

    @property
    def cut_floor_generation(self) -> int:
        return self._cut_floor_generation

    @property
    def cut_pending(self) -> bool:
        return self._pending_anchor_id is not None

    def _checkpoint_token(self) -> str:
        return _digest(
            {
                "world_session_id": self._world_session_id,
                "world_cut_generation": self._world_cut_generation,
                "world_position": self._world_position,
                "outcome_sequence": self._outcome_sequence,
            }
        )

    @staticmethod
    def expected_snapshot_digest(snapshot: WorldAnchorSnapshot) -> str:
        return _digest(
            {
                "world_session_id": snapshot.world_session_id,
                "anchor_id": snapshot.anchor_id,
                "world_cut_generation": snapshot.world_cut_generation,
                "source_checkpoint_token": snapshot.source_checkpoint_token,
                "causal_cut_id": snapshot.causal_cut_id,
                "covered_through_outcome_sequence": (
                    snapshot.covered_through_outcome_sequence
                ),
                "world_position": snapshot.world_position,
                "old_recovery_epoch": snapshot.old_recovery_epoch,
                "proposed_recovery_epoch": snapshot.proposed_recovery_epoch,
            }
        )

    def issue_action(self, action_id: str) -> WorldActionTicket:
        if self._pending_anchor_id is not None:
            raise RuntimeError("WORLD cut is pending rebase")
        return WorldActionTicket(
            world_session_id=self._world_session_id,
            world_cut_generation=self._world_cut_generation,
            action_id=action_id,
            base_outcome_sequence=self._outcome_sequence,
        )

    def _commit_decision(
        self,
        status: WorldCommitStatus,
        reason: str,
        *,
        advanced: bool = False,
    ) -> WorldCommitDecision:
        return WorldCommitDecision(
            status=status,
            reason=reason,
            state_advanced=advanced,
            world_position=self._world_position,
            outcome_sequence=self._outcome_sequence,
            world_cut_generation=self._world_cut_generation,
        )

    def commit_action(
        self,
        ticket: WorldActionTicket,
        *,
        world_position: int,
        outcome_sequence: int,
    ) -> WorldCommitDecision:
        if ticket.world_session_id != self._world_session_id:
            return self._commit_decision(
                "WRONG_WORLD_SESSION", "ACTION_TICKET_WORLD_SESSION_MISMATCH"
            )
        if self._pending_anchor_id is not None:
            return self._commit_decision(
                "WORLD_CUT_PENDING_REBASE",
                "ACTION_COMMIT_FENCED_DURING_ANCHOR_REBASE",
            )
        if ticket.world_cut_generation < self._world_cut_generation:
            return self._commit_decision(
                "STALE_WORLD_ACTION_TICKET", "ACTION_TICKET_CUT_GENERATION_RETIRED"
            )
        if ticket.world_cut_generation > self._world_cut_generation:
            return self._commit_decision(
                "FUTURE_WORLD_ACTION_TICKET",
                "ACTION_TICKET_CUT_GENERATION_NOT_YET_OPEN",
            )
        if ticket.base_outcome_sequence != self._outcome_sequence:
            return self._commit_decision(
                "STALE_WORLD_ACTION_BASE", "ACTION_TICKET_BASE_STATE_CHANGED"
            )
        if outcome_sequence <= self._outcome_sequence:
            return self._commit_decision(
                "OUTCOME_SEQUENCE_NOT_MONOTONIC",
                "WORLD_OUTCOME_SEQUENCE_MUST_ADVANCE",
            )
        self._world_position = world_position
        self._outcome_sequence = outcome_sequence
        return self._commit_decision(
            "COMMITTED", "WORLD_ACTION_COMMITTED", advanced=True
        )

    def snapshot_and_cut(
        self,
        *,
        anchor_id: str,
        old_recovery_epoch: int,
    ) -> WorldAnchorSnapshot:
        if not anchor_id:
            raise ValueError("anchor_id must be non-empty")
        if old_recovery_epoch < 0:
            raise ValueError("old_recovery_epoch must be non-negative")
        if self._pending_anchor_id is not None:
            raise RuntimeError("a WORLD cut is already pending rebase")

        checkpoint_token = self._checkpoint_token()
        generation = self._world_cut_generation
        cut_id = _digest(
            {
                "world_session_id": self._world_session_id,
                "anchor_id": anchor_id,
                "world_cut_generation": generation,
                "source_checkpoint_token": checkpoint_token,
                "outcome_sequence": self._outcome_sequence,
                "world_position": self._world_position,
            }
        )
        partial = WorldAnchorSnapshot(
            world_session_id=self._world_session_id,
            anchor_id=anchor_id,
            world_cut_generation=generation,
            source_checkpoint_token=checkpoint_token,
            causal_cut_id=cut_id,
            covered_through_outcome_sequence=self._outcome_sequence,
            world_position=self._world_position,
            old_recovery_epoch=old_recovery_epoch,
            proposed_recovery_epoch=old_recovery_epoch + 1,
            snapshot_digest="pending",
        )
        snapshot = WorldAnchorSnapshot(
            **{
                **asdict(partial),
                "snapshot_digest": self.expected_snapshot_digest(partial),
            }
        )
        self._cuts[cut_id] = snapshot
        self._cut_order.append(cut_id)
        while len(self._cut_order) > self._cut_window:
            retired_id = self._cut_order.pop(0)
            retired = self._cuts.pop(retired_id)
            self._cut_floor_generation = max(
                self._cut_floor_generation,
                retired.world_cut_generation + 1,
            )
        self._pending_anchor_id = anchor_id
        self._world_cut_generation += 1
        return snapshot

    def finalize_cut(self, anchor_id: str) -> None:
        if self._pending_anchor_id != anchor_id:
            raise ValueError("anchor_id does not own the pending WORLD cut")
        self._pending_anchor_id = None

    def lookup_cut(self, causal_cut_id: str) -> WorldAnchorSnapshot | None:
        return self._cuts.get(causal_cut_id)

    def checkpoint(self) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "world_session_id": self._world_session_id,
                "world_position": self._world_position,
                "outcome_sequence": self._outcome_sequence,
                "world_cut_generation": self._world_cut_generation,
                "cut_window": self._cut_window,
                "cut_floor_generation": self._cut_floor_generation,
                "pending_anchor_id": self._pending_anchor_id,
                "cut_order": list(self._cut_order),
                "cuts": {
                    cut_id: asdict(snapshot)
                    for cut_id, snapshot in sorted(self._cuts.items())
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid WORLD ledger checkpoint schema")
        if payload.get("world_session_id") != self._world_session_id:
            raise ValueError("WORLD session mismatch")
        if payload.get("cut_window") != self._cut_window:
            raise ValueError("cut_window mismatch")
        cuts_raw = payload.get("cuts")
        cut_order = payload.get("cut_order")
        if not isinstance(cuts_raw, dict) or not isinstance(cut_order, list):
            raise ValueError("invalid WORLD cut registry")
        cuts: dict[str, WorldAnchorSnapshot] = {}
        for cut_id, raw in cuts_raw.items():
            if not isinstance(raw, dict):
                raise ValueError("invalid WORLD cut record")
            snapshot = WorldAnchorSnapshot(**raw)
            if cut_id != snapshot.causal_cut_id:
                raise ValueError("WORLD cut identity mismatch")
            cuts[cut_id] = snapshot
        if set(cut_order) != set(cuts):
            raise ValueError("WORLD cut order mismatch")
        world_position = payload.get("world_position")
        sequence = payload.get("outcome_sequence")
        generation = payload.get("world_cut_generation")
        floor = payload.get("cut_floor_generation")
        pending = payload.get("pending_anchor_id")
        if not isinstance(world_position, int):
            raise ValueError("invalid WORLD position")
        if not isinstance(sequence, int) or sequence < 0:
            raise ValueError("invalid WORLD outcome sequence")
        if not isinstance(generation, int) or generation < 0:
            raise ValueError("invalid WORLD cut generation")
        if not isinstance(floor, int) or floor < 0:
            raise ValueError("invalid WORLD cut floor")
        if pending is not None and not isinstance(pending, str):
            raise ValueError("invalid pending anchor identity")
        self._world_position = world_position
        self._outcome_sequence = sequence
        self._world_cut_generation = generation
        self._cut_floor_generation = floor
        self._pending_anchor_id = pending
        self._cuts = cuts
        self._cut_order = list(cut_order)


class ResynchronizationAnchorValidator:
    """Validate a caller-visible snapshot against the independent WORLD ledger."""

    def __init__(self, ledger: WorldSessionLedger) -> None:
        self._ledger = ledger

    @staticmethod
    def _validation_token(snapshot: WorldAnchorSnapshot) -> str:
        return _digest(
            {
                "kind": "VALIDATED_WORLD_RESYNCHRONIZATION_ANCHOR",
                "snapshot_token": snapshot.token(),
            }
        )

    def validate(
        self,
        snapshot: WorldAnchorSnapshot,
        *,
        current_recovery_epoch: int,
        current_outcome_watermark: int,
    ) -> AnchorValidationDecision:
        if snapshot.world_session_id != self._ledger.world_session_id:
            return AnchorValidationDecision(
                "WRONG_WORLD_SESSION", "ANCHOR_WORLD_SESSION_MISMATCH"
            )
        canonical = self._ledger.lookup_cut(snapshot.causal_cut_id)
        if canonical is None:
            return AnchorValidationDecision(
                "UNKNOWN_CAUSAL_CUT", "ANCHOR_CAUSAL_CUT_NOT_IN_WORLD_LEDGER"
            )
        if canonical.token() != snapshot.token():
            return AnchorValidationDecision(
                "CUT_RECORD_MISMATCH", "ANCHOR_DOES_NOT_MATCH_WORLD_CUT_RECORD"
            )
        expected_digest = WorldSessionLedger.expected_snapshot_digest(snapshot)
        if snapshot.snapshot_digest != expected_digest:
            return AnchorValidationDecision(
                "SNAPSHOT_DIGEST_MISMATCH", "ANCHOR_SNAPSHOT_DIGEST_INVALID"
            )
        if snapshot.old_recovery_epoch < current_recovery_epoch:
            return AnchorValidationDecision(
                "STALE_RECOVERY_EPOCH", "ANCHOR_RECOVERY_EPOCH_RETIRED"
            )
        if snapshot.old_recovery_epoch > current_recovery_epoch:
            return AnchorValidationDecision(
                "FUTURE_RECOVERY_EPOCH", "ANCHOR_RECOVERY_EPOCH_NOT_YET_OPEN"
            )
        if snapshot.proposed_recovery_epoch != snapshot.old_recovery_epoch + 1:
            return AnchorValidationDecision(
                "INVALID_RECOVERY_EPOCH_TRANSITION",
                "ANCHOR_MUST_ADVANCE_EXACTLY_ONE_RECOVERY_EPOCH",
            )
        if snapshot.covered_through_outcome_sequence < current_outcome_watermark:
            return AnchorValidationDecision(
                "STALE_ANCHOR_COVERAGE",
                "ANCHOR_DOES_NOT_COVER_CURRENT_OBSERVER_WATERMARK",
            )
        anchor = ValidatedResyncAnchor(
            snapshot=snapshot,
            validation_token=self._validation_token(snapshot),
        )
        return AnchorValidationDecision("VALIDATED", "WORLD_ANCHOR_VALIDATED", anchor)

    def revalidate(
        self,
        anchor: ValidatedResyncAnchor,
        *,
        current_recovery_epoch: int,
        current_outcome_watermark: int,
    ) -> AnchorValidationDecision:
        expected = self._validation_token(anchor.snapshot)
        if anchor.validation_token != expected:
            return AnchorValidationDecision(
                "CUT_RECORD_MISMATCH", "VALIDATED_ANCHOR_TOKEN_MISMATCH"
            )
        return self.validate(
            anchor.snapshot,
            current_recovery_epoch=current_recovery_epoch,
            current_outcome_watermark=current_outcome_watermark,
        )


class _InjectedRebaseFailure(RuntimeError):
    pass


class AnchoredRecoveryReconciler:
    """Require an independently validated WORLD cut for certainty restoration."""

    def __init__(
        self,
        *,
        ledger: WorldSessionLedger,
        exact_window: int = 8,
        max_pending: int = 8,
        anchor_window: int = 8,
    ) -> None:
        if anchor_window < 1:
            raise ValueError("anchor_window must be >= 1")
        self._ledger = ledger
        self._validator = ResynchronizationAnchorValidator(ledger)
        self._fence = RecoveryEpochFencedReconciliation(
            exact_window=exact_window,
            max_pending=max_pending,
        )
        self._exact_window = exact_window
        self._max_pending = max_pending
        self._anchor_window = anchor_window
        self._consumed: dict[str, ConsumedAnchor] = {}
        self._consumed_order: list[str] = []
        self._anchor_replay_floor = 0

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
    def consumed_anchor_count(self) -> int:
        return len(self._consumed)

    @property
    def anchor_replay_floor(self) -> int:
        return self._anchor_replay_floor

    def _horizon_payload(self) -> dict[str, object]:
        fence_payload = json.loads(self._fence.checkpoint())
        return json.loads(fence_payload["horizon"])

    @property
    def observer_certainty(self) -> str:
        return str(self._horizon_payload()["observer_certainty"])

    @property
    def unresolved_gap_events(self) -> int:
        return int(self._horizon_payload()["unresolved_gap_events"])

    @property
    def retained_exact_count(self) -> int:
        gate = json.loads(str(self._horizon_payload()["gate"]))
        return len(gate["consumed_transactions"])

    def bind_source_frame(self, source_frame: SourceFrameRecord) -> EpochBoundSourceFrame:
        return self._fence.bind_source_frame(source_frame)

    def bind_execution(
        self,
        source: EpochBoundSourceFrame,
        journal: ExecutionJournalEntry,
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

    def validate_external_snapshot(
        self, snapshot: WorldAnchorSnapshot
    ) -> AnchorValidationDecision:
        return self._validator.validate(
            snapshot,
            current_recovery_epoch=self.recovery_epoch,
            current_outcome_watermark=self.outcome_watermark,
        )

    @staticmethod
    def _pending_classifications(
        fence_checkpoint: str,
        *,
        covered_through: int,
    ) -> tuple[PendingClassification, ...]:
        fence_payload = json.loads(fence_checkpoint)
        horizon = json.loads(fence_payload["horizon"])
        pending_raw = horizon["pending"]
        classifications = []
        for transaction_id, raw in sorted(pending_raw.items()):
            sequence = int(raw["outcome_sequence"])
            disposition: PendingDisposition = (
                "COVERED_BY_ANCHOR"
                if sequence <= covered_through
                else "RETIRED_BY_REBASE"
            )
            classifications.append(
                PendingClassification(
                    transaction_id=transaction_id,
                    outcome_sequence=sequence,
                    disposition=disposition,
                )
            )
        return tuple(classifications)

    def _decision(
        self,
        status: AtomicRebaseStatus,
        reason: str,
        *,
        advanced: bool = False,
        pending: tuple[PendingClassification, ...] = (),
        anchor: ValidatedResyncAnchor | None = None,
    ) -> AtomicRebaseDecision:
        return AtomicRebaseDecision(
            status=status,
            reason=reason,
            state_advanced=advanced,
            recovery_epoch=self.recovery_epoch,
            world_position=self.world_position,
            outcome_watermark=self.outcome_watermark,
            observer_certainty=self.observer_certainty,
            pending_classifications=pending,
            consumed_anchor_count=len(self._consumed),
            anchor_replay_floor=self._anchor_replay_floor,
            anchor=anchor,
        )

    def _remember_anchor(self, anchor: ValidatedResyncAnchor) -> None:
        anchor_id = anchor.snapshot.anchor_id
        self._consumed[anchor_id] = ConsumedAnchor(
            anchor_token=anchor.token(),
            world_cut_generation=anchor.snapshot.world_cut_generation,
        )
        self._consumed_order.append(anchor_id)
        while len(self._consumed_order) > self._anchor_window:
            retired_id = self._consumed_order.pop(0)
            retired = self._consumed.pop(retired_id)
            self._anchor_replay_floor = max(
                self._anchor_replay_floor,
                retired.world_cut_generation + 1,
            )

    def replay_anchor(self, anchor: ValidatedResyncAnchor) -> AtomicRebaseDecision:
        record = self._consumed.get(anchor.snapshot.anchor_id)
        if record is not None:
            if record.anchor_token == anchor.token():
                return self._decision(
                    "DUPLICATE_ANCHOR_NOOP",
                    "EXACT_VALIDATED_ANCHOR_ALREADY_CONSUMED",
                    anchor=anchor,
                )
            return self._decision(
                "ANCHOR_IDENTITY_CONFLICT",
                "ANCHOR_ID_REUSED_WITH_DIFFERENT_VALIDATED_CONTENT",
            )
        if anchor.snapshot.world_cut_generation < self._anchor_replay_floor:
            return self._decision(
                "ANCHOR_OUTSIDE_REPLAY_HORIZON",
                "ANCHOR_IDENTITY_OUTSIDE_EXACT_REPLAY_RETENTION",
            )
        return self._decision(
            "UNCONSUMED_ANCHOR_REPLAY_REJECTED",
            "ANCHOR_WAS_NOT_COMMITTED_BY_THIS_RECONCILER",
        )

    def atomic_rebase(
        self,
        *,
        anchor_id: str,
        fail_at: Literal["BEFORE_FENCE", "AFTER_FENCE", "AFTER_REGISTRY"] | None = None,
    ) -> AtomicRebaseDecision:
        prior = self._consumed.get(anchor_id)
        if prior is not None:
            return self._decision(
                "DUPLICATE_ANCHOR_NOOP",
                "ANCHOR_ID_ALREADY_COMMITTED",
            )

        ledger_before = self._ledger.checkpoint()
        fence_before = self._fence.checkpoint()
        consumed_before = dict(self._consumed)
        order_before = list(self._consumed_order)
        floor_before = self._anchor_replay_floor
        anchor: ValidatedResyncAnchor | None = None
        pending: tuple[PendingClassification, ...] = ()

        try:
            snapshot = self._ledger.snapshot_and_cut(
                anchor_id=anchor_id,
                old_recovery_epoch=self.recovery_epoch,
            )
            validation = self._validator.validate(
                snapshot,
                current_recovery_epoch=self.recovery_epoch,
                current_outcome_watermark=self.outcome_watermark,
            )
            if validation.status != "VALIDATED" or validation.anchor is None:
                self._ledger.restore(ledger_before)
                return self._decision(
                    "ANCHOR_VALIDATION_REJECTED",
                    validation.reason,
                )
            anchor = validation.anchor
            pending = self._pending_classifications(
                fence_before,
                covered_through=anchor.snapshot.covered_through_outcome_sequence,
            )
            if fail_at == "BEFORE_FENCE":
                raise _InjectedRebaseFailure("injected before fence rebase")

            applied = self._fence.resynchronize(
                authoritative_world_position=anchor.snapshot.world_position,
                outcome_sequence=anchor.snapshot.covered_through_outcome_sequence,
            )
            if self.recovery_epoch != anchor.snapshot.proposed_recovery_epoch:
                raise RuntimeError("recovery epoch did not match validated anchor")
            if fail_at == "AFTER_FENCE":
                raise _InjectedRebaseFailure("injected after fence rebase")

            self._remember_anchor(anchor)
            if fail_at == "AFTER_REGISTRY":
                raise _InjectedRebaseFailure("injected after anchor registry")

            self._ledger.finalize_cut(anchor.snapshot.anchor_id)
            return self._decision(
                "ANCHOR_REBASE_APPLIED",
                "VALIDATED_WORLD_ANCHOR_ATOMICALLY_REBASED",
                advanced=applied.state_advanced,
                pending=pending,
                anchor=anchor,
            )
        except _InjectedRebaseFailure:
            self._ledger.restore(ledger_before)
            self._fence.restore(fence_before)
            self._consumed = consumed_before
            self._consumed_order = order_before
            self._anchor_replay_floor = floor_before
            return self._decision(
                "ATOMIC_REBASE_ROLLED_BACK",
                "INJECTED_REBASE_FAILURE_RESTORED_PRE_ANCHOR_STATE",
                pending=pending,
                anchor=anchor,
            )

    def checkpoint(self) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "exact_window": self._exact_window,
                "max_pending": self._max_pending,
                "anchor_window": self._anchor_window,
                "fence": self._fence.checkpoint(),
                "consumed_anchors": {
                    anchor_id: asdict(record)
                    for anchor_id, record in sorted(self._consumed.items())
                },
                "consumed_order": list(self._consumed_order),
                "anchor_replay_floor": self._anchor_replay_floor,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid anchored reconciler checkpoint schema")
        if payload.get("exact_window") != self._exact_window:
            raise ValueError("exact_window mismatch")
        if payload.get("max_pending") != self._max_pending:
            raise ValueError("max_pending mismatch")
        if payload.get("anchor_window") != self._anchor_window:
            raise ValueError("anchor_window mismatch")
        consumed_raw = payload.get("consumed_anchors")
        order = payload.get("consumed_order")
        floor = payload.get("anchor_replay_floor")
        fence_checkpoint = payload.get("fence")
        if not isinstance(consumed_raw, dict) or not isinstance(order, list):
            raise ValueError("invalid consumed anchor registry")
        if not isinstance(floor, int) or floor < 0:
            raise ValueError("invalid anchor replay floor")
        if not isinstance(fence_checkpoint, str):
            raise ValueError("invalid recovery fence checkpoint")
        consumed: dict[str, ConsumedAnchor] = {}
        for anchor_id, raw in consumed_raw.items():
            if not isinstance(raw, dict):
                raise ValueError("invalid consumed anchor")
            consumed[anchor_id] = ConsumedAnchor(**raw)
        if set(order) != set(consumed):
            raise ValueError("consumed anchor order mismatch")
        if len(consumed) > self._anchor_window:
            raise ValueError("consumed anchor bound exceeded")
        fence = RecoveryEpochFencedReconciliation(
            exact_window=self._exact_window,
            max_pending=self._max_pending,
        )
        fence.restore(fence_checkpoint)
        self._fence = fence
        self._consumed = consumed
        self._consumed_order = list(order)
        self._anchor_replay_floor = floor


def build_resync_anchor_atomic_cut_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "VALIDATED_WORLD_ANCHOR_AND_ATOMIC_RECOVERY_EPOCH_CUT",
        "caller_self_attested_position_can_restore_certainty": False,
        "old_epoch_action_can_commit_after_cut": False,
        "old_receipt_can_mutate_post_anchor_world": False,
        "pending_lineage_disappears_silently": False,
        "atomic_failure_can_leave_mixed_rebase_state": False,
        "retained_anchor_identity_is_bounded": True,
        "ordinary_reduction": (
            "single-writer snapshot/WAL semantics + fencing generation + "
            "checkpoint/rollback + bounded idempotency registry"
        ),
        "simplification_comparator": "local SQLite/WAL single-writer transaction",
        "claim_boundary": (
            "Engineering usefulness does not establish biological fidelity, fly "
            "topology superiority, efficiency, composition contribution, "
            "whole-system superiority, external validity, or scientific novelty."
        ),
        "scientific_credit": 0,
    }

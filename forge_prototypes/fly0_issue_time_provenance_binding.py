"""Issue-time provenance binding for FLY-0 recovery lineage.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. The wrapper fixes causal
identity when a source frame is issued, before execution or later receipt
submission. Historical source material therefore cannot acquire the current
WORLD-cut/recovery lineage merely by being submitted after resynchronization.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal
from forge_prototypes.fly0_upstream_receipt_validator import (
    ExecutionJournalEntry,
    SourceFrameRecord,
)

IssueSubmitStatus = Literal[
    "RECONCILIATION_RESULT",
    "WRONG_WORLD_SESSION",
    "RETIRED_WORLD_CUT",
    "FUTURE_WORLD_CUT",
    "RETIRED_RECOVERY_EPOCH",
    "FUTURE_RECOVERY_EPOCH",
    "ISSUE_IDENTITY_CONFLICT",
    "UNKNOWN_ISSUE_ID",
    "ISSUE_OUTSIDE_REPLAY_HORIZON",
    "ISSUE_BINDING_REJECTED",
]


def _digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class IssueTimeStamp:
    world_session_id: str
    world_cut_generation: int
    recovery_epoch: int
    source_frame_token: str
    source_checkpoint_token: str
    issue_id: str
    issue_sequence: int

    def __post_init__(self) -> None:
        if not self.world_session_id:
            raise ValueError("world_session_id must be non-empty")
        if self.world_cut_generation < 0:
            raise ValueError("world_cut_generation must be non-negative")
        if self.recovery_epoch < 0:
            raise ValueError("recovery_epoch must be non-negative")
        if not self.source_frame_token:
            raise ValueError("source_frame_token must be non-empty")
        if not self.source_checkpoint_token:
            raise ValueError("source_checkpoint_token must be non-empty")
        if not self.issue_id:
            raise ValueError("issue_id must be non-empty")
        if self.issue_sequence < 0:
            raise ValueError("issue_sequence must be non-negative")

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class IssuedSourceFrame:
    stamp: IssueTimeStamp
    source_frame: SourceFrameRecord

    def token(self) -> str:
        return _digest(
            {
                "stamp_token": self.stamp.token(),
                "source_frame_token": self.source_frame.token(),
            }
        )


@dataclass(frozen=True)
class IssueBoundExecution:
    issue_token: str
    journal: ExecutionJournalEntry

    def __post_init__(self) -> None:
        if not self.issue_token:
            raise ValueError("issue_token must be non-empty")


@dataclass(frozen=True)
class IssueTimeProvenanceDecision:
    status: IssueSubmitStatus
    reason: str
    state_advanced: bool
    world_cut_generation: int
    recovery_epoch: int
    outcome_watermark: int
    reconciliation_status: str | None = None


class IssueTimeProvenanceBinding:
    """Bind WORLD/session/recovery identity at source issuance time.

    The issue registry is deliberately bounded. Evicted exact identities become
    unresolved/outside the replay horizon; they are never treated as current or
    silently accepted.
    """

    def __init__(
        self,
        *,
        ledger: WorldSessionLedger,
        reconciler: AnchoredRecoveryReconciler,
        issue_window: int = 8,
    ) -> None:
        if issue_window < 1:
            raise ValueError("issue_window must be >= 1")
        self._ledger = ledger
        self._reconciler = reconciler
        self._issue_window = issue_window
        self._issues: dict[str, IssuedSourceFrame] = {}
        self._issue_order: list[str] = []
        self._next_issue_sequence = 0
        self._issue_replay_floor = 0

    @property
    def issue_count(self) -> int:
        return len(self._issues)

    @property
    def issue_replay_floor(self) -> int:
        return self._issue_replay_floor

    def issue_source(
        self,
        source_frame: SourceFrameRecord,
        *,
        issue_id: str,
    ) -> IssuedSourceFrame:
        if not issue_id:
            raise ValueError("issue_id must be non-empty")
        if issue_id in self._issues:
            raise ValueError("issue_id is already retained")

        stamp = IssueTimeStamp(
            world_session_id=self._ledger.world_session_id,
            world_cut_generation=self._ledger.world_cut_generation,
            recovery_epoch=self._reconciler.recovery_epoch,
            source_frame_token=source_frame.token(),
            source_checkpoint_token=source_frame.source_checkpoint_token,
            issue_id=issue_id,
            issue_sequence=self._next_issue_sequence,
        )
        self._next_issue_sequence += 1
        issued = IssuedSourceFrame(stamp=stamp, source_frame=source_frame)
        self._issues[issue_id] = issued
        self._issue_order.append(issue_id)

        while len(self._issue_order) > self._issue_window:
            retired_id = self._issue_order.pop(0)
            retired = self._issues.pop(retired_id)
            self._issue_replay_floor = max(
                self._issue_replay_floor,
                retired.stamp.issue_sequence + 1,
            )
        return issued

    def lookup_issue(self, issue_id: str) -> IssuedSourceFrame | None:
        return self._issues.get(issue_id)

    def bind_execution(
        self,
        source: IssuedSourceFrame,
        journal: ExecutionJournalEntry,
    ) -> IssueBoundExecution:
        if journal.source_frame_token != source.source_frame.token():
            raise ValueError("execution journal does not match issued source frame")
        if source.stamp.source_frame_token != source.source_frame.token():
            raise ValueError("issued source frame token does not match immutable stamp")
        if (
            source.stamp.source_checkpoint_token
            != source.source_frame.source_checkpoint_token
        ):
            raise ValueError("source checkpoint token does not match immutable stamp")
        return IssueBoundExecution(issue_token=source.token(), journal=journal)

    def _decision(
        self,
        status: IssueSubmitStatus,
        reason: str,
        *,
        advanced: bool = False,
        reconciliation_status: str | None = None,
    ) -> IssueTimeProvenanceDecision:
        return IssueTimeProvenanceDecision(
            status=status,
            reason=reason,
            state_advanced=advanced,
            world_cut_generation=self._ledger.world_cut_generation,
            recovery_epoch=self._reconciler.recovery_epoch,
            outcome_watermark=self._reconciler.outcome_watermark,
            reconciliation_status=reconciliation_status,
        )

    def _registered_issue_status(
        self,
        source: IssuedSourceFrame,
    ) -> IssueTimeProvenanceDecision | None:
        retained = self._issues.get(source.stamp.issue_id)
        if retained is None:
            if source.stamp.issue_sequence < self._issue_replay_floor:
                return self._decision(
                    "ISSUE_OUTSIDE_REPLAY_HORIZON",
                    "ISSUE_IDENTITY_OUTSIDE_EXACT_RETENTION",
                )
            return self._decision("UNKNOWN_ISSUE_ID", "ISSUE_ID_NOT_REGISTERED")
        if retained.token() != source.token():
            return self._decision(
                "ISSUE_IDENTITY_CONFLICT",
                "ISSUE_ID_REUSED_OR_MUTATED_WITH_DIFFERENT_PROVENANCE",
            )
        return None

    def submit(
        self,
        signal: TypedAscendingSignal,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> IssueTimeProvenanceDecision:
        stamp = source.stamp
        if stamp.world_session_id != self._ledger.world_session_id:
            return self._decision(
                "WRONG_WORLD_SESSION",
                "ISSUED_SOURCE_WORLD_SESSION_MISMATCH",
            )

        registry_rejection = self._registered_issue_status(source)
        if registry_rejection is not None:
            return registry_rejection

        if execution.issue_token != source.token():
            return self._decision(
                "ISSUE_BINDING_REJECTED",
                "EXECUTION_NOT_BOUND_TO_ISSUED_SOURCE",
            )
        if execution.journal.source_frame_token != source.source_frame.token():
            return self._decision(
                "ISSUE_BINDING_REJECTED",
                "EXECUTION_JOURNAL_SOURCE_TOKEN_MISMATCH",
            )
        if stamp.source_frame_token != source.source_frame.token():
            return self._decision(
                "ISSUE_BINDING_REJECTED",
                "IMMUTABLE_SOURCE_TOKEN_MISMATCH",
            )
        if stamp.source_checkpoint_token != source.source_frame.source_checkpoint_token:
            return self._decision(
                "ISSUE_BINDING_REJECTED",
                "IMMUTABLE_CHECKPOINT_TOKEN_MISMATCH",
            )

        if stamp.world_cut_generation < self._ledger.world_cut_generation:
            return self._decision(
                "RETIRED_WORLD_CUT",
                "ISSUED_SOURCE_WORLD_CUT_RETIRED",
            )
        if stamp.world_cut_generation > self._ledger.world_cut_generation:
            return self._decision(
                "FUTURE_WORLD_CUT",
                "ISSUED_SOURCE_WORLD_CUT_NOT_YET_OPEN",
            )
        if stamp.recovery_epoch < self._reconciler.recovery_epoch:
            return self._decision(
                "RETIRED_RECOVERY_EPOCH",
                "ISSUED_SOURCE_RECOVERY_EPOCH_RETIRED",
            )
        if stamp.recovery_epoch > self._reconciler.recovery_epoch:
            return self._decision(
                "FUTURE_RECOVERY_EPOCH",
                "ISSUED_SOURCE_RECOVERY_EPOCH_NOT_YET_OPEN",
            )

        # Only after immutable issue-time lineage is proven current may the
        # existing recovery layer create its current-epoch envelope.
        epoch_source = self._reconciler.bind_source_frame(source.source_frame)
        epoch_execution = self._reconciler.bind_execution(
            epoch_source,
            execution.journal,
        )
        decision = self._reconciler.submit(
            signal,
            source=epoch_source,
            journal=epoch_execution,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        return self._decision(
            "RECONCILIATION_RESULT",
            decision.reason,
            advanced=decision.state_advanced,
            reconciliation_status=decision.reconciliation_status,
        )

    def checkpoint(self) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "world_session_id": self._ledger.world_session_id,
                "issue_window": self._issue_window,
                "next_issue_sequence": self._next_issue_sequence,
                "issue_replay_floor": self._issue_replay_floor,
                "issue_order": list(self._issue_order),
                "issues": {
                    issue_id: {
                        "stamp": asdict(issued.stamp),
                        "source_frame": asdict(issued.source_frame),
                    }
                    for issue_id, issued in sorted(self._issues.items())
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid issue-time provenance checkpoint schema")
        if payload.get("world_session_id") != self._ledger.world_session_id:
            raise ValueError("WORLD session mismatch")
        if payload.get("issue_window") != self._issue_window:
            raise ValueError("issue_window mismatch")

        next_sequence = payload.get("next_issue_sequence")
        floor = payload.get("issue_replay_floor")
        order = payload.get("issue_order")
        issues_raw = payload.get("issues")
        if not isinstance(next_sequence, int) or next_sequence < 0:
            raise ValueError("invalid next issue sequence")
        if not isinstance(floor, int) or floor < 0:
            raise ValueError("invalid issue replay floor")
        if not isinstance(order, list) or not isinstance(issues_raw, dict):
            raise ValueError("invalid issue registry")

        issues: dict[str, IssuedSourceFrame] = {}
        for issue_id, raw in issues_raw.items():
            if not isinstance(raw, dict):
                raise ValueError("invalid issue record")
            stamp_raw = raw.get("stamp")
            source_raw = raw.get("source_frame")
            if not isinstance(stamp_raw, dict) or not isinstance(source_raw, dict):
                raise ValueError("invalid issue provenance payload")
            stamp = IssueTimeStamp(**stamp_raw)
            source_frame = SourceFrameRecord(**source_raw)
            issued = IssuedSourceFrame(stamp=stamp, source_frame=source_frame)
            if stamp.issue_id != issue_id:
                raise ValueError("issue registry identity mismatch")
            if stamp.source_frame_token != source_frame.token():
                raise ValueError("issue registry source token mismatch")
            if stamp.source_checkpoint_token != source_frame.source_checkpoint_token:
                raise ValueError("issue registry checkpoint token mismatch")
            issues[issue_id] = issued

        if set(order) != set(issues):
            raise ValueError("issue order mismatch")
        if len(order) > self._issue_window:
            raise ValueError("issue retention bound exceeded")

        self._issues = issues
        self._issue_order = list(order)
        self._next_issue_sequence = next_sequence
        self._issue_replay_floor = floor


def build_issue_time_provenance_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "ISSUE_TIME_WORLD_CUT_AND_RECOVERY_LINEAGE_BINDING",
        "historical_source_can_be_restamped_as_current": False,
        "issue_identity_retention_is_bounded": True,
        "checkpoint_preserves_issue_identity": True,
        "ordinary_reduction": (
            "immutable provenance stamp + generation fencing + bounded "
            "idempotency/lineage registry"
        ),
        "simplification_comparator": "local SQLite/WAL single-writer issuance ledger",
        "limitation": (
            "This prototype authenticates lineage only against its local bounded "
            "issue registry; WORLD truth remains the separate validated anchor."
        ),
        "claim_boundary": (
            "Engineering usefulness does not establish biological fidelity, fly "
            "topology superiority, efficiency, composition contribution, "
            "whole-system superiority, external validity, or scientific novelty."
        ),
        "scientific_credit": 0,
    }

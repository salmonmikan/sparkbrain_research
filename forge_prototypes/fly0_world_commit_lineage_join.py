"""Exact issue-to-WORLD-commit lineage join for the FLY-0 recovery stack.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. This layer requires an
independent WORLD commit record to match the issue-time source, local execution
journal and observed receipt before the reconciliation observer may advance.
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
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    WorldActionTicket,
    WorldSessionLedger,
)
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal

CommitLineageStatus = Literal[
    "COMMITTED",
    "EXACT_COMMIT_REPLAY",
    "ISSUE_REJECTED",
    "WORLD_COMMIT_REJECTED",
    "COMMIT_IDENTITY_CONFLICT",
]
ReceiptJoinStatus = Literal[
    "RECONCILIATION_RESULT",
    "MISSING_WORLD_COMMIT",
    "COMMIT_OUTSIDE_REPLAY_HORIZON",
    "COMMIT_IDENTITY_CONFLICT",
    "ISSUE_COMMIT_CROSS_WIRE",
    "FRONTIER_REJECTED",
    "EXACT_REPLAY_NOOP",
]


def _digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class WorldCommitLineageRecord:
    world_session_id: str
    world_cut_generation: int
    recovery_epoch: int
    issue_id: str
    issue_sequence: int
    issue_token: str
    source_frame_token: str
    action_id: str
    base_outcome_sequence: int
    transaction_id: str
    outcome_sequence: int
    world_position_after: int
    observed_token: str

    def __post_init__(self) -> None:
        if not self.world_session_id:
            raise ValueError("world_session_id must be non-empty")
        for value, label in (
            (self.world_cut_generation, "world_cut_generation"),
            (self.recovery_epoch, "recovery_epoch"),
            (self.issue_sequence, "issue_sequence"),
            (self.base_outcome_sequence, "base_outcome_sequence"),
        ):
            if value < 0:
                raise ValueError(f"{label} must be non-negative")
        if self.outcome_sequence < 1:
            raise ValueError("outcome_sequence must be positive")
        for value, label in (
            (self.issue_id, "issue_id"),
            (self.issue_token, "issue_token"),
            (self.source_frame_token, "source_frame_token"),
            (self.action_id, "action_id"),
            (self.transaction_id, "transaction_id"),
            (self.observed_token, "observed_token"),
        ):
            if not value:
                raise ValueError(f"{label} must be non-empty")

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class CommitLineageDecision:
    status: CommitLineageStatus
    reason: str
    state_advanced: bool
    record: WorldCommitLineageRecord | None = None


@dataclass(frozen=True)
class ReceiptJoinDecision:
    status: ReceiptJoinStatus
    reason: str
    state_advanced: bool
    outcome_watermark: int
    reconciliation_status: str | None = None


class WorldCommitLineageJoin:
    """Require exact retained WORLD-commit lineage before reconciliation."""

    def __init__(
        self,
        *,
        ledger: WorldSessionLedger,
        provenance: IssueTimeProvenanceBinding,
        frontier: SessionCausalFrontierGuard,
        commit_window: int = 8,
    ) -> None:
        if commit_window < 1:
            raise ValueError("commit_window must be >= 1")
        self._ledger = ledger
        self._provenance = provenance
        self._frontier = frontier
        self._commit_window = commit_window
        self._records: dict[str, WorldCommitLineageRecord] = {}
        self._record_order: list[str] = []
        self._commit_replay_floor = 0
        self._submissions: dict[str, str] = {}

    @property
    def commit_count(self) -> int:
        return len(self._records)

    @property
    def commit_replay_floor(self) -> int:
        return self._commit_replay_floor

    def lookup_commit(self, issue_id: str) -> WorldCommitLineageRecord | None:
        return self._records.get(issue_id)

    def _issue_rejection(self, source: IssuedSourceFrame) -> str | None:
        retained = self._provenance.lookup_issue(source.stamp.issue_id)
        if retained is None:
            if source.stamp.issue_sequence < self._provenance.issue_replay_floor:
                return "ISSUE_IDENTITY_OUTSIDE_EXACT_RETENTION"
            return "ISSUE_ID_NOT_REGISTERED"
        if retained.token() != source.token():
            return "ISSUE_IDENTITY_CONFLICT"
        return None

    @staticmethod
    def _record_matches_request(
        record: WorldCommitLineageRecord,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        action_id: str,
    ) -> bool:
        journal = execution.journal
        stamp = source.stamp
        return (
            record.world_session_id == stamp.world_session_id
            and record.world_cut_generation == stamp.world_cut_generation
            and record.recovery_epoch == stamp.recovery_epoch
            and record.issue_id == stamp.issue_id
            and record.issue_sequence == stamp.issue_sequence
            and record.issue_token == source.token()
            and record.source_frame_token == source.source_frame.token()
            and record.action_id == action_id
            and record.transaction_id == journal.transaction_id
            and record.outcome_sequence == journal.outcome_sequence
            and record.world_position_after == journal.world_position_after
            and record.observed_token == journal.observed_token
        )

    def _retain(self, record: WorldCommitLineageRecord) -> None:
        self._records[record.issue_id] = record
        self._record_order.append(record.issue_id)
        while len(self._record_order) > self._commit_window:
            retired_id = self._record_order.pop(0)
            retired = self._records.pop(retired_id)
            self._submissions.pop(retired_id, None)
            self._commit_replay_floor = max(
                self._commit_replay_floor,
                retired.issue_sequence + 1,
            )

    def commit_world(
        self,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        action_id: str,
    ) -> CommitLineageDecision:
        rejection = self._issue_rejection(source)
        if rejection is not None:
            return CommitLineageDecision(
                "ISSUE_REJECTED",
                rejection,
                False,
            )
        if execution.issue_token != source.token():
            return CommitLineageDecision(
                "ISSUE_REJECTED",
                "EXECUTION_NOT_BOUND_TO_ISSUED_SOURCE",
                False,
            )
        if execution.journal.source_frame_token != source.source_frame.token():
            return CommitLineageDecision(
                "ISSUE_REJECTED",
                "EXECUTION_JOURNAL_SOURCE_TOKEN_MISMATCH",
                False,
            )

        frontier = self._frontier.admit_issue_stamp(source.stamp)
        if not frontier.accepted:
            return CommitLineageDecision(
                "ISSUE_REJECTED",
                f"FRONTIER_{frontier.status}:{frontier.reason}",
                False,
            )

        existing = self._records.get(source.stamp.issue_id)
        if existing is not None:
            if self._record_matches_request(
                existing,
                source=source,
                execution=execution,
                action_id=action_id,
            ):
                return CommitLineageDecision(
                    "EXACT_COMMIT_REPLAY",
                    "EXACT_WORLD_COMMIT_LINEAGE_ALREADY_RETAINED",
                    False,
                    existing,
                )
            return CommitLineageDecision(
                "COMMIT_IDENTITY_CONFLICT",
                "ISSUE_ID_ALREADY_BOUND_TO_DIFFERENT_WORLD_COMMIT",
                False,
            )

        try:
            ticket = self._ledger.issue_action(action_id)
        except RuntimeError as exc:
            return CommitLineageDecision(
                "WORLD_COMMIT_REJECTED",
                str(exc),
                False,
            )
        stamp = source.stamp
        if (
            ticket.world_session_id != stamp.world_session_id
            or ticket.world_cut_generation != stamp.world_cut_generation
        ):
            return CommitLineageDecision(
                "WORLD_COMMIT_REJECTED",
                "WORLD_ACTION_TICKET_DOES_NOT_MATCH_ISSUE_LINEAGE",
                False,
            )

        journal = execution.journal
        committed = self._ledger.commit_action(
            ticket,
            world_position=journal.world_position_after,
            outcome_sequence=journal.outcome_sequence,
        )
        if committed.status != "COMMITTED":
            return CommitLineageDecision(
                "WORLD_COMMIT_REJECTED",
                f"{committed.status}:{committed.reason}",
                False,
            )

        record = WorldCommitLineageRecord(
            world_session_id=stamp.world_session_id,
            world_cut_generation=stamp.world_cut_generation,
            recovery_epoch=stamp.recovery_epoch,
            issue_id=stamp.issue_id,
            issue_sequence=stamp.issue_sequence,
            issue_token=source.token(),
            source_frame_token=source.source_frame.token(),
            action_id=ticket.action_id,
            base_outcome_sequence=ticket.base_outcome_sequence,
            transaction_id=journal.transaction_id,
            outcome_sequence=journal.outcome_sequence,
            world_position_after=journal.world_position_after,
            observed_token=journal.observed_token,
        )
        self._retain(record)
        return CommitLineageDecision(
            "COMMITTED",
            "WORLD_COMMIT_RECORDED_WITH_EXACT_ISSUE_LINEAGE",
            True,
            record,
        )

    def _receipt_token(
        self,
        signal: TypedAscendingSignal,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        commit: WorldCommitLineageRecord,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> str:
        return _digest(
            {
                "signal_token": signal.token(),
                "issue_token": source.token(),
                "journal_transaction_id": execution.journal.transaction_id,
                "journal_outcome_sequence": execution.journal.outcome_sequence,
                "world_commit_token": commit.token(),
                "authority_epoch": current_authority_epoch,
                "authority_token": current_authority_token,
            }
        )

    def _join_matches(
        self,
        commit: WorldCommitLineageRecord,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
    ) -> bool:
        return self._record_matches_request(
            commit,
            source=source,
            execution=execution,
            action_id=commit.action_id,
        )

    def _receipt_decision(
        self,
        status: ReceiptJoinStatus,
        reason: str,
        *,
        advanced: bool = False,
        reconciliation_status: str | None = None,
    ) -> ReceiptJoinDecision:
        return ReceiptJoinDecision(
            status=status,
            reason=reason,
            state_advanced=advanced,
            outcome_watermark=self._frontier.frontier.outcome_watermark,
            reconciliation_status=reconciliation_status,
        )

    def submit(
        self,
        signal: TypedAscendingSignal,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        commit: WorldCommitLineageRecord | None,
        current_authority_epoch: int,
        current_authority_token: str,
    ) -> ReceiptJoinDecision:
        rejection = self._issue_rejection(source)
        if rejection is not None:
            return self._receipt_decision("COMMIT_IDENTITY_CONFLICT", rejection)

        if commit is None:
            if source.stamp.issue_sequence < self._commit_replay_floor:
                return self._receipt_decision(
                    "COMMIT_OUTSIDE_REPLAY_HORIZON",
                    "WORLD_COMMIT_LINEAGE_OUTSIDE_EXACT_RETENTION",
                )
            return self._receipt_decision(
                "MISSING_WORLD_COMMIT",
                "NO_RETAINED_WORLD_COMMIT_FOR_ISSUED_SOURCE",
            )

        if commit.issue_id != source.stamp.issue_id:
            return self._receipt_decision(
                "ISSUE_COMMIT_CROSS_WIRE",
                "WORLD_COMMIT_BELONGS_TO_DIFFERENT_ISSUE",
            )

        retained = self._records.get(source.stamp.issue_id)
        if retained is None:
            if source.stamp.issue_sequence < self._commit_replay_floor:
                return self._receipt_decision(
                    "COMMIT_OUTSIDE_REPLAY_HORIZON",
                    "WORLD_COMMIT_LINEAGE_OUTSIDE_EXACT_RETENTION",
                )
            return self._receipt_decision(
                "MISSING_WORLD_COMMIT",
                "WORLD_COMMIT_NOT_RETAINED",
            )
        if retained.token() != commit.token():
            return self._receipt_decision(
                "COMMIT_IDENTITY_CONFLICT",
                "SUPPLIED_WORLD_COMMIT_DOES_NOT_MATCH_RETAINED_RECORD",
            )
        if not self._join_matches(commit, source=source, execution=execution):
            return self._receipt_decision(
                "ISSUE_COMMIT_CROSS_WIRE",
                "ISSUE_WORLD_COMMIT_JOURNAL_JOIN_MISMATCH",
            )

        frontier = self._frontier.admit_issue_stamp(source.stamp)
        if not frontier.accepted:
            return self._receipt_decision(
                "FRONTIER_REJECTED",
                f"{frontier.status}:{frontier.reason}",
            )

        receipt_token = self._receipt_token(
            signal,
            source=source,
            execution=execution,
            commit=commit,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        prior_submission = self._submissions.get(source.stamp.issue_id)
        if prior_submission is not None:
            if prior_submission == receipt_token:
                return self._receipt_decision(
                    "EXACT_REPLAY_NOOP",
                    "EXACT_ISSUE_COMMIT_RECEIPT_REPLAY_ALREADY_CONSUMED",
                )
            return self._receipt_decision(
                "COMMIT_IDENTITY_CONFLICT",
                "ISSUE_ALREADY_CONSUMED_WITH_DIFFERENT_RECEIPT",
            )

        decision = self._provenance.submit(
            signal,
            source=source,
            execution=execution,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        if decision.state_advanced:
            refreshed = self._frontier.refresh_from_inner()
            if not refreshed.accepted:
                raise RuntimeError(
                    "inner reconciliation advanced outside durable causal frontier"
                )
        if (
            decision.status == "RECONCILIATION_RESULT"
            and decision.reconciliation_status == "RECONCILED"
        ):
            self._submissions[source.stamp.issue_id] = receipt_token

        return self._receipt_decision(
            "RECONCILIATION_RESULT",
            decision.reason,
            advanced=decision.state_advanced,
            reconciliation_status=decision.reconciliation_status,
        )

    def checkpoint(self) -> str:
        records = {
            issue_id: asdict(record)
            for issue_id, record in sorted(self._records.items())
        }
        return json.dumps(
            {
                "schema_version": 1,
                "world_session_id": self._ledger.world_session_id,
                "commit_window": self._commit_window,
                "commit_replay_floor": self._commit_replay_floor,
                "record_order": list(self._record_order),
                "records": records,
                "record_tokens": {
                    issue_id: self._records[issue_id].token()
                    for issue_id in sorted(self._records)
                },
                "submissions": dict(sorted(self._submissions.items())),
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid WORLD commit lineage checkpoint schema")
        if payload.get("world_session_id") != self._ledger.world_session_id:
            raise ValueError("WORLD session mismatch")
        if payload.get("commit_window") != self._commit_window:
            raise ValueError("commit_window mismatch")

        floor = payload.get("commit_replay_floor")
        order = payload.get("record_order")
        records_raw = payload.get("records")
        tokens = payload.get("record_tokens")
        submissions = payload.get("submissions")
        if not isinstance(floor, int) or floor < 0:
            raise ValueError("invalid commit replay floor")
        if not isinstance(order, list):
            raise ValueError("invalid WORLD commit record order")
        if not isinstance(records_raw, dict) or not isinstance(tokens, dict):
            raise ValueError("invalid WORLD commit lineage records")
        if not isinstance(submissions, dict):
            raise ValueError("invalid WORLD commit submission registry")

        records: dict[str, WorldCommitLineageRecord] = {}
        for issue_id, raw in records_raw.items():
            if not isinstance(raw, dict):
                raise ValueError("invalid WORLD commit lineage record")
            record = WorldCommitLineageRecord(**raw)
            if record.issue_id != issue_id:
                raise ValueError("WORLD commit issue identity mismatch")
            if record.world_session_id != self._ledger.world_session_id:
                raise ValueError("WORLD commit session mismatch")
            if tokens.get(issue_id) != record.token():
                raise ValueError("WORLD commit lineage token mismatch")
            records[issue_id] = record

        if set(order) != set(records):
            raise ValueError("WORLD commit record order mismatch")
        if len(order) > self._commit_window:
            raise ValueError("WORLD commit retention bound exceeded")
        if not set(submissions).issubset(records):
            raise ValueError("submission exists without retained WORLD commit")
        if not all(
            isinstance(issue_id, str) and isinstance(token, str) and token
            for issue_id, token in submissions.items()
        ):
            raise ValueError("invalid WORLD commit submission identity")

        self._records = records
        self._record_order = list(order)
        self._commit_replay_floor = floor
        self._submissions = dict(submissions)


def build_world_commit_lineage_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "ISSUE_TO_INDEPENDENT_WORLD_COMMIT_EXACT_LINEAGE_JOIN",
        "missing_world_commit_can_advance_observer": False,
        "cross_wired_issue_commit_allowed": False,
        "bounded_commit_retention": True,
        "checkpointable_after_commit_before_receipt": True,
        "ordinary_reduction": (
            "transactional outbox/WAL lineage + idempotency key + generation fencing"
        ),
        "simplification_comparator": (
            "local SQLite/WAL single-writer issuance/commit/receipt table"
        ),
        "limitation": (
            "The in-memory WORLD mutation and lineage-record insertion are not one "
            "crash-atomic storage transaction; a shared local WAL would be stronger."
        ),
        "claim_boundary": (
            "Engineering usefulness does not establish biological fidelity, fly "
            "topology superiority, efficiency, composition contribution, "
            "whole-system superiority, external validity, or scientific novelty."
        ),
        "scientific_credit": 0,
    }

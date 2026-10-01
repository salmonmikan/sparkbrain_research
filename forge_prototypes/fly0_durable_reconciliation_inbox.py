"""Cold-restart receipt/frontier comparator for FLY-0.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. Full issue/execution provenance
is retained in the same SQLite/WAL database as the R30 local WORLD/effect row.
Receipt deduplication and a scalar frontier advance are one transaction.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Literal

from forge_prototypes.fly0_issue_time_provenance_binding import (
    IssueBoundExecution,
    IssuedSourceFrame,
    IssueTimeStamp,
)
from forge_prototypes.fly0_local_atomic_world_effect_journal import WorldEffectRecord
from forge_prototypes.fly0_typed_ascending_signal import TypedAscendingSignal
from forge_prototypes.fly0_upstream_receipt_validator import (
    ExecutionJournalEntry,
    SourceFrameRecord,
    UpstreamReceiptValidator,
)

Status = Literal[
    "ACCEPTED",
    "EXACT_REPLAY",
    "ATOMIC_ROLLBACK",
    "MISSING_PROVENANCE",
    "PROVENANCE_TAMPERED",
    "MISSING_EFFECT",
    "EFFECT_TAMPERED",
    "WORLD_AUTHORITY_DIVERGED",
    "LINEAGE_RETIRED_OR_FUTURE",
    "RECEIPT_REJECTED",
    "OUTCOME_GAP",
    "FRONTIER_AHEAD_UNBOUND",
]


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _token(value: object) -> str:
    return sha256(_json(value).encode()).hexdigest()


@dataclass(frozen=True)
class DurableFrontier:
    world_session_id: str
    world_cut_generation: int
    recovery_epoch: int
    world_position: int
    outcome_watermark: int
    accepted_receipts: int

    def token(self) -> str:
        return _token(asdict(self))


@dataclass(frozen=True)
class ColdRestartContext:
    source: IssuedSourceFrame
    execution: IssueBoundExecution
    effect: WorldEffectRecord


@dataclass(frozen=True)
class InboxDecision:
    status: Status
    reason: str
    accepted: bool
    state_advanced: bool
    frontier: DurableFrontier
    effect_token: str | None = None


class _InjectedFailure(RuntimeError):
    pass


class DurableReconciliationInbox:
    """Durable provenance plus transactional receipt/frontier admission."""

    def __init__(self, path: str | Path) -> None:
        self._db = sqlite3.connect(str(path), isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("PRAGMA synchronous=FULL")
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS reconciliation_provenance (
              issue_id TEXT PRIMARY KEY,
              issue_sequence INTEGER NOT NULL UNIQUE,
              issue_token TEXT NOT NULL UNIQUE,
              source_token TEXT NOT NULL,
              source_payload TEXT NOT NULL,
              execution_token TEXT,
              execution_payload TEXT
            )
            """
        )
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS reconciliation_frontier (
              id INTEGER PRIMARY KEY CHECK(id=1),
              session TEXT NOT NULL,
              cut INTEGER NOT NULL,
              epoch INTEGER NOT NULL,
              position INTEGER NOT NULL,
              outcome INTEGER NOT NULL,
              accepted_receipts INTEGER NOT NULL
            )
            """
        )
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS reconciliation_inbox (
              effect_token TEXT PRIMARY KEY,
              issue_id TEXT NOT NULL,
              signal_token TEXT NOT NULL UNIQUE,
              transaction_id TEXT NOT NULL,
              outcome INTEGER NOT NULL
            )
            """
        )
        self._initialize_frontier()

    def close(self) -> None:
        self._db.close()

    def _world(self) -> sqlite3.Row:
        try:
            row = self._db.execute("SELECT * FROM world_state WHERE id=1").fetchone()
        except sqlite3.OperationalError as exc:
            raise ValueError("R30 WORLD journal must be initialized first") from exc
        if row is None:
            raise ValueError("R30 WORLD journal must be initialized first")
        return row

    def _initialize_frontier(self) -> None:
        row = self._db.execute(
            "SELECT * FROM reconciliation_frontier WHERE id=1"
        ).fetchone()
        if row is not None:
            return
        effect_count = int(
            self._db.execute("SELECT COUNT(*) FROM world_effects").fetchone()[0]
        )
        if effect_count:
            raise ValueError("frontier must be initialized before WORLD effects")
        world = self._world()
        self._db.execute(
            """
            INSERT INTO reconciliation_frontier
            VALUES (1, ?, ?, ?, ?, ?, 0)
            """,
            (
                str(world["session"]),
                int(world["cut"]),
                int(world["epoch"]),
                int(world["position"]),
                int(world["outcome"]),
            ),
        )

    def snapshot(self) -> DurableFrontier:
        row = self._db.execute(
            "SELECT * FROM reconciliation_frontier WHERE id=1"
        ).fetchone()
        if row is None:
            raise RuntimeError("durable frontier missing")
        return DurableFrontier(
            str(row["session"]),
            int(row["cut"]),
            int(row["epoch"]),
            int(row["position"]),
            int(row["outcome"]),
            int(row["accepted_receipts"]),
        )

    @staticmethod
    def _source_payload(source: IssuedSourceFrame) -> str:
        return _json(
            {
                "stamp": asdict(source.stamp),
                "source_frame": asdict(source.source_frame),
            }
        )

    @staticmethod
    def _execution_token(execution: IssueBoundExecution) -> str:
        return _token(
            {
                "issue_token": execution.issue_token,
                "journal": asdict(execution.journal),
            }
        )

    def persist_source(self, source: IssuedSourceFrame) -> None:
        if source.stamp.source_frame_token != source.source_frame.token():
            raise ValueError("source frame token mismatch")
        world = self._world()
        stamp = source.stamp
        if (
            stamp.world_session_id != str(world["session"])
            or stamp.world_cut_generation != int(world["cut"])
            or stamp.recovery_epoch != int(world["epoch"])
        ):
            raise ValueError("source lineage does not match durable WORLD")
        payload = self._source_payload(source)
        prior = self._db.execute(
            "SELECT * FROM reconciliation_provenance WHERE issue_id=?",
            (stamp.issue_id,),
        ).fetchone()
        if prior is not None:
            if (
                str(prior["issue_token"]) == source.token()
                and str(prior["source_payload"]) == payload
            ):
                return
            raise ValueError("issue_id already bound to different source")
        self._db.execute(
            """
            INSERT INTO reconciliation_provenance
            (issue_id, issue_sequence, issue_token, source_token, source_payload)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                stamp.issue_id,
                stamp.issue_sequence,
                source.token(),
                source.source_frame.token(),
                payload,
            ),
        )

    def persist_execution(
        self,
        execution: IssueBoundExecution,
        *,
        issue_id: str,
    ) -> None:
        row = self._db.execute(
            "SELECT * FROM reconciliation_provenance WHERE issue_id=?",
            (issue_id,),
        ).fetchone()
        if row is None:
            raise ValueError("source must be durable before execution")
        source = self._restore_source(row)
        if execution.issue_token != source.token():
            raise ValueError("execution issue token mismatch")
        if execution.journal.source_frame_token != source.source_frame.token():
            raise ValueError("execution source token mismatch")
        payload = _json(asdict(execution.journal))
        token = self._execution_token(execution)
        if row["execution_payload"] is not None:
            if (
                str(row["execution_payload"]) == payload
                and str(row["execution_token"]) == token
            ):
                return
            raise ValueError("issue_id already bound to different execution")
        self._db.execute(
            """
            UPDATE reconciliation_provenance
            SET execution_token=?, execution_payload=?
            WHERE issue_id=?
            """,
            (token, payload, issue_id),
        )

    def _restore_source(self, row: sqlite3.Row) -> IssuedSourceFrame:
        payload = json.loads(str(row["source_payload"]))
        stamp = IssueTimeStamp(**payload["stamp"])
        frame = SourceFrameRecord(**payload["source_frame"])
        source = IssuedSourceFrame(stamp=stamp, source_frame=frame)
        if (
            stamp.issue_id != str(row["issue_id"])
            or stamp.issue_sequence != int(row["issue_sequence"])
            or frame.token() != str(row["source_token"])
            or source.token() != str(row["issue_token"])
            or stamp.source_frame_token != frame.token()
            or stamp.source_checkpoint_token != frame.source_checkpoint_token
        ):
            raise ValueError("durable source identity mismatch")
        return source

    def _restore_execution(
        self,
        row: sqlite3.Row,
        source: IssuedSourceFrame,
    ) -> IssueBoundExecution:
        raw = row["execution_payload"]
        if raw is None or row["execution_token"] is None:
            raise LookupError("MISSING_PROVENANCE")
        journal = ExecutionJournalEntry(**json.loads(str(raw)))
        execution = IssueBoundExecution(source.token(), journal)
        if (
            journal.source_frame_token != source.source_frame.token()
            or self._execution_token(execution) != str(row["execution_token"])
        ):
            raise ValueError("durable execution identity mismatch")
        return execution

    @staticmethod
    def _effect(row: sqlite3.Row) -> WorldEffectRecord:
        return WorldEffectRecord(
            str(row["session"]),
            int(row["cut"]),
            int(row["epoch"]),
            str(row["issue_id"]),
            int(row["issue_sequence"]),
            str(row["issue_token"]),
            str(row["source_token"]),
            str(row["action_id"]),
            int(row["base_outcome"]),
            str(row["transaction_id"]),
            int(row["outcome"]),
            int(row["position"]),
            str(row["observed_token"]),
        )

    def reconstruct(self, issue_id: str) -> ColdRestartContext:
        row = self._db.execute(
            "SELECT * FROM reconciliation_provenance WHERE issue_id=?",
            (issue_id,),
        ).fetchone()
        if row is None:
            raise LookupError("MISSING_PROVENANCE")
        source = self._restore_source(row)
        execution = self._restore_execution(row, source)
        effect_row = self._db.execute(
            "SELECT * FROM world_effects WHERE issue_id=?",
            (issue_id,),
        ).fetchone()
        if effect_row is None:
            raise LookupError("MISSING_EFFECT")
        effect = self._effect(effect_row)
        journal = execution.journal
        if effect.token() != str(effect_row["effect_token"]):
            raise ValueError("WORLD effect token mismatch")
        if not (
            effect.issue_id == source.stamp.issue_id
            and effect.issue_sequence == source.stamp.issue_sequence
            and effect.issue_token == source.token()
            and effect.source_frame_token == source.source_frame.token()
            and effect.transaction_id == journal.transaction_id
            and effect.outcome_sequence == journal.outcome_sequence
            and effect.world_position_after == journal.world_position_after
            and effect.observed_token == journal.observed_token
        ):
            raise ValueError("WORLD effect provenance mismatch")
        return ColdRestartContext(source, execution, effect)

    def _decision(
        self,
        status: Status,
        reason: str,
        *,
        accepted: bool = False,
        advanced: bool = False,
        effect_token: str | None = None,
    ) -> InboxDecision:
        return InboxDecision(
            status,
            reason,
            accepted,
            advanced,
            self.snapshot(),
            effect_token,
        )

    def accept_receipt(
        self,
        signal: TypedAscendingSignal,
        *,
        issue_id: str,
        current_authority_epoch: int,
        current_authority_token: str,
        fail_at: Literal["AFTER_INBOX", "AFTER_FRONTIER"] | None = None,
    ) -> InboxDecision:
        try:
            context = self.reconstruct(issue_id)
        except LookupError as exc:
            status: Status = str(exc)  # type: ignore[assignment]
            return self._decision(status, status.replace("_", " ").lower())
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            return self._decision("PROVENANCE_TAMPERED", str(exc))

        source = context.source
        effect = context.effect
        frontier = self.snapshot()
        world = self._world()
        if (
            str(world["session"]) != frontier.world_session_id
            or int(world["cut"]) != frontier.world_cut_generation
            or int(world["epoch"]) != frontier.recovery_epoch
        ):
            return self._decision(
                "WORLD_AUTHORITY_DIVERGED",
                "WORLD lineage differs from durable receipt frontier",
                effect_token=effect.token(),
            )
        source_lineage = (
            source.stamp.world_session_id,
            source.stamp.world_cut_generation,
            source.stamp.recovery_epoch,
        )
        effect_lineage = (
            effect.world_session_id,
            effect.world_cut_generation,
            effect.recovery_epoch,
        )
        frontier_lineage = (
            frontier.world_session_id,
            frontier.world_cut_generation,
            frontier.recovery_epoch,
        )
        if source_lineage != frontier_lineage or effect_lineage != frontier_lineage:
            return self._decision(
                "LINEAGE_RETIRED_OR_FUTURE",
                "issue/effect lineage differs from durable causal frontier",
                effect_token=effect.token(),
            )
        receipt = UpstreamReceiptValidator().validate(
            signal,
            source_frame=source.source_frame,
            journal=context.execution.journal,
            current_authority_epoch=current_authority_epoch,
            current_authority_token=current_authority_token,
        )
        if (
            receipt.status != "VALIDATED"
            or receipt.proof is None
            or not receipt.proof.source_control_current
        ):
            return self._decision(
                "RECEIPT_REJECTED",
                receipt.reason,
                effect_token=effect.token(),
            )
        expected = sha256(effect.observed_token.encode()).hexdigest()
        if signal.source_token != expected:
            return self._decision(
                "RECEIPT_REJECTED",
                "receipt does not reference exact effect observation",
                effect_token=effect.token(),
            )

        prior = self._db.execute(
            "SELECT * FROM reconciliation_inbox WHERE effect_token=?",
            (effect.token(),),
        ).fetchone()
        if prior is not None:
            if (
                str(prior["issue_id"]) == issue_id
                and str(prior["signal_token"]) == signal.token()
            ):
                return self._decision(
                    "EXACT_REPLAY",
                    "receipt already committed",
                    accepted=True,
                    effect_token=effect.token(),
                )
            return self._decision(
                "PROVENANCE_TAMPERED",
                "effect is already bound to another receipt",
                effect_token=effect.token(),
            )
        if effect.outcome_sequence <= frontier.outcome_watermark:
            return self._decision(
                "FRONTIER_AHEAD_UNBOUND",
                "frontier already covers effect without inbox binding",
                effect_token=effect.token(),
            )
        if effect.outcome_sequence != frontier.outcome_watermark + 1:
            return self._decision(
                "OUTCOME_GAP",
                "receipt cannot skip unresolved outcome",
                effect_token=effect.token(),
            )

        self._db.execute("BEGIN IMMEDIATE")
        try:
            live = self.snapshot()
            if live != frontier:
                self._db.execute("ROLLBACK")
                return self.accept_receipt(
                    signal,
                    issue_id=issue_id,
                    current_authority_epoch=current_authority_epoch,
                    current_authority_token=current_authority_token,
                    fail_at=fail_at,
                )
            self._db.execute(
                """
                INSERT INTO reconciliation_inbox
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    effect.token(),
                    issue_id,
                    signal.token(),
                    effect.transaction_id,
                    effect.outcome_sequence,
                ),
            )
            if fail_at == "AFTER_INBOX":
                raise _InjectedFailure
            self._db.execute(
                """
                UPDATE reconciliation_frontier
                SET position=?, outcome=?, accepted_receipts=accepted_receipts+1
                WHERE id=1
                """,
                (effect.world_position_after, effect.outcome_sequence),
            )
            if fail_at == "AFTER_FRONTIER":
                raise _InjectedFailure
            self._db.execute("COMMIT")
        except _InjectedFailure:
            self._db.execute("ROLLBACK")
            return self._decision(
                "ATOMIC_ROLLBACK",
                "injected failure rolled back inbox and frontier",
                effect_token=effect.token(),
            )
        except sqlite3.IntegrityError:
            if self._db.in_transaction:
                self._db.execute("ROLLBACK")
            return self.accept_receipt(
                signal,
                issue_id=issue_id,
                current_authority_epoch=current_authority_epoch,
                current_authority_token=current_authority_token,
            )
        return self._decision(
            "ACCEPTED",
            "receipt and durable frontier committed atomically",
            accepted=True,
            advanced=True,
            effect_token=effect.token(),
        )


def build_durable_reconciliation_inbox_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "ONE_SQLITE_PROVENANCE_INBOX_SCALAR_FRONTIER",
        "cold_restart_reconstruction": True,
        "atomic_receipt_frontier": True,
        "remote_physical_exactly_once": False,
        "ordinary_reduction": "SQLite/WAL + idempotent inbox + scalar watermark",
        "scientific_credit": 0,
    }

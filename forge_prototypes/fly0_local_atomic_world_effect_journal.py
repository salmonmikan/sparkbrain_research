"""SQLite/WAL comparator for crash-atomic local WORLD effects.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. A local deterministic WORLD
mutation and its issue/action-bound effect row are committed in one transaction.
Local durability does not prove a remote or physical effect.
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
)

CommitStatus = Literal[
    "COMMITTED",
    "EXACT_REPLAY",
    "ATOMIC_ROLLBACK",
    "WRONG_WORLD_SESSION",
    "STALE_WORLD_CUT",
    "FUTURE_WORLD_CUT",
    "STALE_RECOVERY_EPOCH",
    "FUTURE_RECOVERY_EPOCH",
    "STALE_WORLD_BASE",
    "OUTCOME_SEQUENCE_NOT_MONOTONIC",
    "ISSUE_IDENTITY_CONFLICT",
]
JoinStatus = Literal[
    "EXACT_MATCH",
    "MISSING_EFFECT",
    "EFFECT_OUTSIDE_REPLAY_HORIZON",
    "ISSUE_EFFECT_CROSS_WIRE",
    "EFFECT_IDENTITY_CONFLICT",
]


def _digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class LocalWorldSnapshot:
    world_session_id: str
    world_cut_generation: int
    recovery_epoch: int
    world_position: int
    outcome_sequence: int
    effect_replay_floor: int


@dataclass(frozen=True)
class WorldEffectIntent:
    world_session_id: str
    world_cut_generation: int
    recovery_epoch: int
    issue_id: str
    issue_token: str
    action_id: str
    base_outcome_sequence: int

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class WorldEffectRecord:
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

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class CommitDecision:
    status: CommitStatus
    reason: str
    state_advanced: bool
    snapshot: LocalWorldSnapshot
    effect: WorldEffectRecord | None = None


@dataclass(frozen=True)
class JoinDecision:
    status: JoinStatus
    reason: str
    accepted: bool
    effect_token: str | None = None


class _InjectedFailure(RuntimeError):
    pass


class LocalAtomicWorldEffectJournal:
    """Persist local WORLD state and exact effect identity atomically."""

    def __init__(
        self,
        path: str | Path,
        *,
        world_session_id: str,
        initial_world_position: int,
        initial_outcome_sequence: int = 0,
        world_cut_generation: int = 0,
        recovery_epoch: int = 0,
        effect_window: int = 8,
    ) -> None:
        if not world_session_id or effect_window < 1:
            raise ValueError("invalid local WORLD configuration")
        if min(initial_outcome_sequence, world_cut_generation, recovery_epoch) < 0:
            raise ValueError("WORLD counters must be non-negative")
        self._effect_window = effect_window
        self._db = sqlite3.connect(str(path), isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("PRAGMA synchronous=FULL")
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS world_state (
              id INTEGER PRIMARY KEY CHECK(id=1),
              session TEXT NOT NULL,
              cut INTEGER NOT NULL,
              epoch INTEGER NOT NULL,
              position INTEGER NOT NULL,
              outcome INTEGER NOT NULL,
              replay_floor INTEGER NOT NULL,
              effect_window INTEGER NOT NULL
            )
            """
        )
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS world_effects (
              issue_id TEXT PRIMARY KEY,
              issue_sequence INTEGER NOT NULL UNIQUE,
              session TEXT NOT NULL,
              cut INTEGER NOT NULL,
              epoch INTEGER NOT NULL,
              issue_token TEXT NOT NULL,
              source_token TEXT NOT NULL,
              action_id TEXT NOT NULL,
              base_outcome INTEGER NOT NULL,
              transaction_id TEXT NOT NULL,
              outcome INTEGER NOT NULL,
              position INTEGER NOT NULL,
              observed_token TEXT NOT NULL,
              effect_token TEXT NOT NULL UNIQUE
            )
            """
        )
        row = self._db.execute("SELECT * FROM world_state WHERE id=1").fetchone()
        if row is None:
            self._db.execute(
                "INSERT INTO world_state VALUES (1, ?, ?, ?, ?, ?, 0, ?)",
                (
                    world_session_id,
                    world_cut_generation,
                    recovery_epoch,
                    initial_world_position,
                    initial_outcome_sequence,
                    effect_window,
                ),
            )
        elif row["session"] != world_session_id:
            raise ValueError("WORLD session mismatch")
        elif row["effect_window"] != effect_window:
            raise ValueError("effect_window mismatch")

    def close(self) -> None:
        self._db.close()

    def snapshot(self) -> LocalWorldSnapshot:
        row = self._db.execute("SELECT * FROM world_state WHERE id=1").fetchone()
        if row is None:
            raise RuntimeError("local WORLD state missing")
        return LocalWorldSnapshot(
            str(row["session"]),
            int(row["cut"]),
            int(row["epoch"]),
            int(row["position"]),
            int(row["outcome"]),
            int(row["replay_floor"]),
        )

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

    def lookup_effect(self, issue_id: str) -> WorldEffectRecord | None:
        row = self._db.execute(
            "SELECT * FROM world_effects WHERE issue_id=?", (issue_id,)
        ).fetchone()
        return None if row is None else self._effect(row)

    def issue_action(
        self, source: IssuedSourceFrame, *, action_id: str
    ) -> WorldEffectIntent:
        if not action_id:
            raise ValueError("action_id must be non-empty")
        state = self.snapshot()
        stamp = source.stamp
        if (
            stamp.world_session_id != state.world_session_id
            or stamp.world_cut_generation != state.world_cut_generation
            or stamp.recovery_epoch != state.recovery_epoch
        ):
            raise ValueError("issued source does not match current local WORLD lineage")
        return WorldEffectIntent(
            state.world_session_id,
            state.world_cut_generation,
            state.recovery_epoch,
            stamp.issue_id,
            source.token(),
            action_id,
            state.outcome_sequence,
        )

    @staticmethod
    def _matches(
        effect: WorldEffectRecord,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        intent: WorldEffectIntent,
    ) -> bool:
        j = execution.journal
        s = source.stamp
        return (
            effect.world_session_id == s.world_session_id
            and effect.world_cut_generation == s.world_cut_generation
            and effect.recovery_epoch == s.recovery_epoch
            and effect.issue_id == s.issue_id
            and effect.issue_sequence == s.issue_sequence
            and effect.issue_token == source.token()
            and effect.source_frame_token == source.source_frame.token()
            and effect.action_id == intent.action_id
            and effect.base_outcome_sequence == intent.base_outcome_sequence
            and effect.transaction_id == j.transaction_id
            and effect.outcome_sequence == j.outcome_sequence
            and effect.world_position_after == j.world_position_after
            and effect.observed_token == j.observed_token
        )

    def _decision(
        self,
        status: CommitStatus,
        reason: str,
        *,
        advanced: bool = False,
        effect: WorldEffectRecord | None = None,
    ) -> CommitDecision:
        return CommitDecision(status, reason, advanced, self.snapshot(), effect)

    def _reject(self, status: CommitStatus, reason: str) -> CommitDecision:
        self._db.execute("ROLLBACK")
        return self._decision(status, reason)

    def _prune(self) -> None:
        rows = self._db.execute(
            "SELECT issue_id, issue_sequence FROM world_effects ORDER BY issue_sequence"
        ).fetchall()
        floor = self.snapshot().effect_replay_floor
        while len(rows) > self._effect_window:
            row = rows.pop(0)
            self._db.execute(
                "DELETE FROM world_effects WHERE issue_id=?", (row["issue_id"],)
            )
            floor = max(floor, int(row["issue_sequence"]) + 1)
        self._db.execute(
            "UPDATE world_state SET replay_floor=? WHERE id=1", (floor,)
        )

    def commit_effect(
        self,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        intent: WorldEffectIntent,
        fail_at: Literal["AFTER_WORLD_UPDATE", "AFTER_EFFECT_INSERT"] | None = None,
    ) -> CommitDecision:
        if execution.issue_token != source.token():
            return self._decision(
                "ISSUE_IDENTITY_CONFLICT", "execution issue token mismatch"
            )
        if execution.journal.source_frame_token != source.source_frame.token():
            return self._decision(
                "ISSUE_IDENTITY_CONFLICT", "execution source token mismatch"
            )
        if intent.issue_id != source.stamp.issue_id or intent.issue_token != source.token():
            return self._decision(
                "ISSUE_IDENTITY_CONFLICT", "action intent issue mismatch"
            )

        self._db.execute("BEGIN IMMEDIATE")
        try:
            row = self._db.execute(
                "SELECT * FROM world_effects WHERE issue_id=?",
                (source.stamp.issue_id,),
            ).fetchone()
            if row is not None:
                effect = self._effect(row)
                if self._matches(effect, source, execution, intent):
                    self._db.execute("ROLLBACK")
                    return self._decision(
                        "EXACT_REPLAY", "exact effect already committed", effect=effect
                    )
                return self._reject(
                    "ISSUE_IDENTITY_CONFLICT",
                    "issue already bound to a different effect",
                )

            state = self.snapshot()
            stamp = source.stamp
            if stamp.world_session_id != state.world_session_id:
                return self._reject("WRONG_WORLD_SESSION", "WORLD session mismatch")
            if stamp.world_cut_generation < state.world_cut_generation:
                return self._reject("STALE_WORLD_CUT", "WORLD cut retired")
            if stamp.world_cut_generation > state.world_cut_generation:
                return self._reject("FUTURE_WORLD_CUT", "WORLD cut not open")
            if stamp.recovery_epoch < state.recovery_epoch:
                return self._reject("STALE_RECOVERY_EPOCH", "recovery epoch retired")
            if stamp.recovery_epoch > state.recovery_epoch:
                return self._reject(
                    "FUTURE_RECOVERY_EPOCH", "recovery epoch not open"
                )
            if (
                intent.world_session_id != state.world_session_id
                or intent.world_cut_generation != state.world_cut_generation
                or intent.recovery_epoch != state.recovery_epoch
            ):
                return self._reject(
                    "ISSUE_IDENTITY_CONFLICT", "action intent lineage mismatch"
                )
            if intent.base_outcome_sequence != state.outcome_sequence:
                return self._reject("STALE_WORLD_BASE", "action base state changed")

            journal = execution.journal
            if journal.outcome_sequence <= state.outcome_sequence:
                return self._reject(
                    "OUTCOME_SEQUENCE_NOT_MONOTONIC", "outcome must advance"
                )
            effect = WorldEffectRecord(
                state.world_session_id,
                state.world_cut_generation,
                state.recovery_epoch,
                stamp.issue_id,
                stamp.issue_sequence,
                source.token(),
                source.source_frame.token(),
                intent.action_id,
                intent.base_outcome_sequence,
                journal.transaction_id,
                journal.outcome_sequence,
                journal.world_position_after,
                journal.observed_token,
            )
            self._db.execute(
                "UPDATE world_state SET position=?, outcome=? WHERE id=1",
                (journal.world_position_after, journal.outcome_sequence),
            )
            if fail_at == "AFTER_WORLD_UPDATE":
                raise _InjectedFailure
            self._db.execute(
                "INSERT INTO world_effects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    effect.issue_id,
                    effect.issue_sequence,
                    effect.world_session_id,
                    effect.world_cut_generation,
                    effect.recovery_epoch,
                    effect.issue_token,
                    effect.source_frame_token,
                    effect.action_id,
                    effect.base_outcome_sequence,
                    effect.transaction_id,
                    effect.outcome_sequence,
                    effect.world_position_after,
                    effect.observed_token,
                    effect.token(),
                ),
            )
            self._prune()
            if fail_at == "AFTER_EFFECT_INSERT":
                raise _InjectedFailure
            self._db.execute("COMMIT")
            return self._decision(
                "COMMITTED",
                "WORLD mutation and effect row committed atomically",
                advanced=True,
                effect=effect,
            )
        except _InjectedFailure:
            self._db.execute("ROLLBACK")
            return self._decision(
                "ATOMIC_ROLLBACK", "injected failure rolled back WORLD and effect"
            )
        except Exception:
            if self._db.in_transaction:
                self._db.execute("ROLLBACK")
            raise

    def verify_join(
        self,
        *,
        source: IssuedSourceFrame,
        execution: IssueBoundExecution,
        intent: WorldEffectIntent,
        effect: WorldEffectRecord | None,
    ) -> JoinDecision:
        retained = self.lookup_effect(source.stamp.issue_id)
        if retained is None:
            if source.stamp.issue_sequence < self.snapshot().effect_replay_floor:
                return JoinDecision(
                    "EFFECT_OUTSIDE_REPLAY_HORIZON",
                    "effect identity outside exact retention",
                    False,
                )
            return JoinDecision("MISSING_EFFECT", "no retained effect", False)
        if effect is None:
            return JoinDecision("MISSING_EFFECT", "effect not supplied", False)
        if effect.issue_id != source.stamp.issue_id:
            return JoinDecision(
                "ISSUE_EFFECT_CROSS_WIRE", "effect belongs to another issue", False
            )
        if retained.token() != effect.token():
            return JoinDecision(
                "EFFECT_IDENTITY_CONFLICT", "effect token mismatch", False
            )
        if not self._matches(effect, source, execution, intent):
            return JoinDecision(
                "ISSUE_EFFECT_CROSS_WIRE", "exact issue/action/journal join failed", False
            )
        return JoinDecision(
            "EXACT_MATCH", "exact local WORLD effect join verified", True, effect.token()
        )


def build_local_atomic_world_effect_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "LOCAL_SQLITE_WAL_ATOMIC_WORLD_MUTATION_AND_EFFECT_ROW",
        "exact_issue_action_journal_effect_join_required": True,
        "crash_seam_is_one_local_transaction": True,
        "remote_or_physical_effect_proven": False,
        "ordinary_reduction": "SQLite/WAL ACID + identity fencing + bounded replay",
        "scientific_credit": 0,
    }

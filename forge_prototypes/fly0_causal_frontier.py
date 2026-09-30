"""Session-scoped causal frontier guard for FLY-0 recovery composition.

Forge-only, NON_EVIDENTIARY and NONCANONICAL. This layer keeps the durable
causal frontier above replaceable bounded-horizon/dedupe implementations so an
inner object cannot reset WORLD/session causal time when it is recreated.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_issue_time_provenance_binding import IssueTimeStamp
from forge_prototypes.fly0_resync_anchor_atomic_cut import (
    AnchoredRecoveryReconciler,
    WorldAnchorSnapshot,
    WorldSessionLedger,
)

FrontierStatus = Literal[
    "ACCEPTED",
    "WRONG_WORLD_SESSION",
    "WORLD_CUT_ROLLBACK",
    "RECOVERY_EPOCH_ROLLBACK",
    "OUTCOME_WATERMARK_ROLLBACK",
    "HORIZON_FLOOR_ROLLBACK",
    "STALE_ANCHOR_COVERAGE",
    "STALE_RECOVERY_EPOCH",
    "FUTURE_RECOVERY_EPOCH",
    "INVALID_RECOVERY_EPOCH_TRANSITION",
    "STALE_WORLD_CUT",
    "FUTURE_WORLD_CUT",
    "RETIRED_ISSUE_LINEAGE",
    "FUTURE_ISSUE_LINEAGE",
]


def _digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class ReconciliationFrontier:
    world_session_id: str
    world_cut_generation: int
    recovery_epoch: int
    outcome_watermark: int
    horizon_floor: int
    observer_certainty: str

    def __post_init__(self) -> None:
        if not self.world_session_id:
            raise ValueError("world_session_id must be non-empty")
        for value, label in (
            (self.world_cut_generation, "world_cut_generation"),
            (self.recovery_epoch, "recovery_epoch"),
            (self.horizon_floor, "horizon_floor"),
        ):
            if value < 0:
                raise ValueError(f"{label} must be non-negative")
        if self.outcome_watermark < -1:
            raise ValueError("outcome_watermark must be >= -1")
        if not self.observer_certainty:
            raise ValueError("observer_certainty must be non-empty")

    def token(self) -> str:
        return _digest(asdict(self))


@dataclass(frozen=True)
class FrontierDecision:
    status: FrontierStatus
    reason: str
    accepted: bool
    frontier: ReconciliationFrontier


class SessionCausalFrontierGuard:
    """Keep monotonic causal time outside replaceable reconciliation internals."""

    def __init__(
        self,
        *,
        ledger: WorldSessionLedger,
        reconciler: AnchoredRecoveryReconciler,
    ) -> None:
        self._ledger = ledger
        self._reconciler = reconciler
        observed = self._observe(reconciler)
        if observed.world_session_id != ledger.world_session_id:
            raise ValueError("reconciler WORLD session mismatch")
        if observed.world_cut_generation != ledger.world_cut_generation:
            raise ValueError("reconciler WORLD cut mismatch")
        self._frontier = observed

    @property
    def frontier(self) -> ReconciliationFrontier:
        return self._frontier

    @staticmethod
    def _reconciler_ledger(
        reconciler: AnchoredRecoveryReconciler,
    ) -> WorldSessionLedger:
        ledger = getattr(reconciler, "_ledger", None)
        if not isinstance(ledger, WorldSessionLedger):
            raise ValueError("reconciler has no inspectable WORLD ledger")
        return ledger

    @staticmethod
    def _horizon_floor(reconciler: AnchoredRecoveryReconciler) -> int:
        payload = json.loads(reconciler.checkpoint())
        fence = json.loads(payload["fence"])
        horizon = json.loads(fence["horizon"])
        return int(horizon["reconciliation_horizon_floor"])

    def _observe(
        self,
        reconciler: AnchoredRecoveryReconciler,
    ) -> ReconciliationFrontier:
        ledger = self._reconciler_ledger(reconciler)
        return ReconciliationFrontier(
            world_session_id=ledger.world_session_id,
            world_cut_generation=ledger.world_cut_generation,
            recovery_epoch=reconciler.recovery_epoch,
            outcome_watermark=reconciler.outcome_watermark,
            horizon_floor=self._horizon_floor(reconciler),
            observer_certainty=reconciler.observer_certainty,
        )

    def _decision(
        self,
        status: FrontierStatus,
        reason: str,
        *,
        accepted: bool = False,
    ) -> FrontierDecision:
        return FrontierDecision(
            status=status,
            reason=reason,
            accepted=accepted,
            frontier=self._frontier,
        )

    def validate_inner(
        self,
        candidate: AnchoredRecoveryReconciler,
    ) -> FrontierDecision:
        observed = self._observe(candidate)
        current = self._frontier
        if observed.world_session_id != current.world_session_id:
            return self._decision(
                "WRONG_WORLD_SESSION",
                "INNER_RECONCILER_WORLD_SESSION_MISMATCH",
            )
        if observed.world_cut_generation < current.world_cut_generation:
            return self._decision(
                "WORLD_CUT_ROLLBACK",
                "INNER_RECONCILER_WORLD_CUT_BEHIND_DURABLE_FRONTIER",
            )
        if observed.recovery_epoch < current.recovery_epoch:
            return self._decision(
                "RECOVERY_EPOCH_ROLLBACK",
                "INNER_RECONCILER_RECOVERY_EPOCH_BEHIND_DURABLE_FRONTIER",
            )
        if observed.outcome_watermark < current.outcome_watermark:
            return self._decision(
                "OUTCOME_WATERMARK_ROLLBACK",
                "INNER_RECONCILER_WATERMARK_BEHIND_DURABLE_FRONTIER",
            )
        if observed.horizon_floor < current.horizon_floor:
            return self._decision(
                "HORIZON_FLOOR_ROLLBACK",
                "INNER_RECONCILER_HORIZON_FLOOR_BEHIND_DURABLE_FRONTIER",
            )
        return self._decision(
            "ACCEPTED",
            "INNER_RECONCILER_IS_MONOTONIC_WITH_DURABLE_FRONTIER",
            accepted=True,
        )

    def adopt_inner(
        self,
        candidate: AnchoredRecoveryReconciler,
    ) -> FrontierDecision:
        decision = self.validate_inner(candidate)
        if not decision.accepted:
            return decision
        observed = self._observe(candidate)
        self._reconciler = candidate
        self._frontier = ReconciliationFrontier(
            world_session_id=self._frontier.world_session_id,
            world_cut_generation=observed.world_cut_generation,
            recovery_epoch=observed.recovery_epoch,
            outcome_watermark=observed.outcome_watermark,
            horizon_floor=observed.horizon_floor,
            observer_certainty=observed.observer_certainty,
        )
        return self._decision(
            "ACCEPTED",
            "INNER_RECONCILER_ADOPTED_WITHOUT_CAUSAL_ROLLBACK",
            accepted=True,
        )

    def refresh_from_inner(self) -> FrontierDecision:
        return self.adopt_inner(self._reconciler)

    def preflight_anchor(
        self,
        snapshot: WorldAnchorSnapshot,
    ) -> FrontierDecision:
        current = self._frontier
        if snapshot.world_session_id != current.world_session_id:
            return self._decision(
                "WRONG_WORLD_SESSION",
                "ANCHOR_WORLD_SESSION_MISMATCH",
            )
        if snapshot.world_cut_generation < current.world_cut_generation:
            return self._decision(
                "STALE_WORLD_CUT",
                "ANCHOR_WORLD_CUT_BEHIND_DURABLE_FRONTIER",
            )
        if snapshot.world_cut_generation > current.world_cut_generation:
            return self._decision(
                "FUTURE_WORLD_CUT",
                "ANCHOR_WORLD_CUT_AHEAD_OF_DURABLE_FRONTIER",
            )
        if snapshot.old_recovery_epoch < current.recovery_epoch:
            return self._decision(
                "STALE_RECOVERY_EPOCH",
                "ANCHOR_RECOVERY_EPOCH_RETIRED",
            )
        if snapshot.old_recovery_epoch > current.recovery_epoch:
            return self._decision(
                "FUTURE_RECOVERY_EPOCH",
                "ANCHOR_RECOVERY_EPOCH_NOT_YET_OPEN",
            )
        if snapshot.proposed_recovery_epoch != current.recovery_epoch + 1:
            return self._decision(
                "INVALID_RECOVERY_EPOCH_TRANSITION",
                "ANCHOR_MUST_ADVANCE_EXACTLY_ONE_RECOVERY_EPOCH",
            )
        if snapshot.covered_through_outcome_sequence < current.outcome_watermark:
            return self._decision(
                "STALE_ANCHOR_COVERAGE",
                "ANCHOR_DOES_NOT_COVER_DURABLE_FRONTIER_WATERMARK",
            )
        return self._decision(
            "ACCEPTED",
            "ANCHOR_IS_MONOTONIC_WITH_DURABLE_FRONTIER",
            accepted=True,
        )

    def reconcile_after_rebase(self) -> FrontierDecision:
        """Advance the outer frontier after a successful inner atomic rebase.

        A rebase may recreate the inner bounded horizon and therefore lower its
        local retention floor. The outer frontier deliberately preserves the
        prior durable floor while requiring cut/epoch/watermark monotonicity.
        """

        observed = self._observe(self._reconciler)
        prior = self._frontier
        if observed.world_cut_generation != prior.world_cut_generation + 1:
            return self._decision(
                "WORLD_CUT_ROLLBACK"
                if observed.world_cut_generation <= prior.world_cut_generation
                else "FUTURE_WORLD_CUT",
                "REBASE_DID_NOT_ADVANCE_EXACTLY_ONE_WORLD_CUT_GENERATION",
            )
        if observed.recovery_epoch != prior.recovery_epoch + 1:
            return self._decision(
                "RECOVERY_EPOCH_ROLLBACK"
                if observed.recovery_epoch <= prior.recovery_epoch
                else "FUTURE_RECOVERY_EPOCH",
                "REBASE_DID_NOT_ADVANCE_EXACTLY_ONE_RECOVERY_EPOCH",
            )
        if observed.outcome_watermark < prior.outcome_watermark:
            return self._decision(
                "OUTCOME_WATERMARK_ROLLBACK",
                "REBASE_MOVED_OUTCOME_WATERMARK_BACKWARD",
            )

        self._frontier = ReconciliationFrontier(
            world_session_id=prior.world_session_id,
            world_cut_generation=observed.world_cut_generation,
            recovery_epoch=observed.recovery_epoch,
            outcome_watermark=observed.outcome_watermark,
            horizon_floor=max(prior.horizon_floor, observed.horizon_floor),
            observer_certainty=observed.observer_certainty,
        )
        return self._decision(
            "ACCEPTED",
            "DURABLE_FRONTIER_ADVANCED_AFTER_ATOMIC_REBASE",
            accepted=True,
        )

    def admit_issue_stamp(self, stamp: IssueTimeStamp) -> FrontierDecision:
        current = self._frontier
        if stamp.world_session_id != current.world_session_id:
            return self._decision(
                "WRONG_WORLD_SESSION",
                "ISSUE_STAMP_WORLD_SESSION_MISMATCH",
            )
        if (
            stamp.world_cut_generation < current.world_cut_generation
            or stamp.recovery_epoch < current.recovery_epoch
        ):
            return self._decision(
                "RETIRED_ISSUE_LINEAGE",
                "ISSUE_STAMP_BELONGS_TO_RETIRED_CAUSAL_FRONTIER",
            )
        if (
            stamp.world_cut_generation > current.world_cut_generation
            or stamp.recovery_epoch > current.recovery_epoch
        ):
            return self._decision(
                "FUTURE_ISSUE_LINEAGE",
                "ISSUE_STAMP_BELONGS_TO_FUTURE_CAUSAL_FRONTIER",
            )
        return self._decision(
            "ACCEPTED",
            "ISSUE_STAMP_MATCHES_CURRENT_CAUSAL_FRONTIER",
            accepted=True,
        )

    def checkpoint(self) -> str:
        payload = {
            "schema_version": 1,
            "frontier": asdict(self._frontier),
        }
        payload["frontier_token"] = self._frontier.token()
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        if payload.get("schema_version") != 1:
            raise ValueError("invalid causal frontier checkpoint schema")
        raw = payload.get("frontier")
        token = payload.get("frontier_token")
        if not isinstance(raw, dict) or not isinstance(token, str):
            raise ValueError("invalid causal frontier checkpoint")
        frontier = ReconciliationFrontier(**raw)
        if frontier.token() != token:
            raise ValueError("causal frontier checkpoint token mismatch")
        if frontier.world_session_id != self._ledger.world_session_id:
            raise ValueError("WORLD session mismatch")

        observed = self._observe(self._reconciler)
        if observed.world_cut_generation < frontier.world_cut_generation:
            raise ValueError("inner world cut behind durable frontier")
        if observed.recovery_epoch < frontier.recovery_epoch:
            raise ValueError("inner recovery epoch behind durable frontier")
        if observed.outcome_watermark < frontier.outcome_watermark:
            raise ValueError("inner outcome watermark behind durable frontier")

        self._frontier = ReconciliationFrontier(
            world_session_id=frontier.world_session_id,
            world_cut_generation=max(
                frontier.world_cut_generation,
                observed.world_cut_generation,
            ),
            recovery_epoch=max(frontier.recovery_epoch, observed.recovery_epoch),
            outcome_watermark=max(
                frontier.outcome_watermark,
                observed.outcome_watermark,
            ),
            horizon_floor=max(frontier.horizon_floor, observed.horizon_floor),
            observer_certainty=observed.observer_certainty,
        )


def build_causal_frontier_report() -> dict[str, object]:
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "SESSION_SCOPED_DURABLE_CAUSAL_FRONTIER_ABOVE_INNER_HORIZON",
        "inner_recreation_can_reset_causal_time": False,
        "same_session_watermark_rollback_allowed": False,
        "old_issue_lineage_can_cross_rebase": False,
        "frontier_metadata_is_constant_size": True,
        "ordinary_reduction": (
            "state-machine monotonic frontier + WAL metadata row + fencing "
            "generation + explicit session namespace"
        ),
        "simplification_comparator": (
            "local SQLite/WAL single-writer frontier row with composite identities"
        ),
        "limitation": (
            "The guard protects ordering/lineage only; WORLD truth still depends "
            "on the independent validated anchor ledger."
        ),
        "claim_boundary": (
            "Engineering usefulness does not establish biological fidelity, fly "
            "topology superiority, efficiency, composition contribution, "
            "whole-system superiority, external validity, or scientific novelty."
        ),
        "scientific_credit": 0,
    }

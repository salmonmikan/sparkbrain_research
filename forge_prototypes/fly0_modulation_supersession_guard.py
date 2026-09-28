"""Forge-only guard against superseded high-level modulation intent.

The existing FLY-0 modulation frame is locally provenance-bound, but a high-level
state transition can happen without changing the local sensorimotor checkpoint.
This wrapper adds a separate high-level authority epoch/token so a frame minted
under an older high-level state fails closed after that state is superseded.

This is noncanonical, non-evidentiary engineering work. It does not expand the
modulation vocabulary or allocate SYSTEM_BUILD authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from forge_prototypes.fly0_descending_modulation import (
    BridgeStepResult,
    DescendingModulationBridge,
    ModulationFrame,
    Mode,
)
from forge_prototypes.fly0_hierarchical_loop import LoopSnapshot, Side, WorldState
from forge_prototypes.fly0_matched_replacement import Variant

_GUARD_SCHEMA = 1


@dataclass(frozen=True)
class GuardedModulationFrame:
    authority_epoch: int
    authority_token: str
    frame: ModulationFrame


@dataclass(frozen=True)
class GuardedStepResult:
    accepted: bool
    reason: str
    before: LoopSnapshot
    after: LoopSnapshot
    guarded_frame: GuardedModulationFrame
    bridge_result: BridgeStepResult | None


class ModulationSupersessionGuard:
    """Bind modulation frames to the current high-level authority state."""

    def __init__(
        self,
        initial_world: WorldState,
        *,
        variant: Variant,
        authority_token: str,
        mask_feedback: bool = False,
        feedback_delay_steps: int = 1,
        max_feedback_delay_steps: int = 1,
        event_budget: int = 4096,
    ) -> None:
        if not authority_token:
            raise ValueError("authority token must be non-empty")
        self._bridge = DescendingModulationBridge(
            initial_world,
            variant=variant,
            mask_feedback=mask_feedback,
            feedback_delay_steps=feedback_delay_steps,
            max_feedback_delay_steps=max_feedback_delay_steps,
            event_budget=event_budget,
        )
        self._authority_epoch = 0
        self._authority_token = authority_token

    @property
    def snapshot(self) -> LoopSnapshot:
        return self._bridge.snapshot

    @property
    def variant(self) -> Variant:
        return self._bridge.variant

    @property
    def authority_epoch(self) -> int:
        return self._authority_epoch

    @property
    def authority_token(self) -> str:
        return self._authority_token

    @property
    def bridge_sequence(self) -> int:
        return self._bridge.bridge_sequence

    def supersede(self, authority_token: str) -> None:
        """Advance high-level authority without mutating local sensorimotor state."""
        if not authority_token:
            raise ValueError("authority token must be non-empty")
        self._authority_epoch += 1
        self._authority_token = authority_token

    def make_frame(
        self,
        *,
        frame_sequence: int,
        mode: Mode = "neutral",
        target_side: Side | None = None,
        ttl_steps: int = 1,
    ) -> GuardedModulationFrame:
        return GuardedModulationFrame(
            authority_epoch=self._authority_epoch,
            authority_token=self._authority_token,
            frame=self._bridge.make_frame(
                frame_sequence=frame_sequence,
                mode=mode,
                target_side=target_side,
                ttl_steps=ttl_steps,
            ),
        )

    def step(
        self,
        guarded_frame: GuardedModulationFrame,
        *,
        descending_cut: bool = False,
    ) -> GuardedStepResult:
        before = self.snapshot
        if (
            guarded_frame.authority_epoch != self._authority_epoch
            or guarded_frame.authority_token != self._authority_token
        ):
            return GuardedStepResult(
                False,
                "SUPERSEDED_HIGH_LEVEL_AUTHORITY",
                before,
                before,
                guarded_frame,
                None,
            )

        bridge_result = self._bridge.step(
            guarded_frame.frame,
            descending_cut=descending_cut,
        )
        return GuardedStepResult(
            bridge_result.accepted,
            bridge_result.reason,
            before,
            self.snapshot,
            guarded_frame,
            bridge_result,
        )

    def checkpoint(self) -> str:
        payload = {
            "schema_version": _GUARD_SCHEMA,
            "authority_epoch": self._authority_epoch,
            "authority_token": self._authority_token,
            "bridge_checkpoint": self._bridge.checkpoint(),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        current_bridge = self._bridge.checkpoint()
        current_epoch = self._authority_epoch
        current_token = self._authority_token
        try:
            payload = json.loads(checkpoint)
            if payload.get("schema_version") != _GUARD_SCHEMA:
                raise ValueError("supersession guard checkpoint schema mismatch")
            epoch = payload.get("authority_epoch")
            token = payload.get("authority_token")
            if not isinstance(epoch, int) or epoch < 0:
                raise ValueError("authority epoch invalid")
            if not isinstance(token, str) or not token:
                raise ValueError("authority token invalid")

            self._bridge.restore(payload["bridge_checkpoint"])
            self._authority_epoch = epoch
            self._authority_token = token
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            self._bridge.restore(current_bridge)
            self._authority_epoch = current_epoch
            self._authority_token = current_token
            raise


_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)


def build_supersession_guard_report() -> dict[str, object]:
    rows: dict[str, object] = {}
    for variant in _VARIANTS:
        guard = ModulationSupersessionGuard(
            WorldState(position=2, target=-1),
            variant=variant,
            authority_token="intent-a",
        )
        old = guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
        local_before = guard.snapshot.token()
        bridge_sequence_before = guard.bridge_sequence

        guard.supersede("intent-b")
        stale = guard.step(old)
        stale_preserves_local = guard.snapshot.token() == local_before
        stale_preserves_bridge_sequence = (
            guard.bridge_sequence == bridge_sequence_before
        )

        fresh = guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
        fresh_result = guard.step(fresh)

        rows[variant] = {
            "superseded_frame_rejected": (
                not stale.accepted
                and stale.reason == "SUPERSEDED_HIGH_LEVEL_AUTHORITY"
            ),
            "superseded_frame_preserves_local": stale_preserves_local,
            "superseded_frame_preserves_bridge_sequence": (
                stale_preserves_bridge_sequence
            ),
            "fresh_authority_frame_commits": (
                fresh_result.accepted
                and fresh_result.bridge_result is not None
                and fresh_result.bridge_result.local_step_committed
                and guard.snapshot.world.position == 1
            ),
        }

    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "HIGH_LEVEL_INTENT_SUPERSESSION_GUARD",
        "modulation_vocabulary_expanded": False,
        "rows": rows,
        "all_variants_reject_superseded_authority": all(
            row["superseded_frame_rejected"]
            and row["superseded_frame_preserves_local"]
            and row["superseded_frame_preserves_bridge_sequence"]
            for row in rows.values()
        ),
        "all_variants_accept_fresh_authority": all(
            row["fresh_authority_frame_commits"] for row in rows.values()
        ),
        "claim_boundary": (
            "This is a Forge-only asynchronous handoff guard around the existing "
            "bounded modulation contract. It does not establish a richer goal "
            "policy, biological fidelity or equivalence, topology necessity or "
            "superiority, efficiency, composition contribution, whole-system "
            "superiority, external validity, scientific novelty, scientific "
            "credit, or SYSTEM_BUILD completion."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_supersession_guard_report(), indent=2, sort_keys=True))

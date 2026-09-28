"""Bounded descending-modulation contract for the noncanonical FLY-0 loop.

This bridge probes a narrow engineering boundary proposed by Theory R20:
high-level state may gate a local sensorimotor controller only through a
versioned, replayable frame. It is Forge-only, non-evidentiary work.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal

from forge_prototypes.fly0_composed_causal_replacement import (
    ComposedCausalReplacementLoop,
)
from forge_prototypes.fly0_hierarchical_loop import LoopSnapshot, Side, WorldState
from forge_prototypes.fly0_matched_replacement import Variant

Mode = Literal["neutral", "hold", "permit_side"]

_FRAME_SCHEMA = "fly0-modulation-frame-v2"
_BRIDGE_SCHEMA = 2
_MAX_TTL_STEPS = 4


def _contract() -> dict[str, object]:
    return {
        "version": _FRAME_SCHEMA,
        "fields": [
            "schema_version",
            "frame_sequence",
            "mode",
            "target_side",
            "issued_at_local_sequence",
            "ttl_steps",
            "source_checkpoint_token",
        ],
        "modes": ["neutral", "hold", "permit_side"],
        "max_ttl_steps": _MAX_TTL_STEPS,
        "semantics": {
            "neutral": "permit the ordinary local closed-loop step",
            "hold": "commit high-level hold without issuing a local action",
            "permit_side": (
                "permit ordinary local action only when the local task-facing "
                "desired side matches the declared high-level target side"
            ),
        },
        "forbidden": [
            "arbitrary_internal_controller_commands",
            "opaque_callback_control",
            "undeclared_fine_grained_local_control",
        ],
    }


def _fingerprint(value: dict[str, object]) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


@dataclass(frozen=True)
class ModulationFrame:
    schema_version: str
    frame_sequence: int
    mode: Mode
    target_side: Side | None
    issued_at_local_sequence: int
    ttl_steps: int
    source_checkpoint_token: str


@dataclass(frozen=True)
class BridgeStepResult:
    accepted: bool
    reason: str
    before: LoopSnapshot
    after: LoopSnapshot
    frame: ModulationFrame
    descending_cut: bool
    local_step_committed: bool


class DescendingModulationBridge:
    """Versioned high-level gate around one matched local replacement loop."""

    def __init__(
        self,
        initial_world: WorldState,
        *,
        variant: Variant,
        mask_feedback: bool = False,
        feedback_delay_steps: int = 1,
        max_feedback_delay_steps: int = 1,
        event_budget: int = 4096,
    ) -> None:
        self._variant = variant
        self._contract = _contract()
        self._contract_fingerprint = _fingerprint(self._contract)
        self._local = ComposedCausalReplacementLoop(
            initial_world,
            variant=variant,
            mask_feedback=mask_feedback,
            feedback_delay_steps=feedback_delay_steps,
            max_feedback_delay_steps=max_feedback_delay_steps,
            event_budget=event_budget,
        )
        self._bridge_sequence = 0
        self._last_frame_sequence: int | None = None
        self._last_frame: ModulationFrame | None = None

    @property
    def snapshot(self) -> LoopSnapshot:
        return self._local.snapshot

    @property
    def variant(self) -> Variant:
        return self._variant

    @property
    def bridge_sequence(self) -> int:
        return self._bridge_sequence

    @property
    def last_frame_sequence(self) -> int | None:
        return self._last_frame_sequence

    @property
    def modulation_contract(self) -> dict[str, object]:
        return json.loads(json.dumps(self._contract))

    @property
    def modulation_contract_fingerprint(self) -> str:
        return self._contract_fingerprint

    def make_frame(
        self,
        *,
        frame_sequence: int,
        mode: Mode = "neutral",
        target_side: Side | None = None,
        ttl_steps: int = 1,
    ) -> ModulationFrame:
        return ModulationFrame(
            schema_version=_FRAME_SCHEMA,
            frame_sequence=frame_sequence,
            mode=mode,
            target_side=target_side,
            issued_at_local_sequence=self.snapshot.sequence,
            ttl_steps=ttl_steps,
            source_checkpoint_token=self.snapshot.token(),
        )

    def _validate_frame(self, frame: ModulationFrame) -> None:
        if frame.schema_version != _FRAME_SCHEMA:
            raise ValueError("modulation-frame schema mismatch")
        if frame.frame_sequence < 0:
            raise ValueError("frame sequence must be non-negative")
        if (
            self._last_frame_sequence is not None
            and frame.frame_sequence <= self._last_frame_sequence
        ):
            raise ValueError("stale modulation frame sequence")
        if frame.mode not in {"neutral", "hold", "permit_side"}:
            raise ValueError("unsupported modulation mode")
        if frame.mode == "permit_side":
            if frame.target_side not in {"left", "right"}:
                raise ValueError("permit_side requires a declared target side")
        elif frame.target_side is not None:
            raise ValueError("target side is only valid for permit_side")
        if not 1 <= frame.ttl_steps <= _MAX_TTL_STEPS:
            raise ValueError("modulation frame TTL outside bounded contract")
        if frame.issued_at_local_sequence > self.snapshot.sequence:
            raise ValueError("modulation frame issued from future local sequence")
        if self.snapshot.sequence >= frame.issued_at_local_sequence + frame.ttl_steps:
            raise ValueError("expired modulation frame")
        if frame.source_checkpoint_token != self.snapshot.token():
            raise ValueError("modulation frame provenance token mismatch")

    def _commit_frame(self, frame: ModulationFrame) -> None:
        self._bridge_sequence += 1
        self._last_frame_sequence = frame.frame_sequence
        self._last_frame = frame

    def step(
        self,
        frame: ModulationFrame,
        *,
        descending_cut: bool = False,
    ) -> BridgeStepResult:
        before = self.snapshot
        try:
            self._validate_frame(frame)
        except ValueError as exc:
            return BridgeStepResult(
                False,
                str(exc),
                before,
                before,
                frame,
                descending_cut,
                False,
            )

        if not descending_cut:
            if frame.mode == "hold":
                self._commit_frame(frame)
                return BridgeStepResult(
                    True,
                    "HIGH_LEVEL_HOLD_COMMITTED",
                    before,
                    before,
                    frame,
                    False,
                    False,
                )
            if frame.mode == "permit_side":
                error = before.world.target - before.world.position
                local_side: Side | None
                if error < 0:
                    local_side = "left"
                elif error > 0:
                    local_side = "right"
                else:
                    local_side = None
                if local_side is not None and local_side != frame.target_side:
                    self._commit_frame(frame)
                    return BridgeStepResult(
                        True,
                        "HIGH_LEVEL_SIDE_VETO_COMMITTED",
                        before,
                        before,
                        frame,
                        False,
                        False,
                    )

        local = self._local.step()
        if not local.accepted:
            return BridgeStepResult(
                False,
                local.reason,
                before,
                before,
                frame,
                descending_cut,
                False,
            )

        self._commit_frame(frame)
        if descending_cut:
            reason = "DESCENDING_CUT_LOCAL_BASELINE"
        elif frame.mode == "permit_side":
            reason = "HIGH_LEVEL_SIDE_MATCH_LOCAL_STEP_COMMITTED"
        else:
            reason = "NEUTRAL_LOCAL_STEP_COMMITTED"
        return BridgeStepResult(
            True,
            reason,
            before,
            self.snapshot,
            frame,
            descending_cut,
            True,
        )

    def checkpoint(self) -> str:
        payload = {
            "schema_version": _BRIDGE_SCHEMA,
            "variant": self._variant,
            "modulation_contract": self._contract,
            "modulation_contract_fingerprint": self._contract_fingerprint,
            "bridge_sequence": self._bridge_sequence,
            "last_frame_sequence": self._last_frame_sequence,
            "last_frame": (
                asdict(self._last_frame) if self._last_frame is not None else None
            ),
            "local_checkpoint": self._local.checkpoint(),
            "local_token": self.snapshot.token(),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        current_local = self._local.checkpoint()
        current_bridge_sequence = self._bridge_sequence
        current_last_sequence = self._last_frame_sequence
        current_last_frame = self._last_frame
        try:
            payload = json.loads(checkpoint)
            if payload.get("schema_version") != _BRIDGE_SCHEMA:
                raise ValueError("bridge checkpoint schema mismatch")
            if payload.get("variant") != self._variant:
                raise ValueError("bridge replacement variant mismatch")
            if payload.get("modulation_contract") != self._contract:
                raise ValueError("modulation contract mismatch")
            if (
                payload.get("modulation_contract_fingerprint")
                != self._contract_fingerprint
            ):
                raise ValueError("modulation contract fingerprint mismatch")
            bridge_sequence = payload.get("bridge_sequence")
            if not isinstance(bridge_sequence, int) or bridge_sequence < 0:
                raise ValueError("bridge sequence invalid")
            last_sequence = payload.get("last_frame_sequence")
            if last_sequence is not None and (
                not isinstance(last_sequence, int) or last_sequence < 0
            ):
                raise ValueError("last frame sequence invalid")
            raw_frame = payload.get("last_frame")
            last_frame = (
                ModulationFrame(**raw_frame) if raw_frame is not None else None
            )
            if (last_frame is None) != (last_sequence is None):
                raise ValueError("last frame checkpoint mismatch")
            if (
                last_frame is not None
                and last_frame.frame_sequence != last_sequence
            ):
                raise ValueError("last frame sequence mismatch")

            self._local.restore(payload["local_checkpoint"])
            if self.snapshot.token() != payload.get("local_token"):
                raise ValueError("cross-layer local token mismatch")

            self._bridge_sequence = bridge_sequence
            self._last_frame_sequence = last_sequence
            self._last_frame = last_frame
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            self._local.restore(current_local)
            self._bridge_sequence = current_bridge_sequence
            self._last_frame_sequence = current_last_sequence
            self._last_frame = current_last_frame
            raise


_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)


def _three_neutral_steps(variant: Variant) -> tuple[int, ...]:
    bridge = DescendingModulationBridge(
        WorldState(position=2, target=-1),
        variant=variant,
    )
    trace = [bridge.snapshot.world.position]
    for sequence in range(3):
        result = bridge.step(
            bridge.make_frame(
                frame_sequence=sequence,
                mode="neutral",
            )
        )
        if not result.accepted:
            break
        trace.append(bridge.snapshot.world.position)
    return tuple(trace)


def build_descending_modulation_report() -> dict[str, object]:
    rows: dict[str, object] = {}
    for variant in _VARIANTS:
        neutral_trace = _three_neutral_steps(variant)

        hold = DescendingModulationBridge(
            WorldState(position=2, target=-1),
            variant=variant,
        )
        hold_result = hold.step(
            hold.make_frame(frame_sequence=0, mode="hold")
        )

        match = DescendingModulationBridge(
            WorldState(position=2, target=-1),
            variant=variant,
        )
        match_result = match.step(
            match.make_frame(
                frame_sequence=0,
                mode="permit_side",
                target_side="left",
            )
        )

        veto = DescendingModulationBridge(
            WorldState(position=2, target=-1),
            variant=variant,
        )
        veto_result = veto.step(
            veto.make_frame(
                frame_sequence=0,
                mode="permit_side",
                target_side="right",
            )
        )

        cut = DescendingModulationBridge(
            WorldState(position=2, target=-1),
            variant=variant,
        )
        cut_result = cut.step(
            cut.make_frame(
                frame_sequence=0,
                mode="permit_side",
                target_side="right",
            ),
            descending_cut=True,
        )

        feedback_cut = DescendingModulationBridge(
            WorldState(position=2, target=-1),
            variant=variant,
            mask_feedback=True,
        )
        first = feedback_cut.step(
            feedback_cut.make_frame(frame_sequence=0, mode="neutral")
        )
        second = feedback_cut.step(
            feedback_cut.make_frame(frame_sequence=1, mode="neutral")
        )

        rows[variant] = {
            "neutral_trace": neutral_trace,
            "neutral_reaches_target": neutral_trace == (2, 1, 0, -1),
            "hold_commits_without_local_action": (
                hold_result.accepted
                and not hold_result.local_step_committed
                and hold.snapshot.world.position == 2
            ),
            "matching_side_permits_local_action": (
                match_result.accepted
                and match_result.local_step_committed
                and match.snapshot.world.position == 1
            ),
            "mismatched_side_vetoes_local_action": (
                veto_result.accepted
                and not veto_result.local_step_committed
                and veto.snapshot.world.position == 2
            ),
            "descending_cut_restores_local_baseline": (
                cut_result.accepted
                and cut_result.local_step_committed
                and cut.snapshot.world.position == 1
            ),
            "local_feedback_cut_blocks_dependent_continuation": (
                first.accepted
                and not second.accepted
                and second.reason
                == "ascending feedback insufficient for modulation"
            ),
        }

    reference = DescendingModulationBridge(
        WorldState(position=0, target=0),
        variant="structured",
    )
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "DESCENDING_DIRECTIONAL_MODULATION_AUTHORITY_CONTRACT",
        "modulation_contract": reference.modulation_contract,
        "modulation_contract_fingerprint": (
            reference.modulation_contract_fingerprint
        ),
        "rows": rows,
        "all_variants_same_interface": len(rows) == len(_VARIANTS),
        "all_neutral_baselines_green": all(
            row["neutral_reaches_target"] for row in rows.values()
        ),
        "all_hold_gates_green": all(
            row["hold_commits_without_local_action"] for row in rows.values()
        ),
        "all_directional_gates_green": all(
            row["matching_side_permits_local_action"]
            and row["mismatched_side_vetoes_local_action"]
            for row in rows.values()
        ),
        "all_descending_cuts_green": all(
            row["descending_cut_restores_local_baseline"]
            for row in rows.values()
        ),
        "all_local_feedback_cuts_green": all(
            row["local_feedback_cut_blocks_dependent_continuation"]
            for row in rows.values()
        ),
        "claim_boundary": (
            "This is a bounded Forge engineering contract probe. The coarse "
            "directional permission gate is not a rich goal policy and does "
            "not establish biological fidelity or equivalence, topology "
            "necessity or superiority, compute or energy efficiency, "
            "composition contribution, whole-system superiority, external "
            "validity, scientific novelty, scientific credit, or SB003 "
            "allocation."
        ),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            build_descending_modulation_report(),
            indent=2,
            sort_keys=True,
        )
    )

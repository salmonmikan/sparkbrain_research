"""Forge-only ascending observed-state summary for the bounded FLY-0 loop.

This adapter exposes what actually happened after a guarded local sensorimotor
step without adding a new control channel.  It is intended to keep high-level
state informed by observed world/local outcomes rather than by issued
modulation intent alone.

This is noncanonical, non-evidentiary engineering work.  It does not allocate
SYSTEM_BUILD authority or establish a biological model.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from forge_prototypes.fly0_hierarchical_loop import WorldState
from forge_prototypes.fly0_matched_replacement import Variant
from forge_prototypes.fly0_modulation_supersession_guard import (
    GuardedModulationFrame,
    GuardedStepResult,
    ModulationSupersessionGuard,
)


@dataclass(frozen=True)
class ObservedStateSummary:
    accepted: bool
    reason: str
    authority_epoch: int
    authority_token: str
    local_sequence_before: int
    local_sequence_after: int
    bridge_sequence_before: int
    bridge_sequence_after: int
    world_position_before: int
    world_position_after: int
    world_target: int
    position_delta: int
    remaining_signed_error: int
    local_step_committed: bool
    feedback_fired_events: int
    feedback_matched_motor_events: int
    feedback_opposite_motor_events: int

    def token(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class ObservedStepResult:
    guarded_result: GuardedStepResult
    observed: ObservedStateSummary


class AscendingObservedStateBridge:
    """Expose post-step observed state independently from issued intent."""

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
        self._guard = ModulationSupersessionGuard(
            initial_world,
            variant=variant,
            authority_token=authority_token,
            mask_feedback=mask_feedback,
            feedback_delay_steps=feedback_delay_steps,
            max_feedback_delay_steps=max_feedback_delay_steps,
            event_budget=event_budget,
        )

    @property
    def guard(self) -> ModulationSupersessionGuard:
        return self._guard

    @property
    def snapshot(self):
        return self._guard.snapshot

    def checkpoint(self) -> str:
        return self._guard.checkpoint()

    def restore(self, checkpoint: str) -> None:
        self._guard.restore(checkpoint)

    def step(
        self,
        guarded_frame: GuardedModulationFrame,
        *,
        descending_cut: bool = False,
    ) -> ObservedStepResult:
        bridge_sequence_before = self._guard.bridge_sequence
        result = self._guard.step(
            guarded_frame,
            descending_cut=descending_cut,
        )
        bridge_sequence_after = self._guard.bridge_sequence

        local_step_committed = bool(
            result.bridge_result is not None
            and result.bridge_result.local_step_committed
        )
        feedback = result.after.feedback if local_step_committed else ()
        observed = ObservedStateSummary(
            accepted=result.accepted,
            reason=result.reason,
            authority_epoch=self._guard.authority_epoch,
            authority_token=self._guard.authority_token,
            local_sequence_before=result.before.sequence,
            local_sequence_after=result.after.sequence,
            bridge_sequence_before=bridge_sequence_before,
            bridge_sequence_after=bridge_sequence_after,
            world_position_before=result.before.world.position,
            world_position_after=result.after.world.position,
            world_target=result.after.world.target,
            position_delta=(
                result.after.world.position - result.before.world.position
            ),
            remaining_signed_error=(
                result.after.world.target - result.after.world.position
            ),
            local_step_committed=local_step_committed,
            feedback_fired_events=sum(item.fired_events for item in feedback),
            feedback_matched_motor_events=sum(
                item.matched_motor_events for item in feedback
            ),
            feedback_opposite_motor_events=sum(
                item.opposite_motor_events for item in feedback
            ),
        )
        return ObservedStepResult(result, observed)


_VARIANTS: tuple[Variant, ...] = (
    "structured",
    "rewired",
    "random_sparse",
    "reactive",
)


def build_observed_state_report() -> dict[str, object]:
    rows: dict[str, object] = {}
    for variant in _VARIANTS:
        bridge = AscendingObservedStateBridge(
            WorldState(position=2, target=-1),
            variant=variant,
            authority_token="intent-a",
        )
        fresh = bridge.guard.make_frame(
            frame_sequence=0,
            mode="permit_side",
            target_side="left",
        )
        accepted = bridge.step(fresh)

        old = bridge.guard.make_frame(
            frame_sequence=1,
            mode="permit_side",
            target_side="left",
        )
        before_stale = bridge.snapshot.token()
        bridge_before_stale = bridge.guard.bridge_sequence
        bridge.guard.supersede("intent-b")
        stale = bridge.step(old)

        rows[variant] = {
            "fresh_observed_world_delta": accepted.observed.position_delta,
            "fresh_observed_error": accepted.observed.remaining_signed_error,
            "fresh_local_step_committed": accepted.observed.local_step_committed,
            "fresh_feedback_visible": (
                accepted.observed.feedback_fired_events > 0
                or variant == "reactive"
            ),
            "stale_rejected": (
                not stale.observed.accepted
                and stale.observed.reason == "SUPERSEDED_HIGH_LEVEL_AUTHORITY"
            ),
            "stale_observation_no_local_advance": (
                bridge.snapshot.token() == before_stale
                and stale.observed.local_sequence_before
                == stale.observed.local_sequence_after
                and stale.observed.position_delta == 0
            ),
            "stale_observation_no_bridge_advance": (
                bridge.guard.bridge_sequence == bridge_before_stale
                and stale.observed.bridge_sequence_before
                == stale.observed.bridge_sequence_after
            ),
            "stale_observation_has_no_new_feedback": (
                stale.observed.feedback_fired_events == 0
                and stale.observed.feedback_matched_motor_events == 0
                and stale.observed.feedback_opposite_motor_events == 0
            ),
        }

    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "design": "ASCENDING_OBSERVED_STATE_SUMMARY",
        "control_surface_expanded": False,
        "modulation_vocabulary_expanded": False,
        "rows": rows,
        "all_variants_report_committed_outcome": all(
            row["fresh_local_step_committed"]
            and row["fresh_observed_world_delta"] == -1
            and row["fresh_observed_error"] == -2
            for row in rows.values()
        ),
        "all_variants_reject_stale_without_false_observation": all(
            row["stale_rejected"]
            and row["stale_observation_no_local_advance"]
            and row["stale_observation_no_bridge_advance"]
            and row["stale_observation_has_no_new_feedback"]
            for row in rows.values()
        ),
        "claim_boundary": (
            "This is an observation/provenance adapter around the existing FLY-0 "
            "guarded loop. It does not establish biological fidelity or equivalence, "
            "topology necessity or superiority, compute or energy efficiency, "
            "composition contribution, whole-system superiority, external validity, "
            "scientific novelty, scientific credit, or SYSTEM_BUILD completion."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_observed_state_report(), indent=2, sort_keys=True))

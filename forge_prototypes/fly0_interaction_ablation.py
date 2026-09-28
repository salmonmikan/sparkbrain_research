"""Interaction-ablation diagnostic for the noncanonical FLY-0 loop.

This module asks which interface edges are actually causal for bounded world
progress in the current prototype. It is engineering diagnostics only: no
scientific evaluator, biological model, or SYSTEM_BUILD allocation is created.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Literal

from forge_prototypes.fly0_hierarchical_loop import (
    ActionProposal,
    Fly0LocalController,
    HierarchicalSensorimotorLoop,
    LocalController,
    LocalFeedback,
    Modulation,
    Observation,
    Side,
    WorldState,
    run_to_target,
)
from forge_prototypes.fly0_topology_probe import build_structured_topology

Ablation = Literal[
    "intact",
    "local_observation_payload_cut",
    "ascending_feedback_payload_cut",
    "descending_modulation_cut",
    "local_action_cut",
]


@dataclass(frozen=True)
class ControllerAdapter:
    """Apply one bounded interface ablation without changing the base controller."""

    inner: LocalController
    mode: Ablation

    @property
    def module_id(self) -> str:
        return self.inner.module_id

    @property
    def side(self) -> Side:
        return self.inner.side

    def propose(
        self, observation: Observation, modulation: Modulation
    ) -> ActionProposal:
        if self.mode == "local_observation_payload_cut":
            observation = Observation(
                signed_error=0,
                sequence=observation.sequence,
            )
        if self.mode == "descending_modulation_cut":
            modulation = Modulation(desired_side=None)

        proposal = self.inner.propose(observation, modulation)

        if self.mode == "ascending_feedback_payload_cut":
            proposal = ActionProposal(
                module_id=proposal.module_id,
                action=proposal.action,
                active=proposal.active,
                feedback=LocalFeedback(
                    module_id=proposal.feedback.module_id,
                    side=proposal.feedback.side,
                    fired_events=0,
                    matched_motor_events=0,
                    opposite_motor_events=0,
                    first_matched_motor_time=None,
                ),
            )
        if self.mode == "local_action_cut":
            proposal = ActionProposal(
                module_id=proposal.module_id,
                action=0,
                active=proposal.active,
                feedback=proposal.feedback,
            )
        return proposal


@dataclass(frozen=True)
class AblationRow:
    condition: Ablation
    accepted_steps: int
    rejected_steps: int
    final_position: int
    reached_target: bool
    position_trace: tuple[int, ...]
    feedback_payload_present: bool
    first_rejection_reason: str | None


@dataclass(frozen=True)
class InteractionAblationReport:
    status: str
    initial_world: WorldState
    rows: tuple[AblationRow, ...]
    local_observation_payload_causal_for_bounded_trajectory: bool
    ascending_feedback_payload_causal_for_bounded_trajectory: bool
    descending_modulation_required_for_bounded_progress: bool
    local_action_required_for_bounded_progress: bool
    reason_codes: tuple[str, ...]
    claim_boundary: str

    def summary(self) -> dict[str, object]:
        return {
            "status": self.status,
            "initial_world": asdict(self.initial_world),
            "rows": {row.condition: asdict(row) for row in self.rows},
            "causal_matrix": {
                "local_observation_payload_causal_for_bounded_trajectory": (
                    self.local_observation_payload_causal_for_bounded_trajectory
                ),
                "ascending_feedback_payload_causal_for_bounded_trajectory": (
                    self.ascending_feedback_payload_causal_for_bounded_trajectory
                ),
                "descending_modulation_required_for_bounded_progress": (
                    self.descending_modulation_required_for_bounded_progress
                ),
                "local_action_required_for_bounded_progress": (
                    self.local_action_required_for_bounded_progress
                ),
                "reason_codes": list(self.reason_codes),
            },
            "claim_boundary": self.claim_boundary,
        }


def _build_loop(
    condition: Ablation,
    initial_world: WorldState,
) -> HierarchicalSensorimotorLoop:
    topology = build_structured_topology()
    base = (
        Fly0LocalController("fly0-left", "left", topology),
        Fly0LocalController("fly0-right", "right", topology),
    )
    return HierarchicalSensorimotorLoop(
        initial_world=initial_world,
        controllers=tuple(
            ControllerAdapter(controller, condition) for controller in base
        ),
    )


def _run_condition(
    condition: Ablation,
    initial_world: WorldState,
) -> AblationRow:
    loop = _build_loop(condition, initial_world)
    results = run_to_target(loop, max_steps=4)
    feedback = tuple(
        proposal.feedback
        for result in results
        for proposal in result.proposals
    )
    feedback_payload_present = any(
        item.fired_events
        or item.matched_motor_events
        or item.opposite_motor_events
        or item.first_matched_motor_time is not None
        for item in feedback
    )
    rejected = tuple(result for result in results if not result.accepted)
    return AblationRow(
        condition=condition,
        accepted_steps=sum(result.accepted for result in results),
        rejected_steps=len(rejected),
        final_position=loop.snapshot.world.position,
        reached_target=loop.snapshot.world.position == loop.snapshot.world.target,
        position_trace=(
            initial_world.position,
            *(result.after.world.position for result in results),
        ),
        feedback_payload_present=feedback_payload_present,
        first_rejection_reason=(rejected[0].reason if rejected else None),
    )


def build_interaction_ablation_report() -> InteractionAblationReport:
    initial_world = WorldState(position=2, target=-1)
    conditions: tuple[Ablation, ...] = (
        "intact",
        "local_observation_payload_cut",
        "ascending_feedback_payload_cut",
        "descending_modulation_cut",
        "local_action_cut",
    )
    rows = tuple(_run_condition(condition, initial_world) for condition in conditions)
    by_condition = {row.condition: row for row in rows}
    intact = by_condition["intact"]
    observation_cut = by_condition["local_observation_payload_cut"]
    feedback_cut = by_condition["ascending_feedback_payload_cut"]
    modulation_cut = by_condition["descending_modulation_cut"]
    action_cut = by_condition["local_action_cut"]

    observation_causal = (
        observation_cut.position_trace != intact.position_trace
        or observation_cut.reached_target != intact.reached_target
    )
    feedback_causal = (
        feedback_cut.position_trace != intact.position_trace
        or feedback_cut.reached_target != intact.reached_target
    )
    modulation_required = (
        not modulation_cut.reached_target
        and modulation_cut.final_position == initial_world.position
    )
    action_required = (
        not action_cut.reached_target
        and action_cut.final_position == initial_world.position
    )

    reasons: list[str] = []
    if not observation_causal:
        reasons.append("LOCAL_OBSERVATION_PAYLOAD_NOT_CAUSALLY_CONSUMED")
    if not feedback_causal:
        reasons.append("ASCENDING_FEEDBACK_PAYLOAD_NOT_CAUSALLY_CONSUMED")
    if modulation_required:
        reasons.append("DESCENDING_MODULATION_REQUIRED_FOR_PROGRESS")
    if action_required:
        reasons.append("LOCAL_ACTION_REQUIRED_FOR_PROGRESS")

    return InteractionAblationReport(
        status="NON_EVIDENTIARY_NONCANONICAL_FORGE",
        initial_world=initial_world,
        rows=rows,
        local_observation_payload_causal_for_bounded_trajectory=observation_causal,
        ascending_feedback_payload_causal_for_bounded_trajectory=feedback_causal,
        descending_modulation_required_for_bounded_progress=modulation_required,
        local_action_required_for_bounded_progress=action_required,
        reason_codes=tuple(reasons),
        claim_boundary=(
            "This matrix localizes causal use of the current bounded interface only. "
            "It does not establish topology superiority, biological fidelity, "
            "composition contribution, external validity, energy efficiency, "
            "scientific novelty, or SYSTEM_BUILD admission."
        ),
    )


if __name__ == "__main__":
    print(
        json.dumps(
            build_interaction_ablation_report().summary(),
            indent=2,
            sort_keys=True,
        )
    )

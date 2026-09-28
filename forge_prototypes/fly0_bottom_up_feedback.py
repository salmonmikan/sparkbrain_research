"""NON_EVIDENTIARY/NONCANONICAL FLY-0 bottom-up interface prototype."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Literal

from forge_prototypes.fly0_hierarchical_loop import (
    ActionProposal,
    Fly0LocalController,
    LocalFeedback,
    LoopSnapshot,
    Modulation,
    Observation,
    Side,
    StepResult,
    WorldState,
)
from forge_prototypes.fly0_topology_probe import build_structured_topology

Ablation = Literal[
    "intact",
    "local_observation_payload_cut",
    "ascending_feedback_payload_cut",
]


def _side(error: int) -> Side | None:
    return "left" if error < 0 else "right" if error > 0 else None


def _zero(module_id: str, side: Side) -> LocalFeedback:
    return LocalFeedback(module_id, side, 0, 0, 0, None)


@dataclass(frozen=True)
class ObservationAwareController:
    inner: Fly0LocalController
    mask_observation: bool = False

    @property
    def module_id(self) -> str:
        return self.inner.module_id

    @property
    def side(self) -> Side:
        return self.inner.side

    def propose(self, observation: Observation, modulation: Modulation) -> ActionProposal:
        seen = Observation(0, observation.sequence) if self.mask_observation else observation
        if modulation.desired_side == self.side and _side(seen.signed_error) != self.side:
            return ActionProposal(self.module_id, 0, False, _zero(self.module_id, self.side))
        return self.inner.propose(seen, modulation)


class FeedbackIntegratedLoop:
    def __init__(
        self,
        initial_world: WorldState,
        *,
        mask_observation: bool = False,
        mask_feedback: bool = False,
        event_budget: int = 4096,
    ) -> None:
        if event_budget < 1:
            raise ValueError("event_budget must be positive")
        topology = build_structured_topology()
        self._controllers = (
            ObservationAwareController(
                Fly0LocalController("fly0-left", "left", topology), mask_observation
            ),
            ObservationAwareController(
                Fly0LocalController("fly0-right", "right", topology), mask_observation
            ),
        )
        self._mask_observation = mask_observation
        self._mask_feedback = mask_feedback
        self._event_budget = event_budget
        self._snapshot = LoopSnapshot(initial_world, 0)

    @property
    def snapshot(self) -> LoopSnapshot:
        return self._snapshot

    def checkpoint(self) -> str:
        data = {
            "schema_version": 1,
            "module_ids": [c.module_id for c in self._controllers],
            "mask_observation": self._mask_observation,
            "mask_feedback": self._mask_feedback,
            "snapshot": asdict(self._snapshot),
            "token": self._snapshot.token(),
        }
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        data = json.loads(checkpoint)
        if data.get("schema_version") != 1:
            raise ValueError("checkpoint schema mismatch")
        if data.get("module_ids") != [c.module_id for c in self._controllers]:
            raise ValueError("checkpoint controller contract mismatch")
        if data.get("mask_observation") != self._mask_observation:
            raise ValueError("checkpoint observation-mask contract mismatch")
        if data.get("mask_feedback") != self._mask_feedback:
            raise ValueError("checkpoint feedback-mask contract mismatch")
        raw = data["snapshot"]
        restored = LoopSnapshot(
            world=WorldState(**raw["world"]),
            sequence=raw["sequence"],
            feedback=tuple(LocalFeedback(**item) for item in raw["feedback"]),
        )
        if restored.token() != data.get("token"):
            raise ValueError("checkpoint token mismatch")
        self._snapshot = restored

    def _feedback_allows(self, desired: Side) -> bool:
        if self._snapshot.sequence == 0:
            return True
        match = [f for f in self._snapshot.feedback if f.side == desired]
        return (
            len(match) == 1
            and match[0].matched_motor_events > 0
            and match[0].matched_motor_events > match[0].opposite_motor_events
        )

    def step(self) -> StepResult:
        before = self._snapshot
        error = before.world.target - before.world.position
        desired = _side(error)
        if desired is not None and not self._feedback_allows(desired):
            return StepResult(
                False,
                "ascending feedback insufficient for modulation",
                before,
                before,
                Modulation(None),
                (),
            )

        modulation = Modulation(desired)
        observation = Observation(error, before.sequence)
        try:
            proposals = tuple(c.propose(observation, modulation) for c in self._controllers)
            if any(p.feedback.fired_events > self._event_budget for p in proposals):
                raise RuntimeError("local event budget exceeded")
            active = tuple(p for p in proposals if p.active)
            if desired is None:
                if active:
                    raise RuntimeError("local module acted without modulation")
                action = 0
            elif len(active) != 1:
                raise RuntimeError("action arbitration requires one active module")
            else:
                action = active[0].action

            world = WorldState(
                max(-4, min(4, before.world.position + action)),
                before.world.target,
                before.world.step + 1,
            )
            feedback = tuple(p.feedback for p in proposals)
            if self._mask_feedback:
                feedback = tuple(_zero(f.module_id, f.side) for f in feedback)
            after = LoopSnapshot(world, before.sequence + 1, feedback)
            self._snapshot = after
            return StepResult(True, "COMMITTED", before, after, modulation, proposals)
        except (RuntimeError, ValueError) as exc:
            return StepResult(
                False,
                str(exc),
                before,
                before,
                modulation,
                locals().get("proposals", ()),
            )


def build_loop(
    initial_world: WorldState, *, ablation: Ablation = "intact"
) -> FeedbackIntegratedLoop:
    return FeedbackIntegratedLoop(
        initial_world,
        mask_observation=ablation == "local_observation_payload_cut",
        mask_feedback=ablation == "ascending_feedback_payload_cut",
    )


def run_to_target(loop: FeedbackIntegratedLoop, *, max_steps: int = 8) -> tuple[StepResult, ...]:
    results: list[StepResult] = []
    for _ in range(max_steps):
        if loop.snapshot.world.position == loop.snapshot.world.target:
            break
        result = loop.step()
        results.append(result)
        if not result.accepted:
            break
    return tuple(results)


@dataclass(frozen=True)
class Row:
    condition: Ablation
    accepted_steps: int
    rejected_steps: int
    final_position: int
    reached_target: bool
    position_trace: tuple[int, ...]
    first_rejection_reason: str | None


def _row(condition: Ablation) -> Row:
    initial = WorldState(position=2, target=-1)
    loop = build_loop(initial, ablation=condition)
    results = run_to_target(loop, max_steps=4)
    rejected = [r for r in results if not r.accepted]
    return Row(
        condition,
        sum(r.accepted for r in results),
        len(rejected),
        loop.snapshot.world.position,
        loop.snapshot.world.position == loop.snapshot.world.target,
        (initial.position, *(r.after.world.position for r in results)),
        rejected[0].reason if rejected else None,
    )


def probe_summary() -> dict[str, object]:
    rows = tuple(
        _row(c)
        for c in (
            "intact",
            "local_observation_payload_cut",
            "ascending_feedback_payload_cut",
        )
    )
    by = {r.condition: r for r in rows}
    intact = by["intact"]
    observation_cut = by["local_observation_payload_cut"]
    feedback_cut = by["ascending_feedback_payload_cut"]
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "rows": {r.condition: asdict(r) for r in rows},
        "causal_matrix": {
            "local_observation_payload_causal_for_bounded_trajectory":
                observation_cut.position_trace != intact.position_trace,
            "ascending_feedback_payload_causal_for_bounded_trajectory":
                feedback_cut.position_trace != intact.position_trace,
        },
        "ordinary_reduction":
            "Reactive control remains sufficient for the bounded movement task.",
        "claim_boundary": (
            "No topology superiority, biological fidelity, novelty, scientific credit "
            "or SB003 allocation."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(probe_summary(), indent=2, sort_keys=True))

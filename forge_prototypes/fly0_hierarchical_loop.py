"""Bounded, noncanonical hierarchical sensorimotor loop prototype.

This module tests interfaces and transaction boundaries only.  It is not a
biological model, a scientific evaluator, or a SYSTEM_BUILD allocation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Literal, Protocol

from forge_prototypes.fly0_topology_probe import (
    Topology,
    build_structured_topology,
    run_scenario,
)

Side = Literal["left", "right"]


@dataclass(frozen=True)
class WorldState:
    position: int
    target: int
    step: int = 0

    def __post_init__(self) -> None:
        if not -4 <= self.position <= 4:
            raise ValueError("position must be in [-4, 4]")
        if not -4 <= self.target <= 4:
            raise ValueError("target must be in [-4, 4]")
        if not 0 <= self.step <= 32:
            raise ValueError("step must be in [0, 32]")


@dataclass(frozen=True)
class Observation:
    signed_error: int
    sequence: int


@dataclass(frozen=True)
class Modulation:
    desired_side: Side | None


@dataclass(frozen=True)
class LocalFeedback:
    module_id: str
    side: Side
    fired_events: int
    matched_motor_events: int
    opposite_motor_events: int
    first_matched_motor_time: int | None


@dataclass(frozen=True)
class ActionProposal:
    module_id: str
    action: int
    active: bool
    feedback: LocalFeedback

    def __post_init__(self) -> None:
        if self.action not in {-1, 0, 1}:
            raise ValueError("action must be -1, 0 or 1")
        if not self.active and self.action != 0:
            raise ValueError("inactive proposal must abstain")


class LocalController(Protocol):
    module_id: str
    side: Side

    def propose(
        self, observation: Observation, modulation: Modulation
    ) -> ActionProposal: ...


@dataclass(frozen=True)
class Fly0LocalController:
    module_id: str
    side: Side
    topology: Topology

    def propose(
        self, observation: Observation, modulation: Modulation
    ) -> ActionProposal:
        del observation
        if modulation.desired_side != self.side:
            return ActionProposal(
                module_id=self.module_id,
                action=0,
                active=False,
                feedback=LocalFeedback(
                    module_id=self.module_id,
                    side=self.side,
                    fired_events=0,
                    matched_motor_events=0,
                    opposite_motor_events=0,
                    first_matched_motor_time=None,
                ),
            )
        result = run_scenario(self.topology, side=self.side)
        directional = (
            result.matched_motor_events > result.opposite_motor_events
            and result.matched_motor_events > 0
        )
        action = (-1 if self.side == "left" else 1) if directional else 0
        return ActionProposal(
            module_id=self.module_id,
            action=action,
            active=directional,
            feedback=LocalFeedback(
                module_id=self.module_id,
                side=self.side,
                fired_events=result.fired_events,
                matched_motor_events=result.matched_motor_events,
                opposite_motor_events=result.opposite_motor_events,
                first_matched_motor_time=result.first_matched_motor_time,
            ),
        )


@dataclass(frozen=True)
class ReactiveLocalController:
    """Ordinary reference substitute with the same proposal interface."""

    module_id: str
    side: Side

    def propose(
        self, observation: Observation, modulation: Modulation
    ) -> ActionProposal:
        active = modulation.desired_side == self.side
        action = (-1 if self.side == "left" else 1) if active else 0
        return ActionProposal(
            module_id=self.module_id,
            action=action,
            active=active,
            feedback=LocalFeedback(
                module_id=self.module_id,
                side=self.side,
                fired_events=int(active),
                matched_motor_events=int(active),
                opposite_motor_events=0,
                first_matched_motor_time=0 if active else None,
            ),
        )


@dataclass(frozen=True)
class LoopSnapshot:
    world: WorldState
    sequence: int
    feedback: tuple[LocalFeedback, ...] = ()

    def token(self) -> str:
        payload = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":")
        ).encode()
        return sha256(payload).hexdigest()


@dataclass(frozen=True)
class StepResult:
    accepted: bool
    reason: str
    before: LoopSnapshot
    after: LoopSnapshot
    modulation: Modulation
    proposals: tuple[ActionProposal, ...]


class HierarchicalSensorimotorLoop:
    def __init__(
        self,
        *,
        initial_world: WorldState,
        controllers: tuple[LocalController, ...],
        event_budget: int = 4096,
    ) -> None:
        if len(controllers) < 2:
            raise ValueError("at least two local modules are required")
        if event_budget < 1:
            raise ValueError("event_budget must be positive")
        identities = {(controller.module_id, controller.side) for controller in controllers}
        if len(identities) != len(controllers):
            raise ValueError("local module identities must be unique")
        self._controllers = controllers
        self._event_budget = event_budget
        self._snapshot = LoopSnapshot(world=initial_world, sequence=0)

    @property
    def snapshot(self) -> LoopSnapshot:
        return self._snapshot

    def checkpoint(self) -> str:
        payload = {
            "schema_version": 1,
            "module_ids": [controller.module_id for controller in self._controllers],
            "snapshot": asdict(self._snapshot),
            "token": self._snapshot.token(),
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def restore(self, checkpoint: str) -> None:
        payload = json.loads(checkpoint)
        module_ids = [controller.module_id for controller in self._controllers]
        if payload.get("schema_version") != 1 or payload.get("module_ids") != module_ids:
            raise ValueError("checkpoint controller contract mismatch")
        raw = payload["snapshot"]
        feedback = tuple(LocalFeedback(**item) for item in raw["feedback"])
        restored = LoopSnapshot(
            world=WorldState(**raw["world"]),
            sequence=raw["sequence"],
            feedback=feedback,
        )
        if restored.token() != payload.get("token"):
            raise ValueError("checkpoint token mismatch")
        self._snapshot = restored

    def step(self) -> StepResult:
        before = self._snapshot
        error = before.world.target - before.world.position
        desired_side: Side | None
        if error < 0:
            desired_side = "left"
        elif error > 0:
            desired_side = "right"
        else:
            desired_side = None
        modulation = Modulation(desired_side=desired_side)
        observation = Observation(signed_error=error, sequence=before.sequence)
        try:
            proposals = tuple(
                controller.propose(observation, modulation)
                for controller in self._controllers
            )
            if any(
                proposal.feedback.fired_events > self._event_budget
                for proposal in proposals
            ):
                raise RuntimeError("local event budget exceeded")
            active = tuple(proposal for proposal in proposals if proposal.active)
            if desired_side is None:
                if active:
                    raise RuntimeError("local module acted without modulation")
                action = 0
            elif len(active) != 1:
                raise RuntimeError("action arbitration requires one active module")
            else:
                action = active[0].action
            position = max(-4, min(4, before.world.position + action))
            world = WorldState(
                position=position,
                target=before.world.target,
                step=before.world.step + 1,
            )
            after = LoopSnapshot(
                world=world,
                sequence=before.sequence + 1,
                feedback=tuple(proposal.feedback for proposal in proposals),
            )
            self._snapshot = after
            return StepResult(
                accepted=True,
                reason="COMMITTED",
                before=before,
                after=after,
                modulation=modulation,
                proposals=proposals,
            )
        except (RuntimeError, ValueError) as exc:
            return StepResult(
                accepted=False,
                reason=str(exc),
                before=before,
                after=before,
                modulation=modulation,
                proposals=locals().get("proposals", ()),
            )


def build_fly0_loop(initial_world: WorldState) -> HierarchicalSensorimotorLoop:
    topology = build_structured_topology()
    return HierarchicalSensorimotorLoop(
        initial_world=initial_world,
        controllers=(
            Fly0LocalController("fly0-left", "left", topology),
            Fly0LocalController("fly0-right", "right", topology),
        ),
    )


def build_reactive_loop(initial_world: WorldState) -> HierarchicalSensorimotorLoop:
    return HierarchicalSensorimotorLoop(
        initial_world=initial_world,
        controllers=(
            ReactiveLocalController("reactive-left", "left"),
            ReactiveLocalController("reactive-right", "right"),
        ),
    )


def run_to_target(
    loop: HierarchicalSensorimotorLoop, *, max_steps: int = 8
) -> tuple[StepResult, ...]:
    if not 1 <= max_steps <= 16:
        raise ValueError("max_steps must be in [1, 16]")
    results: list[StepResult] = []
    for _ in range(max_steps):
        if loop.snapshot.world.position == loop.snapshot.world.target:
            break
        result = loop.step()
        results.append(result)
        if not result.accepted:
            break
    return tuple(results)


def probe_summary() -> dict[str, object]:
    rows: dict[str, object] = {}
    for name, builder in (
        ("fly0_structured", build_fly0_loop),
        ("reactive_reference", build_reactive_loop),
    ):
        loop = builder(WorldState(position=2, target=-1))
        checkpoint = loop.checkpoint()
        first = run_to_target(loop)
        first_tokens = [result.after.token() for result in first]
        final = loop.snapshot
        loop.restore(checkpoint)
        second = run_to_target(loop)
        rows[name] = {
            "accepted_steps": sum(result.accepted for result in first),
            "final_position": final.world.position,
            "same_history_replay_exact": first_tokens
            == [result.after.token() for result in second],
            "final_token": final.token(),
            "active_event_counts": [
                sum(
                    proposal.feedback.fired_events
                    for proposal in result.proposals
                )
                for result in first
            ],
        }
    return {
        "status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "initial_position": 2,
        "target": -1,
        "controllers": rows,
    }


if __name__ == "__main__":
    print(json.dumps(probe_summary(), indent=2, sort_keys=True))

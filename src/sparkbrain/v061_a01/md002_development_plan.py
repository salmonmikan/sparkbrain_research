"""Outcome-blind input plan for the future A01 MD-002 P2 development runner.

This module deliberately performs no capability execution. It combines the
already-bound reset/world fixture with the already-fixed four-condition schedule
and proves that every condition is derived from the same frozen L/F/C/R checkpoint
and the same admissible external-evidence bytes. The only registered differences
are the anonymous world arm and whether that returned response will later be
supplied to the A01 bridge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .md002_fixtures import P2WorldArmInput, P2WorldOnlyFixture
from .md002_p2_schedule import P2ClonedSubepisodeSchedule, build_p2_condition_matrix

WorldArm = Literal["control", "intervention"]


@dataclass(frozen=True, slots=True)
class P2DevelopmentConditionInput:
    """One execution-disabled condition package for a later development runner."""

    condition_id: str
    world_arm: WorldArm
    returned_external_evidence: bool
    arm_input: P2WorldArmInput
    schedule: P2ClonedSubepisodeSchedule

    def validate(self) -> None:
        if type(self.condition_id) is not str or not self.condition_id:
            raise ValueError("P2 development condition ID must be non-empty")
        if self.world_arm not in ("control", "intervention"):
            raise ValueError("invalid P2 development world arm")
        if type(self.returned_external_evidence) is not bool:
            raise ValueError("returned_external_evidence must be bool")
        self.arm_input.validate()
        self.schedule.validate()
        if self.arm_input.arm != self.world_arm:
            raise ValueError("P2 condition world arm does not match restored arm input")


def build_p2_development_plan(
    fixture: P2WorldOnlyFixture,
    schedule: P2ClonedSubepisodeSchedule,
) -> tuple[P2DevelopmentConditionInput, ...]:
    """Bind the fixed schedule to the exact four execution-disabled P2 inputs."""

    fixture.validate()
    schedule.validate()
    matrix = build_p2_condition_matrix(schedule)
    conditions: list[P2DevelopmentConditionInput] = []
    for row in matrix:
        world_arm = row["world_arm"]
        if world_arm not in ("control", "intervention"):
            raise ValueError("condition matrix contains an unknown world arm")
        value = P2DevelopmentConditionInput(
            condition_id=str(row["condition_id"]),
            world_arm=world_arm,
            returned_external_evidence=bool(row["returned_external_evidence"]),
            arm_input=fixture.arm(world_arm),
            schedule=schedule,
        )
        value.validate()
        conditions.append(value)

    if tuple(row.condition_id for row in conditions) != (
        "p2-w0-returned",
        "p2-w1-returned",
        "p2-w0-withheld",
        "p2-w1-withheld",
    ):
        raise RuntimeError("P2 development condition order drifted")
    if len({row.arm_input.partitions for row in conditions}) != 1:
        raise RuntimeError("P2 conditions do not share one exact L/F/C/R checkpoint")
    if len({row.arm_input.admissible_external_evidence for row in conditions}) != 1:
        raise RuntimeError("P2 conditions do not share byte-identical admissible evidence")
    if len({row.schedule.state_dict().__repr__() for row in conditions}) != 1:
        raise RuntimeError("P2 conditions do not share one fixed attribution schedule")

    by_id = {row.condition_id: row for row in conditions}
    if (
        by_id["p2-w0-returned"].arm_input.world_relation
        != by_id["p2-w0-withheld"].arm_input.world_relation
    ):
        raise RuntimeError("W0 returned/withheld conditions differ outside evidence return")
    if (
        by_id["p2-w1-returned"].arm_input.world_relation
        != by_id["p2-w1-withheld"].arm_input.world_relation
    ):
        raise RuntimeError("W1 returned/withheld conditions differ outside evidence return")
    if (
        by_id["p2-w0-returned"].arm_input.world_relation
        == by_id["p2-w1-returned"].arm_input.world_relation
    ):
        raise RuntimeError("P2 W0/W1 world intervention did not change the world relation")

    return tuple(conditions)


__all__ = ["P2DevelopmentConditionInput", "build_p2_development_plan"]

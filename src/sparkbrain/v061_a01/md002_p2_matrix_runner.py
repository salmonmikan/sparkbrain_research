"""Outcome-blind development matrix runner for A01 MD-002 P2 attribution.

This module closes one construction gap between the already-bound four-condition
P2 plan and the single-subepisode attribution kernel. It executes every cloned
attribution subepisode for every registered development condition and preserves
condition-level raw results without producing a capability score or opening
formal/held-out authority.

The runner is deliberately *not* the final MD-002 P2 capability runner: the
shared post-attribution probe, preregistered capability scoring/thresholds,
formal evidence preservation, and the global MD002 execution gate remain
separate requirements before any one-way MD-002 execution can occur.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sparkbrain.v06.foundation import validate_runtime_mapping

from .md002_development_plan import build_p2_development_plan
from .md002_fixtures import P2WorldOnlyFixture
from .md002_p2_attribution_kernel import (
    P2AttributionKernelResult,
    execute_p2_attribution_subepisode,
)
from .md002_p2_schedule import P2ClonedSubepisodeSchedule

_EXPECTED_CONDITION_IDS = (
    "p2-w0-returned",
    "p2-w1-returned",
    "p2-w0-withheld",
    "p2-w1-withheld",
)


@dataclass(frozen=True, slots=True)
class P2DevelopmentConditionRun:
    """Raw attribution results for one registered P2 development condition."""

    condition_id: str
    world_arm: str
    returned_external_evidence: bool
    subepisodes: tuple[P2AttributionKernelResult, ...]

    def validate(self) -> None:
        if self.condition_id not in _EXPECTED_CONDITION_IDS:
            raise ValueError("unknown P2 development condition ID")
        if self.world_arm not in ("control", "intervention"):
            raise ValueError("unknown P2 development world arm")
        if type(self.returned_external_evidence) is not bool:
            raise ValueError("returned_external_evidence must be bool")
        if not self.subepisodes:
            raise ValueError("P2 condition run must retain subepisode results")
        proposal_ids: set[str] = set()
        for result in self.subepisodes:
            if result.condition_id != self.condition_id:
                raise ValueError("P2 result condition identity drifted")
            if result.world_arm != self.world_arm:
                raise ValueError("P2 result world-arm identity drifted")
            if result.returned_external_evidence != self.returned_external_evidence:
                raise ValueError("P2 result evidence-return identity drifted")
            if result.proposal_id in proposal_ids:
                raise ValueError("P2 condition run contains duplicate proposal results")
            proposal_ids.add(result.proposal_id)
            if result.field_state_hash_before != result.field_state_hash_after:
                raise RuntimeError("P2 development matrix modified Field state")
            if not self.returned_external_evidence:
                if result.resolution is not None:
                    raise RuntimeError("P2 withheld condition produced a credit resolution")
                if result.local_state_hash_before != result.local_state_hash_after:
                    raise RuntimeError("P2 withheld condition modified local causal support")
                if result.consistency_state_hash_before != result.consistency_state_hash_after:
                    raise RuntimeError("P2 withheld condition modified consistency state")
            elif result.resolution is None:
                raise RuntimeError("P2 returned-evidence condition lacks a credit resolution")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value: dict[str, Any] = {
            "condition_id": self.condition_id,
            "world_arm": self.world_arm,
            "returned_external_evidence": self.returned_external_evidence,
            "subepisodes": [row.state_dict() for row in self.subepisodes],
        }
        validate_runtime_mapping(value, path="v061_a01.md002.p2_condition_run")
        return value


@dataclass(frozen=True, slots=True)
class P2DevelopmentMatrixRun:
    """Complete raw four-condition attribution matrix, still capability-unscored."""

    conditions: tuple[P2DevelopmentConditionRun, ...]

    def validate(self) -> None:
        if tuple(row.condition_id for row in self.conditions) != _EXPECTED_CONDITION_IDS:
            raise ValueError("P2 development matrix condition order drifted")
        if len(self.conditions) != 4:
            raise ValueError("P2 development matrix requires exactly four conditions")
        for row in self.conditions:
            row.validate()

        proposal_orders = tuple(
            tuple(result.proposal_id for result in row.subepisodes)
            for row in self.conditions
        )
        if len(set(proposal_orders)) != 1:
            raise RuntimeError("P2 cloned subepisode order drifted across conditions")

        by_id = {row.condition_id: row for row in self.conditions}
        expected_metadata = {
            "p2-w0-returned": ("control", True),
            "p2-w1-returned": ("intervention", True),
            "p2-w0-withheld": ("control", False),
            "p2-w1-withheld": ("intervention", False),
        }
        for condition_id, expected in expected_metadata.items():
            row = by_id[condition_id]
            if (row.world_arm, row.returned_external_evidence) != expected:
                raise RuntimeError("P2 condition metadata drifted from preregistered matrix")

        for proposal_index in range(len(proposal_orders[0])):
            w0_returned = by_id["p2-w0-returned"].subepisodes[proposal_index]
            w1_returned = by_id["p2-w1-returned"].subepisodes[proposal_index]
            w0_withheld = by_id["p2-w0-withheld"].subepisodes[proposal_index]
            w1_withheld = by_id["p2-w1-withheld"].subepisodes[proposal_index]

            if w0_returned.response_target != w0_withheld.response_target:
                raise RuntimeError("P2 W0 returned/withheld world response drifted")
            if w1_returned.response_target != w1_withheld.response_target:
                raise RuntimeError("P2 W1 returned/withheld world response drifted")
            if w0_returned.response_target == w1_returned.response_target:
                raise RuntimeError("P2 W0/W1 intervention did not permute response target")

            before_hashes = {
                w0_returned.local_state_hash_before,
                w1_returned.local_state_hash_before,
                w0_withheld.local_state_hash_before,
                w1_withheld.local_state_hash_before,
            }
            if len(before_hashes) != 1:
                raise RuntimeError("P2 cloned conditions did not start from one local state")

    def state_dict(self) -> dict[str, Any]:
        self.validate()
        value: dict[str, Any] = {
            "conditions": [row.state_dict() for row in self.conditions],
            "capability_scored": False,
            "formal_execution_opened": False,
        }
        validate_runtime_mapping(value, path="v061_a01.md002.p2_matrix_run")
        return value


def execute_p2_development_matrix(
    fixture: P2WorldOnlyFixture,
    schedule: P2ClonedSubepisodeSchedule,
) -> P2DevelopmentMatrixRun:
    """Execute the complete cloned attribution matrix without capability scoring."""

    fixture.validate()
    schedule.validate()
    conditions = build_p2_development_plan(fixture, schedule)
    rows: list[P2DevelopmentConditionRun] = []
    for condition in conditions:
        subepisodes = tuple(
            execute_p2_attribution_subepisode(condition, subepisode)
            for subepisode in schedule.subepisodes
        )
        row = P2DevelopmentConditionRun(
            condition_id=condition.condition_id,
            world_arm=condition.world_arm,
            returned_external_evidence=condition.returned_external_evidence,
            subepisodes=subepisodes,
        )
        row.validate()
        rows.append(row)

    result = P2DevelopmentMatrixRun(tuple(rows))
    result.validate()
    return result


__all__ = [
    "P2DevelopmentConditionRun",
    "P2DevelopmentMatrixRun",
    "execute_p2_development_matrix",
]

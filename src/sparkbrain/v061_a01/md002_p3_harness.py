"""Fail-closed construction harness for the prospective A01 MD-002 P3 execution.

This layer prepares independently restorable baseline/donor/R-transplanted arms,
binds their exact pre-attribution state/evidence/schema hashes and prospective
execution IDs, and proves that the still-unbound MD-002 execution gate blocks
capability. It does not apply evidence, run an arm, create a runtime trace,
score P3, or open held-out/formal authority.
"""

from __future__ import annotations

from dataclasses import dataclass

from .md002_p3_development_plan import (
    P3DevelopmentConditionInput,
    build_p3_development_plan,
)
from .md002_p3_fixture import P3ReturnAddressFixture, restore_p3_arm
from .md002_protocol import (
    MD002ExecutionGate,
    StatePartitionSnapshot,
    bytes_sha256,
    canonical_sha256,
)


@dataclass(frozen=True, slots=True)
class P3PreparedArm:
    """One execution-disabled arm bound before any P3 capability call exists."""

    condition_id: str
    arm: str
    fixture_sha256: str
    prospective_execution_id: str
    pre_attribution: StatePartitionSnapshot
    admissible_external_evidence_sha256: str
    observation_schema_sha256: str
    negative_stop_schema_sha256: str
    restored_state_sha256: str
    execution_authority: bool = False
    runtime_trace_sha256: str | None = None
    capability_result: bool | None = None
    score: float | None = None

    def validate(self) -> None:
        if not self.condition_id or not self.prospective_execution_id:
            raise ValueError("P3 prepared arm requires non-empty identities")
        if self.arm not in ("baseline", "donor", "transplanted"):
            raise ValueError("invalid P3 prepared arm")
        self.pre_attribution.validate()
        for name in (
            "fixture_sha256",
            "admissible_external_evidence_sha256",
            "observation_schema_sha256",
            "negative_stop_schema_sha256",
            "restored_state_sha256",
        ):
            value = getattr(self, name)
            if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
        if self.fixture_sha256 not in self.prospective_execution_id:
            raise ValueError("P3 execution identity is not bound to the fixture digest")
        if self.execution_authority is not False:
            raise PermissionError("P3 preparation cannot carry execution authority")
        if self.runtime_trace_sha256 is not None:
            raise ValueError("P3 preparation cannot contain a runtime trace")
        if self.capability_result is not None or self.score is not None:
            raise ValueError("P3 preparation cannot contain capability output")


def _fixture_digest(fixture: P3ReturnAddressFixture) -> str:
    fixture.validate()
    return canonical_sha256(
        {
            "baseline": fixture.baseline.snapshot().state_dict(),
            "donor": fixture.donor.snapshot().state_dict(),
            "admissible_external_evidence_sha256": bytes_sha256(
                fixture.admissible_external_evidence
            ),
        }
    )


def _restored_state_digest(condition: P3DevelopmentConditionInput) -> str:
    restored = restore_p3_arm(condition.arm_input)
    # The restore adapter itself verifies exact serialized L/F/C/R and evidence
    # round trips. This digest is construction provenance only; it is not a
    # capability observation.
    return canonical_sha256(
        {
            "local": restored.expectation.learned_state_dict(),
            "field": restored.field.state_dict(),
            "consistency": restored.consistency.learned_state_dict(),
            "return_address": condition.arm_input.snapshot().return_address_sha256,
            "evidence_sha256": condition.admissible_external_evidence_sha256,
        }
    )


def prepare_p3_harness(
    fixture: P3ReturnAddressFixture,
) -> tuple[P3PreparedArm, ...]:
    """Prepare all three exact P3 arms without applying evidence or executing."""

    fixture_sha256 = _fixture_digest(fixture)
    conditions = build_p3_development_plan(fixture)
    prepared = tuple(
        P3PreparedArm(
            condition_id=condition.condition_id,
            arm=condition.arm,
            fixture_sha256=fixture_sha256,
            prospective_execution_id=(
                f"md002-p3-exec-{fixture_sha256}-{index:02d}-{condition.arm}"
            ),
            pre_attribution=condition.arm_input.snapshot(),
            admissible_external_evidence_sha256=condition.admissible_external_evidence_sha256,
            observation_schema_sha256=condition.observation_schema_sha256,
            negative_stop_schema_sha256=condition.negative_stop_schema_sha256,
            restored_state_sha256=_restored_state_digest(condition),
        )
        for index, condition in enumerate(conditions)
    )
    for row in prepared:
        row.validate()

    if len({row.prospective_execution_id for row in prepared}) != 3:
        raise RuntimeError("P3 harness requires three distinct prospective execution IDs")
    if len({row.fixture_sha256 for row in prepared}) != 1:
        raise RuntimeError("P3 harness fixture identity drifted across arms")
    if len({row.admissible_external_evidence_sha256 for row in prepared}) != 1:
        raise RuntimeError("P3 harness evidence binding drifted across arms")
    if len({row.observation_schema_sha256 for row in prepared}) != 1:
        raise RuntimeError("P3 harness observation schema drifted across arms")
    if len({row.negative_stop_schema_sha256 for row in prepared}) != 1:
        raise RuntimeError("P3 harness negative-stop schema drifted across arms")

    by_arm = {row.arm: row for row in prepared}
    baseline = by_arm["baseline"].pre_attribution
    donor = by_arm["donor"].pre_attribution
    transplanted = by_arm["transplanted"].pre_attribution
    for name in ("local_sha256", "field_sha256", "consistency_sha256"):
        if getattr(baseline, name) != getattr(donor, name):
            raise RuntimeError(f"P3 donor drifted from baseline in {name}")
        if getattr(baseline, name) != getattr(transplanted, name):
            raise RuntimeError(f"P3 transplanted arm drifted from baseline in {name}")
    if baseline.return_address_sha256 == donor.return_address_sha256:
        raise RuntimeError("P3 donor R did not differ from baseline R")
    if transplanted.return_address_sha256 != donor.return_address_sha256:
        raise RuntimeError("P3 transplanted arm did not receive donor R")

    return prepared


def prepare_p3_matrix(
    fixtures: tuple[P3ReturnAddressFixture, ...],
) -> tuple[P3PreparedArm, ...]:
    """Prepare the complete P3 fixture set and prove global execution-ID uniqueness."""

    if not fixtures:
        raise ValueError("P3 matrix requires at least one fixture")
    groups = tuple(prepare_p3_harness(fixture) for fixture in fixtures)
    fixture_ids = tuple(group[0].fixture_sha256 for group in groups)
    if len(set(fixture_ids)) != len(fixture_ids):
        raise RuntimeError("P3 matrix contains duplicate fixture identities")
    prepared = tuple(row for group in groups for row in group)
    execution_ids = tuple(row.prospective_execution_id for row in prepared)
    if len(set(execution_ids)) != len(execution_ids):
        raise RuntimeError("P3 matrix contains duplicate prospective execution IDs")
    return prepared


def require_p3_execution_authority(gate: MD002ExecutionGate) -> None:
    """Delegate to the global fail-closed gate before any future capability call."""

    gate.require_authorized()


__all__ = [
    "P3PreparedArm",
    "prepare_p3_harness",
    "prepare_p3_matrix",
    "require_p3_execution_authority",
]

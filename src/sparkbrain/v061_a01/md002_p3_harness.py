"""Fail-closed construction harness for the prospective A01 MD-002 P3 execution.

This layer prepares independently restorable baseline/donor/R-transplanted arms,
binds their exact pre-attribution state/evidence/schema hashes and prospective
execution IDs, and proves that the still-unbound MD-002 execution gate blocks
capability. It does not apply evidence, run an arm, create a runtime trace,
score P3, or open held-out/formal authority.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

from .md002_fixtures import FrozenPartitionBytes
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

P3Direction = Literal["A-to-B", "B-to-A"]
P3_LINEAGE_PATH_A = "local:A->B"
P3_LINEAGE_PATH_B = "local:A->C"


def _active_lineage(partitions: FrozenPartitionBytes) -> str:
    """Derive A/B from the active proposal's credited local-path lineage."""

    partitions.validate()
    if partitions.return_address is None:
        raise ValueError("P3 lineage semantics require observed return-address state")
    try:
        state = json.loads(partitions.return_address.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("P3 return-address bytes are not canonical JSON") from exc
    if not isinstance(state, dict):
        raise ValueError("P3 return-address state must be a mapping")
    proposals = state.get("proposals")
    boundary = state.get("boundary")
    if not isinstance(proposals, list) or not isinstance(boundary, dict):
        raise ValueError("P3 return-address state is missing proposals/boundary")
    source_ids = boundary.get("source_proposal_ids")
    if not isinstance(source_ids, list) or len(source_ids) != 1:
        raise ValueError(
            "P3 direction binding requires exactly one active boundary source proposal"
        )
    source_id = source_ids[0]
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("P3 active boundary source proposal ID must be non-empty")
    by_id: dict[str, dict[str, object]] = {}
    for proposal in proposals:
        if not isinstance(proposal, dict):
            raise ValueError("P3 proposal row must be a mapping")
        proposal_id = proposal.get("proposal_id")
        if not isinstance(proposal_id, str) or not proposal_id:
            raise ValueError("P3 proposal ID must be non-empty")
        if proposal_id in by_id:
            raise ValueError("P3 proposal IDs must be unique")
        by_id[proposal_id] = proposal
    active = by_id.get(source_id)
    if active is None:
        raise ValueError("P3 boundary source proposal is absent from retained R state")
    paths = active.get("local_path_ids")
    if not isinstance(paths, list):
        raise ValueError("P3 active proposal must retain local_path_ids")
    registered = {
        "A": P3_LINEAGE_PATH_A,
        "B": P3_LINEAGE_PATH_B,
    }
    matched = tuple(
        lineage
        for lineage, path_id in registered.items()
        if path_id in paths
    )
    if len(matched) != 1:
        raise ValueError(
            "P3 active proposal must identify exactly one registered A/B local lineage"
        )
    lineage = matched[0]
    expected_target = {"A": "B", "B": "C"}[lineage]
    if active.get("target") != expected_target:
        raise ValueError("P3 active proposal target is inconsistent with credited lineage")
    return lineage


@dataclass(frozen=True, slots=True)
class P3DirectionalFixture:
    """One preregistered P3 direction bound to verifiable live-R lineage semantics."""

    direction: P3Direction
    fixture: P3ReturnAddressFixture

    def validate(self) -> None:
        if self.direction not in ("A-to-B", "B-to-A"):
            raise ValueError("P3 direction must be A-to-B or B-to-A")
        self.fixture.validate()
        baseline_lineage = _active_lineage(self.fixture.baseline)
        donor_lineage = _active_lineage(self.fixture.donor)
        expected = {
            "A-to-B": ("A", "B"),
            "B-to-A": ("B", "A"),
        }[self.direction]
        if (baseline_lineage, donor_lineage) != expected:
            raise ValueError(
                "P3 direction does not match baseline/donor credited lineage: "
                f"expected {expected[0]}->{expected[1]}, "
                f"observed {baseline_lineage}->{donor_lineage}"
            )


@dataclass(frozen=True, slots=True)
class P3PreparedArm:
    """One execution-disabled arm bound before any P3 capability call exists."""

    condition_id: str
    direction: P3Direction
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
        if self.direction not in ("A-to-B", "B-to-A"):
            raise ValueError("P3 prepared arm has an invalid direction")
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
        if self.direction not in self.prospective_execution_id:
            raise ValueError("P3 execution identity is not bound to the registered direction")
        if self.execution_authority is not False:
            raise PermissionError("P3 preparation cannot carry execution authority")
        if self.runtime_trace_sha256 is not None:
            raise ValueError("P3 preparation cannot contain a runtime trace")
        if self.capability_result is not None or self.score is not None:
            raise ValueError("P3 preparation cannot contain capability output")


def _fixture_content_digest(fixture: P3ReturnAddressFixture) -> str:
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


def _fixture_digest(directional: P3DirectionalFixture) -> str:
    directional.validate()
    return canonical_sha256(
        {
            "direction": directional.direction,
            "baseline_active_lineage": _active_lineage(directional.fixture.baseline),
            "donor_active_lineage": _active_lineage(directional.fixture.donor),
            "fixture_content_sha256": _fixture_content_digest(directional.fixture),
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
    directional: P3DirectionalFixture,
) -> tuple[P3PreparedArm, ...]:
    """Prepare one registered direction without applying evidence or executing."""

    directional.validate()
    fixture_sha256 = _fixture_digest(directional)
    conditions = build_p3_development_plan(directional.fixture)
    prepared = tuple(
        P3PreparedArm(
            condition_id=condition.condition_id,
            direction=directional.direction,
            arm=condition.arm,
            fixture_sha256=fixture_sha256,
            prospective_execution_id=(
                "md002-p3-exec-"
                f"{directional.direction}-{fixture_sha256}-{index:02d}-{condition.arm}"
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
    if len({row.direction for row in prepared}) != 1:
        raise RuntimeError("P3 harness direction drifted across arms")
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
    fixtures: tuple[P3DirectionalFixture, P3DirectionalFixture],
) -> tuple[P3PreparedArm, ...]:
    """Prepare exactly the registered A-to-B and B-to-A three-arm matrix."""

    if len(fixtures) != 2:
        raise ValueError("P3 matrix requires exactly two directional fixtures")
    for directional in fixtures:
        directional.validate()
    directions = tuple(directional.direction for directional in fixtures)
    if set(directions) != {"A-to-B", "B-to-A"}:
        raise RuntimeError("P3 matrix requires one A-to-B and one B-to-A fixture")
    content_ids = tuple(
        _fixture_content_digest(directional.fixture) for directional in fixtures
    )
    if len(set(content_ids)) != 2:
        raise RuntimeError("P3 opposite directions cannot reuse the same fixture content")

    ordered = tuple(sorted(fixtures, key=lambda row: row.direction))
    groups = tuple(prepare_p3_harness(directional) for directional in ordered)
    prepared = tuple(row for group in groups for row in group)
    if len(prepared) != 6:
        raise RuntimeError("P3 bidirectional matrix must contain exactly six prepared arms")
    execution_ids = tuple(row.prospective_execution_id for row in prepared)
    if len(set(execution_ids)) != 6:
        raise RuntimeError("P3 matrix contains duplicate prospective execution IDs")
    if {row.direction for row in prepared} != {"A-to-B", "B-to-A"}:
        raise RuntimeError("P3 matrix lost one registered direction")
    return prepared


def require_p3_execution_authority(gate: MD002ExecutionGate) -> None:
    """Delegate to the global fail-closed gate before any future capability call."""

    gate.require_authorized()


__all__ = [
    "P3Direction",
    "P3DirectionalFixture",
    "P3PreparedArm",
    "prepare_p3_harness",
    "prepare_p3_matrix",
    "require_p3_execution_authority",
]

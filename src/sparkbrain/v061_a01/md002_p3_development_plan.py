"""Outcome-blind execution-disabled condition plan for A01 MD-002 P3.

This layer binds the already-reviewed three-arm R-only transplant fixture to one
fixed evidence/application/readout contract. It performs no capability execution,
applies no evidence, and leaves the MD-002 execution-authority gate untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .md002_p3_fixture import P3ArmInput, P3ReturnAddressFixture
from .md002_protocol import bytes_sha256
from .md002_state_binding import canonical_bytes

P3ConditionArm = Literal["baseline", "donor", "transplanted"]

_OBSERVATION_SCHEMA = canonical_bytes(
    {
        "protocol": "v061-a01-md-002-p3-r-only-transplant-plan-v1",
        "execution_authority": False,
        "evidence_application": "exact-admissible-external-evidence-once",
        "required_pre_attribution_partitions": [
            "local_sha256",
            "field_sha256",
            "consistency_sha256",
            "return_address_sha256",
        ],
        "required_post_attribution_partitions": [
            "local_sha256",
            "field_sha256",
            "consistency_sha256",
            "return_address_sha256",
        ],
        "required_runtime_records": [
            "md002-arm-record",
            "competition_sha256",
            "output_sha256",
            "runtime_trace_sha256",
        ],
        "runtime_trace_required": True,
        "independent_execution_id_required": True,
        "expected_outcome": None,
        "score": None,
    }
)

_NEGATIVE_STOP_SCHEMA = canonical_bytes(
    {
        "stop_without_rescue_if": [
            "pre_attribution_lfc_drift",
            "transplanted_r_not_equal_donor_r",
            "admissible_external_evidence_drift",
            "runtime_trace_missing_or_unbound",
            "execution_identity_reused",
            "post_attribution_field_or_consistency_drift",
            "registered_local_update_absent",
        ],
        "same_identity_rerun_for_rescue": False,
        "formal_or_held_out_authority": False,
    }
)


@dataclass(frozen=True, slots=True)
class P3DevelopmentConditionInput:
    """One future P3 development execution input, still capability-disabled."""

    condition_id: str
    arm: P3ConditionArm
    arm_input: P3ArmInput
    observation_schema: bytes = _OBSERVATION_SCHEMA
    negative_stop_schema: bytes = _NEGATIVE_STOP_SCHEMA

    def validate(self) -> None:
        if type(self.condition_id) is not str or not self.condition_id:
            raise ValueError("P3 development condition ID must be non-empty")
        if self.arm not in ("baseline", "donor", "transplanted"):
            raise ValueError("invalid P3 development arm")
        self.arm_input.validate()
        if self.arm_input.arm != self.arm:
            raise ValueError("P3 condition arm does not match arm input")
        if self.observation_schema != _OBSERVATION_SCHEMA:
            raise ValueError("P3 observation contract drifted")
        if self.negative_stop_schema != _NEGATIVE_STOP_SCHEMA:
            raise ValueError("P3 negative stopping contract drifted")

    @property
    def admissible_external_evidence_sha256(self) -> str:
        self.validate()
        return self.arm_input.admissible_external_evidence_sha256

    @property
    def observation_schema_sha256(self) -> str:
        self.validate()
        return bytes_sha256(self.observation_schema)

    @property
    def negative_stop_schema_sha256(self) -> str:
        self.validate()
        return bytes_sha256(self.negative_stop_schema)


def build_p3_development_plan(
    fixture: P3ReturnAddressFixture,
) -> tuple[P3DevelopmentConditionInput, ...]:
    """Bind baseline, donor and R-transplanted inputs before P3 execution exists."""

    fixture.validate()
    fixture.validate_isolation()
    conditions = tuple(
        P3DevelopmentConditionInput(
            condition_id=f"p3-{arm}",
            arm=arm,
            arm_input=fixture.arm(arm),
        )
        for arm in ("baseline", "donor", "transplanted")
    )
    for condition in conditions:
        condition.validate()

    if tuple(row.condition_id for row in conditions) != (
        "p3-baseline",
        "p3-donor",
        "p3-transplanted",
    ):
        raise RuntimeError("P3 development condition order drifted")
    if len({row.admissible_external_evidence_sha256 for row in conditions}) != 1:
        raise RuntimeError("P3 conditions do not share byte-identical external evidence")
    if len({row.observation_schema_sha256 for row in conditions}) != 1:
        raise RuntimeError("P3 conditions do not share one observation contract")
    if len({row.negative_stop_schema_sha256 for row in conditions}) != 1:
        raise RuntimeError("P3 conditions do not share one negative stopping contract")

    by_arm = {row.arm: row.arm_input.partitions for row in conditions}
    baseline = by_arm["baseline"]
    donor = by_arm["donor"]
    transplanted = by_arm["transplanted"]
    for name in ("local", "field", "consistency"):
        if getattr(baseline, name) != getattr(donor, name):
            raise RuntimeError(f"P3 donor drifted from baseline in {name}")
        if getattr(baseline, name) != getattr(transplanted, name):
            raise RuntimeError(f"P3 transplanted arm drifted from baseline in {name}")
    if baseline.return_address == donor.return_address:
        raise RuntimeError("P3 donor R did not differ from baseline R")
    if transplanted.return_address != donor.return_address:
        raise RuntimeError("P3 transplanted arm did not receive donor R")

    return conditions


__all__ = [
    "P3ConditionArm",
    "P3DevelopmentConditionInput",
    "build_p3_development_plan",
]

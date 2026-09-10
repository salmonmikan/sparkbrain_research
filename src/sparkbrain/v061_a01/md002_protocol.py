"""Fail-closed construction contracts for A01 MD-002.

This module contains no capability runner.  It exists to make the corrections
required by the independent MD-001 audit executable *before* any new result is
opened.  In particular it distinguishes a changed anonymous world relation
from a changed causal path, requires a real R-only transplanted state, requires
measured plural ancestry for P4, and binds identical admissible evidence for
A01/N1/N3 comparison.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

MD002_ID = "v061-a01-md-002-supplemental-v1"
_NOT_EVALUATED = "NOT_EVALUATED"


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _require_hash(value: str, name: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True)
class StatePartitionSnapshot:
    """Observed state partitions used by corrected P2/P3 construction."""

    local_sha256: str
    field_sha256: str
    consistency_sha256: str
    return_address_sha256: str | None

    def validate(self) -> None:
        _require_hash(self.local_sha256, "local_sha256")
        _require_hash(self.field_sha256, "field_sha256")
        _require_hash(self.consistency_sha256, "consistency_sha256")
        if self.return_address_sha256 is not None:
            _require_hash(self.return_address_sha256, "return_address_sha256")


@dataclass(frozen=True)
class WorldOnlyInterventionPair:
    """P2 pair where only the anonymous world-relation state may differ."""

    control: StatePartitionSnapshot
    intervention: StatePartitionSnapshot
    control_world_relation_sha256: str
    intervention_world_relation_sha256: str
    admissible_external_evidence_sha256: str

    def validate(self) -> None:
        self.control.validate()
        self.intervention.validate()
        for name in (
            "control_world_relation_sha256",
            "intervention_world_relation_sha256",
            "admissible_external_evidence_sha256",
        ):
            _require_hash(getattr(self, name), name)
        if self.control_world_relation_sha256 == self.intervention_world_relation_sha256:
            raise ValueError("P2 requires a genuinely changed anonymous world relation")
        if self.control.local_sha256 != self.intervention.local_sha256:
            raise ValueError("P2 local temporal state drifted before external evidence")
        if self.control.field_sha256 != self.intervention.field_sha256:
            raise ValueError("P2 Field state drifted before external evidence")
        if self.control.return_address_sha256 != self.intervention.return_address_sha256:
            raise ValueError("P2 return-address state drifted before external evidence")
        if self.control.consistency_sha256 == self.intervention.consistency_sha256:
            raise ValueError("P2 relation intervention did not alter consistency state")


@dataclass(frozen=True)
class ReturnAddressTransplant:
    """P3 construction of baseline L/F/C plus donor R, executed as a third arm."""

    baseline: StatePartitionSnapshot
    donor: StatePartitionSnapshot
    transplanted: StatePartitionSnapshot

    def validate(self) -> None:
        self.baseline.validate()
        self.donor.validate()
        self.transplanted.validate()
        if self.baseline.return_address_sha256 is None:
            raise ValueError("baseline R must be explicitly observed")
        if self.donor.return_address_sha256 is None:
            raise ValueError("donor R must be explicitly observed")
        if self.baseline.return_address_sha256 == self.donor.return_address_sha256:
            raise ValueError("R donor must differ from baseline")
        for field in ("local_sha256", "field_sha256", "consistency_sha256"):
            if getattr(self.transplanted, field) != getattr(self.baseline, field):
                raise ValueError(f"R-only transplant illegally changed {field}")
        if self.transplanted.return_address_sha256 != self.donor.return_address_sha256:
            raise ValueError("transplanted R does not equal donor R")


@dataclass(frozen=True)
class MergedAncestryObservation:
    """P4 evidence must come from a live plural BoundaryEvent ancestry."""

    boundary_source_proposal_ids: tuple[str, ...]
    active_lineages_before: tuple[str, ...]
    active_lineages_after: tuple[str, ...]
    measured_from_runtime: bool

    def validate(self) -> None:
        if not self.measured_from_runtime:
            raise ValueError("P4 lineage sets must be measured from continuing runtime")
        if len(set(self.boundary_source_proposal_ids)) < 2:
            raise ValueError("P4 requires irreducibly merged plural BoundaryEvent ancestry")
        if len(set(self.active_lineages_before)) < 2:
            raise ValueError("P4 requires measured early ambiguity, not a supplied singleton")
        if not set(self.boundary_source_proposal_ids).issubset(self.active_lineages_before):
            raise ValueError("BoundaryEvent ancestry is not represented in measured early lineages")
        if not self.active_lineages_after:
            raise ValueError("P4 requires a measured continuing post-evidence state")


@dataclass(frozen=True)
class ComparatorEvidenceBinding:
    """A01/N1/N3 must consume byte-identical admissible anonymous evidence."""

    a01_sha256: str
    n1_sha256: str
    n3_sha256: str
    resource_matching: str = _NOT_EVALUATED
    full_md002: str = _NOT_EVALUATED

    def validate(self) -> None:
        for name in ("a01_sha256", "n1_sha256", "n3_sha256"):
            _require_hash(getattr(self, name), name)
        if len({self.a01_sha256, self.n1_sha256, self.n3_sha256}) != 1:
            raise ValueError("A01/N1/N3 admissible evidence streams are not identical")
        if self.resource_matching != _NOT_EVALUATED or self.full_md002 != _NOT_EVALUATED:
            raise ValueError("construction contract cannot predeclare a scientific result")


@dataclass(frozen=True)
class MeasuredDynamicCounters:
    """Dynamic/resource fields are accepted only when measured by the live harness."""

    external_effect_latency_steps: int
    state_update_count: int
    router_operation_count: int
    persistent_state_bytes: int
    peak_transient_state_bytes: int
    measured_from_runtime: bool

    def validate(self) -> None:
        if not self.measured_from_runtime:
            raise ValueError("MD-002 dynamic/resource metrics may not be hardcoded")
        values = (
            self.external_effect_latency_steps,
            self.state_update_count,
            self.router_operation_count,
            self.persistent_state_bytes,
            self.peak_transient_state_bytes,
        )
        if any(type(value) is not int or value < 0 for value in values):
            raise ValueError("measured dynamic/resource counters must be non-negative integers")


@dataclass(frozen=True)
class MD002ExecutionGate:
    """No MD-002 capability result may open before both prospective gates."""

    independent_technical_review: bool = False
    execution_authority: bool = False

    def require_authorized(self) -> None:
        if not self.independent_technical_review:
            raise PermissionError("MD-002 independent technical review is not complete")
        if not self.execution_authority:
            raise PermissionError("MD-002 execution authority is not issued")

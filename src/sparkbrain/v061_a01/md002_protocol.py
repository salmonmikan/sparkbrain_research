"""Fail-closed construction contracts for A01 MD-002.

This module contains no capability runner. It makes the corrections required by
the independent MD-001 audit explicit before any new result is opened: a true
world-only P2 intervention, an independently executed R-only P3 transplant arm,
a continuing merged-ancestry P4 record, byte-identical A01/N1/N3 evidence, and
runtime-trace-derived dynamic/resource counters.
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


def _require_identity(value: str, name: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


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
    """P2 pair where only the anonymous external world relation may differ."""

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
        for field in (
            "local_sha256",
            "field_sha256",
            "consistency_sha256",
            "return_address_sha256",
        ):
            if getattr(self.control, field) != getattr(self.intervention, field):
                raise ValueError(f"P2 pre-evidence state drifted in {field}")


@dataclass(frozen=True)
class ExecutedArmRecord:
    """One retained runtime execution record around the attribution event."""

    execution_id: str
    pre_attribution: StatePartitionSnapshot
    post_attribution: StatePartitionSnapshot
    admissible_external_evidence_sha256: str
    competition_sha256: str
    output_sha256: str
    runtime_trace_sha256: str

    def validate(self) -> None:
        _require_identity(self.execution_id, "execution_id")
        self.pre_attribution.validate()
        self.post_attribution.validate()
        for name in (
            "admissible_external_evidence_sha256",
            "competition_sha256",
            "output_sha256",
            "runtime_trace_sha256",
        ):
            _require_hash(getattr(self, name), name)


@dataclass(frozen=True)
class ReturnAddressTransplant:
    """P3 baseline/donor plus an independently executed R-only third arm."""

    baseline: ExecutedArmRecord
    donor: ExecutedArmRecord
    transplanted: ExecutedArmRecord

    def validate(self) -> None:
        for arm in (self.baseline, self.donor, self.transplanted):
            arm.validate()
        execution_ids = {
            self.baseline.execution_id,
            self.donor.execution_id,
            self.transplanted.execution_id,
        }
        if len(execution_ids) != 3:
            raise ValueError("P3 requires three independently identified runtime executions")
        evidence_hashes = {
            self.baseline.admissible_external_evidence_sha256,
            self.donor.admissible_external_evidence_sha256,
            self.transplanted.admissible_external_evidence_sha256,
        }
        if len(evidence_hashes) != 1:
            raise ValueError("P3 arms must consume byte-identical admissible external evidence")

        baseline = self.baseline.pre_attribution
        donor = self.donor.pre_attribution
        transplanted = self.transplanted.pre_attribution
        if baseline.return_address_sha256 is None:
            raise ValueError("baseline R must be explicitly observed")
        if donor.return_address_sha256 is None:
            raise ValueError("donor R must be explicitly observed")
        if baseline.return_address_sha256 == donor.return_address_sha256:
            raise ValueError("R donor must differ from baseline")
        for field in ("local_sha256", "field_sha256", "consistency_sha256"):
            if getattr(transplanted, field) != getattr(baseline, field):
                raise ValueError(f"R-only transplant illegally changed {field}")
        if transplanted.return_address_sha256 != donor.return_address_sha256:
            raise ValueError("transplanted R does not equal donor R")


@dataclass(frozen=True)
class MergedAncestryObservation:
    """P4 continuation bound to a retained runtime trace and plural ancestry."""

    boundary_source_proposal_ids: tuple[str, ...]
    active_lineages_before: tuple[str, ...]
    active_lineages_after: tuple[str, ...]
    runtime_trace_sha256: str
    measurement_record_sha256: str

    def measurement_payload(self) -> dict[str, tuple[str, ...]]:
        return {
            "boundary_source_proposal_ids": self.boundary_source_proposal_ids,
            "active_lineages_before": self.active_lineages_before,
            "active_lineages_after": self.active_lineages_after,
        }

    def validate(self) -> None:
        _require_hash(self.runtime_trace_sha256, "runtime_trace_sha256")
        _require_hash(self.measurement_record_sha256, "measurement_record_sha256")
        if self.measurement_record_sha256 != canonical_sha256(self.measurement_payload()):
            raise ValueError("P4 measurement record digest does not match lineage payload")
        boundary = set(self.boundary_source_proposal_ids)
        before = set(self.active_lineages_before)
        after = set(self.active_lineages_after)
        if len(boundary) < 2:
            raise ValueError("P4 requires irreducibly merged plural BoundaryEvent ancestry")
        if len(before) < 2:
            raise ValueError("P4 requires measured early ambiguity, not a supplied singleton")
        if not boundary.issubset(before):
            raise ValueError("BoundaryEvent ancestry is not represented in measured early lineages")
        if not after:
            raise ValueError("P4 requires a measured continuing post-evidence state")
        if not after.issubset(before):
            raise ValueError("P4 post-evidence lineage set contains unbound unrelated ancestry")
        if not boundary.intersection(after):
            raise ValueError("P4 continuation lost all merged BoundaryEvent source ancestry")


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
class DynamicCounterSample:
    """Retained cumulative runtime instrumentation at one ordered step."""

    step: int
    external_effect_observed: bool
    state_update_count: int
    router_operation_count: int
    persistent_state_bytes: int
    transient_state_bytes: int

    def validate(self) -> None:
        values = (
            self.step,
            self.state_update_count,
            self.router_operation_count,
            self.persistent_state_bytes,
            self.transient_state_bytes,
        )
        if any(type(value) is not int or value < 0 for value in values):
            raise ValueError("runtime counter samples require non-negative integer fields")
        if type(self.external_effect_observed) is not bool:
            raise ValueError("external_effect_observed must be boolean")

    def state_dict(self) -> dict[str, int | bool]:
        self.validate()
        return {
            "step": self.step,
            "external_effect_observed": self.external_effect_observed,
            "state_update_count": self.state_update_count,
            "router_operation_count": self.router_operation_count,
            "persistent_state_bytes": self.persistent_state_bytes,
            "transient_state_bytes": self.transient_state_bytes,
        }


@dataclass(frozen=True)
class MeasuredDynamicCounters:
    """Dynamic/resource metrics derived from a retained counter trace."""

    samples: tuple[DynamicCounterSample, ...]
    trace_sha256: str

    def validate(self) -> None:
        _require_hash(self.trace_sha256, "trace_sha256")
        if not self.samples:
            raise ValueError("MD-002 requires retained runtime counter samples")
        rows = [sample.state_dict() for sample in self.samples]
        if self.trace_sha256 != canonical_sha256(rows):
            raise ValueError("runtime counter trace digest mismatch")
        for previous, current in zip(self.samples, self.samples[1:], strict=True):
            if current.step <= previous.step:
                raise ValueError("runtime counter steps must be strictly increasing")
            if current.state_update_count < previous.state_update_count:
                raise ValueError("state update counter must be cumulative")
            if current.router_operation_count < previous.router_operation_count:
                raise ValueError("router operation counter must be cumulative")
            if previous.external_effect_observed and not current.external_effect_observed:
                raise ValueError("external-effect observation must be cumulative")

    @property
    def external_effect_latency_steps(self) -> int | None:
        self.validate()
        start = self.samples[0].step
        for sample in self.samples:
            if sample.external_effect_observed:
                return sample.step - start
        return None

    @property
    def state_update_count(self) -> int:
        self.validate()
        return self.samples[-1].state_update_count - self.samples[0].state_update_count

    @property
    def router_operation_count(self) -> int:
        self.validate()
        return self.samples[-1].router_operation_count - self.samples[0].router_operation_count

    @property
    def persistent_state_bytes(self) -> int:
        self.validate()
        return self.samples[-1].persistent_state_bytes

    @property
    def peak_transient_state_bytes(self) -> int:
        self.validate()
        return max(sample.transient_state_bytes for sample in self.samples)


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

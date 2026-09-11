"""Fail-closed construction contracts for A01 MD-002.

This module contains no capability runner. It makes the corrections required by
the independent MD-001 audit explicit before any new result is opened: a true
world-only P2 intervention, an independently executed and trace-bound R-only P3
transplant arm, a trace-bound continuing merged-ancestry P4 record,
byte-identical A01/N1/N3 evidence, and runtime-trace-derived dynamic/resource
counters.

The execution authority gate is intentionally unbound in this construction
branch. A later, separately reviewed source revision must pin immutable review
and execution-authority artifact hashes before capability can be opened.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

MD002_ID = "v061-a01-md-002-supplemental-v1"
_NOT_EVALUATED = "NOT_EVALUATED"

# Construction-only branch: these remain deliberately unset.  A later
# independently reviewed gate-binding revision must replace both with exact
# SHA-256 digests of immutable authority artifacts before execution is possible.
PINNED_TECHNICAL_REVIEW_ARTIFACT_SHA256: str | None = None
PINNED_EXECUTION_AUTHORITY_ARTIFACT_SHA256: str | None = None


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_hash(value: str, name: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")


def _require_git_sha(value: str, name: str) -> None:
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{name} must be a 40-character lowercase Git SHA")


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

    def state_dict(self) -> dict[str, str | None]:
        self.validate()
        return {
            "local_sha256": self.local_sha256,
            "field_sha256": self.field_sha256,
            "consistency_sha256": self.consistency_sha256,
            "return_address_sha256": self.return_address_sha256,
        }


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
    """One retained runtime execution record around the attribution event.

    The semantic fields are accepted only when the retained trace contains the
    exact arm record and the trace hash matches.  Relabeling a donor record or
    changing a pre/post snapshot without changing the retained trace therefore
    fails validation.
    """

    execution_id: str
    pre_attribution: StatePartitionSnapshot
    post_attribution: StatePartitionSnapshot
    admissible_external_evidence_sha256: str
    competition_sha256: str
    output_sha256: str
    runtime_trace: tuple[dict[str, Any], ...]
    runtime_trace_sha256: str

    def arm_trace_record(self) -> dict[str, Any]:
        return {
            "type": "md002-arm-record",
            "execution_id": self.execution_id,
            "pre_attribution": self.pre_attribution.state_dict(),
            "post_attribution": self.post_attribution.state_dict(),
            "admissible_external_evidence_sha256": self.admissible_external_evidence_sha256,
            "competition_sha256": self.competition_sha256,
            "output_sha256": self.output_sha256,
        }

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
        if not self.runtime_trace:
            raise ValueError("executed arm requires a retained runtime trace")
        if self.runtime_trace_sha256 != canonical_sha256(self.runtime_trace):
            raise ValueError("executed-arm runtime trace digest mismatch")
        matches = [row for row in self.runtime_trace if row == self.arm_trace_record()]
        if len(matches) != 1:
            raise ValueError(
                "executed-arm semantic fields are not bound to exactly one retained runtime record"
            )


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
        trace_hashes = {
            self.baseline.runtime_trace_sha256,
            self.donor.runtime_trace_sha256,
            self.transplanted.runtime_trace_sha256,
        }
        if len(trace_hashes) != 3:
            raise ValueError("P3 requires three distinct retained runtime traces")
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
            if getattr(donor, field) != getattr(baseline, field):
                raise ValueError(f"P3 donor must match baseline before attribution in {field}")
            if getattr(transplanted, field) != getattr(baseline, field):
                raise ValueError(f"R-only transplant illegally changed {field}")
        if transplanted.return_address_sha256 != donor.return_address_sha256:
            raise ValueError("transplanted R does not equal donor R")

        post = self.transplanted.post_attribution
        if post.local_sha256 == transplanted.local_sha256:
            raise ValueError(
                "P3 transplanted arm must measure the required post-attribution L update"
            )
        for field in ("field_sha256", "consistency_sha256"):
            if getattr(post, field) != getattr(transplanted, field):
                raise ValueError(f"P3 attribution unexpectedly changed {field}")


@dataclass(frozen=True)
class MergedAncestryObservation:
    """P4 continuation bound to a retained runtime trace and plural ancestry."""

    boundary_source_proposal_ids: tuple[str, ...]
    active_lineages_before: tuple[str, ...]
    active_lineages_after: tuple[str, ...]
    runtime_trace: tuple[dict[str, Any], ...]
    runtime_trace_sha256: str
    measurement_record_sha256: str

    def measurement_payload(self) -> dict[str, tuple[str, ...]]:
        return {
            "boundary_source_proposal_ids": self.boundary_source_proposal_ids,
            "active_lineages_before": self.active_lineages_before,
            "active_lineages_after": self.active_lineages_after,
        }

    def trace_measurement_record(self) -> dict[str, Any]:
        return {
            "type": "md002-merged-ancestry-measurement",
            "measurement": self.measurement_payload(),
        }

    def validate(self) -> None:
        _require_hash(self.runtime_trace_sha256, "runtime_trace_sha256")
        _require_hash(self.measurement_record_sha256, "measurement_record_sha256")
        if not self.runtime_trace:
            raise ValueError("P4 requires a retained runtime trace")
        if self.runtime_trace_sha256 != canonical_sha256(self.runtime_trace):
            raise ValueError("P4 runtime trace digest mismatch")
        if self.measurement_record_sha256 != canonical_sha256(self.measurement_payload()):
            raise ValueError("P4 measurement record digest does not match lineage payload")
        matches = [row for row in self.runtime_trace if row == self.trace_measurement_record()]
        if len(matches) != 1:
            raise ValueError("P4 lineage measurement is not bound to the retained runtime trace")

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

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> DynamicCounterSample:
        sample = cls(
            step=state["step"],
            external_effect_observed=state["external_effect_observed"],
            state_update_count=state["state_update_count"],
            router_operation_count=state["router_operation_count"],
            persistent_state_bytes=state["persistent_state_bytes"],
            transient_state_bytes=state["transient_state_bytes"],
        )
        sample.validate()
        return sample


@dataclass(frozen=True)
class MeasuredDynamicCounters:
    """Dynamic/resource metrics parsed from a retained runtime trace."""

    runtime_trace: tuple[dict[str, Any], ...]
    trace_sha256: str

    def validate(self) -> None:
        _require_hash(self.trace_sha256, "trace_sha256")
        if not self.runtime_trace:
            raise ValueError("MD-002 requires a retained runtime instrumentation trace")
        if self.trace_sha256 != canonical_sha256(self.runtime_trace):
            raise ValueError("runtime counter trace digest mismatch")
        samples = self.samples
        if not samples:
            raise ValueError("MD-002 runtime trace contains no counter samples")
        for previous, current in zip(samples, samples[1:], strict=False):
            if current.step <= previous.step:
                raise ValueError("runtime counter steps must be strictly increasing")
            if current.state_update_count < previous.state_update_count:
                raise ValueError("state update counter must be cumulative")
            if current.router_operation_count < previous.router_operation_count:
                raise ValueError("router operation counter must be cumulative")
            if previous.external_effect_observed and not current.external_effect_observed:
                raise ValueError("external-effect observation must be cumulative")

    @property
    def samples(self) -> tuple[DynamicCounterSample, ...]:
        rows: list[DynamicCounterSample] = []
        for record in self.runtime_trace:
            if record.get("type") != "md002-counter-sample":
                continue
            sample_state = record.get("sample")
            if not isinstance(sample_state, dict):
                raise ValueError("counter-sample trace record requires a sample object")
            rows.append(DynamicCounterSample.from_state_dict(sample_state))
        return tuple(rows)

    @property
    def external_effect_latency_steps(self) -> int | None:
        self.validate()
        samples = self.samples
        start = samples[0].step
        for sample in samples:
            if sample.external_effect_observed:
                return sample.step - start
        return None

    @property
    def state_update_count(self) -> int:
        self.validate()
        samples = self.samples
        return samples[-1].state_update_count - samples[0].state_update_count

    @property
    def router_operation_count(self) -> int:
        self.validate()
        samples = self.samples
        return samples[-1].router_operation_count - samples[0].router_operation_count

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
    """Execution stays impossible until immutable authority artifacts are pinned.

    The branch intentionally contains no caller-controlled authorization
    booleans.  Later source must pin exact SHA-256 digests of a technical review
    artifact and a distinct MD-002-specific execution-authority artifact.
    """

    technical_review_artifact: bytes | None = None
    execution_authority_artifact: bytes | None = None

    @staticmethod
    def _validate_authority_artifact(
        raw: bytes,
        *,
        expected_hash: str,
        expected_kind: str,
    ) -> None:
        _require_hash(expected_hash, f"{expected_kind}_artifact_sha256")
        if bytes_sha256(raw) != expected_hash:
            raise PermissionError(f"{expected_kind} artifact hash does not match pinned digest")
        try:
            record = json.loads(raw)
        except (TypeError, ValueError) as exc:
            raise PermissionError(f"{expected_kind} artifact is not valid JSON") from exc
        if record.get("md002_id") != MD002_ID:
            raise PermissionError(f"{expected_kind} artifact targets a different diagnostic")
        if record.get("kind") != expected_kind:
            raise PermissionError(f"{expected_kind} artifact has the wrong authority kind")
        if record.get("approved") is not True:
            raise PermissionError(f"{expected_kind} artifact is not approved")
        _require_git_sha(str(record.get("source_git_sha", "")), "source_git_sha")
        _require_hash(str(record.get("protocol_sha256", "")), "protocol_sha256")
        _require_identity(str(record.get("authority", "")), "authority")

    def require_authorized(self) -> None:
        if PINNED_TECHNICAL_REVIEW_ARTIFACT_SHA256 is None:
            raise PermissionError("MD-002 technical-review artifact digest is not pinned")
        if PINNED_EXECUTION_AUTHORITY_ARTIFACT_SHA256 is None:
            raise PermissionError("MD-002 execution-authority artifact digest is not pinned")
        if self.technical_review_artifact is None:
            raise PermissionError("MD-002 technical-review artifact is missing")
        if self.execution_authority_artifact is None:
            raise PermissionError("MD-002 execution-authority artifact is missing")
        self._validate_authority_artifact(
            self.technical_review_artifact,
            expected_hash=PINNED_TECHNICAL_REVIEW_ARTIFACT_SHA256,
            expected_kind="independent-technical-review",
        )
        self._validate_authority_artifact(
            self.execution_authority_artifact,
            expected_hash=PINNED_EXECUTION_AUTHORITY_ARTIFACT_SHA256,
            expected_kind="execution-authority",
        )

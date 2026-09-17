"""Preservation-qualified C19 official-v4 execution wrapper.

The scientific acquisition implementation is inherited unchanged from official-v3.
This wrapper provides a fresh authority identity while translating to/from v3 only
inside the target-blind scientific harness.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from sparkbrain.v03_external_validation import official_execution as inherited
from sparkbrain.v03_external_validation import official_execution_v3 as v3
from sparkbrain.v03_external_validation.official_protocol_v4 import (
    BASELINES,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
)

EXECUTION_HARNESS_ID = "c19-external-v2-official-harness-v4"
SYNTHETIC_SCOPE = v3.SYNTHETIC_SCOPE
OFFICIAL_SCOPE = v3.OFFICIAL_SCOPE


@dataclass(frozen=True, slots=True)
class ExecutionAdmissionV4:
    scope: str
    evidence_analyst_commit: str | None
    exact_package_commit: str | None
    started_ref: str | None
    planned_identity: str = PLANNED_IDENTITY

    @classmethod
    def synthetic_dev(cls) -> "ExecutionAdmissionV4":
        return cls(SYNTHETIC_SCOPE, None, None, None)

    def validate(self) -> None:
        if self.planned_identity != PLANNED_IDENTITY:
            raise ValueError("planned identity drift")
        if self.scope == SYNTHETIC_SCOPE:
            if any(
                value is not None
                for value in (
                    self.evidence_analyst_commit,
                    self.exact_package_commit,
                    self.started_ref,
                )
            ):
                raise ValueError("synthetic admission cannot impersonate official state")
            return
        if self.scope != OFFICIAL_SCOPE:
            raise ValueError("unknown execution scope")
        if not self.evidence_analyst_commit:
            raise ValueError("official execution requires fresh Analyst admission")
        if not self.exact_package_commit:
            raise ValueError("official execution requires exact package commit binding")
        if not self.started_ref:
            raise ValueError("official execution requires STARTED control ref")


@dataclass(frozen=True, slots=True)
class RawBundleV4:
    records: tuple[dict[str, Any], ...]
    sha256: str

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> "RawBundleV4":
        normalized = tuple(dict(record) for record in records)
        validate_raw_records_v4(normalized)
        return cls(records=normalized, sha256=inherited.sha256_json(normalized))


class RowExecutor(Protocol):
    def __call__(
        self,
        row: Mapping[str, object],
        examples: Sequence[Mapping[str, object]],
    ) -> Sequence[Mapping[str, Any]]: ...


class RawWriter(Protocol):
    def __call__(self, raw: RawBundleV4) -> object: ...


def to_v3_raw(raw: RawBundleV4) -> v3.RawBundleV3:
    translated: list[dict[str, Any]] = []
    for record in raw.records:
        converted = dict(record)
        converted["protocol_id"] = v3.PROTOCOL_ID
        converted["run_identity"] = v3.PLANNED_IDENTITY
        translated.append(converted)
    return v3.RawBundleV3.from_records(translated)


def validate_raw_records_v4(records: Sequence[Mapping[str, Any]]) -> None:
    if not records:
        raise ValueError("raw acquisition must contain prediction records")
    translated: list[dict[str, Any]] = []
    for record in records:
        if record.get("protocol_id") != PROTOCOL_ID:
            raise ValueError("raw protocol_id drift from fresh v4")
        if record.get("run_identity") != PLANNED_IDENTITY:
            raise ValueError("raw run_identity drift from fresh v4")
        converted = dict(record)
        converted["protocol_id"] = v3.PROTOCOL_ID
        converted["run_identity"] = v3.PLANNED_IDENTITY
        translated.append(converted)
    v3.validate_raw_records_v3(translated)


def write_raw_jsonl_no_clobber_v4(path: Path, raw: RawBundleV4) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in raw.records:
            handle.write(inherited.canonical_json(record))
            handle.write("\n")
    return path


def reconstruct_raw_jsonl_v4(path: Path, *, expected_sha256: str) -> RawBundleV4:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("raw JSONL entries must be mappings")
            records.append(value)
    raw = RawBundleV4.from_records(records)
    if raw.sha256 != expected_sha256:
        raise ValueError("reconstructed raw digest mismatch")
    return raw


def assert_runtime_closed_v4() -> None:
    v3.assert_runtime_closed_v3()


def runtime_manifest_v4() -> dict[str, object]:
    manifest = dict(v3.runtime_manifest_v3())
    manifest.update(
        {
            "execution_harness_id": EXECUTION_HARNESS_ID,
            "protocol_id": PROTOCOL_ID,
            "planned_identity": PLANNED_IDENTITY,
            "inherited_scientific_harness": v3.EXECUTION_HARNESS_ID,
        }
    )
    return manifest


class OneWayExecutionHarnessV4:
    def __init__(self, *, boundary: inherited.RuntimeBoundary) -> None:
        boundary.validate()
        self._boundary = boundary
        self._raw: RawBundleV4 | None = None

    def acquire(
        self,
        *,
        admission: ExecutionAdmissionV4,
        examples: Iterable[Mapping[str, object]],
        condition_executor: RowExecutor,
        baseline_executors: Mapping[str, RowExecutor],
        raw_writer: RawWriter,
    ) -> RawBundleV4:
        if self._raw is not None:
            raise RuntimeError("no-clobber: acquisition already exists")
        admission.validate()
        if set(baseline_executors) != set(BASELINES):
            raise ValueError("baseline executor registry must cover the frozen five families")

        v3_admission = v3.ExecutionAdmissionV3(
            scope=admission.scope,
            evidence_analyst_commit=admission.evidence_analyst_commit,
            exact_package_commit=admission.exact_package_commit,
            started_ref=admission.started_ref,
        )
        inherited_raw: list[v3.RawBundleV3] = []
        v3_harness = v3.OneWayExecutionHarnessV3(boundary=self._boundary)
        raw_v3 = v3_harness.acquire(
            admission=v3_admission,
            examples=examples,
            condition_executor=condition_executor,
            baseline_executors=baseline_executors,
            raw_writer=lambda bundle: inherited_raw.append(bundle),
        )
        if inherited_raw != [raw_v3]:
            raise RuntimeError("inherited target-blind raw boundary did not execute exactly once")
        translated: list[dict[str, Any]] = []
        for record in raw_v3.records:
            converted = dict(record)
            converted["protocol_id"] = PROTOCOL_ID
            converted["run_identity"] = admission.planned_identity
            translated.append(converted)
        raw = RawBundleV4.from_records(translated)
        raw_writer(raw)
        self._raw = raw
        return raw

"""Runtime-closed C19 official-v3 execution harness.

This successor changes only protocol/run identity and runtime closure. Scientific
row inventory, executors, target-blind raw schema and structural validation are
inherited unchanged from official-v2.
"""

from __future__ import annotations

import json
import platform
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Protocol

from sparkbrain.v03_external_validation import official_execution as inherited
from sparkbrain.v03_external_validation import official_execution_v2 as v2
from sparkbrain.v03_external_validation.official_protocol_v3 import (
    BASELINES,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
    REQUIRED_TORCH_VERSION,
    expected_row_inventory,
)

EXECUTION_HARNESS_ID = "c19-external-v2-official-harness-v3"
SYNTHETIC_SCOPE = "synthetic_dev_only"
OFFICIAL_SCOPE = "official_one_way"


@dataclass(frozen=True, slots=True)
class ExecutionAdmissionV3:
    scope: str
    evidence_analyst_commit: str | None
    exact_package_commit: str | None
    started_ref: str | None
    planned_identity: str = PLANNED_IDENTITY

    @classmethod
    def synthetic_dev(cls) -> "ExecutionAdmissionV3":
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
class RawBundleV3:
    records: tuple[dict[str, Any], ...]
    sha256: str

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> "RawBundleV3":
        normalized = tuple(dict(record) for record in records)
        validate_raw_records_v3(normalized)
        return cls(records=normalized, sha256=inherited.sha256_json(normalized))


class RowExecutor(Protocol):
    def __call__(
        self,
        row: Mapping[str, object],
        examples: Sequence[Mapping[str, object]],
    ) -> Sequence[Mapping[str, Any]]: ...


class RawWriter(Protocol):
    def __call__(self, raw: RawBundleV3) -> object: ...


def to_v2_raw(raw: RawBundleV3) -> v2.RawBundleV2:
    translated: list[dict[str, Any]] = []
    for record in raw.records:
        converted = dict(record)
        converted["protocol_id"] = v2.PROTOCOL_ID
        converted["run_identity"] = v2.PLANNED_IDENTITY
        translated.append(converted)
    return v2.RawBundleV2.from_records(translated)


def validate_raw_records_v3(records: Sequence[Mapping[str, Any]]) -> None:
    if not records:
        raise ValueError("raw acquisition must contain prediction records")
    translated: list[dict[str, Any]] = []
    for record in records:
        if record.get("protocol_id") != PROTOCOL_ID:
            raise ValueError("raw protocol_id drift from fresh v3")
        if record.get("run_identity") != PLANNED_IDENTITY:
            raise ValueError("raw run_identity drift from fresh v3")
        converted = dict(record)
        converted["protocol_id"] = v2.PROTOCOL_ID
        converted["run_identity"] = v2.PLANNED_IDENTITY
        translated.append(converted)
    v2.validate_raw_records_v2(translated)


def write_raw_jsonl_no_clobber_v3(path: Path, raw: RawBundleV3) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in raw.records:
            handle.write(inherited.canonical_json(record))
            handle.write("\n")
    return path


def reconstruct_raw_jsonl_v3(path: Path, *, expected_sha256: str) -> RawBundleV3:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("raw JSONL entries must be mappings")
            records.append(value)
    raw = RawBundleV3.from_records(records)
    if raw.sha256 != expected_sha256:
        raise ValueError("reconstructed raw digest mismatch")
    return raw


def assert_runtime_closed_v3() -> None:
    if platform.python_implementation() != "CPython":
        raise RuntimeError("official C19-v3 execution requires CPython")
    if ".".join(map(str, sys.version_info[:3])) != "3.11.16":
        raise RuntimeError("official C19-v3 execution requires Python 3.11.16")
    installed = metadata.version("torch")
    if installed != REQUIRED_TORCH_VERSION:
        raise RuntimeError(
            f"official C19-v3 requires torch {REQUIRED_TORCH_VERSION}; got {installed}"
        )
    import torch  # noqa: F401


def runtime_manifest_v3() -> dict[str, object]:
    assert_runtime_closed_v3()
    return {
        "execution_harness_id": EXECUTION_HARNESS_ID,
        "protocol_id": PROTOCOL_ID,
        "planned_identity": PLANNED_IDENTITY,
        "python_implementation": platform.python_implementation(),
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "torch_version": metadata.version("torch"),
        "network_allowed": False,
        "official_fit_tune_select_allowed": False,
        "inherited_scientific_harness": v2.EXECUTION_HARNESS_ID,
    }


class OneWayExecutionHarnessV3:
    def __init__(self, *, boundary: inherited.RuntimeBoundary) -> None:
        boundary.validate()
        self._boundary = boundary
        self._raw: RawBundleV3 | None = None

    def acquire(
        self,
        *,
        admission: ExecutionAdmissionV3,
        examples: Iterable[Mapping[str, object]],
        condition_executor: RowExecutor,
        baseline_executors: Mapping[str, RowExecutor],
        raw_writer: RawWriter,
    ) -> RawBundleV3:
        if self._raw is not None:
            raise RuntimeError("no-clobber: acquisition already exists")
        admission.validate()
        self._boundary.validate()
        if not callable(condition_executor):
            raise ValueError("C19 condition executor must be callable")
        if set(baseline_executors) != set(BASELINES):
            raise ValueError("baseline executor registry must cover the frozen five families")
        frozen_examples = tuple(dict(example) for example in examples)
        if not frozen_examples:
            raise ValueError("execution requires injected examples")

        v2_admission = v2.ExecutionAdmissionV2.synthetic_dev()
        records: list[dict[str, Any]] = []
        for row in expected_row_inventory():
            executor = (
                condition_executor
                if row["row_kind"] == "c19_condition"
                else baseline_executors[str(row["baseline_kind"])]
            )
            for emitted in executor(row, frozen_examples):
                record = v2._materialize_raw_record(  # noqa: SLF001
                    row,
                    emitted,
                    admission=v2_admission,
                )
                record["protocol_id"] = PROTOCOL_ID
                record["run_identity"] = admission.planned_identity
                records.append(record)
        raw = RawBundleV3.from_records(records)
        raw_writer(raw)
        self._raw = raw
        return raw

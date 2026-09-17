"""Fresh C19 official-v2 one-way harness.

The inherited v1 harness remains untouched for provenance. This successor binds
all newly produced raw records to the fresh v2 protocol/identity while reusing
the already-green structural raw validator from the frozen predecessor.
"""

from __future__ import annotations

import hashlib
import platform
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from sparkbrain.v03_external_validation import official_execution as inherited
from sparkbrain.v03_external_validation.official_protocol_v2 import (
    BASELINES,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
    expected_row_inventory,
)

EXECUTION_HARNESS_ID = "c19-external-v2-official-harness-v2"
SYNTHETIC_SCOPE = "synthetic_dev_only"
OFFICIAL_SCOPE = "official_one_way"


@dataclass(frozen=True, slots=True)
class ExecutionAdmissionV2:
    scope: str
    evidence_analyst_commit: str | None
    exact_package_commit: str | None
    started_ref: str | None
    planned_identity: str = PLANNED_IDENTITY

    @classmethod
    def synthetic_dev(cls) -> "ExecutionAdmissionV2":
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
class RawBundleV2:
    records: tuple[dict[str, Any], ...]
    sha256: str

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> "RawBundleV2":
        normalized = tuple(dict(record) for record in records)
        validate_raw_records_v2(normalized)
        return cls(records=normalized, sha256=inherited.sha256_json(normalized))


class RowExecutor(Protocol):
    def __call__(
        self,
        row: Mapping[str, object],
        examples: Sequence[Mapping[str, object]],
    ) -> Sequence[Mapping[str, Any]]: ...


class RawWriter(Protocol):
    def __call__(self, raw: RawBundleV2) -> object: ...


class Preserver(Protocol):
    def __call__(self, raw: RawBundleV2) -> inherited.PreservationReceipt: ...


class Scorer(Protocol):
    def __call__(self, raw: RawBundleV2, evaluator_targets: object) -> Mapping[str, object]: ...


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _non_negative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _materialize_raw_record(
    row: Mapping[str, object],
    emitted: Mapping[str, Any],
    *,
    admission: ExecutionAdmissionV2,
) -> dict[str, Any]:
    if set(emitted) != inherited.EXECUTOR_REQUIRED_KEYS:
        raise ValueError("executor payload keys differ from the bound pre-raw contract")
    inherited.reject_target_leakage(emitted, path="executor")
    record_id = emitted["record_id"]
    if not isinstance(record_id, str) or not record_id:
        raise ValueError("record_id must be a non-empty string before hashing")
    metadata = emitted["metadata"]
    if not isinstance(metadata, Mapping):
        raise ValueError("executor metadata must be a mapping")
    required_metadata = {"final_probabilities", "work_counters", "final_step_index"}
    if not required_metadata.issubset(metadata):
        raise ValueError("executor metadata lacks frozen raw-contract material")
    probabilities = metadata["final_probabilities"]
    work_counters = metadata["work_counters"]
    if not isinstance(probabilities, Mapping) or not probabilities:
        raise ValueError("probabilities must be a non-empty mapping")
    if not isinstance(work_counters, Mapping):
        raise ValueError("work_counters must be a mapping")
    return {
        "protocol_id": PROTOCOL_ID,
        "run_identity": admission.planned_identity,
        "row_id": str(row["row_id"]),
        "row_kind": str(row["row_kind"]),
        "seed": int(row["seed"]),
        "pair_index": _non_negative_int(emitted["pair_index"], "pair_index"),
        "record_id_hash": _sha256_text(record_id),
        "source_index": _non_negative_int(emitted["source_index"], "source_index"),
        "step_index": _non_negative_int(metadata["final_step_index"], "step_index"),
        "prediction": emitted["prediction"],
        "probabilities": dict(probabilities),
        "input_track": row.get("input_track"),
        "gate": row.get("gate"),
        "entity": row.get("entity"),
        "baseline_kind": row.get("baseline_kind"),
        "work_counters": dict(work_counters),
    }


def validate_raw_records_v2(records: Sequence[Mapping[str, Any]]) -> None:
    if not records:
        raise ValueError("raw acquisition must contain prediction records")
    inherited_records: list[dict[str, Any]] = []
    for record in records:
        if record.get("protocol_id") != PROTOCOL_ID:
            raise ValueError("raw protocol_id drift from fresh v2")
        if record.get("run_identity") != PLANNED_IDENTITY:
            raise ValueError("raw run_identity drift from fresh v2")
        converted = dict(record)
        converted["protocol_id"] = inherited.PROTOCOL_ID
        converted["run_identity"] = inherited.PLANNED_IDENTITY
        inherited_records.append(converted)
    inherited.validate_raw_records(inherited_records)


def runtime_manifest_v2() -> dict[str, object]:
    return {
        "execution_harness_id": EXECUTION_HARNESS_ID,
        "protocol_id": PROTOCOL_ID,
        "planned_identity": PLANNED_IDENTITY,
        "python_implementation": platform.python_implementation(),
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "network_allowed": False,
        "official_fit_tune_select_allowed": False,
        "inherited_structural_validator": inherited.EXECUTION_HARNESS_ID,
    }


class OneWayExecutionHarnessV2:
    def __init__(self, *, boundary: inherited.RuntimeBoundary) -> None:
        boundary.validate()
        self._boundary = boundary
        self._raw: RawBundleV2 | None = None
        self._receipt: inherited.PreservationReceipt | None = None

    def acquire(
        self,
        *,
        admission: ExecutionAdmissionV2,
        examples: Iterable[Mapping[str, object]],
        condition_executor: RowExecutor,
        baseline_executors: Mapping[str, RowExecutor],
        raw_writer: RawWriter,
    ) -> RawBundleV2:
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

        records: list[Mapping[str, Any]] = []
        for row in expected_row_inventory():
            executor = (
                condition_executor
                if row["row_kind"] == "c19_condition"
                else baseline_executors[str(row["baseline_kind"])]
            )
            for emitted in executor(row, frozen_examples):
                records.append(_materialize_raw_record(row, emitted, admission=admission))
        raw = RawBundleV2.from_records(records)
        raw_writer(raw)
        self._raw = raw
        return raw

    def preserve(self, *, preserver: Preserver) -> inherited.PreservationReceipt:
        if self._raw is None:
            raise RuntimeError("cannot preserve before raw acquisition")
        if self._receipt is not None:
            raise RuntimeError("no-clobber: preservation receipt already exists")
        receipt = preserver(self._raw)
        receipt.validate_for(self._raw)  # type: ignore[arg-type]
        self._receipt = receipt
        return receipt

    def score(self, *, evaluator_targets: object, scorer: Scorer) -> Mapping[str, object]:
        if self._raw is None or self._receipt is None:
            raise RuntimeError("raw must be immutably preserved before scoring")
        self._receipt.validate_for(self._raw)  # type: ignore[arg-type]
        return scorer(self._raw, evaluator_targets)

"""Executable pre-START harness for the frozen C19-v2 official protocol.

The harness is deliberately data-source agnostic: it never locates or opens the
official Belief-R cache. Callers inject examples and row executors only after a
future Evidence Analyst execution admission. Synthetic/dev fixtures may exercise
the state machine before that admission.
"""

from __future__ import annotations

import hashlib
import json
import platform
import string
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from sparkbrain.v03_external_validation.official_protocol import (
    BASELINES,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
    expected_row_inventory,
)

EXECUTION_HARNESS_ID = "c19-external-v2-official-harness-v1"
FROZEN_PROTOCOL_HEAD = "90c936a7abca7eba0dac1f977753503551e73368"
SYNTHETIC_SCOPE = "synthetic_dev_only"
OFFICIAL_SCOPE = "official_one_way"
EXPECTED_PAIRS_PER_ROW = 1744
FORBIDDEN_RAW_KEYS = frozenset(
    {
        "answer",
        "correct",
        "evaluator_target",
        "evaluator_truth",
        "gold",
        "ground_truth",
        "label",
        "target",
        "target_label",
        "truth",
        "update_required",
        "question",
        "premises",
        "choices_text",
        "official_cache_bytes",
    }
)
RAW_REQUIRED_KEYS = frozenset(
    {
        "protocol_id",
        "run_identity",
        "row_id",
        "row_kind",
        "seed",
        "pair_index",
        "record_id_hash",
        "source_index",
        "step_index",
        "prediction",
        "probabilities",
        "input_track",
        "gate",
        "entity",
        "baseline_kind",
        "work_counters",
    }
)
EXECUTOR_REQUIRED_KEYS = frozenset(
    {"record_id", "source_index", "pair_index", "prediction", "metadata"}
)


def canonical_json(value: object) -> str:
    return json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class RuntimeBoundary:
    network_allowed: bool = False
    official_fit_tune_select_allowed: bool = False

    def validate(self) -> None:
        if self.network_allowed:
            raise ValueError("C19-v2 execution requires network-blocked model execution")
        if self.official_fit_tune_select_allowed:
            raise ValueError("official fit/tune/select is forbidden")


@dataclass(frozen=True, slots=True)
class ExecutionAdmission:
    scope: str
    evidence_analyst_commit: str | None
    exact_package_commit: str | None
    started_ref: str | None
    planned_identity: str = PLANNED_IDENTITY

    @classmethod
    def synthetic_dev(cls) -> ExecutionAdmission:
        return cls(
            scope=SYNTHETIC_SCOPE,
            evidence_analyst_commit=None,
            exact_package_commit=None,
            started_ref=None,
        )

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
class RawBundle:
    records: tuple[dict[str, Any], ...]
    sha256: str

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> RawBundle:
        normalized = tuple(dict(record) for record in records)
        validate_raw_records(normalized)
        return cls(records=normalized, sha256=sha256_json(normalized))


@dataclass(frozen=True, slots=True)
class PreservationReceipt:
    raw_sha256: str
    preserve_ref: str
    immutable: bool

    def validate_for(self, raw: RawBundle) -> None:
        if not self.immutable:
            raise ValueError("raw preservation receipt must be immutable")
        if not self.preserve_ref:
            raise ValueError("raw preservation receipt requires an authority ref")
        if self.raw_sha256 != raw.sha256:
            raise ValueError("preserved raw digest does not match acquisition")


class RowExecutor(Protocol):
    def __call__(
        self,
        row: Mapping[str, object],
        examples: Sequence[Mapping[str, object]],
    ) -> Sequence[Mapping[str, Any]]: ...


class RawWriter(Protocol):
    def __call__(self, raw: RawBundle) -> object: ...


class Preserver(Protocol):
    def __call__(self, raw: RawBundle) -> PreservationReceipt: ...


class Scorer(Protocol):
    def __call__(
        self,
        raw: RawBundle,
        evaluator_targets: object,
    ) -> Mapping[str, object]: ...


def _normalized_key(value: object) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def reject_target_leakage(value: object, *, path: str = "raw") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = _normalized_key(key)
            if normalized in FORBIDDEN_RAW_KEYS:
                raise ValueError(f"target leakage at {path}.{key}")
            reject_target_leakage(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            reject_target_leakage(child, path=f"{path}[{index}]")


def _require_non_negative_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _materialize_raw_record(
    row: Mapping[str, object],
    emitted: Mapping[str, Any],
    *,
    admission: ExecutionAdmission,
) -> dict[str, Any]:
    if set(emitted) != EXECUTOR_REQUIRED_KEYS:
        raise ValueError("executor payload keys differ from the bound pre-raw contract")
    reject_target_leakage(emitted, path="executor")

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
        "pair_index": _require_non_negative_integer(emitted["pair_index"], "pair_index"),
        "record_id_hash": _sha256_text(record_id),
        "source_index": _require_non_negative_integer(
            emitted["source_index"], "source_index"
        ),
        "step_index": _require_non_negative_integer(
            metadata["final_step_index"], "step_index"
        ),
        "prediction": emitted["prediction"],
        "probabilities": dict(probabilities),
        "input_track": row.get("input_track"),
        "gate": row.get("gate"),
        "entity": row.get("entity"),
        "baseline_kind": row.get("baseline_kind"),
        "work_counters": dict(work_counters),
    }


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in string.hexdigits for character in value)
        and value == value.lower()
    )


def validate_raw_records(records: Sequence[Mapping[str, Any]]) -> None:
    if not records:
        raise ValueError("raw acquisition must contain prediction records")

    expected_rows = {
        str(row["row_id"]): dict(row) for row in expected_row_inventory()
    }
    expected_pairs = set(range(EXPECTED_PAIRS_PER_ROW))
    pairs_by_row = {row_id: set() for row_id in expected_rows}
    identity_by_pair: dict[int, tuple[str, int, int]] = {}

    for record in records:
        if set(record) != RAW_REQUIRED_KEYS:
            raise ValueError("raw prediction record keys differ from frozen target-blind schema")
        reject_target_leakage(record)
        if record["protocol_id"] != PROTOCOL_ID:
            raise ValueError("raw protocol_id drift")
        if record["run_identity"] != PLANNED_IDENTITY:
            raise ValueError("raw run_identity drift")

        row_id = record["row_id"]
        if not isinstance(row_id, str) or row_id not in expected_rows:
            raise ValueError("raw prediction references an unknown frozen row")
        expected_row = expected_rows[row_id]
        if record["row_kind"] != expected_row["row_kind"]:
            raise ValueError("raw row_kind differs from frozen row inventory")
        if record["seed"] != expected_row["seed"]:
            raise ValueError("raw seed differs from frozen row inventory")
        for key in ("input_track", "gate", "entity", "baseline_kind"):
            if record[key] != expected_row.get(key):
                raise ValueError(f"raw {key} differs from frozen row inventory")

        pair_index = _require_non_negative_integer(record["pair_index"], "pair_index")
        if pair_index >= EXPECTED_PAIRS_PER_ROW:
            raise ValueError("pair_index is outside the frozen official-pair inventory")
        if pair_index in pairs_by_row[row_id]:
            raise ValueError("duplicate pair_index within a frozen row")
        pairs_by_row[row_id].add(pair_index)

        source_index = _require_non_negative_integer(record["source_index"], "source_index")
        step_index = _require_non_negative_integer(record["step_index"], "step_index")
        record_id_hash = record["record_id_hash"]
        if not _is_sha256(record_id_hash):
            raise ValueError("record_id_hash must be a lowercase SHA-256 digest")
        identity = (record_id_hash, source_index, step_index)
        known_identity = identity_by_pair.setdefault(pair_index, identity)
        if known_identity != identity:
            raise ValueError("cross-row official-pair identity mismatch")

        probabilities = record["probabilities"]
        if not isinstance(probabilities, Mapping) or not probabilities:
            raise ValueError("raw probabilities must be a non-empty mapping")
        work_counters = record["work_counters"]
        if not isinstance(work_counters, Mapping):
            raise ValueError("raw work_counters must be a mapping")

    expected_total = len(expected_rows) * EXPECTED_PAIRS_PER_ROW
    if len(records) != expected_total:
        raise ValueError("raw acquisition record count differs from frozen 55x1744 inventory")
    incomplete_rows = [
        row_id for row_id, seen_pairs in pairs_by_row.items() if seen_pairs != expected_pairs
    ]
    if incomplete_rows:
        raise ValueError("raw acquisition must contain exactly 1744 unique pairs per frozen row")


def write_raw_jsonl_no_clobber(path: Path, raw: RawBundle) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in raw.records:
            handle.write(canonical_json(record))
            handle.write("\n")
    return path


def reconstruct_raw_jsonl(path: Path, *, expected_sha256: str) -> RawBundle:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("raw JSONL entries must be mappings")
            records.append(value)
    raw = RawBundle.from_records(records)
    if raw.sha256 != expected_sha256:
        raise ValueError("reconstructed raw digest mismatch")
    return raw


def runtime_manifest() -> dict[str, object]:
    return {
        "execution_harness_id": EXECUTION_HARNESS_ID,
        "protocol_id": PROTOCOL_ID,
        "frozen_protocol_head": FROZEN_PROTOCOL_HEAD,
        "planned_identity": PLANNED_IDENTITY,
        "python_implementation": platform.python_implementation(),
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "stdlib_only_harness": True,
        "network_allowed": False,
        "official_fit_tune_select_allowed": False,
    }


def validate_executor_registry(
    condition_executor: RowExecutor,
    baseline_executors: Mapping[str, RowExecutor],
) -> None:
    if not callable(condition_executor):
        raise ValueError("C19 condition executor must be callable")
    if set(baseline_executors) != set(BASELINES):
        raise ValueError("baseline executor registry must cover the frozen five families")
    if any(not callable(value) for value in baseline_executors.values()):
        raise ValueError("every baseline executor must be callable")


class OneWayExecutionHarness:
    """Stateful executor enforcing admission, no-clobber, and raw-before-score."""

    def __init__(self, *, boundary: RuntimeBoundary) -> None:
        boundary.validate()
        self._boundary = boundary
        self._raw: RawBundle | None = None
        self._receipt: PreservationReceipt | None = None

    def acquire(
        self,
        *,
        admission: ExecutionAdmission,
        examples: Iterable[Mapping[str, object]],
        condition_executor: RowExecutor,
        baseline_executors: Mapping[str, RowExecutor],
        raw_writer: RawWriter,
    ) -> RawBundle:
        if self._raw is not None:
            raise RuntimeError("no-clobber: acquisition already exists")
        admission.validate()
        self._boundary.validate()
        validate_executor_registry(condition_executor, baseline_executors)
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
            emitted = executor(row, frozen_examples)
            for record in emitted:
                records.append(_materialize_raw_record(row, record, admission=admission))

        raw = RawBundle.from_records(records)
        raw_writer(raw)
        self._raw = raw
        return raw

    def preserve(self, *, preserver: Preserver) -> PreservationReceipt:
        if self._raw is None:
            raise RuntimeError("cannot preserve before raw acquisition")
        if self._receipt is not None:
            raise RuntimeError("no-clobber: preservation receipt already exists")
        receipt = preserver(self._raw)
        receipt.validate_for(self._raw)
        self._receipt = receipt
        return receipt

    def score(
        self,
        *,
        evaluator_targets: object,
        scorer: Scorer,
    ) -> Mapping[str, object]:
        if self._raw is None or self._receipt is None:
            raise RuntimeError("raw must be immutably preserved before scoring")
        self._receipt.validate_for(self._raw)
        return scorer(self._raw, evaluator_targets)

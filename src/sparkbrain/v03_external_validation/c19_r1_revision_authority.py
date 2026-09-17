"""Target-blind C19-R1 stateless revision-authority reduction.

This module does not locate official data and cannot score predictions. It
accepts only the already-admitted C19 visible envelope. The I2 encoding and
seeded readout are inherited exactly from the frozen v4 parent package; R1
changes only the decision mechanism.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v03_external_validation import implementation_binding as v4_binding
from sparkbrain.v03_external_validation.c19_r1_protocol import (
    EXPECTED_PAIRS,
    INPUT_TRACK,
    MECHANISM_ID,
    OFFICIAL_SEEDS,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
    ROW_KIND,
    expected_r1_rows,
)
from sparkbrain.v03_external_validation.official_execution import (
    RuntimeBoundary,
    reject_target_leakage,
)

SYNTHETIC_SCOPE = "synthetic_dev_only"
OFFICIAL_SCOPE = "official_one_way"
BINDING_ID = "c19-r1-same-i2-revision-authority-binding-v1"
PROJECTION_SALT = "c19-readout-v1"
CHOICES = ("a", "b", "c")
RAW_REQUIRED_KEYS = frozenset(
    {
        "protocol_id",
        "run_identity",
        "row_id",
        "row_kind",
        "mechanism_id",
        "seed",
        "pair_index",
        "record_id_hash",
        "source_index",
        "step_index",
        "prediction",
        "probabilities",
        "input_track",
        "selected_visible_step",
        "step0_certainty",
        "step1_certainty",
        "work_counters",
    }
)
_ALLOWED_EXAMPLE_KEYS = {
    "record_id",
    "source_index",
    "pair_index",
    "step_index",
    "question",
    "choices",
}


def _canonical(value: object) -> str:
    return json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _non_negative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _validate_visible_example(example: Mapping[str, object]) -> None:
    if set(example) != _ALLOWED_EXAMPLE_KEYS:
        raise ValueError("R1 accepts only the frozen target-blind visible envelope")


def _pairs(
    examples: Sequence[Mapping[str, object]],
) -> tuple[tuple[int, tuple[Mapping[str, object], Mapping[str, object]]], ...]:
    grouped: dict[int, list[Mapping[str, object]]] = {}
    for example in examples:
        _validate_visible_example(example)
        pair_index = _non_negative_int(example["pair_index"], "pair_index")
        grouped.setdefault(pair_index, []).append(example)
    result = []
    for pair_index, pair in sorted(grouped.items()):
        ordered = tuple(sorted(pair, key=lambda item: int(item["step_index"])))
        if len(ordered) != 2 or tuple(int(item["step_index"]) for item in ordered) != (0, 1):
            raise ValueError("R1 requires exactly visible steps 0 and 1 for every pair")
        if tuple(int(item["source_index"]) for item in ordered) != (0, 1):
            raise ValueError("R1 requires exact C19 source indices 0 and 1")
        result.append((pair_index, (ordered[0], ordered[1])))
    return tuple(result)


def certainty_tuple(probabilities: Mapping[str, float]) -> tuple[float, float]:
    """Return the fixed target-free certainty ordering tuple."""

    if set(probabilities) != set(CHOICES):
        raise ValueError("R1 certainty requires exactly choices a/b/c")
    ranked = sorted((float(probabilities[choice]), choice) for choice in CHOICES)
    ranked.reverse()
    top1 = ranked[0][0]
    top2 = ranked[1][0]
    return (top1 - top2, top1)


def select_revision_authority(
    step0_probabilities: Mapping[str, float],
    step1_probabilities: Mapping[str, float],
) -> tuple[int, dict[str, float], tuple[float, float], tuple[float, float]]:
    """Select a step without labels, history, thresholds, or fitted state."""

    step0 = {choice: float(step0_probabilities[choice]) for choice in CHOICES}
    step1 = {choice: float(step1_probabilities[choice]) for choice in CHOICES}
    certainty0 = certainty_tuple(step0)
    certainty1 = certainty_tuple(step1)
    if certainty1 >= certainty0:
        return 1, step1, certainty0, certainty1
    return 0, step0, certainty0, certainty1


def _top(probabilities: Mapping[str, float]) -> str:
    return min(CHOICES, key=lambda choice: (-float(probabilities[choice]), choice))


def revision_authority_executor(
    row: Mapping[str, object],
    examples: Sequence[Mapping[str, object]],
) -> list[dict[str, Any]]:
    if row.get("row_kind") != ROW_KIND:
        raise ValueError("R1 executor received a non-R1 row")
    if row.get("mechanism_id") != MECHANISM_ID:
        raise ValueError("R1 mechanism id drift")
    if row.get("input_track") != INPUT_TRACK:
        raise ValueError("R1 must use exact I2")
    seed = int(row["seed"])
    if seed not in OFFICIAL_SEEDS:
        raise ValueError("R1 seed outside the prospectively fixed inventory")

    output: list[dict[str, Any]] = []
    for pair_index, (step0_raw, step1_raw) in _pairs(examples):
        encoded = []
        projection_work = 0
        representation_hashes = []
        for raw in (step0_raw, step1_raw):
            visible = v4_binding._validate_example(raw)
            representation = v4_binding.encode_visible(visible, INPUT_TRACK)
            probabilities, operations = v4_binding._project(
                representation, seed=seed, salt=PROJECTION_SALT
            )
            projection_work += operations
            encoded.append((visible, probabilities))
            representation_hashes.append(
                hashlib.sha256(v4_binding.representation_bytes(representation)).hexdigest()
            )

        selected_step, probabilities, certainty0, certainty1 = select_revision_authority(
            encoded[0][1], encoded[1][1]
        )
        final_visible = encoded[1][0]
        output.append(
            {
                "record_id": final_visible.record_id,
                "source_index": final_visible.source_index,
                "pair_index": pair_index,
                "prediction": _top(probabilities),
                "metadata": {
                    "binding_id": BINDING_ID,
                    "mechanism_id": MECHANISM_ID,
                    "input_track": INPUT_TRACK,
                    "seed": seed,
                    "representation_sha256": representation_hashes,
                    "selected_visible_step": selected_step,
                    "step0_certainty": list(certainty0),
                    "step1_certainty": list(certainty1),
                    "final_probabilities": probabilities,
                    "work_counters": {
                        "projection_operations": projection_work,
                        "certainty_sort_comparisons_bound": 6,
                        "authority_tuple_comparisons": 1,
                    },
                    "final_step_index": int(step1_raw["step_index"]),
                },
            }
        )
    return output


@dataclass(frozen=True, slots=True)
class ExecutionAdmissionR1:
    scope: str
    evidence_analyst_commit: str | None
    exact_package_commit: str | None
    started_ref: str | None
    planned_identity: str = PLANNED_IDENTITY

    @classmethod
    def synthetic_dev(cls) -> ExecutionAdmissionR1:
        return cls(SYNTHETIC_SCOPE, None, None, None)

    def validate(self) -> None:
        if self.planned_identity != PLANNED_IDENTITY:
            raise ValueError("R1 planned identity drift")
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
            raise ValueError("unknown R1 execution scope")
        if not self.evidence_analyst_commit:
            raise ValueError("official R1 requires fresh Analyst admission")
        if not self.exact_package_commit:
            raise ValueError("official R1 requires exact package commit")
        if not self.started_ref:
            raise ValueError("official R1 requires STARTED ref")


@dataclass(frozen=True, slots=True)
class RawBundleR1:
    records: tuple[dict[str, Any], ...]
    sha256: str

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> RawBundleR1:
        normalized = tuple(dict(record) for record in records)
        validate_raw_records(normalized)
        digest = hashlib.sha256(_canonical(normalized).encode("utf-8")).hexdigest()
        return cls(normalized, digest)


def _materialize(
    row: Mapping[str, object],
    emitted: Mapping[str, Any],
    *,
    admission: ExecutionAdmissionR1,
) -> dict[str, Any]:
    required = {"record_id", "source_index", "pair_index", "prediction", "metadata"}
    if set(emitted) != required:
        raise ValueError("R1 executor payload keys differ from frozen contract")
    reject_target_leakage(emitted, path="r1_executor")
    metadata = emitted["metadata"]
    if not isinstance(metadata, Mapping):
        raise ValueError("R1 executor metadata must be a mapping")
    final_probabilities = metadata.get("final_probabilities")
    work_counters = metadata.get("work_counters")
    if not isinstance(final_probabilities, Mapping) or not final_probabilities:
        raise ValueError("R1 final probabilities missing")
    if not isinstance(work_counters, Mapping):
        raise ValueError("R1 work counters missing")
    record_id = emitted["record_id"]
    if not isinstance(record_id, str) or not record_id:
        raise ValueError("R1 record_id must be a non-empty string")
    return {
        "protocol_id": PROTOCOL_ID,
        "run_identity": admission.planned_identity,
        "row_id": str(row["row_id"]),
        "row_kind": ROW_KIND,
        "mechanism_id": MECHANISM_ID,
        "seed": int(row["seed"]),
        "pair_index": _non_negative_int(emitted["pair_index"], "pair_index"),
        "record_id_hash": _sha256_text(record_id),
        "source_index": _non_negative_int(emitted["source_index"], "source_index"),
        "step_index": _non_negative_int(metadata["final_step_index"], "step_index"),
        "prediction": emitted["prediction"],
        "probabilities": dict(final_probabilities),
        "input_track": INPUT_TRACK,
        "selected_visible_step": _non_negative_int(
            metadata["selected_visible_step"], "selected_visible_step"
        ),
        "step0_certainty": list(metadata["step0_certainty"]),
        "step1_certainty": list(metadata["step1_certainty"]),
        "work_counters": dict(work_counters),
    }


def validate_raw_records(records: Sequence[Mapping[str, Any]]) -> None:
    if not records:
        raise ValueError("R1 raw acquisition must not be empty")
    rows = {str(row["row_id"]): row for row in expected_r1_rows()}
    expected_pairs = set(range(EXPECTED_PAIRS))
    pairs_by_row = {row_id: set() for row_id in rows}
    join_identity: dict[int, tuple[str, int, int]] = {}

    for record in records:
        if set(record) != RAW_REQUIRED_KEYS:
            raise ValueError("R1 raw record keys differ from frozen schema")
        reject_target_leakage(record, path="r1_raw")
        if record["protocol_id"] != PROTOCOL_ID:
            raise ValueError("R1 raw protocol drift")
        if record["run_identity"] != PLANNED_IDENTITY:
            raise ValueError("R1 raw identity drift")
        row_id = str(record["row_id"])
        if row_id not in rows:
            raise ValueError("R1 raw references unknown row")
        expected = rows[row_id]
        if record["row_kind"] != ROW_KIND:
            raise ValueError("R1 raw row kind drift")
        if record["mechanism_id"] != MECHANISM_ID:
            raise ValueError("R1 raw mechanism drift")
        if record["seed"] != expected["seed"]:
            raise ValueError("R1 raw seed drift")
        if record["input_track"] != INPUT_TRACK:
            raise ValueError("R1 raw I2 binding drift")
        pair_index = _non_negative_int(record["pair_index"], "pair_index")
        if pair_index >= EXPECTED_PAIRS:
            raise ValueError("R1 raw pair index out of range")
        if pair_index in pairs_by_row[row_id]:
            raise ValueError("duplicate R1 pair within row")
        pairs_by_row[row_id].add(pair_index)

        record_hash = record["record_id_hash"]
        if not _is_sha256(record_hash):
            raise ValueError("R1 record_id_hash must be SHA-256")
        source_index = _non_negative_int(record["source_index"], "source_index")
        step_index = _non_negative_int(record["step_index"], "step_index")
        if source_index != 1 or step_index != 1:
            raise ValueError("R1 evaluator join must bind to final visible step")
        identity = (str(record_hash), source_index, step_index)
        prior = join_identity.setdefault(pair_index, identity)
        if prior != identity:
            raise ValueError("R1 cross-seed pair identity mismatch")
        if record["selected_visible_step"] not in (0, 1):
            raise ValueError("R1 selected step must be 0 or 1")

    if len(records) != len(rows) * EXPECTED_PAIRS:
        raise ValueError("R1 raw record count drift")
    if any(seen != expected_pairs for seen in pairs_by_row.values()):
        raise ValueError("R1 raw pair coverage must be total for every seed row")


def write_raw_jsonl_no_clobber(path: Path, raw: RawBundleR1) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in raw.records:
            handle.write(_canonical(record))
            handle.write("\n")
    return path


def reconstruct_raw_jsonl(path: Path, *, expected_sha256: str) -> RawBundleR1:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("R1 JSONL entries must be mappings")
            records.append(value)
    raw = RawBundleR1.from_records(records)
    if raw.sha256 != expected_sha256:
        raise ValueError("R1 reconstructed raw digest mismatch")
    return raw


class R1AcquisitionHarness:
    def __init__(self, *, boundary: RuntimeBoundary) -> None:
        boundary.validate()
        self._boundary = boundary
        self._raw: RawBundleR1 | None = None

    def acquire(
        self,
        *,
        admission: ExecutionAdmissionR1,
        examples: Iterable[Mapping[str, object]],
    ) -> RawBundleR1:
        if self._raw is not None:
            raise RuntimeError("R1 no-clobber: acquisition already exists")
        admission.validate()
        self._boundary.validate()
        frozen_examples = tuple(dict(example) for example in examples)
        if not frozen_examples:
            raise ValueError("R1 acquisition requires injected visible examples")
        records: list[dict[str, Any]] = []
        for row in expected_r1_rows():
            emitted = revision_authority_executor(row, frozen_examples)
            records.extend(_materialize(row, item, admission=admission) for item in emitted)
        raw = RawBundleR1.from_records(records)
        self._raw = raw
        return raw


__all__ = [
    "BINDING_ID",
    "ExecutionAdmissionR1",
    "OFFICIAL_SCOPE",
    "PROJECTION_SALT",
    "R1AcquisitionHarness",
    "RAW_REQUIRED_KEYS",
    "RawBundleR1",
    "SYNTHETIC_SCOPE",
    "certainty_tuple",
    "reconstruct_raw_jsonl",
    "revision_authority_executor",
    "select_revision_authority",
    "validate_raw_records",
    "write_raw_jsonl_no_clobber",
]

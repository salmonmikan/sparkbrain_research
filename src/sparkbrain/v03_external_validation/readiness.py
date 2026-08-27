"""Deterministic C19 engineering-readiness bundle.

This module deliberately has no dataset-loader entry point.  It records the
complete official execution plan and the reason it is blocked without opening
the official Belief-R cache or manufacturing an I2 symbolic representation.
"""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .contracts import (
    BASELINE_KIND_ORDER,
    ENTITY_ORDER,
    EXACT_NINE_ARTIFACT_ORDER,
    GATE_ORDER,
    INPUT_TRACK_ORDER,
    canonical,
    digest,
    validate_baseline_matching,
    validate_disabled_preregistration,
)

SCHEMA_VERSION = "0.3"
PROTOCOL_ID = "c19-external-v1"
RUN_ID = "c19-external-blocked-readiness-v1"
BLOCK_REASON = "missing_truth_free_belief_r_symbolic_adapter"
OFFICIAL_SEEDS = (5901, 5902, 5903, 5904, 5905)
BOOTSTRAP_SEED = 9901
PLANNED_BOOTSTRAP_RESAMPLES = 10_000

INITIAL_PREREGISTRATION = "artifacts/v03/c19_external_validation/preregistration.json"
INITIAL_PREREGISTRATION_SHA256 = (
    "97a2448e2918f3b0a4583520ad2f35d5d47d99813585be7bb3fae32e0b340cfe"
)
C18_CONTRACT_PATH = "src/sparkbrain/v03_integration/contracts.py"
C18_CONTRACT_SHA256 = "567724ab1088e5e9259c9bb2151ae513eb0ef579fbce6b287c3f6850ed328df8"
C18_ACCEPTED_SOURCE_COMMIT = "3f561254dc7bd2f97cb4784f0632fe0be48093cd"
C18_EXECUTION_PIN_COMMIT = "c0c242d848588d76015734a309f72fed0bd1d380"
C18_REQUIRED_METHODS = ("inspect", "record", "checkpoint", "fork")

BELIEF_R_SPEC_PATH = "configs/external_validation/belief_r.json"
BELIEF_R_SPEC_SHA256 = "ed092dd97a176813f011cdf007d4e34a0b9bcc7c855c22983a31ff82e7b0d63c"
BELIEF_R_REPOSITORY = "CAiRE/belief_r"
BELIEF_R_REVISION = "3719f5804c63318037465fecf298a7fd78d99121"
BELIEF_R_LICENSE = "CC-BY-SA-4.0"
BELIEF_R_CACHE_SHA256 = "b584c18328965cf3eb3d36f2f9ef145c1e15c9bf57bba084982ba18df1fa4153"
BELIEF_R_CACHE_SIZE = 2_230_828
BELIEF_R_ROWS = 3_656
BELIEF_R_PAIRS = 1_744
BELIEF_R_UPDATE_PAIRS = 1_074

_FULL_COMMIT = re.compile(r"[0-9a-f]{40}")
_FULL_SHA256 = re.compile(r"[0-9a-f]{64}")


class C19ReadinessValidationError(RuntimeError):
    """Raised when a blocked-readiness bundle violates its frozen contract."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def _exact_keys(value: object, expected: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise C19ReadinessValidationError(f"{label} must have exact keys {sorted(expected)}")
    return value


def _require_commit(value: object, label: str) -> str:
    if not isinstance(value, str) or _FULL_COMMIT.fullmatch(value) is None:
        raise C19ReadinessValidationError(f"{label} must be a lowercase full Git commit")
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _FULL_SHA256.fullmatch(value) is None:
        raise C19ReadinessValidationError(f"{label} must be a lowercase SHA-256")
    return value


def _read_initial_preregistration(root: Path) -> tuple[dict[str, Any], bytes]:
    raw = (root / INITIAL_PREREGISTRATION).read_bytes()
    if _sha256_bytes(raw) != INITIAL_PREREGISTRATION_SHA256:
        raise C19ReadinessValidationError("initial C19 preregistration bytes changed")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise C19ReadinessValidationError("initial C19 preregistration is not UTF-8 JSON") from exc
    validate_disabled_preregistration(value)
    return value, raw


def _read_belief_r_spec(root: Path) -> tuple[dict[str, Any], bytes]:
    raw = (root / BELIEF_R_SPEC_PATH).read_bytes()
    if _sha256_bytes(raw) != BELIEF_R_SPEC_SHA256:
        raise C19ReadinessValidationError("Belief-R specification bytes changed")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise C19ReadinessValidationError("Belief-R specification is not UTF-8 JSON") from exc
    expected = {
        "repository_id": BELIEF_R_REPOSITORY,
        "revision": BELIEF_R_REVISION,
        "filename": "test.csv",
        "split": "test",
        "license": BELIEF_R_LICENSE,
        "expected_sha256": BELIEF_R_CACHE_SHA256,
        "expected_size_bytes": BELIEF_R_CACHE_SIZE,
        "expected_rows": BELIEF_R_ROWS,
        "expected_pairs": BELIEF_R_PAIRS,
        "expected_update_pairs": BELIEF_R_UPDATE_PAIRS,
        "expected_header": [
            "questions",
            "ground_truth",
            "step",
            "modus",
            "types_of_relation",
            "agreement_lv",
            "atomic_idx",
            "dataset_id",
            "a",
            "b",
            "c",
        ],
    }
    if value != expected:
        raise C19ReadinessValidationError("Belief-R specification differs from the frozen C06 pin")
    return value, raw


def build_frozen_protocol(*, root: Path, source_commit: str) -> dict[str, Any]:
    """Build the pin amendment without reading the official dataset cache."""

    source_commit = _require_commit(source_commit, "source_commit")
    preregistration, preregistration_raw = _read_initial_preregistration(root)
    _spec, spec_raw = _read_belief_r_spec(root)
    c18_contract = root / C18_CONTRACT_PATH
    if _sha256_file(c18_contract) != C18_CONTRACT_SHA256:
        raise C19ReadinessValidationError("accepted C18 contract source bytes changed")
    return {
        "artifact_inventory": list(EXACT_NINE_ARTIFACT_ORDER),
        "baseline_kinds": list(BASELINE_KIND_ORDER),
        "belief_r_contract": {
            "cache_content_read": False,
            "cache_sha256": BELIEF_R_CACHE_SHA256,
            "cache_size_bytes": BELIEF_R_CACHE_SIZE,
            "expected_pairs": BELIEF_R_PAIRS,
            "expected_rows": BELIEF_R_ROWS,
            "expected_update_pairs": BELIEF_R_UPDATE_PAIRS,
            "filename": "test.csv",
            "license": BELIEF_R_LICENSE,
            "repository_id": BELIEF_R_REPOSITORY,
            "revision": BELIEF_R_REVISION,
            "spec_path": BELIEF_R_SPEC_PATH,
            "spec_sha256": _sha256_bytes(spec_raw),
            "split": "test",
        },
        "blocker": {
            "component": "I2_symbolic_oracle",
            "phase": "preflight",
            "reason_code": BLOCK_REASON,
        },
        "c18_contract": {
            "accepted_source_commit": C18_ACCEPTED_SOURCE_COMMIT,
            "available": True,
            "contract_path": C18_CONTRACT_PATH,
            "contract_sha256": C18_CONTRACT_SHA256,
            "execution_pin_commit": C18_EXECUTION_PIN_COMMIT,
            "provider": "V03TraceSession",
            "required_methods": list(C18_REQUIRED_METHODS),
        },
        "checkpoint_selection": preregistration["checkpoint_selection"],
        "condition_matrix": preregistration["condition_matrix"],
        "fresh_seed_contract": preregistration["fresh_seed_contract"],
        "initial_preregistration_path": INITIAL_PREREGISTRATION,
        "initial_preregistration_sha256": _sha256_bytes(preregistration_raw),
        "official_data_access": {
            "cache_verified": False,
            "examples_read": False,
            "policy": "blocked_before_cache_open",
        },
        "official_evaluation_allowed": False,
        "protocol_id": PROTOCOL_ID,
        "run_id": RUN_ID,
        "schema_version": SCHEMA_VERSION,
        "source_commit": source_commit,
        "status": "blocked_engineering_readiness",
    }


def _matrix_condition_ids() -> tuple[str, ...]:
    return tuple(
        f"{input_track}/{gate}/{entity}"
        for input_track in INPUT_TRACK_ORDER
        for gate in GATE_ORDER
        for entity in ENTITY_ORDER
    )


def _planned_run_rows(source_commit: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in OFFICIAL_SEEDS:
        for condition_id in _matrix_condition_ids():
            rows.append(
                {
                    "baseline_kind": None,
                    "checkpoint_hash": None,
                    "condition_id": condition_id,
                    "official_examples_read": False,
                    "output_row_count": 0,
                    "phase": "preflight",
                    "reason_code": BLOCK_REASON,
                    "row_kind": "official_condition",
                    "run_id": RUN_ID,
                    "seed": seed,
                    "source_commit": source_commit,
                    "status": "blocked",
                }
            )
    for seed in OFFICIAL_SEEDS:
        for baseline_kind in BASELINE_KIND_ORDER:
            rows.append(
                {
                    "baseline_kind": baseline_kind,
                    "checkpoint_hash": None,
                    "condition_id": None,
                    "official_examples_read": False,
                    "output_row_count": 0,
                    "phase": "preflight",
                    "reason_code": BLOCK_REASON,
                    "row_kind": "baseline",
                    "run_id": RUN_ID,
                    "seed": seed,
                    "source_commit": source_commit,
                    "status": "blocked",
                }
            )
    return rows


def _metrics(source_commit: str) -> dict[str, Any]:
    return {
        "autonomous": {"metrics": None, "status": "not_evaluated"},
        "condition_rows": [
            {"condition_id": condition_id, "metrics": None, "status": "not_evaluated"}
            for condition_id in _matrix_condition_ids()
        ],
        "official_prediction_rows": 0,
        "oracle": {"metrics": None, "status": "not_evaluated"},
        "protocol_id": PROTOCOL_ID,
        "reason_code": BLOCK_REASON,
        "schema_version": SCHEMA_VERSION,
        "source_commit": source_commit,
        "status": "not_evaluated",
    }


def _paired_statistics(source_commit: str) -> dict[str, Any]:
    return {
        "bootstrap_seed": BOOTSTRAP_SEED,
        "comparisons": None,
        "executed_resamples": 0,
        "planned_resamples": PLANNED_BOOTSTRAP_RESAMPLES,
        "protocol_id": PROTOCOL_ID,
        "reason_code": BLOCK_REASON,
        "schema_version": SCHEMA_VERSION,
        "source_commit": source_commit,
        "status": "not_evaluated",
    }


def _baseline_matching(source_commit: str) -> dict[str, Any]:
    rows = [
        {
            "baseline_kind": baseline_kind,
            "checkpoint_selection_split": "dev",
            "compute_match": False,
            "data_match": False,
            "optimization_match": False,
            "parameter_match": False,
            "winner_claim_allowed": False,
        }
        for baseline_kind in BASELINE_KIND_ORDER
    ]
    return {
        "protocol_id": PROTOCOL_ID,
        "reason_code": BLOCK_REASON,
        "rows": rows,
        "schema_version": SCHEMA_VERSION,
        "source_commit": source_commit,
        "status": "not_evaluated",
        "winner_claim": False,
    }


def _failure_rows(source_commit: str, frozen_protocol: Mapping[str, Any]) -> list[dict[str, Any]]:
    material = {
        "protocol_id": PROTOCOL_ID,
        "reason_code": BLOCK_REASON,
        "source_commit": source_commit,
    }
    return [
        {
            "failure_id": f"c19-blocker:{digest(material)[:16]}",
            "input_hash": digest(frozen_protocol),
            "reason_code": BLOCK_REASON,
            "source_commit_hash": hashlib.sha256(source_commit.encode("ascii")).hexdigest(),
        }
    ]


def _report(source_commit: str, frozen_protocol: Mapping[str, Any]) -> str:
    protocol_hash = digest(frozen_protocol)
    return f"""# C19 External Validation — Blocked Engineering Readiness

## Engineering status

`blocked_engineering_readiness`. The exact-nine writer, execution inventory, pins, and strict
validators are present. This is not C19 engineering acceptance and does not complete G09.

## Scientific status

`not_evaluated`. No official Belief-R example was opened and no official prediction was made.

## Blocking reason

`{BLOCK_REASON}`. The repository has no preregistered truth-free adapter from Belief-R natural
language to the I2 symbolic-event contract. Evaluator truth is not substituted for that adapter.

## Frozen inputs

- source commit: `{source_commit}`
- frozen protocol canonical SHA-256: `{protocol_hash}`
- Belief-R revision: `{BELIEF_R_REVISION}`
- Belief-R cache SHA-256: `{BELIEF_R_CACHE_SHA256}` (pinned metadata only; cache not opened)
- C18 accepted source: `{C18_ACCEPTED_SOURCE_COMMIT}`

## Planned evaluation

The manifest retains 60 official matrix rows (12 conditions x 5 seeds) and 25 baseline rows
(5 families x 5 seeds). Every row is blocked at preflight and has zero output rows.

## Results boundary

Autonomous metrics, Oracle metrics, paired statistics, attribution, and all baseline matching
outcomes are not evaluated. All four matching axes are false and no winner claim is allowed.
C06 remains the existing negative external result; this bundle neither replaces nor upgrades it.

## Reproduction

Run `python scripts/run_c19_external_validation.py --source-commit {source_commit}` from a clean,
locally available checkout. The command reads only versioned protocol/spec/source-contract files;
it has no official dataset cache argument or loader.
"""


def _json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _jsonl_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join((canonical(row) + "\n").encode("utf-8") for row in rows)


def build_bundle_documents(*, root: Path, source_commit: str) -> dict[str, bytes]:
    frozen_protocol = build_frozen_protocol(root=root, source_commit=source_commit)
    documents = {
        "attribution_rows.jsonl": b"",
        "baseline_matching.json": _json_bytes(_baseline_matching(source_commit)),
        "failure_examples.jsonl": _jsonl_bytes(
            _failure_rows(source_commit, frozen_protocol)
        ),
        "frozen_protocol.json": _json_bytes(frozen_protocol),
        "metrics_by_condition.json": _json_bytes(_metrics(source_commit)),
        "paired_statistics.json": _json_bytes(_paired_statistics(source_commit)),
        "raw_predictions.jsonl": b"",
        "report.md": _report(source_commit, frozen_protocol).encode("utf-8"),
        "run_manifest.jsonl": _jsonl_bytes(_planned_run_rows(source_commit)),
    }
    if tuple(sorted(documents)) != tuple(sorted(EXACT_NINE_ARTIFACT_ORDER)):
        raise C19ReadinessValidationError("writer inventory is not exact-nine")
    return documents


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise C19ReadinessValidationError(f"invalid UTF-8 JSON: {path.name}") from exc


def _load_jsonl(path: Path) -> list[Any]:
    try:
        text = path.read_text(encoding="utf-8")
        return [json.loads(line) for line in text.splitlines()]
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise C19ReadinessValidationError(f"invalid UTF-8 JSONL: {path.name}") from exc


def _validate_frozen_protocol(value: object, *, root: Path) -> str:
    row = _exact_keys(
        value,
        {
            "artifact_inventory",
            "baseline_kinds",
            "belief_r_contract",
            "blocker",
            "c18_contract",
            "checkpoint_selection",
            "condition_matrix",
            "fresh_seed_contract",
            "initial_preregistration_path",
            "initial_preregistration_sha256",
            "official_data_access",
            "official_evaluation_allowed",
            "protocol_id",
            "run_id",
            "schema_version",
            "source_commit",
            "status",
        },
        "frozen_protocol",
    )
    source_commit = _require_commit(row["source_commit"], "frozen_protocol.source_commit")
    expected = build_frozen_protocol(root=root, source_commit=source_commit)
    if row != expected:
        raise C19ReadinessValidationError("frozen_protocol differs from the pinned amendment")
    return source_commit


def _validate_run_rows(rows: list[Any], *, source_commit: str) -> None:
    expected = _planned_run_rows(source_commit)
    if rows != expected:
        raise C19ReadinessValidationError(
            "run_manifest must retain exact ordered 60 matrix and 25 baseline blocked rows"
        )
    keys = {
        "baseline_kind",
        "checkpoint_hash",
        "condition_id",
        "official_examples_read",
        "output_row_count",
        "phase",
        "reason_code",
        "row_kind",
        "run_id",
        "seed",
        "source_commit",
        "status",
    }
    for index, row in enumerate(rows):
        _exact_keys(row, keys, f"run_manifest[{index}]")


def validate_bundle(output: Path, *, root: Path) -> dict[str, str]:
    if not output.is_dir():
        raise C19ReadinessValidationError("bundle output must be a directory")
    entries = sorted(item.name for item in output.iterdir())
    if entries != sorted(EXACT_NINE_ARTIFACT_ORDER):
        raise C19ReadinessValidationError("bundle directory must contain exact-nine files")
    if any(not (output / name).is_file() for name in entries):
        raise C19ReadinessValidationError("bundle inventory must contain files only")

    frozen_protocol = _load_json(output / "frozen_protocol.json")
    source_commit = _validate_frozen_protocol(frozen_protocol, root=root)
    _validate_run_rows(_load_jsonl(output / "run_manifest.jsonl"), source_commit=source_commit)
    if _load_jsonl(output / "raw_predictions.jsonl"):
        raise C19ReadinessValidationError("blocked bundle must contain zero official predictions")
    if _load_jsonl(output / "attribution_rows.jsonl"):
        raise C19ReadinessValidationError("blocked bundle must contain zero attribution rows")

    if _load_json(output / "metrics_by_condition.json") != _metrics(source_commit):
        raise C19ReadinessValidationError("metrics must remain exact not_evaluated/null")
    if _load_json(output / "paired_statistics.json") != _paired_statistics(source_commit):
        raise C19ReadinessValidationError("paired statistics must remain exact not_evaluated/null")
    matching = _load_json(output / "baseline_matching.json")
    expected_matching = _baseline_matching(source_commit)
    if matching != expected_matching:
        raise C19ReadinessValidationError("baseline matching document differs from freeze")
    for row in matching["rows"]:
        validate_baseline_matching(row)

    expected_failures = _failure_rows(source_commit, frozen_protocol)
    if _load_jsonl(output / "failure_examples.jsonl") != expected_failures:
        raise C19ReadinessValidationError("failure examples must contain hashes/reason only")
    report = (output / "report.md").read_text(encoding="utf-8")
    if report != _report(source_commit, frozen_protocol):
        raise C19ReadinessValidationError("report is not the deterministic blocked report")

    return {name: _sha256_file(output / name) for name in EXACT_NINE_ARTIFACT_ORDER}


def write_blocked_readiness_bundle(
    output: Path, *, root: Path, source_commit: str
) -> dict[str, str]:
    """Atomically publish one validated exact-nine directory."""

    source_commit = _require_commit(source_commit, "source_commit")
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    documents = build_bundle_documents(root=root, source_commit=source_commit)
    with tempfile.TemporaryDirectory(prefix=f".{output.name}.staging-", dir=output.parent) as tmp:
        staging = Path(tmp)
        for name in EXACT_NINE_ARTIFACT_ORDER:
            (staging / name).write_bytes(documents[name])
        validate_bundle(staging, root=root)
        staging.replace(output)
    return validate_bundle(output, root=root)

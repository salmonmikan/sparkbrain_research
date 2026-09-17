#!/usr/bin/env python3
"""C19-R2 authority-bound one-way runner over the frozen seven-state FSA contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.evaluation import network_blocked
from sparkbrain.v03_external_validation import official_execution as inherited
from sparkbrain.v03_external_validation.c19_r2_protocol import (
    CONFIG_PATH,
    PROTOCOL_ID,
    expected_r2_rows,
    load_and_validate_contract,
)
from sparkbrain.v03_external_validation.c19_r2_scoring import (
    RawBundleR2,
    score_reduction,
)
from sparkbrain.v03_external_validation.c19_r2_source_map import (
    read_atomic_idx_source_map,
    write_atomic_idx_source_map_no_clobber,
)
from sparkbrain.v03_external_validation.c19_r2_state_tracker import (
    state_tracker_executor,
)
from sparkbrain.v03_external_validation.official_execution_v4 import (
    reconstruct_raw_jsonl_v4,
)
from sparkbrain.v03_external_validation.official_io_v4 import (
    assert_visible_envelope_target_blind,
    evaluator_targets_after_preservation,
    load_verified_official_pairs,
    target_blind_visible_examples,
)

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "configs/external_validation/c19_r2_execution_authority.json"
DEFAULT_SPEC = ROOT / "configs/external_validation/belief_r.json"
DEFAULT_CACHE = ROOT / "data/external/belief_r/test.csv"
SHA1 = re.compile(r"[0-9a-f]{40}")
IDENTITY = "c19-r2-fsa-state-tracker-official-v1"
STARTED_PREFIX = "control/c19-r2-fsa-state-tracker-started-"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_head() -> str:
    return _git("rev-parse", "HEAD")


def _require_sha(value: str, name: str) -> str:
    if SHA1.fullmatch(value) is None:
        raise ValueError(f"{name} must be a full 40-character Git SHA")
    return value


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_json_no_clobber(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


def _write_raw_jsonl_no_clobber(path: Path, raw: RawBundleR2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in raw.records:
            handle.write(inherited.canonical_json(record))
            handle.write("\n")


def _reconstruct_r2_raw(path: Path, expected_sha256: str) -> RawBundleR2:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("R2 raw JSONL entries must be mappings")
            records.append(value)
    raw = RawBundleR2.from_records(records)
    if raw.sha256 != expected_sha256:
        raise ValueError("R2 reconstructed raw digest mismatch")
    return raw


def _validate_authority(
    *, analyst_commit: str, package_commit: str
) -> dict[str, Any]:
    authority = _read_json(AUTHORITY_PATH)
    expected = {
        "schema_version": "1",
        "state": "EXECUTION_AUTHORIZED",
        "run_identity": IDENTITY,
        "execution_limit": 1,
        "no_retry_after_started": True,
    }
    for key, value in expected.items():
        if authority.get(key) != value:
            raise ValueError(f"R2 authority drift: {key}")
    if authority.get("evidence_analyst_commit") != analyst_commit:
        raise ValueError("R2 authority Analyst commit mismatch")
    scientific_package = _require_sha(
        str(authority.get("scientific_package_commit", "")),
        "scientific_package_commit",
    )
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", scientific_package, package_commit],
        cwd=ROOT,
        check=True,
    )
    allowed = authority.get("allowed_authority_paths")
    if not isinstance(allowed, list) or not all(
        isinstance(item, str) for item in allowed
    ):
        raise ValueError("R2 authority allowed path set missing")
    changed = set(
        _git(
            "diff", "--name-only", f"{scientific_package}..{package_commit}"
        ).splitlines()
    )
    forbidden = changed - set(allowed)
    if forbidden:
        raise ValueError(
            f"R2 authority package changed forbidden paths: {sorted(forbidden)}"
        )

    bound_objects: list[Mapping[str, Any]] = []
    for key in ("scientific_contract", "preregistration"):
        value = authority.get(key)
        if not isinstance(value, Mapping):
            raise ValueError(f"R2 authority missing {key}")
        bound_objects.append(value)
    scientific_sources = authority.get("scientific_sources")
    if not isinstance(scientific_sources, Mapping):
        raise ValueError("R2 authority missing scientific source bindings")
    for value in scientific_sources.values():
        if not isinstance(value, Mapping):
            raise ValueError("R2 scientific source binding malformed")
        bound_objects.append(value)
    for binding in bound_objects:
        path = str(binding.get("path", ""))
        expected_blob = str(binding.get("blob_sha", ""))
        if not path or SHA1.fullmatch(expected_blob) is None:
            raise ValueError("R2 scientific blob binding malformed")
        actual_blob = _git("hash-object", path)
        if actual_blob != expected_blob:
            raise ValueError(f"R2 frozen scientific blob drift: {path}")

    frozen = load_and_validate_contract(ROOT / CONFIG_PATH)
    if (
        frozen["formal_identity"] is not None
        or frozen["official_execution_allowed"] is not False
    ):
        raise ValueError(
            "R2 frozen scientific specification was mutated during authority packaging"
        )
    return authority


def prestart_smoke(args: argparse.Namespace) -> None:
    package_commit = _require_sha(
        args.package_commit or _git_head(), "package_commit"
    )
    analyst_commit = _require_sha(args.analyst_commit, "analyst_commit")
    if _git_head() != package_commit:
        raise RuntimeError("R2 pre-START smoke must run from exact package commit")
    authority = _validate_authority(
        analyst_commit=analyst_commit,
        package_commit=package_commit,
    )
    if (
        authority.get("started_ref")
        != "control/c19-r2-fsa-state-tracker-started-v1-20260918"
    ):
        raise ValueError("R2 STARTED ref binding drift")
    if authority.get("preserve_ref") != (
        "preserve/c19-r2-fsa-state-tracker-raw-"
        "c19-r2-fsa-state-tracker-official-v1"
    ):
        raise ValueError("R2 preserve ref binding drift")
    if authority.get("evidence_tag") != (
        "evidence/c19-r2-fsa-state-tracker-"
        "c19-r2-fsa-state-tracker-official-v1"
    ):
        raise ValueError("R2 evidence tag binding drift")
    rows = expected_r2_rows()
    if len(rows) != 5:
        raise ValueError("R2 row inventory drift")
    print(
        json.dumps(
            {
                "status": "R2_AUTHORITY_PACKAGE_READY",
                "run_identity": IDENTITY,
                "rows": len(rows),
            },
            sort_keys=True,
        )
    )


def acquire_raw(args: argparse.Namespace) -> None:
    package_commit = _require_sha(args.package_commit, "package_commit")
    analyst_commit = _require_sha(args.analyst_commit, "analyst_commit")
    if _git_head() != package_commit:
        raise RuntimeError("R2 official acquisition must run from exact package commit")
    if not args.started_ref.startswith(STARTED_PREFIX):
        raise ValueError("R2 STARTED ref outside authorized namespace")
    authority = _validate_authority(
        analyst_commit=analyst_commit,
        package_commit=package_commit,
    )
    if authority.get("started_ref") != args.started_ref:
        raise ValueError("R2 STARTED ref differs from authority binding")

    _spec, pairs = load_verified_official_pairs(args.cache, args.spec)
    examples = target_blind_visible_examples(pairs)
    assert_visible_envelope_target_blind(examples)
    source_map, source_map_sha256 = write_atomic_idx_source_map_no_clobber(
        args.source_map, pairs
    )
    if len(source_map) != 1744:
        raise ValueError("R2 target-free source map inventory drift")

    records: list[dict[str, Any]] = []
    with network_blocked():
        for row in expected_r2_rows():
            for emitted in state_tracker_executor(row, examples):
                metadata = emitted.get("metadata")
                if not isinstance(metadata, Mapping):
                    raise ValueError("R2 emitted metadata missing")
                record_id = emitted.get("record_id")
                if not isinstance(record_id, str) or not record_id:
                    raise ValueError("R2 emitted record_id missing")
                records.append(
                    {
                        "protocol_id": PROTOCOL_ID,
                        "run_identity": IDENTITY,
                        "row_id": str(row["row_id"]),
                        "row_kind": str(row["row_kind"]),
                        "mechanism_id": str(row["mechanism_id"]),
                        "seed": int(row["seed"]),
                        "pair_index": int(emitted["pair_index"]),
                        "record_id_hash": hashlib.sha256(
                            record_id.encode("utf-8")
                        ).hexdigest(),
                        "source_index": int(emitted["source_index"]),
                        "step_index": int(metadata["final_step_index"]),
                        "prediction": emitted["prediction"],
                        "input_track": str(row["input_track"]),
                        "final_state": str(metadata["final_state"]),
                        "work_counters": dict(metadata["work_counters"]),
                    }
                )
    raw = RawBundleR2.from_records(records)
    _write_raw_jsonl_no_clobber(args.raw, raw)
    _write_json_no_clobber(
        args.manifest,
        {
            "schema_version": "1",
            "protocol_id": PROTOCOL_ID,
            "run_identity": IDENTITY,
            "evidence_analyst_commit": analyst_commit,
            "exact_package_commit": package_commit,
            "started_ref": args.started_ref,
            "raw_bundle_sha256": raw.sha256,
            "raw_record_count": len(raw.records),
            "row_count": len(expected_r2_rows()),
            "pairs_per_row": 1744,
            "atomic_idx_source_map_sha256": source_map_sha256,
            "target_fields_materialized": False,
        },
    )


def score_preserved(args: argparse.Namespace) -> None:
    package_commit = _require_sha(args.package_commit, "package_commit")
    analyst_commit = _require_sha(args.analyst_commit, "analyst_commit")
    preservation_commit = _require_sha(
        args.preservation_commit, "preservation_commit"
    )
    if _git_head() != package_commit:
        raise RuntimeError("R2 scoring must run from exact package commit")
    _validate_authority(
        analyst_commit=analyst_commit,
        package_commit=package_commit,
    )
    manifest = _read_json(args.manifest)
    if (
        manifest.get("protocol_id") != PROTOCOL_ID
        or manifest.get("run_identity") != IDENTITY
    ):
        raise ValueError("R2 preserved manifest identity/protocol mismatch")
    if manifest.get("exact_package_commit") != package_commit:
        raise ValueError("R2 preserved manifest package mismatch")
    if manifest.get("evidence_analyst_commit") != analyst_commit:
        raise ValueError("R2 preserved manifest Analyst mismatch")
    raw = _reconstruct_r2_raw(
        args.raw,
        str(manifest.get("raw_bundle_sha256", "")),
    )
    source_map = read_atomic_idx_source_map(
        args.source_map,
        expected_sha256=str(manifest.get("atomic_idx_source_map_sha256", "")),
    )

    v4_manifest = _read_json(args.v4_manifest)
    v4_raw = reconstruct_raw_jsonl_v4(
        args.v4_raw,
        expected_sha256=str(v4_manifest.get("raw_sha256", "")),
    )
    _spec, pairs = load_verified_official_pairs(args.cache, args.spec)
    evaluator_targets = evaluator_targets_after_preservation(pairs, v4_raw)
    with network_blocked():
        result = score_reduction(raw, v4_raw, evaluator_targets, source_map)

    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    for name in (
        "paired_reduction_statistics",
        "pair_iid_sensitivity_statistics",
        "r2_metrics_by_seed",
    ):
        _write_json_no_clobber(output / f"{name}.json", result[name])
    report = dict(result["report"])
    report.update(
        {
            "protocol_id": PROTOCOL_ID,
            "run_identity": IDENTITY,
            "evidence_analyst_commit": analyst_commit,
            "exact_package_commit": package_commit,
            "raw_preservation_commit": preservation_commit,
            "raw_bundle_sha256": raw.sha256,
            "atomic_idx_source_map_sha256": manifest[
                "atomic_idx_source_map_sha256"
            ],
            "v4_raw_sha256": v4_manifest["raw_sha256"],
        }
    )
    _write_json_no_clobber(output / "report.json", report)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C19-R2 authority-bound one-way runner"
    )
    sub = parser.add_subparsers(dest="phase", required=True)

    smoke = sub.add_parser("prestart-smoke")
    smoke.add_argument("--analyst-commit", required=True)
    smoke.add_argument("--package-commit")
    smoke.set_defaults(handler=prestart_smoke)

    acquire = sub.add_parser("acquire-raw")
    acquire.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    acquire.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    acquire.add_argument("--raw", type=Path, required=True)
    acquire.add_argument("--manifest", type=Path, required=True)
    acquire.add_argument("--source-map", type=Path, required=True)
    acquire.add_argument("--analyst-commit", required=True)
    acquire.add_argument("--package-commit", required=True)
    acquire.add_argument("--started-ref", required=True)
    acquire.set_defaults(handler=acquire_raw)

    score = sub.add_parser("score-preserved")
    score.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    score.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    score.add_argument("--raw", type=Path, required=True)
    score.add_argument("--manifest", type=Path, required=True)
    score.add_argument("--source-map", type=Path, required=True)
    score.add_argument("--v4-raw", type=Path, required=True)
    score.add_argument("--v4-manifest", type=Path, required=True)
    score.add_argument("--output", type=Path, required=True)
    score.add_argument("--analyst-commit", required=True)
    score.add_argument("--package-commit", required=True)
    score.add_argument("--preservation-commit", required=True)
    score.set_defaults(handler=score_preserved)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()

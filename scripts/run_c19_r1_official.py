"""Prepared C19-R1 runner.

This runner is intentionally inert until a future Evidence Analyst explicitly
authorizes one-way execution and a STARTED ref exists. The current pre-START
workflow never invokes it on official data.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.evaluation import network_blocked
from sparkbrain.v03_external_validation.c19_r1_io import (
    assert_visible_envelope_target_blind,
    evaluator_targets_after_preservation,
    load_verified_official_pairs,
    target_blind_visible_examples,
)
from sparkbrain.v03_external_validation.c19_r1_protocol import (
    OFFICIAL_PYTHON_IMPLEMENTATION,
    OFFICIAL_PYTHON_VERSION,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
    V4_PRESERVE_COMMIT,
    V4_RAW_SHA256,
)
from sparkbrain.v03_external_validation.c19_r1_revision_authority import (
    OFFICIAL_SCOPE,
    ExecutionAdmissionR1,
    R1AcquisitionHarness,
    RuntimeBoundary,
    reconstruct_raw_jsonl,
    write_raw_jsonl_no_clobber,
)
from sparkbrain.v03_external_validation.c19_r1_scoring import (
    assert_official_python_runtime,
    score_reduction,
)
from sparkbrain.v03_external_validation.c19_r1_source_map import (
    atomic_idx_clusters,
    read_atomic_idx_source_map,
    write_atomic_idx_source_map_no_clobber,
)
from sparkbrain.v03_external_validation.official_execution_v4 import reconstruct_raw_jsonl_v4

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "configs/external_validation/belief_r.json"
DEFAULT_CACHE = ROOT / "data/external/belief_r/test.csv"
SHA1 = re.compile(r"[0-9a-f]{40}")


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _require_sha(value: str, name: str) -> str:
    if SHA1.fullmatch(value) is None:
        raise ValueError(f"{name} must be a full 40-character Git SHA")
    return value


def _write_json_no_clobber(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        handle.write("\n")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def acquire_raw(args: argparse.Namespace) -> None:
    assert_official_python_runtime()
    package_commit = _require_sha(args.package_commit, "package_commit")
    analyst_commit = _require_sha(args.analyst_commit, "analyst_commit")
    if _git_head() != package_commit:
        raise RuntimeError("R1 official acquisition must run from exact package commit")
    if not args.started_ref.startswith("control/c19-r1-revision-authority-started-"):
        raise ValueError("R1 STARTED ref outside bound namespace")

    _spec, pairs = load_verified_official_pairs(args.cache, args.spec)
    examples = target_blind_visible_examples(pairs)
    assert_visible_envelope_target_blind(examples)
    admission = ExecutionAdmissionR1(
        scope=OFFICIAL_SCOPE,
        evidence_analyst_commit=analyst_commit,
        exact_package_commit=package_commit,
        started_ref=args.started_ref,
    )
    harness = R1AcquisitionHarness(boundary=RuntimeBoundary())
    with network_blocked():
        raw = harness.acquire(admission=admission, examples=examples)
    write_raw_jsonl_no_clobber(args.raw, raw)
    source_map, source_map_sha256 = write_atomic_idx_source_map_no_clobber(
        args.atomic_idx_map,
        pairs,
    )
    _write_json_no_clobber(
        args.manifest,
        {
            "schema_version": "1",
            "protocol_id": PROTOCOL_ID,
            "run_identity": PLANNED_IDENTITY,
            "evidence_analyst_commit": analyst_commit,
            "exact_package_commit": package_commit,
            "started_ref": args.started_ref,
            "raw_sha256": raw.sha256,
            "raw_record_count": len(raw.records),
            "atomic_idx_source_map_sha256": source_map_sha256,
            "atomic_idx_source_map_entries": len(source_map),
            "atomic_idx_source_map_clusters": len(atomic_idx_clusters(source_map)),
            "atomic_idx_source_map_target_free": True,
            "target_fields_materialized": False,
            "runtime": {
                "python_implementation": OFFICIAL_PYTHON_IMPLEMENTATION,
                "python_version": OFFICIAL_PYTHON_VERSION,
                "network_allowed": False,
                "official_fit_tune_select_allowed": False,
            },
        },
    )


def score_preserved(args: argparse.Namespace) -> None:
    assert_official_python_runtime()
    package_commit = _require_sha(args.package_commit, "package_commit")
    analyst_commit = _require_sha(args.analyst_commit, "analyst_commit")
    r1_preservation_commit = _require_sha(args.r1_preservation_commit, "r1_preservation_commit")
    v4_preservation_commit = _require_sha(args.v4_preservation_commit, "v4_preservation_commit")
    if _git_head() != package_commit:
        raise RuntimeError("R1 scoring must run from exact package commit")
    if v4_preservation_commit != V4_PRESERVE_COMMIT:
        raise ValueError("R1 scorer v4 preservation binding drift")

    manifest = _read_json(args.manifest)
    if manifest.get("protocol_id") != PROTOCOL_ID:
        raise ValueError("R1 raw manifest protocol drift")
    if manifest.get("run_identity") != PLANNED_IDENTITY:
        raise ValueError("R1 raw manifest identity drift")
    if manifest.get("exact_package_commit") != package_commit:
        raise ValueError("R1 raw manifest package drift")
    if manifest.get("evidence_analyst_commit") != analyst_commit:
        raise ValueError("R1 raw manifest Analyst authority drift")
    if manifest.get("atomic_idx_source_map_target_free") is not True:
        raise ValueError("R1 source-map target-free manifest binding drift")

    r1_raw = reconstruct_raw_jsonl(
        args.raw,
        expected_sha256=str(manifest.get("raw_sha256", "")),
    )
    source_map = read_atomic_idx_source_map(
        args.atomic_idx_map,
        expected_sha256=str(manifest.get("atomic_idx_source_map_sha256", "")),
    )
    if manifest.get("atomic_idx_source_map_entries") != len(source_map):
        raise ValueError("R1 source-map entry count drift")
    if manifest.get("atomic_idx_source_map_clusters") != len(atomic_idx_clusters(source_map)):
        raise ValueError("R1 source-map cluster count drift")
    v4_raw = reconstruct_raw_jsonl_v4(args.v4_raw, expected_sha256=V4_RAW_SHA256)

    _spec, pairs = load_verified_official_pairs(args.cache, args.spec)
    targets = evaluator_targets_after_preservation(pairs, r1_raw)
    with network_blocked():
        result = score_reduction(r1_raw, v4_raw, targets, source_map)
    report = dict(result["report"])
    report.update(
        {
            "protocol_id": PROTOCOL_ID,
            "run_identity": PLANNED_IDENTITY,
            "evidence_analyst_commit": analyst_commit,
            "exact_package_commit": package_commit,
            "r1_raw_preservation_commit": r1_preservation_commit,
            "v4_raw_preservation_commit": v4_preservation_commit,
            "v4_raw_sha256": V4_RAW_SHA256,
            "r1_raw_sha256": r1_raw.sha256,
            "atomic_idx_source_map_sha256": manifest["atomic_idx_source_map_sha256"],
            "atomic_idx_source_map_clusters": len(atomic_idx_clusters(source_map)),
        }
    )
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    _write_json_no_clobber(
        output / "paired_reduction_statistics.json",
        result["paired_reduction_statistics"],
    )
    _write_json_no_clobber(
        output / "pair_iid_sensitivity_statistics.json",
        result["pair_iid_sensitivity_statistics"],
    )
    _write_json_no_clobber(output / "r1_metrics_by_seed.json", result["r1_metrics_by_seed"])
    _write_json_no_clobber(output / "report.json", report)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="C19-R1 matched reduction runner")
    sub = parser.add_subparsers(dest="phase", required=True)
    acquire = sub.add_parser("acquire-raw")
    acquire.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    acquire.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    acquire.add_argument("--raw", type=Path, required=True)
    acquire.add_argument("--atomic-idx-map", type=Path, required=True)
    acquire.add_argument("--manifest", type=Path, required=True)
    acquire.add_argument("--analyst-commit", required=True)
    acquire.add_argument("--package-commit", required=True)
    acquire.add_argument("--started-ref", required=True)
    acquire.set_defaults(handler=acquire_raw)

    score = sub.add_parser("score-preserved")
    score.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    score.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    score.add_argument("--raw", type=Path, required=True)
    score.add_argument("--atomic-idx-map", type=Path, required=True)
    score.add_argument("--manifest", type=Path, required=True)
    score.add_argument("--v4-raw", type=Path, required=True)
    score.add_argument("--output", type=Path, required=True)
    score.add_argument("--analyst-commit", required=True)
    score.add_argument("--package-commit", required=True)
    score.add_argument("--r1-preservation-commit", required=True)
    score.add_argument("--v4-preservation-commit", required=True)
    score.set_defaults(handler=score_preserved)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from sparkbrain.external_validation.evaluation import network_blocked
from sparkbrain.v03_external_validation import official_execution as inherited
from sparkbrain.v03_external_validation.implementation_binding import (
    baseline_registry,
    condition_executor,
)
from sparkbrain.v03_external_validation.official_execution_v4 import (
    OFFICIAL_SCOPE,
    ExecutionAdmissionV4,
    OneWayExecutionHarnessV4,
    reconstruct_raw_jsonl_v4,
    runtime_manifest_v4,
    write_raw_jsonl_no_clobber_v4,
)
from sparkbrain.v03_external_validation.official_io_v4 import (
    assert_visible_envelope_target_blind,
    evaluator_targets_after_preservation,
    load_verified_official_pairs,
    target_blind_visible_examples,
)
from sparkbrain.v03_external_validation.official_protocol_v4 import (
    PLANNED_IDENTITY,
    PROTOCOL_ID,
)
from sparkbrain.v03_external_validation.official_scoring_v4 import (
    assert_official_python_runtime,
    score_official_v4,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "configs/external_validation/belief_r.json"
DEFAULT_CACHE = ROOT / "data/external/belief_r/test.csv"
SHA1 = re.compile(r"[0-9a-f]{40}")


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _require_sha(value: str, name: str) -> str:
    if not SHA1.fullmatch(value):
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
        raise RuntimeError("official acquisition must run from the exact package commit")
    if not args.started_ref.startswith("control/c19-official-v4-started-"):
        raise ValueError("STARTED ref is outside the bound C19-v4 control namespace")

    _spec, pairs = load_verified_official_pairs(args.cache, args.spec)
    examples = target_blind_visible_examples(pairs)
    assert_visible_envelope_target_blind(examples)
    admission = ExecutionAdmissionV4(
        scope=OFFICIAL_SCOPE,
        evidence_analyst_commit=analyst_commit,
        exact_package_commit=package_commit,
        started_ref=args.started_ref,
    )
    harness = OneWayExecutionHarnessV4(boundary=inherited.RuntimeBoundary())
    with network_blocked():
        raw = harness.acquire(
            admission=admission,
            examples=examples,
            condition_executor=condition_executor,
            baseline_executors=baseline_registry(),
            raw_writer=lambda bundle: write_raw_jsonl_no_clobber_v4(args.raw, bundle),
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
            "row_count": 55,
            "pairs_per_row": 1744,
            "runtime": runtime_manifest_v4(),
            "target_fields_materialized": False,
        },
    )


def score_preserved(args: argparse.Namespace) -> None:
    assert_official_python_runtime()
    package_commit = _require_sha(args.package_commit, "package_commit")
    analyst_commit = _require_sha(args.analyst_commit, "analyst_commit")
    preservation_commit = _require_sha(args.preservation_commit, "preservation_commit")
    if _git_head() != package_commit:
        raise RuntimeError("official scoring must run from the exact package commit")
    manifest = _read_json(args.manifest)
    if manifest.get("protocol_id") != PROTOCOL_ID:
        raise ValueError("raw manifest protocol mismatch")
    if manifest.get("run_identity") != PLANNED_IDENTITY:
        raise ValueError("raw manifest identity mismatch")
    if manifest.get("exact_package_commit") != package_commit:
        raise ValueError("raw manifest package-commit mismatch")
    if manifest.get("evidence_analyst_commit") != analyst_commit:
        raise ValueError("raw manifest Analyst-authority mismatch")
    raw = reconstruct_raw_jsonl_v4(args.raw, expected_sha256=str(manifest.get("raw_sha256", "")))
    receipt = inherited.PreservationReceipt(
        raw_sha256=raw.sha256,
        preserve_ref=f"git-commit:{preservation_commit}",
        immutable=True,
    )
    receipt.validate_for(raw)  # type: ignore[arg-type]
    _spec, pairs = load_verified_official_pairs(args.cache, args.spec)
    evaluator_targets = evaluator_targets_after_preservation(pairs, raw)
    with network_blocked():
        result = score_official_v4(raw, evaluator_targets)
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    for name in (
        "scored_predictions",
        "metrics_by_row",
        "paired_statistics",
        "baseline_matching",
        "failure_examples",
    ):
        _write_json_no_clobber(output / f"{name}.json", result[name])
    report = dict(result["report"])
    report.update(
        {
            "protocol_id": PROTOCOL_ID,
            "run_identity": PLANNED_IDENTITY,
            "evidence_analyst_commit": analyst_commit,
            "exact_package_commit": package_commit,
            "raw_preservation_commit": preservation_commit,
            "raw_sha256": raw.sha256,
        }
    )
    _write_json_no_clobber(output / "report.json", report)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="C19 preservation-qualified official-v4 one-way runner"
    )
    subparsers = parser.add_subparsers(dest="phase", required=True)
    acquire = subparsers.add_parser("acquire-raw")
    acquire.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    acquire.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    acquire.add_argument("--raw", type=Path, required=True)
    acquire.add_argument("--manifest", type=Path, required=True)
    acquire.add_argument("--analyst-commit", required=True)
    acquire.add_argument("--package-commit", required=True)
    acquire.add_argument("--started-ref", required=True)
    acquire.set_defaults(handler=acquire_raw)
    score = subparsers.add_parser("score-preserved")
    score.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    score.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    score.add_argument("--raw", type=Path, required=True)
    score.add_argument("--manifest", type=Path, required=True)
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

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
from pathlib import Path
from typing import Any

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from .v06_confirmatory_current_manifest import build_current_confirmatory_manifest
from .v06_confirmatory_external_verification_v2 import (
    load_external_freeze_bundle_v2,
)
from .v06_confirmatory_freeze_bundle_v2 import ExternalFreezeBundleV2
from .v06_confirmatory_scoring import score_strict_confirmatory_results
from .v06_confirmatory_verify_external_raw_v2 import (
    VerifiedExternalRawEvidenceV2,
    verify_external_raw_evidence_v2,
)

_ANALYSIS_VERSION = "v06-external-analysis-2"


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _write_file(path: Path, value: object) -> None:
    payload = (_canonical_json(value) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_results(raw: VerifiedExternalRawEvidenceV2) -> tuple[ConfirmatoryResultRecord, ...]:
    path = Path(raw.raw_root) / "results.jsonl"
    rows = tuple(
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    records = tuple(
        ConfirmatoryResultRecord(
            family_id=str(row["family_id"]),
            seed=int(row["seed"]),
            condition=ConfirmatoryCondition(row["condition"]),
            evidence_domain=EvidenceDomain(row["evidence_domain"]),
            passed=bool(row["passed"]),
            metrics=tuple(
                sorted(
                    (str(key), float(value))
                    for key, value in dict(row["metrics"]).items()
                )
            ),
        )
        for row in rows
    )
    if len(records) != raw.evidence_record_count:
        raise RuntimeError("raw result count changed after verification")
    return records


def _resource_description(raw: VerifiedExternalRawEvidenceV2) -> dict[str, Any]:
    path = Path(raw.raw_root) / "resources.jsonl"
    rows = tuple(
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    by_condition: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        normalized = dict(row["normalized"])
        by_condition.setdefault(str(normalized["condition"]), []).append(normalized)
    summary: dict[str, Any] = {}
    for condition, condition_rows in sorted(by_condition.items()):
        summary[condition] = {
            "execution_count": len(condition_rows),
            "median_canonical_execution_bytes": statistics.median(
                row["common_canonical_execution_bytes"] for row in condition_rows
            ),
            "median_peak_traced_memory_bytes": statistics.median(
                row["common_peak_traced_memory_bytes"] for row in condition_rows
            ),
            "median_process_cpu_ns": statistics.median(
                row["common_process_cpu_ns"] for row in condition_rows
            ),
            "median_wall_clock_ns": statistics.median(
                row["common_wall_clock_ns"] for row in condition_rows
            ),
            "total_adapter_generated_internal_events_proxy": sum(
                row["adapter_generated_internal_events_proxy"]
                for row in condition_rows
            ),
            "total_adapter_observed_external_events_proxy": sum(
                row["adapter_observed_external_events_proxy"]
                for row in condition_rows
            ),
        }
    return {
        "decision_use": "descriptive-only",
        "efficiency_affects_capability_pass_fail": False,
        "per_condition": summary,
        "record_count": len(rows),
    }


def _commit_analysis(
    bundle: ExternalFreezeBundleV2,
    raw: VerifiedExternalRawEvidenceV2,
    *,
    outcome: dict[str, Any],
    resource_description: dict[str, Any],
) -> Path:
    analysis_root = Path(bundle.artifact_layout["analysis_root"])
    analysis_root.mkdir(parents=True, exist_ok=True)
    analysis_id = f"analysis-{raw.raw_tree_hash[:20]}"
    staging = analysis_root / f".{analysis_id}.tmp"
    final = analysis_root / analysis_id
    if staging.exists() or final.exists():
        raise FileExistsError("analysis identity already exists")
    staging.mkdir()
    _write_file(staging / "outcome.json", outcome)
    _write_file(staging / "resource_description.json", resource_description)
    _write_file(staging / "raw_verification.json", raw.state_dict())
    analysis_manifest = {
        "analysis_version": _ANALYSIS_VERSION,
        "bundle_hash": bundle.bundle_hash(),
        "raw_tree_hash": raw.raw_tree_hash,
        "resource_decision_use": "descriptive-only",
        "scoring_command_hash": bundle.scoring_command_hash,
        "source_git_sha": bundle.source_git_sha,
    }
    _write_file(staging / "analysis_manifest.json", analysis_manifest)
    checksums = {
        name: _file_hash(staging / name)
        for name in (
            "analysis_manifest.json",
            "outcome.json",
            "raw_verification.json",
            "resource_description.json",
        )
    }
    _write_file(staging / "checksums.json", checksums)
    _write_file(
        staging / "ANALYSIS_COMPLETE",
        {
            "analysis_id": analysis_id,
            "raw_tree_hash": raw.raw_tree_hash,
            "state": "ANALYSIS_COMPLETE",
        },
    )
    descriptor = os.open(staging, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.replace(staging, final)
    return final


def score_external_raw_v2(bundle: ExternalFreezeBundleV2) -> Path:
    """Verify immutable raw evidence first, then invoke the frozen scorer."""

    bundle.validate_for_execution()
    raw_before = verify_external_raw_evidence_v2(bundle)
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY,
        code_ref=bundle.source_git_sha,
    )
    if manifest.manifest_hash() != bundle.manifest_hash:
        raise RuntimeError("current manifest differs from frozen bundle")
    records = _load_results(raw_before)
    outcome = score_strict_confirmatory_results(manifest, records)
    resources = _resource_description(raw_before)
    raw_after = verify_external_raw_evidence_v2(bundle)
    if raw_after.raw_tree_hash != raw_before.raw_tree_hash:
        raise RuntimeError("raw evidence changed during scoring")
    final = _commit_analysis(
        bundle,
        raw_before,
        outcome=outcome.state_dict(),
        resource_description=resources,
    )
    raw_final = verify_external_raw_evidence_v2(bundle)
    if raw_final.raw_tree_hash != raw_before.raw_tree_hash:
        raise RuntimeError("raw evidence changed after analysis commit")
    return final


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify immutable raw evidence and apply the preregistered scorer.",
    )
    parser.add_argument("--freeze-bundle", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--analysis-root", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    bundle = load_external_freeze_bundle_v2(args.freeze_bundle)
    if args.raw_root.expanduser().resolve(strict=False) != Path(
        bundle.artifact_layout["raw_root"]
    ):
        raise RuntimeError("CLI raw root differs from frozen bundle")
    if args.analysis_root.expanduser().resolve(strict=False) != Path(
        bundle.artifact_layout["analysis_root"]
    ):
        raise RuntimeError("CLI analysis root differs from frozen bundle")
    final = score_external_raw_v2(bundle)
    print(
        json.dumps(
            {"analysis_root": str(final), "state": "ANALYSIS_COMPLETE"},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

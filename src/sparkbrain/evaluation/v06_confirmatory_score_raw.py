from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import fmean, median
from typing import Any

from .v06_confirmatory import ConfirmatoryCondition, ConfirmatoryManifest
from .v06_confirmatory_analysis_contract import (
    ANALYSIS_CONTRACT_VERSION,
    analysis_contract_hash,
)
from .v06_confirmatory_candidate_manifest import build_candidate_manifest
from .v06_confirmatory_environment import (
    environment_lock_from_state,
    require_environment_lock,
)
from .v06_confirmatory_execution_seal import (
    ConfirmatoryFreezeRecord,
    freeze_record_from_state,
    require_execution_seal,
)
from .v06_confirmatory_launch_gate import inspect_git_workspace
from .v06_confirmatory_raw_evidence import (
    VerifiedRawEvidence,
    load_verified_raw_evidence,
)
from .v06_confirmatory_resource_accounting import (
    RESOURCE_POLICY,
    ResourceDecisionUse,
    resource_policy_hash,
)
from .v06_confirmatory_scoring import (
    StrictConfirmatoryOutcome,
    score_strict_confirmatory_results,
)


def _canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _write_exclusive(path: Path, value: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _make_read_only(path: Path) -> None:
    for child in sorted(path.rglob("*"), reverse=True):
        if child.is_file():
            child.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif child.is_dir():
            child.chmod(0o555)
    path.chmod(0o555)


@dataclass(frozen=True, slots=True)
class AnalysisReceipt:
    run_id: str
    analysis_directory: str
    raw_manifest_hash: str
    raw_checksums_hash: str
    summary_hash: str
    analysis_checksums_hash: str
    raw_unchanged_after_scoring: bool
    immutable_permissions_applied: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _distribution(values: list[int]) -> dict[str, float | int]:
    if not values:
        raise ValueError("resource distribution cannot be empty")
    return {
        "maximum": max(values),
        "mean": fmean(values),
        "median": median(values),
        "minimum": min(values),
        "sum": sum(values),
    }


def _resource_summary(evidence: VerifiedRawEvidence) -> dict[str, Any]:
    grouped: defaultdict[ConfirmatoryCondition, list[Any]] = defaultdict(list)
    for record in evidence.normalized_resources:
        grouped[record.condition].append(record)
    summary: dict[str, Any] = {}
    for condition in ConfirmatoryCondition:
        rows = grouped[condition]
        summary[condition.value] = {
            "architecture_specific": {
                "explicit_assembly_entries": _distribution(
                    [row.explicit_assembly_entries for row in rows]
                ),
                "normal_field_threshold_crossings": _distribution(
                    [row.normal_field_threshold_crossings for row in rows]
                ),
                "privileged_information_count": _distribution(
                    [row.privileged_information_count for row in rows]
                ),
                "scalar_reward_observations": _distribution(
                    [row.scalar_reward_observations for row in rows]
                ),
                "typed_head_count": _distribution(
                    [row.typed_head_count for row in rows]
                ),
            },
            "common_evaluator_measurements": {
                "canonical_output_bytes": _distribution(
                    [row.canonical_output_bytes for row in rows]
                ),
                "peak_traced_memory_bytes": _distribution(
                    [row.peak_traced_memory_bytes for row in rows]
                ),
                "process_cpu_ns": _distribution(
                    [row.process_cpu_ns for row in rows]
                ),
                "wall_clock_ns": _distribution(
                    [row.wall_clock_ns for row in rows]
                ),
            },
            "descriptive_adapter_proxies": {
                "adapter_generated_event_proxy": _distribution(
                    [row.adapter_generated_event_proxy for row in rows]
                ),
                "adapter_intervention_event_proxy": _distribution(
                    [row.adapter_intervention_event_proxy for row in rows]
                ),
                "adapter_logical_operation_proxy_units": _distribution(
                    [row.adapter_logical_operation_proxy_units for row in rows]
                ),
                "adapter_mutable_state_scalar_proxy": _distribution(
                    [row.adapter_mutable_state_scalar_proxy for row in rows]
                ),
                "adapter_observed_training_event_proxy": _distribution(
                    [row.adapter_observed_training_event_proxy for row in rows]
                ),
                "adapter_persistent_state_entry_proxy": _distribution(
                    [row.adapter_persistent_state_entry_proxy for row in rows]
                ),
            },
            "execution_count": len(rows),
            "resource_decision_use": ResourceDecisionUse.DESCRIPTIVE_ONLY.value,
            "threshold_bypassed": all(row.threshold_bypassed for row in rows),
        }
    return summary


def _failure_rows(evidence: VerifiedRawEvidence) -> list[dict[str, Any]]:
    return [
        {
            "condition": row.condition.value,
            "evidence_domain": row.evidence_domain.value,
            "family_id": row.family_id,
            "metrics": dict(row.metrics),
            "seed": row.seed,
        }
        for row in evidence.results
        if not row.passed
    ]


def build_analysis_summary(
    evidence: VerifiedRawEvidence,
    manifest: ConfirmatoryManifest,
    freeze_record: ConfirmatoryFreezeRecord,
) -> tuple[dict[str, Any], StrictConfirmatoryOutcome]:
    evidence.validate(manifest)
    RESOURCE_POLICY.validate()
    outcome = score_strict_confirmatory_results(manifest, evidence.results)
    summary = {
        "analysis_contract_hash": analysis_contract_hash(),
        "analysis_contract_version": ANALYSIS_CONTRACT_VERSION,
        "capability_outcome": outcome.state_dict(),
        "failure_records": _failure_rows(evidence),
        "freeze_seal_hash": freeze_record.seal_hash(),
        "manifest_hash": manifest.manifest_hash(),
        "raw_evidence": evidence.state_dict(),
        "resource_accounting": {
            "affects_capability_result": False,
            "decision_use": ResourceDecisionUse.DESCRIPTIVE_ONLY.value,
            "per_condition": _resource_summary(evidence),
            "policy_hash": resource_policy_hash(),
        },
        "source_code_sha": freeze_record.source_code_sha,
    }
    return summary, outcome


def _raw_matches(
    evidence: VerifiedRawEvidence,
    *,
    manifest: ConfirmatoryManifest,
    freeze_record: ConfirmatoryFreezeRecord,
) -> bool:
    verified = load_verified_raw_evidence(
        Path(evidence.raw_directory),
        manifest=manifest,
        freeze_record=freeze_record,
    )
    return (
        verified.receipt.raw_manifest_hash == evidence.receipt.raw_manifest_hash
        and verified.receipt.run_checksums_hash
        == evidence.receipt.run_checksums_hash
    )


def write_analysis_transaction(
    *,
    output_root: Path,
    evidence: VerifiedRawEvidence,
    manifest: ConfirmatoryManifest,
    freeze_record: ConfirmatoryFreezeRecord,
) -> AnalysisReceipt:
    """Write analysis only after raw verification; never modify raw evidence."""

    raw_manifest_before = evidence.receipt.raw_manifest_hash
    raw_checksums_before = evidence.receipt.run_checksums_hash
    summary, _ = build_analysis_summary(evidence, manifest, freeze_record)

    analysis_root = output_root / "analysis"
    staging_root = output_root / ".analysis-staging"
    final_directory = analysis_root / evidence.run_id
    if final_directory.exists():
        raise FileExistsError(final_directory)
    analysis_root.mkdir(parents=True, exist_ok=True)
    staging_root.mkdir(parents=True, exist_ok=True)
    transaction = Path(
        tempfile.mkdtemp(
            prefix=f"{evidence.run_id}.",
            dir=staging_root,
        )
    )
    try:
        summary_bytes = _canonical_json_bytes(summary)
        _write_exclusive(transaction / "summary.json", summary_bytes)
        checksums = {
            "summary.json": hashlib.sha256(summary_bytes).hexdigest(),
        }
        _write_exclusive(
            transaction / "checksums.json",
            _canonical_json_bytes(
                {
                    "algorithm": "sha256",
                    "files": checksums,
                    "raw_checksums_hash": raw_checksums_before,
                    "raw_manifest_hash": raw_manifest_before,
                }
            ),
        )
        _write_exclusive(
            transaction / "ANALYSIS_COMPLETE",
            _canonical_json_bytes(
                {
                    "raw_run_id": evidence.run_id,
                    "summary_hash": checksums["summary.json"],
                }
            ),
        )
        _fsync_directory(transaction)
        if not _raw_matches(
            evidence,
            manifest=manifest,
            freeze_record=freeze_record,
        ):
            raise RuntimeError("raw evidence changed before analysis commit")
        os.rename(transaction, final_directory)
        _fsync_directory(analysis_root)
    except BaseException:
        shutil.rmtree(transaction, ignore_errors=True)
        raise

    if not _raw_matches(
        evidence,
        manifest=manifest,
        freeze_record=freeze_record,
    ):
        shutil.rmtree(final_directory, ignore_errors=True)
        raise RuntimeError("raw evidence changed during scoring")
    _make_read_only(final_directory)
    return AnalysisReceipt(
        run_id=evidence.run_id,
        analysis_directory=str(final_directory),
        raw_manifest_hash=raw_manifest_before,
        raw_checksums_hash=raw_checksums_before,
        summary_hash=_sha256_file(final_directory / "summary.json"),
        analysis_checksums_hash=_sha256_file(
            final_directory / "checksums.json"
        ),
        raw_unchanged_after_scoring=True,
        immutable_permissions_applied=not bool(
            final_directory.stat().st_mode & stat.S_IWUSR
        ),
    )


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def score_raw_cli(
    *,
    repository_root: Path,
    freeze_record_path: Path,
    environment_lock_path: Path,
    raw_directory: Path,
    output_root: Path,
) -> AnalysisReceipt:
    freeze_record = freeze_record_from_state(_read_json(freeze_record_path))
    environment = environment_lock_from_state(_read_json(environment_lock_path))
    manifest = build_candidate_manifest(
        source_code_sha=freeze_record.source_code_sha
    )
    workspace = inspect_git_workspace(repository_root)
    if not workspace.clean or workspace.head_sha != freeze_record.source_code_sha:
        raise RuntimeError("scoring must use the frozen source checkout")
    require_environment_lock(environment)
    require_execution_seal(
        manifest,
        freeze_record,
        repository_root=repository_root,
        environment_lock=environment,
    )
    evidence = load_verified_raw_evidence(
        raw_directory,
        manifest=manifest,
        freeze_record=freeze_record,
    )
    return write_analysis_transaction(
        output_root=output_root,
        evidence=evidence,
        manifest=manifest,
        freeze_record=freeze_record,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score one immutable SparkBrain v0.6 raw confirmatory run."
    )
    parser.add_argument("--freeze-record", type=Path, required=True)
    parser.add_argument("--environment-lock", type=Path, required=True)
    parser.add_argument("--raw-directory", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    receipt = score_raw_cli(
        repository_root=arguments.repository_root,
        freeze_record_path=arguments.freeze_record,
        environment_lock_path=arguments.environment_lock,
        raw_directory=arguments.raw_directory,
        output_root=arguments.output_root,
    )
    print(json.dumps(receipt.state_dict(), sort_keys=True))


if __name__ == "__main__":
    main()

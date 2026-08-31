from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from .v06_confirmatory_artifacts import RawRunReceipt, verify_raw_run
from .v06_confirmatory_resource_accounting import (
    NormalizedConditionResourceRecord,
    ResourceDecisionUse,
    assess_normalized_resource_matrix,
)
from .v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
    assess_resource_matrix,
)
from .v06_confirmatory_scoring import (
    StrictConfirmatoryOutcome,
    score_strict_confirmatory_results,
)

SCORER_CONTRACT_VERSION = "v06-locked-scorer-1"


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _result_from_state(state: dict[str, Any]) -> ConfirmatoryResultRecord:
    return ConfirmatoryResultRecord(
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        evidence_domain=EvidenceDomain(str(state["evidence_domain"])),
        passed=bool(state["passed"]),
        metrics=tuple(
            sorted(
                (str(key), float(value))
                for key, value in dict(state.get("metrics", {})).items()
            )
        ),
    )


def _raw_resource_from_state(state: dict[str, Any]) -> ConditionResourceRecord:
    value = ConditionResourceRecord(
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        observed_training_events=int(state["observed_training_events"]),
        generated_internal_events=int(state["generated_internal_events"]),
        persistent_state_entries=int(state["persistent_state_entries"]),
        intervention_count=int(state["intervention_count"]),
        parameter_count=int(state["parameter_count"]),
        wall_clock_ms=float(state["wall_clock_ms"]),
        normal_field_threshold_present=bool(
            state["normal_field_threshold_present"]
        ),
        normal_field_threshold_crossings=int(
            state["normal_field_threshold_crossings"]
        ),
        threshold_bypassed=bool(state["threshold_bypassed"]),
        explicit_assembly_entries=int(state["explicit_assembly_entries"]),
        typed_head_count=int(state["typed_head_count"]),
        scalar_reward_observations=int(state["scalar_reward_observations"]),
        privileged_information=tuple(
            PrivilegedInformation(str(row))
            for row in state.get("privileged_information", [])
        ),
    )
    value.validate()
    return value


def _normalized_resource_from_state(
    state: dict[str, Any],
) -> NormalizedConditionResourceRecord:
    value = NormalizedConditionResourceRecord(
        family_id=str(state["family_id"]),
        seed=int(state["seed"]),
        condition=ConfirmatoryCondition(str(state["condition"])),
        accounting_version=str(state["accounting_version"]),
        decision_use=ResourceDecisionUse(str(state["decision_use"])),
        observed_external_events=int(state["observed_external_events"]),
        logical_generated_events=int(state["logical_generated_events"]),
        intervention_events=int(state["intervention_events"]),
        mutable_state_scalar_proxy=int(state["mutable_state_scalar_proxy"]),
        persistent_state_entry_proxy=int(state["persistent_state_entry_proxy"]),
        logical_operation_proxy_units=int(state["logical_operation_proxy_units"]),
        wall_clock_ns=int(state["wall_clock_ns"]),
        process_cpu_ns=int(state["process_cpu_ns"]),
        peak_traced_memory_bytes=int(state["peak_traced_memory_bytes"]),
        canonical_output_bytes=int(state["canonical_output_bytes"]),
        normal_field_threshold_present=bool(
            state["normal_field_threshold_present"]
        ),
        normal_field_threshold_crossings=int(
            state["normal_field_threshold_crossings"]
        ),
        threshold_bypassed=bool(state["threshold_bypassed"]),
        explicit_assembly_entries=int(state["explicit_assembly_entries"]),
        typed_head_count=int(state["typed_head_count"]),
        scalar_reward_observations=int(state["scalar_reward_observations"]),
        privileged_information_count=int(state["privileged_information_count"]),
    )
    value.validate()
    return value


@dataclass(frozen=True, slots=True)
class LockedRawEvidence:
    receipt: RawRunReceipt
    records: tuple[ConfirmatoryResultRecord, ...]
    raw_resources: tuple[ConditionResourceRecord, ...]
    normalized_resources: tuple[NormalizedConditionResourceRecord, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "normalized_resource_count": len(self.normalized_resources),
            "raw_resource_count": len(self.raw_resources),
            "receipt": self.receipt.state_dict(),
            "result_record_count": len(self.records),
        }


@dataclass(frozen=True, slots=True)
class LockedScoringSummary:
    scorer_contract_version: str
    analysis_id: str
    raw_manifest_hash: str
    run_checksums_hash: str
    manifest_hash: str
    result_record_count: int
    raw_resource_count: int
    normalized_resource_count: int
    resource_decision_use: str
    outcome: StrictConfirmatoryOutcome

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "outcome": self.outcome.state_dict(),
        }


def load_locked_raw_evidence(path: Path) -> LockedRawEvidence:
    receipt = verify_raw_run(path)
    if not receipt.immutable_permissions_applied:
        raise RuntimeError("raw run must be read-only before scoring")
    records: list[ConfirmatoryResultRecord] = []
    raw_resources: list[ConditionResourceRecord] = []
    normalized_resources: list[NormalizedConditionResourceRecord] = []
    for execution_directory in sorted(path.joinpath("executions").iterdir()):
        if not execution_directory.is_dir():
            continue
        records.extend(
            _result_from_state(json.loads(line))
            for line in execution_directory.joinpath("results.jsonl")
            .read_text("utf-8")
            .splitlines()
            if line.strip()
        )
        raw_resources.append(
            _raw_resource_from_state(
                json.loads(
                    execution_directory.joinpath("raw_resource.json").read_text(
                        "utf-8"
                    )
                )
            )
        )
        normalized_resources.append(
            _normalized_resource_from_state(
                json.loads(
                    execution_directory.joinpath(
                        "normalized_resource.json"
                    ).read_text("utf-8")
                )
            )
        )
    if len(records) != receipt.result_record_count:
        raise RuntimeError("locked raw result count changed after verification")
    if len(raw_resources) != receipt.raw_resource_count:
        raise RuntimeError("locked raw resource count changed after verification")
    if len(normalized_resources) != receipt.normalized_resource_count:
        raise RuntimeError("locked normalized resource count changed after verification")
    return LockedRawEvidence(
        receipt=receipt,
        records=tuple(records),
        raw_resources=tuple(raw_resources),
        normalized_resources=tuple(normalized_resources),
    )


def score_locked_raw_run(
    path: Path,
    manifest: ConfirmatoryManifest,
) -> LockedScoringSummary:
    evidence = load_locked_raw_evidence(path)
    raw_coverage = assess_resource_matrix(manifest, evidence.raw_resources)
    normalized_coverage = assess_normalized_resource_matrix(
        manifest,
        evidence.normalized_resources,
    )
    if not raw_coverage.complete:
        raise RuntimeError("locked raw resource matrix is incomplete")
    if not normalized_coverage.complete:
        raise RuntimeError("locked normalized resource matrix is incomplete")
    outcome = score_strict_confirmatory_results(manifest, evidence.records)
    analysis_id = digest(
        {
            "manifest_hash": manifest.manifest_hash(),
            "raw_manifest_hash": evidence.receipt.raw_manifest_hash,
            "run_checksums_hash": evidence.receipt.run_checksums_hash,
            "scorer_contract_version": SCORER_CONTRACT_VERSION,
        }
    )
    return LockedScoringSummary(
        scorer_contract_version=SCORER_CONTRACT_VERSION,
        analysis_id=analysis_id,
        raw_manifest_hash=evidence.receipt.raw_manifest_hash,
        run_checksums_hash=evidence.receipt.run_checksums_hash,
        manifest_hash=manifest.manifest_hash(),
        result_record_count=len(evidence.records),
        raw_resource_count=len(evidence.raw_resources),
        normalized_resource_count=len(evidence.normalized_resources),
        resource_decision_use=ResourceDecisionUse.DESCRIPTIVE_ONLY.value,
        outcome=outcome,
    )


def write_analysis_summary_atomic(
    analysis_root: Path,
    summary: LockedScoringSummary,
) -> Path:
    analysis_root.mkdir(parents=True, exist_ok=True)
    final_directory = analysis_root / summary.analysis_id
    if final_directory.exists():
        existing = final_directory / "summary.json"
        if existing.is_file() and _sha256_file(existing) == _sha256_file(existing):
            raise FileExistsError(f"analysis already exists: {summary.analysis_id}")
        raise RuntimeError("analysis output collision")
    temporary = Path(
        tempfile.mkdtemp(prefix=f"{summary.analysis_id}.", dir=analysis_root)
    )
    try:
        summary_bytes = (_canonical_json(summary.state_dict()) + "\n").encode("utf-8")
        summary_path = temporary / "summary.json"
        with summary_path.open("xb") as stream:
            stream.write(summary_bytes)
            stream.flush()
            os.fsync(stream.fileno())
        checksums = {
            "algorithm": "sha256",
            "files": {"summary.json": _sha256_file(summary_path)},
        }
        checksum_path = temporary / "checksums.json"
        with checksum_path.open("xb") as stream:
            stream.write((_canonical_json(checksums) + "\n").encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
        os.rename(temporary, final_directory)
    except BaseException:
        if temporary.exists():
            for child in temporary.iterdir():
                child.unlink(missing_ok=True)
            temporary.rmdir()
        raise
    return final_directory

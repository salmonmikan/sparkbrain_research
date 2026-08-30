from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import (
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    assess_confirmatory_readiness,
)
from .v06_confirmatory_adapter_review import (
    adapter_source_inventory_hash,
    expected_privilege_inventory_hash,
    expected_threshold_mode_hash,
)
from .v06_confirmatory_analysis_contract import (
    analysis_contract_hash,
    scoring_command_hash,
)
from .v06_confirmatory_artifacts import artifact_contract_hash
from .v06_confirmatory_environment import (
    RNG_CONTRACT,
    ConfirmatoryEnvironmentLock,
)
from .v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    QUARANTINED_HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
    heldout_world_grid_hash,
)
from .v06_confirmatory_resource_accounting import (
    normalized_resource_schema_hash,
    raw_resource_schema_hash,
    resource_policy_hash,
)
from .v06_confirmatory_schedule_contract import training_schedule_grid_hash

_SOURCE_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_APPROVAL_PATTERN = re.compile(
    r"^APPROVED:[A-Za-z0-9_.@-]+:[0-9a-f]{16}$"
)
FREEZE_RECORD_VERSION = "v06-confirmatory-freeze-record-3"
SEAL_STORAGE_MODE = "external-or-later-commit-with-detached-source-checkout"
EXECUTION_COMMAND = (
    "python -m sparkbrain.evaluation.v06_confirmatory_execute "
    "--freeze-record control/freeze_record.json "
    "--environment-lock control/environment_lock.json "
    "--output-root artifacts/v06/confirmatory"
)
ARTIFACT_PATH_TEMPLATES = (
    "control/freeze_record.json",
    "control/environment_lock.json",
    "control/freeze_verification.json",
    "control/launch_report.json",
    "control/execution_state.json",
    "raw/<run_id>/raw_manifest.json",
    "raw/<run_id>/checksums.json",
    "raw/<run_id>/RAW_COMPLETE",
    "analysis/<run_id>/summary.json",
    "analysis/<run_id>/checksums.json",
    "analysis/<run_id>/ANALYSIS_COMPLETE",
)


def result_schema_hash() -> str:
    return digest(
        {
            "model": ConfirmatoryResultRecord.__name__,
            "fields": list(ConfirmatoryResultRecord.__dataclass_fields__),
        }
    )


def thresholds_hash(manifest: ConfirmatoryManifest) -> str:
    return digest(asdict(manifest.thresholds))


def exclusions_hash(manifest: ConfirmatoryManifest) -> str:
    return digest(list(manifest.exclusions))


def adapter_registration_hash(manifest: ConfirmatoryManifest) -> str:
    return digest(
        [
            {
                "adapter_path": row.adapter_path,
                "adapter_ready": row.adapter_ready,
                "condition": row.condition.value,
                "engineering_evidence_available": (
                    row.engineering_evidence_available
                ),
                "isolated_from_primary": row.isolated_from_primary,
            }
            for row in manifest.conditions
        ]
    )


def execution_command_hash() -> str:
    return digest(EXECUTION_COMMAND)


def artifact_path_hash() -> str:
    return digest(list(ARTIFACT_PATH_TEMPLATES))


@dataclass(frozen=True, slots=True)
class ConfirmatoryFreezeRecord:
    record_version: str
    seal_storage_mode: str
    source_code_sha: str
    manifest_hash: str
    world_generation_id: str
    world_grid_hash: str
    training_schedule_grid_hash: str
    thresholds_hash: str
    exclusions_hash: str
    result_schema_hash: str
    raw_resource_schema_hash: str
    normalized_resource_schema_hash: str
    resource_policy_hash: str
    adapter_registration_hash: str
    adapter_source_inventory_hash: str
    privilege_inventory_hash: str
    threshold_mode_hash: str
    artifact_contract_hash: str
    analysis_contract_hash: str
    execution_command_hash: str
    scoring_command_hash: str
    artifact_path_hash: str
    environment_lock_hash: str
    rng_contract_hash: str
    approval_id: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def seal_hash(self) -> str:
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ExecutionSealReport:
    manifest_ready: bool
    source_code_sha_matches: bool
    manifest_hash_matches: bool
    world_generation_matches: bool
    world_grid_matches: bool
    seeds_fresh_and_exact: bool
    training_schedule_matches: bool
    thresholds_match: bool
    exclusions_match: bool
    result_schema_matches: bool
    raw_resource_schema_matches: bool
    normalized_resource_schema_matches: bool
    resource_policy_matches: bool
    adapter_registration_matches: bool
    adapter_source_inventory_matches: bool
    privilege_inventory_matches: bool
    threshold_mode_matches: bool
    artifact_contract_matches: bool
    analysis_contract_matches: bool
    execution_command_matches: bool
    scoring_command_matches: bool
    artifact_paths_match: bool
    environment_lock_matches: bool
    rng_contract_matches: bool
    storage_mode_matches: bool
    approval_present: bool
    seal_hash: str
    execution_allowed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def freeze_record_from_state(
    state: dict[str, Any],
) -> ConfirmatoryFreezeRecord:
    record = ConfirmatoryFreezeRecord(
        record_version=str(state["record_version"]),
        seal_storage_mode=str(state["seal_storage_mode"]),
        source_code_sha=str(state["source_code_sha"]),
        manifest_hash=str(state["manifest_hash"]),
        world_generation_id=str(state["world_generation_id"]),
        world_grid_hash=str(state["world_grid_hash"]),
        training_schedule_grid_hash=str(state["training_schedule_grid_hash"]),
        thresholds_hash=str(state["thresholds_hash"]),
        exclusions_hash=str(state["exclusions_hash"]),
        result_schema_hash=str(state["result_schema_hash"]),
        raw_resource_schema_hash=str(state["raw_resource_schema_hash"]),
        normalized_resource_schema_hash=str(
            state["normalized_resource_schema_hash"]
        ),
        resource_policy_hash=str(state["resource_policy_hash"]),
        adapter_registration_hash=str(state["adapter_registration_hash"]),
        adapter_source_inventory_hash=str(
            state["adapter_source_inventory_hash"]
        ),
        privilege_inventory_hash=str(state["privilege_inventory_hash"]),
        threshold_mode_hash=str(state["threshold_mode_hash"]),
        artifact_contract_hash=str(state["artifact_contract_hash"]),
        analysis_contract_hash=str(state["analysis_contract_hash"]),
        execution_command_hash=str(state["execution_command_hash"]),
        scoring_command_hash=str(state["scoring_command_hash"]),
        artifact_path_hash=str(state["artifact_path_hash"]),
        environment_lock_hash=str(state["environment_lock_hash"]),
        rng_contract_hash=str(state["rng_contract_hash"]),
        approval_id=str(state["approval_id"]),
    )
    if set(record.state_dict()) != set(state):
        raise ValueError("freeze record contains missing or unexpected fields")
    return record


def build_freeze_record(
    manifest: ConfirmatoryManifest,
    *,
    source_code_sha: str,
    repository_root: Path,
    environment_lock: ConfirmatoryEnvironmentLock,
    approval_id: str,
) -> ConfirmatoryFreezeRecord:
    """Build an external seal for one detached source commit.

    The JSON seal is intentionally not required to live in ``source_code_sha``.
    A later seal commit or immutable artifact may carry it. The launcher must
    detached-checkout this source SHA and verify it before capability execution.
    """

    environment_lock.validate()
    return ConfirmatoryFreezeRecord(
        record_version=FREEZE_RECORD_VERSION,
        seal_storage_mode=SEAL_STORAGE_MODE,
        source_code_sha=source_code_sha,
        manifest_hash=manifest.manifest_hash(),
        world_generation_id=WORLD_GENERATION_ID,
        world_grid_hash=heldout_world_grid_hash(),
        training_schedule_grid_hash=training_schedule_grid_hash(),
        thresholds_hash=thresholds_hash(manifest),
        exclusions_hash=exclusions_hash(manifest),
        result_schema_hash=result_schema_hash(),
        raw_resource_schema_hash=raw_resource_schema_hash(),
        normalized_resource_schema_hash=normalized_resource_schema_hash(),
        resource_policy_hash=resource_policy_hash(),
        adapter_registration_hash=adapter_registration_hash(manifest),
        adapter_source_inventory_hash=adapter_source_inventory_hash(
            repository_root
        ),
        privilege_inventory_hash=expected_privilege_inventory_hash(),
        threshold_mode_hash=expected_threshold_mode_hash(),
        artifact_contract_hash=artifact_contract_hash(),
        analysis_contract_hash=analysis_contract_hash(),
        execution_command_hash=execution_command_hash(),
        scoring_command_hash=scoring_command_hash(),
        artifact_path_hash=artifact_path_hash(),
        environment_lock_hash=environment_lock.environment_hash(),
        rng_contract_hash=RNG_CONTRACT.contract_hash(),
        approval_id=approval_id,
    )


def validate_execution_seal(
    manifest: ConfirmatoryManifest,
    record: ConfirmatoryFreezeRecord,
    *,
    repository_root: Path,
    environment_lock: ConfirmatoryEnvironmentLock,
) -> ExecutionSealReport:
    """Validate every frozen protocol component without running capability."""

    readiness = assess_confirmatory_readiness(manifest)
    manifest_ready = (
        manifest.phase is ConfirmatoryPhase.CONFIRMATORY
        and readiness.ready
        and record.record_version == FREEZE_RECORD_VERSION
    )
    source_matches = (
        bool(_SOURCE_SHA_PATTERN.fullmatch(record.source_code_sha))
        and record.source_code_sha == manifest.code_ref
    )
    manifest_hash_matches = record.manifest_hash == manifest.manifest_hash()
    world_generation_matches = record.world_generation_id == WORLD_GENERATION_ID
    world_grid_matches = record.world_grid_hash == heldout_world_grid_hash()
    manifest_seed_values = tuple(row.seed for row in manifest.seeds)
    seeds_fresh_and_exact = (
        manifest_seed_values == HELDOUT_SEEDS
        and set(manifest_seed_values).isdisjoint(QUARANTINED_HELDOUT_SEEDS)
    )
    checks = {
        "training_schedule_matches": (
            record.training_schedule_grid_hash == training_schedule_grid_hash()
        ),
        "thresholds_match": record.thresholds_hash == thresholds_hash(manifest),
        "exclusions_match": record.exclusions_hash == exclusions_hash(manifest),
        "result_schema_matches": record.result_schema_hash == result_schema_hash(),
        "raw_resource_schema_matches": (
            record.raw_resource_schema_hash == raw_resource_schema_hash()
        ),
        "normalized_resource_schema_matches": (
            record.normalized_resource_schema_hash
            == normalized_resource_schema_hash()
        ),
        "resource_policy_matches": (
            record.resource_policy_hash == resource_policy_hash()
        ),
        "adapter_registration_matches": (
            record.adapter_registration_hash == adapter_registration_hash(manifest)
        ),
        "adapter_source_inventory_matches": (
            record.adapter_source_inventory_hash
            == adapter_source_inventory_hash(repository_root)
        ),
        "privilege_inventory_matches": (
            record.privilege_inventory_hash == expected_privilege_inventory_hash()
        ),
        "threshold_mode_matches": (
            record.threshold_mode_hash == expected_threshold_mode_hash()
        ),
        "artifact_contract_matches": (
            record.artifact_contract_hash == artifact_contract_hash()
        ),
        "analysis_contract_matches": (
            record.analysis_contract_hash == analysis_contract_hash()
        ),
        "execution_command_matches": (
            record.execution_command_hash == execution_command_hash()
        ),
        "scoring_command_matches": (
            record.scoring_command_hash == scoring_command_hash()
        ),
        "artifact_paths_match": record.artifact_path_hash == artifact_path_hash(),
        "environment_lock_matches": (
            record.environment_lock_hash == environment_lock.environment_hash()
        ),
        "rng_contract_matches": (
            record.rng_contract_hash == RNG_CONTRACT.contract_hash()
        ),
        "storage_mode_matches": record.seal_storage_mode == SEAL_STORAGE_MODE,
    }
    approval_present = bool(_APPROVAL_PATTERN.fullmatch(record.approval_id))
    execution_allowed = all(
        (
            manifest_ready,
            source_matches,
            manifest_hash_matches,
            world_generation_matches,
            world_grid_matches,
            seeds_fresh_and_exact,
            *checks.values(),
            approval_present,
        )
    )
    return ExecutionSealReport(
        manifest_ready=manifest_ready,
        source_code_sha_matches=source_matches,
        manifest_hash_matches=manifest_hash_matches,
        world_generation_matches=world_generation_matches,
        world_grid_matches=world_grid_matches,
        seeds_fresh_and_exact=seeds_fresh_and_exact,
        training_schedule_matches=checks["training_schedule_matches"],
        thresholds_match=checks["thresholds_match"],
        exclusions_match=checks["exclusions_match"],
        result_schema_matches=checks["result_schema_matches"],
        raw_resource_schema_matches=checks["raw_resource_schema_matches"],
        normalized_resource_schema_matches=checks[
            "normalized_resource_schema_matches"
        ],
        resource_policy_matches=checks["resource_policy_matches"],
        adapter_registration_matches=checks["adapter_registration_matches"],
        adapter_source_inventory_matches=checks[
            "adapter_source_inventory_matches"
        ],
        privilege_inventory_matches=checks["privilege_inventory_matches"],
        threshold_mode_matches=checks["threshold_mode_matches"],
        artifact_contract_matches=checks["artifact_contract_matches"],
        analysis_contract_matches=checks["analysis_contract_matches"],
        execution_command_matches=checks["execution_command_matches"],
        scoring_command_matches=checks["scoring_command_matches"],
        artifact_paths_match=checks["artifact_paths_match"],
        environment_lock_matches=checks["environment_lock_matches"],
        rng_contract_matches=checks["rng_contract_matches"],
        storage_mode_matches=checks["storage_mode_matches"],
        approval_present=approval_present,
        seal_hash=record.seal_hash(),
        execution_allowed=execution_allowed,
    )


def require_execution_seal(
    manifest: ConfirmatoryManifest,
    record: ConfirmatoryFreezeRecord,
    *,
    repository_root: Path,
    environment_lock: ConfirmatoryEnvironmentLock,
) -> ExecutionSealReport:
    report = validate_execution_seal(
        manifest,
        record,
        repository_root=repository_root,
        environment_lock=environment_lock,
    )
    if not report.execution_allowed:
        raise RuntimeError(
            "held-out capability execution is not sealed and remains prohibited"
        )
    return report

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, fields, replace
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import (
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    assess_confirmatory_readiness,
)
from .v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    QUARANTINED_HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
    heldout_world_grid_hash,
)
from .v06_confirmatory_resources import ConditionResourceRecord

_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
FREEZE_RECORD_VERSION = "v06-confirmatory-freeze-record-1"
EXECUTION_COMMAND = (
    "python -m sparkbrain.evaluation.v06_confirmatory_execute "
    "--freeze-record artifacts/v06/confirmatory/freeze_record.json"
)
ARTIFACT_PATHS = (
    "artifacts/v06/confirmatory/freeze_record.json",
    "artifacts/v06/confirmatory/results.jsonl",
    "artifacts/v06/confirmatory/resources.jsonl",
    "artifacts/v06/confirmatory/summary.json",
    "artifacts/v06/confirmatory/checksums.json",
)


def _schema_hash(model: type[Any]) -> str:
    return digest(
        {
            "model": model.__name__,
            "fields": [row.name for row in fields(model)],
        }
    )


def result_schema_hash() -> str:
    return _schema_hash(ConfirmatoryResultRecord)


def resource_schema_hash() -> str:
    return _schema_hash(ConditionResourceRecord)


def thresholds_hash(manifest: ConfirmatoryManifest) -> str:
    return digest(asdict(manifest.thresholds))


def exclusions_hash(manifest: ConfirmatoryManifest) -> str:
    return digest(list(manifest.exclusions))


def adapter_inventory_hash(manifest: ConfirmatoryManifest) -> str:
    return digest(
        [
            {
                "adapter_path": row.adapter_path,
                "adapter_ready": row.adapter_ready,
                "condition": row.condition.value,
                "isolated_from_primary": row.isolated_from_primary,
            }
            for row in manifest.conditions
        ]
    )


def execution_command_hash() -> str:
    return digest(EXECUTION_COMMAND)


def artifact_path_hash() -> str:
    return digest(list(ARTIFACT_PATHS))


@dataclass(frozen=True, slots=True)
class ConfirmatoryFreezeRecord:
    record_version: str
    code_ref: str
    manifest_hash: str
    world_generation_id: str
    world_grid_hash: str
    thresholds_hash: str
    exclusions_hash: str
    result_schema_hash: str
    resource_schema_hash: str
    adapter_inventory_hash: str
    execution_command_hash: str
    artifact_path_hash: str
    approval: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def seal_hash(self) -> str:
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ExecutionSealReport:
    manifest_ready: bool
    code_ref_matches: bool
    world_generation_matches: bool
    world_grid_matches: bool
    seeds_fresh_and_exact: bool
    thresholds_match: bool
    exclusions_match: bool
    result_schema_matches: bool
    resource_schema_matches: bool
    adapter_inventory_matches: bool
    execution_command_matches: bool
    artifact_paths_match: bool
    approval_present: bool
    seal_hash: str
    execution_allowed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_freeze_record(
    manifest: ConfirmatoryManifest,
    *,
    approval: str,
) -> ConfirmatoryFreezeRecord:
    """Build a candidate record without executing any capability.

    A caller may serialize this record only after independent review. Building
    it does not make an unready manifest executable; ``validate_execution_seal``
    remains the authoritative gate.
    """

    return ConfirmatoryFreezeRecord(
        record_version=FREEZE_RECORD_VERSION,
        code_ref=manifest.code_ref,
        manifest_hash=manifest.manifest_hash(),
        world_generation_id=WORLD_GENERATION_ID,
        world_grid_hash=heldout_world_grid_hash(),
        thresholds_hash=thresholds_hash(manifest),
        exclusions_hash=exclusions_hash(manifest),
        result_schema_hash=result_schema_hash(),
        resource_schema_hash=resource_schema_hash(),
        adapter_inventory_hash=adapter_inventory_hash(manifest),
        execution_command_hash=execution_command_hash(),
        artifact_path_hash=artifact_path_hash(),
        approval=approval,
    )


def validate_execution_seal(
    manifest: ConfirmatoryManifest,
    record: ConfirmatoryFreezeRecord,
) -> ExecutionSealReport:
    """Validate every frozen input before a capability dispatcher may run."""

    readiness = assess_confirmatory_readiness(manifest)
    manifest_ready = (
        manifest.phase is ConfirmatoryPhase.CONFIRMATORY
        and readiness.ready
        and record.record_version == FREEZE_RECORD_VERSION
    )
    code_ref_matches = (
        bool(_SHA_PATTERN.fullmatch(record.code_ref))
        and record.code_ref == manifest.code_ref
    )
    world_generation_matches = record.world_generation_id == WORLD_GENERATION_ID
    world_grid_matches = record.world_grid_hash == heldout_world_grid_hash()
    manifest_seed_values = tuple(row.seed for row in manifest.seeds)
    seeds_fresh_and_exact = (
        manifest_seed_values == HELDOUT_SEEDS
        and set(manifest_seed_values).isdisjoint(QUARANTINED_HELDOUT_SEEDS)
    )
    checks = {
        "thresholds_match": record.thresholds_hash == thresholds_hash(manifest),
        "exclusions_match": record.exclusions_hash == exclusions_hash(manifest),
        "result_schema_matches": record.result_schema_hash == result_schema_hash(),
        "resource_schema_matches": (
            record.resource_schema_hash == resource_schema_hash()
        ),
        "adapter_inventory_matches": (
            record.adapter_inventory_hash == adapter_inventory_hash(manifest)
        ),
        "execution_command_matches": (
            record.execution_command_hash == execution_command_hash()
        ),
        "artifact_paths_match": record.artifact_path_hash == artifact_path_hash(),
    }
    approval_present = bool(record.approval.strip())
    execution_allowed = all(
        (
            manifest_ready,
            code_ref_matches,
            world_generation_matches,
            world_grid_matches,
            seeds_fresh_and_exact,
            *checks.values(),
            approval_present,
        )
    )
    return ExecutionSealReport(
        manifest_ready=manifest_ready,
        code_ref_matches=code_ref_matches,
        world_generation_matches=world_generation_matches,
        world_grid_matches=world_grid_matches,
        seeds_fresh_and_exact=seeds_fresh_and_exact,
        thresholds_match=checks["thresholds_match"],
        exclusions_match=checks["exclusions_match"],
        result_schema_matches=checks["result_schema_matches"],
        resource_schema_matches=checks["resource_schema_matches"],
        adapter_inventory_matches=checks["adapter_inventory_matches"],
        execution_command_matches=checks["execution_command_matches"],
        artifact_paths_match=checks["artifact_paths_match"],
        approval_present=approval_present,
        seal_hash=record.seal_hash(),
        execution_allowed=execution_allowed,
    )


def require_execution_seal(
    manifest: ConfirmatoryManifest,
    record: ConfirmatoryFreezeRecord,
) -> ExecutionSealReport:
    report = validate_execution_seal(manifest, record)
    if not report.execution_allowed:
        raise RuntimeError("held-out capability execution is not sealed and remains prohibited")
    return report


def frozen_manifest_for_test(
    manifest: ConfirmatoryManifest,
    *,
    code_ref: str,
) -> ConfirmatoryManifest:
    """Create a synthetic ready manifest for seal unit tests only.

    The helper does not exist in the execution dispatcher and performs no
    capability work. Production freeze records must use the reviewed current
    manifest and actual branch SHA.
    """

    return replace(
        manifest,
        code_ref=code_ref,
        conditions=tuple(
            replace(
                row,
                adapter_ready=True,
                isolated_from_primary=True,
            )
            for row in manifest.conditions
        ),
    )

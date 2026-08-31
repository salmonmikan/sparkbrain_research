from __future__ import annotations

import ast
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, fields, replace
from pathlib import Path
from typing import Any

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    assess_confirmatory_readiness,
)
from .v06_confirmatory_adapter_registry_v2 import (
    ADAPTER_PATHS_V2,
    validate_adapter_registry_v2,
)
from .v06_confirmatory_environment_lock_v2 import ExecutionEnvironmentLockV2
from .v06_confirmatory_external_freeze import ExternalArtifactLayout
from .v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    QUARANTINED_HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
    HeldoutWorldParameters,
    heldout_world_grid_hash,
)
from .v06_confirmatory_normalized_resource_v2 import (
    NormalizedResourceRecordV2,
    ResourceDecisionPolicyV2,
    normalized_resource_schema_hash_v2,
)
from .v06_confirmatory_resources import ConditionResourceRecord
from .v06_confirmatory_schedule_contract import training_schedule_grid_hash

_FREEZE_BUNDLE_VERSION = "v06-external-freeze-bundle-2"
_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_APPROVAL_PATTERN = re.compile(r"^APPROVED:([A-Za-z0-9_.-]+):([0-9a-f]{16})$")

_ADAPTER_SOURCE_PATHS = (
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_common.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_controls.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_comparators.py",
    "src/sparkbrain/evaluation/v06_confirmatory_adapter_registry_v2.py",
    "src/sparkbrain/baselines/v06/confirmatory_adapters.py",
    "src/sparkbrain/baselines/v06/g3_recurrent.py",
    "src/sparkbrain/baselines/v06/g4_assembly.py",
    "src/sparkbrain/baselines/v06/g5_typed.py",
)
_CONTRACT_SOURCE_PATHS = (
    "src/sparkbrain/evaluation/v06_confirmatory.py",
    "src/sparkbrain/evaluation/v06_confirmatory_current_manifest.py",
    "src/sparkbrain/evaluation/v06_confirmatory_candidate_manifest.py",
    "src/sparkbrain/evaluation/v06_confirmatory_heldout_spec.py",
    "src/sparkbrain/evaluation/v06_confirmatory_resources.py",
    "src/sparkbrain/evaluation/v06_confirmatory_training_schedule.py",
    "src/sparkbrain/evaluation/v06_confirmatory_schedule_contract.py",
    "src/sparkbrain/evaluation/v06_confirmatory_normalized_resource_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_environment_lock_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_external_freeze.py",
    "src/sparkbrain/evaluation/v06_confirmatory_freeze_bundle_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_external_verification_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_external_control_package_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_external_launch_gate_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_execute_external_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_external_raw_store.py",
    "src/sparkbrain/evaluation/v06_confirmatory_verify_external_raw_v2.py",
    "src/sparkbrain/evaluation/v06_confirmatory_scoring.py",
    "src/sparkbrain/evaluation/v06_confirmatory_locked_scoring.py",
    "src/sparkbrain/evaluation/v06_confirmatory_score_external_v2.py",
)

_EXPECTED_PRIVILEGES = {
    ConfirmatoryCondition.PRIMARY.value: (),
    ConfirmatoryCondition.NO_ENDOGENOUS.value: (),
    ConfirmatoryCondition.RANDOM_MATCHED.value: (),
    ConfirmatoryCondition.READOUT_ONLY.value: (),
    ConfirmatoryCondition.SHUFFLED_RELATION.value: (),
    ConfirmatoryCondition.G3_RECURRENT.value: (),
    ConfirmatoryCondition.G4_ASSEMBLY.value: ("explicit-assembly-state",),
    ConfirmatoryCondition.G5_TYPED.value: (
        "typed-prediction-head",
        "typed-boundary-head",
        "typed-memory-head",
        "scalar-reward",
    ),
}
_EXPECTED_THRESHOLD_MODE = {
    ConfirmatoryCondition.PRIMARY.value: "ordinary-field-threshold",
    ConfirmatoryCondition.NO_ENDOGENOUS.value: "ordinary-field-threshold",
    ConfirmatoryCondition.RANDOM_MATCHED.value: "ordinary-field-threshold",
    ConfirmatoryCondition.READOUT_ONLY.value: "ordinary-field-threshold-no-reinjection",
    ConfirmatoryCondition.SHUFFLED_RELATION.value: "ordinary-field-threshold",
    ConfirmatoryCondition.G3_RECURRENT.value: "field-threshold-bypassed",
    ConfirmatoryCondition.G4_ASSEMBLY.value: "field-threshold-bypassed",
    ConfirmatoryCondition.G5_TYPED.value: "field-threshold-bypassed",
}


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_inventory(
    source_root: Path,
    relative_paths: tuple[str, ...],
) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative_path in relative_paths:
        path = source_root / relative_path
        if not path.is_file():
            raise FileNotFoundError(f"freeze source is missing: {relative_path}")
        result[relative_path] = _file_hash(path)
    return result


def _world_field_reads(source_root: Path) -> dict[str, tuple[str, ...]]:
    world_fields = {row.name for row in fields(HeldoutWorldParameters)}
    result: dict[str, tuple[str, ...]] = {}
    for relative_path in _ADAPTER_SOURCE_PATHS[:4]:
        path = source_root / relative_path
        tree = ast.parse(path.read_text(encoding="utf-8"))
        reads = {
            node.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in {"parameters", "world"}
            and node.attr in world_fields
        }
        result[relative_path] = tuple(sorted(reads))
    return result


def _adapter_inventory(manifest: ConfirmatoryManifest) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "adapter_path": row.adapter_path,
            "adapter_ready": row.adapter_ready,
            "condition": row.condition.value,
            "engineering_evidence_available": row.engineering_evidence_available,
            "isolated_from_primary": row.isolated_from_primary,
        }
        for row in manifest.conditions
    )


def combined_training_schedule_hash() -> str:
    return training_schedule_grid_hash()


def _schema_hash(model: type[Any]) -> str:
    return _digest(
        {
            "model": model.__name__,
            "fields": [row.name for row in fields(model)],
        }
    )


def _execution_command(
    layout: ExternalArtifactLayout,
    *,
    python_executable: str,
) -> tuple[str, ...]:
    control_root, raw_root, _ = layout.resolved()
    return (
        python_executable,
        "-m",
        "sparkbrain.evaluation.v06_confirmatory_execute_external_v2",
        "--freeze-bundle",
        str(control_root / "freeze_bundle.json"),
        "--raw-root",
        str(raw_root),
    )


def _scoring_command(
    layout: ExternalArtifactLayout,
    *,
    python_executable: str,
) -> tuple[str, ...]:
    control_root, raw_root, analysis_root = layout.resolved()
    return (
        python_executable,
        "-m",
        "sparkbrain.evaluation.v06_confirmatory_score_external_v2",
        "--freeze-bundle",
        str(control_root / "freeze_bundle.json"),
        "--raw-root",
        str(raw_root),
        "--analysis-root",
        str(analysis_root),
    )


@dataclass(frozen=True, slots=True)
class ExternalFreezeBundleV2:
    bundle_version: str
    source_git_sha: str
    source_checkout: str
    world_generation_id: str
    heldout_seeds: tuple[int, ...]
    quarantined_seeds: tuple[int, ...]
    world_grid_hash: str
    manifest_hash: str
    manifest_execution_ready: bool
    thresholds_hash: str
    exclusions_hash: str
    result_schema_hash: str
    raw_resource_schema_hash: str
    normalized_resource_contract_hash: str
    training_schedule_hash: str
    adapter_inventory: tuple[dict[str, Any], ...]
    adapter_inventory_hash: str
    adapter_source_hashes: dict[str, str]
    adapter_source_inventory_hash: str
    contract_source_hashes: dict[str, str]
    contract_source_inventory_hash: str
    world_field_read_inventory: dict[str, tuple[str, ...]]
    world_field_read_inventory_hash: str
    privilege_inventory: dict[str, tuple[str, ...]]
    privilege_inventory_hash: str
    threshold_mode_inventory: dict[str, str]
    threshold_mode_inventory_hash: str
    environment_lock: dict[str, Any]
    environment_lock_hash: str
    rng_contract_hash: str
    artifact_layout: dict[str, str]
    artifact_layout_hash: str
    execution_command: tuple[str, ...]
    execution_command_hash: str
    scoring_command: tuple[str, ...]
    scoring_command_hash: str
    candidate_execution_counter_initial: int
    builder: str
    reviewer: str | None
    approval: str | None

    def unsigned_state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["reviewer"] = None
        value["approval"] = None
        return value

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def unsigned_hash(self) -> str:
        return _digest(self.unsigned_state_dict())

    def bundle_hash(self) -> str:
        return _digest(self.state_dict())

    def validate_structure(self) -> None:
        if self.bundle_version != _FREEZE_BUNDLE_VERSION:
            raise ValueError("unexpected external freeze bundle version")
        if not _SHA_PATTERN.fullmatch(self.source_git_sha):
            raise ValueError("source_git_sha must be a lowercase 40-character SHA")
        if not Path(self.source_checkout).is_absolute():
            raise ValueError("source checkout must be absolute")
        if self.world_generation_id != WORLD_GENERATION_ID:
            raise ValueError("world generation ID mismatch")
        if self.heldout_seeds != HELDOUT_SEEDS:
            raise ValueError("held-out seed set mismatch")
        if set(self.heldout_seeds).intersection(self.quarantined_seeds):
            raise ValueError("held-out and quarantined seeds overlap")
        if self.candidate_execution_counter_initial != 0:
            raise ValueError("candidate execution counter must begin at zero")
        if not self.builder.strip():
            raise ValueError("freeze bundle requires a builder identity")
        hashes = (
            self.world_grid_hash,
            self.manifest_hash,
            self.thresholds_hash,
            self.exclusions_hash,
            self.result_schema_hash,
            self.raw_resource_schema_hash,
            self.normalized_resource_contract_hash,
            self.training_schedule_hash,
            self.adapter_inventory_hash,
            self.adapter_source_inventory_hash,
            self.contract_source_inventory_hash,
            self.world_field_read_inventory_hash,
            self.privilege_inventory_hash,
            self.threshold_mode_inventory_hash,
            self.environment_lock_hash,
            self.rng_contract_hash,
            self.artifact_layout_hash,
            self.execution_command_hash,
            self.scoring_command_hash,
        )
        if any(len(value) != 64 for value in hashes):
            raise ValueError("freeze bundle contains a malformed SHA-256 hash")
        if self.training_schedule_hash != training_schedule_grid_hash():
            raise ValueError("training schedule hash mismatch")
        if self.adapter_inventory_hash != _digest(list(self.adapter_inventory)):
            raise ValueError("adapter inventory hash mismatch")
        registered_paths = {
            condition.value: adapter_path
            for condition, adapter_path in ADAPTER_PATHS_V2.items()
        }
        inventory_paths = {
            str(row["condition"]): str(row["adapter_path"])
            for row in self.adapter_inventory
        }
        if self.manifest_execution_ready and inventory_paths != registered_paths:
            raise ValueError(
                "frozen adapter paths differ from v2 execution registry"
            )
        if self.adapter_source_inventory_hash != _digest(self.adapter_source_hashes):
            raise ValueError("adapter source inventory hash mismatch")
        if self.contract_source_inventory_hash != _digest(self.contract_source_hashes):
            raise ValueError("contract source inventory hash mismatch")
        if self.world_field_read_inventory_hash != _digest(
            {key: list(value) for key, value in self.world_field_read_inventory.items()}
        ):
            raise ValueError("world-field read inventory hash mismatch")
        if self.privilege_inventory_hash != _digest(
            {key: list(value) for key, value in self.privilege_inventory.items()}
        ):
            raise ValueError("privilege inventory hash mismatch")
        if self.threshold_mode_inventory_hash != _digest(
            self.threshold_mode_inventory
        ):
            raise ValueError("threshold-mode inventory hash mismatch")
        if self.environment_lock_hash != _digest(self.environment_lock):
            raise ValueError("environment lock hash mismatch")
        expected_python = str(self.environment_lock.get("python_executable", ""))
        if not expected_python:
            raise ValueError("environment lock lacks Python executable")
        if self.execution_command[0] != expected_python:
            raise ValueError("execution command Python differs from environment lock")
        if self.scoring_command[0] != expected_python:
            raise ValueError("scoring command Python differs from environment lock")
        if self.artifact_layout_hash != _digest(self.artifact_layout):
            raise ValueError("artifact layout hash mismatch")
        if self.execution_command_hash != _digest(list(self.execution_command)):
            raise ValueError("execution command hash mismatch")
        if self.scoring_command_hash != _digest(list(self.scoring_command)):
            raise ValueError("scoring command hash mismatch")
        if self.reviewer is None or self.approval is None:
            return
        if self.reviewer == self.builder:
            raise ValueError("independent reviewer must differ from builder")
        match = _APPROVAL_PATTERN.fullmatch(self.approval)
        if match is None or match.group(1) != self.reviewer:
            raise ValueError("freeze bundle approval has invalid reviewer identity")
        if match.group(2) != self.unsigned_hash()[:16]:
            raise ValueError("freeze bundle approval does not bind unsigned bundle")

    def validate_for_execution(self) -> None:
        self.validate_structure()
        if not self.manifest_execution_ready:
            raise ValueError("manifest is not execution-ready")
        if self.reviewer is None or self.approval is None:
            raise ValueError("freeze bundle has not been independently approved")


def build_external_freeze_bundle_v2(
    manifest: ConfirmatoryManifest,
    *,
    source_root: Path,
    source_git_sha: str,
    artifact_layout: ExternalArtifactLayout,
    environment_lock: ExecutionEnvironmentLockV2,
    builder: str,
) -> ExternalFreezeBundleV2:
    source = source_root.expanduser().resolve(strict=True)
    artifact_layout.validate(source_checkout=source)
    environment_lock.validate()
    readiness = assess_confirmatory_readiness(manifest)
    validate_adapter_registry_v2()
    registered_paths = {
        row.condition: row.adapter_path for row in manifest.conditions
    }
    if readiness.ready and registered_paths != ADAPTER_PATHS_V2:
        raise ValueError(
            "manifest adapter paths differ from v2 execution registry"
        )
    adapter_sources = _source_inventory(source, _ADAPTER_SOURCE_PATHS)
    contract_sources = _source_inventory(source, _CONTRACT_SOURCE_PATHS)
    field_reads = _world_field_reads(source)
    adapter_inventory = _adapter_inventory(manifest)
    layout_state = artifact_layout.state_dict()
    execution_command = _execution_command(
        artifact_layout,
        python_executable=environment_lock.python_executable,
    )
    scoring_command = _scoring_command(
        artifact_layout,
        python_executable=environment_lock.python_executable,
    )
    resource_policy = ResourceDecisionPolicyV2()
    resource_policy.validate()
    resource_contract_hash = _digest(
        {
            "decision_use": "descriptive-only",
            "normalized_resource_fields": [
                row.name for row in fields(NormalizedResourceRecordV2)
            ],
            "normalized_resource_schema_hash": (
                normalized_resource_schema_hash_v2()
            ),
            "normalized_resource_source": contract_sources[
                "src/sparkbrain/evaluation/"
                "v06_confirmatory_normalized_resource_v2.py"
            ],
            "policy": resource_policy.state_dict(),
            "policy_hash": resource_policy.policy_hash(),
        }
    )
    bundle = ExternalFreezeBundleV2(
        bundle_version=_FREEZE_BUNDLE_VERSION,
        source_git_sha=source_git_sha,
        source_checkout=str(source),
        world_generation_id=WORLD_GENERATION_ID,
        heldout_seeds=HELDOUT_SEEDS,
        quarantined_seeds=QUARANTINED_HELDOUT_SEEDS,
        world_grid_hash=heldout_world_grid_hash(),
        manifest_hash=manifest.manifest_hash(),
        manifest_execution_ready=(
            manifest.phase is ConfirmatoryPhase.CONFIRMATORY
            and readiness.ready
            and manifest.code_ref == source_git_sha
        ),
        thresholds_hash=_digest(asdict(manifest.thresholds)),
        exclusions_hash=_digest(list(manifest.exclusions)),
        result_schema_hash=_schema_hash(ConfirmatoryResultRecord),
        raw_resource_schema_hash=_schema_hash(ConditionResourceRecord),
        normalized_resource_contract_hash=resource_contract_hash,
        training_schedule_hash=combined_training_schedule_hash(),
        adapter_inventory=adapter_inventory,
        adapter_inventory_hash=_digest(list(adapter_inventory)),
        adapter_source_hashes=adapter_sources,
        adapter_source_inventory_hash=_digest(adapter_sources),
        contract_source_hashes=contract_sources,
        contract_source_inventory_hash=_digest(contract_sources),
        world_field_read_inventory=field_reads,
        world_field_read_inventory_hash=_digest(
            {key: list(value) for key, value in field_reads.items()}
        ),
        privilege_inventory=_EXPECTED_PRIVILEGES,
        privilege_inventory_hash=_digest(
            {key: list(value) for key, value in _EXPECTED_PRIVILEGES.items()}
        ),
        threshold_mode_inventory=_EXPECTED_THRESHOLD_MODE,
        threshold_mode_inventory_hash=_digest(_EXPECTED_THRESHOLD_MODE),
        environment_lock=environment_lock.state_dict(),
        environment_lock_hash=environment_lock.lock_hash(),
        rng_contract_hash=environment_lock.rng_contract.contract_hash(),
        artifact_layout=layout_state,
        artifact_layout_hash=_digest(layout_state),
        execution_command=execution_command,
        execution_command_hash=_digest(list(execution_command)),
        scoring_command=scoring_command,
        scoring_command_hash=_digest(list(scoring_command)),
        candidate_execution_counter_initial=0,
        builder=builder,
        reviewer=None,
        approval=None,
    )
    bundle.validate_structure()
    return bundle


def verify_independent_rebuild(
    first: ExternalFreezeBundleV2,
    second: ExternalFreezeBundleV2,
    *,
    reviewer: str,
) -> ExternalFreezeBundleV2:
    first.validate_structure()
    second.validate_structure()
    if reviewer == first.builder:
        raise ValueError("independent reviewer must differ from builder")
    if first.unsigned_state_dict() != second.unsigned_state_dict():
        raise ValueError("independent freeze bundle rebuild differs")
    approved = replace(
        first,
        reviewer=reviewer,
        approval=f"APPROVED:{reviewer}:{first.unsigned_hash()[:16]}",
    )
    approved.validate_for_execution()
    return approved


def write_external_freeze_bundle_v2(
    bundle: ExternalFreezeBundleV2,
    *,
    path: Path,
    require_execution_ready: bool,
) -> str:
    if require_execution_ready:
        bundle.validate_for_execution()
    else:
        bundle.validate_structure()
    target = path.expanduser().resolve(strict=False)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = (_canonical_json(bundle.state_dict()) + "\n").encode("utf-8")
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(target, 0o444)
    return hashlib.sha256(payload).hexdigest()

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from .v06_confirmatory import ConfirmatoryPhase
from .v06_confirmatory_current_manifest import build_current_confirmatory_manifest
from .v06_confirmatory_environment_lock_v2 import (
    ExecutionEnvironmentLockV2,
    RNGContractV2,
    capture_environment_lock_v2,
)
from .v06_confirmatory_external_freeze import ExternalArtifactLayout
from .v06_confirmatory_freeze_bundle_v2 import (
    ExternalFreezeBundleV2,
    build_external_freeze_bundle_v2,
    write_external_freeze_bundle_v2,
)


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


def _write_exclusive(path: Path, value: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (_canonical_json(value) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(path, 0o444)
    return hashlib.sha256(payload).hexdigest()


def _environment_from_state(state: dict[str, Any]) -> ExecutionEnvironmentLockV2:
    rng = RNGContractV2(**state["rng_contract"])
    return ExecutionEnvironmentLockV2(
        lock_version=state["lock_version"],
        python_implementation=state["python_implementation"],
        python_version=state["python_version"],
        python_executable=state["python_executable"],
        python_executable_sha256=state["python_executable_sha256"],
        operating_system=state["operating_system"],
        machine=state["machine"],
        platform_string=state["platform_string"],
        locale=state["locale"],
        timezone=state["timezone"],
        python_hash_seed=state["python_hash_seed"],
        installed_distributions=tuple(state["installed_distributions"]),
        installed_distributions_hash=state["installed_distributions_hash"],
        rng_contract=rng,
    )


def load_external_freeze_bundle_v2(path: Path) -> ExternalFreezeBundleV2:
    state = json.loads(path.expanduser().resolve(strict=True).read_text(encoding="utf-8"))
    bundle = ExternalFreezeBundleV2(
        bundle_version=state["bundle_version"],
        source_git_sha=state["source_git_sha"],
        source_checkout=state["source_checkout"],
        world_generation_id=state["world_generation_id"],
        heldout_seeds=tuple(state["heldout_seeds"]),
        quarantined_seeds=tuple(state["quarantined_seeds"]),
        world_grid_hash=state["world_grid_hash"],
        manifest_hash=state["manifest_hash"],
        manifest_execution_ready=state["manifest_execution_ready"],
        thresholds_hash=state["thresholds_hash"],
        exclusions_hash=state["exclusions_hash"],
        result_schema_hash=state["result_schema_hash"],
        raw_resource_schema_hash=state["raw_resource_schema_hash"],
        normalized_resource_contract_hash=state[
            "normalized_resource_contract_hash"
        ],
        training_schedule_hash=state["training_schedule_hash"],
        adapter_inventory=tuple(state["adapter_inventory"]),
        adapter_inventory_hash=state["adapter_inventory_hash"],
        adapter_source_hashes=dict(state["adapter_source_hashes"]),
        adapter_source_inventory_hash=state["adapter_source_inventory_hash"],
        contract_source_hashes=dict(state["contract_source_hashes"]),
        contract_source_inventory_hash=state[
            "contract_source_inventory_hash"
        ],
        world_field_read_inventory={
            key: tuple(value)
            for key, value in state["world_field_read_inventory"].items()
        },
        world_field_read_inventory_hash=state[
            "world_field_read_inventory_hash"
        ],
        privilege_inventory={
            key: tuple(value) for key, value in state["privilege_inventory"].items()
        },
        privilege_inventory_hash=state["privilege_inventory_hash"],
        threshold_mode_inventory=dict(state["threshold_mode_inventory"]),
        threshold_mode_inventory_hash=state[
            "threshold_mode_inventory_hash"
        ],
        environment_lock=dict(state["environment_lock"]),
        environment_lock_hash=state["environment_lock_hash"],
        rng_contract_hash=state["rng_contract_hash"],
        artifact_layout=dict(state["artifact_layout"]),
        artifact_layout_hash=state["artifact_layout_hash"],
        execution_command=tuple(state["execution_command"]),
        execution_command_hash=state["execution_command_hash"],
        scoring_command=tuple(state["scoring_command"]),
        scoring_command_hash=state["scoring_command_hash"],
        candidate_execution_counter_initial=state[
            "candidate_execution_counter_initial"
        ],
        builder=state["builder"],
        reviewer=state.get("reviewer"),
        approval=state.get("approval"),
    )
    bundle.validate_structure()
    return bundle


@dataclass(frozen=True, slots=True)
class IndependentFreezeVerificationV2:
    source_git_sha_matches: bool
    unsigned_bundle_matches: bool
    environment_matches: bool
    builder_and_reviewer_distinct: bool
    manifest_execution_ready: bool
    candidate_execution_counter_zero: bool
    approval_issued: bool
    reviewer: str
    expected_unsigned_hash: str
    observed_unsigned_hash: str
    verification_passed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def independently_verify_external_bundle_v2(
    expected: ExternalFreezeBundleV2,
    *,
    source_root: Path,
    environment_lock: ExecutionEnvironmentLockV2,
    reviewer: str,
    issue_approval: bool,
) -> tuple[ExternalFreezeBundleV2 | None, IndependentFreezeVerificationV2]:
    expected.validate_structure()
    if reviewer == expected.builder:
        raise ValueError("independent reviewer must differ from builder")
    layout = ExternalArtifactLayout(**expected.artifact_layout)
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY,
        code_ref=expected.source_git_sha,
    )
    observed = build_external_freeze_bundle_v2(
        manifest,
        source_root=source_root,
        source_git_sha=expected.source_git_sha,
        artifact_layout=layout,
        environment_lock=environment_lock,
        builder=expected.builder,
    )
    source_git_sha_matches = observed.source_git_sha == expected.source_git_sha
    unsigned_bundle_matches = (
        observed.unsigned_state_dict() == expected.unsigned_state_dict()
    )
    expected_environment = _environment_from_state(expected.environment_lock)
    environment_matches = (
        expected_environment.state_dict() == environment_lock.state_dict()
    )
    counter_zero = (
        expected.candidate_execution_counter_initial
        == observed.candidate_execution_counter_initial
        == 0
    )
    base_passed = all(
        (
            source_git_sha_matches,
            unsigned_bundle_matches,
            environment_matches,
            counter_zero,
        )
    )
    approved: ExternalFreezeBundleV2 | None = None
    approval_issued = False
    if issue_approval:
        if not base_passed:
            raise ValueError("independent freeze rebuild did not match")
        if not observed.manifest_execution_ready:
            raise ValueError("manifest is not ready; execution approval is prohibited")
        approved = replace(
            observed,
            reviewer=reviewer,
            approval=(
                f"APPROVED:{reviewer}:{observed.unsigned_hash()[:16]}"
            ),
        )
        approved.validate_for_execution()
        approval_issued = True
    report = IndependentFreezeVerificationV2(
        source_git_sha_matches=source_git_sha_matches,
        unsigned_bundle_matches=unsigned_bundle_matches,
        environment_matches=environment_matches,
        builder_and_reviewer_distinct=True,
        manifest_execution_ready=observed.manifest_execution_ready,
        candidate_execution_counter_zero=counter_zero,
        approval_issued=approval_issued,
        reviewer=reviewer,
        expected_unsigned_hash=expected.unsigned_hash(),
        observed_unsigned_hash=observed.unsigned_hash(),
        verification_passed=base_passed,
    )
    return approved, report


def verify_external_bundle_cli(
    *,
    unsigned_bundle_path: Path,
    source_root: Path,
    reviewer: str,
    output_root: Path,
    issue_approval: bool,
) -> IndependentFreezeVerificationV2:
    expected = load_external_freeze_bundle_v2(unsigned_bundle_path)
    observed_environment = capture_environment_lock_v2()
    approved, report = independently_verify_external_bundle_v2(
        expected,
        source_root=source_root,
        environment_lock=observed_environment,
        reviewer=reviewer,
        issue_approval=issue_approval,
    )
    output = output_root.expanduser().resolve(strict=False)
    output.mkdir(parents=True, exist_ok=True)
    _write_exclusive(output / "independent_verification.json", report.state_dict())
    _write_exclusive(
        output / "independent_verification.sha256.json",
        {"verification_hash": _digest(report.state_dict())},
    )
    if approved is not None:
        write_external_freeze_bundle_v2(
            approved,
            path=output / "freeze_bundle.json",
            require_execution_ready=True,
        )
    return report

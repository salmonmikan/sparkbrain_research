from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.baselines.v06.heldout_dryrun import (
    COMPARATOR_DRY_RUN_ADAPTERS,
)

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    EvidenceDomain,
    assess_confirmatory_readiness,
)
from .v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)
from .v06_confirmatory_heldout_dryrun_contract import (
    DomainSchemaRecord,
    HeldoutAdapterDryRun,
    ResourceSchemaDeclaration,
)
from .v06_confirmatory_heldout_primary_dryrun import (
    PRIMARY_CONTROL_DRY_RUN_ADAPTERS,
)
from .v06_confirmatory_heldout_spec import (
    HeldoutWorldParameters,
    build_heldout_world_grid,
    heldout_world_grid_hash,
)

_DRY_RUN_ADAPTERS: dict[
    ConfirmatoryCondition,
    Callable[[HeldoutWorldParameters], HeldoutAdapterDryRun],
] = {
    **PRIMARY_CONTROL_DRY_RUN_ADAPTERS,
    **COMPARATOR_DRY_RUN_ADAPTERS,
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


@dataclass(frozen=True, slots=True)
class HeldoutPreflightMatrix:
    world_grid_hash: str
    adapter_records: tuple[HeldoutAdapterDryRun, ...]

    @property
    def domain_schema_records(self) -> tuple[DomainSchemaRecord, ...]:
        return tuple(
            row
            for adapter in self.adapter_records
            for row in adapter.domain_schemas
        )

    @property
    def resource_schema_records(self) -> tuple[ResourceSchemaDeclaration, ...]:
        return tuple(row.resource_schema for row in self.adapter_records)

    @property
    def world_keys(self) -> tuple[tuple[str, int], ...]:
        return tuple(
            sorted({(row.family_id, row.seed) for row in self.adapter_records})
        )

    @property
    def matrix_hash(self) -> str:
        return _digest([row.state_dict() for row in self.adapter_records])

    def state_dict(self) -> dict[str, Any]:
        return {
            "adapter_record_count": len(self.adapter_records),
            "domain_schema_record_count": len(self.domain_schema_records),
            "matrix_hash": self.matrix_hash,
            "resource_schema_record_count": len(self.resource_schema_records),
            "world_count": len(self.world_keys),
            "world_grid_hash": self.world_grid_hash,
        }


@dataclass(frozen=True, slots=True)
class HeldoutPreflightReport:
    world_count: int
    adapter_record_count: int
    resource_schema_record_count: int
    domain_schema_record_count: int
    expected_domain_schema_record_count: int
    replay_matrix_hash_match: bool
    world_grid_hash_match: bool
    adapter_coverage_complete: bool
    common_input_contract_complete: bool
    parameter_reflection_complete: bool
    branch_competition_preserved: bool
    resource_schema_complete: bool
    safety_declarations_passed: bool
    schema_only: bool
    capability_execution_count: int
    heldout_manifest_ready: bool
    heldout_ready_adapter_count: int
    code_ref_frozen: bool
    ready_for_code_review: bool
    confirmatory_execution_allowed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _adapter_grouped_by_world(
    records: tuple[HeldoutAdapterDryRun, ...],
) -> dict[tuple[str, int], tuple[HeldoutAdapterDryRun, ...]]:
    grouped: defaultdict[
        tuple[str, int],
        list[HeldoutAdapterDryRun],
    ] = defaultdict(list)
    for row in records:
        grouped[(row.family_id, row.seed)].append(row)
    return {
        key: tuple(sorted(rows, key=lambda row: row.condition.value))
        for key, rows in grouped.items()
    }


def _common_input_contract_complete(
    records: tuple[HeldoutAdapterDryRun, ...],
) -> bool:
    for rows in _adapter_grouped_by_world(records).values():
        if {row.condition for row in rows} != set(ConfirmatoryCondition):
            return False
        if len({row.world_specification_hash for row in rows}) != 1:
            return False
        if len({row.input_projection_hash for row in rows}) != 1:
            return False
        first = rows[0].input_projection
        if any(row.input_projection != first for row in rows[1:]):
            return False
    return True


def _parameter_reflection_complete(
    records: tuple[HeldoutAdapterDryRun, ...],
) -> bool:
    for row in records:
        world = row.input_projection
        architecture = row.architecture_projection
        expected_equal = {
            "active_unit_ids": list(world["active_unit_ids"]),
            "alternate_path": list(world["alternate_path"]),
            "boundary_lag_ms": world["boundary_lag_ms"],
            "branch_exposure_counts": list(world["branch_exposure_counts"]),
            "competition_paths": [list(path) for path in world["competition_paths"]],
            "contingency_cycle_targets": list(
                world["contingency_cycle_targets"]
            ),
            "contingency_phase_lengths": list(
                world["contingency_phase_lengths"]
            ),
            "control_path": list(world["control_path"]),
            "control_port": world["control_port"],
            "cue_magnitude": world["cue_magnitude"],
            "distractor_unit_ids": list(world["distractor_unit_ids"]),
            "episode_spacings_ms": list(world["episode_spacings_ms"]),
            "evaluation_lags_ms": list(world["evaluation_lags_ms"]),
            "main_path": list(world["main_path"]),
            "main_port": world["main_port"],
            "new_target": world["new_target"],
            "old_target": world["old_target"],
            "relation_reentry_gain": world["relation_reentry_gain"],
            "third_target": world["third_target"],
            "training_lag_profiles_ms": [
                list(profile) for profile in world["training_lag_profiles_ms"]
            ],
            "unit_count": world["unit_count"],
        }
        if any(architecture.get(key) != value for key, value in expected_equal.items()):
            return False
        if row.safety.normal_field_threshold_present:
            if architecture.get("field_threshold") != world["threshold"]:
                return False
            if architecture.get("normal_field_threshold") != "present":
                return False
        else:
            if architecture.get("provided_world_threshold") != world["threshold"]:
                return False
            if architecture.get("normal_field_threshold") != "bypassed":
                return False
    return True


def _branch_competition_preserved(
    records: tuple[HeldoutAdapterDryRun, ...],
) -> bool:
    rows = tuple(
        row
        for row in records
        if row.family_id == "heldout-branch-competition"
    )
    if len(rows) != 10 * len(ConfirmatoryCondition):
        return False
    for row in rows:
        paths = tuple(
            tuple(path) for path in row.architecture_projection["competition_paths"]
        )
        counts = tuple(row.architecture_projection["branch_exposure_counts"])
        if len(paths) != len(counts) or len(paths) != 3:
            return False
        if len(set(paths)) != 3:
            return False
        if len({path[0] for path in paths}) != 1:
            return False
        if not counts[0] > counts[1] > counts[2]:
            return False
        if max(counts) - min(counts) != 2:
            return False
    return True


def _resource_schema_complete(
    records: tuple[ResourceSchemaDeclaration, ...],
) -> bool:
    keys = {(row.family_id, row.seed, row.condition) for row in records}
    if len(keys) != len(records):
        return False
    try:
        for row in records:
            row.validate()
    except ValueError:
        return False
    return True


def _safety_declarations_passed(
    records: tuple[HeldoutAdapterDryRun, ...],
) -> bool:
    try:
        for row in records:
            row.safety.validate(row.condition)
    except ValueError:
        return False
    return all(
        not row.safety.reads_primary_runtime_state
        and not row.safety.capability_executed
        and not row.safety.generated_events_count_as_observations
        and not row.safety.generated_events_commit_positive_learning
        for row in records
    )


def build_heldout_preflight_matrix() -> HeldoutPreflightMatrix:
    if set(_DRY_RUN_ADAPTERS) != set(ConfirmatoryCondition):
        raise RuntimeError("held-out dry-run adapter registry is incomplete")
    records: list[HeldoutAdapterDryRun] = []
    for world in build_heldout_world_grid():
        for condition in ConfirmatoryCondition:
            row = _DRY_RUN_ADAPTERS[condition](world)
            row.validate(world)
            records.append(row)
    return HeldoutPreflightMatrix(
        world_grid_hash=heldout_world_grid_hash(),
        adapter_records=tuple(records),
    )


def run_heldout_preflight() -> tuple[HeldoutPreflightMatrix, HeldoutPreflightReport]:
    first = build_heldout_preflight_matrix()
    replay = build_heldout_preflight_matrix()
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    readiness = assess_confirmatory_readiness(manifest)
    ready_adapters = sum(row.adapter_ready for row in manifest.conditions)
    capability_execution_count = sum(
        row.safety.capability_executed for row in first.adapter_records
    ) + sum(
        row.capability_result_present for row in first.domain_schema_records
    )
    adapter_coverage = (
        len(first.world_keys) == 50
        and len(first.adapter_records) == 50 * len(ConfirmatoryCondition)
        and all(
            {row.condition for row in rows} == set(ConfirmatoryCondition)
            for rows in _adapter_grouped_by_world(first.adapter_records).values()
        )
    )
    common_input = _common_input_contract_complete(first.adapter_records)
    parameter_reflection = _parameter_reflection_complete(first.adapter_records)
    branch_preserved = _branch_competition_preserved(first.adapter_records)
    resource_complete = _resource_schema_complete(
        first.resource_schema_records
    )
    safety_passed = _safety_declarations_passed(first.adapter_records)
    schema_only = (
        capability_execution_count == 0
        and all(
            row.status.value == "unscored"
            and not row.capability_result_present
            for row in first.domain_schema_records
        )
    )
    preflight_passed = all(
        (
            first.matrix_hash == replay.matrix_hash,
            first.world_grid_hash == heldout_world_grid_hash(),
            adapter_coverage,
            common_input,
            parameter_reflection,
            branch_preserved,
            resource_complete,
            safety_passed,
            schema_only,
            not readiness.ready,
            ready_adapters == 0,
            not readiness.code_ref_frozen,
        )
    )
    report = HeldoutPreflightReport(
        world_count=len(first.world_keys),
        adapter_record_count=len(first.adapter_records),
        resource_schema_record_count=len(first.resource_schema_records),
        domain_schema_record_count=len(first.domain_schema_records),
        expected_domain_schema_record_count=(
            50 * len(ConfirmatoryCondition) * len(EvidenceDomain)
        ),
        replay_matrix_hash_match=first.matrix_hash == replay.matrix_hash,
        world_grid_hash_match=(
            first.world_grid_hash == heldout_world_grid_hash()
        ),
        adapter_coverage_complete=adapter_coverage,
        common_input_contract_complete=common_input,
        parameter_reflection_complete=parameter_reflection,
        branch_competition_preserved=branch_preserved,
        resource_schema_complete=resource_complete,
        safety_declarations_passed=safety_passed,
        schema_only=schema_only,
        capability_execution_count=capability_execution_count,
        heldout_manifest_ready=readiness.ready,
        heldout_ready_adapter_count=ready_adapters,
        code_ref_frozen=readiness.code_ref_frozen,
        ready_for_code_review=preflight_passed,
        confirmatory_execution_allowed=False,
    )
    return first, report

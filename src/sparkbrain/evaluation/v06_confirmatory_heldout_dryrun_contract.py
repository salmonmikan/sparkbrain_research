from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields
from enum import StrEnum
from typing import Any

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters
from .v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
)


class DryRunStatus(StrEnum):
    UNSCORED = "unscored"


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
class AdapterSafetyDeclaration:
    reads_primary_runtime_state: bool
    capability_executed: bool
    generated_events_count_as_observations: bool
    generated_events_commit_positive_learning: bool
    normal_field_threshold_present: bool
    threshold_bypassed: bool
    explicit_assembly_entries: int
    typed_head_count: int
    scalar_reward_observations: int
    privileged_information: tuple[PrivilegedInformation, ...] = ()

    def validate(self, condition: ConfirmatoryCondition) -> None:
        if self.reads_primary_runtime_state:
            raise ValueError("a held-out adapter cannot inspect Primary runtime state")
        if self.capability_executed:
            raise ValueError("schema-only dry runs cannot execute capability")
        if self.generated_events_count_as_observations:
            raise ValueError("generated events cannot count as observations")
        if self.generated_events_commit_positive_learning:
            raise ValueError("generated events cannot commit positive learning")

        probe = ConditionResourceRecord(
            family_id="dry-run",
            seed=0,
            condition=condition,
            observed_training_events=0,
            generated_internal_events=0,
            persistent_state_entries=0,
            intervention_count=0,
            parameter_count=0,
            wall_clock_ms=0.0,
            normal_field_threshold_present=(
                self.normal_field_threshold_present
            ),
            normal_field_threshold_crossings=0,
            threshold_bypassed=self.threshold_bypassed,
            explicit_assembly_entries=self.explicit_assembly_entries,
            typed_head_count=self.typed_head_count,
            scalar_reward_observations=self.scalar_reward_observations,
            privileged_information=self.privileged_information,
        )
        probe.validate()

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["privileged_information"] = [
            row.value for row in self.privileged_information
        ]
        return value


@dataclass(frozen=True, slots=True)
class ResourceSchemaDeclaration:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    record_fields: tuple[str, ...]
    metric_fields: tuple[str, ...]
    dynamic_measurement_fields: tuple[str, ...]
    measurements_present: bool

    def validate(self) -> None:
        expected_record_fields = tuple(
            row.name for row in fields(ConditionResourceRecord)
        )
        if self.record_fields != expected_record_fields:
            raise ValueError("resource record schema is incomplete")
        if set(self.dynamic_measurement_fields) != {
            "generated_internal_events",
            "intervention_count",
            "normal_field_threshold_crossings",
            "observed_training_events",
            "parameter_count",
            "persistent_state_entries",
            "wall_clock_ms",
        }:
            raise ValueError("dynamic resource measurement schema is incomplete")
        if self.measurements_present:
            raise ValueError("schema-only dry run cannot contain resource measurements")
        if not self.metric_fields:
            raise ValueError("resource metric schema must be declared")

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["condition"] = self.condition.value
        return value


@dataclass(frozen=True, slots=True)
class DomainSchemaRecord:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    evidence_domain: EvidenceDomain
    status: DryRunStatus
    result_field_types: tuple[tuple[str, str], ...]
    required_metric_names: tuple[str, ...]
    capability_result_present: bool

    def validate(self) -> None:
        if self.status is not DryRunStatus.UNSCORED:
            raise ValueError("dry-run domain records must remain unscored")
        if self.capability_result_present:
            raise ValueError("dry-run domain records cannot contain capability results")
        if dict(self.result_field_types) != {
            "condition": "ConfirmatoryCondition",
            "evidence_domain": "EvidenceDomain",
            "family_id": "str",
            "metrics": "tuple[tuple[str, float], ...]",
            "passed": "bool",
            "seed": "int",
        }:
            raise ValueError("confirmatory result schema does not match the contract")

    def state_dict(self) -> dict[str, Any]:
        return {
            "capability_result_present": self.capability_result_present,
            "condition": self.condition.value,
            "evidence_domain": self.evidence_domain.value,
            "family_id": self.family_id,
            "required_metric_names": list(self.required_metric_names),
            "result_field_types": dict(self.result_field_types),
            "seed": self.seed,
            "status": self.status.value,
        }


@dataclass(frozen=True, slots=True)
class HeldoutAdapterDryRun:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    adapter_path: str
    world_specification_hash: str
    consumed_world_field_names: tuple[str, ...]
    input_projection: dict[str, Any]
    input_projection_hash: str
    architecture_projection: dict[str, Any]
    configuration_hash: str
    safety: AdapterSafetyDeclaration
    resource_schema: ResourceSchemaDeclaration
    domain_schemas: tuple[DomainSchemaRecord, ...]
    status: DryRunStatus

    def validate(self, world: HeldoutWorldParameters) -> None:
        if self.family_id != world.family_id or self.seed != world.seed:
            raise ValueError("adapter dry run does not match the world identity")
        if self.world_specification_hash != world.specification_hash():
            raise ValueError("adapter consumed a different held-out world")
        expected_fields = tuple(row.name for row in fields(HeldoutWorldParameters))
        if self.consumed_world_field_names != expected_fields:
            raise ValueError("adapter did not consume the complete held-out contract")
        if self.input_projection != world.state_dict():
            raise ValueError("adapter input projection differs from the held-out world")
        if self.input_projection_hash != _digest(self.input_projection):
            raise ValueError("adapter input projection hash is invalid")
        if self.input_projection_hash != self.world_specification_hash:
            raise ValueError("adapter input hash differs from the world specification hash")
        expected_configuration_hash = _digest(
            {
                "architecture": self.architecture_projection,
                "condition": self.condition.value,
                "input": self.input_projection,
            }
        )
        if self.configuration_hash != expected_configuration_hash:
            raise ValueError("adapter configuration hash is invalid")
        if self.status is not DryRunStatus.UNSCORED:
            raise ValueError("held-out adapter dry runs must remain unscored")
        self.safety.validate(self.condition)
        self.resource_schema.validate()
        if len(self.domain_schemas) != len(EvidenceDomain):
            raise ValueError("each adapter requires one schema row per evidence domain")
        if {row.evidence_domain for row in self.domain_schemas} != set(
            EvidenceDomain
        ):
            raise ValueError("adapter domain schema coverage is incomplete")
        for row in self.domain_schemas:
            if (
                row.family_id != self.family_id
                or row.seed != self.seed
                or row.condition is not self.condition
            ):
                raise ValueError("domain schema identity differs from its adapter")
            row.validate()

    def state_dict(self) -> dict[str, Any]:
        return {
            "adapter_path": self.adapter_path,
            "architecture_projection": self.architecture_projection,
            "condition": self.condition.value,
            "configuration_hash": self.configuration_hash,
            "consumed_world_field_names": list(self.consumed_world_field_names),
            "domain_schemas": [row.state_dict() for row in self.domain_schemas],
            "family_id": self.family_id,
            "input_projection": self.input_projection,
            "input_projection_hash": self.input_projection_hash,
            "resource_schema": self.resource_schema.state_dict(),
            "safety": self.safety.state_dict(),
            "seed": self.seed,
            "status": self.status.value,
            "world_specification_hash": self.world_specification_hash,
        }


def _required_metric_names(
    condition: ConfirmatoryCondition,
) -> tuple[str, ...]:
    common = (
        "self_confirmation_violations",
        "taxonomy_hash_match",
    )
    if condition is ConfirmatoryCondition.PRIMARY:
        return tuple(
            sorted(
                {
                    *common,
                    "boundary_matched_impairment",
                    "boundary_targeted_impairment",
                    "chain_matched_impairment",
                    "chain_targeted_impairment",
                }
            )
        )
    if condition in {
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }:
        return tuple(sorted({*common, "control_contract_passed"}))
    return tuple(sorted(common))


def build_resource_schema(
    world: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
    safety: AdapterSafetyDeclaration,
) -> ResourceSchemaDeclaration:
    safety.validate(condition)
    metric_probe = ConditionResourceRecord(
        family_id=world.family_id,
        seed=world.seed,
        condition=condition,
        observed_training_events=0,
        generated_internal_events=0,
        persistent_state_entries=0,
        intervention_count=0,
        parameter_count=0,
        wall_clock_ms=0.0,
        normal_field_threshold_present=safety.normal_field_threshold_present,
        normal_field_threshold_crossings=0,
        threshold_bypassed=safety.threshold_bypassed,
        explicit_assembly_entries=safety.explicit_assembly_entries,
        typed_head_count=safety.typed_head_count,
        scalar_reward_observations=safety.scalar_reward_observations,
        privileged_information=safety.privileged_information,
    )
    declaration = ResourceSchemaDeclaration(
        family_id=world.family_id,
        seed=world.seed,
        condition=condition,
        record_fields=tuple(row.name for row in fields(ConditionResourceRecord)),
        metric_fields=tuple(sorted(metric_probe.metric_dict())),
        dynamic_measurement_fields=(
            "generated_internal_events",
            "intervention_count",
            "normal_field_threshold_crossings",
            "observed_training_events",
            "parameter_count",
            "persistent_state_entries",
            "wall_clock_ms",
        ),
        measurements_present=False,
    )
    declaration.validate()
    return declaration


def build_domain_schemas(
    world: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> tuple[DomainSchemaRecord, ...]:
    result_fields = (
        ("condition", "ConfirmatoryCondition"),
        ("evidence_domain", "EvidenceDomain"),
        ("family_id", "str"),
        ("metrics", "tuple[tuple[str, float], ...]"),
        ("passed", "bool"),
        ("seed", "int"),
    )
    return tuple(
        DomainSchemaRecord(
            family_id=world.family_id,
            seed=world.seed,
            condition=condition,
            evidence_domain=domain,
            status=DryRunStatus.UNSCORED,
            result_field_types=result_fields,
            required_metric_names=_required_metric_names(condition),
            capability_result_present=False,
        )
        for domain in EvidenceDomain
    )


def build_adapter_dry_run(
    world: HeldoutWorldParameters,
    *,
    condition: ConfirmatoryCondition,
    adapter_path: str,
    architecture_projection: dict[str, Any],
    safety: AdapterSafetyDeclaration,
) -> HeldoutAdapterDryRun:
    world.validate()
    safety.validate(condition)
    input_projection = world.state_dict()
    record = HeldoutAdapterDryRun(
        family_id=world.family_id,
        seed=world.seed,
        condition=condition,
        adapter_path=adapter_path,
        world_specification_hash=world.specification_hash(),
        consumed_world_field_names=tuple(
            row.name for row in fields(HeldoutWorldParameters)
        ),
        input_projection=input_projection,
        input_projection_hash=_digest(input_projection),
        architecture_projection=architecture_projection,
        configuration_hash=_digest(
            {
                "architecture": architecture_projection,
                "condition": condition.value,
                "input": input_projection,
            }
        ),
        safety=safety,
        resource_schema=build_resource_schema(world, condition, safety),
        domain_schemas=build_domain_schemas(world, condition),
        status=DryRunStatus.UNSCORED,
    )
    record.validate(world)
    return record

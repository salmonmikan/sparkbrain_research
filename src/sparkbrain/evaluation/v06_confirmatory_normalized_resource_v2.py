from __future__ import annotations

import hashlib
import json
import math
import time
import tracemalloc
from dataclasses import asdict, dataclass, fields
from typing import Any, Callable, TypeVar

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_common import HeldoutConditionExecution

_RESOURCE_POLICY_VERSION = "v06-normalized-resource-policy-2"
_RESOURCE_SCHEMA_VERSION = "v06-normalized-resource-schema-2"
_T = TypeVar("_T")


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
class ResourceDecisionPolicyV2:
    policy_version: str = _RESOURCE_POLICY_VERSION
    efficiency_affects_capability_pass_fail: bool = False
    common_measurements_are_descriptive: bool = True
    adapter_proxies_are_descriptive: bool = True
    architecture_specific_values_are_descriptive: bool = True
    missing_record_is_execution_failure: bool = True
    nonfinite_value_is_execution_failure: bool = True
    privilege_mismatch_is_execution_failure: bool = True
    threshold_mode_mismatch_is_execution_failure: bool = True

    def validate(self) -> None:
        if self.policy_version != _RESOURCE_POLICY_VERSION:
            raise ValueError("unexpected normalized resource policy version")
        if self.efficiency_affects_capability_pass_fail:
            raise ValueError("resource efficiency must not alter v0.6 capability pass/fail")
        if not all(
            (
                self.common_measurements_are_descriptive,
                self.adapter_proxies_are_descriptive,
                self.architecture_specific_values_are_descriptive,
                self.missing_record_is_execution_failure,
                self.nonfinite_value_is_execution_failure,
                self.privilege_mismatch_is_execution_failure,
                self.threshold_mode_mismatch_is_execution_failure,
            )
        ):
            raise ValueError("normalized resource policy cannot weaken integrity gates")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def policy_hash(self) -> str:
        return _digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class NormalizedResourceRecordV2:
    schema_version: str
    execution_id: str
    family_id: str
    seed: int
    condition: str
    world_specification_hash: str
    common_wall_clock_ns: int
    common_process_cpu_ns: int
    common_peak_traced_memory_bytes: int
    common_canonical_execution_bytes: int
    common_result_record_count: int
    common_resource_record_count: int
    adapter_observed_external_events_proxy: int
    adapter_generated_internal_events_proxy: int
    adapter_mutable_state_entries_proxy: int
    adapter_parameter_entries_proxy: int
    adapter_intervention_count_proxy: int
    architecture_normal_field_threshold_present: bool
    architecture_normal_field_threshold_crossings: int
    architecture_threshold_bypassed: bool
    architecture_explicit_assembly_entries: int
    architecture_typed_head_count: int
    architecture_scalar_reward_observations: int
    architecture_privileged_information: tuple[str, ...]
    decision_use: str

    def validate(self) -> None:
        if self.schema_version != _RESOURCE_SCHEMA_VERSION:
            raise ValueError("unexpected normalized resource schema version")
        if len(self.execution_id) != 64:
            raise ValueError("normalized resource execution_id must be SHA-256")
        if len(self.world_specification_hash) != 64:
            raise ValueError("normalized resource world hash must be SHA-256")
        if not self.family_id or not self.condition:
            raise ValueError("normalized resource identity fields must be non-empty")
        numeric_values = (
            self.common_wall_clock_ns,
            self.common_process_cpu_ns,
            self.common_peak_traced_memory_bytes,
            self.common_canonical_execution_bytes,
            self.common_result_record_count,
            self.common_resource_record_count,
            self.adapter_observed_external_events_proxy,
            self.adapter_generated_internal_events_proxy,
            self.adapter_mutable_state_entries_proxy,
            self.adapter_parameter_entries_proxy,
            self.adapter_intervention_count_proxy,
            self.architecture_normal_field_threshold_crossings,
            self.architecture_explicit_assembly_entries,
            self.architecture_typed_head_count,
            self.architecture_scalar_reward_observations,
        )
        if any(value < 0 or not math.isfinite(float(value)) for value in numeric_values):
            raise ValueError("normalized resource values must be finite and non-negative")
        if self.common_result_record_count < 1 or self.common_resource_record_count != 1:
            raise ValueError("normalized resource record counts are invalid")
        if self.architecture_threshold_bypassed:
            if self.architecture_normal_field_threshold_present:
                raise ValueError("threshold bypass and ordinary threshold cannot both be active")
            if self.architecture_normal_field_threshold_crossings != 0:
                raise ValueError("threshold-bypassed condition cannot report Field crossings")
        elif not self.architecture_normal_field_threshold_present:
            raise ValueError("non-bypassed condition must retain ordinary Field threshold")
        if self.decision_use != "descriptive-only":
            raise ValueError("normalized resource efficiency must remain descriptive-only")

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["architecture_privileged_information"] = list(
            self.architecture_privileged_information
        )
        return value

    def record_hash(self) -> str:
        return _digest(self.state_dict())


def normalized_resource_schema_hash_v2() -> str:
    return _digest(
        {
            "fields": [row.name for row in fields(NormalizedResourceRecordV2)],
            "policy": ResourceDecisionPolicyV2().state_dict(),
            "schema_version": _RESOURCE_SCHEMA_VERSION,
        }
    )


def deterministic_execution_id_v2(
    *,
    envelope_hash: str,
    source_git_sha: str,
    manifest_hash: str,
    world_generation_id: str,
    family_id: str,
    seed: int,
    condition: ConfirmatoryCondition,
    world_specification_hash: str,
) -> str:
    return _digest(
        {
            "condition": condition.value,
            "envelope_hash": envelope_hash,
            "family_id": family_id,
            "manifest_hash": manifest_hash,
            "seed": seed,
            "source_git_sha": source_git_sha,
            "world_generation_id": world_generation_id,
            "world_specification_hash": world_specification_hash,
        }
    )


def measure_condition_execution_v2(
    adapter: Callable[[], HeldoutConditionExecution],
    *,
    execution_id: str,
    policy: ResourceDecisionPolicyV2 | None = None,
) -> tuple[HeldoutConditionExecution, NormalizedResourceRecordV2]:
    """Measure one already-bound adapter invocation from the evaluator boundary."""

    decision_policy = policy or ResourceDecisionPolicyV2()
    decision_policy.validate()
    tracemalloc.start()
    started_wall = time.perf_counter_ns()
    started_cpu = time.process_time_ns()
    try:
        execution = adapter()
        process_cpu_ns = time.process_time_ns() - started_cpu
        wall_clock_ns = time.perf_counter_ns() - started_wall
        _, peak_memory = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    execution.validate()
    canonical_bytes = len(
        _canonical_json(execution.state_dict()).encode("utf-8")
    )
    resource = execution.resource
    record = NormalizedResourceRecordV2(
        schema_version=_RESOURCE_SCHEMA_VERSION,
        execution_id=execution_id,
        family_id=execution.family_id,
        seed=execution.seed,
        condition=execution.condition.value,
        world_specification_hash=execution.world_specification_hash,
        common_wall_clock_ns=wall_clock_ns,
        common_process_cpu_ns=process_cpu_ns,
        common_peak_traced_memory_bytes=peak_memory,
        common_canonical_execution_bytes=canonical_bytes,
        common_result_record_count=len(execution.records),
        common_resource_record_count=1,
        adapter_observed_external_events_proxy=resource.observed_training_events,
        adapter_generated_internal_events_proxy=resource.generated_internal_events,
        adapter_mutable_state_entries_proxy=resource.persistent_state_entries,
        adapter_parameter_entries_proxy=resource.parameter_count,
        adapter_intervention_count_proxy=resource.intervention_count,
        architecture_normal_field_threshold_present=(
            resource.normal_field_threshold_present
        ),
        architecture_normal_field_threshold_crossings=(
            resource.normal_field_threshold_crossings
        ),
        architecture_threshold_bypassed=resource.threshold_bypassed,
        architecture_explicit_assembly_entries=resource.explicit_assembly_entries,
        architecture_typed_head_count=resource.typed_head_count,
        architecture_scalar_reward_observations=(
            resource.scalar_reward_observations
        ),
        architecture_privileged_information=tuple(
            row.value for row in resource.privileged_information
        ),
        decision_use="descriptive-only",
    )
    record.validate()
    return execution, record

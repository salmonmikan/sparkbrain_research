from __future__ import annotations

import json
import math
import time
import tracemalloc
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any, TypeVar

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import ConfirmatoryCondition, ConfirmatoryManifest
from .v06_confirmatory_heldout_common import HeldoutConditionExecution
from .v06_confirmatory_resources import ConditionResourceRecord

RESOURCE_ACCOUNTING_VERSION = "v06-resource-accounting-1"


class ResourceDecisionUse(StrEnum):
    DESCRIPTIVE_ONLY = "descriptive-only"


@dataclass(frozen=True, slots=True)
class ResourceAccountingPolicy:
    """Frozen interpretation of resource measurements.

    Resource values are descriptive in v0.6. They cannot change a capability
    pass/fail result. Completeness, finite values, measurement-method identity,
    and privilege disclosure remain hard execution-integrity requirements.
    """

    version: str = RESOURCE_ACCOUNTING_VERSION
    decision_use: ResourceDecisionUse = ResourceDecisionUse.DESCRIPTIVE_ONLY
    efficiency_affects_capability_result: bool = False
    wall_clock_method: str = "time.perf_counter_ns"
    cpu_time_method: str = "time.process_time_ns"
    peak_memory_method: str = "tracemalloc.get_traced_memory.peak"
    operation_proxy_formula: str = (
        "observed_training_events + generated_internal_events + "
        "intervention_count + normal_field_threshold_crossings"
    )
    mutable_state_scalar_method: str = "adapter-declared parameter_count proxy"
    persistent_state_method: str = "adapter-declared persistent_state_entries proxy"
    output_size_method: str = "canonical semantic execution JSON UTF-8 bytes"

    def validate(self) -> None:
        if self.version != RESOURCE_ACCOUNTING_VERSION:
            raise ValueError("resource accounting version mismatch")
        if self.decision_use is not ResourceDecisionUse.DESCRIPTIVE_ONLY:
            raise ValueError("v0.6 resource accounting must remain descriptive-only")
        if self.efficiency_affects_capability_result:
            raise ValueError("resource efficiency cannot alter v0.6 capability results")
        for name in (
            "wall_clock_method",
            "cpu_time_method",
            "peak_memory_method",
            "operation_proxy_formula",
            "mutable_state_scalar_method",
            "persistent_state_method",
            "output_size_method",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["decision_use"] = self.decision_use.value
        return value

    def policy_hash(self) -> str:
        self.validate()
        return digest(self.state_dict())


RESOURCE_POLICY = ResourceAccountingPolicy()


@dataclass(frozen=True, slots=True)
class NormalizedConditionResourceRecord:
    family_id: str
    seed: int
    condition: ConfirmatoryCondition
    accounting_version: str
    decision_use: ResourceDecisionUse
    observed_external_events: int
    logical_generated_events: int
    intervention_events: int
    mutable_state_scalar_proxy: int
    persistent_state_entry_proxy: int
    logical_operation_proxy_units: int
    wall_clock_ns: int
    process_cpu_ns: int
    peak_traced_memory_bytes: int
    canonical_output_bytes: int
    normal_field_threshold_present: bool
    normal_field_threshold_crossings: int
    threshold_bypassed: bool
    explicit_assembly_entries: int
    typed_head_count: int
    scalar_reward_observations: int
    privileged_information_count: int

    @property
    def key(self) -> tuple[str, int, ConfirmatoryCondition]:
        return (self.family_id, self.seed, self.condition)

    def validate(self) -> None:
        if not self.family_id or self.seed < 0:
            raise ValueError("normalized resource identity must be valid")
        if self.accounting_version != RESOURCE_ACCOUNTING_VERSION:
            raise ValueError("normalized resource accounting version mismatch")
        if self.decision_use is not ResourceDecisionUse.DESCRIPTIVE_ONLY:
            raise ValueError("normalized resource values must remain descriptive-only")
        integer_fields = (
            "observed_external_events",
            "logical_generated_events",
            "intervention_events",
            "mutable_state_scalar_proxy",
            "persistent_state_entry_proxy",
            "logical_operation_proxy_units",
            "wall_clock_ns",
            "process_cpu_ns",
            "peak_traced_memory_bytes",
            "canonical_output_bytes",
            "normal_field_threshold_crossings",
            "explicit_assembly_entries",
            "typed_head_count",
            "scalar_reward_observations",
            "privileged_information_count",
        )
        if any(getattr(self, name) < 0 for name in integer_fields):
            raise ValueError("normalized resource counts must be non-negative")
        expected_proxy = (
            self.observed_external_events
            + self.logical_generated_events
            + self.intervention_events
            + self.normal_field_threshold_crossings
        )
        if self.logical_operation_proxy_units != expected_proxy:
            raise ValueError("logical operation proxy does not match the frozen formula")
        if self.canonical_output_bytes < 1:
            raise ValueError("canonical output size must be positive")
        if self.normal_field_threshold_present and self.threshold_bypassed:
            raise ValueError("a condition cannot both use and bypass Field thresholding")
        if (
            self.normal_field_threshold_crossings > 0
            and not self.normal_field_threshold_present
        ):
            raise ValueError("Field threshold crossings require an ordinary Field threshold")

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["condition"] = self.condition.value
        value["decision_use"] = self.decision_use.value
        return value


@dataclass(frozen=True, slots=True)
class MeasuredConditionExecution:
    execution: HeldoutConditionExecution
    normalized_resource: NormalizedConditionResourceRecord

    def validate(self) -> None:
        self.execution.validate()
        self.normalized_resource.validate()
        if self.execution.resource.key != self.normalized_resource.key:
            raise ValueError("raw and normalized resource identities must match")

    def state_dict(self) -> dict[str, Any]:
        return {
            "execution": self.execution.state_dict(),
            "normalized_resource": self.normalized_resource.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class NormalizedResourceMatrixCoverage:
    expected_record_count: int
    observed_record_count: int
    duplicate_keys: tuple[str, ...]
    missing_keys: tuple[str, ...]
    unexpected_keys: tuple[str, ...]
    invalid_records: tuple[str, ...]
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _canonical_semantic_output_bytes(execution: HeldoutConditionExecution) -> int:
    state = execution.state_dict()
    resource = dict(state["resource"])
    resource["wall_clock_ms"] = 0.0
    state["resource"] = resource
    encoded = json.dumps(
        state,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return len(encoded)


def normalize_resource_record(
    execution: HeldoutConditionExecution,
    *,
    wall_clock_ns: int,
    process_cpu_ns: int,
    peak_traced_memory_bytes: int,
) -> NormalizedConditionResourceRecord:
    execution.validate()
    raw = execution.resource
    raw.validate()
    operation_proxy = (
        raw.observed_training_events
        + raw.generated_internal_events
        + raw.intervention_count
        + raw.normal_field_threshold_crossings
    )
    record = NormalizedConditionResourceRecord(
        family_id=raw.family_id,
        seed=raw.seed,
        condition=raw.condition,
        accounting_version=RESOURCE_ACCOUNTING_VERSION,
        decision_use=ResourceDecisionUse.DESCRIPTIVE_ONLY,
        observed_external_events=raw.observed_training_events,
        logical_generated_events=raw.generated_internal_events,
        intervention_events=raw.intervention_count,
        mutable_state_scalar_proxy=raw.parameter_count,
        persistent_state_entry_proxy=raw.persistent_state_entries,
        logical_operation_proxy_units=operation_proxy,
        wall_clock_ns=wall_clock_ns,
        process_cpu_ns=process_cpu_ns,
        peak_traced_memory_bytes=peak_traced_memory_bytes,
        canonical_output_bytes=_canonical_semantic_output_bytes(execution),
        normal_field_threshold_present=raw.normal_field_threshold_present,
        normal_field_threshold_crossings=raw.normal_field_threshold_crossings,
        threshold_bypassed=raw.threshold_bypassed,
        explicit_assembly_entries=raw.explicit_assembly_entries,
        typed_head_count=raw.typed_head_count,
        scalar_reward_observations=raw.scalar_reward_observations,
        privileged_information_count=len(raw.privileged_information),
    )
    record.validate()
    return record


T = TypeVar("T", bound=HeldoutConditionExecution)


def measure_condition_execution(
    runner: Callable[[], T],
) -> MeasuredConditionExecution:
    """Measure one adapter with one evaluator-owned instrumentation path."""

    RESOURCE_POLICY.validate()
    if tracemalloc.is_tracing():
        raise RuntimeError("resource measurement cannot be nested")
    tracemalloc.start()
    wall_start = time.perf_counter_ns()
    cpu_start = time.process_time_ns()
    try:
        execution = runner()
        process_cpu_ns = time.process_time_ns() - cpu_start
        wall_clock_ns = time.perf_counter_ns() - wall_start
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    measured = MeasuredConditionExecution(
        execution=execution,
        normalized_resource=normalize_resource_record(
            execution,
            wall_clock_ns=wall_clock_ns,
            process_cpu_ns=process_cpu_ns,
            peak_traced_memory_bytes=peak_bytes,
        ),
    )
    measured.validate()
    return measured


def _key_text(key: tuple[str, int, ConfirmatoryCondition]) -> str:
    return f"{key[0]}|{key[1]}|{key[2].value}"


def assess_normalized_resource_matrix(
    manifest: ConfirmatoryManifest,
    records: tuple[NormalizedConditionResourceRecord, ...],
) -> NormalizedResourceMatrixCoverage:
    expected = {
        (family.family_id, seed.seed, condition.condition)
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
    }
    observed = [row.key for row in records]
    counts = Counter(observed)
    duplicates = tuple(
        sorted(_key_text(key) for key, count in counts.items() if count > 1)
    )
    observed_set = set(observed)
    missing = tuple(sorted(_key_text(key) for key in expected - observed_set))
    unexpected = tuple(sorted(_key_text(key) for key in observed_set - expected))
    invalid: list[str] = []
    for row in records:
        try:
            row.validate()
        except ValueError as exc:
            invalid.append(f"{_key_text(row.key)}:{exc}")
    return NormalizedResourceMatrixCoverage(
        expected_record_count=len(expected),
        observed_record_count=len(records),
        duplicate_keys=duplicates,
        missing_keys=missing,
        unexpected_keys=unexpected,
        invalid_records=tuple(sorted(invalid)),
        complete=(
            len(records) == len(expected)
            and not duplicates
            and not missing
            and not unexpected
            and not invalid
        ),
    )


def resource_policy_hash() -> str:
    return RESOURCE_POLICY.policy_hash()


def raw_resource_schema_hash() -> str:
    return digest(
        {
            "model": ConditionResourceRecord.__name__,
            "fields": list(ConditionResourceRecord.__dataclass_fields__),
        }
    )


def normalized_resource_schema_hash() -> str:
    return digest(
        {
            "model": NormalizedConditionResourceRecord.__name__,
            "fields": list(NormalizedConditionResourceRecord.__dataclass_fields__),
        }
    )


def validate_finite_normalized_metrics(
    record: NormalizedConditionResourceRecord,
) -> None:
    record.validate()
    numeric = (
        float(record.wall_clock_ns),
        float(record.process_cpu_ns),
        float(record.peak_traced_memory_bytes),
        float(record.logical_operation_proxy_units),
    )
    if not all(math.isfinite(value) for value in numeric):
        raise ValueError("normalized resource metrics must be finite")

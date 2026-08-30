from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
)
from sparkbrain.evaluation.v06_confirmatory_normalized_resource_v2 import (
    ResourceDecisionPolicyV2,
    deterministic_execution_id_v2,
    measure_condition_execution_v2,
    normalized_resource_schema_hash_v2,
)
from sparkbrain.evaluation.v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
)

_ENVELOPE_HASH = "a" * 64
_SOURCE_SHA = "b" * 40
_MANIFEST_HASH = "c" * 64
_WORLD_HASH = "d" * 64


def _execution(condition: ConfirmatoryCondition) -> HeldoutConditionExecution:
    records = tuple(
        ConfirmatoryResultRecord(
            family_id="development-resource-v2",
            seed=900001,
            condition=condition,
            evidence_domain=domain,
            passed=domain is EvidenceDomain.TAXONOMY_NON_INTERFERENCE,
            metrics=(
                ("self_confirmation_violations", 0.0),
                ("taxonomy_hash_match", 1.0),
            ),
        )
        for domain in EvidenceDomain
    )
    if condition is ConfirmatoryCondition.G4_ASSEMBLY:
        resource = ConditionResourceRecord(
            family_id="development-resource-v2",
            seed=900001,
            condition=condition,
            observed_training_events=12,
            generated_internal_events=3,
            persistent_state_entries=8,
            intervention_count=1,
            parameter_count=8,
            wall_clock_ms=0.0,
            normal_field_threshold_present=False,
            normal_field_threshold_crossings=0,
            threshold_bypassed=True,
            explicit_assembly_entries=2,
            typed_head_count=0,
            scalar_reward_observations=0,
            privileged_information=(
                PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
            ),
        )
    else:
        resource = ConditionResourceRecord(
            family_id="development-resource-v2",
            seed=900001,
            condition=condition,
            observed_training_events=24,
            generated_internal_events=6,
            persistent_state_entries=16,
            intervention_count=2,
            parameter_count=20,
            wall_clock_ms=0.0,
            normal_field_threshold_present=True,
            normal_field_threshold_crossings=6,
            threshold_bypassed=False,
            explicit_assembly_entries=0,
            typed_head_count=0,
            scalar_reward_observations=0,
            privileged_information=(),
        )
    execution = HeldoutConditionExecution(
        family_id="development-resource-v2",
        seed=900001,
        condition=condition,
        world_specification_hash=_WORLD_HASH,
        records=records,
        resource=resource,
        semantic_hash="e" * 64,
    )
    execution.validate()
    return execution


def _execution_id(condition: ConfirmatoryCondition) -> str:
    return deterministic_execution_id_v2(
        envelope_hash=_ENVELOPE_HASH,
        source_git_sha=_SOURCE_SHA,
        manifest_hash=_MANIFEST_HASH,
        world_generation_id="development-only",
        family_id="development-resource-v2",
        seed=900001,
        condition=condition,
        world_specification_hash=_WORLD_HASH,
    )


def test_common_evaluator_measurements_are_separate_from_adapter_proxies() -> None:
    execution, record = measure_condition_execution_v2(
        lambda: _execution(ConfirmatoryCondition.PRIMARY),
        execution_id=_execution_id(ConfirmatoryCondition.PRIMARY),
    )
    assert execution.condition is ConfirmatoryCondition.PRIMARY
    assert record.common_wall_clock_ns >= 0
    assert record.common_process_cpu_ns >= 0
    assert record.common_peak_traced_memory_bytes >= 0
    assert record.common_canonical_execution_bytes > 0
    assert record.common_result_record_count == len(EvidenceDomain)
    assert record.common_resource_record_count == 1
    assert record.adapter_observed_external_events_proxy == 24
    assert record.adapter_generated_internal_events_proxy == 6
    assert record.adapter_mutable_state_entries_proxy == 16
    assert record.adapter_parameter_entries_proxy == 20
    assert record.architecture_normal_field_threshold_present is True
    assert record.architecture_normal_field_threshold_crossings == 6
    assert record.architecture_threshold_bypassed is False
    assert record.decision_use == "descriptive-only"
    assert len(record.record_hash()) == 64


def test_architecture_specific_privilege_remains_explicit() -> None:
    _, record = measure_condition_execution_v2(
        lambda: _execution(ConfirmatoryCondition.G4_ASSEMBLY),
        execution_id=_execution_id(ConfirmatoryCondition.G4_ASSEMBLY),
    )
    assert record.architecture_normal_field_threshold_present is False
    assert record.architecture_threshold_bypassed is True
    assert record.architecture_normal_field_threshold_crossings == 0
    assert record.architecture_explicit_assembly_entries == 2
    assert record.architecture_privileged_information == (
        "explicit-assembly-state",
    )


def test_resource_efficiency_cannot_become_a_capability_gate() -> None:
    policy = ResourceDecisionPolicyV2()
    policy.validate()
    assert policy.efficiency_affects_capability_pass_fail is False
    assert policy.common_measurements_are_descriptive is True
    assert policy.adapter_proxies_are_descriptive is True
    assert policy.architecture_specific_values_are_descriptive is True
    with pytest.raises(ValueError, match="must not alter"):
        replace(policy, efficiency_affects_capability_pass_fail=True).validate()
    with pytest.raises(ValueError, match="cannot weaken"):
        replace(policy, missing_record_is_execution_failure=False).validate()


def test_invalid_threshold_mode_and_nonfinite_values_fail_closed() -> None:
    _, record = measure_condition_execution_v2(
        lambda: _execution(ConfirmatoryCondition.PRIMARY),
        execution_id=_execution_id(ConfirmatoryCondition.PRIMARY),
    )
    with pytest.raises(ValueError, match="cannot both be active"):
        replace(
            record,
            architecture_threshold_bypassed=True,
        ).validate()
    with pytest.raises(ValueError, match="finite and non-negative"):
        replace(record, common_wall_clock_ns=-1).validate()
    with pytest.raises(ValueError, match="descriptive-only"):
        replace(record, decision_use="pass-fail").validate()


def test_normalized_schema_and_execution_identity_are_deterministic() -> None:
    assert _execution_id(ConfirmatoryCondition.PRIMARY) == _execution_id(
        ConfirmatoryCondition.PRIMARY
    )
    assert _execution_id(ConfirmatoryCondition.PRIMARY) != _execution_id(
        ConfirmatoryCondition.G4_ASSEMBLY
    )
    assert len(normalized_resource_schema_hash_v2()) == 64

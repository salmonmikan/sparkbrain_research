from __future__ import annotations

from dataclasses import replace

import pytest
from test_capability_staging_development_fixture import (
    DevelopmentCapabilityWorld,
)
from test_capability_staging_development_fixture import (
    _run as run_development_condition,
)

from sparkbrain.evaluation.v06_confirmatory import ConfirmatoryCondition
from sparkbrain.evaluation.v06_confirmatory_resource_accounting import (
    RESOURCE_POLICY,
    ResourceDecisionUse,
    measure_condition_execution,
    normalized_resource_schema_hash,
    raw_resource_schema_hash,
    resource_policy_hash,
)


def test_resource_policy_is_frozen_as_descriptive_only() -> None:
    RESOURCE_POLICY.validate()
    assert RESOURCE_POLICY.decision_use is ResourceDecisionUse.DESCRIPTIVE_ONLY
    assert RESOURCE_POLICY.efficiency_affects_capability_result is False
    assert RESOURCE_POLICY.common_evaluator_measurements == (
        "wall_clock_ns",
        "process_cpu_ns",
        "peak_traced_memory_bytes",
        "canonical_output_bytes",
    )
    assert all(
        name.startswith("adapter_")
        for name in RESOURCE_POLICY.descriptive_adapter_proxies
    )
    assert set(RESOURCE_POLICY.common_evaluator_measurements).isdisjoint(
        RESOURCE_POLICY.descriptive_adapter_proxies
    )
    assert len(resource_policy_hash()) == 64
    assert len(raw_resource_schema_hash()) == 64
    assert len(normalized_resource_schema_hash()) == 64


@pytest.mark.parametrize("condition", tuple(ConfirmatoryCondition))
def test_one_evaluator_measurement_path_covers_all_eight_conditions(
    condition: ConfirmatoryCondition,
) -> None:
    world = DevelopmentCapabilityWorld()
    measured = measure_condition_execution(
        lambda: run_development_condition(world, condition)
    )
    measured.validate()
    normalized = measured.normalized_resource
    raw = measured.execution.resource
    assert normalized.key == raw.key
    assert normalized.decision_use is ResourceDecisionUse.DESCRIPTIVE_ONLY
    assert (
        normalized.adapter_observed_training_event_proxy
        == raw.observed_training_events
    )
    assert normalized.adapter_generated_event_proxy == raw.generated_internal_events
    assert normalized.adapter_intervention_event_proxy == raw.intervention_count
    assert normalized.adapter_mutable_state_scalar_proxy == raw.parameter_count
    assert (
        normalized.adapter_persistent_state_entry_proxy
        == raw.persistent_state_entries
    )
    assert normalized.adapter_logical_operation_proxy_units == (
        raw.observed_training_events
        + raw.generated_internal_events
        + raw.intervention_count
        + raw.normal_field_threshold_crossings
    )
    assert normalized.wall_clock_ns >= 0
    assert normalized.process_cpu_ns >= 0
    assert normalized.peak_traced_memory_bytes >= 0
    assert normalized.canonical_output_bytes > 0


def test_architecture_specific_values_are_separate_from_common_measurements() -> None:
    world = DevelopmentCapabilityWorld()
    primary = measure_condition_execution(
        lambda: run_development_condition(world, ConfirmatoryCondition.PRIMARY)
    ).normalized_resource
    g4 = measure_condition_execution(
        lambda: run_development_condition(world, ConfirmatoryCondition.G4_ASSEMBLY)
    ).normalized_resource
    g5 = measure_condition_execution(
        lambda: run_development_condition(world, ConfirmatoryCondition.G5_TYPED)
    ).normalized_resource

    assert primary.normal_field_threshold_present is True
    assert primary.threshold_bypassed is False
    assert primary.explicit_assembly_entries == 0
    assert primary.typed_head_count == 0
    assert primary.scalar_reward_observations == 0

    assert g4.normal_field_threshold_present is False
    assert g4.threshold_bypassed is True
    assert g4.explicit_assembly_entries >= 1
    assert g4.typed_head_count == 0

    assert g5.normal_field_threshold_present is False
    assert g5.threshold_bypassed is True
    assert g5.typed_head_count >= 3
    assert g5.scalar_reward_observations >= 1


def test_resource_efficiency_cannot_be_relabelled_as_a_capability_gate() -> None:
    with pytest.raises(ValueError, match="descriptive-only"):
        replace(
            RESOURCE_POLICY,
            decision_use="capability-gate",  # type: ignore[arg-type]
        ).validate()
    with pytest.raises(ValueError, match="cannot alter"):
        replace(
            RESOURCE_POLICY,
            efficiency_affects_capability_result=True,
        ).validate()


def test_nested_resource_measurement_fails_closed() -> None:
    import tracemalloc

    tracemalloc.start()
    try:
        with pytest.raises(RuntimeError, match="cannot be nested"):
            measure_condition_execution(
                lambda: run_development_condition(
                    DevelopmentCapabilityWorld(),
                    ConfirmatoryCondition.PRIMARY,
                )
            )
    finally:
        tracemalloc.stop()

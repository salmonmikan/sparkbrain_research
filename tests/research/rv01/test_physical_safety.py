from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.physical_safety import (
    PhysicalExecutionBudget,
    run_physical_safety_suite,
)


def test_normal_physical_chain_completes_inside_budget() -> None:
    suite = run_physical_safety_suite()
    row = suite.normal_chain
    assert row.later_units == (1, 2, 3)
    assert row.budget_exceeded is False
    assert row.halt_reason == "queue_drained"
    assert row.connection_state_hash_before == row.connection_state_hash_after
    assert suite.assessment.normal_chain_completes_within_budget is True


def test_recurrent_cycle_persists_to_horizon_without_intrinsic_stop() -> None:
    suite = run_physical_safety_suite()
    row = suite.finite_horizon_cycle
    assert row.budget_exceeded is False
    assert row.halt_reason == "horizon_reached"
    assert row.generated_spike_count > 10
    assert row.final_queue_size > 0
    assert suite.assessment.recurrent_cycle_persists_to_finite_horizon is True
    assert (
        suite.assessment.recurrent_cycle_is_not_intrinsically_self_terminating
        is True
    )
    assert suite.assessment.intrinsic_runtime_safety_supported is False


def test_spike_budget_halts_recurrent_cycle() -> None:
    suite = run_physical_safety_suite()
    row = suite.budgeted_cycle
    assert row.budget_exceeded is True
    assert row.halt_reason == "spike_budget_exceeded"
    assert row.total_spike_count > 10
    assert row.final_queue_size > 0
    assert suite.assessment.spike_budget_halts_cycle is True
    assert suite.assessment.external_execution_guard_required is True


def test_breaking_one_cycle_edge_allows_queue_to_drain() -> None:
    suite = run_physical_safety_suite()
    row = suite.broken_cycle
    assert row.later_units == (1, 2)
    assert row.budget_exceeded is False
    assert row.halt_reason == "queue_drained"
    assert row.final_queue_size == 0
    assert suite.assessment.broken_cycle_drains_without_budget_failure is True


def test_excessive_active_fanout_is_rejected_before_external_input() -> None:
    suite = run_physical_safety_suite()
    row = suite.fanout_preflight_rejection
    assert row.maximum_active_fanout_observed == 6
    assert row.budget_exceeded is True
    assert row.halt_reason == "active_fanout_budget_exceeded"
    assert row.external_input_count == 0
    assert row.total_spike_count == 0
    assert (
        suite.assessment.excessive_active_fanout_fails_closed_before_execution
        is True
    )


def test_queue_budget_halts_high_fanout_after_cue() -> None:
    suite = run_physical_safety_suite()
    row = suite.queue_budget_rejection
    assert row.maximum_active_fanout_observed == 6
    assert row.budget_exceeded is True
    assert row.halt_reason == "queue_budget_exceeded"
    assert row.external_input_count == 1
    assert row.maximum_queue_size_observed > 3
    assert suite.assessment.queue_budget_halts_safe_fanout_execution is True


def test_local_path_failure_does_not_destroy_disjoint_route() -> None:
    suite = run_physical_safety_suite()
    assert suite.failed_target_path.later_units == (1,)
    assert suite.unaffected_control_path.later_units == (5, 6, 7)
    assert (
        suite.assessment.local_path_failure_does_not_destroy_disjoint_path
        is True
    )


def test_plasticity_stress_respects_weight_and_delay_bounds() -> None:
    suite = run_physical_safety_suite()
    row = suite.plasticity_bounds
    assert row.finite_weight_count == row.connection_count
    assert row.finite_delay_count == row.connection_count
    assert (
        row.configured_minimum_weight
        <= row.observed_minimum_weight
        <= row.observed_maximum_weight
        <= row.configured_maximum_weight
    )
    assert row.observed_minimum_delay_ms > 0.0
    assert row.observed_minimum_weight == pytest.approx(
        row.configured_minimum_weight
    )
    assert row.observed_maximum_weight == pytest.approx(
        row.configured_maximum_weight
    )
    assert suite.assessment.plasticity_weight_bounds_respected is True
    assert (
        suite.assessment.plasticity_delay_values_remain_positive_and_finite
        is True
    )
    assert suite.assessment.upper_and_lower_weight_saturation_observed is True


def test_endogenous_stress_cannot_write_physical_connections() -> None:
    suite = run_physical_safety_suite()
    row = suite.plasticity_bounds
    assert row.ignored_endogenous_observations == 128
    assert row.endogenous_stress_changed_connections is False
    assert (
        row.connection_hash_before_endogenous_stress
        == row.connection_hash_after_endogenous_stress
    )
    assert suite.assessment.endogenous_activity_cannot_write_connections is True


def test_all_logical_resource_records_are_complete_unique_and_deterministic() -> None:
    first = run_physical_safety_suite()
    second = run_physical_safety_suite()
    assert len(first.resource_records) == 8
    assert len({row.condition_id for row in first.resource_records}) == 8
    for row in first.resource_records:
        row.validate()
        assert row.unit_count > 0
        assert row.connection_count > 0
        assert row.execution_slice_count >= 0
        assert row.maximum_queue_size_observed >= row.final_queue_size
    assert first == second
    assert first.suite_hash == second.suite_hash
    assert first.assessment.resource_records_complete_and_unique is True


def test_invalid_execution_budgets_fail_closed() -> None:
    with pytest.raises(ValueError, match="horizon_ms"):
        PhysicalExecutionBudget(horizon_ms=0.0).validate()
    with pytest.raises(ValueError, match="time_slice_ms"):
        PhysicalExecutionBudget(horizon_ms=10.0, time_slice_ms=0.0).validate()
    with pytest.raises(ValueError, match="maximum_total_spikes"):
        PhysicalExecutionBudget(horizon_ms=10.0, maximum_total_spikes=0).validate()
    with pytest.raises(ValueError, match="maximum_queue_size"):
        PhysicalExecutionBudget(horizon_ms=10.0, maximum_queue_size=0).validate()
    with pytest.raises(ValueError, match="maximum_active_fanout"):
        PhysicalExecutionBudget(horizon_ms=10.0, maximum_active_fanout=0).validate()


def test_safety_guard_has_no_learning_or_cognitive_taxonomy() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "physical_safety.py"
    )
    source = path.read_text(encoding="utf-8")
    for forbidden in (
        "LocalTemporalExpectation",
        "SparseLocalTransitionAdaptation",
        "EndogenousPulseProposal",
        "meaning_state",
        "correct_action",
        "scalar_reward",
        "assembly_id",
    ):
        assert forbidden not in source
    assert "observe_external" not in source.split("def run_bounded_physical_field", 1)[1].split("def _trained_field", 1)[0]
    assert run_physical_safety_suite().assessment.safety_layer_has_no_learned_cognitive_state is True


def test_r01_11_reports_external_guard_not_intrinsic_safety() -> None:
    assessment = run_physical_safety_suite().assessment
    assert assessment.engineering_candidate is True
    assert assessment.intrinsic_runtime_safety_supported is False
    assert assessment.external_execution_guard_required is True

from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.physical_persistence_locus import (
    run_physical_persistence_locus_suite,
)


def test_full_learned_connection_state_reproduces_physical_chain() -> None:
    suite = run_physical_persistence_locus_suite()
    row = suite.trained
    assert row.later_units == (1, 2, 3)
    assert row.later_times_ms == pytest.approx((105.375, 110.75, 116.125))
    assert row.full_chain_generated is True
    assert suite.assessment.trained_connection_state_generates_chain is True


def test_weight_reset_removes_chain_even_when_learned_delays_remain() -> None:
    suite = run_physical_persistence_locus_suite()
    row = suite.weight_reset
    assert row.later_units == ()
    assert row.path_delays_ms == pytest.approx((5.375, 5.375, 5.375))
    assert all(weight == pytest.approx(0.05) for weight in row.path_weights)
    assert suite.assessment.weight_reset_removes_chain is True
    assert suite.assessment.weight_state_is_necessary_canonical_carrier is True


def test_learned_weights_alone_transfer_order_with_naive_delays() -> None:
    suite = run_physical_persistence_locus_suite()
    row = suite.weights_only_transplant
    assert row.later_units == (1, 2, 3)
    assert row.later_times_ms == pytest.approx((108.0, 116.0, 124.0))
    assert row.path_delays_ms == pytest.approx((8.0, 8.0, 8.0))
    assert suite.assessment.learned_weights_alone_transfer_order is True
    assert suite.assessment.weight_state_is_sufficient_canonical_carrier is True


def test_learned_delays_alone_do_not_transfer_chain() -> None:
    suite = run_physical_persistence_locus_suite()
    row = suite.delays_only_transplant
    assert row.later_units == ()
    assert row.path_delays_ms == pytest.approx((5.375, 5.375, 5.375))
    assert all(weight == pytest.approx(0.05) for weight in row.path_weights)
    assert suite.assessment.learned_delays_alone_do_not_transfer_chain is True


def test_delay_reset_preserves_order_but_changes_temporal_calibration() -> None:
    suite = run_physical_persistence_locus_suite()
    trained = suite.trained
    reset = suite.delay_reset
    assert reset.later_units == trained.later_units == (1, 2, 3)
    assert reset.later_times_ms == pytest.approx((108.0, 116.0, 124.0))
    assert reset.later_times_ms != trained.later_times_ms
    assert suite.assessment.delay_reset_preserves_order is True
    assert suite.assessment.learned_delays_change_timing is True
    assert suite.assessment.delay_state_is_temporal_calibration_carrier is True


def test_full_connection_transplant_moves_units_and_exact_timing() -> None:
    suite = run_physical_persistence_locus_suite()
    donor = suite.trained
    receiver = suite.full_connection_transplant
    assert receiver.later_units == donor.later_units
    assert receiver.later_times_ms == donor.later_times_ms
    assert receiver.weight_state_hash == donor.weight_state_hash
    assert receiver.delay_state_hash == donor.delay_state_hash
    assert suite.assessment.full_connection_transplant_matches_trace is True


def test_dynamic_unit_state_alone_does_not_transfer_learned_chain() -> None:
    suite = run_physical_persistence_locus_suite()
    assert suite.dynamic_state_only.later_units == ()
    assert (
        suite.training_dynamic_hash_before
        == suite.training_dynamic_hash_after
    )
    assert suite.assessment.training_does_not_write_unit_dynamic_state is True
    assert suite.assessment.dynamic_state_only_does_not_transfer_chain is True


def test_working_trace_only_does_not_drive_field_execution() -> None:
    suite = run_physical_persistence_locus_suite()
    row = suite.working_trace_only
    assert row.controller_trace_count > 0
    assert row.later_units == ()
    assert suite.assessment.working_trace_only_does_not_transfer_chain is True


def test_receptor_and_fixed_structure_are_not_learned_carriers() -> None:
    suite = run_physical_persistence_locus_suite()
    assert suite.receptor_state_only.later_units == ()
    assert suite.structure_only.later_units == ()
    assert suite.training_receptor_hash_before == suite.training_receptor_hash_after
    assert suite.training_structure_hash_before == suite.training_structure_hash_after
    assert suite.assessment.receptor_state_only_does_not_transfer_chain is True
    assert suite.assessment.fixed_structure_only_does_not_transfer_chain is True
    assert (
        suite.assessment.training_does_not_change_receptors_or_edge_structure
        is True
    )


def test_plasticity_can_be_disabled_after_learning_without_erasing_execution() -> None:
    suite = run_physical_persistence_locus_suite()
    trained = suite.trained
    frozen = suite.plasticity_disabled_after_learning
    assert frozen.later_units == trained.later_units == (1, 2, 3)
    assert frozen.later_times_ms == trained.later_times_ms
    assert frozen.plasticity_flag_hash != trained.plasticity_flag_hash
    assert suite.assessment.ongoing_plasticity_not_required_for_execution is True


def test_r01_08_supports_edge_localized_not_broad_dynamic_persistence() -> None:
    assessment = run_physical_persistence_locus_suite().assessment
    assert assessment.edge_localized_physical_carrier_supported is True
    assert assessment.broad_distributed_dynamic_carrier_supported is False
    assert assessment.pairwise_physical_storage_limitation is True
    assert assessment.no_g1_or_g2_runtime_required is True
    assert assessment.engineering_candidate is True


def test_persistence_locus_route_imports_no_g1_or_g2_runtime() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "physical_persistence_locus.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "LocalTemporalExpectation" not in source
    assert "SparseLocalTransitionAdaptation" not in source
    assert "EndogenousPulseProposal" not in source


def test_physical_persistence_locus_suite_is_deterministic() -> None:
    first = run_physical_persistence_locus_suite()
    second = run_physical_persistence_locus_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash

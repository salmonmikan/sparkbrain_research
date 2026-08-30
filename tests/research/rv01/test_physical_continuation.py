from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.physical_continuation import (
    run_physical_continuation_suite,
)


def test_learned_physical_connections_generate_a_real_field_chain() -> None:
    suite = run_physical_continuation_suite()
    row = suite.trained
    assert row.total_spike_units == (0, 1, 2, 3)
    assert row.later_units == (1, 2, 3)
    assert row.later_times_ms == pytest.approx((105.375, 110.75, 116.125))
    assert suite.assessment.trained_field_continues is True


def test_untrained_uniform_field_does_not_continue_after_the_same_cue() -> None:
    suite = run_physical_continuation_suite()
    row = suite.untrained
    assert row.total_spike_units == (0,)
    assert row.later_units == ()
    assert suite.assessment.untrained_field_does_not_continue is True


def test_different_external_history_changes_later_physical_dynamics() -> None:
    suite = run_physical_continuation_suite()
    main = suite.trained
    alternate = suite.alternate_history
    assert main.cue_unit_id == alternate.cue_unit_id == 0
    assert main.initial_dynamic_state_hash == alternate.initial_dynamic_state_hash
    assert main.later_units == (1, 2, 3)
    assert alternate.later_units == (2, 1, 3)
    assert alternate.later_units != main.later_units
    assert suite.assessment.different_physical_history_changes_continuation is True


def test_connection_reset_removes_the_learned_continuation() -> None:
    suite = run_physical_continuation_suite()
    assert suite.connection_reset.total_spike_units == (0,)
    assert suite.connection_reset.later_units == ()
    assert suite.assessment.connection_reset_removes_continuation is True


def test_connection_state_transplant_moves_the_learned_chain() -> None:
    suite = run_physical_continuation_suite()
    donor = suite.trained
    receiver = suite.connection_transplant
    assert receiver.initial_dynamic_state_hash == donor.initial_dynamic_state_hash
    assert receiver.connection_state_hash == donor.connection_state_hash
    assert receiver.later_units == donor.later_units == (1, 2, 3)
    assert receiver.later_times_ms == donor.later_times_ms
    assert suite.assessment.connection_transplant_transfers_continuation is True


def test_short_lived_unit_traces_are_not_needed_after_physical_learning() -> None:
    suite = run_physical_continuation_suite()
    assert suite.trained.later_units == (1, 2, 3)
    assert suite.assessment.unit_trace_reset_preserves_continuation is True


def test_endogenous_only_training_cannot_write_the_physical_chain() -> None:
    suite = run_physical_continuation_suite()
    assert suite.endogenous_only_training.total_spike_units == (0,)
    assert suite.endogenous_only_training.later_units == ()
    assert (
        suite.assessment.endogenous_only_training_cannot_create_continuation
        is True
    )


def test_all_comparisons_start_from_the_same_dynamic_field_state() -> None:
    suite = run_physical_continuation_suite()
    hashes = {
        row.initial_dynamic_state_hash
        for row in (
            suite.trained,
            suite.untrained,
            suite.alternate_history,
            suite.connection_reset,
            suite.connection_transplant,
            suite.endogenous_only_training,
        )
    }
    assert len(hashes) == 1
    assert suite.assessment.initial_dynamic_states_match is True


def test_physical_continuation_route_imports_no_g1_or_g2_runtime() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "physical_continuation.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "LocalTemporalExpectation" not in source
    assert "SparseLocalTransitionAdaptation" not in source
    assert "EndogenousPulseProposal" not in source
    assert suite_no_g1_g2() is True


def suite_no_g1_g2() -> bool:
    return run_physical_continuation_suite().assessment.no_g1_or_g2_runtime_required


def test_r01_04_physical_continuation_candidate_is_complete() -> None:
    assessment = run_physical_continuation_suite().assessment
    assert assessment.trained_field_continues is True
    assert assessment.untrained_field_does_not_continue is True
    assert assessment.different_physical_history_changes_continuation is True
    assert assessment.connection_reset_removes_continuation is True
    assert assessment.connection_transplant_transfers_continuation is True
    assert assessment.unit_trace_reset_preserves_continuation is True
    assert assessment.endogenous_only_training_cannot_create_continuation is True
    assert assessment.initial_dynamic_states_match is True
    assert assessment.no_g1_or_g2_runtime_required is True
    assert assessment.engineering_candidate is True


def test_physical_continuation_suite_is_deterministic() -> None:
    first = run_physical_continuation_suite()
    second = run_physical_continuation_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash

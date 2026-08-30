from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.physical_revision import (
    NEW_SEQUENCE,
    OLD_SEQUENCE,
    run_physical_revision_suite,
)


def test_acquisition_selects_only_the_old_physical_path() -> None:
    suite = run_physical_revision_suite()
    row = suite.acquisition
    assert row.generated_units == OLD_SEQUENCE[1:]
    assert row.old_path_completed is True
    assert row.new_path_completed is False
    assert row.old_gateway_weight == pytest.approx(0.9597959895689502)
    assert row.new_gateway_weight == pytest.approx(0.0)
    assert suite.assessment.acquisition_selects_old_path is True


def test_reversal_switches_to_the_new_path_without_explicit_counters() -> None:
    suite = run_physical_revision_suite()
    row = suite.reversed_state
    assert row.generated_units == NEW_SEQUENCE[1:]
    assert row.old_path_completed is False
    assert row.new_path_completed is True
    assert row.old_gateway_weight == pytest.approx(0.11065306597126337)
    assert row.new_gateway_weight == pytest.approx(1.2130613194252668)
    assert suite.assessment.reversal_crossing_episode == 3
    assert suite.assessment.reversal_selects_new_path is True


def test_reacquisition_switches_back_to_the_old_path() -> None:
    suite = run_physical_revision_suite()
    row = suite.reacquired_state
    assert row.generated_units == OLD_SEQUENCE[1:]
    assert row.old_path_completed is True
    assert row.new_path_completed is False
    assert row.old_gateway_weight == pytest.approx(1.25)
    assert row.new_gateway_weight == pytest.approx(0.36391839582758)
    assert suite.assessment.reacquisition_crossing_episode == 3
    assert suite.assessment.reacquisition_selects_old_path is True


def test_intermediate_reversal_and_reacquisition_steps_are_preserved() -> None:
    suite = run_physical_revision_suite()
    assert len(suite.reversal_steps) == 4
    assert len(suite.reacquisition_steps) == 4

    assert suite.reversal_steps[0].generated_units == (1,)
    assert suite.reversal_steps[1].generated_units == (1,)
    assert suite.reversal_steps[2].generated_units == NEW_SEQUENCE[1:]
    assert suite.reversal_steps[3].generated_units == NEW_SEQUENCE[1:]

    assert suite.reacquisition_steps[0].generated_units == NEW_SEQUENCE[1:]
    assert suite.reacquisition_steps[1].new_path_completed is True
    assert suite.reacquisition_steps[2].generated_units == OLD_SEQUENCE[1:]
    assert suite.reacquisition_steps[3].generated_units == OLD_SEQUENCE[1:]


def test_stable_world_does_not_create_the_unobserved_alternative() -> None:
    suite = run_physical_revision_suite()
    row = suite.stable_control
    assert row.old_path_completed is True
    assert row.new_path_completed is False
    assert row.generated_units == OLD_SEQUENCE[1:]
    assert suite.assessment.stable_world_does_not_invent_new_path is True


def test_potentiation_without_local_competition_retains_both_paths() -> None:
    suite = run_physical_revision_suite()
    row = suite.potentiation_only_control
    assert row.old_path_completed is True
    assert row.new_path_completed is True
    assert set(OLD_SEQUENCE[1:]).issubset(row.generated_units)
    assert set(NEW_SEQUENCE[1:]).issubset(row.generated_units)
    assert suite.assessment.potentiation_only_fails_to_remove_old_path is True


def test_endogenous_only_new_history_cannot_revise_physical_connections() -> None:
    suite = run_physical_revision_suite()
    row = suite.endogenous_only_reversal
    assert suite.endogenous_ignored_count == 16
    assert row.old_path_completed is True
    assert row.new_path_completed is False
    assert row.generated_units == OLD_SEQUENCE[1:]
    assert (
        suite.assessment.endogenous_only_experience_cannot_revamp_connections
        is True
    )


def test_connection_reset_removes_and_transplant_moves_reversed_behavior() -> None:
    suite = run_physical_revision_suite()
    reset = suite.reset_control
    transplant = suite.reversed_transplant
    assert reset.generated_units == ()
    assert reset.old_path_completed is False
    assert reset.new_path_completed is False
    assert transplant.generated_units == NEW_SEQUENCE[1:]
    assert transplant.connection_state_hash == suite.reversed_state.connection_state_hash
    assert suite.assessment.connection_reset_removes_acquired_behavior is True
    assert suite.assessment.reversed_connection_transplant_moves_behavior is True


def test_all_phase_probes_start_from_the_same_naive_dynamic_state() -> None:
    suite = run_physical_revision_suite()
    rows = (
        suite.acquisition,
        *suite.reversal_steps,
        *suite.reacquisition_steps,
        suite.stable_control,
        suite.potentiation_only_control,
        suite.endogenous_only_reversal,
        suite.reset_control,
        suite.reversed_transplant,
    )
    assert len({row.initial_dynamic_state_hash for row in rows}) == 1
    assert suite.assessment.initial_dynamic_states_match is True


def test_revision_controller_has_no_explicit_correctness_or_path_counters() -> None:
    suite = run_physical_revision_suite()
    lowered = str(suite.competitive_controller_state).lower()
    for forbidden in (
        "confirmed_count",
        "contradicted_count",
        "correct_target",
        "correct_action",
        "relation_table",
        "path_score",
        "reward",
    ):
        assert forbidden not in lowered
    assert suite.assessment.no_confirmed_or_contradicted_counters is True


def test_physical_revision_runtime_imports_no_g1_or_g2() -> None:
    root = Path(__file__).parents[3] / "src" / "sparkbrain" / "research" / "rv01"
    for filename in ("competitive_field_plasticity.py", "physical_revision.py"):
        source = (root / filename).read_text(encoding="utf-8")
        assert "LocalTemporalExpectation" not in source
        assert "SparseLocalTransitionAdaptation" not in source
        assert "EndogenousPulseProposal" not in source


def test_r01_07_physical_revision_candidate_is_complete() -> None:
    assessment = run_physical_revision_suite().assessment
    assert assessment.acquisition_selects_old_path is True
    assert assessment.reversal_selects_new_path is True
    assert assessment.reacquisition_selects_old_path is True
    assert assessment.stable_world_does_not_invent_new_path is True
    assert assessment.potentiation_only_fails_to_remove_old_path is True
    assert assessment.endogenous_only_experience_cannot_revamp_connections is True
    assert assessment.connection_reset_removes_acquired_behavior is True
    assert assessment.reversed_connection_transplant_moves_behavior is True
    assert assessment.reversal_crossing_episode == 3
    assert assessment.reacquisition_crossing_episode == 3
    assert assessment.initial_dynamic_states_match is True
    assert assessment.no_confirmed_or_contradicted_counters is True
    assert assessment.no_g1_or_g2_runtime_required is True
    assert assessment.engineering_candidate is True


def test_physical_revision_suite_is_deterministic() -> None:
    first = run_physical_revision_suite()
    second = run_physical_revision_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash

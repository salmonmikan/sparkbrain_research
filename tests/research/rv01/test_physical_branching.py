from __future__ import annotations

import math
from pathlib import Path

import pytest

from sparkbrain.research.rv01.physical_branching import (
    BASE_DELAY_MS,
    BASE_WEIGHT,
    BRANCH_A,
    BRANCH_B,
    run_physical_branching_suite,
)


def test_equal_histories_generate_both_physical_branches() -> None:
    suite = run_physical_branching_suite()
    row = suite.equal
    assert row.generated_units == (1, 2, 3, 4, 5)
    assert row.branch_a_completed is True
    assert row.branch_b_completed is True
    assert row.both_branches_completed is True
    assert row.branch_a.divergence_weight == pytest.approx(
        row.branch_b.divergence_weight
    )
    assert row.branch_a.divergence_delay_ms == pytest.approx(
        row.branch_b.divergence_delay_ms
    )
    assert suite.assessment.equal_exposure_preserves_both_branches is True


def test_mild_exposure_bias_preserves_weaker_branch_with_graded_physics() -> None:
    suite = run_physical_branching_suite()
    row = suite.mildly_biased
    increment = 0.25 * math.exp(-5.0 / 10.0)
    assert row.exposure_counts == (3, 2)
    assert row.branch_a.divergence_weight == pytest.approx(
        BASE_WEIGHT + 3 * increment
    )
    assert row.branch_b.divergence_weight == pytest.approx(
        BASE_WEIGHT + 2 * increment
    )
    assert row.branch_a.divergence_delay_ms == pytest.approx(5.375)
    assert row.branch_b.divergence_delay_ms == pytest.approx(5.75)
    assert row.branch_a_completed is True
    assert row.branch_b_completed is True
    assert row.generated_times_ms[row.generated_units.index(BRANCH_A[2])] < (
        row.generated_times_ms[row.generated_units.index(BRANCH_B[2])]
    )
    assert suite.assessment.mild_bias_preserves_weaker_branch is True
    assert suite.assessment.mild_bias_is_physically_graded is True


def test_single_history_does_not_invent_unobserved_second_branch() -> None:
    suite = run_physical_branching_suite()
    row = suite.single_branch_a
    assert row.generated_units == (1, 2, 4)
    assert row.branch_a_completed is True
    assert row.branch_b_completed is False
    assert row.branch_b.divergence_weight == pytest.approx(BASE_WEIGHT)
    assert row.branch_b.divergence_delay_ms == pytest.approx(BASE_DELAY_MS)
    assert suite.assessment.single_history_does_not_invent_second_branch is True


def test_untrained_field_has_no_branch_completion() -> None:
    suite = run_physical_branching_suite()
    row = suite.untrained
    assert row.generated_units == ()
    assert row.branch_a_completed is False
    assert row.branch_b_completed is False
    assert suite.assessment.untrained_field_has_no_branch_completion is True


def test_targeted_branch_a_suppression_preserves_branch_b() -> None:
    suite = run_physical_branching_suite()
    row = suite.suppress_branch_a
    assert row.suppressed_edge == (1, 2)
    assert row.branch_a_completed is False
    assert row.branch_b_completed is True
    assert 2 not in row.generated_units
    assert 4 not in row.generated_units
    assert 3 in row.generated_units
    assert 5 in row.generated_units
    assert suite.assessment.targeted_branch_a_suppression_is_selective is True


def test_targeted_branch_b_suppression_preserves_branch_a() -> None:
    suite = run_physical_branching_suite()
    row = suite.suppress_branch_b
    assert row.suppressed_edge == (1, 3)
    assert row.branch_a_completed is True
    assert row.branch_b_completed is False
    assert 2 in row.generated_units
    assert 4 in row.generated_units
    assert 3 not in row.generated_units
    assert 5 not in row.generated_units
    assert suite.assessment.targeted_branch_b_suppression_is_selective is True


def test_all_branch_conditions_share_current_cue_and_naive_dynamic_state() -> None:
    suite = run_physical_branching_suite()
    rows = (
        suite.equal,
        suite.mildly_biased,
        suite.single_branch_a,
        suite.untrained,
        suite.suppress_branch_a,
        suite.suppress_branch_b,
    )
    assert {row.cue_signature for row in rows} == {(100.0, 0)}
    assert len({row.initial_dynamic_state_hash for row in rows}) == 1
    assert suite.assessment.same_cue_and_dynamic_state is True


def test_branching_runtime_uses_no_g1_g2_or_explicit_winner() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "physical_branching.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "LocalTemporalExpectation" not in source
    assert "SparseLocalTransitionAdaptation" not in source
    assert "EndogenousPulseProposal" not in source
    for forbidden in (
        "winner_id",
        "correct_branch",
        "branch_reward",
        "chosen_branch",
    ):
        assert forbidden not in source


def test_r01_06_supports_coactive_ambiguity_not_competitive_resolution() -> None:
    assessment = run_physical_branching_suite().assessment
    assert assessment.equal_exposure_preserves_both_branches is True
    assert assessment.mild_bias_preserves_weaker_branch is True
    assert assessment.mild_bias_is_physically_graded is True
    assert assessment.single_history_does_not_invent_second_branch is True
    assert assessment.untrained_field_has_no_branch_completion is True
    assert assessment.targeted_branch_a_suppression_is_selective is True
    assert assessment.targeted_branch_b_suppression_is_selective is True
    assert assessment.same_cue_and_dynamic_state is True
    assert assessment.no_explicit_winner_or_branch_runtime_state is True
    assert assessment.coactive_ambiguity_supported is True
    assert assessment.competitive_resolution_supported is False
    assert assessment.engineering_candidate is True


def test_physical_branching_suite_is_deterministic() -> None:
    first = run_physical_branching_suite()
    second = run_physical_branching_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash

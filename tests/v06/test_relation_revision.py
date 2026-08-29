from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_revision_probe import (
    run_canonical_revision_suite,
    run_revision_condition,
    run_stable_control,
)


def test_acquisition_stabilizes_only_the_initial_anonymous_link() -> None:
    suite = run_canonical_revision_suite()
    row = suite.revision.acquisition
    assert row.boundary_count == 3
    assert row.old_consistent_count == 3
    assert row.old_inconsistent_count == 0
    assert row.old_reliability == pytest.approx(0.8)
    assert row.new_consistent_count == 0
    assert row.new_reliability is None
    assert suite.assessment.acquired_old_relation is True


def test_reversal_shifts_external_consistency_to_the_new_raw_target() -> None:
    suite = run_canonical_revision_suite()
    row = suite.revision.reversal
    assert row.boundary_count == 6
    assert row.link_count == 2
    assert row.old_consistent_count == 3
    assert row.old_inconsistent_count == 3
    assert row.old_reliability == pytest.approx(0.5)
    assert row.new_consistent_count == 3
    assert row.new_inconsistent_count == 0
    assert row.new_reliability == pytest.approx(0.8)
    assert suite.assessment.reversed_to_new_relation is True
    assert suite.assessment.reversal_crossing_episode == 2


def test_return_to_old_reacquires_without_erasing_relation_history() -> None:
    suite = run_canonical_revision_suite()
    row = suite.revision.return_to_old
    assert row.boundary_count == 9
    assert row.link_count == 2
    assert row.old_consistent_count == 6
    assert row.old_inconsistent_count == 3
    assert row.old_reliability == pytest.approx(7 / 11)
    assert row.new_consistent_count == 3
    assert row.new_inconsistent_count == 3
    assert row.new_reliability == pytest.approx(0.5)
    assert suite.assessment.reacquired_old_relation is True
    assert suite.assessment.reacquisition_crossing_episode == 2
    assert suite.assessment.old_relation_retained is True


def test_stable_control_does_not_proliferate_or_invent_revision() -> None:
    control = run_stable_control()
    row = control.snapshot
    assert row.boundary_count == 9
    assert row.link_count == 1
    assert row.old_consistent_count == 9
    assert row.old_inconsistent_count == 0
    assert row.old_reliability == pytest.approx(10 / 11)
    assert row.new_consistent_count == 0
    assert row.new_reliability is None


def test_revision_suite_is_single_world_level3_engineering_candidate() -> None:
    assessment = run_canonical_revision_suite().assessment
    assert assessment.engineering_candidate is True
    assert assessment.acquired_old_relation is True
    assert assessment.reversed_to_new_relation is True
    assert assessment.reacquired_old_relation is True
    assert assessment.stable_control_single_link is True
    assert assessment.stable_control_no_inconsistency is True
    assert assessment.no_positive_self_confirmation is True
    assert assessment.runtime_taxonomy_free is True


def test_external_relation_updates_do_not_commit_internal_positive_learning() -> None:
    suite = run_canonical_revision_suite()
    assert suite.revision.acquisition.committed_positive_updates == 0
    assert suite.revision.reversal.committed_positive_updates == 0
    assert suite.revision.return_to_old.committed_positive_updates == 0
    assert suite.stable_control.snapshot.committed_positive_updates == 0


def test_revision_runtime_contains_no_functional_taxonomy_or_reward() -> None:
    suite = run_canonical_revision_suite()
    lowered = str(
        {
            "revision": suite.revision.runtime_state,
            "stable": suite.stable_control.runtime_state,
        }
    ).lower()
    for forbidden in (
        "assembly_id",
        "relation_type",
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "correct_action",
        "scalar_reward",
        "outcome_label",
        "functional_role",
        "meaning_state",
    ):
        assert forbidden not in lowered


def test_revision_runs_are_deterministic() -> None:
    first = run_revision_condition()
    second = run_revision_condition()
    assert first.acquisition == second.acquisition
    assert first.reversal == second.reversal
    assert first.return_to_old == second.return_to_old
    assert first.reversal_crossing_episode == second.reversal_crossing_episode
    assert first.reacquisition_crossing_episode == second.reacquisition_crossing_episode
    assert first.runtime_state == second.runtime_state

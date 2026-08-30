from __future__ import annotations

import pytest

from sparkbrain.research.rv01.g2_dependency import (
    MINIMUM_LONG_RUN_CONFIDENCE_GAP,
    run_g2_dependency_suite,
)


def test_raw_g1_proposals_survive_without_g2_adaptation() -> None:
    suite = run_g2_dependency_suite()
    rows = suite.initial.g1_only_rows
    assert {row.target for row in rows} == {"unit:1", "unit:2"}
    assert all(row.raw_confidence == pytest.approx(0.5) for row in rows)
    assert all(row.adapted_confidence == pytest.approx(0.5) for row in rows)
    assert all(
        row.raw_arrival_ms - suite.initial.source_time_ms == pytest.approx(5.0)
        for row in rows
    )
    assert suite.assessment.raw_g1_generation_survives_without_g2 is True


def test_prepare_only_cannot_self_confirm() -> None:
    suite = run_g2_dependency_suite()
    assert suite.prepare_only_commits_before_external == 0
    assert suite.initial.committed_positive_updates == 0
    assert suite.assessment.prepare_only_cannot_self_confirm is True


def test_external_old_target_stabilizes_only_through_g2() -> None:
    suite = run_g2_dependency_suite()
    phase = suite.stabilized_old
    old = phase.by_target("unit:1", g2_enabled=True)
    new = phase.by_target("unit:2", g2_enabled=True)
    old_g1 = phase.by_target("unit:1", g2_enabled=False)
    new_g1 = phase.by_target("unit:2", g2_enabled=False)

    assert old.confirmed_count == 3
    assert old.contradicted_count == 0
    assert new.confirmed_count == 0
    assert new.contradicted_count == 3
    assert old.adapted_confidence == pytest.approx(0.75)
    assert new.adapted_confidence == pytest.approx(0.20)
    assert old_g1.adapted_confidence == pytest.approx(0.5)
    assert new_g1.adapted_confidence == pytest.approx(0.5)
    assert suite.assessment.stabilization_requires_g2 is True


def test_timing_correction_is_carried_by_g2_not_raw_g1() -> None:
    suite = run_g2_dependency_suite()
    phase = suite.stabilized_old
    old = phase.by_target("unit:1", g2_enabled=True)
    old_g1 = phase.by_target("unit:1", g2_enabled=False)

    assert old.raw_arrival_ms - phase.source_time_ms == pytest.approx(5.0)
    # G2 updates its correction from the residual error of an already-corrected
    # proposal. With lr=0.2, three +2 ms observations produce +0.784 ms.
    assert old.adapted_arrival_ms - phase.source_time_ms == pytest.approx(5.784)
    assert old_g1.raw_arrival_ms - phase.source_time_ms == pytest.approx(5.0)
    assert old_g1.adapted_arrival_ms - phase.source_time_ms == pytest.approx(5.0)
    assert suite.assessment.timing_correction_requires_g2 is True


def test_reversal_changes_g2_selectivity_while_g1_remains_tied() -> None:
    suite = run_g2_dependency_suite()
    phase = suite.reversed_new
    old = phase.by_target("unit:1", g2_enabled=True)
    new = phase.by_target("unit:2", g2_enabled=True)

    assert old.confirmed_count == 3
    assert old.contradicted_count == 6
    assert new.confirmed_count == 6
    assert new.contradicted_count == 3
    assert old.adapted_confidence == pytest.approx(4 / 11)
    assert new.adapted_confidence == pytest.approx(7 / 11)
    assert all(
        row.adapted_confidence == pytest.approx(0.5)
        for row in phase.g1_only_rows
    )
    assert suite.assessment.reversal_requires_g2 is True


def test_reacquisition_moves_selectivity_back_to_old_target() -> None:
    suite = run_g2_dependency_suite()
    phase = suite.reacquired_old
    old = phase.by_target("unit:1", g2_enabled=True)
    new = phase.by_target("unit:2", g2_enabled=True)
    gap = old.adapted_confidence - new.adapted_confidence

    assert old.confirmed_count == 9
    assert old.contradicted_count == 6
    assert new.confirmed_count == 6
    assert new.contradicted_count == 9
    assert old.adapted_confidence == pytest.approx(10 / 17)
    assert new.adapted_confidence == pytest.approx(7 / 17)
    assert gap >= MINIMUM_LONG_RUN_CONFIDENCE_GAP
    assert suite.assessment.reacquisition_requires_g2 is True
    assert suite.assessment.long_run_selectivity_requires_g2 is True


def test_raw_g1_route_is_structurally_static_across_all_phases() -> None:
    suite = run_g2_dependency_suite()
    baseline = suite.initial.normalized_rows(g2_enabled=False)
    assert suite.stabilized_old.normalized_rows(g2_enabled=False) == baseline
    assert suite.reversed_new.normalized_rows(g2_enabled=False) == baseline
    assert suite.reacquired_old.normalized_rows(g2_enabled=False) == baseline
    assert suite.assessment.g1_only_route_remains_static is True


def test_positive_g2_commits_equal_external_matches_only() -> None:
    suite = run_g2_dependency_suite()
    assert suite.initial.g2_confirmed_count == 0
    assert suite.initial.g2_contradicted_count == 0
    assert suite.stabilized_old.g2_confirmed_count == 3
    assert suite.stabilized_old.g2_contradicted_count == 3
    assert suite.reversed_new.g2_confirmed_count == 9
    assert suite.reversed_new.g2_contradicted_count == 9
    assert suite.reacquired_old.g2_confirmed_count == 15
    assert suite.reacquired_old.g2_contradicted_count == 15

    assert suite.initial.committed_positive_updates == 0
    assert suite.stabilized_old.committed_positive_updates == 3
    assert suite.reversed_new.committed_positive_updates == 9
    assert suite.reacquired_old.committed_positive_updates == 15
    assert suite.assessment.positive_commits_are_external_only is True


def test_external_observation_accounting_is_explicit() -> None:
    suite = run_g2_dependency_suite()
    assert suite.initial.external_observation_count == 1
    assert suite.stabilized_old.external_observation_count == 7
    assert suite.reversed_new.external_observation_count == 19
    assert suite.reacquired_old.external_observation_count == 31


def test_r01_02_identifies_g2_burden_without_mutating_g1() -> None:
    assessment = run_g2_dependency_suite().assessment
    assert assessment.raw_g1_generation_survives_without_g2 is True
    assert assessment.stabilization_requires_g2 is True
    assert assessment.timing_correction_requires_g2 is True
    assert assessment.reversal_requires_g2 is True
    assert assessment.reacquisition_requires_g2 is True
    assert assessment.long_run_selectivity_requires_g2 is True
    assert assessment.g1_only_route_remains_static is True
    assert assessment.prepare_only_cannot_self_confirm is True
    assert assessment.positive_commits_are_external_only is True
    assert assessment.g2_burden_identified is True


def test_g2_dependency_suite_is_deterministic() -> None:
    first = run_g2_dependency_suite()
    second = run_g2_dependency_suite()
    assert first.suite_hash == second.suite_hash
    assert first == second

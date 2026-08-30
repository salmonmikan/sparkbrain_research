from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.physical_missing_middle import (
    CONTROL_LATE_UNIT,
    CONTROL_MISSING_UNIT,
    LATE_EXTERNAL_TIME_MS,
    MAIN_LATE_UNIT,
    MAIN_MISSING_UNIT,
    run_physical_missing_middle_suite,
)


def test_intact_physical_field_generates_missing_and_downstream_units_forward() -> None:
    suite = run_physical_missing_middle_suite()
    row = suite.intact
    assert row.pre_late_units == (0, 4, 1, 5, 2, 6, 3, 7)
    assert row.pre_late_times_ms == pytest.approx(
        (100.0, 100.0, 105.0, 105.0, 110.375, 110.375, 115.75, 115.75)
    )
    assert row.missing_unit_generated_before_late_input is True
    assert row.downstream_unit_generated_before_late_input is True
    assert row.control_missing_unit_generated_before_late_input is True
    assert row.control_downstream_generated_before_late_input is True
    assert MAIN_MISSING_UNIT in row.pre_late_units
    assert MAIN_LATE_UNIT in row.pre_late_units
    assert CONTROL_MISSING_UNIT in row.pre_late_units
    assert CONTROL_LATE_UNIT in row.pre_late_units
    assert all(time_ms < LATE_EXTERNAL_TIME_MS for time_ms in row.pre_late_times_ms)


def test_future_external_d_and_h_are_not_in_the_queue_before_completion() -> None:
    suite = run_physical_missing_middle_suite()
    for row in (
        suite.intact,
        suite.targeted_main_middle_edge,
        suite.matched_control_middle_edge,
        suite.untrained,
    ):
        assert row.late_external_events_preloaded is False
        assert not any(
            pulse_id.endswith(":D") or pulse_id.endswith(":H")
            for pulse_id in row.queue_pulse_ids_before_late_external
        )
    assert suite.assessment.future_external_event_not_preloaded is True


def test_targeted_middle_edge_suppression_removes_main_bridge_and_downstream() -> None:
    suite = run_physical_missing_middle_suite()
    row = suite.targeted_main_middle_edge
    intervention = row.intervention
    assert intervention is not None
    assert (intervention.source_id, intervention.target_id) == (1, 2)
    assert intervention.weight_before > 0.8
    assert intervention.weight_after == 0.0
    assert MAIN_MISSING_UNIT not in row.pre_late_units
    assert MAIN_LATE_UNIT not in row.pre_late_units
    assert CONTROL_MISSING_UNIT in row.pre_late_units
    assert CONTROL_LATE_UNIT in row.pre_late_units
    assert suite.assessment.targeted_middle_path_suppression_removes_downstream is True


def test_matched_active_control_suppression_preserves_main_bridge() -> None:
    suite = run_physical_missing_middle_suite()
    row = suite.matched_control_middle_edge
    intervention = row.intervention
    assert intervention is not None
    assert (intervention.source_id, intervention.target_id) == (5, 6)
    assert intervention.weight_before > 0.8
    assert intervention.weight_after == 0.0
    assert MAIN_MISSING_UNIT in row.pre_late_units
    assert MAIN_LATE_UNIT in row.pre_late_units
    assert CONTROL_MISSING_UNIT not in row.pre_late_units
    assert CONTROL_LATE_UNIT not in row.pre_late_units
    assert suite.assessment.matched_active_suppression_preserves_main_downstream is True
    assert suite.assessment.matched_control_path_is_actively_impaired is True


def test_targeted_and_matched_interventions_have_identical_physical_strength() -> None:
    suite = run_physical_missing_middle_suite()
    targeted = suite.targeted_main_middle_edge.intervention
    matched = suite.matched_control_middle_edge.intervention
    assert targeted is not None and matched is not None
    assert targeted.weight_before == pytest.approx(matched.weight_before)
    assert targeted.delay_before_ms == pytest.approx(matched.delay_before_ms)
    assert targeted.weight_after == matched.weight_after == 0.0
    assert targeted.delay_after_ms == pytest.approx(matched.delay_after_ms)
    assert suite.assessment.intervention_strength_is_matched is True
    assert suite.assessment.selective_causal_effect == 1.0


def test_untrained_field_does_not_fill_either_missing_middle() -> None:
    suite = run_physical_missing_middle_suite()
    row = suite.untrained
    assert row.pre_late_units == (0, 4, 1, 5)
    assert row.missing_unit_generated_before_late_input is False
    assert row.downstream_unit_generated_before_late_input is False
    assert row.control_missing_unit_generated_before_late_input is False
    assert row.control_downstream_generated_before_late_input is False
    assert suite.assessment.untrained_field_does_not_complete is True


def test_all_conditions_receive_identical_external_inputs() -> None:
    suite = run_physical_missing_middle_suite()
    signatures = {
        row.external_input_signature
        for row in (
            suite.intact,
            suite.targeted_main_middle_edge,
            suite.matched_control_middle_edge,
            suite.untrained,
        )
    }
    assert signatures == {
        (
            (100.0, 0),
            (100.0, 4),
            (105.0, 1),
            (105.0, 5),
            (120.0, 3),
            (120.0, 7),
        )
    }
    assert suite.assessment.current_external_inputs_are_identical is True


def test_late_external_events_are_processed_only_after_forward_assay_window() -> None:
    suite = run_physical_missing_middle_suite()
    for row in (
        suite.intact,
        suite.targeted_main_middle_edge,
        suite.matched_control_middle_edge,
        suite.untrained,
    ):
        assert row.post_late_units == (3, 7)
        assert row.post_late_times_ms == pytest.approx((120.0, 120.0))


def test_missing_middle_runtime_imports_no_g1_g2_or_matcher() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "physical_missing_middle.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "LocalTemporalExpectation" not in source
    assert "SparseLocalTransitionAdaptation" not in source
    assert "EndogenousPulseProposal" not in source
    assert "similarity" not in source.lower()
    assert "matcher" not in source.lower()


def test_r01_05_physical_missing_middle_candidate_is_complete() -> None:
    assessment = run_physical_missing_middle_suite().assessment
    assert assessment.forward_missing_middle_generated is True
    assert assessment.forward_downstream_generated_before_external_late_event is True
    assert assessment.future_external_event_not_preloaded is True
    assert assessment.targeted_middle_path_suppression_removes_downstream is True
    assert assessment.matched_active_suppression_preserves_main_downstream is True
    assert assessment.matched_control_path_is_actively_impaired is True
    assert assessment.intervention_strength_is_matched is True
    assert assessment.untrained_field_does_not_complete is True
    assert assessment.current_external_inputs_are_identical is True
    assert assessment.selective_causal_effect == 1.0
    assert assessment.no_g1_or_g2_runtime_required is True
    assert assessment.engineering_candidate is True


def test_physical_missing_middle_suite_is_deterministic() -> None:
    first = run_physical_missing_middle_suite()
    second = run_physical_missing_middle_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash

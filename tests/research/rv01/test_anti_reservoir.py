from __future__ import annotations

from pathlib import Path

from sparkbrain.research.rv01.anti_reservoir import (
    SEQUENCE,
    ExternalSequenceReadout,
    run_anti_reservoir_suite,
)


def test_fixed_field_needs_external_readout_to_mimic_sequence_output() -> None:
    suite = run_anti_reservoir_suite()
    row = suite.readout_alternative
    assert row.fixed_field_later_units == ()
    assert row.readout_output == SEQUENCE[1:]
    assert row.reset_readout_output == ()
    assert suite.assessment.fixed_field_has_no_internal_continuation is True
    assert suite.assessment.external_readout_can_mimic_output is True
    assert suite.assessment.readout_removal_erases_output is True


def test_fixed_field_edge_intervention_cannot_change_external_readout() -> None:
    suite = run_anti_reservoir_suite()
    row = suite.readout_alternative
    assert row.edge_suppressed_connection_hash != row.fixed_connection_hash
    assert row.edge_suppressed_fixed_field_later_units == ()
    assert row.edge_suppressed_readout_output == row.readout_output == (1, 2, 3)
    assert (
        suite.assessment.physical_edge_intervention_does_not_change_readout
        is True
    )


def test_readout_state_transplant_moves_output_but_not_field_dynamics() -> None:
    suite = run_anti_reservoir_suite()
    row = suite.readout_alternative
    assert row.transplanted_readout_state_hash == row.readout_learned_state_hash
    assert row.transplanted_readout_output == (1, 2, 3)
    assert row.transplanted_fixed_field_later_units == ()
    assert (
        suite.assessment.readout_transplant_moves_output_without_field_dynamics
        is True
    )


def test_rv01_field_continues_without_readout_and_is_internally_causal() -> None:
    suite = run_anti_reservoir_suite()
    assert suite.rv01_trained_units == (1, 2, 3)
    assert suite.rv01_untrained_units == ()
    assert suite.rv01_transplanted_units == (1, 2, 3)
    assert 3 not in suite.rv01_targeted_missing_middle_units
    assert 3 in suite.rv01_matched_missing_middle_units
    assert suite.assessment.rv01_field_continues_without_external_readout is True
    assert (
        suite.assessment.rv01_internal_edge_intervention_changes_field_dynamics
        is True
    )
    assert suite.assessment.rv01_connection_transplant_moves_field_dynamics is True
    assert suite.assessment.rv01_training_changes_recurrent_substrate is True


def test_r01_09_rejects_only_the_passive_readout_explanation() -> None:
    assessment = run_anti_reservoir_suite().assessment
    assert (
        assessment.passive_fixed_reservoir_readout_rejected_for_internal_causality
        is True
    )
    assert assessment.generic_trainable_recurrent_explanation_remains_viable is True
    assert assessment.architectural_uniqueness_established is False
    assert assessment.engineering_candidate is True


def test_external_readout_generation_does_not_modify_its_learned_state() -> None:
    readout = ExternalSequenceReadout()
    readout.observe_sequence((0, 1, 2, 3), repetitions=3)
    before = readout.learned_state_dict()
    assert readout.read(0) == (1, 2, 3)
    assert readout.learned_state_dict() == before
    assert readout.output_count == 1


def test_anti_reservoir_module_contains_no_g1_or_g2_runtime() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "anti_reservoir.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "LocalTemporalExpectation" not in source
    assert "SparseLocalTransitionAdaptation" not in source
    assert "EndogenousPulseProposal" not in source


def test_anti_reservoir_suite_is_deterministic() -> None:
    first = run_anti_reservoir_suite()
    second = run_anti_reservoir_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash

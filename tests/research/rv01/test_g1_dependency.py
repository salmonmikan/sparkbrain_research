from __future__ import annotations

from sparkbrain.research.rv01.g1_dependency import run_g1_dependency_suite


def test_same_input_history_dependence_disappears_without_g1() -> None:
    suite = run_g1_dependency_suite()
    assert suite.enabled.same_input_response.generated_units == (1,)
    assert suite.disabled.same_input_response.generated_units == ()
    assert suite.assessment.same_input_response_requires_g1 is True


def test_sequential_continuation_disappears_without_g1() -> None:
    suite = run_g1_dependency_suite()
    assert suite.enabled.sequential_continuation.generated_units == (1, 2, 3)
    assert suite.enabled.sequential_continuation.generated_times_ms == (
        105.0,
        110.0,
        115.0,
    )
    assert suite.disabled.sequential_continuation.generated_units == ()
    assert suite.assessment.sequential_continuation_requires_g1 is True


def test_equal_exposure_branches_disappear_without_g1() -> None:
    suite = run_g1_dependency_suite()
    assert set(suite.enabled.branching.generated_units) == {1, 2}
    assert suite.disabled.branching.generated_units == ()
    assert suite.assessment.branching_requires_g1 is True


def test_forward_missing_middle_bridge_disappears_without_g1() -> None:
    suite = run_g1_dependency_suite()
    enabled = suite.enabled.forward_bridge
    disabled = suite.disabled.forward_bridge
    assert any(
        unit_id == 2 and time_ms < 120.0
        for unit_id, time_ms in zip(
            enabled.generated_units,
            enabled.generated_times_ms,
            strict=True,
        )
    )
    assert 2 not in disabled.generated_units
    assert enabled.input_signature == disabled.input_signature == (
        (100.0, 0),
        (105.0, 1),
        (120.0, 3),
    )
    assert suite.assessment.forward_bridge_requires_g1 is True


def test_boundary_event_disappears_when_g1_cannot_reach_terminal_unit() -> None:
    suite = run_g1_dependency_suite()
    assert suite.enabled.boundary_effect.generated_units == (1, 2, 3)
    assert suite.enabled.boundary_effect.boundary_port_ids == ("port:7",)
    assert suite.disabled.boundary_effect.generated_units == ()
    assert suite.disabled.boundary_effect.boundary_port_ids == ()
    assert suite.assessment.boundary_effect_requires_g1 is True


def test_enabled_and_disabled_conditions_match_field_and_external_inputs() -> None:
    suite = run_g1_dependency_suite()
    for enabled, disabled in zip(
        suite.enabled.observations(),
        suite.disabled.observations(),
        strict=True,
    ):
        assert enabled.assay_id == disabled.assay_id
        assert enabled.input_signature == disabled.input_signature
        assert enabled.initial_field_state_hash == disabled.initial_field_state_hash
        assert enabled.g1_transition_count > 0
        assert disabled.g1_transition_count == 0
    assert suite.assessment.field_initial_states_matched is True
    assert suite.assessment.external_inputs_matched is True
    assert suite.assessment.disabled_g1_has_no_transition_state is True


def test_internal_activity_without_external_confirmation_never_commits_learning() -> None:
    suite = run_g1_dependency_suite()
    for condition in (suite.enabled, suite.disabled):
        for row in (
            condition.same_input_response,
            condition.sequential_continuation,
            condition.branching,
            condition.boundary_effect,
        ):
            assert row.committed_positive_updates == 0
    assert (
        suite.assessment.endogenous_only_runs_do_not_commit_positive_learning
        is True
    )


def test_r01_01_identifies_the_complete_current_g1_burden() -> None:
    suite = run_g1_dependency_suite()
    assert suite.assessment.explicit_g1_burden_identified is True


def test_g1_dependency_suite_is_deterministic() -> None:
    first = run_g1_dependency_suite()
    second = run_g1_dependency_suite()
    assert first.suite_hash == second.suite_hash
    assert first == second

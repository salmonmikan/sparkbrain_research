from __future__ import annotations

from sparkbrain.evaluation.v061_state_factorization_diagnostics import (
    run_state_factorization_diagnosis,
)


def _cells(result):
    return {
        (row["transition_label"], row["consistency_label"]): row
        for row in result["cells"]
    }


def test_transition_state_selects_trajectory_independently_of_consistency() -> None:
    result = run_state_factorization_diagnosis()
    cells = _cells(result)

    alternate_old = cells[("alternate-favoring", "old-target")]
    alternate_new = cells[("alternate-favoring", "new-target")]
    main_old = cells[("main-favoring", "old-target")]
    main_new = cells[("main-favoring", "new-target")]

    assert alternate_old["trajectory_units"] == (4, 5, 6)
    assert alternate_new["trajectory_units"] == (4, 5, 6)
    assert alternate_old["trajectory_class"] == "alternate-only-substitution"
    assert alternate_new["trajectory_class"] == "alternate-only-substitution"

    assert main_old["trajectory_units"] == (1, 2, 3)
    assert main_new["trajectory_units"] == (1, 2, 3)
    assert main_old["trajectory_class"] == "main-only-exact"
    assert main_new["trajectory_class"] == "main-only-exact"


def test_consistency_state_selects_relation_expression_independently_of_g1() -> None:
    result = run_state_factorization_diagnosis()
    cells = _cells(result)

    assert cells[("alternate-favoring", "old-target")][
        "relation_reentry_units"
    ] == (14,)
    assert cells[("main-favoring", "old-target")][
        "relation_reentry_units"
    ] == (14,)
    assert cells[("alternate-favoring", "new-target")][
        "relation_reentry_units"
    ] == (15,)
    assert cells[("main-favoring", "new-target")][
        "relation_reentry_units"
    ] == (15,)


def test_current_primary_state_components_form_a_cartesian_product() -> None:
    result = run_state_factorization_diagnosis()
    assessment = result["assessment"]

    assert result["candidate_003_executions"] == 0
    assert len(result["cells"]) == 4
    assert assessment["transition_states_distinct"] is True
    assert assessment["consistency_states_distinct"] is True
    assert assessment["transition_changes_trajectory"] is True
    assert assessment["consistency_changes_relation_expression"] is True
    assert assessment["trajectory_invariant_under_consistency_swap"] is True
    assert assessment["relation_expression_invariant_under_transition_swap"] is True
    assert assessment["full_cartesian_factorization"] is True
    assert assessment["missing_consistency_to_trajectory_edge_supported"] is True


def test_factorization_diagnosis_is_deterministic() -> None:
    first = run_state_factorization_diagnosis()
    second = run_state_factorization_diagnosis()
    assert first == second

from __future__ import annotations

import inspect

from forge_prototypes.scope_revision_boundary_stress import (
    run_scope_revision_stress_probe,
    stress_cases,
)


def _outcomes():
    return {row.case_id: row for row in run_scope_revision_stress_probe().outcomes}


def test_moderate_overlap_retains_both_contexts_and_rejects_midpoint() -> None:
    row = _outcomes()["moderate_overlap_with_midpoint_reject"]
    queries = {query.label: query for query in row.queries}

    assert row.full_commits == row.cut_commits == 4
    assert row.full_scope_tokens == row.cut_scope_tokens == (
        "scope-00000001",
        "scope-00000002",
    )
    assert queries["qa"].full_selected_value == "A"
    assert queries["qb"].full_selected_value == "B"
    assert queries["midpoint"].full_abstained
    assert all(query.cut_abstained for query in row.queries)
    assert row.boundary_class.endswith("AMBIGUOUS_MIDPOINT_REJECT")


def test_within_reuse_radius_collision_is_an_explicit_failure_boundary() -> None:
    row = _outcomes()["within_reuse_radius_collision"]
    queries = {query.label: query for query in row.queries}

    assert row.full_scope_tokens == row.cut_scope_tokens == ("scope-00000001",)
    assert queries["qa"].full_selected_value == "A"
    assert queries["qb"].full_selected_value is None
    assert queries["qb"].full_abstained
    assert row.boundary_class == (
        "ROUTER_RESOLUTION_LIMIT_PREVENTS_SCOPE_SPECIFIC_REVISION"
    )


def test_single_conflicting_label_preserves_only_context_specific_majorities() -> None:
    row = _outcomes()["single_conflicting_label"]
    queries = {query.label: query for query in row.queries}

    assert queries["qa"].full_selected_value == "A"
    assert queries["qb"].full_selected_value == "B"
    assert {query.cut_selected_value for query in row.queries} == {"B"}
    assert row.boundary_class.endswith("CONTEXT_SPECIFIC_MAJORITY_ONLY")


def test_probe_is_deterministic_and_serializable() -> None:
    first = run_scope_revision_stress_probe()
    second = run_scope_revision_stress_probe()

    assert first == second
    assert first.as_dict() == second.as_dict()
    assert len(first.outcomes) == len(stress_cases()) == 3


def test_public_probe_api_has_no_privileged_identity_input() -> None:
    parameters = inspect.signature(run_scope_revision_stress_probe).parameters
    forbidden = {"scope", "scope_id", "regime", "episode", "truth", "evaluator"}

    assert not parameters
    assert forbidden.isdisjoint(parameters)

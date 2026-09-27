from __future__ import annotations

import inspect

import pytest

from forge_prototypes.scope_allocator_component_replacement import (
    GaussianMixtureReferenceAllocator,
    run_scope_allocator_component_replacement_probe,
)


def _outcomes():
    return {
        row.case_id: row
        for row in run_scope_allocator_component_replacement_probe().outcomes
    }


def test_reference_allocator_resolves_the_fixed_radius_collision() -> None:
    report = run_scope_allocator_component_replacement_probe()
    row = _outcomes()["within_reuse_radius_collision"]
    queries = {query.label: query for query in row.queries}

    assert report.fixed_radius_scope_tokens == ("scope-00000001",)
    assert report.fixed_radius_b_query_abstained
    assert row.fit.identifiable
    assert row.committed_events == 4
    assert row.scope_tokens == ("gmm-scope-00000001", "gmm-scope-00000002")
    assert queries["qa"].selected_value == "A"
    assert queries["qb"].selected_value == "B"
    assert row.classification == (
        "ESTABLISHED_BATCH_ALLOCATOR_RESOLVES_FIXED_RADIUS_COLLISION"
    )


def test_reference_allocator_rejects_the_close_case_midpoint() -> None:
    query = {
        row.case_id: {query.label: query for query in row.queries}
        for row in run_scope_allocator_component_replacement_probe().outcomes
    }["within_reuse_radius_collision"]["midpoint"]

    assert query.abstained
    assert query.scope_token is None
    assert query.routing_reason == "ambiguous_component_posterior"


def test_identical_observations_remain_unidentifiable_and_no_write() -> None:
    row = _outcomes()["identical_observation_conflicting_labels"]

    assert not row.fit.identifiable
    assert row.committed_events == 0
    assert row.scope_tokens == ()
    assert all(query.abstained for query in row.queries)
    assert row.classification == (
        "OBSERVATIONS_IDENTICAL_REFERENCE_ALLOCATOR_FAILS_CLOSED"
    )


def test_probe_is_deterministic_and_serializable() -> None:
    first = run_scope_allocator_component_replacement_probe()
    second = run_scope_allocator_component_replacement_probe()

    assert first == second
    assert first.as_dict() == second.as_dict()


def test_reference_allocator_validates_observations() -> None:
    allocator = GaussianMixtureReferenceAllocator()

    with pytest.raises(ValueError, match="at least two"):
        allocator.fit(((0.0,),))
    with pytest.raises(ValueError, match="dimension"):
        allocator.fit(((0.0,), (0.0, 1.0)))


def test_public_probe_api_has_no_privileged_identity_input() -> None:
    parameters = inspect.signature(
        run_scope_allocator_component_replacement_probe
    ).parameters
    forbidden = {"scope", "scope_id", "regime", "episode", "truth", "evaluator"}

    assert not parameters
    assert forbidden.isdisjoint(parameters)

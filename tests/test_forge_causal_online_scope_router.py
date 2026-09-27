from __future__ import annotations

import inspect
import json

import pytest

from forge_prototypes.causal_online_scope_router import (
    CausalOnlineRouterConfig,
    CausalOnlineScopeRouter,
    run_causal_online_scope_router_probe,
)


def _outcomes():
    return {
        row.stream_id: row
        for row in run_causal_online_scope_router_probe().outcomes
    }


def test_router_api_has_no_label_or_privileged_identity_inputs() -> None:
    parameters = set(inspect.signature(CausalOnlineScopeRouter.observe).parameters)
    forbidden = {
        "label",
        "value",
        "scope",
        "episode",
        "regime",
        "truth",
        "target",
        "evaluator",
    }
    assert not parameters & forbidden


@pytest.mark.parametrize(
    "stream_id", ["interleaved", "blocked", "reversed_interleaved"]
)
def test_causal_router_recovers_close_a_b_without_future_context(
    stream_id: str,
) -> None:
    outcome = _outcomes()[stream_id]
    queries = {row.label: row for row in outcome.queries}

    assert outcome.classification == (
        "CAUSAL_ONLINE_TWO_COMPONENT_ROUTING_RECOVERS_BOUNDED_A_B"
    )
    assert outcome.committed_events == 4
    assert outcome.rejected_events == 0
    assert len(outcome.components) == 2
    assert queries["qa"].selected_value == "A"
    assert queries["qb"].selected_value == "B"
    assert queries["midpoint"].abstained
    assert queries["midpoint"].routing_reason == "ambiguous_nearest_components"
    assert queries["out_of_support"].abstained
    assert queries["out_of_support"].routing_reason == (
        "observation_outside_component_support"
    )


def test_identical_observations_collapse_and_revision_abstains() -> None:
    outcome = _outcomes()["identical_observations"]

    assert len(outcome.components) == 1
    assert outcome.committed_events == 4
    assert outcome.classification == "IDENTICAL_OBSERVATIONS_COLLAPSE_REVISION_ABSTAINS"
    assert all(row.abstained for row in outcome.queries)


def test_shared_prefix_is_independent_of_unseen_suffix() -> None:
    report = run_causal_online_scope_router_probe()

    assert report.prefix_state_equal_before_divergent_suffix
    assert report.prefix_action_equal_before_divergent_suffix
    assert not report.future_context_used


def test_ambiguous_observation_is_no_write() -> None:
    router = CausalOnlineScopeRouter()
    router.observe((0.0,))
    router.observe((0.45,))
    before = router.state_dict()

    route = router.observe((0.225,))

    assert route.abstained
    assert route.reason == "ambiguous_nearest_components"
    assert router.state_dict() == before


def test_component_capacity_rejects_out_of_support_without_write() -> None:
    router = CausalOnlineScopeRouter()
    router.observe((0.0,))
    router.observe((0.45,))
    before = router.state_dict()

    route = router.observe((1.0,))

    assert route.abstained
    assert route.reason == "component_capacity_exhausted_out_of_support"
    assert router.state_dict() == before


def test_checkpoint_roundtrip_preserves_next_decision() -> None:
    router = CausalOnlineScopeRouter()
    router.observe((0.0,))
    router.observe((0.45,))
    router.observe((0.05,))
    state = json.loads(json.dumps(router.state_dict()))
    restored = CausalOnlineScopeRouter.from_state_dict(state)

    assert restored.route((0.40,)) == router.route((0.40,))
    assert restored.observe((0.40,)) == router.observe((0.40,))
    assert restored.state_dict() == router.state_dict()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"birth_distance": 0.0},
        {"maximum_assignment_distance": 0.0},
        {"minimum_distance_margin": -0.1},
        {"max_components": 3},
    ],
)
def test_invalid_config_is_rejected(kwargs: dict[str, float | int]) -> None:
    with pytest.raises(ValueError):
        CausalOnlineRouterConfig(**kwargs)

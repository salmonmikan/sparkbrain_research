from __future__ import annotations

import inspect

from forge_prototypes.continuous_scope_revision_ablation import (
    AblationEvent,
    ContinuousScopeRevisionAblation,
)
from forge_prototypes.internal_scope_allocator import InternalScopeAllocatorConfig
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.plural_scope_posterior import ScopePosteriorConfig


def _base() -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        assembly_id="assembly-a",
        hypotheses=(
            WeightedHypothesis("A", 5, 0.5),
            WeightedHypothesis("B", 5, 0.5),
        ),
        selected_value=None,
        confidence=0.5,
        margin=0.0,
        abstained=True,
        reason="ambiguous_hypotheses",
    )


def _harness() -> ContinuousScopeRevisionAblation:
    return ContinuousScopeRevisionAblation(
        InternalScopeAllocatorConfig(
            reuse_radius=0.75,
            create_error_threshold=0.4,
            centroid_learning_rate=0.0,
            max_scopes=4,
        ),
        ScopePosteriorConfig(
            temperature=0.35,
            new_scope_error_scale=2.0,
            top_k=3,
            min_margin=0.15,
            min_selected_mass=0.55,
        ),
    )


def _alternating_events() -> tuple[AblationEvent, ...]:
    return (
        AblationEvent("a1", (0.0,), "A"),
        AblationEvent("b1", (10.0,), "B"),
        AblationEvent("a2", (0.0,), "A"),
        AblationEvent("b2", (10.0,), "B"),
    )


def test_connected_loop_retains_cluster_specific_revision_after_return() -> None:
    report = _harness().run(
        _base(),
        _alternating_events(),
        (("qa", (0.0,), "A"), ("qb", (10.0,), "B")),
    )

    assert report.full_commits == report.cut_commits == 4
    assert [row.full_scope_token for row in report.steps] == [
        "scope-00000001",
        "scope-00000002",
        "scope-00000001",
        "scope-00000002",
    ]
    assert [row.cut_scope_token for row in report.steps] == [
        "scope-00000001",
        "scope-00000002",
        "scope-00000001",
        "scope-00000002",
    ]
    assert [row.full_selected_value for row in report.queries] == ["A", "B"]
    assert [row.full_abstained for row in report.queries] == [False, False]


def test_cut_connection_collapses_contradictory_support_and_abstains() -> None:
    report = _harness().run(
        _base(),
        _alternating_events(),
        (("qa", (0.0,), "A"), ("qb", (10.0,), "B")),
    )

    assert [row.cut_selected_value for row in report.queries] == [None, None]
    assert [row.cut_abstained for row in report.queries] == [True, True]


def test_single_cluster_control_does_not_manufacture_an_advantage() -> None:
    report = _harness().run(
        _base(),
        (
            AblationEvent("a1", (0.0,), "A"),
            AblationEvent("a2", (0.1,), "A"),
        ),
        (("qa", (0.0,), "A"),),
    )

    query = report.queries[0]
    assert query.full_selected_value == "A"
    assert query.cut_selected_value == "A"
    assert not query.full_abstained
    assert not query.cut_abstained


def test_query_is_read_only_and_checkpoint_replay_is_deterministic() -> None:
    harness = _harness()
    for event in _alternating_events():
        harness.apply_event(_base(), event)
    before = harness.state_dict()

    first = harness.query(
        _base(), label="qa", observation=(0.0,), reference_value="A"
    )
    restored = ContinuousScopeRevisionAblation.from_state_dict(before)
    second = restored.query(
        _base(), label="qa", observation=(0.0,), reference_value="A"
    )

    assert first == second
    assert harness.state_dict() == before
    assert restored.state_dict() == before


def test_unexposed_outcome_is_no_write_in_both_arms() -> None:
    harness = _harness()
    before = harness.state_dict()
    step = harness.apply_event(_base(), AblationEvent("missing", (0.0,), "C"))

    assert not step.full_committed
    assert not step.cut_committed
    assert harness.state_dict() == before


def test_public_api_has_no_privileged_scope_or_evaluator_input() -> None:
    parameters = inspect.signature(ContinuousScopeRevisionAblation.apply_event).parameters
    forbidden = {"scope", "scope_id", "regime", "episode", "truth", "evaluator"}

    assert forbidden.isdisjoint(parameters)


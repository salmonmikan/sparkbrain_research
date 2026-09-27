import inspect

from forge_prototypes.internal_scope_allocator import InternalScopeAllocator
from forge_prototypes.plural_scope_posterior import (
    NEW_SCOPE,
    PluralScopePosteriorRouter,
    ScopePosteriorConfig,
)


def two_scope_allocator() -> InternalScopeAllocator:
    allocator = InternalScopeAllocator()
    allocator.observe([0.0], prediction_error=1.0)
    allocator.observe([2.0], prediction_error=1.0)
    return allocator


def test_route_api_has_no_privileged_identity_inputs() -> None:
    parameters = set(inspect.signature(PluralScopePosteriorRouter.route).parameters)
    forbidden = {"scope", "episode", "regime", "entity", "target", "truth", "evaluator"}
    assert not parameters & forbidden


def test_equal_distance_scopes_remain_plural_and_abstain() -> None:
    posterior = PluralScopePosteriorRouter(
        ScopePosteriorConfig(min_selected_mass=0.4, min_margin=0.2)
    ).route(two_scope_allocator(), [1.0], prediction_error=0.0)

    assert posterior.abstained
    assert posterior.selected_scope is None
    tokens = {row.scope_token for row in posterior.hypotheses}
    assert {"scope-00000001", "scope-00000002"} <= tokens


def test_clear_return_selects_prior_scope() -> None:
    posterior = PluralScopePosteriorRouter().route(
        two_scope_allocator(), [0.05], prediction_error=0.05
    )

    assert not posterior.abstained
    assert posterior.selected_scope == "scope-00000001"


def test_large_mismatch_can_rank_new_scope_without_creating_it() -> None:
    allocator = two_scope_allocator()
    before = allocator.state_dict()

    posterior = PluralScopePosteriorRouter().route(
        allocator, [5.0], prediction_error=1.0
    )

    assert posterior.selected_scope == NEW_SCOPE
    assert not posterior.abstained
    assert allocator.state_dict() == before


def test_router_keeps_at_least_three_bounded_alternatives() -> None:
    allocator = InternalScopeAllocator()
    allocator.observe([0.0], prediction_error=1.0)
    allocator.observe([2.0], prediction_error=1.0)
    allocator.observe([4.0], prediction_error=1.0)

    posterior = PluralScopePosteriorRouter(
        ScopePosteriorConfig(top_k=3, min_selected_mass=0.99)
    ).route(allocator, [2.0], prediction_error=0.1)

    assert posterior.abstained
    assert len(posterior.hypotheses) == 3


def test_routing_is_deterministic_across_allocator_checkpoint_roundtrip() -> None:
    allocator = two_scope_allocator()
    restored = InternalScopeAllocator.from_state_dict(allocator.state_dict())
    router = PluralScopePosteriorRouter()

    left = router.route(allocator, [1.0], prediction_error=0.2)
    right = router.route(restored, [1.0], prediction_error=0.2)

    assert left == right

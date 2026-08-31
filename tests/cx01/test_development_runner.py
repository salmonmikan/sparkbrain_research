from __future__ import annotations

from sparkbrain.comparison.cx01.contract import ComparatorKind, ComparatorProtocol
from sparkbrain.comparison.cx01.development import (
    COMPARATOR_KINDS,
    create_model,
    run_development_execution,
)
from sparkbrain.comparison.cx01.worlds import CX01Family, build_world


def test_every_comparator_implements_shared_protocol() -> None:
    for kind in COMPARATOR_KINDS:
        model = create_model(kind)
        assert isinstance(model, ComparatorProtocol)
        assert model.kind is kind


def test_timing_world_separates_timestamp_aware_g8_from_token_only_g6() -> None:
    world = build_world("cx01-runner-test", CX01Family.TIMING, 4400)
    g6 = run_development_execution(ComparatorKind.G6_VARIABLE_ORDER, world)
    g8p = run_development_execution(ComparatorKind.G8_PREDICTION, world)
    g8r = run_development_execution(ComparatorKind.G8_REPLAY, world)
    assert not g6.decision.passed
    assert g8p.decision.passed
    assert g8r.decision.passed


def test_high_order_world_is_solved_by_g6_and_g7() -> None:
    world = build_world("cx01-runner-test", CX01Family.HIGH_ORDER, 4401)
    g6 = run_development_execution(ComparatorKind.G6_VARIABLE_ORDER, world)
    g7 = run_development_execution(ComparatorKind.G7_HTM_TEMPORAL_MEMORY, world)
    assert g6.decision.passed
    assert g7.decision.passed


def test_resources_are_descriptive_only() -> None:
    world = build_world("cx01-runner-test", CX01Family.HIGH_ORDER, 4402)
    row = run_development_execution(ComparatorKind.G3_FIRST_ORDER, world)
    assert row.resource.decision_use == "descriptive-only"

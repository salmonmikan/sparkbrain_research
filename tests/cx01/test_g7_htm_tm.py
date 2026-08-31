from __future__ import annotations

from sparkbrain.comparison.cx01.events import ComparatorEvent, EventOrigin
from sparkbrain.comparison.cx01.g7_htm_tm import HTMTemporalMemoryComparator
from sparkbrain.comparison.cx01.worlds import CX01Family, build_world


def _feed(
    model: HTMTemporalMemoryComparator,
    tokens: tuple[str, ...],
    lags: tuple[float, ...],
    start: float,
) -> float:
    now = start
    model.observe_external(ComparatorEvent(tokens[0], now, EventOrigin.EXTERNAL, True))
    for token, lag in zip(tokens[1:], lags, strict=True):
        now += lag
        model.observe_external(ComparatorEvent(token, now, EventOrigin.EXTERNAL))
    return now + 20.0


def _train_world(
    model: HTMTemporalMemoryComparator, family: CX01Family, seed: int
) -> tuple[object, float]:
    world = build_world("cx01-g7-test", family, seed)
    now = 0.0
    for row in world.training:
        for _ in range(row.exposures):
            now = _feed(model, row.tokens, row.lags_ms, now)
    return world, now


def test_fixed_sdr_is_deterministic_and_sparse() -> None:
    model = HTMTemporalMemoryComparator()
    left = model.token_columns("anonymous:1")
    right = model.token_columns("anonymous:1")
    other = model.token_columns("anonymous:2")
    assert left == right
    assert len(left) == model.config.active_columns_per_token
    assert left != other


def test_high_order_context_uses_different_cells_for_shared_suffix() -> None:
    model = HTMTemporalMemoryComparator()
    world, now = _train_world(model, CX01Family.HIGH_ORDER, 4200)
    for probe in world.probes:
        now += 10.0
        now = _feed(model, probe.prefix, probe.lags_ms, now)
        generated = model.generate(max_steps=1)
        assert generated
        assert generated[0].token == probe.expected_distribution[0][0]


def test_temporal_memory_does_not_secretly_use_timing() -> None:
    model = HTMTemporalMemoryComparator()
    world, now = _train_world(model, CX01Family.TIMING, 4201)
    distributions = []
    for probe in world.probes:
        now += 10.0
        now = _feed(model, probe.prefix, probe.lags_ms, now)
        distributions.append(model.distribution().as_dict())
    assert distributions[0] == distributions[1]


def test_generated_events_do_not_create_segments() -> None:
    model = HTMTemporalMemoryComparator()
    _feed(model, ("a", "b", "c"), (1.0, 1.0), 0.0)
    # Repeat until segments become connected.
    for index in range(5):
        _feed(model, ("a", "b", "c"), (1.0, 1.0), 20.0 + index * 10.0)
    model.observe_external(ComparatorEvent("a", 100.0, EventOrigin.EXTERNAL, True))
    model.observe_external(ComparatorEvent("b", 101.0, EventOrigin.EXTERNAL))
    before = model.parameter_count
    model.generate(max_steps=2)
    assert model.parameter_count == before

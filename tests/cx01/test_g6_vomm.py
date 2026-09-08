from __future__ import annotations

from sparkbrain.comparison.cx01.events import ComparatorEvent, EventOrigin
from sparkbrain.comparison.cx01.g3_anchor import G3FirstOrderAnchor
from sparkbrain.comparison.cx01.g6_vomm import (
    VariableOrderConfig,
    VariableOrderMarkovPredictor,
)
from sparkbrain.comparison.cx01.worlds import CX01Family, build_world


def _feed(model: object, tokens: tuple[str, ...], lags: tuple[float, ...], start: float) -> float:
    now = start
    model.observe_external(ComparatorEvent(tokens[0], now, EventOrigin.EXTERNAL, True))
    for token, lag in zip(tokens[1:], lags, strict=True):
        now += lag
        model.observe_external(ComparatorEvent(token, now, EventOrigin.EXTERNAL))
    return now + 20.0


def test_order_one_matches_g3_anchor_predictions() -> None:
    g3 = G3FirstOrderAnchor(retention=0.8)
    g6 = VariableOrderMarkovPredictor(VariableOrderConfig(max_order=1, retention=0.8))
    now = 0.0
    sequences = (
        (("a", "b", "c"), (2.0, 3.0)),
        (("a", "b", "d"), (2.0, 3.0)),
        (("a", "b", "c"), (2.0, 3.0)),
    )
    for tokens, lags in sequences:
        now = _feed(g3, tokens, lags, now)
        _feed(g6, tokens, lags, now - 20.0 - sum(lags))

    probe_time = now + 10.0
    for model in (g3, g6):
        model.observe_external(ComparatorEvent("a", probe_time, EventOrigin.EXTERNAL, True))
        model.observe_external(ComparatorEvent("b", probe_time + 2.0, EventOrigin.EXTERNAL))
    assert g6.distribution().as_dict() == g3.distribution().as_dict()
    assert tuple(row.token for row in g6.generate(max_steps=2)) == tuple(
        row.token for row in g3.generate(max_steps=2)
    )


def test_high_order_context_resolves_shared_suffix_alias() -> None:
    world = build_world("cx01-g6-test", CX01Family.HIGH_ORDER, 4100)
    model = VariableOrderMarkovPredictor(VariableOrderConfig(max_order=3, retention=0.8))
    now = 0.0
    for row in world.training:
        for _ in range(row.exposures):
            now = _feed(model, row.tokens, row.lags_ms, now)

    for probe in world.probes:
        now += 10.0
        now = _feed(model, probe.prefix, probe.lags_ms, now)
        expected = probe.expected_distribution[0][0]
        generated = model.generate(max_steps=1)
        assert generated and generated[0].token == expected


def test_generated_events_never_update_transition_tables() -> None:
    model = VariableOrderMarkovPredictor()
    _feed(model, ("a", "b", "c"), (1.0, 1.0), 0.0)
    before = model.snapshot()["scores"]
    model.observe_external(ComparatorEvent("a", 20.0, EventOrigin.EXTERNAL, True))
    model.generate(max_steps=2)
    after = model.snapshot()["scores"]
    assert before == after

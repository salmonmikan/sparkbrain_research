from __future__ import annotations

from sparkbrain.comparison.cx01.events import ComparatorEvent, EventOrigin
from sparkbrain.comparison.cx01.g3_anchor import G3FirstOrderAnchor


def _event(token: str, time_ms: float, *, start: bool = False) -> ComparatorEvent:
    return ComparatorEvent(token, time_ms, EventOrigin.EXTERNAL, start)


def test_g3_anchor_remains_first_order_and_external_only() -> None:
    model = G3FirstOrderAnchor()
    model.observe_external(_event("a", 0.0, start=True))
    model.observe_external(_event("b", 5.0))
    model.observe_external(_event("c", 10.0))
    before = model.observed_external_events
    generated = model.generate(max_steps=1)
    assert tuple(row.token for row in generated) == ()
    assert model.observed_external_events == before

    model.observe_external(_event("a", 20.0, start=True))
    after_external_cue = model.observed_external_events
    assert after_external_cue == before + 1
    prediction = model.generate(max_steps=2)
    assert tuple(row.token for row in prediction) == ("b", "c")
    assert model.observed_external_events == after_external_cue


def test_g3_anchor_snapshot_round_trip() -> None:
    model = G3FirstOrderAnchor()
    model.observe_external(_event("a", 0.0, start=True))
    model.observe_external(_event("b", 1.0))
    state = model.snapshot()
    restored = G3FirstOrderAnchor()
    restored.restore(state)
    assert restored.snapshot() == state

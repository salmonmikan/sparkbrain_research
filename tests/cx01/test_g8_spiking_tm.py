from __future__ import annotations

from sparkbrain.comparison.cx01.events import ComparatorEvent, EventOrigin
from sparkbrain.comparison.cx01.g8_spiking_tm import SpikingTemporalMemoryComparator
from sparkbrain.comparison.cx01.worlds import CX01Family, build_world


def _feed(model: SpikingTemporalMemoryComparator, tokens: tuple[str, ...], lags: tuple[float, ...], start: float) -> float:
    now = start
    model.observe_external(ComparatorEvent(tokens[0], now, EventOrigin.EXTERNAL, True))
    for token, lag in zip(tokens[1:], lags, strict=True):
        now += lag
        model.observe_external(ComparatorEvent(token, now, EventOrigin.EXTERNAL))
    return now + 25.0


def _train(model: SpikingTemporalMemoryComparator, family: CX01Family, seed: int) -> tuple[object, float]:
    world = build_world("cx01-g8-test", family, seed)
    now = 0.0
    for row in world.training:
        for _ in range(row.exposures):
            now = _feed(model, row.tokens, row.lags_ms, now)
    return world, now


def test_prediction_mode_discriminates_same_tokens_by_timing() -> None:
    model = SpikingTemporalMemoryComparator(replay_mode=False)
    world, now = _train(model, CX01Family.TIMING, 4300)
    for probe in world.probes:
        now += 10.0
        now = _feed(model, probe.prefix, probe.lags_ms, now)
        generated = model.generate(max_steps=3)
        assert len(generated) == 1
        assert generated[0].token == probe.expected_distribution[0][0]


def test_prediction_and_replay_modes_share_learned_contract_but_not_rollout_privilege() -> None:
    prediction = SpikingTemporalMemoryComparator(replay_mode=False)
    replay = SpikingTemporalMemoryComparator(replay_mode=True)
    sequence = ("a", "b", "c", "d")
    now = 0.0
    for _ in range(5):
        now = _feed(prediction, sequence, (2.0, 3.0, 4.0), now)
    state = prediction.snapshot()
    replay_state = dict(state)
    replay_state["replay_mode"] = True
    replay_state["kind"] = replay.kind.value
    replay.restore(replay_state)

    start = now + 10.0
    for model in (prediction, replay):
        _feed(model, ("a",), (), start)
    assert len(prediction.generate(max_steps=3)) <= 1
    assert tuple(row.token for row in replay.generate(max_steps=3)) == ("b", "c", "d")


def test_generated_replay_does_not_train_associations() -> None:
    model = SpikingTemporalMemoryComparator(replay_mode=True)
    now = 0.0
    for _ in range(5):
        now = _feed(model, ("a", "b", "c"), (1.0, 2.0), now)
    _feed(model, ("a",), (), now + 10.0)
    before = model.snapshot()["associations"]
    model.generate(max_steps=2)
    after = model.snapshot()["associations"]
    assert before == after


def test_population_mapping_is_deterministic() -> None:
    model = SpikingTemporalMemoryComparator()
    assert model.population("x") == model.population("x")
    assert model.population("x") != model.population("y")

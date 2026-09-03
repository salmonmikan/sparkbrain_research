from __future__ import annotations

import pytest

from sparkbrain.comparison.cx01.development import (
    COMPARATOR_KINDS,
    _feed,
    _learning_state_hash,
    _train,
    create_model,
)
from sparkbrain.comparison.cx01.fairness import build_training_transcript
from sparkbrain.comparison.cx01.historical_anchors import G4AssemblyAnchor
from sparkbrain.comparison.cx01.worlds import (
    DEVELOPMENT_GENERATION_ID,
    CX01Family,
    build_world,
)


@pytest.mark.parametrize("kind", COMPARATOR_KINDS)
def test_probe_prefix_advances_context_without_learning(kind) -> None:
    world = build_world(DEVELOPMENT_GENERATION_ID, CX01Family.HIGH_ORDER, 3000)
    model = create_model(kind)
    now = _train(model, build_training_transcript(world))
    before = _learning_state_hash(model)

    probe = world.probes[0]
    _feed(model, probe.prefix, probe.lags_ms, now, learn=False)
    model.distribution()

    assert _learning_state_hash(model) == before


def test_g4_final_training_episode_is_committed_before_probe() -> None:
    world = build_world(DEVELOPMENT_GENERATION_ID, CX01Family.HIGH_ORDER, 3000)
    model = G4AssemblyAnchor()
    _train(model, build_training_transcript(world))

    state = model.snapshot()
    assert state["episode"] == []
    assert state["episode_learnable"] is False
    assert model.learned_state_dict()["assemblies"]

from __future__ import annotations

import copy
import json
from dataclasses import replace

from sparkbrain.v05 import IntegratedV05Brain, held_out_episodes, training_episodes


def _train_dev_brain() -> IntegratedV05Brain:
    brain = IntegratedV05Brain()
    for episode in training_episodes(seed=907, count=16):
        result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
        reward = 1.0 if result.action.action == episode.rewarded_action else -0.35
        brain.learn_outcome(next_event=episode.future_event, reward=reward)
    return brain


def _shift_probe(brain: IntegratedV05Brain) -> tuple[object, ...]:
    episode = held_out_episodes(seed=907, count=1, condition="jitter", start_ms=0.0)[0]
    earliest = min(pulse.time_ms for pulse in episode.pulses)
    target_start = brain.current_time_ms + 100.0
    return tuple(
        replace(pulse, time_ms=target_start + (pulse.time_ms - earliest))
        for pulse in episode.pulses
    )


def _functional_summary(result: object) -> dict[str, object]:
    mature = tuple(
        sorted(
            row.assembly_id
            for row in result.assembly_activations
            if row.mature and not row.suppressed
        )
    )
    return {
        "spike_count": len(result.v04_result.spikes),
        "spikes": tuple(
            (round(row.time_ms, 12), row.unit_id) for row in result.v04_result.spikes
        ),
        "pattern_count": len(result.patterns),
        "mature_assemblies": mature,
        "prediction": result.prediction.value,
        "action": result.action.action,
    }


def test_default_supported_step_has_no_input_free_functional_continuation() -> None:
    """EXPLORATORY / NON_EVIDENTIARY theory-backward diagnostic.

    Prospective contract and contingency tree:
    analysis/exploratory/sub_v05_endogenous_continuation_20260920.md

    This first fixed probe tests terminal
    NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE. If it fails, the assertion
    payload exposes the pre-bound observations and the already-bound queue-clear
    comparator is the only permitted next diagnostic within this cycle.
    """

    trained = _train_dev_brain()
    probe = _shift_probe(trained)
    driven = trained.process_episode(
        probe,
        episode_id="exploratory-endogenous-driven",
        learn_assembly=False,
        learn_field=False,
        explore_action=False,
    )
    post_driven = copy.deepcopy(trained)
    queue_before = post_driven.base.field.state_dict()["queue"]

    empty = post_driven.process_episode(
        (),
        episode_id="exploratory-endogenous-empty",
        learn_assembly=False,
        learn_field=False,
        explore_action=False,
    )
    queue_after = post_driven.base.field.state_dict()["queue"]

    payload = {
        "driven": _functional_summary(driven),
        "empty": _functional_summary(empty),
        "queue_before_count": len(queue_before),
        "queue_before_earliest_ms": queue_before[0]["time_ms"] if queue_before else None,
        "queue_after_count": len(queue_after),
        "current_time_after_empty_ms": post_driven.current_time_ms,
    }

    summary = payload["empty"]
    assert summary == {
        "spike_count": 0,
        "spikes": (),
        "pattern_count": 0,
        "mature_assemblies": (),
        "prediction": None,
        "action": None,
    }, json.dumps(payload, sort_keys=True)

from __future__ import annotations

import copy
import json
import statistics
from dataclasses import replace

from sparkbrain.v05 import IntegratedV05Brain, held_out_episodes, training_episodes


def _train_dev_brain() -> IntegratedV05Brain:
    brain = IntegratedV05Brain()
    for episode in training_episodes(seed=501, count=16):
        result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
        reward = 1.0 if result.action.action == episode.rewarded_action else -0.35
        brain.learn_outcome(next_event=episode.future_event, reward=reward)
    return brain


def _evaluate_order(
    trained: IntegratedV05Brain,
    indexed_episodes: list[tuple[int, object]],
) -> tuple[dict[str, dict[str, object]], dict[str, float]]:
    brain = copy.deepcopy(trained)
    first_slot = brain.current_time_ms + 100.0
    keyed: dict[str, dict[str, object]] = {}
    correct_actions = 0
    correct_predictions = 0
    prediction_coverage = 0
    mature_count = 0
    similarities: list[float] = []
    runaway_count = 0
    dead_count = 0

    for slot, (original_index, episode) in enumerate(indexed_episodes):
        slot_start = first_slot + slot * 220.0
        original_start = original_index * 220.0
        shifted = tuple(
            replace(pulse, time_ms=slot_start + (pulse.time_ms - original_start))
            for pulse in episode.pulses
        )
        result = brain.process_episode(
            shifted,
            episode_id=episode.episode_id,
            learn_assembly=False,
            learn_field=False,
            explore_action=False,
        )
        mature = [
            row for row in result.assembly_activations if row.mature and not row.suppressed
        ]
        strongest = max(
            mature,
            key=lambda row: (row.similarity, row.episode_count, row.assembly_id),
            default=None,
        )
        activation_rows = tuple(
            sorted(
                (row.assembly_id, round(row.similarity, 12), row.episode_count)
                for row in mature
            )
        )
        keyed[episode.episode_id] = {
            "action": result.action.action,
            "prediction": result.prediction.value,
            "spike_count": len(result.v04_result.spikes),
            "pattern_count": len(result.patterns),
            "mature_activations": activation_rows,
            "runaway": result.stability.runaway,
            "dead": result.stability.dead,
        }
        correct_actions += result.action.action == episode.rewarded_action
        correct_predictions += result.prediction.value == episode.future_event
        prediction_coverage += result.prediction.value is not None
        mature_count += strongest is not None
        similarities.append(strongest.similarity if strongest is not None else 0.0)
        runaway_count += result.stability.runaway
        dead_count += result.stability.dead

    count = len(indexed_episodes)
    aggregate = {
        "action_accuracy": correct_actions / count,
        "prediction_accuracy": correct_predictions / count,
        "prediction_coverage": prediction_coverage / count,
        "assembly_activation_rate": mature_count / count,
        "mean_similarity": statistics.fmean(similarities),
        "runaway_rate": runaway_count / count,
        "dead_rate": dead_count / count,
    }
    return keyed, aggregate


def test_nonlearning_eval_is_order_invariant_at_supported_spacing() -> None:
    """EXPLORATORY / NON_EVIDENTIARY diagnostic.

    The prospective contract is in
    analysis/exploratory/sub_v05_eval_order_dependence_20260920.md.
    This first diagnostic asserts the reduction terminal. If it fails, the
    assertion payload exposes the fixed forward/reverse observations without
    changing the experiment.
    """

    trained = _train_dev_brain()
    episodes = list(held_out_episodes(seed=501, count=8, condition="jitter", start_ms=0.0))
    indexed = list(enumerate(episodes))

    forward_keyed, forward_aggregate = _evaluate_order(trained, indexed)
    reverse_keyed, reverse_aggregate = _evaluate_order(trained, list(reversed(indexed)))

    payload = {
        "forward_keyed": forward_keyed,
        "reverse_keyed": reverse_keyed,
        "forward_aggregate": forward_aggregate,
        "reverse_aggregate": reverse_aggregate,
    }
    assert forward_keyed == reverse_keyed and forward_aggregate == reverse_aggregate, json.dumps(
        payload, sort_keys=True
    )

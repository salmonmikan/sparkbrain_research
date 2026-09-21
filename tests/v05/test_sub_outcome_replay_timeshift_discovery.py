from __future__ import annotations

import json
import warnings

from sparkbrain.v05 import (
    MOTIF_X,
    IntegratedV05Brain,
    make_episode,
    training_episodes,
)

EVENT = "sub-replay-event"
REWARD = 1.0


def _emit(payload: dict[str, object]) -> None:
    warnings.warn(
        "SUB_OUTCOME_REPLAY_TIMESHIFT_RESULT="
        + json.dumps(payload, sort_keys=True, separators=(",", ":")),
        RuntimeWarning,
        stacklevel=2,
    )


def test_fixed_outcome_replay_timeshift_discovery(tmp_path) -> None:
    brain = IntegratedV05Brain()
    for episode in training_episodes(seed=501, count=24, start_ms=0.0):
        result = brain.process_episode(episode.pulses)
        reward = 1.0 if result.action.action == episode.rewarded_action else -0.35
        brain.learn_outcome(next_event=episode.future_event, reward=reward)

    support = make_episode(
        seed=501,
        index=100,
        motif=MOTIF_X,
        condition="motif",
        start_ms=brain.current_time_ms + 100.0,
    )
    brain.process_episode(
        support.pulses,
        learn_assembly=False,
        learn_field=False,
        explore_action=False,
    )

    activation = brain.pending_activation
    action_pending = brain.action_policy.pending
    if (
        activation is None
        or not activation.mature
        or activation.suppressed
        or action_pending is None
    ):
        _emit(
            {
                "terminal": "UNSUPPORTED_NO_PENDING_ASSOCIATION",
                "pending_activation": (
                    None if activation is None else activation.as_dict()
                ),
                "action_pending": (
                    None if action_pending is None else list(action_pending)
                ),
            }
        )
        return

    checkpoint = tmp_path / "support-checkpoint.json"
    brain.save_checkpoint(checkpoint)
    single = IntegratedV05Brain.load_checkpoint(checkpoint)
    replay = IntegratedV05Brain.load_checkpoint(checkpoint)

    single_pre_hash = single.state_hash()
    replay_pre_hash = replay.state_hash()
    if single_pre_hash != replay_pre_hash:
        _emit(
            {
                "terminal": "INVALID_COMPARATOR_OR_RUNTIME",
                "single_pre_hash": single_pre_hash,
                "replay_pre_hash": replay_pre_hash,
            }
        )
        return

    assembly_id, action = action_pending
    learning_rate = single.action_policy.config.learning_rate
    pre_episode_index = single.state_dict()["episode_index"]
    pre_pending_activation = single.pending_activation.as_dict()
    pre_action_pending = list(single.action_policy.pending or ())

    try:
        single.learn_outcome(next_event=EVENT, reward=REWARD)
        replay.learn_outcome(next_event=EVENT, reward=REWARD)
        replay_second_error = None
        try:
            replay.learn_outcome(next_event=EVENT, reward=REWARD)
        except Exception as exc:  # pragma: no cover - terminal data capture
            replay_second_error = f"{type(exc).__name__}: {exc}"
    except Exception as exc:  # pragma: no cover - terminal data capture
        _emit(
            {
                "terminal": "INVALID_COMPARATOR_OR_RUNTIME",
                "first_outcome_error": f"{type(exc).__name__}: {exc}",
            }
        )
        return

    single_count = single.predictor.counts.get(assembly_id, {}).get(EVENT, 0)
    replay_count = replay.predictor.counts.get(assembly_id, {}).get(EVENT, 0)
    single_score = single.action_policy.scores[assembly_id][action]
    replay_score = replay.action_policy.scores[assembly_id][action]
    single_episode_index = single.state_dict()["episode_index"]
    replay_episode_index = replay.state_dict()["episode_index"]
    single_pending_activation = single.pending_activation.as_dict()
    replay_pending_activation = replay.pending_activation.as_dict()
    single_action_pending = list(single.action_policy.pending or ())
    replay_action_pending = list(replay.action_policy.pending or ())

    exact_reduction = (
        replay_second_error is None
        and replay_count == single_count + 1
        and replay_score == single_score + learning_rate * REWARD
        and replay_episode_index == single_episode_index
        and single_episode_index == pre_episode_index
        and single_pending_activation == pre_pending_activation
        and replay_pending_activation == pre_pending_activation
        and single_action_pending == pre_action_pending
        and replay_action_pending == pre_action_pending
    )
    idempotent_or_guarded = (
        replay_second_error is not None
        or (replay_count == single_count and replay_score == single_score)
    )
    if exact_reduction:
        terminal = "ORDINARY_PENDING_STATE_REUSE_REDUCTION"
    elif idempotent_or_guarded:
        terminal = "OUTCOME_CALL_IDEMPOTENT_OR_GUARDED"
    else:
        terminal = "OUTCOME_REPLAY_MUTATES_WITH_UNEXPLAINED_STATE"

    _emit(
        {
            "terminal": terminal,
            "assembly_id": assembly_id,
            "action": action,
            "learning_rate": learning_rate,
            "single_count": single_count,
            "replay_count": replay_count,
            "count_delta": replay_count - single_count,
            "single_score": single_score,
            "replay_score": replay_score,
            "score_delta": replay_score - single_score,
            "single_episode_index": single_episode_index,
            "replay_episode_index": replay_episode_index,
            "pre_episode_index": pre_episode_index,
            "pending_activation_unchanged": (
                single_pending_activation == pre_pending_activation
                and replay_pending_activation == pre_pending_activation
            ),
            "action_pending_unchanged": (
                single_action_pending == pre_action_pending
                and replay_action_pending == pre_action_pending
            ),
            "single_pre_hash": single_pre_hash,
            "replay_pre_hash": replay_pre_hash,
            "single_post_hash": single.state_hash(),
            "replay_post_hash": replay.state_hash(),
            "replay_second_error": replay_second_error,
        }
    )

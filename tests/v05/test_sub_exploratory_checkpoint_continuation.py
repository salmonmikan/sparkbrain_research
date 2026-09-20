from __future__ import annotations

from pathlib import Path

from sparkbrain.v05 import IntegratedV05Brain, training_episodes


def _reward_for(result_action: str | None, rewarded_action: str) -> float:
    return 1.0 if result_action == rewarded_action else -0.35


def _apply_episode(brain: IntegratedV05Brain, episode) -> tuple[dict, dict, dict]:
    result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
    before_outcome = brain.state_dict()
    brain.learn_outcome(
        next_event=episode.future_event,
        reward=_reward_for(result.action.action, episode.rewarded_action),
    )
    after_outcome = brain.state_dict()
    return result.as_dict(), before_outcome, after_outcome


def test_exploratory_checkpoint_continuation_is_equivalent(tmp_path: Path) -> None:
    """EXPLORATORY / NON_EVIDENTIARY checkpoint continuation diagnostic."""
    episodes = training_episodes(seed=777, count=6)
    original = IntegratedV05Brain()

    for episode in episodes[:4]:
        _apply_episode(original, episode)

    checkpoint = tmp_path / "v05-checkpoint.json"
    original.save_checkpoint(checkpoint)
    restored = IntegratedV05Brain.load_checkpoint(checkpoint)

    assert restored.state_dict() == original.state_dict()

    for episode in episodes[4:]:
        original_result, original_before, original_after = _apply_episode(original, episode)
        restored_result, restored_before, restored_after = _apply_episode(restored, episode)

        assert restored_result == original_result
        assert restored_before == original_before
        assert restored_after == original_after

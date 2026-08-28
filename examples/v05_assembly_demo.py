from __future__ import annotations

import json

from sparkbrain.v05 import IntegratedV05Brain, held_out_episodes, training_episodes


def main() -> int:
    brain = IntegratedV05Brain()
    for episode in training_episodes(seed=501, count=16):
        result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
        reward = 1.0 if result.action.action == episode.rewarded_action else -0.35
        brain.learn_outcome(next_event=episode.future_event, reward=reward)
    episode = held_out_episodes(seed=501, count=1, condition="jitter")[0]
    result = brain.process_episode(
        episode.pulses,
        episode_id=episode.episode_id,
        learn_assembly=False,
        learn_field=False,
    )
    print(json.dumps({
        "action": result.action.as_dict(),
        "assemblies": [row.as_dict() for row in result.assembly_activations],
        "expected_action": episode.rewarded_action,
        "expected_prediction": episode.future_event,
        "prediction": result.prediction.as_dict(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import copy
import hashlib

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v05 import IntegratedV05Brain, training_episodes


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def test_step_result_state_hash_is_pre_bookkeeping_state() -> None:
    episode = training_episodes(seed=501, count=1)[0]
    brain = IntegratedV05Brain()

    result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
    post_return_hash = brain.state_hash()

    assert result.state_hash != post_return_hash

    reduced = copy.deepcopy(brain.state_dict())
    assert len(reduced["trace"]) == 1
    assert reduced["episode_index"] == 1
    reduced["trace"] = reduced["trace"][:-1]
    reduced["episode_index"] -= 1

    assert _digest(reduced) == result.state_hash

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.v05 import IntegratedV05Brain, held_out_episodes, training_episodes


def trained_brain(count: int = 8) -> IntegratedV05Brain:
    brain = IntegratedV05Brain()
    for episode in training_episodes(seed=501, count=count):
        result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
        brain.learn_outcome(
            next_event=episode.future_event,
            reward=1.0 if result.action.action == episode.rewarded_action else -0.35,
        )
    return brain


def test_runtime_never_receives_motif_id() -> None:
    episode = training_episodes(seed=501, count=1)[0]
    assert "motif" not in episode.pulses[0].metadata
    brain = IntegratedV05Brain()
    result = brain.process_episode(
        episode.pulses,
        metadata={"condition": episode.condition},
        episode_id=episode.episode_id,
    )
    assert "motif_name" not in result.metadata


def test_training_and_held_out_episode_run() -> None:
    brain = trained_brain()
    episode = held_out_episodes(
        seed=501,
        count=1,
        condition="jitter",
        start_ms=brain.current_time_ms + 100,
    )[0]
    result = brain.process_episode(
        episode.pulses,
        episode_id=episode.episode_id,
        learn_assembly=False,
        learn_field=False,
        explore_action=False,
    )
    assert result.end_ms > result.start_ms
    assert result.state_hash



def test_primary_patterns_exclude_receptor_units() -> None:
    brain = IntegratedV05Brain()
    episode = training_episodes(seed=501, count=1)[0]
    result = brain.process_episode(episode.pulses, episode_id=episode.episode_id)
    receptor_ids = set(brain.base.field.receptor_ids)
    assert result.patterns
    assert all(pattern.source_kind == "internal_reservoir" for pattern in result.patterns)
    assert all(not (set(pattern.unit_ids) & receptor_ids) for pattern in result.patterns)

def test_checkpoint_restores_pending_state_and_detects_tamper(tmp_path: Path) -> None:
    brain = trained_brain(4)
    path = tmp_path / "brain.json"
    brain.save_checkpoint(path)
    restored = IntegratedV05Brain.load_checkpoint(path)
    assert restored.state_dict() == brain.state_dict()
    wrapper = json.loads(path.read_text())
    wrapper["payload"]["episode_index"] += 1
    path.write_text(json.dumps(wrapper))
    with pytest.raises(ValueError, match="hash mismatch"):
        IntegratedV05Brain.load_checkpoint(path)


def test_unit_suppression_is_reversible() -> None:
    brain = IntegratedV05Brain()
    brain.suppress_units([0, 1])
    assert brain.suppressed_unit_ids == {0, 1}
    brain.clear_unit_suppression()
    assert not brain.suppressed_unit_ids

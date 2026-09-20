from __future__ import annotations

from sparkbrain.v05 import IntegratedV05Brain, V05BrainConfig, training_episodes


def _config() -> V05BrainConfig:
    return V05BrainConfig(
        enable_homeostasis=False,
        enable_weight_learning=False,
        enable_delay_learning=False,
        enable_reward_modulation=False,
        enable_prediction=False,
        enable_action=False,
    )


def _template_pattern():
    episode = training_episodes(seed=913, count=1)[0]
    brain = IntegratedV05Brain(_config())
    result = brain.process_episode(
        episode.pulses,
        episode_id="template",
        learn_assembly=False,
        learn_field=False,
        explore_action=False,
    )
    assert result.patterns
    return episode, result.patterns[0]


def _seed_mature(brain: IntegratedV05Brain, pattern) -> str:
    activation = None
    for index in range(3):
        activation = brain.assemblies.observe(
            pattern,
            time_ms=float(index),
            episode_id=f"assembly-seed-{index}",
            learn=True,
        )
    assert activation is not None
    assert activation.mature
    return activation.assembly_id


def _run_probe(brain: IntegratedV05Brain, episode, episode_id: str):
    return brain.process_episode(
        episode.pulses,
        episode_id=episode_id,
        learn_assembly=False,
        learn_field=False,
        explore_action=False,
    )


def test_mature_assembly_recognition_does_not_feed_back_into_field_dynamics() -> None:
    episode, pattern = _template_pattern()
    mature = IntegratedV05Brain(_config())
    empty = IntegratedV05Brain(_config())
    _seed_mature(mature, pattern)

    mature_result = _run_probe(mature, episode, "probe-mature")
    empty_result = _run_probe(empty, episode, "probe-empty")

    assert any(row.mature for row in mature_result.assembly_activations)
    assert not empty_result.assembly_activations
    assert mature_result.v04_result.as_dict() == empty_result.v04_result.as_dict()
    assert mature.base.field.state_dict() == empty.base.field.state_dict()


def test_assembly_suppression_changes_readout_status_not_lower_field_dynamics() -> None:
    episode, pattern = _template_pattern()
    unsuppressed = IntegratedV05Brain(_config())
    suppressed = IntegratedV05Brain(_config())
    unsuppressed_id = _seed_mature(unsuppressed, pattern)
    suppressed_id = _seed_mature(suppressed, pattern)
    assert unsuppressed_id == suppressed_id
    suppressed.suppress_assembly(suppressed_id)

    unsuppressed_result = _run_probe(unsuppressed, episode, "probe-unsuppressed")
    suppressed_result = _run_probe(suppressed, episode, "probe-suppressed")

    assert any(
        row.mature and not row.suppressed for row in unsuppressed_result.assembly_activations
    )
    assert any(row.mature and row.suppressed for row in suppressed_result.assembly_activations)
    assert unsuppressed_result.v04_result.as_dict() == suppressed_result.v04_result.as_dict()
    assert unsuppressed.base.field.state_dict() == suppressed.base.field.state_dict()

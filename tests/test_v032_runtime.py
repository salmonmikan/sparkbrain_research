from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor

import pytest

from sparkbrain.v03 import IntegratedV03Brain, SensorySample, V03BrainConfig
from sparkbrain.v03_seed import (
    IgnitionDecision,
    PersistentBeliefField,
    RevisionBeliefField,
)
from sparkbrain.v032 import IntegratedV032Brain, disable_loser_residual_only

pytestmark = pytest.mark.integration


def sample(index: int, *, value: float = 1.0) -> SensorySample:
    return SensorySample(
        sample_id=f"runtime:{index}",
        time=float(index),
        source_id=f"source-{index}",
        modality="fixture",
        values={"tone": value},
        metadata={"text": "Ada is a bird."},
    )


def test_runtime_preserves_v03_kwargs_and_exact_sensory_diagnostics() -> None:
    brain = IntegratedV032Brain()
    result = brain.step(
        sample(0),
        goal_bias={"fixture:tone": 0.2},
        world_feedback={"status": "observed", "values": {"reward_signal": 0.25}},
    )
    assert result.base_result.world_feedback["status"] == "observed"
    assert result.sensory_channel_trace[0].novelty == 1.0
    assert result.dense_inspection_count == 1
    assert result.accepted_channels == ("fixture:tone",)

    feedback_result = brain.step(
        sample(1, value=2.0),
        world_feedback={"status": "observed", "values": {"reward_signal": 0.5}},
    )
    assert feedback_result.base_result.world_feedback["status"] == "observed"
    assert feedback_result.base_result.action is not None
    assert feedback_result.sensory_channel_trace[0].channel == "fixture:tone"
    assert feedback_result.dense_inspection_count == 1


def test_runtime_patch_is_instance_local_and_removed_after_step() -> None:
    brains = [IntegratedV032Brain(), IntegratedV032Brain()]

    def run(index: int) -> tuple[str, ...]:
        return brains[index].step(sample(index)).accepted_channels

    with ThreadPoolExecutor(max_workers=2) as executor:
        outputs = list(executor.map(run, range(2)))
    assert outputs == [("fixture:tone",), ("fixture:tone",)]
    assert "observe_with_trace" not in vars(brains[0].sensory_field)
    assert "observe_with_trace" not in vars(brains[1].sensory_field)


def test_facades_for_the_same_base_share_a_step_lock() -> None:
    base = IntegratedV03Brain()
    first = IntegratedV032Brain(base=base)
    second = IntegratedV032Brain(base=base)
    assert first._step_lock is second._step_lock


def test_runtime_rejects_ambiguous_or_inexact_base() -> None:
    base = IntegratedV03Brain()
    with pytest.raises(ValueError, match="mutually exclusive"):
        IntegratedV032Brain(V03BrainConfig(), base=base)

    class DerivedBrain(IntegratedV03Brain):
        pass

    with pytest.raises(TypeError, match="exact IntegratedV03Brain"):
        IntegratedV032Brain(base=DerivedBrain())


def test_pure_residual_ablation_changes_only_c15_retention_config() -> None:
    field = RevisionBeliefField()
    field.apply(
        entity_key="entity",
        decision=IgnitionDecision(True, "alpha", "entity", 1.0, 1.0, "test", ()),
        proposal_activation=0.8,
        citations=("evidence-1",),
    )
    before = json.loads(field.serialize_state())
    result = disable_loser_residual_only(field)
    after = json.loads(field.serialize_state())
    assert result.changed_paths == ("config.loser_retention",)
    assert before["states"] == after["states"]
    assert after["config"]["loser_retention"] == 0.0


def test_persistent_field_is_rejected_because_its_factor_is_not_loser_only() -> None:
    field = PersistentBeliefField()
    field.seed(None, "alpha", activation=0.5)
    before = [(row.belief_key, row.activation) for row in field.ranked(None)]
    with pytest.raises(NotImplementedError, match="RevisionBeliefField"):
        disable_loser_residual_only(field)
    assert [(row.belief_key, row.activation) for row in field.ranked(None)] == before

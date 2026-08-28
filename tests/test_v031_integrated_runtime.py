from __future__ import annotations

import copy

import pytest

from sparkbrain.v03 import (
    IntegratedV03Brain,
    SensorySample,
    V03BrainConfig,
    V03StepResult,
)
from sparkbrain.v03_seed import EvidenceContribution


def sample(
    world: str,
    index: int,
    *,
    source: str,
    entity: str | None = None,
    metadata: dict | None = None,
    values: dict[str, float] | None = None,
    correlation_group: str | None = None,
    omitted_channels: tuple[str, ...] = (),
) -> SensorySample:
    return SensorySample(
        sample_id=f"{world}:{index}:{source}",
        time=float(index),
        source_id=source,
        modality="fixture",
        values=values if values is not None else {f"channel-{index}": 1.0},
        omitted_channels=omitted_channels,
        correlation_group=correlation_group,
        entity_hint=entity,
        metadata=metadata or {"text": f"stable {world} target"},
    )


WORLD_FIXTURES = (
    {
        "name": "habituation",
        "invariant": "repetition_suppressed",
        "samples": tuple(
            sample("habituation", index, source="steady", values={"tone": 1.0})
            for index in range(3)
        ),
    },
    {
        "name": "unexpected_change",
        "invariant": "change_recovers_salience",
        "samples": (
            sample("unexpected", 0, source="steady", values={"tone": 1.0}),
            sample("unexpected", 1, source="steady", values={"tone": 1.0}),
            sample("unexpected", 2, source="steady", values={"tone": 0.0}),
        ),
    },
    {
        "name": "goal_target",
        "invariant": "goal_selects_quiet_channel",
        "samples": (
            sample("goal", 0, source="goal-source", values={"quiet": 1.0}),
            sample("goal", 1, source="goal-source", values={"quiet": 1.0}),
            sample("goal", 2, source="goal-source", values={"quiet": 0.4}),
        ),
        "goal_bias": {"fixture:quiet": 2.0},
    },
    {
        "name": "entity_isolation",
        "invariant": "entities_do_not_cross_talk",
        "config": V03BrainConfig(
            entity_track="E1_oracle_entity", allow_oracle_diagnostics=True
        ),
        "samples": (
            sample("entity", 0, source="a-vision", entity="a"),
            sample("entity", 1, source="b-vision", entity="b"),
            sample("entity", 2, source="a-audio", entity="a"),
            sample("entity", 3, source="b-audio", entity="b"),
        ),
    },
    {
        "name": "correlation_and_contradiction",
        "invariant": "dependent_or_contradicted_evidence_does_not_ignite",
        "samples": (
            sample("correlated", 0, source="camera-a", correlation_group="same-frame"),
            sample("correlated", 1, source="camera-b", correlation_group="same-frame"),
            sample("correlated", 2, source="microphone", correlation_group="independent"),
        ),
    },
    {
        "name": "evidence_persistence",
        "invariant": "winner_persists_without_new_evidence",
        "samples": (
            sample("persistence", 0, source="source-a"),
            sample("persistence", 1, source="source-b"),
            sample(
                "persistence",
                2,
                source="source-c",
                values={},
                omitted_channels=("channel-0",),
            ),
        ),
    },
    {
        "name": "belief_reversal",
        "invariant": "counterevidence_enables_revision",
        "samples": (
            sample("reversal", 0, source="old-a", metadata={"text": "alpha zeta"}),
            sample("reversal", 1, source="old-b", metadata={"text": "alpha zeta"}),
            sample("reversal", 20, source="new-a", metadata={"text": "beta omega"}),
            sample("reversal", 21, source="new-b", metadata={"text": "beta omega"}),
        ),
    },
    {
        "name": "world_feedback",
        "invariant": "action_feedback_returns_to_evidence",
        "samples": (
            sample("feedback-world", 0, source="source-a"),
            sample("feedback-world", 1, source="source-b"),
        ),
        "feedback": {
            "status": "observed",
            "text": "environment changed",
            "values": {"reward_signal": 0.25},
        },
    },
)


def ignite(brain: IntegratedV03Brain, world: str = "fixture") -> V03StepResult:
    brain.step(sample(world, 0, source="source-a"))
    return brain.step(sample(world, 1, source="source-b"))


@pytest.mark.parametrize("world", WORLD_FIXTURES, ids=lambda row: row["name"])
def test_eight_world_fixtures_cross_distinct_integrated_invariants(world: dict) -> None:
    brain = IntegratedV03Brain(world.get("config"))
    samples = world["samples"]
    invariant = world["invariant"]

    if invariant == "goal_selects_quiet_channel":
        control = IntegratedV03Brain()
        for sensory in samples[:-1]:
            control.step(sensory)
            brain.step(sensory)
        quiet = control.step(samples[-1])
        biased = brain.step(samples[-1], goal_bias=world["goal_bias"])
        assert len(biased.sparks) > len(quiet.sparks)
        return

    results = []
    for index, sensory in enumerate(samples):
        if invariant == "counterevidence_enables_revision" and index == 2:
            old = results[1].decisions[0].belief_key
            assert old is not None
            brain.ledger.add(
                EvidenceContribution(
                    "counterevidence", "counter-source", old, 2.0, contradiction=10.0
                )
            )
        if invariant == "dependent_or_contradicted_evidence_does_not_ignite" and index == 2:
            belief = results[1].decisions[0].coalitions[0].belief_key
            brain.ledger.add(
                EvidenceContribution(
                    "contradiction", "counter-source", belief, 1.5, contradiction=10.0
                )
            )
        feedback = world.get("feedback") if index == len(samples) - 1 else None
        results.append(brain.step(sensory, world_feedback=feedback))

    if invariant == "repetition_suppressed":
        assert len(results[0].sparks) > sum(len(row.sparks) for row in results[1:])
    elif invariant == "change_recovers_salience":
        assert not results[1].sparks and results[2].sparks
    elif invariant == "entities_do_not_cross_talk":
        assert set(results[-1].beliefs) == {"a", "b"}
        assert all(results[-1].beliefs[entity] is not None for entity in ("a", "b"))
    elif invariant == "dependent_or_contradicted_evidence_does_not_ignite":
        assert results[1].decisions[0].coalitions[0].independent_group_count == 1
        assert not results[1].decisions[0].ignited
        assert results[2].decisions[0].coalitions[0].effective_contradiction > 0
        assert not results[2].decisions[0].ignited
    elif invariant == "winner_persists_without_new_evidence":
        assert results[1].beliefs["__global__"] is not None
        assert results[2].beliefs == results[1].beliefs
    elif invariant == "counterevidence_enables_revision":
        assert results[-1].revision_transitions[0]["transition"] == "revise"
        assert results[-1].revision_transitions[0]["previous_belief"] != results[-1].beliefs[
            "__global__"
        ]
    elif invariant == "action_feedback_returns_to_evidence":
        assert results[-1].action is not None
        assert any(spark.feature_id.endswith("reward_signal") for spark in results[-1].sparks)
    else:  # pragma: no cover - fixture table and assertion dispatcher must evolve together.
        raise AssertionError(f"missing invariant assertion: {invariant}")


def test_public_facade_and_inspection_are_non_mutating() -> None:
    brain = IntegratedV03Brain()
    assert isinstance(brain.config, V03BrainConfig)
    before = brain.state_hash()
    first = brain.inspect()
    first["workspace"].append({"forged": True})
    assert brain.state_hash() == before
    assert brain.inspect()["workspace"] == []


def test_oracle_tracks_are_separated_and_e2_is_not_fabricated() -> None:
    with pytest.raises(ValueError, match="diagnostic-only"):
        IntegratedV03Brain(V03BrainConfig(input_track="I2_symbolic_oracle"))
    with pytest.raises(ValueError, match="diagnostic-only"):
        IntegratedV03Brain(V03BrainConfig(entity_track="E1_oracle_entity"))
    with pytest.raises(NotImplementedError, match="not implemented"):
        IntegratedV03Brain(V03BrainConfig(entity_track="E2_learned_slots"))

    oracle = IntegratedV03Brain(
        V03BrainConfig(
            input_track="I2_symbolic_oracle",
            entity_track="E1_oracle_entity",
            allow_oracle_diagnostics=True,
        )
    )
    literal = {
        "symbolic_event": {
            "kind": "literal",
            "literal": {"entity": "entity-a", "positive": True, "predicate": "opens"},
        }
    }
    result = oracle.step(
        sample("oracle", 0, source="oracle-source", entity="entity-a", metadata=literal)
    )
    assert result.oracle_diagnostic is True
    assert set(result.beliefs) == {"entity-a"}
    with pytest.raises(ValueError, match="cannot consume autonomous world feedback"):
        oracle.step(
            sample("oracle", 1, source="oracle-source-2", entity="entity-a", metadata=literal),
            world_feedback={"values": {"reward": 1.0}},
        )


def test_i3_is_truth_free_and_exposes_revision_and_attribution() -> None:
    brain = IntegratedV03Brain(V03BrainConfig(input_track="I3_truth_free_revision"))
    first = brain.step(sample("i3", 0, source="source-a", metadata={}))
    second = brain.step(sample("i3", 1, source="source-b", metadata={}))

    assert first.model_status == "deterministic_untrained_c15_reference"
    assert first.revision_controller_status == "connected_actual_c15_revision_controller"
    assert len(first.model_hash) == 64
    assert second.revision_transitions[0]["transition"] in {
        "maintain",
        "recover",
        "revise",
        "insufficient_information",
    }
    assert set(second.revision_transitions[0]["transition_probabilities"]) == {
        "insufficient_information",
        "maintain",
        "recover",
        "revise",
    }
    rows = second.attributions[0]["rows"]
    if second.revision_transitions[0]["accepted"]:
        assert rows and sum(row["weight"] for row in rows) == pytest.approx(1.0)
    else:
        assert rows == []

    assert second.oracle_diagnostic is False


def test_action_feedback_returns_as_truth_free_sensory_and_evidence() -> None:
    brain = IntegratedV03Brain()
    brain.step(sample("feedback", 0, source="source-a"))
    result = brain.step(
        sample("feedback", 1, source="source-b"),
        world_feedback={
            "status": "observed",
            "text": "environment changed",
            "values": {"reward_signal": 0.25},
        },
    )

    assert result.action is not None
    assert any(spark.feature_id == "world_feedback:reward_signal" for spark in result.sparks)
    assert len(brain.ledger.rows()) == 3
    assert [event.kind for event in brain.trace.events][-3:] == [
        "workspace_broadcast",
        "sensory_accepted",
        "evidence_added",
    ]
    with pytest.raises(ValueError, match="forbidden evaluator field"):
        brain.step(
            sample("feedback", 2, source="source-c"),
            world_feedback={"values": {"truth": 1.0}},
        )


def test_checkpoint_has_full_inventory_and_restores_exactly() -> None:
    brain = IntegratedV03Brain()
    ignite(brain, "checkpoint")
    checkpoint = brain.checkpoint("checkpoint-a")
    assert set(checkpoint["component_inventory"]) == {
        "belief",
        "coalition",
        "concept",
        "entity",
        "evidence",
        "model",
        "organ",
        "rng",
        "sensory",
        "trace",
        "workspace",
    }
    coalition = checkpoint["component_inventory"]["coalition"]
    assert set(coalition) == {
        "c14_signatures",
        "c14_stability",
        "last_decisions",
        "last_top",
        "last_top_signature",
        "stability",
    }
    assert coalition["last_top"] is not None
    assert coalition["last_top_signature"] is not None
    assert coalition["stability"]

    restored = IntegratedV03Brain.restore(checkpoint)
    assert restored.state_hash() == brain.state_hash()
    assert restored.component_inventory() == brain.component_inventory()
    assert restored.checkpoint("checkpoint-a") == checkpoint


@pytest.mark.parametrize("field", ["model_hash", "final_state_hash", "component_inventory"])
def test_checkpoint_tampering_fails_closed(field: str) -> None:
    brain = IntegratedV03Brain()
    brain.step(sample("tamper", 0, source="source-a"))
    checkpoint = brain.checkpoint("tamper")
    broken = copy.deepcopy(checkpoint)
    if field == "component_inventory":
        broken[field]["workspace"] = [{"forged": True}]
    else:
        broken[field] = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        IntegratedV03Brain.restore(broken)


def test_replay_is_exact_and_inspect_does_not_change_it() -> None:
    brain = IntegratedV03Brain()
    ignite(brain, "replay")
    expected = [item.as_dict() for item in brain._results]
    history = brain.history
    brain.inspect()
    actual = [item.as_dict() for item in brain.replay(history)]
    assert actual == expected

from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_bottom_up_feedback import (
    build_loop,
    probe_summary,
    run_to_target,
)
from forge_prototypes.fly0_hierarchical_loop import WorldState


def test_intact_bottom_up_loop_reaches_target() -> None:
    initial = WorldState(position=2, target=-1)
    loop = build_loop(initial)

    results = run_to_target(loop, max_steps=4)

    assert [result.accepted for result in results] == [True, True, True]
    assert (initial.position, *(result.after.world.position for result in results)) == (
        2,
        1,
        0,
        -1,
    )
    assert loop.snapshot.world.position == -1


def test_observation_payload_cut_fails_closed_before_progress() -> None:
    loop = build_loop(
        WorldState(position=2, target=-1),
        ablation="local_observation_payload_cut",
    )
    before = loop.snapshot

    result = loop.step()

    assert result.accepted is False
    assert result.reason == "action arbitration requires one active module"
    assert result.after == before
    assert loop.snapshot == before


def test_ascending_feedback_cut_blocks_next_modulation() -> None:
    loop = build_loop(
        WorldState(position=2, target=-1),
        ablation="ascending_feedback_payload_cut",
    )

    first = loop.step()
    second = loop.step()

    assert first.accepted is True
    assert first.after.world.position == 1
    assert second.accepted is False
    assert second.reason == "ascending feedback insufficient for modulation"
    assert second.after == first.after
    assert loop.snapshot == first.after


def test_probe_summary_marks_both_bottom_up_edges_causal() -> None:
    summary = probe_summary()
    matrix = summary["causal_matrix"]

    assert matrix["local_observation_payload_causal_for_bounded_trajectory"] is True
    assert matrix["ascending_feedback_payload_causal_for_bounded_trajectory"] is True


def test_checkpoint_restore_replays_exact_history() -> None:
    loop = build_loop(WorldState(position=2, target=-1))
    checkpoint = loop.checkpoint()

    first = run_to_target(loop, max_steps=4)
    first_tokens = [result.after.token() for result in first]
    final_token = loop.snapshot.token()

    loop.restore(checkpoint)
    second = run_to_target(loop, max_steps=4)

    assert [result.after.token() for result in second] == first_tokens
    assert loop.snapshot.token() == final_token


def test_checkpoint_rejects_observation_mask_semantic_mismatch() -> None:
    intact = build_loop(WorldState(position=2, target=-1))
    observation_cut = build_loop(
        WorldState(position=2, target=-1),
        ablation="local_observation_payload_cut",
    )

    with pytest.raises(ValueError, match="observation-mask contract"):
        observation_cut.restore(intact.checkpoint())


def test_checkpoint_rejects_feedback_mask_semantic_mismatch() -> None:
    intact = build_loop(WorldState(position=2, target=-1))
    feedback_cut = build_loop(
        WorldState(position=2, target=-1),
        ablation="ascending_feedback_payload_cut",
    )

    with pytest.raises(ValueError, match="feedback-mask contract"):
        feedback_cut.restore(intact.checkpoint())


def test_probe_summary_is_deterministic() -> None:
    first = probe_summary()
    second = probe_summary()

    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)

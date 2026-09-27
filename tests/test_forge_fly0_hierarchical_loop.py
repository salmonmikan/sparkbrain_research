from __future__ import annotations

from dataclasses import dataclass

import pytest

from forge_prototypes.fly0_hierarchical_loop import (
    ActionProposal,
    HierarchicalSensorimotorLoop,
    LocalFeedback,
    Modulation,
    Observation,
    ReactiveLocalController,
    WorldState,
    build_fly0_loop,
    build_reactive_loop,
    probe_summary,
    run_to_target,
)


def test_fly0_modules_close_bounded_world_loop() -> None:
    loop = build_fly0_loop(WorldState(position=2, target=-1))

    results = run_to_target(loop)

    assert len(results) == 3
    assert all(result.accepted for result in results)
    assert loop.snapshot.world.position == -1
    assert {item.module_id for item in loop.snapshot.feedback} == {
        "fly0-left",
        "fly0-right",
    }


def test_reactive_replacement_preserves_interface_and_function() -> None:
    loop = build_reactive_loop(WorldState(position=-2, target=1))

    results = run_to_target(loop)

    assert len(results) == 3
    assert all(result.accepted for result in results)
    assert loop.snapshot.world.position == 1
    assert sum(item.fired_events for item in loop.snapshot.feedback) == 1


def test_checkpoint_restore_replays_exact_same_history() -> None:
    loop = build_fly0_loop(WorldState(position=2, target=0))
    checkpoint = loop.checkpoint()

    first = run_to_target(loop)
    first_token = loop.snapshot.token()
    loop.restore(checkpoint)
    second = run_to_target(loop)

    assert [item.after.token() for item in first] == [
        item.after.token() for item in second
    ]
    assert loop.snapshot.token() == first_token


@dataclass(frozen=True)
class AlwaysActiveController:
    module_id: str
    side: str
    action: int
    fired_events: int = 1

    def propose(
        self, observation: Observation, modulation: Modulation
    ) -> ActionProposal:
        del observation, modulation
        return ActionProposal(
            module_id=self.module_id,
            action=self.action,
            active=True,
            feedback=LocalFeedback(
                module_id=self.module_id,
                side=self.side,
                fired_events=self.fired_events,
                matched_motor_events=1,
                opposite_motor_events=0,
                first_matched_motor_time=0,
            ),
        )


def test_conflicting_active_modules_roll_back_complete_step() -> None:
    loop = HierarchicalSensorimotorLoop(
        initial_world=WorldState(position=1, target=-1),
        controllers=(
            AlwaysActiveController("left", "left", -1),
            AlwaysActiveController("right", "right", 1),
        ),
    )
    before = loop.snapshot

    result = loop.step()

    assert result.accepted is False
    assert result.reason == "action arbitration requires one active module"
    assert result.after == before
    assert loop.snapshot == before


def test_event_budget_violation_rolls_back() -> None:
    loop = HierarchicalSensorimotorLoop(
        initial_world=WorldState(position=1, target=-1),
        controllers=(
            AlwaysActiveController("left", "left", -1, fired_events=2),
            ReactiveLocalController("right", "right"),
        ),
        event_budget=1,
    )
    before = loop.snapshot

    result = loop.step()

    assert result.accepted is False
    assert result.reason == "local event budget exceeded"
    assert loop.snapshot == before


def test_checkpoint_rejects_controller_mismatch() -> None:
    fly_loop = build_fly0_loop(WorldState(position=1, target=0))
    checkpoint = fly_loop.checkpoint()
    reactive_loop = build_reactive_loop(WorldState(position=1, target=0))

    with pytest.raises(ValueError, match="controller contract"):
        reactive_loop.restore(checkpoint)


def test_feedback_exposes_runtime_metrics_not_world_target() -> None:
    loop = build_fly0_loop(WorldState(position=2, target=0))

    result = loop.step()

    assert result.accepted is True
    for feedback in result.after.feedback:
        assert not hasattr(feedback, "target")
        assert not hasattr(feedback, "oracle")


def test_probe_summary_records_exact_replay_and_resource_mismatch() -> None:
    summary = probe_summary()
    controllers = summary["controllers"]

    assert controllers["fly0_structured"]["same_history_replay_exact"] is True
    assert controllers["reactive_reference"]["same_history_replay_exact"] is True
    assert controllers["fly0_structured"]["active_event_counts"] == [300, 300, 300]
    assert controllers["reactive_reference"]["active_event_counts"] == [1, 1, 1]

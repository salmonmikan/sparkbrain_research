from __future__ import annotations

import json

from forge_prototypes.fly0_interaction_ablation import (
    build_interaction_ablation_report,
)


def _rows() -> dict[str, object]:
    report = build_interaction_ablation_report()
    return {row.condition: row for row in report.rows}


def test_intact_loop_reaches_target_in_three_steps() -> None:
    rows = _rows()
    intact = rows["intact"]

    assert intact.reached_target is True
    assert intact.accepted_steps == 3
    assert intact.rejected_steps == 0
    assert intact.position_trace == (2, 1, 0, -1)


def test_local_observation_payload_cut_preserves_bounded_trajectory() -> None:
    rows = _rows()

    assert rows["local_observation_payload_cut"].position_trace == (
        rows["intact"].position_trace
    )
    assert rows["local_observation_payload_cut"].reached_target is True


def test_ascending_feedback_payload_cut_preserves_world_trajectory() -> None:
    rows = _rows()
    feedback_cut = rows["ascending_feedback_payload_cut"]

    assert feedback_cut.position_trace == rows["intact"].position_trace
    assert feedback_cut.reached_target is True
    assert feedback_cut.feedback_payload_present is False


def test_descending_modulation_cut_fails_closed_without_world_progress() -> None:
    rows = _rows()
    modulation_cut = rows["descending_modulation_cut"]

    assert modulation_cut.reached_target is False
    assert modulation_cut.accepted_steps == 0
    assert modulation_cut.rejected_steps == 1
    assert modulation_cut.final_position == 2
    assert modulation_cut.first_rejection_reason == (
        "action arbitration requires one active module"
    )


def test_local_action_cut_prevents_progress_even_when_steps_commit() -> None:
    rows = _rows()
    action_cut = rows["local_action_cut"]

    assert action_cut.reached_target is False
    assert action_cut.accepted_steps == 4
    assert action_cut.rejected_steps == 0
    assert action_cut.position_trace == (2, 2, 2, 2, 2)


def test_report_localizes_current_causal_interface_edges() -> None:
    report = build_interaction_ablation_report()

    assert report.local_observation_payload_causal_for_bounded_trajectory is False
    assert report.ascending_feedback_payload_causal_for_bounded_trajectory is False
    assert report.descending_modulation_required_for_bounded_progress is True
    assert report.local_action_required_for_bounded_progress is True
    assert report.reason_codes == (
        "LOCAL_OBSERVATION_PAYLOAD_NOT_CAUSALLY_CONSUMED",
        "ASCENDING_FEEDBACK_PAYLOAD_NOT_CAUSALLY_CONSUMED",
        "DESCENDING_MODULATION_REQUIRED_FOR_PROGRESS",
        "LOCAL_ACTION_REQUIRED_FOR_PROGRESS",
    )


def test_report_is_deterministic() -> None:
    first = build_interaction_ablation_report().summary()
    second = build_interaction_ablation_report().summary()

    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)

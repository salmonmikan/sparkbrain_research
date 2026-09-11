from __future__ import annotations

import pytest

from sparkbrain.v061_a01.md002_p2_schedule import (
    P2AttributionSubepisode,
    P2ClonedSubepisodeSchedule,
    P2SharedProbeSchedule,
    build_p2_condition_matrix,
)


def schedule() -> P2ClonedSubepisodeSchedule:
    return P2ClonedSubepisodeSchedule(
        subepisodes=(
            P2AttributionSubepisode(
                proposal_id="proposal-a",
                boundary_event_id="boundary-a",
                response_event_id="response-a",
                boundary_time_ms=20.0,
                response_time_ms=22.0,
            ),
            P2AttributionSubepisode(
                proposal_id="proposal-b",
                boundary_event_id="boundary-b",
                response_event_id="response-b",
                boundary_time_ms=20.0,
                response_time_ms=22.0,
            ),
        ),
        shared_probe=P2SharedProbeSchedule(
            cue_event_id="shared-root-probe",
            cue_time_ms=40.0,
            root_target="A",
            origin_state_hash="field:shared-root",
        ),
    )


def test_p2_matrix_fixes_exact_four_conditions_and_common_schedule() -> None:
    matrix = build_p2_condition_matrix(schedule())
    assert tuple(row["condition_id"] for row in matrix) == (
        "p2-w0-returned",
        "p2-w1-returned",
        "p2-w0-withheld",
        "p2-w1-withheld",
    )
    assert tuple((row["world_arm"], row["returned_external_evidence"]) for row in matrix) == (
        ("control", True),
        ("intervention", True),
        ("control", False),
        ("intervention", False),
    )
    assert len({repr(row["schedule"]) for row in matrix}) == 1
    assert "expected" not in repr(matrix).lower()
    assert "path" not in repr(matrix).lower()


def test_p2_schedule_requires_matched_cloned_subepisode_clocks() -> None:
    value = schedule()
    mismatched = P2ClonedSubepisodeSchedule(
        subepisodes=(
            value.subepisodes[0],
            P2AttributionSubepisode(
                proposal_id="proposal-b",
                boundary_event_id="boundary-b",
                response_event_id="response-b",
                boundary_time_ms=21.0,
                response_time_ms=23.0,
            ),
        ),
        shared_probe=value.shared_probe,
    )
    with pytest.raises(ValueError, match="matched clocks"):
        mismatched.validate()


def test_p2_schedule_requires_distinct_anonymous_proposal_identities() -> None:
    value = schedule()
    duplicate = P2ClonedSubepisodeSchedule(
        subepisodes=(
            value.subepisodes[0],
            P2AttributionSubepisode(
                proposal_id=value.subepisodes[0].proposal_id,
                boundary_event_id="boundary-b",
                response_event_id="response-b",
                boundary_time_ms=20.0,
                response_time_ms=22.0,
            ),
        ),
        shared_probe=value.shared_probe,
    )
    with pytest.raises(ValueError, match="distinct proposal"):
        duplicate.validate()


def test_p2_shared_probe_must_follow_attribution_response() -> None:
    value = schedule()
    invalid = P2ClonedSubepisodeSchedule(
        subepisodes=value.subepisodes,
        shared_probe=P2SharedProbeSchedule(
            cue_event_id="too-early",
            cue_time_ms=22.0,
            root_target="A",
            origin_state_hash="field:shared-root",
        ),
    )
    with pytest.raises(ValueError, match="after attribution response"):
        invalid.validate()

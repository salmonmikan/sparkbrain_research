from __future__ import annotations

from sparkbrain.v061_a01.md002_development_plan import build_p2_development_plan
from sparkbrain.v061_a01.md002_fixtures import FrozenPartitionBytes, P2WorldOnlyFixture
from sparkbrain.v061_a01.md002_p2_schedule import (
    P2AttributionSubepisode,
    P2ClonedSubepisodeSchedule,
    P2SharedProbeSchedule,
)


def fixture() -> P2WorldOnlyFixture:
    return P2WorldOnlyFixture(
        checkpoint=FrozenPartitionBytes(
            local=b"local-checkpoint",
            field=b"field-checkpoint",
            consistency=b"consistency-checkpoint",
            return_address=b"return-address-checkpoint",
        ),
        control_world_relation=b"world-control",
        intervention_world_relation=b"world-intervention",
        admissible_external_evidence=b"shared-evidence",
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


def test_development_plan_binds_exact_four_conditions_without_executing() -> None:
    value = build_p2_development_plan(fixture(), schedule())

    assert tuple(row.condition_id for row in value) == (
        "p2-w0-returned",
        "p2-w1-returned",
        "p2-w0-withheld",
        "p2-w1-withheld",
    )
    assert tuple((row.world_arm, row.returned_external_evidence) for row in value) == (
        ("control", True),
        ("intervention", True),
        ("control", False),
        ("intervention", False),
    )
    assert len({row.arm_input.partitions for row in value}) == 1
    assert len({row.arm_input.admissible_external_evidence for row in value}) == 1
    assert all(row.schedule is value[0].schedule for row in value)


def test_withheld_conditions_change_only_future_return_flag() -> None:
    value = {row.condition_id: row for row in build_p2_development_plan(fixture(), schedule())}

    w0_returned = value["p2-w0-returned"]
    w0_withheld = value["p2-w0-withheld"]
    assert w0_returned.arm_input == w0_withheld.arm_input
    assert w0_returned.schedule is w0_withheld.schedule
    assert w0_returned.returned_external_evidence is True
    assert w0_withheld.returned_external_evidence is False

    w1_returned = value["p2-w1-returned"]
    w1_withheld = value["p2-w1-withheld"]
    assert w1_returned.arm_input == w1_withheld.arm_input
    assert w1_returned.schedule is w1_withheld.schedule
    assert w1_returned.returned_external_evidence is True
    assert w1_withheld.returned_external_evidence is False


def test_world_intervention_changes_only_world_relation_bytes_at_plan_stage() -> None:
    value = {row.condition_id: row for row in build_p2_development_plan(fixture(), schedule())}
    control = value["p2-w0-returned"].arm_input
    intervention = value["p2-w1-returned"].arm_input

    assert control.partitions == intervention.partitions
    assert control.admissible_external_evidence == intervention.admissible_external_evidence
    assert control.world_relation != intervention.world_relation

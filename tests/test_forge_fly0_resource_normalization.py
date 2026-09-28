from __future__ import annotations

import json

import pytest

from forge_prototypes.fly0_resource_normalization import (
    build_resource_normalization_report,
    require_matched_activity_exposure,
)


def test_common_interface_exposure_is_matched_but_activity_is_not() -> None:
    report = build_resource_normalization_report()

    assert report.common_interface_exposure_matched is True
    assert report.activity_instrumentation_commensurate is False
    assert report.activity_resource_exposure_matched is False
    assert report.reason_codes == (
        "DISTINCT_ACTIVITY_INSTRUMENTATION",
        "RAW_ACTIVITY_EXPOSURE_MISMATCH",
    )


def test_normalized_rows_keep_activity_basis_attached() -> None:
    summary = build_resource_normalization_report().summary()
    structured = summary["rows"]["fly0_structured"]
    reactive = summary["rows"]["reactive_reference"]

    assert structured["common_surface_per_transition"] == (
        reactive["common_surface_per_transition"]
    )
    assert structured["activity_basis"] == "topology_trace_events"
    assert reactive["activity_basis"] == "reactive_activation_events"
    assert structured["activity_per_transition"]["fired_events"] == 288.0
    assert reactive["activity_per_transition"]["fired_events"] == 1.0
    assert structured["fired_events"] == 864
    assert reactive["fired_events"] == 3


def test_same_declared_ceiling_does_not_create_a_resource_match() -> None:
    report = build_resource_normalization_report()

    assert {row.event_budget_per_controller_call for row in report.rows} == {4096}
    assert all(
        0 <= row.activity_per_transition()["peak_budget_fraction"] <= 1
        for row in report.rows
    )
    assert report.activity_resource_exposure_matched is False


def test_strict_match_request_fails_closed_with_reason_codes() -> None:
    report = build_resource_normalization_report()

    with pytest.raises(RuntimeError, match="DISTINCT_ACTIVITY_INSTRUMENTATION"):
        require_matched_activity_exposure(report)


def test_report_is_deterministic_and_replay_exact() -> None:
    first = build_resource_normalization_report()
    second = build_resource_normalization_report()

    assert json.dumps(first.summary(), sort_keys=True) == json.dumps(
        second.summary(), sort_keys=True
    )
    assert all(row.replay_exact for row in first.rows)
    assert first.status == "NON_EVIDENTIARY_NONCANONICAL_FORGE"

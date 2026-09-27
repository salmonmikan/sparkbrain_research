from __future__ import annotations

from pathlib import Path

from scripts.audit_rv02_rd006_v3_causal_opportunity import (
    ADJACENT_ONLY,
    CEILING_CENSORED,
    LAG_OUTSIDE,
    NO_OTHER_CONSTRUCTION_SOURCE,
    NO_SECOND_HIDDEN_SPIKE,
    SPIKE_WITHOUT_EDGE,
    build_audit,
)

ARTIFACT = Path(
    "artifacts/rv02_rd006/"
    "external_learning_reachability_a_v3_d0_execution/"
    "attempt-001/artifact.json.gz"
)


def test_audit_binds_exact_preserved_result_without_dynamic_execution() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["preserved_result_head"] == (
        "540fa54f45a8cdc467eb2695270035cb9332f2fb"
    )
    assert audit["preserved_source_head"] == (
        "8867c0565e25a0c76749c12eec7f4c03238b7aef"
    )
    assert audit["new_dynamic_execution"] is False
    assert audit["artifact_mutated"] is False
    assert audit["capability_scoring"] is False
    assert audit["preserved_v3_result_changed"] is False


def test_every_planned_clock_receives_one_mutually_exclusive_cause() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["planned_clock_count"] == 832
    assert audit["inspected_clock_count"] == 816
    assert audit["aggregate_cause_counts"] == {
        NO_SECOND_HIDDEN_SPIKE: 433,
        SPIKE_WITHOUT_EDGE: 10,
        LAG_OUTSIDE: 0,
        ADJACENT_ONLY: 1,
        CEILING_CENSORED: 16,
        NO_OTHER_CONSTRUCTION_SOURCE: 372,
    }
    assert sum(audit["aggregate_cause_counts"].values()) == 832
    assert all(
        sum(cell["cause_counts"].values()) == cell["planned_clock_count"]
        for cell in audit["cells"]
    )


def test_off_on_and_completed_bounded_counts_remain_separate() -> None:
    audit = build_audit(ARTIFACT)
    grouped = audit["cause_counts_by_arm_and_completion"]
    assert set(grouped) == {
        "external_learning_off/COMPLETE",
        "external_learning_on/COMPLETE",
        "external_learning_on/BOUNDED",
    }
    assert sum(grouped["external_learning_off/COMPLETE"].values()) == 416
    assert sum(grouped["external_learning_on/COMPLETE"].values()) == 368
    assert sum(grouped["external_learning_on/BOUNDED"].values()) == 48
    assert grouped["external_learning_on/BOUNDED"][CEILING_CENSORED] == 16


def test_adjacent_only_and_ceiling_rows_do_not_infer_same_clock_outcomes() -> None:
    audit = build_audit(ARTIFACT)
    adjacent = [
        row
        for cell in audit["cells"]
        for row in cell["clock_audit"]
        if row["cause"] == ADJACENT_ONLY
    ]
    assert [(row["return_event_id"], row["return_unit_id"]) for row in adjacent] == [
        ("rd006-v2-ext-000030", 27)
    ]
    assert {
        source
        for neighbor in adjacent[0]["adjacent_clock_eligible_sources"]
        for source in neighbor["eligible_hidden_source_ids"]
    } == {36, 37}

    censored = [
        row
        for cell in audit["cells"]
        for row in cell["clock_audit"]
        if row["cause"] == CEILING_CENSORED
    ]
    assert len(censored) == 16
    assert all(row["observed"] is False for row in censored)
    assert all(row["dynamic_gate_deficit"] is None for row in censored)


def test_fixed_gate_deficit_and_recommendation_are_bounded() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["minimum_deficit_to_fixed_two_source_gate"] == {
        "minimum_observed_clock_deficit": 1,
        "maximum_observed_clock_deficit": 2,
        "sum_over_inspected_clocks": 1625,
        "unobserved_ceiling_censored_clocks_excluded": 16,
    }
    recommendation = audit["recommendation"]
    assert recommendation["disposition"] == "ONE_FRESH_PROSPECTIVE_REVISION"
    assert recommendation["single_changed_invariant"] == (
        "ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY"
    )
    assert recommendation["implementation_or_execution_authorized"] is False
    assert audit["later_e0_e1_es_authorized"] is False

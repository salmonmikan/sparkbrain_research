from pathlib import Path

from scripts.audit_rv02_rd006_v4_return_alignment import (
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
    "external_learning_reachability_a_v4_d0_execution/"
    "attempt-001/artifact.json.gz"
)


def test_exact_preserved_result_and_no_dynamic_execution() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["preserved_result_head"] == "50112626ef6a4da364e3fa9268e8feb0d723ea7f"
    assert audit["preserved_source_head"] == "44bef35c90f24a11e27000e3c328778733da92b6"
    assert audit["new_dynamic_execution"] is False
    assert audit["artifact_mutated"] is False
    assert audit["result_reclassified"] is False
    assert audit["preserved_v4_result_changed"] is False


def test_each_planned_on_clock_has_one_exclusive_class() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["planned_on_clock_count"] == 416
    assert audit["inspected_on_clock_count"] == 400
    assert audit["aggregate_cause_counts"] == {
        NO_SECOND_HIDDEN_SPIKE: 205,
        SPIKE_WITHOUT_EDGE: 11,
        LAG_OUTSIDE: 0,
        ADJACENT_ONLY: 0,
        CEILING_CENSORED: 16,
        NO_OTHER_CONSTRUCTION_SOURCE: 184,
    }
    assert sum(audit["aggregate_cause_counts"].values()) == 416
    assert all(
        sum(cell["cause_counts"].values()) == cell["planned_clock_count"]
        for cell in audit["cells"]
    )


def test_fixed_gate_deficit_and_censoring_are_bounded() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["minimum_deficit_to_fixed_two_source_gate"] == {
        "minimum_observed_clock_deficit": 1,
        "maximum_observed_clock_deficit": 2,
        "sum_over_inspected_on_clocks": 793,
        "unobserved_ceiling_censored_on_clocks_excluded": 16,
    }
    censored = [
        row
        for cell in audit["cells"]
        for row in cell["clock_audit"]
        if row["cause"] == CEILING_CENSORED
    ]
    assert len(censored) == 16
    assert all(
        row["observed"] is False and row["dynamic_gate_deficit"] is None
        for row in censored
    )


def test_port_to_hidden_linkage_is_descriptive_only() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["port_to_hidden_update_linkage_aggregate"] == {
        "port_to_hidden_update_count": 58,
        "target_hidden_spike_located_count": 58,
        "updates_followed_by_later_same_source_hidden_spike": 51,
        "updates_followed_by_later_same_source_dynamic_eligible_spike": 6,
    }
    assert audit["linkage_interpretation"]["status"] == "DESCRIPTIVE_NOT_CAUSAL"
    assert audit["linkage_interpretation"]["causal_effect_identified"] is False


def test_audit_stops_without_a_new_invariant_proposal() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["recommendation"]["disposition"] == "NO_PROPOSAL"
    assert audit["recommendation"]["implementation_or_execution_authorized"] is False
    assert audit["later_e0_e1_es_authorized"] is False
    assert audit["scale_expansion_authorized"] is False

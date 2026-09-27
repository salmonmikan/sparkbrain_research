from __future__ import annotations

from pathlib import Path

from scripts.audit_rv02_rd006_v2_static_topology_return_coverage import (
    build_audit,
)
from sparkbrain.research import rv02_rd006_external_learning_reachability as v1
from sparkbrain.research import rv02_rd006_external_learning_reachability_v2 as v2

ARTIFACT = Path(
    "artifacts/rv02_rd006/external_learning_reachability_a_v2_lag_alignment/"
    "attempt-001/artifact.json.gz"
)


def test_audit_uses_preserved_bytes_and_static_construction_only(monkeypatch) -> None:
    def forbidden(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("new dynamics are forbidden in the static audit")

    monkeypatch.setattr(v1, "run_arm", forbidden)
    monkeypatch.setattr(v1, "run_cell", forbidden)
    monkeypatch.setattr(v1, "run_matrix", forbidden)
    monkeypatch.setattr(v2, "run_cell", forbidden)
    monkeypatch.setattr(v2, "run_matrix", forbidden)

    audit = build_audit(ARTIFACT)
    assert audit["new_dynamic_execution"] is False
    assert audit["new_result_bearing_matrix"] is False
    assert audit["topology_mutated"] is False
    assert audit["observed_spike_identity_used_for_edge_selection"] is False


def test_current_structural_and_temporal_census_matches_r148() -> None:
    audit = build_audit(ARTIFACT)
    aggregate = audit["aggregate"]
    assert aggregate["inspected_on_arm_clocks"] == 400
    assert aggregate["unobserved_on_arm_clocks"] == 16
    assert aggregate["time_aligned_ge_1"] == 51
    assert aggregate["time_aligned_ge_2"] == 12
    assert aggregate["current_eligible_ge_1"] == 7
    assert aggregate["current_eligible_ge_2"] == 0


def test_role_rule_is_budget_matched_but_not_claimed_sufficient() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["disposition"]["static_role_rule_budget_feasibility"] == (
        "STRUCTURALLY_FEASIBLE_UNDER_SAME_UNIT_COUNT_AND_EDGE_BUDGET"
    )
    assert audit["disposition"]["static_role_rule_preserved_timing_sufficiency"] == (
        "NOT_SUFFICIENT_ON_PRESERVED_V2_TIMING"
    )
    assert audit["aggregate"]["role_rule_eligible_ge_2"] == 0
    for family in audit["families"]:
        rule = family["static_role_rule"]
        assert rule["observed_spike_id_input"] is False
        assert rule["planned_total_edge_count"] == 384
        assert rule["planned_mean_out_degree"] == 8.0
        assert rule["added_edge_count"] == rule["removed_edge_count"]
        assert rule["port_source_edges_preserved"] is True
        assert rule["required_route_edges_preserved"] is True
        assert rule["all_return_units_have_two_role_sources"] is True
        assert all(
            row["planned_hidden_incoming_count"] >= 2
            for row in family["return_units"]
        )


def test_v2_and_later_stages_remain_closed() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["disposition"]["current_v2_contract"] == (
        "CLOSED_UNCHANGED_D0_INCONCLUSIVE_BOUNDED_EXPLOSION"
    )
    assert audit["optional_prospective_v3_contract_proposal"]["status"] == (
        "PROPOSAL_ONLY_NOT_AUTHORIZED_FOR_EXECUTION"
    )
    assert audit["v3_execution_authorized"] is False
    assert audit["later_e0_e1_es_authorized"] is False
    assert audit["scale_expansion_authorized"] is False
    assert audit["reservoir_comparison_authorized"] is False

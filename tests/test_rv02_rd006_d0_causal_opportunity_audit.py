from __future__ import annotations

from pathlib import Path

from scripts.audit_rv02_rd006_d0_causal_opportunity import build_audit

ARTIFACT = Path(
    "artifacts/rv02_rd006/external_learning_reachability_a_v1/"
    "attempt-002/artifact.json.gz"
)


def test_preserved_audit_reconstructs_identity_without_new_execution() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["preserved_result_head"] == (
        "49b91ca801522f3d6685ebd22097a1e64f9234c9"
    )
    assert audit["new_dynamic_execution"] is False
    assert audit["execution_procedure_nonconformance"] == {
        "observed": True,
        "class": "NON_PERSISTED_LOCAL_DYNAMIC_UNIT_TEST_INVOCATION",
        "command_scope": "tests/test_rv02_rd006_external_learning_reachability.py",
        "used_for_audit": False,
        "persisted_as_scientific_output": False,
        "preserved_v1_mutated": False,
        "follow_up": "DISCLOSE_TO_EVIDENCE_ANALYST_AND_DO_NOT_REPEAT",
    }
    assert audit["capability_scoring"] is False
    assert audit["v1_result_changed"] is False
    assert len(audit["cells"]) == 6


def test_external_trace_rule_cannot_directly_update_hidden_boundary_edges() -> None:
    audit = build_audit(ARTIFACT)
    contract = audit["ordinary_external_learner_contract"]
    assert contract["directly_updatable_edge_classes"] == ["PORT_TO_PORT"]
    assert contract["port_to_hidden_direct_update_possible"] is False
    assert contract["hidden_to_port_direct_update_possible"] is False
    for cell in audit["cells"]:
        for arm in cell["arms"]:
            assert set(arm["actual_ordinary_update_class_counts"]) <= {
                "PORT_TO_PORT"
            }


def test_bounded_arm_does_not_infer_unobserved_clocks() -> None:
    audit = build_audit(ARTIFACT)
    opposing = next(
        cell for cell in audit["cells"] if cell["family"] == "opposing-reversal"
    )
    on = next(
        arm for arm in opposing["arms"] if arm["arm"] == "external_learning_on"
    )
    assert on["inspected_clock_count"] == 32
    assert len(on["clock_audit"]) == 32
    assert on["bounded_failure_clock"]["failure_class"] == (
        "BOUNDED_EXPLOSION_BEFORE_DECISION"
    )
    assert on["bounded_failure_clock"]["unobserved_clock_count"] == 16
    assert on["pre_ceiling_causal_opportunity"] == {
        "structural_return_edge_observed": True,
        "eligible_single_or_multi_source_observed": False,
        "eligible_multi_source_observed": False,
    }


def test_preserved_clock_failure_census_is_complete_and_non_capability_scored() -> None:
    audit = build_audit(ARTIFACT)
    assert audit["aggregate_failure_class_counts"] == {
        "NO_STRUCTURAL_RETURN_EDGE": 124,
        "STRUCTURAL_EDGE_NO_HIDDEN_SPIKE": 684,
        "HIDDEN_SPIKE_OUTSIDE_LAG": 8,
        "BOUNDED_EXPLOSION_BEFORE_DECISION": 1,
    }
    inspected = sum(
        arm["inspected_clock_count"]
        for cell in audit["cells"]
        for arm in cell["arms"]
    )
    assert inspected == 816
    assert not any(
        name in audit["aggregate_failure_class_counts"]
        for name in ("ELIGIBLE_SINGLE_SOURCE_ONLY", "ELIGIBLE_MULTI_SOURCE")
    )


def test_only_connected_hidden_spikes_are_simultaneous_with_return() -> None:
    audit = build_audit(ARTIFACT)
    timing_rows = [
        clock["nearest_structurally_connected_hidden_spike"]
        for cell in audit["cells"]
        for arm in cell["arms"]
        for clock in arm["clock_audit"]
        if clock["nearest_structurally_connected_hidden_spike"] is not None
    ]
    assert len(timing_rows) == 8
    assert {row["lag_ms"] for row in timing_rows} == {0.0}
    assert {row["distance_to_fixed_window_ms"] for row in timing_rows} == {0.5}


def test_every_family_has_some_structural_return_opportunity() -> None:
    audit = build_audit(ARTIFACT)
    assert all(
        any(
            arm["pre_ceiling_causal_opportunity"][
                "structural_return_edge_observed"
            ]
            for arm in cell["arms"]
        )
        for cell in audit["cells"]
    )

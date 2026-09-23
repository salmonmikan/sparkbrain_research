from __future__ import annotations

from sparkbrain.v05.route_preformal_r2 import (
    ANALYST_AUTHORITY,
    CUE_POLICY,
    DEVELOPMENT_REVISION,
    PRIMARY_REDUCTION,
    RESPONSE_FIELDS,
    SECONDARY_EXPORT,
    bind_preformal_r2_contract_closure,
)


def test_r2_closure_binds_canonical_r92_and_stays_non_result() -> None:
    closure, queue = bind_preformal_r2_contract_closure()
    assert ANALYST_AUTHORITY == "EVA-20260923T105725+0900-R92-6B8E31D4"
    assert closure.development_revision == DEVELOPMENT_REVISION
    assert closure.prior_development_result == "D34-Q001"
    assert closure.prior_result_preserved_unchanged is True
    assert closure.response_bearing_execution_allowed is False
    assert closure.fresh_analyst_ready_review_required is True
    assert closure.formal_action_allowed is False
    assert queue.status == "AWAITING_FRESH_ANALYST_READY_REVIEW"
    assert queue.response_bearing_execution_performed is False
    assert queue.formal_action_performed is False


def test_r2_opportunity_ledger_uses_source_only_cues() -> None:
    closure, _ = bind_preformal_r2_contract_closure()
    assert closure.cue_policy == CUE_POLICY
    assert closure.opportunity_ledger
    for row in closure.opportunity_ledger:
        assert row.target_cue_source_id == row.target_edge.source_id
        assert row.control_cue_source_id == row.matched_control_edge.source_id
        assert row.target_destination_directly_cued is False
        assert row.control_destination_directly_cued is False
        assert row.target_cue_source_id != row.target_edge.target_id
        assert row.control_cue_source_id != row.matched_control_edge.target_id
        assert row.sign_class_matched is True
        assert row.plasticity_matched is True
        assert row.causal_opportunity_predeclared is True
        assert row.target_delayed_arrival_ms == row.target_nominal_arrival_ms + 1.0
        assert row.control_delayed_arrival_ms == row.control_nominal_arrival_ms + 1.0


def test_r2_queue_binds_opportunity_plan_without_response() -> None:
    closure, queue = bind_preformal_r2_contract_closure()
    assert closure.queue_conditions
    assert queue.opportunity_plan_sha256 == closure.opportunity_plan_sha256
    assert queue.checkpoint_sha256 == closure.checkpoint_sha256
    assert {row.opportunity_plan_sha256 for row in closure.queue_conditions} == {
        closure.opportunity_plan_sha256
    }
    expected_arms = {
        "target_sham",
        "target_transmission_null",
        "target_delay_plus_1ms",
        "matched_non_target_transmission_null",
        "matched_non_target_delay_plus_1ms",
    }
    assert {row.arm for row in closure.queue_conditions} == expected_arms
    for row in closure.queue_conditions:
        assert row.cue_source_id == row.intervention_edge.source_id
        assert row.observed_destination_unit_id == row.intervention_edge.target_id


def test_r2_claim_observable_alignment_is_prospective() -> None:
    closure, _ = bind_preformal_r2_contract_closure()
    assert closure.primary_reduction == PRIMARY_REDUCTION
    assert closure.secondary_export == SECONDARY_EXPORT
    assert closure.response_fields == RESPONSE_FIELDS
    assert "edge_destination_membrane_potential_at_nominal_arrival" in RESPONSE_FIELDS
    assert "assembly_level_frozen_response_secondary" in RESPONSE_FIELDS
    assert "development-only physical route influence" in closure.claim_scope


def test_r2_closure_is_deterministic() -> None:
    left_closure, left_queue = bind_preformal_r2_contract_closure()
    right_closure, right_queue = bind_preformal_r2_contract_closure()
    assert left_closure == right_closure
    assert left_queue == right_queue
    assert len(left_closure.sha256) == 64
    assert len(left_queue.sha256) == 64

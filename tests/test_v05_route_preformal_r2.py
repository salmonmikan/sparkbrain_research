from __future__ import annotations

from sparkbrain.v05.route_preformal_r2 import (
    ANALYST_AUTHORITY,
    PRIMARY_REDUCTION,
    SECONDARY_EXPORT,
    bind_preformal_r2_contract_closure,
)


def test_r2_closure_is_non_result_and_preserves_r1() -> None:
    closure, queue = bind_preformal_r2_contract_closure()
    assert ANALYST_AUTHORITY == "EVA-20260923T110053+0900-R92-A7B61F3C"
    assert closure.prior_development_result == "D34-Q001"
    assert closure.prior_result_preserved_unchanged is True
    assert closure.response_bearing_execution_allowed is False
    assert closure.formal_action_allowed is False
    assert queue.status == "QUEUED_NOT_EXECUTED"
    assert queue.response_bearing_execution_performed is False
    assert queue.formal_action_performed is False


def test_r2_queue_pins_one_untouched_anchor_for_every_condition() -> None:
    closure, queue = bind_preformal_r2_contract_closure()
    anchors = {row.anchor_checkpoint_sha256 for row in closure.queue_conditions}
    plans = {row.execution_plan_sha256 for row in closure.queue_conditions}
    assert anchors == {closure.checkpoint_sha256}
    assert plans == {closure.execution_plan_sha256}
    assert queue.checkpoint_sha256 == closure.checkpoint_sha256
    assert queue.execution_plan_sha256 == closure.execution_plan_sha256
    arms = {row.arm for row in closure.queue_conditions}
    assert "target_sham" in arms
    assert "target_transmission_null" in arms
    assert "target_delay_plus_1ms" in arms
    assert "matched_non_target_transmission_null" in arms
    assert "matched_non_target_delay_plus_1ms" in arms


def test_r2_primary_reduction_and_unit_export_map_are_prospective() -> None:
    closure, _ = bind_preformal_r2_contract_closure()
    assert closure.primary_reduction == PRIMARY_REDUCTION
    assert closure.secondary_export == SECONDARY_EXPORT
    assert "assembly_level" in closure.primary_reduction
    assert "secondary" in closure.secondary_export
    assert closure.unit_export_map
    assert len({row.assembly_id for row in closure.unit_export_map}) == len(
        closure.unit_export_map
    )
    for row in closure.unit_export_map:
        assert row.unit_ids
        assert len(set(row.unit_ids)) == len(row.unit_ids)
        assert len(row.prototype_sha256) == 64


def test_r2_closure_is_deterministic() -> None:
    left_closure, left_queue = bind_preformal_r2_contract_closure()
    right_closure, right_queue = bind_preformal_r2_contract_closure()
    assert left_closure == right_closure
    assert left_queue == right_queue
    assert len(left_closure.sha256) == 64
    assert len(left_queue.sha256) == 64

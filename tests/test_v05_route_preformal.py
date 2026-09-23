from __future__ import annotations

from sparkbrain.v05.route_architecture_contract import frozen_contract
from sparkbrain.v05.route_preformal import (
    ANALYST_AUTHORITY,
    ARCHITECTURE_R2_HEAD,
    CANDIDATE_ID,
    CUE_POLICY,
    DEVELOPMENT_SURFACE_ID,
    bind_development_surface,
    bind_preformal_r1,
    build_development_checkpoint,
)


def test_preformal_wrapper_pins_fresh_authority_without_editing_r2() -> None:
    contract = frozen_contract()
    assert ARCHITECTURE_R2_HEAD == "a6455a3929b86ad25fd106ea93a03604192fc3be"
    assert ANALYST_AUTHORITY == "EVA-20260923T101328+0900-R91-C199605F"
    assert CANDIDATE_ID == "CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY"
    assert contract.response_bearing_execution_allowed is False
    assert contract.preformal_execution_allowed is False
    assert contract.formal_action_allowed is False


def test_development_checkpoint_and_surface_are_exactly_reproducible() -> None:
    left = build_development_checkpoint()
    right = build_development_checkpoint()
    assert left.state_hash() == right.state_hash()
    assert left.results == right.results == []

    left_surface = bind_development_surface(left)
    right_surface = bind_development_surface(right)
    assert left_surface == right_surface
    assert left_surface.development_surface_id == DEVELOPMENT_SURFACE_ID
    assert left_surface.cue_policy == CUE_POLICY
    assert left_surface.target_prototype.assembly_id == "assembly-0001"
    assert left_surface.collateral_prototype.assembly_id == "assembly-0002"
    assert left_surface.response_bearing_execution_allowed is True
    assert left_surface.formal_action_allowed is False
    assert len(left_surface.sha256) == 64


def test_cues_are_checkpoint_only_threshold_replays() -> None:
    brain = build_development_checkpoint()
    surface = bind_development_surface(brain)
    for cue in (surface.target_cue, surface.collateral_cue):
        assert cue.arrivals
        for arrival in cue.arrivals:
            unit = brain.base.field.units[arrival.unit_id]
            assert arrival.current == unit.base_threshold
            assert arrival.relative_time_ms >= 0.0
            assert arrival.pulse_id.startswith(f"{DEVELOPMENT_SURFACE_ID}:{cue.role}:")


def test_preformal_prebind_constructs_complete_plan_without_candidate_response() -> None:
    brain, contract, surface, plan, binding = bind_preformal_r1()
    assert binding.architecture_contract_sha256 == contract.sha256
    assert binding.development_surface_sha256 == surface.sha256
    assert binding.checkpoint_sha256 == brain.state_hash()
    assert binding.execution_plan_sha256 == plan.sha256
    assert plan.evaluation_surface_sha256 == surface.sha256
    assert binding.response_bearing_execution_performed is False
    assert binding.evidentiary_status == "PREFORMAL_DEVELOPMENT_PREBIND_NO_RESULT"
    assert brain.results == []
    assert brain.trace == []
    assert len(binding.sha256) == 64

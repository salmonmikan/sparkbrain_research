from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_primary import run_condition
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELD_OUT_FAMILY_IDS,
    heldout_world_parameters,
)


@pytest.mark.parametrize("family_id", HELD_OUT_FAMILY_IDS)
def test_primary_adapter_emits_complete_valid_payload_for_each_family(
    family_id: str,
) -> None:
    parameters = heldout_world_parameters(family_id, 100)
    execution = run_condition(parameters)
    execution.validate()
    assert execution.condition is ConfirmatoryCondition.PRIMARY
    assert execution.family_id == family_id
    assert execution.seed == 100
    assert execution.world_specification_hash == parameters.specification_hash()
    assert len(execution.records) == len(EvidenceDomain)
    assert {row.evidence_domain for row in execution.records} == set(EvidenceDomain)
    assert execution.resource.normal_field_threshold_present is True
    assert execution.resource.threshold_bypassed is False
    assert execution.resource.privileged_information == ()


def test_primary_adapter_semantic_replay_is_deterministic() -> None:
    parameters = heldout_world_parameters("branch-competition", 103)
    first = run_condition(parameters)
    second = run_condition(parameters)
    assert first.semantic_hash == second.semantic_hash
    assert first.records == second.records
    assert first.world_specification_hash == second.world_specification_hash
    assert first.resource.wall_clock_ms >= 0.0
    assert second.resource.wall_clock_ms >= 0.0


def test_primary_adapter_consumes_branch_and_cycle_contracts() -> None:
    parameters = heldout_world_parameters("contingency-cycles", 107)
    execution = run_condition(parameters)
    metrics = dict(execution.records[0].metrics)
    assert metrics["branch_count"] == float(parameters.branch_count)
    assert metrics["contingency_change_count"] == float(
        parameters.contingency_change_count
    )
    assert metrics["heldout_relation_boundary_count"] > 0.0
    assert metrics["world_specification_hash_prefix"] > 0.0

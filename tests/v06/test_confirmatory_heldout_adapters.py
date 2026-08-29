from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_matrix import (
    preflight_report,
    run_execution,
    run_matrix,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELD_OUT_FAMILY_IDS,
    heldout_world_parameters,
)
from sparkbrain.evaluation.v06_confirmatory_resources import PrivilegedInformation


@pytest.mark.parametrize("family_id", HELD_OUT_FAMILY_IDS)
def test_primary_adapter_emits_complete_payload_for_every_heldout_family(
    family_id: str,
) -> None:
    parameters = heldout_world_parameters(family_id, 100)
    execution = run_execution(parameters, ConfirmatoryCondition.PRIMARY)
    execution.validate()
    assert execution.family_id == family_id
    assert execution.seed == 100
    assert execution.condition is ConfirmatoryCondition.PRIMARY
    assert execution.world_specification_hash == parameters.specification_hash()
    assert len(execution.records) == len(EvidenceDomain)
    assert {row.evidence_domain for row in execution.records} == set(EvidenceDomain)
    assert execution.resource.normal_field_threshold_present is True
    assert execution.resource.threshold_bypassed is False
    assert execution.resource.privileged_information == ()


def test_all_eight_conditions_share_one_world_specification() -> None:
    parameters = heldout_world_parameters("sparse-identity-topology", 100)
    executions = run_matrix((parameters,))
    assert len(executions) == len(ConfirmatoryCondition)
    assert {row.condition for row in executions} == set(ConfirmatoryCondition)
    assert {
        row.world_specification_hash for row in executions
    } == {parameters.specification_hash()}
    assert all(len(row.records) == len(EvidenceDomain) for row in executions)


def test_comparator_privileges_are_reported_not_hidden() -> None:
    parameters = heldout_world_parameters("lag-dispersion", 101)
    g3 = run_execution(parameters, ConfirmatoryCondition.G3_RECURRENT)
    g4 = run_execution(parameters, ConfirmatoryCondition.G4_ASSEMBLY)
    g5 = run_execution(parameters, ConfirmatoryCondition.G5_TYPED)

    assert g3.resource.privileged_information == ()
    assert g3.resource.threshold_bypassed is True
    assert g3.resource.normal_field_threshold_present is False

    assert g4.resource.privileged_information == (
        PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
    )
    assert g4.resource.explicit_assembly_entries > 0
    assert g4.resource.threshold_bypassed is True

    assert set(g5.resource.privileged_information) == {
        PrivilegedInformation.TYPED_PREDICTION_HEAD,
        PrivilegedInformation.TYPED_BOUNDARY_HEAD,
        PrivilegedInformation.TYPED_MEMORY_HEAD,
        PrivilegedInformation.SCALAR_REWARD,
    }
    assert g5.resource.typed_head_count >= 3
    assert g5.resource.scalar_reward_observations >= 1
    assert g5.resource.threshold_bypassed is True


def test_control_contract_metrics_are_explicit() -> None:
    parameters = heldout_world_parameters("threshold-magnitude-band", 102)
    for condition in (
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    ):
        execution = run_execution(parameters, condition)
        metrics = dict(execution.records[0].metrics)
        assert metrics["control_contract_passed"] in {0.0, 1.0}
        assert metrics["self_confirmation_violations"] == 0.0
        assert execution.resource.privileged_information == ()


def test_semantic_replay_ignores_wall_clock_but_not_runtime_results() -> None:
    parameters = heldout_world_parameters("branch-competition", 103)
    first = run_execution(parameters, ConfirmatoryCondition.PRIMARY)
    second = run_execution(parameters, ConfirmatoryCondition.PRIMARY)
    assert first.semantic_hash == second.semantic_hash
    assert first.records == second.records
    assert first.resource.wall_clock_ms >= 0.0
    assert second.resource.wall_clock_ms >= 0.0


def test_preflight_counts_shape_without_scoring_capability() -> None:
    parameters = heldout_world_parameters("contingency-cycles", 104)
    executions = run_matrix((parameters,))
    replay = tuple(
        run_execution(parameters, condition)
        for condition in (
            ConfirmatoryCondition.PRIMARY,
            ConfirmatoryCondition.G3_RECURRENT,
        )
    )
    report = preflight_report(
        (parameters,),
        executions,
        replay_executions=replay,
    )
    assert report.complete is True
    assert report.expected_execution_count == len(ConfirmatoryCondition)
    assert report.observed_execution_count == len(ConfirmatoryCondition)
    assert report.expected_result_count == (
        len(ConfirmatoryCondition) * len(EvidenceDomain)
    )
    assert report.observed_result_count == report.expected_result_count
    assert report.missing_execution_keys == ()
    assert report.duplicate_execution_keys == ()
    assert report.invalid_executions == ()
    assert report.semantic_replay_mismatches == ()

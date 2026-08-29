from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    build_draft_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
    assess_resource_matrix,
)


def _record(
    condition: ConfirmatoryCondition,
    *,
    family_id: str = "identifier-permutation",
    seed: int = 0,
) -> ConditionResourceRecord:
    common = {
        "family_id": family_id,
        "seed": seed,
        "condition": condition,
        "observed_training_events": 12,
        "generated_internal_events": 3,
        "persistent_state_entries": 9,
        "intervention_count": 2,
        "parameter_count": 9,
        "wall_clock_ms": 1.25,
        "normal_field_threshold_present": True,
        "normal_field_threshold_crossings": 3,
        "threshold_bypassed": False,
        "explicit_assembly_entries": 0,
        "typed_head_count": 0,
        "scalar_reward_observations": 0,
        "privileged_information": (),
    }
    if condition is ConfirmatoryCondition.G3_RECURRENT:
        common.update(
            {
                "normal_field_threshold_present": False,
                "normal_field_threshold_crossings": 0,
                "threshold_bypassed": True,
            }
        )
    elif condition is ConfirmatoryCondition.G4_ASSEMBLY:
        common.update(
            {
                "normal_field_threshold_present": False,
                "normal_field_threshold_crossings": 0,
                "threshold_bypassed": True,
                "explicit_assembly_entries": 6,
                "privileged_information": (
                    PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
                ),
            }
        )
    elif condition is ConfirmatoryCondition.G5_TYPED:
        common.update(
            {
                "normal_field_threshold_present": False,
                "normal_field_threshold_crossings": 0,
                "threshold_bypassed": True,
                "typed_head_count": 3,
                "scalar_reward_observations": 9,
                "privileged_information": (
                    PrivilegedInformation.TYPED_PREDICTION_HEAD,
                    PrivilegedInformation.TYPED_BOUNDARY_HEAD,
                    PrivilegedInformation.TYPED_MEMORY_HEAD,
                    PrivilegedInformation.SCALAR_REWARD,
                ),
            }
        )
    return ConditionResourceRecord(**common)


@pytest.mark.parametrize("condition", tuple(ConfirmatoryCondition))
def test_each_condition_has_an_explicit_valid_resource_contract(
    condition: ConfirmatoryCondition,
) -> None:
    record = _record(condition)
    record.validate()
    metrics = record.metric_dict()
    assert metrics["resource_observed_training_events"] == 12.0
    assert metrics["resource_generated_internal_events"] == 3.0
    assert metrics["resource_wall_clock_ms"] == 1.25


def test_primary_and_controls_reject_hidden_assembly_typed_heads_or_reward() -> None:
    primary = _record(ConfirmatoryCondition.PRIMARY)
    with pytest.raises(ValueError, match="Assembly"):
        replace(primary, explicit_assembly_entries=1).validate()
    with pytest.raises(ValueError, match="typed heads or reward"):
        replace(primary, typed_head_count=1).validate()
    with pytest.raises(ValueError, match="typed heads or reward"):
        replace(primary, scalar_reward_observations=1).validate()
    with pytest.raises(ValueError, match="privileged information"):
        replace(
            primary,
            privileged_information=(PrivilegedInformation.SCALAR_REWARD,),
        ).validate()


def test_g3_must_report_that_it_bypasses_the_primary_field_threshold() -> None:
    record = _record(ConfirmatoryCondition.G3_RECURRENT)
    with pytest.raises(ValueError, match="explicitly report Field-threshold bypass"):
        replace(record, threshold_bypassed=False).validate()
    with pytest.raises(ValueError, match="not a Field runtime"):
        replace(
            record,
            normal_field_threshold_present=True,
            threshold_bypassed=False,
        ).validate()


def test_g4_must_disclose_explicit_assembly_state_and_only_that_privilege() -> None:
    record = _record(ConfirmatoryCondition.G4_ASSEMBLY)
    with pytest.raises(ValueError, match="report explicit Assembly state"):
        replace(record, explicit_assembly_entries=0).validate()
    with pytest.raises(ValueError, match="privilege inventory"):
        replace(record, privileged_information=()).validate()


def test_g5_must_disclose_typed_heads_and_scalar_reward() -> None:
    record = _record(ConfirmatoryCondition.G5_TYPED)
    with pytest.raises(ValueError, match="typed functional heads"):
        replace(record, typed_head_count=2).validate()
    with pytest.raises(ValueError, match="scalar reward"):
        replace(record, scalar_reward_observations=0).validate()
    with pytest.raises(ValueError, match="privilege inventory"):
        replace(
            record,
            privileged_information=(PrivilegedInformation.SCALAR_REWARD,),
        ).validate()


def test_complete_qualification_resource_matrix_requires_one_record_per_cell() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    records = tuple(
        _record(
            condition.condition,
            family_id=family.family_id,
            seed=seed.seed,
        )
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
    )
    coverage = assess_resource_matrix(manifest, records)
    assert coverage.expected_record_count == 72
    assert coverage.observed_record_count == 72
    assert coverage.complete is True


def test_missing_duplicate_and_invalid_resource_records_fail_closed() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    records = tuple(
        _record(
            condition.condition,
            family_id=family.family_id,
            seed=seed.seed,
        )
        for family in manifest.world_families
        for seed in manifest.seeds
        for condition in manifest.conditions
    )
    missing = assess_resource_matrix(manifest, records[:-1])
    assert missing.complete is False
    assert missing.missing_keys

    duplicate = assess_resource_matrix(manifest, (*records, records[0]))
    assert duplicate.complete is False
    assert duplicate.duplicate_keys

    invalid_row = replace(records[0], wall_clock_ms=-1.0)
    invalid = assess_resource_matrix(manifest, (invalid_row, *records[1:]))
    assert invalid.complete is False
    assert invalid.invalid_records

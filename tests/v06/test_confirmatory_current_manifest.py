from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    assess_confirmatory_readiness,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)

_QUALIFICATION_READY_CONDITIONS = set(ConfirmatoryCondition)

_EXPECTED_PATHS = {
    ConfirmatoryCondition.PRIMARY: (
        "sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition"
    ),
    ConfirmatoryCondition.NO_ENDOGENOUS: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_no_endogenous"
    ),
    ConfirmatoryCondition.RANDOM_MATCHED: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_random_matched"
    ),
    ConfirmatoryCondition.READOUT_ONLY: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_readout_only"
    ),
    ConfirmatoryCondition.SHUFFLED_RELATION: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_shuffled_relation"
    ),
    ConfirmatoryCondition.G3_RECURRENT: (
        "sparkbrain.baselines.v06.g3_recurrent.run_condition"
    ),
    ConfirmatoryCondition.G4_ASSEMBLY: (
        "sparkbrain.baselines.v06.g4_assembly.run_condition"
    ),
    ConfirmatoryCondition.G5_TYPED: (
        "sparkbrain.baselines.v06.g5_typed.run_condition"
    ),
}


def test_qualification_marks_all_eight_adapters_ready() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    registrations = {row.condition: row for row in manifest.conditions}
    assert {
        condition
        for condition, row in registrations.items()
        if row.adapter_ready
    } == _QUALIFICATION_READY_CONDITIONS
    for condition in _QUALIFICATION_READY_CONDITIONS:
        row = registrations[condition]
        assert row.isolated_from_primary is True
        assert row.engineering_evidence_available is True
        assert row.adapter_path == _EXPECTED_PATHS[condition]


def test_qualification_manifest_is_adapter_complete_but_unfrozen() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert readiness.ready is False
    assert readiness.code_ref_frozen is False
    assert readiness.isolation_violations == ()
    assert readiness.unavailable_adapters == ()
    assert readiness.shape_errors == ()


def test_confirmatory_manifest_does_not_reuse_qualification_readiness() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert readiness.family_count == readiness.required_family_count == 5
    assert readiness.seed_count == readiness.required_seed_count == 10
    assert all(row.held_out for row in manifest.world_families)
    assert readiness.ready is False
    assert set(readiness.unavailable_adapters) == {
        row.value for row in ConfirmatoryCondition
    }
    registrations = {row.condition: row for row in manifest.conditions}
    for condition in _QUALIFICATION_READY_CONDITIONS:
        row = registrations[condition]
        assert row.adapter_ready is False
        assert row.engineering_evidence_available is True
        assert row.adapter_path == _EXPECTED_PATHS[condition]
        assert "held-out" in row.notes

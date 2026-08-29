from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    assess_confirmatory_readiness,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)

_READY_CONDITIONS = {
    ConfirmatoryCondition.PRIMARY,
    ConfirmatoryCondition.NO_ENDOGENOUS,
    ConfirmatoryCondition.RANDOM_MATCHED,
    ConfirmatoryCondition.READOUT_ONLY,
    ConfirmatoryCondition.SHUFFLED_RELATION,
}

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
}


def test_current_manifest_marks_primary_and_four_controls_ready() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    registrations = {row.condition: row for row in manifest.conditions}
    assert {
        condition
        for condition, row in registrations.items()
        if row.adapter_ready
    } == _READY_CONDITIONS
    for condition in _READY_CONDITIONS:
        row = registrations[condition]
        assert row.isolated_from_primary is True
        assert row.engineering_evidence_available is True
        assert row.adapter_path == _EXPECTED_PATHS[condition]


def test_current_manifest_remains_fail_closed_and_unfrozen() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert readiness.ready is False
    assert readiness.code_ref_frozen is False
    assert set(readiness.unavailable_adapters) == {
        "g3-recurrent",
        "g4-assembly-conditioned",
        "g5-typed-functional-heads",
    }


def test_confirmatory_manifest_uses_held_out_shape_but_is_not_ready() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert readiness.family_count == readiness.required_family_count == 5
    assert readiness.seed_count == readiness.required_seed_count == 10
    assert all(row.held_out for row in manifest.world_families)
    assert readiness.ready is False
    assert set(readiness.unavailable_adapters) == {
        "g3-recurrent",
        "g4-assembly-conditioned",
        "g5-typed-functional-heads",
    }

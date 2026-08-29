from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    assess_confirmatory_readiness,
)
from sparkbrain.evaluation.v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)


def test_current_manifest_marks_only_primary_adapter_ready() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    registrations = {row.condition: row for row in manifest.conditions}
    primary = registrations[ConfirmatoryCondition.PRIMARY]
    assert primary.adapter_ready is True
    assert primary.isolated_from_primary is True
    assert primary.adapter_path == (
        "sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition"
    )
    assert all(
        not row.adapter_ready
        for condition, row in registrations.items()
        if condition is not ConfirmatoryCondition.PRIMARY
    )


def test_current_manifest_remains_fail_closed_and_unfrozen() -> None:
    manifest = build_current_confirmatory_manifest(
        ConfirmatoryPhase.QUALIFICATION
    )
    readiness = assess_confirmatory_readiness(manifest)
    assert readiness.ready is False
    assert readiness.code_ref_frozen is False
    assert "primary" not in readiness.unavailable_adapters
    assert set(readiness.unavailable_adapters) == {
        "no-endogenous",
        "random-endogenous-matched",
        "readout-only",
        "shuffled-relation",
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

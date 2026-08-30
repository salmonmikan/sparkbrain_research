from __future__ import annotations

from test_capability_staging_development_fixture import DevelopmentCapabilityWorld
from test_capability_staging_development_variants import development_variants

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_controls import (
    run_condition as run_control,
)


def test_shuffled_relation_breaks_every_observable_correct_mapping() -> None:
    worlds = (DevelopmentCapabilityWorld(), *development_variants())
    for world in worlds:
        execution = run_control(
            world,  # type: ignore[arg-type]
            ConfirmatoryCondition.SHUFFLED_RELATION,
        )
        execution.validate()
        metrics = dict(execution.records[0].metrics)
        assert metrics["control_contract_passed"] == 1.0, world.family_id
        assert metrics["heldout_shuffled_original_nonempty_count"] > 0.0
        assert metrics["heldout_shuffled_changed_fraction"] == 1.0
        assert metrics["heldout_shuffled_correct_reentry_fraction"] == 0.0
        passed = {
            row.evidence_domain: row.passed for row in execution.records
        }
        assert passed[EvidenceDomain.RELATION_REENTRY] is False
        assert passed[EvidenceDomain.PERSISTENCE_LOCUS] is False


def test_shuffled_control_remains_development_only() -> None:
    worlds = (DevelopmentCapabilityWorld(), *development_variants())
    for world in worlds:
        assert world.structural_token.startswith("development-only:")
        assert not 100 <= world.seed <= 109
        assert not 1000 <= world.seed <= 1009

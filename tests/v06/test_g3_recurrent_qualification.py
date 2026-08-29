from __future__ import annotations

from pathlib import Path

from sparkbrain.baselines.v06.g3_recurrent import (
    GenericRecurrentPredictor,
    evaluate_world,
    run_condition,
    run_qualification_grid,
)
from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)


def test_generated_tokens_never_train_the_recurrent_comparator() -> None:
    model = GenericRecurrentPredictor()
    model.observe_sequence(("unit:0", "unit:1", "unit:2"), repetitions=3)
    before_observations = model.observation_count
    before_learned_state = model.learned_state_dict()
    assert model.rollout("unit:0", steps=2) == ("unit:1", "unit:2")
    assert model.observation_count == before_observations
    assert model.learned_state_dict() == before_learned_state
    assert model.generated_token_count == 2


def test_g3_qualification_grid_covers_three_families_three_seeds_nine_domains() -> None:
    grid = run_qualification_grid()
    assert grid.complete is True
    assert grid.passed_world_count == 9
    assert len(grid.worlds) == 9
    assert len(grid.records) == 81
    assert {row.condition for row in grid.records} == {
        ConfirmatoryCondition.G3_RECURRENT
    }
    assert {row.evidence_domain for row in grid.records} == set(EvidenceDomain)
    assert all(row.passed for row in grid.records)


def test_g3_world_exposes_selective_effect_and_zero_self_confirmation() -> None:
    evidence = evaluate_world("temporal-perturbation", 2)
    metrics = dict(evidence.metrics)
    assert evidence.all_passed is True
    assert metrics["g3_chain_targeted_impairment"] == 1.0
    assert metrics["g3_chain_matched_impairment"] == 0.0
    assert metrics["g3_chain_selective_effect"] == 1.0
    assert metrics["g3_boundary_targeted_impairment"] == 1.0
    assert metrics["g3_boundary_matched_impairment"] == 0.0
    assert metrics["g3_boundary_selective_effect"] == 1.0
    assert metrics["taxonomy_hash_match"] == 1.0
    assert metrics["self_confirmation_violations"] == 0.0


def test_g3_relation_reverses_reacquires_and_transplants_explicit_state() -> None:
    evidence = evaluate_world("field-gain-perturbation", 1)
    metrics = dict(evidence.metrics)
    assert evidence.domain_passed(EvidenceDomain.RELATION_STABILIZATION)
    assert evidence.domain_passed(EvidenceDomain.REVERSAL_REACQUISITION)
    assert evidence.domain_passed(EvidenceDomain.RELATION_REENTRY)
    assert evidence.domain_passed(EvidenceDomain.PERSISTENCE_LOCUS)
    assert metrics["g3_reversal_crossing_episode"] >= 1.0
    assert metrics["g3_reacquisition_crossing_episode"] >= 1.0
    assert metrics["g3_reversed_new_confidence"] > 0.5
    assert metrics["g3_returned_old_confidence"] > 0.5


def test_g3_public_adapter_emits_all_nine_records_deterministically() -> None:
    first = run_condition("identifier-permutation", 0)
    second = run_condition("identifier-permutation", 0)
    assert first == second
    assert len(first) == 9
    assert all(row.passed for row in first)


def test_g3_comparator_package_does_not_import_primary_runtime() -> None:
    root = Path(__file__).parents[2] / "src" / "sparkbrain" / "baselines" / "v06"
    for path in sorted(root.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        assert "from sparkbrain.v06" not in source
        assert "import sparkbrain.v06" not in source

from __future__ import annotations

from pathlib import Path

from sparkbrain.baselines.v06.g4_assembly import (
    ExplicitAssemblyComparator,
    evaluate_world,
    run_condition,
    run_qualification_grid,
)
from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)


def test_g4_explicitly_stores_and_activates_assembly_identity() -> None:
    model = ExplicitAssemblyComparator()
    assembly_id = model.observe_sequence(
        ("unit:0", "unit:1", "unit:2"),
        repetitions=3,
    )
    assert assembly_id.startswith("assembly:")
    assert model.activate("unit:0") == assembly_id
    assert model.rollout("unit:0", steps=2) == ("unit:1", "unit:2")
    state = model.state_dict()
    assert assembly_id in state["assemblies"]
    assert state["assemblies"][assembly_id]["members"] == (
        "unit:0",
        "unit:1",
        "unit:2",
    )


def test_generated_assembly_rollout_does_not_train_the_model() -> None:
    model = ExplicitAssemblyComparator()
    model.observe_sequence(("unit:0", "unit:1", "unit:2"), repetitions=3)
    before_observations = model.observation_count
    before_state = model.learned_state_dict()
    model.rollout("unit:0", steps=2)
    assert model.observation_count == before_observations
    assert model.learned_state_dict() == before_state


def test_g4_qualification_grid_covers_all_worlds_and_domains() -> None:
    grid = run_qualification_grid()
    assert grid.complete is True
    assert grid.passed_world_count == 9
    assert len(grid.worlds) == 9
    assert len(grid.records) == 81
    assert {row.condition for row in grid.records} == {
        ConfirmatoryCondition.G4_ASSEMBLY
    }
    assert {row.evidence_domain for row in grid.records} == set(EvidenceDomain)
    assert all(row.passed for row in grid.records)


def test_g4_world_has_explicit_assembly_causal_and_relation_evidence() -> None:
    evidence = evaluate_world("identifier-permutation", 1)
    metrics = dict(evidence.metrics)
    assert evidence.all_passed is True
    assert metrics["g4_assembly_count"] == 1.0
    assert metrics["g4_chain_targeted_impairment"] == 1.0
    assert metrics["g4_chain_matched_impairment"] == 0.0
    assert metrics["g4_boundary_targeted_impairment"] == 1.0
    assert metrics["g4_boundary_matched_impairment"] == 0.0
    assert metrics["g4_reversed_new_confidence"] > 0.5
    assert metrics["g4_returned_old_confidence"] > 0.5
    assert metrics["self_confirmation_violations"] == 0.0
    assert metrics["taxonomy_hash_match"] == 1.0


def test_g4_public_adapter_is_deterministic_and_complete() -> None:
    first = run_condition("temporal-perturbation", 2)
    second = run_condition("temporal-perturbation", 2)
    assert first == second
    assert len(first) == 9
    assert all(row.passed for row in first)


def test_g4_is_isolated_from_primary_runtime_imports() -> None:
    path = (
        Path(__file__).parents[2]
        / "src"
        / "sparkbrain"
        / "baselines"
        / "v06"
        / "g4_assembly.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "from sparkbrain.v06" not in source
    assert "import sparkbrain.v06" not in source

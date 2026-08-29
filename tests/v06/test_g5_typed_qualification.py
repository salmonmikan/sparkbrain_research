from __future__ import annotations

from pathlib import Path

from sparkbrain.baselines.v06.g5_typed import (
    TypedFunctionalHeadComparator,
    evaluate_world,
    run_condition,
    run_qualification_grid,
)
from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)


def test_g5_explicitly_uses_prediction_action_reward_and_memory_heads() -> None:
    model = TypedFunctionalHeadComparator()
    model.train_prediction_sequence(("unit:0", "unit:1"), repetitions=2)
    model.train_action("unit:1", "port:7", repetitions=2)
    model.observe_reward("port:7", "unit:8", reward=1.0)
    assert model.predict_rollout("unit:0", steps=1) == ("unit:1",)
    assert model.choose_action("unit:1") == "port:7"
    assert model.choose_rewarded_target("port:7") == "unit:8"
    state = model.learned_state_dict()
    assert state["prediction_head"]
    assert state["action_head"]
    assert state["reward_head"]
    assert state["memory_head"]


def test_g5_generation_does_not_update_any_typed_learned_head() -> None:
    model = TypedFunctionalHeadComparator()
    model.train_prediction_sequence(("unit:0", "unit:1"), repetitions=3)
    model.train_action("unit:1", "port:7", repetitions=3)
    model.observe_reward("port:7", "unit:8", reward=1.0)
    before = model.learned_state_dict()
    observations = model.observation_count
    model.predict_rollout("unit:0", steps=1)
    model.choose_action("unit:1")
    model.choose_rewarded_target("port:7")
    assert model.learned_state_dict() == before
    assert model.observation_count == observations


def test_g5_qualification_grid_covers_all_worlds_and_domains() -> None:
    grid = run_qualification_grid()
    assert grid.complete is True
    assert grid.passed_world_count == 9
    assert len(grid.worlds) == 9
    assert len(grid.records) == 81
    assert {row.condition for row in grid.records} == {
        ConfirmatoryCondition.G5_TYPED
    }
    assert {row.evidence_domain for row in grid.records} == set(EvidenceDomain)
    assert all(row.passed for row in grid.records)


def test_g5_world_reports_typed_head_success_and_privileged_reward_use() -> None:
    evidence = evaluate_world("field-gain-perturbation", 2)
    metrics = dict(evidence.metrics)
    assert evidence.all_passed is True
    assert metrics["g5_prediction_head_entry_count"] == 3.0
    assert metrics["g5_chain_targeted_impairment"] == 1.0
    assert metrics["g5_chain_matched_impairment"] == 0.0
    assert metrics["g5_boundary_targeted_impairment"] == 1.0
    assert metrics["g5_boundary_matched_impairment"] == 0.0
    assert metrics["g5_reward_observation_count"] == 9.0
    assert metrics["g5_reversed_new_confidence"] > 0.5
    assert metrics["g5_returned_old_confidence"] > 0.5
    assert metrics["self_confirmation_violations"] == 0.0
    assert metrics["taxonomy_hash_match"] == 1.0


def test_g5_public_adapter_is_deterministic_and_complete() -> None:
    first = run_condition("identifier-permutation", 0)
    second = run_condition("identifier-permutation", 0)
    assert first == second
    assert len(first) == 9
    assert all(row.passed for row in first)


def test_g5_is_isolated_from_primary_runtime_imports() -> None:
    path = (
        Path(__file__).parents[2]
        / "src"
        / "sparkbrain"
        / "baselines"
        / "v06"
        / "g5_typed.py"
    )
    source = path.read_text(encoding="utf-8")
    assert "from sparkbrain.v06" not in source
    assert "import sparkbrain.v06" not in source

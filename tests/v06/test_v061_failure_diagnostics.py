from __future__ import annotations

from sparkbrain.evaluation.v061_diagnostic_worlds import (
    lag_factor_worlds,
    relation_factor_worlds,
)
from sparkbrain.evaluation.v061_lag_diagnostics import (
    diagnose_lag_world,
    run_lag_diagnostic_suite,
)
from sparkbrain.evaluation.v061_relation_diagnostics import (
    run_relation_diagnostic_suite,
)


def _lag_by_family():
    return {world.family_id: diagnose_lag_world(world) for world in lag_factor_worlds()}


def test_all_diagnostic_worlds_are_development_only_and_disjoint() -> None:
    worlds = (*lag_factor_worlds(), *relation_factor_worlds())
    assert len({world.specification_hash() for world in worlds}) == len(worlds)
    for world in worlds:
        world.validate()
        assert world.structural_token.startswith("development-only:diagnostic:")
        assert world.seed >= 900_000
        assert not 1000 <= world.seed <= 1009
        assert not 2000 <= world.seed <= 2009


def test_profile_assignment_swap_reverses_the_root_confidence_order() -> None:
    rows = _lag_by_family()
    resonant = rows["diagnostic-lag-resonant-shared"]
    swapped = rows["diagnostic-lag-assignment-swapped"]
    assert resonant.predicted_root_winner == "alternate"
    assert swapped.predicted_root_winner == "main"
    assert resonant.root_candidates[0].confidence > resonant.root_candidates[1].confidence
    assert swapped.root_candidates[0].confidence > swapped.root_candidates[1].confidence


def test_removing_shared_root_removes_alternate_competition_on_main_cue() -> None:
    rows = _lag_by_family()
    shared = rows["diagnostic-lag-resonant-shared"]
    separated = rows["diagnostic-lag-resonant-separated"]
    assert shared.shared_root is True
    assert separated.shared_root is False
    assert shared.sham.alternate_trajectory_present is True
    assert separated.sham.alternate_trajectory_present is False
    assert separated.sham.main_trajectory_present is True


def test_main_variance_sweep_reduces_main_root_current_monotonically() -> None:
    rows = _lag_by_family()
    sweep = [
        rows[f"diagnostic-lag-main-variance-{index}"] for index in range(7)
    ]
    ratios = []
    for row in sweep:
        main = next(candidate for candidate in row.root_candidates if candidate.branch == "main")
        ratios.append(main.current_threshold_ratio)
    assert all(left >= right for left, right in zip(ratios, ratios[1:], strict=False))
    assert ratios[0] > 1.0
    assert ratios[-1] < 1.0


def test_causal_selectivity_is_not_interpreted_when_sham_main_is_absent() -> None:
    suite = run_lag_diagnostic_suite()
    absent = [
        row
        for row in suite["worlds"]
        if row["causal_baseline"]["baseline_status"] == "absent"
    ]
    assert absent
    for row in absent:
        causal = row["causal_baseline"]
        assert causal["selectivity_interpretable"] is False
        assert causal["diagnostic_selective_effect"] is None
        assert "absent" in causal["interpretation"]


def test_root_threshold_prediction_matches_shared_root_expression() -> None:
    suite = run_lag_diagnostic_suite()
    assert suite["candidate_003_executions"] == 0
    assert suite["shared_root_world_count"] > 0
    assert suite["root_threshold_prediction_match_count"] == suite[
        "shared_root_world_count"
    ]
    assert suite["root_threshold_prediction_match_fraction"] == 1.0


def test_relation_suite_separates_storage_and_expression_failures() -> None:
    suite = run_relation_diagnostic_suite()
    assert suite["candidate_003_executions"] == 0
    assert suite["world_count"] == 3
    assert suite["phase_count"] == 18
    assert suite["storage_failure_count"] > 0
    assert suite["expression_failure_after_correct_storage_count"] > 0
    assert suite["abstention_count"] > 0
    assert suite["superposition_count"] > 0
    assert suite["exact_singleton_count"] > 0


def test_expression_abstention_world_keeps_correct_relation_storage() -> None:
    suite = run_relation_diagnostic_suite()
    world = next(
        row
        for row in suite["worlds"]
        if row["factor_value"] == "expression-abstention"
    )
    assert world["storage_match_fraction"] == 1.0
    assert world["expression_failure_after_correct_storage_count"] > 0
    assert world["storage_failure_count"] == 0


def test_failure_diagnostics_are_deterministic() -> None:
    assert run_lag_diagnostic_suite() == run_lag_diagnostic_suite()
    assert run_relation_diagnostic_suite() == run_relation_diagnostic_suite()

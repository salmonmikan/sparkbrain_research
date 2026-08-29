from __future__ import annotations

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryPhase,
    build_draft_confirmatory_manifest,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    HELDOUT_FAMILIES,
    HELDOUT_SEEDS,
    build_heldout_world_grid,
    heldout_world_grid_hash,
    heldout_world_parameters,
)


def test_heldout_grid_matches_manifest_shape_without_running_conditions() -> None:
    manifest = build_draft_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY
    )
    grid = build_heldout_world_grid()
    assert tuple(row.family_id for row in manifest.world_families) == HELDOUT_FAMILIES
    assert tuple(row.seed for row in manifest.seeds) == HELDOUT_SEEDS
    assert len(grid) == 50
    assert {(row.family_id, row.seed) for row in grid} == {
        (family_id, seed)
        for family_id in HELDOUT_FAMILIES
        for seed in HELDOUT_SEEDS
    }


def test_heldout_world_generation_is_deterministic_and_hashable() -> None:
    first = build_heldout_world_grid()
    second = build_heldout_world_grid()
    assert first == second
    assert heldout_world_grid_hash() == heldout_world_grid_hash()
    assert len(heldout_world_grid_hash()) == 64
    assert len({row.specification_hash() for row in first}) == 50


def test_sparse_permutation_worlds_use_a_sparse_active_subset() -> None:
    rows = tuple(
        heldout_world_parameters("heldout-sparse-permutation", seed)
        for seed in HELDOUT_SEEDS
    )
    assert all(row.active_fraction < 0.50 for row in rows)
    assert all(len(row.distractor_unit_ids) >= 8 for row in rows)
    assert all(row.main_port != row.control_port for row in rows)
    assert len({row.main_path for row in rows}) == len(rows)


def test_lag_dispersion_worlds_have_nonuniform_edge_and_episode_timing() -> None:
    rows = tuple(
        heldout_world_parameters("heldout-lag-dispersion", seed)
        for seed in HELDOUT_SEEDS
    )
    for row in rows:
        assert len(row.training_lag_profiles_ms) == 6
        assert len(set(row.training_lag_profiles_ms)) > 3
        assert len(set(row.evaluation_lags_ms)) > 1
        assert len(set(row.episode_spacings_ms)) > 6


def test_threshold_band_is_distinct_and_spans_a_wide_ordinary_field_range() -> None:
    rows = tuple(
        heldout_world_parameters("heldout-threshold-band", seed)
        for seed in HELDOUT_SEEDS
    )
    thresholds = tuple(row.threshold for row in rows)
    assert len(set(thresholds)) == 10
    assert min(thresholds) < 0.40
    assert max(thresholds) > 0.65
    assert all(row.cue_magnitude > row.threshold for row in rows)


def test_branch_competition_contains_three_close_exposure_alternatives() -> None:
    rows = tuple(
        heldout_world_parameters("heldout-branch-competition", seed)
        for seed in HELDOUT_SEEDS
    )
    for row in rows:
        assert row.branch_count == 3
        assert all(path[0] == row.main_path[0] for path in row.competition_paths)
        assert row.branch_exposure_counts[0] > row.branch_exposure_counts[1]
        assert row.branch_exposure_counts[1] > row.branch_exposure_counts[2]
        assert max(row.branch_exposure_counts) - min(row.branch_exposure_counts) == 2


def test_contingency_cycle_worlds_require_multiple_reversals_and_reacquisition() -> None:
    rows = tuple(
        heldout_world_parameters("heldout-contingency-cycles", seed)
        for seed in HELDOUT_SEEDS
    )
    for row in rows:
        assert len(row.contingency_cycle_targets) == 6
        assert row.contingency_change_count == 5
        assert set(row.contingency_cycle_targets) == {
            row.old_target,
            row.new_target,
            row.third_target,
        }
        assert all(2 <= value <= 4 for value in row.contingency_phase_lengths)


def test_heldout_spec_contains_no_privileged_functional_taxonomy() -> None:
    lowered = str([row.state_dict() for row in build_heldout_world_grid()]).lower()
    for forbidden in (
        "assembly_id",
        "correct_action",
        "reward_value",
        "utility_target",
        "outcome_label",
        "functional_role",
        "meaning_state",
        "relation_type",
    ):
        assert forbidden not in lowered

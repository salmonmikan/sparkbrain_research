from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    EvidenceDomain,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_dryrun_contract import (
    DryRunStatus,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_preflight import (
    build_heldout_preflight_matrix,
    run_heldout_preflight,
)
from sparkbrain.evaluation.v06_confirmatory_resources import (
    PrivilegedInformation,
)


@pytest.fixture(scope="module")
def preflight():
    return run_heldout_preflight()


def test_preflight_covers_all_worlds_adapters_and_schema_rows(preflight) -> None:
    matrix, report = preflight
    assert report.world_count == 50
    assert report.adapter_record_count == 400
    assert report.resource_schema_record_count == 400
    assert report.domain_schema_record_count == 3600
    assert report.expected_domain_schema_record_count == 3600
    assert len(matrix.adapter_records) == 400
    assert len(matrix.resource_schema_records) == 400
    assert len(matrix.domain_schema_records) == 3600
    assert report.adapter_coverage_complete is True
    assert report.common_input_contract_complete is True
    assert report.parameter_reflection_complete is True
    assert report.branch_competition_preserved is True
    assert report.resource_schema_complete is True
    assert report.safety_declarations_passed is True


def test_preflight_is_reproducible_and_keeps_confirmatory_blocked(preflight) -> None:
    _, report = preflight
    assert report.replay_matrix_hash_match is True
    assert report.world_grid_hash_match is True
    assert report.schema_only is True
    assert report.capability_execution_count == 0
    assert report.heldout_manifest_ready is False
    assert report.heldout_ready_adapter_count == 0
    assert report.code_ref_frozen is False
    assert report.ready_for_code_review is True
    assert report.confirmatory_execution_allowed is False


def test_all_eight_conditions_consume_exactly_the_same_world_input(preflight) -> None:
    matrix, _ = preflight
    grouped = defaultdict(list)
    for row in matrix.adapter_records:
        grouped[(row.family_id, row.seed)].append(row)
    assert len(grouped) == 50
    for rows in grouped.values():
        assert {row.condition for row in rows} == set(ConfirmatoryCondition)
        assert len({row.world_specification_hash for row in rows}) == 1
        assert len({row.input_projection_hash for row in rows}) == 1
        first = rows[0].input_projection
        assert all(row.input_projection == first for row in rows)


def test_threshold_lag_topology_and_contingency_are_reflected(preflight) -> None:
    matrix, _ = preflight
    for row in matrix.adapter_records:
        world = row.input_projection
        architecture = row.architecture_projection
        assert architecture["unit_count"] == world["unit_count"]
        assert architecture["active_unit_ids"] == list(world["active_unit_ids"])
        assert architecture["distractor_unit_ids"] == list(
            world["distractor_unit_ids"]
        )
        assert architecture["training_lag_profiles_ms"] == [
            list(profile) for profile in world["training_lag_profiles_ms"]
        ]
        assert architecture["evaluation_lags_ms"] == list(
            world["evaluation_lags_ms"]
        )
        assert architecture["episode_spacings_ms"] == list(
            world["episode_spacings_ms"]
        )
        assert architecture["contingency_cycle_targets"] == list(
            world["contingency_cycle_targets"]
        )
        assert architecture["contingency_phase_lengths"] == list(
            world["contingency_phase_lengths"]
        )
        if row.safety.normal_field_threshold_present:
            assert architecture["field_threshold"] == world["threshold"]
            assert architecture["normal_field_threshold"] == "present"
        else:
            assert architecture["provided_world_threshold"] == world["threshold"]
            assert architecture["normal_field_threshold"] == "bypassed"


def test_parameter_changes_produce_distinct_adapter_configurations(preflight) -> None:
    matrix, _ = preflight
    for condition in ConfirmatoryCondition:
        rows = tuple(
            row for row in matrix.adapter_records if row.condition is condition
        )
        assert len(rows) == 50
        assert len({row.configuration_hash for row in rows}) == 50

    threshold_rows = tuple(
        row
        for row in matrix.adapter_records
        if row.condition is ConfirmatoryCondition.PRIMARY
        and row.family_id == "heldout-threshold-band"
    )
    assert len({row.architecture_projection["field_threshold"] for row in threshold_rows}) == 10

    lag_rows = tuple(
        row
        for row in matrix.adapter_records
        if row.condition is ConfirmatoryCondition.G3_RECURRENT
        and row.family_id == "heldout-lag-dispersion"
    )
    assert len(
        {
            tuple(row.architecture_projection["evaluation_lags_ms"])
            for row in lag_rows
        }
    ) == 10


def test_branch_competition_is_not_collapsed_by_any_adapter(preflight) -> None:
    matrix, _ = preflight
    rows = tuple(
        row
        for row in matrix.adapter_records
        if row.family_id == "heldout-branch-competition"
    )
    assert len(rows) == 80
    for row in rows:
        paths = tuple(
            tuple(path) for path in row.architecture_projection["competition_paths"]
        )
        counts = tuple(row.architecture_projection["branch_exposure_counts"])
        assert len(paths) == len(counts) == 3
        assert len(set(paths)) == 3
        assert len({path[0] for path in paths}) == 1
        assert counts[0] > counts[1] > counts[2]
        assert max(counts) - min(counts) == 2


def test_resource_schema_exists_for_every_cell_without_fake_measurements(preflight) -> None:
    matrix, _ = preflight
    keys = {
        (row.family_id, row.seed, row.condition)
        for row in matrix.resource_schema_records
    }
    assert len(keys) == 400
    for row in matrix.resource_schema_records:
        row.validate()
        assert row.measurements_present is False
        assert "wall_clock_ms" in row.record_fields
        assert "generated_internal_events" in row.record_fields
        assert "resource_wall_clock_ms" in row.metric_fields
        assert "resource_privileged_information_count" in row.metric_fields


def test_privilege_inventory_is_explicit_and_condition_specific(preflight) -> None:
    matrix, _ = preflight
    for row in matrix.adapter_records:
        safety = row.safety
        if row.condition is ConfirmatoryCondition.G3_RECURRENT:
            assert safety.threshold_bypassed is True
            assert safety.privileged_information == ()
        elif row.condition is ConfirmatoryCondition.G4_ASSEMBLY:
            assert safety.threshold_bypassed is True
            assert safety.explicit_assembly_entries >= 1
            assert safety.privileged_information == (
                PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
            )
        elif row.condition is ConfirmatoryCondition.G5_TYPED:
            assert safety.threshold_bypassed is True
            assert safety.typed_head_count == 3
            assert safety.scalar_reward_observations == 1
            assert set(safety.privileged_information) == {
                PrivilegedInformation.TYPED_PREDICTION_HEAD,
                PrivilegedInformation.TYPED_BOUNDARY_HEAD,
                PrivilegedInformation.TYPED_MEMORY_HEAD,
                PrivilegedInformation.SCALAR_REWARD,
            }
        else:
            assert safety.threshold_bypassed is False
            assert safety.normal_field_threshold_present is True
            assert safety.explicit_assembly_entries == 0
            assert safety.typed_head_count == 0
            assert safety.scalar_reward_observations == 0
            assert safety.privileged_information == ()


def test_schema_only_records_are_unscored_and_have_no_result_value(preflight) -> None:
    matrix, _ = preflight
    assert {row.evidence_domain for row in matrix.domain_schema_records} == set(
        EvidenceDomain
    )
    for row in matrix.domain_schema_records:
        row.validate()
        state = row.state_dict()
        assert row.status is DryRunStatus.UNSCORED
        assert row.capability_result_present is False
        assert "passed" not in state
        assert state["result_field_types"]["passed"] == "bool"


def test_safety_and_privilege_guards_fail_closed(preflight) -> None:
    matrix, _ = preflight
    primary = next(
        row
        for row in matrix.adapter_records
        if row.condition is ConfirmatoryCondition.PRIMARY
    )
    with pytest.raises(ValueError, match="inspect Primary runtime state"):
        replace(primary.safety, reads_primary_runtime_state=True).validate(
            primary.condition
        )
    with pytest.raises(ValueError, match="cannot execute capability"):
        replace(primary.safety, capability_executed=True).validate(
            primary.condition
        )
    with pytest.raises(ValueError, match="cannot count as observations"):
        replace(
            primary.safety,
            generated_events_count_as_observations=True,
        ).validate(primary.condition)
    with pytest.raises(ValueError, match="cannot commit positive learning"):
        replace(
            primary.safety,
            generated_events_commit_positive_learning=True,
        ).validate(primary.condition)

    g3 = next(
        row
        for row in matrix.adapter_records
        if row.condition is ConfirmatoryCondition.G3_RECURRENT
    )
    with pytest.raises(ValueError, match="Field-threshold bypass"):
        replace(g3.safety, threshold_bypassed=False).validate(g3.condition)

    g4 = next(
        row
        for row in matrix.adapter_records
        if row.condition is ConfirmatoryCondition.G4_ASSEMBLY
    )
    with pytest.raises(ValueError, match="privilege inventory"):
        replace(g4.safety, privileged_information=()).validate(g4.condition)

    g5 = next(
        row
        for row in matrix.adapter_records
        if row.condition is ConfirmatoryCondition.G5_TYPED
    )
    with pytest.raises(ValueError, match="scalar reward"):
        replace(g5.safety, scalar_reward_observations=0).validate(g5.condition)


def test_dry_run_modules_do_not_call_capability_entrypoints() -> None:
    root = Path(__file__).parents[2]
    paths = (
        root
        / "src"
        / "sparkbrain"
        / "evaluation"
        / "v06_confirmatory_heldout_primary_dryrun.py",
        root
        / "src"
        / "sparkbrain"
        / "baselines"
        / "v06"
        / "heldout_dryrun.py",
    )
    for path in paths:
        source = path.read_text(encoding="utf-8")
        assert "v06_confirmatory_primary_adapter" not in source
        assert "v06_confirmatory_controls" not in source
        assert "g3_recurrent" not in source
        assert "g4_assembly" not in source
        assert "g5_typed" not in source
        assert "run_condition" not in source


def test_comparator_sources_do_not_import_primary_runtime_or_internal_adapter() -> None:
    root = (
        Path(__file__).parents[2]
        / "src"
        / "sparkbrain"
        / "baselines"
        / "v06"
    )
    for filename in (
        "common.py",
        "g3_recurrent.py",
        "g4_assembly.py",
        "g5_typed.py",
        "heldout_dryrun.py",
    ):
        tree = ast.parse((root / filename).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert not module.startswith("sparkbrain.v06")
                assert "v06_confirmatory_primary" not in module
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("sparkbrain.v06")
                    assert "v06_confirmatory_primary" not in alias.name


def test_building_preflight_twice_is_byte_stable() -> None:
    first = build_heldout_preflight_matrix()
    second = build_heldout_preflight_matrix()
    assert first.world_grid_hash == second.world_grid_hash
    assert first.matrix_hash == second.matrix_hash
    assert first.state_dict() == second.state_dict()

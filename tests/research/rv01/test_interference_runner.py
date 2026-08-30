from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from sparkbrain.research.rv01.interference_contract import (
    DEVELOPMENT_SEEDS,
    InterferenceFamily,
    InterferencePhase,
    held_out_worlds,
    interference_world,
)
from sparkbrain.research.rv01.interference_runner import (
    run_development_interference_suite,
    run_interference_world,
)


@pytest.fixture(scope="module")
def suite():
    return run_development_interference_suite()


def test_development_runner_executes_exactly_fifteen_frozen_worlds(suite) -> None:
    assert suite.world_count == 15
    assert len({row.world_id for row in suite.worlds}) == 15
    assert Counter(
        row.world_id.split(":", maxsplit=2)[1] for row in suite.worlds
    ) == {family.value: 3 for family in InterferenceFamily}
    assert {
        int(row.world_id.rsplit(":", maxsplit=1)[1]) for row in suite.worlds
    } == set(DEVELOPMENT_SEEDS)


def test_every_world_has_complete_phase_probe_and_resource_coverage(suite) -> None:
    expected_probe_count = 0
    for world in suite.worlds:
        route_count = world.resource.route_count
        assert len(world.training_phases) == route_count
        assert len(world.probes) == route_count * route_count
        assert world.resource.training_phase_count == route_count
        assert world.resource.probe_count == route_count * route_count
        assert world.resource.persistent_connection_entry_count == (
            world.resource.directed_edge_count
        )
        assert world.assessment.development_diagnostic_complete is True
        world.resource.validate()
        expected_probe_count += route_count * route_count
    assert suite.total_probe_count == expected_probe_count
    assert suite.total_resource_count == 15


def test_current_physical_learner_is_reused_consistently(suite) -> None:
    api_hashes = {row.learner_api.api_hash for row in suite.worlds}
    learner_classes = {row.learner_api.learner_class_name for row in suite.worlds}
    observe_methods = {row.learner_api.observe_method_name for row in suite.worlds}
    assert len(api_hashes) == 1
    assert len(learner_classes) == 1
    assert len(observe_methods) == 1
    assert all(row.assessment.any_connection_learning_detected for row in suite.worlds)


def test_endogenous_stress_cannot_modify_learned_connections(suite) -> None:
    for world in suite.worlds:
        assert world.resource.ignored_endogenous_observation_count == 1
        assert (
            world.assessment.endogenous_activity_cannot_write_connections
            is True
        )


def test_probe_rows_keep_negative_and_positive_outcomes_without_filtering(suite) -> None:
    for world in suite.worlds:
        phase_indices = {row.phase_index for row in world.training_phases}
        route_ids = {row.route_id for row in world.training_phases}
        assert phase_indices == set(range(1, world.resource.route_count + 1))
        assert {
            (row.training_phase_index, row.probe_route_id)
            for row in world.probes
        } == {
            (phase_index, route_id)
            for phase_index in phase_indices
            for route_id in route_ids
        }
        assert all(0.0 <= row.ordered_retention_fraction <= 1.0 for row in world.probes)
        assert all(0.0 <= row.first_hop_coverage_fraction <= 1.0 for row in world.probes)


def test_dense_worlds_keep_the_frozen_structural_budget(suite) -> None:
    dense = tuple(
        row
        for row in suite.worlds
        if f":{InterferenceFamily.DENSE_ROUTE_LOAD.value}:" in row.world_id
    )
    assert len(dense) == 3
    for world in dense:
        assert world.resource.route_count == 8
        assert world.resource.directed_edge_count > 12
        assert world.assessment.dense_edge_budget_exceeded in {True, False}


def test_family_specific_assessment_fields_are_not_fabricated(suite) -> None:
    for world in suite.worlds:
        family = world.world_id.split(":", maxsplit=2)[1]
        assessment = world.assessment
        if family == InterferenceFamily.DISJOINT_ROUTES.value:
            assert assessment.all_disjoint_routes_retained in {True, False}
            assert assessment.shared_branch_coverage_fraction is None
        elif family == InterferenceFamily.SHARED_CUE_BRANCHES.value:
            assert assessment.shared_branch_coverage_fraction is not None
            assert assessment.shared_branch_collapse_detected in {True, False}
        elif family == InterferenceFamily.SHARED_PREFIX_BRANCHES.value:
            assert assessment.shared_prefix_retained in {True, False}
        elif family == InterferenceFamily.EDGE_REVERSAL.value:
            assert assessment.reversal_routes_retained in {True, False}
        else:
            assert assessment.dense_edge_budget_exceeded in {True, False}


def test_semantic_replay_is_deterministic_even_when_wall_clock_differs(suite) -> None:
    replay = run_development_interference_suite()
    assert replay.world_grid_hash == suite.world_grid_hash
    assert replay.suite_hash == suite.suite_hash
    assert [row.semantic_hash for row in replay.worlds] == [
        row.semantic_hash for row in suite.worlds
    ]
    assert [
        row.resource.semantic_state_dict() for row in replay.worlds
    ] == [row.resource.semantic_state_dict() for row in suite.worlds]


def test_held_out_interference_capability_remains_sealed() -> None:
    for world in held_out_worlds():
        with pytest.raises(RuntimeError, match="sealed before freeze"):
            run_interference_world(world)


def test_runner_contains_no_g1_g2_or_functional_runtime_escape_hatch() -> None:
    root = Path(__file__).parents[3] / "src" / "sparkbrain" / "research" / "rv01"
    source = (root / "interference_runner.py").read_text(encoding="utf-8")
    bridge = (root / "physical_learner_bridge.py").read_text(encoding="utf-8")
    combined = source + bridge
    for forbidden in (
        "LocalTemporalExpectation",
        "SparseLocalTransitionAdaptation",
        "EndogenousPulseProposal",
        "PredictionRelation",
        "ActionRelation",
        "MemoryRelation",
        "RewardRelation",
        "correct_action",
        "scalar_reward",
        "meaning_state",
        "assembly_id",
    ):
        assert forbidden not in combined


def test_one_world_result_validates_against_its_original_spec() -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.SHARED_PREFIX_BRANCHES,
        1,
    )
    result = run_interference_world(world)
    result.validate(world)
    assert result.world_specification_hash == world.specification_hash()

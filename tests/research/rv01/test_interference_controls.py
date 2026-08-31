from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.interference_contract import (
    InterferenceFamily,
    InterferencePhase,
    development_worlds,
    held_out_worlds,
    interference_world,
)
from sparkbrain.research.rv01.interference_controls import (
    run_development_interference_control_suite,
    run_interference_control_world,
)
from sparkbrain.research.rv01.interference_runner import run_interference_world


@pytest.fixture(scope="module")
def suite():
    return run_development_interference_control_suite()


def test_r01_12c_executes_exactly_the_fifteen_development_worlds(suite) -> None:
    expected = {world.world_id for world in development_worlds()}
    assert suite.world_count == 15
    assert {row.world_id for row in suite.worlds} == expected
    assert len(suite.world_grid_hash) == 64
    assert len(suite.suite_hash) == 64


def test_every_world_records_all_preregistered_intervention_classes(suite) -> None:
    for result in suite.worlds:
        conditions = (
            result.baseline,
            result.reset_all_connections,
            result.weights_only_transplant,
            result.delays_only_transplant,
            result.target_edge_removed,
            result.matched_edge_removed,
            result.reversed_training_order,
            result.permuted_probe_order,
            result.deterministic_replay,
        )
        assert len({row.condition_id for row in conditions}) == len(conditions)
        assert all(len(row.connection_state_hash) == 64 for row in conditions)
        assert all(len(row.probe_signature_hash) == 64 for row in conditions)
        assert len(result.semantic_hash) == 64


def test_edge_selection_is_structural_and_matched_edge_is_endpoint_disjoint(suite) -> None:
    worlds = {world.world_id: world for world in development_worlds()}
    for result in suite.worlds:
        world = worlds[result.world_id]
        structural_edges = {
            edge
            for route in world.routes
            for edge in zip(route.units, route.units[1:], strict=False)
        }
        selection = result.edge_selection
        assert selection.target_edge in structural_edges
        assert selection.matched_edge in structural_edges
        assert not set(selection.target_edge).intersection(selection.matched_edge)
        assert selection.target_route_id != selection.matched_route_id


def test_replay_probe_order_and_write_boundaries_are_measured_as_invariants(suite) -> None:
    for result in suite.worlds:
        assessment = result.assessment
        assert assessment.deterministic_replay_connection_hash is True
        assert assessment.deterministic_replay_probe_hash is True
        assert assessment.probe_order_invariant is True
        assert assessment.plasticity_disable_preserves_execution is True
        assert assessment.plasticity_disable_blocks_external_learning is True
        assert assessment.endogenous_activity_cannot_write_connections is True
        assert result.plasticity_freeze.all_phase_probes_equivalent is True
        assert result.plasticity_freeze.all_external_writes_blocked is True


def test_capability_effects_remain_diagnostic_not_forced_to_pass(suite) -> None:
    for result in suite.worlds:
        assessment = result.assessment
        assert -1.0 <= assessment.target_edge_retention_delta <= 1.0
        assert -1.0 <= assessment.matched_ablation_target_retention_delta <= 1.0
        assert -2.0 <= assessment.target_edge_selective_delta <= 2.0
        assert -1.0 <= assessment.reversed_order_retention_delta <= 1.0
        assert 0.0 <= result.reset_all_connections.mean_ordered_retention_fraction <= 1.0
        assert 0.0 <= result.weights_only_transplant.mean_ordered_retention_fraction <= 1.0
        assert 0.0 <= result.delays_only_transplant.mean_ordered_retention_fraction <= 1.0


def test_control_baseline_matches_r01_12b_final_physical_state() -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.SHARED_PREFIX_BRANCHES,
        1,
    )
    control = run_interference_control_world(world)
    original = run_interference_world(world)
    final_phase_hashes = {
        row.connection_state_hash
        for row in original.probes
        if row.training_phase_index == world.route_count
    }
    assert final_phase_hashes == {control.baseline.connection_state_hash}


def test_one_world_control_replay_is_semantically_deterministic() -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.EDGE_REVERSAL,
        0,
    )
    first = run_interference_control_world(world)
    second = run_interference_control_world(world)
    assert first.semantic_hash == second.semantic_hash
    assert first.state_dict() == second.state_dict()


def test_held_out_interference_controls_remain_sealed() -> None:
    for world in held_out_worlds():
        with pytest.raises(RuntimeError, match="sealed before R01-12E freeze"):
            run_interference_control_world(world)


def test_r01_12c_contains_no_functional_runtime_escape_hatch() -> None:
    root = Path(__file__).parents[3] / "src" / "sparkbrain" / "research" / "rv01"
    source = (root / "interference_controls.py").read_text(encoding="utf-8")
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
        assert forbidden not in source

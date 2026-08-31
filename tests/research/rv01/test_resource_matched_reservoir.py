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
from sparkbrain.research.rv01.resource_matched_reservoir import (
    ResourceMatchedReservoirConfig,
    ResourceMatchedSparseReservoir,
    run_development_resource_matched_reservoir_suite,
    run_resource_matched_reservoir_world,
)


@pytest.fixture(scope="module")
def suite():
    return run_development_resource_matched_reservoir_suite()


def test_r01_12d_executes_exactly_the_fifteen_development_worlds(suite) -> None:
    expected = {world.world_id for world in development_worlds()}
    assert suite.world_count == 15
    assert {row.world_id for row in suite.worlds} == expected
    assert len(suite.world_grid_hash) == 64
    assert len(suite.suite_hash) == 64


def test_every_world_is_exactly_state_and_event_budget_matched(suite) -> None:
    for result in suite.worlds:
        resources = result.resources
        assert resources.resource_match_passed is True
        assert resources.exact_persistent_state_match is True
        assert resources.exact_external_event_match is True
        assert resources.matched_unit_state_count is True
        assert resources.matched_generation_budget is True
        assert resources.matched_active_output_budget is True
        assert (
            resources.reservoir_fixed_recurrent_scalar_count
            == resources.directed_edge_count
        )
        assert (
            resources.reservoir_learned_readout_scalar_count
            == resources.directed_edge_count
        )
        assert (
            resources.reservoir_persistent_scalar_count
            == resources.field_persistent_scalar_count
        )


def test_comparator_replay_is_deterministic_without_training_replay(suite) -> None:
    for result in suite.worlds:
        assessment = result.assessment
        assert assessment.deterministic_replay_state_hash is True
        assert assessment.deterministic_replay_probe_hash is True
        assert assessment.no_training_replay is True
        assert result.recurrent_state_hash == result.replay_recurrent_state_hash
        assert result.probe_signature_hash == result.replay_probe_signature_hash


def test_comparator_outcome_is_recorded_without_forcing_reservoir_or_field_win(suite) -> None:
    for result in suite.worlds:
        assessment = result.assessment
        assert 0.0 <= assessment.field_mean_ordered_retention <= 1.0
        assert 0.0 <= assessment.reservoir_mean_ordered_retention <= 1.0
        assert -1.0 <= assessment.field_minus_reservoir_retention <= 1.0
        assert isinstance(
            assessment.reservoir_matches_or_exceeds_mean_retention,
            bool,
        )
        assert 0 <= assessment.field_exact_route_count
        assert 0 <= assessment.reservoir_exact_route_count


def test_one_world_resource_matched_comparison_is_semantically_repeatable() -> None:
    world = interference_world(
        InterferencePhase.DEVELOPMENT,
        InterferenceFamily.EDGE_REVERSAL,
        1,
    )
    first = run_resource_matched_reservoir_world(world)
    second = run_resource_matched_reservoir_world(world)
    assert first.semantic_hash == second.semantic_hash
    assert first.state_dict() == second.state_dict()


def test_sparse_reservoir_persistent_budget_is_two_scalars_per_edge() -> None:
    edges = ((0, 1), (1, 2), (2, 3), (3, 4))
    model = ResourceMatchedSparseReservoir(
        unit_count=12,
        directed_edges=edges,
        maximum_active_outputs=2,
        seed=12001,
        config=ResourceMatchedReservoirConfig(),
    )
    assert model.fixed_recurrent_scalar_count == len(edges)
    assert model.learned_readout_scalar_count == len(edges)
    assert model.persistent_scalar_count == 2 * len(edges)


def test_held_out_resource_matched_comparison_remains_sealed() -> None:
    for world in held_out_worlds():
        with pytest.raises(RuntimeError, match="sealed before R01-12E"):
            run_resource_matched_reservoir_world(world)


def test_r01_12d_runtime_contains_no_semantic_or_g1_g2_escape_hatch() -> None:
    root = Path(__file__).parents[3] / "src" / "sparkbrain" / "research" / "rv01"
    source = (root / "resource_matched_reservoir.py").read_text(encoding="utf-8")
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

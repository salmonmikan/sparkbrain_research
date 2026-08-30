from __future__ import annotations

import math
from pathlib import Path

import pytest

from sparkbrain.research.rv01.direct_field_plasticity import (
    DirectFieldPlasticityConfig,
    ExternalGatedDirectFieldPlasticity,
)
from sparkbrain.research.rv01.direct_field_plasticity_probe import (
    BASE_DELAY_MS,
    BASE_WEIGHT,
    TRAINING_EPISODES,
    TRAINING_INTERVAL_MS,
    new_uniform_field,
    run_direct_plasticity_suite,
    train_external_sequence,
)
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse


def _pulse(
    event_id: str,
    time_ms: float,
    unit_id: int,
    origin: EventOrigin = EventOrigin.EXTERNAL,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
        polarity=1,
        origin=origin,
    )


def test_external_sequence_changes_only_adjacent_physical_edges() -> None:
    suite = run_direct_plasticity_suite()
    trained = suite.trained
    expected_weight = BASE_WEIGHT + TRAINING_EPISODES * 0.5 * math.exp(
        -TRAINING_INTERVAL_MS / 10.0
    )

    assert trained.connection_state_hash_before != trained.connection_state_hash_after
    assert trained.external_observation_count == 12
    assert trained.ignored_endogenous_count == 0
    assert trained.update_count == 18
    for row in trained.adjacent:
        assert row.weight == pytest.approx(expected_weight)
        assert row.delay_ms == pytest.approx(5.375)
    for row in trained.reverse:
        assert row.weight == pytest.approx(0.0)
        assert row.delay_ms == pytest.approx(BASE_DELAY_MS)
    for row in trained.untouched:
        assert row.weight == pytest.approx(BASE_WEIGHT)
        assert row.delay_ms == pytest.approx(BASE_DELAY_MS)


def test_unit_local_trace_reset_does_not_erase_connection_learning() -> None:
    suite = run_direct_plasticity_suite()
    assert suite.trace_reset_hash_before == suite.trace_reset_hash_after
    assert suite.assessment.trace_reset_preserves_learned_connections is True


def test_endogenous_events_cannot_modify_physical_connections() -> None:
    suite = run_direct_plasticity_suite()
    row = suite.endogenous_only
    assert row.connection_state_hash_after == row.connection_state_hash_before
    assert row.external_observation_count == 0
    assert row.ignored_endogenous_count == 12
    assert row.update_count == 0
    assert suite.assessment.endogenous_activity_cannot_update_connections is True


def test_same_local_rule_works_under_unit_permutation() -> None:
    suite = run_direct_plasticity_suite()
    row = suite.permuted
    assert row.sequence == (3, 1, 4, 0)
    assert all(edge.weight > BASE_WEIGHT for edge in row.adjacent)
    assert all(edge.weight < BASE_WEIGHT for edge in row.reverse)
    assert all(
        TRAINING_INTERVAL_MS < edge.delay_ms < BASE_DELAY_MS
        for edge in row.adjacent
    )
    assert suite.assessment.unit_permutation_is_supported is True


def test_connection_updates_are_bounded_under_long_training() -> None:
    field = new_uniform_field(4)
    controller = train_external_sequence(
        field,
        (0, 1, 2, 3),
        episodes=100,
    )
    config = controller.config
    for edge in field.connections.values():
        assert config.minimum_weight <= edge.weight <= config.maximum_weight
        assert config.minimum_delay_ms <= edge.delay_ms <= config.maximum_delay_ms
    assert field.connection(0, 1).weight == pytest.approx(config.maximum_weight)
    assert field.connection(1, 0).weight == pytest.approx(config.minimum_weight)
    assert field.connection(0, 1).delay_ms == pytest.approx(5.0)


def test_controller_state_contains_only_unit_local_working_traces() -> None:
    suite = run_direct_plasticity_suite()
    state = suite.trained.controller_state
    assert set(state) == {
        "config",
        "current_time_ms",
        "external_observation_count",
        "ignored_endogenous_count",
        "unit_traces",
        "update_count",
    }
    lowered = str(state).lower()
    for forbidden in (
        "transitions",
        "proposals",
        "paths",
        "confirmed_count",
        "contradicted_count",
        "reward",
    ):
        assert forbidden not in lowered
    assert suite.assessment.controller_has_no_pairwise_learned_table is True


def test_invalid_or_nonlocal_observations_fail_closed() -> None:
    controller = ExternalGatedDirectFieldPlasticity(new_uniform_field(3))
    controller.observe(_pulse("first", 10.0, 0))
    with pytest.raises(ValueError, match="cannot move backwards"):
        controller.observe(_pulse("backwards", 9.0, 1))
    with pytest.raises(ValueError, match="requires a unit target"):
        controller.observe(
            RuntimePulse(
                event_id="wrong-target",
                time_ms=11.0,
                target="port:7",
                magnitude=1.0,
                polarity=1,
                origin=EventOrigin.EXTERNAL,
            )
        )
    with pytest.raises(KeyError, match="unknown external target"):
        controller.observe(_pulse("unknown", 11.0, 99))


def test_config_rejects_unbounded_or_invalid_ranges() -> None:
    with pytest.raises(ValueError, match="maximum_lag_ms"):
        DirectFieldPlasticityConfig(maximum_lag_ms=0.25).validate()
    with pytest.raises(ValueError, match="maximum_weight"):
        DirectFieldPlasticityConfig(
            minimum_weight=1.0,
            maximum_weight=0.5,
        ).validate()
    with pytest.raises(ValueError, match="maximum_updates_per_event"):
        DirectFieldPlasticityConfig(maximum_updates_per_event=0).validate()


def test_r01_03_direct_physical_plasticity_candidate_is_complete() -> None:
    assessment = run_direct_plasticity_suite().assessment
    assert assessment.physical_connection_state_changed is True
    assert assessment.adjacent_edges_potentiated is True
    assert assessment.reverse_edges_depressed is True
    assert assessment.nonadjacent_edges_unchanged is True
    assert assessment.adjacent_delays_moved_toward_observed_lag is True
    assert assessment.trace_reset_preserves_learned_connections is True
    assert assessment.endogenous_activity_cannot_update_connections is True
    assert assessment.unit_permutation_is_supported is True
    assert assessment.weights_and_delays_are_bounded is True
    assert assessment.controller_has_no_pairwise_learned_table is True
    assert assessment.engineering_candidate is True


def test_direct_physical_plasticity_is_deterministic() -> None:
    first = run_direct_plasticity_suite()
    second = run_direct_plasticity_suite()
    assert first == second
    assert first.suite_hash == second.suite_hash


def test_rv01_direct_plasticity_does_not_import_g1_g2_or_reward_state() -> None:
    root = Path(__file__).parents[3] / "src" / "sparkbrain" / "research" / "rv01"
    source = (root / "direct_field_plasticity.py").read_text(encoding="utf-8")
    assert "LocalTemporalExpectation" not in source
    assert "SparseLocalTransitionAdaptation" not in source
    assert "EndogenousPulseProposal" not in source
    assert "reward_trace" not in source

from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_validity_probe import (
    CanonicalValidityAssaySuite,
    run_canonical_validity_assay_suite,
)


@pytest.fixture(scope="module")
def suite() -> CanonicalValidityAssaySuite:
    return run_canonical_validity_assay_suite()


def test_missing_middle_is_strictly_forward_and_not_readout_only(
    suite: CanonicalValidityAssaySuite,
) -> None:
    row = suite.missing_middle
    assert row.generated_target == "unit:2"
    assert row.generated_time_ms == 110.0
    assert row.generated_time_ms < row.later_external_time_ms
    assert row.strict_forward is True
    assert row.later_link_confirmed is True
    assert row.readout_only_generated_count == 0
    assert row.early_future_generated_count == 0
    assert row.early_future_retrospective_only is True


def test_prefix_continuation_requires_history_and_field_reinjection(
    suite: CanonicalValidityAssaySuite,
) -> None:
    row = suite.prefix_continuation
    assert row.generated_targets == ("unit:2", "unit:3")
    assert row.generated_times_ms == (110.0, 115.0)
    assert row.external_observation_count == 2
    assert row.committed_positive_updates == 1
    assert row.no_reinjection_generated_count == 0
    assert row.no_history_generated_count == 0


def test_equal_branch_alternatives_are_preserved_in_the_field(
    suite: CanonicalValidityAssaySuite,
) -> None:
    row = suite.branching
    assert row.equal_branch_proposal_targets == ("unit:2", "unit:3")
    assert row.equal_branch_generated_targets == ("unit:2", "unit:3")
    assert row.equal_branch_effective_currents == pytest.approx((0.5, 0.5))
    assert row.readout_only_generated_count == 0


def test_imbalanced_branch_strength_changes_normal_rule_field_outcome(
    suite: CanonicalValidityAssaySuite,
) -> None:
    row = suite.branching
    assert row.imbalanced_branch_proposal_targets == ("unit:2", "unit:3")
    assert row.imbalanced_branch_effective_currents == pytest.approx((2 / 3, 1 / 3))
    assert row.imbalanced_branch_generated_targets == ("unit:2",)


def test_omission_generates_internal_event_but_external_observation_wins(
    suite: CanonicalValidityAssaySuite,
) -> None:
    row = suite.omission
    assert row.omitted_generated_targets == ("unit:1",)
    assert row.observed_generated_count == 0
    assert row.observed_external_spike_units == (1,)
    assert row.matched_prediction_count == 1
    assert row.external_observation_count == 2


def test_origin_controls_reject_copy_echo_and_unexcluded_queue(
    suite: CanonicalValidityAssaySuite,
) -> None:
    row = suite.origin_controls
    assert row.direct_copy_candidate is False
    assert "direct_current_input_copy" in row.direct_copy_reasons
    assert row.fixed_echo_candidate is False
    assert "known_fixed_delay_echo" in row.fixed_echo_reasons
    assert row.queue_unexcluded_candidate is False
    assert "queue_replay_not_excluded" in row.queue_unexcluded_reasons
    assert row.unknown_source_generated_count == 0


def test_validity_suite_passes_only_as_supporting_engineering_diagnostic(
    suite: CanonicalValidityAssaySuite,
) -> None:
    assessment = suite.assessment
    assert assessment.strict_missing_middle_supported is True
    assert assessment.readout_only_rejected is True
    assert assessment.retrospective_not_forward is True
    assert assessment.prefix_continuation_supported is True
    assert assessment.no_history_and_no_reinjection_controls_passed is True
    assert assessment.equal_branch_alternatives_preserved is True
    assert assessment.branch_strength_changes_field_outcome is True
    assert assessment.omission_generates_internal_event is True
    assert assessment.matching_external_event_remains_authoritative is True
    assert assessment.direct_copy_rejected is True
    assert assessment.fixed_echo_rejected is True
    assert assessment.unresolved_queue_rejected is True
    assert assessment.no_unknown_source_generation is True
    assert assessment.engineering_candidate is True


def test_validity_suite_is_deterministic_and_taxonomy_free_in_runtime_inputs(
    suite: CanonicalValidityAssaySuite,
) -> None:
    assert suite == run_canonical_validity_assay_suite()
    lowered = str(suite.state_dict()).lower()
    for forbidden in (
        "assembly_id",
        "correct_action",
        "scalar_reward",
        "reward_value",
        "utility_target",
        "meaning_state",
    ):
        assert forbidden not in lowered

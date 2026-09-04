from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_relation_reentry_probe import (
    CanonicalRelationReentrySuite,
    run_canonical_relation_reentry_suite,
)


@pytest.fixture(scope="module")
def suite() -> CanonicalRelationReentrySuite:
    return run_canonical_relation_reentry_suite()


def test_acquired_anonymous_relation_changes_later_field_dynamics(
    suite: CanonicalRelationReentrySuite,
) -> None:
    row = suite.acquisition
    assert row.learned_links == (("port:7", "unit:8", 0.8, 3, 0),)
    assert row.relation_record_targets == ("unit:8",)
    assert row.relation_record_reliabilities == pytest.approx((0.8,))
    assert row.effective_currents == pytest.approx((0.72,))
    assert row.accepted_count == 1
    assert row.generated_units == (8,)


def test_reversal_changes_the_later_endogenous_field_spark(
    suite: CanonicalRelationReentrySuite,
) -> None:
    row = suite.reversal
    assert row.relation_record_targets == ("unit:8", "unit:9")
    assert row.relation_record_reliabilities == pytest.approx((0.5, 0.8))
    assert row.effective_currents == pytest.approx((0.45, 0.72))
    assert row.accepted_count == 2
    assert row.generated_units == (9,)
    assert suite.assessment.reversal_changes_field is True


def test_return_to_old_contingency_restores_the_old_field_response(
    suite: CanonicalRelationReentrySuite,
) -> None:
    row = suite.return_to_old
    assert row.relation_record_targets == ("unit:8", "unit:9")
    assert row.relation_record_reliabilities == pytest.approx((7 / 11, 0.5))
    assert row.effective_currents == pytest.approx((6.3 / 11, 0.45))
    assert row.generated_units == (8,)
    assert suite.assessment.return_restores_field is True


def test_stable_world_keeps_the_same_relation_driven_response(
    suite: CanonicalRelationReentrySuite,
) -> None:
    row = suite.stable
    assert row.learned_links == (("port:7", "unit:8", 10 / 11, 9, 0),)
    assert row.generated_units == (8,)
    assert suite.assessment.stable_control_stays_stable is True


def test_no_reentry_and_consistency_reset_remove_the_later_spark(
    suite: CanonicalRelationReentrySuite,
) -> None:
    assert suite.no_reentry.generated_units == ()
    assert suite.no_reentry.accepted_count == 0
    assert suite.consistency_reset.learned_links == (
        ("port:7", "unit:8", 0.8, 3, 0),
    )
    assert suite.consistency_reset.relation_record_targets == ()
    assert suite.consistency_reset.generated_units == ()
    assert suite.assessment.no_reentry_has_no_effect is True
    assert suite.assessment.consistency_reset_has_no_effect is True


def test_unrelated_active_relation_does_not_affect_the_target_port(
    suite: CanonicalRelationReentrySuite,
) -> None:
    row = suite.unrelated_relation
    assert row.learned_links == (("port:9", "unit:9", 0.8, 3, 0),)
    assert row.relation_record_targets == ()
    assert row.generated_units == ()
    assert suite.assessment.unrelated_relation_has_no_effect is True


def test_all_links_are_projected_by_one_rule_not_evaluator_argmax(
    suite: CanonicalRelationReentrySuite,
) -> None:
    row = suite.reversal
    assert row.accepted_count == 2
    assert row.effective_currents[0] < 0.5
    assert row.effective_currents[1] > 0.5
    assert row.generated_units == (9,)
    assert suite.assessment.all_links_use_same_projection is True


def test_reentry_creates_no_external_observation_or_positive_self_confirmation(
    suite: CanonicalRelationReentrySuite,
) -> None:
    for row in (
        suite.acquisition,
        suite.reversal,
        suite.return_to_old,
        suite.stable,
        suite.no_reentry,
        suite.consistency_reset,
        suite.unrelated_relation,
    ):
        assert row.external_observation_count_before_probe == (
            row.external_observation_count_after_probe
        )
        assert row.committed_positive_updates_before_probe == (
            row.committed_positive_updates_after_probe
        )
    assert suite.assessment.no_external_count_from_reentry is True
    assert suite.assessment.no_positive_self_confirmation is True


def test_relation_reentry_runtime_remains_assembly_and_taxonomy_free(
    suite: CanonicalRelationReentrySuite,
) -> None:
    lowered = str(suite.state_dict()).lower()
    for forbidden in (
        "assembly_id",
        "relation_type",
        "prediction_relation",
        "action_relation",
        "memory_relation",
        "reward_relation",
        "correct_action",
        "reward_value",
        "utility_target",
        "functional_role",
        "meaning_state",
    ):
        assert forbidden not in lowered
    assert suite.assessment.taxonomy_free is True
    assert suite.assessment.engineering_candidate is True

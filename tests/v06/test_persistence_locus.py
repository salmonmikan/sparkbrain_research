from __future__ import annotations

from sparkbrain.evaluation.v06_persistence_probe import (
    CanonicalPersistenceLocusSuite,
    run_canonical_persistence_locus_suite,
)


def suite() -> CanonicalPersistenceLocusSuite:
    return run_canonical_persistence_locus_suite()


def test_local_transition_state_transfers_same_input_response() -> None:
    result = suite().local_transition
    assert result.transplanted_generated_units == (1,)
    assert result.reset_generated_units == ()
    assert result.field_only_generated_units == ()
    assert result.unrelated_generated_units == (2,)


def test_local_transition_effect_follows_explicit_state_not_recipient_field() -> None:
    result = suite().local_transition
    assert result.transplanted_field_before_hash == result.reset_field_before_hash
    assert result.transplanted_field_before_hash == result.field_only_field_before_hash
    assert result.transplanted_field_before_hash == result.unrelated_field_before_hash
    assert result.transplanted_external_observation_count == 1
    assert result.transplanted_positive_updates == 0


def test_anonymous_consistency_state_transfers_relation_reentry_response() -> None:
    result = suite().consistency
    assert result.transplanted_generated_units == (8,)
    assert result.reset_generated_units == ()
    assert result.unrelated_port_generated_units == ()
    assert result.alternate_target_generated_units == (9,)


def test_consistency_effect_follows_explicit_state_not_recipient_field() -> None:
    result = suite().consistency
    assert result.transplanted_field_before_hash == result.reset_field_before_hash
    assert result.transplanted_field_before_hash == result.unrelated_field_before_hash
    assert result.transplanted_field_before_hash == result.alternate_field_before_hash
    assert result.transplanted_external_observation_count == 0
    assert result.transplanted_positive_updates == 0


def test_current_persistence_locus_is_explicit_state_dominant_candidate() -> None:
    assessment = suite().assessment
    assert assessment.local_transition_reset_removes_effect is True
    assert assessment.local_transition_transplant_moves_effect is True
    assert assessment.local_unrelated_state_redirects_effect is True
    assert assessment.field_state_alone_does_not_transfer_local_effect is True
    assert assessment.consistency_reset_removes_effect is True
    assert assessment.consistency_transplant_moves_effect is True
    assert assessment.unrelated_consistency_does_not_transfer_target_effect is True
    assert assessment.alternate_consistency_redirects_effect is True
    assert assessment.recipient_field_states_matched is True
    assert assessment.no_positive_self_confirmation is True
    assert assessment.explicit_state_dominant_candidate is True
    assert assessment.distributed_field_persistence_supported is False
    assert assessment.engineering_candidate is True


def test_persistence_locus_probe_is_deterministic() -> None:
    first = run_canonical_persistence_locus_suite()
    second = run_canonical_persistence_locus_suite()
    assert first == second

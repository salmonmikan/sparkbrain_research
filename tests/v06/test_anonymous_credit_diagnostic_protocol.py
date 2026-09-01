from __future__ import annotations

from dataclasses import replace

from sparkbrain.evaluation.v061_anonymous_credit_diagnostic_protocol import (
    CausalCreditObservation,
    EvidenceSource,
    WorldRelationPermutationTrial,
    assess_causal_credit_trial,
    assess_world_relation_permutation,
    build_causal_credit_protocol_matrix,
)


def _trial(trial_id: str):
    return next(
        row for row in build_causal_credit_protocol_matrix() if row.trial_id == trial_id
    )


def test_protocol_matrix_covers_match_swap_contradiction_absence_and_internal_only() -> None:
    matrix = build_causal_credit_protocol_matrix()
    assert len(matrix) == 5
    assert {row.evidence_source for row in matrix} == set(EvidenceSource)
    assert {row.trial_id for row in matrix} == {
        "external-match-a",
        "external-match-b-lineage-swap",
        "external-contradiction-a",
        "external-absence-a",
        "internal-replay-only-a",
    }
    for row in matrix:
        row.validate()
        assert (
            row.causal_lineage.matching_signature()
            == row.matched_lineage.matching_signature()
        )


def test_external_match_updates_only_the_causal_lineage() -> None:
    trial = _trial("external-match-a")
    observation = CausalCreditObservation(
        trial_id=trial.trial_id,
        causal_lineage_update=1.0,
        matched_lineage_update=0.0,
        external_observation_count_delta=1,
        positive_commit_count_delta=1,
    )
    assessment = assess_causal_credit_trial(trial, observation)
    assert assessment.accepted is True
    assert assessment.causal_selective_update is True
    assert assessment.reason == "accepted"


def test_lineage_swap_requires_credit_to_follow_the_new_causal_lineage() -> None:
    trial = _trial("external-match-b-lineage-swap")
    correct = assess_causal_credit_trial(
        trial,
        CausalCreditObservation(
            trial_id=trial.trial_id,
            causal_lineage_update=1.0,
            matched_lineage_update=0.0,
            external_observation_count_delta=1,
            positive_commit_count_delta=1,
        ),
    )
    wrong = assess_causal_credit_trial(
        trial,
        CausalCreditObservation(
            trial_id=trial.trial_id,
            causal_lineage_update=0.0,
            matched_lineage_update=1.0,
            external_observation_count_delta=1,
            positive_commit_count_delta=1,
        ),
    )
    assert correct.accepted is True
    assert wrong.accepted is False
    assert wrong.reason == "causal_lineage_not_selective"


def test_external_contradiction_must_selectively_weaken_the_causal_lineage() -> None:
    trial = _trial("external-contradiction-a")
    accepted = assess_causal_credit_trial(
        trial,
        CausalCreditObservation(
            trial_id=trial.trial_id,
            causal_lineage_update=-1.0,
            matched_lineage_update=0.0,
            external_observation_count_delta=1,
            positive_commit_count_delta=0,
        ),
    )
    nonselective = assess_causal_credit_trial(
        trial,
        CausalCreditObservation(
            trial_id=trial.trial_id,
            causal_lineage_update=-1.0,
            matched_lineage_update=-1.0,
            external_observation_count_delta=1,
            positive_commit_count_delta=0,
        ),
    )
    assert accepted.accepted is True
    assert accepted.contradiction_corrective_update is True
    assert nonselective.accepted is False
    assert nonselective.reason == "contradiction_not_lineage_selective"


def test_absence_and_internal_replay_cannot_create_positive_credit() -> None:
    for trial_id in ("external-absence-a", "internal-replay-only-a"):
        trial = _trial(trial_id)
        neutral = assess_causal_credit_trial(
            trial,
            CausalCreditObservation(
                trial_id=trial.trial_id,
                causal_lineage_update=0.0,
                matched_lineage_update=0.0,
                external_observation_count_delta=0,
                positive_commit_count_delta=0,
            ),
        )
        positive = assess_causal_credit_trial(
            trial,
            CausalCreditObservation(
                trial_id=trial.trial_id,
                causal_lineage_update=1.0,
                matched_lineage_update=0.0,
                external_observation_count_delta=0,
                positive_commit_count_delta=1,
            ),
        )
        assert neutral.accepted is True
        assert positive.accepted is False
    internal = _trial("internal-replay-only-a")
    violation = assess_causal_credit_trial(
        internal,
        CausalCreditObservation(
            trial_id=internal.trial_id,
            causal_lineage_update=1.0,
            matched_lineage_update=0.0,
            external_observation_count_delta=0,
            positive_commit_count_delta=1,
        ),
    )
    assert violation.self_confirmation_guard_passed is False
    assert violation.reason == "self_confirmation_violation"


def test_fixed_local_state_currently_exposes_missing_world_to_transition_path() -> None:
    unchanged = WorldRelationPermutationTrial(
        trial_id="current-primary-structure",
        local_state_hash_before="a" * 64,
        local_state_hash_after="a" * 64,
        world_relation_before="external:1",
        world_relation_after="external:2",
        selected_lineage_before="lineage-a",
        selected_lineage_after="lineage-a",
    )
    changed = replace(unchanged, selected_lineage_after="lineage-b")
    current_assessment = assess_world_relation_permutation(unchanged)
    hypothetical_assessment = assess_world_relation_permutation(changed)
    assert current_assessment.world_to_transition_circulation_observed is False
    assert hypothetical_assessment.world_to_transition_circulation_observed is True


def test_protocol_contains_no_typed_reward_or_semantic_answer_contract() -> None:
    lowered = str([row.state_dict() for row in build_causal_credit_protocol_matrix()]).lower()
    for forbidden in (
        "correct_action",
        "reward_value",
        "meaning_state",
        "functional_role",
        "assembly_id",
        "expected_answer",
    ):
        assert forbidden not in lowered

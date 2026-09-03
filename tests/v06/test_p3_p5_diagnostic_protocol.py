from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import (
    AmbiguityContinuationTrial,
    BehavioralChallenge,
    BehavioralMechanismRun,
    BehavioralOutcome,
    ContinuationEvidence,
    StateLocus,
    StateLocusCrossTransplantTrial,
    StateLocusSnapshot,
    assess_ambiguity_continuation,
    assess_behavioral_table_equivalence,
    assess_state_locus_cross_transplant,
)


def _state(
    *,
    local: str = "local-a",
    field: str = "field-a",
    consistency: str = "consistency-a",
    return_address: str | None = "return-a",
) -> StateLocusSnapshot:
    return StateLocusSnapshot(
        local_transition_hash=local,
        field_state_hash=field,
        consistency_hash=consistency,
        transient_return_address_hash=return_address,
    )


def test_p3_local_transition_only_can_be_classified_as_competition_carrier() -> None:
    trial = StateLocusCrossTransplantTrial(
        trial_id="local-only",
        baseline_state=_state(),
        donor_state=_state(local="local-b"),
        transplanted_state=_state(local="local-b"),
        transplanted_loci=(StateLocus.LOCAL_TRANSITION,),
        selected_lineage_before="lineage-a",
        selected_lineage_after="lineage-b",
        donor_selected_lineage="lineage-b",
        reentry_signature_before=("reentry-a",),
        reentry_signature_after=("reentry-a",),
        donor_reentry_signature=("reentry-b",),
    )
    assessment = assess_state_locus_cross_transplant(trial)
    assert assessment.local_transition_carries_competition is True
    assert assessment.field_state_independently_carries_competition is False
    assert assessment.interpretation == "explicit_local_transition_state_transfers_future_competition"


def test_p3_consistency_only_reentry_change_does_not_count_as_g1_transfer() -> None:
    trial = StateLocusCrossTransplantTrial(
        trial_id="consistency-reentry-only",
        baseline_state=_state(),
        donor_state=_state(consistency="consistency-b"),
        transplanted_state=_state(consistency="consistency-b"),
        transplanted_loci=(StateLocus.CONSISTENCY,),
        selected_lineage_before="lineage-a",
        selected_lineage_after="lineage-a",
        donor_selected_lineage="lineage-b",
        reentry_signature_before=("reentry-a",),
        reentry_signature_after=("reentry-b",),
        donor_reentry_signature=("reentry-b",),
    )
    assessment = assess_state_locus_cross_transplant(trial)
    assert assessment.future_competition_changed is False
    assert assessment.donor_reentry_effect_transferred is True
    assert assessment.consistency_independently_reaches_competition is False
    assert assessment.interpretation == (
        "transplant_changes_downstream_reentry_without_upstream_competition"
    )


def test_p3_field_only_competition_transfer_is_an_explicit_falsifier() -> None:
    trial = StateLocusCrossTransplantTrial(
        trial_id="field-only-falsifier",
        baseline_state=_state(),
        donor_state=_state(field="field-b"),
        transplanted_state=_state(field="field-b"),
        transplanted_loci=(StateLocus.FIELD_STATE,),
        selected_lineage_before="lineage-a",
        selected_lineage_after="lineage-b",
        donor_selected_lineage="lineage-b",
        reentry_signature_before=(),
        reentry_signature_after=(),
        donor_reentry_signature=(),
    )
    assessment = assess_state_locus_cross_transplant(trial)
    assert assessment.field_state_independently_carries_competition is True
    assert assessment.interpretation == "field_state_alone_transfers_future_competition"


def test_p3_fails_closed_when_an_undeclared_locus_changes() -> None:
    trial = StateLocusCrossTransplantTrial(
        trial_id="undeclared-change",
        baseline_state=_state(),
        donor_state=_state(local="local-b", field="field-b"),
        transplanted_state=_state(local="local-b", field="field-b"),
        transplanted_loci=(StateLocus.LOCAL_TRANSITION,),
        selected_lineage_before="lineage-a",
        selected_lineage_after="lineage-b",
        donor_selected_lineage="lineage-b",
        reentry_signature_before=(),
        reentry_signature_after=(),
        donor_reentry_signature=(),
    )
    with pytest.raises(ValueError, match="non-transplanted locus changed"):
        assess_state_locus_cross_transplant(trial)


def _ambiguity_trial(**changes: object) -> AmbiguityContinuationTrial:
    base = AmbiguityContinuationTrial(
        trial_id="ambiguity",
        candidate_lineages=("lineage-a", "lineage-b"),
        initial_competition_strengths=(1.0, 1.0),
        early_active_lineages=("lineage-a", "lineage-b"),
        evidence_source=ContinuationEvidence.EXTERNAL_MATCH,
        causal_lineage="lineage-a",
        later_competition_strengths=(1.8, 1.0),
        later_active_lineages=("lineage-a", "lineage-b"),
        external_observation_count_delta=1,
        positive_commit_count_delta=1,
    )
    return replace(base, **changes)


def test_p4_preserves_co_maximal_plurality_then_uses_external_evidence() -> None:
    assessment = assess_ambiguity_continuation(_ambiguity_trial())
    assert assessment.initial_plurality_preserved is True
    assert assessment.premature_singleton_avoided is True
    assert assessment.causal_history_changes_later_competition is True
    assert assessment.accepted is True


def test_p4_rejects_forced_early_singleton() -> None:
    assessment = assess_ambiguity_continuation(
        _ambiguity_trial(early_active_lineages=("lineage-a",))
    )
    assert assessment.accepted is False
    assert assessment.reason == "premature_singleton_or_missing_initial_plurality"


def test_p4_current_downstream_only_shape_fails_continuation_requirement() -> None:
    assessment = assess_ambiguity_continuation(
        _ambiguity_trial(
            later_competition_strengths=(1.0, 1.0),
            positive_commit_count_delta=0,
        )
    )
    assert assessment.accepted is False
    assert assessment.causal_history_changes_later_competition is False
    assert assessment.reason == "later_external_evidence_did_not_change_competition"


def test_p4_internal_replay_cannot_break_the_tie_or_positive_commit() -> None:
    neutral = _ambiguity_trial(
        evidence_source=ContinuationEvidence.INTERNAL_REPLAY_ONLY,
        later_competition_strengths=(1.0, 1.0),
        external_observation_count_delta=0,
        positive_commit_count_delta=0,
    )
    violation = replace(
        neutral,
        later_competition_strengths=(1.8, 1.0),
        positive_commit_count_delta=1,
    )
    assert assess_ambiguity_continuation(neutral).accepted is True
    violated = assess_ambiguity_continuation(violation)
    assert violated.accepted is False
    assert violated.self_confirmation_guard_passed is False
    assert violated.reason == "self_confirmation_violation"


def _outcomes(*, unseen_suffix: str = "same") -> tuple[BehavioralOutcome, ...]:
    rows: list[BehavioralOutcome] = []
    for challenge in BehavioralChallenge:
        suffix = unseen_suffix if challenge is BehavioralChallenge.UNSEEN_LINEAGE_COMBINATION else "same"
        rows.append(
            BehavioralOutcome(
                challenge=challenge,
                future_competition_signature=(challenge.value, suffix),
                boundary_signature=("boundary", challenge.value),
                positive_commit_count_delta=(
                    1
                    if challenge
                    in {
                        BehavioralChallenge.MATCHED_CAUSAL_LINEAGE,
                        BehavioralChallenge.LINEAGE_SWAP,
                        BehavioralChallenge.WORLD_RELATION_PERMUTATION,
                        BehavioralChallenge.BOUNDED_AMBIGUITY,
                    }
                    else 0
                ),
            )
        )
    return tuple(rows)


def _candidate(**changes: object) -> BehavioralMechanismRun:
    base = BehavioralMechanismRun(
        mechanism_id="anonymous-candidate",
        outcomes=_outcomes(),
        persistent_state_units=16,
        state_size_bytes=2048,
        global_keyed_query_count=0,
        direct_keyed_target_query=False,
        uses_forbidden_privilege=False,
        explicit_predictor=False,
        p1_p4_contracts_passed=True,
    )
    return replace(base, **changes)


def _baseline(**changes: object) -> BehavioralMechanismRun:
    base = BehavioralMechanismRun(
        mechanism_id="smallest-explicit-baseline",
        outcomes=_outcomes(),
        persistent_state_units=8,
        state_size_bytes=1024,
        global_keyed_query_count=8,
        direct_keyed_target_query=True,
        uses_forbidden_privilege=False,
        explicit_predictor=True,
        claimed_minimal_explicit_predictor=True,
    )
    return replace(base, **changes)


def test_p5_matching_smaller_explicit_predictor_forces_explicit_classification() -> None:
    assessment = assess_behavioral_table_equivalence(_candidate(), _baseline())
    assert assessment.required_challenge_coverage_passed is True
    assert assessment.behavior_matches_explicit_baseline is True
    assert assessment.candidate_reduced_to_explicit_predictor is True
    assert assessment.classification == "behaviorally-explicit-table-equivalent"
    assert assessment.accepted_as_emergent_field_organization is False


def test_p5_difference_on_unseen_combination_falsifies_only_tested_table() -> None:
    assessment = assess_behavioral_table_equivalence(
        _candidate(outcomes=_outcomes(unseen_suffix="candidate-generalizes")),
        _baseline(outcomes=_outcomes(unseen_suffix="table-misses")),
    )
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.tested_baseline_falsified is True
    assert assessment.classification == (
        "tested-explicit-baseline-falsified-not-emergence-proof"
    )
    assert assessment.accepted_as_emergent_field_organization is False
    assert assessment.mismatched_challenges == (
        BehavioralChallenge.UNSEEN_LINEAGE_COMBINATION,
    )


def test_p5_fails_closed_when_required_interventions_are_missing() -> None:
    incomplete = _candidate(outcomes=_outcomes()[:-1])
    assessment = assess_behavioral_table_equivalence(incomplete, _baseline())
    assert assessment.required_challenge_coverage_passed is False
    assert assessment.classification == "insufficient-challenge-coverage"
    assert assessment.accepted_as_emergent_field_organization is False


def test_p5_rejects_privileged_candidate_even_when_behavior_matches() -> None:
    privileged = _candidate(uses_forbidden_privilege=True)
    assessment = assess_behavioral_table_equivalence(privileged, _baseline())
    assert assessment.candidate_uses_forbidden_privilege is True
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.classification == "forbidden-privileged-candidate"


def test_p3_p5_protocol_surface_contains_no_typed_reward_or_semantic_answer_key() -> None:
    lowered = str(
        {
            "state_loci": [locus.value for locus in StateLocus],
            "evidence": [source.value for source in ContinuationEvidence],
            "challenges": [challenge.value for challenge in BehavioralChallenge],
        }
    ).lower()
    for forbidden in (
        "assembly_id",
        "correct_action",
        "reward_value",
        "expected_answer",
        "semantic_role",
    ):
        assert forbidden not in lowered

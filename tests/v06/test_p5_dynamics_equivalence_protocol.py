from __future__ import annotations

from dataclasses import replace

from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import BehavioralChallenge
from sparkbrain.evaluation.v061_p5_dynamics_equivalence_protocol import (
    DynamicBehavioralOutcome,
    DynamicMechanismRun,
    UpdateLocus,
    assess_dynamic_table_equivalence,
)


def _outcomes(
    *,
    unseen_suffix: str = "same",
    latency_override: dict[BehavioralChallenge, int | None] | None = None,
    locus_override: dict[BehavioralChallenge, tuple[UpdateLocus, ...]] | None = None,
) -> tuple[DynamicBehavioralOutcome, ...]:
    latency_override = latency_override or {}
    locus_override = locus_override or {}
    rows: list[DynamicBehavioralOutcome] = []
    for challenge in BehavioralChallenge:
        suffix = (
            unseen_suffix
            if challenge is BehavioralChallenge.UNSEEN_LINEAGE_COMBINATION
            else "same"
        )
        positive = int(
            challenge
            in {
                BehavioralChallenge.MATCHED_CAUSAL_LINEAGE,
                BehavioralChallenge.LINEAGE_SWAP,
                BehavioralChallenge.WORLD_RELATION_PERMUTATION,
                BehavioralChallenge.BOUNDED_AMBIGUITY,
            }
        )
        rows.append(
            DynamicBehavioralOutcome(
                challenge=challenge,
                future_competition_signature=(challenge.value, suffix),
                boundary_signature=("boundary", challenge.value),
                positive_commit_count_delta=positive,
                competition_trace=(
                    ("co-maximal", challenge.value),
                    ("settled", challenge.value, suffix),
                ),
                ambiguity_cardinality_trace=(2, 2 if challenge is BehavioralChallenge.BOUNDED_AMBIGUITY else 1),
                external_effect_latency_steps=latency_override.get(
                    challenge,
                    1
                    if challenge
                    not in {
                        BehavioralChallenge.EXTERNAL_ABSENCE,
                        BehavioralChallenge.INTERNAL_REPLAY_ONLY,
                    }
                    else None,
                ),
                state_update_loci=locus_override.get(
                    challenge,
                    (UpdateLocus.LOCAL_TRANSITION,),
                ),
                state_update_count=positive,
                global_indexed_lookup_count_delta=0,
            )
        )
    return tuple(rows)


def _candidate(**changes: object) -> DynamicMechanismRun:
    base = DynamicMechanismRun(
        mechanism_id="anonymous-candidate",
        outcomes=_outcomes(),
        persistent_state_units=16,
        persistent_state_bytes=2048,
        transient_state_peak_units=8,
        global_keyed_query_count=0,
        direct_keyed_target_query=False,
        uses_forbidden_privilege=False,
        explicit_predictor=False,
        p1_p4_contracts_passed=True,
    )
    return replace(base, **changes)


def _baseline(**changes: object) -> DynamicMechanismRun:
    base = DynamicMechanismRun(
        mechanism_id="minimal-local-explicit-baseline",
        outcomes=_outcomes(),
        persistent_state_units=8,
        persistent_state_bytes=1024,
        transient_state_peak_units=4,
        global_keyed_query_count=0,
        direct_keyed_target_query=False,
        uses_forbidden_privilege=False,
        explicit_predictor=True,
        minimality_established=True,
    )
    return replace(base, **changes)


def test_full_endpoint_and_dynamics_match_reduces_candidate_to_explicit_memory() -> None:
    assessment = assess_dynamic_table_equivalence(_candidate(), _baseline())
    assert assessment.required_challenge_coverage_passed is True
    assert assessment.endpoint_behavior_matches is True
    assert assessment.temporal_state_signatures_match is True
    assert assessment.baseline_minimality_established is True
    assert assessment.baseline_not_larger_than_candidate is True
    assert assessment.baseline_not_more_lookup_privileged is True
    assert assessment.candidate_reduced_to_explicit_predictor is True
    assert assessment.classification == (
        "behaviorally-and-dynamically-explicit-memory-equivalent"
    )
    assert assessment.accepted_as_emergent_field_organization is False


def test_same_endpoints_with_different_external_effect_latency_is_not_equivalent() -> None:
    challenge = BehavioralChallenge.WORLD_RELATION_PERMUTATION
    candidate = _candidate(
        outcomes=_outcomes(latency_override={challenge: 3}),
    )
    assessment = assess_dynamic_table_equivalence(candidate, _baseline())
    assert assessment.endpoint_behavior_matches is True
    assert assessment.temporal_state_signatures_match is False
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.tested_explicit_baseline_falsified is True
    assert assessment.classification == "matching-endpoints-different-dynamics"
    assert assessment.dynamics_mismatches == (challenge,)
    assert assessment.accepted_as_emergent_field_organization is False


def test_same_endpoints_with_different_update_locus_is_not_equivalent() -> None:
    challenge = BehavioralChallenge.STATE_LOCUS_TRANSPLANT
    candidate = _candidate(
        outcomes=_outcomes(
            locus_override={challenge: (UpdateLocus.FIELD_STATE,)},
        )
    )
    assessment = assess_dynamic_table_equivalence(candidate, _baseline())
    assert assessment.endpoint_behavior_matches is True
    assert assessment.temporal_state_signatures_match is False
    assert assessment.dynamics_mismatches == (challenge,)
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.accepted_as_emergent_field_organization is False


def test_matching_global_lookup_table_is_not_structurally_equivalent_to_local_candidate() -> None:
    table = _baseline(
        global_keyed_query_count=8,
        direct_keyed_target_query=True,
    )
    assessment = assess_dynamic_table_equivalence(_candidate(), table)
    assert assessment.endpoint_behavior_matches is True
    assert assessment.temporal_state_signatures_match is True
    assert assessment.baseline_not_more_lookup_privileged is False
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.classification == (
        "matching-explicit-baseline-structurally-non-equivalent"
    )
    assert assessment.accepted_as_emergent_field_organization is False


def test_matching_baseline_without_established_minimality_fails_closed() -> None:
    assessment = assess_dynamic_table_equivalence(
        _candidate(),
        _baseline(minimality_established=False),
    )
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.classification == "matching-baseline-minimality-not-established"
    assert assessment.accepted_as_emergent_field_organization is False


def test_unseen_combination_difference_falsifies_only_the_tested_baseline() -> None:
    assessment = assess_dynamic_table_equivalence(
        _candidate(outcomes=_outcomes(unseen_suffix="candidate-generalizes")),
        _baseline(outcomes=_outcomes(unseen_suffix="table-misses")),
    )
    assert assessment.endpoint_behavior_matches is False
    assert assessment.tested_explicit_baseline_falsified is True
    assert assessment.classification == (
        "tested-explicit-baseline-falsified-not-emergence-proof"
    )
    assert assessment.endpoint_mismatches == (
        BehavioralChallenge.UNSEEN_LINEAGE_COMBINATION,
    )
    assert assessment.accepted_as_emergent_field_organization is False


def test_p5_refuses_to_classify_before_p1_p4_contracts_pass() -> None:
    assessment = assess_dynamic_table_equivalence(
        _candidate(p1_p4_contracts_passed=False),
        _baseline(),
    )
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.classification == "candidate-fails-prior-p1-p4-contracts"


def test_p5_rejects_forbidden_privilege_before_equivalence_claim() -> None:
    assessment = assess_dynamic_table_equivalence(
        _candidate(uses_forbidden_privilege=True),
        _baseline(),
    )
    assert assessment.candidate_uses_forbidden_privilege is True
    assert assessment.candidate_reduced_to_explicit_predictor is False
    assert assessment.classification == "forbidden-privileged-candidate"
    assert assessment.accepted_as_emergent_field_organization is False


def test_p5_fails_closed_on_missing_required_challenge() -> None:
    assessment = assess_dynamic_table_equivalence(
        _candidate(outcomes=_outcomes()[:-1]),
        _baseline(),
    )
    assert assessment.required_challenge_coverage_passed is False
    assert assessment.classification == "insufficient-challenge-coverage"
    assert assessment.accepted_as_emergent_field_organization is False

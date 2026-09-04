from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class StateLocus(StrEnum):
    LOCAL_TRANSITION = "local-transition"
    FIELD_STATE = "field-state"
    CONSISTENCY = "consistency"
    TRANSIENT_RETURN_ADDRESS = "transient-return-address"


@dataclass(frozen=True, slots=True)
class StateLocusSnapshot:
    local_transition_hash: str | None
    field_state_hash: str | None
    consistency_hash: str | None
    transient_return_address_hash: str | None

    def hash_for(self, locus: StateLocus) -> str | None:
        return {
            StateLocus.LOCAL_TRANSITION: self.local_transition_hash,
            StateLocus.FIELD_STATE: self.field_state_hash,
            StateLocus.CONSISTENCY: self.consistency_hash,
            StateLocus.TRANSIENT_RETURN_ADDRESS: self.transient_return_address_hash,
        }[locus]


@dataclass(frozen=True, slots=True)
class StateLocusCrossTransplantTrial:
    trial_id: str
    baseline_state: StateLocusSnapshot
    donor_state: StateLocusSnapshot
    transplanted_state: StateLocusSnapshot
    transplanted_loci: tuple[StateLocus, ...]
    selected_lineage_before: str
    selected_lineage_after: str
    donor_selected_lineage: str
    reentry_signature_before: tuple[str, ...]
    reentry_signature_after: tuple[str, ...]
    donor_reentry_signature: tuple[str, ...]

    def validate(self) -> None:
        if not self.trial_id:
            raise ValueError("trial_id must be non-empty")
        if not self.transplanted_loci:
            raise ValueError("at least one state locus must be transplanted")
        if len(set(self.transplanted_loci)) != len(self.transplanted_loci):
            raise ValueError("transplanted loci must be unique")
        if not all(
            (self.selected_lineage_before, self.selected_lineage_after, self.donor_selected_lineage)
        ):
            raise ValueError("lineage identities must be non-empty")

        transplanted = set(self.transplanted_loci)
        for locus in StateLocus:
            baseline_value = self.baseline_state.hash_for(locus)
            donor_value = self.donor_state.hash_for(locus)
            observed_value = self.transplanted_state.hash_for(locus)
            if locus in transplanted:
                if donor_value is None:
                    raise ValueError(
                        f"donor state unavailable for transplanted locus: {locus.value}"
                    )
                if donor_value == baseline_value:
                    raise ValueError(
                        f"donor and baseline must differ at transplanted locus: {locus.value}"
                    )
                if observed_value != donor_value:
                    raise ValueError(f"transplanted state must match donor at locus: {locus.value}")
            elif observed_value != baseline_value:
                raise ValueError(f"non-transplanted locus changed: {locus.value}")


@dataclass(frozen=True, slots=True)
class StateLocusCrossTransplantAssessment:
    trial_id: str
    transplanted_loci: tuple[StateLocus, ...]
    future_competition_changed: bool
    donor_competition_effect_transferred: bool
    relation_reentry_changed: bool
    donor_reentry_effect_transferred: bool
    local_transition_carries_competition: bool
    field_state_independently_carries_competition: bool
    consistency_independently_reaches_competition: bool
    transient_return_address_independently_carries_competition: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "transplanted_loci": tuple(locus.value for locus in self.transplanted_loci),
        }


def assess_state_locus_cross_transplant(
    trial: StateLocusCrossTransplantTrial,
) -> StateLocusCrossTransplantAssessment:
    trial.validate()
    loci = set(trial.transplanted_loci)
    competition_changed = trial.selected_lineage_after != trial.selected_lineage_before
    competition_transferred = (
        competition_changed and trial.selected_lineage_after == trial.donor_selected_lineage
    )
    reentry_changed = trial.reentry_signature_after != trial.reentry_signature_before
    reentry_transferred = (
        reentry_changed and trial.reentry_signature_after == trial.donor_reentry_signature
    )

    local_only = loci == {StateLocus.LOCAL_TRANSITION} and competition_transferred
    field_only = loci == {StateLocus.FIELD_STATE} and competition_transferred
    consistency_only = loci == {StateLocus.CONSISTENCY} and competition_transferred
    return_only = loci == {StateLocus.TRANSIENT_RETURN_ADDRESS} and competition_transferred

    if field_only:
        interpretation = "field_state_alone_transfers_future_competition"
    elif consistency_only:
        interpretation = "consistency_state_alone_reaches_future_competition"
    elif return_only:
        interpretation = "transient_return_address_alone_transfers_future_competition"
    elif local_only:
        interpretation = "explicit_local_transition_state_transfers_future_competition"
    elif competition_transferred:
        interpretation = "competition_transfer_requires_joint_state_loci"
    elif reentry_transferred:
        interpretation = "transplant_changes_downstream_reentry_without_upstream_competition"
    else:
        interpretation = "transplanted_state_does_not_transfer_donor_behavior"

    return StateLocusCrossTransplantAssessment(
        trial_id=trial.trial_id,
        transplanted_loci=trial.transplanted_loci,
        future_competition_changed=competition_changed,
        donor_competition_effect_transferred=competition_transferred,
        relation_reentry_changed=reentry_changed,
        donor_reentry_effect_transferred=reentry_transferred,
        local_transition_carries_competition=local_only,
        field_state_independently_carries_competition=field_only,
        consistency_independently_reaches_competition=consistency_only,
        transient_return_address_independently_carries_competition=return_only,
        interpretation=interpretation,
    )


class ContinuationEvidence(StrEnum):
    EXTERNAL_MATCH = "external-match"
    EXTERNAL_CONTRADICTION = "external-contradiction"
    EXTERNAL_ABSENCE = "external-absence"
    INTERNAL_REPLAY_ONLY = "internal-replay-only"


@dataclass(frozen=True, slots=True)
class AmbiguityContinuationTrial:
    trial_id: str
    candidate_lineages: tuple[str, ...]
    initial_competition_strengths: tuple[float, ...]
    early_active_lineages: tuple[str, ...]
    evidence_source: ContinuationEvidence
    causal_lineage: str
    later_competition_strengths: tuple[float, ...]
    later_active_lineages: tuple[str, ...]
    external_observation_count_delta: int
    positive_commit_count_delta: int
    maximum_active_lineages: int = 4

    def validate(self) -> None:
        if not self.trial_id:
            raise ValueError("trial_id must be non-empty")
        if len(self.candidate_lineages) < 2:
            raise ValueError("P4 requires at least two co-maximal candidate lineages")
        if len(set(self.candidate_lineages)) != len(self.candidate_lineages):
            raise ValueError("candidate lineage identities must be unique")
        if self.causal_lineage not in self.candidate_lineages:
            raise ValueError("causal_lineage must be one of the candidate lineages")
        if len(self.initial_competition_strengths) != len(self.candidate_lineages):
            raise ValueError("initial strengths must match candidate count")
        if len(self.later_competition_strengths) != len(self.candidate_lineages):
            raise ValueError("later strengths must match candidate count")
        if any(
            not math.isfinite(value)
            for value in (*self.initial_competition_strengths, *self.later_competition_strengths)
        ):
            raise ValueError("competition strengths must be finite")
        if len(set(self.initial_competition_strengths)) != 1:
            raise ValueError("P4 requires genuinely co-maximal initial strengths")
        if self.maximum_active_lineages < 2:
            raise ValueError("maximum_active_lineages must permit initial plurality")
        if not set(self.early_active_lineages).issubset(self.candidate_lineages):
            raise ValueError("early active lineages must be candidate lineages")
        if not set(self.later_active_lineages).issubset(self.candidate_lineages):
            raise ValueError("later active lineages must be candidate lineages")
        if self.external_observation_count_delta < 0:
            raise ValueError("external observation delta must be non-negative")
        if self.positive_commit_count_delta < 0:
            raise ValueError("positive commit delta must be non-negative")


@dataclass(frozen=True, slots=True)
class AmbiguityContinuationAssessment:
    trial_id: str
    initial_plurality_preserved: bool
    initial_plurality_bounded: bool
    premature_singleton_avoided: bool
    later_plurality_bounded: bool
    external_evidence_contract_passed: bool
    causal_history_changes_later_competition: bool
    contradiction_corrects_causal_lineage: bool
    self_confirmation_guard_passed: bool
    accepted: bool
    reason: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_ambiguity_continuation(
    trial: AmbiguityContinuationTrial,
    *,
    minimum_differentiation: float = 0.5,
) -> AmbiguityContinuationAssessment:
    trial.validate()
    if minimum_differentiation <= 0.0:
        raise ValueError("minimum_differentiation must be positive")

    candidate_set = set(trial.candidate_lineages)
    early_set = set(trial.early_active_lineages)
    initial_plurality = early_set == candidate_set
    initial_bounded = 1 < len(early_set) <= trial.maximum_active_lineages
    no_early_singleton = len(early_set) > 1
    later_bounded = 1 <= len(set(trial.later_active_lineages)) <= trial.maximum_active_lineages

    external_expected = trial.evidence_source in {
        ContinuationEvidence.EXTERNAL_MATCH,
        ContinuationEvidence.EXTERNAL_CONTRADICTION,
    }
    external_contract = (
        trial.external_observation_count_delta > 0
        if external_expected
        else trial.external_observation_count_delta == 0
    )
    self_confirmation_guard = not (
        trial.evidence_source is ContinuationEvidence.INTERNAL_REPLAY_ONLY
        and (
            trial.positive_commit_count_delta > 0
            or trial.later_competition_strengths != trial.initial_competition_strengths
        )
    )

    index = {
        lineage: position for position, lineage in enumerate(trial.candidate_lineages)
    }
    causal_position = index[trial.causal_lineage]
    causal_later = trial.later_competition_strengths[causal_position]
    other_later = tuple(
        value
        for position, value in enumerate(trial.later_competition_strengths)
        if position != causal_position
    )

    causal_differentiation = False
    corrective = False
    if trial.evidence_source is ContinuationEvidence.EXTERNAL_MATCH:
        causal_differentiation = all(
            causal_later - value >= minimum_differentiation for value in other_later
        )
    elif trial.evidence_source is ContinuationEvidence.EXTERNAL_CONTRADICTION:
        corrective = any(
            value - causal_later >= minimum_differentiation for value in other_later
        )
    else:
        causal_differentiation = (
            trial.later_competition_strengths == trial.initial_competition_strengths
            and trial.positive_commit_count_delta == 0
        )

    evidence_behavior_ok = (
        corrective
        if trial.evidence_source is ContinuationEvidence.EXTERNAL_CONTRADICTION
        else causal_differentiation
    )
    accepted = all(
        (
            initial_plurality,
            initial_bounded,
            no_early_singleton,
            later_bounded,
            external_contract,
            self_confirmation_guard,
            evidence_behavior_ok,
        )
    )

    if not initial_plurality or not no_early_singleton:
        reason = "premature_singleton_or_missing_initial_plurality"
    elif not initial_bounded or not later_bounded:
        reason = "ambiguity_unbounded"
    elif not external_contract:
        reason = "external_evidence_contract_failed"
    elif not self_confirmation_guard:
        reason = "self_confirmation_violation"
    elif (
        trial.evidence_source is ContinuationEvidence.EXTERNAL_CONTRADICTION
        and not corrective
    ):
        reason = "contradiction_did_not_correct_causal_lineage"
    elif not causal_differentiation:
        reason = "later_external_evidence_did_not_change_competition"
    else:
        reason = "accepted"

    return AmbiguityContinuationAssessment(
        trial_id=trial.trial_id,
        initial_plurality_preserved=initial_plurality,
        initial_plurality_bounded=initial_bounded,
        premature_singleton_avoided=no_early_singleton,
        later_plurality_bounded=later_bounded,
        external_evidence_contract_passed=external_contract,
        causal_history_changes_later_competition=(
            causal_differentiation
            if trial.evidence_source is ContinuationEvidence.EXTERNAL_MATCH
            else corrective
        ),
        contradiction_corrects_causal_lineage=corrective,
        self_confirmation_guard_passed=self_confirmation_guard,
        accepted=accepted,
        reason=reason,
    )


class BehavioralChallenge(StrEnum):
    MATCHED_CAUSAL_LINEAGE = "matched-causal-lineage"
    LINEAGE_SWAP = "lineage-swap"
    EXTERNAL_CONTRADICTION = "external-contradiction"
    EXTERNAL_ABSENCE = "external-absence"
    INTERNAL_REPLAY_ONLY = "internal-replay-only"
    WORLD_RELATION_PERMUTATION = "world-relation-permutation"
    STATE_LOCUS_TRANSPLANT = "state-locus-transplant"
    BOUNDED_AMBIGUITY = "bounded-ambiguity"
    IDENTIFIER_PERMUTATION = "identifier-permutation"
    PHYSICAL_TRAJECTORY_SUBSTITUTION = "physical-trajectory-substitution"
    UNSEEN_LINEAGE_COMBINATION = "unseen-lineage-combination"


P5_REQUIRED_CHALLENGES = frozenset(BehavioralChallenge)


@dataclass(frozen=True, slots=True)
class BehavioralOutcome:
    challenge: BehavioralChallenge
    future_competition_signature: tuple[str, ...]
    boundary_signature: tuple[str, ...]
    positive_commit_count_delta: int

    def validate(self) -> None:
        if self.positive_commit_count_delta < 0:
            raise ValueError("positive commit delta must be non-negative")


@dataclass(frozen=True, slots=True)
class BehavioralMechanismRun:
    mechanism_id: str
    outcomes: tuple[BehavioralOutcome, ...]
    persistent_state_units: int
    state_size_bytes: int
    global_keyed_query_count: int
    direct_keyed_target_query: bool
    uses_forbidden_privilege: bool
    explicit_predictor: bool
    claimed_minimal_explicit_predictor: bool = False
    p1_p4_contracts_passed: bool = False

    def validate(self) -> None:
        if not self.mechanism_id:
            raise ValueError("mechanism_id must be non-empty")
        if self.persistent_state_units < 0 or self.state_size_bytes < 0:
            raise ValueError("state sizes must be non-negative")
        if self.global_keyed_query_count < 0:
            raise ValueError("global keyed query count must be non-negative")
        challenges = [outcome.challenge for outcome in self.outcomes]
        if len(set(challenges)) != len(challenges):
            raise ValueError("behavioral challenges must be unique per run")
        for outcome in self.outcomes:
            outcome.validate()

    def outcome_map(self) -> dict[BehavioralChallenge, BehavioralOutcome]:
        return {outcome.challenge: outcome for outcome in self.outcomes}


@dataclass(frozen=True, slots=True)
class BehavioralTableEquivalenceAssessment:
    candidate_mechanism_id: str
    baseline_mechanism_id: str
    required_challenge_coverage_passed: bool
    behavior_matches_explicit_baseline: bool
    baseline_is_minimal_explicit_predictor: bool
    baseline_not_larger_than_candidate: bool
    candidate_uses_forbidden_privilege: bool
    candidate_reduced_to_explicit_predictor: bool
    tested_baseline_falsified: bool
    accepted_as_emergent_field_organization: bool
    classification: str
    mismatched_challenges: tuple[BehavioralChallenge, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "mismatched_challenges": tuple(
                challenge.value for challenge in self.mismatched_challenges
            ),
        }


def assess_behavioral_table_equivalence(
    candidate: BehavioralMechanismRun,
    baseline: BehavioralMechanismRun,
) -> BehavioralTableEquivalenceAssessment:
    candidate.validate()
    baseline.validate()
    if not baseline.explicit_predictor:
        raise ValueError("P5 baseline must be an explicit predictor")

    candidate_map = candidate.outcome_map()
    baseline_map = baseline.outcome_map()
    candidate_coverage = set(candidate_map) == P5_REQUIRED_CHALLENGES
    baseline_coverage = set(baseline_map) == P5_REQUIRED_CHALLENGES
    coverage = candidate_coverage and baseline_coverage

    mismatches: list[BehavioralChallenge] = []
    if coverage:
        for challenge in BehavioralChallenge:
            if candidate_map[challenge] != baseline_map[challenge]:
                mismatches.append(challenge)

    behavior_match = coverage and not mismatches
    minimal_baseline = baseline.claimed_minimal_explicit_predictor
    baseline_not_larger = (
        baseline.persistent_state_units <= candidate.persistent_state_units
        and baseline.state_size_bytes <= candidate.state_size_bytes
    )
    reduced = all(
        (
            coverage,
            behavior_match,
            minimal_baseline,
            baseline_not_larger,
            not candidate.uses_forbidden_privilege,
        )
    )
    tested_baseline_falsified = all(
        (
            coverage,
            bool(mismatches),
            candidate.p1_p4_contracts_passed,
            not candidate.uses_forbidden_privilege,
        )
    )

    # P5 can classify reduction to an explicit predictor. Failure to reduce to
    # one tested table is not sufficient to prove emergent Field organization.
    accepted_as_emergent = False

    if candidate.uses_forbidden_privilege:
        classification = "forbidden-privileged-candidate"
    elif not coverage:
        classification = "insufficient-challenge-coverage"
    elif reduced:
        classification = "behaviorally-explicit-table-equivalent"
    elif behavior_match and not minimal_baseline:
        classification = "matching-baseline-not-established-minimal"
    elif behavior_match and not baseline_not_larger:
        classification = "matching-explicit-baseline-is-larger-than-candidate"
    elif tested_baseline_falsified:
        classification = "tested-explicit-baseline-falsified-not-emergence-proof"
    else:
        classification = "behavioral-non-equivalence-inconclusive"

    return BehavioralTableEquivalenceAssessment(
        candidate_mechanism_id=candidate.mechanism_id,
        baseline_mechanism_id=baseline.mechanism_id,
        required_challenge_coverage_passed=coverage,
        behavior_matches_explicit_baseline=behavior_match,
        baseline_is_minimal_explicit_predictor=minimal_baseline,
        baseline_not_larger_than_candidate=baseline_not_larger,
        candidate_uses_forbidden_privilege=candidate.uses_forbidden_privilege,
        candidate_reduced_to_explicit_predictor=reduced,
        tested_baseline_falsified=tested_baseline_falsified,
        accepted_as_emergent_field_organization=accepted_as_emergent,
        classification=classification,
        mismatched_challenges=tuple(mismatches),
    )

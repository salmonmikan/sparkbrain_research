from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .v061_p3_p5_diagnostic_protocol import P5_REQUIRED_CHALLENGES, BehavioralChallenge


class UpdateLocus(StrEnum):
    LOCAL_TRANSITION = "local-transition"
    FIELD_STATE = "field-state"
    CONSISTENCY = "consistency"
    TRANSIENT_RETURN_ADDRESS = "transient-return-address"
    CENTRAL_TABLE = "central-table"


@dataclass(frozen=True, slots=True)
class DynamicBehavioralOutcome:
    challenge: BehavioralChallenge
    future_competition_signature: tuple[str, ...]
    boundary_signature: tuple[str, ...]
    positive_commit_count_delta: int
    competition_trace: tuple[tuple[str, ...], ...]
    ambiguity_cardinality_trace: tuple[int, ...]
    external_effect_latency_steps: int | None
    state_update_loci: tuple[UpdateLocus, ...]
    state_update_count: int
    global_indexed_lookup_count_delta: int

    def validate(self) -> None:
        if self.positive_commit_count_delta < 0:
            raise ValueError("positive commit delta must be non-negative")
        if not self.competition_trace:
            raise ValueError("competition trace must be non-empty")
        if not self.ambiguity_cardinality_trace:
            raise ValueError("ambiguity cardinality trace must be non-empty")
        if any(value < 0 for value in self.ambiguity_cardinality_trace):
            raise ValueError("ambiguity cardinality values must be non-negative")
        if (
            self.external_effect_latency_steps is not None
            and self.external_effect_latency_steps < 0
        ):
            raise ValueError("external effect latency must be non-negative")
        if len(set(self.state_update_loci)) != len(self.state_update_loci):
            raise ValueError("state update loci must be unique")
        if self.state_update_count < 0:
            raise ValueError("state update count must be non-negative")
        if self.global_indexed_lookup_count_delta < 0:
            raise ValueError("global indexed lookup delta must be non-negative")

    def endpoint_signature(self) -> tuple[Any, ...]:
        return (
            self.future_competition_signature,
            self.boundary_signature,
            self.positive_commit_count_delta,
        )

    def dynamics_signature(self) -> tuple[Any, ...]:
        return (
            self.competition_trace,
            self.ambiguity_cardinality_trace,
            self.external_effect_latency_steps,
            tuple(locus.value for locus in self.state_update_loci),
            self.state_update_count,
            self.global_indexed_lookup_count_delta,
        )


@dataclass(frozen=True, slots=True)
class DynamicMechanismRun:
    mechanism_id: str
    outcomes: tuple[DynamicBehavioralOutcome, ...]
    persistent_state_units: int
    persistent_state_bytes: int
    transient_state_peak_units: int
    global_keyed_query_count: int
    direct_keyed_target_query: bool
    uses_forbidden_privilege: bool
    explicit_predictor: bool
    minimality_established: bool = False
    p1_p4_contracts_passed: bool = False

    def validate(self) -> None:
        if not self.mechanism_id:
            raise ValueError("mechanism_id must be non-empty")
        if min(
            self.persistent_state_units,
            self.persistent_state_bytes,
            self.transient_state_peak_units,
            self.global_keyed_query_count,
        ) < 0:
            raise ValueError("state and query counts must be non-negative")
        challenges = [outcome.challenge for outcome in self.outcomes]
        if len(challenges) != len(set(challenges)):
            raise ValueError("behavioral challenges must be unique per run")
        for outcome in self.outcomes:
            outcome.validate()

    def outcome_map(self) -> dict[BehavioralChallenge, DynamicBehavioralOutcome]:
        return {outcome.challenge: outcome for outcome in self.outcomes}


@dataclass(frozen=True, slots=True)
class DynamicTableEquivalenceAssessment:
    candidate_mechanism_id: str
    baseline_mechanism_id: str
    required_challenge_coverage_passed: bool
    candidate_p1_p4_contracts_passed: bool
    endpoint_behavior_matches: bool
    temporal_state_signatures_match: bool
    baseline_minimality_established: bool
    baseline_not_larger_than_candidate: bool
    baseline_not_more_lookup_privileged: bool
    candidate_uses_forbidden_privilege: bool
    candidate_reduced_to_explicit_predictor: bool
    tested_explicit_baseline_falsified: bool
    accepted_as_emergent_field_organization: bool
    classification: str
    endpoint_mismatches: tuple[BehavioralChallenge, ...]
    dynamics_mismatches: tuple[BehavioralChallenge, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "endpoint_mismatches": tuple(row.value for row in self.endpoint_mismatches),
            "dynamics_mismatches": tuple(row.value for row in self.dynamics_mismatches),
        }


def assess_dynamic_table_equivalence(
    candidate: DynamicMechanismRun,
    baseline: DynamicMechanismRun,
) -> DynamicTableEquivalenceAssessment:
    """Fail-closed P5 comparison of endpoints, temporal response and state-update structure.

    This evaluator may classify a candidate as reducible to an explicit predictor. It never
    establishes emergent Field organization merely because one explicit baseline fails.
    """

    candidate.validate()
    baseline.validate()
    if not baseline.explicit_predictor:
        raise ValueError("P5 baseline must be an explicit predictor")

    candidate_map = candidate.outcome_map()
    baseline_map = baseline.outcome_map()
    coverage = (
        set(candidate_map) == P5_REQUIRED_CHALLENGES
        and set(baseline_map) == P5_REQUIRED_CHALLENGES
    )

    endpoint_mismatches: list[BehavioralChallenge] = []
    dynamics_mismatches: list[BehavioralChallenge] = []
    if coverage:
        for challenge in BehavioralChallenge:
            candidate_outcome = candidate_map[challenge]
            baseline_outcome = baseline_map[challenge]
            if candidate_outcome.endpoint_signature() != baseline_outcome.endpoint_signature():
                endpoint_mismatches.append(challenge)
            if candidate_outcome.dynamics_signature() != baseline_outcome.dynamics_signature():
                dynamics_mismatches.append(challenge)

    endpoint_match = coverage and not endpoint_mismatches
    dynamics_match = coverage and not dynamics_mismatches
    baseline_not_larger = (
        baseline.persistent_state_units <= candidate.persistent_state_units
        and baseline.persistent_state_bytes <= candidate.persistent_state_bytes
        and baseline.transient_state_peak_units <= candidate.transient_state_peak_units
    )
    baseline_not_more_lookup_privileged = (
        not baseline.uses_forbidden_privilege
        and baseline.global_keyed_query_count <= candidate.global_keyed_query_count
        and not (
            baseline.direct_keyed_target_query
            and not candidate.direct_keyed_target_query
        )
    )

    reduced = all(
        (
            coverage,
            candidate.p1_p4_contracts_passed,
            endpoint_match,
            dynamics_match,
            baseline.minimality_established,
            baseline_not_larger,
            baseline_not_more_lookup_privileged,
            not candidate.uses_forbidden_privilege,
        )
    )
    tested_baseline_falsified = all(
        (
            coverage,
            candidate.p1_p4_contracts_passed,
            bool(endpoint_mismatches or dynamics_mismatches),
            not candidate.uses_forbidden_privilege,
        )
    )

    # Non-equivalence to one explicit baseline is only a falsification of that baseline.
    # It is never positive proof of emergent Field organization.
    accepted_as_emergent = False

    if candidate.uses_forbidden_privilege:
        classification = "forbidden-privileged-candidate"
    elif not coverage:
        classification = "insufficient-challenge-coverage"
    elif not candidate.p1_p4_contracts_passed:
        classification = "candidate-fails-prior-p1-p4-contracts"
    elif endpoint_match and dynamics_match and not baseline.minimality_established:
        classification = "matching-baseline-minimality-not-established"
    elif endpoint_match and dynamics_match and (
        not baseline_not_larger or not baseline_not_more_lookup_privileged
    ):
        classification = "matching-explicit-baseline-structurally-non-equivalent"
    elif reduced:
        classification = "behaviorally-and-dynamically-explicit-memory-equivalent"
    elif endpoint_match and not dynamics_match:
        classification = "matching-endpoints-different-dynamics"
    elif tested_baseline_falsified:
        classification = "tested-explicit-baseline-falsified-not-emergence-proof"
    else:
        classification = "dynamic-equivalence-inconclusive"

    return DynamicTableEquivalenceAssessment(
        candidate_mechanism_id=candidate.mechanism_id,
        baseline_mechanism_id=baseline.mechanism_id,
        required_challenge_coverage_passed=coverage,
        candidate_p1_p4_contracts_passed=candidate.p1_p4_contracts_passed,
        endpoint_behavior_matches=endpoint_match,
        temporal_state_signatures_match=dynamics_match,
        baseline_minimality_established=baseline.minimality_established,
        baseline_not_larger_than_candidate=baseline_not_larger,
        baseline_not_more_lookup_privileged=baseline_not_more_lookup_privileged,
        candidate_uses_forbidden_privilege=candidate.uses_forbidden_privilege,
        candidate_reduced_to_explicit_predictor=reduced,
        tested_explicit_baseline_falsified=tested_baseline_falsified,
        accepted_as_emergent_field_organization=accepted_as_emergent,
        classification=classification,
        endpoint_mismatches=tuple(endpoint_mismatches),
        dynamics_mismatches=tuple(dynamics_mismatches),
    )

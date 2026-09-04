from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.evaluation.v061_anonymous_credit_diagnostic_protocol import (
    CausalCreditObservation,
)
from sparkbrain.v06.foundation import RuntimePulse, digest

from .credit_bridge import A01LocalTemporalExpectation


@dataclass(frozen=True, slots=True)
class A01PathSupportSnapshot:
    path_scores: tuple[tuple[str, int], ...]

    def score(self, path_id: str) -> int:
        for candidate, value in self.path_scores:
            if candidate == path_id:
                return value
        return 0

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def capture_path_support(
    expectation: A01LocalTemporalExpectation,
    path_ids: tuple[str, ...],
) -> A01PathSupportSnapshot:
    unique = tuple(dict.fromkeys(path_ids))
    if len(unique) != len(path_ids):
        raise ValueError("A01 support snapshot path IDs must be unique")
    rows = []
    for path_id in sorted(unique):
        support = expectation.causal_support(path_id)
        score = support.external_consistent_count - support.external_contradicted_count
        rows.append((path_id, score))
    return A01PathSupportSnapshot(path_scores=tuple(rows))


def build_p1_observation(
    *,
    trial_id: str,
    causal_path_id: str,
    matched_path_id: str,
    before: A01PathSupportSnapshot,
    after: A01PathSupportSnapshot,
    external_observation_count_delta: int,
    positive_commit_count_delta: int,
) -> CausalCreditObservation:
    if causal_path_id == matched_path_id:
        raise ValueError("P1 causal and matched A01 paths must be distinct")
    return CausalCreditObservation(
        trial_id=trial_id,
        causal_lineage_update=float(
            after.score(causal_path_id) - before.score(causal_path_id)
        ),
        matched_lineage_update=float(
            after.score(matched_path_id) - before.score(matched_path_id)
        ),
        external_observation_count_delta=external_observation_count_delta,
        positive_commit_count_delta=positive_commit_count_delta,
    )


def base_temporal_learned_state_hash(
    expectation: A01LocalTemporalExpectation,
) -> str:
    value = expectation.learned_state_dict()
    value.pop("a01_causal_support", None)
    return digest(value)


def causal_support_state_hash(
    expectation: A01LocalTemporalExpectation,
) -> str:
    support = expectation.learned_state_dict().get("a01_causal_support", {})
    return digest({"a01_causal_support": support})


def competition_signature(
    expectation: A01LocalTemporalExpectation,
    source: RuntimePulse,
    *,
    origin_state_hash: str,
) -> tuple[tuple[str, float], ...]:
    return tuple(
        sorted(
            (
                (proposal.target, proposal.confidence)
                for proposal in expectation.proposals_for(
                    source,
                    origin_state_hash=origin_state_hash,
                )
            ),
            key=lambda row: row[0],
        )
    )


@dataclass(frozen=True, slots=True)
class A01WorldRelationPermutationTrial:
    trial_id: str
    base_temporal_hash_before: str
    base_temporal_hash_after: str
    causal_support_hash_before: str
    causal_support_hash_after: str
    world_relation_before: str
    world_relation_after: str
    competition_signature_before: tuple[tuple[str, float], ...]
    competition_signature_after: tuple[tuple[str, float], ...]
    external_observation_count_delta: int

    def validate(self) -> None:
        if not self.trial_id:
            raise ValueError("trial_id must be non-empty")
        if self.base_temporal_hash_before != self.base_temporal_hash_after:
            raise ValueError("A01 P2 requires fixed base local temporal learned state")
        if self.world_relation_before == self.world_relation_after:
            raise ValueError("A01 P2 requires a world-relation permutation")
        if self.external_observation_count_delta < 1:
            raise ValueError("A01 P2 requires new external evidence")


@dataclass(frozen=True, slots=True)
class A01WorldRelationPermutationAssessment:
    trial_id: str
    base_temporal_state_fixed: bool
    world_relation_changed: bool
    causal_support_changed: bool
    future_competition_changed: bool
    world_to_transition_circulation_observed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_a01_world_relation_permutation(
    trial: A01WorldRelationPermutationTrial,
) -> A01WorldRelationPermutationAssessment:
    trial.validate()
    support_changed = trial.causal_support_hash_before != trial.causal_support_hash_after
    competition_changed = (
        trial.competition_signature_before != trial.competition_signature_after
    )
    circulation = support_changed and competition_changed
    return A01WorldRelationPermutationAssessment(
        trial_id=trial.trial_id,
        base_temporal_state_fixed=True,
        world_relation_changed=True,
        causal_support_changed=support_changed,
        future_competition_changed=competition_changed,
        world_to_transition_circulation_observed=circulation,
    )

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class EvidenceSource(StrEnum):
    EXTERNAL_MATCH = "external-match"
    EXTERNAL_CONTRADICTION = "external-contradiction"
    EXTERNAL_ABSENCE = "external-absence"
    INTERNAL_REPLAY_ONLY = "internal-replay-only"


@dataclass(frozen=True, slots=True)
class MatchedLineageProfile:
    lineage_id: str
    event_count: int
    event_times_ms: tuple[float, ...]
    effective_currents: tuple[float, ...]
    energy_costs: tuple[float, ...]

    def validate(self) -> None:
        if not self.lineage_id:
            raise ValueError("lineage_id must be non-empty")
        if self.event_count < 1:
            raise ValueError("event_count must be positive")
        if not (
            len(self.event_times_ms)
            == len(self.effective_currents)
            == len(self.energy_costs)
            == self.event_count
        ):
            raise ValueError("lineage profile vectors must match event_count")
        if any(
            not math.isfinite(value)
            for values in (
                self.event_times_ms,
                self.effective_currents,
                self.energy_costs,
            )
            for value in values
        ):
            raise ValueError("lineage profile values must be finite")
        if any(value < 0.0 for value in self.energy_costs):
            raise ValueError("energy costs must be non-negative")

    def matching_signature(self) -> tuple[Any, ...]:
        return (
            self.event_count,
            self.event_times_ms,
            self.effective_currents,
            self.energy_costs,
        )


@dataclass(frozen=True, slots=True)
class CausalCreditTrial:
    trial_id: str
    causal_lineage: MatchedLineageProfile
    matched_lineage: MatchedLineageProfile
    evidence_source: EvidenceSource
    expected_external_target: str | None
    observed_external_target: str | None

    def validate(self) -> None:
        if not self.trial_id:
            raise ValueError("trial_id must be non-empty")
        self.causal_lineage.validate()
        self.matched_lineage.validate()
        if self.causal_lineage.lineage_id == self.matched_lineage.lineage_id:
            raise ValueError("causal and matched lineages must be distinct")
        if self.causal_lineage.matching_signature() != self.matched_lineage.matching_signature():
            raise ValueError("causal and matched lineage resources must be identical")
        if self.evidence_source is EvidenceSource.EXTERNAL_MATCH:
            if (
                self.expected_external_target is None
                or self.observed_external_target != self.expected_external_target
            ):
                raise ValueError("external-match requires identical expected/observed target")
        elif self.evidence_source is EvidenceSource.EXTERNAL_CONTRADICTION:
            if (
                self.expected_external_target is None
                or self.observed_external_target is None
                or self.observed_external_target == self.expected_external_target
            ):
                raise ValueError("external-contradiction requires different targets")
        else:
            if self.observed_external_target is not None:
                raise ValueError("absence/internal-only trials have no external target")

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "evidence_source": self.evidence_source.value,
        }


@dataclass(frozen=True, slots=True)
class CausalCreditObservation:
    trial_id: str
    causal_lineage_update: float
    matched_lineage_update: float
    external_observation_count_delta: int
    positive_commit_count_delta: int

    def validate(self) -> None:
        if not self.trial_id:
            raise ValueError("trial_id must be non-empty")
        if not math.isfinite(self.causal_lineage_update):
            raise ValueError("causal update must be finite")
        if not math.isfinite(self.matched_lineage_update):
            raise ValueError("matched update must be finite")
        if self.external_observation_count_delta < 0:
            raise ValueError("external observation delta must be non-negative")
        if self.positive_commit_count_delta < 0:
            raise ValueError("positive commit delta must be non-negative")


@dataclass(frozen=True, slots=True)
class CausalCreditAssessment:
    trial_id: str
    evidence_source: EvidenceSource
    matched_resource_contract_passed: bool
    external_evidence_contract_passed: bool
    self_confirmation_guard_passed: bool
    causal_selective_update: bool
    contradiction_corrective_update: bool
    accepted: bool
    reason: str

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "evidence_source": self.evidence_source.value,
        }


def assess_causal_credit_trial(
    trial: CausalCreditTrial,
    observation: CausalCreditObservation,
    *,
    minimum_selective_effect: float = 0.5,
) -> CausalCreditAssessment:
    """Evaluate a future mechanism without prescribing how it stores credit."""

    trial.validate()
    observation.validate()
    if observation.trial_id != trial.trial_id:
        raise ValueError("trial/observation identity mismatch")
    if minimum_selective_effect <= 0.0:
        raise ValueError("minimum_selective_effect must be positive")

    matched_resources = (
        trial.causal_lineage.matching_signature() == trial.matched_lineage.matching_signature()
    )
    has_external = trial.evidence_source in {
        EvidenceSource.EXTERNAL_MATCH,
        EvidenceSource.EXTERNAL_CONTRADICTION,
    }
    external_contract = (
        observation.external_observation_count_delta > 0
        if has_external
        else observation.external_observation_count_delta == 0
    )
    self_confirmation_guard = not (
        trial.evidence_source is EvidenceSource.INTERNAL_REPLAY_ONLY
        and (
            observation.positive_commit_count_delta > 0
            or observation.causal_lineage_update > 0.0
            or observation.matched_lineage_update > 0.0
        )
    )

    selective = False
    corrective = False
    if trial.evidence_source is EvidenceSource.EXTERNAL_MATCH:
        selective = (
            observation.causal_lineage_update - observation.matched_lineage_update
            >= minimum_selective_effect
            and observation.positive_commit_count_delta > 0
        )
    elif trial.evidence_source is EvidenceSource.EXTERNAL_CONTRADICTION:
        corrective = (
            observation.causal_lineage_update <= -minimum_selective_effect
            and abs(observation.matched_lineage_update) < minimum_selective_effect
        )
    elif trial.evidence_source in {
        EvidenceSource.EXTERNAL_ABSENCE,
        EvidenceSource.INTERNAL_REPLAY_ONLY,
    }:
        selective = (
            observation.causal_lineage_update == 0.0
            and observation.matched_lineage_update == 0.0
            and observation.positive_commit_count_delta == 0
        )

    accepted = all(
        (
            matched_resources,
            external_contract,
            self_confirmation_guard,
            corrective
            if trial.evidence_source is EvidenceSource.EXTERNAL_CONTRADICTION
            else selective,
        )
    )
    if not matched_resources:
        reason = "resource_mismatch"
    elif not external_contract:
        reason = "external_evidence_contract_failed"
    elif not self_confirmation_guard:
        reason = "self_confirmation_violation"
    elif trial.evidence_source is EvidenceSource.EXTERNAL_CONTRADICTION and not corrective:
        reason = "contradiction_not_lineage_selective"
    elif not selective:
        reason = "causal_lineage_not_selective"
    else:
        reason = "accepted"
    return CausalCreditAssessment(
        trial_id=trial.trial_id,
        evidence_source=trial.evidence_source,
        matched_resource_contract_passed=matched_resources,
        external_evidence_contract_passed=external_contract,
        self_confirmation_guard_passed=self_confirmation_guard,
        causal_selective_update=selective,
        contradiction_corrective_update=corrective,
        accepted=accepted,
        reason=reason,
    )


@dataclass(frozen=True, slots=True)
class WorldRelationPermutationTrial:
    trial_id: str
    local_state_hash_before: str
    local_state_hash_after: str
    world_relation_before: str
    world_relation_after: str
    selected_lineage_before: str
    selected_lineage_after: str

    def validate(self) -> None:
        if not self.trial_id:
            raise ValueError("trial_id must be non-empty")
        if self.local_state_hash_before != self.local_state_hash_after:
            raise ValueError("P2 requires fixed local transition state")
        if self.world_relation_before == self.world_relation_after:
            raise ValueError("P2 requires an anonymous world-relation permutation")


@dataclass(frozen=True, slots=True)
class WorldRelationPermutationAssessment:
    trial_id: str
    local_state_fixed: bool
    world_relation_changed: bool
    future_competition_changed: bool
    world_to_transition_circulation_observed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_world_relation_permutation(
    trial: WorldRelationPermutationTrial,
) -> WorldRelationPermutationAssessment:
    trial.validate()
    competition_changed = trial.selected_lineage_before != trial.selected_lineage_after
    return WorldRelationPermutationAssessment(
        trial_id=trial.trial_id,
        local_state_fixed=True,
        world_relation_changed=True,
        future_competition_changed=competition_changed,
        world_to_transition_circulation_observed=competition_changed,
    )


def canonical_matched_profile(lineage_id: str) -> MatchedLineageProfile:
    return MatchedLineageProfile(
        lineage_id=lineage_id,
        event_count=3,
        event_times_ms=(5.0, 10.0, 15.0),
        effective_currents=(0.6, 0.6, 0.6),
        energy_costs=(0.1, 0.1, 0.1),
    )


def build_causal_credit_protocol_matrix() -> tuple[CausalCreditTrial, ...]:
    causal_a = canonical_matched_profile("lineage-a")
    matched_b = canonical_matched_profile("lineage-b")
    causal_b = canonical_matched_profile("lineage-b")
    matched_a = canonical_matched_profile("lineage-a")
    return (
        CausalCreditTrial(
            trial_id="external-match-a",
            causal_lineage=causal_a,
            matched_lineage=matched_b,
            evidence_source=EvidenceSource.EXTERNAL_MATCH,
            expected_external_target="external:1",
            observed_external_target="external:1",
        ),
        CausalCreditTrial(
            trial_id="external-match-b-lineage-swap",
            causal_lineage=causal_b,
            matched_lineage=matched_a,
            evidence_source=EvidenceSource.EXTERNAL_MATCH,
            expected_external_target="external:1",
            observed_external_target="external:1",
        ),
        CausalCreditTrial(
            trial_id="external-contradiction-a",
            causal_lineage=causal_a,
            matched_lineage=matched_b,
            evidence_source=EvidenceSource.EXTERNAL_CONTRADICTION,
            expected_external_target="external:1",
            observed_external_target="external:2",
        ),
        CausalCreditTrial(
            trial_id="external-absence-a",
            causal_lineage=causal_a,
            matched_lineage=matched_b,
            evidence_source=EvidenceSource.EXTERNAL_ABSENCE,
            expected_external_target="external:1",
            observed_external_target=None,
        ),
        CausalCreditTrial(
            trial_id="internal-replay-only-a",
            causal_lineage=causal_a,
            matched_lineage=matched_b,
            evidence_source=EvidenceSource.INTERNAL_REPLAY_ONLY,
            expected_external_target="external:1",
            observed_external_target=None,
        ),
    )

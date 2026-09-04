from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .v061_p3_p5_diagnostic_protocol import StateLocus


class MechanismFamily(StrEnum):
    TRANSIENT_RETURN_ADDRESS = "transient-return-address"
    DISTRIBUTED_FIELD_TRACE = "distributed-field-trace"
    JOINT_RETURN_AND_LOCAL_FIELD_UPDATE = "joint-return-and-local-field-update"


REQUIRED_NEGATIVE_COMPLETION_FAMILIES = frozenset(MechanismFamily)


@dataclass(frozen=True, slots=True)
class PreMechanismProposal:
    proposal_id: str
    mechanism_family: MechanismFamily
    lineage_swap_test_declared: bool
    external_confirmation_only_positive: bool
    contradiction_correction_declared: bool
    future_local_competition_effect_declared: bool
    bounded_ambiguity_declared: bool
    uses_forbidden_privilege: bool
    expected_p3_carrier_loci: tuple[StateLocus, ...]
    explicit_null_declared: bool
    recurrent_null_declared: bool
    negative_stop_observation_declared: bool

    def validate(self) -> None:
        if not self.proposal_id:
            raise ValueError("proposal_id must be non-empty")
        if len(set(self.expected_p3_carrier_loci)) != len(
            self.expected_p3_carrier_loci
        ):
            raise ValueError("expected P3 carrier loci must be unique")


@dataclass(frozen=True, slots=True)
class PreMechanismAdmissionAssessment:
    proposal_id: str
    mechanism_family: MechanismFamily
    admitted_for_implementation: bool
    missing_requirements: tuple[str, ...]
    classification: str

    def state_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["mechanism_family"] = self.mechanism_family.value
        return payload


def assess_premechanism_admission(
    proposal: PreMechanismProposal,
) -> PreMechanismAdmissionAssessment:
    proposal.validate()
    requirements = (
        ("lineage-swap-test", proposal.lineage_swap_test_declared),
        (
            "external-confirmation-only-positive-update",
            proposal.external_confirmation_only_positive,
        ),
        ("contradiction-correction", proposal.contradiction_correction_declared),
        (
            "future-local-competition-effect",
            proposal.future_local_competition_effect_declared,
        ),
        ("bounded-ambiguity", proposal.bounded_ambiguity_declared),
        ("p3-carrier-locus", bool(proposal.expected_p3_carrier_loci)),
        ("explicit-null", proposal.explicit_null_declared),
        ("recurrent-null", proposal.recurrent_null_declared),
        ("negative-stop-observation", proposal.negative_stop_observation_declared),
    )
    missing = tuple(name for name, satisfied in requirements if not satisfied)
    if proposal.uses_forbidden_privilege:
        missing = (*missing, "no-forbidden-privilege")

    admitted = not missing
    classification = (
        "admitted-for-discriminator-first-implementation"
        if admitted
        else "premechanism-contract-incomplete"
    )
    return PreMechanismAdmissionAssessment(
        proposal_id=proposal.proposal_id,
        mechanism_family=proposal.mechanism_family,
        admitted_for_implementation=admitted,
        missing_requirements=missing,
        classification=classification,
    )


@dataclass(frozen=True, slots=True)
class CandidateDisposition:
    candidate_id: str
    mechanism_family: MechanismFamily
    non_privileged: bool
    p1_passed: bool
    p2_passed: bool
    p3_passed: bool
    p4_passed: bool
    p5_assessed: bool
    p5_reduced_to_explicit_memory: bool

    def validate(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")
        if self.p5_reduced_to_explicit_memory and not self.p5_assessed:
            raise ValueError("P5 reduction cannot be true before P5 assessment")

    @property
    def survives_p1_p4(self) -> bool:
        return all(
            (
                self.non_privileged,
                self.p1_passed,
                self.p2_passed,
                self.p3_passed,
                self.p4_passed,
            )
        )


@dataclass(frozen=True, slots=True)
class NegativeCompletionProgramme:
    candidate_programme_complete: bool
    completed_families: tuple[MechanismFamily, ...]
    dispositions: tuple[CandidateDisposition, ...]

    def validate(self) -> None:
        candidate_ids = [row.candidate_id for row in self.dispositions]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate IDs must be unique")
        if len(set(self.completed_families)) != len(self.completed_families):
            raise ValueError("completed mechanism families must be unique")
        for disposition in self.dispositions:
            disposition.validate()
        if self.candidate_programme_complete and not self.dispositions:
            raise ValueError("a complete candidate programme must contain dispositions")


@dataclass(frozen=True, slots=True)
class NegativeCompletionAssessment:
    candidate_programme_complete: bool
    required_family_coverage_passed: bool
    completed_families: tuple[MechanismFamily, ...]
    candidate_count: int
    p1_p4_survivor_ids: tuple[str, ...]
    all_survivors_p5_assessed: bool
    all_survivors_reduced_to_explicit_memory: bool
    stop_stronger_field_claim: bool
    classification: str

    def state_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["completed_families"] = tuple(
            family.value for family in self.completed_families
        )
        return payload


def assess_negative_completion(
    programme: NegativeCompletionProgramme,
) -> NegativeCompletionAssessment:
    programme.validate()
    family_coverage = (
        set(programme.completed_families) == REQUIRED_NEGATIVE_COMPLETION_FAMILIES
    )
    survivors = tuple(row for row in programme.dispositions if row.survives_p1_p4)
    survivor_ids = tuple(row.candidate_id for row in survivors)
    all_p5_assessed = bool(survivors) and all(row.p5_assessed for row in survivors)
    all_reduced = all_p5_assessed and all(
        row.p5_reduced_to_explicit_memory for row in survivors
    )

    stop = False
    if not programme.candidate_programme_complete:
        classification = "programme-incomplete"
    elif not family_coverage:
        classification = "mechanism-family-coverage-incomplete"
    elif not survivors:
        stop = True
        classification = "negative-completion-no-p1-p4-survivor"
    elif not all_p5_assessed:
        classification = "p5-incomplete-for-survivors"
    elif all_reduced:
        stop = True
        classification = "negative-completion-all-survivors-explicit-memory-reducible"
    else:
        classification = "stronger-field-claim-remains-open"

    return NegativeCompletionAssessment(
        candidate_programme_complete=programme.candidate_programme_complete,
        required_family_coverage_passed=family_coverage,
        completed_families=programme.completed_families,
        candidate_count=len(programme.dispositions),
        p1_p4_survivor_ids=survivor_ids,
        all_survivors_p5_assessed=all_p5_assessed,
        all_survivors_reduced_to_explicit_memory=all_reduced,
        stop_stronger_field_claim=stop,
        classification=classification,
    )

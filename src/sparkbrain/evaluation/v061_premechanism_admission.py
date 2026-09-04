from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from enum import StrEnum
from typing import Any

from .v061_p3_p5_diagnostic_protocol import StateLocus


class MechanismFamily(StrEnum):
    TRANSIENT_RETURN_ADDRESS = "transient-return-address"
    DISTRIBUTED_FIELD_TRACE = "distributed-field-trace"
    JOINT_RETURN_AND_LOCAL_FIELD_UPDATE = "joint-return-and-local-field-update"


REQUIRED_NEGATIVE_COMPLETION_FAMILIES = frozenset(MechanismFamily)


def _is_hex_digest(value: str, *, length: int) -> bool:
    if len(value) != length:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _is_sha256(value: str) -> bool:
    return _is_hex_digest(value, length=64)


def _is_git_sha(value: str) -> bool:
    return _is_hex_digest(value, length=40)


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
    lineage_swap_protocol_id: str
    contradiction_protocol_id: str
    future_competition_protocol_id: str
    bounded_ambiguity_protocol_id: str
    p3_protocol_id: str
    explicit_null_id: str
    recurrent_null_id: str
    negative_stop_observation_id: str
    protocol_bundle_source_sha: str
    mechanism_rule_spec_path: str
    null_ladder_spec_path: str
    bound_specification_hash: str = ""

    def validate(self) -> None:
        if not self.proposal_id:
            raise ValueError("proposal_id must be non-empty")
        if len(set(self.expected_p3_carrier_loci)) != len(
            self.expected_p3_carrier_loci
        ):
            raise ValueError("expected P3 carrier loci must be unique")

    def specification_payload(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "mechanism_family": self.mechanism_family.value,
            "lineage_swap_test_declared": self.lineage_swap_test_declared,
            "external_confirmation_only_positive": (
                self.external_confirmation_only_positive
            ),
            "contradiction_correction_declared": (
                self.contradiction_correction_declared
            ),
            "future_local_competition_effect_declared": (
                self.future_local_competition_effect_declared
            ),
            "bounded_ambiguity_declared": self.bounded_ambiguity_declared,
            "uses_forbidden_privilege": self.uses_forbidden_privilege,
            "expected_p3_carrier_loci": tuple(
                locus.value for locus in self.expected_p3_carrier_loci
            ),
            "explicit_null_declared": self.explicit_null_declared,
            "recurrent_null_declared": self.recurrent_null_declared,
            "negative_stop_observation_declared": (
                self.negative_stop_observation_declared
            ),
            "lineage_swap_protocol_id": self.lineage_swap_protocol_id,
            "contradiction_protocol_id": self.contradiction_protocol_id,
            "future_competition_protocol_id": self.future_competition_protocol_id,
            "bounded_ambiguity_protocol_id": self.bounded_ambiguity_protocol_id,
            "p3_protocol_id": self.p3_protocol_id,
            "explicit_null_id": self.explicit_null_id,
            "recurrent_null_id": self.recurrent_null_id,
            "negative_stop_observation_id": self.negative_stop_observation_id,
            "protocol_bundle_source_sha": self.protocol_bundle_source_sha,
            "mechanism_rule_spec_path": self.mechanism_rule_spec_path,
            "null_ladder_spec_path": self.null_ladder_spec_path,
        }

    def specification_hash(self) -> str:
        canonical = json.dumps(
            self.specification_payload(),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def bind(self) -> PreMechanismProposal:
        return replace(self, bound_specification_hash=self.specification_hash())


@dataclass(frozen=True, slots=True)
class PreMechanismAdmissionAssessment:
    proposal_id: str
    mechanism_family: MechanismFamily
    specification_hash: str
    specification_binding_valid: bool
    protocol_source_binding_valid: bool
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
    specification_hash = proposal.specification_hash()
    binding_valid = (
        _is_sha256(proposal.bound_specification_hash)
        and proposal.bound_specification_hash == specification_hash
    )
    source_binding_valid = _is_git_sha(proposal.protocol_bundle_source_sha)
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
        ("lineage-swap-protocol-id", bool(proposal.lineage_swap_protocol_id)),
        ("contradiction-protocol-id", bool(proposal.contradiction_protocol_id)),
        (
            "future-competition-protocol-id",
            bool(proposal.future_competition_protocol_id),
        ),
        (
            "bounded-ambiguity-protocol-id",
            bool(proposal.bounded_ambiguity_protocol_id),
        ),
        ("p3-protocol-id", bool(proposal.p3_protocol_id)),
        ("explicit-null-id", bool(proposal.explicit_null_id)),
        ("recurrent-null-id", bool(proposal.recurrent_null_id)),
        (
            "negative-stop-observation-id",
            bool(proposal.negative_stop_observation_id),
        ),
        ("protocol-bundle-source-sha", source_binding_valid),
        ("mechanism-rule-spec-path", bool(proposal.mechanism_rule_spec_path)),
        ("null-ladder-spec-path", bool(proposal.null_ladder_spec_path)),
        ("proposal-specification-binding", binding_valid),
    )
    missing = tuple(name for name, satisfied in requirements if not satisfied)
    if proposal.uses_forbidden_privilege:
        missing = (*missing, "no-forbidden-privilege")

    admitted = not missing
    if not binding_valid:
        classification = "proposal-specification-binding-invalid"
    elif not source_binding_valid:
        classification = "protocol-source-binding-invalid"
    else:
        classification = (
            "admitted-for-discriminator-first-implementation"
            if admitted
            else "premechanism-contract-incomplete"
        )
    return PreMechanismAdmissionAssessment(
        proposal_id=proposal.proposal_id,
        mechanism_family=proposal.mechanism_family,
        specification_hash=specification_hash,
        specification_binding_valid=binding_valid,
        protocol_source_binding_valid=source_binding_valid,
        admitted_for_implementation=admitted,
        missing_requirements=missing,
        classification=classification,
    )


@dataclass(frozen=True, slots=True)
class CandidateDisposition:
    candidate_id: str
    mechanism_family: MechanismFamily
    proposal_specification_hash: str
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
        if not _is_sha256(self.proposal_specification_hash):
            raise ValueError("proposal_specification_hash must be a SHA-256 digest")
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

from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import StateLocus
from sparkbrain.evaluation.v061_premechanism_admission import (
    CandidateDisposition,
    MechanismFamily,
    NegativeCompletionProgramme,
    PreMechanismProposal,
    assess_negative_completion,
    assess_premechanism_admission,
)


PROTOCOL_SOURCE_SHA = "92c2ead081844861847d679315639da6de401e1b"
MECHANISM_SPEC_PATH = "docs/V061_A01_TRANSIENT_RETURN_ADDRESS_PROTOCOL.md"
NULL_SPEC_PATH = "docs/V061_A01_NULL_LADDER.md"


def _all_families() -> tuple[MechanismFamily, ...]:
    return tuple(MechanismFamily)


def _proposal(**changes: object) -> PreMechanismProposal:
    base = PreMechanismProposal(
        proposal_id="candidate-a",
        mechanism_family=MechanismFamily.DISTRIBUTED_FIELD_TRACE,
        lineage_swap_test_declared=True,
        external_confirmation_only_positive=True,
        contradiction_correction_declared=True,
        future_local_competition_effect_declared=True,
        bounded_ambiguity_declared=True,
        uses_forbidden_privilege=False,
        expected_p3_carrier_loci=(StateLocus.FIELD_STATE,),
        explicit_null_declared=True,
        recurrent_null_declared=True,
        negative_stop_observation_declared=True,
        lineage_swap_protocol_id="P1-lineage-swap-v1",
        contradiction_protocol_id="P1-contradiction-v1",
        future_competition_protocol_id="P2-world-to-local-v1",
        bounded_ambiguity_protocol_id="P4-bounded-ambiguity-v1",
        p3_protocol_id="P3-state-locus-cross-v1",
        explicit_null_id="P5-minimal-explicit-memory-v1",
        recurrent_null_id="P5-resource-matched-recurrent-v1",
        negative_stop_observation_id="NEG-stop-observation-v1",
        protocol_bundle_source_sha=PROTOCOL_SOURCE_SHA,
        mechanism_rule_spec_path=MECHANISM_SPEC_PATH,
        null_ladder_spec_path=NULL_SPEC_PATH,
    )
    return replace(base, **changes).bind()


def _disposition(
    candidate_id: str,
    **changes: object,
) -> CandidateDisposition:
    base = CandidateDisposition(
        candidate_id=candidate_id,
        mechanism_family=MechanismFamily.DISTRIBUTED_FIELD_TRACE,
        proposal_specification_hash="a" * 64,
        non_privileged=True,
        p1_passed=True,
        p2_passed=True,
        p3_passed=True,
        p4_passed=True,
        p5_assessed=True,
        p5_reduced_to_explicit_memory=False,
    )
    return replace(base, **changes)


def test_complete_premechanism_contract_is_admitted() -> None:
    proposal = _proposal()
    assessment = assess_premechanism_admission(proposal)
    assert assessment.specification_binding_valid is True
    assert assessment.protocol_source_binding_valid is True
    assert assessment.specification_hash == proposal.bound_specification_hash
    assert assessment.admitted_for_implementation is True
    assert assessment.missing_requirements == ()
    assert assessment.classification == "admitted-for-discriminator-first-implementation"


def test_admission_fails_closed_without_lineage_and_null_contracts() -> None:
    assessment = assess_premechanism_admission(
        _proposal(
            lineage_swap_test_declared=False,
            explicit_null_declared=False,
            recurrent_null_declared=False,
            negative_stop_observation_declared=False,
        )
    )
    assert assessment.admitted_for_implementation is False
    assert assessment.missing_requirements == (
        "lineage-swap-test",
        "explicit-null",
        "recurrent-null",
        "negative-stop-observation",
    )


def test_admission_rejects_forbidden_privilege() -> None:
    assessment = assess_premechanism_admission(
        _proposal(uses_forbidden_privilege=True)
    )
    assert assessment.admitted_for_implementation is False
    assert "no-forbidden-privilege" in assessment.missing_requirements


def test_admission_requires_declared_p3_carrier_locus() -> None:
    assessment = assess_premechanism_admission(
        _proposal(expected_p3_carrier_loci=())
    )
    assert assessment.admitted_for_implementation is False
    assert "p3-carrier-locus" in assessment.missing_requirements


def test_post_binding_specification_edit_is_rejected() -> None:
    tampered = replace(_proposal(), recurrent_null_id="changed-after-binding")
    assessment = assess_premechanism_admission(tampered)
    assert assessment.specification_binding_valid is False
    assert assessment.admitted_for_implementation is False
    assert "proposal-specification-binding" in assessment.missing_requirements
    assert assessment.classification == "proposal-specification-binding-invalid"


def test_admission_requires_concrete_protocol_and_null_ids() -> None:
    assessment = assess_premechanism_admission(
        _proposal(
            future_competition_protocol_id="",
            explicit_null_id="",
            recurrent_null_id="",
        )
    )
    assert assessment.admitted_for_implementation is False
    assert "future-competition-protocol-id" in assessment.missing_requirements
    assert "explicit-null-id" in assessment.missing_requirements
    assert "recurrent-null-id" in assessment.missing_requirements


def test_admission_rejects_invalid_protocol_source_sha() -> None:
    assessment = assess_premechanism_admission(
        _proposal(protocol_bundle_source_sha="not-a-git-sha")
    )
    assert assessment.protocol_source_binding_valid is False
    assert assessment.admitted_for_implementation is False
    assert "protocol-bundle-source-sha" in assessment.missing_requirements
    assert assessment.classification == "protocol-source-binding-invalid"


def test_admission_requires_bound_mechanism_and_null_spec_paths() -> None:
    assessment = assess_premechanism_admission(
        _proposal(mechanism_rule_spec_path="", null_ladder_spec_path="")
    )
    assert assessment.admitted_for_implementation is False
    assert "mechanism-rule-spec-path" in assessment.missing_requirements
    assert "null-ladder-spec-path" in assessment.missing_requirements


def test_incomplete_candidate_programme_never_triggers_negative_completion() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=False,
        completed_families=(),
        dispositions=(
            _disposition(
                "failed",
                p1_passed=False,
                p5_assessed=False,
            ),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.stop_stronger_field_claim is False
    assert assessment.classification == "programme-incomplete"


def test_complete_programme_requires_all_preregistered_mechanism_families() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
        completed_families=(MechanismFamily.DISTRIBUTED_FIELD_TRACE,),
        dispositions=(
            _disposition("p1-fail", p1_passed=False, p5_assessed=False),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.required_family_coverage_passed is False
    assert assessment.stop_stronger_field_claim is False
    assert assessment.classification == "mechanism-family-coverage-incomplete"


def test_complete_programme_with_no_p1_p4_survivor_stops_stronger_claim() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
        completed_families=_all_families(),
        dispositions=(
            _disposition("p1-fail", p1_passed=False, p5_assessed=False),
            _disposition("privileged", non_privileged=False, p5_assessed=False),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.required_family_coverage_passed is True
    assert assessment.p1_p4_survivor_ids == ()
    assert assessment.stop_stronger_field_claim is True
    assert assessment.classification == "negative-completion-no-p1-p4-survivor"


def test_complete_programme_waits_until_every_survivor_has_p5_assessment() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
        completed_families=_all_families(),
        dispositions=(
            _disposition(
                "survivor",
                p5_assessed=False,
                p5_reduced_to_explicit_memory=False,
            ),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.p1_p4_survivor_ids == ("survivor",)
    assert assessment.all_survivors_p5_assessed is False
    assert assessment.stop_stronger_field_claim is False
    assert assessment.classification == "p5-incomplete-for-survivors"


def test_all_survivors_reduced_under_p5_stops_stronger_claim() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
        completed_families=_all_families(),
        dispositions=(
            _disposition("a", p5_reduced_to_explicit_memory=True),
            _disposition("b", p5_reduced_to_explicit_memory=True),
            _disposition("p3-fail", p3_passed=False, p5_assessed=False),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.p1_p4_survivor_ids == ("a", "b")
    assert assessment.all_survivors_p5_assessed is True
    assert assessment.all_survivors_reduced_to_explicit_memory is True
    assert assessment.stop_stronger_field_claim is True
    assert assessment.classification == (
        "negative-completion-all-survivors-explicit-memory-reducible"
    )


def test_one_nonreduced_survivor_keeps_stronger_claim_open() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
        completed_families=_all_families(),
        dispositions=(
            _disposition("reduced", p5_reduced_to_explicit_memory=True),
            _disposition("not-reduced"),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.stop_stronger_field_claim is False
    assert assessment.classification == "stronger-field-claim-remains-open"


def test_candidate_disposition_requires_registered_proposal_hash() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=False,
        completed_families=(),
        dispositions=(
            _disposition("invalid-hash", proposal_specification_hash="not-a-hash"),
        ),
    )
    with pytest.raises(ValueError, match="SHA-256"):
        assess_negative_completion(programme)


def test_p5_reduction_cannot_precede_p5_assessment() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=False,
        completed_families=(),
        dispositions=(
            _disposition(
                "invalid",
                p5_assessed=False,
                p5_reduced_to_explicit_memory=True,
            ),
        ),
    )
    with pytest.raises(ValueError, match="before P5 assessment"):
        assess_negative_completion(programme)


def test_complete_programme_cannot_be_empty() -> None:
    with pytest.raises(ValueError, match="must contain dispositions"):
        assess_negative_completion(
            NegativeCompletionProgramme(
                candidate_programme_complete=True,
                completed_families=_all_families(),
                dispositions=(),
            )
        )

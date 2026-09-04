from __future__ import annotations

from dataclasses import replace

import pytest

from sparkbrain.evaluation.v061_p3_p5_diagnostic_protocol import StateLocus
from sparkbrain.evaluation.v061_premechanism_admission import (
    CandidateDisposition,
    NegativeCompletionProgramme,
    PreMechanismProposal,
    assess_negative_completion,
    assess_premechanism_admission,
)


def _proposal(**changes: object) -> PreMechanismProposal:
    base = PreMechanismProposal(
        proposal_id="candidate-a",
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
    )
    return replace(base, **changes)


def _disposition(
    candidate_id: str,
    **changes: object,
) -> CandidateDisposition:
    base = CandidateDisposition(
        candidate_id=candidate_id,
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
    assessment = assess_premechanism_admission(_proposal())
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


def test_incomplete_candidate_programme_never_triggers_negative_completion() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=False,
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


def test_complete_programme_with_no_p1_p4_survivor_stops_stronger_claim() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
        dispositions=(
            _disposition("p1-fail", p1_passed=False, p5_assessed=False),
            _disposition("privileged", non_privileged=False, p5_assessed=False),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.p1_p4_survivor_ids == ()
    assert assessment.stop_stronger_field_claim is True
    assert assessment.classification == "negative-completion-no-p1-p4-survivor"


def test_complete_programme_waits_until_every_survivor_has_p5_assessment() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=True,
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
        dispositions=(
            _disposition("reduced", p5_reduced_to_explicit_memory=True),
            _disposition("not-reduced"),
        ),
    )
    assessment = assess_negative_completion(programme)
    assert assessment.stop_stronger_field_claim is False
    assert assessment.classification == "stronger-field-claim-remains-open"


def test_p5_reduction_cannot_precede_p5_assessment() -> None:
    programme = NegativeCompletionProgramme(
        candidate_programme_complete=False,
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
                dispositions=(),
            )
        )

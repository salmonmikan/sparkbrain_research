import pytest

from sparkbrain.evaluation.terminal_provenance import (
    PhaseAssessment,
    TerminalClass,
    TerminalProvenanceRecord,
    assess_evidence_backed_family_coverage,
)


NA = PhaseAssessment.NOT_ASSESSED
PASS = PhaseAssessment.PASSED
FAIL = PhaseAssessment.FAILED


def test_executed_phase_failure_preserves_assessed_boundary() -> None:
    record = TerminalProvenanceRecord(
        mechanism_family="family-a",
        terminal_class=TerminalClass.EXECUTED_PHASE_FAILURE,
        phase_assessments=(PASS, PASS, PASS, FAIL, NA),
        started=True,
        identity_consumed=True,
        canonical_authority="synthetic://family-a/terminal",
        identity="synthetic-family-a-v1",
    )

    assert record.phase_status() == {
        "P1": PASS,
        "P2": PASS,
        "P3": PASS,
        "P4": FAIL,
        "P5": NA,
    }


def test_pre_start_static_reduction_keeps_every_phase_unassessed() -> None:
    record = TerminalProvenanceRecord(
        mechanism_family="family-b",
        terminal_class=TerminalClass.PRE_START_STATIC_REDUCTION,
        phase_assessments=(NA, NA, NA, NA, NA),
        started=False,
        identity_consumed=False,
        canonical_authority="synthetic://family-b/closeout",
        identity="synthetic-family-b-v1",
        comparator_authority="synthetic://family-b/comparator",
    )

    assert set(record.phase_status().values()) == {NA}


def test_pre_start_record_rejects_fabricated_phase_result() -> None:
    with pytest.raises(ValueError, match="P1-P5 NOT_ASSESSED"):
        TerminalProvenanceRecord(
            mechanism_family="family-b",
            terminal_class=TerminalClass.PRE_START_STATIC_REDUCTION,
            phase_assessments=(PASS, NA, NA, NA, NA),
            started=False,
            identity_consumed=False,
            canonical_authority="synthetic://family-b/closeout",
            comparator_authority="synthetic://family-b/comparator",
        )


def test_static_reduction_requires_comparator_authority() -> None:
    with pytest.raises(ValueError, match="comparator_authority"):
        TerminalProvenanceRecord(
            mechanism_family="family-c",
            terminal_class=TerminalClass.PRE_START_STATIC_REDUCTION,
            phase_assessments=(NA, NA, NA, NA, NA),
            started=False,
            identity_consumed=False,
            canonical_authority="synthetic://family-c/closeout",
        )


def test_executed_terminal_record_requires_started_consumed_identity() -> None:
    with pytest.raises(ValueError, match="STARTED"):
        TerminalProvenanceRecord(
            mechanism_family="family-a",
            terminal_class=TerminalClass.EXECUTED_PHASE_FAILURE,
            phase_assessments=(PASS, FAIL, NA, NA, NA),
            started=False,
            identity_consumed=False,
            canonical_authority="synthetic://family-a/terminal",
            identity="synthetic-family-a-v1",
        )


def test_executed_phase_failure_is_sequential() -> None:
    with pytest.raises(ValueError, match="after the terminal failure"):
        TerminalProvenanceRecord(
            mechanism_family="family-a",
            terminal_class=TerminalClass.EXECUTED_PHASE_FAILURE,
            phase_assessments=(PASS, FAIL, PASS, NA, NA),
            started=True,
            identity_consumed=True,
            canonical_authority="synthetic://family-a/terminal",
            identity="synthetic-family-a-v1",
        )


def test_executed_p5_reduction_has_explicit_comparator() -> None:
    record = TerminalProvenanceRecord(
        mechanism_family="family-p5",
        terminal_class=TerminalClass.EXECUTED_P5_REDUCTION,
        phase_assessments=(PASS, PASS, PASS, PASS, FAIL),
        started=True,
        identity_consumed=True,
        canonical_authority="synthetic://family-p5/terminal",
        identity="synthetic-family-p5-v1",
        comparator_authority="synthetic://family-p5/comparator",
    )

    assert record.phase_status()["P5"] is FAIL


def test_family_coverage_is_derived_from_terminal_records() -> None:
    family_a = TerminalProvenanceRecord(
        mechanism_family="family-a",
        terminal_class=TerminalClass.EXECUTED_PHASE_FAILURE,
        phase_assessments=(PASS, PASS, PASS, FAIL, NA),
        started=True,
        identity_consumed=True,
        canonical_authority="synthetic://family-a/terminal",
        identity="synthetic-family-a-v1",
    )
    family_b = TerminalProvenanceRecord(
        mechanism_family="family-b",
        terminal_class=TerminalClass.PRE_START_STATIC_REDUCTION,
        phase_assessments=(NA, NA, NA, NA, NA),
        started=False,
        identity_consumed=False,
        canonical_authority="synthetic://family-b/closeout",
        comparator_authority="synthetic://family-b/comparator",
    )

    coverage = assess_evidence_backed_family_coverage(
        ("family-a", "family-b", "family-c"),
        (family_a, family_b),
    )

    assert coverage.complete is False
    assert coverage.missing_families == frozenset({"family-c"})

    family_c = TerminalProvenanceRecord(
        mechanism_family="family-c",
        terminal_class=TerminalClass.PRE_START_OTHER_REJECTION,
        phase_assessments=(NA, NA, NA, NA, NA),
        started=False,
        identity_consumed=False,
        canonical_authority="synthetic://family-c/closeout",
    )
    complete = assess_evidence_backed_family_coverage(
        ("family-a", "family-b", "family-c"),
        (family_a, family_b, family_c),
    )

    assert complete.complete is True
    assert complete.missing_families == frozenset()


def test_duplicate_family_records_are_rejected() -> None:
    record = TerminalProvenanceRecord(
        mechanism_family="family-b",
        terminal_class=TerminalClass.PRE_START_OTHER_REJECTION,
        phase_assessments=(NA, NA, NA, NA, NA),
        started=False,
        identity_consumed=False,
        canonical_authority="synthetic://family-b/closeout",
    )

    with pytest.raises(ValueError, match="duplicate terminal provenance"):
        assess_evidence_backed_family_coverage(("family-b",), (record, record))

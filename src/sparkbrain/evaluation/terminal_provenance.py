"""Generic evidence-backed terminal provenance bookkeeping.

This module deliberately does not depend on the V061/A01 evaluator.  It models
terminal provenance without forcing pre-START rejections into executed phase
booleans and makes family coverage a consequence of terminal records rather
than a bare family-name list.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class TerminalClass(StrEnum):
    """How a prospective object reached a terminal state."""

    EXECUTED_PHASE_FAILURE = "executed_phase_failure"
    EXECUTED_P5_REDUCTION = "executed_p5_reduction"
    PRE_START_STATIC_REDUCTION = "pre_start_static_reduction"
    PRE_START_OTHER_REJECTION = "pre_start_other_rejection"


class PhaseAssessment(StrEnum):
    """Whether a protocol phase was actually assessed and, if so, its result."""

    NOT_ASSESSED = "not_assessed"
    PASSED = "passed"
    FAILED = "failed"


PHASE_NAMES = ("P1", "P2", "P3", "P4", "P5")


@dataclass(frozen=True, slots=True)
class TerminalProvenanceRecord:
    """Evidence-backed provenance for one terminal mechanism-family object.

    ``phase_assessments`` is positional in ``PHASE_NAMES`` order.  Pre-START
    terminal records must leave every phase explicitly ``NOT_ASSESSED``; this
    prevents bookkeeping from inventing phase failures for objects that were
    never executed.
    """

    mechanism_family: str
    terminal_class: TerminalClass
    phase_assessments: tuple[PhaseAssessment, ...]
    started: bool
    identity_consumed: bool
    canonical_authority: str
    identity: str | None = None
    comparator_authority: str | None = None

    def __post_init__(self) -> None:
        if not self.mechanism_family.strip():
            raise ValueError("mechanism_family must be non-empty")
        if not self.canonical_authority.strip():
            raise ValueError("canonical_authority must be non-empty")
        if self.identity is not None and not self.identity.strip():
            raise ValueError("identity must be non-empty when supplied")
        if len(self.phase_assessments) != len(PHASE_NAMES):
            raise ValueError("phase_assessments must contain exactly P1-P5")

        pre_start = self.terminal_class in {
            TerminalClass.PRE_START_STATIC_REDUCTION,
            TerminalClass.PRE_START_OTHER_REJECTION,
        }
        if pre_start:
            self._validate_pre_start()
        else:
            self._validate_executed()

    def _validate_pre_start(self) -> None:
        if self.started:
            raise ValueError("pre-START terminal record cannot be STARTED")
        if self.identity_consumed:
            raise ValueError("pre-START terminal record cannot consume its identity")
        if any(value is not PhaseAssessment.NOT_ASSESSED for value in self.phase_assessments):
            raise ValueError("pre-START terminal record must mark P1-P5 NOT_ASSESSED")
        if (
            self.terminal_class is TerminalClass.PRE_START_STATIC_REDUCTION
            and not (self.comparator_authority or "").strip()
        ):
            raise ValueError("pre-START static reduction requires comparator_authority")

    def _validate_executed(self) -> None:
        if not self.started:
            raise ValueError("executed terminal record must be STARTED")
        if not self.identity_consumed:
            raise ValueError("executed terminal record must consume its identity")
        if not (self.identity or "").strip():
            raise ValueError("executed terminal record requires identity")

        if self.terminal_class is TerminalClass.EXECUTED_PHASE_FAILURE:
            self._validate_sequential_phase_failure()
        elif self.terminal_class is TerminalClass.EXECUTED_P5_REDUCTION:
            expected = (
                PhaseAssessment.PASSED,
                PhaseAssessment.PASSED,
                PhaseAssessment.PASSED,
                PhaseAssessment.PASSED,
                PhaseAssessment.FAILED,
            )
            if self.phase_assessments != expected:
                raise ValueError("executed P5 reduction requires P1-P4 PASSED and P5 FAILED")
            if not (self.comparator_authority or "").strip():
                raise ValueError("executed P5 reduction requires comparator_authority")

    def _validate_sequential_phase_failure(self) -> None:
        try:
            failed_index = self.phase_assessments.index(PhaseAssessment.FAILED)
        except ValueError as exc:
            raise ValueError("executed phase failure requires one FAILED phase") from exc

        if any(
            value is not PhaseAssessment.PASSED
            for value in self.phase_assessments[:failed_index]
        ):
            raise ValueError("phases before the terminal failure must be PASSED")
        if any(
            value is not PhaseAssessment.NOT_ASSESSED
            for value in self.phase_assessments[failed_index + 1 :]
        ):
            raise ValueError("phases after the terminal failure must be NOT_ASSESSED")

    def phase_status(self) -> dict[str, PhaseAssessment]:
        """Return named phase provenance without changing the immutable record."""

        return dict(zip(PHASE_NAMES, self.phase_assessments, strict=True))


@dataclass(frozen=True, slots=True)
class FamilyCoverageAssessment:
    """Coverage derived from evidence-backed terminal records."""

    required_families: frozenset[str]
    evidenced_families: frozenset[str]
    missing_families: frozenset[str]

    @property
    def complete(self) -> bool:
        return not self.missing_families


def assess_evidence_backed_family_coverage(
    required_families: Iterable[str],
    records: Iterable[TerminalProvenanceRecord],
) -> FamilyCoverageAssessment:
    """Cross-check required families against one unambiguous terminal record each."""

    required = frozenset(family.strip() for family in required_families if family.strip())
    if not required:
        raise ValueError("required_families must contain at least one non-empty family")

    by_family: dict[str, TerminalProvenanceRecord] = {}
    for record in records:
        family = record.mechanism_family
        if family in by_family:
            raise ValueError(f"duplicate terminal provenance for mechanism family: {family}")
        by_family[family] = record

    evidenced = frozenset(by_family)
    return FamilyCoverageAssessment(
        required_families=required,
        evidenced_families=evidenced,
        missing_families=required - evidenced,
    )

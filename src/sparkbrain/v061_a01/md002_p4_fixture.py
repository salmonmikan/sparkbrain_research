"""Execution-disabled prospective fixture for A01 MD-002 P4.

P4 asks whether genuinely merged anonymous ancestry can remain plural and later
respond correctly when external evidence either separates the causal lineages or
leaves them inseparable. This module freezes the six preregistered P4 condition
shapes without supplying runtime-active lineage lists, capability outcomes, or
scientific scores.

The later runner must derive active lineages from retained runtime traces and
hand those traces to :mod:`md002_p4_trace_binding`; this fixture deliberately
contains no field for caller-selected ``active_lineages_before`` or
``active_lineages_after`` values.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

P4BoundaryMode = Literal["separate", "merged"]
P4EvidenceMode = Literal["confirmation", "contradiction", "absence", "internal-replay"]


@dataclass(frozen=True, slots=True)
class P4BoundaryAncestrySpec:
    """Prospective BoundaryEvent ancestry shape, not a runtime observation."""

    boundary_id: str
    source_proposal_ids: tuple[str, ...]

    def validate(self) -> None:
        if not isinstance(self.boundary_id, str) or not self.boundary_id:
            raise ValueError("P4 boundary ID must be non-empty")
        if not self.source_proposal_ids:
            raise ValueError("P4 boundary ancestry requires proposal IDs")
        if any(
            not isinstance(value, str) or not value
            for value in self.source_proposal_ids
        ):
            raise ValueError("P4 proposal IDs must be non-empty strings")
        if len(self.source_proposal_ids) != len(set(self.source_proposal_ids)):
            raise ValueError("P4 boundary ancestry proposal IDs must be unique")

    @property
    def is_merged(self) -> bool:
        self.validate()
        return len(self.source_proposal_ids) >= 2


@dataclass(frozen=True, slots=True)
class P4ConditionSpec:
    """One outcome-blind P4 condition declaration.

    ``requires_later_separation`` describes the external-evidence contract only;
    it is not an expected runtime lineage list and cannot satisfy the P4 trace
    binding by itself.
    """

    condition_id: str
    boundary_mode: P4BoundaryMode
    evidence_mode: P4EvidenceMode
    requires_later_separation: bool
    returned_external_evidence: bool
    positive_credit_permitted: bool

    def validate(self) -> None:
        if not isinstance(self.condition_id, str) or not self.condition_id:
            raise ValueError("P4 condition ID must be non-empty")
        if self.boundary_mode not in ("separate", "merged"):
            raise ValueError("invalid P4 boundary mode")
        if self.evidence_mode not in (
            "confirmation",
            "contradiction",
            "absence",
            "internal-replay",
        ):
            raise ValueError("invalid P4 evidence mode")
        if not isinstance(self.requires_later_separation, bool):
            raise TypeError("P4 requires_later_separation must be bool")
        if not isinstance(self.returned_external_evidence, bool):
            raise TypeError("P4 returned_external_evidence must be bool")
        if not isinstance(self.positive_credit_permitted, bool):
            raise TypeError("P4 positive_credit_permitted must be bool")

        if self.evidence_mode in ("absence", "internal-replay"):
            if self.returned_external_evidence:
                raise ValueError(
                    "P4 absence/replay controls cannot return external evidence"
                )
            if self.positive_credit_permitted:
                raise ValueError(
                    "P4 absence/replay controls cannot permit positive causal credit"
                )
        elif not self.returned_external_evidence:
            raise ValueError(
                "P4 external confirmation/contradiction requires returned evidence"
            )

        if self.evidence_mode == "contradiction" and self.positive_credit_permitted:
            raise ValueError("P4 contradiction cannot be declared positive-credit evidence")
        if self.requires_later_separation and self.boundary_mode != "merged":
            raise ValueError("P4 later-separation assay is defined only for merged ancestry")
        if self.requires_later_separation and self.evidence_mode not in (
            "confirmation",
            "contradiction",
        ):
            raise ValueError("P4 later separation requires external confirmation or contradiction")


@dataclass(frozen=True, slots=True)
class P4ProspectiveFixture:
    """Fixed two-lineage ancestry and six-condition P4 construction."""

    lineage_a_proposal_id: str
    lineage_b_proposal_id: str
    separate_a_boundary_id: str = "p4-boundary-separate-a"
    separate_b_boundary_id: str = "p4-boundary-separate-b"
    merged_boundary_id: str = "p4-boundary-merged-ab"

    def validate(self) -> None:
        proposal_ids = (self.lineage_a_proposal_id, self.lineage_b_proposal_id)
        if any(not isinstance(value, str) or not value for value in proposal_ids):
            raise ValueError("P4 lineage proposal IDs must be non-empty strings")
        if len(set(proposal_ids)) != 2:
            raise ValueError("P4 requires two distinct proposal lineages")
        boundary_ids = (
            self.separate_a_boundary_id,
            self.separate_b_boundary_id,
            self.merged_boundary_id,
        )
        if any(not isinstance(value, str) or not value for value in boundary_ids):
            raise ValueError("P4 boundary IDs must be non-empty strings")
        if len(set(boundary_ids)) != 3:
            raise ValueError("P4 separate and merged BoundaryEvent IDs must be distinct")
        for value in self.boundary_specs:
            value.validate()
        if any(value.is_merged for value in self.boundary_specs[:2]):
            raise RuntimeError("P4 separate BoundaryEvents accidentally carry merged ancestry")
        if not self.boundary_specs[2].is_merged:
            raise RuntimeError("P4 merged BoundaryEvent does not carry plural ancestry")

    @property
    def boundary_specs(self) -> tuple[P4BoundaryAncestrySpec, ...]:
        return (
            P4BoundaryAncestrySpec(
                boundary_id=self.separate_a_boundary_id,
                source_proposal_ids=(self.lineage_a_proposal_id,),
            ),
            P4BoundaryAncestrySpec(
                boundary_id=self.separate_b_boundary_id,
                source_proposal_ids=(self.lineage_b_proposal_id,),
            ),
            P4BoundaryAncestrySpec(
                boundary_id=self.merged_boundary_id,
                source_proposal_ids=(
                    self.lineage_a_proposal_id,
                    self.lineage_b_proposal_id,
                ),
            ),
        )

    @property
    def conditions(self) -> tuple[P4ConditionSpec, ...]:
        rows = (
            P4ConditionSpec(
                condition_id="p4-separate-confirmation",
                boundary_mode="separate",
                evidence_mode="confirmation",
                requires_later_separation=False,
                returned_external_evidence=True,
                positive_credit_permitted=True,
            ),
            P4ConditionSpec(
                condition_id="p4-merged-confirmation",
                boundary_mode="merged",
                evidence_mode="confirmation",
                requires_later_separation=False,
                returned_external_evidence=True,
                positive_credit_permitted=True,
            ),
            P4ConditionSpec(
                condition_id="p4-merged-separating-confirmation",
                boundary_mode="merged",
                evidence_mode="confirmation",
                requires_later_separation=True,
                returned_external_evidence=True,
                positive_credit_permitted=True,
            ),
            P4ConditionSpec(
                condition_id="p4-merged-separating-contradiction",
                boundary_mode="merged",
                evidence_mode="contradiction",
                requires_later_separation=True,
                returned_external_evidence=True,
                positive_credit_permitted=False,
            ),
            P4ConditionSpec(
                condition_id="p4-merged-absence",
                boundary_mode="merged",
                evidence_mode="absence",
                requires_later_separation=False,
                returned_external_evidence=False,
                positive_credit_permitted=False,
            ),
            P4ConditionSpec(
                condition_id="p4-merged-replay",
                boundary_mode="merged",
                evidence_mode="internal-replay",
                requires_later_separation=False,
                returned_external_evidence=False,
                positive_credit_permitted=False,
            ),
        )
        for row in rows:
            row.validate()
        return rows

    def validate_matrix(self) -> None:
        self.validate()
        rows = self.conditions
        expected_ids = (
            "p4-separate-confirmation",
            "p4-merged-confirmation",
            "p4-merged-separating-confirmation",
            "p4-merged-separating-contradiction",
            "p4-merged-absence",
            "p4-merged-replay",
        )
        if tuple(row.condition_id for row in rows) != expected_ids:
            raise RuntimeError("P4 condition order drifted")
        if len({row.condition_id for row in rows}) != len(rows):
            raise RuntimeError("P4 condition IDs must be unique")
        if sum(row.boundary_mode == "separate" for row in rows) != 1:
            raise RuntimeError("P4 matrix requires exactly one separate-event condition")
        if sum(row.requires_later_separation for row in rows) != 2:
            raise RuntimeError(
                "P4 matrix requires confirmation and contradiction separation assays"
            )
        if sum(row.evidence_mode == "absence" for row in rows) != 1:
            raise RuntimeError("P4 matrix requires exactly one absence control")
        if sum(row.evidence_mode == "internal-replay" for row in rows) != 1:
            raise RuntimeError("P4 matrix requires exactly one replay control")


__all__ = [
    "P4BoundaryAncestrySpec",
    "P4BoundaryMode",
    "P4ConditionSpec",
    "P4EvidenceMode",
    "P4ProspectiveFixture",
]

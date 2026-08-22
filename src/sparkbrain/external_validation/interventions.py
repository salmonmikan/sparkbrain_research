from __future__ import annotations

from dataclasses import dataclass, replace

from ..tasks.schema import Observation


@dataclass(frozen=True, slots=True)
class EvidenceIntervention:
    kind: str
    evidence_id: str
    replacement_label: str | None = None

    def validate(self) -> None:
        if self.kind not in {"remove", "replace"}:
            raise ValueError(f"Unsupported intervention kind: {self.kind!r}")
        if not self.evidence_id:
            raise ValueError("Intervention evidence_id must not be empty")
        if self.kind == "replace" and not self.replacement_label:
            raise ValueError("Replace intervention requires replacement_label")
        if self.kind == "remove" and self.replacement_label is not None:
            raise ValueError("Remove intervention must not include replacement_label")


@dataclass(frozen=True, slots=True)
class InterventionAssessment:
    expected_prediction_change: bool
    observed_prediction_change: bool
    passed: bool


def apply_evidence_intervention(
    observations: tuple[Observation, ...], intervention: EvidenceIntervention
) -> tuple[Observation, ...]:
    intervention.validate()
    matching = [row for row in observations if row.evidence_id == intervention.evidence_id]
    if not matching:
        raise ValueError(f"Evidence ID not found: {intervention.evidence_id}")
    if intervention.kind == "remove":
        result = tuple(row for row in observations if row.evidence_id != intervention.evidence_id)
    else:
        result = tuple(
            replace(
                row,
                evidence_label=intervention.replacement_label,
                metadata={**row.metadata, "intervention": {"kind": "replace"}},
            )
            if row.evidence_id == intervention.evidence_id
            else row
            for row in observations
        )
    for index, row in enumerate(result):
        replace(row, step_index=index, delivery_time=float(index)).validate()
    return tuple(
        replace(row, step_index=index, delivery_time=float(index))
        for index, row in enumerate(result)
    )


def assess_intervention(
    *, original_prediction: str | None, intervened_prediction: str | None,
    expected_prediction_change: bool,
) -> InterventionAssessment:
    observed = original_prediction != intervened_prediction
    return InterventionAssessment(
        expected_prediction_change,
        observed,
        observed == expected_prediction_change,
    )

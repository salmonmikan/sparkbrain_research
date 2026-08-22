from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PredictionStep:
    """Backend output without evaluator targets or hidden annotations."""

    prediction: str | None
    confidence: float | None = None
    cited_evidence_ids: tuple[str, ...] = ()
    object_id: str = "answer"

    def validate(self) -> None:
        if self.confidence is not None and (
            not math.isfinite(self.confidence) or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("Prediction confidence must be finite and in [0, 1]")
        if not self.object_id:
            raise ValueError("Prediction object_id must not be empty")
        if len(set(self.cited_evidence_ids)) != len(self.cited_evidence_ids):
            raise ValueError("Prediction citations must be unique")


@dataclass(frozen=True, slots=True)
class RevisionTarget:
    """Evaluator-only target for one sequential prediction step."""

    truth: str
    update_required: bool
    decision_justified: bool = True
    required_evidence_ids: tuple[str, ...] = ()
    scenario_tags: tuple[str, ...] = ()
    object_id: str = "answer"

    def validate(self) -> None:
        if not self.truth or not self.object_id:
            raise ValueError("Revision target truth and object_id must not be empty")
        if len(set(self.required_evidence_ids)) != len(self.required_evidence_ids):
            raise ValueError("Required evidence IDs must be unique")

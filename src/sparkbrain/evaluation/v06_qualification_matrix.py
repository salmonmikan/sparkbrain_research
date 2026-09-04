from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sparkbrain.baselines.v06.g3_recurrent import (
    run_qualification_grid as run_g3_grid,
)
from sparkbrain.baselines.v06.g4_assembly import (
    run_qualification_grid as run_g4_grid,
)
from sparkbrain.baselines.v06.g5_typed import (
    run_qualification_grid as run_g5_grid,
)

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryPhase,
    ConfirmatoryResultRecord,
    assess_result_coverage,
    build_draft_confirmatory_manifest,
    frozen_manifest_copy,
    with_all_adapters_ready,
)
from .v06_confirmatory_controls import run_control_qualification_grid
from .v06_confirmatory_primary_adapter import run_primary_qualification_grid
from .v06_confirmatory_scoring import (
    StrictConfirmatoryOutcome,
    StrictMetricCoverageReport,
    assess_strict_metric_coverage,
    score_strict_confirmatory_results,
)


@dataclass(frozen=True, slots=True)
class CompleteQualificationMatrix:
    code_ref: str
    records: tuple[ConfirmatoryResultRecord, ...]
    strict_metric_coverage: StrictMetricCoverageReport
    outcome: StrictConfirmatoryOutcome

    @property
    def condition_count(self) -> int:
        return len({row.condition for row in self.records})

    @property
    def family_count(self) -> int:
        return len({row.family_id for row in self.records})

    @property
    def seed_count(self) -> int:
        return len({row.seed for row in self.records})

    @property
    def record_count(self) -> int:
        return len(self.records)

    def condition_record_counts(self) -> dict[str, int]:
        return {
            condition.value: sum(row.condition is condition for row in self.records)
            for condition in ConfirmatoryCondition
        }

    def state_dict(self) -> dict[str, Any]:
        return {
            "code_ref": self.code_ref,
            "condition_count": self.condition_count,
            "condition_record_counts": self.condition_record_counts(),
            "family_count": self.family_count,
            "outcome": self.outcome.state_dict(),
            "record_count": self.record_count,
            "seed_count": self.seed_count,
            "strict_metric_coverage": self.strict_metric_coverage.state_dict(),
        }


def qualification_manifest(code_ref: str):
    manifest = with_all_adapters_ready(
        build_draft_confirmatory_manifest(ConfirmatoryPhase.QUALIFICATION)
    )
    return frozen_manifest_copy(manifest, code_ref=code_ref)


def run_complete_qualification_matrix(
    *,
    code_ref: str,
) -> CompleteQualificationMatrix:
    """Run all eight qualification conditions through one strict scorer."""

    manifest = qualification_manifest(code_ref)
    primary = run_primary_qualification_grid()
    controls = run_control_qualification_grid()
    g3 = run_g3_grid()
    g4 = run_g4_grid()
    g5 = run_g5_grid()
    records = (
        *primary.records,
        *controls.records,
        *g3.records,
        *g4.records,
        *g5.records,
    )
    coverage = assess_result_coverage(manifest, records)
    if not coverage.complete:
        raise RuntimeError("complete qualification matrix has invalid coverage")
    metric_coverage = assess_strict_metric_coverage(manifest, records)
    if not metric_coverage.complete:
        raise RuntimeError("complete qualification matrix has invalid metrics")
    outcome = score_strict_confirmatory_results(manifest, records)
    return CompleteQualificationMatrix(
        code_ref=code_ref,
        records=records,
        strict_metric_coverage=metric_coverage,
        outcome=outcome,
    )

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from forge_prototypes.continuous_scope_revision_ablation import (
    AblationEvent,
    AblationQuery,
    ContinuousRevisionAblationReport,
    ContinuousScopeRevisionAblation,
)
from forge_prototypes.internal_scope_allocator import InternalScopeAllocatorConfig
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.plural_scope_posterior import ScopePosteriorConfig


@dataclass(frozen=True, slots=True)
class ScopeRevisionStressCase:
    case_id: str
    events: tuple[AblationEvent, ...]
    queries: tuple[tuple[str, tuple[float, ...], str], ...]


@dataclass(frozen=True, slots=True)
class ScopeRevisionStressOutcome:
    case_id: str
    full_commits: int
    cut_commits: int
    full_scope_tokens: tuple[str, ...]
    cut_scope_tokens: tuple[str, ...]
    queries: tuple[AblationQuery, ...]
    boundary_class: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "full_commits": self.full_commits,
            "cut_commits": self.cut_commits,
            "full_scope_tokens": list(self.full_scope_tokens),
            "cut_scope_tokens": list(self.cut_scope_tokens),
            "queries": [asdict(query) for query in self.queries],
            "boundary_class": self.boundary_class,
        }


@dataclass(frozen=True, slots=True)
class ScopeRevisionStressReport:
    outcomes: tuple[ScopeRevisionStressOutcome, ...]

    def as_dict(self) -> dict[str, Any]:
        return {"outcomes": [outcome.as_dict() for outcome in self.outcomes]}


def _base_prediction() -> PredictionPoolSnapshot:
    return PredictionPoolSnapshot(
        assembly_id="assembly-a",
        hypotheses=(
            WeightedHypothesis("A", 5, 0.5),
            WeightedHypothesis("B", 5, 0.5),
        ),
        selected_value=None,
        confidence=0.5,
        margin=0.0,
        abstained=True,
        reason="ambiguous_hypotheses",
    )


def _harness() -> ContinuousScopeRevisionAblation:
    return ContinuousScopeRevisionAblation(
        InternalScopeAllocatorConfig(
            reuse_radius=0.75,
            create_error_threshold=0.4,
            centroid_learning_rate=0.0,
            max_scopes=4,
        ),
        ScopePosteriorConfig(
            temperature=0.35,
            new_scope_error_scale=2.0,
            top_k=3,
            min_margin=0.15,
            min_selected_mass=0.55,
        ),
    )


def stress_cases() -> tuple[ScopeRevisionStressCase, ...]:
    """Return the fixed Forge-only boundary cases.

    These cases deliberately expose ordinary nearest-centroid/reject-option
    behavior. They are diagnostics, not a benchmark or a calibrated task.
    """

    return (
        ScopeRevisionStressCase(
            "moderate_overlap_with_midpoint_reject",
            (
                AblationEvent("a1", (0.0,), "A"),
                AblationEvent("b1", (1.2,), "B"),
                AblationEvent("a2", (0.15,), "A"),
                AblationEvent("b2", (1.05,), "B"),
            ),
            (
                ("qa", (0.1,), "A"),
                ("qb", (1.1,), "B"),
                ("midpoint", (0.6,), "A"),
            ),
        ),
        ScopeRevisionStressCase(
            "within_reuse_radius_collision",
            (
                AblationEvent("a1", (0.0,), "A"),
                AblationEvent("b1", (0.5,), "B"),
                AblationEvent("a2", (0.1,), "A"),
                AblationEvent("b2", (0.4,), "B"),
            ),
            (("qa", (0.0,), "A"), ("qb", (0.5,), "B")),
        ),
        ScopeRevisionStressCase(
            "single_conflicting_label",
            (
                AblationEvent("a1", (0.0,), "A"),
                AblationEvent("b1", (1.2,), "B"),
                AblationEvent("a-noise", (0.1,), "B"),
                AblationEvent("a2", (0.2,), "A"),
                AblationEvent("b2", (1.1,), "B"),
            ),
            (("qa", (0.1,), "A"), ("qb", (1.1,), "B")),
        ),
    )


def _scope_tokens(report: ContinuousRevisionAblationReport, arm: str) -> tuple[str, ...]:
    values = {
        token
        for row in report.steps
        if (token := getattr(row, f"{arm}_scope_token")) is not None
    }
    return tuple(sorted(values))


def _classify(case_id: str, report: ContinuousRevisionAblationReport) -> str:
    full = {query.label: query for query in report.queries}
    if case_id == "moderate_overlap_with_midpoint_reject":
        if (
            full["qa"].full_selected_value == "A"
            and full["qb"].full_selected_value == "B"
            and full["midpoint"].full_abstained
            and all(query.cut_abstained for query in report.queries)
        ):
            return "CONNECTED_FIXTURE_SURVIVES_JITTER_WITH_AMBIGUOUS_MIDPOINT_REJECT"
    elif case_id == "within_reuse_radius_collision":
        if len(_scope_tokens(report, "full")) == 1 and full["qb"].full_abstained:
            return "ROUTER_RESOLUTION_LIMIT_PREVENTS_SCOPE_SPECIFIC_REVISION"
    elif case_id == "single_conflicting_label":
        if (
            full["qa"].full_selected_value == "A"
            and full["qb"].full_selected_value == "B"
            and {query.cut_selected_value for query in report.queries} == {"B"}
        ):
            return "CONNECTED_FIXTURE_RETAINS_CONTEXT_SPECIFIC_MAJORITY_ONLY"
    return "UNCLASSIFIED_BOUNDARY_OBSERVATION"


def run_scope_revision_stress_probe() -> ScopeRevisionStressReport:
    outcomes: list[ScopeRevisionStressOutcome] = []
    base = _base_prediction()
    for case in stress_cases():
        report = _harness().run(base, case.events, case.queries)
        outcomes.append(
            ScopeRevisionStressOutcome(
                case_id=case.case_id,
                full_commits=report.full_commits,
                cut_commits=report.cut_commits,
                full_scope_tokens=_scope_tokens(report, "full"),
                cut_scope_tokens=_scope_tokens(report, "cut"),
                queries=report.queries,
                boundary_class=_classify(case.case_id, report),
            )
        )
    return ScopeRevisionStressReport(tuple(outcomes))


__all__ = [
    "ScopeRevisionStressCase",
    "ScopeRevisionStressOutcome",
    "ScopeRevisionStressReport",
    "run_scope_revision_stress_probe",
    "stress_cases",
]

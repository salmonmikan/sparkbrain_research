from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from statistics import fmean
from typing import Any


@dataclass(frozen=True, slots=True)
class BranchObservation:
    """Observer-only evidence for one anonymous shared-root branch.

    ``world_consistency`` is deliberately unavailable to the G1 selector.  It
    exists only so the evaluator can ask whether locally stable temporal
    structure and later anonymous world function agree.
    """

    branch_id: str
    exposure_count: int
    lags_ms: tuple[float, ...]
    world_consistency: float

    def validate(self) -> None:
        if not self.branch_id:
            raise ValueError("branch_id must be non-empty")
        if self.exposure_count < 1:
            raise ValueError("exposure_count must be positive")
        if len(self.lags_ms) != self.exposure_count:
            raise ValueError("one lag observation is required per exposure")
        if any(not math.isfinite(value) or value <= 0.0 for value in self.lags_ms):
            raise ValueError("all lag observations must be positive and finite")
        if not math.isfinite(self.world_consistency):
            raise ValueError("world_consistency must be finite")

    @property
    def lag_mean_ms(self) -> float:
        return fmean(self.lags_ms)

    @property
    def lag_variance_ms2(self) -> float:
        if len(self.lags_ms) < 2:
            return 0.0
        mean = self.lag_mean_ms
        return sum((value - mean) ** 2 for value in self.lags_ms) / (
            len(self.lags_ms) - 1
        )


@dataclass(frozen=True, slots=True)
class BranchScore:
    branch_id: str
    exposure_count: int
    frequency: float
    lag_mean_ms: float
    lag_variance_ms2: float
    temporal_stability: float
    g1_confidence: float
    world_consistency: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BranchCompetitionDiagnosis:
    scores: tuple[BranchScore, ...]
    selected_by_g1: str
    selected_by_exposure: str
    selected_by_world_consistency: str
    g1_matches_exposure: bool
    g1_matches_world_consistency: bool
    temporal_functional_decoupling: bool
    selection_margin: float

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "scores": [row.state_dict() for row in self.scores],
        }


def g1_confidence(
    *,
    exposure_count: int,
    total_exposure_count: int,
    lag_variance_ms2: float,
    variance_scale_ms2: float,
) -> float:
    """Reproduce the anonymous G1 frequency × temporal-stability score."""

    if exposure_count < 1 or total_exposure_count < exposure_count:
        raise ValueError("exposure counts are inconsistent")
    if lag_variance_ms2 < 0.0 or not math.isfinite(lag_variance_ms2):
        raise ValueError("lag variance must be finite and non-negative")
    if variance_scale_ms2 <= 0.0 or not math.isfinite(variance_scale_ms2):
        raise ValueError("variance scale must be positive and finite")
    frequency = exposure_count / total_exposure_count
    temporal_stability = 1.0 / (1.0 + lag_variance_ms2 / variance_scale_ms2)
    return frequency * temporal_stability


def diagnose_branch_competition(
    observations: tuple[BranchObservation, ...],
    *,
    variance_scale_ms2: float,
) -> BranchCompetitionDiagnosis:
    """Separate local temporal selection from later anonymous world function."""

    if len(observations) < 2:
        raise ValueError("at least two competing branches are required")
    if len({row.branch_id for row in observations}) != len(observations):
        raise ValueError("branch IDs must be unique")
    for row in observations:
        row.validate()
    total = sum(row.exposure_count for row in observations)
    scores = tuple(
        BranchScore(
            branch_id=row.branch_id,
            exposure_count=row.exposure_count,
            frequency=row.exposure_count / total,
            lag_mean_ms=row.lag_mean_ms,
            lag_variance_ms2=row.lag_variance_ms2,
            temporal_stability=(
                1.0
                / (1.0 + row.lag_variance_ms2 / variance_scale_ms2)
            ),
            g1_confidence=g1_confidence(
                exposure_count=row.exposure_count,
                total_exposure_count=total,
                lag_variance_ms2=row.lag_variance_ms2,
                variance_scale_ms2=variance_scale_ms2,
            ),
            world_consistency=row.world_consistency,
        )
        for row in observations
    )
    ranked_g1 = sorted(scores, key=lambda row: (-row.g1_confidence, row.branch_id))
    selected_by_g1 = ranked_g1[0].branch_id
    selected_by_exposure = min(
        scores,
        key=lambda row: (-row.exposure_count, row.branch_id),
    ).branch_id
    selected_by_world = min(
        scores,
        key=lambda row: (-row.world_consistency, row.branch_id),
    ).branch_id
    return BranchCompetitionDiagnosis(
        scores=scores,
        selected_by_g1=selected_by_g1,
        selected_by_exposure=selected_by_exposure,
        selected_by_world_consistency=selected_by_world,
        g1_matches_exposure=selected_by_g1 == selected_by_exposure,
        g1_matches_world_consistency=selected_by_g1 == selected_by_world,
        temporal_functional_decoupling=selected_by_g1 != selected_by_world,
        selection_margin=(
            ranked_g1[0].g1_confidence - ranked_g1[1].g1_confidence
        ),
    )


@dataclass(frozen=True, slots=True)
class RelationLinkObservation:
    target: str
    consistent_count: int
    inconsistent_count: int
    mean_magnitude_ratio: float = 1.0

    def validate(self) -> None:
        if not self.target:
            raise ValueError("target must be non-empty")
        if self.consistent_count < 0 or self.inconsistent_count < 0:
            raise ValueError("relation counts must be non-negative")
        if not math.isfinite(self.mean_magnitude_ratio):
            raise ValueError("mean_magnitude_ratio must be finite")
        if self.mean_magnitude_ratio < 0.0:
            raise ValueError("mean_magnitude_ratio must be non-negative")


@dataclass(frozen=True, slots=True)
class RelationExpressionScore:
    target: str
    reliability: float
    effective_current: float
    threshold_ratio: float
    proposal_eligible: bool
    field_expressed: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationExpressionDiagnosis:
    scores: tuple[RelationExpressionScore, ...]
    dominant_target: str | None
    expected_world_target: str
    expressed_targets: tuple[str, ...]
    storage_matches_world: bool
    exact_expression_matches_world: bool
    expression_abstention: bool
    multi_link_superposition: bool
    storage_failure: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "scores": [row.state_dict() for row in self.scores],
        }


def relation_reliability(
    *,
    consistent_count: int,
    inconsistent_count: int,
    prior_consistent: float = 1.0,
    prior_inconsistent: float = 1.0,
) -> float:
    if consistent_count < 0 or inconsistent_count < 0:
        raise ValueError("relation counts must be non-negative")
    if prior_consistent <= 0.0 or prior_inconsistent <= 0.0:
        raise ValueError("relation priors must be positive")
    return (prior_consistent + consistent_count) / (
        prior_consistent
        + prior_inconsistent
        + consistent_count
        + inconsistent_count
    )


def diagnose_relation_expression(
    links: tuple[RelationLinkObservation, ...],
    *,
    expected_world_target: str,
    field_threshold: float,
    relation_reentry_gain: float,
    base_magnitude: float = 1.0,
    minimum_consistent_count: int = 1,
    minimum_reliability: float = 0.0,
    prior_consistent: float = 1.0,
    prior_inconsistent: float = 1.0,
) -> RelationExpressionDiagnosis:
    """Separate relation storage/dominance from proposal and Field expression."""

    if not expected_world_target:
        raise ValueError("expected_world_target must be non-empty")
    if field_threshold <= 0.0 or relation_reentry_gain <= 0.0:
        raise ValueError("threshold and re-entry gain must be positive")
    if base_magnitude < 0.0:
        raise ValueError("base_magnitude must be non-negative")
    if len({row.target for row in links}) != len(links):
        raise ValueError("relation targets must be unique")
    for row in links:
        row.validate()

    scores = []
    for row in links:
        reliability = relation_reliability(
            consistent_count=row.consistent_count,
            inconsistent_count=row.inconsistent_count,
            prior_consistent=prior_consistent,
            prior_inconsistent=prior_inconsistent,
        )
        eligible = (
            row.consistent_count >= minimum_consistent_count
            and reliability >= minimum_reliability
        )
        effective_current = (
            base_magnitude
            * row.mean_magnitude_ratio
            * relation_reentry_gain
            * reliability
            if eligible
            else 0.0
        )
        scores.append(
            RelationExpressionScore(
                target=row.target,
                reliability=reliability,
                effective_current=effective_current,
                threshold_ratio=effective_current / field_threshold,
                proposal_eligible=eligible,
                field_expressed=eligible and effective_current >= field_threshold,
            )
        )
    ranked = sorted(scores, key=lambda row: (-row.reliability, row.target))
    dominant = ranked[0].target if ranked else None
    expressed = tuple(
        row.target
        for row in sorted(scores, key=lambda item: item.target)
        if row.field_expressed
    )
    storage_matches = dominant == expected_world_target
    exact_expression = expressed == (expected_world_target,)
    return RelationExpressionDiagnosis(
        scores=tuple(scores),
        dominant_target=dominant,
        expected_world_target=expected_world_target,
        expressed_targets=expressed,
        storage_matches_world=storage_matches,
        exact_expression_matches_world=exact_expression,
        expression_abstention=storage_matches and not expressed,
        multi_link_superposition=(
            expected_world_target in expressed and len(expressed) > 1
        ),
        storage_failure=dominant is not None and not storage_matches,
    )


def canonical_temporal_counterfactuals() -> dict[str, BranchCompetitionDiagnosis]:
    """Development-only counterfactuals; no candidate world is executed."""

    stable = (5.0, 5.0, 5.0, 5.0)
    dispersed_main = (3.0, 7.0, 3.0, 7.0, 5.0)
    dispersed_alt = (3.0, 7.0, 3.0, 7.0)
    main_stable = (5.0, 5.0, 5.0, 5.0, 5.0)
    return {
        "aligned": diagnose_branch_competition(
            (
                BranchObservation("main", 5, main_stable, 1.0),
                BranchObservation("alternate", 4, dispersed_alt, 0.0),
            ),
            variance_scale_ms2=4.0,
        ),
        "decoupled": diagnose_branch_competition(
            (
                BranchObservation("main", 5, dispersed_main, 1.0),
                BranchObservation("alternate", 4, stable, 0.0),
            ),
            variance_scale_ms2=4.0,
        ),
        "equal_variance": diagnose_branch_competition(
            (
                BranchObservation("main", 5, main_stable, 1.0),
                BranchObservation("alternate", 4, stable, 0.0),
            ),
            variance_scale_ms2=4.0,
        ),
    }


def canonical_relation_counterfactuals() -> dict[str, RelationExpressionDiagnosis]:
    threshold = 0.5
    gain = threshold / 0.60
    return {
        "correct_but_abstains": diagnose_relation_expression(
            (RelationLinkObservation("current", 4, 4),),
            expected_world_target="current",
            field_threshold=threshold,
            relation_reentry_gain=gain,
        ),
        "multi_link_superposition": diagnose_relation_expression(
            (
                RelationLinkObservation("current", 5, 2),
                RelationLinkObservation("old", 4, 2),
            ),
            expected_world_target="current",
            field_threshold=threshold,
            relation_reentry_gain=gain,
        ),
        "hysteresis": diagnose_relation_expression(
            (
                RelationLinkObservation("current", 3, 3),
                RelationLinkObservation("old", 5, 2),
            ),
            expected_world_target="current",
            field_threshold=threshold,
            relation_reentry_gain=gain,
        ),
    }

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace
from typing import Any

from .v061_temporal_functional_decoupling import (
    BranchCompetitionDiagnosis,
    BranchObservation,
    RelationExpressionDiagnosis,
    RelationLinkObservation,
    diagnose_branch_competition,
    diagnose_relation_expression,
)


@dataclass(frozen=True, slots=True)
class LagAssignmentPermutationExperiment:
    assignment_a: BranchCompetitionDiagnosis
    assignment_b: BranchCompetitionDiagnosis
    total_lag_multiset_a: tuple[float, ...]
    total_lag_multiset_b: tuple[float, ...]
    total_evidence_preserved: bool
    world_consistency_winner_preserved: bool
    g1_selection_flipped: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "assignment_a": self.assignment_a.state_dict(),
            "assignment_b": self.assignment_b.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class ConsequencePermutationExperiment:
    original: BranchCompetitionDiagnosis
    permuted: BranchCompetitionDiagnosis
    local_transition_evidence_identical: bool
    g1_selection_unchanged: bool
    world_consistency_winner_changed: bool
    missing_world_to_transition_feedback: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "original": self.original.state_dict(),
            "permuted": self.permuted.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class StorageExpressionCrossExperiment:
    high_threshold: RelationExpressionDiagnosis
    low_threshold: RelationExpressionDiagnosis
    stored_state_identical: bool
    dominant_relation_identical: bool
    expression_changed: bool
    expression_bottleneck_demonstrated: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "high_threshold": self.high_threshold.state_dict(),
            "low_threshold": self.low_threshold.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class AmbiguityExperiment:
    diagnosis: BranchCompetitionDiagnosis
    co_maximal_branches: tuple[str, ...]
    exact_confidence_tie: bool
    evaluator_singleton_is_only_tie_break: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "diagnosis": self.diagnosis.state_dict(),
        }


def run_lag_assignment_permutation() -> LagAssignmentPermutationExperiment:
    """Permute lag ownership while preserving counts, lag multiset, and function."""

    main_dispersed = (3.0, 7.0, 3.0, 7.0, 5.0)
    alternate_stable = (5.0, 5.0, 5.0, 5.0)
    main_stable = (5.0, 5.0, 5.0, 5.0, 5.0)
    alternate_dispersed = (3.0, 7.0, 3.0, 7.0)
    assignment_a_observations = (
        BranchObservation("main", 5, main_dispersed, 1.0),
        BranchObservation("alternate", 4, alternate_stable, 0.0),
    )
    assignment_b_observations = (
        BranchObservation("main", 5, main_stable, 1.0),
        BranchObservation("alternate", 4, alternate_dispersed, 0.0),
    )
    assignment_a = diagnose_branch_competition(
        assignment_a_observations,
        variance_scale_ms2=4.0,
    )
    assignment_b = diagnose_branch_competition(
        assignment_b_observations,
        variance_scale_ms2=4.0,
    )
    multiset_a = tuple(
        sorted(value for row in assignment_a_observations for value in row.lags_ms)
    )
    multiset_b = tuple(
        sorted(value for row in assignment_b_observations for value in row.lags_ms)
    )
    return LagAssignmentPermutationExperiment(
        assignment_a=assignment_a,
        assignment_b=assignment_b,
        total_lag_multiset_a=multiset_a,
        total_lag_multiset_b=multiset_b,
        total_evidence_preserved=(
            multiset_a == multiset_b
            and tuple(row.exposure_count for row in assignment_a_observations)
            == tuple(row.exposure_count for row in assignment_b_observations)
        ),
        world_consistency_winner_preserved=(
            assignment_a.selected_by_world_consistency
            == assignment_b.selected_by_world_consistency
            == "main"
        ),
        g1_selection_flipped=(
            assignment_a.selected_by_g1 != assignment_b.selected_by_g1
        ),
    )


def run_consequence_permutation() -> ConsequencePermutationExperiment:
    """Change only observer-side world relation after local transition learning."""

    local = (
        BranchObservation("main", 5, (3.0, 7.0, 3.0, 7.0, 5.0), 1.0),
        BranchObservation("alternate", 4, (5.0, 5.0, 5.0, 5.0), 0.0),
    )
    original = diagnose_branch_competition(local, variance_scale_ms2=4.0)
    permuted_observations = tuple(
        replace(
            row,
            world_consistency=(0.0 if row.branch_id == "main" else 1.0),
        )
        for row in local
    )
    permuted = diagnose_branch_competition(
        permuted_observations,
        variance_scale_ms2=4.0,
    )
    local_identical = all(
        (
            left.branch_id,
            left.exposure_count,
            left.lags_ms,
        )
        == (
            right.branch_id,
            right.exposure_count,
            right.lags_ms,
        )
        for left, right in zip(local, permuted_observations, strict=True)
    )
    selection_unchanged = original.selected_by_g1 == permuted.selected_by_g1
    world_changed = (
        original.selected_by_world_consistency
        != permuted.selected_by_world_consistency
    )
    return ConsequencePermutationExperiment(
        original=original,
        permuted=permuted,
        local_transition_evidence_identical=local_identical,
        g1_selection_unchanged=selection_unchanged,
        world_consistency_winner_changed=world_changed,
        missing_world_to_transition_feedback=(
            local_identical and selection_unchanged and world_changed
        ),
    )


def run_storage_expression_cross() -> StorageExpressionCrossExperiment:
    """Hold relation storage fixed while changing only Field expression demand."""

    links = (RelationLinkObservation("current", 4, 4),)
    high = diagnose_relation_expression(
        links,
        expected_world_target="current",
        field_threshold=0.50,
        relation_reentry_gain=0.50 / 0.60,
    )
    low = diagnose_relation_expression(
        links,
        expected_world_target="current",
        field_threshold=0.40,
        relation_reentry_gain=0.50 / 0.60,
    )
    storage_identical = all(
        math.isclose(left.reliability, right.reliability)
        and left.target == right.target
        for left, right in zip(high.scores, low.scores, strict=True)
    )
    dominant_identical = high.dominant_target == low.dominant_target == "current"
    expression_changed = high.expressed_targets != low.expressed_targets
    return StorageExpressionCrossExperiment(
        high_threshold=high,
        low_threshold=low,
        stored_state_identical=storage_identical,
        dominant_relation_identical=dominant_identical,
        expression_changed=expression_changed,
        expression_bottleneck_demonstrated=(
            storage_identical
            and dominant_identical
            and expression_changed
            and high.expression_abstention
            and low.exact_expression_matches_world
        ),
    )


def run_ambiguity_experiment() -> AmbiguityExperiment:
    observations = (
        BranchObservation("branch-a", 4, (5.0, 5.0, 5.0, 5.0), 0.5),
        BranchObservation("branch-b", 4, (5.0, 5.0, 5.0, 5.0), 0.5),
    )
    diagnosis = diagnose_branch_competition(
        observations,
        variance_scale_ms2=4.0,
    )
    maximum = max(row.g1_confidence for row in diagnosis.scores)
    co_maximal = tuple(
        sorted(
            row.branch_id
            for row in diagnosis.scores
            if math.isclose(
                row.g1_confidence,
                maximum,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )
    )
    return AmbiguityExperiment(
        diagnosis=diagnosis,
        co_maximal_branches=co_maximal,
        exact_confidence_tie=len(co_maximal) > 1,
        evaluator_singleton_is_only_tie_break=(
            len(co_maximal) > 1 and diagnosis.selected_by_g1 == co_maximal[0]
        ),
    )


def build_discriminator_report() -> dict[str, Any]:
    lag = run_lag_assignment_permutation()
    consequence = run_consequence_permutation()
    cross = run_storage_expression_cross()
    ambiguity = run_ambiguity_experiment()
    return {
        "candidate_reexecuted": False,
        "runtime_modified": False,
        "lag_assignment_permutation": lag.state_dict(),
        "consequence_permutation": consequence.state_dict(),
        "storage_expression_cross": cross.state_dict(),
        "ambiguity": ambiguity.state_dict(),
        "supported_diagnostic_inferences": {
            "lag_assignment_is_causal_for_g1_selection": (
                lag.total_evidence_preserved
                and lag.world_consistency_winner_preserved
                and lag.g1_selection_flipped
            ),
            "world_consistency_does_not_enter_current_g1_selection": (
                consequence.missing_world_to_transition_feedback
            ),
            "relation_storage_and_field_expression_are_separable": (
                cross.expression_bottleneck_demonstrated
            ),
            "equal_local_evidence_does_not_define_a_unique_internal_winner": (
                ambiguity.exact_confidence_tie
            ),
        },
    }

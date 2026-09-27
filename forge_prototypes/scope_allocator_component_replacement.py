from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import exp, isfinite, log, pi
from typing import Any

from forge_prototypes.hypothesis_revision_overlay import RevisionOverlayConfig
from forge_prototypes.managed_scope_hypothesis_revision import (
    ManagedScopeHypothesisRevisionOverlay,
)
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)
from forge_prototypes.scope_revision_boundary_stress import (
    ScopeRevisionStressCase,
    run_scope_revision_stress_probe,
    stress_cases,
)


@dataclass(frozen=True, slots=True)
class GaussianMixtureAllocatorConfig:
    component_count: int = 2
    max_iterations: int = 64
    convergence_tolerance: float = 1e-9
    variance_floor: float = 0.0025
    minimum_component_weight: float = 0.10
    minimum_assignment_mass: float = 0.80
    minimum_assignment_margin: float = 0.35
    minimum_seed_separation: float = 1e-9

    def __post_init__(self) -> None:
        if self.component_count != 2:
            raise ValueError("this bounded reference comparator requires two components")
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be positive")
        if self.convergence_tolerance <= 0.0:
            raise ValueError("convergence_tolerance must be positive")
        if self.variance_floor <= 0.0:
            raise ValueError("variance_floor must be positive")
        if not 0.0 < self.minimum_component_weight < 0.5:
            raise ValueError("minimum_component_weight must be in (0, 0.5)")
        if not 0.5 <= self.minimum_assignment_mass <= 1.0:
            raise ValueError("minimum_assignment_mass must be in [0.5, 1]")
        if not 0.0 <= self.minimum_assignment_margin <= 1.0:
            raise ValueError("minimum_assignment_margin must be in [0, 1]")
        if self.minimum_seed_separation < 0.0:
            raise ValueError("minimum_seed_separation must be non-negative")


@dataclass(frozen=True, slots=True)
class GaussianMixtureFit:
    centroids: tuple[tuple[float, ...], ...]
    variances: tuple[float, ...]
    weights: tuple[float, ...]
    iterations: int
    converged: bool
    identifiable: bool
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ReferenceRouting:
    scope_token: str | None
    posterior_mass: float
    posterior_margin: float
    abstained: bool
    reason: str


@dataclass(frozen=True, slots=True)
class ReferenceQuery:
    label: str
    scope_token: str | None
    selected_value: str | None
    abstained: bool
    routing_reason: str
    posterior_mass: float
    posterior_margin: float


@dataclass(frozen=True, slots=True)
class ComponentReplacementOutcome:
    case_id: str
    fit: GaussianMixtureFit
    committed_events: int
    scope_tokens: tuple[str, ...]
    queries: tuple[ReferenceQuery, ...]
    classification: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "fit": self.fit.as_dict(),
            "committed_events": self.committed_events,
            "scope_tokens": list(self.scope_tokens),
            "queries": [asdict(query) for query in self.queries],
            "classification": self.classification,
        }


@dataclass(frozen=True, slots=True)
class ScopeAllocatorComponentReplacementReport:
    fixed_radius_scope_tokens: tuple[str, ...]
    fixed_radius_b_query_abstained: bool
    outcomes: tuple[ComponentReplacementOutcome, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "fixed_radius_scope_tokens": list(self.fixed_radius_scope_tokens),
            "fixed_radius_b_query_abstained": self.fixed_radius_b_query_abstained,
            "outcomes": [outcome.as_dict() for outcome in self.outcomes],
        }


class GaussianMixtureReferenceAllocator:
    """Small batch Gaussian-mixture reference allocator.

    The model receives observations only.  It deliberately fixes K=2 and uses
    the complete bounded stream before routing, so it is an established
    component-replacement diagnostic rather than an online-system competitor.
    """

    def __init__(self, config: GaussianMixtureAllocatorConfig | None = None) -> None:
        self.config = config or GaussianMixtureAllocatorConfig()
        self.fit_result: GaussianMixtureFit | None = None

    @staticmethod
    def _vector(observation: Sequence[float]) -> tuple[float, ...]:
        if isinstance(observation, (str, bytes)):
            raise ValueError("observation must be a non-empty numeric vector")
        vector = tuple(float(value) for value in observation)
        if not vector or not all(isfinite(value) for value in vector):
            raise ValueError("observation must be a non-empty finite numeric vector")
        return vector

    @staticmethod
    def _squared_distance(left: Sequence[float], right: Sequence[float]) -> float:
        return sum((a - b) ** 2 for a, b in zip(left, right, strict=True))

    @staticmethod
    def _mean(vectors: Sequence[Sequence[float]]) -> tuple[float, ...]:
        return tuple(
            sum(row[index] for row in vectors) / len(vectors)
            for index in range(len(vectors[0]))
        )

    def _log_density(
        self,
        vector: Sequence[float],
        centroid: Sequence[float],
        variance: float,
        weight: float,
    ) -> float:
        dimension = len(vector)
        return (
            log(max(weight, 1e-300))
            - 0.5 * dimension * log(2.0 * pi * variance)
            - self._squared_distance(vector, centroid) / (2.0 * variance)
        )

    @staticmethod
    def _softmax_pair(left: float, right: float) -> tuple[float, float]:
        maximum = max(left, right)
        left_weight = exp(left - maximum)
        right_weight = exp(right - maximum)
        total = left_weight + right_weight
        return left_weight / total, right_weight / total

    def fit(self, observations: Sequence[Sequence[float]]) -> GaussianMixtureFit:
        vectors = tuple(self._vector(row) for row in observations)
        if len(vectors) < 2:
            raise ValueError("at least two observations are required")
        dimension = len(vectors[0])
        if any(len(row) != dimension for row in vectors):
            raise ValueError("observation dimension changed")

        seed_left, seed_right = max(
            (
                (left, right)
                for left in vectors
                for right in vectors
            ),
            key=lambda pair: self._squared_distance(pair[0], pair[1]),
        )
        if self._squared_distance(seed_left, seed_right) <= self.config.minimum_seed_separation**2:
            mean = self._mean(vectors)
            result = GaussianMixtureFit(
                centroids=(mean,),
                variances=(self.config.variance_floor,),
                weights=(1.0,),
                iterations=0,
                converged=True,
                identifiable=False,
                reason="observations_do_not_support_two_distinct_components",
            )
            self.fit_result = result
            return result

        centroids = [tuple(seed_left), tuple(seed_right)]
        if centroids[1] < centroids[0]:
            centroids.reverse()
        overall = self._mean(vectors)
        initial_variance = max(
            self.config.variance_floor,
            sum(self._squared_distance(row, overall) for row in vectors)
            / (len(vectors) * dimension),
        )
        variances = [initial_variance, initial_variance]
        weights = [0.5, 0.5]
        converged = False
        iterations = 0

        for iteration in range(1, self.config.max_iterations + 1):
            responsibilities = [
                self._softmax_pair(
                    self._log_density(row, centroids[0], variances[0], weights[0]),
                    self._log_density(row, centroids[1], variances[1], weights[1]),
                )
                for row in vectors
            ]
            masses = [sum(row[index] for row in responsibilities) for index in range(2)]
            if any(mass / len(vectors) < self.config.minimum_component_weight for mass in masses):
                result = GaussianMixtureFit(
                    centroids=tuple(centroids),
                    variances=tuple(variances),
                    weights=tuple(weights),
                    iterations=iteration,
                    converged=False,
                    identifiable=False,
                    reason="component_weight_below_floor",
                )
                self.fit_result = result
                return result

            updated_centroids = [
                tuple(
                    sum(
                        responsibilities[row_index][component] * row[axis]
                        for row_index, row in enumerate(vectors)
                    )
                    / masses[component]
                    for axis in range(dimension)
                )
                for component in range(2)
            ]
            updated_variances = [
                max(
                    self.config.variance_floor,
                    sum(
                        responsibilities[row_index][component]
                        * self._squared_distance(row, updated_centroids[component])
                        for row_index, row in enumerate(vectors)
                    )
                    / (masses[component] * dimension),
                )
                for component in range(2)
            ]
            updated_weights = [mass / len(vectors) for mass in masses]
            movement = max(
                self._squared_distance(before, after)
                for before, after in zip(centroids, updated_centroids, strict=True)
            )
            centroids = updated_centroids
            variances = updated_variances
            weights = updated_weights
            iterations = iteration
            if movement <= self.config.convergence_tolerance**2:
                converged = True
                break

        order = sorted(range(2), key=lambda index: centroids[index])
        result = GaussianMixtureFit(
            centroids=tuple(centroids[index] for index in order),
            variances=tuple(variances[index] for index in order),
            weights=tuple(weights[index] for index in order),
            iterations=iterations,
            converged=converged,
            identifiable=True,
            reason="two_component_batch_reference_fit",
        )
        self.fit_result = result
        return result

    def route(self, observation: Sequence[float]) -> ReferenceRouting:
        vector = self._vector(observation)
        fit = self.fit_result
        if fit is None:
            raise RuntimeError("fit must be called before route")
        if not fit.identifiable:
            return ReferenceRouting(None, 0.5, 0.0, True, fit.reason)
        if len(vector) != len(fit.centroids[0]):
            raise ValueError("observation dimension changed")
        posterior = self._softmax_pair(
            self._log_density(vector, fit.centroids[0], fit.variances[0], fit.weights[0]),
            self._log_density(vector, fit.centroids[1], fit.variances[1], fit.weights[1]),
        )
        ranking = sorted(enumerate(posterior), key=lambda row: (-row[1], row[0]))
        best_index, best_mass = ranking[0]
        margin = best_mass - ranking[1][1]
        ambiguous = (
            best_mass < self.config.minimum_assignment_mass
            or margin < self.config.minimum_assignment_margin
        )
        return ReferenceRouting(
            None if ambiguous else f"gmm-scope-{best_index + 1:08d}",
            best_mass,
            margin,
            ambiguous,
            "ambiguous_component_posterior" if ambiguous else "selected_component",
        )


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


def _run_reference_case(case: ScopeRevisionStressCase) -> ComponentReplacementOutcome:
    allocator = GaussianMixtureReferenceAllocator()
    fit = allocator.fit(tuple(event.observation for event in case.events))
    overlay = ManagedScopeHypothesisRevisionOverlay(RevisionOverlayConfig())
    base = _base_prediction()
    committed = 0
    tokens: set[str] = set()
    for event in case.events:
        route = allocator.route(event.observation)
        if route.scope_token is None:
            continue
        overlay.apply_evidence(
            base,
            scope_token=route.scope_token,
            value=event.observed_value,
            strength=event.strength,
        )
        tokens.add(route.scope_token)
        committed += 1

    queries: list[ReferenceQuery] = []
    for label, observation, _reference_value in case.queries:
        route = allocator.route(observation)
        revision = (
            None
            if route.scope_token is None
            else overlay.evaluate(base, scope_token=route.scope_token)
        )
        queries.append(
            ReferenceQuery(
                label=label,
                scope_token=route.scope_token,
                selected_value=None if revision is None else revision.selected_value,
                abstained=True if revision is None else revision.abstained,
                routing_reason=route.reason,
                posterior_mass=route.posterior_mass,
                posterior_margin=route.posterior_margin,
            )
        )

    by_label = {query.label: query for query in queries}
    if case.case_id == "within_reuse_radius_collision" and (
        by_label["qa"].selected_value == "A"
        and by_label["qb"].selected_value == "B"
        and by_label["midpoint"].abstained
    ):
        classification = "ESTABLISHED_BATCH_ALLOCATOR_RESOLVES_FIXED_RADIUS_COLLISION"
    elif not fit.identifiable and all(query.abstained for query in queries):
        classification = "OBSERVATIONS_IDENTICAL_REFERENCE_ALLOCATOR_FAILS_CLOSED"
    else:
        classification = "UNCLASSIFIED_COMPONENT_REPLACEMENT_OBSERVATION"
    return ComponentReplacementOutcome(
        case_id=case.case_id,
        fit=fit,
        committed_events=committed,
        scope_tokens=tuple(sorted(tokens)),
        queries=tuple(queries),
        classification=classification,
    )


def run_scope_allocator_component_replacement_probe() -> ScopeAllocatorComponentReplacementReport:
    boundary = {
        row.case_id: row for row in run_scope_revision_stress_probe().outcomes
    }["within_reuse_radius_collision"]
    boundary_queries = {query.label: query for query in boundary.queries}
    close_case = next(
        row for row in stress_cases() if row.case_id == "within_reuse_radius_collision"
    )
    close_case = ScopeRevisionStressCase(
        close_case.case_id,
        close_case.events,
        close_case.queries + (("midpoint", (0.25,), "A"),),
    )
    identical_case = ScopeRevisionStressCase(
        "identical_observation_conflicting_labels",
        (
            close_case.events[0].__class__("a1", (0.0,), "A"),
            close_case.events[0].__class__("b1", (0.0,), "B"),
            close_case.events[0].__class__("a2", (0.0,), "A"),
            close_case.events[0].__class__("b2", (0.0,), "B"),
        ),
        (("same", (0.0,), "A"),),
    )
    return ScopeAllocatorComponentReplacementReport(
        fixed_radius_scope_tokens=boundary.full_scope_tokens,
        fixed_radius_b_query_abstained=boundary_queries["qb"].full_abstained,
        outcomes=tuple(_run_reference_case(case) for case in (close_case, identical_case)),
    )


__all__ = [
    "ComponentReplacementOutcome",
    "GaussianMixtureAllocatorConfig",
    "GaussianMixtureFit",
    "GaussianMixtureReferenceAllocator",
    "ReferenceQuery",
    "ReferenceRouting",
    "ScopeAllocatorComponentReplacementReport",
    "run_scope_allocator_component_replacement_probe",
]

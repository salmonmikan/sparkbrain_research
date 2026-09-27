from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import isfinite, sqrt
from typing import Any

from forge_prototypes.hypothesis_revision_overlay import RevisionOverlayConfig
from forge_prototypes.managed_scope_hypothesis_revision import (
    ManagedScopeHypothesisRevisionOverlay,
)
from forge_prototypes.multi_hypothesis_prediction_pool import (
    PredictionPoolSnapshot,
    WeightedHypothesis,
)


@dataclass(frozen=True, slots=True)
class CausalOnlineRouterConfig:
    birth_distance: float = 0.25
    maximum_assignment_distance: float = 0.25
    minimum_distance_margin: float = 0.05
    max_components: int = 2

    def __post_init__(self) -> None:
        if self.birth_distance <= 0.0:
            raise ValueError("birth_distance must be positive")
        if self.maximum_assignment_distance <= 0.0:
            raise ValueError("maximum_assignment_distance must be positive")
        if self.minimum_distance_margin < 0.0:
            raise ValueError("minimum_distance_margin must be non-negative")
        if self.max_components != 2:
            raise ValueError("this bounded probe requires exactly two components")


@dataclass(frozen=True, slots=True)
class OnlineComponent:
    scope_token: str
    centroid: tuple[float, ...]
    count: int


@dataclass(frozen=True, slots=True)
class CausalRouting:
    scope_token: str | None
    action: str
    abstained: bool
    reason: str
    nearest_distance: float | None
    distance_margin: float | None


@dataclass(frozen=True, slots=True)
class StreamQuery:
    label: str
    scope_token: str | None
    selected_value: str | None
    abstained: bool
    routing_reason: str


@dataclass(frozen=True, slots=True)
class CausalStreamOutcome:
    stream_id: str
    committed_events: int
    rejected_events: int
    components: tuple[OnlineComponent, ...]
    queries: tuple[StreamQuery, ...]
    classification: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "stream_id": self.stream_id,
            "committed_events": self.committed_events,
            "rejected_events": self.rejected_events,
            "components": [asdict(row) for row in self.components],
            "queries": [asdict(row) for row in self.queries],
            "classification": self.classification,
        }


@dataclass(frozen=True, slots=True)
class CausalOnlineScopeRouterReport:
    outcomes: tuple[CausalStreamOutcome, ...]
    prefix_state_equal_before_divergent_suffix: bool
    prefix_action_equal_before_divergent_suffix: bool
    future_context_used: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "outcomes": [row.as_dict() for row in self.outcomes],
            "prefix_state_equal_before_divergent_suffix": (
                self.prefix_state_equal_before_divergent_suffix
            ),
            "prefix_action_equal_before_divergent_suffix": (
                self.prefix_action_equal_before_divergent_suffix
            ),
            "future_context_used": self.future_context_used,
        }


class CausalOnlineScopeRouter:
    """Bounded streaming two-centroid router with fail-closed rejection.

    Every decision uses only the current observation and state accumulated from
    earlier observations. Labels and evaluator identity are deliberately absent
    from the API. This is ordinary online clustering, not a scientific model.
    """

    def __init__(self, config: CausalOnlineRouterConfig | None = None) -> None:
        self.config = config or CausalOnlineRouterConfig()
        self._components: list[OnlineComponent] = []

    @staticmethod
    def _vector(observation: Sequence[float]) -> tuple[float, ...]:
        if isinstance(observation, (str, bytes)):
            raise TypeError("observation must be a non-empty numeric vector")
        vector = tuple(float(value) for value in observation)
        if not vector or not all(isfinite(value) for value in vector):
            raise ValueError("observation must be a non-empty finite numeric vector")
        return vector

    @staticmethod
    def _distance(left: Sequence[float], right: Sequence[float]) -> float:
        return sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=True)))

    @property
    def components(self) -> tuple[OnlineComponent, ...]:
        return tuple(self._components)

    def _validate_dimension(self, vector: Sequence[float]) -> None:
        if self._components and len(vector) != len(self._components[0].centroid):
            raise ValueError("observation dimension changed")

    def _create(self, vector: tuple[float, ...], action: str) -> CausalRouting:
        component = OnlineComponent(
            scope_token=f"online-scope-{len(self._components) + 1:08d}",
            centroid=vector,
            count=1,
        )
        self._components.append(component)
        return CausalRouting(component.scope_token, action, False, action, 0.0, None)

    def _rank(
        self, vector: Sequence[float]
    ) -> tuple[tuple[int, float], tuple[int, float] | None]:
        ranked = sorted(
            (
                (index, self._distance(vector, component.centroid))
                for index, component in enumerate(self._components)
            ),
            key=lambda row: (row[1], row[0]),
        )
        return ranked[0], None if len(ranked) == 1 else ranked[1]

    def route(self, observation: Sequence[float]) -> CausalRouting:
        vector = self._vector(observation)
        self._validate_dimension(vector)
        if not self._components:
            return CausalRouting(None, "abstained", True, "no_components", None, None)

        best, second = self._rank(vector)
        best_index, best_distance = best
        if best_distance > self.config.maximum_assignment_distance:
            return CausalRouting(
                None,
                "abstained",
                True,
                "observation_outside_component_support",
                best_distance,
                None if second is None else second[1] - best_distance,
            )
        if second is not None:
            margin = second[1] - best_distance
            if margin < self.config.minimum_distance_margin:
                return CausalRouting(
                    None,
                    "abstained",
                    True,
                    "ambiguous_nearest_components",
                    best_distance,
                    margin,
                )
        else:
            margin = None
        return CausalRouting(
            self._components[best_index].scope_token,
            "selected_existing",
            False,
            "selected_nearest_component",
            best_distance,
            margin,
        )

    def observe(self, observation: Sequence[float]) -> CausalRouting:
        vector = self._vector(observation)
        self._validate_dimension(vector)
        if not self._components:
            return self._create(vector, "created_initial_component")

        best, second = self._rank(vector)
        best_index, best_distance = best
        if len(self._components) < self.config.max_components:
            if best_distance >= self.config.birth_distance:
                return self._create(vector, "created_second_component")
        else:
            if best_distance > self.config.maximum_assignment_distance:
                return CausalRouting(
                    None,
                    "abstained",
                    True,
                    "component_capacity_exhausted_out_of_support",
                    best_distance,
                    second[1] - best_distance if second is not None else None,
                )
            if second is not None:
                margin = second[1] - best_distance
                if margin < self.config.minimum_distance_margin:
                    return CausalRouting(
                        None,
                        "abstained",
                        True,
                        "ambiguous_nearest_components",
                        best_distance,
                        margin,
                    )

        component = self._components[best_index]
        count = component.count + 1
        centroid = tuple(
            old + (new - old) / count
            for old, new in zip(component.centroid, vector, strict=True)
        )
        self._components[best_index] = OnlineComponent(
            component.scope_token,
            centroid,
            count,
        )
        return CausalRouting(
            component.scope_token,
            "updated_existing_component",
            False,
            "selected_nearest_component",
            best_distance,
            None if second is None else second[1] - best_distance,
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "components": [asdict(row) for row in self._components],
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> CausalOnlineScopeRouter:
        result = cls(CausalOnlineRouterConfig(**state["config"]))
        rows = state.get("components", [])
        if len(rows) > result.config.max_components:
            raise ValueError("persisted component count exceeds capacity")
        for index, row in enumerate(rows, start=1):
            centroid = result._vector(row["centroid"])
            count = int(row["count"])
            token = str(row["scope_token"])
            if count < 1:
                raise ValueError("persisted component count must be positive")
            if token != f"online-scope-{index:08d}":
                raise ValueError("persisted component token sequence is invalid")
            if result._components and len(centroid) != len(
                result._components[0].centroid
            ):
                raise ValueError("persisted component dimension changed")
            result._components.append(OnlineComponent(token, centroid, count))
        return result


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


def _run_stream(
    stream_id: str,
    events: Sequence[tuple[tuple[float, ...], str]],
) -> CausalStreamOutcome:
    router = CausalOnlineScopeRouter()
    overlay = ManagedScopeHypothesisRevisionOverlay(RevisionOverlayConfig())
    base = _base_prediction()
    committed = 0
    rejected = 0
    for observation, value in events:
        route = router.observe(observation)
        if route.scope_token is None:
            rejected += 1
            continue
        overlay.apply_evidence(
            base,
            scope_token=route.scope_token,
            value=value,
        )
        committed += 1

    queries: list[StreamQuery] = []
    for label, observation in (
        ("qa", (0.025,)),
        ("qb", (0.425,)),
        ("midpoint", (0.225,)),
        ("out_of_support", (1.0,)),
    ):
        route = router.route(observation)
        revision = (
            None
            if route.scope_token is None
            else overlay.evaluate(base, scope_token=route.scope_token)
        )
        queries.append(
            StreamQuery(
                label,
                route.scope_token,
                None if revision is None else revision.selected_value,
                True if revision is None else revision.abstained,
                route.reason,
            )
        )

    by_label = {row.label: row for row in queries}
    if (
        by_label["qa"].selected_value == "A"
        and by_label["qb"].selected_value == "B"
        and by_label["midpoint"].abstained
        and by_label["out_of_support"].abstained
    ):
        classification = "CAUSAL_ONLINE_TWO_COMPONENT_ROUTING_RECOVERS_BOUNDED_A_B"
    elif len(router.components) == 1 and all(row.abstained for row in queries):
        classification = "IDENTICAL_OBSERVATIONS_COLLAPSE_REVISION_ABSTAINS"
    else:
        classification = "UNCLASSIFIED_CAUSAL_ONLINE_ROUTING_OBSERVATION"
    return CausalStreamOutcome(
        stream_id,
        committed,
        rejected,
        router.components,
        tuple(queries),
        classification,
    )


def run_causal_online_scope_router_probe() -> CausalOnlineScopeRouterReport:
    interleaved = (
        ((0.0,), "A"),
        ((0.45,), "B"),
        ((0.05,), "A"),
        ((0.40,), "B"),
    )
    blocked = (
        ((0.0,), "A"),
        ((0.05,), "A"),
        ((0.45,), "B"),
        ((0.40,), "B"),
    )
    reversed_interleaved = (
        ((0.45,), "B"),
        ((0.0,), "A"),
        ((0.40,), "B"),
        ((0.05,), "A"),
    )
    identical = (
        ((0.0,), "A"),
        ((0.0,), "B"),
        ((0.0,), "A"),
        ((0.0,), "B"),
    )

    left = CausalOnlineScopeRouter()
    right = CausalOnlineScopeRouter()
    left_actions: list[CausalRouting] = []
    right_actions: list[CausalRouting] = []
    shared_prefix = ((0.0,), (0.45,), (0.05,))
    for observation in shared_prefix:
        left_actions.append(left.observe(observation))
        right_actions.append(right.observe(observation))
    prefix_state_equal = left.state_dict() == right.state_dict()
    prefix_action_equal = left_actions == right_actions
    left.observe((0.40,))
    right.observe((0.02,))

    return CausalOnlineScopeRouterReport(
        outcomes=tuple(
            _run_stream(stream_id, events)
            for stream_id, events in (
                ("interleaved", interleaved),
                ("blocked", blocked),
                ("reversed_interleaved", reversed_interleaved),
                ("identical_observations", identical),
            )
        ),
        prefix_state_equal_before_divergent_suffix=prefix_state_equal,
        prefix_action_equal_before_divergent_suffix=prefix_action_equal,
        future_context_used=False,
    )


__all__ = [
    "CausalOnlineRouterConfig",
    "CausalOnlineScopeRouter",
    "CausalOnlineScopeRouterReport",
    "CausalRouting",
    "CausalStreamOutcome",
    "OnlineComponent",
    "StreamQuery",
    "run_causal_online_scope_router_probe",
]

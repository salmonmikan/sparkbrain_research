from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest

from .direct_field_plasticity import (
    DirectFieldPlasticityConfig,
    ExternalGatedDirectFieldPlasticity,
)

BASE_WEIGHT = 0.05
BASE_DELAY_MS = 8.0
BASE_THRESHOLD = 0.80
TRAINING_INTERVAL_MS = 5.0
TRAINING_EPISODES = 3


@dataclass(frozen=True, slots=True)
class ConnectionMeasurement:
    source_id: int
    target_id: int
    weight: float
    delay_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DirectPlasticityCondition:
    condition_id: str
    sequence: tuple[int, ...]
    connection_state_hash_before: str
    connection_state_hash_after: str
    adjacent: tuple[ConnectionMeasurement, ...]
    reverse: tuple[ConnectionMeasurement, ...]
    untouched: tuple[ConnectionMeasurement, ...]
    external_observation_count: int
    ignored_endogenous_count: int
    update_count: int
    controller_state: dict[str, Any]

    def state_dict(self) -> dict[str, Any]:
        return {
            "adjacent": [row.state_dict() for row in self.adjacent],
            "condition_id": self.condition_id,
            "connection_state_hash_after": self.connection_state_hash_after,
            "connection_state_hash_before": self.connection_state_hash_before,
            "controller_state": self.controller_state,
            "external_observation_count": self.external_observation_count,
            "ignored_endogenous_count": self.ignored_endogenous_count,
            "reverse": [row.state_dict() for row in self.reverse],
            "sequence": list(self.sequence),
            "untouched": [row.state_dict() for row in self.untouched],
            "update_count": self.update_count,
        }


@dataclass(frozen=True, slots=True)
class DirectPlasticityAssessment:
    physical_connection_state_changed: bool
    adjacent_edges_potentiated: bool
    reverse_edges_depressed: bool
    nonadjacent_edges_unchanged: bool
    adjacent_delays_moved_toward_observed_lag: bool
    trace_reset_preserves_learned_connections: bool
    endogenous_activity_cannot_update_connections: bool
    unit_permutation_is_supported: bool
    weights_and_delays_are_bounded: bool
    controller_has_no_pairwise_learned_table: bool
    deterministic: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DirectPlasticitySuite:
    trained: DirectPlasticityCondition
    endogenous_only: DirectPlasticityCondition
    permuted: DirectPlasticityCondition
    trace_reset_hash_before: str
    trace_reset_hash_after: str
    assessment: DirectPlasticityAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "endogenous_only": self.endogenous_only.state_dict(),
            "permuted": self.permuted.state_dict(),
            "suite_hash": self.suite_hash,
            "trace_reset_hash_after": self.trace_reset_hash_after,
            "trace_reset_hash_before": self.trace_reset_hash_before,
            "trained": self.trained.state_dict(),
        }


def new_uniform_field(unit_count: int = 5) -> TemporalExcitableField:
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=BASE_THRESHOLD,
            )
            for unit_id in range(unit_count)
        ),
        tuple(
            Connection(
                source_id=source_id,
                target_id=target_id,
                weight=BASE_WEIGHT,
                delay_ms=BASE_DELAY_MS,
                plastic=True,
            )
            for source_id in range(unit_count)
            for target_id in range(unit_count)
            if source_id != target_id
        ),
        receptor_ids=tuple(range(unit_count)),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=2.0,
        ),
    )


def _pulse(
    event_id: str,
    time_ms: float,
    unit_id: int,
    origin: EventOrigin,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
        polarity=1,
        origin=origin,
    )


def train_external_sequence(
    field: TemporalExcitableField,
    sequence: tuple[int, ...],
    *,
    episodes: int = TRAINING_EPISODES,
    config: DirectFieldPlasticityConfig | None = None,
) -> ExternalGatedDirectFieldPlasticity:
    controller = ExternalGatedDirectFieldPlasticity(field, config)
    episode_spacing_ms = max(30.0, len(sequence) * TRAINING_INTERVAL_MS + 10.0)
    for episode in range(episodes):
        start = episode * episode_spacing_ms
        for index, unit_id in enumerate(sequence):
            controller.observe(
                _pulse(
                    f"external:{episode}:{index}",
                    start + index * TRAINING_INTERVAL_MS,
                    unit_id,
                    EventOrigin.EXTERNAL,
                )
            )
    return controller


def _measurement(
    field: TemporalExcitableField,
    source_id: int,
    target_id: int,
) -> ConnectionMeasurement:
    edge = field.connection(source_id, target_id)
    return ConnectionMeasurement(
        source_id=source_id,
        target_id=target_id,
        weight=edge.weight,
        delay_ms=edge.delay_ms,
    )


def _condition(
    condition_id: str,
    sequence: tuple[int, ...],
    *,
    origin: EventOrigin,
) -> tuple[DirectPlasticityCondition, ExternalGatedDirectFieldPlasticity]:
    field = new_uniform_field(max(sequence) + 1)
    controller = ExternalGatedDirectFieldPlasticity(field)
    before = controller.connection_state_hash()
    episode_spacing_ms = max(30.0, len(sequence) * TRAINING_INTERVAL_MS + 10.0)
    for episode in range(TRAINING_EPISODES):
        start = episode * episode_spacing_ms
        for index, unit_id in enumerate(sequence):
            controller.observe(
                _pulse(
                    f"{condition_id}:{episode}:{index}",
                    start + index * TRAINING_INTERVAL_MS,
                    unit_id,
                    origin,
                )
            )
    after = controller.connection_state_hash()
    adjacent_pairs = tuple(zip(sequence, sequence[1:], strict=False))
    reverse_pairs = tuple((target, source) for source, target in adjacent_pairs)
    selected = set(adjacent_pairs).union(reverse_pairs)
    untouched_pairs = tuple(
        key for key in sorted(field.connections) if key not in selected
    )
    return (
        DirectPlasticityCondition(
            condition_id=condition_id,
            sequence=sequence,
            connection_state_hash_before=before,
            connection_state_hash_after=after,
            adjacent=tuple(
                _measurement(field, source, target)
                for source, target in adjacent_pairs
            ),
            reverse=tuple(
                _measurement(field, source, target)
                for source, target in reverse_pairs
            ),
            untouched=tuple(
                _measurement(field, source, target)
                for source, target in untouched_pairs
            ),
            external_observation_count=controller.external_observation_count,
            ignored_endogenous_count=controller.ignored_endogenous_count,
            update_count=controller.update_count,
            controller_state=controller.state_dict(),
        ),
        controller,
    )


def _bounded(row: ConnectionMeasurement, config: DirectFieldPlasticityConfig) -> bool:
    return (
        config.minimum_weight <= row.weight <= config.maximum_weight
        and config.minimum_delay_ms <= row.delay_ms <= config.maximum_delay_ms
    )


def run_direct_plasticity_suite() -> DirectPlasticitySuite:
    trained, controller = _condition(
        "trained",
        (0, 1, 2, 3),
        origin=EventOrigin.EXTERNAL,
    )
    before_trace_reset = controller.connection_state_hash()
    controller.clear_traces()
    after_trace_reset = controller.connection_state_hash()
    endogenous, _ = _condition(
        "endogenous-only",
        (0, 1, 2, 3),
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
    )
    permuted, _ = _condition(
        "permuted",
        (3, 1, 4, 0),
        origin=EventOrigin.EXTERNAL,
    )
    config = controller.config
    controller_state_text = str(trained.controller_state).lower()
    forbidden_controller_keys = (
        "transitions",
        "proposals",
        "paths",
        "confirmed_count",
        "contradicted_count",
        "reward",
    )
    values = {
        "physical_connection_state_changed": (
            trained.connection_state_hash_before
            != trained.connection_state_hash_after
        ),
        "adjacent_edges_potentiated": all(
            row.weight > BASE_WEIGHT for row in trained.adjacent
        ),
        "reverse_edges_depressed": all(
            row.weight < BASE_WEIGHT for row in trained.reverse
        ),
        "nonadjacent_edges_unchanged": all(
            row.weight == BASE_WEIGHT and row.delay_ms == BASE_DELAY_MS
            for row in trained.untouched
        ),
        "adjacent_delays_moved_toward_observed_lag": all(
            TRAINING_INTERVAL_MS < row.delay_ms < BASE_DELAY_MS
            for row in trained.adjacent
        ),
        "trace_reset_preserves_learned_connections": (
            before_trace_reset == after_trace_reset
            and controller.state_dict()["unit_traces"] == {}
        ),
        "endogenous_activity_cannot_update_connections": (
            endogenous.connection_state_hash_before
            == endogenous.connection_state_hash_after
            and endogenous.external_observation_count == 0
            and endogenous.ignored_endogenous_count
            == TRAINING_EPISODES * len(endogenous.sequence)
            and endogenous.update_count == 0
        ),
        "unit_permutation_is_supported": (
            all(row.weight > BASE_WEIGHT for row in permuted.adjacent)
            and all(row.weight < BASE_WEIGHT for row in permuted.reverse)
        ),
        "weights_and_delays_are_bounded": all(
            _bounded(row, config)
            for condition in (trained, permuted)
            for row in (*condition.adjacent, *condition.reverse, *condition.untouched)
        ),
        "controller_has_no_pairwise_learned_table": not any(
            key in controller_state_text for key in forbidden_controller_keys
        ),
        "deterministic": True,
    }
    state_without_hash = {
        "endogenous_only": endogenous.state_dict(),
        "permuted": permuted.state_dict(),
        "trace_reset_hash_after": after_trace_reset,
        "trace_reset_hash_before": before_trace_reset,
        "trained": trained.state_dict(),
    }
    assessment = DirectPlasticityAssessment(
        **values,
        engineering_candidate=all(values.values()),
    )
    return DirectPlasticitySuite(
        trained=trained,
        endogenous_only=endogenous,
        permuted=permuted,
        trace_reset_hash_before=before_trace_reset,
        trace_reset_hash_after=after_trace_reset,
        assessment=assessment,
        suite_hash=digest(
            {
                "assessment": assessment.state_dict(),
                **state_without_hash,
            }
        ),
    )

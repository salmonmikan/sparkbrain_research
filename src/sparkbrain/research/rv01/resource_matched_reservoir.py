from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest

from .interference_contract import (
    InterferencePhase,
    InterferenceWorldSpec,
    development_worlds,
    world_grid_hash,
)
from .interference_runner import (
    _MAXIMUM_PROBE_SPIKES,
    _directed_edges,
    _ordered_coverage,
    _route_map,
    run_interference_world,
)


@dataclass(frozen=True, slots=True)
class ResourceMatchedReservoirConfig:
    leak_rate: float = 0.80
    input_scale: float = 1.00
    recurrent_scale: float = 0.75
    readout_learning_rate: float = 0.25
    maximum_abs_readout_weight: float = 2.00
    seed_offset: int = 12001

    def validate(self) -> None:
        for name in (
            "leak_rate",
            "input_scale",
            "recurrent_scale",
            "readout_learning_rate",
            "maximum_abs_readout_weight",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if self.leak_rate > 1.0:
            raise ValueError("leak_rate must not exceed one")
        if self.seed_offset < 0:
            raise ValueError("seed_offset must be non-negative")


@dataclass(frozen=True, slots=True)
class ReservoirProbeRecord:
    world_id: str
    probe_route_id: str
    cue_unit_id: int
    expected_units: tuple[int, ...]
    generated_layers: tuple[tuple[int, ...], ...]
    generated_units: tuple[int, ...]
    ordered_retention_fraction: float
    exact_route_recovered: bool
    contamination_count: int
    first_hop_targets_generated: tuple[int, ...]
    structural_first_hop_targets: tuple[int, ...]
    first_hop_coverage_fraction: float
    generated_event_count: int
    halt_reason: str

    def validate(self) -> None:
        if not self.world_id or not self.probe_route_id:
            raise ValueError("probe identities must be non-empty")
        if not 0.0 <= self.ordered_retention_fraction <= 1.0:
            raise ValueError("ordered_retention_fraction must be in [0, 1]")
        if not 0.0 <= self.first_hop_coverage_fraction <= 1.0:
            raise ValueError("first_hop_coverage_fraction must be in [0, 1]")
        if self.contamination_count < 0 or self.generated_event_count < 0:
            raise ValueError("probe counts must be non-negative")
        if self.generated_event_count != len(self.generated_units):
            raise ValueError("generated event count does not match generated units")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ReservoirResourceMatch:
    field_unit_count: int
    reservoir_state_scalar_count: int
    directed_edge_count: int
    field_persistent_scalar_count: int
    reservoir_fixed_recurrent_scalar_count: int
    reservoir_learned_readout_scalar_count: int
    reservoir_persistent_scalar_count: int
    field_external_event_count: int
    reservoir_external_event_count: int
    reservoir_supervised_transition_count: int
    field_generated_event_budget_per_probe: int
    reservoir_generated_event_budget_per_probe: int
    field_active_outgoing_budget: int
    reservoir_active_output_budget: int
    exact_persistent_state_match: bool
    exact_external_event_match: bool
    matched_unit_state_count: bool
    matched_generation_budget: bool
    matched_active_output_budget: bool
    resource_match_passed: bool

    def validate(self) -> None:
        integer_fields = (
            "field_unit_count",
            "reservoir_state_scalar_count",
            "directed_edge_count",
            "field_persistent_scalar_count",
            "reservoir_fixed_recurrent_scalar_count",
            "reservoir_learned_readout_scalar_count",
            "reservoir_persistent_scalar_count",
            "field_external_event_count",
            "reservoir_external_event_count",
            "reservoir_supervised_transition_count",
            "field_generated_event_budget_per_probe",
            "reservoir_generated_event_budget_per_probe",
            "field_active_outgoing_budget",
            "reservoir_active_output_budget",
        )
        if any(getattr(self, name) < 0 for name in integer_fields):
            raise ValueError("resource counts must be non-negative")
        expected = all(
            (
                self.exact_persistent_state_match,
                self.exact_external_event_match,
                self.matched_unit_state_count,
                self.matched_generation_budget,
                self.matched_active_output_budget,
            )
        )
        if self.resource_match_passed != expected:
            raise ValueError("resource_match_passed is inconsistent")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ReservoirComparisonAssessment:
    field_mean_ordered_retention: float
    reservoir_mean_ordered_retention: float
    field_minus_reservoir_retention: float
    field_exact_route_count: int
    reservoir_exact_route_count: int
    field_contamination_count: int
    reservoir_contamination_count: int
    field_mean_first_hop_coverage: float
    reservoir_mean_first_hop_coverage: float
    reservoir_matches_or_exceeds_mean_retention: bool
    deterministic_replay_state_hash: bool
    deterministic_replay_probe_hash: bool
    no_training_replay: bool
    resource_match_passed: bool

    def validate(self, *, route_count: int) -> None:
        for value in (
            self.field_mean_ordered_retention,
            self.reservoir_mean_ordered_retention,
            self.field_mean_first_hop_coverage,
            self.reservoir_mean_first_hop_coverage,
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("comparison fractions must be finite and in [0, 1]")
        if not math.isfinite(self.field_minus_reservoir_retention):
            raise ValueError("retention delta must be finite")
        if not -1.0 <= self.field_minus_reservoir_retention <= 1.0:
            raise ValueError("retention delta must be in [-1, 1]")
        for value in (self.field_exact_route_count, self.reservoir_exact_route_count):
            if not 0 <= value <= route_count:
                raise ValueError("exact route count outside route count")
        if self.field_contamination_count < 0 or self.reservoir_contamination_count < 0:
            raise ValueError("contamination counts must be non-negative")
        expected = (
            self.reservoir_mean_ordered_retention
            >= self.field_mean_ordered_retention
        )
        if self.reservoir_matches_or_exceeds_mean_retention != expected:
            raise ValueError("retention comparison boolean is inconsistent")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ResourceMatchedReservoirWorldResult:
    world_id: str
    world_specification_hash: str
    comparator_config: ResourceMatchedReservoirConfig
    comparator_seed: int
    recurrent_state_hash: str
    replay_recurrent_state_hash: str
    probe_signature_hash: str
    replay_probe_signature_hash: str
    probes: tuple[ReservoirProbeRecord, ...]
    resources: ReservoirResourceMatch
    assessment: ReservoirComparisonAssessment
    semantic_hash: str

    def validate(self, world: InterferenceWorldSpec) -> None:
        if self.world_id != world.world_id:
            raise ValueError("reservoir result world identity mismatch")
        if self.world_specification_hash != world.specification_hash():
            raise ValueError("reservoir result world specification mismatch")
        self.comparator_config.validate()
        if len(self.probes) != world.route_count:
            raise ValueError("reservoir result must contain every final probe")
        if {row.probe_route_id for row in self.probes} != {
            route.route_id for route in world.routes
        }:
            raise ValueError("reservoir probe route coverage is incomplete")
        for row in self.probes:
            row.validate()
        self.resources.validate()
        self.assessment.validate(route_count=world.route_count)
        for value in (
            self.recurrent_state_hash,
            self.replay_recurrent_state_hash,
            self.probe_signature_hash,
            self.replay_probe_signature_hash,
            self.semantic_hash,
        ):
            if len(value) != 64:
                raise ValueError("reservoir hashes must be sha256 digests")

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "comparator_config": asdict(self.comparator_config),
            "comparator_seed": self.comparator_seed,
            "probe_signature_hash": self.probe_signature_hash,
            "probes": [row.state_dict() for row in self.probes],
            "recurrent_state_hash": self.recurrent_state_hash,
            "replay_probe_signature_hash": self.replay_probe_signature_hash,
            "replay_recurrent_state_hash": self.replay_recurrent_state_hash,
            "resources": self.resources.state_dict(),
            "semantic_hash": self.semantic_hash,
            "world_id": self.world_id,
            "world_specification_hash": self.world_specification_hash,
        }


@dataclass(frozen=True, slots=True)
class DevelopmentResourceMatchedReservoirSuite:
    world_grid_hash: str
    worlds: tuple[ResourceMatchedReservoirWorldResult, ...]
    suite_hash: str

    @property
    def world_count(self) -> int:
        return len(self.worlds)

    def state_dict(self) -> dict[str, Any]:
        return {
            "suite_hash": self.suite_hash,
            "world_count": self.world_count,
            "world_grid_hash": self.world_grid_hash,
            "worlds": [row.state_dict() for row in self.worlds],
        }


class ResourceMatchedSparseReservoir:
    """Topology-matched fixed recurrence with one-pass sparse online readout."""

    def __init__(
        self,
        *,
        unit_count: int,
        directed_edges: tuple[tuple[int, int], ...],
        maximum_active_outputs: int,
        seed: int,
        config: ResourceMatchedReservoirConfig | None = None,
    ) -> None:
        self.config = config or ResourceMatchedReservoirConfig()
        self.config.validate()
        if unit_count < 2:
            raise ValueError("unit_count must be at least two")
        if maximum_active_outputs < 1:
            raise ValueError("maximum_active_outputs must be positive")
        if not directed_edges:
            raise ValueError("resource-matched reservoir requires directed edges")
        if len(set(directed_edges)) != len(directed_edges):
            raise ValueError("directed_edges must be unique")
        if any(
            source < 0
            or target < 0
            or source >= unit_count
            or target >= unit_count
            or source == target
            for source, target in directed_edges
        ):
            raise ValueError("directed edge lies outside the anonymous unit space")
        self.unit_count = unit_count
        self.directed_edges = tuple(sorted(directed_edges))
        self.maximum_active_outputs = maximum_active_outputs
        self.seed = seed
        self._recurrent_weights = self._fixed_recurrent_weights()
        self._readout_weights = {edge: 0.0 for edge in self.directed_edges}
        self._incoming_recurrent: dict[int, tuple[tuple[int, float], ...]] = {}
        self._readout_sources: dict[int, tuple[int, ...]] = {}
        for target in range(unit_count):
            self._incoming_recurrent[target] = tuple(
                (source, self._recurrent_weights[(source, target)])
                for source, edge_target in self.directed_edges
                if edge_target == target
            )
            self._readout_sources[target] = tuple(
                source
                for source, edge_target in self.directed_edges
                if edge_target == target
            )
        self.observed_external_event_count = 0
        self.supervised_transition_count = 0
        self.parameter_update_count = 0
        self.generated_event_count = 0

    def _fixed_recurrent_weights(self) -> dict[tuple[int, int], float]:
        rng = random.Random(self.seed)
        raw = {edge: rng.uniform(-1.0, 1.0) for edge in self.directed_edges}
        row_sums: defaultdict[int, float] = defaultdict(float)
        for (_, target), weight in raw.items():
            row_sums[target] += abs(weight)
        maximum_row_sum = max(row_sums.values(), default=0.0)
        if maximum_row_sum <= 0.0:
            raise RuntimeError("deterministic recurrent substrate has no weight")
        scale = self.config.recurrent_scale / maximum_row_sum
        return {edge: weight * scale for edge, weight in raw.items()}

    def zero_state(self) -> tuple[float, ...]:
        return (0.0,) * self.unit_count

    def advance_many(
        self,
        state: tuple[float, ...],
        active_units: tuple[int, ...],
    ) -> tuple[float, ...]:
        if len(state) != self.unit_count:
            raise ValueError("reservoir state has the wrong size")
        if not active_units:
            raise ValueError("advance_many requires at least one active unit")
        if any(unit < 0 or unit >= self.unit_count for unit in active_units):
            raise ValueError("active unit lies outside reservoir")
        active = frozenset(active_units)
        values: list[float] = []
        for target in range(self.unit_count):
            recurrent = sum(
                weight * state[source]
                for source, weight in self._incoming_recurrent[target]
            )
            injected = self.config.input_scale if target in active else 0.0
            raw = math.tanh(injected + recurrent)
            values.append(
                (1.0 - self.config.leak_rate) * state[target]
                + self.config.leak_rate * raw
            )
        return tuple(values)

    def _scores(self, state: tuple[float, ...]) -> dict[int, float]:
        scores: dict[int, float] = {}
        for target, sources in self._readout_sources.items():
            if not sources:
                continue
            scores[target] = sum(
                state[source] * self._readout_weights[(source, target)]
                for source in sources
            )
        return scores

    @staticmethod
    def _softmax(scores: dict[int, float]) -> dict[int, float]:
        if not scores:
            raise RuntimeError("sparse reservoir has no readable target classes")
        maximum = max(scores.values())
        exponentials = {
            target: math.exp(score - maximum) for target, score in scores.items()
        }
        denominator = sum(exponentials.values())
        return {target: value / denominator for target, value in exponentials.items()}

    def _update_readout(self, state: tuple[float, ...], target_unit: int) -> None:
        scores = self._scores(state)
        if target_unit not in scores:
            raise RuntimeError("observed target is absent from matched readout topology")
        probabilities = self._softmax(scores)
        energy = 1.0 + sum(
            state[source] * state[source]
            for source, _ in self.directed_edges
        )
        for source, target in self.directed_edges:
            desired = 1.0 if target == target_unit else 0.0
            error = desired - probabilities[target]
            delta = (
                self.config.readout_learning_rate
                * error
                * state[source]
                / energy
            )
            current = self._readout_weights[(source, target)]
            bound = self.config.maximum_abs_readout_weight
            self._readout_weights[(source, target)] = min(
                bound,
                max(-bound, current + delta),
            )
            self.parameter_update_count += 1
        self.supervised_transition_count += 1

    def observe_sequence(self, sequence: tuple[int, ...]) -> None:
        if len(sequence) < 2:
            raise ValueError("training sequence must contain at least two units")
        state = self.zero_state()
        for index, unit in enumerate(sequence):
            state = self.advance_many(state, (unit,))
            self.observed_external_event_count += 1
            if index + 1 < len(sequence):
                self._update_readout(state, sequence[index + 1])

    def rollout_layers(
        self,
        cue_unit: int,
        *,
        steps: int,
    ) -> tuple[tuple[tuple[int, ...], ...], str]:
        if steps < 0:
            raise ValueError("steps must be non-negative")
        state = self.zero_state()
        active = (cue_unit,)
        layers: list[tuple[int, ...]] = []
        generated = 0
        for _ in range(steps):
            state = self.advance_many(state, active)
            ranked = tuple(
                sorted(
                    (
                        (score, target)
                        for target, score in self._scores(state).items()
                        if score > 0.0
                    ),
                    key=lambda row: (-row[0], row[1]),
                )
            )
            selected = tuple(
                target
                for _, target in ranked[: self.maximum_active_outputs]
            )
            if not selected:
                return tuple(layers), "no_positive_output"
            remaining = _MAXIMUM_PROBE_SPIKES - generated
            if remaining <= 0:
                return tuple(layers), "event_budget_exceeded"
            if len(selected) > remaining:
                selected = selected[:remaining]
            layers.append(selected)
            generated += len(selected)
            self.generated_event_count += len(selected)
            if generated >= _MAXIMUM_PROBE_SPIKES:
                return tuple(layers), "event_budget_exceeded"
            active = selected
        return tuple(layers), "step_horizon_reached"

    @property
    def fixed_recurrent_scalar_count(self) -> int:
        return len(self._recurrent_weights)

    @property
    def learned_readout_scalar_count(self) -> int:
        return len(self._readout_weights)

    @property
    def persistent_scalar_count(self) -> int:
        return self.fixed_recurrent_scalar_count + self.learned_readout_scalar_count

    def persistent_state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "directed_edges": [list(edge) for edge in self.directed_edges],
            "maximum_active_outputs": self.maximum_active_outputs,
            "readout_weights": [
                {
                    "source": source,
                    "target": target,
                    "weight": self._readout_weights[(source, target)],
                }
                for source, target in self.directed_edges
            ],
            "recurrent_weights": [
                {
                    "source": source,
                    "target": target,
                    "weight": self._recurrent_weights[(source, target)],
                }
                for source, target in self.directed_edges
            ],
            "seed": self.seed,
            "unit_count": self.unit_count,
        }

    def persistent_state_hash(self) -> str:
        return digest(self.persistent_state_dict())


def _train_reservoir(
    world: InterferenceWorldSpec,
    config: ResourceMatchedReservoirConfig,
) -> ResourceMatchedSparseReservoir:
    routes = _route_map(world)
    model = ResourceMatchedSparseReservoir(
        unit_count=world.unit_count,
        directed_edges=_directed_edges(world),
        maximum_active_outputs=world.maximum_active_outgoing_edges,
        seed=config.seed_offset + world.seed,
        config=config,
    )
    for route_id in world.training_order:
        route = routes[route_id]
        for _ in range(route.exposure_count):
            model.observe_sequence(route.units)
    return model


def _probe_reservoir(
    world: InterferenceWorldSpec,
    model: ResourceMatchedSparseReservoir,
    route_id: str,
) -> ReservoirProbeRecord:
    route = _route_map(world)[route_id]
    layers, halt_reason = model.rollout_layers(
        route.units[0],
        steps=len(route.units) - 1,
    )
    generated = tuple(unit for layer in layers for unit in layer)
    expected = route.units[1:]
    contamination = sum(unit not in route.units for unit in generated)
    structural_first_hops = tuple(
        sorted(
            {
                candidate.units[1]
                for candidate in world.routes
                if candidate.units[0] == route.units[0]
            }
        )
    )
    first_layer = layers[0] if layers else ()
    generated_first_hops = tuple(
        sorted(set(first_layer).intersection(structural_first_hops))
    )
    first_hop_coverage = (
        len(generated_first_hops) / len(structural_first_hops)
        if structural_first_hops
        else 1.0
    )
    retention = _ordered_coverage(expected, generated)
    row = ReservoirProbeRecord(
        world_id=world.world_id,
        probe_route_id=route.route_id,
        cue_unit_id=route.units[0],
        expected_units=expected,
        generated_layers=layers,
        generated_units=generated,
        ordered_retention_fraction=retention,
        exact_route_recovered=(retention == 1.0 and contamination == 0),
        contamination_count=contamination,
        first_hop_targets_generated=generated_first_hops,
        structural_first_hop_targets=structural_first_hops,
        first_hop_coverage_fraction=first_hop_coverage,
        generated_event_count=len(generated),
        halt_reason=halt_reason,
    )
    row.validate()
    return row


def _probe_signature(probes: tuple[ReservoirProbeRecord, ...]) -> str:
    return digest(
        [
            {
                "contamination_count": row.contamination_count,
                "exact_route_recovered": row.exact_route_recovered,
                "first_hop_coverage_fraction": row.first_hop_coverage_fraction,
                "generated_layers": [list(layer) for layer in row.generated_layers],
                "ordered_retention_fraction": row.ordered_retention_fraction,
                "probe_route_id": row.probe_route_id,
            }
            for row in sorted(probes, key=lambda item: item.probe_route_id)
        ]
    )


def run_resource_matched_reservoir_world(
    world: InterferenceWorldSpec,
    *,
    config: ResourceMatchedReservoirConfig | None = None,
) -> ResourceMatchedReservoirWorldResult:
    if world.phase is not InterferencePhase.DEVELOPMENT:
        raise RuntimeError(
            "held-out resource-matched reservoir execution is sealed before R01-12E"
        )
    world.validate()
    resolved_config = config or ResourceMatchedReservoirConfig()
    resolved_config.validate()

    field_result = run_interference_world(world)
    model = _train_reservoir(world, resolved_config)
    probes = tuple(
        _probe_reservoir(world, model, route_id)
        for route_id in world.probe_order
    )
    replay = _train_reservoir(world, resolved_config)
    replay_probes = tuple(
        _probe_reservoir(world, replay, route_id)
        for route_id in world.probe_order
    )

    edges = _directed_edges(world)
    field_persistent_scalar_count = len(field_result.final_connections) * 2
    reservoir_persistent_scalar_count = model.persistent_scalar_count
    resource_match = ReservoirResourceMatch(
        field_unit_count=world.unit_count,
        reservoir_state_scalar_count=model.unit_count,
        directed_edge_count=len(edges),
        field_persistent_scalar_count=field_persistent_scalar_count,
        reservoir_fixed_recurrent_scalar_count=model.fixed_recurrent_scalar_count,
        reservoir_learned_readout_scalar_count=model.learned_readout_scalar_count,
        reservoir_persistent_scalar_count=reservoir_persistent_scalar_count,
        field_external_event_count=(
            field_result.resource.external_transition_observation_count
        ),
        reservoir_external_event_count=model.observed_external_event_count,
        reservoir_supervised_transition_count=model.supervised_transition_count,
        field_generated_event_budget_per_probe=_MAXIMUM_PROBE_SPIKES,
        reservoir_generated_event_budget_per_probe=_MAXIMUM_PROBE_SPIKES,
        field_active_outgoing_budget=world.maximum_active_outgoing_edges,
        reservoir_active_output_budget=model.maximum_active_outputs,
        exact_persistent_state_match=(
            reservoir_persistent_scalar_count == field_persistent_scalar_count
        ),
        exact_external_event_match=(
            model.observed_external_event_count
            == field_result.resource.external_transition_observation_count
        ),
        matched_unit_state_count=(model.unit_count == world.unit_count),
        matched_generation_budget=True,
        matched_active_output_budget=(
            model.maximum_active_outputs == world.maximum_active_outgoing_edges
        ),
        resource_match_passed=False,
    )
    resource_match = ReservoirResourceMatch(
        **{
            **resource_match.state_dict(),
            "resource_match_passed": all(
                (
                    resource_match.exact_persistent_state_match,
                    resource_match.exact_external_event_match,
                    resource_match.matched_unit_state_count,
                    resource_match.matched_generation_budget,
                    resource_match.matched_active_output_budget,
                )
            ),
        }
    )
    resource_match.validate()

    field_final = tuple(
        row
        for row in field_result.probes
        if row.training_phase_index == world.route_count
    )
    field_mean_retention = sum(
        row.ordered_retention_fraction for row in field_final
    ) / len(field_final)
    reservoir_mean_retention = sum(
        row.ordered_retention_fraction for row in probes
    ) / len(probes)
    assessment = ReservoirComparisonAssessment(
        field_mean_ordered_retention=field_mean_retention,
        reservoir_mean_ordered_retention=reservoir_mean_retention,
        field_minus_reservoir_retention=(
            field_mean_retention - reservoir_mean_retention
        ),
        field_exact_route_count=sum(row.exact_route_recovered for row in field_final),
        reservoir_exact_route_count=sum(row.exact_route_recovered for row in probes),
        field_contamination_count=sum(row.contamination_count for row in field_final),
        reservoir_contamination_count=sum(row.contamination_count for row in probes),
        field_mean_first_hop_coverage=(
            sum(row.first_hop_coverage_fraction for row in field_final)
            / len(field_final)
        ),
        reservoir_mean_first_hop_coverage=(
            sum(row.first_hop_coverage_fraction for row in probes) / len(probes)
        ),
        reservoir_matches_or_exceeds_mean_retention=(
            reservoir_mean_retention >= field_mean_retention
        ),
        deterministic_replay_state_hash=(
            replay.persistent_state_hash() == model.persistent_state_hash()
        ),
        deterministic_replay_probe_hash=(
            _probe_signature(replay_probes) == _probe_signature(probes)
        ),
        no_training_replay=True,
        resource_match_passed=resource_match.resource_match_passed,
    )
    assessment.validate(route_count=world.route_count)

    semantic_payload = {
        "assessment": assessment.state_dict(),
        "comparator_config": asdict(resolved_config),
        "comparator_seed": model.seed,
        "probe_signature_hash": _probe_signature(probes),
        "probes": [row.state_dict() for row in probes],
        "recurrent_state_hash": model.persistent_state_hash(),
        "replay_probe_signature_hash": _probe_signature(replay_probes),
        "replay_recurrent_state_hash": replay.persistent_state_hash(),
        "resources": resource_match.state_dict(),
        "world_id": world.world_id,
        "world_specification_hash": world.specification_hash(),
    }
    result = ResourceMatchedReservoirWorldResult(
        world_id=world.world_id,
        world_specification_hash=world.specification_hash(),
        comparator_config=resolved_config,
        comparator_seed=model.seed,
        recurrent_state_hash=model.persistent_state_hash(),
        replay_recurrent_state_hash=replay.persistent_state_hash(),
        probe_signature_hash=_probe_signature(probes),
        replay_probe_signature_hash=_probe_signature(replay_probes),
        probes=probes,
        resources=resource_match,
        assessment=assessment,
        semantic_hash=digest(semantic_payload),
    )
    result.validate(world)
    return result


def run_development_resource_matched_reservoir_suite(
    *,
    config: ResourceMatchedReservoirConfig | None = None,
) -> DevelopmentResourceMatchedReservoirSuite:
    specs = development_worlds()
    worlds = tuple(
        run_resource_matched_reservoir_world(world, config=config)
        for world in specs
    )
    payload = {
        "world_grid_hash": world_grid_hash(specs),
        "worlds": [
            {"semantic_hash": row.semantic_hash, "world_id": row.world_id}
            for row in worlds
        ],
    }
    return DevelopmentResourceMatchedReservoirSuite(
        world_grid_hash=world_grid_hash(specs),
        worlds=worlds,
        suite_hash=digest(payload),
    )

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest

from .competitive_field_plasticity import (
    ExternalGatedCompetitiveFieldPlasticity,
)
from .direct_field_plasticity import ExternalGatedDirectFieldPlasticity
from .direct_field_plasticity_probe import new_uniform_field, train_external_sequence


@dataclass(frozen=True, slots=True)
class PhysicalExecutionBudget:
    horizon_ms: float
    time_slice_ms: float = 1.0
    maximum_total_spikes: int = 64
    maximum_queue_size: int = 64
    maximum_active_fanout: int = 8
    active_weight_threshold: float = 0.5

    def validate(self) -> None:
        for name in ("horizon_ms", "time_slice_ms", "active_weight_threshold"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if self.maximum_total_spikes < 1:
            raise ValueError("maximum_total_spikes must be positive")
        if self.maximum_queue_size < 1:
            raise ValueError("maximum_queue_size must be positive")
        if self.maximum_active_fanout < 1:
            raise ValueError("maximum_active_fanout must be positive")


@dataclass(frozen=True, slots=True)
class PhysicalResourceRecord:
    condition_id: str
    unit_count: int
    connection_count: int
    external_input_count: int
    total_spike_count: int
    generated_spike_count: int
    execution_slice_count: int
    maximum_queue_size_observed: int
    final_queue_size: int
    maximum_active_fanout_observed: int
    budget_exceeded: bool
    halt_reason: str
    final_simulation_time_ms: float
    connection_state_hash_before: str
    connection_state_hash_after: str
    later_units: tuple[int, ...]
    later_times_ms: tuple[float, ...]

    def validate(self) -> None:
        if not self.condition_id:
            raise ValueError("condition_id must be non-empty")
        integer_values = (
            self.unit_count,
            self.connection_count,
            self.external_input_count,
            self.total_spike_count,
            self.generated_spike_count,
            self.execution_slice_count,
            self.maximum_queue_size_observed,
            self.final_queue_size,
            self.maximum_active_fanout_observed,
        )
        if any(value < 0 for value in integer_values):
            raise ValueError("physical resource counts must be non-negative")
        if not math.isfinite(self.final_simulation_time_ms):
            raise ValueError("final simulation time must be finite")
        if len(self.connection_state_hash_before) != 64:
            raise ValueError("connection_state_hash_before must be a SHA-256 digest")
        if len(self.connection_state_hash_after) != 64:
            raise ValueError("connection_state_hash_after must be a SHA-256 digest")
        if len(self.later_units) != len(self.later_times_ms):
            raise ValueError("later unit and timing records must align")
        if self.generated_spike_count != len(self.later_units):
            raise ValueError("generated_spike_count must equal later event count")
        if self.total_spike_count < self.generated_spike_count:
            raise ValueError("total spikes cannot be below generated spikes")
        if self.budget_exceeded and self.halt_reason == "horizon_reached":
            raise ValueError("budget failure requires a budget-specific halt reason")
        if not self.budget_exceeded and self.halt_reason not in {
            "horizon_reached",
            "queue_drained",
        }:
            raise ValueError("successful execution has an invalid halt reason")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PlasticityBoundObservation:
    configured_minimum_weight: float
    configured_maximum_weight: float
    observed_minimum_weight: float
    observed_maximum_weight: float
    observed_minimum_delay_ms: float
    observed_maximum_delay_ms: float
    finite_weight_count: int
    finite_delay_count: int
    connection_count: int
    ignored_endogenous_observations: int
    connection_hash_before_endogenous_stress: str
    connection_hash_after_endogenous_stress: str

    @property
    def endogenous_stress_changed_connections(self) -> bool:
        return (
            self.connection_hash_before_endogenous_stress
            != self.connection_hash_after_endogenous_stress
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "endogenous_stress_changed_connections": (
                self.endogenous_stress_changed_connections
            ),
        }


@dataclass(frozen=True, slots=True)
class PhysicalSafetyAssessment:
    normal_chain_completes_within_budget: bool
    recurrent_cycle_persists_to_finite_horizon: bool
    recurrent_cycle_is_not_intrinsically_self_terminating: bool
    spike_budget_halts_cycle: bool
    broken_cycle_drains_without_budget_failure: bool
    excessive_active_fanout_fails_closed_before_execution: bool
    queue_budget_halts_safe_fanout_execution: bool
    local_path_failure_does_not_destroy_disjoint_path: bool
    plasticity_weight_bounds_respected: bool
    plasticity_delay_values_remain_positive_and_finite: bool
    upper_and_lower_weight_saturation_observed: bool
    endogenous_activity_cannot_write_connections: bool
    resource_records_complete_and_unique: bool
    safety_layer_has_no_learned_cognitive_state: bool
    intrinsic_runtime_safety_supported: bool
    external_execution_guard_required: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalSafetySuite:
    normal_chain: PhysicalResourceRecord
    finite_horizon_cycle: PhysicalResourceRecord
    budgeted_cycle: PhysicalResourceRecord
    broken_cycle: PhysicalResourceRecord
    fanout_preflight_rejection: PhysicalResourceRecord
    queue_budget_rejection: PhysicalResourceRecord
    failed_target_path: PhysicalResourceRecord
    unaffected_control_path: PhysicalResourceRecord
    plasticity_bounds: PlasticityBoundObservation
    assessment: PhysicalSafetyAssessment
    suite_hash: str

    @property
    def resource_records(self) -> tuple[PhysicalResourceRecord, ...]:
        return (
            self.normal_chain,
            self.finite_horizon_cycle,
            self.budgeted_cycle,
            self.broken_cycle,
            self.fanout_preflight_rejection,
            self.queue_budget_rejection,
            self.failed_target_path,
            self.unaffected_control_path,
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "broken_cycle": self.broken_cycle.state_dict(),
            "budgeted_cycle": self.budgeted_cycle.state_dict(),
            "failed_target_path": self.failed_target_path.state_dict(),
            "fanout_preflight_rejection": (
                self.fanout_preflight_rejection.state_dict()
            ),
            "finite_horizon_cycle": self.finite_horizon_cycle.state_dict(),
            "normal_chain": self.normal_chain.state_dict(),
            "plasticity_bounds": self.plasticity_bounds.state_dict(),
            "queue_budget_rejection": self.queue_budget_rejection.state_dict(),
            "suite_hash": self.suite_hash,
            "unaffected_control_path": self.unaffected_control_path.state_dict(),
        }


def _connection_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "delay_ms": edge.delay_ms,
                "plastic": edge.plastic,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "weight": edge.weight,
            }
            for _, edge in sorted(field.connections.items())
        ]
    )


def _active_fanout(
    field: TemporalExcitableField,
    minimum_weight: float,
) -> int:
    counts: dict[int, int] = {}
    for edge in field.connections.values():
        if edge.weight < minimum_weight:
            continue
        counts[edge.source_id] = counts.get(edge.source_id, 0) + 1
    return max(counts.values(), default=0)


def _queue_size(field: TemporalExcitableField) -> int:
    return len(field.state_dict()["queue"])


def run_bounded_physical_field(
    condition_id: str,
    field: TemporalExcitableField,
    *,
    cue_unit_id: int,
    cue_time_ms: float,
    budget: PhysicalExecutionBudget,
) -> PhysicalResourceRecord:
    """Execute a Field under an operational, non-learning resource guard.

    The guard never changes weights, delays, thresholds, or event identities. It
    may reject an over-fanout substrate before scheduling input or stop advancing
    simulation after a logical budget is exceeded.
    """

    budget.validate()
    if not math.isfinite(cue_time_ms) or cue_time_ms < 0.0:
        raise ValueError("cue_time_ms must be finite and non-negative")
    before_hash = _connection_hash(field)
    state = field.state_dict()
    unit_count = len(state["units"])
    connection_count = len(field.connections)
    max_fanout = _active_fanout(field, budget.active_weight_threshold)
    if max_fanout > budget.maximum_active_fanout:
        record = PhysicalResourceRecord(
            condition_id=condition_id,
            unit_count=unit_count,
            connection_count=connection_count,
            external_input_count=0,
            total_spike_count=0,
            generated_spike_count=0,
            execution_slice_count=0,
            maximum_queue_size_observed=_queue_size(field),
            final_queue_size=_queue_size(field),
            maximum_active_fanout_observed=max_fanout,
            budget_exceeded=True,
            halt_reason="active_fanout_budget_exceeded",
            final_simulation_time_ms=float(state["current_time_ms"]),
            connection_state_hash_before=before_hash,
            connection_state_hash_after=_connection_hash(field),
            later_units=(),
            later_times_ms=(),
        )
        record.validate()
        return record

    field.schedule_arrival(
        SynapticArrival(
            time_ms=cue_time_ms,
            target_id=cue_unit_id,
            current=1.0,
            source_id=None,
            pulse_id=f"external-cue:{condition_id}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    all_spikes = []
    slices = 0
    max_queue = _queue_size(field)
    halt_reason = "horizon_reached"
    budget_exceeded = False
    cursor = cue_time_ms
    while cursor <= budget.horizon_ms:
        next_time = min(cursor, budget.horizon_ms)
        rows = field.run_until(next_time)
        all_spikes.extend(rows)
        slices += 1
        queue_size = _queue_size(field)
        max_queue = max(max_queue, queue_size)
        if len(all_spikes) > budget.maximum_total_spikes:
            budget_exceeded = True
            halt_reason = "spike_budget_exceeded"
            break
        if queue_size > budget.maximum_queue_size:
            budget_exceeded = True
            halt_reason = "queue_budget_exceeded"
            break
        if queue_size == 0 and cursor >= cue_time_ms:
            halt_reason = "queue_drained"
            break
        if cursor >= budget.horizon_ms:
            halt_reason = "horizon_reached"
            break
        cursor = min(budget.horizon_ms, cursor + budget.time_slice_ms)

    later = tuple(row for row in all_spikes if row.time_ms > cue_time_ms)
    final_state = field.state_dict()
    record = PhysicalResourceRecord(
        condition_id=condition_id,
        unit_count=unit_count,
        connection_count=connection_count,
        external_input_count=1,
        total_spike_count=len(all_spikes),
        generated_spike_count=len(later),
        execution_slice_count=slices,
        maximum_queue_size_observed=max_queue,
        final_queue_size=_queue_size(field),
        maximum_active_fanout_observed=max_fanout,
        budget_exceeded=budget_exceeded,
        halt_reason=halt_reason,
        final_simulation_time_ms=float(final_state["current_time_ms"]),
        connection_state_hash_before=before_hash,
        connection_state_hash_after=_connection_hash(field),
        later_units=tuple(row.unit_id for row in later),
        later_times_ms=tuple(row.time_ms for row in later),
    )
    record.validate()
    return record


def _trained_field(
    unit_count: int,
    sequences: tuple[tuple[int, ...], ...],
) -> TemporalExcitableField:
    field = new_uniform_field(unit_count)
    for sequence in sequences:
        train_external_sequence(field, sequence)
    return field


def _fanout_field(targets: tuple[int, ...]) -> TemporalExcitableField:
    field = new_uniform_field(max(targets) + 1)
    for target in targets:
        train_external_sequence(field, (0, target))
    return field


def _runtime_pulse(
    event_id: str,
    time_ms: float,
    unit_id: int,
    *,
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


def _find_config_bound(
    config_state: dict[str, Any],
    quantity: str,
    *,
    lower: bool,
) -> float:
    markers = ("minimum", "min") if lower else ("maximum", "max")
    rows = [
        float(value)
        for key, value in config_state.items()
        if quantity in key.lower()
        and any(marker in key.lower() for marker in markers)
        and isinstance(value, (int, float))
    ]
    if not rows:
        raise RuntimeError(f"no configured {quantity} bound was found")
    return min(rows) if lower else max(rows)


def _plasticity_stress() -> PlasticityBoundObservation:
    field = new_uniform_field(6)
    controller = ExternalGatedCompetitiveFieldPlasticity(field)
    sequence = (0, 1, 2, 3)
    for episode in range(96):
        start = episode * 50.0
        for index, unit_id in enumerate(sequence):
            controller.observe_external(
                _runtime_pulse(
                    f"saturation:{episode}:{index}",
                    start + index * 5.0,
                    unit_id,
                    origin=EventOrigin.EXTERNAL,
                )
            )
        controller.clear_traces()

    config_state = controller.state_dict()["config"]
    minimum_weight = _find_config_bound(config_state, "weight", lower=True)
    maximum_weight = _find_config_bound(config_state, "weight", lower=False)
    weights = tuple(edge.weight for edge in field.connections.values())
    delays = tuple(edge.delay_ms for edge in field.connections.values())
    before = _connection_hash(field)
    for index in range(128):
        controller.observe_external(
            _runtime_pulse(
                f"endogenous-stress:{index}",
                10000.0 + index,
                index % 4,
                origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
            )
        )
    after = _connection_hash(field)
    state = controller.state_dict()
    ignored = int(state.get("ignored_endogenous_observations", 0))
    return PlasticityBoundObservation(
        configured_minimum_weight=minimum_weight,
        configured_maximum_weight=maximum_weight,
        observed_minimum_weight=min(weights),
        observed_maximum_weight=max(weights),
        observed_minimum_delay_ms=min(delays),
        observed_maximum_delay_ms=max(delays),
        finite_weight_count=sum(math.isfinite(value) for value in weights),
        finite_delay_count=sum(math.isfinite(value) for value in delays),
        connection_count=len(field.connections),
        ignored_endogenous_observations=ignored,
        connection_hash_before_endogenous_stress=before,
        connection_hash_after_endogenous_stress=after,
    )


def run_physical_safety_suite() -> PhysicalSafetySuite:
    normal = run_bounded_physical_field(
        "normal-chain",
        _trained_field(4, ((0, 1, 2, 3),)),
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=140.0,
            maximum_total_spikes=12,
            maximum_queue_size=12,
            maximum_active_fanout=2,
        ),
    )

    cycle_source = _trained_field(3, ((0, 1, 2, 0),))
    finite_cycle = run_bounded_physical_field(
        "finite-horizon-cycle",
        TemporalExcitableField.from_state_dict(cycle_source.state_dict()),
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=220.0,
            maximum_total_spikes=128,
            maximum_queue_size=32,
            maximum_active_fanout=2,
        ),
    )
    budgeted_cycle = run_bounded_physical_field(
        "budgeted-cycle",
        TemporalExcitableField.from_state_dict(cycle_source.state_dict()),
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=220.0,
            maximum_total_spikes=10,
            maximum_queue_size=32,
            maximum_active_fanout=2,
        ),
    )
    broken_cycle_field = TemporalExcitableField.from_state_dict(
        cycle_source.state_dict()
    )
    broken_cycle_field.connection(2, 0).weight = 0.0
    broken_cycle = run_bounded_physical_field(
        "broken-cycle",
        broken_cycle_field,
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=220.0,
            maximum_total_spikes=10,
            maximum_queue_size=32,
            maximum_active_fanout=2,
        ),
    )

    fanout_source = _fanout_field((1, 2, 3, 4, 5, 6))
    fanout_rejection = run_bounded_physical_field(
        "fanout-preflight-rejection",
        TemporalExcitableField.from_state_dict(fanout_source.state_dict()),
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=130.0,
            maximum_total_spikes=32,
            maximum_queue_size=32,
            maximum_active_fanout=3,
        ),
    )
    queue_rejection = run_bounded_physical_field(
        "queue-budget-rejection",
        TemporalExcitableField.from_state_dict(fanout_source.state_dict()),
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=130.0,
            maximum_total_spikes=32,
            maximum_queue_size=3,
            maximum_active_fanout=8,
        ),
    )

    dual = _trained_field(
        8,
        (
            (0, 1, 2, 3),
            (4, 5, 6, 7),
        ),
    )
    dual.connection(1, 2).weight = 0.0
    failed_target = run_bounded_physical_field(
        "failed-target-path",
        TemporalExcitableField.from_state_dict(dual.state_dict()),
        cue_unit_id=0,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=140.0,
            maximum_total_spikes=12,
            maximum_queue_size=12,
            maximum_active_fanout=2,
        ),
    )
    unaffected_control = run_bounded_physical_field(
        "unaffected-control-path",
        TemporalExcitableField.from_state_dict(dual.state_dict()),
        cue_unit_id=4,
        cue_time_ms=100.0,
        budget=PhysicalExecutionBudget(
            horizon_ms=140.0,
            maximum_total_spikes=12,
            maximum_queue_size=12,
            maximum_active_fanout=2,
        ),
    )
    bounds = _plasticity_stress()

    records = (
        normal,
        finite_cycle,
        budgeted_cycle,
        broken_cycle,
        fanout_rejection,
        queue_rejection,
        failed_target,
        unaffected_control,
    )
    resource_complete = (
        len({row.condition_id for row in records}) == len(records)
        and all(_validated(row) for row in records)
    )
    intrinsic_cycle_continues = (
        finite_cycle.halt_reason == "horizon_reached"
        and finite_cycle.final_queue_size > 0
        and finite_cycle.generated_spike_count > 10
    )
    positive_values = {
        "normal_chain_completes_within_budget": (
            normal.later_units == (1, 2, 3)
            and not normal.budget_exceeded
            and normal.halt_reason == "queue_drained"
        ),
        "recurrent_cycle_persists_to_finite_horizon": intrinsic_cycle_continues,
        "recurrent_cycle_is_not_intrinsically_self_terminating": (
            intrinsic_cycle_continues
        ),
        "spike_budget_halts_cycle": (
            budgeted_cycle.budget_exceeded
            and budgeted_cycle.halt_reason == "spike_budget_exceeded"
        ),
        "broken_cycle_drains_without_budget_failure": (
            not broken_cycle.budget_exceeded
            and broken_cycle.halt_reason == "queue_drained"
            and broken_cycle.later_units == (1, 2)
        ),
        "excessive_active_fanout_fails_closed_before_execution": (
            fanout_rejection.budget_exceeded
            and fanout_rejection.halt_reason
            == "active_fanout_budget_exceeded"
            and fanout_rejection.external_input_count == 0
            and fanout_rejection.total_spike_count == 0
        ),
        "queue_budget_halts_safe_fanout_execution": (
            queue_rejection.budget_exceeded
            and queue_rejection.halt_reason == "queue_budget_exceeded"
            and queue_rejection.maximum_queue_size_observed > 3
        ),
        "local_path_failure_does_not_destroy_disjoint_path": (
            failed_target.later_units == (1,)
            and unaffected_control.later_units == (5, 6, 7)
        ),
        "plasticity_weight_bounds_respected": (
            bounds.finite_weight_count == bounds.connection_count
            and bounds.configured_minimum_weight
            <= bounds.observed_minimum_weight
            <= bounds.observed_maximum_weight
            <= bounds.configured_maximum_weight
        ),
        "plasticity_delay_values_remain_positive_and_finite": (
            bounds.finite_delay_count == bounds.connection_count
            and bounds.observed_minimum_delay_ms > 0.0
        ),
        "upper_and_lower_weight_saturation_observed": (
            math.isclose(
                bounds.observed_minimum_weight,
                bounds.configured_minimum_weight,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
            and math.isclose(
                bounds.observed_maximum_weight,
                bounds.configured_maximum_weight,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        ),
        "endogenous_activity_cannot_write_connections": (
            bounds.ignored_endogenous_observations == 128
            and not bounds.endogenous_stress_changed_connections
        ),
        "resource_records_complete_and_unique": resource_complete,
        "safety_layer_has_no_learned_cognitive_state": True,
        "external_execution_guard_required": intrinsic_cycle_continues,
    }
    assessment = PhysicalSafetyAssessment(
        **positive_values,
        intrinsic_runtime_safety_supported=False,
        engineering_candidate=all(positive_values.values()),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "plasticity_bounds": bounds.state_dict(),
        "resource_records": [row.state_dict() for row in records],
    }
    return PhysicalSafetySuite(
        normal_chain=normal,
        finite_horizon_cycle=finite_cycle,
        budgeted_cycle=budgeted_cycle,
        broken_cycle=broken_cycle,
        fanout_preflight_rejection=fanout_rejection,
        queue_budget_rejection=queue_rejection,
        failed_target_path=failed_target,
        unaffected_control_path=unaffected_control,
        plasticity_bounds=bounds,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )


def _validated(record: PhysicalResourceRecord) -> bool:
    try:
        record.validate()
    except ValueError:
        return False
    return True

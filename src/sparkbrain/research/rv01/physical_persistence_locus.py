from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import digest

from .direct_field_plasticity import (
    ExternalGatedDirectFieldPlasticity,
    UnitExternalTrace,
)
from .direct_field_plasticity_probe import (
    BASE_DELAY_MS,
    BASE_WEIGHT,
    new_uniform_field,
    train_external_sequence,
)

SEQUENCE = (0, 1, 2, 3)
CUE_TIME_MS = 100.0
HORIZON_MS = 132.0


@dataclass(frozen=True, slots=True)
class PersistenceLocusObservation:
    condition_id: str
    initial_dynamic_state_hash: str
    connection_state_hash: str
    weight_state_hash: str
    delay_state_hash: str
    structure_state_hash: str
    receptor_state_hash: str
    plasticity_flag_hash: str
    controller_trace_count: int
    path_weights: tuple[float, ...]
    path_delays_ms: tuple[float, ...]
    later_units: tuple[int, ...]
    later_times_ms: tuple[float, ...]

    @property
    def full_chain_generated(self) -> bool:
        return self.later_units == SEQUENCE[1:]

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "full_chain_generated": self.full_chain_generated,
        }


@dataclass(frozen=True, slots=True)
class PhysicalPersistenceLocusAssessment:
    trained_connection_state_generates_chain: bool
    weight_reset_removes_chain: bool
    learned_weights_alone_transfer_order: bool
    learned_delays_alone_do_not_transfer_chain: bool
    delay_reset_preserves_order: bool
    learned_delays_change_timing: bool
    full_connection_transplant_matches_trace: bool
    dynamic_state_only_does_not_transfer_chain: bool
    working_trace_only_does_not_transfer_chain: bool
    receptor_state_only_does_not_transfer_chain: bool
    fixed_structure_only_does_not_transfer_chain: bool
    training_does_not_write_unit_dynamic_state: bool
    training_does_not_change_receptors_or_edge_structure: bool
    ongoing_plasticity_not_required_for_execution: bool
    weight_state_is_necessary_canonical_carrier: bool
    weight_state_is_sufficient_canonical_carrier: bool
    delay_state_is_temporal_calibration_carrier: bool
    broad_distributed_dynamic_carrier_supported: bool
    edge_localized_physical_carrier_supported: bool
    pairwise_physical_storage_limitation: bool
    no_g1_or_g2_runtime_required: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalPersistenceLocusSuite:
    trained: PersistenceLocusObservation
    untrained: PersistenceLocusObservation
    weight_reset: PersistenceLocusObservation
    delay_reset: PersistenceLocusObservation
    weights_only_transplant: PersistenceLocusObservation
    delays_only_transplant: PersistenceLocusObservation
    full_connection_transplant: PersistenceLocusObservation
    dynamic_state_only: PersistenceLocusObservation
    working_trace_only: PersistenceLocusObservation
    receptor_state_only: PersistenceLocusObservation
    structure_only: PersistenceLocusObservation
    plasticity_disabled_after_learning: PersistenceLocusObservation
    training_dynamic_hash_before: str
    training_dynamic_hash_after: str
    training_structure_hash_before: str
    training_structure_hash_after: str
    training_receptor_hash_before: str
    training_receptor_hash_after: str
    assessment: PhysicalPersistenceLocusAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "delay_reset": self.delay_reset.state_dict(),
            "delays_only_transplant": self.delays_only_transplant.state_dict(),
            "dynamic_state_only": self.dynamic_state_only.state_dict(),
            "full_connection_transplant": (
                self.full_connection_transplant.state_dict()
            ),
            "plasticity_disabled_after_learning": (
                self.plasticity_disabled_after_learning.state_dict()
            ),
            "receptor_state_only": self.receptor_state_only.state_dict(),
            "structure_only": self.structure_only.state_dict(),
            "suite_hash": self.suite_hash,
            "trained": self.trained.state_dict(),
            "training_dynamic_hash_after": self.training_dynamic_hash_after,
            "training_dynamic_hash_before": self.training_dynamic_hash_before,
            "training_receptor_hash_after": self.training_receptor_hash_after,
            "training_receptor_hash_before": self.training_receptor_hash_before,
            "training_structure_hash_after": self.training_structure_hash_after,
            "training_structure_hash_before": self.training_structure_hash_before,
            "untrained": self.untrained.state_dict(),
            "weight_reset": self.weight_reset.state_dict(),
            "weights_only_transplant": self.weights_only_transplant.state_dict(),
            "working_trace_only": self.working_trace_only.state_dict(),
        }


def _dynamic_state_hash(field: TemporalExcitableField) -> str:
    state = field.state_dict()
    return digest(
        {
            "config": state["config"],
            "counter": state["counter"],
            "current_time_ms": state["current_time_ms"],
            "queue": state["queue"],
            "totals": state["totals"],
            "units": state["units"],
        }
    )


def _connection_state_hash(field: TemporalExcitableField) -> str:
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


def _weight_state_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "weight": edge.weight,
            }
            for _, edge in sorted(field.connections.items())
        ]
    )


def _delay_state_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "delay_ms": edge.delay_ms,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
            }
            for _, edge in sorted(field.connections.items())
        ]
    )


def _structure_state_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "source_id": source_id,
                "target_id": target_id,
            }
            for source_id, target_id in sorted(field.connections)
        ]
    )


def _receptor_state_hash(field: TemporalExcitableField) -> str:
    return digest(tuple(field.receptor_ids))


def _plasticity_flag_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "plastic": edge.plastic,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
            }
            for _, edge in sorted(field.connections.items())
        ]
    )


def _clone(field: TemporalExcitableField) -> TemporalExcitableField:
    return TemporalExcitableField.from_state_dict(field.state_dict())


def _copy_weights(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> None:
    _require_compatible_connections(source, target)
    for key in sorted(source.connections):
        target.connections[key].weight = source.connections[key].weight


def _copy_delays(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> None:
    _require_compatible_connections(source, target)
    for key in sorted(source.connections):
        target.connections[key].delay_ms = source.connections[key].delay_ms


def _copy_all_connection_state(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> None:
    _copy_weights(source, target)
    _copy_delays(source, target)
    for key in sorted(source.connections):
        target.connections[key].plastic = source.connections[key].plastic


def _require_compatible_connections(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> None:
    if set(source.connections) != set(target.connections):
        raise ValueError("persistence-locus transplant requires compatible topology")


def _copy_dynamic_state(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> TemporalExcitableField:
    source_state = source.state_dict()
    target_state = target.state_dict()
    target_state["counter"] = source_state["counter"]
    target_state["current_time_ms"] = source_state["current_time_ms"]
    target_state["queue"] = source_state["queue"]
    target_state["totals"] = source_state["totals"]
    target_state["units"] = source_state["units"]
    return TemporalExcitableField.from_state_dict(target_state)


def _copy_working_traces(
    source: ExternalGatedDirectFieldPlasticity,
    target: ExternalGatedDirectFieldPlasticity,
) -> int:
    rows = source.state_dict()["unit_traces"]
    target._unit_traces = {  # noqa: SLF001
        int(unit_id): UnitExternalTrace(**state)
        for unit_id, state in rows.items()
    }
    return len(rows)


def _run(
    condition_id: str,
    field: TemporalExcitableField,
    *,
    controller_trace_count: int = 0,
) -> PersistenceLocusObservation:
    initial_dynamic_hash = _dynamic_state_hash(field)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=CUE_TIME_MS,
            target_id=SEQUENCE[0],
            current=1.0,
            source_id=None,
            pulse_id=f"cue:{condition_id}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    spikes = field.run_until(HORIZON_MS)
    later = tuple(row for row in spikes if row.time_ms > CUE_TIME_MS)
    path_edges = tuple(zip(SEQUENCE, SEQUENCE[1:], strict=False))
    return PersistenceLocusObservation(
        condition_id=condition_id,
        initial_dynamic_state_hash=initial_dynamic_hash,
        connection_state_hash=_connection_state_hash(field),
        weight_state_hash=_weight_state_hash(field),
        delay_state_hash=_delay_state_hash(field),
        structure_state_hash=_structure_state_hash(field),
        receptor_state_hash=_receptor_state_hash(field),
        plasticity_flag_hash=_plasticity_flag_hash(field),
        controller_trace_count=controller_trace_count,
        path_weights=tuple(
            field.connection(source_id, target_id).weight
            for source_id, target_id in path_edges
        ),
        path_delays_ms=tuple(
            field.connection(source_id, target_id).delay_ms
            for source_id, target_id in path_edges
        ),
        later_units=tuple(row.unit_id for row in later),
        later_times_ms=tuple(row.time_ms for row in later),
    )


def run_physical_persistence_locus_suite() -> PhysicalPersistenceLocusSuite:
    naive_before = new_uniform_field(4)
    training_dynamic_before = _dynamic_state_hash(naive_before)
    training_structure_before = _structure_state_hash(naive_before)
    training_receptor_before = _receptor_state_hash(naive_before)

    donor = new_uniform_field(4)
    donor_controller = train_external_sequence(donor, SEQUENCE)
    training_dynamic_after = _dynamic_state_hash(donor)
    training_structure_after = _structure_state_hash(donor)
    training_receptor_after = _receptor_state_hash(donor)

    trained = _run("trained", _clone(donor))
    untrained = _run("untrained", new_uniform_field(4))

    weight_reset_field = _clone(donor)
    for edge in weight_reset_field.connections.values():
        edge.weight = BASE_WEIGHT
    weight_reset = _run("weight-reset", weight_reset_field)

    delay_reset_field = _clone(donor)
    for edge in delay_reset_field.connections.values():
        edge.delay_ms = BASE_DELAY_MS
    delay_reset = _run("delay-reset", delay_reset_field)

    weights_only_field = new_uniform_field(4)
    _copy_weights(donor, weights_only_field)
    weights_only = _run("weights-only-transplant", weights_only_field)

    delays_only_field = new_uniform_field(4)
    _copy_delays(donor, delays_only_field)
    delays_only = _run("delays-only-transplant", delays_only_field)

    full_field = new_uniform_field(4)
    _copy_all_connection_state(donor, full_field)
    full_transplant = _run("full-connection-transplant", full_field)

    dynamic_only_field = _copy_dynamic_state(donor, new_uniform_field(4))
    dynamic_only = _run("dynamic-state-only", dynamic_only_field)

    trace_only_field = new_uniform_field(4)
    trace_receiver = ExternalGatedDirectFieldPlasticity(trace_only_field)
    trace_count = _copy_working_traces(donor_controller, trace_receiver)
    trace_only = _run(
        "working-trace-only",
        trace_only_field,
        controller_trace_count=trace_count,
    )

    receptor_only_field = new_uniform_field(4)
    receptor_only_field.receptor_ids = tuple(donor.receptor_ids)
    receptor_only = _run("receptor-state-only", receptor_only_field)

    structure_only = _run("structure-only", new_uniform_field(4))

    plasticity_disabled_field = _clone(donor)
    for edge in plasticity_disabled_field.connections.values():
        edge.plastic = False
    plasticity_disabled = _run(
        "plasticity-disabled-after-learning",
        plasticity_disabled_field,
    )

    positive_values = {
        "trained_connection_state_generates_chain": trained.full_chain_generated,
        "weight_reset_removes_chain": not weight_reset.full_chain_generated,
        "learned_weights_alone_transfer_order": weights_only.full_chain_generated,
        "learned_delays_alone_do_not_transfer_chain": (
            not delays_only.full_chain_generated
        ),
        "delay_reset_preserves_order": delay_reset.full_chain_generated,
        "learned_delays_change_timing": (
            trained.later_times_ms != delay_reset.later_times_ms
            and weights_only.later_times_ms == delay_reset.later_times_ms
        ),
        "full_connection_transplant_matches_trace": (
            full_transplant.later_units == trained.later_units
            and full_transplant.later_times_ms == trained.later_times_ms
            and full_transplant.weight_state_hash == trained.weight_state_hash
            and full_transplant.delay_state_hash == trained.delay_state_hash
        ),
        "dynamic_state_only_does_not_transfer_chain": (
            not dynamic_only.full_chain_generated
        ),
        "working_trace_only_does_not_transfer_chain": (
            trace_only.controller_trace_count > 0
            and not trace_only.full_chain_generated
        ),
        "receptor_state_only_does_not_transfer_chain": (
            not receptor_only.full_chain_generated
        ),
        "fixed_structure_only_does_not_transfer_chain": (
            not structure_only.full_chain_generated
        ),
        "training_does_not_write_unit_dynamic_state": (
            training_dynamic_before == training_dynamic_after
        ),
        "training_does_not_change_receptors_or_edge_structure": (
            training_structure_before == training_structure_after
            and training_receptor_before == training_receptor_after
        ),
        "ongoing_plasticity_not_required_for_execution": (
            plasticity_disabled.later_units == trained.later_units
            and plasticity_disabled.later_times_ms == trained.later_times_ms
        ),
        "weight_state_is_necessary_canonical_carrier": (
            trained.full_chain_generated and not weight_reset.full_chain_generated
        ),
        "weight_state_is_sufficient_canonical_carrier": (
            weights_only.full_chain_generated
        ),
        "delay_state_is_temporal_calibration_carrier": (
            delay_reset.full_chain_generated
            and delay_reset.later_times_ms != trained.later_times_ms
            and not delays_only.full_chain_generated
        ),
        "edge_localized_physical_carrier_supported": (
            weights_only.full_chain_generated
            and full_transplant.full_chain_generated
            and not dynamic_only.full_chain_generated
        ),
        "pairwise_physical_storage_limitation": True,
        "no_g1_or_g2_runtime_required": True,
    }
    assessment = PhysicalPersistenceLocusAssessment(
        **positive_values,
        broad_distributed_dynamic_carrier_supported=False,
        engineering_candidate=all(positive_values.values()),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "delay_reset": delay_reset.state_dict(),
        "delays_only_transplant": delays_only.state_dict(),
        "dynamic_state_only": dynamic_only.state_dict(),
        "full_connection_transplant": full_transplant.state_dict(),
        "plasticity_disabled_after_learning": plasticity_disabled.state_dict(),
        "receptor_state_only": receptor_only.state_dict(),
        "structure_only": structure_only.state_dict(),
        "trained": trained.state_dict(),
        "training_dynamic_hash_after": training_dynamic_after,
        "training_dynamic_hash_before": training_dynamic_before,
        "training_receptor_hash_after": training_receptor_after,
        "training_receptor_hash_before": training_receptor_before,
        "training_structure_hash_after": training_structure_after,
        "training_structure_hash_before": training_structure_before,
        "untrained": untrained.state_dict(),
        "weight_reset": weight_reset.state_dict(),
        "weights_only_transplant": weights_only.state_dict(),
        "working_trace_only": trace_only.state_dict(),
    }
    return PhysicalPersistenceLocusSuite(
        trained=trained,
        untrained=untrained,
        weight_reset=weight_reset,
        delay_reset=delay_reset,
        weights_only_transplant=weights_only,
        delays_only_transplant=delays_only,
        full_connection_transplant=full_transplant,
        dynamic_state_only=dynamic_only,
        working_trace_only=trace_only,
        receptor_state_only=receptor_only,
        structure_only=structure_only,
        plasticity_disabled_after_learning=plasticity_disabled,
        training_dynamic_hash_before=training_dynamic_before,
        training_dynamic_hash_after=training_dynamic_after,
        training_structure_hash_before=training_structure_before,
        training_structure_hash_after=training_structure_after,
        training_receptor_hash_before=training_receptor_before,
        training_receptor_hash_after=training_receptor_after,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

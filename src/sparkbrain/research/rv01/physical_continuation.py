from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest

from .direct_field_plasticity import ExternalGatedDirectFieldPlasticity
from .direct_field_plasticity_probe import (
    BASE_DELAY_MS,
    BASE_WEIGHT,
    new_uniform_field,
    train_external_sequence,
)


@dataclass(frozen=True, slots=True)
class PhysicalContinuationObservation:
    condition_id: str
    training_sequence: tuple[int, ...]
    cue_unit_id: int
    initial_dynamic_state_hash: str
    connection_state_hash: str
    later_units: tuple[int, ...]
    later_times_ms: tuple[float, ...]
    total_spike_units: tuple[int, ...]
    total_spike_times_ms: tuple[float, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalContinuationAssessment:
    trained_field_continues: bool
    untrained_field_does_not_continue: bool
    different_physical_history_changes_continuation: bool
    connection_reset_removes_continuation: bool
    connection_transplant_transfers_continuation: bool
    unit_trace_reset_preserves_continuation: bool
    endogenous_only_training_cannot_create_continuation: bool
    initial_dynamic_states_match: bool
    no_g1_or_g2_runtime_required: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalContinuationSuite:
    trained: PhysicalContinuationObservation
    untrained: PhysicalContinuationObservation
    alternate_history: PhysicalContinuationObservation
    connection_reset: PhysicalContinuationObservation
    connection_transplant: PhysicalContinuationObservation
    endogenous_only_training: PhysicalContinuationObservation
    assessment: PhysicalContinuationAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "alternate_history": self.alternate_history.state_dict(),
            "assessment": self.assessment.state_dict(),
            "connection_reset": self.connection_reset.state_dict(),
            "connection_transplant": self.connection_transplant.state_dict(),
            "endogenous_only_training": self.endogenous_only_training.state_dict(),
            "suite_hash": self.suite_hash,
            "trained": self.trained.state_dict(),
            "untrained": self.untrained.state_dict(),
        }


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


def _dynamic_state_hash(field: TemporalExcitableField) -> str:
    state = field.state_dict()
    return digest(
        {
            "config": state["config"],
            "counter": state["counter"],
            "current_time_ms": state["current_time_ms"],
            "queue": state["queue"],
            "receptor_ids": state["receptor_ids"],
            "totals": state["totals"],
            "units": state["units"],
        }
    )


def _run_cue(
    condition_id: str,
    training_sequence: tuple[int, ...],
    field: TemporalExcitableField,
    *,
    cue_unit_id: int = 0,
) -> PhysicalContinuationObservation:
    initial_dynamic_hash = _dynamic_state_hash(field)
    connection_hash = _connection_state_hash(field)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=100.0,
            target_id=cue_unit_id,
            current=1.0,
            source_id=None,
            pulse_id=f"cue:{condition_id}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    spikes = field.run_until(122.0)
    later = tuple(row for row in spikes if row.time_ms > 100.0)
    return PhysicalContinuationObservation(
        condition_id=condition_id,
        training_sequence=training_sequence,
        cue_unit_id=cue_unit_id,
        initial_dynamic_state_hash=initial_dynamic_hash,
        connection_state_hash=connection_hash,
        later_units=tuple(row.unit_id for row in later),
        later_times_ms=tuple(row.time_ms for row in later),
        total_spike_units=tuple(row.unit_id for row in spikes),
        total_spike_times_ms=tuple(row.time_ms for row in spikes),
    )


def _trained_field(
    sequence: tuple[int, ...],
    *,
    external: bool = True,
) -> tuple[TemporalExcitableField, ExternalGatedDirectFieldPlasticity]:
    field = new_uniform_field(max(sequence) + 1)
    if external:
        controller = train_external_sequence(field, sequence)
    else:
        controller = ExternalGatedDirectFieldPlasticity(field)
        episode_spacing_ms = max(30.0, len(sequence) * 5.0 + 10.0)
        for episode in range(3):
            start = episode * episode_spacing_ms
            for index, unit_id in enumerate(sequence):
                controller.observe(
                    RuntimePulse(
                        event_id=f"internal:{episode}:{index}",
                        time_ms=start + index * 5.0,
                        target=f"unit:{unit_id}",
                        magnitude=1.0,
                        polarity=1,
                        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
                    )
                )
    controller.clear_traces()
    return field, controller


def _reset_connections(field: TemporalExcitableField) -> None:
    for edge in field.connections.values():
        edge.weight = BASE_WEIGHT
        edge.delay_ms = BASE_DELAY_MS


def _transplant_connections(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> None:
    if set(source.connections) != set(target.connections):
        raise ValueError("physical connection transplant requires compatible topology")
    for key in sorted(source.connections):
        donor = source.connections[key]
        receiver = target.connections[key]
        receiver.weight = donor.weight
        receiver.delay_ms = donor.delay_ms
        receiver.plastic = donor.plastic


def run_physical_continuation_suite() -> PhysicalContinuationSuite:
    main_sequence = (0, 1, 2, 3)
    alternate_sequence = (0, 2, 1, 3)

    trained_field, trained_controller = _trained_field(main_sequence)
    trained = _run_cue("trained", main_sequence, trained_field)

    untrained_field = new_uniform_field(4)
    untrained = _run_cue("untrained", (), untrained_field)

    alternate_field, _ = _trained_field(alternate_sequence)
    alternate = _run_cue(
        "alternate-history",
        alternate_sequence,
        alternate_field,
    )

    reset_field, _ = _trained_field(main_sequence)
    _reset_connections(reset_field)
    reset = _run_cue("connection-reset", main_sequence, reset_field)

    transplant_source, _ = _trained_field(main_sequence)
    transplant_receiver = new_uniform_field(4)
    _transplant_connections(transplant_source, transplant_receiver)
    transplant = _run_cue(
        "connection-transplant",
        main_sequence,
        transplant_receiver,
    )

    endogenous_field, endogenous_controller = _trained_field(
        main_sequence,
        external=False,
    )
    endogenous = _run_cue(
        "endogenous-only-training",
        main_sequence,
        endogenous_field,
    )

    initial_hashes = {
        row.initial_dynamic_state_hash
        for row in (
            trained,
            untrained,
            alternate,
            reset,
            transplant,
            endogenous,
        )
    }
    values = {
        "trained_field_continues": trained.later_units == (1, 2, 3),
        "untrained_field_does_not_continue": untrained.later_units == (),
        "different_physical_history_changes_continuation": (
            alternate.later_units == (2, 1, 3)
            and alternate.later_units != trained.later_units
        ),
        "connection_reset_removes_continuation": reset.later_units == (),
        "connection_transplant_transfers_continuation": (
            transplant.later_units == trained.later_units
            and transplant.later_times_ms == trained.later_times_ms
            and transplant.connection_state_hash == trained.connection_state_hash
        ),
        "unit_trace_reset_preserves_continuation": (
            trained_controller.state_dict()["unit_traces"] == {}
            and trained.later_units == (1, 2, 3)
        ),
        "endogenous_only_training_cannot_create_continuation": (
            endogenous_controller.external_observation_count == 0
            and endogenous_controller.ignored_endogenous_count == 12
            and endogenous.later_units == ()
        ),
        "initial_dynamic_states_match": len(initial_hashes) == 1,
        "no_g1_or_g2_runtime_required": True,
    }
    assessment = PhysicalContinuationAssessment(
        **values,
        engineering_candidate=all(values.values()),
    )
    state_without_hash = {
        "alternate_history": alternate.state_dict(),
        "assessment": assessment.state_dict(),
        "connection_reset": reset.state_dict(),
        "connection_transplant": transplant.state_dict(),
        "endogenous_only_training": endogenous.state_dict(),
        "trained": trained.state_dict(),
        "untrained": untrained.state_dict(),
    }
    return PhysicalContinuationSuite(
        trained=trained,
        untrained=untrained,
        alternate_history=alternate,
        connection_reset=reset,
        connection_transplant=transplant,
        endogenous_only_training=endogenous,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

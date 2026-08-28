from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .brain import IntegratedV04Brain, V04BrainConfig
from .dynamics import BurstDetectorConfig, CascadeTrackerConfig, IgnitionGateConfig
from .field import ExcitableFieldConfig
from .topology import Connection, UnitState, explicit_topology
from .worlds import (
    moving_point_frames,
    noisy_motif_stream,
    order_cases,
    repetition_train,
    weak_coincidence_cases,
)


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    name: str
    metrics: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {"metrics": self.metrics, "name": self.name}


def _new_brain(factory: Callable[[], IntegratedV04Brain] | None = None) -> IntegratedV04Brain:
    return factory() if factory is not None else IntegratedV04Brain()


def evaluate_temporal_order(
    factory: Callable[[], IntegratedV04Brain] | None = None,
) -> ExperimentResult:
    signatures: dict[str, list[str]] = {}
    spike_sequences: dict[str, list[int]] = {}
    for case in order_cases():
        brain = (
            _new_brain(factory)
            if factory is not None
            else IntegratedV04Brain(
                V04BrainConfig(enable_expectations=False, enable_plasticity=False)
            )
        )
        result = brain.ingest_pulses(case.pulses)
        flush = brain.advance(brain.current_time_ms + 300.0)
        cascades = result.cascades + flush.cascades
        signatures[case.name] = [row.signature for row in cascades]
        spike_sequences[case.name] = [row.unit_id for row in result.spikes + flush.spikes]
    unique = len({tuple(value) for value in signatures.values()})
    return ExperimentResult(
        "temporal_order",
        {
            "distinct_cascade_signatures": unique,
            "signatures": signatures,
            "spike_sequences": spike_sequences,
        },
    )


def _coincidence_brain() -> IntegratedV04Brain:
    units = (
        UnitState(0, 0.0, 0.0, base_threshold=0.50),
        UnitState(1, 1.0, 0.0, base_threshold=0.50),
        UnitState(2, 2.0, 0.0, base_threshold=0.50),
        UnitState(3, 1.0, 1.0, base_threshold=0.90),
        UnitState(4, 0.5, 2.0, base_threshold=0.62),
        UnitState(5, 1.5, 2.0, base_threshold=0.62),
    )
    connections = (
        Connection(0, 3, 0.34, 6.0, plastic=False),
        Connection(1, 3, 0.34, 3.0, plastic=False),
        Connection(2, 3, 0.34, 0.5, plastic=False),
        Connection(3, 4, 0.75, 1.0, plastic=False),
        Connection(3, 5, 0.75, 1.0, plastic=False),
    )
    topology = explicit_topology(units, connections, receptor_ids=(0, 1, 2))
    return IntegratedV04Brain(
        V04BrainConfig(enable_plasticity=False, enable_expectations=False, settle_ms=20.0),
        topology=topology,
        field_config=ExcitableFieldConfig(receptor_fanout=1),
        burst_config=BurstDetectorConfig(window_ms=8.0, min_spikes=3, min_units=3),
        cascade_config=CascadeTrackerConfig(max_gap_ms=4.0, min_spikes=2),
        ignition_config=IgnitionGateConfig(threshold=2.4, min_spikes=3, min_units=3),
    )


def evaluate_coincidence(
    factory: Callable[[], IntegratedV04Brain] | None = None,
) -> ExperimentResult:
    metrics: dict[str, Any] = {}
    cases = weak_coincidence_cases()
    for case in cases:
        brain = factory() if factory is not None else _coincidence_brain()
        located = tuple(
            type(pulse)(
                time_ms=pulse.time_ms,
                channel=pulse.channel,
                magnitude=0.62,
                polarity=pulse.polarity,
                location=(float(index), 0.0),
                novelty=pulse.novelty,
                prediction_error=pulse.prediction_error,
                source_id=pulse.source_id,
                metadata=pulse.metadata,
            )
            for index, pulse in enumerate(case.pulses)
        )
        result = brain.ingest_pulses(located)
        flush = brain.advance(brain.current_time_ms + 5.0)
        spikes = result.spikes + flush.spikes
        bursts = result.bursts + flush.bursts
        ignitions = result.ignitions + flush.ignitions
        metrics[case.name] = {
            "burst_count": len(bursts),
            "convergence_unit_spikes": sum(1 for row in spikes if row.unit_id == 3),
            "ignition_count": len(ignitions),
            "spike_count": len(spikes),
        }
    metrics["aligned_minus_dispersed_spikes"] = (
        metrics["aligned"]["spike_count"] - metrics["dispersed"]["spike_count"]
    )
    return ExperimentResult("temporal_coincidence", metrics)


def _repetition_brain() -> IntegratedV04Brain:
    topology = explicit_topology(
        (UnitState(0, 0.0, 0.0, base_threshold=0.52),),
        (),
        receptor_ids=(0,),
    )
    return IntegratedV04Brain(
        V04BrainConfig(enable_plasticity=False, enable_expectations=True, settle_ms=1.0),
        topology=topology,
        field_config=ExcitableFieldConfig(
            receptor_fanout=1,
            adaptation_increment=0.28,
            adaptation_tau_ms=120.0,
        ),
        cascade_config=CascadeTrackerConfig(max_gap_ms=3.0, min_spikes=1),
        ignition_config=IgnitionGateConfig(threshold=99.0),
    )


def evaluate_repetition_and_omission(
    factory: Callable[[], IntegratedV04Brain] | None = None,
) -> ExperimentResult:
    brain = factory() if factory is not None else _repetition_brain()
    pulses = repetition_train(interval_ms=12.0)
    spike_counts: list[int] = []
    for pulse in pulses:
        result = brain.ingest_pulses((pulse,), settle_ms=1.0)
        spike_counts.append(len(result.spikes))
    omission_time = pulses[-1].time_ms + 30.0
    omission = brain.advance(omission_time)
    split = len(spike_counts) // 2
    return ExperimentResult(
        "repetition_omission",
        {
            "early_spikes": sum(spike_counts[:split]),
            "late_spikes": sum(spike_counts[split:]),
            "per_pulse_spikes": spike_counts,
            "omission_prediction_error_pulses": sum(
                1 for row in omission.input_pulses if row.channel.startswith("omission:")
            ),
            "omission_spikes": len(omission.spikes),
        },
    )


def evaluate_moving_point(
    factory: Callable[[], IntegratedV04Brain] | None = None,
) -> ExperimentResult:
    signatures: dict[str, list[str]] = {}
    for name, reverse in (("left_to_right", False), ("right_to_left", True)):
        brain = _new_brain(factory)
        time_ms = 0.0
        collected: list[str] = []
        for frame in moving_point_frames(reverse=reverse):
            result = brain.observe_frame(frame, time_ms=time_ms)
            collected.extend(row.signature for row in result.cascades)
            time_ms = brain.current_time_ms + 5.0
        signatures[name] = collected
    return ExperimentResult(
        "moving_point",
        {
            "direction_signatures_differ": signatures["left_to_right"]
            != signatures["right_to_left"],
            "signatures": signatures,
        },
    )


def evaluate_noisy_motif(
    factory: Callable[[], IntegratedV04Brain] | None = None,
) -> ExperimentResult:
    brain = _new_brain(factory)
    result = brain.ingest_pulses(noisy_motif_stream(), settle_ms=45.0)
    recurrent = [row for row in result.cascades if row.recurrence > 0]
    return ExperimentResult(
        "noisy_motif",
        {
            "cascade_count": len(result.cascades),
            "ignition_count": len(result.ignitions),
            "recurrent_cascade_count": len(recurrent),
            "spike_count": len(result.spikes),
        },
    )


def run_reference_experiments(
    *,
    config: V04BrainConfig | None = None,
) -> dict[str, Any]:
    def factory():
        return IntegratedV04Brain(config or V04BrainConfig())

    rows = (
        evaluate_temporal_order(factory),
        evaluate_coincidence(),
        evaluate_repetition_and_omission(),
        evaluate_moving_point(factory),
        evaluate_noisy_motif(factory),
    )
    return {
        "claim_boundary": (
            "engineering dynamics only; no semantic understanding, biological equivalence, "
            "energy advantage, concept formation, or general intelligence claim"
        ),
        "experiments": [row.as_dict() for row in rows],
        "schema": "sparkbrain-v04-reference-experiments-1",
    }

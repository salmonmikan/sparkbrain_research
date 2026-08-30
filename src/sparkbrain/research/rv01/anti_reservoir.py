from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import digest

from .direct_field_plasticity_probe import new_uniform_field
from .physical_missing_middle import run_physical_missing_middle_suite
from .physical_persistence_locus import run_physical_persistence_locus_suite

SEQUENCE = (0, 1, 2, 3)
CUE_TIME_MS = 100.0
HORIZON_MS = 132.0


class ExternalSequenceReadout:
    """Explicit external output model used only as an alternative explanation.

    It is not part of RV01 Field runtime. It can mimic a requested sequence at
    the output boundary while leaving all Field units and connections untouched.
    """

    def __init__(self) -> None:
        self._rows: dict[int, dict[tuple[int, ...], int]] = {}
        self.observation_count = 0
        self.output_count = 0

    def observe_sequence(
        self,
        sequence: tuple[int, ...],
        *,
        repetitions: int = 1,
    ) -> None:
        if len(sequence) < 2:
            raise ValueError("readout training sequence requires at least two units")
        if repetitions < 1:
            raise ValueError("repetitions must be positive")
        cue = sequence[0]
        output = sequence[1:]
        row = self._rows.setdefault(cue, {})
        row[output] = row.get(output, 0) + repetitions
        self.observation_count += repetitions

    def read(self, cue_unit_id: int) -> tuple[int, ...]:
        row = self._rows.get(cue_unit_id)
        if not row:
            return ()
        self.output_count += 1
        return min(row, key=lambda output: (-row[output], output))

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "observation_count": self.observation_count,
            "rows": {
                str(cue): {
                    ",".join(str(unit_id) for unit_id in output): count
                    for output, count in sorted(row.items())
                }
                for cue, row in sorted(self._rows.items())
            },
        }

    def state_dict(self) -> dict[str, Any]:
        return {
            **self.learned_state_dict(),
            "output_count": self.output_count,
        }

    @classmethod
    def from_learned_state_dict(
        cls,
        state: dict[str, Any],
    ) -> ExternalSequenceReadout:
        model = cls()
        model.observation_count = int(state["observation_count"])
        model._rows = {
            int(cue): {
                tuple(int(unit_id) for unit_id in output.split(",")): int(count)
                for output, count in row.items()
            }
            for cue, row in state["rows"].items()
        }
        return model

    def learned_state_hash(self) -> str:
        return digest(self.learned_state_dict())


@dataclass(frozen=True, slots=True)
class ReadoutAlternativeObservation:
    fixed_field_later_units: tuple[int, ...]
    readout_output: tuple[int, ...]
    reset_readout_output: tuple[int, ...]
    edge_suppressed_fixed_field_later_units: tuple[int, ...]
    edge_suppressed_readout_output: tuple[int, ...]
    transplanted_fixed_field_later_units: tuple[int, ...]
    transplanted_readout_output: tuple[int, ...]
    fixed_connection_hash: str
    edge_suppressed_connection_hash: str
    readout_learned_state_hash: str
    transplanted_readout_state_hash: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AntiReservoirAssessment:
    fixed_field_has_no_internal_continuation: bool
    external_readout_can_mimic_output: bool
    readout_removal_erases_output: bool
    physical_edge_intervention_does_not_change_readout: bool
    readout_transplant_moves_output_without_field_dynamics: bool
    rv01_field_continues_without_external_readout: bool
    rv01_internal_edge_intervention_changes_field_dynamics: bool
    rv01_connection_transplant_moves_field_dynamics: bool
    rv01_training_changes_recurrent_substrate: bool
    passive_fixed_reservoir_readout_rejected_for_internal_causality: bool
    generic_trainable_recurrent_explanation_remains_viable: bool
    architectural_uniqueness_established: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AntiReservoirSuite:
    readout_alternative: ReadoutAlternativeObservation
    rv01_trained_units: tuple[int, ...]
    rv01_untrained_units: tuple[int, ...]
    rv01_transplanted_units: tuple[int, ...]
    rv01_targeted_missing_middle_units: tuple[int, ...]
    rv01_matched_missing_middle_units: tuple[int, ...]
    assessment: AntiReservoirAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "readout_alternative": self.readout_alternative.state_dict(),
            "rv01_matched_missing_middle_units": list(
                self.rv01_matched_missing_middle_units
            ),
            "rv01_targeted_missing_middle_units": list(
                self.rv01_targeted_missing_middle_units
            ),
            "rv01_trained_units": list(self.rv01_trained_units),
            "rv01_transplanted_units": list(self.rv01_transplanted_units),
            "rv01_untrained_units": list(self.rv01_untrained_units),
            "suite_hash": self.suite_hash,
        }


def _connection_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "delay_ms": edge.delay_ms,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "weight": edge.weight,
            }
            for _, edge in sorted(field.connections.items())
        ]
    )


def _run_fixed_field(
    condition_id: str,
    *,
    suppress_edge: tuple[int, int] | None = None,
) -> tuple[tuple[int, ...], str]:
    field = new_uniform_field(4)
    if suppress_edge is not None:
        field.connection(*suppress_edge).weight = 0.0
    connection_hash = _connection_hash(field)
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
    return (
        tuple(row.unit_id for row in spikes if row.time_ms > CUE_TIME_MS),
        connection_hash,
    )


def _readout_alternative() -> ReadoutAlternativeObservation:
    readout = ExternalSequenceReadout()
    readout.observe_sequence(SEQUENCE, repetitions=3)
    learned_state = readout.learned_state_dict()
    readout_output = readout.read(SEQUENCE[0])

    fixed_units, fixed_hash = _run_fixed_field("fixed")
    edge_units, edge_hash = _run_fixed_field(
        "edge-suppressed",
        suppress_edge=(1, 2),
    )
    edge_readout = readout.read(SEQUENCE[0])

    reset_readout = ExternalSequenceReadout()
    reset_output = reset_readout.read(SEQUENCE[0])

    transplanted = ExternalSequenceReadout.from_learned_state_dict(learned_state)
    transplanted_output = transplanted.read(SEQUENCE[0])
    transplanted_units, _ = _run_fixed_field("readout-transplant")
    return ReadoutAlternativeObservation(
        fixed_field_later_units=fixed_units,
        readout_output=readout_output,
        reset_readout_output=reset_output,
        edge_suppressed_fixed_field_later_units=edge_units,
        edge_suppressed_readout_output=edge_readout,
        transplanted_fixed_field_later_units=transplanted_units,
        transplanted_readout_output=transplanted_output,
        fixed_connection_hash=fixed_hash,
        edge_suppressed_connection_hash=edge_hash,
        readout_learned_state_hash=digest(learned_state),
        transplanted_readout_state_hash=transplanted.learned_state_hash(),
    )


def run_anti_reservoir_suite() -> AntiReservoirSuite:
    readout = _readout_alternative()
    persistence = run_physical_persistence_locus_suite()
    causal = run_physical_missing_middle_suite()

    positive_values = {
        "fixed_field_has_no_internal_continuation": (
            readout.fixed_field_later_units == ()
        ),
        "external_readout_can_mimic_output": (
            readout.readout_output == SEQUENCE[1:]
        ),
        "readout_removal_erases_output": readout.reset_readout_output == (),
        "physical_edge_intervention_does_not_change_readout": (
            readout.edge_suppressed_readout_output == readout.readout_output
            and readout.edge_suppressed_fixed_field_later_units == ()
        ),
        "readout_transplant_moves_output_without_field_dynamics": (
            readout.transplanted_readout_output == readout.readout_output
            and readout.transplanted_fixed_field_later_units == ()
            and readout.transplanted_readout_state_hash
            == readout.readout_learned_state_hash
        ),
        "rv01_field_continues_without_external_readout": (
            persistence.trained.later_units == SEQUENCE[1:]
        ),
        "rv01_internal_edge_intervention_changes_field_dynamics": (
            causal.intact.downstream_unit_generated_before_late_input
            and not causal.targeted_main_middle_edge.downstream_unit_generated_before_late_input
            and causal.matched_control_middle_edge.downstream_unit_generated_before_late_input
        ),
        "rv01_connection_transplant_moves_field_dynamics": (
            persistence.full_connection_transplant.later_units
            == persistence.trained.later_units
            and persistence.full_connection_transplant.later_times_ms
            == persistence.trained.later_times_ms
        ),
        "rv01_training_changes_recurrent_substrate": (
            persistence.trained.connection_state_hash
            != persistence.untrained.connection_state_hash
        ),
        "passive_fixed_reservoir_readout_rejected_for_internal_causality": (
            readout.readout_output == SEQUENCE[1:]
            and readout.fixed_field_later_units == ()
            and readout.edge_suppressed_readout_output == readout.readout_output
            and causal.assessment.selective_causal_effect == 1.0
        ),
        "generic_trainable_recurrent_explanation_remains_viable": True,
    }
    assessment = AntiReservoirAssessment(
        **positive_values,
        architectural_uniqueness_established=False,
        engineering_candidate=all(positive_values.values()),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "readout_alternative": readout.state_dict(),
        "rv01_matched_missing_middle_units": (
            causal.matched_control_middle_edge.pre_late_units
        ),
        "rv01_targeted_missing_middle_units": (
            causal.targeted_main_middle_edge.pre_late_units
        ),
        "rv01_trained_units": persistence.trained.later_units,
        "rv01_transplanted_units": (
            persistence.full_connection_transplant.later_units
        ),
        "rv01_untrained_units": persistence.untrained.later_units,
    }
    return AntiReservoirSuite(
        readout_alternative=readout,
        rv01_trained_units=persistence.trained.later_units,
        rv01_untrained_units=persistence.untrained.later_units,
        rv01_transplanted_units=(
            persistence.full_connection_transplant.later_units
        ),
        rv01_targeted_missing_middle_units=(
            causal.targeted_main_middle_edge.pre_late_units
        ),
        rv01_matched_missing_middle_units=(
            causal.matched_control_middle_edge.pre_late_units
        ),
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

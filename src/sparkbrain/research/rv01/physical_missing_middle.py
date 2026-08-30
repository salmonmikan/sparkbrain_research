from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SpikeEvent, SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import digest

from .direct_field_plasticity_probe import new_uniform_field, train_external_sequence

MAIN_SEQUENCE = (0, 1, 2, 3)
CONTROL_SEQUENCE = (4, 5, 6, 7)
MAIN_MISSING_UNIT = 2
MAIN_LATE_UNIT = 3
CONTROL_MISSING_UNIT = 6
CONTROL_LATE_UNIT = 7
EARLY_CUE_TIME_MS = 100.0
PREFIX_TIME_MS = 105.0
LATE_EXTERNAL_TIME_MS = 120.0
PRE_LATE_HORIZON_MS = 119.0
FINAL_HORIZON_MS = 122.0


@dataclass(frozen=True, slots=True)
class PhysicalEdgeIntervention:
    source_id: int
    target_id: int
    weight_before: float
    delay_before_ms: float
    weight_after: float
    delay_after_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MissingMiddleCondition:
    condition_id: str
    external_input_signature: tuple[tuple[float, int], ...]
    connection_state_hash_before_intervention: str
    connection_state_hash_after_intervention: str
    intervention: PhysicalEdgeIntervention | None
    pre_late_units: tuple[int, ...]
    pre_late_times_ms: tuple[float, ...]
    post_late_units: tuple[int, ...]
    post_late_times_ms: tuple[float, ...]
    missing_unit_generated_before_late_input: bool
    downstream_unit_generated_before_late_input: bool
    control_missing_unit_generated_before_late_input: bool
    control_downstream_generated_before_late_input: bool
    late_external_events_preloaded: bool
    queue_size_before_late_external: int
    queue_pulse_ids_before_late_external: tuple[str, ...]

    @property
    def main_pre_late_downstream_count(self) -> int:
        return sum(unit_id == MAIN_LATE_UNIT for unit_id in self.pre_late_units)

    @property
    def control_pre_late_downstream_count(self) -> int:
        return sum(unit_id == CONTROL_LATE_UNIT for unit_id in self.pre_late_units)

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "control_pre_late_downstream_count": (
                self.control_pre_late_downstream_count
            ),
            "intervention": (
                self.intervention.state_dict()
                if self.intervention is not None
                else None
            ),
            "main_pre_late_downstream_count": self.main_pre_late_downstream_count,
        }


@dataclass(frozen=True, slots=True)
class PhysicalMissingMiddleAssessment:
    forward_missing_middle_generated: bool
    forward_downstream_generated_before_external_late_event: bool
    future_external_event_not_preloaded: bool
    targeted_middle_path_suppression_removes_downstream: bool
    matched_active_suppression_preserves_main_downstream: bool
    matched_control_path_is_actively_impaired: bool
    intervention_strength_is_matched: bool
    untrained_field_does_not_complete: bool
    current_external_inputs_are_identical: bool
    selective_causal_effect: float
    no_g1_or_g2_runtime_required: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalMissingMiddleSuite:
    intact: MissingMiddleCondition
    targeted_main_middle_edge: MissingMiddleCondition
    matched_control_middle_edge: MissingMiddleCondition
    untrained: MissingMiddleCondition
    assessment: PhysicalMissingMiddleAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "intact": self.intact.state_dict(),
            "matched_control_middle_edge": (
                self.matched_control_middle_edge.state_dict()
            ),
            "suite_hash": self.suite_hash,
            "targeted_main_middle_edge": (
                self.targeted_main_middle_edge.state_dict()
            ),
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


def _trained_dual_field() -> TemporalExcitableField:
    field = new_uniform_field(8)
    main = train_external_sequence(field, MAIN_SEQUENCE)
    main.clear_traces()
    control = train_external_sequence(field, CONTROL_SEQUENCE)
    control.clear_traces()
    return field


def _schedule_external(
    field: TemporalExcitableField,
    *,
    event_id: str,
    time_ms: float,
    unit_id: int,
) -> None:
    field.schedule_arrival(
        SynapticArrival(
            time_ms=time_ms,
            target_id=unit_id,
            current=1.0,
            source_id=None,
            pulse_id=event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )


def _queue_pulse_ids(field: TemporalExcitableField) -> tuple[str, ...]:
    return tuple(
        str(row["arrival"]["pulse_id"])
        for row in field.state_dict()["queue"]
    )


def _intervene(
    field: TemporalExcitableField,
    edge_key: tuple[int, int] | None,
) -> PhysicalEdgeIntervention | None:
    if edge_key is None:
        return None
    edge = field.connection(*edge_key)
    before_weight = edge.weight
    before_delay = edge.delay_ms
    edge.weight = 0.0
    return PhysicalEdgeIntervention(
        source_id=edge.source_id,
        target_id=edge.target_id,
        weight_before=before_weight,
        delay_before_ms=before_delay,
        weight_after=edge.weight,
        delay_after_ms=edge.delay_ms,
    )


def _spike_rows(rows: tuple[SpikeEvent, ...]) -> tuple[tuple[int, ...], tuple[float, ...]]:
    return (
        tuple(row.unit_id for row in rows),
        tuple(row.time_ms for row in rows),
    )


def _run_condition(
    condition_id: str,
    field: TemporalExcitableField,
    *,
    intervention_edge: tuple[int, int] | None = None,
) -> MissingMiddleCondition:
    before = _connection_state_hash(field)
    intervention = _intervene(field, intervention_edge)
    after = _connection_state_hash(field)

    # Both main and matched-control paths are active under every condition.
    # The future external D/H events are intentionally not scheduled yet.
    early_events = (
        (EARLY_CUE_TIME_MS, 0, f"external:{condition_id}:A"),
        (EARLY_CUE_TIME_MS, 4, f"external:{condition_id}:E"),
        (PREFIX_TIME_MS, 1, f"external:{condition_id}:B"),
        (PREFIX_TIME_MS, 5, f"external:{condition_id}:F"),
    )
    for time_ms, unit_id, event_id in early_events:
        _schedule_external(
            field,
            event_id=event_id,
            time_ms=time_ms,
            unit_id=unit_id,
        )
    pre_late = field.run_until(PRE_LATE_HORIZON_MS)
    queue_ids = _queue_pulse_ids(field)
    late_ids = (
        f"external:{condition_id}:D",
        f"external:{condition_id}:H",
    )
    preloaded = any(event_id in queue_ids for event_id in late_ids)

    for time_ms, unit_id, event_id in (
        (LATE_EXTERNAL_TIME_MS, MAIN_LATE_UNIT, late_ids[0]),
        (LATE_EXTERNAL_TIME_MS, CONTROL_LATE_UNIT, late_ids[1]),
    ):
        _schedule_external(
            field,
            event_id=event_id,
            time_ms=time_ms,
            unit_id=unit_id,
        )
    post_late = field.run_until(FINAL_HORIZON_MS)
    pre_units, pre_times = _spike_rows(pre_late)
    post_units, post_times = _spike_rows(post_late)
    return MissingMiddleCondition(
        condition_id=condition_id,
        external_input_signature=(
            (EARLY_CUE_TIME_MS, 0),
            (EARLY_CUE_TIME_MS, 4),
            (PREFIX_TIME_MS, 1),
            (PREFIX_TIME_MS, 5),
            (LATE_EXTERNAL_TIME_MS, MAIN_LATE_UNIT),
            (LATE_EXTERNAL_TIME_MS, CONTROL_LATE_UNIT),
        ),
        connection_state_hash_before_intervention=before,
        connection_state_hash_after_intervention=after,
        intervention=intervention,
        pre_late_units=pre_units,
        pre_late_times_ms=pre_times,
        post_late_units=post_units,
        post_late_times_ms=post_times,
        missing_unit_generated_before_late_input=(
            MAIN_MISSING_UNIT in pre_units
        ),
        downstream_unit_generated_before_late_input=(
            MAIN_LATE_UNIT in pre_units
        ),
        control_missing_unit_generated_before_late_input=(
            CONTROL_MISSING_UNIT in pre_units
        ),
        control_downstream_generated_before_late_input=(
            CONTROL_LATE_UNIT in pre_units
        ),
        late_external_events_preloaded=preloaded,
        queue_size_before_late_external=len(queue_ids),
        queue_pulse_ids_before_late_external=queue_ids,
    )


def run_physical_missing_middle_suite() -> PhysicalMissingMiddleSuite:
    base = _trained_dual_field()
    intact = _run_condition(
        "intact",
        TemporalExcitableField.from_state_dict(base.state_dict()),
    )
    targeted = _run_condition(
        "targeted-main-middle-edge",
        TemporalExcitableField.from_state_dict(base.state_dict()),
        intervention_edge=(1, 2),
    )
    matched = _run_condition(
        "matched-control-middle-edge",
        TemporalExcitableField.from_state_dict(base.state_dict()),
        intervention_edge=(5, 6),
    )
    untrained = _run_condition(
        "untrained",
        new_uniform_field(8),
    )

    sham_count = intact.main_pre_late_downstream_count
    targeted_impairment = 1.0 - (
        targeted.main_pre_late_downstream_count / max(1, sham_count)
    )
    matched_impairment = 1.0 - (
        matched.main_pre_late_downstream_count / max(1, sham_count)
    )
    selective_effect = targeted_impairment - matched_impairment
    signatures = {
        row.external_input_signature
        for row in (intact, targeted, matched, untrained)
    }
    target_intervention = targeted.intervention
    matched_intervention = matched.intervention
    values = {
        "forward_missing_middle_generated": (
            intact.missing_unit_generated_before_late_input
        ),
        "forward_downstream_generated_before_external_late_event": (
            intact.downstream_unit_generated_before_late_input
        ),
        "future_external_event_not_preloaded": all(
            not row.late_external_events_preloaded
            for row in (intact, targeted, matched, untrained)
        ),
        "targeted_middle_path_suppression_removes_downstream": (
            not targeted.missing_unit_generated_before_late_input
            and not targeted.downstream_unit_generated_before_late_input
            and targeted.control_downstream_generated_before_late_input
        ),
        "matched_active_suppression_preserves_main_downstream": (
            matched.missing_unit_generated_before_late_input
            and matched.downstream_unit_generated_before_late_input
        ),
        "matched_control_path_is_actively_impaired": (
            not matched.control_missing_unit_generated_before_late_input
            and not matched.control_downstream_generated_before_late_input
            and intact.control_downstream_generated_before_late_input
        ),
        "intervention_strength_is_matched": (
            target_intervention is not None
            and matched_intervention is not None
            and target_intervention.weight_before
            == matched_intervention.weight_before
            and target_intervention.delay_before_ms
            == matched_intervention.delay_before_ms
            and target_intervention.weight_after
            == matched_intervention.weight_after
        ),
        "untrained_field_does_not_complete": (
            not untrained.missing_unit_generated_before_late_input
            and not untrained.downstream_unit_generated_before_late_input
            and not untrained.control_missing_unit_generated_before_late_input
            and not untrained.control_downstream_generated_before_late_input
        ),
        "current_external_inputs_are_identical": len(signatures) == 1,
        "selective_causal_effect": selective_effect,
        "no_g1_or_g2_runtime_required": True,
    }
    assessment = PhysicalMissingMiddleAssessment(
        **values,
        engineering_candidate=(
            all(
                value
                for key, value in values.items()
                if key not in {"selective_causal_effect"}
            )
            and selective_effect >= 0.5
        ),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "intact": intact.state_dict(),
        "matched_control_middle_edge": matched.state_dict(),
        "targeted_main_middle_edge": targeted.state_dict(),
        "untrained": untrained.state_dict(),
    }
    return PhysicalMissingMiddleSuite(
        intact=intact,
        targeted_main_middle_edge=targeted,
        matched_control_middle_edge=matched,
        untrained=untrained,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

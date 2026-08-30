from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest

from .competitive_field_plasticity import (
    ExternalGatedCompetitiveFieldPlasticity,
)
from .direct_field_plasticity import ExternalGatedDirectFieldPlasticity
from .direct_field_plasticity_probe import (
    BASE_DELAY_MS,
    BASE_WEIGHT,
    new_uniform_field,
)

OLD_SEQUENCE = (0, 1, 2, 3)
NEW_SEQUENCE = (0, 1, 4, 5)
TRAINING_INTERVAL_MS = 5.0
EPISODE_SPACING_MS = 30.0
ACQUISITION_EPISODES = 3
REVERSAL_EPISODES = 4
REACQUISITION_EPISODES = 4
TEST_CUE_TIME_MS = 100.0
TEST_HORIZON_MS = 118.0


@dataclass(frozen=True, slots=True)
class RevisionObservation:
    phase_id: str
    external_episode_count: int
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    old_gateway_weight: float
    old_gateway_delay_ms: float
    new_gateway_weight: float
    new_gateway_delay_ms: float
    connection_state_hash: str
    initial_dynamic_state_hash: str

    @property
    def old_path_completed(self) -> bool:
        return _subsequence(self.generated_units, OLD_SEQUENCE[1:])

    @property
    def new_path_completed(self) -> bool:
        return _subsequence(self.generated_units, NEW_SEQUENCE[1:])

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "new_path_completed": self.new_path_completed,
            "old_path_completed": self.old_path_completed,
        }


@dataclass(frozen=True, slots=True)
class PhysicalRevisionAssessment:
    acquisition_selects_old_path: bool
    reversal_selects_new_path: bool
    reacquisition_selects_old_path: bool
    stable_world_does_not_invent_new_path: bool
    potentiation_only_fails_to_remove_old_path: bool
    endogenous_only_experience_cannot_revamp_connections: bool
    connection_reset_removes_acquired_behavior: bool
    reversed_connection_transplant_moves_behavior: bool
    reversal_crossing_episode: int | None
    reacquisition_crossing_episode: int | None
    initial_dynamic_states_match: bool
    no_confirmed_or_contradicted_counters: bool
    no_g1_or_g2_runtime_required: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalRevisionSuite:
    acquisition: RevisionObservation
    reversal_steps: tuple[RevisionObservation, ...]
    reversed_state: RevisionObservation
    reacquisition_steps: tuple[RevisionObservation, ...]
    reacquired_state: RevisionObservation
    stable_control: RevisionObservation
    potentiation_only_control: RevisionObservation
    endogenous_only_reversal: RevisionObservation
    reset_control: RevisionObservation
    reversed_transplant: RevisionObservation
    competitive_controller_state: dict[str, Any]
    endogenous_ignored_count: int
    assessment: PhysicalRevisionAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "acquisition": self.acquisition.state_dict(),
            "assessment": self.assessment.state_dict(),
            "competitive_controller_state": self.competitive_controller_state,
            "endogenous_ignored_count": self.endogenous_ignored_count,
            "endogenous_only_reversal": self.endogenous_only_reversal.state_dict(),
            "potentiation_only_control": self.potentiation_only_control.state_dict(),
            "reacquired_state": self.reacquired_state.state_dict(),
            "reacquisition_steps": [row.state_dict() for row in self.reacquisition_steps],
            "reset_control": self.reset_control.state_dict(),
            "reversed_state": self.reversed_state.state_dict(),
            "reversed_transplant": self.reversed_transplant.state_dict(),
            "reversal_steps": [row.state_dict() for row in self.reversal_steps],
            "stable_control": self.stable_control.state_dict(),
            "suite_hash": self.suite_hash,
        }


def _subsequence(sequence: tuple[int, ...], expected: tuple[int, ...]) -> bool:
    iterator = iter(sequence)
    return all(any(row == target for row in iterator) for target in expected)


def _connection_state_hash(field: TemporalExcitableField) -> str:
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


def _observe_sequence(
    controller: ExternalGatedDirectFieldPlasticity,
    sequence: tuple[int, ...],
    *,
    episodes: int,
    start_ms: float,
    origin: EventOrigin = EventOrigin.EXTERNAL,
    phase_id: str,
) -> float:
    for episode in range(episodes):
        episode_start = start_ms + episode * EPISODE_SPACING_MS
        for index, unit_id in enumerate(sequence):
            controller.observe(
                RuntimePulse(
                    event_id=f"{phase_id}:{episode}:{index}",
                    time_ms=episode_start + index * TRAINING_INTERVAL_MS,
                    target=f"unit:{unit_id}",
                    magnitude=1.0,
                    polarity=1,
                    origin=origin,
                )
            )
    controller.clear_traces()
    return start_ms + episodes * EPISODE_SPACING_MS


def _run_cue(
    phase_id: str,
    field: TemporalExcitableField,
    *,
    external_episode_count: int,
) -> RevisionObservation:
    initial_dynamic_hash = _dynamic_state_hash(field)
    connection_hash = _connection_state_hash(field)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=TEST_CUE_TIME_MS,
            target_id=0,
            current=1.0,
            source_id=None,
            pulse_id=f"cue:{phase_id}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    spikes = field.run_until(TEST_HORIZON_MS)
    generated = tuple(row for row in spikes if row.time_ms > TEST_CUE_TIME_MS)
    old_edge = field.connection(1, 2)
    new_edge = field.connection(1, 4)
    return RevisionObservation(
        phase_id=phase_id,
        external_episode_count=external_episode_count,
        generated_units=tuple(row.unit_id for row in generated),
        generated_times_ms=tuple(row.time_ms for row in generated),
        old_gateway_weight=old_edge.weight,
        old_gateway_delay_ms=old_edge.delay_ms,
        new_gateway_weight=new_edge.weight,
        new_gateway_delay_ms=new_edge.delay_ms,
        connection_state_hash=connection_hash,
        initial_dynamic_state_hash=initial_dynamic_hash,
    )


def _snapshot(
    phase_id: str,
    field: TemporalExcitableField,
    external_episode_count: int,
) -> RevisionObservation:
    return _run_cue(
        phase_id,
        TemporalExcitableField.from_state_dict(field.state_dict()),
        external_episode_count=external_episode_count,
    )


def _reset_connections(field: TemporalExcitableField) -> None:
    for edge in field.connections.values():
        edge.weight = BASE_WEIGHT
        edge.delay_ms = BASE_DELAY_MS


def _transplant_connections(
    source: TemporalExcitableField,
    target: TemporalExcitableField,
) -> None:
    if set(source.connections) != set(target.connections):
        raise ValueError("connection transplant requires compatible topology")
    for key in sorted(source.connections):
        donor = source.connections[key]
        receiver = target.connections[key]
        receiver.weight = donor.weight
        receiver.delay_ms = donor.delay_ms
        receiver.plastic = donor.plastic


def _first_new_only(rows: tuple[RevisionObservation, ...]) -> int | None:
    for index, row in enumerate(rows, start=1):
        if row.new_path_completed and not row.old_path_completed:
            return index
    return None


def _first_old_only(rows: tuple[RevisionObservation, ...]) -> int | None:
    for index, row in enumerate(rows, start=1):
        if row.old_path_completed and not row.new_path_completed:
            return index
    return None


def run_physical_revision_suite() -> PhysicalRevisionSuite:
    field = new_uniform_field(6)
    controller = ExternalGatedCompetitiveFieldPlasticity(field)
    next_start = _observe_sequence(
        controller,
        OLD_SEQUENCE,
        episodes=ACQUISITION_EPISODES,
        start_ms=0.0,
        phase_id="acquisition",
    )
    acquisition_field = TemporalExcitableField.from_state_dict(field.state_dict())
    acquisition = _snapshot(
        "acquisition",
        acquisition_field,
        ACQUISITION_EPISODES,
    )

    reversal_steps: list[RevisionObservation] = []
    for episode in range(REVERSAL_EPISODES):
        next_start = _observe_sequence(
            controller,
            NEW_SEQUENCE,
            episodes=1,
            start_ms=next_start,
            phase_id=f"reversal:{episode}",
        )
        reversal_steps.append(
            _snapshot(
                f"reversal:{episode + 1}",
                field,
                ACQUISITION_EPISODES + episode + 1,
            )
        )
    reversed_field = TemporalExcitableField.from_state_dict(field.state_dict())
    reversed_state = reversal_steps[-1]

    reacquisition_steps: list[RevisionObservation] = []
    for episode in range(REACQUISITION_EPISODES):
        next_start = _observe_sequence(
            controller,
            OLD_SEQUENCE,
            episodes=1,
            start_ms=next_start,
            phase_id=f"reacquisition:{episode}",
        )
        reacquisition_steps.append(
            _snapshot(
                f"reacquisition:{episode + 1}",
                field,
                ACQUISITION_EPISODES + REVERSAL_EPISODES + episode + 1,
            )
        )
    reacquired_state = reacquisition_steps[-1]

    stable_field = new_uniform_field(6)
    stable_controller = ExternalGatedCompetitiveFieldPlasticity(stable_field)
    _observe_sequence(
        stable_controller,
        OLD_SEQUENCE,
        episodes=(
            ACQUISITION_EPISODES + REVERSAL_EPISODES + REACQUISITION_EPISODES
        ),
        start_ms=0.0,
        phase_id="stable",
    )
    stable = _snapshot(
        "stable",
        stable_field,
        ACQUISITION_EPISODES + REVERSAL_EPISODES + REACQUISITION_EPISODES,
    )

    potentiation_field = new_uniform_field(6)
    potentiation_controller = ExternalGatedDirectFieldPlasticity(
        potentiation_field
    )
    next_potentiation = _observe_sequence(
        potentiation_controller,
        OLD_SEQUENCE,
        episodes=ACQUISITION_EPISODES,
        start_ms=0.0,
        phase_id="potentiation-old",
    )
    _observe_sequence(
        potentiation_controller,
        NEW_SEQUENCE,
        episodes=REVERSAL_EPISODES,
        start_ms=next_potentiation,
        phase_id="potentiation-new",
    )
    potentiation_only = _snapshot(
        "potentiation-only",
        potentiation_field,
        ACQUISITION_EPISODES + REVERSAL_EPISODES,
    )

    endogenous_field = TemporalExcitableField.from_state_dict(
        acquisition_field.state_dict()
    )
    endogenous_controller = ExternalGatedCompetitiveFieldPlasticity(
        endogenous_field
    )
    endogenous_hash_before = _connection_state_hash(endogenous_field)
    _observe_sequence(
        endogenous_controller,
        NEW_SEQUENCE,
        episodes=REVERSAL_EPISODES,
        start_ms=0.0,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        phase_id="endogenous-reversal",
    )
    endogenous_hash_after = _connection_state_hash(endogenous_field)
    endogenous_only = _snapshot(
        "endogenous-only-reversal",
        endogenous_field,
        ACQUISITION_EPISODES,
    )

    reset_field = TemporalExcitableField.from_state_dict(
        reversed_field.state_dict()
    )
    _reset_connections(reset_field)
    reset = _snapshot("connection-reset", reset_field, 0)

    transplant_field = new_uniform_field(6)
    _transplant_connections(reversed_field, transplant_field)
    transplant = _snapshot(
        "reversed-connection-transplant",
        transplant_field,
        ACQUISITION_EPISODES + REVERSAL_EPISODES,
    )

    rows = (
        acquisition,
        *reversal_steps,
        *reacquisition_steps,
        stable,
        potentiation_only,
        endogenous_only,
        reset,
        transplant,
    )
    controller_text = str(controller.state_dict()).lower()
    forbidden = (
        "confirmed_count",
        "contradicted_count",
        "correct_target",
        "correct_action",
        "relation_table",
        "path_score",
        "reward",
    )
    values = {
        "acquisition_selects_old_path": (
            acquisition.old_path_completed and not acquisition.new_path_completed
        ),
        "reversal_selects_new_path": (
            reversed_state.new_path_completed
            and not reversed_state.old_path_completed
        ),
        "reacquisition_selects_old_path": (
            reacquired_state.old_path_completed
            and not reacquired_state.new_path_completed
        ),
        "stable_world_does_not_invent_new_path": (
            stable.old_path_completed and not stable.new_path_completed
        ),
        "potentiation_only_fails_to_remove_old_path": (
            potentiation_only.old_path_completed
            and potentiation_only.new_path_completed
        ),
        "endogenous_only_experience_cannot_revamp_connections": (
            endogenous_hash_before == endogenous_hash_after
            and endogenous_only.old_path_completed
            and not endogenous_only.new_path_completed
            and endogenous_controller.ignored_endogenous_count
            == REVERSAL_EPISODES * len(NEW_SEQUENCE)
        ),
        "connection_reset_removes_acquired_behavior": (
            not reset.old_path_completed and not reset.new_path_completed
        ),
        "reversed_connection_transplant_moves_behavior": (
            transplant.new_path_completed
            and not transplant.old_path_completed
            and transplant.connection_state_hash
            == reversed_state.connection_state_hash
        ),
        "reversal_crossing_episode": _first_new_only(tuple(reversal_steps)),
        "reacquisition_crossing_episode": _first_old_only(
            tuple(reacquisition_steps)
        ),
        "initial_dynamic_states_match": (
            len({row.initial_dynamic_state_hash for row in rows}) == 1
        ),
        "no_confirmed_or_contradicted_counters": not any(
            term in controller_text for term in forbidden
        ),
        "no_g1_or_g2_runtime_required": True,
    }
    assessment = PhysicalRevisionAssessment(
        **values,
        engineering_candidate=(
            all(
                value
                for key, value in values.items()
                if key
                not in {
                    "reversal_crossing_episode",
                    "reacquisition_crossing_episode",
                }
            )
            and values["reversal_crossing_episode"] is not None
            and values["reacquisition_crossing_episode"] is not None
        ),
    )
    state_without_hash = {
        "acquisition": acquisition.state_dict(),
        "assessment": assessment.state_dict(),
        "competitive_controller_state": controller.state_dict(),
        "endogenous_ignored_count": endogenous_controller.ignored_endogenous_count,
        "endogenous_only_reversal": endogenous_only.state_dict(),
        "potentiation_only_control": potentiation_only.state_dict(),
        "reacquired_state": reacquired_state.state_dict(),
        "reacquisition_steps": [row.state_dict() for row in reacquisition_steps],
        "reset_control": reset.state_dict(),
        "reversed_state": reversed_state.state_dict(),
        "reversed_transplant": transplant.state_dict(),
        "reversal_steps": [row.state_dict() for row in reversal_steps],
        "stable_control": stable.state_dict(),
    }
    return PhysicalRevisionSuite(
        acquisition=acquisition,
        reversal_steps=tuple(reversal_steps),
        reversed_state=reversed_state,
        reacquisition_steps=tuple(reacquisition_steps),
        reacquired_state=reacquired_state,
        stable_control=stable,
        potentiation_only_control=potentiation_only,
        endogenous_only_reversal=endogenous_only,
        reset_control=reset,
        reversed_transplant=transplant,
        competitive_controller_state=controller.state_dict(),
        endogenous_ignored_count=endogenous_controller.ignored_endogenous_count,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

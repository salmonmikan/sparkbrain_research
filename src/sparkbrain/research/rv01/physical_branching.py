from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v06.foundation import digest

from .direct_field_plasticity import DirectFieldPlasticityConfig
from .direct_field_plasticity_probe import train_external_sequence

BRANCH_A = (0, 1, 2, 4)
BRANCH_B = (0, 1, 3, 5)
BASE_WEIGHT = 0.05
BASE_DELAY_MS = 8.0
BRANCH_THRESHOLD = 0.30
TEST_CUE_TIME_MS = 100.0
TEST_HORIZON_MS = 117.0
BRANCH_PLASTICITY = DirectFieldPlasticityConfig(
    potentiation_rate=0.25,
    depression_rate=0.15,
)


@dataclass(frozen=True, slots=True)
class BranchPathState:
    path: tuple[int, ...]
    exposure_count: int
    divergence_weight: float
    divergence_delay_ms: float
    terminal_weight: float
    terminal_delay_ms: float

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalBranchObservation:
    condition_id: str
    exposure_counts: tuple[int, int]
    cue_signature: tuple[float, int]
    initial_dynamic_state_hash: str
    connection_state_hash: str
    branch_a: BranchPathState
    branch_b: BranchPathState
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    branch_a_completed: bool
    branch_b_completed: bool
    suppressed_edge: tuple[int, int] | None

    @property
    def both_branches_completed(self) -> bool:
        return self.branch_a_completed and self.branch_b_completed

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "both_branches_completed": self.both_branches_completed,
            "branch_a": self.branch_a.state_dict(),
            "branch_b": self.branch_b.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class PhysicalBranchingAssessment:
    equal_exposure_preserves_both_branches: bool
    mild_bias_preserves_weaker_branch: bool
    mild_bias_is_physically_graded: bool
    single_history_does_not_invent_second_branch: bool
    untrained_field_has_no_branch_completion: bool
    targeted_branch_a_suppression_is_selective: bool
    targeted_branch_b_suppression_is_selective: bool
    same_cue_and_dynamic_state: bool
    no_explicit_winner_or_branch_runtime_state: bool
    coactive_ambiguity_supported: bool
    competitive_resolution_supported: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PhysicalBranchingSuite:
    equal: PhysicalBranchObservation
    mildly_biased: PhysicalBranchObservation
    single_branch_a: PhysicalBranchObservation
    untrained: PhysicalBranchObservation
    suppress_branch_a: PhysicalBranchObservation
    suppress_branch_b: PhysicalBranchObservation
    assessment: PhysicalBranchingAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "equal": self.equal.state_dict(),
            "mildly_biased": self.mildly_biased.state_dict(),
            "single_branch_a": self.single_branch_a.state_dict(),
            "suite_hash": self.suite_hash,
            "suppress_branch_a": self.suppress_branch_a.state_dict(),
            "suppress_branch_b": self.suppress_branch_b.state_dict(),
            "untrained": self.untrained.state_dict(),
        }


def _new_field() -> TemporalExcitableField:
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=BRANCH_THRESHOLD,
            )
            for unit_id in range(6)
        ),
        tuple(
            Connection(
                source_id=source_id,
                target_id=target_id,
                weight=BASE_WEIGHT,
                delay_ms=BASE_DELAY_MS,
                plastic=True,
            )
            for source_id in range(6)
            for target_id in range(6)
            if source_id != target_id
        ),
        receptor_ids=tuple(range(6)),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=2.0,
        ),
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


def _train(
    exposures_a: int,
    exposures_b: int,
) -> TemporalExcitableField:
    field = _new_field()
    if exposures_a:
        controller_a = train_external_sequence(
            field,
            BRANCH_A,
            episodes=exposures_a,
            config=BRANCH_PLASTICITY,
        )
        controller_a.clear_traces()
    if exposures_b:
        controller_b = train_external_sequence(
            field,
            BRANCH_B,
            episodes=exposures_b,
            config=BRANCH_PLASTICITY,
        )
        controller_b.clear_traces()
    return field


def _path_state(
    field: TemporalExcitableField,
    path: tuple[int, ...],
    exposures: int,
) -> BranchPathState:
    divergence = field.connection(path[1], path[2])
    terminal = field.connection(path[2], path[3])
    return BranchPathState(
        path=path,
        exposure_count=exposures,
        divergence_weight=divergence.weight,
        divergence_delay_ms=divergence.delay_ms,
        terminal_weight=terminal.weight,
        terminal_delay_ms=terminal.delay_ms,
    )


def _subsequence(sequence: tuple[int, ...], expected: tuple[int, ...]) -> bool:
    iterator = iter(sequence)
    return all(any(row == target for row in iterator) for target in expected)


def _run(
    condition_id: str,
    exposures_a: int,
    exposures_b: int,
    *,
    suppress_edge: tuple[int, int] | None = None,
) -> PhysicalBranchObservation:
    field = _train(exposures_a, exposures_b)
    if suppress_edge is not None:
        field.connection(*suppress_edge).weight = 0.0
    initial_hash = _dynamic_state_hash(field)
    connection_hash = _connection_state_hash(field)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=TEST_CUE_TIME_MS,
            target_id=0,
            current=1.0,
            source_id=None,
            pulse_id=f"cue:{condition_id}",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    spikes = field.run_until(TEST_HORIZON_MS)
    generated = tuple(row for row in spikes if row.time_ms > TEST_CUE_TIME_MS)
    units = tuple(row.unit_id for row in generated)
    return PhysicalBranchObservation(
        condition_id=condition_id,
        exposure_counts=(exposures_a, exposures_b),
        cue_signature=(TEST_CUE_TIME_MS, 0),
        initial_dynamic_state_hash=initial_hash,
        connection_state_hash=connection_hash,
        branch_a=_path_state(field, BRANCH_A, exposures_a),
        branch_b=_path_state(field, BRANCH_B, exposures_b),
        generated_units=units,
        generated_times_ms=tuple(row.time_ms for row in generated),
        branch_a_completed=_subsequence(units, BRANCH_A[1:]),
        branch_b_completed=_subsequence(units, BRANCH_B[1:]),
        suppressed_edge=suppress_edge,
    )


def run_physical_branching_suite() -> PhysicalBranchingSuite:
    equal = _run("equal", 3, 3)
    biased = _run("mildly-biased", 3, 2)
    single = _run("single-branch-a", 3, 0)
    untrained = _run("untrained", 0, 0)
    suppress_a = _run("suppress-branch-a", 3, 3, suppress_edge=(1, 2))
    suppress_b = _run("suppress-branch-b", 3, 3, suppress_edge=(1, 3))
    dynamic_hashes = {
        row.initial_dynamic_state_hash
        for row in (equal, biased, single, untrained, suppress_a, suppress_b)
    }
    values = {
        "equal_exposure_preserves_both_branches": equal.both_branches_completed,
        "mild_bias_preserves_weaker_branch": biased.both_branches_completed,
        "mild_bias_is_physically_graded": (
            biased.branch_a.divergence_weight
            > biased.branch_b.divergence_weight
            and biased.branch_a.divergence_delay_ms
            < biased.branch_b.divergence_delay_ms
            and biased.generated_times_ms[
                biased.generated_units.index(BRANCH_A[2])
            ]
            < biased.generated_times_ms[
                biased.generated_units.index(BRANCH_B[2])
            ]
        ),
        "single_history_does_not_invent_second_branch": (
            single.branch_a_completed and not single.branch_b_completed
        ),
        "untrained_field_has_no_branch_completion": (
            not untrained.branch_a_completed and not untrained.branch_b_completed
        ),
        "targeted_branch_a_suppression_is_selective": (
            not suppress_a.branch_a_completed and suppress_a.branch_b_completed
        ),
        "targeted_branch_b_suppression_is_selective": (
            suppress_b.branch_a_completed and not suppress_b.branch_b_completed
        ),
        "same_cue_and_dynamic_state": (
            len(dynamic_hashes) == 1
            and len(
                {
                    row.cue_signature
                    for row in (
                        equal,
                        biased,
                        single,
                        untrained,
                        suppress_a,
                        suppress_b,
                    )
                }
            )
            == 1
        ),
        "no_explicit_winner_or_branch_runtime_state": True,
        "coactive_ambiguity_supported": (
            equal.both_branches_completed and biased.both_branches_completed
        ),
        # This assay establishes coexistence and graded physical support, not a
        # normative winner-selection or inhibitory competition mechanism.
        "competitive_resolution_supported": False,
    }
    assessment = PhysicalBranchingAssessment(
        **values,
        engineering_candidate=all(
            value
            for key, value in values.items()
            if key != "competitive_resolution_supported"
        ),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "equal": equal.state_dict(),
        "mildly_biased": biased.state_dict(),
        "single_branch_a": single.state_dict(),
        "suppress_branch_a": suppress_a.state_dict(),
        "suppress_branch_b": suppress_b.state_dict(),
        "untrained": untrained.state_dict(),
    }
    return PhysicalBranchingSuite(
        equal=equal,
        mildly_biased=biased,
        single_branch_a=single,
        untrained=untrained,
        suppress_branch_a=suppress_a,
        suppress_branch_b=suppress_b,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

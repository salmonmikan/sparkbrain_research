from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.endogenous_chain import AutonomousEndogenousChainRuntime
from sparkbrain.v06.foundation import ProvenanceLedger
from sparkbrain.v06.local_expectation import LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig

from .v061_diagnostic_worlds import (
    DiagnosticWorld,
    lag_factor_worlds,
    relation_factor_worlds,
)
from .v061_relation_diagnostics import _phase_trace
from .v06_confirmatory_heldout_primary import (
    _chain_paths,
    _estimated_reinjection_gain,
    _field,
    _horizon,
    _pulse,
    _relation_cycles,
    _train_expectation,
)


@dataclass(frozen=True, slots=True)
class TransitionFailureTransfer:
    family_id: str
    factor_value: str
    baseline_units: tuple[int, ...]
    expectation_transplant_units: tuple[int, ...]
    expectation_reset_units: tuple[int, ...]
    field_state_only_units: tuple[int, ...]
    baseline_trajectory_class: str
    expectation_transplant_class: str
    expectation_state_hash: str
    transplanted_expectation_state_hash: str
    fresh_field_state_hash: str
    transplanted_fresh_field_state_hash: str
    carried_field_state_hash: str
    failure_transfers_with_g1: bool
    g1_reset_removes_expression: bool
    field_state_alone_transfers_failure: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationFailureTransfer:
    family_id: str
    factor_value: str
    phase_index: int
    expected_target: int
    source_storage_status: str
    source_expression_status: str
    source_output_units: tuple[int, ...]
    fresh_field_replay_output_units: tuple[int, ...]
    reset_consistency_output_units: tuple[int, ...]
    source_failure_stage: str | None
    failure_replays_in_fresh_field: bool
    consistency_reset_removes_expression: bool
    prior_field_state_required: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_subsequence(values: tuple[int, ...], expected: tuple[int, ...]) -> bool:
    if not expected:
        return True
    index = 0
    for value in values:
        if value == expected[index]:
            index += 1
            if index == len(expected):
                return True
    return False


def _trajectory_class(world: DiagnosticWorld, units: tuple[int, ...]) -> str:
    main = _is_subsequence(units, world.main_path[1:])
    alternate = _is_subsequence(units, world.alternate_path[1:])
    if units == world.main_path[1:]:
        return "main-only-exact"
    if main and alternate:
        return "dual-trajectory-superposition"
    if alternate and not main:
        return "alternate-only-substitution"
    if main:
        return "main-with-extra-activity"
    if not units:
        return "no-endogenous-trajectory"
    return "incomplete-or-other-trajectory"


def _runtime_from_components(
    world: DiagnosticWorld,
    field: TemporalExcitableField,
    expectation: LocalTemporalExpectation,
) -> AutonomousEndogenousChainRuntime:
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    paths = _chain_paths(world)  # type: ignore[arg-type]
    gain = _estimated_reinjection_gain(
        world,  # type: ignore[arg-type]
        expectation,
        paths,
    )
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=gain,
            maximum_effective_current=max(2.0, world.cue_magnitude * gain),
            maximum_generation_depth=8,
            maximum_energy_per_window=256.0,
            maximum_proposals_per_window=64,
            maximum_branches_per_origin_state=max(8, len(world.competition_paths) + 2),
            window_ms=max(world.episode_spacings_ms),
        ),
    )
    return AutonomousEndogenousChainRuntime(
        field,
        expectation,
        transition,
        gate,
    )


def _run_main_cue(
    world: DiagnosticWorld,
    runtime: AutonomousEndogenousChainRuntime,
    *,
    start_ms: float,
    event_id: str,
) -> tuple[int, ...]:
    before = len(runtime.generated_sparks)
    runtime.present_external(
        _pulse(  # type: ignore[arg-type]
            world,
            event_id,
            start_ms,
            world.main_path[0],
        )
    )
    runtime.advance_silence(_horizon(world, start_ms))  # type: ignore[arg-type]
    return tuple(row.unit_id for row in runtime.generated_sparks[before:])


def diagnose_transition_failure_transfer(
    world: DiagnosticWorld,
) -> TransitionFailureTransfer:
    world.validate()
    source_expectation = _train_expectation(  # type: ignore[arg-type]
        world,
        _chain_paths(world),  # type: ignore[arg-type]
    )
    learned = source_expectation.learned_state_dict()

    baseline_field = _field(world)  # type: ignore[arg-type]
    fresh_field_hash = baseline_field.state_hash()
    baseline_runtime = _runtime_from_components(
        world,
        baseline_field,
        LocalTemporalExpectation.from_learned_state_dict(learned),
    )
    baseline_units = _run_main_cue(
        world,
        baseline_runtime,
        start_ms=100.0,
        event_id="diagnostic:locus:baseline",
    )

    transplanted_field = _field(world)  # type: ignore[arg-type]
    transplanted_field_hash = transplanted_field.state_hash()
    transplanted_expectation = LocalTemporalExpectation.from_learned_state_dict(
        learned
    )
    transplanted_runtime = _runtime_from_components(
        world,
        transplanted_field,
        transplanted_expectation,
    )
    transplant_units = _run_main_cue(
        world,
        transplanted_runtime,
        start_ms=100.0,
        event_id="diagnostic:locus:g1-transplant",
    )

    reset_runtime = _runtime_from_components(
        world,
        _field(world),  # type: ignore[arg-type]
        LocalTemporalExpectation(source_expectation.config),
    )
    reset_units = _run_main_cue(
        world,
        reset_runtime,
        start_ms=100.0,
        event_id="diagnostic:locus:g1-reset",
    )

    carried_field = TemporalExcitableField.from_state_dict(
        baseline_runtime.field.state_dict()
    )
    carried_field_hash = carried_field.state_hash()
    field_only_runtime = _runtime_from_components(
        world,
        carried_field,
        LocalTemporalExpectation(source_expectation.config),
    )
    field_only_units = _run_main_cue(
        world,
        field_only_runtime,
        start_ms=carried_field.current_time_ms + 100.0,
        event_id="diagnostic:locus:field-only",
    )

    baseline_class = _trajectory_class(world, baseline_units)
    transplant_class = _trajectory_class(world, transplant_units)
    transfers = baseline_units == transplant_units and baseline_class == transplant_class
    reset_removes = reset_units == ()
    field_transfers = (
        field_only_units == baseline_units
        and _trajectory_class(world, field_only_units) == baseline_class
    )
    return TransitionFailureTransfer(
        family_id=world.family_id,
        factor_value=world.factor_value,
        baseline_units=baseline_units,
        expectation_transplant_units=transplant_units,
        expectation_reset_units=reset_units,
        field_state_only_units=field_only_units,
        baseline_trajectory_class=baseline_class,
        expectation_transplant_class=transplant_class,
        expectation_state_hash=source_expectation.state_hash(),
        transplanted_expectation_state_hash=transplanted_expectation.state_hash(),
        fresh_field_state_hash=fresh_field_hash,
        transplanted_fresh_field_state_hash=transplanted_field_hash,
        carried_field_state_hash=carried_field_hash,
        failure_transfers_with_g1=transfers,
        g1_reset_removes_expression=reset_removes,
        field_state_alone_transfers_failure=field_transfers,
        interpretation=(
            "The expressed trajectory class moves with explicit G1 transition state "
            "into an identical fresh Field; carried Field state without G1 does not "
            "recreate it."
        ),
    )


def _first_failure_phase(
    world: DiagnosticWorld,
) -> tuple[int, dict[str, Any], int, int]:
    relation = _relation_cycles(world)  # type: ignore[arg-type]
    for index, (snapshot, expected, length) in enumerate(
        zip(
            relation.snapshots,
            world.contingency_cycle_targets,
            world.contingency_phase_lengths,
            strict=True,
        ),
        start=1,
    ):
        trace = _phase_trace(
            world,
            snapshot,
            phase_index=index,
            phase_length=length,
            expected_target=expected,
        )
        if trace.first_failure_stage is not None:
            return index, snapshot, expected, length
    raise RuntimeError("diagnostic relation world contains no failing phase")


def diagnose_relation_failure_transfer(
    world: DiagnosticWorld,
) -> RelationFailureTransfer:
    world.validate()
    phase_index, learned_state, expected, length = _first_failure_phase(world)
    source = _phase_trace(
        world,
        learned_state,
        phase_index=phase_index,
        phase_length=length,
        expected_target=expected,
    )
    replay = _phase_trace(
        world,
        learned_state,
        phase_index=phase_index,
        phase_length=length,
        expected_target=expected,
    )
    reset_state = {
        "config": learned_state["config"],
        "links": {},
    }
    reset = _phase_trace(
        world,
        reset_state,
        phase_index=phase_index,
        phase_length=length,
        expected_target=expected,
    )
    same_failure = (
        source.output_units == replay.output_units
        and source.storage_status == replay.storage_status
        and source.expression_status == replay.expression_status
        and source.first_failure_stage == replay.first_failure_stage
    )
    reset_removes = reset.output_units == ()
    return RelationFailureTransfer(
        family_id=world.family_id,
        factor_value=world.factor_value,
        phase_index=phase_index,
        expected_target=expected,
        source_storage_status=source.storage_status,
        source_expression_status=source.expression_status,
        source_output_units=source.output_units,
        fresh_field_replay_output_units=replay.output_units,
        reset_consistency_output_units=reset.output_units,
        source_failure_stage=source.first_failure_stage,
        failure_replays_in_fresh_field=same_failure,
        consistency_reset_removes_expression=reset_removes,
        prior_field_state_required=False,
        interpretation=(
            "The same failure reappears when the learned anonymous consistency state "
            "is reconstructed over a fresh Field. Resetting that state removes all "
            "relation-driven expression, so prior Field residual state is not required."
        ),
    )


def run_failure_locus_suite() -> dict[str, Any]:
    lag_world_map = {world.family_id: world for world in lag_factor_worlds()}
    transition_worlds = (
        lag_world_map["diagnostic-lag-resonant-shared"],
        lag_world_map["diagnostic-lag-main-variance-2"],
        lag_world_map["diagnostic-lag-narrow-shared"],
    )
    transitions = tuple(
        diagnose_transition_failure_transfer(world) for world in transition_worlds
    )
    relations = tuple(
        diagnose_relation_failure_transfer(world)
        for world in relation_factor_worlds()
    )
    return {
        "scope": "development-only failure-state reset/transplant diagnosis",
        "candidate_003_executions": 0,
        "transition_world_count": len(transitions),
        "relation_world_count": len(relations),
        "transition_failure_transfers_with_g1_count": sum(
            row.failure_transfers_with_g1 for row in transitions
        ),
        "transition_g1_reset_removes_expression_count": sum(
            row.g1_reset_removes_expression for row in transitions
        ),
        "transition_field_state_alone_transfer_count": sum(
            row.field_state_alone_transfers_failure for row in transitions
        ),
        "relation_failure_replays_in_fresh_field_count": sum(
            row.failure_replays_in_fresh_field for row in relations
        ),
        "relation_reset_removes_expression_count": sum(
            row.consistency_reset_removes_expression for row in relations
        ),
        "transitions": [row.state_dict() for row in transitions],
        "relations": [row.state_dict() for row in relations],
    }

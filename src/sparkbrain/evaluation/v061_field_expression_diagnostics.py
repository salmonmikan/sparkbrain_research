from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.endogenous_chain import AutonomousEndogenousChainRuntime
from sparkbrain.v06.foundation import ProvenanceLedger, digest
from sparkbrain.v06.local_expectation import LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.relation_reentry import (
    AnonymousRelationReentry,
    RelationReentryConfig,
)

from .v06_confirmatory_heldout_primary import (
    _chain_paths,
    _estimated_reinjection_gain,
    _horizon,
    _probe_boundary,
    _pulse,
    _relation_cycles,
    _train_expectation,
)
from .v061_diagnostic_worlds import DiagnosticWorld, lag_factor_worlds
from .v061_failure_locus_diagnostics import (
    _trajectory_class,
    run_failure_locus_suite,
)
from .v061_state_factorization_diagnostics import (
    run_state_factorization_diagnosis,
)


@dataclass(frozen=True, slots=True)
class TransitionExpressionCondition:
    condition: str
    field_threshold: float
    expectation_state_hash: str
    proposal_targets: tuple[int, ...]
    proposal_confidences: tuple[tuple[int, float], ...]
    accepted_currents: tuple[tuple[int, float], ...]
    primer_target: int | None
    primer_current: float
    primer_time_ms: float | None
    generated_units: tuple[int, ...]
    trajectory_class: str
    external_primer_spike_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationExpressionCondition:
    condition: str
    field_threshold: float
    consistency_state_hash_before: str
    consistency_state_hash_after: str
    proposal_targets: tuple[int, ...]
    accepted_currents: tuple[tuple[int, float], ...]
    primer_target: int | None
    primer_current: float
    primer_time_ms: float | None
    endogenous_output_units: tuple[int, ...]
    external_primer_spike_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FieldExpressionAssessment:
    proposal_identity_invariant_across_field_conditions: bool
    readout_without_reinjection_has_no_endogenous_spark: bool
    threshold_changes_trajectory_expression: bool
    residual_state_rescues_subthreshold_branch: bool
    refractory_state_suppresses_selected_branch: bool
    relation_state_is_read_only: bool
    relation_threshold_changes_expression: bool
    relation_refractory_state_suppresses_expression: bool
    learned_transition_organization_moves_with_g1: bool
    learned_relation_organization_moves_with_consistency: bool
    field_active_expression_substrate_supported: bool
    field_learned_organizer_supported: bool
    distributed_field_memory_supported: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _world(family_id: str) -> DiagnosticWorld:
    return next(
        world for world in lag_factor_worlds() if world.family_id == family_id
    )


def _field_at_threshold(
    world: DiagnosticWorld,
    threshold: float,
) -> TemporalExcitableField:
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=threshold,
            )
            for unit_id in range(world.unit_count)
        ),
        (),
        receptor_ids=world.active_unit_ids,
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=max(1.0, min(world.evaluation_lags_ms) * 0.25),
        ),
    )


def _unit_id(target: str) -> int:
    if not target.startswith("unit:"):
        raise ValueError("diagnostic target must use unit:<id>")
    return int(target.removeprefix("unit:"))


def _runtime(
    world: DiagnosticWorld,
    *,
    threshold: float,
    expectation_state: dict[str, Any],
    fixed_gain: float,
) -> AutonomousEndogenousChainRuntime:
    field = _field_at_threshold(world, threshold)
    expectation = LocalTemporalExpectation.from_learned_state_dict(
        expectation_state
    )
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=fixed_gain,
            maximum_effective_current=max(
                2.0,
                world.cue_magnitude * fixed_gain,
            ),
            maximum_generation_depth=8,
            maximum_energy_per_window=256.0,
            maximum_proposals_per_window=64,
            maximum_branches_per_origin_state=max(
                8,
                len(world.competition_paths) + 2,
            ),
            window_ms=max(world.episode_spacings_ms),
        ),
    )
    return AutonomousEndogenousChainRuntime(
        field,
        expectation,
        transition,
        reinjection,
    )


def _root_records(runtime: AutonomousEndogenousChainRuntime):
    return tuple(
        row
        for row in runtime.proposal_records
        if row.generation_depth == 1 and row.reinjection is not None
    )


def _schedule_primer(
    runtime: AutonomousEndogenousChainRuntime,
    world: DiagnosticWorld,
    mode: str,
) -> tuple[int | None, float, float | None]:
    if mode == "none":
        return None, 0.0, None
    records = _root_records(runtime)
    if mode == "residual-main":
        target = world.main_path[1]
        record = next(row for row in records if _unit_id(row.target) == target)
        if record.reinjection is None:
            raise RuntimeError("main proposal has no reinjection decision")
        delta = 0.25
        time_ms = record.predicted_arrival_ms - delta
        endogenous_current = abs(record.reinjection.effective_current)
        residual_at_arrival = (
            world.threshold - endogenous_current + world.threshold * 0.05
        )
        primer_current = residual_at_arrival / math.exp(
            -delta / runtime.field.config.membrane_tau_ms
        )
        if not 0.0 < primer_current < world.threshold:
            raise RuntimeError("residual primer must remain subthreshold")
    elif mode == "refractory-alternate":
        target = world.alternate_path[1]
        record = next(row for row in records if _unit_id(row.target) == target)
        delta = min(0.25, runtime.field.config.refractory_ms * 0.25)
        time_ms = record.predicted_arrival_ms - delta
        primer_current = world.threshold * 1.10
    else:
        raise ValueError(f"unsupported primer mode: {mode}")
    runtime.field.schedule_arrival(
        SynapticArrival(
            time_ms=time_ms,
            target_id=target,
            current=primer_current,
            source_id=None,
            pulse_id=f"diagnostic:{mode}:primer",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    return target, primer_current, time_ms


def _transition_condition(
    world: DiagnosticWorld,
    expectation_state: dict[str, Any],
    fixed_gain: float,
    *,
    condition: str,
    threshold: float,
    primer_mode: str = "none",
    reinject: bool = True,
) -> TransitionExpressionCondition:
    runtime = _runtime(
        world,
        threshold=threshold,
        expectation_state=expectation_state,
        fixed_gain=fixed_gain,
    )
    cue = _pulse(  # type: ignore[arg-type]
        world,
        f"diagnostic:field-expression:{condition}:cue",
        100.0,
        world.main_path[0],
    )
    if reinject:
        runtime.present_external(cue)
        records = _root_records(runtime)
        proposal_targets = tuple(_unit_id(row.target) for row in records)
        confidences = tuple(
            sorted(
                (
                    _unit_id(row.target),
                    runtime.ledger.proposals[row.proposal_id].confidence,
                )
                for row in records
            )
        )
        currents = tuple(
            sorted(
                (
                    _unit_id(row.target),
                    abs(row.reinjection.effective_current),
                )
                for row in records
                if row.reinjection is not None and row.reinjection.accepted
            )
        )
    else:
        runtime.ledger.register_external(cue)
        runtime.field.schedule_arrival(
            SynapticArrival(
                time_ms=cue.time_ms,
                target_id=world.main_path[0],
                current=cue.magnitude,
                source_id=None,
                pulse_id=cue.event_id,
                novelty=0.0,
                prediction_error=0.0,
            )
        )
        runtime.field.run_until(cue.time_ms)
        proposals = runtime.expectation.proposals_for(
            cue,
            origin_state_hash=runtime.field.state_hash(),
        )
        proposal_targets = tuple(_unit_id(row.target) for row in proposals)
        confidences = tuple(
            sorted((_unit_id(row.target), row.confidence) for row in proposals)
        )
        currents = ()
    primer_target, primer_current, primer_time = _schedule_primer(
        runtime,
        world,
        primer_mode,
    )
    spikes_before = runtime.field.total_spikes
    runtime.advance_silence(_horizon(world, cue.time_ms))  # type: ignore[arg-type]
    units = tuple(row.unit_id for row in runtime.generated_sparks)
    external_primer_spikes = max(
        0,
        runtime.field.total_spikes - spikes_before - len(units),
    )
    return TransitionExpressionCondition(
        condition=condition,
        field_threshold=threshold,
        expectation_state_hash=digest(expectation_state),
        proposal_targets=proposal_targets,
        proposal_confidences=confidences,
        accepted_currents=currents,
        primer_target=primer_target,
        primer_current=primer_current,
        primer_time_ms=primer_time,
        generated_units=units,
        trajectory_class=_trajectory_class(world, units),
        external_primer_spike_count=external_primer_spikes,
    )


def _single_relation_state(world: DiagnosticWorld) -> dict[str, Any]:
    relation_world = replace(
        world,
        family_id="diagnostic-field-expression-relation-source",
        seed=933_900,
        structural_token=(
            "development-only:diagnostic:field-expression-relation-source:933900"
        ),
        contingency_cycle_targets=(world.old_target,),
        contingency_phase_lengths=(6,),
        factor_name="field-expression-relation-source",
        factor_value="old-target-six-exposures",
    )
    relation_world.validate()
    relation = _relation_cycles(relation_world)  # type: ignore[arg-type]
    if len(relation.snapshots) != 1:
        raise RuntimeError("relation source must contain one phase")
    return relation.snapshots[0]


def _relation_condition(
    world: DiagnosticWorld,
    consistency_state: dict[str, Any],
    *,
    condition: str,
    threshold: float,
    refractory_primer: bool = False,
) -> RelationExpressionCondition:
    field = _field_at_threshold(world, threshold)
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency.from_learned_state_dict(
        consistency_state,
        ledger=ledger,
    )
    before_hash = consistency.state_hash()
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            maximum_effective_current=max(2.0, world.threshold * 4.0),
            maximum_generation_depth=8,
            maximum_energy_per_window=128.0,
            maximum_proposals_per_window=32,
            maximum_branches_per_origin_state=8,
        ),
    )
    reentry = AnonymousRelationReentry(
        consistency,
        ledger,
        gate,
        RelationReentryConfig(
            delay_ms=1.0,
            magnitude_gain=world.relation_reentry_gain,
            maximum_magnitude=max(2.0, world.threshold * 4.0),
            minimum_consistent_count=1,
            minimum_reliability=0.0,
            maximum_links_per_boundary=8,
        ),
    )
    records = reentry.schedule(
        _probe_boundary(  # type: ignore[arg-type]
            world,
            f"diagnostic:field-expression:relation:{condition}",
        ),
        field,
    )
    primer_target = None
    primer_current = 0.0
    primer_time = None
    if refractory_primer:
        accepted = next(
            row
            for row in records
            if row.reinjection.accepted
            and _unit_id(row.target) == world.old_target
        )
        if accepted.reinjection.scheduled_time_ms is None:
            raise RuntimeError("accepted relation proposal lacks scheduled time")
        primer_target = world.old_target
        primer_time = accepted.reinjection.scheduled_time_ms - min(
            0.25,
            field.config.refractory_ms * 0.25,
        )
        primer_current = threshold * 1.10
        field.schedule_arrival(
            SynapticArrival(
                time_ms=primer_time,
                target_id=primer_target,
                current=primer_current,
                source_id=None,
                pulse_id="diagnostic:relation:refractory-primer",
                novelty=0.0,
                prediction_error=0.0,
            )
        )
    spikes = field.run_until(102.0)
    endogenous = tuple(
        spike.unit_id
        for spike in spikes
        if any(source.startswith("endo:") for source in spike.source_pulse_ids)
    )
    return RelationExpressionCondition(
        condition=condition,
        field_threshold=threshold,
        consistency_state_hash_before=before_hash,
        consistency_state_hash_after=consistency.state_hash(),
        proposal_targets=tuple(_unit_id(row.target) for row in records),
        accepted_currents=tuple(
            sorted(
                (
                    _unit_id(row.target),
                    abs(row.reinjection.effective_current),
                )
                for row in records
                if row.reinjection.accepted
            )
        ),
        primer_target=primer_target,
        primer_current=primer_current,
        primer_time_ms=primer_time,
        endogenous_output_units=endogenous,
        external_primer_spike_count=len(spikes) - len(endogenous),
    )


def run_field_expression_diagnosis() -> dict[str, Any]:
    transition_world = _world("diagnostic-lag-resonant-shared")
    paths = _chain_paths(transition_world)  # type: ignore[arg-type]
    expectation = _train_expectation(  # type: ignore[arg-type]
        transition_world,
        paths,
    )
    expectation_state = expectation.learned_state_dict()
    fixed_gain = _estimated_reinjection_gain(  # type: ignore[arg-type]
        transition_world,
        expectation,
        paths,
    )
    transition_conditions = (
        _transition_condition(
            transition_world,
            expectation_state,
            fixed_gain,
            condition="readout-only",
            threshold=transition_world.threshold,
            reinject=False,
        ),
        _transition_condition(
            transition_world,
            expectation_state,
            fixed_gain,
            condition="low-threshold",
            threshold=transition_world.threshold * 0.50,
        ),
        _transition_condition(
            transition_world,
            expectation_state,
            fixed_gain,
            condition="ordinary-field",
            threshold=transition_world.threshold,
        ),
        _transition_condition(
            transition_world,
            expectation_state,
            fixed_gain,
            condition="high-threshold",
            threshold=transition_world.threshold * 1.20,
        ),
        _transition_condition(
            transition_world,
            expectation_state,
            fixed_gain,
            condition="residual-main-primer",
            threshold=transition_world.threshold,
            primer_mode="residual-main",
        ),
        _transition_condition(
            transition_world,
            expectation_state,
            fixed_gain,
            condition="refractory-alternate-primer",
            threshold=transition_world.threshold,
            primer_mode="refractory-alternate",
        ),
    )
    transition_by_name = {
        row.condition: row for row in transition_conditions
    }

    relation_world = _world("diagnostic-lag-narrow-shared")
    consistency_state = _single_relation_state(relation_world)
    relation_conditions = (
        _relation_condition(
            relation_world,
            consistency_state,
            condition="ordinary-field",
            threshold=relation_world.threshold,
        ),
        _relation_condition(
            relation_world,
            consistency_state,
            condition="high-threshold",
            threshold=relation_world.threshold * 1.60,
        ),
        _relation_condition(
            relation_world,
            consistency_state,
            condition="refractory-target-primer",
            threshold=relation_world.threshold,
            refractory_primer=True,
        ),
    )
    relation_by_name = {row.condition: row for row in relation_conditions}

    proposal_signatures = {
        (row.proposal_targets, row.proposal_confidences)
        for row in transition_conditions
    }
    threshold_classes = {
        transition_by_name["low-threshold"].trajectory_class,
        transition_by_name["ordinary-field"].trajectory_class,
        transition_by_name["high-threshold"].trajectory_class,
    }
    locus = run_failure_locus_suite()
    factorization = run_state_factorization_diagnosis()["assessment"]
    transition_moves_with_g1 = (
        locus["transition_failure_transfers_with_g1_count"]
        == locus["transition_world_count"]
        and locus["transition_field_state_alone_transfer_count"] == 0
    )
    relation_moves_with_consistency = (
        locus["relation_failure_replays_in_fresh_field_count"]
        == locus["relation_world_count"]
        and locus["relation_reset_removes_expression_count"]
        == locus["relation_world_count"]
    )
    active_expression = all(
        (
            len(proposal_signatures) == 1,
            transition_by_name["readout-only"].generated_units == (),
            len(threshold_classes) == 3,
            transition_world.main_path[1]
            in transition_by_name["residual-main-primer"].generated_units,
            transition_world.alternate_path[1]
            not in transition_by_name[
                "refractory-alternate-primer"
            ].generated_units,
            relation_by_name["ordinary-field"].endogenous_output_units
            == (relation_world.old_target,),
            relation_by_name["high-threshold"].endogenous_output_units == (),
            relation_by_name[
                "refractory-target-primer"
            ].endogenous_output_units
            == (),
        )
    )
    assessment = FieldExpressionAssessment(
        proposal_identity_invariant_across_field_conditions=(
            len(proposal_signatures) == 1
        ),
        readout_without_reinjection_has_no_endogenous_spark=(
            transition_by_name["readout-only"].generated_units == ()
        ),
        threshold_changes_trajectory_expression=len(threshold_classes) == 3,
        residual_state_rescues_subthreshold_branch=(
            transition_world.main_path[1]
            in transition_by_name["residual-main-primer"].generated_units
        ),
        refractory_state_suppresses_selected_branch=(
            transition_world.alternate_path[1]
            not in transition_by_name[
                "refractory-alternate-primer"
            ].generated_units
        ),
        relation_state_is_read_only=all(
            row.consistency_state_hash_before
            == row.consistency_state_hash_after
            for row in relation_conditions
        ),
        relation_threshold_changes_expression=(
            relation_by_name["ordinary-field"].endogenous_output_units
            != relation_by_name["high-threshold"].endogenous_output_units
        ),
        relation_refractory_state_suppresses_expression=(
            relation_by_name[
                "refractory-target-primer"
            ].endogenous_output_units
            == ()
        ),
        learned_transition_organization_moves_with_g1=transition_moves_with_g1,
        learned_relation_organization_moves_with_consistency=(
            relation_moves_with_consistency
        ),
        field_active_expression_substrate_supported=active_expression,
        field_learned_organizer_supported=not (
            transition_moves_with_g1
            and relation_moves_with_consistency
            and factorization["full_cartesian_factorization"]
        ),
        distributed_field_memory_supported=(
            locus["transition_field_state_alone_transfer_count"] > 0
        ),
        interpretation=(
            "Fixed anonymous G1 state emits the same proposal identities and "
            "confidences, while Field threshold, residual potential, and refractory "
            "state transform them into no trajectory, one trajectory, or concurrent "
            "trajectories. Fixed anonymous consistency state is likewise expressed "
            "or suppressed by Field state. Field Dynamics are therefore an active "
            "expression substrate rather than a passive readout. D5-D7 nevertheless "
            "show that learned trajectory organization moves with explicit G1 state "
            "and learned relation organization moves with explicit consistency state; "
            "Field state alone does not carry either learned organization."
        ),
    )
    return {
        "scope": "development-only Field necessity and expression diagnosis",
        "candidate_003_executions": 0,
        "transition_world": transition_world.state_dict(),
        "fixed_expectation_state_hash": digest(expectation_state),
        "fixed_reinjection_gain": fixed_gain,
        "transition_conditions": [
            row.state_dict() for row in transition_conditions
        ],
        "relation_world": relation_world.state_dict(),
        "fixed_consistency_state_hash": digest(consistency_state),
        "relation_conditions": [
            row.state_dict() for row in relation_conditions
        ],
        "assessment": assessment.state_dict(),
    }

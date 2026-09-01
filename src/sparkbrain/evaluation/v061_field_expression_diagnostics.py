from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
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
    _field,
    _horizon,
    _probe_boundary,
    _pulse,
    _relation_cycles,
    _train_expectation,
)
from .v061_diagnostic_worlds import DiagnosticWorld, lag_factor_worlds
from .v061_failure_locus_diagnostics import _trajectory_class
from .v061_state_factorization_diagnostics import (
    run_state_factorization_diagnosis,
)


@dataclass(frozen=True, slots=True)
class TransitionFieldCondition:
    condition: str
    field_threshold: float
    expectation_state_hash: str
    root_proposal_targets: tuple[int, ...]
    root_proposal_confidences: tuple[tuple[int, float], ...]
    accepted_root_currents: tuple[tuple[int, float], ...]
    primer_target: int | None
    primer_current: float
    primer_time_ms: float | None
    generated_units: tuple[int, ...]
    trajectory_class: str
    external_primer_spike_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationFieldCondition:
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
    transition_proposals_invariant_across_field_conditions: bool
    readout_without_reinjection_has_no_endogenous_spark: bool
    threshold_changes_trajectory_expression: bool
    residual_state_rescues_subthreshold_branch: bool
    refractory_state_suppresses_selected_branch: bool
    relation_state_read_only_across_field_conditions: bool
    relation_threshold_changes_expression: bool
    relation_refractory_state_suppresses_expression: bool
    learned_transition_organization_moves_without_field_state: bool
    learned_relation_organization_moves_without_field_state: bool
    field_active_expression_substrate_supported: bool
    field_learned_organizer_supported: bool
    distributed_field_memory_supported: bool
    interpretation: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _diagnostic_world() -> DiagnosticWorld:
    return next(
        world
        for world in lag_factor_worlds()
        if world.family_id == "diagnostic-lag-resonant-shared"
    )


def _field_world(world: DiagnosticWorld, threshold: float) -> DiagnosticWorld:
    result = replace(
        world,
        family_id=f"diagnostic-field-expression-{threshold:.6f}",
        seed=933_000 + int(round(threshold * 1000.0)),
        structural_token=(
            "development-only:diagnostic:field-expression:"
            f"{threshold:.6f}"
        ),
        threshold=threshold,
        factor_name="field-expression-threshold",
        factor_value=f"{threshold:.6f}",
    )
    result.validate()
    return result


def _runtime_with_fixed_gain(
    world: DiagnosticWorld,
    *,
    field_threshold: float,
    expectation_state: dict[str, Any],
    gain: float,
) -> AutonomousEndogenousChainRuntime:
    field_world = _field_world(world, field_threshold)
    field = _field(field_world)  # type: ignore[arg-type]
    expectation = LocalTemporalExpectation.from_learned_state_dict(
        expectation_state
    )
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=gain,
            maximum_effective_current=max(2.0, world.cue_magnitude * gain),
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
        gate,
    )


def _unit_id(target: str) -> int:
    prefix = "unit:"
    if not target.startswith(prefix):
        raise ValueError("diagnostic target must use unit:<id>")
    return int(target[len(prefix) :])


def _root_records(runtime: AutonomousEndogenousChainRuntime):
    return tuple(
        row
        for row in runtime.proposal_records
        if row.generation_depth == 1 and row.reinjection is not None
    )


def _schedule_transition_primer(
    runtime: AutonomousEndogenousChainRuntime,
    world: DiagnosticWorld,
    *,
    mode: str,
) -> tuple[int | None, float, float | None]:
    records = _root_records(runtime)
    if mode == "none":
        return None, 0.0, None
    if mode == "residual-main":
        target = world.main_path[1]
        record = next(row for row in records if _unit_id(row.target) == target)
        if record.reinjection is None:
            raise RuntimeError("main proposal has no reinjection decision")
        delta = 0.25
        time_ms = record.predicted_arrival_ms - delta
        current = abs(record.reinjection.effective_current)
        residual_needed = world.threshold - current + world.threshold * 0.05
        primer_current = residual_needed / math.exp(
            -delta / runtime.field.config.membrane_tau_ms
        )
        if not 0.0 < primer_current < world.threshold:
            raise RuntimeError("residual primer must remain subthreshold")
        target_id = target
    elif mode == "refractory-alternate":
        target = world.alternate_path[1]
        record = next(row for row in records if _unit_id(row.target) == target)
        delta = min(0.25, runtime.field.config.refractory_ms * 0.25)
        time_ms = record.predicted_arrival_ms - delta
        primer_current = world.threshold * 1.10
        target_id = target
    else:
        raise ValueError(f"unsupported transition primer mode: {mode}")
    runtime.field.schedule_arrival(
        SynapticArrival(
            time_ms=time_ms,
            target_id=target_id,
            current=primer_current,
            source_id=None,
            pulse_id=f"diagnostic:{mode}:primer",
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    return target_id, primer_current, time_ms


def _transition_condition(
    world: DiagnosticWorld,
    expectation_state: dict[str, Any],
    gain: float,
    *,
    condition: str,
    field_threshold: float,
    primer_mode: str = "none",
    reinject: bool = True,
) -> TransitionFieldCondition:
    runtime = _runtime_with_fixed_gain(
        world,
        field_threshold=field_threshold,
        expectation_state=expectation_state,
        gain=gain,
    )
    cue = _pulse(  # type: ignore[arg-type]
        world,
        f"diagnostic:field-expression:{condition}:cue",
        100.0,
        world.main_path[0],
    )
    if reinject:
        runtime.present_external(cue)
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
        runtime.expectation.proposals_for(
            cue,
            origin_state_hash=runtime.field.state_hash(),
        )
    records = _root_records(runtime)
    primer_target, primer_current, primer_time = _schedule_transition_primer(
        runtime,
        world,
        mode=primer_mode,
    )
    external_before = runtime.field.total_spikes
    runtime.advance_silence(_horizon(world, cue.time_ms))  # type: ignore[arg-type]
    external_primer_spikes = max(
        0,
        runtime.field.total_spikes
        - external_before
        - len(runtime.generated_sparks),
    )
    units = tuple(row.unit_id for row in runtime.generated_sparks)
    if reinject:
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
        source = _pulse(  # type: ignore[arg-type]
            world,
            f"diagnostic:field-expression:{condition}:readout",
            100.0,
            world.main_path[0],
        )
        proposals = runtime.expectation.proposals_for(
            source,
            origin_state_hash=runtime.field.state_hash(),
        )
        proposal_targets = tuple(_unit_id(row.target) for row in proposals)
        confidences = tuple(
            sorted((_unit_id(row.target), row.confidence) for row in proposals)
        )
        currents = ()
    return TransitionFieldCondition(
        condition=condition,
        field_threshold=field_threshold,
        expectation_state_hash=digest(expectation_state),
        root_proposal_targets=proposal_targets,
        root_proposal_confidences=confidences,
        accepted_root_currents=currents,
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
        family_id="diagnostic-field-expression-relation",
        seed=933_900,
        structural_token=(
            "development-only:diagnostic:field-expression-relation:933900"
        ),
        contingency_cycle_targets=(world.old_target,),
        contingency_phase_lengths=(6,),
        factor_name="field-expression-relation",
        factor_value="old-target-six-exposures",
    )
    relation_world.validate()
    result = _relation_cycles(relation_world)  # type: ignore[arg-type]
    if len(result.snapshots) != 1:
        raise RuntimeError("relation expression diagnostic requires one snapshot")
    return result.snapshots[0]


def _relation_condition(
    world: DiagnosticWorld,
    consistency_state: dict[str, Any],
    *,
    condition: str,
    field_threshold: float,
    refractory_primer: bool = False,
) -> RelationFieldCondition:
    field_world = _field_world(world, field_threshold)
    field = _field(field_world)  # type: ignore[arg-type]
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
        primer_target = world.old_target
        primer_time = accepted.reinjection.scheduled_time_ms - min(
            0.25,
            field.config.refractory_ms * 0.25,
        )
        primer_current = field_threshold * 1.10
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
    endogenous_units = tuple(
        spike.unit_id
        for spike in spikes
        if any(source.startswith("endo:") for source in spike.source_pulse_ids)
    )
    external_spikes = len(spikes) - len(endogenous_units)
    currents = tuple(
        sorted(
            (
                _unit_id(row.target),
                abs(row.reinjection.effective_current),
            )
            for row in records
            if row.reinjection.accepted
        )
    )
    return RelationFieldCondition(
        condition=condition,
        field_threshold=field_threshold,
        consistency_state_hash_before=before_hash,
        consistency_state_hash_after=consistency.state_hash(),
        proposal_targets=tuple(_unit_id(row.target) for row in records),
        accepted_currents=currents,
        primer_target=primer_target,
        primer_current=primer_current,
        primer_time_ms=primer_time,
        endogenous_output_units=endogenous_units,
        external_primer_spike_count=external_spikes,
    )


def run_field_expression_diagnosis() -> dict[str, Any]:
    world = _diagnostic_world()
    paths = _chain_paths(world)  # type: ignore[arg-type]
    expectation = _train_expectation(world, paths)  # type: ignore[arg-type]
    expectation_state = expectation.learned_state_dict()
    gain = _estimated_reinjection_gain(  # type: ignore[arg-type]
        world,
        expectation,
        paths,
    )
    transition_conditions = tuple(
        (
            _transition_condition(
                world,
                expectation_state,
                gain,
                condition="readout-only",
                field_threshold=world.threshold,
                reinject=False,
            ),
            _transition_condition(
                world,
                expectation_state,
                gain,
                condition="low-threshold",
                field_threshold=world.threshold * 0.50,
            ),
            _transition_condition(
                world,
                expectation_state,
                gain,
                condition="ordinary-field",
                field_threshold=world.threshold,
            ),
            _transition_condition(
                world,
                expectation_state,
                gain,
                condition="high-threshold",
                field_threshold=world.threshold * 1.20,
            ),
            _transition_condition(
                world,
                expectation_state,
                gain,
                condition="residual-main-primer",
                field_threshold=world.threshold,
                primer_mode="residual-main",
            ),
            _transition_condition(
                world,
                expectation_state,
                gain,
                condition="refractory-alternate-primer",
                field_threshold=world.threshold,
                primer_mode="refractory-alternate",
            ),
        )
    )[0]
    transition_by_name = {row.condition: row for row in transition_conditions}

    consistency_state = _single_relation_state(world)
    relation_conditions = (
        _relation_condition(
            world,
            consistency_state,
            condition="ordinary-field",
            field_threshold=world.threshold,
        ),
        _relation_condition(
            world,
            consistency_state,
            condition="high-threshold",
            field_threshold=world.threshold * 1.60,
        ),
        _relation_condition(
            world,
            consistency_state,
            condition="refractory-target-primer",
            field_threshold=world.threshold,
            refractory_primer=True,
        ),
    )
    relation_by_name = {row.condition: row for row in relation_conditions}

    proposal_signatures = {
        (
            row.root_proposal_targets,
            row.root_proposal_confidences,
        )
        for row in transition_conditions
        if row.condition != "readout-only"
    }
    locus = run_state_factorization_diagnosis()
    factorization = locus["assessment"]
    threshold_classes = {
        transition_by_name["low-threshold"].trajectory_class,
        transition_by_name["ordinary-field"].trajectory_class,
        transition_by_name["high-threshold"].trajectory_class,
    }
    learned_transition_outside_field = (
        factorization["transition_changes_trajectory"]
        and factorization["trajectory_invariant_under_consistency_swap"]
    )
    learned_relation_outside_field = (
        factorization["consistency_changes_relation_expression"]
        and factorization["relation_expression_invariant_under_transition_swap"]
    )
    active_expression = all(
        (
            len(proposal_signatures) == 1,
            transition_by_name["readout-only"].generated_units == (),
            len(threshold_classes) >= 3,
            world.main_path[1]
            in transition_by_name["residual-main-primer"].generated_units,
            world.alternate_path[1]
            not in transition_by_name[
                "refractory-alternate-primer"
            ].generated_units,
            relation_by_name["ordinary-field"].endogenous_output_units
            == (world.old_target,),
            relation_by_name["high-threshold"].endogenous_output_units == (),
            relation_by_name[
                "refractory-target-primer"
            ].endogenous_output_units
            == (),
        )
    )
    assessment = FieldExpressionAssessment(
        transition_proposals_invariant_across_field_conditions=(
            len(proposal_signatures) == 1
        ),
        readout_without_reinjection_has_no_endogenous_spark=(
            transition_by_name["readout-only"].generated_units == ()
        ),
        threshold_changes_trajectory_expression=len(threshold_classes) >= 3,
        residual_state_rescues_subthreshold_branch=(
            world.main_path[1]
            in transition_by_name["residual-main-primer"].generated_units
        ),
        refractory_state_suppresses_selected_branch=(
            world.alternate_path[1]
            not in transition_by_name[
                "refractory-alternate-primer"
            ].generated_units
        ),
        relation_state_read_only_across_field_conditions=all(
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
        learned_transition_organization_moves_without_field_state=(
            learned_transition_outside_field
        ),
        learned_relation_organization_moves_without_field_state=(
            learned_relation_outside_field
        ),
        field_active_expression_substrate_supported=active_expression,
        field_learned_organizer_supported=False,
        distributed_field_memory_supported=False,
        interpretation=(
            "The same explicit anonymous G1 state emits the same proposal identity and "
            "confidence structure, while Field threshold, residual potential, and "
            "refractory state transform those proposals into no trajectory, one "
            "trajectory, or concurrent trajectories. The same anonymous consistency "
            "state likewise yields or suppresses a relation-driven Spark depending on "
            "Field state. Field Dynamics are therefore an active expression substrate, "
            "not a passive UI. However, D5-D7 show that the learned trajectory and "
            "relation organization move with explicit G1 and consistency state rather "
            "than with Field state, so learned organization and distributed Field "
            "memory remain unsupported."
        ),
    )
    return {
        "scope": "development-only Field necessity and expression diagnosis",
        "candidate_003_executions": 0,
        "world": world.state_dict(),
        "fixed_expectation_state_hash": digest(expectation_state),
        "fixed_reinjection_gain": gain,
        "transition_conditions": [
            row.state_dict() for row in transition_conditions
        ],
        "fixed_consistency_state_hash": digest(consistency_state),
        "relation_conditions": [row.state_dict() for row in relation_conditions],
        "assessment": assessment.state_dict(),
    }

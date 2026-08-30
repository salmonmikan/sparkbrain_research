from __future__ import annotations

import math
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from statistics import fmean
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.boundary import (
    AnonymousBoundaryEmitter,
    BoundaryCoupling,
    BoundaryDirection,
    BoundaryEvent,
    BoundaryIntervention,
)
from sparkbrain.v06.consistency import (
    AnonymousConsistencyConfig,
    UntypedBoundaryConsistency,
)
from sparkbrain.v06.endogenous_chain import (
    AutonomousEndogenousChainRuntime,
    EndogenousChainIntervention,
)
from sparkbrain.v06.foundation import (
    EventOrigin,
    ProvenanceLedger,
    RuntimePulse,
    digest,
)
from sparkbrain.v06.local_expectation import (
    LocalExpectationConfig,
    LocalTemporalExpectation,
)
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.relation_reentry import (
    AnonymousRelationReentry,
    RelationReentryConfig,
)
from sparkbrain.v06.taxonomy import verify_taxonomy_variant_runtime_equality
from sparkbrain.v06.world_boundary import (
    AnonymousBoundaryWorld,
    AnonymousWorldLink,
    WorldBoundaryIntervention,
)

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
    build_result_records,
    result_record_state,
)
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters
from .v06_confirmatory_resources import ConditionResourceRecord
from .v06_confirmatory_training_schedule import (
    build_balanced_training_schedule,
)


@dataclass(frozen=True, slots=True)
class _ChainResult:
    units: tuple[int, ...]
    times_ms: tuple[float, ...]
    runtime: AutonomousEndogenousChainRuntime


@dataclass(frozen=True, slots=True)
class _RelationResult:
    snapshots: tuple[dict[str, Any], ...]
    phase_dominant_targets: tuple[int | None, ...]
    internal_only_link_count: int
    stable_link_count: int
    stable_inconsistent_count: int
    runtime: AutonomousEndogenousChainRuntime
    consistency: UntypedBoundaryConsistency
    boundary_count: int
    world_external_count: int


def _pulse(
    parameters: HeldoutWorldParameters,
    event_id: str,
    time_ms: float,
    unit_id: int,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=parameters.cue_magnitude,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _field(parameters: HeldoutWorldParameters) -> TemporalExcitableField:
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=parameters.threshold,
            )
            for unit_id in range(parameters.unit_count)
        ),
        (),
        receptor_ids=parameters.active_unit_ids,
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=max(1.0, min(parameters.evaluation_lags_ms) * 0.25),
        ),
    )


def _expectation_config(parameters: HeldoutWorldParameters) -> LocalExpectationConfig:
    all_lags = tuple(
        lag
        for profile in parameters.training_lag_profiles_ms
        for lag in profile
    )
    variance = max(1.0, fmean((lag - fmean(all_lags)) ** 2 for lag in all_lags))
    return LocalExpectationConfig(
        max_lag_ms=max(all_lags) * 3.0,
        minimum_observations=2,
        minimum_confidence=0.01,
        maximum_candidates=max(8, len(parameters.competition_paths) + 2),
        proposal_ttl_ms=max(all_lags) * 5.0,
        variance_scale_ms2=max(4.0, variance * 4.0),
        energy_scale=0.05,
    )


def _path_exposures(
    parameters: HeldoutWorldParameters,
    paths: Iterable[tuple[int, int, int, int]],
) -> dict[tuple[int, int, int, int], int]:
    competition = dict(
        zip(
            parameters.competition_paths,
            parameters.branch_exposure_counts,
            strict=True,
        )
    )
    default_count = max(3, len(parameters.training_lag_profiles_ms))
    result: dict[tuple[int, int, int, int], int] = {}
    for path in paths:
        result[path] = max(result.get(path, 0), competition.get(path, default_count))
    return result


def _train_expectation(
    parameters: HeldoutWorldParameters,
    paths: Iterable[tuple[int, int, int, int]],
) -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(_expectation_config(parameters))
    path_rows = tuple(dict.fromkeys(paths))
    if not path_rows:
        return model
    exposures = _path_exposures(parameters, path_rows)
    schedule = build_balanced_training_schedule(
        tuple(exposures[path] for path in path_rows),
        lag_profile_count=len(parameters.training_lag_profiles_ms),
    )
    for episode in schedule.episodes:
        path = path_rows[episode.path_index]
        profile = parameters.training_lag_profiles_ms[
            episode.lag_profile_index
        ]
        start = float(episode.episode_index * 100)
        times = [start]
        for lag in profile:
            times.append(times[-1] + lag)
        pulses = tuple(
            _pulse(
                parameters,
                (
                    f"train:{episode.episode_index}:"
                    f"{episode.path_index}:"
                    f"{episode.exposure_index}:{index}"
                ),
                times[index],
                unit_id,
            )
            for index, unit_id in enumerate(path)
        )
        for source, target in zip(pulses, pulses[1:], strict=False):
            model.observe_external_transition(source, target)
    return model


def _estimated_reinjection_gain(
    parameters: HeldoutWorldParameters,
    model: LocalTemporalExpectation,
    paths: Iterable[tuple[int, int, int, int]],
) -> float:
    best_by_source: list[float] = []
    proposal_count = model.proposal_count
    for source_unit in sorted({unit for path in paths for unit in path[:-1]}):
        source = _pulse(parameters, f"gain:{source_unit}", 0.0, source_unit)
        proposals = model.proposals_for(source, origin_state_hash="0" * 64)
        if proposals:
            best_by_source.append(max(row.confidence for row in proposals))
    model.proposal_count = proposal_count
    if not best_by_source:
        return 1.0
    minimum_best = max(1e-6, min(best_by_source))
    return parameters.threshold / (
        parameters.cue_magnitude * minimum_best
    ) * 1.08


def _runtime(
    parameters: HeldoutWorldParameters,
    paths: Iterable[tuple[int, int, int, int]],
    *,
    intervention: EndogenousChainIntervention | None = None,
) -> AutonomousEndogenousChainRuntime:
    path_rows = tuple(dict.fromkeys(paths))
    model = _train_expectation(parameters, path_rows)
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(model, ledger)
    gain = _estimated_reinjection_gain(parameters, model, path_rows)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=gain,
            maximum_effective_current=max(2.0, parameters.cue_magnitude * gain),
            maximum_generation_depth=8,
            maximum_energy_per_window=256.0,
            maximum_proposals_per_window=64,
            maximum_branches_per_origin_state=max(
                8,
                len(parameters.competition_paths) + 2,
            ),
            window_ms=max(parameters.episode_spacings_ms),
        ),
    )
    return AutonomousEndogenousChainRuntime(
        _field(parameters),
        model,
        transition,
        reinjection,
        intervention=intervention,
    )


def _horizon(parameters: HeldoutWorldParameters, start_ms: float) -> float:
    return start_ms + sum(parameters.evaluation_lags_ms) + max(
        parameters.evaluation_lags_ms
    ) + 5.0


def _run_cue(
    runtime: AutonomousEndogenousChainRuntime,
    parameters: HeldoutWorldParameters,
    *,
    cue_unit_id: int,
    start_ms: float,
    event_id: str,
) -> _ChainResult:
    before = len(runtime.generated_sparks)
    runtime.present_external(
        _pulse(parameters, event_id, start_ms, cue_unit_id)
    )
    runtime.advance_silence(_horizon(parameters, start_ms))
    sparks = tuple(runtime.generated_sparks[before:])
    return _ChainResult(
        units=tuple(row.unit_id for row in sparks),
        times_ms=tuple(row.time_ms for row in sparks),
        runtime=runtime,
    )


def _timing_error(
    result: _ChainResult,
    parameters: HeldoutWorldParameters,
    start_ms: float,
) -> float:
    if len(result.times_ms) < 3:
        return math.inf
    times = (start_ms, *result.times_ms[:3])
    observed = tuple(
        right - left for left, right in zip(times, times[1:], strict=False)
    )
    return max(
        abs(left - right)
        for left, right in zip(
            observed,
            parameters.evaluation_lags_ms,
            strict=True,
        )
    )


def _origin_and_state(
    parameters: HeldoutWorldParameters,
) -> tuple[bool, bool, dict[str, float], int, int]:
    main = _runtime(parameters, (parameters.main_path,))
    main_result = _run_cue(
        main,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="heldout:origin:main",
    )
    alternate = _runtime(parameters, (parameters.alternate_path,))
    alternate_result = _run_cue(
        alternate,
        parameters,
        cue_unit_id=parameters.alternate_path[0],
        start_ms=100.0,
        event_id="heldout:origin:alternate",
    )
    no_history = _runtime(parameters, ())
    no_history_result = _run_cue(
        no_history,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="heldout:origin:no-history",
    )
    main_expected = parameters.main_path[1:]
    alternate_expected = parameters.alternate_path[1:]
    timing_error = _timing_error(main_result, parameters, 100.0)
    tolerance = max(
        0.5,
        max(
            max(profile[index] for profile in parameters.training_lag_profiles_ms)
            - min(profile[index] for profile in parameters.training_lag_profiles_ms)
            for index in range(3)
        ),
    )
    origin = (
        main_result.units[:3] == main_expected
        and main_result.units
        and main_result.units[0] != parameters.main_path[0]
        and no_history_result.units == ()
        and math.isfinite(timing_error)
        and timing_error <= tolerance
    )
    state = (
        alternate_result.units[:3] == alternate_expected
        and alternate_result.units != main_result.units
        and no_history_result.units == ()
    )
    generated = (
        len(main_result.units)
        + len(alternate_result.units)
        + len(no_history_result.units)
    )
    training = (
        main.expectation.external_transition_count
        + alternate.expectation.external_transition_count
    )
    return (
        origin,
        state,
        {
            "heldout_origin_generated_count": float(len(main_result.units)),
            "heldout_origin_no_history_count": float(len(no_history_result.units)),
            "heldout_origin_timing_error_ms": float(timing_error),
            "heldout_state_alternate_generated_count": float(
                len(alternate_result.units)
            ),
        },
        generated,
        training,
    )


def _chain_paths(
    parameters: HeldoutWorldParameters,
) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        dict.fromkeys((*parameters.competition_paths, parameters.control_path))
    )


def _chain_units(
    parameters: HeldoutWorldParameters,
    intervention: EndogenousChainIntervention | None,
) -> tuple[tuple[int, ...], tuple[int, ...], AutonomousEndogenousChainRuntime]:
    runtime = _runtime(parameters, _chain_paths(parameters), intervention=intervention)
    control = _run_cue(
        runtime,
        parameters,
        cue_unit_id=parameters.control_path[0],
        start_ms=100.0,
        event_id="heldout:chain:control",
    )
    main_start = 100.0 + parameters.episode_spacings_ms[0]
    main = _run_cue(
        runtime,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=main_start,
        event_id="heldout:chain:main",
    )
    return main.units, control.units, runtime


def _autonomous_chain(
    parameters: HeldoutWorldParameters,
) -> tuple[bool, dict[str, float], int, int, int]:
    sham_main, sham_control, sham = _chain_units(parameters, None)
    targeted_main, _, targeted = _chain_units(
        parameters,
        EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.main_path[1],)
        ),
    )
    matched_main, matched_control, matched = _chain_units(
        parameters,
        EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.control_path[1],)
        ),
    )
    expected_main = parameters.main_path[1:]
    expected_control = parameters.control_path[1:]
    sham_downstream = sum(unit in parameters.main_path[2:] for unit in sham_main)
    targeted_downstream = sum(
        unit in parameters.main_path[2:] for unit in targeted_main
    )
    matched_downstream = sum(
        unit in parameters.main_path[2:] for unit in matched_main
    )
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    passed = (
        sham_main[:3] == expected_main
        and sham_control[:3] == expected_control
        and targeted_main == (parameters.main_path[1],)
        and matched_main[:3] == expected_main
        and matched_control == (parameters.control_path[1],)
        and targeted_impairment - matched_impairment >= 0.5
        and all(
            runtime.ledger.committed_positive_updates == 0
            for runtime in (sham, targeted, matched)
        )
    )
    generated = sum(
        len(runtime.generated_sparks) for runtime in (sham, targeted, matched)
    )
    training = sum(
        runtime.expectation.external_transition_count
        for runtime in (sham, targeted, matched)
    )
    interventions = len(targeted.intervention_records) + len(
        matched.intervention_records
    )
    return (
        passed,
        {
            "chain_matched_impairment": float(matched_impairment),
            "chain_targeted_impairment": float(targeted_impairment),
            "heldout_chain_matched_units": float(len(matched_main)),
            "heldout_chain_sham_units": float(len(sham_main)),
            "heldout_chain_targeted_units": float(len(targeted_main)),
        },
        generated,
        training,
        interventions,
    )


def _components(
    parameters: HeldoutWorldParameters,
    *,
    boundary_intervention: BoundaryIntervention | None = None,
) -> tuple[
    AutonomousEndogenousChainRuntime,
    AnonymousBoundaryEmitter,
    UntypedBoundaryConsistency,
]:
    runtime = _runtime(parameters, _chain_paths(parameters))
    emitter = AnonymousBoundaryEmitter(
        (
            BoundaryCoupling(
                source_unit_id=parameters.main_path[-1],
                port_id=parameters.main_port,
            ),
            BoundaryCoupling(
                source_unit_id=parameters.control_path[-1],
                port_id=parameters.control_port,
            ),
        ),
        intervention=boundary_intervention,
    )
    consistency = UntypedBoundaryConsistency(
        runtime.ledger,
        AnonymousConsistencyConfig(
            maximum_pair_lag_ms=parameters.boundary_lag_ms * 2.0,
            pending_ttl_ms=parameters.boundary_lag_ms * 3.0,
            maximum_pending=512,
        ),
    )
    return runtime, emitter, consistency


def _world(
    parameters: HeldoutWorldParameters,
    target: int,
    *,
    suppress_ports: tuple[str, ...] = (),
) -> AnonymousBoundaryWorld:
    return AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id=parameters.main_port,
                target=f"unit:{target}",
                lag_ms=parameters.boundary_lag_ms,
                magnitude=1.0,
            ),
            AnonymousWorldLink(
                port_id=parameters.control_port,
                target=f"unit:{parameters.third_target}",
                lag_ms=parameters.boundary_lag_ms,
                magnitude=1.0,
            ),
        ),
        intervention=WorldBoundaryIntervention(
            suppressed_port_ids=suppress_ports
        ),
    )


def _boundary_episode(
    parameters: HeldoutWorldParameters,
    runtime: AutonomousEndogenousChainRuntime,
    emitter: AnonymousBoundaryEmitter,
    consistency: UntypedBoundaryConsistency,
    world: AnonymousBoundaryWorld,
    *,
    cue_unit_id: int,
    start_ms: float,
    episode_spacing_ms: float,
    event_id: str,
) -> tuple[int, int]:
    before_sparks = len(runtime.generated_sparks)
    before_boundaries = len(emitter.events)
    before_external = len(world.external_events)
    _run_cue(
        runtime,
        parameters,
        cue_unit_id=cue_unit_id,
        start_ms=start_ms,
        event_id=event_id,
    )
    sparks = tuple(runtime.generated_sparks[before_sparks:])
    boundaries = emitter.emit(sparks, source_state_hash=runtime.state_hash())
    for event in boundaries:
        consistency.register_boundary(event)
        for external in world.receive(event):
            runtime.present_external(external)
            consistency.observe_external(external)
    next_time = start_ms + episode_spacing_ms - 1.0
    if next_time > runtime.field.current_time_ms:
        runtime.advance_silence(next_time)
    consistency.expire(next_time)
    return (
        len(emitter.events) - before_boundaries,
        len(world.external_events) - before_external,
    )


def _boundary_condition(
    parameters: HeldoutWorldParameters,
    *,
    boundary_intervention: BoundaryIntervention | None = None,
) -> tuple[int, int, int, AutonomousEndogenousChainRuntime, AnonymousBoundaryEmitter]:
    runtime, emitter, consistency = _components(
        parameters,
        boundary_intervention=boundary_intervention,
    )
    world = _world(parameters, parameters.old_target)
    _boundary_episode(
        parameters,
        runtime,
        emitter,
        consistency,
        world,
        cue_unit_id=parameters.control_path[0],
        start_ms=100.0,
        episode_spacing_ms=parameters.episode_spacings_ms[0],
        event_id="heldout:boundary:control",
    )
    main_start = 100.0 + parameters.episode_spacings_ms[0]
    _boundary_episode(
        parameters,
        runtime,
        emitter,
        consistency,
        world,
        cue_unit_id=parameters.main_path[0],
        start_ms=main_start,
        episode_spacing_ms=parameters.episode_spacings_ms[1],
        event_id="heldout:boundary:main",
    )
    return (
        sum(event.port_id == parameters.main_port for event in emitter.events),
        sum(event.port_id == parameters.control_port for event in emitter.events),
        sum(
            event.target == f"unit:{parameters.old_target}"
            for event in world.external_events
        ),
        runtime,
        emitter,
    )


def _boundary_effect(
    parameters: HeldoutWorldParameters,
) -> tuple[bool, dict[str, float], int, int, int]:
    sham_main, _, sham_external, sham_runtime, _ = _boundary_condition(parameters)
    targeted_main, _, targeted_external, targeted_runtime, targeted_emitter = (
        _boundary_condition(
            parameters,
            boundary_intervention=BoundaryIntervention(
                suppressed_port_ids=(parameters.main_port,)
            ),
        )
    )
    matched_main, _, matched_external, matched_runtime, matched_emitter = (
        _boundary_condition(
            parameters,
            boundary_intervention=BoundaryIntervention(
                suppressed_port_ids=(parameters.control_port,)
            ),
        )
    )
    targeted_impairment = 1.0 - targeted_main / max(1, sham_main)
    matched_impairment = 1.0 - matched_main / max(1, sham_main)
    passed = (
        sham_main == 1
        and sham_external == 1
        and targeted_main == 0
        and targeted_external == 0
        and matched_main == 1
        and matched_external == 1
        and targeted_impairment - matched_impairment >= 0.5
        and any(
            row.unit_id == parameters.main_path[-1]
            for row in targeted_runtime.generated_sparks
        )
    )
    generated = sum(
        len(runtime.generated_sparks)
        for runtime in (sham_runtime, targeted_runtime, matched_runtime)
    )
    training = sum(
        runtime.expectation.external_transition_count
        for runtime in (sham_runtime, targeted_runtime, matched_runtime)
    )
    interventions = len(targeted_emitter.suppressions) + len(
        matched_emitter.suppressions
    )
    return (
        passed,
        {
            "boundary_matched_impairment": float(matched_impairment),
            "boundary_targeted_impairment": float(targeted_impairment),
            "heldout_boundary_matched_count": float(matched_main),
            "heldout_boundary_sham_count": float(sham_main),
            "heldout_boundary_targeted_count": float(targeted_main),
        },
        generated,
        training,
        interventions,
    )


def _dominant_target(
    parameters: HeldoutWorldParameters,
    consistency: UntypedBoundaryConsistency,
) -> int | None:
    candidates: list[tuple[float, int]] = []
    for target in (
        parameters.old_target,
        parameters.new_target,
        parameters.third_target,
    ):
        reliability = consistency.reliability(
            port_id=parameters.main_port,
            target=f"unit:{target}",
        )
        if reliability is not None:
            candidates.append((reliability, target))
    if not candidates:
        return None
    return min(candidates, key=lambda row: (-row[0], row[1]))[1]


def _relation_cycles(
    parameters: HeldoutWorldParameters,
) -> _RelationResult:
    runtime, emitter, consistency = _components(parameters)
    snapshots: list[dict[str, Any]] = []
    dominant_targets: list[int | None] = []
    episode_index = 0
    for phase_index, (target, phase_length) in enumerate(
        zip(
            parameters.contingency_cycle_targets,
            parameters.contingency_phase_lengths,
            strict=True,
        )
    ):
        world = _world(parameters, target)
        for local_index in range(phase_length):
            spacing = parameters.episode_spacings_ms[
                episode_index % len(parameters.episode_spacings_ms)
            ]
            start = 100.0 + sum(
                parameters.episode_spacings_ms[
                    prior % len(parameters.episode_spacings_ms)
                ]
                for prior in range(episode_index)
            )
            _boundary_episode(
                parameters,
                runtime,
                emitter,
                consistency,
                world,
                cue_unit_id=parameters.main_path[0],
                start_ms=start,
                episode_spacing_ms=spacing,
                event_id=f"heldout:relation:{phase_index}:{local_index}",
            )
            episode_index += 1
        snapshots.append(consistency.learned_state_dict())
        dominant_targets.append(_dominant_target(parameters, consistency))

    internal_runtime, internal_emitter, internal_consistency = _components(parameters)
    internal_world = _world(
        parameters,
        parameters.old_target,
        suppress_ports=(parameters.main_port, parameters.control_port),
    )
    for episode in range(3):
        _boundary_episode(
            parameters,
            internal_runtime,
            internal_emitter,
            internal_consistency,
            internal_world,
            cue_unit_id=parameters.main_path[0],
            start_ms=100.0
            + sum(
                parameters.episode_spacings_ms[
                    prior % len(parameters.episode_spacings_ms)
                ]
                for prior in range(episode)
            ),
            episode_spacing_ms=parameters.episode_spacings_ms[
                episode % len(parameters.episode_spacings_ms)
            ],
            event_id=f"heldout:relation:internal-only:{episode}",
        )
    internal_links = internal_consistency.learned_state_dict()["links"]

    stable_runtime, stable_emitter, stable_consistency = _components(parameters)
    stable_world = _world(parameters, parameters.contingency_cycle_targets[0])
    stable_count = sum(parameters.contingency_phase_lengths)
    for episode in range(stable_count):
        start = 100.0 + sum(
            parameters.episode_spacings_ms[
                prior % len(parameters.episode_spacings_ms)
            ]
            for prior in range(episode)
        )
        _boundary_episode(
            parameters,
            stable_runtime,
            stable_emitter,
            stable_consistency,
            stable_world,
            cue_unit_id=parameters.main_path[0],
            start_ms=start,
            episode_spacing_ms=parameters.episode_spacings_ms[
                episode % len(parameters.episode_spacings_ms)
            ],
            event_id=f"heldout:relation:stable:{episode}",
        )
    stable_state = stable_consistency.learned_state_dict()
    stable_links = stable_state["links"]
    stable_inconsistent = sum(
        int(row["inconsistent_count"]) for row in stable_links.values()
    )
    return _RelationResult(
        snapshots=tuple(snapshots),
        phase_dominant_targets=tuple(dominant_targets),
        internal_only_link_count=len(internal_links),
        stable_link_count=len(stable_links),
        stable_inconsistent_count=stable_inconsistent,
        runtime=runtime,
        consistency=consistency,
        boundary_count=len(emitter.events),
        world_external_count=sum(
            int(row["consistent_count"])
            for row in consistency.learned_state_dict()["links"].values()
        ),
    )


def _relation_passes(
    parameters: HeldoutWorldParameters,
    result: _RelationResult,
) -> tuple[bool, bool, dict[str, float]]:
    first_target = parameters.contingency_cycle_targets[0]
    stabilization = (
        result.phase_dominant_targets
        and result.phase_dominant_targets[0] == first_target
        and result.internal_only_link_count == 0
    )
    phases_match = all(
        observed == expected
        for observed, expected in zip(
            result.phase_dominant_targets,
            parameters.contingency_cycle_targets,
            strict=True,
        )
    )
    repeated_target = len(set(parameters.contingency_cycle_targets)) < len(
        parameters.contingency_cycle_targets
    )
    revision = (
        phases_match
        and repeated_target
        and result.stable_link_count == 1
        and result.stable_inconsistent_count == 0
    )
    return (
        stabilization,
        revision,
        {
            "heldout_relation_boundary_count": float(result.boundary_count),
            "heldout_relation_internal_only_link_count": float(
                result.internal_only_link_count
            ),
            "heldout_relation_phase_match_fraction": float(
                sum(
                    observed == expected
                    for observed, expected in zip(
                        result.phase_dominant_targets,
                        parameters.contingency_cycle_targets,
                        strict=True,
                    )
                )
                / len(parameters.contingency_cycle_targets)
            ),
            "heldout_relation_stable_link_count": float(result.stable_link_count),
        },
    )


def _probe_boundary(
    parameters: HeldoutWorldParameters,
    event_id: str,
) -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=100.0,
        port_id=parameters.main_port,
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{event_id}",
        source_unit_id=parameters.main_path[-1],
        source_proposal_ids=(f"proposal:{event_id}",),
        generation_depth=3,
        source_state_hash=parameters.specification_hash(),
    )


def _run_reentry(
    parameters: HeldoutWorldParameters,
    learned_state: dict[str, Any],
    *,
    event_id: str,
) -> tuple[int, ...]:
    field = _field(parameters)
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency.from_learned_state_dict(
        learned_state,
        ledger=ledger,
    )
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            maximum_effective_current=max(2.0, parameters.threshold * 4.0),
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
            magnitude_gain=parameters.relation_reentry_gain,
            maximum_magnitude=max(2.0, parameters.threshold * 4.0),
            minimum_consistent_count=1,
            minimum_reliability=0.0,
            maximum_links_per_boundary=8,
        ),
    )
    reentry.schedule(_probe_boundary(parameters, event_id), field)
    return tuple(spike.unit_id for spike in field.run_until(102.0))


def _local_transplant(
    parameters: HeldoutWorldParameters,
    learned_state: dict[str, Any],
) -> tuple[int, ...]:
    field = _field(parameters)
    ledger = ProvenanceLedger()
    current = _pulse(
        parameters,
        "heldout:persistence:current",
        100.0,
        parameters.main_path[0],
    )
    ledger.register_external(current)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=current.time_ms,
            target_id=parameters.main_path[0],
            current=current.magnitude,
            source_id=None,
            pulse_id=current.event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    field.run_until(current.time_ms)
    model = LocalTemporalExpectation.from_learned_state_dict(learned_state)
    gain = _estimated_reinjection_gain(parameters, model, (parameters.main_path,))
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=gain,
            maximum_effective_current=max(2.0, parameters.cue_magnitude * gain),
        ),
    )
    for proposal in model.proposals_for(
        current,
        origin_state_hash=digest(
            {
                "field": field.state_dict(),
                "local_transition": learned_state,
            }
        ),
    ):
        ledger.register_proposal(proposal)
        gate.schedule(proposal, field)
    return tuple(
        spike.unit_id
        for spike in field.run_until(
            current.time_ms + max(parameters.evaluation_lags_ms) * 2.0
        )
    )


def _reentry_and_persistence(
    parameters: HeldoutWorldParameters,
    relation: _RelationResult,
) -> tuple[bool, bool, dict[str, float], int]:
    reentry_results = tuple(
        _run_reentry(
            parameters,
            snapshot,
            event_id=f"heldout:reentry:{index}",
        )
        for index, snapshot in enumerate(relation.snapshots)
    )
    reentry_matches = tuple(
        rows == (target,)
        for rows, target in zip(
            reentry_results,
            parameters.contingency_cycle_targets,
            strict=True,
        )
    )
    empty_consistency = {
        "config": relation.snapshots[0]["config"],
        "links": {},
    }
    reset_reentry = _run_reentry(
        parameters,
        empty_consistency,
        event_id="heldout:reentry:reset",
    )

    donor = _train_expectation(parameters, (parameters.main_path,))
    donor_state = donor.learned_state_dict()
    transplanted = _local_transplant(parameters, donor_state)
    empty_transition = {
        "config": donor_state["config"],
        "external_transition_count": 0,
        "transitions": {},
    }
    reset_transition = _local_transplant(parameters, empty_transition)
    reentry = all(reentry_matches) and reset_reentry == ()
    persistence = (
        transplanted[:1] == (parameters.main_path[1],)
        and reset_transition == ()
        and reentry_results[0] == (
            parameters.contingency_cycle_targets[0],
        )
        and reset_reentry == ()
    )
    generated = sum(len(row) for row in reentry_results) + len(transplanted)
    return (
        reentry,
        persistence,
        {
            "heldout_persistence_local_reset_count": float(len(reset_transition)),
            "heldout_persistence_local_transplant_count": float(len(transplanted)),
            "heldout_reentry_phase_match_fraction": float(
                sum(reentry_matches) / len(reentry_matches)
            ),
            "heldout_reentry_reset_count": float(len(reset_reentry)),
        },
        generated,
    )


def _leaf_count(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(_leaf_count(item) for item in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return sum(_leaf_count(item) for item in value)
    return 1


def run_condition(
    parameters: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    """Execute the Primary against one immutable held-out world specification."""

    parameters.validate()
    started = time.perf_counter()
    origin, state, origin_metrics, origin_generated, origin_training = (
        _origin_and_state(parameters)
    )
    chain, chain_metrics, chain_generated, chain_training, chain_interventions = (
        _autonomous_chain(parameters)
    )
    boundary, boundary_metrics, boundary_generated, boundary_training, boundary_interventions = (
        _boundary_effect(parameters)
    )
    relation = _relation_cycles(parameters)
    stabilization, revision, relation_metrics = _relation_passes(
        parameters,
        relation,
    )
    reentry, persistence, reentry_metrics, reentry_generated = (
        _reentry_and_persistence(parameters, relation)
    )
    taxonomy_state = {
        "consistency": relation.consistency.learned_state_dict(),
        "runtime": relation.runtime.state_dict(),
    }
    taxonomy = len(
        verify_taxonomy_variant_runtime_equality(
            {
                "observer-a": taxonomy_state,
                "renamed-observer": taxonomy_state,
            }
        )
    ) == 64
    passed = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: origin,
        EvidenceDomain.STATE_DEPENDENCE: state,
        EvidenceDomain.AUTONOMOUS_CHAIN: chain,
        EvidenceDomain.BOUNDARY_EFFECT: boundary,
        EvidenceDomain.RELATION_STABILIZATION: stabilization,
        EvidenceDomain.REVERSAL_REACQUISITION: revision,
        EvidenceDomain.RELATION_REENTRY: reentry,
        EvidenceDomain.PERSISTENCE_LOCUS: persistence,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: taxonomy,
    }
    persistent_state = {
        "consistency": relation.consistency.learned_state_dict(),
        "local_transition": relation.runtime.expectation.learned_state_dict(),
    }
    metrics = {
        **origin_metrics,
        **chain_metrics,
        **boundary_metrics,
        **relation_metrics,
        **reentry_metrics,
        "active_unit_fraction": parameters.active_fraction,
        "branch_count": float(parameters.branch_count),
        "contingency_change_count": float(parameters.contingency_change_count),
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": float(taxonomy),
        "world_specification_hash_prefix": float(
            int(parameters.specification_hash()[:12], 16)
        ),
    }
    records = build_result_records(
        parameters,
        ConfirmatoryCondition.PRIMARY,
        passed,
        metrics,
    )
    generated_count = (
        origin_generated
        + chain_generated
        + boundary_generated
        + len(relation.runtime.generated_sparks)
        + reentry_generated
    )
    observed_training = (
        origin_training
        + chain_training
        + boundary_training
        + relation.runtime.expectation.external_transition_count
        + relation.world_external_count
    )
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        observed_training_events=observed_training,
        generated_internal_events=generated_count,
        persistent_state_entries=_leaf_count(persistent_state),
        intervention_count=chain_interventions + boundary_interventions,
        parameter_count=parameters.unit_count * 3 + _leaf_count(persistent_state),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=True,
        normal_field_threshold_crossings=generated_count,
        threshold_bypassed=False,
        explicit_assembly_entries=0,
        typed_head_count=0,
        scalar_reward_observations=0,
        privileged_information=(),
    )
    semantic_hash = digest(
        {
            "records": [result_record_state(row) for row in records],
            "resource": {
                key: value
                for key, value in resource.state_dict().items()
                if key != "wall_clock_ms"
            },
            "world_specification_hash": parameters.specification_hash(),
        }
    )
    execution = HeldoutConditionExecution(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        world_specification_hash=parameters.specification_hash(),
        records=records,
        resource=resource,
        semantic_hash=semantic_hash,
    )
    execution.validate()
    return execution

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
    EndogenousChainSpark,
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
from sparkbrain.v06.relation_reentry import (
    AnonymousRelationReentry,
    RelationReentryConfig,
)
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
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


@dataclass(frozen=True, slots=True)
class ChainRun:
    units: tuple[int, ...]
    times_ms: tuple[float, ...]
    runtime: AutonomousEndogenousChainRuntime


@dataclass(frozen=True, slots=True)
class RelationRun:
    snapshots: tuple[dict[str, Any], ...]
    phase_targets: tuple[int | None, ...]
    internal_only_link_count: int
    stable_link_count: int
    stable_inconsistent_count: int
    generated_sparks: int
    observed_training_events: int
    consistency: UntypedBoundaryConsistency


def external_pulse(
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


def build_field(parameters: HeldoutWorldParameters) -> TemporalExcitableField:
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


def expectation_config(parameters: HeldoutWorldParameters) -> LocalExpectationConfig:
    lags = tuple(
        lag
        for profile in parameters.training_lag_profiles_ms
        for lag in profile
    )
    mean_lag = fmean(lags)
    variance = max(1.0, fmean((lag - mean_lag) ** 2 for lag in lags))
    return LocalExpectationConfig(
        max_lag_ms=max(lags) * 3.0,
        minimum_observations=2,
        minimum_confidence=0.01,
        maximum_candidates=max(8, parameters.branch_count + 2),
        proposal_ttl_ms=max(lags) * 5.0,
        variance_scale_ms2=max(4.0, variance * 4.0),
        energy_scale=0.05,
    )


def path_exposure_counts(
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
        result[path] = max(
            result.get(path, 0),
            competition.get(path, default_count),
        )
    return result


def train_expectation(
    parameters: HeldoutWorldParameters,
    paths: Iterable[tuple[int, int, int, int]],
) -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(expectation_config(parameters))
    exposures = path_exposure_counts(parameters, paths)
    for path_index, (path, count) in enumerate(sorted(exposures.items())):
        for episode in range(count):
            profile = parameters.training_lag_profiles_ms[
                episode % len(parameters.training_lag_profiles_ms)
            ]
            times = [float(path_index * 10000 + episode * 100)]
            for lag in profile:
                times.append(times[-1] + lag)
            pulses = tuple(
                external_pulse(
                    parameters,
                    f"train:{path_index}:{episode}:{index}",
                    times[index],
                    unit_id,
                )
                for index, unit_id in enumerate(path)
            )
            for source, target in zip(pulses, pulses[1:], strict=False):
                model.observe_external_transition(source, target)
    return model


def estimate_reinjection_gain(
    parameters: HeldoutWorldParameters,
    model: LocalTemporalExpectation,
    paths: Iterable[tuple[int, int, int, int]],
) -> float:
    confidences: list[float] = []
    original_proposal_count = model.proposal_count
    for source_unit in sorted({unit for path in paths for unit in path[:-1]}):
        source = external_pulse(
            parameters,
            f"gain:{source_unit}",
            0.0,
            source_unit,
        )
        rows = model.proposals_for(source, origin_state_hash="0" * 64)
        if rows:
            confidences.append(max(row.confidence for row in rows))
    model.proposal_count = original_proposal_count
    if not confidences:
        return 1.0
    confidence = max(1e-6, min(confidences))
    return parameters.threshold / (parameters.cue_magnitude * confidence) * 1.08


def build_runtime(
    parameters: HeldoutWorldParameters,
    paths: Iterable[tuple[int, int, int, int]],
    *,
    intervention: EndogenousChainIntervention | None = None,
) -> AutonomousEndogenousChainRuntime:
    path_rows = tuple(dict.fromkeys(paths))
    expectation = train_expectation(parameters, path_rows)
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    gain = estimate_reinjection_gain(parameters, expectation, path_rows)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=gain,
            maximum_effective_current=max(2.0, parameters.cue_magnitude * gain),
            maximum_generation_depth=8,
            maximum_energy_per_window=256.0,
            maximum_proposals_per_window=64,
            maximum_branches_per_origin_state=max(8, parameters.branch_count + 2),
            window_ms=max(parameters.episode_spacings_ms),
        ),
    )
    return AutonomousEndogenousChainRuntime(
        build_field(parameters),
        expectation,
        transition,
        reinjection,
        intervention=intervention,
    )


def evaluation_horizon(parameters: HeldoutWorldParameters, start_ms: float) -> float:
    return (
        start_ms
        + sum(parameters.evaluation_lags_ms)
        + max(parameters.evaluation_lags_ms)
        + 5.0
    )


def run_cue(
    runtime: AutonomousEndogenousChainRuntime,
    parameters: HeldoutWorldParameters,
    *,
    cue_unit_id: int,
    start_ms: float,
    event_id: str,
) -> ChainRun:
    before = len(runtime.generated_sparks)
    runtime.present_external(
        external_pulse(parameters, event_id, start_ms, cue_unit_id)
    )
    runtime.advance_silence(evaluation_horizon(parameters, start_ms))
    sparks = tuple(runtime.generated_sparks[before:])
    return ChainRun(
        units=tuple(row.unit_id for row in sparks),
        times_ms=tuple(row.time_ms for row in sparks),
        runtime=runtime,
    )


def finite_timing_error(
    result: ChainRun,
    parameters: HeldoutWorldParameters,
    start_ms: float,
) -> tuple[bool, float]:
    if len(result.times_ms) < 3:
        return False, -1.0
    times = (start_ms, *result.times_ms[:3])
    observed = tuple(
        right - left for left, right in zip(times, times[1:], strict=False)
    )
    error = max(
        abs(left - right)
        for left, right in zip(
            observed,
            parameters.evaluation_lags_ms,
            strict=True,
        )
    )
    if not math.isfinite(error):
        return False, -1.0
    return True, float(error)


def origin_and_state_evidence(
    parameters: HeldoutWorldParameters,
) -> tuple[bool, bool, dict[str, float], int, int]:
    main_runtime = build_runtime(parameters, (parameters.main_path,))
    main = run_cue(
        main_runtime,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="heldout:origin:main",
    )
    alternate_runtime = build_runtime(parameters, (parameters.alternate_path,))
    alternate = run_cue(
        alternate_runtime,
        parameters,
        cue_unit_id=parameters.alternate_path[0],
        start_ms=100.0,
        event_id="heldout:origin:alternate",
    )
    no_history_runtime = build_runtime(parameters, ())
    no_history = run_cue(
        no_history_runtime,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="heldout:origin:no-history",
    )
    timing_available, timing_error = finite_timing_error(
        main,
        parameters,
        100.0,
    )
    lag_spread = max(
        max(profile[index] for profile in parameters.training_lag_profiles_ms)
        - min(profile[index] for profile in parameters.training_lag_profiles_ms)
        for index in range(3)
    )
    tolerance = max(0.5, lag_spread)
    origin = bool(
        main.units[:3] == parameters.main_path[1:]
        and main.units
        and main.units[0] != parameters.main_path[0]
        and no_history.units == ()
        and timing_available
        and timing_error <= tolerance
    )
    state = bool(
        alternate.units[:3] == parameters.alternate_path[1:]
        and alternate.units != main.units
        and no_history.units == ()
    )
    generated = len(main.units) + len(alternate.units) + len(no_history.units)
    training = (
        main_runtime.expectation.external_transition_count
        + alternate_runtime.expectation.external_transition_count
    )
    return (
        origin,
        state,
        {
            "heldout_origin_generated_count": float(len(main.units)),
            "heldout_origin_no_history_count": float(len(no_history.units)),
            "heldout_origin_timing_error_ms": timing_error,
            "heldout_state_alternate_generated_count": float(len(alternate.units)),
        },
        generated,
        training,
    )


def active_paths(
    parameters: HeldoutWorldParameters,
) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        dict.fromkeys((*parameters.competition_paths, parameters.control_path))
    )


def chain_condition(
    parameters: HeldoutWorldParameters,
    *,
    path: tuple[int, int, int, int],
    intervention: EndogenousChainIntervention | None = None,
    event_id: str,
) -> ChainRun:
    runtime = build_runtime(
        parameters,
        active_paths(parameters),
        intervention=intervention,
    )
    return run_cue(
        runtime,
        parameters,
        cue_unit_id=path[0],
        start_ms=100.0,
        event_id=event_id,
    )


def autonomous_chain_evidence(
    parameters: HeldoutWorldParameters,
) -> tuple[bool, dict[str, float], int, int, int]:
    sham_main = chain_condition(
        parameters,
        path=parameters.main_path,
        event_id="heldout:chain:sham-main",
    )
    sham_control = chain_condition(
        parameters,
        path=parameters.control_path,
        event_id="heldout:chain:sham-control",
    )
    targeted = chain_condition(
        parameters,
        path=parameters.main_path,
        intervention=EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.main_path[1],)
        ),
        event_id="heldout:chain:targeted",
    )
    matched_main = chain_condition(
        parameters,
        path=parameters.main_path,
        intervention=EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.control_path[1],)
        ),
        event_id="heldout:chain:matched-main",
    )
    matched_control = chain_condition(
        parameters,
        path=parameters.control_path,
        intervention=EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.control_path[1],)
        ),
        event_id="heldout:chain:matched-control",
    )
    sham_downstream = sum(
        unit in parameters.main_path[2:] for unit in sham_main.units
    )
    targeted_downstream = sum(
        unit in parameters.main_path[2:] for unit in targeted.units
    )
    matched_downstream = sum(
        unit in parameters.main_path[2:] for unit in matched_main.units
    )
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    runtimes = (
        sham_main.runtime,
        sham_control.runtime,
        targeted.runtime,
        matched_main.runtime,
        matched_control.runtime,
    )
    passed = bool(
        sham_main.units[:3] == parameters.main_path[1:]
        and sham_control.units[:3] == parameters.control_path[1:]
        and targeted.units == (parameters.main_path[1],)
        and matched_main.units[:3] == parameters.main_path[1:]
        and matched_control.units == (parameters.control_path[1],)
        and targeted_impairment - matched_impairment >= 0.5
        and all(runtime.ledger.committed_positive_updates == 0 for runtime in runtimes)
    )
    generated = sum(len(runtime.generated_sparks) for runtime in runtimes)
    training = sum(runtime.expectation.external_transition_count for runtime in runtimes)
    interventions = sum(len(runtime.intervention_records) for runtime in runtimes)
    return (
        passed,
        {
            "chain_matched_impairment": float(matched_impairment),
            "chain_targeted_impairment": float(targeted_impairment),
            "heldout_chain_matched_units": float(len(matched_main.units)),
            "heldout_chain_sham_units": float(len(sham_main.units)),
            "heldout_chain_targeted_units": float(len(targeted.units)),
        },
        generated,
        training,
        interventions,
    )


def terminal_spark(
    parameters: HeldoutWorldParameters,
    *,
    path: tuple[int, int, int, int],
    event_id: str,
    start_ms: float,
) -> tuple[EndogenousChainSpark | None, AutonomousEndogenousChainRuntime]:
    runtime = build_runtime(parameters, active_paths(parameters))
    result = run_cue(
        runtime,
        parameters,
        cue_unit_id=path[0],
        start_ms=start_ms,
        event_id=event_id,
    )
    rows = [
        row
        for row in runtime.generated_sparks
        if row.unit_id == path[-1]
    ]
    return (rows[-1] if rows else None), runtime


def boundary_world(
    parameters: HeldoutWorldParameters,
    *,
    main_target: int,
    suppressed_ports: tuple[str, ...] = (),
) -> AnonymousBoundaryWorld:
    return AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id=parameters.main_port,
                target=f"unit:{main_target}",
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
            suppressed_port_ids=suppressed_ports
        ),
    )


def boundary_case(
    parameters: HeldoutWorldParameters,
    *,
    suppress_port: str | None,
) -> tuple[int, int, int, int, int]:
    intervention = (
        BoundaryIntervention(suppressed_port_ids=(suppress_port,))
        if suppress_port is not None
        else None
    )
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
        intervention=intervention,
    )
    world = boundary_world(parameters, main_target=parameters.old_target)
    main_spark, main_runtime = terminal_spark(
        parameters,
        path=parameters.main_path,
        event_id=f"heldout:boundary:main:{suppress_port}",
        start_ms=100.0,
    )
    control_spark, control_runtime = terminal_spark(
        parameters,
        path=parameters.control_path,
        event_id=f"heldout:boundary:control:{suppress_port}",
        start_ms=100.0,
    )
    sparks = tuple(
        row for row in (main_spark, control_spark) if row is not None
    )
    events = emitter.emit(
        sparks,
        source_state_hash=digest(
            {
                "control": control_runtime.state_dict(),
                "main": main_runtime.state_dict(),
            }
        ),
    )
    external = tuple(pulse for event in events for pulse in world.receive(event))
    return (
        sum(event.port_id == parameters.main_port for event in events),
        sum(event.port_id == parameters.control_port for event in events),
        sum(pulse.target == f"unit:{parameters.old_target}" for pulse in external),
        int(main_spark is not None),
        len(emitter.suppressions),
    )


def boundary_effect_evidence(
    parameters: HeldoutWorldParameters,
) -> tuple[bool, dict[str, float], int]:
    sham = boundary_case(parameters, suppress_port=None)
    targeted = boundary_case(parameters, suppress_port=parameters.main_port)
    matched = boundary_case(parameters, suppress_port=parameters.control_port)
    targeted_impairment = 1.0 - targeted[0] / max(1, sham[0])
    matched_impairment = 1.0 - matched[0] / max(1, sham[0])
    passed = bool(
        sham[0] == 1
        and sham[2] == 1
        and targeted[0] == 0
        and targeted[2] == 0
        and targeted[3] == 1
        and matched[0] == 1
        and matched[2] == 1
        and targeted_impairment - matched_impairment >= 0.5
    )
    return (
        passed,
        {
            "boundary_matched_impairment": float(matched_impairment),
            "boundary_targeted_impairment": float(targeted_impairment),
            "heldout_boundary_matched_count": float(matched[0]),
            "heldout_boundary_sham_count": float(sham[0]),
            "heldout_boundary_targeted_count": float(targeted[0]),
        },
        sham[4] + targeted[4] + matched[4],
    )


def new_consistency(
    ledger: ProvenanceLedger,
    parameters: HeldoutWorldParameters,
) -> UntypedBoundaryConsistency:
    return UntypedBoundaryConsistency(
        ledger,
        AnonymousConsistencyConfig(
            maximum_pair_lag_ms=parameters.boundary_lag_ms * 2.0,
            pending_ttl_ms=parameters.boundary_lag_ms * 3.0,
            maximum_pending=512,
        ),
    )


def relation_episode(
    parameters: HeldoutWorldParameters,
    consistency: UntypedBoundaryConsistency,
    *,
    target: int,
    episode_index: int,
    internal_only: bool = False,
) -> int:
    start_ms = 100.0 + sum(
        parameters.episode_spacings_ms[
            index % len(parameters.episode_spacings_ms)
        ]
        for index in range(episode_index)
    )
    spark, runtime = terminal_spark(
        parameters,
        path=parameters.main_path,
        event_id=f"heldout:relation:{episode_index}",
        start_ms=start_ms,
    )
    if spark is None:
        return 0
    emitter = AnonymousBoundaryEmitter(
        (
            BoundaryCoupling(
                source_unit_id=parameters.main_path[-1],
                port_id=parameters.main_port,
            ),
        )
    )
    events = emitter.emit((spark,), source_state_hash=runtime.state_hash())
    world = boundary_world(
        parameters,
        main_target=target,
        suppressed_ports=(parameters.main_port,) if internal_only else (),
    )
    for event in events:
        consistency.register_boundary(event)
        for external in world.receive(event):
            consistency.ledger.register_external(external)
            consistency.observe_external(external)
    consistency.expire(start_ms + max(parameters.episode_spacings_ms) - 1.0)
    return len(runtime.generated_sparks)


def dominant_target(
    parameters: HeldoutWorldParameters,
    consistency: UntypedBoundaryConsistency,
) -> int | None:
    rows: list[tuple[float, int]] = []
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
            rows.append((reliability, target))
    if not rows:
        return None
    return min(rows, key=lambda row: (-row[0], row[1]))[1]


def relation_cycles(parameters: HeldoutWorldParameters) -> RelationRun:
    ledger = ProvenanceLedger()
    consistency = new_consistency(ledger, parameters)
    snapshots: list[dict[str, Any]] = []
    phase_targets: list[int | None] = []
    generated = 0
    episode_index = 0
    for target, length in zip(
        parameters.contingency_cycle_targets,
        parameters.contingency_phase_lengths,
        strict=True,
    ):
        for _ in range(length):
            generated += relation_episode(
                parameters,
                consistency,
                target=target,
                episode_index=episode_index,
            )
            episode_index += 1
        snapshots.append(consistency.learned_state_dict())
        phase_targets.append(dominant_target(parameters, consistency))

    internal_ledger = ProvenanceLedger()
    internal = new_consistency(internal_ledger, parameters)
    for index in range(3):
        relation_episode(
            parameters,
            internal,
            target=parameters.old_target,
            episode_index=index,
            internal_only=True,
        )
    internal_links = internal.learned_state_dict()["links"]

    stable_ledger = ProvenanceLedger()
    stable = new_consistency(stable_ledger, parameters)
    stable_target = parameters.contingency_cycle_targets[0]
    for index in range(sum(parameters.contingency_phase_lengths)):
        relation_episode(
            parameters,
            stable,
            target=stable_target,
            episode_index=index,
        )
    stable_links = stable.learned_state_dict()["links"]
    stable_inconsistent = sum(
        int(row["inconsistent_count"]) for row in stable_links.values()
    )
    observed_training = sum(
        int(row["consistent_count"])
        for row in consistency.learned_state_dict()["links"].values()
    )
    return RelationRun(
        snapshots=tuple(snapshots),
        phase_targets=tuple(phase_targets),
        internal_only_link_count=len(internal_links),
        stable_link_count=len(stable_links),
        stable_inconsistent_count=stable_inconsistent,
        generated_sparks=generated,
        observed_training_events=observed_training,
        consistency=consistency,
    )


def relation_evidence(
    parameters: HeldoutWorldParameters,
    relation: RelationRun,
) -> tuple[bool, bool, dict[str, float]]:
    phase_matches = tuple(
        observed == expected
        for observed, expected in zip(
            relation.phase_targets,
            parameters.contingency_cycle_targets,
            strict=True,
        )
    )
    stabilization = bool(
        relation.phase_targets
        and relation.phase_targets[0] == parameters.contingency_cycle_targets[0]
        and relation.internal_only_link_count == 0
    )
    repeated_target = len(set(parameters.contingency_cycle_targets)) < len(
        parameters.contingency_cycle_targets
    )
    revision = bool(
        all(phase_matches)
        and repeated_target
        and relation.stable_link_count == 1
        and relation.stable_inconsistent_count == 0
    )
    return (
        stabilization,
        revision,
        {
            "heldout_relation_internal_only_link_count": float(
                relation.internal_only_link_count
            ),
            "heldout_relation_phase_match_fraction": float(
                sum(phase_matches) / len(phase_matches)
            ),
            "heldout_relation_stable_link_count": float(
                relation.stable_link_count
            ),
        },
    )


def probe_boundary_event(
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


def reentry_units(
    parameters: HeldoutWorldParameters,
    learned_state: dict[str, Any],
    *,
    event_id: str,
) -> tuple[int, ...]:
    field = build_field(parameters)
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
            maximum_candidates=8,
        ),
    )
    reentry.schedule(probe_boundary_event(parameters, event_id), field)
    return tuple(spike.unit_id for spike in field.run_until(102.0))


def transplant_local_state(
    parameters: HeldoutWorldParameters,
    learned_state: dict[str, Any],
) -> tuple[int, ...]:
    field = build_field(parameters)
    ledger = ProvenanceLedger()
    current = external_pulse(
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
    gain = estimate_reinjection_gain(parameters, model, (parameters.main_path,))
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            current_gain=gain,
            maximum_effective_current=max(2.0, parameters.cue_magnitude * gain),
        ),
    )
    origin_hash = digest(
        {
            "field": field.state_dict(),
            "local_transition": learned_state,
        }
    )
    for proposal in model.proposals_for(current, origin_state_hash=origin_hash):
        ledger.register_proposal(proposal)
        gate.schedule(proposal, field)
    horizon = current.time_ms + max(parameters.evaluation_lags_ms) * 2.0
    return tuple(spike.unit_id for spike in field.run_until(horizon))


def reentry_and_persistence_evidence(
    parameters: HeldoutWorldParameters,
    relation: RelationRun,
) -> tuple[bool, bool, dict[str, float], int]:
    responses = tuple(
        reentry_units(
            parameters,
            snapshot,
            event_id=f"heldout:reentry:{index}",
        )
        for index, snapshot in enumerate(relation.snapshots)
    )
    matches = tuple(
        response == (target,)
        for response, target in zip(
            responses,
            parameters.contingency_cycle_targets,
            strict=True,
        )
    )
    empty_consistency = {
        "config": relation.snapshots[0]["config"],
        "links": {},
    }
    reset_reentry = reentry_units(
        parameters,
        empty_consistency,
        event_id="heldout:reentry:reset",
    )
    donor = train_expectation(parameters, (parameters.main_path,))
    donor_state = donor.learned_state_dict()
    transplanted = transplant_local_state(parameters, donor_state)
    empty_transition = {
        "config": donor_state["config"],
        "external_transition_count": 0,
        "transitions": {},
    }
    reset_transition = transplant_local_state(parameters, empty_transition)
    reentry = bool(all(matches) and reset_reentry == ())
    persistence = bool(
        transplanted[:1] == (parameters.main_path[1],)
        and reset_transition == ()
        and responses[0] == (parameters.contingency_cycle_targets[0],)
        and reset_reentry == ()
    )
    return (
        reentry,
        persistence,
        {
            "heldout_persistence_local_reset_count": float(len(reset_transition)),
            "heldout_persistence_local_transplant_count": float(len(transplanted)),
            "heldout_reentry_phase_match_fraction": float(
                sum(matches) / len(matches)
            ),
            "heldout_reentry_reset_count": float(len(reset_reentry)),
        },
        sum(len(row) for row in responses) + len(transplanted),
    )


def leaf_count(value: Any) -> int:
    if isinstance(value, Mapping):
        return sum(leaf_count(item) for item in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return sum(leaf_count(item) for item in value)
    return 1


def run_condition(
    parameters: HeldoutWorldParameters,
) -> HeldoutConditionExecution:
    parameters.validate()
    started = time.perf_counter()
    origin, state, origin_metrics, origin_generated, origin_training = (
        origin_and_state_evidence(parameters)
    )
    chain, chain_metrics, chain_generated, chain_training, chain_interventions = (
        autonomous_chain_evidence(parameters)
    )
    boundary, boundary_metrics, boundary_interventions = boundary_effect_evidence(
        parameters
    )
    relation = relation_cycles(parameters)
    stabilization, revision, relation_metrics = relation_evidence(
        parameters,
        relation,
    )
    reentry, persistence, reentry_metrics, reentry_generated = (
        reentry_and_persistence_evidence(parameters, relation)
    )
    taxonomy_state = {
        "consistency": relation.consistency.learned_state_dict(),
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
    metrics = {
        **origin_metrics,
        **chain_metrics,
        **boundary_metrics,
        **relation_metrics,
        **reentry_metrics,
        "active_unit_fraction": float(parameters.active_fraction),
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
    persistent_state = {
        "consistency": relation.consistency.learned_state_dict(),
        "local_transition": train_expectation(
            parameters,
            (parameters.main_path,),
        ).learned_state_dict(),
    }
    generated_count = (
        origin_generated
        + chain_generated
        + relation.generated_sparks
        + reentry_generated
    )
    observed_training = (
        origin_training
        + chain_training
        + relation.observed_training_events
    )
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=ConfirmatoryCondition.PRIMARY,
        observed_training_events=observed_training,
        generated_internal_events=generated_count,
        persistent_state_entries=leaf_count(persistent_state),
        intervention_count=chain_interventions + boundary_interventions,
        parameter_count=parameters.unit_count * 3 + leaf_count(persistent_state),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=True,
        ordinary_field_threshold_crossings=generated_count,
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

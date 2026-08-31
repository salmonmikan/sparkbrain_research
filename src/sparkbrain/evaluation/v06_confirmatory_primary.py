from __future__ import annotations

import random
from dataclasses import asdict, dataclass
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

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)

QUALIFICATION_FAMILIES = (
    "identifier-permutation",
    "temporal-perturbation",
    "field-gain-perturbation",
)
QUALIFICATION_SEEDS = (0, 1, 2)


@dataclass(frozen=True, slots=True)
class PrimaryWorldParameters:
    family_id: str
    seed: int
    main_path: tuple[int, int, int, int]
    alternate_path: tuple[int, int, int, int]
    control_path: tuple[int, int, int, int]
    old_target: int
    new_target: int
    main_port: str
    control_port: str
    transition_lag_ms: float
    boundary_lag_ms: float
    threshold: float
    cue_magnitude: float
    relation_reentry_gain: float
    episode_spacing_ms: float
    unit_count: int = 13

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PrimaryWorldEvidence:
    family_id: str
    seed: int
    endogenous_origin_passed: bool
    state_dependence_passed: bool
    autonomous_chain_passed: bool
    boundary_effect_passed: bool
    relation_stabilization_passed: bool
    reversal_reacquisition_passed: bool
    relation_reentry_passed: bool
    persistence_locus_passed: bool
    taxonomy_non_interference_passed: bool
    metrics: tuple[tuple[str, float], ...]

    @property
    def all_passed(self) -> bool:
        return all(
            (
                self.endogenous_origin_passed,
                self.state_dependence_passed,
                self.autonomous_chain_passed,
                self.boundary_effect_passed,
                self.relation_stabilization_passed,
                self.reversal_reacquisition_passed,
                self.relation_reentry_passed,
                self.persistence_locus_passed,
                self.taxonomy_non_interference_passed,
            )
        )

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["all_passed"] = self.all_passed
        return value


@dataclass(frozen=True, slots=True)
class PrimaryQualificationGrid:
    worlds: tuple[PrimaryWorldEvidence, ...]
    records: tuple[ConfirmatoryResultRecord, ...]

    @property
    def passed_world_count(self) -> int:
        return sum(row.all_passed for row in self.worlds)

    @property
    def complete(self) -> bool:
        return (
            len(self.worlds) == 9
            and len(self.records) == 81
            and self.passed_world_count == len(self.worlds)
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "complete": self.complete,
            "passed_world_count": self.passed_world_count,
            "record_count": len(self.records),
            "worlds": [row.state_dict() for row in self.worlds],
        }


def world_parameters(family_id: str, seed: int) -> PrimaryWorldParameters:
    if family_id not in QUALIFICATION_FAMILIES:
        raise ValueError(f"unknown qualification world family: {family_id}")
    if seed not in QUALIFICATION_SEEDS:
        raise ValueError(f"unsupported qualification seed: {seed}")
    rng_seed = int(digest({"family_id": family_id, "seed": seed})[:16], 16)
    rng = random.Random(rng_seed)
    roles = list(range(13))
    rng.shuffle(roles)

    if family_id == "identifier-permutation":
        lag_ms = 5.0
        boundary_lag_ms = 10.0
        threshold = 0.5
        cue_magnitude = 1.0
        main_port = f"port:{100 + roles[0]}"
        control_port = f"port:{200 + roles[7]}"
    elif family_id == "temporal-perturbation":
        lag_ms = float(4 + seed)
        boundary_lag_ms = float(8 + seed * 2)
        threshold = 0.5
        cue_magnitude = 1.0
        main_port = "port:7"
        control_port = "port:9"
    else:
        lag_ms = 5.0
        boundary_lag_ms = 10.0
        threshold = (0.44, 0.50, 0.56)[seed]
        cue_magnitude = threshold + 0.44
        main_port = "port:7"
        control_port = "port:9"

    spacing = max(70.0, 6.0 * lag_ms + boundary_lag_ms + 20.0)
    return PrimaryWorldParameters(
        family_id=family_id,
        seed=seed,
        main_path=(roles[0], roles[1], roles[2], roles[3]),
        alternate_path=(roles[0], roles[4], roles[5], roles[6]),
        control_path=(roles[7], roles[8], roles[9], roles[10]),
        old_target=roles[11],
        new_target=roles[12],
        main_port=main_port,
        control_port=control_port,
        transition_lag_ms=lag_ms,
        boundary_lag_ms=boundary_lag_ms,
        threshold=threshold,
        cue_magnitude=cue_magnitude,
        relation_reentry_gain=threshold / 0.65,
        episode_spacing_ms=spacing,
    )


def _pulse(
    event_id: str,
    time_ms: float,
    unit_id: int,
    parameters: PrimaryWorldParameters,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=parameters.cue_magnitude,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _expectation(
    parameters: PrimaryWorldParameters,
    paths: tuple[tuple[int, int, int, int], ...],
) -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(
        LocalExpectationConfig(
            max_lag_ms=max(20.0, parameters.transition_lag_ms * 3.0),
            minimum_observations=2,
            minimum_confidence=0.1,
            maximum_candidates=4,
            proposal_ttl_ms=max(20.0, parameters.transition_lag_ms * 4.0),
        )
    )
    cursor = 0
    for path_index, path in enumerate(paths):
        for episode in range(3):
            start_ms = cursor * parameters.episode_spacing_ms
            rows = tuple(
                _pulse(
                    f"train:{path_index}:{episode}:{index}",
                    start_ms + index * parameters.transition_lag_ms,
                    unit_id,
                    parameters,
                )
                for index, unit_id in enumerate(path)
            )
            for source, target in zip(rows, rows[1:], strict=False):
                model.observe_external_transition(source, target)
            cursor += 1
    return model


def _field(parameters: PrimaryWorldParameters) -> TemporalExcitableField:
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
        receptor_ids=tuple(range(parameters.unit_count)),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=max(1.0, parameters.transition_lag_ms / 2.0),
        ),
    )


def _runtime(
    parameters: PrimaryWorldParameters,
    paths: tuple[tuple[int, int, int, int], ...],
    *,
    intervention: EndogenousChainIntervention | None = None,
) -> AutonomousEndogenousChainRuntime:
    expectation = _expectation(parameters, paths)
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.1,
            maximum_effective_current=2.0,
            maximum_generation_depth=6,
            maximum_proposals_per_window=32,
            maximum_branches_per_origin_state=8,
            maximum_energy_per_window=16.0,
            window_ms=max(50.0, parameters.episode_spacing_ms),
        ),
    )
    return AutonomousEndogenousChainRuntime(
        _field(parameters),
        expectation,
        transition,
        reinjection,
        intervention=intervention,
    )


def _run_cue(
    runtime: AutonomousEndogenousChainRuntime,
    parameters: PrimaryWorldParameters,
    *,
    cue_unit_id: int,
    start_ms: float,
    event_id: str,
) -> tuple[int, ...]:
    before = len(runtime.generated_sparks)
    runtime.present_external(
        _pulse(event_id, start_ms, cue_unit_id, parameters)
    )
    runtime.advance_silence(
        start_ms + parameters.transition_lag_ms * 4.0
    )
    return tuple(row.unit_id for row in runtime.generated_sparks[before:])


def _state_and_origin(
    parameters: PrimaryWorldParameters,
) -> tuple[bool, bool, dict[str, float]]:
    main = _runtime(parameters, (parameters.main_path,))
    main_units = _run_cue(
        main,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="origin:main",
    )
    alternate = _runtime(parameters, (parameters.alternate_path,))
    alternate_units = _run_cue(
        alternate,
        parameters,
        cue_unit_id=parameters.alternate_path[0],
        start_ms=100.0,
        event_id="origin:alternate",
    )
    no_history = _runtime(parameters, ())
    no_history_units = _run_cue(
        no_history,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0,
        event_id="origin:no-history",
    )
    root = main_units[:1]
    origin_passed = (
        main_units == parameters.main_path[1:]
        and root == (parameters.main_path[1],)
        and parameters.main_path[1] != parameters.main_path[0]
        and main.ledger.external_observation_count == 1
        and main.ledger.committed_positive_updates == 0
    )
    state_passed = (
        alternate_units == parameters.alternate_path[1:]
        and main_units != alternate_units
        and no_history_units == ()
    )
    return (
        origin_passed,
        state_passed,
        {
            "origin_main_generated_count": float(len(main_units)),
            "state_alternate_generated_count": float(len(alternate_units)),
            "state_no_history_generated_count": float(len(no_history_units)),
        },
    )


def _run_two_chain_condition(
    parameters: PrimaryWorldParameters,
    intervention: EndogenousChainIntervention | None = None,
) -> tuple[tuple[int, ...], tuple[int, ...], int, int, int]:
    runtime = _runtime(
        parameters,
        (parameters.main_path, parameters.control_path),
        intervention=intervention,
    )
    control = _run_cue(
        runtime,
        parameters,
        cue_unit_id=parameters.control_path[0],
        start_ms=100.0,
        event_id="chain:control",
    )
    main = _run_cue(
        runtime,
        parameters,
        cue_unit_id=parameters.main_path[0],
        start_ms=100.0 + parameters.episode_spacing_ms,
        event_id="chain:main",
    )
    return (
        main,
        control,
        len(runtime.intervention_records),
        runtime.ledger.external_observation_count,
        runtime.ledger.committed_positive_updates,
    )


def _autonomous_chain(
    parameters: PrimaryWorldParameters,
) -> tuple[bool, dict[str, float]]:
    sham = _run_two_chain_condition(parameters)
    targeted = _run_two_chain_condition(
        parameters,
        EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.main_path[1],)
        ),
    )
    matched = _run_two_chain_condition(
        parameters,
        EndogenousChainIntervention(
            suppress_expansion_unit_ids=(parameters.control_path[1],)
        ),
    )
    sham_downstream = sum(unit_id in parameters.main_path[2:] for unit_id in sham[0])
    targeted_downstream = sum(
        unit_id in parameters.main_path[2:] for unit_id in targeted[0]
    )
    matched_downstream = sum(
        unit_id in parameters.main_path[2:] for unit_id in matched[0]
    )
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    passed = (
        sham[0] == parameters.main_path[1:]
        and sham[1] == parameters.control_path[1:]
        and targeted[0] == (parameters.main_path[1],)
        and matched[0] == parameters.main_path[1:]
        and targeted[2] == 1
        and matched[2] == 1
        and targeted_impairment - matched_impairment >= 0.5
        and all(row[4] == 0 for row in (sham, targeted, matched))
    )
    return (
        passed,
        {
            "chain_sham_downstream": float(sham_downstream),
            "chain_targeted_impairment": targeted_impairment,
            "chain_matched_impairment": matched_impairment,
        },
    )


def _closed_loop_components(
    parameters: PrimaryWorldParameters,
    *,
    boundary_intervention: BoundaryIntervention | None = None,
    suppress_world: bool = False,
) -> tuple[
    AutonomousEndogenousChainRuntime,
    AnonymousBoundaryEmitter,
    AnonymousBoundaryWorld,
    UntypedBoundaryConsistency,
]:
    runtime = _runtime(parameters, (parameters.main_path, parameters.control_path))
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
    world_intervention = None
    if suppress_world:
        world_intervention = WorldBoundaryIntervention(
            suppressed_port_ids=(parameters.main_port, parameters.control_port)
        )
    world = AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id=parameters.main_port,
                target=f"unit:{parameters.old_target}",
                lag_ms=parameters.boundary_lag_ms,
                magnitude=1.0,
            ),
            AnonymousWorldLink(
                port_id=parameters.control_port,
                target=f"unit:{parameters.new_target}",
                lag_ms=parameters.boundary_lag_ms,
                magnitude=1.0,
            ),
        ),
        intervention=world_intervention,
    )
    consistency = UntypedBoundaryConsistency(
        runtime.ledger,
        AnonymousConsistencyConfig(
            maximum_pair_lag_ms=parameters.boundary_lag_ms + 5.0,
            pending_ttl_ms=parameters.boundary_lag_ms + 15.0,
        ),
    )
    return runtime, emitter, world, consistency


def _run_episode(
    runtime: AutonomousEndogenousChainRuntime,
    emitter: AnonymousBoundaryEmitter,
    world: AnonymousBoundaryWorld,
    consistency: UntypedBoundaryConsistency,
    parameters: PrimaryWorldParameters,
    *,
    cue_unit_id: int,
    start_ms: float,
    episode_id: str,
) -> None:
    before = len(runtime.generated_sparks)
    runtime.present_external(
        _pulse(f"cue:{episode_id}", start_ms, cue_unit_id, parameters)
    )
    runtime.advance_silence(
        start_ms + parameters.transition_lag_ms * 4.0
    )
    sparks = tuple(runtime.generated_sparks[before:])
    events = emitter.emit(sparks, source_state_hash=runtime.state_hash())
    for event in events:
        consistency.register_boundary(event)
        for external in world.receive(event):
            runtime.present_external(external)
            consistency.observe_external(external)


def _run_boundary_condition(
    parameters: PrimaryWorldParameters,
    *,
    suppressed_port: str | None = None,
    suppress_world: bool = False,
) -> dict[str, Any]:
    intervention = None
    if suppressed_port is not None:
        intervention = BoundaryIntervention(suppressed_port_ids=(suppressed_port,))
    runtime, emitter, world, consistency = _closed_loop_components(
        parameters,
        boundary_intervention=intervention,
        suppress_world=suppress_world,
    )
    for episode in range(3):
        base = 100.0 + episode * parameters.episode_spacing_ms * 2.0
        _run_episode(
            runtime,
            emitter,
            world,
            consistency,
            parameters,
            cue_unit_id=parameters.control_path[0],
            start_ms=base,
            episode_id=f"control:{episode}",
        )
        _run_episode(
            runtime,
            emitter,
            world,
            consistency,
            parameters,
            cue_unit_id=parameters.main_path[0],
            start_ms=base + parameters.episode_spacing_ms,
            episode_id=f"main:{episode}",
        )
    consistency.expire(runtime.field.current_time_ms + 100.0)
    ports = tuple(event.port_id for event in emitter.events)
    targets = tuple(event.target for event in world.external_events)
    main_link = consistency.link_state(
        port_id=parameters.main_port,
        target=f"unit:{parameters.old_target}",
    )
    primary_state = {
        "boundary": emitter.state_dict(),
        "chain": runtime.state_dict(),
        "consistency": consistency.state_dict(),
    }
    return {
        "main_terminal_count": sum(
            row.unit_id == parameters.main_path[-1]
            for row in runtime.generated_sparks
        ),
        "control_terminal_count": sum(
            row.unit_id == parameters.control_path[-1]
            for row in runtime.generated_sparks
        ),
        "main_boundary_count": ports.count(parameters.main_port),
        "control_boundary_count": ports.count(parameters.control_port),
        "main_external_count": targets.count(f"unit:{parameters.old_target}"),
        "control_external_count": targets.count(f"unit:{parameters.new_target}"),
        "main_consistent_count": (
            main_link.consistent_count if main_link is not None else 0
        ),
        "main_reliability": consistency.reliability(
            port_id=parameters.main_port,
            target=f"unit:{parameters.old_target}",
        ),
        "link_count": len(consistency.learned_state_dict()["links"]),
        "committed_positive_updates": runtime.ledger.committed_positive_updates,
        "primary_state": primary_state,
    }


def _boundary_and_stabilization(
    parameters: PrimaryWorldParameters,
) -> tuple[bool, bool, bool, dict[str, float]]:
    sham = _run_boundary_condition(parameters)
    targeted = _run_boundary_condition(
        parameters,
        suppressed_port=parameters.main_port,
    )
    matched = _run_boundary_condition(
        parameters,
        suppressed_port=parameters.control_port,
    )
    internal_only = _run_boundary_condition(parameters, suppress_world=True)
    denominator = max(1, int(sham["main_boundary_count"]))
    targeted_impairment = 1.0 - int(targeted["main_boundary_count"]) / denominator
    matched_impairment = 1.0 - int(matched["main_boundary_count"]) / denominator
    boundary_passed = (
        sham["main_boundary_count"] == 3
        and sham["main_external_count"] == 3
        and targeted["main_terminal_count"] == sham["main_terminal_count"]
        and targeted["main_boundary_count"] == 0
        and targeted["main_external_count"] == 0
        and matched["main_boundary_count"] == 3
        and matched["main_external_count"] == 3
        and targeted_impairment - matched_impairment >= 0.5
    )
    stabilization_passed = (
        sham["main_consistent_count"] == 3
        and sham["main_reliability"] is not None
        and float(sham["main_reliability"]) > 0.5
        and internal_only["main_boundary_count"] == 3
        and internal_only["main_external_count"] == 0
        and internal_only["link_count"] == 0
        and internal_only["committed_positive_updates"] == 0
    )
    taxonomy_hash = verify_taxonomy_variant_runtime_equality(
        {
            "view-alpha": sham["primary_state"],
            "renamed-view": sham["primary_state"],
        }
    )
    taxonomy_passed = len(taxonomy_hash) == 64
    return (
        boundary_passed,
        stabilization_passed,
        taxonomy_passed,
        {
            "boundary_targeted_impairment": targeted_impairment,
            "boundary_matched_impairment": matched_impairment,
            "relation_acquired_reliability": float(sham["main_reliability"] or 0.0),
        },
    )


def _main_only_components(
    parameters: PrimaryWorldParameters,
) -> tuple[
    AutonomousEndogenousChainRuntime,
    AnonymousBoundaryEmitter,
    UntypedBoundaryConsistency,
]:
    runtime = _runtime(parameters, (parameters.main_path,))
    emitter = AnonymousBoundaryEmitter(
        (
            BoundaryCoupling(
                source_unit_id=parameters.main_path[-1],
                port_id=parameters.main_port,
            ),
        )
    )
    consistency = UntypedBoundaryConsistency(
        runtime.ledger,
        AnonymousConsistencyConfig(
            maximum_pair_lag_ms=parameters.boundary_lag_ms + 5.0,
            pending_ttl_ms=parameters.boundary_lag_ms + 15.0,
        ),
    )
    return runtime, emitter, consistency


def _phase(
    runtime: AutonomousEndogenousChainRuntime,
    emitter: AnonymousBoundaryEmitter,
    consistency: UntypedBoundaryConsistency,
    parameters: PrimaryWorldParameters,
    *,
    target_unit_id: int,
    start_episode: int,
    count: int,
) -> None:
    world = AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id=parameters.main_port,
                target=f"unit:{target_unit_id}",
                lag_ms=parameters.boundary_lag_ms,
                magnitude=1.0,
            ),
        )
    )
    for local_index in range(count):
        episode = start_episode + local_index
        _run_episode(
            runtime,
            emitter,
            world,
            consistency,
            parameters,
            cue_unit_id=parameters.main_path[0],
            start_ms=100.0 + episode * parameters.episode_spacing_ms,
            episode_id=f"phase:{target_unit_id}:{episode}",
        )


def _link_reliability(
    consistency: UntypedBoundaryConsistency,
    parameters: PrimaryWorldParameters,
    target_unit_id: int,
) -> float | None:
    return consistency.reliability(
        port_id=parameters.main_port,
        target=f"unit:{target_unit_id}",
    )


def _revision_states(
    parameters: PrimaryWorldParameters,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], bool, dict[str, float]]:
    runtime, emitter, consistency = _main_only_components(parameters)
    _phase(
        runtime,
        emitter,
        consistency,
        parameters,
        target_unit_id=parameters.old_target,
        start_episode=0,
        count=3,
    )
    acquired = consistency.learned_state_dict()
    acquired_old = _link_reliability(
        consistency, parameters, parameters.old_target
    )
    _phase(
        runtime,
        emitter,
        consistency,
        parameters,
        target_unit_id=parameters.new_target,
        start_episode=3,
        count=3,
    )
    reversed_state = consistency.learned_state_dict()
    reversed_old = _link_reliability(
        consistency, parameters, parameters.old_target
    )
    reversed_new = _link_reliability(
        consistency, parameters, parameters.new_target
    )
    _phase(
        runtime,
        emitter,
        consistency,
        parameters,
        target_unit_id=parameters.old_target,
        start_episode=6,
        count=3,
    )
    returned = consistency.learned_state_dict()
    returned_old = _link_reliability(
        consistency, parameters, parameters.old_target
    )
    returned_new = _link_reliability(
        consistency, parameters, parameters.new_target
    )

    stable_runtime, stable_emitter, stable_consistency = _main_only_components(parameters)
    _phase(
        stable_runtime,
        stable_emitter,
        stable_consistency,
        parameters,
        target_unit_id=parameters.old_target,
        start_episode=0,
        count=9,
    )
    stable_links = stable_consistency.learned_state_dict()["links"]
    passed = (
        acquired_old is not None
        and acquired_old > 0.5
        and reversed_old is not None
        and reversed_new is not None
        and reversed_new > reversed_old
        and returned_old is not None
        and returned_new is not None
        and returned_old > returned_new
        and len(stable_links) == 1
        and runtime.ledger.committed_positive_updates == 0
        and stable_runtime.ledger.committed_positive_updates == 0
    )
    return (
        acquired,
        reversed_state,
        returned,
        passed,
        {
            "revision_acquired_old": float(acquired_old or 0.0),
            "revision_reversed_old": float(reversed_old or 0.0),
            "revision_reversed_new": float(reversed_new or 0.0),
            "revision_returned_old": float(returned_old or 0.0),
            "revision_returned_new": float(returned_new or 0.0),
        },
    )


def _probe_boundary(
    parameters: PrimaryWorldParameters,
    *,
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
        source_state_hash=digest(parameters.state_dict()),
    )


def _run_reentry_state(
    parameters: PrimaryWorldParameters,
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
            maximum_effective_current=2.0,
            maximum_generation_depth=6,
        ),
    )
    reentry = AnonymousRelationReentry(
        consistency,
        ledger,
        gate,
        RelationReentryConfig(
            delay_ms=1.0,
            magnitude_gain=parameters.relation_reentry_gain,
            maximum_magnitude=2.0,
            minimum_consistent_count=1,
            minimum_reliability=0.0,
        ),
    )
    reentry.schedule(
        _probe_boundary(parameters, event_id=event_id),
        field,
    )
    spikes = field.run_until(102.0)
    return tuple(spike.unit_id for spike in spikes)


def _relation_reentry_and_persistence(
    parameters: PrimaryWorldParameters,
    acquired: dict[str, Any],
    reversed_state: dict[str, Any],
    returned: dict[str, Any],
) -> tuple[bool, bool, dict[str, float]]:
    acquired_units = _run_reentry_state(
        parameters, acquired, event_id="reentry:acquired"
    )
    reversed_units = _run_reentry_state(
        parameters, reversed_state, event_id="reentry:reversed"
    )
    returned_units = _run_reentry_state(
        parameters, returned, event_id="reentry:returned"
    )
    reset_consistency = {
        "config": acquired["config"],
        "links": {},
    }
    reset_units = _run_reentry_state(
        parameters,
        reset_consistency,
        event_id="reentry:reset",
    )

    donor_expectation = _expectation(parameters, (parameters.main_path,))
    donor_state = donor_expectation.learned_state_dict()
    local_transplant = _run_local_transplant(parameters, donor_state)
    empty_state = {
        "config": donor_state["config"],
        "external_transition_count": 0,
        "transitions": {},
    }
    local_reset = _run_local_transplant(parameters, empty_state)

    reentry_passed = (
        acquired_units == (parameters.old_target,)
        and reversed_units == (parameters.new_target,)
        and returned_units == (parameters.old_target,)
        and reset_units == ()
    )
    persistence_passed = (
        local_transplant == (parameters.main_path[1],)
        and local_reset == ()
        and acquired_units == (parameters.old_target,)
        and reset_units == ()
    )
    return (
        reentry_passed,
        persistence_passed,
        {
            "reentry_acquired_generated_count": float(len(acquired_units)),
            "reentry_reversed_generated_count": float(len(reversed_units)),
            "persistence_local_transplant_count": float(len(local_transplant)),
            "persistence_local_reset_count": float(len(local_reset)),
        },
    )


def _run_local_transplant(
    parameters: PrimaryWorldParameters,
    learned_state: dict[str, Any],
) -> tuple[int, ...]:
    field = _field(parameters)
    current = _pulse(
        "persistence:current",
        100.0,
        parameters.main_path[0],
        parameters,
    )
    ledger = ProvenanceLedger()
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
    field.run_until(100.0)
    model = LocalTemporalExpectation.from_learned_state_dict(learned_state)
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            maximum_effective_current=2.0,
        ),
    )
    origin_state_hash = digest(
        {
            "field": field.state_dict(),
            "local_transition": learned_state,
        }
    )
    for proposal in model.proposals_for(
        current,
        origin_state_hash=origin_state_hash,
    ):
        ledger.register_proposal(proposal)
        gate.schedule(proposal, field)
    spikes = field.run_until(100.0 + parameters.transition_lag_ms + 1.0)
    return tuple(spike.unit_id for spike in spikes)


def evaluate_primary_world(
    family_id: str,
    seed: int,
) -> PrimaryWorldEvidence:
    parameters = world_parameters(family_id, seed)
    origin, state, origin_metrics = _state_and_origin(parameters)
    chain, chain_metrics = _autonomous_chain(parameters)
    boundary, stabilization, taxonomy, boundary_metrics = (
        _boundary_and_stabilization(parameters)
    )
    acquired, reversed_state, returned, revision, revision_metrics = (
        _revision_states(parameters)
    )
    reentry, persistence, reentry_metrics = _relation_reentry_and_persistence(
        parameters,
        acquired,
        reversed_state,
        returned,
    )
    metrics = tuple(
        sorted(
            {
                **origin_metrics,
                **chain_metrics,
                **boundary_metrics,
                **revision_metrics,
                **reentry_metrics,
                "transition_lag_ms": parameters.transition_lag_ms,
                "boundary_lag_ms": parameters.boundary_lag_ms,
                "threshold": parameters.threshold,
            }.items()
        )
    )
    return PrimaryWorldEvidence(
        family_id=family_id,
        seed=seed,
        endogenous_origin_passed=origin,
        state_dependence_passed=state,
        autonomous_chain_passed=chain,
        boundary_effect_passed=boundary,
        relation_stabilization_passed=stabilization,
        reversal_reacquisition_passed=revision,
        relation_reentry_passed=reentry,
        persistence_locus_passed=persistence,
        taxonomy_non_interference_passed=taxonomy,
        metrics=metrics,
    )


def run_condition(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    evidence = evaluate_primary_world(family_id, seed)
    passed = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: evidence.endogenous_origin_passed,
        EvidenceDomain.STATE_DEPENDENCE: evidence.state_dependence_passed,
        EvidenceDomain.AUTONOMOUS_CHAIN: evidence.autonomous_chain_passed,
        EvidenceDomain.BOUNDARY_EFFECT: evidence.boundary_effect_passed,
        EvidenceDomain.RELATION_STABILIZATION: (
            evidence.relation_stabilization_passed
        ),
        EvidenceDomain.REVERSAL_REACQUISITION: (
            evidence.reversal_reacquisition_passed
        ),
        EvidenceDomain.RELATION_REENTRY: evidence.relation_reentry_passed,
        EvidenceDomain.PERSISTENCE_LOCUS: evidence.persistence_locus_passed,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: (
            evidence.taxonomy_non_interference_passed
        ),
    }
    return tuple(
        ConfirmatoryResultRecord(
            family_id=family_id,
            seed=seed,
            condition=ConfirmatoryCondition.PRIMARY,
            evidence_domain=domain,
            passed=passed[domain],
            metrics=evidence.metrics,
        )
        for domain in EvidenceDomain
    )


def run_primary_qualification_grid() -> PrimaryQualificationGrid:
    worlds = tuple(
        evaluate_primary_world(family_id, seed)
        for family_id in QUALIFICATION_FAMILIES
        for seed in QUALIFICATION_SEEDS
    )
    records = tuple(
        record
        for world in worlds
        for record in run_condition(world.family_id, world.seed)
    )
    return PrimaryQualificationGrid(worlds=worlds, records=records)

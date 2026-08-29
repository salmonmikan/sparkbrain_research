from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.boundary import (
    AnonymousBoundaryEmitter,
    BoundaryCoupling,
    BoundaryEvent,
    BoundaryIntervention,
)
from sparkbrain.v06.consistency import (
    AnonymousConsistencyConfig,
    UntypedBoundaryConsistency,
)
from sparkbrain.v06.endogenous_chain import AutonomousEndogenousChainRuntime
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse, digest
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.world_boundary import (
    AnonymousBoundaryWorld,
    AnonymousWorldLink,
    WorldBoundaryIntervention,
)


@dataclass(frozen=True, slots=True)
class BoundaryProbeCondition:
    condition_id: str
    main_internal_terminal_count: int
    control_internal_terminal_count: int
    boundary_port_ids: tuple[str, ...]
    external_targets: tuple[str, ...]
    main_boundary_count: int
    control_boundary_count: int
    main_external_count: int
    control_external_count: int
    main_link_consistent_count: int
    control_link_consistent_count: int
    main_link_reliability: float | None
    control_link_reliability: float | None
    external_observation_count: int
    committed_positive_updates: int
    boundary_suppression_count: int
    world_suppression_count: int
    primary_state_hash: str
    primary_state: dict[str, Any]
    world_state: dict[str, Any]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BoundaryProbeAssessment:
    sham_main_boundary_count: int
    targeted_main_boundary_count: int
    matched_random_main_boundary_count: int
    targeted_boundary_impairment: float
    matched_random_boundary_impairment: float
    selective_boundary_effect: float
    targeted_main_chain_preserved: bool
    sham_main_external_count: int
    targeted_main_external_count: int
    matched_random_main_external_count: int
    main_external_stream_selective_effect: float
    externally_stabilized_main_link: bool
    internal_only_boundary_count: int
    internal_only_link_count: int
    internal_only_positive_updates: int
    taxonomy_projection_hash_unchanged: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalBoundarySuite:
    sham: BoundaryProbeCondition
    targeted_port_suppression: BoundaryProbeCondition
    matched_random_port_suppression: BoundaryProbeCondition
    internal_only: BoundaryProbeCondition
    assessment: BoundaryProbeAssessment
    projection_a: dict[str, Any]
    projection_b: dict[str, Any]

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "internal_only": self.internal_only.state_dict(),
            "matched_random_port_suppression": (
                self.matched_random_port_suppression.state_dict()
            ),
            "projection_a": self.projection_a,
            "projection_b": self.projection_b,
            "sham": self.sham.state_dict(),
            "targeted_port_suppression": self.targeted_port_suppression.state_dict(),
        }


def pulse(event_id: str, time_ms: float, unit_id: int) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _train_chain(
    expectation: LocalTemporalExpectation,
    *,
    unit_ids: tuple[int, ...],
    prefix: str,
) -> None:
    for episode, offset in enumerate((0.0, 25.0, 50.0)):
        rows = tuple(
            pulse(f"{prefix}-{episode}-{index}", offset + index * 5.0, unit_id)
            for index, unit_id in enumerate(unit_ids)
        )
        for source, target in zip(rows, rows[1:], strict=False):
            expectation.observe_external_transition(source, target)


def _build_primary(
    *,
    boundary_intervention: BoundaryIntervention | None = None,
    world_intervention: WorldBoundaryIntervention | None = None,
) -> tuple[
    AutonomousEndogenousChainRuntime,
    AnonymousBoundaryEmitter,
    AnonymousBoundaryWorld,
    UntypedBoundaryConsistency,
]:
    expectation = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=25.0,
        )
    )
    _train_chain(expectation, unit_ids=(0, 1, 2, 3), prefix="main")
    _train_chain(expectation, unit_ids=(4, 5, 6, 7), prefix="control")
    topology = explicit_topology(
        tuple(
            UnitState(unit_id=unit_id, x=float(unit_id), y=0.0, base_threshold=0.5)
            for unit_id in range(10)
        ),
        (),
        receptor_ids=tuple(range(10)),
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=2.0,
        ),
    )
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.1,
            maximum_effective_current=2.0,
            maximum_generation_depth=4,
            maximum_proposals_per_window=16,
            maximum_branches_per_origin_state=4,
        ),
    )
    runtime = AutonomousEndogenousChainRuntime(
        field,
        expectation,
        transition,
        reinjection,
    )
    emitter = AnonymousBoundaryEmitter(
        (
            BoundaryCoupling(source_unit_id=3, port_id="port:7"),
            BoundaryCoupling(source_unit_id=7, port_id="port:9"),
        ),
        intervention=boundary_intervention,
    )
    world = AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id="port:7",
                target="unit:8",
                lag_ms=10.0,
                magnitude=1.0,
            ),
            AnonymousWorldLink(
                port_id="port:9",
                target="unit:9",
                lag_ms=10.0,
                magnitude=1.0,
            ),
        ),
        intervention=world_intervention,
    )
    consistency = UntypedBoundaryConsistency(
        ledger,
        AnonymousConsistencyConfig(
            maximum_pair_lag_ms=20.0,
            pending_ttl_ms=30.0,
        ),
    )
    return runtime, emitter, world, consistency


def _run_episode(
    runtime: AutonomousEndogenousChainRuntime,
    emitter: AnonymousBoundaryEmitter,
    world: AnonymousBoundaryWorld,
    consistency: UntypedBoundaryConsistency,
    *,
    cue_unit_id: int,
    start_ms: float,
    episode_id: str,
) -> None:
    before = len(runtime.generated_sparks)
    runtime.present_external(pulse(f"cue:{episode_id}", start_ms, cue_unit_id))
    runtime.advance_silence(start_ms + 20.0)
    sparks = tuple(runtime.generated_sparks[before:])
    boundary_events = emitter.emit(
        sparks,
        source_state_hash=runtime.state_hash(),
    )
    for event in boundary_events:
        consistency.register_boundary(event)
        for external in world.receive(event):
            runtime.present_external(external)
            consistency.observe_external(external)
    consistency.expire(start_ms + 45.0)


def run_boundary_condition(
    condition_id: str,
    *,
    boundary_intervention: BoundaryIntervention | None = None,
    world_intervention: WorldBoundaryIntervention | None = None,
    repetitions: int = 3,
) -> BoundaryProbeCondition:
    runtime, emitter, world, consistency = _build_primary(
        boundary_intervention=boundary_intervention,
        world_intervention=world_intervention,
    )
    for episode in range(repetitions):
        base = 100.0 + episode * 120.0
        _run_episode(
            runtime,
            emitter,
            world,
            consistency,
            cue_unit_id=4,
            start_ms=base,
            episode_id=f"{condition_id}:control:{episode}",
        )
        _run_episode(
            runtime,
            emitter,
            world,
            consistency,
            cue_unit_id=0,
            start_ms=base + 50.0,
            episode_id=f"{condition_id}:main:{episode}",
        )
    runtime.advance_silence(100.0 + repetitions * 120.0)
    consistency.expire(runtime.field.current_time_ms + 50.0)

    boundary_ports = tuple(event.port_id for event in emitter.events)
    external_targets = tuple(event.target for event in world.external_events)
    main_state = consistency.link_state(port_id="port:7", target="unit:8")
    control_state = consistency.link_state(port_id="port:9", target="unit:9")
    primary_state = {
        "boundary": emitter.state_dict(),
        "chain": runtime.state_dict(),
        "consistency": consistency.state_dict(),
    }
    return BoundaryProbeCondition(
        condition_id=condition_id,
        main_internal_terminal_count=sum(
            spark.unit_id == 3 for spark in runtime.generated_sparks
        ),
        control_internal_terminal_count=sum(
            spark.unit_id == 7 for spark in runtime.generated_sparks
        ),
        boundary_port_ids=boundary_ports,
        external_targets=external_targets,
        main_boundary_count=boundary_ports.count("port:7"),
        control_boundary_count=boundary_ports.count("port:9"),
        main_external_count=external_targets.count("unit:8"),
        control_external_count=external_targets.count("unit:9"),
        main_link_consistent_count=(
            main_state.consistent_count if main_state is not None else 0
        ),
        control_link_consistent_count=(
            control_state.consistent_count if control_state is not None else 0
        ),
        main_link_reliability=consistency.reliability(
            port_id="port:7",
            target="unit:8",
        ),
        control_link_reliability=consistency.reliability(
            port_id="port:9",
            target="unit:9",
        ),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
        boundary_suppression_count=len(emitter.suppressions),
        world_suppression_count=len(world.suppressed_boundary_event_ids),
        primary_state_hash=digest(primary_state),
        primary_state=primary_state,
        world_state=world.state_dict(),
    )


def project_boundary_view(
    events: tuple[BoundaryEvent, ...],
    labels: dict[str, str],
) -> dict[str, Any]:
    """Post-hoc view whose names cannot affect Primary runtime state."""

    return {
        "rows": [
            {
                "event_id": event.event_id,
                "port_description": labels.get(event.port_id, event.port_id),
                "port_id": event.port_id,
                "source_spark_id": event.source_spark_id,
                "time_ms": event.time_ms,
            }
            for event in events
        ]
    }


def run_canonical_boundary_suite() -> CanonicalBoundarySuite:
    sham = run_boundary_condition("sham")
    targeted = run_boundary_condition(
        "targeted-port",
        boundary_intervention=BoundaryIntervention(
            suppressed_port_ids=("port:7",)
        ),
    )
    matched_random = run_boundary_condition(
        "matched-random-port",
        boundary_intervention=BoundaryIntervention(
            suppressed_port_ids=("port:9",)
        ),
    )
    internal_only = run_boundary_condition(
        "internal-only",
        world_intervention=WorldBoundaryIntervention(
            suppressed_port_ids=("port:7", "port:9")
        ),
    )

    denominator = max(1, sham.main_boundary_count)
    targeted_impairment = 1.0 - targeted.main_boundary_count / denominator
    random_impairment = 1.0 - matched_random.main_boundary_count / denominator
    external_selective_effect = (
        sham.main_external_count
        - targeted.main_external_count
        - (sham.main_external_count - matched_random.main_external_count)
    ) / max(1, sham.main_external_count)

    emitter_events = tuple(
        BoundaryEvent(
            event_id=row["event_id"],
            time_ms=row["time_ms"],
            port_id=row["port_id"],
            magnitude=row["magnitude"],
            polarity=row["polarity"],
            direction=row["direction"],
            source_spark_id=row["source_spark_id"],
            source_unit_id=row["source_unit_id"],
            source_proposal_ids=tuple(row["source_proposal_ids"]),
            generation_depth=row["generation_depth"],
            source_state_hash=row["source_state_hash"],
        )
        for row in sham.primary_state["boundary"]["events"]
    )
    before_projection = sham.primary_state_hash
    projection_a = project_boundary_view(
        emitter_events,
        {"port:7": "view-alpha", "port:9": "view-beta"},
    )
    projection_b = project_boundary_view(
        emitter_events,
        {"port:7": "view-beta", "port:9": "view-alpha"},
    )
    taxonomy_unchanged = before_projection == digest(sham.primary_state)

    internal_links = internal_only.primary_state["consistency"]["links"]
    assessment = BoundaryProbeAssessment(
        sham_main_boundary_count=sham.main_boundary_count,
        targeted_main_boundary_count=targeted.main_boundary_count,
        matched_random_main_boundary_count=matched_random.main_boundary_count,
        targeted_boundary_impairment=targeted_impairment,
        matched_random_boundary_impairment=random_impairment,
        selective_boundary_effect=targeted_impairment - random_impairment,
        targeted_main_chain_preserved=(
            targeted.main_internal_terminal_count
            == sham.main_internal_terminal_count
        ),
        sham_main_external_count=sham.main_external_count,
        targeted_main_external_count=targeted.main_external_count,
        matched_random_main_external_count=matched_random.main_external_count,
        main_external_stream_selective_effect=external_selective_effect,
        externally_stabilized_main_link=(
            sham.main_link_consistent_count == 3
            and sham.main_link_reliability is not None
            and sham.main_link_reliability > 0.5
        ),
        internal_only_boundary_count=internal_only.main_boundary_count,
        internal_only_link_count=len(internal_links),
        internal_only_positive_updates=internal_only.committed_positive_updates,
        taxonomy_projection_hash_unchanged=taxonomy_unchanged,
        engineering_candidate=(
            sham.main_boundary_count == 3
            and sham.main_external_count == 3
            and targeted.main_boundary_count == 0
            and targeted.main_external_count == 0
            and matched_random.main_boundary_count == 3
            and matched_random.main_external_count == 3
            and targeted.main_internal_terminal_count
            == sham.main_internal_terminal_count
            and targeted_impairment > random_impairment
            and external_selective_effect > 0
            and sham.main_link_consistent_count == 3
            and sham.main_link_reliability is not None
            and sham.main_link_reliability > 0.5
            and internal_only.main_boundary_count == 3
            and not internal_links
            and internal_only.committed_positive_updates == 0
            and taxonomy_unchanged
        ),
    )
    return CanonicalBoundarySuite(
        sham=sham,
        targeted_port_suppression=targeted,
        matched_random_port_suppression=matched_random,
        internal_only=internal_only,
        assessment=assessment,
        projection_a=projection_a,
        projection_b=projection_b,
    )

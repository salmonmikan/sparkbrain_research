from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.boundary import BoundaryDirection, BoundaryEvent
from sparkbrain.v06.consistency import (
    AnonymousConsistencyConfig,
    UntypedBoundaryConsistency,
)
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse, digest
from sparkbrain.v06.local_expectation import (
    LocalExpectationConfig,
    LocalTemporalExpectation,
)
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.relation_reentry import (
    AnonymousRelationReentry,
    RelationReentryConfig,
)


@dataclass(frozen=True, slots=True)
class LocalTransitionLocusResult:
    donor_learned_state_hash: str
    transplanted_generated_units: tuple[int, ...]
    reset_generated_units: tuple[int, ...]
    field_only_generated_units: tuple[int, ...]
    unrelated_generated_units: tuple[int, ...]
    transplanted_field_before_hash: str
    reset_field_before_hash: str
    field_only_field_before_hash: str
    unrelated_field_before_hash: str
    transplanted_external_observation_count: int
    transplanted_positive_updates: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ConsistencyLocusResult:
    donor_learned_state_hash: str
    transplanted_generated_units: tuple[int, ...]
    reset_generated_units: tuple[int, ...]
    unrelated_port_generated_units: tuple[int, ...]
    alternate_target_generated_units: tuple[int, ...]
    transplanted_field_before_hash: str
    reset_field_before_hash: str
    unrelated_field_before_hash: str
    alternate_field_before_hash: str
    transplanted_external_observation_count: int
    transplanted_positive_updates: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PersistenceLocusAssessment:
    local_transition_reset_removes_effect: bool
    local_transition_transplant_moves_effect: bool
    local_unrelated_state_redirects_effect: bool
    field_state_alone_does_not_transfer_local_effect: bool
    consistency_reset_removes_effect: bool
    consistency_transplant_moves_effect: bool
    unrelated_consistency_does_not_transfer_target_effect: bool
    alternate_consistency_redirects_effect: bool
    recipient_field_states_matched: bool
    no_positive_self_confirmation: bool
    explicit_state_dominant_candidate: bool
    distributed_field_persistence_supported: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalPersistenceLocusSuite:
    local_transition: LocalTransitionLocusResult
    consistency: ConsistencyLocusResult
    assessment: PersistenceLocusAssessment

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "consistency": self.consistency.state_dict(),
            "local_transition": self.local_transition.state_dict(),
        }


def _field(unit_ids: tuple[int, ...]) -> TemporalExcitableField:
    topology = explicit_topology(
        tuple(
            UnitState(unit_id=unit_id, x=float(unit_id), y=0.0, base_threshold=0.5)
            for unit_id in unit_ids
        ),
        (),
        receptor_ids=unit_ids,
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=2.0,
        ),
    )


def _external(event_id: str, time_ms: float, target: str) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=target,
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _train_local_state(target: str) -> dict[str, Any]:
    model = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=20.0,
        )
    )
    for index, time_ms in enumerate((0.0, 20.0, 40.0)):
        model.observe_external_transition(
            _external(f"local-source:{target}:{index}", time_ms, "unit:0"),
            _external(f"local-target:{target}:{index}", time_ms + 5.0, target),
        )
    return model.learned_state_dict()


def _field_after_current() -> tuple[TemporalExcitableField, RuntimePulse, ProvenanceLedger]:
    field = _field((0, 1, 2))
    current = _external("current", 100.0, "unit:0")
    ledger = ProvenanceLedger()
    ledger.register_external(current)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=current.time_ms,
            target_id=0,
            current=current.magnitude,
            source_id=None,
            pulse_id=current.event_id,
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    field.run_until(current.time_ms)
    return field, current, ledger


def _run_local_state(
    model: LocalTemporalExpectation,
    *,
    field_state: dict[str, Any] | None = None,
) -> tuple[tuple[int, ...], str, int, int]:
    if field_state is None:
        field, current, ledger = _field_after_current()
    else:
        field = TemporalExcitableField.from_state_dict(field_state)
        current = _external("current", 100.0, "unit:0")
        ledger = ProvenanceLedger()
        ledger.register_external(current)
    field_before_hash = field.state_hash()
    origin_state_hash = digest(
        {
            "field": field.state_dict(),
            "local_transition": model.learned_state_dict(),
        }
    )
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.1,
            maximum_effective_current=2.0,
        ),
    )
    for proposal in model.proposals_for(
        current,
        origin_state_hash=origin_state_hash,
    ):
        ledger.register_proposal(proposal)
        gate.schedule(proposal, field)
    spikes = field.run_until(106.0)
    generated_units = tuple(
        spike.unit_id for spike in spikes if spike.time_ms > current.time_ms
    )
    return (
        generated_units,
        field_before_hash,
        ledger.external_observation_count,
        ledger.committed_positive_updates,
    )


def run_local_transition_locus() -> LocalTransitionLocusResult:
    donor_state = _train_local_state("unit:1")
    transplanted = LocalTemporalExpectation.from_learned_state_dict(donor_state)
    reset = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=0.1,
            proposal_ttl_ms=20.0,
        )
    )
    unrelated = LocalTemporalExpectation.from_learned_state_dict(
        _train_local_state("unit:2")
    )

    donor_field, _, _ = _field_after_current()
    donor_field_state = donor_field.state_dict()
    transplanted_run = _run_local_state(transplanted)
    reset_run = _run_local_state(reset)
    field_only_run = _run_local_state(
        LocalTemporalExpectation.from_learned_state_dict(
            reset.learned_state_dict()
        ),
        field_state=donor_field_state,
    )
    unrelated_run = _run_local_state(unrelated)
    return LocalTransitionLocusResult(
        donor_learned_state_hash=digest(donor_state),
        transplanted_generated_units=transplanted_run[0],
        reset_generated_units=reset_run[0],
        field_only_generated_units=field_only_run[0],
        unrelated_generated_units=unrelated_run[0],
        transplanted_field_before_hash=transplanted_run[1],
        reset_field_before_hash=reset_run[1],
        field_only_field_before_hash=field_only_run[1],
        unrelated_field_before_hash=unrelated_run[1],
        transplanted_external_observation_count=transplanted_run[2],
        transplanted_positive_updates=transplanted_run[3],
    )


def _boundary(event_id: str, *, port_id: str = "port:7") -> BoundaryEvent:
    return BoundaryEvent(
        event_id=event_id,
        time_ms=100.0,
        port_id=port_id,
        magnitude=1.0,
        polarity=1,
        direction=BoundaryDirection.FIELD_TO_WORLD,
        source_spark_id=f"spark:{event_id}",
        source_unit_id=3,
        source_proposal_ids=(f"proposal:{event_id}",),
        generation_depth=3,
        source_state_hash=digest({"boundary": event_id}),
    )


def _train_consistency_state(
    *,
    port_id: str,
    target: str,
) -> dict[str, Any]:
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency(
        ledger,
        AnonymousConsistencyConfig(
            maximum_pair_lag_ms=20.0,
            pending_ttl_ms=30.0,
        ),
    )
    for index in range(3):
        boundary = BoundaryEvent(
            event_id=f"train-boundary:{port_id}:{target}:{index}",
            time_ms=index * 20.0,
            port_id=port_id,
            magnitude=1.0,
            polarity=1,
            direction=BoundaryDirection.FIELD_TO_WORLD,
            source_spark_id=f"train-spark:{index}",
            source_unit_id=3,
            source_proposal_ids=(f"train-proposal:{index}",),
            generation_depth=3,
            source_state_hash=digest({"training": index}),
        )
        consistency.register_boundary(boundary)
        external = RuntimePulse(
            event_id=f"train-external:{port_id}:{target}:{index}",
            time_ms=boundary.time_ms + 10.0,
            target=target,
            magnitude=1.0,
            polarity=1,
            origin=EventOrigin.EXTERNAL,
            parent_event_ids=(boundary.event_id,),
        )
        ledger.register_external(external)
        consistency.observe_external(external)
    return consistency.learned_state_dict()


def _run_consistency_state(
    learned_state: dict[str, Any],
    *,
    boundary_port_id: str = "port:7",
) -> tuple[tuple[int, ...], str, int, int]:
    field = _field((8, 9))
    field_before_hash = field.state_hash()
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
        ),
    )
    reentry = AnonymousRelationReentry(
        consistency,
        ledger,
        gate,
        RelationReentryConfig(
            delay_ms=1.0,
            magnitude_gain=0.9,
            maximum_magnitude=2.0,
            minimum_consistent_count=1,
            minimum_reliability=0.0,
        ),
    )
    reentry.schedule(_boundary("probe", port_id=boundary_port_id), field)
    spikes = field.run_until(102.0)
    return (
        tuple(spike.unit_id for spike in spikes),
        field_before_hash,
        ledger.external_observation_count,
        ledger.committed_positive_updates,
    )


def run_consistency_locus() -> ConsistencyLocusResult:
    donor_state = _train_consistency_state(
        port_id="port:7",
        target="unit:8",
    )
    config = donor_state["config"]
    reset_state = {"config": config, "links": {}}
    unrelated_state = _train_consistency_state(
        port_id="port:9",
        target="unit:9",
    )
    alternate_state = _train_consistency_state(
        port_id="port:7",
        target="unit:9",
    )
    transplanted = _run_consistency_state(donor_state)
    reset = _run_consistency_state(reset_state)
    unrelated = _run_consistency_state(unrelated_state)
    alternate = _run_consistency_state(alternate_state)
    return ConsistencyLocusResult(
        donor_learned_state_hash=digest(donor_state),
        transplanted_generated_units=transplanted[0],
        reset_generated_units=reset[0],
        unrelated_port_generated_units=unrelated[0],
        alternate_target_generated_units=alternate[0],
        transplanted_field_before_hash=transplanted[1],
        reset_field_before_hash=reset[1],
        unrelated_field_before_hash=unrelated[1],
        alternate_field_before_hash=alternate[1],
        transplanted_external_observation_count=transplanted[2],
        transplanted_positive_updates=transplanted[3],
    )


def run_canonical_persistence_locus_suite() -> CanonicalPersistenceLocusSuite:
    local = run_local_transition_locus()
    consistency = run_consistency_locus()
    field_hashes = {
        local.transplanted_field_before_hash,
        local.reset_field_before_hash,
        local.field_only_field_before_hash,
        local.unrelated_field_before_hash,
        consistency.transplanted_field_before_hash,
        consistency.reset_field_before_hash,
        consistency.unrelated_field_before_hash,
        consistency.alternate_field_before_hash,
    }
    no_positive = (
        local.transplanted_positive_updates == 0
        and consistency.transplanted_positive_updates == 0
    )
    assessment = PersistenceLocusAssessment(
        local_transition_reset_removes_effect=local.reset_generated_units == (),
        local_transition_transplant_moves_effect=(
            local.transplanted_generated_units == (1,)
        ),
        local_unrelated_state_redirects_effect=local.unrelated_generated_units == (2,),
        field_state_alone_does_not_transfer_local_effect=(
            local.field_only_generated_units == ()
        ),
        consistency_reset_removes_effect=consistency.reset_generated_units == (),
        consistency_transplant_moves_effect=(
            consistency.transplanted_generated_units == (8,)
        ),
        unrelated_consistency_does_not_transfer_target_effect=(
            consistency.unrelated_port_generated_units == ()
        ),
        alternate_consistency_redirects_effect=(
            consistency.alternate_target_generated_units == (9,)
        ),
        recipient_field_states_matched=len(field_hashes) == 2,
        no_positive_self_confirmation=no_positive,
        explicit_state_dominant_candidate=False,
        distributed_field_persistence_supported=False,
        engineering_candidate=False,
    )
    explicit = all(
        (
            assessment.local_transition_reset_removes_effect,
            assessment.local_transition_transplant_moves_effect,
            assessment.local_unrelated_state_redirects_effect,
            assessment.field_state_alone_does_not_transfer_local_effect,
            assessment.consistency_reset_removes_effect,
            assessment.consistency_transplant_moves_effect,
            assessment.unrelated_consistency_does_not_transfer_target_effect,
            assessment.alternate_consistency_redirects_effect,
            assessment.recipient_field_states_matched,
            assessment.no_positive_self_confirmation,
        )
    )
    assessment = PersistenceLocusAssessment(
        **{
            **assessment.state_dict(),
            "explicit_state_dominant_candidate": explicit,
            "engineering_candidate": explicit,
        }
    )
    return CanonicalPersistenceLocusSuite(
        local_transition=local,
        consistency=consistency,
        assessment=assessment,
    )

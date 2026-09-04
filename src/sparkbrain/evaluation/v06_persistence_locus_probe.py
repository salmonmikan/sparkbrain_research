from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.endogenous_chain import AutonomousEndogenousChainRuntime
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse, digest
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig

from .v06_relation_reentry_confirm import run_isolated_relation_reentry_suite


@dataclass(frozen=True, slots=True)
class TransitionCarrierCondition:
    condition_id: str
    transition_state_hash: str
    initial_field_state_hash: str
    initial_queue_size: int
    initial_g2_path_count: int
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    external_observation_count: int
    committed_positive_updates: int
    final_g2_path_count: int
    runtime_state_hash: str
    runtime_state: dict[str, Any]

    @property
    def root_generated(self) -> bool:
        return bool(self.generated_units) and self.generated_units[0] == 1

    @property
    def full_chain_generated(self) -> bool:
        return self.generated_units == (1, 2, 3)

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["full_chain_generated"] = self.full_chain_generated
        value["root_generated"] = self.root_generated
        return value


@dataclass(frozen=True, slots=True)
class TransitionTransplantReport:
    source_state_hash: str
    receiver_state_hash_before: str
    receiver_state_hash_after: str
    receiver_field_state_hash: str
    source_transition_count: int
    receiver_transition_count_before: int
    receiver_transition_count_after: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PersistenceLocusAssessment:
    g1_reset_removes_root: bool
    g1_reset_removes_full_chain: bool
    g1_transplant_transfers_root: bool
    g1_transplant_transfers_full_chain: bool
    receiver_field_is_naive_and_identical: bool
    pending_queue_not_persistent_carrier: bool
    g2_path_calibration_not_required: bool
    consistency_reset_removes_reentry: bool
    consistency_transplant_transfers_reentry: bool
    reentry_adapter_has_no_learned_state: bool
    explicit_transition_carrier_candidate: bool
    explicit_consistency_carrier_candidate: bool
    independent_field_carrier_supported: bool
    distributed_carrier_supported: bool
    limiting_interpretation_supported: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalPersistenceLocusSuite:
    transition_baseline: TransitionCarrierCondition
    transition_reset: TransitionCarrierCondition
    transition_transplant: TransitionCarrierCondition
    transition_transplant_report: TransitionTransplantReport
    relation_reentry_summary: dict[str, Any]
    assessment: PersistenceLocusAssessment

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "relation_reentry_summary": self.relation_reentry_summary,
            "transition_baseline": self.transition_baseline.state_dict(),
            "transition_reset": self.transition_reset.state_dict(),
            "transition_transplant": self.transition_transplant.state_dict(),
            "transition_transplant_report": (
                self.transition_transplant_report.state_dict()
            ),
        }


def _pulse(event_id: str, time_ms: float, unit_id: int) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _config() -> LocalExpectationConfig:
    return LocalExpectationConfig(
        minimum_observations=2,
        minimum_confidence=0.1,
        proposal_ttl_ms=25.0,
    )


def _trained_transition_state() -> LocalTemporalExpectation:
    expectation = LocalTemporalExpectation(_config())
    for episode, offset in enumerate((0.0, 25.0, 50.0)):
        rows = tuple(
            _pulse(f"train:{episode}:{index}", offset + index * 5.0, unit_id)
            for index, unit_id in enumerate((0, 1, 2, 3))
        )
        for source, target in zip(rows, rows[1:], strict=False):
            expectation.observe_external_transition(source, target)
    return expectation


def _transition_count(expectation: LocalTemporalExpectation) -> int:
    state = expectation.state_dict()
    return sum(int(row["count"]) for row in state["transitions"].values())


def _new_chain_runtime(
    expectation: LocalTemporalExpectation,
) -> tuple[AutonomousEndogenousChainRuntime, int, int, str]:
    topology = explicit_topology(
        tuple(
            UnitState(unit_id=unit_id, x=float(unit_id), y=0.0, base_threshold=0.5)
            for unit_id in range(4)
        ),
        (),
        receptor_ids=tuple(range(4)),
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
    initial_state = field.state_dict()
    return (
        runtime,
        len(initial_state["queue"]),
        len(transition.state_dict()["paths"]),
        field.state_hash(),
    )


def _run_transition_condition(
    condition_id: str,
    expectation: LocalTemporalExpectation,
) -> TransitionCarrierCondition:
    runtime, queue_size, g2_path_count, initial_field_hash = _new_chain_runtime(
        expectation
    )
    runtime.present_external(_pulse(f"cue:{condition_id}", 100.0, 0))
    runtime.advance_silence(120.0)
    generated = tuple(runtime.generated_sparks)
    state = runtime.state_dict()
    return TransitionCarrierCondition(
        condition_id=condition_id,
        transition_state_hash=expectation.state_hash(),
        initial_field_state_hash=initial_field_hash,
        initial_queue_size=queue_size,
        initial_g2_path_count=g2_path_count,
        generated_units=tuple(row.unit_id for row in generated),
        generated_times_ms=tuple(row.time_ms for row in generated),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
        final_g2_path_count=len(runtime.transition.state_dict()["paths"]),
        runtime_state_hash=digest(state),
        runtime_state=state,
    )


def run_canonical_persistence_locus_suite() -> CanonicalPersistenceLocusSuite:
    source = _trained_transition_state()
    source_state = source.state_dict()

    baseline_expectation = LocalTemporalExpectation.from_state_dict(source_state)
    reset_expectation = LocalTemporalExpectation(_config())
    receiver_before = reset_expectation.state_hash()
    receiver_count_before = _transition_count(reset_expectation)
    transplanted_expectation = LocalTemporalExpectation.from_state_dict(source_state)

    baseline = _run_transition_condition("baseline", baseline_expectation)
    reset = _run_transition_condition("g1-reset", reset_expectation)
    transplanted = _run_transition_condition(
        "g1-transplant",
        transplanted_expectation,
    )
    transplant_report = TransitionTransplantReport(
        source_state_hash=source.state_hash(),
        receiver_state_hash_before=receiver_before,
        receiver_state_hash_after=transplanted_expectation.state_hash(),
        receiver_field_state_hash=transplanted.initial_field_state_hash,
        source_transition_count=_transition_count(source),
        receiver_transition_count_before=receiver_count_before,
        receiver_transition_count_after=_transition_count(transplanted_expectation),
    )

    reentry = run_isolated_relation_reentry_suite()
    relation_summary = {
        "reset_endogenous_field_units": (
            reentry.consistency_reset.endogenous_field_units
        ),
        "reset_boundary_port_ids": reentry.consistency_reset.boundary_port_ids,
        "transplant_endogenous_field_units": (
            reentry.reversal_transplant.endogenous_field_units
        ),
        "transplant_boundary_port_ids": (
            reentry.reversal_transplant.boundary_port_ids
        ),
        "transplant_link_count": (
            reentry.reversal_transplant.transplant_report.copied_link_count
            if reentry.reversal_transplant.transplant_report is not None
            else 0
        ),
        "no_reentry_endogenous_field_units": (
            reentry.no_reentry.endogenous_field_units
        ),
        "consistency_read_only": reentry.assessment.consistency_is_read_only,
    }

    same_naive_field = len(
        {
            baseline.initial_field_state_hash,
            reset.initial_field_state_hash,
            transplanted.initial_field_state_hash,
        }
    ) == 1
    values = {
        "g1_reset_removes_root": not reset.root_generated,
        "g1_reset_removes_full_chain": not reset.full_chain_generated,
        "g1_transplant_transfers_root": transplanted.root_generated,
        "g1_transplant_transfers_full_chain": transplanted.full_chain_generated,
        "receiver_field_is_naive_and_identical": same_naive_field,
        "pending_queue_not_persistent_carrier": (
            baseline.initial_queue_size
            == reset.initial_queue_size
            == transplanted.initial_queue_size
            == 0
        ),
        "g2_path_calibration_not_required": (
            baseline.initial_g2_path_count
            == baseline.final_g2_path_count
            == transplanted.initial_g2_path_count
            == transplanted.final_g2_path_count
            == 0
        ),
        "consistency_reset_removes_reentry": (
            reentry.consistency_reset.endogenous_field_units == ()
            and reentry.consistency_reset.boundary_port_ids == ()
        ),
        "consistency_transplant_transfers_reentry": (
            reentry.reversal_transplant.endogenous_field_units == (9,)
            and reentry.reversal_transplant.boundary_port_ids == ("port:9",)
        ),
        "reentry_adapter_has_no_learned_state": (
            reentry.assessment.consistency_is_read_only
            and reentry.no_reentry.endogenous_field_units == ()
        ),
        "explicit_transition_carrier_candidate": (
            baseline.full_chain_generated
            and not reset.root_generated
            and transplanted.full_chain_generated
        ),
        "explicit_consistency_carrier_candidate": (
            reentry.assessment.reset_removes_effect
            and reentry.assessment.transplant_transfers_effect
        ),
        "independent_field_carrier_supported": False,
        "distributed_carrier_supported": False,
        "limiting_interpretation_supported": True,
    }
    assessment = PersistenceLocusAssessment(
        **values,
        engineering_candidate=all(
            value
            for key, value in values.items()
            if key
            not in {
                "independent_field_carrier_supported",
                "distributed_carrier_supported",
            }
        ),
    )
    return CanonicalPersistenceLocusSuite(
        transition_baseline=baseline,
        transition_reset=reset,
        transition_transplant=transplanted,
        transition_transplant_report=transplant_report,
        relation_reentry_summary=relation_summary,
        assessment=assessment,
    )

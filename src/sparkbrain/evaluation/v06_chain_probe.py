from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.endogenous_chain import (
    AutonomousEndogenousChainRuntime,
    EndogenousChainIntervention,
)
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig


@dataclass(frozen=True, slots=True)
class ChainConditionResult:
    condition_id: str
    main_units: tuple[int, ...]
    control_units: tuple[int, ...]
    main_times_ms: tuple[float, ...]
    control_times_ms: tuple[float, ...]
    external_observation_count: int
    committed_positive_updates: int
    proposal_count: int
    intervention_count: int
    suppressed_reasons: tuple[str, ...]
    runtime_state_hash: str
    runtime_state: dict[str, Any]

    @property
    def main_downstream_count(self) -> int:
        return sum(unit_id in {2, 3} for unit_id in self.main_units)

    @property
    def main_root_present(self) -> bool:
        return 1 in self.main_units

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["main_downstream_count"] = self.main_downstream_count
        value["main_root_present"] = self.main_root_present
        return value


@dataclass(frozen=True, slots=True)
class CausalChainAssessment:
    sham_main_downstream_count: int
    targeted_main_downstream_count: int
    matched_random_main_downstream_count: int
    targeted_impairment: float
    matched_random_impairment: float
    selective_effect: float
    root_preserved_under_targeted_intervention: bool
    targeted_intervention_active: bool
    matched_random_intervention_active: bool
    no_positive_self_confirmation: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalChainSuite:
    sham: ChainConditionResult
    targeted_expansion: ChainConditionResult
    matched_random_expansion: ChainConditionResult
    root_reinjection_suppressed: ChainConditionResult
    downstream_reinjection_suppressed: ChainConditionResult
    assessment: CausalChainAssessment

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "downstream_reinjection_suppressed": (
                self.downstream_reinjection_suppressed.state_dict()
            ),
            "matched_random_expansion": self.matched_random_expansion.state_dict(),
            "root_reinjection_suppressed": self.root_reinjection_suppressed.state_dict(),
            "sham": self.sham.state_dict(),
            "targeted_expansion": self.targeted_expansion.state_dict(),
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


def build_runtime(
    intervention: EndogenousChainIntervention | None = None,
) -> AutonomousEndogenousChainRuntime:
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
            for unit_id in range(8)
        ),
        (),
        receptor_ids=tuple(range(8)),
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
    return AutonomousEndogenousChainRuntime(
        field,
        expectation,
        transition,
        reinjection,
        intervention=intervention,
    )


def run_condition(
    condition_id: str,
    intervention: EndogenousChainIntervention | None = None,
) -> ChainConditionResult:
    runtime = build_runtime(intervention)
    runtime.present_external(pulse("control-cue", 100.0, 4))
    runtime.advance_silence(120.0)
    runtime.present_external(pulse("main-cue", 150.0, 0))
    runtime.advance_silence(170.0)
    main = tuple(row for row in runtime.generated_sparks if 150.0 < row.time_ms <= 170.0)
    control = tuple(row for row in runtime.generated_sparks if 100.0 < row.time_ms <= 120.0)
    return ChainConditionResult(
        condition_id=condition_id,
        main_units=tuple(row.unit_id for row in main),
        control_units=tuple(row.unit_id for row in control),
        main_times_ms=tuple(row.time_ms for row in main),
        control_times_ms=tuple(row.time_ms for row in control),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
        proposal_count=len(runtime.proposal_records),
        intervention_count=len(runtime.intervention_records),
        suppressed_reasons=tuple(row.reason for row in runtime.intervention_records),
        runtime_state_hash=runtime.state_hash(),
        runtime_state=runtime.state_dict(),
    )


def run_canonical_chain_suite() -> CanonicalChainSuite:
    sham = run_condition("sham")
    targeted = run_condition(
        "targeted-expansion",
        EndogenousChainIntervention(suppress_expansion_unit_ids=(1,)),
    )
    matched_random = run_condition(
        "matched-random-expansion",
        EndogenousChainIntervention(suppress_expansion_unit_ids=(5,)),
    )
    root_suppressed = run_condition(
        "root-reinjection-suppressed",
        EndogenousChainIntervention(
            suppress_reinjection_path_ids=("local:unit:0->unit:1",)
        ),
    )
    downstream_suppressed = run_condition(
        "downstream-reinjection-suppressed",
        EndogenousChainIntervention(
            suppress_reinjection_path_ids=("local:unit:1->unit:2",)
        ),
    )
    denominator = max(1, sham.main_downstream_count)
    targeted_impairment = 1.0 - targeted.main_downstream_count / denominator
    random_impairment = 1.0 - matched_random.main_downstream_count / denominator
    no_self_confirmation = all(
        row.committed_positive_updates == 0
        for row in (
            sham,
            targeted,
            matched_random,
            root_suppressed,
            downstream_suppressed,
        )
    )
    assessment = CausalChainAssessment(
        sham_main_downstream_count=sham.main_downstream_count,
        targeted_main_downstream_count=targeted.main_downstream_count,
        matched_random_main_downstream_count=matched_random.main_downstream_count,
        targeted_impairment=targeted_impairment,
        matched_random_impairment=random_impairment,
        selective_effect=targeted_impairment - random_impairment,
        root_preserved_under_targeted_intervention=targeted.main_root_present,
        targeted_intervention_active=targeted.intervention_count == 1,
        matched_random_intervention_active=matched_random.intervention_count == 1,
        no_positive_self_confirmation=no_self_confirmation,
        engineering_candidate=(
            sham.main_units == (1, 2, 3)
            and targeted.main_units == (1,)
            and matched_random.main_units == (1, 2, 3)
            and targeted_impairment > random_impairment
            and targeted.main_root_present
            and targeted.intervention_count == 1
            and matched_random.intervention_count == 1
            and no_self_confirmation
        ),
    )
    return CanonicalChainSuite(
        sham=sham,
        targeted_expansion=targeted,
        matched_random_expansion=matched_random,
        root_reinjection_suppressed=root_suppressed,
        downstream_reinjection_suppressed=downstream_suppressed,
        assessment=assessment,
    )

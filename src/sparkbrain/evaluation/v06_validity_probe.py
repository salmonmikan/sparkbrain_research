from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.forward import (
    AssemblyFreeForwardRuntime,
    ForwardRuntimeConfig,
    evaluate_forward_completion,
    train_external_sequences,
)
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reality import RealityCorrectionEngine
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig

from .v06_endogenous import (
    EndogenousOriginAuditConfig,
    audit_endogenous_origin,
)


@dataclass(frozen=True, slots=True)
class MissingMiddleAssayResult:
    generated_target: str | None
    generated_time_ms: float | None
    later_external_time_ms: float
    strict_forward: bool
    later_link_confirmed: bool
    readout_only_generated_count: int
    early_future_generated_count: int
    early_future_retrospective_only: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PrefixContinuationAssayResult:
    generated_targets: tuple[str, ...]
    generated_times_ms: tuple[float, ...]
    external_observation_count: int
    committed_positive_updates: int
    no_reinjection_generated_count: int
    no_history_generated_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BranchingAssayResult:
    equal_branch_proposal_targets: tuple[str, ...]
    equal_branch_generated_targets: tuple[str, ...]
    equal_branch_effective_currents: tuple[float, ...]
    imbalanced_branch_proposal_targets: tuple[str, ...]
    imbalanced_branch_generated_targets: tuple[str, ...]
    imbalanced_branch_effective_currents: tuple[float, ...]
    readout_only_generated_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class OmissionAssayResult:
    omitted_generated_targets: tuple[str, ...]
    observed_generated_count: int
    observed_external_spike_units: tuple[int, ...]
    matched_prediction_count: int
    external_observation_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class OriginControlResult:
    direct_copy_candidate: bool
    direct_copy_reasons: tuple[str, ...]
    fixed_echo_candidate: bool
    fixed_echo_reasons: tuple[str, ...]
    queue_unexcluded_candidate: bool
    queue_unexcluded_reasons: tuple[str, ...]
    unknown_source_generated_count: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ValidityAssayAssessment:
    strict_missing_middle_supported: bool
    readout_only_rejected: bool
    retrospective_not_forward: bool
    prefix_continuation_supported: bool
    no_history_and_no_reinjection_controls_passed: bool
    equal_branch_alternatives_preserved: bool
    branch_strength_changes_field_outcome: bool
    omission_generates_internal_event: bool
    matching_external_event_remains_authoritative: bool
    direct_copy_rejected: bool
    fixed_echo_rejected: bool
    unresolved_queue_rejected: bool
    no_unknown_source_generation: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CanonicalValidityAssaySuite:
    missing_middle: MissingMiddleAssayResult
    prefix_continuation: PrefixContinuationAssayResult
    branching: BranchingAssayResult
    omission: OmissionAssayResult
    origin_controls: OriginControlResult
    assessment: ValidityAssayAssessment

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "branching": self.branching.state_dict(),
            "missing_middle": self.missing_middle.state_dict(),
            "omission": self.omission.state_dict(),
            "origin_controls": self.origin_controls.state_dict(),
            "prefix_continuation": self.prefix_continuation.state_dict(),
        }


def pulse(
    event_id: str,
    time_ms: float,
    unit_id: int,
    *,
    magnitude: float = 1.0,
    origin: EventOrigin = EventOrigin.EXTERNAL,
    origin_state_hash: str | None = None,
) -> RuntimePulse:
    metadata: dict[str, Any] = {}
    if origin_state_hash is not None:
        metadata["origin_state_hash"] = origin_state_hash
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=magnitude,
        polarity=1,
        origin=origin,
        metadata=metadata,
    )


def _build_runtime(
    sequences: tuple[tuple[RuntimePulse, ...], ...],
    *,
    unit_count: int,
    reinjection_enabled: bool = True,
    minimum_confidence: float = 0.1,
) -> AssemblyFreeForwardRuntime:
    expectation = LocalTemporalExpectation(
        LocalExpectationConfig(
            minimum_observations=2,
            minimum_confidence=minimum_confidence,
            maximum_candidates=4,
            proposal_ttl_ms=25.0,
        )
    )
    train_external_sequences(expectation, sequences)
    topology = explicit_topology(
        tuple(
            UnitState(
                unit_id=unit_id,
                x=float(unit_id),
                y=0.0,
                base_threshold=0.5,
            )
            for unit_id in range(unit_count)
        ),
        (),
        receptor_ids=tuple(range(unit_count)),
    )
    field = TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            receptor_fanout=1,
            refractory_ms=2.0,
            adaptation_increment=0.0,
        ),
    )
    ledger = ProvenanceLedger()
    transition = SparseLocalTransitionAdaptation(expectation, ledger)
    reinjection = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=minimum_confidence,
            maximum_effective_current=2.0,
            maximum_branches_per_origin_state=4,
            maximum_proposals_per_window=16,
        ),
    )
    reality = RealityCorrectionEngine(transition, ledger)
    return AssemblyFreeForwardRuntime(
        field,
        expectation,
        transition,
        reinjection,
        reality,
        ForwardRuntimeConfig(
            reinjection_enabled=reinjection_enabled,
            expand_endogenous_sparks=True,
        ),
    )


def _linear_sequences() -> tuple[tuple[RuntimePulse, ...], ...]:
    return tuple(
        tuple(
            pulse(
                f"linear:{episode}:{index}",
                episode * 30.0 + index * 5.0,
                unit_id,
            )
            for index, unit_id in enumerate((0, 1, 2, 3))
        )
        for episode in range(3)
    )


def run_missing_middle_assay() -> MissingMiddleAssayResult:
    runtime = _build_runtime(_linear_sequences(), unit_count=4)
    runtime.process_external(pulse("mm:a", 100.0, 0))
    runtime.process_external(pulse("mm:b", 105.0, 1))
    runtime.process_external(pulse("mm:d", 115.0, 3))
    result = evaluate_forward_completion(
        runtime,
        expected_target="unit:2",
        later_external_event_id="mm:d",
        later_external_time_ms=115.0,
    )

    readout = _build_runtime(
        _linear_sequences(),
        unit_count=4,
        reinjection_enabled=False,
    )
    readout.process_external(pulse("readout:a", 100.0, 0))
    readout.process_external(pulse("readout:b", 105.0, 1))
    readout.process_external(pulse("readout:d", 115.0, 3))

    early = _build_runtime(_linear_sequences(), unit_count=4)
    early.process_external(pulse("early:a", 100.0, 0))
    early.process_external(pulse("early:b", 105.0, 1))
    early.process_external(pulse("early:d", 109.0, 3))
    early_result = evaluate_forward_completion(
        early,
        expected_target="unit:2",
        later_external_event_id="early:d",
        later_external_time_ms=109.0,
    )

    return MissingMiddleAssayResult(
        generated_target="unit:2" if result.forward_generated else None,
        generated_time_ms=result.endogenous_spark_time_ms,
        later_external_time_ms=115.0,
        strict_forward=result.temporal_compliance,
        later_link_confirmed=result.later_prediction_matched,
        readout_only_generated_count=len(readout.generated_sparks),
        early_future_generated_count=len(early.generated_sparks),
        early_future_retrospective_only=early_result.retrospective_only,
    )


def run_prefix_continuation_assay() -> PrefixContinuationAssayResult:
    runtime = _build_runtime(_linear_sequences(), unit_count=4)
    runtime.process_external(pulse("prefix:a", 100.0, 0))
    runtime.process_external(pulse("prefix:b", 105.0, 1))
    generated = runtime.advance_internal_until(116.0)

    no_reinjection = _build_runtime(
        _linear_sequences(),
        unit_count=4,
        reinjection_enabled=False,
    )
    no_reinjection.process_external(pulse("no-reinjection:a", 100.0, 0))
    no_reinjection.process_external(pulse("no-reinjection:b", 105.0, 1))
    no_reinjection.advance_internal_until(116.0)

    no_history = _build_runtime((), unit_count=4)
    no_history.process_external(pulse("no-history:a", 100.0, 0))
    no_history.process_external(pulse("no-history:b", 105.0, 1))
    no_history.advance_internal_until(116.0)

    return PrefixContinuationAssayResult(
        generated_targets=tuple(row.target for row in generated),
        generated_times_ms=tuple(row.time_ms for row in generated),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
        no_reinjection_generated_count=len(no_reinjection.generated_sparks),
        no_history_generated_count=len(no_history.generated_sparks),
    )


def _branch_sequences(
    *,
    first_count: int,
    second_count: int,
) -> tuple[tuple[RuntimePulse, ...], ...]:
    rows: list[tuple[RuntimePulse, ...]] = []
    cursor = 0
    for target, count in ((2, first_count), (3, second_count)):
        for occurrence in range(count):
            start = cursor * 20.0
            rows.append(
                (
                    pulse(f"branch:{target}:{occurrence}:source", start, 1),
                    pulse(f"branch:{target}:{occurrence}:target", start + 5.0, target),
                )
            )
            cursor += 1
    return tuple(rows)


def _run_branch_condition(
    sequences: tuple[tuple[RuntimePulse, ...], ...],
    *,
    reinjection_enabled: bool = True,
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[float, ...]]:
    runtime = _build_runtime(
        sequences,
        unit_count=4,
        reinjection_enabled=reinjection_enabled,
        minimum_confidence=0.1,
    )
    runtime.process_external(pulse("branch:probe", 200.0, 1))
    runtime.advance_internal_until(206.0)
    proposal_targets = tuple(row.target for row in runtime.proposal_schedules)
    currents = tuple(
        row.reinjection.effective_current
        for row in runtime.proposal_schedules
        if row.reinjection is not None and row.reinjection.accepted
    )
    generated_targets = tuple(row.target for row in runtime.generated_sparks)
    return proposal_targets, generated_targets, currents


def run_branching_assay() -> BranchingAssayResult:
    equal = _run_branch_condition(
        _branch_sequences(first_count=3, second_count=3)
    )
    imbalanced = _run_branch_condition(
        _branch_sequences(first_count=4, second_count=2)
    )
    readout = _run_branch_condition(
        _branch_sequences(first_count=3, second_count=3),
        reinjection_enabled=False,
    )
    return BranchingAssayResult(
        equal_branch_proposal_targets=equal[0],
        equal_branch_generated_targets=equal[1],
        equal_branch_effective_currents=equal[2],
        imbalanced_branch_proposal_targets=imbalanced[0],
        imbalanced_branch_generated_targets=imbalanced[1],
        imbalanced_branch_effective_currents=imbalanced[2],
        readout_only_generated_count=len(readout[1]),
    )


def _omission_sequences() -> tuple[tuple[RuntimePulse, ...], ...]:
    return tuple(
        (
            pulse(f"omission:{index}:source", index * 20.0, 0),
            pulse(f"omission:{index}:target", index * 20.0 + 5.0, 1),
        )
        for index in range(3)
    )


def run_omission_assay() -> OmissionAssayResult:
    omitted = _build_runtime(_omission_sequences(), unit_count=2)
    omitted.process_external(pulse("omitted:source", 100.0, 0))
    omitted.advance_internal_until(106.0)

    observed = _build_runtime(_omission_sequences(), unit_count=2)
    observed.process_external(pulse("observed:source", 100.0, 0))
    external_step = observed.process_external(pulse("observed:target", 105.0, 1))
    matched = sum(
        row.external_event_id == "observed:target" and row.status == "matched"
        for row in observed.ledger.matches.values()
    )
    return OmissionAssayResult(
        omitted_generated_targets=tuple(row.target for row in omitted.generated_sparks),
        observed_generated_count=len(observed.generated_sparks),
        observed_external_spike_units=external_step.field_spike_ids,
        matched_prediction_count=matched,
        external_observation_count=observed.ledger.external_observation_count,
    )


def run_origin_controls() -> OriginControlResult:
    state_hash = "s" * 64
    external_current = pulse("control:external", 10.0, 2, magnitude=0.7)
    direct_copy = pulse(
        "control:direct-copy",
        10.2,
        2,
        magnitude=0.7,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        origin_state_hash=state_hash,
    )
    echo = pulse(
        "control:echo",
        15.0,
        2,
        magnitude=0.7,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        origin_state_hash=state_hash,
    )
    clean_other_target = pulse(
        "control:queue-unexcluded",
        15.0,
        3,
        magnitude=0.7,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
        origin_state_hash=state_hash,
    )
    direct_audit = audit_endogenous_origin(
        direct_copy,
        current_external_events=(external_current,),
        survives_queue_drained_control=True,
    )
    echo_audit = audit_endogenous_origin(
        echo,
        current_external_events=(external_current,),
        survives_queue_drained_control=True,
        config=EndogenousOriginAuditConfig(
            known_echo_delays_ms=(5.0,),
            echo_delay_tolerance_ms=0.1,
        ),
    )
    queue_audit = audit_endogenous_origin(
        clean_other_target,
        current_external_events=(external_current,),
        survives_queue_drained_control=False,
    )

    unknown = _build_runtime(_omission_sequences(), unit_count=4)
    unknown.process_external(pulse("unknown:source", 100.0, 3))
    unknown.advance_internal_until(110.0)

    return OriginControlResult(
        direct_copy_candidate=direct_audit.candidate,
        direct_copy_reasons=direct_audit.reason_codes,
        fixed_echo_candidate=echo_audit.candidate,
        fixed_echo_reasons=echo_audit.reason_codes,
        queue_unexcluded_candidate=queue_audit.candidate,
        queue_unexcluded_reasons=queue_audit.reason_codes,
        unknown_source_generated_count=len(unknown.generated_sparks),
    )


def run_canonical_validity_assay_suite() -> CanonicalValidityAssaySuite:
    missing = run_missing_middle_assay()
    prefix = run_prefix_continuation_assay()
    branching = run_branching_assay()
    omission = run_omission_assay()
    controls = run_origin_controls()

    assessment = ValidityAssayAssessment(
        strict_missing_middle_supported=(
            missing.generated_target == "unit:2"
            and missing.generated_time_ms == 110.0
            and missing.generated_time_ms < missing.later_external_time_ms
            and missing.strict_forward
            and missing.later_link_confirmed
        ),
        readout_only_rejected=missing.readout_only_generated_count == 0,
        retrospective_not_forward=(
            missing.early_future_generated_count == 0
            and missing.early_future_retrospective_only
        ),
        prefix_continuation_supported=(
            prefix.generated_targets == ("unit:2", "unit:3")
            and prefix.generated_times_ms == (110.0, 115.0)
        ),
        no_history_and_no_reinjection_controls_passed=(
            prefix.no_history_generated_count == 0
            and prefix.no_reinjection_generated_count == 0
        ),
        equal_branch_alternatives_preserved=(
            branching.equal_branch_proposal_targets == ("unit:2", "unit:3")
            and branching.equal_branch_generated_targets == ("unit:2", "unit:3")
        ),
        branch_strength_changes_field_outcome=(
            branching.imbalanced_branch_proposal_targets == ("unit:2", "unit:3")
            and branching.imbalanced_branch_generated_targets == ("unit:2",)
            and branching.imbalanced_branch_effective_currents[0]
            > branching.imbalanced_branch_effective_currents[1]
        ),
        omission_generates_internal_event=(
            omission.omitted_generated_targets == ("unit:1",)
        ),
        matching_external_event_remains_authoritative=(
            omission.observed_generated_count == 0
            and omission.observed_external_spike_units == (1,)
            and omission.matched_prediction_count == 1
            and omission.external_observation_count == 2
        ),
        direct_copy_rejected=(
            not controls.direct_copy_candidate
            and "direct_current_input_copy" in controls.direct_copy_reasons
        ),
        fixed_echo_rejected=(
            not controls.fixed_echo_candidate
            and "known_fixed_delay_echo" in controls.fixed_echo_reasons
        ),
        unresolved_queue_rejected=(
            not controls.queue_unexcluded_candidate
            and "queue_replay_not_excluded" in controls.queue_unexcluded_reasons
        ),
        no_unknown_source_generation=controls.unknown_source_generated_count == 0,
        engineering_candidate=False,
    )
    assessment = ValidityAssayAssessment(
        **{
            **assessment.state_dict(),
            "engineering_candidate": all(
                value
                for key, value in assessment.state_dict().items()
                if key != "engineering_candidate"
            ),
        }
    )
    return CanonicalValidityAssaySuite(
        missing_middle=missing,
        prefix_continuation=prefix,
        branching=branching,
        omission=omission,
        origin_controls=controls,
        assessment=assessment,
    )

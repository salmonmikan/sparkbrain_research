from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import UnitState, explicit_topology
from sparkbrain.v06.boundary import AnonymousBoundaryEmitter, BoundaryCoupling
from sparkbrain.v06.endogenous_chain import AutonomousEndogenousChainRuntime
from sparkbrain.v06.forward import AssemblyFreeForwardRuntime
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse, digest
from sparkbrain.v06.local_expectation import LocalExpectationConfig, LocalTemporalExpectation
from sparkbrain.v06.local_transition import SparseLocalTransitionAdaptation
from sparkbrain.v06.reality import RealityCorrectionEngine
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig


@dataclass(frozen=True, slots=True)
class G1AssayObservation:
    assay_id: str
    g1_enabled: bool
    input_signature: tuple[tuple[float, int], ...]
    initial_field_state_hash: str
    g1_transition_count: int
    generated_units: tuple[int, ...]
    generated_times_ms: tuple[float, ...]
    proposal_count: int
    boundary_port_ids: tuple[str, ...]
    external_observation_count: int
    committed_positive_updates: int

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class G1DependencyCondition:
    g1_enabled: bool
    same_input_response: G1AssayObservation
    sequential_continuation: G1AssayObservation
    branching: G1AssayObservation
    forward_bridge: G1AssayObservation
    boundary_effect: G1AssayObservation

    def observations(self) -> tuple[G1AssayObservation, ...]:
        return (
            self.same_input_response,
            self.sequential_continuation,
            self.branching,
            self.forward_bridge,
            self.boundary_effect,
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "boundary_effect": self.boundary_effect.state_dict(),
            "branching": self.branching.state_dict(),
            "forward_bridge": self.forward_bridge.state_dict(),
            "g1_enabled": self.g1_enabled,
            "same_input_response": self.same_input_response.state_dict(),
            "sequential_continuation": self.sequential_continuation.state_dict(),
        }


@dataclass(frozen=True, slots=True)
class G1DependencyAssessment:
    same_input_response_requires_g1: bool
    sequential_continuation_requires_g1: bool
    branching_requires_g1: bool
    forward_bridge_requires_g1: bool
    boundary_effect_requires_g1: bool
    field_initial_states_matched: bool
    external_inputs_matched: bool
    disabled_g1_has_no_transition_state: bool
    endogenous_only_runs_do_not_commit_positive_learning: bool
    explicit_g1_burden_identified: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class G1DependencySuite:
    enabled: G1DependencyCondition
    disabled: G1DependencyCondition
    assessment: G1DependencyAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "disabled": self.disabled.state_dict(),
            "enabled": self.enabled.state_dict(),
            "suite_hash": self.suite_hash,
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


def _expectation_config() -> LocalExpectationConfig:
    return LocalExpectationConfig(
        minimum_observations=2,
        minimum_confidence=0.1,
        maximum_candidates=8,
        proposal_ttl_ms=25.0,
    )


def _train_paths(
    model: LocalTemporalExpectation,
    paths: tuple[tuple[int, ...], ...],
) -> None:
    for path_index, path in enumerate(paths):
        for episode, offset in enumerate((0.0, 30.0, 60.0)):
            rows = tuple(
                _pulse(
                    f"g1:{path_index}:{episode}:{index}",
                    offset + index * 5.0,
                    unit_id,
                )
                for index, unit_id in enumerate(path)
            )
            for source, target in zip(rows, rows[1:], strict=False):
                model.observe_external_transition(source, target)


def _build_expectation(
    *,
    g1_enabled: bool,
    paths: tuple[tuple[int, ...], ...],
) -> LocalTemporalExpectation:
    model = LocalTemporalExpectation(_expectation_config())
    if g1_enabled:
        _train_paths(model, paths)
    return model


def _transition_count(model: LocalTemporalExpectation) -> int:
    return sum(
        int(row["count"])
        for table in model.state_dict()["transitions"].values()
        for row in table.values()
    )


def _new_field(unit_count: int) -> TemporalExcitableField:
    topology = explicit_topology(
        tuple(
            UnitState(unit_id=unit_id, x=float(unit_id), y=0.0, base_threshold=0.5)
            for unit_id in range(unit_count)
        ),
        (),
        receptor_ids=tuple(range(unit_count)),
    )
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            adaptation_increment=0.0,
            receptor_fanout=1,
            refractory_ms=2.0,
        ),
    )


def _build_chain_runtime(
    *,
    g1_enabled: bool,
    paths: tuple[tuple[int, ...], ...],
    unit_count: int,
) -> tuple[AutonomousEndogenousChainRuntime, str]:
    expectation = _build_expectation(g1_enabled=g1_enabled, paths=paths)
    field = _new_field(unit_count)
    initial_field_hash = field.state_hash()
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
            maximum_energy_per_window=64.0,
        ),
    )
    return (
        AutonomousEndogenousChainRuntime(
            field,
            expectation,
            transition,
            reinjection,
        ),
        initial_field_hash,
    )


def _run_chain_assay(
    *,
    assay_id: str,
    g1_enabled: bool,
    paths: tuple[tuple[int, ...], ...],
    unit_count: int,
    cue_unit_id: int = 0,
    horizon_ms: float = 125.0,
) -> tuple[G1AssayObservation, AutonomousEndogenousChainRuntime]:
    runtime, initial_field_hash = _build_chain_runtime(
        g1_enabled=g1_enabled,
        paths=paths,
        unit_count=unit_count,
    )
    cue = _pulse(f"{assay_id}:cue", 100.0, cue_unit_id)
    runtime.present_external(cue)
    runtime.advance_silence(horizon_ms)
    generated = tuple(runtime.generated_sparks)
    observation = G1AssayObservation(
        assay_id=assay_id,
        g1_enabled=g1_enabled,
        input_signature=((cue.time_ms, cue_unit_id),),
        initial_field_state_hash=initial_field_hash,
        g1_transition_count=_transition_count(runtime.expectation),
        generated_units=tuple(row.unit_id for row in generated),
        generated_times_ms=tuple(row.time_ms for row in generated),
        proposal_count=len(runtime.proposal_records),
        boundary_port_ids=(),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
    )
    return observation, runtime


def _run_boundary_assay(
    *,
    g1_enabled: bool,
) -> G1AssayObservation:
    observation, runtime = _run_chain_assay(
        assay_id="boundary-effect",
        g1_enabled=g1_enabled,
        paths=((0, 1, 2, 3),),
        unit_count=4,
    )
    emitter = AnonymousBoundaryEmitter(
        (BoundaryCoupling(source_unit_id=3, port_id="port:7"),)
    )
    events = emitter.emit(
        tuple(runtime.generated_sparks),
        source_state_hash=runtime.state_hash(),
    )
    return G1AssayObservation(
        **{
            **observation.state_dict(),
            "boundary_port_ids": tuple(row.port_id for row in events),
        }
    )


def _build_forward_runtime(
    *,
    g1_enabled: bool,
) -> tuple[AssemblyFreeForwardRuntime, str]:
    expectation = _build_expectation(
        g1_enabled=g1_enabled,
        paths=((0, 1, 2, 3),),
    )
    field = _new_field(4)
    initial_field_hash = field.state_hash()
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
            maximum_energy_per_window=64.0,
        ),
    )
    reality = RealityCorrectionEngine(transition, ledger)
    return (
        AssemblyFreeForwardRuntime(
            field,
            expectation,
            transition,
            reinjection,
            reality,
        ),
        initial_field_hash,
    )


def _run_forward_bridge_assay(
    *,
    g1_enabled: bool,
) -> G1AssayObservation:
    runtime, initial_field_hash = _build_forward_runtime(g1_enabled=g1_enabled)
    events = (
        _pulse("forward:A", 100.0, 0),
        _pulse("forward:B", 105.0, 1),
        _pulse("forward:D", 120.0, 3),
    )
    for event in events:
        runtime.process_external(event)
    generated = tuple(runtime.generated_sparks)
    return G1AssayObservation(
        assay_id="forward-bridge",
        g1_enabled=g1_enabled,
        input_signature=tuple(
            (event.time_ms, int(event.target.removeprefix("unit:")))
            for event in events
        ),
        initial_field_state_hash=initial_field_hash,
        g1_transition_count=_transition_count(runtime.expectation),
        generated_units=tuple(row.unit_id for row in generated),
        generated_times_ms=tuple(row.time_ms for row in generated),
        proposal_count=len(runtime.proposal_schedules),
        boundary_port_ids=(),
        external_observation_count=runtime.ledger.external_observation_count,
        committed_positive_updates=runtime.ledger.committed_positive_updates,
    )


def _run_condition(g1_enabled: bool) -> G1DependencyCondition:
    same_input, _ = _run_chain_assay(
        assay_id="same-input-response",
        g1_enabled=g1_enabled,
        paths=((0, 1),),
        unit_count=3,
        horizon_ms=110.0,
    )
    chain, _ = _run_chain_assay(
        assay_id="sequential-continuation",
        g1_enabled=g1_enabled,
        paths=((0, 1, 2, 3),),
        unit_count=4,
    )
    branching, _ = _run_chain_assay(
        assay_id="branching",
        g1_enabled=g1_enabled,
        paths=((0, 1), (0, 2)),
        unit_count=3,
        horizon_ms=110.0,
    )
    return G1DependencyCondition(
        g1_enabled=g1_enabled,
        same_input_response=same_input,
        sequential_continuation=chain,
        branching=branching,
        forward_bridge=_run_forward_bridge_assay(g1_enabled=g1_enabled),
        boundary_effect=_run_boundary_assay(g1_enabled=g1_enabled),
    )


def run_g1_dependency_suite() -> G1DependencySuite:
    """Measure what disappears when explicit G1 state is empty.

    This is a dependency assay, not a replacement architecture. Both conditions
    retain the same Field, G2, reinjection, reality, and boundary mechanisms.
    The disabled condition differs only in having no learned G1 transition rows.
    """

    enabled = _run_condition(True)
    disabled = _run_condition(False)
    paired = tuple(zip(enabled.observations(), disabled.observations(), strict=True))
    field_matched = all(
        left.initial_field_state_hash == right.initial_field_state_hash
        for left, right in paired
    )
    inputs_matched = all(
        left.input_signature == right.input_signature for left, right in paired
    )
    disabled_empty = all(
        row.g1_transition_count == 0 for row in disabled.observations()
    )
    endogenous_only_rows = (
        enabled.same_input_response,
        enabled.sequential_continuation,
        enabled.branching,
        enabled.boundary_effect,
        disabled.same_input_response,
        disabled.sequential_continuation,
        disabled.branching,
        disabled.boundary_effect,
    )
    no_internal_commit = all(
        row.committed_positive_updates == 0 for row in endogenous_only_rows
    )
    values = {
        "same_input_response_requires_g1": (
            enabled.same_input_response.generated_units == (1,)
            and disabled.same_input_response.generated_units == ()
        ),
        "sequential_continuation_requires_g1": (
            enabled.sequential_continuation.generated_units == (1, 2, 3)
            and disabled.sequential_continuation.generated_units == ()
        ),
        "branching_requires_g1": (
            set(enabled.branching.generated_units) == {1, 2}
            and disabled.branching.generated_units == ()
        ),
        "forward_bridge_requires_g1": (
            2 in enabled.forward_bridge.generated_units
            and any(
                unit_id == 2 and time_ms < 120.0
                for unit_id, time_ms in zip(
                    enabled.forward_bridge.generated_units,
                    enabled.forward_bridge.generated_times_ms,
                    strict=True,
                )
            )
            and 2 not in disabled.forward_bridge.generated_units
        ),
        "boundary_effect_requires_g1": (
            enabled.boundary_effect.boundary_port_ids == ("port:7",)
            and disabled.boundary_effect.boundary_port_ids == ()
        ),
        "field_initial_states_matched": field_matched,
        "external_inputs_matched": inputs_matched,
        "disabled_g1_has_no_transition_state": disabled_empty,
        "endogenous_only_runs_do_not_commit_positive_learning": no_internal_commit,
    }
    assessment = G1DependencyAssessment(
        **values,
        explicit_g1_burden_identified=all(values.values()),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "disabled": disabled.state_dict(),
        "enabled": enabled.state_dict(),
    }
    return G1DependencySuite(
        enabled=enabled,
        disabled=disabled,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )

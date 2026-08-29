from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Protocol

from sparkbrain.baselines.v06.g3_recurrent import GenericRecurrentPredictor
from sparkbrain.baselines.v06.g4_assembly import AssemblyConditionedPredictor
from sparkbrain.baselines.v06.g5_typed import TypedFunctionalHeadSystem
from sparkbrain.v06.foundation import digest

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
    build_result_records,
    result_record_state,
)
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters
from .v06_confirmatory_resources import (
    ConditionResourceRecord,
    PrivilegedInformation,
)


class ComparatorFacade(Protocol):
    condition: ConfirmatoryCondition

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None: ...

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]: ...

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None: ...

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None: ...

    def state_dict(self) -> dict[str, Any]: ...

    def parameter_count(self) -> int: ...

    def observed_count(self) -> int: ...

    def generated_count(self) -> int: ...

    def intervention_count(self) -> int: ...

    def assembly_entries(self) -> int: ...

    def typed_head_count(self) -> int: ...

    def reward_observation_count(self) -> int: ...

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]: ...


@dataclass
class G3Facade:
    model: GenericRecurrentPredictor
    condition: ConfirmatoryCondition = ConfirmatoryCondition.G3_RECURRENT

    @classmethod
    def create(cls) -> G3Facade:
        return cls(GenericRecurrentPredictor())

    @classmethod
    def restore(cls, state: dict[str, Any]) -> G3Facade:
        return cls(GenericRecurrentPredictor.from_state_dict(state))

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None:
        del context_id
        self.model.observe_sequence(path, repetitions=repetitions)

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]:
        del context_id
        result = self.model.rollout(
            cue,
            steps=3,
            suppressed_sources=suppressed_sources,
        )
        return tuple(int(row) for row in result.generated_tokens)

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None:
        del context_id
        self.model.observe_boundary(
            port_id,
            target,
            alternate_targets=alternate_targets,
        )

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None:
        del context_id
        result = self.model.boundary_output(
            port_id,
            suppressed_ports=suppressed_ports,
        )
        return int(result.target) if result.target is not None else None

    def state_dict(self) -> dict[str, Any]:
        return self.model.state_dict()

    def parameter_count(self) -> int:
        return self.model.parameter_count

    def observed_count(self) -> int:
        return (
            self.model.observed_sequence_count
            + self.model.relation_observation_count
        )

    def generated_count(self) -> int:
        return (
            self.model.generated_token_count
            + self.model.boundary_output_count
        )

    def intervention_count(self) -> int:
        return self.model.intervention_count

    def assembly_entries(self) -> int:
        return 0

    def typed_head_count(self) -> int:
        return 0

    def reward_observation_count(self) -> int:
        return 0

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]:
        return ()


@dataclass
class G4Facade:
    model: AssemblyConditionedPredictor
    condition: ConfirmatoryCondition = ConfirmatoryCondition.G4_ASSEMBLY

    @classmethod
    def create(cls) -> G4Facade:
        return cls(AssemblyConditionedPredictor())

    @classmethod
    def restore(cls, state: dict[str, Any]) -> G4Facade:
        return cls(AssemblyConditionedPredictor.from_state_dict(state))

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None:
        self.model.observe_sequence(
            context_id,
            path,
            repetitions=repetitions,
        )

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]:
        result = self.model.rollout(
            context_id,
            cue,
            steps=3,
            suppressed_sources=suppressed_sources,
        )
        return tuple(int(row) for row in result.generated_tokens)

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None:
        del context_id
        self.model.observe_boundary(
            port_id,
            target,
            alternate_targets=alternate_targets,
        )

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None:
        del context_id
        result = self.model.boundary_output(
            port_id,
            suppressed_ports=suppressed_ports,
        )
        return int(result.target) if result.target is not None else None

    def state_dict(self) -> dict[str, Any]:
        return self.model.state_dict()

    def parameter_count(self) -> int:
        return self.model.parameter_count

    def observed_count(self) -> int:
        return (
            self.model.observed_sequence_count
            + self.model.relation_observation_count
        )

    def generated_count(self) -> int:
        return (
            self.model.generated_token_count
            + self.model.boundary_output_count
        )

    def intervention_count(self) -> int:
        return self.model.intervention_count

    def assembly_entries(self) -> int:
        return len(self.model.state_dict()["assemblies"])

    def typed_head_count(self) -> int:
        return 0

    def reward_observation_count(self) -> int:
        return 0

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]:
        return (PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,)


@dataclass
class G5Facade:
    model: TypedFunctionalHeadSystem
    condition: ConfirmatoryCondition = ConfirmatoryCondition.G5_TYPED

    @classmethod
    def create(cls) -> G5Facade:
        return cls(TypedFunctionalHeadSystem())

    @classmethod
    def restore(cls, state: dict[str, Any]) -> G5Facade:
        return cls(TypedFunctionalHeadSystem.from_typed_state_dict(state))

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None:
        self.model.observe_prediction_sequence(
            context_id,
            path,
            repetitions=repetitions,
        )

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]:
        result = self.model.rollout_prediction(
            context_id,
            cue,
            steps=3,
            suppressed_sources=suppressed_sources,
        )
        return tuple(int(row) for row in result.generated_tokens)

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None:
        del context_id
        self.model.observe_boundary_action(
            port_id,
            target,
            reward=1.0,
            alternate_targets=alternate_targets,
        )
        self.model.update_memory(f"memory:{port_id}", target)

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None:
        del context_id
        result = self.model.boundary_output(
            port_id,
            suppress_action_heads=suppressed_ports,
        )
        return int(result.target) if result.target is not None else None

    def state_dict(self) -> dict[str, Any]:
        return self.model.typed_state_dict()

    def parameter_count(self) -> int:
        return self.model.parameter_count

    def observed_count(self) -> int:
        return (
            self.model.observed_sequence_count
            + self.model.action_observation_count
            + self.model.memory_update_count
        )

    def generated_count(self) -> int:
        return (
            self.model.generated_token_count
            + self.model.boundary_output_count
        )

    def intervention_count(self) -> int:
        return self.model.intervention_count

    def assembly_entries(self) -> int:
        return 0

    def typed_head_count(self) -> int:
        state = self.model.typed_state_dict()
        return (
            len(state["prediction_heads"])
            + len(state["action_heads"])
            + len(state["memory_heads"])
        )

    def reward_observation_count(self) -> int:
        return self.model.reward_observation_count

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]:
        return (
            PrivilegedInformation.TYPED_PREDICTION_HEAD,
            PrivilegedInformation.TYPED_BOUNDARY_HEAD,
            PrivilegedInformation.TYPED_MEMORY_HEAD,
            PrivilegedInformation.SCALAR_REWARD,
        )


FACADE_FACTORIES: dict[ConfirmatoryCondition, type[Any]] = {
    ConfirmatoryCondition.G3_RECURRENT: G3Facade,
    ConfirmatoryCondition.G4_ASSEMBLY: G4Facade,
    ConfirmatoryCondition.G5_TYPED: G5Facade,
}


def context_id(prefix: str, path: tuple[int, int, int, int]) -> str:
    return f"{prefix}:{'-'.join(str(row) for row in path)}"


def exposure_count(
    parameters: HeldoutWorldParameters,
    path: tuple[int, int, int, int],
) -> int:
    counts = dict(
        zip(
            parameters.competition_paths,
            parameters.branch_exposure_counts,
            strict=True,
        )
    )
    return counts.get(path, max(3, len(parameters.training_lag_profiles_ms)))


def train_paths(
    facade: ComparatorFacade,
    parameters: HeldoutWorldParameters,
    paths: tuple[tuple[int, int, int, int], ...],
) -> None:
    for path in dict.fromkeys(paths):
        facade.observe_path(
            context_id("sequence", path),
            path,
            exposure_count(parameters, path),
        )


def empty_rollout(
    facade: ComparatorFacade,
    parameters: HeldoutWorldParameters,
) -> tuple[int, ...]:
    if isinstance(facade, G4Facade):
        return ()
    return facade.rollout(
        context_id("sequence", parameters.main_path),
        parameters.main_path[0],
    )


def origin_and_state(
    factory: type[Any],
    parameters: HeldoutWorldParameters,
) -> tuple[bool, bool, int, int]:
    main = factory.create()
    train_paths(main, parameters, (parameters.main_path,))
    main_output = main.rollout(
        context_id("sequence", parameters.main_path),
        parameters.main_path[0],
    )
    alternate = factory.create()
    train_paths(alternate, parameters, (parameters.alternate_path,))
    alternate_output = alternate.rollout(
        context_id("sequence", parameters.alternate_path),
        parameters.alternate_path[0],
    )
    empty = factory.create()
    empty_output = empty_rollout(empty, parameters)
    origin = bool(
        main_output == parameters.main_path[1:]
        and empty_output == ()
    )
    state = bool(
        alternate_output == parameters.alternate_path[1:]
        and alternate_output != main_output
    )
    observed = main.observed_count() + alternate.observed_count()
    generated = (
        main.generated_count()
        + alternate.generated_count()
        + empty.generated_count()
    )
    return origin, state, observed, generated


def chain_evidence(
    factory: type[Any],
    parameters: HeldoutWorldParameters,
) -> tuple[bool, dict[str, float], ComparatorFacade]:
    paths = (*parameters.competition_paths, parameters.control_path)
    main_context = context_id("sequence", parameters.main_path)
    control_context = context_id("sequence", parameters.control_path)

    sham = factory.create()
    train_paths(sham, parameters, paths)
    sham_main = sham.rollout(main_context, parameters.main_path[0])
    sham_control = sham.rollout(control_context, parameters.control_path[0])

    targeted = factory.create()
    train_paths(targeted, parameters, paths)
    targeted_main = targeted.rollout(
        main_context,
        parameters.main_path[0],
        suppressed_sources=(parameters.main_path[1],),
    )

    matched = factory.create()
    train_paths(matched, parameters, paths)
    matched_control = matched.rollout(
        control_context,
        parameters.control_path[0],
        suppressed_sources=(parameters.control_path[1],),
    )
    matched_main = matched.rollout(main_context, parameters.main_path[0])

    sham_downstream = sum(row in parameters.main_path[2:] for row in sham_main)
    targeted_downstream = sum(
        row in parameters.main_path[2:] for row in targeted_main
    )
    matched_downstream = sum(
        row in parameters.main_path[2:] for row in matched_main
    )
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    passed = bool(
        sham_main == parameters.main_path[1:]
        and sham_control == parameters.control_path[1:]
        and targeted_main == (parameters.main_path[1],)
        and matched_control == (parameters.control_path[1],)
        and matched_main == parameters.main_path[1:]
        and targeted_impairment - matched_impairment >= 0.5
    )
    metrics = {
        "chain_matched_impairment": float(matched_impairment),
        "chain_targeted_impairment": float(targeted_impairment),
        "heldout_comparator_chain_main_count": float(len(sham_main)),
    }
    return passed, metrics, sham


def relation_evidence(
    factory: type[Any],
    parameters: HeldoutWorldParameters,
) -> tuple[
    bool,
    bool,
    bool,
    bool,
    dict[str, float],
    ComparatorFacade,
]:
    main_context = context_id("boundary", parameters.main_path)
    control_context = context_id("boundary", parameters.control_path)
    targets = (
        parameters.old_target,
        parameters.new_target,
        parameters.third_target,
    )
    facade = factory.create()
    for _ in range(3):
        facade.observe_boundary(
            main_context,
            parameters.main_port,
            parameters.old_target,
            tuple(row for row in targets if row != parameters.old_target),
        )
        facade.observe_boundary(
            control_context,
            parameters.control_port,
            parameters.third_target,
            (),
        )
    sham_main = facade.boundary_output(main_context, parameters.main_port)
    targeted_main = facade.boundary_output(
        main_context,
        parameters.main_port,
        suppressed_ports=(parameters.main_port,),
    )
    matched_main = facade.boundary_output(
        main_context,
        parameters.main_port,
        suppressed_ports=(parameters.control_port,),
    )
    targeted_impairment = float(sham_main is not None and targeted_main is None)
    matched_impairment = float(sham_main is not None and matched_main is None)
    boundary = bool(
        sham_main == parameters.old_target
        and targeted_main is None
        and matched_main == parameters.old_target
        and targeted_impairment - matched_impairment >= 0.5
    )

    internal_only = factory.create()
    stabilization = bool(
        sham_main == parameters.old_target
        and internal_only.boundary_output(
            main_context,
            parameters.main_port,
        )
        is None
    )

    revision_model = factory.create()
    snapshots: list[dict[str, Any]] = []
    phase_outputs: list[int | None] = []
    for target, phase_length in zip(
        parameters.contingency_cycle_targets,
        parameters.contingency_phase_lengths,
        strict=True,
    ):
        for _ in range(phase_length):
            revision_model.observe_boundary(
                main_context,
                parameters.main_port,
                target,
                tuple(row for row in targets if row != target),
            )
        snapshots.append(revision_model.state_dict())
        phase_outputs.append(
            revision_model.boundary_output(main_context, parameters.main_port)
        )
    revision = tuple(phase_outputs) == parameters.contingency_cycle_targets

    stable = factory.create()
    stable_target = parameters.contingency_cycle_targets[0]
    for _ in range(sum(parameters.contingency_phase_lengths)):
        stable.observe_boundary(
            main_context,
            parameters.main_port,
            stable_target,
            tuple(row for row in targets if row != stable_target),
        )
    revision = bool(
        revision
        and stable.boundary_output(main_context, parameters.main_port)
        == stable_target
    )

    reentry_outputs = tuple(
        factory.restore(state).boundary_output(main_context, parameters.main_port)
        for state in snapshots
    )
    reset_output = factory.create().boundary_output(
        main_context,
        parameters.main_port,
    )
    reentry = reentry_outputs == parameters.contingency_cycle_targets
    persistence = bool(
        reentry_outputs
        and reentry_outputs[0] == parameters.contingency_cycle_targets[0]
        and reset_output is None
    )
    metrics = {
        "boundary_matched_impairment": matched_impairment,
        "boundary_targeted_impairment": targeted_impairment,
        "heldout_comparator_phase_match_fraction": float(
            sum(
                observed == expected
                for observed, expected in zip(
                    phase_outputs,
                    parameters.contingency_cycle_targets,
                    strict=True,
                )
            )
            / len(phase_outputs)
        ),
        "heldout_comparator_reentry_match_fraction": float(
            sum(
                observed == expected
                for observed, expected in zip(
                    reentry_outputs,
                    parameters.contingency_cycle_targets,
                    strict=True,
                )
            )
            / len(reentry_outputs)
        ),
    }
    return (
        boundary,
        stabilization,
        revision,
        reentry and persistence,
        metrics,
        revision_model,
    )


def taxonomy_result(condition: ConfirmatoryCondition) -> bool:
    return condition is not ConfirmatoryCondition.G5_TYPED


def run_condition(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    try:
        factory = FACADE_FACTORIES[condition]
    except KeyError as error:
        raise ValueError(f"not a held-out comparator: {condition.value}") from error
    parameters.validate()
    started = time.perf_counter()
    origin, state, origin_observed, origin_generated = origin_and_state(
        factory,
        parameters,
    )
    chain, chain_metrics, chain_model = chain_evidence(factory, parameters)
    (
        boundary,
        stabilization,
        revision,
        reentry_and_persistence,
        relation_metrics,
        relation_model,
    ) = relation_evidence(factory, parameters)
    taxonomy = taxonomy_result(condition)
    passed = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: origin,
        EvidenceDomain.STATE_DEPENDENCE: state,
        EvidenceDomain.AUTONOMOUS_CHAIN: chain,
        EvidenceDomain.BOUNDARY_EFFECT: boundary,
        EvidenceDomain.RELATION_STABILIZATION: stabilization,
        EvidenceDomain.REVERSAL_REACQUISITION: revision,
        EvidenceDomain.RELATION_REENTRY: reentry_and_persistence,
        EvidenceDomain.PERSISTENCE_LOCUS: reentry_and_persistence,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: taxonomy,
    }
    metrics = {
        **chain_metrics,
        **relation_metrics,
        "branch_count": float(parameters.branch_count),
        "contingency_change_count": float(parameters.contingency_change_count),
        "self_confirmation_violations": 0.0,
        "taxonomy_hash_match": float(taxonomy),
        "world_specification_hash_prefix": float(
            int(parameters.specification_hash()[:12], 16)
        ),
    }
    records = build_result_records(parameters, condition, passed, metrics)
    observed = (
        origin_observed
        + chain_model.observed_count()
        + relation_model.observed_count()
    )
    generated = (
        origin_generated
        + chain_model.generated_count()
        + relation_model.generated_count()
    )
    privilege = relation_model.privileged_information()
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=condition,
        observed_training_events=observed,
        generated_internal_events=generated,
        persistent_state_entries=(
            chain_model.parameter_count()
            + relation_model.parameter_count()
        ),
        intervention_count=(
            chain_model.intervention_count()
            + relation_model.intervention_count()
        ),
        parameter_count=(
            chain_model.parameter_count()
            + relation_model.parameter_count()
        ),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=False,
        ordinary_field_threshold_crossings=0,
        threshold_bypassed=True,
        explicit_assembly_entries=max(
            chain_model.assembly_entries(),
            relation_model.assembly_entries(),
        ),
        typed_head_count=max(
            chain_model.typed_head_count(),
            relation_model.typed_head_count(),
        ),
        scalar_reward_observations=(
            chain_model.reward_observation_count()
            + relation_model.reward_observation_count()
        ),
        privileged_information=privilege,
    )
    semantic_hash = digest(
        {
            "condition": condition.value,
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
        condition=condition,
        world_specification_hash=parameters.specification_hash(),
        records=records,
        resource=resource,
        semantic_hash=semantic_hash,
    )
    execution.validate()
    return execution

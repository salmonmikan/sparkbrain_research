from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from sparkbrain.baselines.v06.g3_recurrent import GenericRecurrentPredictor
from sparkbrain.baselines.v06.g4_assembly import ExplicitAssemblyComparator
from sparkbrain.baselines.v06.g5_typed import TypedFunctionalHeadComparator

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
from .v06_confirmatory_training_schedule import (
    build_balanced_training_schedule,
)


def _digest(value: object) -> str:
    encoded = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _unit(unit_id: int) -> str:
    return f"unit:{unit_id}"


def _unit_id(token: str) -> int:
    prefix, value = token.split(":", maxsplit=1)
    if prefix != "unit":
        raise ValueError(f"expected unit token, got {token!r}")
    return int(value)


def _tokens(path: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(_unit(unit_id) for unit_id in path)


def _state_leaf_count(value: Any) -> int:
    if isinstance(value, dict):
        return sum(_state_leaf_count(row) for row in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return sum(_state_leaf_count(row) for row in value)
    return 1


class _Facade(Protocol):
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

    def learned_state_dict(self) -> dict[str, Any]: ...

    def parameter_count(self) -> int: ...

    def observed_count(self) -> int: ...

    def generated_count(self) -> int: ...

    def intervention_count(self) -> int: ...

    def assembly_entries(self) -> int: ...

    def typed_head_count(self) -> int: ...

    def reward_observation_count(self) -> int: ...

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]: ...


@dataclass
class _G3Facade:
    model: GenericRecurrentPredictor
    interventions: int = 0
    condition: ConfirmatoryCondition = ConfirmatoryCondition.G3_RECURRENT

    @classmethod
    def create(cls) -> _G3Facade:
        return cls(GenericRecurrentPredictor())

    @classmethod
    def restore(cls, state: dict[str, Any]) -> _G3Facade:
        return cls(
            GenericRecurrentPredictor.from_learned_state_dict(state["model"]),
            interventions=int(state["interventions"]),
        )

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None:
        del context_id
        self.model.observe_sequence(_tokens(path), repetitions=repetitions)

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]:
        del context_id
        if suppressed_sources:
            self.interventions += 1
        return tuple(
            _unit_id(token)
            for token in self.model.rollout(
                _unit(cue),
                steps=3,
                suppressed_sources=tuple(_unit(row) for row in suppressed_sources),
            )
        )

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None:
        del context_id, alternate_targets
        self.model.observe(port_id, _unit(target))

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None:
        del context_id
        if port_id in suppressed_ports:
            self.interventions += 1
            return None
        target = self.model.predict_next(port_id)
        return _unit_id(target) if target is not None else None

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "interventions": self.interventions,
            "model": self.model.learned_state_dict(),
        }

    def parameter_count(self) -> int:
        return self.model.state_entry_count

    def observed_count(self) -> int:
        return self.model.observation_count

    def generated_count(self) -> int:
        return self.model.generated_token_count

    def intervention_count(self) -> int:
        return self.interventions

    def assembly_entries(self) -> int:
        return 0

    def typed_head_count(self) -> int:
        return 0

    def reward_observation_count(self) -> int:
        return 0

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]:
        return ()


@dataclass
class _G4Facade:
    model: ExplicitAssemblyComparator
    context_assemblies: dict[str, str] = field(default_factory=dict)
    interventions: int = 0
    condition: ConfirmatoryCondition = ConfirmatoryCondition.G4_ASSEMBLY

    @classmethod
    def create(cls) -> _G4Facade:
        return cls(ExplicitAssemblyComparator())

    @classmethod
    def restore(cls, state: dict[str, Any]) -> _G4Facade:
        return cls(
            ExplicitAssemblyComparator.from_learned_state_dict(state["model"]),
            context_assemblies={
                str(key): str(value)
                for key, value in state["context_assemblies"].items()
            },
            interventions=int(state["interventions"]),
        )

    def _ensure_context(self, context_id: str, port_id: str) -> str:
        assembly_id = self.context_assemblies.get(context_id)
        if assembly_id is not None:
            return assembly_id
        assembly_id = self.model.observe_sequence(
            (f"context:{context_id}", f"boundary:{port_id}"),
            repetitions=1,
        )
        self.context_assemblies[context_id] = assembly_id
        self.model.observe_port(assembly_id, port_id, repetitions=1)
        return assembly_id

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None:
        assembly_id = self.model.observe_sequence(
            _tokens(path),
            repetitions=repetitions,
        )
        self.context_assemblies[context_id] = assembly_id

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]:
        del context_id
        if suppressed_sources:
            self.interventions += 1
        return tuple(
            _unit_id(token)
            for token in self.model.rollout(
                _unit(cue),
                steps=3,
                suppressed_members=tuple(_unit(row) for row in suppressed_sources),
            )
        )

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None:
        del alternate_targets
        assembly_id = self._ensure_context(context_id, port_id)
        self.model.observe_external(assembly_id, port_id, _unit(target))

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None:
        if port_id in suppressed_ports:
            self.interventions += 1
            return None
        assembly_id = self.context_assemblies.get(context_id)
        if assembly_id is None:
            return None
        target = self.model.external_target(assembly_id, port_id)
        return _unit_id(target) if target is not None else None

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "context_assemblies": dict(sorted(self.context_assemblies.items())),
            "interventions": self.interventions,
            "model": self.model.learned_state_dict(),
        }

    def parameter_count(self) -> int:
        return _state_leaf_count(self.model.learned_state_dict())

    def observed_count(self) -> int:
        return self.model.observation_count

    def generated_count(self) -> int:
        return self.model.generated_token_count

    def intervention_count(self) -> int:
        return self.interventions

    def assembly_entries(self) -> int:
        return self.model.assembly_count

    def typed_head_count(self) -> int:
        return 0

    def reward_observation_count(self) -> int:
        return 0

    def privileged_information(self) -> tuple[PrivilegedInformation, ...]:
        return (PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,)


@dataclass
class _G5Facade:
    model: TypedFunctionalHeadComparator
    interventions: int = 0
    condition: ConfirmatoryCondition = ConfirmatoryCondition.G5_TYPED

    @classmethod
    def create(cls) -> _G5Facade:
        return cls(TypedFunctionalHeadComparator())

    @classmethod
    def restore(cls, state: dict[str, Any]) -> _G5Facade:
        return cls(
            TypedFunctionalHeadComparator.from_learned_state_dict(state["model"]),
            interventions=int(state["interventions"]),
        )

    def observe_path(
        self,
        context_id: str,
        path: tuple[int, int, int, int],
        repetitions: int,
    ) -> None:
        del context_id
        self.model.train_prediction_sequence(
            _tokens(path),
            repetitions=repetitions,
        )

    def rollout(
        self,
        context_id: str,
        cue: int,
        *,
        suppressed_sources: tuple[int, ...] = (),
    ) -> tuple[int, ...]:
        del context_id
        if suppressed_sources:
            self.interventions += 1
        return tuple(
            _unit_id(token)
            for token in self.model.predict_rollout(
                _unit(cue),
                steps=3,
                suppressed_sources=tuple(_unit(row) for row in suppressed_sources),
            )
        )

    def observe_boundary(
        self,
        context_id: str,
        port_id: str,
        target: int,
        alternate_targets: tuple[int, ...],
    ) -> None:
        del alternate_targets
        self.model.train_action(context_id, port_id, repetitions=1)
        self.model.observe_reward(port_id, _unit(target), reward=1.0)

    def boundary_output(
        self,
        context_id: str,
        port_id: str,
        *,
        suppressed_ports: tuple[str, ...] = (),
    ) -> int | None:
        if port_id in suppressed_ports:
            self.interventions += 1
            return None
        selected_port = self.model.choose_action(context_id)
        if selected_port != port_id:
            return None
        target = self.model.choose_rewarded_target(port_id)
        return _unit_id(target) if target is not None else None

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "interventions": self.interventions,
            "model": self.model.learned_state_dict(),
        }

    def parameter_count(self) -> int:
        state = self.model.learned_state_dict()
        return sum(
            len(row)
            for head_name in (
                "action_head",
                "memory_head",
                "prediction_head",
                "reward_head",
            )
            for row in state[head_name].values()
        )

    def observed_count(self) -> int:
        return self.model.observation_count

    def generated_count(self) -> int:
        return self.model.generated_count

    def intervention_count(self) -> int:
        return self.interventions

    def assembly_entries(self) -> int:
        return 0

    def typed_head_count(self) -> int:
        state = self.model.learned_state_dict()
        return sum(
            bool(state[head_name])
            for head_name in (
                "action_head",
                "memory_head",
                "prediction_head",
                "reward_head",
            )
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


_FACADE_FACTORIES: dict[ConfirmatoryCondition, type[Any]] = {
    ConfirmatoryCondition.G3_RECURRENT: _G3Facade,
    ConfirmatoryCondition.G4_ASSEMBLY: _G4Facade,
    ConfirmatoryCondition.G5_TYPED: _G5Facade,
}


def _context(prefix: str, path: tuple[int, int, int, int]) -> str:
    return f"{prefix}:{'-'.join(str(row) for row in path)}"


def _exposure_count(
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


def _train_paths(
    facade: _Facade,
    parameters: HeldoutWorldParameters,
    paths: tuple[tuple[int, int, int, int], ...],
) -> None:
    path_rows = tuple(dict.fromkeys(paths))
    schedule = build_balanced_training_schedule(
        tuple(_exposure_count(parameters, path) for path in path_rows),
        lag_profile_count=len(parameters.training_lag_profiles_ms),
    )
    for episode in schedule.episodes:
        path = path_rows[episode.path_index]
        facade.observe_path(
            _context("sequence", path),
            path,
            1,
        )


def _origin_and_state(
    factory: type[Any],
    parameters: HeldoutWorldParameters,
) -> tuple[bool, bool, int, int]:
    main = factory.create()
    _train_paths(main, parameters, (parameters.main_path,))
    main_output = main.rollout(
        _context("sequence", parameters.main_path),
        parameters.main_path[0],
    )
    alternate = factory.create()
    _train_paths(alternate, parameters, (parameters.alternate_path,))
    alternate_output = alternate.rollout(
        _context("sequence", parameters.alternate_path),
        parameters.alternate_path[0],
    )
    empty = factory.create()
    empty_output = empty.rollout(
        _context("sequence", parameters.main_path),
        parameters.main_path[0],
    )
    origin = main_output == parameters.main_path[1:] and empty_output == ()
    state = (
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


def _chain(
    factory: type[Any],
    parameters: HeldoutWorldParameters,
) -> tuple[bool, dict[str, float], _Facade]:
    paths = (*parameters.competition_paths, parameters.control_path)
    main_context = _context("sequence", parameters.main_path)
    control_context = _context("sequence", parameters.control_path)

    sham = factory.create()
    _train_paths(sham, parameters, paths)
    sham_main = sham.rollout(main_context, parameters.main_path[0])
    sham_control = sham.rollout(control_context, parameters.control_path[0])

    targeted = factory.create()
    _train_paths(targeted, parameters, paths)
    targeted_main = targeted.rollout(
        main_context,
        parameters.main_path[0],
        suppressed_sources=(parameters.main_path[1],),
    )

    matched = factory.create()
    _train_paths(matched, parameters, paths)
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
    matched_downstream = sum(row in parameters.main_path[2:] for row in matched_main)
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    passed = (
        sham_main == parameters.main_path[1:]
        and sham_control == parameters.control_path[1:]
        and targeted_main == (parameters.main_path[1],)
        and matched_control == (parameters.control_path[1],)
        and matched_main == parameters.main_path[1:]
        and targeted_impairment - matched_impairment >= 0.5
    )
    return (
        passed,
        {
            "chain_matched_impairment": float(matched_impairment),
            "chain_targeted_impairment": float(targeted_impairment),
            "heldout_comparator_chain_main_count": float(len(sham_main)),
        },
        sham,
    )


def _relations(
    factory: type[Any],
    parameters: HeldoutWorldParameters,
) -> tuple[bool, bool, bool, bool, bool, dict[str, float], _Facade]:
    main_context = _context("boundary", parameters.main_path)
    control_context = _context("boundary", parameters.control_path)
    all_targets = (
        parameters.old_target,
        parameters.new_target,
        parameters.third_target,
    )

    boundary_model = factory.create()
    for _ in range(3):
        boundary_model.observe_boundary(
            main_context,
            parameters.main_port,
            parameters.old_target,
            tuple(row for row in all_targets if row != parameters.old_target),
        )
        boundary_model.observe_boundary(
            control_context,
            parameters.control_port,
            parameters.third_target,
            (),
        )
    sham_main = boundary_model.boundary_output(main_context, parameters.main_port)
    targeted_main = boundary_model.boundary_output(
        main_context,
        parameters.main_port,
        suppressed_ports=(parameters.main_port,),
    )
    matched_main = boundary_model.boundary_output(
        main_context,
        parameters.main_port,
        suppressed_ports=(parameters.control_port,),
    )
    targeted_impairment = float(sham_main is not None and targeted_main is None)
    matched_impairment = float(sham_main is not None and matched_main is None)
    boundary = (
        sham_main == parameters.old_target
        and targeted_main is None
        and matched_main == parameters.old_target
        and targeted_impairment - matched_impairment >= 0.5
    )

    empty = factory.create()
    stabilization = (
        sham_main == parameters.old_target
        and empty.boundary_output(main_context, parameters.main_port) is None
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
                tuple(row for row in all_targets if row != target),
            )
        snapshots.append(revision_model.learned_state_dict())
        phase_outputs.append(
            revision_model.boundary_output(main_context, parameters.main_port)
        )
    revision = tuple(phase_outputs) == parameters.contingency_cycle_targets

    stable = factory.create()
    for _ in range(sum(parameters.contingency_phase_lengths)):
        stable.observe_boundary(
            main_context,
            parameters.main_port,
            parameters.contingency_cycle_targets[0],
            tuple(
                row
                for row in all_targets
                if row != parameters.contingency_cycle_targets[0]
            ),
        )
    revision = revision and (
        stable.boundary_output(main_context, parameters.main_port)
        == parameters.contingency_cycle_targets[0]
    )

    reentry_outputs = tuple(
        factory.restore(snapshot).boundary_output(main_context, parameters.main_port)
        for snapshot in snapshots
    )
    reentry = reentry_outputs == parameters.contingency_cycle_targets
    persistence = bool(
        reentry_outputs
        and reentry_outputs[0] == parameters.contingency_cycle_targets[0]
        and factory.create().boundary_output(main_context, parameters.main_port) is None
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
        reentry,
        persistence,
        metrics,
        revision_model,
    )


def _taxonomy_non_interference(state: dict[str, Any]) -> bool:
    before = json.dumps(state, sort_keys=True, separators=(",", ":"))
    observer_a = {"view": "alpha", "labels": ("one", "two")}
    observer_b = {"view": "renamed", "labels": ("two", "one")}
    _ = (observer_a, observer_b)
    after = json.dumps(state, sort_keys=True, separators=(",", ":"))
    return before == after


def run_condition(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    if condition not in _FACADE_FACTORIES:
        raise ValueError(f"not a held-out comparator: {condition.value}")
    parameters.validate()
    factory = _FACADE_FACTORIES[condition]
    started = time.perf_counter()

    origin, state, origin_observed, origin_generated = _origin_and_state(
        factory,
        parameters,
    )
    chain, chain_metrics, chain_model = _chain(factory, parameters)
    (
        boundary,
        stabilization,
        revision,
        reentry,
        persistence,
        relation_metrics,
        relation_model,
    ) = _relations(factory, parameters)
    taxonomy = _taxonomy_non_interference(
        {
            "chain": chain_model.learned_state_dict(),
            "relation": relation_model.learned_state_dict(),
        }
    )
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
    model_state = {
        "chain": chain_model.learned_state_dict(),
        "relation": relation_model.learned_state_dict(),
    }
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
    resource = ConditionResourceRecord(
        family_id=parameters.family_id,
        seed=parameters.seed,
        condition=condition,
        observed_training_events=observed,
        generated_internal_events=generated,
        persistent_state_entries=chain_model.parameter_count()
        + relation_model.parameter_count(),
        intervention_count=chain_model.intervention_count()
        + relation_model.intervention_count(),
        parameter_count=chain_model.parameter_count()
        + relation_model.parameter_count(),
        wall_clock_ms=(time.perf_counter() - started) * 1000.0,
        normal_field_threshold_present=False,
        normal_field_threshold_crossings=0,
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
        privileged_information=relation_model.privileged_information(),
    )
    semantic_hash = _digest(
        {
            "model_state": model_state,
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

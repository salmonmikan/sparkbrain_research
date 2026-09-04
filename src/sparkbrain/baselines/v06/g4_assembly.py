from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.evaluation.v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryResultRecord,
    EvidenceDomain,
)

from .common import (
    QUALIFICATION_FAMILIES,
    QUALIFICATION_SEEDS,
    ComparatorWorldEvidence,
    ComparatorWorldParameters,
    world_parameters,
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


@dataclass(frozen=True, slots=True)
class AssemblyComparatorConfig:
    retention: float = 0.8
    maximum_rollout_steps: int = 8

    def validate(self) -> None:
        if not 0.0 < self.retention <= 1.0:
            raise ValueError("retention must be in (0, 1]")
        if self.maximum_rollout_steps < 1:
            raise ValueError("maximum_rollout_steps must be positive")


@dataclass(slots=True)
class ExplicitAssemblyPrototype:
    assembly_id: str
    members: tuple[str, ...]
    observation_count: int = 0

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExplicitAssemblyComparator:
    """Comparator whose runtime cognition explicitly depends on Assembly IDs.

    A complete observed sequence is stored as a named prototype. A cue selects
    an Assembly, and its stored members drive rollout. Boundary and external
    consequence state are keyed by that Assembly ID. This is intentionally the
    mechanism that the Primary v0.6 path forbids.
    """

    def __init__(self, config: AssemblyComparatorConfig | None = None) -> None:
        self.config = config or AssemblyComparatorConfig()
        self.config.validate()
        self._assemblies: dict[str, ExplicitAssemblyPrototype] = {}
        self._cue_index: dict[str, set[str]] = {}
        self._port_scores: dict[str, dict[str, float]] = {}
        self._external_scores: dict[tuple[str, str], dict[str, float]] = {}
        self.observation_count = 0
        self.generated_token_count = 0

    def observe_sequence(
        self,
        members: tuple[str, ...],
        *,
        repetitions: int = 1,
    ) -> str:
        if repetitions < 1:
            raise ValueError("repetitions must be positive")
        if len(members) < 2 or any(not member for member in members):
            raise ValueError("an Assembly requires at least two non-empty members")
        assembly_id = f"assembly:{_digest({'members': list(members)})[:24]}"
        prototype = self._assemblies.get(assembly_id)
        if prototype is None:
            prototype = ExplicitAssemblyPrototype(
                assembly_id=assembly_id,
                members=members,
            )
            self._assemblies[assembly_id] = prototype
            self._cue_index.setdefault(members[0], set()).add(assembly_id)
        elif prototype.members != members:
            raise RuntimeError("Assembly hash collision")
        prototype.observation_count += repetitions
        self.observation_count += repetitions * (len(members) - 1)
        return assembly_id

    def activate(self, cue: str) -> str | None:
        candidates = self._cue_index.get(cue, set())
        if not candidates:
            return None
        return min(
            candidates,
            key=lambda assembly_id: (
                -self._assemblies[assembly_id].observation_count,
                assembly_id,
            ),
        )

    def rollout(
        self,
        cue: str,
        *,
        steps: int,
        suppressed_members: tuple[str, ...] = (),
    ) -> tuple[str, ...]:
        if steps < 0 or steps > self.config.maximum_rollout_steps:
            raise ValueError("rollout steps exceed the configured bound")
        assembly_id = self.activate(cue)
        if assembly_id is None:
            return ()
        generated: list[str] = []
        for member in self._assemblies[assembly_id].members[1 : steps + 1]:
            generated.append(member)
            self.generated_token_count += 1
            if member in suppressed_members:
                break
        return tuple(generated)

    def observe_port(
        self,
        assembly_id: str,
        port_id: str,
        *,
        repetitions: int = 1,
    ) -> None:
        if assembly_id not in self._assemblies:
            raise ValueError("unknown Assembly")
        if not port_id or repetitions < 1:
            raise ValueError("port and repetitions must be valid")
        for _ in range(repetitions):
            row = self._port_scores.setdefault(assembly_id, {})
            for candidate in tuple(row):
                row[candidate] *= self.config.retention
            row[port_id] = row.get(port_id, 0.0) + 1.0
            self.observation_count += 1

    def emit_port(
        self,
        assembly_id: str,
        *,
        suppressed_assembly_ids: tuple[str, ...] = (),
    ) -> str | None:
        if assembly_id in suppressed_assembly_ids:
            return None
        row = self._port_scores.get(assembly_id)
        if not row:
            return None
        self.generated_token_count += 1
        return min(row, key=lambda port: (-row[port], port))

    def observe_external(
        self,
        assembly_id: str,
        port_id: str,
        target: str,
    ) -> None:
        if assembly_id not in self._assemblies:
            raise ValueError("unknown Assembly")
        if not port_id or not target:
            raise ValueError("port and target must be non-empty")
        row = self._external_scores.setdefault((assembly_id, port_id), {})
        for candidate in tuple(row):
            row[candidate] *= self.config.retention
        row[target] = row.get(target, 0.0) + 1.0
        self.observation_count += 1

    def external_target(self, assembly_id: str, port_id: str) -> str | None:
        row = self._external_scores.get((assembly_id, port_id))
        if not row:
            return None
        self.generated_token_count += 1
        return min(row, key=lambda target: (-row[target], target))

    def external_confidence(
        self,
        assembly_id: str,
        port_id: str,
        target: str,
    ) -> float | None:
        row = self._external_scores.get((assembly_id, port_id))
        if not row:
            return None
        total = sum(row.values())
        if total <= 0:
            return None
        return row.get(target, 0.0) / total

    @property
    def assembly_count(self) -> int:
        return len(self._assemblies)

    @property
    def external_relation_count(self) -> int:
        return sum(len(row) for row in self._external_scores.values())

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "assemblies": {
                assembly_id: prototype.state_dict()
                for assembly_id, prototype in sorted(self._assemblies.items())
            },
            "config": asdict(self.config),
            "cue_index": {
                cue: sorted(assembly_ids)
                for cue, assembly_ids in sorted(self._cue_index.items())
            },
            "external_scores": {
                f"{assembly_id}|{port_id}": dict(sorted(row.items()))
                for (assembly_id, port_id), row in sorted(
                    self._external_scores.items()
                )
            },
            "observation_count": self.observation_count,
            "port_scores": {
                assembly_id: dict(sorted(row.items()))
                for assembly_id, row in sorted(self._port_scores.items())
            },
        }

    def state_dict(self) -> dict[str, Any]:
        return {
            **self.learned_state_dict(),
            "generated_token_count": self.generated_token_count,
        }

    @classmethod
    def from_learned_state_dict(
        cls,
        state: dict[str, Any],
    ) -> ExplicitAssemblyComparator:
        model = cls(AssemblyComparatorConfig(**state["config"]))
        model._assemblies = {
            str(assembly_id): ExplicitAssemblyPrototype(
                assembly_id=str(row["assembly_id"]),
                members=tuple(str(member) for member in row["members"]),
                observation_count=int(row["observation_count"]),
            )
            for assembly_id, row in state["assemblies"].items()
        }
        model._cue_index = {
            str(cue): {str(assembly_id) for assembly_id in assembly_ids}
            for cue, assembly_ids in state["cue_index"].items()
        }
        model._port_scores = {
            str(assembly_id): {
                str(port): float(score) for port, score in row.items()
            }
            for assembly_id, row in state["port_scores"].items()
        }
        external_scores: dict[tuple[str, str], dict[str, float]] = {}
        for key, row in state["external_scores"].items():
            assembly_id, port_id = str(key).split("|", maxsplit=1)
            external_scores[(assembly_id, port_id)] = {
                str(target): float(score) for target, score in row.items()
            }
        model._external_scores = external_scores
        model.observation_count = int(state["observation_count"])
        return model

    def state_hash(self) -> str:
        return _digest(self.state_dict())


def _unit(unit_id: int) -> str:
    return f"unit:{unit_id}"


def _tokens(path: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(_unit(unit_id) for unit_id in path)


def _trained(
    paths: tuple[tuple[int, ...], ...],
) -> tuple[ExplicitAssemblyComparator, dict[tuple[int, ...], str]]:
    model = ExplicitAssemblyComparator()
    assembly_ids = {
        path: model.observe_sequence(_tokens(path), repetitions=3)
        for path in paths
    }
    return model, assembly_ids


def _origin_and_state(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, bool, dict[str, float]]:
    main, _ = _trained((parameters.main_path,))
    alternate, _ = _trained((parameters.alternate_path,))
    no_history = ExplicitAssemblyComparator()
    main_observations = main.observation_count
    main_tokens = main.rollout(_unit(parameters.main_path[0]), steps=3)
    alternate_tokens = alternate.rollout(
        _unit(parameters.alternate_path[0]),
        steps=3,
    )
    no_history_tokens = no_history.rollout(
        _unit(parameters.main_path[0]),
        steps=3,
    )
    origin = (
        main_tokens == _tokens(parameters.main_path[1:])
        and main.observation_count == main_observations
        and main_tokens[0] != _unit(parameters.main_path[0])
    )
    state = (
        alternate_tokens == _tokens(parameters.alternate_path[1:])
        and alternate_tokens != main_tokens
        and no_history_tokens == ()
    )
    return (
        origin,
        state,
        {
            "g4_assembly_count": float(main.assembly_count),
            "g4_origin_generated_count": float(len(main_tokens)),
            "g4_state_alternate_generated_count": float(len(alternate_tokens)),
        },
    )


def _chain(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, dict[str, float]]:
    model, _ = _trained((parameters.main_path, parameters.control_path))
    main_cue = _unit(parameters.main_path[0])
    control_cue = _unit(parameters.control_path[0])
    sham = model.rollout(main_cue, steps=3)
    targeted = model.rollout(
        main_cue,
        steps=3,
        suppressed_members=(_unit(parameters.main_path[1]),),
    )
    matched = model.rollout(
        main_cue,
        steps=3,
        suppressed_members=(_unit(parameters.control_path[1]),),
    )
    matched_control = model.rollout(
        control_cue,
        steps=3,
        suppressed_members=(_unit(parameters.control_path[1]),),
    )
    sham_downstream = sum(
        token in _tokens(parameters.main_path[2:]) for token in sham
    )
    targeted_downstream = sum(
        token in _tokens(parameters.main_path[2:]) for token in targeted
    )
    matched_downstream = sum(
        token in _tokens(parameters.main_path[2:]) for token in matched
    )
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    passed = (
        sham == _tokens(parameters.main_path[1:])
        and targeted == (_unit(parameters.main_path[1]),)
        and matched == sham
        and matched_control == (_unit(parameters.control_path[1]),)
        and targeted_impairment - matched_impairment >= 0.5
    )
    return (
        passed,
        {
            "g4_chain_matched_impairment": matched_impairment,
            "g4_chain_selective_effect": targeted_impairment - matched_impairment,
            "g4_chain_targeted_impairment": targeted_impairment,
        },
    )


def _boundary(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, dict[str, float]]:
    model, assembly_ids = _trained(
        (parameters.main_path, parameters.control_path)
    )
    main_id = assembly_ids[parameters.main_path]
    control_id = assembly_ids[parameters.control_path]
    model.observe_port(main_id, parameters.main_port, repetitions=3)
    model.observe_port(control_id, parameters.control_port, repetitions=3)
    sham = model.emit_port(main_id)
    targeted = model.emit_port(main_id, suppressed_assembly_ids=(main_id,))
    matched = model.emit_port(main_id, suppressed_assembly_ids=(control_id,))
    matched_control = model.emit_port(
        control_id,
        suppressed_assembly_ids=(control_id,),
    )
    targeted_impairment = float(sham is not None and targeted is None)
    matched_impairment = float(sham is not None and matched != sham)
    passed = (
        sham == parameters.main_port
        and targeted is None
        and matched == parameters.main_port
        and matched_control is None
        and targeted_impairment - matched_impairment >= 0.5
    )
    return (
        passed,
        {
            "g4_boundary_matched_impairment": matched_impairment,
            "g4_boundary_selective_effect": (
                targeted_impairment - matched_impairment
            ),
            "g4_boundary_targeted_impairment": targeted_impairment,
        },
    )


@dataclass(frozen=True, slots=True)
class _RelationEvidence:
    stabilization: bool
    reversal: bool
    reentry: bool
    persistence: bool
    learned_state: dict[str, Any]
    metrics: dict[str, float]


def _relation(parameters: ComparatorWorldParameters) -> _RelationEvidence:
    model, assembly_ids = _trained((parameters.main_path,))
    assembly_id = assembly_ids[parameters.main_path]
    model.observe_port(assembly_id, parameters.main_port, repetitions=3)
    old_target = _unit(parameters.old_target)
    new_target = _unit(parameters.new_target)
    for _ in range(3):
        model.observe_external(assembly_id, parameters.main_port, old_target)
    acquired = model.external_target(assembly_id, parameters.main_port)
    acquired_confidence = model.external_confidence(
        assembly_id,
        parameters.main_port,
        old_target,
    )
    learned_state = model.learned_state_dict()

    reversal_crossing = 0
    for episode in range(1, 4):
        model.observe_external(assembly_id, parameters.main_port, new_target)
        if (
            reversal_crossing == 0
            and model.external_target(assembly_id, parameters.main_port)
            == new_target
        ):
            reversal_crossing = episode
    reversed_target = model.external_target(assembly_id, parameters.main_port)
    reversed_new_confidence = model.external_confidence(
        assembly_id,
        parameters.main_port,
        new_target,
    )

    return_crossing = 0
    for episode in range(1, 4):
        model.observe_external(assembly_id, parameters.main_port, old_target)
        if (
            return_crossing == 0
            and model.external_target(assembly_id, parameters.main_port)
            == old_target
        ):
            return_crossing = episode
    returned_target = model.external_target(assembly_id, parameters.main_port)
    returned_old_confidence = model.external_confidence(
        assembly_id,
        parameters.main_port,
        old_target,
    )

    stable, stable_ids = _trained((parameters.main_path,))
    stable_id = stable_ids[parameters.main_path]
    stable.observe_port(stable_id, parameters.main_port, repetitions=3)
    for _ in range(9):
        stable.observe_external(stable_id, parameters.main_port, old_target)
    stable_passed = (
        stable.external_target(stable_id, parameters.main_port) == old_target
        and stable.external_relation_count == 1
    )

    internal_only, internal_ids = _trained((parameters.main_path,))
    internal_id = internal_ids[parameters.main_path]
    internal_only.observe_port(
        internal_id,
        parameters.main_port,
        repetitions=3,
    )
    before_observations = internal_only.observation_count
    internal_result = internal_only.external_target(
        internal_id,
        parameters.main_port,
    )
    internal_safe = (
        internal_result is None
        and internal_only.observation_count == before_observations
    )

    transplanted = ExplicitAssemblyComparator.from_learned_state_dict(
        learned_state
    )
    reset = ExplicitAssemblyComparator()
    unrelated, unrelated_ids = _trained((parameters.control_path,))
    unrelated_id = unrelated_ids[parameters.control_path]
    unrelated.observe_port(
        unrelated_id,
        parameters.control_port,
        repetitions=3,
    )
    for _ in range(3):
        unrelated.observe_external(
            unrelated_id,
            parameters.control_port,
            new_target,
        )
    persistence = (
        transplanted.external_target(assembly_id, parameters.main_port)
        == old_target
        and reset.activate(_unit(parameters.main_path[0])) is None
        and unrelated.activate(_unit(parameters.main_path[0])) is None
    )
    stabilization = (
        acquired == old_target
        and acquired_confidence is not None
        and math.isclose(acquired_confidence, 1.0)
        and internal_safe
    )
    reversal = (
        reversed_target == new_target
        and returned_target == old_target
        and reversal_crossing > 0
        and return_crossing > 0
        and reversed_new_confidence is not None
        and returned_old_confidence is not None
        and reversed_new_confidence > 0.5
        and returned_old_confidence > 0.5
        and stable_passed
    )
    reentry = (
        acquired == old_target
        and reversed_target == new_target
        and returned_target == old_target
    )
    return _RelationEvidence(
        stabilization=stabilization,
        reversal=reversal,
        reentry=reentry,
        persistence=persistence,
        learned_state=learned_state,
        metrics={
            "g4_acquired_old_confidence": float(acquired_confidence or 0.0),
            "g4_reacquisition_crossing_episode": float(return_crossing),
            "g4_reversed_new_confidence": float(reversed_new_confidence or 0.0),
            "g4_reversal_crossing_episode": float(reversal_crossing),
            "g4_returned_old_confidence": float(returned_old_confidence or 0.0),
            "g4_stable_relation_count": float(stable.external_relation_count),
        },
    )


def _generation_safety(parameters: ComparatorWorldParameters) -> tuple[int, bool]:
    model, _ = _trained((parameters.main_path, parameters.control_path))
    before = model.learned_state_dict()
    observations = model.observation_count
    model.rollout(_unit(parameters.main_path[0]), steps=3)
    model.rollout(_unit(parameters.control_path[0]), steps=3)
    return model.observation_count - observations, model.learned_state_dict() == before


def _taxonomy_passed(state: dict[str, Any]) -> bool:
    before = json.dumps(state, sort_keys=True, separators=(",", ":"))
    observer_view_a = {"assembly-view": "alpha", "function-view": "beta"}
    observer_view_b = {"renamed-view": "beta", "other-view": "alpha"}
    _ = (observer_view_a, observer_view_b)
    after = json.dumps(state, sort_keys=True, separators=(",", ":"))
    return before == after


def evaluate_world(family_id: str, seed: int) -> ComparatorWorldEvidence:
    parameters = world_parameters(family_id, seed)
    origin, state, origin_metrics = _origin_and_state(parameters)
    chain, chain_metrics = _chain(parameters)
    boundary, boundary_metrics = _boundary(parameters)
    relation = _relation(parameters)
    violations, state_unchanged = _generation_safety(parameters)
    taxonomy = _taxonomy_passed(relation.learned_state)
    domain_values = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: origin,
        EvidenceDomain.STATE_DEPENDENCE: state,
        EvidenceDomain.AUTONOMOUS_CHAIN: chain,
        EvidenceDomain.BOUNDARY_EFFECT: boundary,
        EvidenceDomain.RELATION_STABILIZATION: relation.stabilization,
        EvidenceDomain.REVERSAL_REACQUISITION: relation.reversal,
        EvidenceDomain.RELATION_REENTRY: relation.reentry,
        EvidenceDomain.PERSISTENCE_LOCUS: relation.persistence,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: taxonomy,
    }
    metrics = {
        **origin_metrics,
        **chain_metrics,
        **boundary_metrics,
        **relation.metrics,
        "g4_generation_preserved_learned_state": float(state_unchanged),
        "self_confirmation_violations": float(violations),
        "taxonomy_hash_match": float(taxonomy),
    }
    return ComparatorWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.G4_ASSEMBLY,
        passed_domains=tuple(
            domain for domain in EvidenceDomain if domain_values[domain]
        ),
        metrics=tuple(sorted(metrics.items())),
    )


@dataclass(frozen=True, slots=True)
class G4QualificationGrid:
    worlds: tuple[ComparatorWorldEvidence, ...]
    records: tuple[ConfirmatoryResultRecord, ...]

    @property
    def passed_world_count(self) -> int:
        return sum(row.all_passed for row in self.worlds)

    @property
    def complete(self) -> bool:
        return (
            len(self.worlds)
            == len(QUALIFICATION_FAMILIES) * len(QUALIFICATION_SEEDS)
            and len(self.records) == len(self.worlds) * len(EvidenceDomain)
            and self.passed_world_count == len(self.worlds)
        )

    def state_dict(self) -> dict[str, Any]:
        return {
            "complete": self.complete,
            "passed_world_count": self.passed_world_count,
            "record_count": len(self.records),
            "world_count": len(self.worlds),
            "worlds": [row.state_dict() for row in self.worlds],
        }


def run_condition(
    family_id: str,
    seed: int,
) -> tuple[ConfirmatoryResultRecord, ...]:
    return evaluate_world(family_id, seed).records()


def run_qualification_grid() -> G4QualificationGrid:
    worlds = tuple(
        evaluate_world(family_id, seed)
        for family_id in QUALIFICATION_FAMILIES
        for seed in QUALIFICATION_SEEDS
    )
    records = tuple(record for world in worlds for record in world.records())
    return G4QualificationGrid(worlds=worlds, records=records)

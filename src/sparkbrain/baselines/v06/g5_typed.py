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
class TypedHeadConfig:
    retention: float = 0.8
    maximum_rollout_steps: int = 8

    def validate(self) -> None:
        if not 0.0 < self.retention <= 1.0:
            raise ValueError("retention must be in (0, 1]")
        if self.maximum_rollout_steps < 1:
            raise ValueError("maximum_rollout_steps must be positive")


class TypedFunctionalHeadComparator:
    """Comparator with explicit prediction, action, reward, and memory heads.

    This is intentionally outside the Primary runtime. It receives typed
    training calls and a privileged scalar reward. Success here shows what a
    human-designed functional decomposition can solve; it cannot count as
    Primary SparkBrain support.
    """

    def __init__(self, config: TypedHeadConfig | None = None) -> None:
        self.config = config or TypedHeadConfig()
        self.config.validate()
        self.prediction_head: dict[str, dict[str, float]] = {}
        self.action_head: dict[str, dict[str, float]] = {}
        self.reward_head: dict[str, dict[str, float]] = {}
        self.memory_head: dict[str, dict[str, int]] = {}
        self.observation_count = 0
        self.generated_count = 0
        self.reward_observation_count = 0

    def _typed_update(
        self,
        head: dict[str, dict[str, float]],
        source: str,
        target: str,
        amount: float,
    ) -> None:
        if not source or not target:
            raise ValueError("typed-head source and target must be non-empty")
        if not math.isfinite(amount):
            raise ValueError("typed-head update amount must be finite")
        row = head.setdefault(source, {})
        for candidate in tuple(row):
            row[candidate] *= self.config.retention
        row[target] = row.get(target, 0.0) + amount

    @staticmethod
    def _best(head: dict[str, dict[str, float]], source: str) -> str | None:
        row = head.get(source)
        if not row:
            return None
        return min(row, key=lambda target: (-row[target], target))

    def train_prediction_sequence(
        self,
        tokens: tuple[str, ...],
        *,
        repetitions: int = 1,
    ) -> None:
        if repetitions < 1 or len(tokens) < 2:
            raise ValueError("prediction training requires a sequence and repetitions")
        for _ in range(repetitions):
            for source, target in zip(tokens, tokens[1:], strict=False):
                self._typed_update(self.prediction_head, source, target, 1.0)
                self.observation_count += 1

    def predict_rollout(
        self,
        cue: str,
        *,
        steps: int,
        suppressed_sources: tuple[str, ...] = (),
    ) -> tuple[str, ...]:
        if steps < 0 or steps > self.config.maximum_rollout_steps:
            raise ValueError("prediction rollout exceeds the configured bound")
        current = cue
        generated: list[str] = []
        for _ in range(steps):
            if current in suppressed_sources:
                break
            target = self._best(self.prediction_head, current)
            if target is None:
                break
            generated.append(target)
            self.generated_count += 1
            current = target
        return tuple(generated)

    def train_action(
        self,
        terminal: str,
        port_id: str,
        *,
        repetitions: int = 1,
    ) -> None:
        if repetitions < 1:
            raise ValueError("action repetitions must be positive")
        for _ in range(repetitions):
            self._typed_update(self.action_head, terminal, port_id, 1.0)
            self.observation_count += 1

    def choose_action(
        self,
        terminal: str,
        *,
        suppressed_terminals: tuple[str, ...] = (),
    ) -> str | None:
        if terminal in suppressed_terminals:
            return None
        result = self._best(self.action_head, terminal)
        if result is not None:
            self.generated_count += 1
        return result

    def observe_reward(
        self,
        port_id: str,
        external_target: str,
        *,
        reward: float,
    ) -> None:
        if not math.isfinite(reward):
            raise ValueError("reward must be finite")
        self._typed_update(
            self.reward_head,
            port_id,
            external_target,
            reward,
        )
        memory = self.memory_head.setdefault(port_id, {})
        memory[external_target] = memory.get(external_target, 0) + 1
        self.observation_count += 1
        self.reward_observation_count += 1

    def choose_rewarded_target(self, port_id: str) -> str | None:
        result = self._best(self.reward_head, port_id)
        if result is not None:
            self.generated_count += 1
        return result

    def reward_confidence(self, port_id: str, target: str) -> float | None:
        row = self.reward_head.get(port_id)
        if not row:
            return None
        denominator = sum(abs(value) for value in row.values())
        if denominator <= 0:
            return None
        return row.get(target, 0.0) / denominator

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "action_head": {
                source: dict(sorted(row.items()))
                for source, row in sorted(self.action_head.items())
            },
            "config": asdict(self.config),
            "memory_head": {
                source: dict(sorted(row.items()))
                for source, row in sorted(self.memory_head.items())
            },
            "observation_count": self.observation_count,
            "prediction_head": {
                source: dict(sorted(row.items()))
                for source, row in sorted(self.prediction_head.items())
            },
            "reward_head": {
                source: dict(sorted(row.items()))
                for source, row in sorted(self.reward_head.items())
            },
            "reward_observation_count": self.reward_observation_count,
        }

    def state_dict(self) -> dict[str, Any]:
        return {
            **self.learned_state_dict(),
            "generated_count": self.generated_count,
        }

    @classmethod
    def from_learned_state_dict(
        cls,
        state: dict[str, Any],
    ) -> TypedFunctionalHeadComparator:
        model = cls(TypedHeadConfig(**state["config"]))
        model.action_head = _float_head(state["action_head"])
        model.prediction_head = _float_head(state["prediction_head"])
        model.reward_head = _float_head(state["reward_head"])
        model.memory_head = {
            str(source): {
                str(target): int(count) for target, count in row.items()
            }
            for source, row in state["memory_head"].items()
        }
        model.observation_count = int(state["observation_count"])
        model.reward_observation_count = int(state["reward_observation_count"])
        return model

    def state_hash(self) -> str:
        return _digest(self.state_dict())


def _float_head(value: dict[str, Any]) -> dict[str, dict[str, float]]:
    return {
        str(source): {
            str(target): float(score) for target, score in row.items()
        }
        for source, row in value.items()
    }


def _unit(unit_id: int) -> str:
    return f"unit:{unit_id}"


def _tokens(path: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(_unit(unit_id) for unit_id in path)


def _trained_prediction(
    paths: tuple[tuple[int, ...], ...],
) -> TypedFunctionalHeadComparator:
    model = TypedFunctionalHeadComparator()
    for path in paths:
        model.train_prediction_sequence(_tokens(path), repetitions=3)
    return model


def _origin_and_state(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, bool, dict[str, float]]:
    main = _trained_prediction((parameters.main_path,))
    alternate = _trained_prediction((parameters.alternate_path,))
    no_history = TypedFunctionalHeadComparator()
    before = main.observation_count
    main_tokens = main.predict_rollout(_unit(parameters.main_path[0]), steps=3)
    alternate_tokens = alternate.predict_rollout(
        _unit(parameters.alternate_path[0]),
        steps=3,
    )
    no_history_tokens = no_history.predict_rollout(
        _unit(parameters.main_path[0]),
        steps=3,
    )
    origin = (
        main_tokens == _tokens(parameters.main_path[1:])
        and main.observation_count == before
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
            "g5_origin_generated_count": float(len(main_tokens)),
            "g5_prediction_head_entry_count": float(
                sum(len(row) for row in main.prediction_head.values())
            ),
        },
    )


def _chain(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, dict[str, float]]:
    model = _trained_prediction(
        (parameters.main_path, parameters.control_path)
    )
    main_cue = _unit(parameters.main_path[0])
    control_cue = _unit(parameters.control_path[0])
    sham = model.predict_rollout(main_cue, steps=3)
    targeted = model.predict_rollout(
        main_cue,
        steps=3,
        suppressed_sources=(_unit(parameters.main_path[1]),),
    )
    matched = model.predict_rollout(
        main_cue,
        steps=3,
        suppressed_sources=(_unit(parameters.control_path[1]),),
    )
    matched_control = model.predict_rollout(
        control_cue,
        steps=3,
        suppressed_sources=(_unit(parameters.control_path[1]),),
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
            "g5_chain_matched_impairment": matched_impairment,
            "g5_chain_selective_effect": targeted_impairment - matched_impairment,
            "g5_chain_targeted_impairment": targeted_impairment,
        },
    )


def _boundary(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, dict[str, float]]:
    model = _trained_prediction(
        (parameters.main_path, parameters.control_path)
    )
    main_terminal = _unit(parameters.main_path[-1])
    control_terminal = _unit(parameters.control_path[-1])
    model.train_action(main_terminal, parameters.main_port, repetitions=3)
    model.train_action(control_terminal, parameters.control_port, repetitions=3)
    sham = model.choose_action(main_terminal)
    targeted = model.choose_action(
        main_terminal,
        suppressed_terminals=(main_terminal,),
    )
    matched = model.choose_action(
        main_terminal,
        suppressed_terminals=(control_terminal,),
    )
    matched_control = model.choose_action(
        control_terminal,
        suppressed_terminals=(control_terminal,),
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
            "g5_boundary_matched_impairment": matched_impairment,
            "g5_boundary_selective_effect": (
                targeted_impairment - matched_impairment
            ),
            "g5_boundary_targeted_impairment": targeted_impairment,
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
    model = _trained_prediction((parameters.main_path,))
    terminal = _unit(parameters.main_path[-1])
    model.train_action(terminal, parameters.main_port, repetitions=3)
    old_target = _unit(parameters.old_target)
    new_target = _unit(parameters.new_target)
    for _ in range(3):
        model.observe_reward(
            parameters.main_port,
            old_target,
            reward=1.0,
        )
    acquired = model.choose_rewarded_target(parameters.main_port)
    acquired_confidence = model.reward_confidence(
        parameters.main_port,
        old_target,
    )
    learned_state = model.learned_state_dict()

    reversal_crossing = 0
    for episode in range(1, 4):
        model.observe_reward(
            parameters.main_port,
            new_target,
            reward=1.0,
        )
        if (
            reversal_crossing == 0
            and model.choose_rewarded_target(parameters.main_port) == new_target
        ):
            reversal_crossing = episode
    reversed = model.choose_rewarded_target(parameters.main_port)
    reversed_confidence = model.reward_confidence(
        parameters.main_port,
        new_target,
    )

    return_crossing = 0
    for episode in range(1, 4):
        model.observe_reward(
            parameters.main_port,
            old_target,
            reward=1.0,
        )
        if (
            return_crossing == 0
            and model.choose_rewarded_target(parameters.main_port) == old_target
        ):
            return_crossing = episode
    returned = model.choose_rewarded_target(parameters.main_port)
    returned_confidence = model.reward_confidence(
        parameters.main_port,
        old_target,
    )

    stable = TypedFunctionalHeadComparator()
    for _ in range(9):
        stable.observe_reward(parameters.main_port, old_target, reward=1.0)
    stable_passed = (
        stable.choose_rewarded_target(parameters.main_port) == old_target
        and len(stable.reward_head[parameters.main_port]) == 1
    )

    internal_only = TypedFunctionalHeadComparator()
    before = internal_only.learned_state_dict()
    internal_result = internal_only.choose_rewarded_target(parameters.main_port)
    internal_safe = (
        internal_result is None
        and internal_only.learned_state_dict() == before
    )

    transplanted = TypedFunctionalHeadComparator.from_learned_state_dict(
        learned_state
    )
    reset = TypedFunctionalHeadComparator()
    unrelated = TypedFunctionalHeadComparator()
    unrelated.observe_reward(
        parameters.control_port,
        new_target,
        reward=1.0,
    )
    persistence = (
        transplanted.choose_rewarded_target(parameters.main_port) == old_target
        and reset.choose_rewarded_target(parameters.main_port) is None
        and unrelated.choose_rewarded_target(parameters.main_port) is None
    )
    stabilization = (
        acquired == old_target
        and acquired_confidence is not None
        and math.isclose(acquired_confidence, 1.0)
        and internal_safe
    )
    reversal = (
        reversed == new_target
        and returned == old_target
        and reversal_crossing > 0
        and return_crossing > 0
        and reversed_confidence is not None
        and returned_confidence is not None
        and reversed_confidence > 0.5
        and returned_confidence > 0.5
        and stable_passed
    )
    reentry = (
        acquired == old_target
        and reversed == new_target
        and returned == old_target
    )
    return _RelationEvidence(
        stabilization=stabilization,
        reversal=reversal,
        reentry=reentry,
        persistence=persistence,
        learned_state=learned_state,
        metrics={
            "g5_acquired_old_confidence": float(acquired_confidence or 0.0),
            "g5_reacquisition_crossing_episode": float(return_crossing),
            "g5_reversed_new_confidence": float(reversed_confidence or 0.0),
            "g5_reversal_crossing_episode": float(reversal_crossing),
            "g5_returned_old_confidence": float(returned_confidence or 0.0),
            "g5_reward_observation_count": float(model.reward_observation_count),
            "g5_stable_reward_target_count": float(
                len(stable.reward_head[parameters.main_port])
            ),
        },
    )


def _generation_safety(parameters: ComparatorWorldParameters) -> tuple[int, bool]:
    model = _trained_prediction(
        (parameters.main_path, parameters.control_path)
    )
    before = model.learned_state_dict()
    observations = model.observation_count
    model.predict_rollout(_unit(parameters.main_path[0]), steps=3)
    model.predict_rollout(_unit(parameters.control_path[0]), steps=3)
    return model.observation_count - observations, model.learned_state_dict() == before


def _taxonomy_passed(state: dict[str, Any]) -> bool:
    before = json.dumps(state, sort_keys=True, separators=(",", ":"))
    observer_view_a = {"prediction-view": "alpha", "action-view": "beta"}
    observer_view_b = {"memory-view": "beta", "reward-view": "alpha"}
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
        "g5_generation_preserved_learned_state": float(state_unchanged),
        "self_confirmation_violations": float(violations),
        "taxonomy_hash_match": float(taxonomy),
    }
    return ComparatorWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.G5_TYPED,
        passed_domains=tuple(
            domain for domain in EvidenceDomain if domain_values[domain]
        ),
        metrics=tuple(sorted(metrics.items())),
    )


@dataclass(frozen=True, slots=True)
class G5QualificationGrid:
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


def run_qualification_grid() -> G5QualificationGrid:
    worlds = tuple(
        evaluate_world(family_id, seed)
        for family_id in QUALIFICATION_FAMILIES
        for seed in QUALIFICATION_SEEDS
    )
    records = tuple(record for world in worlds for record in world.records())
    return G5QualificationGrid(worlds=worlds, records=records)

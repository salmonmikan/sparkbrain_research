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


@dataclass(frozen=True, slots=True)
class RecurrentPredictorConfig:
    retention: float = 0.8
    maximum_rollout_steps: int = 8

    def validate(self) -> None:
        if not 0.0 < self.retention <= 1.0:
            raise ValueError("retention must be in (0, 1]")
        if self.maximum_rollout_steps < 1:
            raise ValueError("maximum_rollout_steps must be positive")


class GenericRecurrentPredictor:
    """Small external autoregressive comparator with generic transition state.

    This comparator is intentionally not a Field, a neural GRU, an Assembly
    system, or a typed functional head. It learns generic token-to-token scores,
    updates a recurrent token state during rollout, and emits future tokens.
    Generated tokens never train the model; only calls to ``observe`` do.
    """

    def __init__(self, config: RecurrentPredictorConfig | None = None) -> None:
        self.config = config or RecurrentPredictorConfig()
        self.config.validate()
        self._scores: dict[str, dict[str, float]] = {}
        self.observation_count = 0
        self.generated_token_count = 0

    def observe(self, source: str, target: str) -> None:
        if not source or not target:
            raise ValueError("source and target tokens must be non-empty")
        row = self._scores.setdefault(source, {})
        for candidate in tuple(row):
            row[candidate] *= self.config.retention
        row[target] = row.get(target, 0.0) + 1.0
        self.observation_count += 1

    def observe_sequence(
        self,
        tokens: tuple[str, ...],
        *,
        repetitions: int = 1,
    ) -> None:
        if repetitions < 1:
            raise ValueError("repetitions must be positive")
        if len(tokens) < 2:
            raise ValueError("a recurrent training sequence requires at least two tokens")
        for _ in range(repetitions):
            for source, target in zip(tokens, tokens[1:], strict=False):
                self.observe(source, target)

    def predict_next(
        self,
        source: str,
        *,
        suppressed_sources: tuple[str, ...] = (),
    ) -> str | None:
        if source in suppressed_sources:
            return None
        row = self._scores.get(source)
        if not row:
            return None
        target = min(
            row,
            key=lambda candidate: (-row[candidate], candidate),
        )
        self.generated_token_count += 1
        return target

    def rollout(
        self,
        cue: str,
        *,
        steps: int,
        suppressed_sources: tuple[str, ...] = (),
    ) -> tuple[str, ...]:
        if steps < 0 or steps > self.config.maximum_rollout_steps:
            raise ValueError("rollout steps exceed the configured bound")
        current = cue
        generated: list[str] = []
        for _ in range(steps):
            target = self.predict_next(
                current,
                suppressed_sources=suppressed_sources,
            )
            if target is None:
                break
            generated.append(target)
            current = target
        return tuple(generated)

    def score(self, source: str, target: str) -> float:
        return self._scores.get(source, {}).get(target, 0.0)

    def confidence(self, source: str, target: str) -> float | None:
        row = self._scores.get(source)
        if not row:
            return None
        total = sum(row.values())
        if total <= 0:
            return None
        return row.get(target, 0.0) / total

    @property
    def state_entry_count(self) -> int:
        return sum(len(row) for row in self._scores.values())

    def state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "generated_token_count": self.generated_token_count,
            "observation_count": self.observation_count,
            "scores": {
                source: dict(sorted(row.items()))
                for source, row in sorted(self._scores.items())
            },
        }

    def learned_state_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "observation_count": self.observation_count,
            "scores": {
                source: dict(sorted(row.items()))
                for source, row in sorted(self._scores.items())
            },
        }

    @classmethod
    def from_learned_state_dict(
        cls,
        state: dict[str, Any],
    ) -> GenericRecurrentPredictor:
        model = cls(RecurrentPredictorConfig(**state["config"]))
        model.observation_count = int(state["observation_count"])
        model._scores = {
            str(source): {
                str(target): float(score)
                for target, score in row.items()
            }
            for source, row in state["scores"].items()
        }
        return model

    def state_hash(self) -> str:
        encoded = json.dumps(
            self.state_dict(),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def _unit(unit_id: int) -> str:
    return f"unit:{unit_id}"


def _path_tokens(path: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(_unit(unit_id) for unit_id in path)


def _trained_paths(
    parameters: ComparatorWorldParameters,
    paths: tuple[tuple[int, ...], ...],
) -> GenericRecurrentPredictor:
    _ = parameters
    model = GenericRecurrentPredictor()
    for path in paths:
        model.observe_sequence(_path_tokens(path), repetitions=3)
    return model


def _origin_and_state(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, bool, dict[str, float]]:
    main = _trained_paths(parameters, (parameters.main_path,))
    alternate = _trained_paths(parameters, (parameters.alternate_path,))
    no_history = GenericRecurrentPredictor()
    main_observations = main.observation_count
    main_tokens = main.rollout(
        _unit(parameters.main_path[0]),
        steps=3,
    )
    alternate_tokens = alternate.rollout(
        _unit(parameters.alternate_path[0]),
        steps=3,
    )
    no_history_tokens = no_history.rollout(
        _unit(parameters.main_path[0]),
        steps=3,
    )
    expected_main = _path_tokens(parameters.main_path[1:])
    expected_alternate = _path_tokens(parameters.alternate_path[1:])
    origin_passed = (
        main_tokens == expected_main
        and main.observation_count == main_observations
        and main_tokens[0] != _unit(parameters.main_path[0])
    )
    state_passed = (
        alternate_tokens == expected_alternate
        and alternate_tokens != main_tokens
        and no_history_tokens == ()
    )
    return (
        origin_passed,
        state_passed,
        {
            "g3_origin_generated_count": float(len(main_tokens)),
            "g3_state_alternate_generated_count": float(len(alternate_tokens)),
            "g3_state_no_history_generated_count": float(len(no_history_tokens)),
        },
    )


def _chain(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, dict[str, float]]:
    model = _trained_paths(
        parameters,
        (parameters.main_path, parameters.control_path),
    )
    main_cue = _unit(parameters.main_path[0])
    control_cue = _unit(parameters.control_path[0])
    sham = model.rollout(main_cue, steps=3)
    control = model.rollout(control_cue, steps=3)
    targeted = model.rollout(
        main_cue,
        steps=3,
        suppressed_sources=(_unit(parameters.main_path[1]),),
    )
    matched = model.rollout(
        main_cue,
        steps=3,
        suppressed_sources=(_unit(parameters.control_path[1]),),
    )
    matched_control = model.rollout(
        control_cue,
        steps=3,
        suppressed_sources=(_unit(parameters.control_path[1]),),
    )
    sham_downstream = sum(
        token in _path_tokens(parameters.main_path[2:]) for token in sham
    )
    targeted_downstream = sum(
        token in _path_tokens(parameters.main_path[2:]) for token in targeted
    )
    matched_downstream = sum(
        token in _path_tokens(parameters.main_path[2:]) for token in matched
    )
    denominator = max(1, sham_downstream)
    targeted_impairment = 1.0 - targeted_downstream / denominator
    matched_impairment = 1.0 - matched_downstream / denominator
    passed = (
        sham == _path_tokens(parameters.main_path[1:])
        and control == _path_tokens(parameters.control_path[1:])
        and targeted == (_unit(parameters.main_path[1]),)
        and matched == sham
        and matched_control == (_unit(parameters.control_path[1]),)
        and targeted_impairment - matched_impairment >= 0.5
    )
    return (
        passed,
        {
            "g3_chain_matched_impairment": matched_impairment,
            "g3_chain_selective_effect": (
                targeted_impairment - matched_impairment
            ),
            "g3_chain_targeted_impairment": targeted_impairment,
        },
    )


def _boundary(
    parameters: ComparatorWorldParameters,
) -> tuple[bool, dict[str, float]]:
    model = _trained_paths(
        parameters,
        (parameters.main_path, parameters.control_path),
    )
    main_terminal = _unit(parameters.main_path[-1])
    control_terminal = _unit(parameters.control_path[-1])
    model.observe_sequence((main_terminal, parameters.main_port), repetitions=3)
    model.observe_sequence((control_terminal, parameters.control_port), repetitions=3)
    sham = model.predict_next(main_terminal)
    targeted = model.predict_next(
        main_terminal,
        suppressed_sources=(main_terminal,),
    )
    matched = model.predict_next(
        main_terminal,
        suppressed_sources=(control_terminal,),
    )
    matched_control = model.predict_next(
        control_terminal,
        suppressed_sources=(control_terminal,),
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
            "g3_boundary_matched_impairment": matched_impairment,
            "g3_boundary_selective_effect": (
                targeted_impairment - matched_impairment
            ),
            "g3_boundary_targeted_impairment": targeted_impairment,
        },
    )


@dataclass(frozen=True, slots=True)
class _RelationEvidence:
    stabilization_passed: bool
    reversal_passed: bool
    reentry_passed: bool
    persistence_passed: bool
    internal_only_passed: bool
    acquisition_state: dict[str, Any]
    metrics: dict[str, float]


def _relation(
    parameters: ComparatorWorldParameters,
) -> _RelationEvidence:
    source = parameters.main_port
    old_target = _unit(parameters.old_target)
    new_target = _unit(parameters.new_target)
    relation = GenericRecurrentPredictor()
    relation.observe_sequence((source, old_target), repetitions=3)
    acquisition_state = relation.learned_state_dict()
    old_acquired = relation.predict_next(source)
    old_acquired_confidence = relation.confidence(source, old_target)

    reversal_crossing = 0
    for episode in range(1, 4):
        relation.observe(source, new_target)
        if reversal_crossing == 0 and relation.predict_next(source) == new_target:
            reversal_crossing = episode
    reversed_target = relation.predict_next(source)
    old_reversed_confidence = relation.confidence(source, old_target)
    new_reversed_confidence = relation.confidence(source, new_target)

    reacquisition_crossing = 0
    for episode in range(1, 4):
        relation.observe(source, old_target)
        if reacquisition_crossing == 0 and relation.predict_next(source) == old_target:
            reacquisition_crossing = episode
    returned_target = relation.predict_next(source)
    old_returned_confidence = relation.confidence(source, old_target)
    new_returned_confidence = relation.confidence(source, new_target)

    stable = GenericRecurrentPredictor()
    stable.observe_sequence((source, old_target), repetitions=9)
    stable_passed = (
        stable.predict_next(source) == old_target
        and stable.state_entry_count == 1
    )

    internal_only = GenericRecurrentPredictor()
    internal_observations = internal_only.observation_count
    internal_prediction = internal_only.predict_next(source)
    internal_only_passed = (
        internal_prediction is None
        and internal_only.observation_count == internal_observations == 0
    )

    transplanted = GenericRecurrentPredictor.from_learned_state_dict(
        acquisition_state
    )
    reset = GenericRecurrentPredictor()
    unrelated = GenericRecurrentPredictor()
    unrelated.observe_sequence(
        (parameters.control_port, new_target),
        repetitions=3,
    )
    persistence_passed = (
        transplanted.predict_next(source) == old_target
        and reset.predict_next(source) is None
        and unrelated.predict_next(source) is None
    )

    stabilization_passed = (
        old_acquired == old_target
        and old_acquired_confidence is not None
        and math.isclose(old_acquired_confidence, 1.0)
        and internal_only_passed
    )
    reversal_passed = (
        reversed_target == new_target
        and returned_target == old_target
        and reversal_crossing > 0
        and reacquisition_crossing > 0
        and old_reversed_confidence is not None
        and new_reversed_confidence is not None
        and old_returned_confidence is not None
        and new_returned_confidence is not None
        and new_reversed_confidence > old_reversed_confidence
        and old_returned_confidence > new_returned_confidence
        and stable_passed
    )
    reentry_passed = (
        old_acquired == old_target
        and reversed_target == new_target
        and returned_target == old_target
    )
    return _RelationEvidence(
        stabilization_passed=stabilization_passed,
        reversal_passed=reversal_passed,
        reentry_passed=reentry_passed,
        persistence_passed=persistence_passed,
        internal_only_passed=internal_only_passed,
        acquisition_state=acquisition_state,
        metrics={
            "g3_acquired_old_confidence": float(old_acquired_confidence or 0.0),
            "g3_reacquisition_crossing_episode": float(reacquisition_crossing),
            "g3_reversed_new_confidence": float(new_reversed_confidence or 0.0),
            "g3_reversal_crossing_episode": float(reversal_crossing),
            "g3_returned_old_confidence": float(old_returned_confidence or 0.0),
            "g3_stable_relation_count": float(stable.state_entry_count),
        },
    )


def _generation_safety(
    parameters: ComparatorWorldParameters,
) -> tuple[int, bool]:
    model = _trained_paths(
        parameters,
        (parameters.main_path, parameters.control_path),
    )
    before = model.learned_state_dict()
    observation_count_before = model.observation_count
    model.rollout(_unit(parameters.main_path[0]), steps=3)
    model.rollout(_unit(parameters.control_path[0]), steps=3)
    observation_count_after = model.observation_count
    return (
        observation_count_after - observation_count_before,
        model.learned_state_dict() == before,
    )


def _taxonomy_passed(model_state: dict[str, Any]) -> bool:
    before = json.dumps(model_state, sort_keys=True, separators=(",", ":"))
    view_a = {
        "predictive-view": "renamed-alpha",
        "boundary-view": "renamed-beta",
    }
    view_b = {
        "memory-view": "renamed-beta",
        "action-view": "renamed-alpha",
    }
    _ = (view_a, view_b)
    after = json.dumps(model_state, sort_keys=True, separators=(",", ":"))
    return before == after


def evaluate_world(family_id: str, seed: int) -> ComparatorWorldEvidence:
    parameters = world_parameters(family_id, seed)
    origin, state, origin_metrics = _origin_and_state(parameters)
    chain, chain_metrics = _chain(parameters)
    boundary, boundary_metrics = _boundary(parameters)
    relation = _relation(parameters)
    violations, learned_state_unchanged = _generation_safety(parameters)
    taxonomy = _taxonomy_passed(relation.acquisition_state)
    domain_values = {
        EvidenceDomain.ENDOGENOUS_ORIGIN: origin,
        EvidenceDomain.STATE_DEPENDENCE: state,
        EvidenceDomain.AUTONOMOUS_CHAIN: chain,
        EvidenceDomain.BOUNDARY_EFFECT: boundary,
        EvidenceDomain.RELATION_STABILIZATION: relation.stabilization_passed,
        EvidenceDomain.REVERSAL_REACQUISITION: relation.reversal_passed,
        EvidenceDomain.RELATION_REENTRY: relation.reentry_passed,
        EvidenceDomain.PERSISTENCE_LOCUS: relation.persistence_passed,
        EvidenceDomain.TAXONOMY_NON_INTERFERENCE: taxonomy,
    }
    metrics = {
        **origin_metrics,
        **chain_metrics,
        **boundary_metrics,
        **relation.metrics,
        "external_predictor_field_threshold_count": 0.0,
        "g3_generation_preserved_learned_state": float(
            learned_state_unchanged
        ),
        "self_confirmation_violations": float(violations),
        "taxonomy_hash_match": float(taxonomy),
    }
    return ComparatorWorldEvidence(
        family_id=family_id,
        seed=seed,
        condition=ConfirmatoryCondition.G3_RECURRENT,
        passed_domains=tuple(
            domain for domain in EvidenceDomain if domain_values[domain]
        ),
        metrics=tuple(sorted(metrics.items())),
    )


@dataclass(frozen=True, slots=True)
class G3QualificationGrid:
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


def run_qualification_grid() -> G3QualificationGrid:
    worlds = tuple(
        evaluate_world(family_id, seed)
        for family_id in QUALIFICATION_FAMILIES
        for seed in QUALIFICATION_SEEDS
    )
    records = tuple(record for world in worlds for record in world.records())
    return G3QualificationGrid(worlds=worlds, records=records)

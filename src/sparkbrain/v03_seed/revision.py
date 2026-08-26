from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType

from .coalition import C14_BOUNDED_MODE, CoalitionGate
from .contracts import IgnitionDecision
from .evidence import EvidenceLedger
from .revision_worlds import (
    BELIEF_ORDER,
    C15_SCHEMA_VERSION,
    FixtureEvidence,
    adapt_fixture_entity_key,
    add_fixture_evidence,
    canonical_json_bytes,
    fixture_evidence_to_record,
)

_FORBIDDEN_PRODUCTION_KEYS = {
    "answer",
    "decision_justified",
    "belief_index",
    "episode_seed",
    "evaluator",
    "expected",
    "label",
    "scenario_tags",
    "split",
    "sufficient_information",
    "target",
    "test_only",
    "transition_target",
    "truth",
    "truth_belief",
    "previous_truth_belief",
    "recovery_opportunity",
    "update_required",
}


class TransitionKind(StrEnum):
    MAINTAIN = "maintain"
    UPDATE = "update"
    RECOVER = "recover"
    INSUFFICIENT_INFORMATION = "insufficient_information"


def _finite_probability(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite probability")
    result = float(value)
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must be a finite probability in [0, 1]")
    return result


def _finite_nonnegative(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be finite and non-negative")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def _nonempty(value: object, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _reject_forbidden(value: object, *, path: str = "observation") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in _FORBIDDEN_PRODUCTION_KEYS:
                raise ValueError(f"forbidden production field at {path}.{key}")
            _reject_forbidden(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_forbidden(child, path=f"{path}[{index}]")


@dataclass(frozen=True, slots=True)
class RevisionTarget:
    """Evaluator-only target derived from truth history, never model output."""

    truth_belief: str
    previous_truth_belief: str
    transition: TransitionKind
    sufficient_information: bool
    recovery_opportunity: bool
    schema_version: str = C15_SCHEMA_VERSION

    def validate(self) -> None:
        if self.schema_version != C15_SCHEMA_VERSION:
            raise ValueError("unsupported revision target schema")
        if self.truth_belief not in BELIEF_ORDER or self.previous_truth_belief not in BELIEF_ORDER:
            raise ValueError("target beliefs must use the frozen belief order")
        if not isinstance(self.transition, TransitionKind):
            raise ValueError("transition must be a TransitionKind")
        if not isinstance(self.sufficient_information, bool) or not isinstance(
            self.recovery_opportunity, bool
        ):
            raise ValueError("target flags must be booleans")
        if self.sufficient_information == (
            self.transition is TransitionKind.INSUFFICIENT_INFORMATION
        ):
            raise ValueError("target sufficiency and transition are inconsistent")
        if self.recovery_opportunity != (self.transition is TransitionKind.RECOVER):
            raise ValueError("recovery_opportunity must match a recover transition")
        if self.transition is TransitionKind.MAINTAIN and (
            self.truth_belief != self.previous_truth_belief
        ):
            raise ValueError("maintain requires an unchanged truth belief")
        if self.transition in {TransitionKind.UPDATE, TransitionKind.RECOVER} and (
            self.truth_belief == self.previous_truth_belief
        ):
            raise ValueError("update and recover require a changed truth belief")

    def to_canonical_json(self) -> str:
        self.validate()
        return canonical_json_bytes(
            {
                "previous_truth_belief": self.previous_truth_belief,
                "recovery_opportunity": self.recovery_opportunity,
                "schema_version": self.schema_version,
                "sufficient_information": self.sufficient_information,
                "transition": self.transition.value,
                "truth_belief": self.truth_belief,
            }
        ).decode()

    @classmethod
    def from_canonical_json(cls, payload: str) -> RevisionTarget:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("revision target must be valid JSON") from exc
        expected = {
            "previous_truth_belief",
            "recovery_opportunity",
            "schema_version",
            "sufficient_information",
            "transition",
            "truth_belief",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("revision target has unexpected fields")
        try:
            transition = TransitionKind(value["transition"])
        except (TypeError, ValueError) as exc:
            raise ValueError("revision target transition is invalid") from exc
        target = cls(
            truth_belief=value["truth_belief"],
            previous_truth_belief=value["previous_truth_belief"],
            transition=transition,
            sufficient_information=value["sufficient_information"],
            recovery_opportunity=value["recovery_opportunity"],
            schema_version=value["schema_version"],
        )
        target.validate()
        if target.to_canonical_json() != payload:
            raise ValueError("revision target is not strict canonical JSON")
        return target

    @classmethod
    def from_truth_history(
        cls,
        truth_history: Sequence[str],
        *,
        truth_belief: str,
        causal_source_count: int,
        causal_group_count: int,
    ) -> RevisionTarget:
        if not truth_history:
            raise ValueError("assessment requires an established truth history")
        if (
            any(item not in BELIEF_ORDER for item in truth_history)
            or truth_belief not in BELIEF_ORDER
        ):
            raise ValueError("truth history must use the frozen belief order")
        if (
            not isinstance(causal_source_count, int)
            or isinstance(causal_source_count, bool)
            or not isinstance(causal_group_count, int)
            or isinstance(causal_group_count, bool)
            or causal_source_count < 0
            or causal_group_count < 0
        ):
            raise ValueError("causal source/group counts must be non-negative integers")
        sufficient = causal_source_count >= 2 and causal_group_count >= 2
        previous = truth_history[-1]
        recovery = (
            sufficient
            and truth_belief != previous
            and truth_belief in truth_history[:-1]
        )
        if not sufficient:
            transition = TransitionKind.INSUFFICIENT_INFORMATION
        elif recovery:
            transition = TransitionKind.RECOVER
        elif truth_belief != previous:
            transition = TransitionKind.UPDATE
        else:
            transition = TransitionKind.MAINTAIN
        target = cls(truth_belief, previous, transition, sufficient, recovery)
        target.validate()
        return target


@dataclass(frozen=True, slots=True)
class RevisionHeadOutput:
    belief_probabilities: Mapping[str, float]
    maintain_probability: float
    update_probability: float
    recovery_probability: float
    abstention_probability: float

    def __post_init__(self) -> None:
        if not isinstance(self.belief_probabilities, Mapping):
            raise ValueError("belief_probabilities must be a mapping")
        if set(self.belief_probabilities) != set(BELIEF_ORDER):
            raise ValueError("belief_probabilities must have exact alpha/beta/gamma keys")
        probabilities = {
            key: _finite_probability(self.belief_probabilities[key], name=f"belief {key}")
            for key in BELIEF_ORDER
        }
        if not math.isclose(
            sum(probabilities.values()), 1.0, rel_tol=0.0, abs_tol=1e-12
        ):
            raise ValueError("belief probabilities must sum to one within 1e-12")
        object.__setattr__(self, "belief_probabilities", MappingProxyType(probabilities))
        for field_name in (
            "maintain_probability",
            "update_probability",
            "recovery_probability",
            "abstention_probability",
        ):
            object.__setattr__(
                self,
                field_name,
                _finite_probability(getattr(self, field_name), name=field_name),
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "abstention_probability": self.abstention_probability,
            "belief_probabilities": dict(self.belief_probabilities),
            "maintain_probability": self.maintain_probability,
            "recovery_probability": self.recovery_probability,
            "update_probability": self.update_probability,
        }

    @classmethod
    def from_dict(cls, value: object) -> RevisionHeadOutput:
        expected = {
            "abstention_probability",
            "belief_probabilities",
            "maintain_probability",
            "recovery_probability",
            "update_probability",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("revision head output has unexpected fields")
        return cls(**value)


@dataclass(frozen=True, slots=True)
class RevisionObservation:
    """Strict production input; evaluator truth and transition fields are impossible here."""

    entity_key: str
    time: float
    evidence: tuple[FixtureEvidence, ...]
    entity_condition: str
    heads: RevisionHeadOutput
    metadata: Mapping[str, object] = field(default_factory=dict)
    schema_version: str = C15_SCHEMA_VERSION
    _canonical_payload: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _nonempty(self.entity_key, name="entity_key")
        adapt_fixture_entity_key(
            self.entity_key, entity_condition=self.entity_condition
        )
        if self.schema_version != C15_SCHEMA_VERSION:
            raise ValueError("unsupported revision observation schema")
        if isinstance(self.time, bool) or not isinstance(self.time, (int, float)):
            raise ValueError("observation time must be finite and non-negative")
        if not math.isfinite(self.time) or self.time < 0:
            raise ValueError("observation time must be finite and non-negative")
        if not isinstance(self.evidence, tuple) or not self.evidence:
            raise ValueError("observation requires a non-empty evidence tuple")
        for row in self.evidence:
            if not isinstance(row, FixtureEvidence):
                raise ValueError("observation evidence must use FixtureEvidence")
            row.validate()
            if row.entity_key != self.entity_key:
                raise ValueError("all evidence must match the evaluated entity")
        if not isinstance(self.heads, RevisionHeadOutput):
            raise ValueError("heads must use RevisionHeadOutput")
        if not isinstance(self.metadata, Mapping):
            raise ValueError("observation metadata must be a mapping")
        _reject_forbidden(self.metadata)
        try:
            metadata_payload = canonical_json_bytes(dict(self.metadata)).decode()
        except (TypeError, ValueError) as exc:
            raise ValueError("observation metadata must be finite JSON data") from exc
        normalized_metadata = json.loads(metadata_payload)
        object.__setattr__(self, "metadata", MappingProxyType(normalized_metadata))
        object.__setattr__(
            self,
            "_canonical_payload",
            canonical_json_bytes(
                {
                    "entity_condition": self.entity_condition,
                    "entity_key": self.entity_key,
                    "evidence": [row.to_dict() for row in self.evidence],
                    "heads": self.heads.to_dict(),
                    "metadata": normalized_metadata,
                    "schema_version": self.schema_version,
                    "time": self.time,
                }
            ).decode(),
        )

    def to_canonical_json(self) -> str:
        return self._canonical_payload

    @classmethod
    def from_canonical_json(cls, payload: str) -> RevisionObservation:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("revision observation must be valid JSON") from exc
        expected = {
            "entity_condition",
            "entity_key",
            "evidence",
            "heads",
            "metadata",
            "schema_version",
            "time",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("revision observation has unexpected fields")
        if not isinstance(value["evidence"], list):
            raise ValueError("revision observation evidence must be a list")
        observation = cls(
            entity_key=value["entity_key"],
            time=value["time"],
            evidence=tuple(FixtureEvidence.from_dict(row) for row in value["evidence"]),
            entity_condition=value["entity_condition"],
            heads=RevisionHeadOutput.from_dict(value["heads"]),
            metadata=value["metadata"],
            schema_version=value["schema_version"],
        )
        if observation.to_canonical_json() != payload:
            raise ValueError("revision observation is not strict canonical JSON")
        return observation

    @property
    def input_hash(self) -> str:
        return hashlib.sha256(self.to_canonical_json().encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class RevisionBeliefSnapshot:
    activations: Mapping[str, float]
    citations: tuple[str, ...]
    entity_key: str
    history: tuple[str, ...]
    state_hash: str
    winner: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "activations": dict(self.activations),
            "citations": list(self.citations),
            "entity_key": self.entity_key,
            "history": list(self.history),
            "state_hash": self.state_hash,
            "winner": self.winner,
        }


@dataclass(slots=True)
class _EntityBeliefState:
    activations: dict[str, float]
    citations: tuple[str, ...]
    history: list[str]
    winner: str | None


class RevisionBeliefField:
    """Entity-scoped residual state with strict canonical replay."""

    def __init__(self, *, decay: float = 0.88, loser_retention: float = 0.92) -> None:
        self.decay = _finite_probability(decay, name="decay")
        self.loser_retention = _finite_probability(
            loser_retention, name="loser_retention"
        )
        self._states: dict[str, _EntityBeliefState] = {}

    def reset(self) -> None:
        self._states.clear()

    def _state(self, entity_key: str) -> _EntityBeliefState:
        _nonempty(entity_key, name="entity_key")
        return self._states.setdefault(
            entity_key,
            _EntityBeliefState({key: 0.0 for key in BELIEF_ORDER}, (), [], None),
        )

    def snapshot(self, entity_key: str) -> RevisionBeliefSnapshot:
        _nonempty(entity_key, name="entity_key")
        state = self._states.get(entity_key)
        if state is None:
            state = _EntityBeliefState(
                {key: 0.0 for key in BELIEF_ORDER}, (), [], None
            )
        body = {
            "activations": {key: state.activations[key] for key in BELIEF_ORDER},
            "citations": list(state.citations),
            "entity_key": entity_key,
            "history": list(state.history),
            "winner": state.winner,
        }
        state_hash = hashlib.sha256(canonical_json_bytes(body)).hexdigest()
        return RevisionBeliefSnapshot(
            MappingProxyType(dict(body["activations"])),  # type: ignore[arg-type]
            state.citations,
            entity_key,
            tuple(state.history),
            state_hash,
            state.winner,
        )

    def apply(
        self,
        *,
        entity_key: str,
        decision: IgnitionDecision,
        proposal_activation: float,
        citations: tuple[str, ...],
    ) -> None:
        state = self._state(entity_key)
        for belief_key in BELIEF_ORDER:
            state.activations[belief_key] *= self.decay
            if decision.ignited and belief_key != decision.belief_key:
                state.activations[belief_key] *= self.loser_retention
        if not decision.ignited or decision.belief_key is None:
            return
        state.activations[decision.belief_key] = max(
            state.activations[decision.belief_key],
            _finite_probability(proposal_activation, name="proposal_activation"),
        )
        state.winner = decision.belief_key
        state.history.append(decision.belief_key)
        state.citations = tuple(sorted(set(citations)))

    def to_canonical_json(self) -> str:
        payload = {
            "config": {
                "decay": self.decay,
                "loser_retention": self.loser_retention,
            },
            "schema_version": C15_SCHEMA_VERSION,
            "states": {
                entity: {
                    "activations": {key: state.activations[key] for key in BELIEF_ORDER},
                    "citations": list(state.citations),
                    "history": list(state.history),
                    "winner": state.winner,
                }
                for entity, state in sorted(self._states.items())
            },
        }
        return canonical_json_bytes(payload).decode()

    serialize_state = to_canonical_json

    @classmethod
    def from_canonical_json(cls, payload: str) -> RevisionBeliefField:
        try:
            value = json.loads(payload)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("belief field state must be valid JSON") from exc
        if not isinstance(value, dict) or set(value) != {"config", "schema_version", "states"}:
            raise ValueError("belief field state has unexpected fields")
        if value["schema_version"] != C15_SCHEMA_VERSION:
            raise ValueError("unsupported belief field state schema")
        config = value["config"]
        if not isinstance(config, dict) or set(config) != {"decay", "loser_retention"}:
            raise ValueError("belief field config has unexpected fields")
        result = cls(decay=config["decay"], loser_retention=config["loser_retention"])
        states = value["states"]
        if not isinstance(states, dict):
            raise ValueError("belief field states must be an object")
        for entity, raw in states.items():
            _nonempty(entity, name="entity_key")
            if not isinstance(raw, dict) or set(raw) != {
                "activations",
                "citations",
                "history",
                "winner",
            }:
                raise ValueError("belief entity state has unexpected fields")
            activations = raw["activations"]
            if not isinstance(activations, dict) or set(activations) != set(BELIEF_ORDER):
                raise ValueError("belief activations have unexpected fields")
            normalized = {
                key: _finite_nonnegative(activations[key], name=f"activation {key}")
                for key in BELIEF_ORDER
            }
            history = raw["history"]
            citations = raw["citations"]
            winner = raw["winner"]
            if not isinstance(history, list) or any(item not in BELIEF_ORDER for item in history):
                raise ValueError("belief history is invalid")
            if not isinstance(citations, list) or citations != sorted(set(citations)) or any(
                not isinstance(item, str) or not item.strip() for item in citations
            ):
                raise ValueError("belief citations are invalid")
            if winner is not None and winner not in BELIEF_ORDER:
                raise ValueError("belief winner is invalid")
            if history and winner != history[-1]:
                raise ValueError("belief winner must equal the last accepted history item")
            if not history and winner is not None:
                raise ValueError("belief winner requires accepted history")
            result._states[entity] = _EntityBeliefState(
                normalized, tuple(citations), list(history), winner
            )
        if result.to_canonical_json() != payload:
            raise ValueError("belief field state is not strict canonical JSON")
        return result

    from_serialized_state = from_canonical_json


@dataclass(frozen=True, slots=True)
class RevisionDecision:
    evaluated_entity_key: str
    ignited: bool
    belief_key: str | None
    object_key: str | None
    score: float
    margin: float
    reason: str
    citation_ids: tuple[str, ...]
    predicted_transition: TransitionKind
    proposal: IgnitionDecision
    gate_passes: tuple[IgnitionDecision, IgnitionDecision]
    state_before: RevisionBeliefSnapshot
    state_after: RevisionBeliefSnapshot
    input_hash: str


class RevisionController:
    """C15 C14-before-mutation controller with learned vetoes and entity state."""

    def __init__(
        self,
        *,
        ledger: EvidenceLedger | None = None,
        gate: CoalitionGate | None = None,
        belief_field: RevisionBeliefField | None = None,
        abstention_threshold: float = 0.5,
    ) -> None:
        self.ledger = ledger or EvidenceLedger()
        self.gate = gate or CoalitionGate()
        self.belief_field = belief_field or RevisionBeliefField()
        self.abstention_threshold = _finite_probability(
            abstention_threshold, name="abstention_threshold"
        )
        self._seen_evidence_ids: set[str] = set()

    def reset(self) -> None:
        self.ledger.reset()
        self.gate.reset()
        self.belief_field.reset()
        self._seen_evidence_ids.clear()

    def process_stage(
        self,
        observation: RevisionObservation,
        *,
        stage_role: str = "assessment",
    ) -> RevisionDecision:
        if not isinstance(observation, RevisionObservation):
            raise ValueError("observation must use RevisionObservation")
        if stage_role not in {"context", "assessment"}:
            raise ValueError("stage_role must be context or assessment")
        # Validate all immutable records before mutating ledger, gate, or belief state.
        records = tuple(
            fixture_evidence_to_record(
                row, entity_condition=observation.entity_condition
            )
            for row in observation.evidence
        )
        current_records: dict[str, object] = {}
        for record in records:
            previous_in_stage = current_records.get(record.evidence_id)
            if previous_in_stage is not None and previous_in_stage != record:
                raise ValueError("one stage cannot change an immutable evidence payload")
            current_records[record.evidence_id] = record
            if record.evidence_id in self._seen_evidence_ids:
                if self.ledger.resolve(record.evidence_id) != record:
                    raise ValueError("one evidence_id cannot change its immutable payload")
                if not self.ledger.is_active(record.evidence_id):
                    raise ValueError("a C15 stage cannot restore prior inactive evidence")

        trial_ledger = EvidenceLedger.from_serialized_state(self.ledger.serialize_state())
        trial_seen = set(self._seen_evidence_ids)
        evaluated_entity_key = adapt_fixture_entity_key(
            observation.entity_key, entity_condition=observation.entity_condition
        )
        current_ids = set(current_records)
        for prior in trial_ledger.rows(active_only=True):
            if (
                prior.entity_key == evaluated_entity_key
                and prior.evidence_id not in current_ids
            ):
                trial_ledger.deactivate(
                    prior.evidence_id,
                    at_time=float(observation.time),
                    reason="c15_stage_scope",
                )
        for evidence in observation.evidence:
            add_fixture_evidence(
                trial_ledger,
                evidence,
                entity_condition=observation.entity_condition,
                seen_evidence_ids=trial_seen,
            )

        state_before = self.belief_field.snapshot(evaluated_entity_key)
        activations = {
            (evaluated_entity_key, belief): -math.log(
                max(1.0 - observation.heads.belief_probabilities[belief], 1e-12)
            )
            for belief in BELIEF_ORDER
        }
        trial_gate = deepcopy(self.gate)
        first = trial_gate.evaluate(
            activations,
            trial_ledger,
            now=float(observation.time),
            mode=C14_BOUNDED_MODE,
        )
        second = trial_gate.evaluate(
            activations,
            trial_ledger,
            now=float(observation.time),
            mode=C14_BOUNDED_MODE,
        )
        final = (
            second
            if stage_role == "context"
            else self._apply_veto(second, observation.heads, state_before)
        )
        citations = self._proposal_citations(second)
        proposal_activation = (
            observation.heads.belief_probabilities[second.belief_key]
            if second.belief_key is not None
            else 0.0
        )
        self.belief_field.apply(
            entity_key=evaluated_entity_key,
            decision=final,
            proposal_activation=proposal_activation,
            citations=citations,
        )
        self.ledger = trial_ledger
        self.gate = trial_gate
        self._seen_evidence_ids = trial_seen
        state_after = self.belief_field.snapshot(evaluated_entity_key)
        predicted_transition = (
            self._proposal_transition(second.belief_key, state_before)
            if final.ignited
            else TransitionKind.INSUFFICIENT_INFORMATION
        )
        return RevisionDecision(
            evaluated_entity_key=evaluated_entity_key,
            ignited=final.ignited,
            belief_key=final.belief_key,
            object_key=final.object_key,
            score=final.score,
            margin=final.margin,
            reason=final.reason,
            citation_ids=citations,
            predicted_transition=predicted_transition,
            proposal=second,
            gate_passes=(first, second),
            state_before=state_before,
            state_after=state_after,
            input_hash=observation.input_hash,
        )

    def _apply_veto(
        self,
        proposal: IgnitionDecision,
        heads: RevisionHeadOutput,
        state: RevisionBeliefSnapshot,
    ) -> IgnitionDecision:
        if not proposal.ignited or proposal.belief_key is None:
            return proposal
        if heads.abstention_probability >= self.abstention_threshold:
            reason = "learned_insufficient_information"
        elif state.winner is None:
            return proposal
        else:
            transition = self._proposal_transition(proposal.belief_key, state)
            probability, reason = {
                TransitionKind.MAINTAIN: (
                    heads.maintain_probability,
                    "maintain_head_below_threshold",
                ),
                TransitionKind.RECOVER: (
                    heads.recovery_probability,
                    "recovery_head_below_threshold",
                ),
                TransitionKind.UPDATE: (
                    heads.update_probability,
                    "update_head_below_threshold",
                ),
            }[transition]
            if probability >= 0.5:
                return proposal
        return IgnitionDecision(
            False,
            None,
            None,
            proposal.score,
            proposal.margin,
            reason,
            proposal.coalitions,
        )

    @staticmethod
    def _proposal_transition(
        belief_key: str | None,
        state: RevisionBeliefSnapshot,
    ) -> TransitionKind:
        if belief_key is None:
            return TransitionKind.INSUFFICIENT_INFORMATION
        if belief_key == state.winner:
            return TransitionKind.MAINTAIN
        if belief_key in state.history[:-1]:
            return TransitionKind.RECOVER
        return TransitionKind.UPDATE

    @staticmethod
    def _proposal_citations(proposal: IgnitionDecision) -> tuple[str, ...]:
        if not proposal.coalitions:
            return ()
        for coalition in proposal.coalitions:
            if (
                coalition.belief_key == proposal.belief_key
                and coalition.object_key == proposal.object_key
            ):
                return tuple(sorted(set(coalition.support_ids)))
        return ()

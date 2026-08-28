from __future__ import annotations

import hashlib
import json
import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from typing import Any

from sparkbrain.v03_integration import V03TraceSession
from sparkbrain.v03_seed import (
    CoalitionGate,
    CoalitionGateConfig,
    EvidenceContribution,
    EvidenceLedger,
    IgnitionDecision,
    InputRecord,
    LocalCompositionalFrontend,
    OnlineConceptFormer,
    PerceptualSpark,
    PersistentBeliefField,
    SensorySample,
    StrictSymbolicOracleFrontend,
    WholeHashFrontend,
)

I0 = "I0_whole_hash"
I1 = "I1_local_compositional"
I2 = "I2_symbolic_oracle"
I3 = "I3_truth_free_revision"
E0 = "E0_global"
E1 = "E1_oracle_entity"
E2 = "E2_learned_slots"
_INPUT_TRACKS = frozenset({I0, I1, I2, I3})
_ENTITY_TRACKS = frozenset({E0, E1, E2})
_CHECKPOINT_VERSION = "0.3.1"
_EVALUATOR_KEYS = frozenset(
    {"answer", "evaluator", "gold", "label", "split", "target", "test_only", "truth"}
)


def _canonical(value: object) -> str:
    return json.dumps(
        value, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _json_copy(value: object) -> Any:
    return json.loads(_canonical(value))


def _tuple_tree(value: object) -> object:
    if isinstance(value, list):
        return tuple(_tuple_tree(item) for item in value)
    return value


def _reject_evaluator_keys(value: object, *, path: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in _EVALUATOR_KEYS:
                raise ValueError(f"forbidden evaluator field at {path}.{key}")
            _reject_evaluator_keys(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_evaluator_keys(child, path=f"{path}[{index}]")


@dataclass(frozen=True, slots=True)
class V03BrainConfig:
    """Configuration for the integrated reference runtime.

    I2 and E1 expose evaluator-provided structure and therefore require the
    explicit ``allow_oracle_diagnostics`` switch. E2 remains deliberately
    unavailable until a learned slot binder exists.
    """

    input_track: str = I1
    entity_track: str = E0
    allow_oracle_diagnostics: bool = False
    random_seed: int = 31
    workspace_capacity: int = 1
    ignition_threshold: float = 1.2
    ignition_margin: float = 0.20
    stability_steps: int = 1
    action_prefix: str = "broadcast"

    def validate(self) -> None:
        if self.input_track not in _INPUT_TRACKS:
            raise ValueError(f"unsupported input track: {self.input_track}")
        if self.entity_track not in _ENTITY_TRACKS:
            raise ValueError(f"unsupported entity track: {self.entity_track}")
        if self.entity_track == E2:
            raise NotImplementedError("E2_learned_slots is not implemented")
        if not isinstance(self.allow_oracle_diagnostics, bool):
            raise ValueError("allow_oracle_diagnostics must be a boolean")
        if (self.input_track == I2 or self.entity_track == E1) and not (
            self.allow_oracle_diagnostics
        ):
            raise ValueError("I2/E1 are diagnostic-only and require explicit oracle permission")
        if isinstance(self.random_seed, bool) or not isinstance(self.random_seed, int):
            raise ValueError("random_seed must be an integer")
        if isinstance(self.workspace_capacity, bool) or not isinstance(
            self.workspace_capacity, int
        ) or self.workspace_capacity < 1:
            raise ValueError("workspace_capacity must be a positive integer")
        for name in ("ignition_threshold", "ignition_margin"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a finite non-negative number")
            if not math.isfinite(float(value)) or value < 0:
                raise ValueError(f"{name} must be a finite non-negative number")
        if isinstance(self.stability_steps, bool) or not isinstance(
            self.stability_steps, int
        ) or self.stability_steps < 1:
            raise ValueError("stability_steps must be a positive integer")
        if not isinstance(self.action_prefix, str) or not self.action_prefix.strip():
            raise ValueError("action_prefix must be a non-empty string")

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, value: object) -> V03BrainConfig:
        expected = {field for field in cls.__dataclass_fields__}
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("v0.3.1 config has unexpected fields")
        try:
            result = cls(**value)
        except TypeError as exc:
            raise ValueError("v0.3.1 config is invalid") from exc
        result.validate()
        return result


@dataclass(frozen=True, slots=True)
class V03StepResult:
    step_index: int
    input_track: str
    entity_track: str
    oracle_diagnostic: bool
    sparks: tuple[PerceptualSpark, ...]
    decisions: tuple[IgnitionDecision, ...]
    revision_transitions: tuple[Mapping[str, Any], ...]
    attributions: tuple[Mapping[str, Any], ...]
    beliefs: Mapping[str, str | None]
    workspace: tuple[Mapping[str, Any], ...]
    action: str | None
    world_feedback: Mapping[str, Any]
    concept_observations: tuple[Mapping[str, Any], ...]
    organ_observation: Mapping[str, Any]
    trace_event_hashes: tuple[str, ...]
    state_hash: str
    model_hash: str
    model_status: str
    revision_controller_status: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "beliefs": dict(self.beliefs),
            "concept_observations": [dict(item) for item in self.concept_observations],
            "decisions": [asdict(item) for item in self.decisions],
            "revision_transitions": [dict(item) for item in self.revision_transitions],
            "attributions": [dict(item) for item in self.attributions],
            "entity_track": self.entity_track,
            "input_track": self.input_track,
            "model_hash": self.model_hash,
            "model_status": self.model_status,
            "revision_controller_status": self.revision_controller_status,
            "oracle_diagnostic": self.oracle_diagnostic,
            "organ_observation": dict(self.organ_observation),
            "sparks": [json.loads(item.to_canonical_json()) for item in self.sparks],
            "state_hash": self.state_hash,
            "step_index": self.step_index,
            "trace_event_hashes": list(self.trace_event_hashes),
            "workspace": [dict(item) for item in self.workspace],
            "world_feedback": dict(self.world_feedback),
        }


class IntegratedV03Brain:
    """Stateful v0.3.1 reference composition.

    Concept, organ, and trace outputs are observers: none is read while making
    evidence, ignition, workspace, or action decisions. The I3 generic adapter
    uses the existing C15 revision heads with truth-free sensory features; it
    does not instantiate ``RevisionController``. The default weights are
    deterministic reference weights and are explicitly not claimed as trained.
    """

    def __init__(
        self,
        config: V03BrainConfig | None = None,
        *,
        revision_model: object | None = None,
    ) -> None:
        self.config = config or V03BrainConfig()
        self.config.validate()
        self._provided_revision_model = revision_model
        self._initialize_runtime()

    def _initialize_runtime(self) -> None:
        from sparkbrain.v03_seed import AdaptiveSensoryField

        self.sensory_field = AdaptiveSensoryField()
        self.ledger = EvidenceLedger()
        self.coalition_gate = CoalitionGate(
            CoalitionGateConfig(
                ignition_threshold=float(self.config.ignition_threshold),
                ignition_margin=float(self.config.ignition_margin),
                stability_steps=self.config.stability_steps,
            )
        )
        self.belief_field = PersistentBeliefField()
        self._concept_observer = OnlineConceptFormer()
        self._candidate_keys: set[tuple[str | None, str]] = set()
        self._workspace: list[dict[str, Any]] = []
        self._last_action: str | None = None
        self._last_feedback: dict[str, Any] = {}
        self._last_revisions: list[dict[str, Any]] = []
        self._last_attributions: list[dict[str, Any]] = []
        self._last_concepts: list[dict[str, Any]] = []
        self._last_no_ignition: dict[str, bool] = {}
        self._pending_i3: dict[str, dict[str, Any]] = {}
        self._history: list[dict[str, Any]] = []
        self._results: list[V03StepResult] = []
        self._rng = random.Random(self.config.random_seed)
        self._revision_model = None
        self._model_status = "not_used"
        if self.config.input_track == I3:
            self._revision_model = self._provided_revision_model or self._new_reference_model()
            reset_runtime = getattr(self._revision_model, "reset_runtime", None)
            if callable(reset_runtime):
                reset_runtime()
            self._model_status = (
                "provided_c15_model" if self._provided_revision_model is not None
                else "deterministic_untrained_c15_reference"
            )
        self._model_hash = self._parameter_hash(self._revision_model)
        self.trace = V03TraceSession(config=self._trace_config())

    def _trace_config(self) -> dict[str, Any]:
        return {
            "mode": f"integrated:{self.config.input_track}:{self.config.entity_track}",
            "seed": self.config.random_seed,
        }

    def _new_reference_model(self) -> object:
        try:
            import torch

            from sparkbrain.v03_learned import C15RevisionModel
        except ImportError as exc:
            raise RuntimeError("I3 requires the optional torch runtime") from exc
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(self.config.random_seed)
            model = C15RevisionModel()
        model.eval()
        return model

    @staticmethod
    def _parameter_hash(model: object | None) -> str:
        if model is None:
            return _digest({"model": None})
        state_dict = getattr(model, "state_dict", None)
        if not callable(state_dict):
            raise TypeError("revision_model must expose a state_dict() method")
        digest = hashlib.sha256()
        for name, tensor in sorted(state_dict().items()):
            digest.update(name.encode("utf-8"))
            value = tensor.detach().cpu().contiguous()
            digest.update(str(value.dtype).encode("ascii"))
            digest.update(_canonical(list(value.shape)).encode("ascii"))
            digest.update(value.numpy().tobytes())
        return digest.hexdigest()

    @property
    def model_hash(self) -> str:
        return self._model_hash

    @property
    def history(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(_json_copy(self._history))

    def reset(self) -> None:
        self._initialize_runtime()

    def inspect(self) -> dict[str, Any]:
        """Return an isolated JSON snapshot without advancing any component."""

        beliefs: dict[str, dict[str, Any]] = {}
        entities = {entity for entity, _ in self._candidate_keys}
        for entity in sorted(entities, key=lambda item: item or ""):
            ranked = self.belief_field.ranked(entity)
            beliefs[entity or "__global__"] = {
                "activations": {item.belief_key: item.activation for item in ranked},
                "winner": self.belief_field.winner(entity),
            }
        return _json_copy(
            {
                "action": self._last_action,
                "beliefs": beliefs,
                "config_hash": _digest(self.config.as_dict()),
                "evidence_state_hash": self.ledger.state_hash(),
                "history_length": len(self._history),
                "model_hash": self._model_hash,
                "model_status": self._model_status,
                "revision_controller_status": "not_connected_generic_adapter",
                "revision_transitions": self._last_revisions,
                "attributions": self._last_attributions,
                "sensory_state_hash": _digest(json.loads(self.sensory_field.serialize_state())),
                "trace_state_hash": self.trace.state_hash(),
                "workspace": self._workspace,
                "world_feedback": self._last_feedback,
            }
        )

    def state_hash(self) -> str:
        return _digest(self.inspect())

    def component_inventory(self) -> dict[str, Any]:
        """Return every replayed component in an audit-friendly structure."""

        decision_rows = (
            [asdict(item) for item in self._results[-1].decisions] if self._results else []
        )
        return _json_copy(
            {
                "belief": self.inspect()["beliefs"],
                "coalition": self._coalition_inventory(decision_rows),
                "concept": {"mode": "observation_only", "rows": self._last_concepts},
                "entity": {
                    "candidate_keys": [
                        [entity, belief]
                        for entity, belief in sorted(
                            self._candidate_keys, key=lambda item: (item[0] or "", item[1])
                        )
                    ],
                    "track": self.config.entity_track,
                },
                "evidence": json.loads(self.ledger.serialize_state()),
                "model": {
                    "hash": self._model_hash,
                    "revision_controller_status": "not_connected_generic_adapter",
                    "status": self._model_status,
                },
                "organ": {"mode": "observation_only", "status": "not_evaluated"},
                "rng": {"state": self._rng.getstate()},
                "sensory": json.loads(self.sensory_field.serialize_state()),
                "trace": {
                    "event_hashes": [item.event_hash for item in self.trace.events],
                    "state": self.trace.inspect(),
                    "state_hash": self.trace.state_hash(),
                },
                "workspace": list(self._workspace),
            }
        )

    def _coalition_inventory(self, decision_rows: list[dict[str, Any]]) -> dict[str, Any]:
        def stability_rows(values: Mapping[tuple[str | None, str], int]) -> list[dict[str, Any]]:
            return [
                {"belief_key": belief, "entity_key": entity, "steps": steps}
                for (entity, belief), steps in sorted(
                    values.items(), key=lambda item: (item[0][0] or "", item[0][1])
                )
            ]

        c14_signatures = [
            {
                "belief_key": belief,
                "entity_key": entity,
                "signature": _json_copy(signature),
            }
            for (entity, belief), signature in sorted(
                self.coalition_gate._c14_signatures.items(),
                key=lambda item: (item[0][0] or "", item[0][1]),
            )
        ]
        return {
            "c14_signatures": c14_signatures,
            "c14_stability": stability_rows(self.coalition_gate._c14_stability),
            "last_decisions": decision_rows,
            "last_top": _json_copy(self.coalition_gate._last_top),
            "last_top_signature": _json_copy(self.coalition_gate._last_top_signature),
            "stability": stability_rows(self.coalition_gate._stability),
        }

    def step(
        self,
        sample: SensorySample,
        *,
        goal_bias: Mapping[str, float] | None = None,
        world_feedback: Mapping[str, Any] | None = None,
    ) -> V03StepResult:
        sample.validate()
        bias = self._finite_bias(goal_bias)
        feedback = self._feedback(world_feedback)
        before_events = len(self.trace.events)
        observation = self.sensory_field.observe_with_trace(sample, goal_bias=bias)
        for spark in observation.sparks:
            self._record_sensory(spark)

        grouped = self._interpret(sample, observation.sparks)
        touched: set[str | None] = set()
        for spark, belief_key, support in grouped:
            entity = self._entity(sample, spark)
            self.ledger.add(
                EvidenceContribution(
                    evidence_id=spark.evidence_id,
                    source_id=spark.source_id,
                    belief_key=belief_key,
                    time=spark.time,
                    support=support,
                    correlation_group=spark.correlation_group,
                    object_key=entity,
                )
            )
            self._candidate_keys.add((entity, belief_key))
            self.belief_field.seed(entity, belief_key)
            touched.add(entity)
            self._record_evidence(spark, entity, belief_key)

        decisions = tuple(
            self._decide(entity, now=sample.time) for entity in self._entities(touched)
        )
        revisions, attributions = self._revise(decisions, now=sample.time)
        action = self._broadcast(decisions, revisions, sample.time)
        self._last_action = action
        self._last_feedback = feedback

        # Observation-only paths run after the decision and never feed back into it.
        self._concept_observer.observe(
            {spark.feature_id for spark in observation.sparks}, time=sample.time
        )
        concepts = tuple(
            {
                "activation": candidate.strength,
                "concept_id": candidate.concept_id,
                "label": "label_free",
                "members": list(candidate.members),
            }
            for candidate in self._concept_observer.candidates()
        )
        self._last_concepts = _json_copy(list(concepts))
        organ = {"mode": "observation_only", "status": "not_evaluated"}
        self._record_outcome(decisions, action, feedback, concepts)
        feedback_sparks = self._return_feedback(sample, action, feedback)
        event_hashes = tuple(
            event.event_hash for event in self.trace.events[before_events:]
        )
        beliefs = self._belief_winners()
        history_row = {
            "goal_bias": bias,
            "sample": json.loads(sample.to_canonical_json()),
            "world_feedback": feedback,
        }
        self._history.append(_json_copy(history_row))
        result = V03StepResult(
            step_index=len(self._history) - 1,
            input_track=self.config.input_track,
            entity_track=self.config.entity_track,
            oracle_diagnostic=self.config.input_track == I2 or self.config.entity_track == E1,
            sparks=observation.sparks + feedback_sparks,
            decisions=decisions,
            revision_transitions=tuple(revisions),
            attributions=tuple(attributions),
            beliefs=beliefs,
            workspace=tuple(_json_copy(self._workspace)),
            action=action,
            world_feedback=feedback,
            concept_observations=concepts,
            organ_observation=organ,
            trace_event_hashes=event_hashes,
            state_hash="pending",
            model_hash=self._model_hash,
            model_status=self._model_status,
            revision_controller_status="not_connected_generic_adapter",
        )
        final = replace(result, state_hash=self.state_hash())
        self._results.append(final)
        return final

    @staticmethod
    def _finite_bias(value: Mapping[str, float] | None) -> dict[str, float]:
        if value is None:
            return {}
        if not isinstance(value, Mapping):
            raise ValueError("goal_bias must be a mapping")
        result: dict[str, float] = {}
        for key, raw in value.items():
            if not isinstance(key, str) or not key:
                raise ValueError("goal_bias keys must be non-empty strings")
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                raise ValueError("goal_bias values must be finite numbers")
            number = float(raw)
            if not math.isfinite(number):
                raise ValueError("goal_bias values must be finite numbers")
            result[key] = number
        return dict(sorted(result.items()))

    @staticmethod
    def _feedback(value: Mapping[str, Any] | None) -> dict[str, Any]:
        if value is None:
            return {"status": "not_connected"}
        if not isinstance(value, Mapping):
            raise ValueError("world_feedback must be a mapping")
        try:
            result = _json_copy(dict(value))
        except (TypeError, ValueError) as exc:
            raise ValueError("world_feedback must be finite JSON data") from exc
        _reject_evaluator_keys(result, path="world_feedback")
        return result

    def _interpret(
        self, sample: SensorySample, sparks: tuple[PerceptualSpark, ...]
    ) -> tuple[tuple[PerceptualSpark, str, float], ...]:
        if not sparks:
            return ()
        if self.config.input_track == I3:
            by_entity: dict[str, list[PerceptualSpark]] = {}
            for spark in sparks:
                key = self._entity(sample, spark) or "__global__"
                by_entity.setdefault(key, []).append(spark)
            result: list[tuple[PerceptualSpark, str, float]] = []
            for entity, rows in sorted(by_entity.items()):
                belief, confidence = self._i3_belief(entity, rows)
                result.extend(
                    (spark, belief, min(1.0, 0.5 + confidence)) for spark in rows
                )
            return tuple(result)

        text = sample.metadata.get("text", "") if isinstance(sample.metadata, Mapping) else ""
        if text and not isinstance(text, str):
            raise ValueError("metadata.text must be a string")
        if self.config.input_track == I2:
            encoded = StrictSymbolicOracleFrontend().encode(
                InputRecord(sample.sample_id, text or sample.sample_id, sample.metadata)
            )
        else:
            frontend = (
                WholeHashFrontend()
                if self.config.input_track == I0
                else LocalCompositionalFrontend()
            )
            encoded = frontend.encode(InputRecord(sample.sample_id, text or sample.sample_id))
        feature, weight = max(encoded.features, key=lambda item: (item[1], item[0]))
        belief = f"{self.config.input_track}:{feature}"
        support = max(0.05, min(1.0, float(weight)))
        return tuple((spark, belief, support) for spark in sparks)

    def _i3_belief(
        self, entity: str, sparks: Sequence[PerceptualSpark]
    ) -> tuple[str, float]:
        import torch

        from sparkbrain.v03_seed.revision_worlds import BELIEF_ORDER

        rows = [self._i3_features(spark) for spark in sparks[:5]]
        ids: list[str | None] = [spark.evidence_id for spark in sparks[:5]]
        mask = [True] * len(rows)
        while len(rows) < 5:
            rows.append([0.0] * 12)
            ids.append(None)
            mask.append(False)
        with torch.no_grad():
            output = self._revision_model.forward_visible(
                entity_key=entity,
                features=torch.tensor(rows, dtype=torch.float32),
                evidence_ids=tuple(ids),
                padding_mask=torch.tensor(mask, dtype=torch.bool),
            )
            probabilities = output.conditional_belief_probabilities()
            transition_probabilities = output.transition_probabilities()
            attribution_probabilities = torch.softmax(
                output.attribution_logits[output.attribution_mask], dim=0
            )
        transitions = ("insufficient_information", "maintain", "recover", "revise")
        self._pending_i3[entity] = {
            "attribution": [
                {"evidence_id": evidence_id, "weight": float(weight.item())}
                for evidence_id, weight in zip(
                    (item for item in ids if item is not None),
                    attribution_probabilities,
                    strict=True,
                )
            ],
            "transition": transitions[int(transition_probabilities.argmax().item())],
            "transition_probabilities": {
                key: float(transition_probabilities[position].item())
                for position, key in enumerate(transitions)
            },
        }
        index = int(probabilities.argmax().item())
        return BELIEF_ORDER[index], float(probabilities[index].item())

    @staticmethod
    def _i3_features(spark: PerceptualSpark) -> list[float]:
        def unit(value: str) -> float:
            return int(hashlib.sha256(value.encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF

        return [
            float(spark.activation),
            float(spark.salience),
            float(spark.prediction_error),
            float(spark.threshold),
            min(1.0, float(spark.time) / 1000.0),
            unit(spark.feature_id),
            unit(spark.source_id),
            unit(spark.correlation_group or ""),
            unit(spark.evidence_id),
            1.0 if spark.entity_slot else 0.0,
            float(len(spark.parents)) / 8.0,
            1.0,
        ]

    def _entity(self, sample: SensorySample, spark: PerceptualSpark) -> str | None:
        if self.config.entity_track == E0:
            return None
        if not spark.entity_slot or spark.entity_slot != sample.entity_hint:
            raise ValueError("E1 requires one consistent evaluator-provided entity hint")
        return spark.entity_slot

    @staticmethod
    def _entities(values: set[str | None]) -> tuple[str | None, ...]:
        return tuple(sorted(values, key=lambda item: item or ""))

    def _decide(self, entity: str | None, *, now: float) -> IgnitionDecision:
        activations = {
            (candidate_entity, belief): self.belief_field.activation(candidate_entity, belief)
            for candidate_entity, belief in sorted(
                self._candidate_keys, key=lambda item: (item[0] or "", item[1])
            )
            if candidate_entity == entity
        }
        return self.coalition_gate.evaluate(activations, self.ledger, now=now)

    def _revise(
        self, decisions: Sequence[IgnitionDecision], *, now: float
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        revisions: list[dict[str, Any]] = []
        attributions: list[dict[str, Any]] = []
        for decision in decisions:
            entity = decision.object_key or "__global__"
            previous = self.belief_field.winner(decision.object_key)
            cited = list(decision.coalitions[0].support_ids) if decision.coalitions else []
            if not decision.ignited or decision.belief_key is None:
                transition = "insufficient_information"
            elif self.config.input_track == I3:
                transition = self._pending_i3[entity]["transition"]
            elif (
                self._last_no_ignition.get(entity, False)
                and previous is not None
                and previous == decision.belief_key
            ):
                transition = "recover"
            elif previous == decision.belief_key:
                transition = "maintain"
            else:
                transition = "revise"
            accepted = decision.ignited and transition != "insufficient_information"
            if accepted:
                self.belief_field.update(decision, time=now)
            revision = {
                "accepted": accepted,
                "belief_key": decision.belief_key if accepted else previous,
                "entity_key": entity,
                "previous_belief": previous,
                "transition": transition,
            }
            if self.config.input_track == I3:
                attribution_rows = self._pending_i3[entity]["attribution"]
                revision["transition_probabilities"] = self._pending_i3[entity][
                    "transition_probabilities"
                ]
            else:
                weight = 1.0 / len(cited) if cited else 0.0
                attribution_rows = [
                    {"evidence_id": evidence_id, "weight": weight}
                    for evidence_id in cited
                ]
            revisions.append(revision)
            attributions.append(
                {"entity_key": entity, "rows": attribution_rows, "source": self.config.input_track}
            )
            self._last_no_ignition[entity] = not decision.ignited
        self._last_revisions = _json_copy(revisions)
        self._last_attributions = _json_copy(attributions)
        return revisions, attributions

    def _broadcast(
        self,
        decisions: Sequence[IgnitionDecision],
        revisions: Sequence[Mapping[str, Any]],
        now: float,
    ) -> str | None:
        accepted_entities = {
            str(item["entity_key"]) for item in revisions if item["accepted"] is True
        }
        ignited = [
            item
            for item in decisions
            if item.ignited
            and item.belief_key is not None
            and (item.object_key or "__global__") in accepted_entities
        ]
        if not ignited:
            return None
        winner = sorted(ignited, key=lambda item: (-item.score, item.belief_key or ""))[0]
        row = {
            "belief_key": winner.belief_key,
            "entity_key": winner.object_key or "__global__",
            "score": winner.score,
            "time": now,
        }
        self._workspace = [
            row,
            *(item for item in self._workspace if item["entity_key"] != row["entity_key"]),
        ][: self.config.workspace_capacity]
        return f"{self.config.action_prefix}:{winner.belief_key}"

    def _belief_winners(self) -> dict[str, str | None]:
        entities = {entity for entity, _ in self._candidate_keys}
        return {
            entity or "__global__": self.belief_field.winner(entity)
            for entity in sorted(entities, key=lambda item: item or "")
        }

    def _return_feedback(
        self,
        triggering_sample: SensorySample,
        action: str | None,
        feedback: Mapping[str, Any],
    ) -> tuple[PerceptualSpark, ...]:
        values = feedback.get("values")
        if action is None or values is None:
            return ()
        if self.config.input_track == I2:
            raise ValueError("I2 diagnostic mode cannot consume autonomous world feedback")
        if not isinstance(values, Mapping) or not values:
            raise ValueError("world_feedback.values must be a non-empty numeric mapping")
        normalized: dict[str, float] = {}
        for key, raw in values.items():
            if not isinstance(key, str) or not key:
                raise ValueError("world feedback channel names must be non-empty strings")
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                raise ValueError("world feedback values must be finite numbers")
            number = float(raw)
            if not math.isfinite(number):
                raise ValueError("world feedback values must be finite numbers")
            normalized[key] = number
        feedback_id = f"feedback:{len(self._history)}:{_digest([action, normalized])[:16]}"
        feedback_sample = SensorySample(
            sample_id=feedback_id,
            time=triggering_sample.time + 1e-9,
            source_id=f"world:{_digest(action)[:16]}",
            modality="world_feedback",
            values=normalized,
            correlation_group=feedback_id,
            entity_hint=triggering_sample.entity_hint,
            metadata={"text": str(feedback.get("text", action))},
        )
        observation = self.sensory_field.observe_with_trace(feedback_sample)
        for spark in observation.sparks:
            self._record_sensory(spark)
        for spark, belief_key, support in self._interpret(feedback_sample, observation.sparks):
            entity = self._entity(feedback_sample, spark)
            self.ledger.add(
                EvidenceContribution(
                    evidence_id=spark.evidence_id,
                    source_id=spark.source_id,
                    belief_key=belief_key,
                    time=spark.time,
                    support=support,
                    correlation_group=spark.correlation_group,
                    object_key=entity,
                )
            )
            self._candidate_keys.add((entity, belief_key))
            self.belief_field.seed(entity, belief_key)
            self._record_evidence(spark, entity, belief_key)
        return observation.sparks

    def _record_sensory(self, spark: PerceptualSpark) -> None:
        self.trace.record(
            "sensory_accepted",
            {"cited_evidence_ids": [], "reason": "adaptive_sensory_acceptance"},
            state_delta={},
        )

    def _record_evidence(
        self, spark: PerceptualSpark, entity: str | None, belief_key: str
    ) -> None:
        state = self.trace.inspect()
        evidence = state["evidence"]
        evidence[spark.evidence_id] = {
            "active": True,
            "entity": entity or "__global__",
            "polarity": "support",
            "source_id": spark.source_id,
        }
        self.trace.record(
            "evidence_added",
            {
                "cited_evidence_ids": [],
                "entity": entity or "__global__",
                "evidence_id": spark.evidence_id,
                "hypothesis": belief_key,
            },
            state_delta={"evidence": evidence},
        )

    def _observer_state(self, concepts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        beliefs = {
            entity: {
                "residual_losers": [
                    item.belief_key
                    for item in self.belief_field.ranked(None if entity == "__global__" else entity)
                    if item.belief_key
                    != self.belief_field.winner(None if entity == "__global__" else entity)
                ],
                "winner": self.belief_field.winner(None if entity == "__global__" else entity),
            }
            for entity in self._belief_winners()
        }
        candidates = {
            str(item["concept_id"]): {
                "activation": float(item["activation"]),
                "label": str(item["label"]),
            }
            for item in concepts
        }
        return {"beliefs": beliefs, "concept_candidates": candidates}

    def _record_outcome(
        self,
        decisions: Sequence[IgnitionDecision],
        action: str | None,
        feedback: Mapping[str, Any],
        concepts: Sequence[Mapping[str, Any]],
    ) -> None:
        cited = sorted(
            {
                evidence_id
                for decision in decisions
                for coalition in decision.coalitions[:1]
                for evidence_id in coalition.support_ids
            }
        )
        observer_state = self._observer_state(concepts)
        if action is None:
            self.trace.record(
                "no_ignition",
                {
                    "cited_evidence_ids": cited,
                    "reason": ",".join(item.reason for item in decisions) or "no_candidates",
                },
                state_delta=observer_state,
            )
        else:
            self.trace.record(
                "workspace_broadcast",
                {
                    "cited_evidence_ids": cited,
                    "hypothesis": action,
                    "reason": str(feedback.get("status", "feedback_recorded")),
                },
                state_delta=observer_state,
            )

    def checkpoint(self, checkpoint_id: str = "integrated-v03") -> dict[str, Any]:
        if not isinstance(checkpoint_id, str) or not checkpoint_id.strip():
            raise ValueError("checkpoint_id must be a non-empty string")
        body = {
            "checkpoint_id": checkpoint_id,
            "component_inventory": self.component_inventory(),
            "config": self.config.as_dict(),
            "config_hash": _digest(self.config.as_dict()),
            "final_state_hash": self.state_hash(),
            "history": _json_copy(self._history),
            "model_hash": self._model_hash,
            "rng_state": _json_copy(self._rng.getstate()),
            "runtime_version": _CHECKPOINT_VERSION,
            "trace_checkpoint": self.trace.checkpoint(f"{checkpoint_id}:trace").as_dict(),
        }
        return {**body, "checkpoint_hash": _digest(body)}

    @classmethod
    def restore(
        cls,
        checkpoint: Mapping[str, Any],
        *,
        revision_model: object | None = None,
    ) -> IntegratedV03Brain:
        expected = {
            "checkpoint_hash",
            "checkpoint_id",
            "component_inventory",
            "config",
            "config_hash",
            "final_state_hash",
            "history",
            "model_hash",
            "rng_state",
            "runtime_version",
            "trace_checkpoint",
        }
        if not isinstance(checkpoint, Mapping) or set(checkpoint) != expected:
            raise ValueError("integrated checkpoint has unexpected fields")
        value = _json_copy(dict(checkpoint))
        body = {key: item for key, item in value.items() if key != "checkpoint_hash"}
        if value["runtime_version"] != _CHECKPOINT_VERSION:
            raise ValueError("unsupported integrated checkpoint version")
        if _digest(body) != value["checkpoint_hash"]:
            raise ValueError("integrated checkpoint hash mismatch")
        config = V03BrainConfig.from_dict(value["config"])
        if _digest(config.as_dict()) != value["config_hash"]:
            raise ValueError("integrated checkpoint config hash mismatch")
        brain = cls(config, revision_model=revision_model)
        if brain.model_hash != value["model_hash"]:
            raise ValueError("integrated checkpoint model hash mismatch")
        history = value["history"]
        if not isinstance(history, list):
            raise ValueError("integrated checkpoint history must be a list")
        for row in history:
            if not isinstance(row, dict) or set(row) != {"goal_bias", "sample", "world_feedback"}:
                raise ValueError("integrated checkpoint history row is invalid")
            sample = SensorySample.from_canonical_json(_canonical(row["sample"]))
            brain.step(
                sample,
                goal_bias=row["goal_bias"],
                world_feedback=row["world_feedback"],
            )
        if brain.state_hash() != value["final_state_hash"]:
            raise ValueError("integrated checkpoint replay diverged")
        if brain.component_inventory() != value["component_inventory"]:
            raise ValueError("integrated checkpoint component inventory diverged")
        brain._rng.setstate(_tuple_tree(value["rng_state"]))
        if brain.trace.checkpoint(f"{value['checkpoint_id']}:trace").as_dict() != value[
            "trace_checkpoint"
        ]:
            raise ValueError("integrated trace checkpoint replay diverged")
        return brain

    def replay(
        self, history: Sequence[Mapping[str, Any]] | None = None
    ) -> tuple[V03StepResult, ...]:
        rows = _json_copy(list(self._history if history is None else history))
        self.reset()
        for row in rows:
            if not isinstance(row, dict) or set(row) != {"goal_bias", "sample", "world_feedback"}:
                raise ValueError("replay history row is invalid")
            self.step(
                SensorySample.from_canonical_json(_canonical(row["sample"])),
                goal_bias=row["goal_bias"],
                world_feedback=row["world_feedback"],
            )
        return tuple(self._results)

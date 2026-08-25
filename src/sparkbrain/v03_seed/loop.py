from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Protocol

from .belief import PersistentBeliefField
from .coalition import C14_BOUNDED_MODE, LEGACY_MODE, CoalitionGate, CoalitionGateConfig
from .contracts import EvidenceContribution, IgnitionDecision, PerceptualSpark, SensorySample
from .evidence import EvidenceLedger
from .sensory_field import AdaptiveSensoryField


class PerceptualInterpreter(Protocol):
    """Replaceable bridge used to isolate input quality from cognitive dynamics."""

    def interpret(self, spark: PerceptualSpark) -> Iterable[EvidenceContribution]: ...


@dataclass(frozen=True, slots=True)
class V03StepResult:
    sparks: tuple[PerceptualSpark, ...]
    decisions: tuple[IgnitionDecision, ...]
    beliefs: Mapping[str, str | None]


class V03ReferenceLoop:
    """Minimal perception → evidence → coalition → persistent belief loop.

    The interpreter is injectable on purpose:
    - a symbolic oracle is a diagnostic upper bound;
    - a compositional local frontend tests information retention;
    - a learned frontend can later test autonomous concept formation.
    None of those modes changes the downstream evidence and ignition contracts.
    """

    def __init__(
        self,
        interpreter: PerceptualInterpreter,
        *,
        sensory_field: AdaptiveSensoryField | None = None,
        ledger: EvidenceLedger | None = None,
        coalition_gate: CoalitionGate | None = None,
        belief_field: PersistentBeliefField | None = None,
    ) -> None:
        self.interpreter = interpreter
        self.sensory_field = sensory_field or AdaptiveSensoryField()
        self.ledger = ledger or EvidenceLedger()
        self.coalition_gate = coalition_gate or CoalitionGate(
            CoalitionGateConfig(ignition_threshold=1.2)
        )
        self.belief_field = belief_field or PersistentBeliefField()
        self._candidate_keys: set[tuple[str | None, str]] = set()

    def reset(self) -> None:
        self.sensory_field.reset()
        self.ledger.reset()
        self.coalition_gate.reset()
        self.belief_field.reset()
        self._candidate_keys.clear()

    def process(
        self,
        sample: SensorySample,
        *,
        goal_bias: dict[str, float] | None = None,
    ) -> V03StepResult:
        sparks = self.sensory_field.observe(sample, goal_bias=goal_bias)
        touched_objects: set[str | None] = set()
        for spark in sparks:
            for contribution in self.interpreter.interpret(spark):
                self.ledger.add(contribution)
                key = (contribution.object_key, contribution.belief_key)
                self._candidate_keys.add(key)
                touched_objects.add(contribution.object_key)
                self.belief_field.seed(contribution.object_key, contribution.belief_key)

        decisions = tuple(
            self._evaluate_object(object_key, now=sample.time)
            for object_key in sorted(touched_objects, key=lambda item: item or "")
        )
        return V03StepResult(sparks, decisions, self._belief_snapshot())

    def settle(
        self,
        *,
        now: float,
        object_key: str | None = None,
        activation_overrides: Mapping[str, float] | None = None,
        gate_mode: str = LEGACY_MODE,
    ) -> IgnitionDecision:
        """Re-evaluate stable evidence without manufacturing another evidence vote."""

        allowed_modes = {
            LEGACY_MODE,
            C14_BOUNDED_MODE,
            "G0_probability_margin",
            "G1_no_coalition_ablation",
        }
        if gate_mode not in allowed_modes:
            raise ValueError(f"unsupported v0.3 settle gate mode: {gate_mode}")
        if isinstance(now, bool) or not isinstance(now, (int, float)) or not math.isfinite(now):
            raise ValueError("settle time must be a finite number")
        if now < 0:
            raise ValueError("settle time must be non-negative")
        if object_key is not None and (not isinstance(object_key, str) or not object_key.strip()):
            raise ValueError("settle object_key must be a non-empty string or null")
        overrides = self._validate_activation_overrides(activation_overrides)
        if overrides is not None:
            for belief_key in sorted(overrides):
                self._candidate_keys.add((object_key, belief_key))
                self.belief_field.seed(object_key, belief_key)
        return self._evaluate_object(
            object_key,
            now=now,
            activation_overrides=overrides,
            gate_mode=gate_mode,
        )

    @staticmethod
    def _validate_activation_overrides(
        values: Mapping[str, float] | None,
    ) -> dict[str, float] | None:
        if values is None:
            return None
        if not isinstance(values, Mapping) or not values:
            raise ValueError("activation_overrides must be a non-empty mapping")
        result: dict[str, float] = {}
        for belief_key, value in values.items():
            if not isinstance(belief_key, str) or not belief_key.strip():
                raise ValueError("activation override hypotheses must be non-empty strings")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("activation overrides must be finite probabilities")
            numeric = float(value)
            if not 0.0 <= numeric <= 1.0:
                raise ValueError("activation overrides must be finite probabilities in [0, 1]")
            result[belief_key] = numeric
        return result

    def _evaluate_object(
        self,
        object_key: str | None,
        *,
        now: float,
        activation_overrides: Mapping[str, float] | None = None,
        gate_mode: str = LEGACY_MODE,
    ) -> IgnitionDecision:
        activations: dict[tuple[str | None, str], float] = {}
        for candidate_object, belief_key in sorted(
            self._candidate_keys,
            key=lambda row: ((row[0] or ""), row[1]),
        ):
            if candidate_object != object_key:
                continue
            activations[(object_key, belief_key)] = (
                activation_overrides[belief_key]
                if activation_overrides is not None and belief_key in activation_overrides
                else self.belief_field.activation(object_key, belief_key)
            )
        if gate_mode in {"G0_probability_margin", "G1_no_coalition_ablation"}:
            decision = self._probability_decision(activations, object_key=object_key)
        else:
            decision = self.coalition_gate.evaluate(
                activations,
                self.ledger,
                now=now,
                mode=gate_mode,
            )
        self.belief_field.update(decision, time=now)
        return decision

    @staticmethod
    def _probability_decision(
        activations: Mapping[tuple[str | None, str], float],
        *,
        object_key: str | None,
    ) -> IgnitionDecision:
        ranked = sorted(
            ((float(value), belief_key) for (_, belief_key), value in activations.items()),
            key=lambda item: (-item[0], item[1]),
        )
        if not ranked:
            return IgnitionDecision(False, None, None, 0.0, 0.0, "probability_below_threshold", ())
        score, belief_key = ranked[0]
        runner_up = ranked[1][0] if len(ranked) > 1 else 0.0
        margin = score - runner_up
        if score < 0.50:
            reason = "probability_below_threshold"
        elif margin < 0.08:
            reason = "probability_margin_below_threshold"
        else:
            return IgnitionDecision(True, belief_key, object_key, score, margin, "ignited", ())
        return IgnitionDecision(False, None, None, score, margin, reason, ())

    def _belief_snapshot(self) -> dict[str, str | None]:
        objects = {object_key for object_key, _ in self._candidate_keys}
        return {
            object_key or "__global__": self.belief_field.winner(object_key)
            for object_key in sorted(objects, key=lambda item: item or "")
        }

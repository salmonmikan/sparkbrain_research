from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Protocol

from .belief import PersistentBeliefField
from .coalition import CoalitionGate, CoalitionGateConfig
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

    def settle(self, *, now: float, object_key: str | None = None) -> IgnitionDecision:
        """Re-evaluate stable evidence without manufacturing another evidence vote."""

        return self._evaluate_object(object_key, now=now)

    def _evaluate_object(self, object_key: str | None, *, now: float) -> IgnitionDecision:
        activations: dict[tuple[str | None, str], float] = {}
        for candidate_object, belief_key in sorted(
            self._candidate_keys,
            key=lambda row: ((row[0] or ""), row[1]),
        ):
            if candidate_object != object_key:
                continue
            activations[(object_key, belief_key)] = self.belief_field.activation(
                object_key, belief_key
            )
        decision = self.coalition_gate.evaluate(activations, self.ledger, now=now)
        self.belief_field.update(decision, time=now)
        return decision

    def _belief_snapshot(self) -> dict[str, str | None]:
        objects = {object_key for object_key, _ in self._candidate_keys}
        return {
            object_key or "__global__": self.belief_field.winner(object_key)
            for object_key in sorted(objects, key=lambda item: item or "")
        }

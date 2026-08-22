from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass

from ..tasks.schema import Episode, EpisodeStep, Observation, Target, config_hash, episode_id


@dataclass(frozen=True, order=True, slots=True)
class Literal:
    predicate: str
    entity: str
    positive: bool = True

    def opposite(self) -> Literal:
        return Literal(self.predicate, self.entity, not self.positive)

    def render(self) -> str:
        return f"{self.entity} is {'not ' if not self.positive else ''}{self.predicate}"


@dataclass(frozen=True, slots=True)
class SymbolicRule:
    rule_id: str
    antecedents: tuple[Literal, ...]
    conclusion: Literal
    defeasible: bool = False

    def render(self) -> str:
        qualifier = "Normally, " if self.defeasible else ""
        premises = " and ".join(item.render() for item in self.antecedents)
        return f"{qualifier}if {premises}, then {self.conclusion.render()}"


@dataclass(frozen=True, slots=True)
class SymbolicEvent:
    kind: str
    literal: Literal | None = None
    rule: SymbolicRule | None = None
    source_id: str = "symbolic"

    def validate(self) -> None:
        if self.kind in {"assert", "retract"} and (self.literal is None or self.rule is not None):
            raise ValueError(f"{self.kind} requires exactly one literal")
        if self.kind in {"add_rule", "remove_rule"} and (
            self.rule is None or self.literal is not None
        ):
            raise ValueError(f"{self.kind} requires exactly one rule")
        if self.kind not in {"assert", "retract", "add_rule", "remove_rule"}:
            raise ValueError(f"Unsupported symbolic event kind: {self.kind!r}")

    def render(self) -> str:
        self.validate()
        if self.kind == "assert":
            return f"Add fact: {self.literal.render()}"
        if self.kind == "retract":
            return f"Retract fact: {self.literal.render()}"
        if self.kind == "add_rule":
            return f"Add rule: {self.rule.render()}"
        return f"Remove rule: {self.rule.rule_id}"

    def metadata(self) -> dict[str, object]:
        self.validate()
        payload: dict[str, object] = {"kind": self.kind}
        if self.literal is not None:
            payload["literal"] = {
                "predicate": self.literal.predicate,
                "entity": self.literal.entity,
                "positive": self.literal.positive,
            }
        if self.rule is not None:
            payload["rule"] = {
                "rule_id": self.rule.rule_id,
                "antecedents": [
                    {
                        "predicate": item.predicate,
                        "entity": item.entity,
                        "positive": item.positive,
                    }
                    for item in self.rule.antecedents
                ],
                "conclusion": {
                    "predicate": self.rule.conclusion.predicate,
                    "entity": self.rule.conclusion.entity,
                    "positive": self.rule.conclusion.positive,
                },
                "defeasible": self.rule.defeasible,
            }
        return payload


class SymbolicOracle:
    """Small independent forward-chaining oracle with defeasible blocking."""

    def __init__(self) -> None:
        self._facts: set[Literal] = set()
        self._rules: dict[str, SymbolicRule] = {}

    def apply(self, event: SymbolicEvent) -> None:
        event.validate()
        if event.kind == "assert":
            self._facts.add(event.literal)  # type: ignore[arg-type]
        elif event.kind == "retract":
            self._facts.discard(event.literal)  # type: ignore[arg-type]
        elif event.kind == "add_rule":
            self._rules[event.rule.rule_id] = event.rule  # type: ignore[union-attr]
        else:
            self._rules.pop(event.rule.rule_id, None)  # type: ignore[union-attr]

    def closure(self) -> frozenset[Literal]:
        derived = set(self._facts)
        changed = True
        while changed:
            changed = False
            for rule in sorted(self._rules.values(), key=lambda item: item.rule_id):
                if not set(rule.antecedents) <= derived:
                    continue
                if rule.defeasible and rule.conclusion.opposite() in derived:
                    continue
                if rule.conclusion not in derived:
                    derived.add(rule.conclusion)
                    changed = True
        return frozenset(derived)

    def query(self, literal: Literal) -> str:
        closure = self.closure()
        positive = literal in closure
        negative = literal.opposite() in closure
        if positive and negative:
            return "both"
        if positive:
            return "true"
        if negative:
            return "false"
        return "unknown"


@dataclass(frozen=True, slots=True)
class SymbolicTemplate:
    group_id: str
    base_predicate: str
    conclusion_predicate: str
    distractor_predicate: str
    pattern: str


TEMPLATES = (
    SymbolicTemplate("animal_exception", "bird", "flies", "blue", "exception"),
    SymbolicTemplate("vehicle_exception", "vehicle", "mobile", "painted", "exception"),
    SymbolicTemplate("staff_retraction", "employee", "authorized", "remote", "retraction"),
    SymbolicTemplate("device_retraction", "device", "online", "new", "retraction"),
    SymbolicTemplate("weather_contradiction", "cloudy", "wet", "cold", "contradiction"),
    SymbolicTemplate("sensor_contradiction", "triggered", "hazard", "calibrated", "contradiction"),
    SymbolicTemplate("plant_exception", "plant", "grows", "green", "exception"),
    SymbolicTemplate("member_retraction", "member", "eligible", "local", "retraction"),
    SymbolicTemplate("signal_contradiction", "received", "valid", "loud", "contradiction"),
    SymbolicTemplate("permit_exception", "permitted", "admitted", "early", "exception"),
    SymbolicTemplate("account_retraction", "active", "accessible", "old", "retraction"),
    SymbolicTemplate("report_contradiction", "filed", "accepted", "short", "contradiction"),
)


def template_group_splits(*, seed: int) -> dict[str, tuple[str, ...]]:
    """Assign whole template families, never examples, to train/dev/test."""

    ranked = sorted(
        (template.group_id for template in TEMPLATES),
        key=lambda group: hashlib.sha256(f"{seed}:{group}".encode()).hexdigest(),
    )
    return {
        "train": tuple(ranked[:6]),
        "dev": tuple(ranked[6:9]),
        "test": tuple(ranked[9:]),
    }


def _events(template: SymbolicTemplate, entity: str) -> tuple[SymbolicEvent, ...]:
    base = Literal(template.base_predicate, entity)
    conclusion = Literal(template.conclusion_predicate, entity)
    distractor = Literal(template.distractor_predicate, entity)
    rule = SymbolicRule("r-main", (base,), conclusion, defeasible=template.pattern == "exception")
    common = (
        SymbolicEvent("assert", literal=base, source_id="source:base"),
        SymbolicEvent("add_rule", rule=rule, source_id="source:rule"),
        SymbolicEvent("assert", literal=distractor, source_id="source:distractor"),
    )
    if template.pattern == "exception":
        return common + (
            SymbolicEvent("assert", literal=conclusion.opposite(), source_id="source:exception"),
            SymbolicEvent("retract", literal=conclusion.opposite(), source_id="source:correction"),
        )
    if template.pattern == "retraction":
        return common + (
            SymbolicEvent("retract", literal=base, source_id="source:retraction"),
            SymbolicEvent("assert", literal=base, source_id="source:restoration"),
        )
    return common + (
        SymbolicEvent("assert", literal=conclusion.opposite(), source_id="source:contradiction"),
        SymbolicEvent("retract", literal=conclusion.opposite(), source_id="source:resolution"),
    )


def generate_symbolic_episode(
    group_id: str, *, seed: int, split: str, split_seed: int = 1729
) -> Episode:
    groups = template_group_splits(seed=split_seed)
    if split not in groups and split != "smoke":
        raise ValueError(f"Unsupported symbolic split: {split!r}")
    if split != "smoke" and group_id not in groups[split]:
        raise ValueError(f"Template group {group_id!r} is not assigned to split {split!r}")
    templates = {template.group_id: template for template in TEMPLATES}
    try:
        template = templates[group_id]
    except KeyError as exc:
        raise ValueError(f"Unknown symbolic template group: {group_id!r}") from exc
    rng = random.Random(seed)
    entity = rng.choice(("ada", "ben", "cy", "dia", "eli", "fox"))
    events = list(_events(template, entity))
    if rng.random() < 0.5:
        events[0], events[1] = events[1], events[0]
    oracle = SymbolicOracle()
    query = Literal(template.conclusion_predicate, entity)
    steps: list[EpisodeStep] = []
    previous_truth = "unknown"
    for index, event in enumerate(events):
        oracle.apply(event)
        truth = oracle.query(query)
        observation = Observation(
            observation_id=f"{group_id}:{seed}:{index}",
            step_index=index,
            emitted_time=float(index),
            delivery_time=float(index),
            channel="evidence",
            source_id=event.source_id,
            evidence_id=f"symbolic:{group_id}:{seed}:{index}",
            evidence_label=event.render(),
            object_id=entity,
            metadata={
                "track": "B",
                "template_group": group_id,
                "symbolic_event": event.metadata(),
                "query": {
                    "predicate": query.predicate,
                    "entity": query.entity,
                    "positive": query.positive,
                },
            },
        )
        target = Target(
            belief_truth_by_object={entity: truth},
            decision_justified_by_object={entity: truth != "unknown"},
            update_required=index > 0 and truth != previous_truth,
            scenario_tags=("track_b", template.pattern, group_id),
            annotations={"oracle": "symbolic_forward_chain_v1"},
        )
        steps.append(EpisodeStep(observation, target))
        previous_truth = truth
    digest = config_hash(
        {"group_id": group_id, "seed": seed, "split": split, "split_seed": split_seed}
    )
    result = Episode(
        episode_id=episode_id("symbolic_nonmonotonic", split, seed, digest),
        world_id="symbolic_nonmonotonic",
        world_version="1",
        split=split,
        seed=seed,
        generator_config_hash=digest,
        steps=tuple(steps),
    )
    result.validate()
    return result

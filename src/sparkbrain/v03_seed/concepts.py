from __future__ import annotations

import hashlib
import itertools
from dataclasses import dataclass

from .contracts import ConceptCandidate


@dataclass(frozen=True, slots=True)
class ConceptFormationConfig:
    association_threshold: float = 0.70
    minimum_occurrences: int = 3
    minimum_members: int = 2
    activation_fraction: float = 0.60
    maximum_concepts: int = 256

    def validate(self) -> None:
        if not 0 < self.association_threshold <= 1:
            raise ValueError("association_threshold must be in (0, 1]")
        if self.minimum_occurrences < 1 or self.minimum_members < 2:
            raise ValueError("minimum occurrence/member bounds are invalid")
        if not 0 < self.activation_fraction <= 1:
            raise ValueError("activation_fraction must be in (0, 1]")
        if self.maximum_concepts < 1:
            raise ValueError("maximum_concepts must be >= 1")


@dataclass(slots=True)
class _MutableConcept:
    members: tuple[str, ...]
    strength: float
    observations: int
    reuse_count: int
    first_seen: float
    last_seen: float


class OnlineConceptFormer:
    """Label-free concept candidates from repeated co-activation.

    A candidate is only a recurring assembly, not yet a human-like concept.  The
    surrounding experiments must still test predictive usefulness, transfer, and
    causal necessity before assigning a stronger interpretation.
    """

    def __init__(self, config: ConceptFormationConfig | None = None) -> None:
        self.config = config or ConceptFormationConfig()
        self.config.validate()
        self.feature_counts: dict[str, int] = {}
        self.pair_counts: dict[tuple[str, str], int] = {}
        self._concepts: dict[str, _MutableConcept] = {}

    def reset(self) -> None:
        self.feature_counts.clear()
        self.pair_counts.clear()
        self._concepts.clear()

    def observe(
        self, active_features: set[str] | tuple[str, ...], *, time: float
    ) -> tuple[ConceptCandidate, ...]:
        features = tuple(sorted(set(active_features)))
        for feature in features:
            self.feature_counts[feature] = self.feature_counts.get(feature, 0) + 1
        for left, right in itertools.combinations(features, 2):
            key = (left, right)
            self.pair_counts[key] = self.pair_counts.get(key, 0) + 1

        graph: dict[str, set[str]] = {feature: set() for feature in features}
        eligible = {
            feature
            for feature, count in self.feature_counts.items()
            if count >= self.config.minimum_occurrences
        }
        for (left, right), count in self.pair_counts.items():
            if left not in eligible or right not in eligible:
                continue
            denominator = min(self.feature_counts[left], self.feature_counts[right])
            association = count / max(1, denominator)
            if association >= self.config.association_threshold:
                graph.setdefault(left, set()).add(right)
                graph.setdefault(right, set()).add(left)

        for component in self._components(graph):
            if len(component) < self.config.minimum_members:
                continue
            members = tuple(sorted(component))
            concept_id = "concept:" + hashlib.sha256("|".join(members).encode()).hexdigest()[:16]
            strengths = [self._association(a, b) for a, b in itertools.combinations(members, 2)]
            strength = sum(strengths) / max(1, len(strengths))
            existing = self._concepts.get(concept_id)
            if existing is None:
                if len(self._concepts) >= self.config.maximum_concepts:
                    continue
                self._concepts[concept_id] = _MutableConcept(
                    members=members,
                    strength=strength,
                    observations=1,
                    reuse_count=0,
                    first_seen=time,
                    last_seen=time,
                )
            else:
                existing.strength = strength
                existing.observations += 1
                existing.last_seen = time

        active_set = set(features)
        for concept in self._concepts.values():
            overlap = len(active_set.intersection(concept.members)) / len(concept.members)
            if overlap >= self.config.activation_fraction:
                concept.reuse_count += 1
                concept.last_seen = time
        return self.candidates()

    def active_concepts(
        self, active_features: set[str] | tuple[str, ...]
    ) -> tuple[ConceptCandidate, ...]:
        active_set = set(active_features)
        return tuple(
            candidate
            for candidate in self.candidates()
            if len(active_set.intersection(candidate.members)) / len(candidate.members)
            >= self.config.activation_fraction
        )

    def candidates(self) -> tuple[ConceptCandidate, ...]:
        return tuple(
            ConceptCandidate(
                concept_id=concept_id,
                members=value.members,
                strength=value.strength,
                observations=value.observations,
                reuse_count=value.reuse_count,
                first_seen=value.first_seen,
                last_seen=value.last_seen,
            )
            for concept_id, value in sorted(self._concepts.items())
        )

    def _association(self, left: str, right: str) -> float:
        key = tuple(sorted((left, right)))
        count = self.pair_counts.get(key, 0)
        denominator = min(self.feature_counts.get(left, 0), self.feature_counts.get(right, 0))
        return count / max(1, denominator)

    @staticmethod
    def _components(graph: dict[str, set[str]]) -> tuple[set[str], ...]:
        remaining = set(graph)
        components: list[set[str]] = []
        while remaining:
            start = min(remaining)
            stack = [start]
            component: set[str] = set()
            while stack:
                node = stack.pop()
                if node in component:
                    continue
                component.add(node)
                remaining.discard(node)
                stack.extend(sorted(graph.get(node, ()), reverse=True))
            components.append(component)
        return tuple(components)

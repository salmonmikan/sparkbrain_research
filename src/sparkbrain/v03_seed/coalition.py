from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, fields

from .contracts import CoalitionState, IgnitionDecision
from .evidence import EvidenceLedger


@dataclass(frozen=True, slots=True)
class CoalitionGateConfig:
    ignition_threshold: float = 1.60
    ignition_margin: float = 0.20
    minimum_sources: int = 2
    minimum_independent_groups: int = 2
    minimum_evidence: int = 2
    stability_steps: int = 2
    activation_weight: float = 1.0
    support_weight: float = 0.75
    diversity_bonus: float = 0.15
    contradiction_weight: float = 0.85
    redundancy_weight: float = 0.35

    def validate(self) -> None:
        if self.minimum_sources < 1 or self.minimum_independent_groups < 1:
            raise ValueError("minimum source/group counts must be positive")
        if self.minimum_evidence < 1 or self.stability_steps < 1:
            raise ValueError("minimum evidence and stability must be positive")
        for item in fields(self):
            name = item.name
            value = getattr(self, name)
            if isinstance(value, float) and (not math.isfinite(value) or value < 0):
                raise ValueError(f"{name} must be finite and non-negative")


class CoalitionGate:
    """Coalition-first ignition with an explicit no-ignition state."""

    def __init__(self, config: CoalitionGateConfig | None = None) -> None:
        self.config = config or CoalitionGateConfig()
        self.config.validate()
        self._last_top: tuple[str | None, str] | None = None
        self._last_top_signature: (
            tuple[tuple[str | None, str], tuple[str, ...], tuple[str, ...]] | None
        ) = None
        self._stability: dict[tuple[str | None, str], int] = {}

    def reset(self) -> None:
        self._last_top = None
        self._last_top_signature = None
        self._stability.clear()

    def evaluate(
        self,
        activations: Mapping[tuple[str | None, str], float],
        ledger: EvidenceLedger,
        *,
        now: float,
    ) -> IgnitionDecision:
        coalitions: list[CoalitionState] = []
        for (object_key, belief_key), activation in sorted(activations.items()):
            summary = ledger.summary(belief_key, object_key=object_key, now=now)
            score = (
                self.config.activation_weight * max(0.0, float(activation))
                + self.config.support_weight * summary.effective_support
                + self.config.diversity_bonus * max(0, summary.independent_group_count - 1)
                - self.config.contradiction_weight * summary.effective_contradiction
                - self.config.redundancy_weight * summary.redundancy
            )
            key = (object_key, belief_key)
            coalitions.append(
                CoalitionState(
                    belief_key=belief_key,
                    object_key=object_key,
                    score=score,
                    activation=float(activation),
                    effective_support=summary.effective_support,
                    effective_contradiction=summary.effective_contradiction,
                    redundancy=summary.redundancy,
                    source_count=summary.source_count,
                    independent_group_count=summary.independent_group_count,
                    evidence_count=summary.unique_evidence_count,
                    stability=self._stability.get(key, 0),
                    support_ids=summary.support_ids,
                    contradiction_ids=summary.contradiction_ids,
                )
            )

        coalitions.sort(key=lambda item: (-item.score, str(item.object_key), item.belief_key))
        if not coalitions:
            return IgnitionDecision(False, None, None, 0.0, 0.0, "no_candidates", ())

        top_key = (coalitions[0].object_key, coalitions[0].belief_key)
        top_signature = (
            top_key,
            coalitions[0].support_ids,
            coalitions[0].contradiction_ids,
        )
        if top_signature == self._last_top_signature:
            self._stability[top_key] = self._stability.get(top_key, 0) + 1
        else:
            self._last_top = top_key
            self._last_top_signature = top_signature
            self._stability[top_key] = 1
            for key in tuple(self._stability):
                if key != top_key:
                    self._stability[key] = max(0, self._stability[key] - 1)

        updated = tuple(
            CoalitionState(
                belief_key=item.belief_key,
                object_key=item.object_key,
                score=item.score,
                activation=item.activation,
                effective_support=item.effective_support,
                effective_contradiction=item.effective_contradiction,
                redundancy=item.redundancy,
                source_count=item.source_count,
                independent_group_count=item.independent_group_count,
                evidence_count=item.evidence_count,
                stability=self._stability.get((item.object_key, item.belief_key), 0),
                support_ids=item.support_ids,
                contradiction_ids=item.contradiction_ids,
            )
            for item in coalitions
        )
        top = updated[0]
        second_score = updated[1].score if len(updated) > 1 else 0.0
        margin = top.score - second_score

        conditions = (
            (top.score >= self.config.ignition_threshold, "score_below_threshold"),
            (margin >= self.config.ignition_margin, "margin_below_threshold"),
            (top.source_count >= self.config.minimum_sources, "insufficient_sources"),
            (
                top.independent_group_count >= self.config.minimum_independent_groups,
                "insufficient_independent_groups",
            ),
            (top.evidence_count >= self.config.minimum_evidence, "insufficient_evidence"),
            (top.stability >= self.config.stability_steps, "insufficient_stability"),
        )
        for passed, reason in conditions:
            if not passed:
                return IgnitionDecision(
                    False,
                    None,
                    None,
                    top.score,
                    margin,
                    reason,
                    updated,
                )
        return IgnitionDecision(
            True,
            top.belief_key,
            top.object_key,
            top.score,
            margin,
            "ignited",
            updated,
        )

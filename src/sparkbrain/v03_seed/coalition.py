from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, fields

from .contracts import CoalitionState, IgnitionDecision
from .evidence import EvidenceLedger

C14_BOUNDED_MODE = "c14_bounded_v1"
LEGACY_MODE = "legacy_v03_seed"

_C14_WEIGHTS = {
    "activation": 0.25,
    "effective_support": 0.25,
    "source_diversity": 0.05,
    "group_diversity": 0.05,
    "temporal_stability": 0.10,
    "recency": 0.20,
    "contradiction": -0.15,
    "redundancy": -0.10,
}


def decide_c14(coalitions: tuple[CoalitionState, ...]) -> IgnitionDecision:
    """Apply the frozen C14 gate to already-scored candidates without side effects."""

    if not coalitions:
        return IgnitionDecision(False, None, None, 0.0, 0.0, "no_candidates", ())
    top = coalitions[0]
    runner_up = coalitions[1].score if len(coalitions) > 1 else 0.0
    margin = top.score - runner_up
    conditions = (
        (top.evidence_count >= 2, "insufficient_evidence"),
        (top.source_count >= 2, "insufficient_sources"),
        (top.independent_group_count >= 2, "insufficient_independent_groups"),
        (top.normalized_contradiction <= 0.35, "excessive_contradiction"),
        (top.stability >= 2, "insufficient_stability"),
        (top.normalized_recency >= 0.30, "insufficient_recency"),
        (top.score >= 0.55, "score_below_threshold"),
        (margin >= 0.10, "margin_below_threshold"),
    )
    for passed, reason in conditions:
        if not passed:
            return IgnitionDecision(False, None, None, top.score, margin, reason, coalitions)
    return IgnitionDecision(
        True,
        top.belief_key,
        top.object_key,
        top.score,
        margin,
        "ignited",
        coalitions,
    )


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
        self._c14_signatures: dict[tuple[str | None, str], tuple[object, ...]] = {}
        self._c14_stability: dict[tuple[str | None, str], int] = {}

    def reset(self) -> None:
        self._last_top = None
        self._last_top_signature = None
        self._stability.clear()
        self._c14_signatures.clear()
        self._c14_stability.clear()

    def evaluate(
        self,
        activations: Mapping[tuple[str | None, str], float],
        ledger: EvidenceLedger,
        *,
        now: float,
        mode: str = LEGACY_MODE,
    ) -> IgnitionDecision:
        if mode == C14_BOUNDED_MODE:
            return self._evaluate_c14(activations, ledger, now=now)
        if mode != LEGACY_MODE:
            raise ValueError(f"unsupported Coalition gate mode: {mode}")
        return self._evaluate_legacy(activations, ledger, now=now)

    def _evaluate_legacy(
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

    def _evaluate_c14(
        self,
        activations: Mapping[tuple[str | None, str], float],
        ledger: EvidenceLedger,
        *,
        now: float,
    ) -> IgnitionDecision:
        if isinstance(now, bool) or not isinstance(now, (int, float)) or not math.isfinite(now):
            raise ValueError("C14 evaluation time must be finite")
        if now < 0:
            raise ValueError("C14 evaluation time must be non-negative")

        drafts: list[dict[str, object]] = []
        for key, raw_activation in sorted(
            activations.items(), key=lambda item: ((item[0][0] or ""), item[0][1])
        ):
            object_key, belief_key = key
            if object_key is not None and (
                not isinstance(object_key, str) or not object_key.strip()
            ):
                raise ValueError("C14 entity keys must be non-empty strings or null")
            if not isinstance(belief_key, str) or not belief_key.strip():
                raise ValueError("C14 hypothesis IDs must be non-empty strings")
            if (
                isinstance(raw_activation, bool)
                or not isinstance(raw_activation, (int, float))
                or not math.isfinite(raw_activation)
            ):
                raise ValueError("C14 activations must be finite numbers")
            summary = ledger.summary(belief_key, object_key=object_key, now=float(now))
            support_times = tuple(ledger.resolve(item).time for item in summary.support_ids)
            recency = (
                sum(math.exp(-max(0.0, float(now) - item) / 30.0) for item in support_times)
                / len(support_times)
                if support_times
                else 0.0
            )
            signature = (
                object_key,
                belief_key,
                float(raw_activation),
                summary.support_ids,
                summary.contradiction_ids,
                summary.source_count,
                summary.independent_group_count,
                summary.unique_evidence_count,
                summary.effective_support,
                summary.effective_contradiction,
                summary.redundancy,
            )
            drafts.append(
                {
                    "key": key,
                    "activation": float(raw_activation),
                    "summary": summary,
                    "support_times": support_times,
                    "recency": recency,
                    "signature": signature,
                }
            )

        next_signatures = dict(self._c14_signatures)
        next_stability = dict(self._c14_stability)
        active_keys = {draft["key"] for draft in drafts}
        for draft in drafts:
            key = draft["key"]
            signature = draft["signature"]
            if next_signatures.get(key) == signature:
                next_stability[key] = next_stability.get(key, 0) + 1
            else:
                next_signatures[key] = signature
                next_stability[key] = 1
        for key in tuple(next_stability):
            if key not in active_keys:
                del next_stability[key]
                next_signatures.pop(key, None)

        coalitions: list[CoalitionState] = []
        for draft in drafts:
            key = draft["key"]
            object_key, belief_key = key
            summary = draft["summary"]
            stability = next_stability[key]
            activation = min(max(float(draft["activation"]), 0.0), 1.0)
            support = 1.0 - math.exp(-max(summary.effective_support, 0.0))
            source_diversity = min(summary.source_count / 2.0, 1.0)
            group_diversity = min(summary.independent_group_count / 2.0, 1.0)
            temporal_stability = min(stability / 2.0, 1.0)
            recency = min(max(float(draft["recency"]), 0.0), 1.0)
            contradiction = 1.0 - math.exp(-max(summary.effective_contradiction, 0.0))
            redundancy = 1.0 - math.exp(-max(summary.redundancy, 0.0))
            weighted = {
                "activation": _C14_WEIGHTS["activation"] * activation,
                "support": _C14_WEIGHTS["effective_support"] * support,
                "source": _C14_WEIGHTS["source_diversity"] * source_diversity,
                "group": _C14_WEIGHTS["group_diversity"] * group_diversity,
                "stability": _C14_WEIGHTS["temporal_stability"] * temporal_stability,
                "recency": _C14_WEIGHTS["recency"] * recency,
                "contradiction": _C14_WEIGHTS["contradiction"] * contradiction,
                "redundancy": _C14_WEIGHTS["redundancy"] * redundancy,
            }
            score = sum(weighted.values())
            coalitions.append(
                CoalitionState(
                    belief_key=belief_key,
                    object_key=object_key,
                    score=score,
                    activation=float(draft["activation"]),
                    effective_support=summary.effective_support,
                    effective_contradiction=summary.effective_contradiction,
                    redundancy=summary.redundancy,
                    source_count=summary.source_count,
                    independent_group_count=summary.independent_group_count,
                    evidence_count=summary.unique_evidence_count,
                    stability=stability,
                    support_ids=summary.support_ids,
                    contradiction_ids=summary.contradiction_ids,
                    support_times=draft["support_times"],
                    normalized_activation=activation,
                    normalized_support=support,
                    normalized_source_diversity=source_diversity,
                    normalized_group_diversity=group_diversity,
                    normalized_stability=temporal_stability,
                    normalized_recency=recency,
                    normalized_contradiction=contradiction,
                    normalized_redundancy=redundancy,
                    weighted_activation=weighted["activation"],
                    weighted_support=weighted["support"],
                    weighted_source_diversity=weighted["source"],
                    weighted_group_diversity=weighted["group"],
                    weighted_stability=weighted["stability"],
                    weighted_recency=weighted["recency"],
                    weighted_contradiction=weighted["contradiction"],
                    weighted_redundancy=weighted["redundancy"],
                )
            )

        coalitions.sort(key=lambda item: (-item.score, item.object_key or "", item.belief_key))
        if not coalitions:
            self._c14_signatures = next_signatures
            self._c14_stability = next_stability
            return IgnitionDecision(False, None, None, 0.0, 0.0, "no_candidates", ())

        self._c14_signatures = next_signatures
        self._c14_stability = next_stability
        result = tuple(coalitions)
        return decide_c14(result)

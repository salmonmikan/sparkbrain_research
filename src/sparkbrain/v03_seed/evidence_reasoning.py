from __future__ import annotations

import math

from .evidence import EvidenceLedger
from .evidence_worlds import G0Decision

G0_HYPOTHESES = ("state-left", "state-right")


def probability_snapshot(
    ledger: EvidenceLedger, *, entity_key: str, hypothesis_id: str, now: float
) -> dict[str, object]:
    object_key = None if entity_key == "__global__" else entity_key
    summary = ledger.summary(hypothesis_id, object_key=object_key, now=now)
    logit = summary.effective_support - summary.effective_contradiction
    probability = 1.0 / (1.0 + math.exp(-logit))
    return {
        "active_projection": ledger.active_projection(entity_key),
        "citations": list(summary.support_ids + summary.contradiction_ids),
        "confidence": max(probability, 1.0 - probability),
        "positive_probability": probability,
        "probability_margin": abs(2.0 * probability - 1.0),
        "summary": {
            "contradiction_ids": list(summary.contradiction_ids),
            "effective_contradiction": summary.effective_contradiction,
            "effective_support": summary.effective_support,
            "independent_group_count": summary.independent_group_count,
            "redundancy": summary.redundancy,
            "source_count": summary.source_count,
            "support_ids": list(summary.support_ids),
            "unique_evidence_count": summary.unique_evidence_count,
        },
    }


def decide_g0(ledger: EvidenceLedger, *, entity_key: str, now: float) -> G0Decision:
    candidates: list[tuple[float, str, dict[str, object]]] = []
    for hypothesis_id in G0_HYPOTHESES:
        snapshot = probability_snapshot(
            ledger, entity_key=entity_key, hypothesis_id=hypothesis_id, now=now
        )
        probability = float(snapshot["positive_probability"])
        confidence = float(snapshot["confidence"])
        margin = float(snapshot["probability_margin"])
        if probability >= 0.5 and confidence >= 0.5 and margin >= 0.08:
            candidates.append((probability, hypothesis_id, snapshot))
    if not candidates:
        return G0Decision(None, None, None, None, (), True)
    probability, winner, snapshot = sorted(
        candidates, key=lambda item: (-item[0], item[1])
    )[0]
    citations = tuple(sorted(str(item) for item in snapshot["citations"]))
    return G0Decision(
        winner=winner,
        positive_probability=probability,
        confidence=float(snapshot["confidence"]),
        probability_margin=float(snapshot["probability_margin"]),
        citations=citations,
        abstained=False,
    )


def aggregate_condition_rows(
    rows: list[dict[str, object]], *, condition_id: str
) -> list[dict[str, object]]:
    if not condition_id or any("condition_id" not in row for row in rows):
        raise ValueError("every execution row requires condition_id")
    observed = {row["condition_id"] for row in rows}
    if observed != {condition_id}:
        raise ValueError("E0 and E1 execution rows must not be merged")
    return rows

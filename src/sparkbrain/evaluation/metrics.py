from __future__ import annotations

import math
from collections import defaultdict
from statistics import mean
from typing import Any


def brier_score(probabilities: list[dict[str, float]], truths: list[str]) -> float | None:
    if not probabilities or len(probabilities) != len(truths):
        return None
    return mean(
        sum((row.get(label, 0.0) - float(label == truth)) ** 2 for label in row)
        for row, truth in zip(probabilities, truths, strict=True)
    )


def expected_calibration_error(
    confidences: list[float], correct: list[bool], *, bins: int = 10
) -> float | None:
    if not confidences or len(confidences) != len(correct):
        return None
    grouped: dict[int, list[int]] = defaultdict(list)
    for index, confidence in enumerate(confidences):
        grouped[min(bins - 1, int(max(0.0, min(1.0, confidence)) * bins))].append(index)
    total = len(confidences)
    return sum(
        len(indices)
        / total
        * abs(mean(float(correct[i]) for i in indices) - mean(confidences[i] for i in indices))
        for indices in grouped.values()
    )


def quantiles(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {key: None for key in ("mean", "p50", "p95", "p99", "max")}
    ordered = sorted(values)

    def pick(q: float) -> float:
        return ordered[min(len(ordered) - 1, math.ceil(q * len(ordered)) - 1)]

    return {
        "mean": mean(values),
        "p50": pick(0.50),
        "p95": pick(0.95),
        "p99": pick(0.99),
        "max": ordered[-1],
    }


def pareto_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row in rows:
        dominated_by: list[str] = []
        for other in rows:
            if other is row:
                continue
            no_worse = (
                other["unnecessary_revision_rate"] <= row["unnecessary_revision_rate"]
                and other["revision_recall"] >= row["revision_recall"]
                and other["mean_switch_latency"] <= row["mean_switch_latency"]
            )
            better = (
                other["unnecessary_revision_rate"] < row["unnecessary_revision_rate"]
                or other["revision_recall"] > row["revision_recall"]
                or other["mean_switch_latency"] < row["mean_switch_latency"]
            )
            if no_worse and better:
                dominated_by.append(str(other["condition"]))
        result.append({**row, "dominated": bool(dominated_by), "dominated_by": dominated_by})
    return result

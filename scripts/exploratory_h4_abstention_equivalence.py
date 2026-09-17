"""EXPLORATORY / NON_EVIDENTIARY H4 abstention-equivalence probe."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from itertools import product

MARGINS = (0.20, 0.35, 0.50, 0.65, 0.80, 0.95)
DIVERSITIES = (1, 2, 3, 4)
CONTRADICTIONS = (False, True)
VARIANTS = tuple(range(4))


@dataclass(frozen=True)
class SelectiveMetrics:
    accepted: int
    total: int
    coverage: float
    selective_risk: float


@dataclass(frozen=True)
class Example:
    margin: float
    diversity: int
    contradiction: bool
    variant: int
    prediction_correct: bool
    matched_feature_score: float


def build_examples() -> list[Example]:
    """Build a fixed synthetic selective-prediction grid."""
    examples: list[Example] = []
    for margin, diversity, contradiction, variant in product(
        MARGINS,
        DIVERSITIES,
        CONTRADICTIONS,
        VARIANTS,
    ):
        reliability = margin
        reliability += 0.15 if diversity >= 2 else -0.05
        reliability -= 0.35 if contradiction else 0.0
        reliability = max(0.0, min(1.0, reliability))
        deterministic_quantile = (variant + 0.5) / len(VARIANTS)

        matched_feature_score = margin + 0.10 * (diversity - 1)
        matched_feature_score -= 0.35 if contradiction else 0.0

        examples.append(
            Example(
                margin=margin,
                diversity=diversity,
                contradiction=contradiction,
                variant=variant,
                prediction_correct=deterministic_quantile <= reliability,
                matched_feature_score=round(matched_feature_score, 2),
            )
        )
    return examples


def _metrics(examples: list[Example], accepted: list[Example]) -> SelectiveMetrics:
    if not accepted:
        return SelectiveMetrics(
            accepted=0,
            total=len(examples),
            coverage=0.0,
            selective_risk=0.0,
        )

    correct = sum(int(example.prediction_correct) for example in accepted)
    return SelectiveMetrics(
        accepted=len(accepted),
        total=len(examples),
        coverage=len(accepted) / len(examples),
        selective_risk=1.0 - correct / len(accepted),
    )


def workspace_no_ignition_metrics(examples: list[Example]) -> SelectiveMetrics:
    """Fixed toy workspace gate using margin, diversity, and contradiction."""
    accepted = [
        example
        for example in examples
        if example.margin >= 0.50
        and example.diversity >= 2
        and not example.contradiction
    ]
    return _metrics(examples, accepted)


def margin_only_frontier(examples: list[Example]) -> list[dict[str, object]]:
    """Ordinary abstention restricted to the scalar prediction margin."""
    frontier: list[dict[str, object]] = []
    for threshold in MARGINS:
        metrics = _metrics(
            examples,
            [example for example in examples if example.margin >= threshold],
        )
        frontier.append({"threshold": threshold, **asdict(metrics)})
    return frontier


def matched_feature_frontier(examples: list[Example]) -> list[dict[str, object]]:
    """Ordinary scalar abstention with the same uncertainty features as the gate."""
    thresholds = sorted({example.matched_feature_score for example in examples})
    frontier: list[dict[str, object]] = []
    for threshold in thresholds:
        metrics = _metrics(
            examples,
            [
                example
                for example in examples
                if example.matched_feature_score >= threshold
            ],
        )
        frontier.append({"threshold": threshold, **asdict(metrics)})
    return frontier


def build_report() -> dict[str, object]:
    examples = build_examples()
    workspace = workspace_no_ignition_metrics(examples)
    margin_frontier = margin_only_frontier(examples)
    matched_frontier = matched_feature_frontier(examples)

    matched_dominators = [
        point
        for point in matched_frontier
        if point["coverage"] >= workspace.coverage
        and point["selective_risk"] <= workspace.selective_risk
        and (
            point["coverage"] > workspace.coverage
            or point["selective_risk"] < workspace.selective_risk
        )
    ]
    best_margin_at_or_above_coverage = min(
        (
            point
            for point in margin_frontier
            if point["coverage"] >= workspace.coverage
        ),
        key=lambda point: point["selective_risk"],
    )
    best_matched_dominator = min(
        matched_dominators,
        key=lambda point: (point["selective_risk"], -point["coverage"]),
    )

    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "hypothesis_or_reduction_question": (
            "Does toy no-ignition retain a selective-prediction advantage once an ordinary "
            "abstention comparator receives the same margin/diversity/contradiction information?"
        ),
        "inputs": {
            "margins": list(MARGINS),
            "diversities": list(DIVERSITIES),
            "contradictions": list(CONTRADICTIONS),
            "variants": list(VARIANTS),
            "example_count": len(examples),
        },
        "workspace_no_ignition": asdict(workspace),
        "margin_only_abstention_frontier": margin_frontier,
        "matched_feature_abstention_frontier": matched_frontier,
        "comparison": {
            "best_margin_only_at_or_above_workspace_coverage": (
                best_margin_at_or_above_coverage
            ),
            "matched_feature_dominator_count": len(matched_dominators),
            "best_matched_feature_dominator": best_matched_dominator,
            "workspace_dominated_when_information_matched": bool(matched_dominators),
        },
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

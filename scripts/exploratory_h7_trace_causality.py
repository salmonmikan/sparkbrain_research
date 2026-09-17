"""EXPLORATORY / NON_EVIDENTIARY H7 trace-causality bypass probe."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

EXAMPLE_COUNT = 64
BYPASS_COVERAGES = (0.0, 0.25, 0.50, 0.75, 1.0)
BYPASS_WEIGHT = 1.5
ROUTED_WEIGHT = 1.0


@dataclass(frozen=True)
class Scenario:
    bypass_coverage: float
    baseline_accuracy: float
    route_stability: float
    trace_deletion_accuracy: float
    wrong_route_replacement_accuracy: float
    deletion_sensitivity: float
    replacement_sensitivity: float


def _is_correct(score: float, target: int) -> bool:
    return score * target > 0.0


def scenario(bypass_coverage: float) -> Scenario:
    """Measure stable trace IDs against causal interventions under a hidden bypass."""
    if bypass_coverage not in BYPASS_COVERAGES:
        raise ValueError("bypass_coverage must be one of the fixed exploratory values")

    covered_examples = int(EXAMPLE_COUNT * bypass_coverage)
    baseline_correct = 0
    deletion_correct = 0
    replacement_correct = 0
    stable_routes = 0

    for index in range(EXAMPLE_COUNT):
        target = 1 if index % 2 == 0 else -1
        route_id = index % 2
        nuisance_view_route_id = index % 2
        stable_routes += int(route_id == nuisance_view_route_id)

        bypass_vote = BYPASS_WEIGHT * target if index < covered_examples else 0.0
        routed_vote = ROUTED_WEIGHT * target
        wrong_route_vote = -ROUTED_WEIGHT * target

        baseline_correct += int(_is_correct(routed_vote + bypass_vote, target))
        deletion_correct += int(_is_correct(bypass_vote, target))
        replacement_correct += int(_is_correct(wrong_route_vote + bypass_vote, target))

    baseline_accuracy = baseline_correct / EXAMPLE_COUNT
    deletion_accuracy = deletion_correct / EXAMPLE_COUNT
    replacement_accuracy = replacement_correct / EXAMPLE_COUNT

    return Scenario(
        bypass_coverage=bypass_coverage,
        baseline_accuracy=baseline_accuracy,
        route_stability=stable_routes / EXAMPLE_COUNT,
        trace_deletion_accuracy=deletion_accuracy,
        wrong_route_replacement_accuracy=replacement_accuracy,
        deletion_sensitivity=baseline_accuracy - deletion_accuracy,
        replacement_sensitivity=baseline_accuracy - replacement_accuracy,
    )


def build_report() -> dict[str, object]:
    scenarios = [scenario(coverage) for coverage in BYPASS_COVERAGES]
    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "hypothesis": (
            "Stable learned-route identifiers can coexist with weak trace-to-output causal "
            "necessity when an unreported bypass carries the same task signal"
        ),
        "example_count": EXAMPLE_COUNT,
        "routed_weight": ROUTED_WEIGHT,
        "bypass_weight": BYPASS_WEIGHT,
        "scenarios": [asdict(item) for item in scenarios],
        "summary": {
            "route_stability_all_scenarios": all(
                item.route_stability == 1.0 for item in scenarios
            ),
            "baseline_accuracy_all_scenarios": all(
                item.baseline_accuracy == 1.0 for item in scenarios
            ),
            "deletion_sensitivity_range": [
                min(item.deletion_sensitivity for item in scenarios),
                max(item.deletion_sensitivity for item in scenarios),
            ],
            "replacement_sensitivity_range": [
                min(item.replacement_sensitivity for item in scenarios),
                max(item.replacement_sensitivity for item in scenarios),
            ],
        },
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

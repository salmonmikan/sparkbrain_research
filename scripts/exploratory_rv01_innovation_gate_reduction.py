"""EXPLORATORY / NON_EVIDENTIARY final RV01 scalar-filter reduction probe.

Evidence Analyst authority 719b9e74063e5e10f6226fd49f1835036ed75e5b permits exactly one
final stronger ordinary scalar-filter probe after the clipped-EWMA sensitivity result.
This synthetic-only follow-up compares the same residual-deadzone learner with a stronger
ordinary innovation-gated EWMA. It cannot count as formal evidence or authorize execution.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from functools import cache
from pathlib import Path

from exploratory_rv01_delay_filter_reduction import (
    DEADZONE_ETAS,
    DEADZONE_WIDTHS,
    DEV_OUTLIER_PROBABILITY,
    DEV_SEEDS,
    TEST_OUTLIER_PROBABILITIES,
    TEST_SEEDS,
    _deadzone_mean,
    _mean_metrics,
    _metrics,
    _utility,
    evaluate_deadzone,
    make_sequences,
)

GATED_EWMA_ALPHAS = (0.10, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80)
GATED_EWMA_THRESHOLDS = (0.20, 0.35, 0.50, 0.75, 1.0, 1.25, 1.50)


@cache
def evaluate_innovation_gated_ewma(
    *, seed: int, outlier_probability: float, alpha: float, threshold: float
) -> dict[str, float]:
    """Evaluate an ordinary one-scalar EWMA with a symmetric innovation gate."""
    rows: list[tuple[tuple[float, ...], tuple[float, ...]]] = []

    for truth, observations in make_sequences(
        seed=seed, outlier_probability=outlier_probability
    ):
        estimate = observations[0]
        predictions = [estimate]
        for observed in observations[1:]:
            residual = observed - estimate
            if abs(residual) >= threshold:
                estimate += alpha * residual
            predictions.append(estimate)
        rows.append((truth, tuple(predictions)))

    return _metrics(rows)


def _gated_mean(
    *, seeds: Iterable[int], alpha: float, threshold: float
) -> dict[str, float]:
    return _mean_metrics(
        evaluate_innovation_gated_ewma(
            seed=seed,
            outlier_probability=DEV_OUTLIER_PROBABILITY,
            alpha=alpha,
            threshold=threshold,
        )
        for seed in seeds
    )


def _select_parameters() -> tuple[tuple[float, float], tuple[float, float]]:
    deadzone_parameters = max(
        ((eta, deadzone) for eta in DEADZONE_ETAS for deadzone in DEADZONE_WIDTHS),
        key=lambda parameters: (
            _utility(
                _deadzone_mean(
                    seeds=DEV_SEEDS,
                    eta=parameters[0],
                    deadzone=parameters[1],
                )
            ),
            -parameters[0],
            -parameters[1],
        ),
    )
    gated_parameters = max(
        (
            (alpha, threshold)
            for alpha in GATED_EWMA_ALPHAS
            for threshold in GATED_EWMA_THRESHOLDS
        ),
        key=lambda parameters: (
            _utility(
                _gated_mean(
                    seeds=DEV_SEEDS,
                    alpha=parameters[0],
                    threshold=parameters[1],
                )
            ),
            -parameters[0],
            -parameters[1],
        ),
    )
    return deadzone_parameters, gated_parameters


@cache
def run_probe() -> dict[str, object]:
    """Select on DEV once, then open the fixed disjoint TEST sweep once."""
    deadzone_parameters, gated_parameters = _select_parameters()
    rows: list[dict[str, object]] = []

    for outlier_probability in TEST_OUTLIER_PROBABILITIES:
        deadzone_metrics = _mean_metrics(
            evaluate_deadzone(
                seed=seed,
                outlier_probability=outlier_probability,
                eta=deadzone_parameters[0],
                deadzone=deadzone_parameters[1],
            )
            for seed in TEST_SEEDS
        )
        gated_metrics = _mean_metrics(
            evaluate_innovation_gated_ewma(
                seed=seed,
                outlier_probability=outlier_probability,
                alpha=gated_parameters[0],
                threshold=gated_parameters[1],
            )
            for seed in TEST_SEEDS
        )
        deadzone_utility = _utility(deadzone_metrics)
        gated_utility = _utility(gated_metrics)
        rows.append(
            {
                "outlier_probability": outlier_probability,
                "deadzone_delay_learner": {
                    **deadzone_metrics,
                    "utility": deadzone_utility,
                },
                "generic_innovation_gated_ewma": {
                    **gated_metrics,
                    "utility": gated_utility,
                },
                "generic_minus_deadzone_utility": gated_utility - deadzone_utility,
            }
        )

    generic_wins = sum(
        int(float(row["generic_minus_deadzone_utility"]) > 0.0) for row in rows
    )
    deadzone_wins = sum(
        int(float(row["generic_minus_deadzone_utility"]) < 0.0) for row in rows
    )

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "mode": "exploratory_incubator",
        "exploratory_target": (
            "Final RV01 scalar-filter reduction: residual-deadzone learner versus "
            "resource-matched generic innovation-gated EWMA"
        ),
        "analyst_authority": "719b9e74063e5e10f6226fd49f1835036ed75e5b",
        "analyst_bound": (
            "Exactly one final stronger ordinary scalar-filter synthetic reduction, "
            "then mandatory stop/reclassification regardless of outcome."
        ),
        "interpretation_boundary": (
            "Synthetic reduction diagnostic only. It does not rerun or reinterpret consumed "
            "RV01 evidence and cannot support or reject RV01 scientifically."
        ),
        "synthetic_contract": {
            "source_world": "same fixed world as preceding RV01 clipped-EWMA probe",
            "dev_outlier_probability": DEV_OUTLIER_PROBABILITY,
            "test_outlier_probabilities": list(TEST_OUTLIER_PROBABILITIES),
            "dev_seeds": list(DEV_SEEDS),
            "test_seeds": list(TEST_SEEDS),
            "resource_match": (
                "Both filters retain exactly one persistent scalar delay estimate and select "
                "exactly two controls on DEV only."
            ),
            "selection_rule": (
                "Comparator family and both parameter grids were fixed before TEST. Each "
                "filter is selected independently on the single fixed DEV world, then "
                "parameters are frozen before the disjoint TEST sweep is opened. "
                "No TEST-driven comparator selection or tuning."
            ),
            "deadzone_parameter_grid": {
                "eta": list(DEADZONE_ETAS),
                "deadzone_ms": list(DEADZONE_WIDTHS),
            },
            "innovation_gated_ewma_parameter_grid": {
                "alpha": list(GATED_EWMA_ALPHAS),
                "gate_threshold_ms": list(GATED_EWMA_THRESHOLDS),
            },
        },
        "selected_on_dev": {
            "deadzone_delay_learner": {
                "eta": deadzone_parameters[0],
                "deadzone_ms": deadzone_parameters[1],
            },
            "generic_innovation_gated_ewma": {
                "alpha": gated_parameters[0],
                "gate_threshold_ms": gated_parameters[1],
            },
        },
        "rows": rows,
        "summary": {
            "deadzone_wins": deadzone_wins,
            "generic_wins": generic_wins,
            "crossover_observed": deadzone_wins > 0 and generic_wins > 0,
            "hard_stop_reached": True,
            "promotion_recommendation": "REJECT",
            "promotion_scope": (
                "Reject this exploratory candidate as a direct formalization basis. "
                "This is not a formal rejection of RV01."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_probe()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(text, end="")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

"""EXPLORATORY / NON_EVIDENTIARY RV01 delay-filter reduction probe.

This synthetic-only probe asks whether an RV01-motivated adaptive-delay update retains a
stable advantage over a strong ordinary robust scalar filter when both have one persistent
scalar and two DEV-selected controls. It does not execute, rerun, score, reinterpret, or
modify any consumed RV01 identity or formal SparkBrain evidence.
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Iterable
from functools import cache
from pathlib import Path

LEVELS = (1.0, 3.0, 5.0)
DEV_SEEDS = (20260901, 20260902, 20260903, 20260904, 20260905)
TEST_SEEDS = (20260918, 20260919, 20260920, 20260921, 20260922)
SEQUENCES_PER_SEED = 128
SEQUENCE_LENGTH = 64
STAY_PROBABILITY = 0.94
OBSERVATION_NOISE_SIGMA = 0.55
OUTLIER_MAGNITUDE = 3.0
DEV_OUTLIER_PROBABILITY = 0.06
TEST_OUTLIER_PROBABILITIES = (0.0, 0.03, 0.06, 0.12, 0.20)

FALSE_ADJUSTMENT_WEIGHT = 0.20
SWITCH_LATENCY_WEIGHT = 0.03
RETURN_RECOVERY_WEIGHT = 0.15

DEADZONE_ETAS = (0.10, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80)
DEADZONE_WIDTHS = (0.0, 0.20, 0.35, 0.50, 0.75, 1.0)
CLIPPED_EWMA_ALPHAS = (0.10, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80)
CLIPPED_EWMA_CLIPS = (0.50, 1.0, 1.50, 2.0, 3.0, 4.0)


@cache
def make_sequences(
    *, seed: int, outlier_probability: float
) -> tuple[tuple[tuple[float, ...], tuple[float, ...]], ...]:
    """Create coupled synthetic changing-delay sequences with noisy observations."""
    rng = random.Random(seed)
    sequences: list[tuple[tuple[float, ...], tuple[float, ...]]] = []

    for _ in range(SEQUENCES_PER_SEED):
        current = rng.choice(LEVELS)
        truth: list[float] = []
        observations: list[float] = []

        for step in range(SEQUENCE_LENGTH):
            transition_draw = rng.random() if step else 0.0
            next_level = rng.choice(tuple(level for level in LEVELS if level != current))
            if step and transition_draw >= STAY_PROBABILITY:
                current = next_level
            truth.append(current)

            noise = rng.gauss(0.0, OBSERVATION_NOISE_SIGMA)
            outlier_draw = rng.random()
            outlier_sign = rng.choice((-1.0, 1.0))
            outlier = (
                outlier_sign * OUTLIER_MAGNITUDE
                if outlier_draw < outlier_probability
                else 0.0
            )
            observations.append(current + noise + outlier)

        sequences.append((tuple(truth), tuple(observations)))

    return tuple(sequences)


def _metrics(
    rows: Iterable[tuple[tuple[float, ...], tuple[float, ...]]],
) -> dict[str, float]:
    absolute_error = 0.0
    total = 0
    false_adjustments = 0
    stable_steps = 0
    switch_latencies: list[int] = []
    return_events = 0
    return_recoveries = 0

    for truth, predictions in rows:
        absolute_error += sum(
            abs(target - prediction)
            for target, prediction in zip(truth, predictions, strict=True)
        )
        total += len(truth)
        seen_levels = {truth[0]}

        for step in range(1, len(truth)):
            if truth[step] == truth[step - 1]:
                stable_steps += 1
                false_adjustments += int(abs(predictions[step] - predictions[step - 1]) > 0.15)
                continue

            target = truth[step]
            latency = 8
            for candidate_step in range(step, min(len(truth), step + 8)):
                if abs(predictions[candidate_step] - target) <= 0.50:
                    latency = candidate_step - step
                    break
            switch_latencies.append(latency)

            if target in seen_levels:
                return_events += 1
                return_recoveries += int(
                    any(
                        abs(predictions[candidate_step] - target) <= 0.50
                        for candidate_step in range(step, min(len(truth), step + 3))
                    )
                )
            seen_levels.add(target)

    return {
        "mae": absolute_error / total,
        "false_adjustment_rate": false_adjustments / stable_steps,
        "switch_latency": sum(switch_latencies) / len(switch_latencies),
        "return_recovery_2step": return_recoveries / return_events,
    }


@cache
def evaluate_deadzone(
    *, seed: int, outlier_probability: float, eta: float, deadzone: float
) -> dict[str, float]:
    """Evaluate an RV01-motivated scalar delay learner with a residual deadzone."""
    rows: list[tuple[tuple[float, ...], tuple[float, ...]]] = []

    for truth, observations in make_sequences(
        seed=seed, outlier_probability=outlier_probability
    ):
        estimate = observations[0]
        predictions = [estimate]
        for observed in observations[1:]:
            residual = observed - estimate
            magnitude = max(0.0, abs(residual) - deadzone)
            sign = 1.0 if residual >= 0.0 else -1.0
            estimate += eta * sign * magnitude
            predictions.append(estimate)
        rows.append((truth, tuple(predictions)))

    return _metrics(rows)


@cache
def evaluate_clipped_ewma(
    *, seed: int, outlier_probability: float, alpha: float, clip: float
) -> dict[str, float]:
    """Evaluate a generic robust EWMA with clipped innovation."""
    rows: list[tuple[tuple[float, ...], tuple[float, ...]]] = []

    for truth, observations in make_sequences(
        seed=seed, outlier_probability=outlier_probability
    ):
        estimate = observations[0]
        predictions = [estimate]
        for observed in observations[1:]:
            residual = max(-clip, min(clip, observed - estimate))
            estimate += alpha * residual
            predictions.append(estimate)
        rows.append((truth, tuple(predictions)))

    return _metrics(rows)


def _mean_metrics(rows: Iterable[dict[str, float]]) -> dict[str, float]:
    rows = tuple(rows)
    return {key: sum(row[key] for row in rows) / len(rows) for key in rows[0]}


def _utility(metrics: dict[str, float]) -> float:
    return (
        -metrics["mae"]
        - FALSE_ADJUSTMENT_WEIGHT * metrics["false_adjustment_rate"]
        - SWITCH_LATENCY_WEIGHT * metrics["switch_latency"]
        + RETURN_RECOVERY_WEIGHT * metrics["return_recovery_2step"]
    )


def _deadzone_mean(*, seeds: Iterable[int], eta: float, deadzone: float) -> dict[str, float]:
    return _mean_metrics(
        evaluate_deadzone(
            seed=seed,
            outlier_probability=DEV_OUTLIER_PROBABILITY,
            eta=eta,
            deadzone=deadzone,
        )
        for seed in seeds
    )


def _clipped_mean(*, seeds: Iterable[int], alpha: float, clip: float) -> dict[str, float]:
    return _mean_metrics(
        evaluate_clipped_ewma(
            seed=seed,
            outlier_probability=DEV_OUTLIER_PROBABILITY,
            alpha=alpha,
            clip=clip,
        )
        for seed in seeds
    )


def _select_parameters() -> tuple[tuple[float, float], tuple[float, float]]:
    deadzone_parameters = max(
        ((eta, deadzone) for eta in DEADZONE_ETAS for deadzone in DEADZONE_WIDTHS),
        key=lambda parameters: (
            _utility(
                _deadzone_mean(
                    seeds=DEV_SEEDS, eta=parameters[0], deadzone=parameters[1]
                )
            ),
            -parameters[0],
            -parameters[1],
        ),
    )
    clipped_parameters = max(
        ((alpha, clip) for alpha in CLIPPED_EWMA_ALPHAS for clip in CLIPPED_EWMA_CLIPS),
        key=lambda parameters: (
            _utility(
                _clipped_mean(
                    seeds=DEV_SEEDS, alpha=parameters[0], clip=parameters[1]
                )
            ),
            -parameters[0],
            -parameters[1],
        ),
    )
    return deadzone_parameters, clipped_parameters


@cache
def run_probe() -> dict[str, object]:
    """Select on DEV once, then sensitivity-test fixed parameters on disjoint TEST seeds."""
    deadzone_parameters, clipped_parameters = _select_parameters()
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
        clipped_metrics = _mean_metrics(
            evaluate_clipped_ewma(
                seed=seed,
                outlier_probability=outlier_probability,
                alpha=clipped_parameters[0],
                clip=clipped_parameters[1],
            )
            for seed in TEST_SEEDS
        )
        deadzone_utility = _utility(deadzone_metrics)
        clipped_utility = _utility(clipped_metrics)
        rows.append(
            {
                "outlier_probability": outlier_probability,
                "deadzone_delay_learner": {
                    **deadzone_metrics,
                    "utility": deadzone_utility,
                },
                "generic_clipped_ewma": {
                    **clipped_metrics,
                    "utility": clipped_utility,
                },
                "generic_minus_deadzone_utility": clipped_utility - deadzone_utility,
            }
        )

    generic_wins = sum(int(float(row["generic_minus_deadzone_utility"]) > 0.0) for row in rows)
    deadzone_wins = sum(int(float(row["generic_minus_deadzone_utility"]) < 0.0) for row in rows)

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "exploratory_target": (
            "RV01 adaptive-delay reduction sensitivity: residual-deadzone learner versus "
            "resource-matched generic clipped EWMA"
        ),
        "interpretation_boundary": (
            "Synthetic reduction diagnostic only. It does not rerun or reinterpret consumed "
            "RV01 evidence and cannot support or reject RV01 scientifically."
        ),
        "synthetic_contract": {
            "latent_delay_levels_ms": list(LEVELS),
            "sequences_per_seed": SEQUENCES_PER_SEED,
            "sequence_length": SEQUENCE_LENGTH,
            "stay_probability": STAY_PROBABILITY,
            "observation_noise_sigma_ms": OBSERVATION_NOISE_SIGMA,
            "outlier_magnitude_ms": OUTLIER_MAGNITUDE,
            "dev_outlier_probability": DEV_OUTLIER_PROBABILITY,
            "test_outlier_probabilities": list(TEST_OUTLIER_PROBABILITIES),
            "dev_seeds": list(DEV_SEEDS),
            "test_seeds": list(TEST_SEEDS),
            "resource_match": (
                "Both filters retain exactly one persistent scalar delay estimate and select "
                "exactly two control parameters on DEV only."
            ),
            "selection_rule": (
                "Select each filter independently on the single fixed DEV world at outlier "
                "probability 0.06, then keep parameters fixed across disjoint TEST seeds and "
                "the full outlier sensitivity sweep."
            ),
            "utility": {
                "formula": (
                    "-mae - 0.20*false_adjustment_rate - 0.03*switch_latency "
                    "+ 0.15*return_recovery_2step"
                ),
                "false_adjustment_threshold_ms": 0.15,
                "recovery_tolerance_ms": 0.50,
                "switch_latency_cap_steps": 8,
            },
            "deadzone_parameter_grid": {
                "eta": list(DEADZONE_ETAS),
                "deadzone_ms": list(DEADZONE_WIDTHS),
            },
            "clipped_ewma_parameter_grid": {
                "alpha": list(CLIPPED_EWMA_ALPHAS),
                "innovation_clip_ms": list(CLIPPED_EWMA_CLIPS),
            },
        },
        "selected_on_dev": {
            "deadzone_delay_learner": {
                "eta": deadzone_parameters[0],
                "deadzone_ms": deadzone_parameters[1],
            },
            "generic_clipped_ewma": {
                "alpha": clipped_parameters[0],
                "innovation_clip_ms": clipped_parameters[1],
            },
        },
        "rows": rows,
        "summary": {
            "deadzone_wins": deadzone_wins,
            "generic_wins": generic_wins,
            "crossover_observed": deadzone_wins > 0 and generic_wins > 0,
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

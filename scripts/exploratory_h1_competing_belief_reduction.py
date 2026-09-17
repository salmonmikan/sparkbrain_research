"""EXPLORATORY / NON_EVIDENTIARY H1 matched-probabilistic reduction probe.

This synthetic-only probe asks whether an explicit competing-belief heuristic retains a
mechanism-specific advantage once a matched probabilistic recurrent filter receives the
same observations, three-state memory budget, and two DEV-selected control parameters.
It does not rerun, reinterpret, score, or modify any formal SparkBrain evidence.
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Iterable
from functools import cache

STATES = (0, 1, 2)
DEV_SEEDS = (20260901, 20260902, 20260903, 20260904, 20260905)
TEST_SEEDS = (20260918, 20260919, 20260920, 20260921, 20260922)
SEQUENCES_PER_SEED = 256
SEQUENCE_LENGTH = 72
WORLD_STAY_PROBABILITY = 0.92
WORLD_CORRECT_OBSERVATION_PROBABILITY = 0.68

COMPETING_DECAYS = (0.0, 0.25, 0.50, 0.65, 0.75, 0.82, 0.88, 0.92, 0.95, 0.97)
COMPETING_MARGINS = (0.0, 0.25, 0.50, 0.75, 1.0, 1.5)
PROBABILISTIC_STAY_PRIORS = (0.70, 0.80, 0.86, 0.90, 0.92, 0.94, 0.96, 0.98)
PROBABILISTIC_HYSTERESIS = (0.0, 0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35)

UTILITY_WEIGHTS = (
    (1.0, 0.03, 0.15),
    (2.0, 0.03, 0.15),
    (1.0, 0.06, 0.15),
    (1.0, 0.03, 0.30),
    (0.5, 0.02, 0.10),
    (2.0, 0.06, 0.30),
)


@cache
def make_sequences(*, seed: int) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Create fixed three-state non-monotonic Markov sequences and noisy observations."""
    rng = random.Random(seed)
    sequences: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for _ in range(SEQUENCES_PER_SEED):
        truth: list[int] = []
        observations: list[int] = []
        current = rng.choice(STATES)

        for step in range(SEQUENCE_LENGTH):
            if step > 0 and rng.random() >= WORLD_STAY_PROBABILITY:
                current = rng.choice(tuple(state for state in STATES if state != current))
            truth.append(current)

            if rng.random() < WORLD_CORRECT_OBSERVATION_PROBABILITY:
                observed = current
            else:
                observed = rng.choice(tuple(state for state in STATES if state != current))
            observations.append(observed)

        sequences.append((tuple(truth), tuple(observations)))

    return tuple(sequences)


def _argmax(values: list[float]) -> int:
    return max(STATES, key=lambda state: (values[state], -state))


def _metrics(
    rows: Iterable[tuple[tuple[int, ...], tuple[int, ...]]],
) -> dict[str, float]:
    correct = 0
    total = 0
    false_revisions = 0
    stable_steps = 0
    switch_latencies: list[int] = []
    return_events = 0
    return_recoveries = 0

    for truth, predictions in rows:
        correct += sum(
            int(target == prediction)
            for target, prediction in zip(truth, predictions, strict=True)
        )
        total += len(truth)
        seen_states = {truth[0]}

        for step in range(1, len(truth)):
            if truth[step] == truth[step - 1]:
                stable_steps += 1
                false_revisions += int(predictions[step] != predictions[step - 1])
                continue

            target = truth[step]
            latency = 7
            for candidate_step in range(step, min(len(truth), step + 7)):
                if predictions[candidate_step] == target:
                    latency = candidate_step - step
                    break
            switch_latencies.append(latency)

            if target in seen_states:
                return_events += 1
                return_recoveries += int(
                    any(
                        predictions[candidate_step] == target
                        for candidate_step in range(step, min(len(truth), step + 3))
                    )
                )
            seen_states.add(target)

    return {
        "accuracy": correct / total,
        "false_revision_rate": false_revisions / stable_steps,
        "switch_latency": sum(switch_latencies) / len(switch_latencies),
        "return_recovery_2step": return_recoveries / return_events,
    }


@cache
def evaluate_competing(*, seed: int, decay: float, margin: float) -> dict[str, float]:
    """Evaluate explicit three-score competing beliefs with revision hysteresis."""
    rows: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for truth, observations in make_sequences(seed=seed):
        scores = [0.0, 0.0, 0.0]
        prediction = 0
        predictions: list[int] = []

        for step, observed in enumerate(observations):
            scores = [decay * value for value in scores]
            scores[observed] += 1.0
            challenger = _argmax(scores)

            if step == 0 or (
                challenger != prediction
                and scores[challenger] - scores[prediction] >= margin
            ):
                prediction = challenger
            predictions.append(prediction)

        rows.append((truth, tuple(predictions)))

    return _metrics(rows)


@cache
def evaluate_probabilistic(
    *,
    seed: int,
    stay_prior: float,
    hysteresis: float,
) -> dict[str, float]:
    """Evaluate a generic three-state HMM-style filter with matched hysteresis."""
    rows: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    switch_prior = (1.0 - stay_prior) / 2.0
    wrong_observation = (1.0 - WORLD_CORRECT_OBSERVATION_PROBABILITY) / 2.0

    for truth, observations in make_sequences(seed=seed):
        posterior = [1.0 / 3.0] * 3
        prediction = 0
        predictions: list[int] = []

        for step, observed in enumerate(observations):
            total_mass = sum(posterior)
            prior = [
                stay_prior * posterior[state]
                + switch_prior * (total_mass - posterior[state])
                for state in STATES
            ]
            unnormalized = [
                prior[state]
                * (
                    WORLD_CORRECT_OBSERVATION_PROBABILITY
                    if observed == state
                    else wrong_observation
                )
                for state in STATES
            ]
            normalization = sum(unnormalized)
            posterior = [value / normalization for value in unnormalized]
            challenger = _argmax(posterior)

            if step == 0 or (
                challenger != prediction
                and posterior[challenger] - posterior[prediction] >= hysteresis
            ):
                prediction = challenger
            predictions.append(prediction)

        rows.append((truth, tuple(predictions)))

    return _metrics(rows)


def mean_metrics(
    evaluator: object,
    *,
    seeds: Iterable[int],
    first_parameter: float,
    second_parameter: float,
) -> dict[str, float]:
    if evaluator == "competing":
        metrics = [
            evaluate_competing(seed=seed, decay=first_parameter, margin=second_parameter)
            for seed in seeds
        ]
    elif evaluator == "probabilistic":
        metrics = [
            evaluate_probabilistic(
                seed=seed,
                stay_prior=first_parameter,
                hysteresis=second_parameter,
            )
            for seed in seeds
        ]
    else:
        raise ValueError(f"unknown evaluator: {evaluator}")

    return {
        key: sum(row[key] for row in metrics) / len(metrics)
        for key in metrics[0]
    }


def utility(
    metrics: dict[str, float],
    *,
    false_revision_weight: float,
    latency_weight: float,
    return_recovery_weight: float,
) -> float:
    return (
        metrics["accuracy"]
        - false_revision_weight * metrics["false_revision_rate"]
        - latency_weight * metrics["switch_latency"]
        + return_recovery_weight * metrics["return_recovery_2step"]
    )


def _precompute_dev() -> tuple[
    dict[tuple[float, float], dict[str, float]],
    dict[tuple[float, float], dict[str, float]],
]:
    competing = {
        (decay, margin): mean_metrics(
            "competing",
            seeds=DEV_SEEDS,
            first_parameter=decay,
            second_parameter=margin,
        )
        for decay in COMPETING_DECAYS
        for margin in COMPETING_MARGINS
    }
    probabilistic = {
        (stay_prior, hysteresis): mean_metrics(
            "probabilistic",
            seeds=DEV_SEEDS,
            first_parameter=stay_prior,
            second_parameter=hysteresis,
        )
        for stay_prior in PROBABILISTIC_STAY_PRIORS
        for hysteresis in PROBABILISTIC_HYSTERESIS
    }
    return competing, probabilistic


def run_probe() -> dict[str, object]:
    competing_dev, probabilistic_dev = _precompute_dev()
    rows: list[dict[str, object]] = []

    for false_weight, latency_weight, return_weight in UTILITY_WEIGHTS:
        competing_parameters = max(
            competing_dev,
            key=lambda parameters: (
                utility(
                    competing_dev[parameters],
                    false_revision_weight=false_weight,
                    latency_weight=latency_weight,
                    return_recovery_weight=return_weight,
                ),
                -parameters[0],
                -parameters[1],
            ),
        )
        probabilistic_parameters = max(
            probabilistic_dev,
            key=lambda parameters: (
                utility(
                    probabilistic_dev[parameters],
                    false_revision_weight=false_weight,
                    latency_weight=latency_weight,
                    return_recovery_weight=return_weight,
                ),
                -parameters[0],
                -parameters[1],
            ),
        )

        competing_test = mean_metrics(
            "competing",
            seeds=TEST_SEEDS,
            first_parameter=competing_parameters[0],
            second_parameter=competing_parameters[1],
        )
        probabilistic_test = mean_metrics(
            "probabilistic",
            seeds=TEST_SEEDS,
            first_parameter=probabilistic_parameters[0],
            second_parameter=probabilistic_parameters[1],
        )
        competing_utility = utility(
            competing_test,
            false_revision_weight=false_weight,
            latency_weight=latency_weight,
            return_recovery_weight=return_weight,
        )
        probabilistic_utility = utility(
            probabilistic_test,
            false_revision_weight=false_weight,
            latency_weight=latency_weight,
            return_recovery_weight=return_weight,
        )

        rows.append(
            {
                "false_revision_weight": false_weight,
                "latency_weight": latency_weight,
                "return_recovery_weight": return_weight,
                "competing_beliefs": {
                    "selected_decay": competing_parameters[0],
                    "selected_margin": competing_parameters[1],
                    "test": {**competing_test, "utility": competing_utility},
                },
                "probabilistic_filter": {
                    "selected_stay_prior": probabilistic_parameters[0],
                    "selected_hysteresis": probabilistic_parameters[1],
                    "test": {**probabilistic_test, "utility": probabilistic_utility},
                },
                "probabilistic_minus_competing_test_utility": (
                    probabilistic_utility - competing_utility
                ),
            }
        )

    absolute_gaps = [
        abs(float(row["probabilistic_minus_competing_test_utility"]))
        for row in rows
    ]
    probabilistic_wins = sum(
        int(float(row["probabilistic_minus_competing_test_utility"]) > 0.0)
        for row in rows
    )

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "exploratory_target": (
            "H1 explicit competing-belief retention versus a matched probabilistic "
            "recurrent filter in a synthetic three-state non-monotonic world"
        ),
        "synthetic_contract": {
            "states": list(STATES),
            "sequences_per_seed": SEQUENCES_PER_SEED,
            "sequence_length": SEQUENCE_LENGTH,
            "world_stay_probability": WORLD_STAY_PROBABILITY,
            "world_correct_observation_probability": (
                WORLD_CORRECT_OBSERVATION_PROBABILITY
            ),
            "dev_seeds": list(DEV_SEEDS),
            "test_seeds": list(TEST_SEEDS),
            "memory_budget": (
                "Both mechanisms retain three scalar state values and use exactly two "
                "DEV-selected control parameters; neither sees TEST truth during selection."
            ),
            "competing_parameter_grid": {
                "decay": list(COMPETING_DECAYS),
                "revision_margin": list(COMPETING_MARGINS),
            },
            "probabilistic_parameter_grid": {
                "stay_prior": list(PROBABILISTIC_STAY_PRIORS),
                "revision_hysteresis": list(PROBABILISTIC_HYSTERESIS),
            },
            "probabilistic_observation_model": (
                "The synthetic observation reliability is part of the declared task model "
                "and is not tuned on TEST outcomes."
            ),
            "utility_weights": [
                {
                    "false_revision_weight": false_weight,
                    "latency_weight": latency_weight,
                    "return_recovery_weight": return_weight,
                }
                for false_weight, latency_weight, return_weight in UTILITY_WEIGHTS
            ],
            "selection_rule": (
                "Each mechanism selects its two parameters independently on DEV utility "
                "only, then evaluates those fixed parameters on disjoint TEST seeds."
            ),
        },
        "rows": rows,
        "summary": {
            "probabilistic_wins": probabilistic_wins,
            "competing_wins": len(rows) - probabilistic_wins,
            "max_absolute_test_utility_gap": max(absolute_gaps),
            "mean_absolute_test_utility_gap": sum(absolute_gaps) / len(absolute_gaps),
        },
        "interpretation_boundary": (
            "This is a synthetic reduction diagnostic only. Near-equivalence here cannot "
            "support or reject H1 formally and does not reinterpret any formal result."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(run_probe(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

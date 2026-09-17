"""EXPLORATORY / NON_EVIDENTIARY H2 matched-memory reduction probe.

This synthetic-only probe asks whether a residual-loser-specific recovery advantage
survives a simple resource-matched recurrent-memory reduction. It does not rerun,
reinterpret, score, or modify C15 or any formal SparkBrain evidence.
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache

DECAY_GRID = tuple(round(step / 100.0, 2) for step in range(96))
DWELL_STEPS = (2, 4, 8, 16)
DEV_SEEDS = (20260908, 20260909, 20260910, 20260911, 20260912)
TEST_SEEDS = (20260918, 20260919, 20260920, 20260921, 20260922)
UTILITY_WEIGHTS = (
    (0.5, 0.05),
    (1.0, 0.05),
    (2.0, 0.05),
    (0.5, 0.10),
    (1.0, 0.10),
    (2.0, 0.10),
    (1.0, 0.20),
)


@dataclass(frozen=True)
class Episode:
    truth: tuple[int, ...]
    evidence: tuple[float, ...]
    return_index: int


@cache
def make_episodes(*, seed: int, count: int = 512) -> tuple[Episode, ...]:
    """Create A -> B -> A returning-state episodes from a fixed synthetic world."""
    rng = random.Random(seed)
    episodes: list[Episode] = []
    for _ in range(count):
        dwell = rng.choice(DWELL_STEPS)
        truth = (1,) * 6 + (-1,) * dwell + (1,) * 6
        evidence = tuple(state * 1.0 + rng.gauss(0.0, 1.2) for state in truth)
        episodes.append(
            Episode(
                truth=truth,
                evidence=evidence,
                return_index=6 + dwell,
            )
        )
    return tuple(episodes)


def _predict(score_a: float, score_b: float) -> int:
    return 1 if score_a >= score_b else -1


@cache
def evaluate(*, seed: int, decay: float, mechanism: str) -> dict[str, float]:
    """Evaluate one fixed mechanism/decay without fitting to the evaluation seed."""
    if not 0.0 <= decay <= 0.95:
        raise ValueError("decay must be in [0, 0.95]")
    if mechanism not in {"residual_loser", "symmetric_recurrent"}:
        raise ValueError(f"unknown mechanism: {mechanism}")

    correct = 0
    total = 0
    false_revision = 0
    stable_a_steps = 0
    return_latencies: list[int] = []

    for episode in make_episodes(seed=seed):
        score_a = 0.0
        score_b = 0.0
        first_correct_return: int | None = None

        for step, (truth, evidence_delta) in enumerate(
            zip(episode.truth, episode.evidence, strict=True)
        ):
            evidence_a = evidence_delta
            evidence_b = -evidence_delta

            if mechanism == "residual_loser":
                if score_a >= score_b:
                    score_a, score_b = (
                        evidence_a,
                        decay * score_b + evidence_b,
                    )
                else:
                    score_a, score_b = (
                        decay * score_a + evidence_a,
                        evidence_b,
                    )
            else:
                score_a = decay * score_a + evidence_a
                score_b = decay * score_b + evidence_b

            prediction = _predict(score_a, score_b)
            correct += int(prediction == truth)
            total += 1

            if step < 6:
                false_revision += int(prediction == -1)
                stable_a_steps += 1

            if (
                step >= episode.return_index
                and first_correct_return is None
                and prediction == 1
            ):
                first_correct_return = step - episode.return_index

        return_latencies.append(6 if first_correct_return is None else first_correct_return)

    return {
        "accuracy": correct / total,
        "false_revision_rate": false_revision / stable_a_steps,
        "return_latency": sum(return_latencies) / len(return_latencies),
    }


def mean_metrics(
    *,
    seeds: Iterable[int],
    decay: float,
    mechanism: str,
) -> dict[str, float]:
    metrics = [evaluate(seed=seed, decay=decay, mechanism=mechanism) for seed in seeds]
    return {
        key: sum(row[key] for row in metrics) / len(metrics)
        for key in metrics[0]
    }


def utility(
    metrics: dict[str, float],
    *,
    false_revision_weight: float,
    latency_weight: float,
) -> float:
    return (
        metrics["accuracy"]
        - false_revision_weight * metrics["false_revision_rate"]
        - latency_weight * metrics["return_latency"]
    )


def select_decay(
    *,
    mechanism: str,
    false_revision_weight: float,
    latency_weight: float,
) -> tuple[float, dict[str, float]]:
    """Select only on fixed DEV seeds; TEST seeds are never used for selection."""
    candidates: list[tuple[float, float, dict[str, float]]] = []
    for decay in DECAY_GRID:
        metrics = mean_metrics(
            seeds=DEV_SEEDS,
            decay=decay,
            mechanism=mechanism,
        )
        score = utility(
            metrics,
            false_revision_weight=false_revision_weight,
            latency_weight=latency_weight,
        )
        candidates.append((score, -decay, metrics))

    best_score, negative_decay, best_metrics = max(candidates)
    selected_decay = -negative_decay
    return selected_decay, {
        **best_metrics,
        "utility": best_score,
    }


def run_probe() -> dict[str, object]:
    rows: list[dict[str, object]] = []

    for false_revision_weight, latency_weight in UTILITY_WEIGHTS:
        row: dict[str, object] = {
            "false_revision_weight": false_revision_weight,
            "latency_weight": latency_weight,
        }

        for mechanism in ("residual_loser", "symmetric_recurrent"):
            selected_decay, dev_metrics = select_decay(
                mechanism=mechanism,
                false_revision_weight=false_revision_weight,
                latency_weight=latency_weight,
            )
            test_metrics = mean_metrics(
                seeds=TEST_SEEDS,
                decay=selected_decay,
                mechanism=mechanism,
            )
            row[mechanism] = {
                "selected_decay": selected_decay,
                "dev": dev_metrics,
                "test": {
                    **test_metrics,
                    "utility": utility(
                        test_metrics,
                        false_revision_weight=false_revision_weight,
                        latency_weight=latency_weight,
                    ),
                },
            }

        residual = row["residual_loser"]
        recurrent = row["symmetric_recurrent"]
        assert isinstance(residual, dict)
        assert isinstance(recurrent, dict)
        residual_test = residual["test"]
        recurrent_test = recurrent["test"]
        assert isinstance(residual_test, dict)
        assert isinstance(recurrent_test, dict)
        row["symmetric_minus_residual_test_utility"] = (
            recurrent_test["utility"] - residual_test["utility"]
        )
        rows.append(row)

    return {
        "evidentiary_status": "NON_EVIDENTIARY",
        "exploratory_target": (
            "H2 residual-loser retention versus resource-matched generic "
            "symmetric recurrent memory on returning-state episodes"
        ),
        "synthetic_contract": {
            "episodes_per_seed": 512,
            "initial_a_steps": 6,
            "b_dwell_steps": list(DWELL_STEPS),
            "return_a_steps": 6,
            "evidence_mean_magnitude": 1.0,
            "evidence_noise_sigma": 1.2,
            "state_budget": (
                "Both mechanisms use two scalar hypothesis states and one "
                "prospectively selected decay parameter."
            ),
            "residual_loser_semantics": (
                "Only the prior losing hypothesis carries decayed state; "
                "the prior winner is replaced by current evidence."
            ),
            "symmetric_recurrent_semantics": (
                "Both hypothesis states carry the same generic recurrent decay."
            ),
            "decay_grid": list(DECAY_GRID),
            "dev_seeds": list(DEV_SEEDS),
            "test_seeds": list(TEST_SEEDS),
            "utility_weights": [
                {
                    "false_revision_weight": false_weight,
                    "latency_weight": latency_weight,
                }
                for false_weight, latency_weight in UTILITY_WEIGHTS
            ],
            "selection_rule": (
                "Select each mechanism's decay independently on DEV utility only; "
                "evaluate the fixed selected decay on disjoint TEST seeds."
            ),
        },
        "rows": rows,
        "interpretation_boundary": (
            "This is a synthetic reduction diagnostic only. It does not rerun or "
            "reinterpret C15 and cannot support or reject H2 formally."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(run_probe(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

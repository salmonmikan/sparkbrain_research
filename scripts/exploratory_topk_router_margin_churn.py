"""EXPLORATORY / NON_EVIDENTIARY top-k routing-margin churn probe.

This script studies a synthetic linear router with the same hard top-k selection shape used
by SparkBrain's SparseRoutingModel. It does not load repository datasets, checkpoints,
formal identities, preserved TEST material, or official scorers.

Purpose: characterize whether small input perturbations can create discrete selected-set
changes and whether those changes reduce to ordinary linear top-k boundary geometry.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

import numpy as np

SEED = 20260919
EVENT_DIM = 24
ACTIVE_K = 4
STATE_DIM = 24
MODULE_COUNTS = (8, 12, 24, 48)
EPSILONS = (0.005, 0.01, 0.05, 0.10)
SAMPLES_PER_CELL = 6000


@dataclass(frozen=True)
class CellResult:
    module_count: int
    active_k: int
    event_dim: int
    epsilon: float
    samples: int
    turnover_rate: float
    exact_boundary_predictor_accuracy: float
    median_boundary_margin: float
    p10_first_crossing_radius: float
    median_first_crossing_radius: float
    mean_hard_amplification: float
    p95_hard_amplification: float
    mean_turnover_jump: float
    mean_soft_amplification: float
    p95_soft_amplification: float


def topk_indices(logits: np.ndarray, k: int) -> np.ndarray:
    return np.argpartition(logits, -k)[-k:]


def first_crossing_radius(
    logits: np.ndarray,
    directional_derivative: np.ndarray,
    selected: np.ndarray,
) -> float:
    """Exact first radius along +u where any unselected logit overtakes a selected one."""
    selected_set = set(int(index) for index in selected)
    radius = math.inf
    for inside in selected:
        inside_i = int(inside)
        for outside_i in range(logits.shape[0]):
            if outside_i in selected_set:
                continue
            closing_speed = (
                directional_derivative[outside_i] - directional_derivative[inside_i]
            )
            if closing_speed <= 0:
                continue
            gap = logits[inside_i] - logits[outside_i]
            candidate = gap / closing_speed
            if 0 <= candidate < radius:
                radius = float(candidate)
    return radius


def run_cell(
    module_count: int,
    epsilon: float,
    *,
    active_k: int = ACTIVE_K,
    event_dim: int = EVENT_DIM,
    state_dim: int = STATE_DIM,
    samples: int = SAMPLES_PER_CELL,
) -> CellResult:
    rng = np.random.default_rng(
        SEED + module_count * 1000 + int(round(epsilon * 1_000_000))
    )
    router = rng.normal(size=(module_count, event_dim)) / math.sqrt(event_dim)
    module_states = rng.normal(size=(module_count, state_dim))

    turnovers = 0
    predictor_correct = 0
    margins: list[float] = []
    crossing_radii: list[float] = []
    hard_amplifications: list[float] = []
    turnover_jumps: list[float] = []
    soft_amplifications: list[float] = []

    for _ in range(samples):
        x = rng.normal(size=event_dim)
        direction = rng.normal(size=event_dim)
        direction /= np.linalg.norm(direction)

        logits = router @ x
        directional_derivative = router @ direction
        selected = topk_indices(logits, active_k)

        ordered = np.sort(logits)
        margins.append(float(ordered[-active_k] - ordered[-active_k - 1]))

        crossing_radius = first_crossing_radius(
            logits,
            directional_derivative,
            selected,
        )
        crossing_radii.append(crossing_radius)

        perturbed_logits = logits + epsilon * directional_derivative
        perturbed_selected = topk_indices(perturbed_logits, active_k)

        selected_set = set(int(index) for index in selected)
        perturbed_set = set(int(index) for index in perturbed_selected)
        actual_turnover = selected_set != perturbed_set
        predicted_turnover = epsilon >= crossing_radius - 1e-12

        turnovers += int(actual_turnover)
        predictor_correct += int(actual_turnover == predicted_turnover)

        hard_before = module_states[selected].mean(axis=0)
        hard_after = module_states[perturbed_selected].mean(axis=0)
        hard_jump = float(np.linalg.norm(hard_after - hard_before))
        hard_amplifications.append(hard_jump / epsilon)
        if actual_turnover:
            turnover_jumps.append(hard_jump)

        soft_weights = np.exp(logits - logits.max())
        soft_weights /= soft_weights.sum()
        soft_perturbed = np.exp(perturbed_logits - perturbed_logits.max())
        soft_perturbed /= soft_perturbed.sum()
        soft_before = soft_weights @ module_states
        soft_after = soft_perturbed @ module_states
        soft_amplifications.append(
            float(np.linalg.norm(soft_after - soft_before) / epsilon)
        )

    return CellResult(
        module_count=module_count,
        active_k=active_k,
        event_dim=event_dim,
        epsilon=epsilon,
        samples=samples,
        turnover_rate=turnovers / samples,
        exact_boundary_predictor_accuracy=predictor_correct / samples,
        median_boundary_margin=float(np.median(margins)),
        p10_first_crossing_radius=float(np.quantile(crossing_radii, 0.10)),
        median_first_crossing_radius=float(np.quantile(crossing_radii, 0.50)),
        mean_hard_amplification=float(np.mean(hard_amplifications)),
        p95_hard_amplification=float(np.quantile(hard_amplifications, 0.95)),
        mean_turnover_jump=(
            float(np.mean(turnover_jumps)) if turnover_jumps else 0.0
        ),
        mean_soft_amplification=float(np.mean(soft_amplifications)),
        p95_soft_amplification=float(np.quantile(soft_amplifications, 0.95)),
    )


def build_report() -> dict[str, object]:
    cells = [
        asdict(run_cell(module_count, epsilon))
        for module_count in MODULE_COUNTS
        for epsilon in EPSILONS
    ]
    return {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "candidate": "TOPK_ROUTER_MARGIN_CHURN_STABILITY_DISCOVERY",
        "exploration_cycle": 1,
        "seed": SEED,
        "design": {
            "event_dim": EVENT_DIM,
            "active_k": ACTIVE_K,
            "module_counts": list(MODULE_COUNTS),
            "epsilons": list(EPSILONS),
            "samples_per_cell": SAMPLES_PER_CELL,
            "total_samples": len(cells) * SAMPLES_PER_CELL,
        },
        "cells": cells,
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

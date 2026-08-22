from __future__ import annotations

import math
import random
from statistics import mean


def paired_bootstrap(
    values: list[float], *, seed: int = 1729, samples: int = 400
) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    estimates = sorted(mean(rng.choice(values) for _ in values) for _ in range(samples))
    return estimates[int(0.025 * samples)], estimates[min(samples - 1, int(0.975 * samples))]


def paired_sign_flip(values: list[float], *, seed: int = 1733, samples: int = 2000) -> float:
    if not values:
        return 1.0
    observed = abs(mean(values))
    rng = random.Random(seed)
    extreme = 1
    for _ in range(samples):
        permuted = abs(mean(value if rng.random() < 0.5 else -value for value in values))
        extreme += int(permuted >= observed)
    return extreme / (samples + 1)


def holm_adjust(p_values: dict[str, float]) -> dict[str, float]:
    ordered = sorted(p_values.items(), key=lambda item: item[1])
    adjusted: dict[str, float] = {}
    running = 0.0
    total = len(ordered)
    for index, (name, value) in enumerate(ordered):
        running = max(running, min(1.0, value * (total - index)))
        adjusted[name] = running
    return adjusted


def standardized_effect(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    average = mean(values)
    variance = sum((value - average) ** 2 for value in values) / (len(values) - 1)
    return average / math.sqrt(variance) if variance > 0 else 0.0

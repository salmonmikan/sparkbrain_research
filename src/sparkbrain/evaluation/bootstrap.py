from __future__ import annotations

import random
from statistics import mean


def percentile_interval(
    values: list[float], *, seed: int = 1729, samples: int = 1000
) -> tuple[float, float] | None:
    if not values:
        return None
    rng = random.Random(seed)
    estimates = sorted(mean(rng.choices(values, k=len(values))) for _ in range(samples))
    return estimates[int(0.025 * (samples - 1))], estimates[int(0.975 * (samples - 1))]

from __future__ import annotations

import statistics
import time
from collections.abc import Callable
from typing import Any

from ..baselines.neural import trainable_parameter_count


def profile_calls(
    call: Callable[[], Any], *, warmups: int = 2, repeats: int = 7
) -> dict[str, float]:
    for _ in range(warmups):
        call()
    timings = []
    for _ in range(repeats):
        started = time.perf_counter_ns()
        call()
        timings.append((time.perf_counter_ns() - started) / 1_000_000)
    ordered = sorted(timings)
    p95_index = min(len(ordered) - 1, int(0.95 * len(ordered)))
    return {"cpu_ms_p50": statistics.median(ordered), "cpu_ms_p95": ordered[p95_index]}


def model_profile(module: Any, analytical_work: int) -> dict[str, int]:
    return {
        "trainable_parameters": trainable_parameter_count(module),
        "analytical_training_operations": analytical_work,
        "state_bytes": sum(
            parameter.numel() * parameter.element_size() for parameter in module.parameters()
        ),
    }

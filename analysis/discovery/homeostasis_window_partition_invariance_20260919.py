"""EXPLORATORY / NON_EVIDENTIARY homeostasis window-partition probe.

Uses only stable v0.5 HomeostaticController semantics and a synthetic fixed spike
train. No repository datasets, checkpoints, formal raw material, held-out TEST
inputs, consumed identities, or official scorers are accessed.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

from sparkbrain.v05.homeostasis import HomeostaticController

SOURCE_SEMANTICS = "main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
WINDOWS_MS = (10.0, 20.0, 25.0, 50.0, 100.0, 200.0)
DURATION_MS = 1000.0
UNIT_IDS = (0, 1, 2, 3)
RESULT_PATH = Path(
    "analysis/discovery/homeostasis_window_partition_invariance_20260919.json"
)


@dataclass(slots=True)
class _Unit:
    base_threshold: float = 1.0


def synthetic_spikes() -> tuple[tuple[float, int], ...]:
    """Return the same physical 40-spike train for every partition."""
    times = range(25, 1001, 25)
    return tuple(
        (float(time_ms), UNIT_IDS[index % len(UNIT_IDS)])
        for index, time_ms in enumerate(times)
    )


def run_partition(window_ms: float) -> dict[str, object]:
    controller = HomeostaticController()
    field = SimpleNamespace(units={unit_id: _Unit() for unit_id in UNIT_IDS})
    rows = synthetic_spikes()
    windows = int(math.ceil(DURATION_MS / window_ms))
    empty_windows = 0

    for index in range(windows):
        lower = index * window_ms
        upper = min((index + 1) * window_ms, DURATION_MS)
        window_rows = [
            SimpleNamespace(unit_id=unit_id)
            for time_ms, unit_id in rows
            if lower < time_ms <= upper
        ]
        if not window_rows:
            empty_windows += 1
        controller.observe(
            cast(Any, field),
            cast(Any, window_rows),
            time_ms=upper,
        )

    thresholds = [field.units[unit_id].base_threshold for unit_id in UNIT_IDS]
    rates = [controller.rate_ema[unit_id] for unit_id in UNIT_IDS]
    return {
        "window_ms": window_ms,
        "windows": windows,
        "empty_windows": empty_windows,
        "final_mean_threshold": sum(thresholds) / len(thresholds),
        "min_unit_threshold": min(thresholds),
        "max_unit_threshold": max(thresholds),
        "mean_final_rate_ema": sum(rates) / len(rates),
    }


def main() -> None:
    rows = [run_partition(window_ms) for window_ms in WINDOWS_MS]
    thresholds = [float(row["final_mean_threshold"]) for row in rows]
    result = {
        "label": "EXPLORATORY / NON_EVIDENTIARY",
        "source_semantics": SOURCE_SEMANTICS,
        "question": (
            "Does v0.5 homeostatic adaptation preserve the final threshold under "
            "different observation-window partitions of the same physical spike train?"
        ),
        "protocol": {
            "duration_ms": DURATION_MS,
            "units": len(UNIT_IDS),
            "spikes": len(synthetic_spikes()),
            "spike_interval_ms": 25.0,
            "spikes_per_unit": 10,
            "initial_threshold": 1.0,
            "window_widths_ms": list(WINDOWS_MS),
            "controller_config": {
                "target_spikes_per_window": 0.35,
                "learning_rate": 0.004,
                "rate_decay": 0.88,
            },
        },
        "rows": rows,
        "summary": {
            "threshold_span": max(thresholds) - min(thresholds),
            "smallest_window_final_mean_threshold": thresholds[0],
            "largest_window_final_mean_threshold": thresholds[-1],
            "interpretation": (
                "The same elapsed-time spike train produces different homeostatic "
                "thresholds because target_spikes_per_window and rate_decay are applied "
                "once per observe() call, not normalized by physical window duration. "
                "The effect is therefore reduced to explicit per-window controller "
                "semantics rather than a distinct scientific phenomenon."
            ),
        },
        "evidentiary_status": "NON_EVIDENTIARY",
        "recommendation": "REJECT",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

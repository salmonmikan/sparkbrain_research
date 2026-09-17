"""EXPLORATORY / NON_EVIDENTIARY synthetic H9 boundary probe.

This does not execute historical C07, access formal inputs, or define a successor.
It asks whether a spike-valued interface can appear to preserve delayed behavior
when memory is actually carried by hidden continuous decoder/filter state.
"""

from __future__ import annotations

import json
from statistics import mean

LABELS = ("A", "B")
GAPS = tuple(range(1, 21))
DECAYS = (0.5, 0.8, 0.9, 0.95, 0.99)
EPSILON = 0.05


def stateless_current_spike_only(label: str, gap: int) -> tuple[str | None, int]:
    del label, gap
    return None, 0


def analog_leaky_hidden_state(
    label: str, gap: int, decay: float
) -> tuple[str | None, float]:
    a = 1.0 if label == "A" else 0.0
    b = 1.0 if label == "B" else 0.0
    for _ in range(gap):
        a *= decay
        b *= decay
    magnitude = max(a, b)
    if magnitude < EPSILON:
        return None, magnitude
    return ("A" if a > b else "B"), magnitude


def toy_recurrent_spike_latch(label: str, gap: int) -> tuple[str, int]:
    recurrent_spikes = 0
    current = label
    for _ in range(gap):
        recurrent_spikes += 1
        current = label
    return current, recurrent_spikes


def run() -> dict:
    total = len(LABELS) * len(GAPS)
    stateless_correct = sum(
        stateless_current_spike_only(label, gap)[0] == label
        for label in LABELS
        for gap in GAPS
    )

    analog = []
    for decay in DECAYS:
        correct = 0
        max_full_gap = 0
        for gap in GAPS:
            gap_correct = 0
            for label in LABELS:
                predicted, _ = analog_leaky_hidden_state(label, gap, decay)
                gap_correct += predicted == label
            correct += gap_correct
            if gap_correct == len(LABELS):
                max_full_gap = gap
        analog.append(
            {
                "decay": decay,
                "accuracy": correct / total,
                "max_gap_with_full_accuracy": max_full_gap,
                "non_sensory_recurrent_spikes": 0,
            }
        )

    spike_correct = 0
    spike_costs = []
    for label in LABELS:
        for gap in GAPS:
            predicted, spike_cost = toy_recurrent_spike_latch(label, gap)
            spike_correct += predicted == label
            spike_costs.append(spike_cost)

    return {
        "schema": "exploratory-h9-decoder-state-boundary-v1",
        "evidentiary_status": "NON_EVIDENTIARY",
        "synthetic_task": {
            "labels": list(LABELS),
            "silent_gap_range": [min(GAPS), max(GAPS)],
            "trials": total,
            "query": "recall cue after silent gap",
            "abstention_counts_incorrect": True,
        },
        "fixed_probe_choices": {
            "analog_detection_epsilon": EPSILON,
            "analog_decay_grid": list(DECAYS),
            "note": "Sensitivity grid only; no selection against formal outcomes.",
        },
        "stateless_current_spike_only": {
            "accuracy": stateless_correct / total,
            "correct": stateless_correct,
            "total": total,
        },
        "analog_leaky_hidden_state": analog,
        "toy_recurrent_spike_latch": {
            "accuracy": spike_correct / total,
            "correct": spike_correct,
            "total": total,
            "mean_recurrent_spikes_per_trial": mean(spike_costs),
            "max_recurrent_spikes_per_trial": max(spike_costs),
        },
        "interpretation": [
            (
                "No current query spike plus no retained state cannot solve this "
                "delayed recall toy."
            ),
            (
                "Hidden continuous leaky state can solve a decay-dependent horizon "
                "with zero non-sensory recurrent spikes."
            ),
            (
                "A toy recurrent spike latch solves all tested gaps but uses recurrent "
                "spike activity proportional to the gap."
            ),
            (
                "A future H9 fully-spiking boundary must explicitly account for state "
                "carried by decoders/filters; spike-valued I/O alone is insufficient."
            ),
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

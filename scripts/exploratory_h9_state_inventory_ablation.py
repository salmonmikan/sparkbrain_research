"""EXPLORATORY / NON_EVIDENTIARY H9 state-inventory ablation probe.

This synthetic diagnostic does not execute historical C07, access formal inputs,
create a formal identity, or touch the C19 frontier. It tests whether a fixed
inventory of persistent state plus reset interventions can attribute delayed
performance to spike-mediated versus hidden non-spike state.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

LABELS = ("A", "B")
GAPS = tuple(range(1, 21))
FILTER_DECAY = 0.95

STATE_SLOTS = (
    "spike_state",
    "decoder_state",
    "filter_state",
    "algorithmic_state",
)

RESET_CONDITIONS = (
    "none",
    "spike_state",
    "decoder_state",
    "filter_state",
    "algorithmic_state",
    "all_non_spike",
    "all_state",
)


@dataclass
class StateInventory:
    spike_state: str | None = None
    decoder_state: float = 0.0
    filter_state: float = 0.0
    algorithmic_state: str | None = None


def encode(label: str) -> float:
    return 1.0 if label == "A" else -1.0


def decode_scalar(value: float) -> str | None:
    if value > 0.0:
        return "A"
    if value < 0.0:
        return "B"
    return None


def apply_reset(state: StateInventory, condition: str) -> None:
    if condition in {"spike_state", "all_state"}:
        state.spike_state = None
    if condition in {"decoder_state", "all_non_spike", "all_state"}:
        state.decoder_state = 0.0
    if condition in {"filter_state", "all_non_spike", "all_state"}:
        state.filter_state = 0.0
    if condition in {"algorithmic_state", "all_non_spike", "all_state"}:
        state.algorithmic_state = None


def prepare_state(mechanism: str, label: str, gap: int) -> StateInventory:
    state = StateInventory()

    if mechanism in {"spike_latch", "hybrid_spike_plus_decoder"}:
        state.spike_state = label
    if mechanism in {"decoder_memory", "hybrid_spike_plus_decoder"}:
        state.decoder_state = encode(label)
    if mechanism == "filter_trace":
        state.filter_state = encode(label) * (FILTER_DECAY**gap)
    if mechanism == "algorithmic_memory":
        state.algorithmic_state = label

    return state


def predict(mechanism: str, state: StateInventory) -> str | None:
    if mechanism == "stateless":
        return None
    if mechanism == "spike_latch":
        return state.spike_state
    if mechanism == "decoder_memory":
        return decode_scalar(state.decoder_state)
    if mechanism == "filter_trace":
        return decode_scalar(state.filter_state)
    if mechanism == "algorithmic_memory":
        return state.algorithmic_state
    if mechanism == "hybrid_spike_plus_decoder":
        if state.decoder_state != 0.0:
            return decode_scalar(state.decoder_state)
        return state.spike_state
    raise ValueError(f"unknown mechanism: {mechanism}")


def run_mechanism(mechanism: str, reset_condition: str) -> dict[str, int | float]:
    total = len(LABELS) * len(GAPS)
    correct = 0
    for label in LABELS:
        for gap in GAPS:
            state = prepare_state(mechanism, label, gap)
            apply_reset(state, reset_condition)
            correct += predict(mechanism, state) == label

    return {
        "correct": correct,
        "total": total,
        "accuracy": correct / total,
    }


def run() -> dict:
    mechanisms = (
        "stateless",
        "spike_latch",
        "decoder_memory",
        "filter_trace",
        "algorithmic_memory",
        "hybrid_spike_plus_decoder",
    )
    matrix = {
        mechanism: {
            reset_condition: run_mechanism(mechanism, reset_condition)
            for reset_condition in RESET_CONDITIONS
        }
        for mechanism in mechanisms
    }

    attribution_checks = {
        "spike_latch_killed_by_spike_reset": (
            matrix["spike_latch"]["spike_state"]["correct"] == 0
        ),
        "non_spike_memories_killed_by_all_non_spike_reset": all(
            matrix[mechanism]["all_non_spike"]["correct"] == 0
            for mechanism in (
                "decoder_memory",
                "filter_trace",
                "algorithmic_memory",
            )
        ),
        "spike_latch_survives_all_non_spike_reset": (
            matrix["spike_latch"]["all_non_spike"]["correct"]
            == matrix["spike_latch"]["none"]["correct"]
        ),
        "hybrid_survives_single_channel_reset": all(
            matrix["hybrid_spike_plus_decoder"][condition]["correct"]
            == matrix["hybrid_spike_plus_decoder"]["none"]["correct"]
            for condition in ("spike_state", "decoder_state")
        ),
        "hybrid_killed_by_all_state_reset": (
            matrix["hybrid_spike_plus_decoder"]["all_state"]["correct"] == 0
        ),
        "stateless_never_solves_delayed_recall": all(
            result["correct"] == 0
            for result in matrix["stateless"].values()
        ),
    }

    return {
        "schema": "exploratory-h9-state-inventory-ablation-v1",
        "evidentiary_status": "NON_EVIDENTIARY",
        "synthetic_task": {
            "labels": list(LABELS),
            "silent_gap_range": [min(GAPS), max(GAPS)],
            "trials_per_mechanism_condition": len(LABELS) * len(GAPS),
            "query": "recall cue after silent gap",
        },
        "predeclared_state_inventory": {
            "spike_state": "discrete recurrent spike-mediated latch",
            "decoder_state": "non-spiking continuous decoder-held memory",
            "filter_state": "non-spiking leaky trace",
            "algorithmic_state": "non-spiking discrete controller memory",
        },
        "fixed_choices": {
            "filter_decay": FILTER_DECAY,
            "filter_decode": "sign(trace), no fitted threshold",
            "reset_timing": "immediately before query",
            "reset_conditions": list(RESET_CONDITIONS),
            "note": (
                "Synthetic attribution diagnostic only; no parameter selection "
                "against formal or held-out outcomes."
            ),
        },
        "mechanism_reset_matrix": matrix,
        "attribution_checks": attribution_checks,
        "interpretation": [
            (
                "Each single-state memory succeeds only while its declared backing "
                "state remains available."
            ),
            (
                "Resetting every non-spike state removes delayed performance from "
                "decoder/filter/algorithmic mechanisms while leaving spike-latch "
                "performance intact."
            ),
            (
                "The hybrid retains perfect performance after either single-channel "
                "reset, showing that hidden decoder state can mask ablation of a "
                "spike-mediated memory channel unless the state inventory is explicit."
            ),
            (
                "This supports a prospective state-accounting/reset gate as a "
                "methodological safeguard; it is not evidence for H9."
            ),
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

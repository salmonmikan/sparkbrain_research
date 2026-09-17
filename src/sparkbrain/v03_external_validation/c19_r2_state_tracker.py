"""Target-blind C19-R2 explicit finite-state/state-tracker reduction.

The mechanism uses the immutable C19-v4 I2 encoder and deterministic projection,
then replaces SparkBrain-specific coalition dynamics with one explicit seven-state
hysteresis tracker that resets for every pair. It cannot locate official data,
materialize evaluator targets, or authorize a formal run.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Any

from sparkbrain.v03_external_validation import implementation_binding as v4_binding
from sparkbrain.v03_external_validation.c19_r2_protocol import (
    CHOICES,
    INPUT_TRACK,
    MAJORITY_THRESHOLD,
    MECHANISM_ID,
    OFFICIAL_SEEDS,
    PROJECTION_SALT,
    ROW_KIND,
    STATE_ALPHABET,
)

RESET_STATE = "RESET"
_ALLOWED_EXAMPLE_KEYS = {
    "record_id",
    "source_index",
    "pair_index",
    "step_index",
    "question",
    "choices",
}


def _validate_visible_example(example: Mapping[str, object]) -> None:
    if set(example) != _ALLOWED_EXAMPLE_KEYS:
        raise ValueError("R2 accepts only the frozen target-blind visible envelope")


def _pairs(
    examples: Sequence[Mapping[str, object]],
) -> tuple[tuple[int, tuple[Mapping[str, object], Mapping[str, object]]], ...]:
    grouped: dict[int, list[Mapping[str, object]]] = {}
    for example in examples:
        _validate_visible_example(example)
        pair_index = example["pair_index"]
        if isinstance(pair_index, bool) or not isinstance(pair_index, int) or pair_index < 0:
            raise ValueError("R2 pair_index must be a non-negative integer")
        grouped.setdefault(pair_index, []).append(example)
    result = []
    for pair_index, pair in sorted(grouped.items()):
        ordered = tuple(sorted(pair, key=lambda item: int(item["step_index"])))
        if len(ordered) != 2 or tuple(int(item["step_index"]) for item in ordered) != (0, 1):
            raise ValueError("R2 requires exactly visible steps 0 and 1 for every pair")
        if tuple(int(item["source_index"]) for item in ordered) != (0, 1):
            raise ValueError("R2 requires exact C19 source indices 0 and 1")
        result.append((pair_index, (ordered[0], ordered[1])))
    return tuple(result)


def _top(probabilities: Mapping[str, float]) -> str:
    if set(probabilities) != set(CHOICES):
        raise ValueError("R2 observation requires exactly choices a/b/c")
    return min(CHOICES, key=lambda choice: (-float(probabilities[choice]), choice))


def observe(probabilities: Mapping[str, float]) -> tuple[str, bool]:
    """Map one projected probability vector to a finite target-free observation."""

    leader = _top(probabilities)
    strong = float(probabilities[leader]) >= MAJORITY_THRESHOLD
    return leader, strong


def _state(choice: str, strong: bool) -> str:
    value = f"{choice.upper()}_{'STRONG' if strong else 'WEAK'}"
    if value not in STATE_ALPHABET:
        raise ValueError("R2 generated state outside frozen alphabet")
    return value


def _decode_state(state: str) -> tuple[str, bool]:
    if state not in STATE_ALPHABET or state == RESET_STATE:
        raise ValueError("R2 active state must be one of six choice/strength states")
    choice_token, strength_token = state.split("_", maxsplit=1)
    return choice_token.lower(), strength_token == "STRONG"


def transition(state: str, probabilities: Mapping[str, float]) -> str:
    """Apply the prospectively fixed seven-state transition table."""

    current_choice, current_strong = observe(probabilities)
    if state == RESET_STATE:
        return _state(current_choice, current_strong)

    prior_choice, prior_strong = _decode_state(state)
    if prior_choice == current_choice:
        return _state(current_choice, prior_strong or current_strong)
    if current_strong:
        return _state(current_choice, True)
    if prior_strong:
        return _state(prior_choice, False)
    return _state(current_choice, False)


def readout(state: str) -> str:
    choice, _strong = _decode_state(state)
    return choice


def state_tracker_executor(
    row: Mapping[str, object],
    examples: Sequence[Mapping[str, object]],
) -> list[dict[str, Any]]:
    """Execute the fixed R2 tracker over an injected target-blind visible envelope."""

    if row.get("row_kind") != ROW_KIND:
        raise ValueError("R2 executor received a non-R2 row")
    if row.get("mechanism_id") != MECHANISM_ID:
        raise ValueError("R2 mechanism id drift")
    if row.get("input_track") != INPUT_TRACK:
        raise ValueError("R2 must use exact I2")
    seed = int(row["seed"])
    if seed not in OFFICIAL_SEEDS:
        raise ValueError("R2 seed outside the frozen inventory")

    output: list[dict[str, Any]] = []
    for pair_index, pair in _pairs(examples):
        state = RESET_STATE
        state_trace = [state]
        observation_trace: list[dict[str, object]] = []
        representation_hashes = []
        projection_operations = 0
        final_probabilities: dict[str, float] | None = None
        final_visible = None

        for raw in pair:
            visible = v4_binding._validate_example(raw)
            representation = v4_binding.encode_visible(visible, INPUT_TRACK)
            probabilities, operations = v4_binding._project(
                representation,
                seed=seed,
                salt=PROJECTION_SALT,
            )
            projection_operations += operations
            leader, strong = observe(probabilities)
            state = transition(state, probabilities)
            state_trace.append(state)
            observation_trace.append(
                {
                    "leader": leader,
                    "strength": "strong" if strong else "weak",
                }
            )
            representation_hashes.append(
                hashlib.sha256(v4_binding.representation_bytes(representation)).hexdigest()
            )
            final_probabilities = dict(probabilities)
            final_visible = visible

        if final_visible is None or final_probabilities is None:
            raise RuntimeError("R2 pair execution produced no final visible record")
        output.append(
            {
                "record_id": final_visible.record_id,
                "source_index": final_visible.source_index,
                "pair_index": pair_index,
                "prediction": readout(state),
                "metadata": {
                    "mechanism_id": MECHANISM_ID,
                    "input_track": INPUT_TRACK,
                    "seed": seed,
                    "representation_sha256": representation_hashes,
                    "state_trace": state_trace,
                    "observation_trace": observation_trace,
                    "final_state": state,
                    "final_probabilities": final_probabilities,
                    "work_counters": {
                        "encodings": 2,
                        "projection_passes": 2,
                        "projection_operations": projection_operations,
                        "state_transitions": 2,
                    },
                    "final_step_index": int(pair[-1]["step_index"]),
                },
            }
        )
    return output


__all__ = [
    "RESET_STATE",
    "observe",
    "readout",
    "state_tracker_executor",
    "transition",
]

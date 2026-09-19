from __future__ import annotations

import json
import math
from pathlib import Path

SOURCE_MAIN_SHA = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
TARGET = "PLASTICITY_REWARD_OMISSION_BASELINE_DISCOVERY"
LAGS_MS = (2.0, 5.0, 10.0, 20.0)
CONDITIONS = (
    "omission",
    "neutral_each_step",
    "negative_once",
    "negative_each_step",
    "positive_once",
)
STEPS = 40
LEARNING_RATE = 0.001
TAU_PLUS_MS = 18.0
ELIGIBILITY_DECAY = 0.90
REWARD_TRACE_DEFAULT = 1.0
REWARD_RELAXATION = 0.85
MIN_WEIGHT = -1.4
MAX_WEIGHT = 1.4


def simulate(lag_ms: float, condition: str) -> list[dict[str, float | int]]:
    """Mirror the single-edge causal branch of main V05PlasticityController.apply.

    This is an EXPLORATORY / NON_EVIDENTIARY synthetic reduction probe. It does
    not import datasets, checkpoints, preserved raw material, TEST inputs or any
    formal scorer. The only spike statistic is one repeated causal pre/post pair.
    """
    delta = math.exp(-lag_ms / TAU_PLUS_MS)
    eligibility = 0.0
    reward_trace = REWARD_TRACE_DEFAULT
    weight = 0.0
    rows: list[dict[str, float | int]] = []

    for step in range(1, STEPS + 1):
        if condition == "neutral_each_step":
            reward_trace = 0.0
        elif condition == "negative_each_step":
            reward_trace = -1.0
        elif condition == "negative_once" and step == 1:
            reward_trace = -1.0
        elif condition == "positive_once" and step == 1:
            reward_trace = 2.0

        eligibility *= ELIGIBILITY_DECAY
        if abs(eligibility) < 1e-8:
            eligibility = 0.0
        eligibility += delta

        delta_weight = LEARNING_RATE * reward_trace * eligibility
        weight = max(MIN_WEIGHT, min(MAX_WEIGHT, weight + delta_weight))
        rows.append(
            {
                "step": step,
                "reward_trace_used": reward_trace,
                "eligibility": eligibility,
                "delta_weight": delta_weight,
                "weight": weight,
            }
        )

        # Exact main semantics: relax toward +1.0 after every apply().
        reward_trace = 1.0 + (reward_trace - 1.0) * REWARD_RELAXATION

    return rows


def summarize(rows: list[dict[str, float | int]], condition: str) -> dict[str, float | int | None]:
    weights = [float(row["weight"]) for row in rows]
    out: dict[str, float | int | None] = {
        "weight_step_5": weights[4],
        "weight_step_10": weights[9],
        "weight_step_20": weights[19],
        "weight_step_40": weights[39],
        "minimum_weight": min(weights),
        "minimum_weight_step": weights.index(min(weights)) + 1,
    }
    if condition == "negative_once":
        out["first_positive_reward_trace_step_after_negative"] = next(
            (int(row["step"]) for row in rows if float(row["reward_trace_used"]) > 0.0),
            None,
        )
        out["first_nonnegative_weight_step_after_negative"] = next(
            (
                int(row["step"])
                for row in rows[1:]
                if float(row["weight"]) >= 0.0
            ),
            None,
        )
    return out


def main() -> None:
    result: dict[str, object] = {
        "status": "EXPLORATORY_NON_EVIDENTIARY",
        "target": TARGET,
        "source_main_sha": SOURCE_MAIN_SHA,
        "config": {
            "learning_rate": LEARNING_RATE,
            "tau_plus_ms": TAU_PLUS_MS,
            "eligibility_decay": ELIGIBILITY_DECAY,
            "reward_trace_default": REWARD_TRACE_DEFAULT,
            "reward_trace_relaxation_to_default": REWARD_RELAXATION,
            "steps": STEPS,
            "lags_ms": list(LAGS_MS),
            "conditions": list(CONDITIONS),
        },
        "summary": {},
        "observations": {
            "omission_is_not_neutral": (
                "With no reward() call, reward_trace remains exactly +1.0, so every "
                "causal eligibility event potentiates the edge."
            ),
            "explicit_neutral_is_neutral": (
                "Calling reward(0.0) before every step keeps weight exactly 0.0 in this "
                "single-edge harness."
            ),
            "one_shot_negative_recovers": (
                "For all tested lags, one reward(-1.0) event reaches minimum weight at "
                "step 5 and crosses back to nonnegative at step 9 when later updates omit "
                "reward()."
            ),
            "continuous_negative_required_for_sustained_depression": (
                "Calling reward(-1.0) before every step mirrors omission with opposite "
                "weight sign."
            ),
            "reduction": (
                "The effect is fully predicted by the explicit reward_trace baseline "
                "recurrence toward +1.0 combined with positive causal eligibility; no "
                "additional adaptive mechanism is required."
            ),
        },
    }

    summary = result["summary"]
    assert isinstance(summary, dict)
    for lag_ms in LAGS_MS:
        lag_summary: dict[str, object] = {}
        for condition in CONDITIONS:
            rows = simulate(lag_ms, condition)
            lag_summary[condition] = summarize(rows, condition)
        summary[f"{lag_ms:g}"] = lag_summary

    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

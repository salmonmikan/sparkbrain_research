"""Concrete fail-closed scorer for the prospectively fixed C19 official-v2 run."""

from __future__ import annotations

import math
import platform
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from statistics import mean
from typing import Any

from sparkbrain.v03_external_validation.official_execution_v2 import RawBundleV2
from sparkbrain.v03_external_validation.official_protocol_v2 import (
    BOOTSTRAP_DRAWS_PER_RESAMPLE,
    BOOTSTRAP_LOWER_P,
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    BOOTSTRAP_UPPER_P,
    EVALUATOR_TARGET_FIELDS,
    EXPECTED_MAINTAIN_PAIRS,
    EXPECTED_PAIRS,
    EXPECTED_UPDATE_PAIRS,
    OFFICIAL_PYTHON_IMPLEMENTATION,
    OFFICIAL_PYTHON_VERSION,
    OFFICIAL_SEEDS,
    PLANNED_IDENTITY,
    PRIMARY_CONDITION,
    PROTOCOL_ID,
    REFERENCE_CONDITION,
)

Target = dict[str, Any]
JoinKey = tuple[int, str, int, int]


def assert_official_python_runtime() -> None:
    if platform.python_implementation() != OFFICIAL_PYTHON_IMPLEMENTATION:
        raise RuntimeError("official C19-v2 scoring requires CPython")
    if platform.python_version() != OFFICIAL_PYTHON_VERSION:
        raise RuntimeError(
            f"official C19-v2 scoring requires Python {OFFICIAL_PYTHON_VERSION}"
        )


def _require_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _require_non_negative_int(value: object, name: str) -> int:
    integer = _require_int(value, name)
    if integer < 0:
        raise ValueError(f"{name} must be non-negative")
    return integer


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return value == value.lower() and all(ch in "0123456789abcdef" for ch in value)


def _join_key(row: Mapping[str, Any]) -> JoinKey:
    return (
        _require_non_negative_int(row["pair_index"], "pair_index"),
        str(row["record_id_hash"]),
        _require_non_negative_int(row["source_index"], "source_index"),
        _require_non_negative_int(row["step_index"], "step_index"),
    )


def validate_evaluator_targets(
    raw: RawBundleV2,
    evaluator_targets: Sequence[Mapping[str, Any]],
) -> tuple[Target, ...]:
    """Validate the exact post-preservation evaluator join and return pair order."""

    if len(evaluator_targets) != EXPECTED_PAIRS:
        raise ValueError("evaluator targets must contain exactly 1744 pairs")

    raw_keys_by_pair: dict[int, JoinKey] = {}
    for record in raw.records:
        if record["protocol_id"] != PROTOCOL_ID:
            raise ValueError("raw protocol is not C19 official-v2")
        if record["run_identity"] != PLANNED_IDENTITY:
            raise ValueError("raw identity is not C19 official-v2")
        pair_index = _require_non_negative_int(record["pair_index"], "pair_index")
        key = _join_key(record)
        prior = raw_keys_by_pair.setdefault(pair_index, key)
        if prior != key:
            raise ValueError("raw join identity differs across rows")

    if set(raw_keys_by_pair) != set(range(EXPECTED_PAIRS)):
        raise ValueError("raw pair inventory is not total for evaluator join")

    seen_keys: set[JoinKey] = set()
    seen_pairs: set[int] = set()
    by_pair: dict[int, Target] = {}
    update_count = 0

    for target_value in evaluator_targets:
        target = dict(target_value)
        if set(target) != EVALUATOR_TARGET_FIELDS:
            raise ValueError("evaluator target fields differ from the frozen v2 contract")
        pair_index = _require_non_negative_int(target["pair_index"], "pair_index")
        if pair_index >= EXPECTED_PAIRS:
            raise ValueError("evaluator pair_index is out of range")
        if not _is_sha256(target["record_id_hash"]):
            raise ValueError("evaluator record_id_hash must be lowercase SHA-256")
        _require_non_negative_int(target["source_index"], "source_index")
        _require_non_negative_int(target["step_index"], "step_index")
        if not isinstance(target["target_choice_id"], str) or not target[
            "target_choice_id"
        ]:
            raise ValueError("target_choice_id must be a non-empty string")
        if not isinstance(target["update_required"], bool):
            raise ValueError("update_required must be boolean")

        key = _join_key(target)
        if key in seen_keys or pair_index in seen_pairs:
            raise ValueError("duplicate evaluator target join key or pair_index")
        if raw_keys_by_pair.get(pair_index) != key:
            raise ValueError("evaluator target join is missing or does not match raw identity")

        seen_keys.add(key)
        seen_pairs.add(pair_index)
        by_pair[pair_index] = target
        update_count += int(target["update_required"])

    if seen_pairs != set(range(EXPECTED_PAIRS)):
        raise ValueError("evaluator target join is not total")
    if update_count != EXPECTED_UPDATE_PAIRS:
        raise ValueError("evaluator update slice count differs from frozen 1074")
    if EXPECTED_PAIRS - update_count != EXPECTED_MAINTAIN_PAIRS:
        raise ValueError("evaluator maintain slice count differs from frozen 670")

    return tuple(by_pair[index] for index in range(EXPECTED_PAIRS))


def linear_quantile_10k(effects: Sequence[float], p: float) -> float:
    """Frozen 10k-effect linear empirical quantile."""

    if len(effects) != BOOTSTRAP_RESAMPLES:
        raise ValueError("quantile requires exactly 10000 effects")
    if (
        not isinstance(p, (int, float))
        or isinstance(p, bool)
        or not 0.0 <= float(p) <= 1.0
    ):
        raise ValueError("quantile p must be in [0, 1]")
    values = [float(value) for value in effects]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("quantile effects must all be finite")
    values.sort()
    probability = float(p)
    rank = (len(values) - 1) * probability
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return values[lower]
    fraction = rank - lower
    return values[lower] + (values[upper] - values[lower]) * fraction


def _condition_id(record: Mapping[str, Any]) -> str | None:
    if record["row_kind"] != "c19_condition":
        return None
    return f"{record['input_track']}/{record['gate']}/{record['entity']}"


def _correct(record: Mapping[str, Any], target: Mapping[str, Any]) -> float:
    return float(record["prediction"] == target["target_choice_id"])


def _row_metrics(
    records: Sequence[Mapping[str, Any]], targets: Sequence[Target]
) -> dict[str, float]:
    by_pair = {int(record["pair_index"]): record for record in records}
    if set(by_pair) != set(range(EXPECTED_PAIRS)):
        raise ValueError("row scoring requires complete pair coverage")
    updates = [index for index, target in enumerate(targets) if target["update_required"]]
    maintains = [
        index for index, target in enumerate(targets) if not target["update_required"]
    ]
    bu = mean(_correct(by_pair[index], targets[index]) for index in updates)
    bm = mean(_correct(by_pair[index], targets[index]) for index in maintains)
    return {
        "BU_Acc": bu,
        "BM_Acc": bm,
        "BREU": (bu + bm) / 2.0,
        "all_pair_accuracy": mean(
            _correct(by_pair[index], targets[index]) for index in range(EXPECTED_PAIRS)
        ),
        "final_coverage": 1.0,
    }


def _primary_reference_delta_by_pair(
    raw: RawBundleV2, targets: Sequence[Target]
) -> tuple[float, ...]:
    condition_rows: dict[
        tuple[str, int], dict[int, Mapping[str, Any]]
    ] = defaultdict(dict)
    for record in raw.records:
        condition_id = _condition_id(record)
        if condition_id not in {PRIMARY_CONDITION, REFERENCE_CONDITION}:
            continue
        seed = int(record["seed"])
        pair_index = int(record["pair_index"])
        bucket = condition_rows[(condition_id, seed)]
        if pair_index in bucket:
            raise ValueError("duplicate primary/reference pair during scoring")
        bucket[pair_index] = record

    expected_pair_set = set(range(EXPECTED_PAIRS))
    for condition_id in (PRIMARY_CONDITION, REFERENCE_CONDITION):
        for seed in OFFICIAL_SEEDS:
            if set(condition_rows[(condition_id, seed)]) != expected_pair_set:
                raise ValueError("primary/reference seed row is incomplete")

    deltas: list[float] = []
    for pair_index, target in enumerate(targets):
        primary_mean = mean(
            _correct(condition_rows[(PRIMARY_CONDITION, seed)][pair_index], target)
            for seed in OFFICIAL_SEEDS
        )
        reference_mean = mean(
            _correct(condition_rows[(REFERENCE_CONDITION, seed)][pair_index], target)
            for seed in OFFICIAL_SEEDS
        )
        deltas.append(primary_mean - reference_mean)
    return tuple(deltas)


def _effect_from_indices(
    deltas: Sequence[float], targets: Sequence[Target], sampled_indices: Sequence[int]
) -> float:
    update_sum = 0.0
    maintain_sum = 0.0
    update_n = 0
    maintain_n = 0
    for pair_index in sampled_indices:
        if targets[pair_index]["update_required"]:
            update_sum += deltas[pair_index]
            update_n += 1
        else:
            maintain_sum += deltas[pair_index]
            maintain_n += 1
    if update_n == 0 or maintain_n == 0:
        raise ValueError("bootstrap resample produced an empty registered slice")
    return ((update_sum / update_n) + (maintain_sum / maintain_n)) / 2.0


def paired_breu_bootstrap(
    raw: RawBundleV2, targets: Sequence[Target]
) -> dict[str, Any]:
    deltas = _primary_reference_delta_by_pair(raw, targets)
    observed = _effect_from_indices(deltas, targets, tuple(range(EXPECTED_PAIRS)))
    rng = random.Random(BOOTSTRAP_SEED)
    effects: list[float] = []
    for _ in range(BOOTSTRAP_RESAMPLES):
        sampled = tuple(
            rng.randrange(EXPECTED_PAIRS) for _ in range(BOOTSTRAP_DRAWS_PER_RESAMPLE)
        )
        effects.append(_effect_from_indices(deltas, targets, sampled))

    lower = linear_quantile_10k(effects, BOOTSTRAP_LOWER_P)
    upper = linear_quantile_10k(effects, BOOTSTRAP_UPPER_P)
    if lower > 0.0:
        result_class = "PASS"
    elif upper <= 0.0:
        result_class = "FAIL"
    else:
        result_class = "INCONCLUSIVE"
    return {
        "method": "paired_official_pair_bootstrap",
        "resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "draws_per_resample": BOOTSTRAP_DRAWS_PER_RESAMPLE,
        "shared_resample_indices_across_all_five_seeds": True,
        "seed_aggregation": (
            "recompute per-seed BU_Acc/BM_Acc/BREU then mean the five seed BREU values"
        ),
        "primary_contrast": "primary_condition_minus_reference_condition",
        "observed_effect": observed,
        "confidence_interval": {"level": 0.95, "lower": lower, "upper": upper},
        "result_class": result_class,
    }


def score_official_v2(
    raw: RawBundleV2,
    evaluator_targets: Sequence[Mapping[str, Any]],
    *,
    enforce_official_runtime: bool = True,
) -> Mapping[str, object]:
    """Score only an already-preserved raw bundle supplied by the harness."""

    if enforce_official_runtime:
        assert_official_python_runtime()
    targets = validate_evaluator_targets(raw, evaluator_targets)

    records_by_row: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for record in raw.records:
        records_by_row[str(record["row_id"])].append(record)
    metrics_by_row = {
        row_id: _row_metrics(records, targets)
        for row_id, records in sorted(records_by_row.items())
    }
    paired = paired_breu_bootstrap(raw, targets)

    scored_predictions = [
        {
            "row_id": record["row_id"],
            "seed": record["seed"],
            "pair_index": record["pair_index"],
            "correct": bool(
                record["prediction"]
                == targets[int(record["pair_index"])]["target_choice_id"]
            ),
            "update_required": bool(
                targets[int(record["pair_index"])]["update_required"]
            ),
        }
        for record in raw.records
    ]
    failures = [row for row in scored_predictions if not row["correct"]]
    return {
        "protocol_id": PROTOCOL_ID,
        "run_identity": PLANNED_IDENTITY,
        "raw_sha256": raw.sha256,
        "scored_predictions": scored_predictions,
        "metrics_by_row": metrics_by_row,
        "paired_statistics": paired,
        "baseline_matching": {
            "winner_claim_allowed": False,
            "reason": (
                "parameter/compute matching remains unasserted; "
                "baseline rows are descriptive"
            ),
        },
        "failure_examples": failures,
        "report": {
            "primary_result_class": paired["result_class"],
            "claim_boundary": "truth_free_surface_structural_representation_gain_only",
        },
    }

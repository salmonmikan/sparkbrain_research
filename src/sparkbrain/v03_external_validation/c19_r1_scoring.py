"""Fail-closed scorer for the prospective C19-R1 matched reduction.

The scorer consumes only immutable R1 raw, immutable C19-v4 raw bound to the
terminal v4 preserve digest, a preserved target-free atomic_idx source map, and
evaluator targets materialized after R1 raw/source-map preservation.
"""

from __future__ import annotations

import math
import platform
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from statistics import mean
from typing import Any

from sparkbrain.v03_external_validation.c19_r1_protocol import (
    BOOTSTRAP_LOWER_P,
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    BOOTSTRAP_UPPER_P,
    EXPECTED_MAINTAIN_PAIRS,
    EXPECTED_PAIRS,
    EXPECTED_UPDATE_PAIRS,
    OFFICIAL_PYTHON_IMPLEMENTATION,
    OFFICIAL_PYTHON_VERSION,
    OFFICIAL_SEEDS,
    PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE,
    V4_PRIMARY_CONDITION,
)
from sparkbrain.v03_external_validation.c19_r1_revision_authority import RawBundleR1
from sparkbrain.v03_external_validation.c19_r1_source_map import (
    atomic_idx_clusters,
    validate_atomic_idx_source_map,
)
from sparkbrain.v03_external_validation.official_execution_v4 import RawBundleV4
from sparkbrain.v03_external_validation.official_protocol_v4 import EVALUATOR_TARGET_FIELDS

Target = dict[str, Any]
JoinKey = tuple[int, str, int, int]


def assert_official_python_runtime() -> None:
    if platform.python_implementation() != OFFICIAL_PYTHON_IMPLEMENTATION:
        raise RuntimeError("official C19-R1 scoring requires CPython")
    if platform.python_version() != OFFICIAL_PYTHON_VERSION:
        raise RuntimeError(
            f"official C19-R1 scoring requires Python {OFFICIAL_PYTHON_VERSION}"
        )


def _non_negative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def _join_key(row: Mapping[str, Any]) -> JoinKey:
    return (
        _non_negative_int(row["pair_index"], "pair_index"),
        str(row["record_id_hash"]),
        _non_negative_int(row["source_index"], "source_index"),
        _non_negative_int(row["step_index"], "step_index"),
    )


def validate_evaluator_targets(
    raw: RawBundleR1,
    evaluator_targets: Sequence[Mapping[str, Any]],
) -> tuple[Target, ...]:
    if len(evaluator_targets) != EXPECTED_PAIRS:
        raise ValueError("R1 evaluator targets must contain exactly 1744 pairs")
    raw_keys: dict[int, JoinKey] = {}
    for record in raw.records:
        pair_index = int(record["pair_index"])
        key = _join_key(record)
        prior = raw_keys.setdefault(pair_index, key)
        if prior != key:
            raise ValueError("R1 raw join identity differs across seed rows")
    if set(raw_keys) != set(range(EXPECTED_PAIRS)):
        raise ValueError("R1 raw pair inventory is not total")

    seen_pairs: set[int] = set()
    seen_keys: set[JoinKey] = set()
    targets: dict[int, Target] = {}
    updates = 0
    for target_value in evaluator_targets:
        target = dict(target_value)
        if set(target) != set(EVALUATOR_TARGET_FIELDS):
            raise ValueError("R1 evaluator target fields drift")
        pair_index = _non_negative_int(target["pair_index"], "pair_index")
        key = _join_key(target)
        if pair_index in seen_pairs or key in seen_keys:
            raise ValueError("duplicate R1 evaluator target")
        if raw_keys.get(pair_index) != key:
            raise ValueError("R1 evaluator join mismatch")
        if not isinstance(target["target_choice_id"], str) or not target["target_choice_id"]:
            raise ValueError("R1 target choice id must be non-empty")
        if not isinstance(target["update_required"], bool):
            raise ValueError("R1 update_required must be boolean")
        seen_pairs.add(pair_index)
        seen_keys.add(key)
        targets[pair_index] = target
        updates += int(target["update_required"])

    if seen_pairs != set(range(EXPECTED_PAIRS)):
        raise ValueError("R1 evaluator target join is not total")
    if updates != EXPECTED_UPDATE_PAIRS:
        raise ValueError("R1 update slice count drift")
    if EXPECTED_PAIRS - updates != EXPECTED_MAINTAIN_PAIRS:
        raise ValueError("R1 maintain slice count drift")
    return tuple(targets[index] for index in range(EXPECTED_PAIRS))


def _correct(record: Mapping[str, Any], target: Mapping[str, Any]) -> float:
    return float(record["prediction"] == target["target_choice_id"])


def _v4_primary_rows(raw: RawBundleV4) -> dict[tuple[int, int], Mapping[str, Any]]:
    rows: dict[tuple[int, int], Mapping[str, Any]] = {}
    for record in raw.records:
        if record["row_kind"] != "c19_condition":
            continue
        condition = f"{record['input_track']}/{record['gate']}/{record['entity']}"
        if condition != V4_PRIMARY_CONDITION:
            continue
        key = (int(record["seed"]), int(record["pair_index"]))
        if key in rows:
            raise ValueError("duplicate v4 primary seed/pair")
        rows[key] = record
    expected = {
        (seed, pair_index)
        for seed in OFFICIAL_SEEDS
        for pair_index in range(EXPECTED_PAIRS)
    }
    if set(rows) != expected:
        raise ValueError("v4 primary condition coverage is incomplete")
    return rows


def _r1_rows(raw: RawBundleR1) -> dict[tuple[int, int], Mapping[str, Any]]:
    rows: dict[tuple[int, int], Mapping[str, Any]] = {}
    for record in raw.records:
        key = (int(record["seed"]), int(record["pair_index"]))
        if key in rows:
            raise ValueError("duplicate R1 seed/pair")
        rows[key] = record
    expected = {
        (seed, pair_index)
        for seed in OFFICIAL_SEEDS
        for pair_index in range(EXPECTED_PAIRS)
    }
    if set(rows) != expected:
        raise ValueError("R1 seed/pair coverage is incomplete")
    return rows


def reduction_delta_by_pair(
    r1_raw: RawBundleR1,
    v4_raw: RawBundleV4,
    targets: Sequence[Target],
) -> tuple[float, ...]:
    r1 = _r1_rows(r1_raw)
    v4 = _v4_primary_rows(v4_raw)
    deltas = []
    for pair_index, target in enumerate(targets):
        v4_mean = mean(_correct(v4[(seed, pair_index)], target) for seed in OFFICIAL_SEEDS)
        r1_mean = mean(_correct(r1[(seed, pair_index)], target) for seed in OFFICIAL_SEEDS)
        deltas.append(v4_mean - r1_mean)
    return tuple(deltas)


def _effect_from_indices(
    deltas: Sequence[float],
    targets: Sequence[Target],
    sampled_indices: Sequence[int],
) -> float:
    update_values = []
    maintain_values = []
    for pair_index in sampled_indices:
        if targets[pair_index]["update_required"]:
            update_values.append(deltas[pair_index])
        else:
            maintain_values.append(deltas[pair_index])
    if not update_values or not maintain_values:
        raise ValueError("R1 bootstrap resample produced an empty registered slice")
    return (mean(update_values) + mean(maintain_values)) / 2.0


def linear_quantile_10k(effects: Sequence[float], p: float) -> float:
    if len(effects) != BOOTSTRAP_RESAMPLES:
        raise ValueError("R1 quantile requires exactly 10000 effects")
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not 0.0 <= float(p) <= 1.0:
        raise ValueError("R1 quantile p must be in [0,1]")
    values = sorted(float(value) for value in effects)
    if any(not math.isfinite(value) for value in values):
        raise ValueError("R1 quantile effects must be finite")
    rank = (len(values) - 1) * float(p)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return values[lower]
    fraction = rank - lower
    return values[lower] + (values[upper] - values[lower]) * fraction


def atomic_idx_cluster_resample_indices(
    atomic_idx_source_map: Sequence[Mapping[str, Any]],
    rng: random.Random,
) -> tuple[int, ...]:
    clusters = atomic_idx_clusters(atomic_idx_source_map)
    sampled: list[int] = []
    for _ in range(len(clusters)):
        _, pair_indices = clusters[rng.randrange(len(clusters))]
        sampled.extend(pair_indices)
    return tuple(sampled)


def _classify_interval(lower: float, upper: float) -> str:
    if lower > 0.0:
        return "SURVIVES_REDUCTION"
    if upper <= 0.0:
        return "REDUCED"
    return "INCONCLUSIVE"


def paired_reduction_bootstrap(
    r1_raw: RawBundleR1,
    v4_raw: RawBundleV4,
    targets: Sequence[Target],
    atomic_idx_source_map: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_map = validate_atomic_idx_source_map(atomic_idx_source_map)
    clusters = atomic_idx_clusters(source_map)
    deltas = reduction_delta_by_pair(r1_raw, v4_raw, targets)
    observed = _effect_from_indices(deltas, targets, tuple(range(EXPECTED_PAIRS)))
    rng = random.Random(BOOTSTRAP_SEED)
    effects = []
    for _ in range(BOOTSTRAP_RESAMPLES):
        sampled = atomic_idx_cluster_resample_indices(source_map, rng)
        effects.append(_effect_from_indices(deltas, targets, sampled))
    lower = linear_quantile_10k(effects, BOOTSTRAP_LOWER_P)
    upper = linear_quantile_10k(effects, BOOTSTRAP_UPPER_P)
    result_class = _classify_interval(lower, upper)
    return {
        "method": "paired_atomic_idx_cluster_bootstrap",
        "contrast": "c19_v4_primary_breu_minus_r1_breu",
        "cluster_key": "atomic_idx",
        "unique_clusters": len(clusters),
        "clusters_per_resample": len(clusters),
        "cluster_observation_policy": "carry_all_paired_observations_at_sampled_cluster_multiplicity",
        "cluster_order": "first_occurrence_in_pair_index_order",
        "resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "observed_effect": observed,
        "confidence_interval": {"level": 0.95, "lower": lower, "upper": upper},
        "result_class": result_class,
        "claim_boundary": (
            "SURVIVES_REDUCTION rejects only this fixed stateless authority reduction; "
            "it is not proof of persistent dynamics"
        ),
    }


def pair_iid_sensitivity_bootstrap(
    r1_raw: RawBundleR1,
    v4_raw: RawBundleV4,
    targets: Sequence[Target],
) -> dict[str, Any]:
    deltas = reduction_delta_by_pair(r1_raw, v4_raw, targets)
    observed = _effect_from_indices(deltas, targets, tuple(range(EXPECTED_PAIRS)))
    rng = random.Random(BOOTSTRAP_SEED)
    effects = []
    for _ in range(BOOTSTRAP_RESAMPLES):
        sampled = tuple(
            rng.randrange(EXPECTED_PAIRS)
            for _ in range(PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE)
        )
        effects.append(_effect_from_indices(deltas, targets, sampled))
    lower = linear_quantile_10k(effects, BOOTSTRAP_LOWER_P)
    upper = linear_quantile_10k(effects, BOOTSTRAP_UPPER_P)
    return {
        "method": "paired_official_pair_bootstrap_sensitivity",
        "contrast": "c19_v4_primary_breu_minus_r1_breu",
        "resamples": BOOTSTRAP_RESAMPLES,
        "draws_per_resample": PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "observed_effect": observed,
        "confidence_interval": {"level": 0.95, "lower": lower, "upper": upper},
        "result_class": _classify_interval(lower, upper),
        "role": "secondary_sensitivity_only",
    }


def score_reduction(
    r1_raw: RawBundleR1,
    v4_raw: RawBundleV4,
    evaluator_targets: Sequence[Mapping[str, Any]],
    atomic_idx_source_map: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_map = validate_atomic_idx_source_map(atomic_idx_source_map)
    targets = validate_evaluator_targets(r1_raw, evaluator_targets)
    primary = paired_reduction_bootstrap(r1_raw, v4_raw, targets, source_map)
    sensitivity = pair_iid_sensitivity_bootstrap(r1_raw, v4_raw, targets)

    r1_rows: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for record in r1_raw.records:
        r1_rows[int(record["seed"])].append(record)
    metrics = {}
    for seed, records in sorted(r1_rows.items()):
        by_pair = {int(record["pair_index"]): record for record in records}
        updates = [index for index, target in enumerate(targets) if target["update_required"]]
        maintains = [
            index for index, target in enumerate(targets) if not target["update_required"]
        ]
        bu = mean(_correct(by_pair[index], targets[index]) for index in updates)
        bm = mean(_correct(by_pair[index], targets[index]) for index in maintains)
        metrics[str(seed)] = {"BU_Acc": bu, "BM_Acc": bm, "BREU": (bu + bm) / 2.0}

    return {
        "paired_reduction_statistics": primary,
        "pair_iid_sensitivity_statistics": sensitivity,
        "r1_metrics_by_seed": metrics,
        "report": {
            "reduction_result_class": primary["result_class"],
            "primary_inference_method": primary["method"],
            "pair_iid_result_role": "secondary_sensitivity_only",
            "claim_boundary": primary["claim_boundary"],
        },
    }


__all__ = [
    "assert_official_python_runtime",
    "atomic_idx_cluster_resample_indices",
    "linear_quantile_10k",
    "pair_iid_sensitivity_bootstrap",
    "paired_reduction_bootstrap",
    "reduction_delta_by_pair",
    "score_reduction",
    "validate_evaluator_targets",
]

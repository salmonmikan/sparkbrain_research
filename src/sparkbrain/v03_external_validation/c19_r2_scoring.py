"""Fail-closed scorer contract for the prospective C19-R2 FSA reduction.

This module never locates official data. A future authorized runner must first
immutably preserve target-blind R2 raw plus the atomic_idx source map, re-fetch
and digest-verify them, and only then materialize evaluator targets.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import mean
from typing import Any

from sparkbrain.v03_external_validation.c19_r2_protocol import (
    BOOTSTRAP_LOWER_P,
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    BOOTSTRAP_UPPER_P,
    CHOICES,
    EXPECTED_MAINTAIN_PAIRS,
    EXPECTED_PAIRS,
    EXPECTED_UPDATE_PAIRS,
    INPUT_TRACK,
    MECHANISM_ID,
    OFFICIAL_SEEDS,
    PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE,
    PROTOCOL_ID,
    ROW_KIND,
    STATE_ALPHABET,
    V4_PRIMARY_CONDITION,
    expected_r2_rows,
)
from sparkbrain.v03_external_validation.c19_r2_source_map import (
    atomic_idx_clusters,
    validate_atomic_idx_source_map,
)
from sparkbrain.v03_external_validation.official_execution import reject_target_leakage
from sparkbrain.v03_external_validation.official_execution_v4 import RawBundleV4
from sparkbrain.v03_external_validation.official_protocol_v4 import EVALUATOR_TARGET_FIELDS

Target = dict[str, Any]
JoinKey = tuple[int, str, int, int]
_RAW_KEYS = frozenset(
    {
        "protocol_id",
        "run_identity",
        "row_id",
        "row_kind",
        "mechanism_id",
        "seed",
        "pair_index",
        "record_id_hash",
        "source_index",
        "step_index",
        "prediction",
        "input_track",
        "final_state",
        "work_counters",
    }
)


def _canonical(value: object) -> str:
    return json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _non_negative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def validate_r2_raw_records(records: Sequence[Mapping[str, Any]]) -> str:
    rows = {str(row["row_id"]): row for row in expected_r2_rows()}
    expected_pairs = set(range(EXPECTED_PAIRS))
    pairs_by_row = {row_id: set() for row_id in rows}
    join_identity: dict[int, tuple[str, int, int]] = {}
    run_identity: str | None = None

    if len(records) != len(rows) * EXPECTED_PAIRS:
        raise ValueError("R2 raw record count drift")
    for record in records:
        if set(record) != _RAW_KEYS:
            raise ValueError("R2 raw record keys differ from frozen schema")
        reject_target_leakage(record, path="r2_raw")
        if record["protocol_id"] != PROTOCOL_ID:
            raise ValueError("R2 raw protocol drift")
        identity = record["run_identity"]
        if not isinstance(identity, str) or not identity:
            raise ValueError("R2 raw requires one future non-empty formal identity")
        if run_identity is None:
            run_identity = identity
        elif identity != run_identity:
            raise ValueError("R2 raw identity differs across records")
        row_id = str(record["row_id"])
        if row_id not in rows:
            raise ValueError("R2 raw references unknown row")
        expected = rows[row_id]
        if record["row_kind"] != ROW_KIND or record["mechanism_id"] != MECHANISM_ID:
            raise ValueError("R2 raw row/mechanism drift")
        if record["seed"] != expected["seed"]:
            raise ValueError("R2 raw seed drift")
        if record["input_track"] != INPUT_TRACK:
            raise ValueError("R2 raw I2 binding drift")
        pair_index = _non_negative_int(record["pair_index"], "pair_index")
        if pair_index >= EXPECTED_PAIRS or pair_index in pairs_by_row[row_id]:
            raise ValueError("R2 raw pair inventory drift")
        pairs_by_row[row_id].add(pair_index)
        record_hash = record["record_id_hash"]
        if not _is_sha256(record_hash):
            raise ValueError("R2 record_id_hash must be SHA-256")
        source_index = _non_negative_int(record["source_index"], "source_index")
        step_index = _non_negative_int(record["step_index"], "step_index")
        if (source_index, step_index) != (1, 1):
            raise ValueError("R2 evaluator join must bind to final visible step")
        join = (str(record_hash), source_index, step_index)
        prior = join_identity.setdefault(pair_index, join)
        if prior != join:
            raise ValueError("R2 cross-seed pair join identity mismatch")
        if record["prediction"] not in CHOICES:
            raise ValueError("R2 prediction outside frozen choice alphabet")
        if record["final_state"] not in STATE_ALPHABET[1:]:
            raise ValueError("R2 raw final state outside active state alphabet")
        if not isinstance(record["work_counters"], Mapping):
            raise ValueError("R2 work counters missing")

    if any(seen != expected_pairs for seen in pairs_by_row.values()):
        raise ValueError("R2 raw pair coverage must be total for every seed row")
    assert run_identity is not None
    return run_identity


@dataclass(frozen=True, slots=True)
class RawBundleR2:
    records: tuple[dict[str, Any], ...]
    sha256: str

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> RawBundleR2:
        normalized = tuple(dict(record) for record in records)
        validate_r2_raw_records(normalized)
        digest = hashlib.sha256(_canonical(normalized).encode("utf-8")).hexdigest()
        return cls(normalized, digest)


def _join_key(row: Mapping[str, Any]) -> JoinKey:
    return (
        _non_negative_int(row["pair_index"], "pair_index"),
        str(row["record_id_hash"]),
        _non_negative_int(row["source_index"], "source_index"),
        _non_negative_int(row["step_index"], "step_index"),
    )


def validate_evaluator_targets(
    raw: RawBundleR2,
    evaluator_targets: Sequence[Mapping[str, Any]],
) -> tuple[Target, ...]:
    if len(evaluator_targets) != EXPECTED_PAIRS:
        raise ValueError("R2 evaluator targets must contain exactly 1744 pairs")
    raw_keys: dict[int, JoinKey] = {}
    for record in raw.records:
        pair_index = int(record["pair_index"])
        key = _join_key(record)
        prior = raw_keys.setdefault(pair_index, key)
        if prior != key:
            raise ValueError("R2 raw join identity differs across seed rows")
    if set(raw_keys) != set(range(EXPECTED_PAIRS)):
        raise ValueError("R2 raw pair inventory is not total")

    seen_pairs: set[int] = set()
    seen_keys: set[JoinKey] = set()
    targets: dict[int, Target] = {}
    updates = 0
    for target_value in evaluator_targets:
        target = dict(target_value)
        if set(target) != set(EVALUATOR_TARGET_FIELDS):
            raise ValueError("R2 evaluator target fields drift")
        pair_index = _non_negative_int(target["pair_index"], "pair_index")
        key = _join_key(target)
        if pair_index in seen_pairs or key in seen_keys:
            raise ValueError("duplicate R2 evaluator target")
        if raw_keys.get(pair_index) != key:
            raise ValueError("R2 evaluator join mismatch")
        if not isinstance(target["target_choice_id"], str) or not target["target_choice_id"]:
            raise ValueError("R2 target choice id must be non-empty")
        if not isinstance(target["update_required"], bool):
            raise ValueError("R2 update_required must be boolean")
        seen_pairs.add(pair_index)
        seen_keys.add(key)
        targets[pair_index] = target
        updates += int(target["update_required"])

    if seen_pairs != set(range(EXPECTED_PAIRS)):
        raise ValueError("R2 evaluator target join is not total")
    if updates != EXPECTED_UPDATE_PAIRS:
        raise ValueError("R2 update slice count drift")
    if EXPECTED_PAIRS - updates != EXPECTED_MAINTAIN_PAIRS:
        raise ValueError("R2 maintain slice count drift")
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


def _r2_rows(raw: RawBundleR2) -> dict[tuple[int, int], Mapping[str, Any]]:
    rows: dict[tuple[int, int], Mapping[str, Any]] = {}
    for record in raw.records:
        key = (int(record["seed"]), int(record["pair_index"]))
        if key in rows:
            raise ValueError("duplicate R2 seed/pair")
        rows[key] = record
    expected = {
        (seed, pair_index)
        for seed in OFFICIAL_SEEDS
        for pair_index in range(EXPECTED_PAIRS)
    }
    if set(rows) != expected:
        raise ValueError("R2 seed/pair coverage is incomplete")
    return rows


def reduction_delta_by_pair(
    r2_raw: RawBundleR2,
    v4_raw: RawBundleV4,
    targets: Sequence[Target],
) -> tuple[float, ...]:
    r2 = _r2_rows(r2_raw)
    v4 = _v4_primary_rows(v4_raw)
    deltas = []
    for pair_index, target in enumerate(targets):
        v4_mean = mean(_correct(v4[(seed, pair_index)], target) for seed in OFFICIAL_SEEDS)
        r2_mean = mean(_correct(r2[(seed, pair_index)], target) for seed in OFFICIAL_SEEDS)
        deltas.append(v4_mean - r2_mean)
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
        raise ValueError("R2 bootstrap resample produced an empty registered slice")
    return (mean(update_values) + mean(maintain_values)) / 2.0


def linear_quantile_10k(effects: Sequence[float], p: float) -> float:
    if len(effects) != BOOTSTRAP_RESAMPLES:
        raise ValueError("R2 quantile requires exactly 10000 effects")
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not 0.0 <= float(p) <= 1.0:
        raise ValueError("R2 quantile p must be in [0,1]")
    values = sorted(float(value) for value in effects)
    if any(not math.isfinite(value) for value in values):
        raise ValueError("R2 quantile effects must be finite")
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
        return "SURVIVES_FSA_REDUCTION"
    if upper <= 0.0:
        return "REDUCED_BY_FSA"
    return "INCONCLUSIVE"


def paired_reduction_bootstrap(
    r2_raw: RawBundleR2,
    v4_raw: RawBundleV4,
    targets: Sequence[Target],
    atomic_idx_source_map: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_map = validate_atomic_idx_source_map(atomic_idx_source_map)
    clusters = atomic_idx_clusters(source_map)
    deltas = reduction_delta_by_pair(r2_raw, v4_raw, targets)
    observed = _effect_from_indices(deltas, targets, tuple(range(EXPECTED_PAIRS)))
    rng = random.Random(BOOTSTRAP_SEED)
    effects = []
    for _ in range(BOOTSTRAP_RESAMPLES):
        sampled = atomic_idx_cluster_resample_indices(source_map, rng)
        effects.append(_effect_from_indices(deltas, targets, sampled))
    lower = linear_quantile_10k(effects, BOOTSTRAP_LOWER_P)
    upper = linear_quantile_10k(effects, BOOTSTRAP_UPPER_P)
    return {
        "method": "paired_atomic_idx_cluster_bootstrap",
        "contrast": "c19_v4_primary_breu_minus_r2_breu",
        "cluster_key": "atomic_idx",
        "unique_clusters": len(clusters),
        "clusters_per_resample": len(clusters),
        "cluster_observation_policy": (
            "carry_all_paired_observations_at_sampled_cluster_multiplicity"
        ),
        "cluster_order": "first_occurrence_in_pair_index_order",
        "resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "observed_effect": observed,
        "confidence_interval": {"level": 0.95, "lower": lower, "upper": upper},
        "result_class": _classify_interval(lower, upper),
        "claim_boundary": (
            "This contrast tests only the fixed seven-state FSA reduction. R1 revision-authority "
            "remains scientifically unresolved and therefore remains an interpretation ceiling."
        ),
    }


def pair_iid_sensitivity_bootstrap(
    r2_raw: RawBundleR2,
    v4_raw: RawBundleV4,
    targets: Sequence[Target],
) -> dict[str, Any]:
    deltas = reduction_delta_by_pair(r2_raw, v4_raw, targets)
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
        "contrast": "c19_v4_primary_breu_minus_r2_breu",
        "resamples": BOOTSTRAP_RESAMPLES,
        "draws_per_resample": PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "observed_effect": observed,
        "confidence_interval": {"level": 0.95, "lower": lower, "upper": upper},
        "result_class": _classify_interval(lower, upper),
        "role": "secondary_sensitivity_only",
    }


def score_reduction(
    r2_raw: RawBundleR2,
    v4_raw: RawBundleV4,
    evaluator_targets: Sequence[Mapping[str, Any]],
    atomic_idx_source_map: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_map = validate_atomic_idx_source_map(atomic_idx_source_map)
    targets = validate_evaluator_targets(r2_raw, evaluator_targets)
    primary = paired_reduction_bootstrap(r2_raw, v4_raw, targets, source_map)
    sensitivity = pair_iid_sensitivity_bootstrap(r2_raw, v4_raw, targets)

    rows_by_seed: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for record in r2_raw.records:
        rows_by_seed[int(record["seed"])].append(record)
    metrics = {}
    for seed, records in sorted(rows_by_seed.items()):
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
        "r2_metrics_by_seed": metrics,
        "report": {
            "reduction_result_class": primary["result_class"],
            "primary_inference_method": primary["method"],
            "pair_iid_result_role": "secondary_sensitivity_only",
            "claim_boundary": primary["claim_boundary"],
        },
    }


__all__ = [
    "RawBundleR2",
    "atomic_idx_cluster_resample_indices",
    "linear_quantile_10k",
    "pair_iid_sensitivity_bootstrap",
    "paired_reduction_bootstrap",
    "reduction_delta_by_pair",
    "score_reduction",
    "validate_evaluator_targets",
    "validate_r2_raw_records",
]

from __future__ import annotations

import hashlib
import math

import pytest

from sparkbrain.v03_external_validation.official_execution_v2 import RawBundleV2
from sparkbrain.v03_external_validation.official_protocol_v2 import (
    EXPECTED_PAIRS,
    EXPECTED_UPDATE_PAIRS,
    PLANNED_IDENTITY,
    PROTOCOL_ID,
    expected_row_inventory,
)
from sparkbrain.v03_external_validation.official_scoring_v2 import (
    linear_quantile_10k,
    validate_evaluator_targets,
)


def _hash_record(pair_index: int) -> str:
    return hashlib.sha256(f"record-{pair_index}".encode()).hexdigest()


def _targets() -> list[dict[str, object]]:
    return [
        {
            "pair_index": pair_index,
            "record_id_hash": _hash_record(pair_index),
            "source_index": pair_index,
            "step_index": 1,
            "target_choice_id": "a" if pair_index % 2 == 0 else "b",
            "update_required": pair_index < EXPECTED_UPDATE_PAIRS,
        }
        for pair_index in range(EXPECTED_PAIRS)
    ]


def _raw() -> RawBundleV2:
    records: list[dict[str, object]] = []
    for row in expected_row_inventory():
        for pair_index in range(EXPECTED_PAIRS):
            records.append(
                {
                    "protocol_id": PROTOCOL_ID,
                    "run_identity": PLANNED_IDENTITY,
                    "row_id": row["row_id"],
                    "row_kind": row["row_kind"],
                    "seed": row["seed"],
                    "pair_index": pair_index,
                    "record_id_hash": _hash_record(pair_index),
                    "source_index": pair_index,
                    "step_index": 1,
                    "prediction": "a",
                    "probabilities": {"a": 1.0, "b": 0.0, "c": 0.0},
                    "input_track": row.get("input_track"),
                    "gate": row.get("gate"),
                    "entity": row.get("entity"),
                    "baseline_kind": row.get("baseline_kind"),
                    "work_counters": {"ops": 1},
                }
            )
    return RawBundleV2.from_records(records)


def test_full_evaluator_join_is_unique_total_and_post_raw() -> None:
    raw = _raw()
    targets = validate_evaluator_targets(raw, _targets())
    assert len(targets) == 1744
    assert [target["pair_index"] for target in targets] == list(range(1744))
    assert sum(bool(target["update_required"]) for target in targets) == 1074
    assert all("target_choice_id" not in record for record in raw.records)
    assert all("update_required" not in record for record in raw.records)


def test_duplicate_evaluator_join_fails_closed() -> None:
    targets = _targets()
    targets[-1] = dict(targets[0])
    with pytest.raises(ValueError, match="duplicate"):
        validate_evaluator_targets(_raw(), targets)


def test_missing_evaluator_join_fails_closed() -> None:
    with pytest.raises(ValueError, match="exactly 1744"):
        validate_evaluator_targets(_raw(), _targets()[:-1])


def test_evaluator_field_leakage_or_expansion_fails_closed() -> None:
    targets = _targets()
    targets[0]["question"] = "forbidden evaluator expansion"
    with pytest.raises(ValueError, match="fields differ"):
        validate_evaluator_targets(_raw(), targets)


def test_linear_quantile_golden_ties_and_boundaries() -> None:
    tied = [0.125] * 10_000
    assert linear_quantile_10k(tied, 0.025) == 0.125
    assert linear_quantile_10k(tied, 0.975) == 0.125
    values = [float(index) for index in range(10_000)]
    assert linear_quantile_10k(values, 0.0) == 0.0
    assert linear_quantile_10k(values, 1.0) == 9999.0
    assert linear_quantile_10k(values, 0.025) == pytest.approx(249.975)
    assert linear_quantile_10k(values, 0.975) == pytest.approx(9749.025)


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_linear_quantile_rejects_non_finite(bad: float) -> None:
    values = [0.0] * 10_000
    values[123] = bad
    with pytest.raises(ValueError, match="finite"):
        linear_quantile_10k(values, 0.5)


def test_linear_quantile_rejects_empty_and_wrong_length() -> None:
    with pytest.raises(ValueError, match="exactly 10000"):
        linear_quantile_10k([], 0.5)
    with pytest.raises(ValueError, match="exactly 10000"):
        linear_quantile_10k([0.0] * 9999, 0.5)

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.v03_external_validation.contracts import (
    EXACT_NINE_ARTIFACTS,
    autonomous_aggregate_rows,
    validate_attribution_row,
    validate_baseline_matching,
    validate_disabled_preregistration,
)
from sparkbrain.v03_external_validation.proxy import (
    attribute_fault,
    fresh_proxy_splits,
    synthetic_proxy_row,
)

ROOT = Path(__file__).parents[1]


def test_disabled_preregistration_freezes_exact_nine_and_c18_boundary() -> None:
    protocol = json.loads(
        (ROOT / "artifacts/v03/c19_external_validation/preregistration.json").read_text(
            encoding="utf-8"
        )
    )
    validate_disabled_preregistration(protocol)
    assert set(protocol["artifact_inventory"]) == EXACT_NINE_ARTIFACTS
    assert protocol["official_evaluation_allowed"] is False
    assert protocol["source_commit"] is None


def test_preregistration_rejects_official_selection_and_seed_overlap() -> None:
    protocol = json.loads(
        (ROOT / "artifacts/v03/c19_external_validation/preregistration.json").read_text(
            encoding="utf-8"
        )
    )
    protocol["checkpoint_selection"]["calibration_split"] = "official_test"
    with pytest.raises(ValueError, match="official test"):
        validate_disabled_preregistration(protocol)
    protocol["checkpoint_selection"]["calibration_split"] = "dev"
    protocol["fresh_seed_contract"]["reserved_test_seed_range"][0] = 5901
    with pytest.raises(ValueError, match="must not overlap"):
        validate_disabled_preregistration(protocol)


def test_proxy_splits_are_fresh_disjoint_and_do_not_include_official_test() -> None:
    splits = fresh_proxy_splits(seed=7901)
    assert fresh_proxy_splits(seed=7901) == splits
    assert set(splits) == {"train", "dev", "synthetic_proxy"}
    assert not (set(splits["train"]) & set(splits["dev"]))
    assert not (set(splits["train"]) & set(splits["synthetic_proxy"]))
    assert not (set(splits["dev"]) & set(splits["synthetic_proxy"]))


def test_oracle_and_autonomous_proxy_rows_remain_separate() -> None:
    autonomous, _ = synthetic_proxy_row(
        seed=6901, episode_id="proxy-a", input_track="I1_local_compositional"
    )
    oracle, _ = synthetic_proxy_row(
        seed=6901, episode_id="proxy-b", input_track="I2_symbolic_oracle"
    )
    assert autonomous["oracle_diagnostic"] is False
    assert oracle["oracle_diagnostic"] is True
    assert autonomous["split"] == oracle["split"] == "synthetic_proxy"
    with pytest.raises(ValueError, match="excluded"):
        autonomous_aggregate_rows([autonomous, oracle])


def test_single_entity_fault_attribution_is_inconclusive() -> None:
    result = attribute_fault(
        entity_count=1,
        local_correct=False,
        oracle_correct=True,
        gate_changed_decision=False,
        state_changed_decision=False,
        objective_changed_decision=False,
    )
    assert result.status == "inconclusive"
    assert result.dominant_component is None


def test_strict_attribution_schema_rejects_single_entity_overclaim() -> None:
    with pytest.raises(ValueError, match="single-entity"):
        validate_attribution_row(
            {
                "available": True,
                "condition_id": "I1/G0/E0",
                "dominant_component": "entity",
                "entity_count": 1,
                "episode_id_hash": "x",
                "reason": "wrong",
                "seed": 1,
                "status": "attributed",
            }
        )


def test_single_entity_available_claim_is_rejected_even_when_inconclusive() -> None:
    with pytest.raises(ValueError, match="single-entity"):
        validate_attribution_row(
            {
                "available": True,
                "condition_id": "I1/G0/E0",
                "dominant_component": None,
                "entity_count": 1,
                "episode_id_hash": "x",
                "reason": "wrong",
                "seed": 1,
                "status": "inconclusive",
            }
        )


def test_baseline_winner_claim_requires_all_matching_dimensions() -> None:
    with pytest.raises(ValueError, match="winner claims"):
        validate_baseline_matching(
            {
                "baseline_kind": "transformer",
                "checkpoint_selection_split": "dev",
                "compute_match": False,
                "data_match": True,
                "parameter_match": True,
                "winner_claim_allowed": True,
            }
        )


def test_fully_matched_baseline_can_still_make_no_winner_claim() -> None:
    validate_baseline_matching(
        {
            "baseline_kind": "transformer",
            "checkpoint_selection_split": "dev",
            "compute_match": True,
            "data_match": True,
            "parameter_match": True,
            "winner_claim_allowed": False,
        }
    )


def test_nested_target_leakage_in_work_counters_is_rejected() -> None:
    row, _ = synthetic_proxy_row(
        seed=6901, episode_id="proxy-a", input_track="I1_local_compositional"
    )
    row["work_counters"]["nested"] = {"target_label": "retain"}
    with pytest.raises(ValueError, match="target leakage"):
        from sparkbrain.v03_external_validation.contracts import validate_prediction_row

        validate_prediction_row(row)

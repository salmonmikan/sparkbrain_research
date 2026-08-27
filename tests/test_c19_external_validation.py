from __future__ import annotations

import inspect
import json
from copy import deepcopy
from pathlib import Path

import pytest

from sparkbrain.v03_external_validation.contracts import (
    EXACT_NINE_ARTIFACTS,
    C18TraceCheckpointAdapter,
    autonomous_aggregate_rows,
    validate_attribution_row,
    validate_baseline_matching,
    validate_disabled_preregistration,
    validate_prediction_row,
)
from sparkbrain.v03_external_validation.proxy import (
    attribute_fault,
    fresh_proxy_splits,
    synthetic_proxy_row,
)

ROOT = Path(__file__).parents[1]


def test_c18_trace_adapter_record_signature_matches_v6_contract() -> None:
    signature = inspect.signature(C18TraceCheckpointAdapter.record)
    parameters = signature.parameters
    assert tuple(parameters) == ("self", "kind", "payload", "state_delta")
    assert parameters["self"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameters["kind"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameters["payload"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameters["state_delta"].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters["state_delta"].default is inspect.Parameter.empty
    assert signature.return_annotation == "V03TraceEvent"


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


def test_preregistration_rejects_duplicate_inventory_and_matrix_extensions() -> None:
    protocol = json.loads(
        (ROOT / "artifacts/v03/c19_external_validation/preregistration.json").read_text(
            encoding="utf-8"
        )
    )
    duplicate = deepcopy(protocol)
    duplicate["artifact_inventory"].append(duplicate["artifact_inventory"][0])
    with pytest.raises(ValueError, match="exact-nine"):
        validate_disabled_preregistration(duplicate)
    reordered = deepcopy(protocol)
    reordered["artifact_inventory"].reverse()
    with pytest.raises(ValueError, match="exact-nine"):
        validate_disabled_preregistration(reordered)
    duplicate_baseline = deepcopy(protocol)
    duplicate_baseline["baseline_kinds"].append(duplicate_baseline["baseline_kinds"][0])
    with pytest.raises(ValueError, match="baseline inventory"):
        validate_disabled_preregistration(duplicate_baseline)
    extended = deepcopy(protocol)
    extended["condition_matrix"]["unauthorized"] = True
    with pytest.raises(ValueError, match="condition matrix"):
        validate_disabled_preregistration(extended)


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
                "condition_id": "I1_local_compositional/G0_probability_margin/E0_global",
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
                "condition_id": "I1_local_compositional/G0_probability_margin/E0_global",
                "dominant_component": None,
                "entity_count": 1,
                "episode_id_hash": "x",
                "reason": "wrong",
                "seed": 1,
                "status": "inconclusive",
            }
        )


@pytest.mark.parametrize(
    "mismatch_key",
    ("compute_match", "data_match", "optimization_match", "parameter_match"),
)
def test_baseline_winner_claim_requires_all_matching_dimensions(mismatch_key: str) -> None:
    row = {
        "baseline_kind": "transformer",
        "checkpoint_selection_split": "dev",
        "compute_match": True,
        "data_match": True,
        "optimization_match": True,
        "parameter_match": True,
        "winner_claim_allowed": True,
    }
    row[mismatch_key] = False
    with pytest.raises(ValueError, match="winner claims"):
        validate_baseline_matching(row)


def test_baseline_rejects_official_test_selection_even_without_winner_claim() -> None:
    with pytest.raises(ValueError, match="preregistered dev"):
        validate_baseline_matching(
            {
                "baseline_kind": "transformer",
            "checkpoint_selection_split": "official_test",
            "compute_match": True,
            "data_match": True,
            "optimization_match": True,
            "parameter_match": True,
                "winner_claim_allowed": False,
            }
        )


def test_fully_matched_baseline_can_still_make_no_winner_claim() -> None:
    validate_baseline_matching(
        {
            "baseline_kind": "transformer",
            "checkpoint_selection_split": "dev",
            "compute_match": True,
            "data_match": True,
            "optimization_match": True,
            "parameter_match": True,
            "winner_claim_allowed": False,
        }
    )


def test_baseline_matching_requires_optimization_dimension() -> None:
    row = {
        "baseline_kind": "transformer",
        "checkpoint_selection_split": "dev",
        "compute_match": True,
        "data_match": True,
        "parameter_match": True,
        "winner_claim_allowed": False,
    }
    with pytest.raises(ValueError, match="exact keys"):
        validate_baseline_matching(row)


@pytest.mark.parametrize(
    "key",
    (
        "compute_match",
        "data_match",
        "optimization_match",
        "parameter_match",
        "winner_claim_allowed",
    ),
)
def test_baseline_matching_flags_require_exact_booleans(key: str) -> None:
    row = {
        "baseline_kind": "transformer",
        "checkpoint_selection_split": "dev",
        "compute_match": False,
        "data_match": False,
        "optimization_match": False,
        "parameter_match": False,
        "winner_claim_allowed": False,
    }
    row[key] = 1
    with pytest.raises(ValueError, match="exact booleans"):
        validate_baseline_matching(row)


def test_nested_target_leakage_in_work_counters_is_rejected() -> None:
    row, _ = synthetic_proxy_row(
        seed=6901, episode_id="proxy-a", input_track="I1_local_compositional"
    )
    row["work_counters"]["nested"] = {"target_label": "retain"}
    with pytest.raises(ValueError, match="target leakage"):
        validate_prediction_row(row)


def test_condition_oracle_cannot_spoof_autonomous_flags() -> None:
    row, _ = synthetic_proxy_row(seed=6901, episode_id="proxy-o", input_track="I2_symbolic_oracle")
    row["oracle_diagnostic"] = False
    row["evaluator_only"] = False
    row["track"] = "autonomous"
    with pytest.raises(ValueError, match="diagnostic"):
        autonomous_aggregate_rows([row])


def test_prediction_rejects_unknown_condition_axes_and_integer_oracle_flags() -> None:
    row, _ = synthetic_proxy_row(
        seed=6901, episode_id="proxy-a", input_track="I0_whole_hash"
    )
    row["condition_id"] = "I0_whole_hash/UNKNOWN/UNKNOWN"
    with pytest.raises(ValueError, match="frozen input/gate/entity"):
        validate_prediction_row(row)

    oracle, _ = synthetic_proxy_row(
        seed=6901, episode_id="proxy-o", input_track="I2_symbolic_oracle"
    )
    oracle["oracle_diagnostic"] = 1
    oracle["evaluator_only"] = 1
    with pytest.raises(ValueError, match="exact booleans"):
        validate_prediction_row(oracle)


@pytest.mark.parametrize(
    ("status", "available", "dominant_component"),
    (
        ("fabricated", False, None),
        ("attributed", False, "input"),
        ("attributed", True, "entity"),
        ("inconclusive", True, None),
        ("inconclusive", False, "gate"),
    ),
)
def test_multi_entity_attribution_requires_registered_consistent_state(
    status: str, available: bool, dominant_component: str | None
) -> None:
    with pytest.raises(ValueError):
        validate_attribution_row(
            {
                "available": available,
                "condition_id": "I1_local_compositional/G0_probability_margin/E1_oracle_entity",
                "dominant_component": dominant_component,
                "entity_count": 2,
                "episode_id_hash": "x",
                "reason": "adversarial",
                "seed": 6901,
                "status": status,
            }
        )

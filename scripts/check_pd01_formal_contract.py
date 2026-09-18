#!/usr/bin/env python3
"""Fail-closed checks for the PD0.1 matched fading-memory formal-contract proposal."""

from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.external_validation.fading_memory import (
    DeterministicReservoir,
    PD01WorldConfig,
    ReservoirConfig,
    build_pd01_inputs,
    build_pd01_targets,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "research" / "pd01" / "formal_contract.json"
EXPECTED_ANALYST = "28108fffc2e4e346bff79bf3e38d1cac27d3265c"
EXPECTED_BASE = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
EXPECTED_IMPLEMENTATION_BLOB = "16bbfb6ed57d6c9701e8437360692b62e7c36915"


def main() -> None:
    raw = CONTRACT.read_text(encoding="utf-8")
    assert "UNRESOLVED" not in raw
    contract = json.loads(raw)

    assert contract["status"] == "FORMAL_CONTRACT_PROPOSAL_REVIEW_ONLY"
    assert contract["analyst_authority"] == EXPECTED_ANALYST
    assert contract["base_main"] == EXPECTED_BASE
    assert contract["formal_identity_proposed"] == "pd01-long-history-fading-memory-official-v1"
    assert contract["formal_identity_reserved"] is False
    assert contract["started_allowed"] is False
    assert contract["official_test_access_allowed"] is False
    assert contract["official_test_target_access_allowed"] is False
    assert contract["one_way_execution_allowed"] is False

    source = contract["source_binding"]
    assert source["sparkbrain_commit"] == EXPECTED_BASE
    assert source["sparkbrain_class"] == "sparkbrain.v04.brain:IntegratedV04Brain"
    assert source["pd01_implementation_git_blob"] == EXPECTED_IMPLEMENTATION_BLOB
    assert source["package_version"] == "0.3.2.dev0"

    runtime = contract["runtime_binding"]
    assert runtime == {
        "python": "3.11.16",
        "third_party_runtime_dependencies": [],
        "network_during_dev_or_test_execution": False,
        "gpu_allowed": False,
    }

    task = contract["task_world"]
    assert task["lag_grid_steps"] == [16, 32, 64, 128]
    assert task["recent_window_steps"] == 8
    assert task["history_reset"].startswith("fresh SparkBrain")
    assert task["cross_history_state"] is False

    comparator = contract["formal_comparator"]
    expected_reservoir = ReservoirConfig()
    assert comparator["family"] == "deterministic_sparse_contractive_tanh_reservoir"
    assert comparator["state_dimension"] == expected_reservoir.state_dim == 64
    assert comparator["fan_in"] == expected_reservoir.fan_in == 8
    assert comparator["reservoir_seed"] == expected_reservoir.seed == 90917
    assert comparator["recurrent_training"] is False
    assert comparator["cross_history_state"] is False
    reservoir = DeterministicReservoir(expected_reservoir)
    assert all(abs(value - 0.90) <= 1e-12 for value in reservoir.recurrent_row_l1_sums)

    world = PD01WorldConfig()
    dev_inputs = build_pd01_inputs("DEV", world)
    test_inputs = build_pd01_inputs("TEST", world)
    test_targets = build_pd01_targets("TEST", world)
    inventory = contract["inventory"]
    assert len(dev_inputs) == inventory["dev_histories"] == 512
    assert len(test_inputs) == inventory["test_histories"] == 1024
    assert sum(len(row.observations) for row in dev_inputs) == inventory["dev_observations"]
    assert sum(len(row.observations) for row in test_inputs) == inventory["test_observations"]
    assert len(test_targets) == inventory["test_target_rows"] == 1024
    assert inventory["test_raw_prediction_rows"] == 2 * len(test_inputs) == 2048
    assert {row.history_id for row in test_inputs} == {row.history_id for row in test_targets}

    matching = {}
    for row in test_inputs:
        matching.setdefault((row.base_world_id, row.lag), []).append(row)
    assert all(len(rows) == 2 for rows in matching.values())
    assert all(rows[0].observations[1:] == rows[1].observations[1:] for rows in matching.values())

    scoring = contract["primary_scoring"]
    assert scoring["primary_lags"] == [64, 128]
    assert scoring["bootstrap_resamples"] == 10_000
    assert scoring["bootstrap_seed"] == 19_901
    assert "effect_ci95_lower >= 0.10" in scoring["pass"]
    assert "effect_ci95_upper <= 0.05" in scoring["fail_reduced"]

    resource = contract["resource_matching"]
    assert resource["formal_contender_count"] == 2
    assert resource["candidate_feature_dimension"] == 64
    assert resource["comparator_state_dimension"] == 64
    assert resource["readout_parameter_count_each"] == 65
    assert resource["gpu"] is False
    assert resource["network"] is False

    gate = contract["review_gate"]
    assert gate["required_status"] == "PD01_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW"
    assert gate["ordinary_ci_same_head_required"] is True
    assert gate["dedicated_prestart_same_head_required"] is True
    assert gate["fresh_analyst_authority_required_before_identity_or_started"] is True

    print("PD0.1 formal contract: READY_FOR_ANALYST_REVIEW")


if __name__ == "__main__":
    main()

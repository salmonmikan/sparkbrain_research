#!/usr/bin/env python3
"""Fail-closed readiness checks for the PD0.1 pre-formal package."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "research" / "pd01" / "preformal_contract.json"
EXPECTED_ANALYST = "b009f497e65cddf1dd93cd4edc50f874c159ccd7"
EXPECTED_BASE = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
EXPECTED_BLOCKED = {
    "task_world_subset",
    "official_input_universe",
    "official_history_construction",
    "official_history_order_field",
    "lag_grid",
    "comparator_configuration",
    "representation_binding",
    "scoring_metrics",
    "effect_contrast",
    "no_effect_criterion",
    "inconclusive_criterion",
    "success_criterion",
    "threshold_or_equivalence_rule",
    "formal_contender_count",
    "resource_cost_budget",
    "runtime_version",
    "package_versions",
    "official_raw_cardinality",
}


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["status"] == "PREFORMAL_REVIEW_ONLY"
    assert contract["analyst_authority"] == EXPECTED_ANALYST
    assert contract["base_main"] == EXPECTED_BASE
    assert contract["formal_identity"] is None
    assert contract["formal_identity_reserved"] is False
    assert contract["started_allowed"] is False
    assert contract["official_data_access_allowed"] is False
    assert contract["official_target_access_allowed"] is False
    assert contract["one_way_execution_allowed"] is False
    assert contract["learned_recurrent_training_allowed"] is False

    candidate = contract["preformal_candidate"]
    assert candidate["implementation_count"] == 1
    assert candidate["family"] == "deterministic_exponential_fading_memory"
    assert candidate["fit_tune_select"] is False
    assert candidate["trainable_parameters"] == 0
    assert candidate["formal_configuration"] == "UNRESOLVED_BY_ANALYST"

    integrity = contract["prospective_integrity"]
    assert integrity["target_free_history_and_inventory"] is True
    assert integrity["raw_before_score_required"] is True
    assert integrity["preserve_before_targets_required"] is True
    assert integrity["scorability_gate_required_before_official_access"] is True
    assert integrity["terminal_c19_r2_tuning_forbidden"] is True

    blocked = contract["blocked_fields"]
    assert set(blocked) == EXPECTED_BLOCKED
    assert set(blocked.values()) == {"UNRESOLVED_BY_ANALYST"}

    dev = contract["dev_fixture"]
    assert dev["scope"] == "SYNTHETIC_NON_SCIENTIFIC_ONLY"
    assert dev["promotion_to_formal_protocol_forbidden"] is True

    print("PD0.1 pre-formal contract: READY_FOR_ANALYST_REVIEW")


if __name__ == "__main__":
    main()

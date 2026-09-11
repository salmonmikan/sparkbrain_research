from __future__ import annotations

import json

from sparkbrain.v061_a01.mechanism_discrimination import (
    run_a01_mechanism_discrimination,
)


def _result() -> dict[str, object]:
    return run_a01_mechanism_discrimination(source_sha="test-source-sha")


def test_a01_p1_mechanism_discrimination_passes_all_registered_trials() -> None:
    result = _result()
    p1 = result["p1"]
    assert p1["verdict"] == "SUPPORTED"
    assert all(row["accepted"] for row in p1["trials"])
    assert p1["lineage_swap_passed"] is True
    assert p1["absence_leakage_detected"] is False
    assert p1["replay_leakage_detected"] is False
    assert p1["contradiction_correction"]["existing_support_corrected"] is True


def test_a01_p2_changes_support_and_future_shared_root_competition() -> None:
    result = _result()
    p2 = result["p2"]
    assert p2["verdict"] == "SUPPORTED"
    assert p2["arm_a"]["base_temporal_hash"] == p2["arm_b"]["base_temporal_hash"]
    assert p2["arm_a"]["causal_support_hash"] != p2["arm_b"]["causal_support_hash"]
    assert p2["arm_a"]["selected_lineage"] == "lineage-a"
    assert p2["arm_b"]["selected_lineage"] == "lineage-b"
    assert p2["future_competition_changed"] is True
    assert p2["only_final_reentry_changed"] is False


def test_a01_p3_separates_persistent_carrier_from_transient_router() -> None:
    result = _result()
    p3 = result["p3"]
    assert p3["verdict"] == "SUPPORTED"
    assert p3["valid_state_partition"] is True
    assert p3["undeclared_state_changes_detected"] is False
    assert p3["actual_carrier_locus"] == "L.local-transition.a01-causal-support"
    assert p3["transient_router_locus"] == "R.transient-return-address"
    assert p3["field_carrier_observed"] is False
    assert p3["crosses"]["L_only_post_learning"]["assessment"][
        "local_transition_carries_competition"
    ]
    assert not p3["crosses"]["F_only_post_learning"]["assessment"][
        "field_state_independently_carries_competition"
    ]
    assert not p3["crosses"]["C_only_post_learning"]["assessment"][
        "consistency_independently_reaches_competition"
    ]
    assert p3["crosses"]["R_only_attribution_episode"]["assessment"][
        "transient_return_address_independently_carries_competition"
    ]


def test_a01_p4_preserves_initial_plurality_and_uses_external_evidence_later() -> None:
    result = _result()
    p4 = result["p4"]
    assert p4["verdict"] == "SUPPORTED"
    assert p4["forced_early_winner_take_all"] is False
    assert all(row["accepted"] for row in p4["trials"])
    assert all(row["co_maximal_cardinality_trace"][0] == 2 for row in p4["trials"])


def test_a01_p5_reduces_to_minimal_explicit_local_support_memory() -> None:
    result = _result()
    p5 = result["p5"]
    assert p5["verdict"] == (
        "behaviorally-and-dynamically-explicit-memory-equivalent"
    )
    assert p5["assessment"]["required_challenge_coverage_passed"] is True
    assert p5["assessment"]["endpoint_behavior_matches"] is True
    assert p5["assessment"]["temporal_state_signatures_match"] is True
    assert p5["assessment"]["baseline_minimality_established"] is True
    assert p5["assessment"]["baseline_not_larger_than_candidate"] is True
    assert p5["assessment"]["baseline_not_more_lookup_privileged"] is True
    assert p5["assessment"]["candidate_reduced_to_explicit_predictor"] is True
    assert p5["assessment"]["accepted_as_emergent_field_organization"] is False


def test_a01_discrimination_result_is_serializable_and_records_fixed_guards() -> None:
    result = _result()
    assert result["candidate_003_touched"] is False
    assert result["threshold_tuning_performed"] is False
    assert result["forbidden_privilege_used"] is False
    assert result["summary"]["absence_replay_leakage"] is False
    assert result["result_digest"]
    json.dumps(result, allow_nan=False, sort_keys=True)

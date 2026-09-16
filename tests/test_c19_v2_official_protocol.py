from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sparkbrain.v03_external_validation.official_protocol import (
    ADAPTER_CONTRACT_ID,
    BASELINES,
    INPUTS,
    OFFICIAL_SEEDS,
    PLANNED_IDENTITY,
    PRIMARY_CONDITION,
    PROTOCOL_ID,
    READINESS_ANCHOR,
    REFERENCE_CONDITION,
    expected_baseline_rows,
    expected_condition_rows,
    load_and_validate_protocol,
)

ROOT = Path(__file__).parents[1]
PROTOCOL_PATH = ROOT / "artifacts/v03/c19_external_validation/v2/official_protocol.json"
BINDING_PATH = ROOT / "artifacts/v03/c19_external_validation/v2/official_protocol_binding.json"


def protocol() -> dict[str, object]:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def test_protocol_is_prestart_and_binds_exact_readiness_anchor() -> None:
    value = protocol()
    assert value["protocol_id"] == PROTOCOL_ID
    assert value["adapter_contract_id"] == ADAPTER_CONTRACT_ID
    assert value["planned_official_identity"] == PLANNED_IDENTITY
    assert value["official_execution_allowed"] is False
    readiness = value["readiness_authority"]
    assert isinstance(readiness, dict)
    assert readiness["commit"] == READINESS_ANCHOR
    assert readiness["mutation_allowed"] is False
    metadata = value["belief_r_metadata_pin"]
    assert isinstance(metadata, dict)
    assert metadata["cache_content_accessed_during_protocolization"] is False
    assert metadata["cache_verified_during_protocolization"] is False
    assert metadata["examples_read_during_protocolization"] is False


def test_exact_30_plus_25_row_inventory_is_frozen() -> None:
    value = protocol()
    condition_rows = expected_condition_rows()
    baseline_rows = expected_baseline_rows()
    assert len(condition_rows) == 30
    assert len(baseline_rows) == 25
    assert value["row_inventory"] == [*condition_rows, *baseline_rows]
    matrix = value["condition_matrix"]
    assert isinstance(matrix, dict)
    assert matrix["inputs"] == list(INPUTS)
    assert matrix["official_seeds"] == list(OFFICIAL_SEEDS)
    baseline_matrix = value["baseline_matrix"]
    assert isinstance(baseline_matrix, dict)
    assert baseline_matrix["baseline_kinds"] == list(BASELINES)


def test_primary_discriminator_and_result_triggers_are_prospective() -> None:
    value = protocol()
    discriminator = value["primary_discriminator"]
    assert isinstance(discriminator, dict)
    assert discriminator["primary_condition"] == PRIMARY_CONDITION
    assert discriminator["reference_condition"] == REFERENCE_CONDITION
    assert discriminator["primary_metric"] == "BREU"
    classes = value["result_classification"]
    assert isinstance(classes, dict)
    assert classes["PASS"]["trigger"].endswith("lower_bound > 0")
    assert classes["FAIL"]["trigger"].endswith("upper_bound <= 0")
    assert classes["INCONCLUSIVE"]["trigger"].endswith("contains 0")
    assert "INVALID_EVIDENCE" in classes


def test_raw_schema_is_target_blind_and_raw_is_preserved_before_score() -> None:
    value = protocol()
    raw = value["raw_prediction_schema"]
    assert isinstance(raw, dict)
    assert raw["target_blind"] is True
    forbidden = set(raw["forbidden_fields"])
    assert {"ground_truth", "truth", "target", "label", "answer", "correct"} <= forbidden
    sequence = value["official_access_sequence_after_future_admission"]
    preserve = sequence.index("hash_and_preserve_raw_predictions_before_any_scoring")
    score = sequence.index("score_only_from_preserved_raw_predictions_plus_evaluator_targets")
    assert preserve < score


def test_started_precedes_future_cache_verification_and_retry_is_forbidden() -> None:
    value = protocol()
    sequence = value["official_access_sequence_after_future_admission"]
    admission = sequence.index("fresh_evidence_analyst_execution_admission")
    started = sequence.index("create_STARTED_control_ref_bound_to_exact_protocol_package")
    verify = sequence.index("verify_local_official_cache_hash_size_header_row_and_pair_counts")
    assert admission < started < verify
    integrity = value["one_way_integrity"]
    assert isinstance(integrity, dict)
    assert integrity["retry_after_started"] is False
    assert integrity["failure_after_started_consumes_identity"] is True


def test_baseline_winner_claim_requires_all_registered_matching_dimensions() -> None:
    value = protocol()
    matching = value["baseline_resource_matching"]
    assert isinstance(matching, dict)
    assert matching["required_dimensions"] == [
        "data_match",
        "optimization_match",
        "parameter_match",
        "compute_match",
    ]
    assert matching["parameter_count_relative_tolerance"] == 0.02
    assert matching["optimization_update_relative_tolerance"] == 0.05
    assert matching["analytical_training_plus_inference_ops_relative_tolerance"] == 0.05
    assert matching["unmatched_baseline_role"] == "descriptive_only_no_superiority_claim"


def test_official_protocol_package_binding_matches_tracked_blobs() -> None:
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    assert binding["protocol_id"] == PROTOCOL_ID
    assert binding["planned_official_identity"] == PLANNED_IDENTITY
    assert binding["readiness_anchor_commit"] == READINESS_ANCHOR
    assert binding["future_execution_admission_required"] is True
    assert binding["stop_when_reviewable"] is True
    for record in [*binding["bound_files"], *binding["immutable_readiness_files"]]:
        assert git_blob_sha1(ROOT / record["path"]) == record["git_blob_sha1"]
    assert set(binding["official_data_access"].values()) == {False}
    assert set(binding["one_way_state"].values()) == {False}


def test_source_only_validator_accepts_exact_protocol() -> None:
    summary = load_and_validate_protocol(PROTOCOL_PATH)
    assert summary == {
        "protocol_id": PROTOCOL_ID,
        "planned_official_identity": PLANNED_IDENTITY,
        "readiness_anchor": READINESS_ANCHOR,
        "condition_rows": 30,
        "baseline_rows": 25,
        "total_rows": 55,
        "official_data_access": False,
        "official_execution_allowed": False,
        "status": "prestart_protocol_checks_pass",
    }

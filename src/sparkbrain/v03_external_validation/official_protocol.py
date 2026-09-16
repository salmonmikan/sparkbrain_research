"""Source-only validation for the C19-v2 official execution protocol package.

This module validates preregistered execution semantics without reading or loading
official Belief-R examples.  It is intentionally incapable of execution.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

PROTOCOL_ID = "c19-external-v2-official-protocol-v1"
READINESS_PROTOCOL_ID = "c19-external-v2"
ADAPTER_CONTRACT_ID = "c19-belief-r-truth-free-symbolic-adapter-v1"
PLANNED_IDENTITY = "c19-external-v2-official-v1"
READINESS_ANCHOR = "7ede1bfb41285ec0107136b4f6abd5e893adcacf"

INPUTS = (
    "I0_whole_hash",
    "I1_local_compositional",
    "I2_truth_free_symbolic_surface",
)
GATES = ("G0_probability_margin", "G1_coalition")
ENTITY = "E0_global"
OFFICIAL_SEEDS = (15901, 15902, 15903, 15904, 15905)
BASELINES = (
    "direct_stateless",
    "explicit_state_probabilistic",
    "modular_rim_like",
    "recurrent",
    "transformer",
)
PRIMARY_CONDITION = "I2_truth_free_symbolic_surface/G1_coalition/E0_global"
REFERENCE_CONDITION = "I1_local_compositional/G1_coalition/E0_global"
SECONDARY_REFERENCE_CONDITION = "I0_whole_hash/G1_coalition/E0_global"


def expected_condition_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for input_track in INPUTS:
        for gate in GATES:
            for seed in OFFICIAL_SEEDS:
                condition_id = f"{input_track}/{gate}/{ENTITY}"
                rows.append(
                    {
                        "row_id": (
                            f"c19:{input_track}:{gate}:{ENTITY}:seed-{seed}"
                        ),
                        "row_kind": "c19_condition",
                        "condition_id": condition_id,
                        "input_track": input_track,
                        "gate": gate,
                        "entity": ENTITY,
                        "seed": seed,
                    }
                )
    return rows


def expected_baseline_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for baseline_kind in BASELINES:
        for seed in OFFICIAL_SEEDS:
            rows.append(
                {
                    "row_id": f"baseline:{baseline_kind}:seed-{seed}",
                    "row_kind": "baseline",
                    "baseline_kind": baseline_kind,
                    "seed": seed,
                }
            )
    return rows


def expected_row_inventory() -> list[dict[str, object]]:
    return [*expected_condition_rows(), *expected_baseline_rows()]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _require_exact_keys(
    value: Mapping[str, Any],
    expected: set[str],
    name: str,
) -> None:
    if set(value) != expected:
        raise ValueError(f"{name} keys differ from the frozen contract")


def validate_protocol(protocol: Mapping[str, Any]) -> dict[str, object]:
    _require(protocol["schema_version"] == "1", "unexpected schema version")
    _require(protocol["protocol_id"] == PROTOCOL_ID, "unexpected protocol id")
    _require(
        protocol["readiness_protocol_id"] == READINESS_PROTOCOL_ID,
        "readiness protocol id drift",
    )
    _require(
        protocol["adapter_contract_id"] == ADAPTER_CONTRACT_ID,
        "adapter contract id drift",
    )
    _require(
        protocol["planned_official_identity"] == PLANNED_IDENTITY,
        "planned identity drift",
    )
    _require(
        protocol["status"] == "prestart_protocolized_not_execution_admitted",
        "protocol status must remain pre-START",
    )
    _require(
        protocol["official_execution_allowed"] is False,
        "protocolization must not enable official execution",
    )

    readiness = protocol["readiness_authority"]
    _require(readiness["commit"] == READINESS_ANCHOR, "readiness anchor drift")
    _require(
        readiness["readiness_package_binding_blob"]
        == "d2dbfb32ba6b3babec8d7891d18c3e30f235a3cf",
        "readiness package blob drift",
    )
    _require(
        readiness["readiness_preregistration_blob"]
        == "0921f92c9cc29ac68f13972e24117870d159fc65",
        "readiness preregistration blob drift",
    )
    _require(
        readiness["truth_free_adapter_blob"]
        == "3153fcb61d5872e93d22f30f0f1f808f856bfaeb",
        "adapter blob drift",
    )
    _require(readiness["mutation_allowed"] is False, "readiness object must be immutable")

    belief_r = protocol["belief_r_metadata_pin"]
    expected_metadata = {
        "repository_id": "CAiRE/belief_r",
        "revision": "3719f5804c63318037465fecf298a7fd78d99121",
        "spec_sha256": (
            "ed092dd97a176813f011cdf007d4e34a0b9bcc7c855c22983a31ff82e7b0d63c"
        ),
        "expected_cache_sha256": (
            "b584c18328965cf3eb3d36f2f9ef145c1e15c9bf57bba084982ba18df1fa4153"
        ),
        "expected_size_bytes": 2230828,
        "expected_rows": 3656,
        "expected_pairs": 1744,
        "expected_update_pairs": 1074,
        "cache_content_accessed_during_protocolization": False,
        "cache_verified_during_protocolization": False,
        "examples_read_during_protocolization": False,
    }
    _require(belief_r == expected_metadata, "Belief-R metadata/access boundary drift")

    matrix = protocol["condition_matrix"]
    _require(matrix["inputs"] == list(INPUTS), "input matrix drift")
    _require(matrix["gates"] == list(GATES), "gate matrix drift")
    _require(matrix["entities"] == [ENTITY], "entity matrix drift")
    _require(matrix["official_seeds"] == list(OFFICIAL_SEEDS), "seed matrix drift")

    baseline_matrix = protocol["baseline_matrix"]
    _require(
        baseline_matrix["baseline_kinds"] == list(BASELINES),
        "baseline inventory drift",
    )
    _require(
        baseline_matrix["official_seeds"] == list(OFFICIAL_SEEDS),
        "baseline seed matrix drift",
    )

    expected_rows = expected_row_inventory()
    _require(protocol["row_inventory"] == expected_rows, "55-row inventory drift")
    _require(len(expected_rows) == 55, "row count contract drift")

    discriminator = protocol["primary_discriminator"]
    _require(
        discriminator["primary_condition"] == PRIMARY_CONDITION,
        "primary condition drift",
    )
    _require(
        discriminator["reference_condition"] == REFERENCE_CONDITION,
        "reference condition drift",
    )
    _require(
        discriminator["secondary_reference_condition"] == SECONDARY_REFERENCE_CONDITION,
        "secondary reference drift",
    )
    _require(discriminator["primary_metric"] == "BREU", "primary metric drift")
    _require(
        discriminator["claim_boundary"]
        == "truth_free_surface_structural_representation_gain_only",
        "claim boundary drift",
    )

    metrics = protocol["metrics"]
    _require(metrics["BU_Acc"] == {"slice": "update", "expected_pairs": 1074}, "BU drift")
    _require(
        metrics["BM_Acc"] == {"slice": "maintain", "expected_pairs": 670},
        "BM drift",
    )
    _require(
        metrics["BREU"]
        == {"formula": "(BU_Acc + BM_Acc) / 2", "primary": True},
        "BREU drift",
    )

    paired = protocol["paired_statistics"]
    _require(
        paired["method"] == "paired_official_pair_bootstrap",
        "paired method drift",
    )
    _require(paired["resamples"] == 10000, "bootstrap resample drift")
    _require(paired["bootstrap_seed"] == 19901, "bootstrap seed drift")
    _require(paired["confidence_level"] == 0.95, "confidence level drift")
    _require(
        paired["primary_contrast"]
        == "primary_condition_minus_reference_condition",
        "primary contrast drift",
    )
    _require(
        paired["primary_contrast_only_controls_result_class"] is True,
        "result class must use only the frozen primary contrast",
    )

    classes = protocol["result_classification"]
    _require(set(classes) == {"PASS", "FAIL", "INCONCLUSIVE", "INVALID_EVIDENCE"}, "classes drift")
    _require(
        classes["PASS"]["trigger"]
        == "primary BREU paired-bootstrap 95% CI lower_bound > 0",
        "PASS trigger drift",
    )
    _require(
        classes["FAIL"]["trigger"]
        == "primary BREU paired-bootstrap 95% CI upper_bound <= 0",
        "FAIL trigger drift",
    )
    _require(
        classes["INCONCLUSIVE"]["trigger"]
        == "primary BREU paired-bootstrap 95% CI contains 0",
        "INCONCLUSIVE trigger drift",
    )

    matching = protocol["baseline_resource_matching"]
    _require(
        matching["required_dimensions"]
        == ["data_match", "optimization_match", "parameter_match", "compute_match"],
        "matching dimensions drift",
    )
    _require(matching["same_official_pairs_required"] == 1744, "baseline pair count drift")
    _require(
        matching["same_target_blind_information_boundary_required"] is True,
        "baseline information boundary must match",
    )
    _require(matching["parameter_count_relative_tolerance"] == 0.02, "parameter tolerance drift")
    _require(
        matching["optimization_update_relative_tolerance"] == 0.05,
        "optimization tolerance drift",
    )
    _require(
        matching["analytical_training_plus_inference_ops_relative_tolerance"] == 0.05,
        "compute tolerance drift",
    )
    _require(
        matching["unmatched_baseline_role"] == "descriptive_only_no_superiority_claim",
        "unmatched baseline claim boundary drift",
    )

    sequence = protocol["official_access_sequence_after_future_admission"]
    _require(
        sequence.index("fresh_evidence_analyst_execution_admission")
        < sequence.index("create_STARTED_control_ref_bound_to_exact_protocol_package")
        < sequence.index("verify_local_official_cache_hash_size_header_row_and_pair_counts"),
        "execution admission/STARTED/cache order drift",
    )
    _require(
        sequence.index("hash_and_preserve_raw_predictions_before_any_scoring")
        < sequence.index("score_only_from_preserved_raw_predictions_plus_evaluator_targets"),
        "raw-before-score order drift",
    )

    integrity = protocol["one_way_integrity"]
    _require(integrity["single_use_identity"] is True, "identity must be single-use")
    _require(
        integrity["started_required_before_cache_verification"] is True,
        "STARTED order drift",
    )
    _require(integrity["retry_after_started"] is False, "retry after STARTED is forbidden")
    _require(
        integrity["failure_after_started_consumes_identity"] is True,
        "post-START failure must consume identity",
    )
    _require(integrity["raw_before_score"] is True, "raw-before-score required")
    _require(integrity["no_clobber"] is True, "no-clobber required")

    runner = protocol["runner_contract"]
    _require(
        (
            runner["c19_condition_rows"],
            runner["baseline_rows"],
            runner["total_rows"],
            runner["official_pairs_per_row"],
        )
        == (30, 25, 55, 1744),
        "runner inventory drift",
    )
    _require(runner["model_execution_network_allowed"] is False, "network must be blocked")
    _require(runner["official_fit_tune_select_allowed"] is False, "official tuning forbidden")
    _require(runner["all_rows_required"] is True, "all rows are mandatory")

    raw = protocol["raw_prediction_schema"]
    _require(raw["target_blind"] is True, "raw predictions must be target-blind")
    forbidden = set(raw["forbidden_fields"])
    _require(
        {"ground_truth", "truth", "target", "label", "answer", "correct"}.issubset(forbidden),
        "raw target-field prohibition incomplete",
    )
    _require(raw["official_text_committed"] is False, "official text must not be committed")

    expected_artifact_order = [
        "acquisition_manifest",
        "run_manifest",
        "raw_predictions",
        "raw_manifest",
        "scored_predictions",
        "metrics_by_row",
        "paired_statistics",
        "baseline_matching",
        "failure_examples",
        "report",
    ]
    _require(protocol["artifact_order"] == expected_artifact_order, "artifact order drift")

    admission = protocol["admission_boundary"]
    _require(
        admission["fresh_evidence_analyst_execution_admission_required"] is True,
        "fresh execution admission required",
    )
    _require(
        admission["official_data_access_before_execution_admission"] is False,
        "official data access remains forbidden",
    )
    _require(
        admission["started_before_execution_admission"] is False,
        "STARTED remains forbidden",
    )
    _require(
        admission["workflow_dispatch_before_execution_admission"] is False,
        "workflow dispatch remains forbidden",
    )
    _require(
        admission["identity_consumption_before_execution_admission"] is False,
        "identity consumption remains forbidden",
    )
    _require(
        admission["stop_when_exact_protocol_package_is_reviewable"] is True,
        "reviewable package is the mandatory stop boundary",
    )

    return {
        "protocol_id": PROTOCOL_ID,
        "planned_official_identity": PLANNED_IDENTITY,
        "readiness_anchor": READINESS_ANCHOR,
        "condition_rows": len(expected_condition_rows()),
        "baseline_rows": len(expected_baseline_rows()),
        "total_rows": len(expected_rows),
        "official_data_access": False,
        "official_execution_allowed": False,
        "status": "prestart_protocol_checks_pass",
    }


def load_and_validate_protocol(path: Path) -> dict[str, object]:
    protocol = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(protocol, Mapping):
        raise ValueError("protocol must be a mapping")
    return validate_protocol(protocol)

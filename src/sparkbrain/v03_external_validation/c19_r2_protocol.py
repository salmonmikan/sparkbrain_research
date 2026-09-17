"""Prospectively fixed pre-formal contract for C19-R2.

R2 is a scientifically distinct representation-matched finite-state/state-tracker
reduction of the narrow immutable C19-v4 I2 result. This module contains no
formal run identity and cannot authorize execution.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from sparkbrain.v03_external_validation.official_protocol_v4 import (
    EXPECTED_MAINTAIN_PAIRS,
    EXPECTED_PAIRS,
    EXPECTED_UPDATE_PAIRS,
    OFFICIAL_PYTHON_IMPLEMENTATION,
    OFFICIAL_PYTHON_VERSION,
    OFFICIAL_SEEDS,
)

SPEC_ID = "c19-r2-fsa-state-tracker-spec-v1"
PROTOCOL_ID = "c19-r2-fsa-state-tracker-protocol-v1"
PACKAGE_ID = "c19-r2-fsa-state-tracker-preformal-package-v1"
PARENT_V4_PACKAGE_COMMIT = "74bfe6b4a39758656f291baaa3f16236e3e71964"
V4_PRESERVE_COMMIT = "d8fcc5216ff24940836972816cb0ec8f11e4ba06"
V4_EVIDENCE_COMMIT = "a0f83318356ced1c84863737803080d0dc69d208"
V4_RAW_SHA256 = "692f8a5dba48f604eb1f5518a8545b80da01e1a00a9e2d2b6b1c0567355d65af"
V4_PRIMARY_CONDITION = "I2_truth_free_symbolic_surface/G1_coalition/E0_global"
INPUT_TRACK = "I2_truth_free_symbolic_surface"
ROW_KIND = "c19_r2_reduction"
MECHANISM_ID = "same-i2-seven-state-majority-hysteresis-tracker-v1"
PROJECTION_SALT = "c19-readout-v1"
CHOICES = ("a", "b", "c")
STATE_ALPHABET = (
    "RESET",
    "A_WEAK",
    "A_STRONG",
    "B_WEAK",
    "B_STRONG",
    "C_WEAK",
    "C_STRONG",
)
MAJORITY_THRESHOLD = 0.5

BOOTSTRAP_SEED = 19901
BOOTSTRAP_RESAMPLES = 10_000
PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE = EXPECTED_PAIRS
BOOTSTRAP_LOWER_P = 0.025
BOOTSTRAP_UPPER_P = 0.975
PRIMARY_BOOTSTRAP_CLUSTER_KEY = "atomic_idx"

CONFIG_PATH = Path("configs/external_validation/c19_r2_fsa_state_tracker.json")


def expected_r2_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": f"c19-r2:{MECHANISM_ID}:seed-{seed}",
            "row_kind": ROW_KIND,
            "mechanism_id": MECHANISM_ID,
            "input_track": INPUT_TRACK,
            "seed": seed,
        }
        for seed in OFFICIAL_SEEDS
    ]


def validate_contract(value: Mapping[str, Any]) -> dict[str, object]:
    if value.get("schema_version") != "1":
        raise ValueError("R2 schema version drift")
    if value.get("spec_id") != SPEC_ID or value.get("protocol_id") != PROTOCOL_ID:
        raise ValueError("R2 spec/protocol id drift")
    if value.get("formal_identity") is not None:
        raise ValueError("R2 formal identity must remain unreserved pre-review")
    if value.get("status") != "preformal_specification_only":
        raise ValueError("R2 must remain pre-formal in this handoff")
    if value.get("official_execution_allowed") is not False:
        raise ValueError("R2 execution is not authorized")

    source = value.get("source_binding")
    expected_source = {
        "parent_v4_package_commit": PARENT_V4_PACKAGE_COMMIT,
        "v4_preserve_commit": V4_PRESERVE_COMMIT,
        "v4_evidence_commit": V4_EVIDENCE_COMMIT,
        "v4_raw_sha256": V4_RAW_SHA256,
        "implementation_binding_blob": "223642c732563549cecd9fc977504b5db76c5557",
        "truth_free_adapter_blob": "3153fcb61d5872e93d22f30f0f1f808f856bfaeb",
        "v4_protocol_blob": "88e63e0bde27fcca3202173982a982580eb49700",
        "v4_scoring_blob": "55ca473f954b405579e62d4bfbfdc762a974e036",
        "v4_execution_blob": "ddb356ef8057319872b728310c1c4b780b401a16",
        "preserver_blob": "fe288f617d323620d3bda519f9300f60e73c0f8d",
    }
    if not isinstance(source, Mapping) or dict(source) != expected_source:
        raise ValueError("R2 exact source/evidence binding drift")

    inputs = value.get("input_binding")
    if not isinstance(inputs, Mapping):
        raise ValueError("R2 input binding missing")
    expected_inputs = {
        "expected_pairs": EXPECTED_PAIRS,
        "expected_update_pairs": EXPECTED_UPDATE_PAIRS,
        "expected_maintain_pairs": EXPECTED_MAINTAIN_PAIRS,
        "representation": INPUT_TRACK,
        "visible_steps_per_pair": [0, 1],
        "source_indices_per_pair": [0, 1],
        "target_use_before_raw_preservation": False,
    }
    if dict(inputs) != expected_inputs:
        raise ValueError("R2 exact input binding drift")

    mechanism = value.get("mechanism")
    if not isinstance(mechanism, Mapping):
        raise ValueError("R2 mechanism missing")
    expected_mechanism = {
        "family": "representation_matched_explicit_finite_state_tracker",
        "state_alphabet": list(STATE_ALPHABET),
        "reset_state": "RESET",
        "reset_scope": "every_pair",
        "cross_pair_state": False,
        "projection_salt": PROJECTION_SALT,
        "observation": {
            "leader": "deterministic_top_choice_lexical_tie_break",
            "strength": "top_probability_gte_0.5",
            "majority_threshold": MAJORITY_THRESHOLD,
        },
        "transition": {
            "same_leader": "same_choice_strong_if_prior_or_current_strong_else_weak",
            "different_current_strong": "switch_to_current_strong",
            "different_prior_strong_current_weak": "retain_prior_choice_but_decay_to_weak",
            "different_both_weak": "switch_to_current_weak",
        },
        "readout": "choice_component_of_state_after_visible_step_1",
        "history_privilege": "only_current_finite_state_no_raw_history_lookup",
        "external_lookup": False,
        "fit_tune_select": False,
        "trainable_parameters": 0,
        "official_seeds": list(OFFICIAL_SEEDS),
    }
    if dict(mechanism) != expected_mechanism:
        raise ValueError("R2 finite-state mechanism drift")

    resources = value.get("resource_contract")
    expected_resources = {
        "states_including_reset": len(STATE_ALPHABET),
        "persistent_state_per_pair": "one_of_seven_enumerated_states",
        "cross_pair_memory": False,
        "encodings_per_pair": 2,
        "projection_passes_per_pair": 2,
        "transition_updates_per_pair": 2,
        "fit_updates": 0,
        "tune_trials": 0,
        "selection_trials": 0,
        "artificial_compute_padding": False,
        "claim_type": "reduction_sufficiency_not_compute_matched_superiority",
    }
    if not isinstance(resources, Mapping) or dict(resources) != expected_resources:
        raise ValueError("R2 resource contract drift")

    runtime = value.get("runtime_binding")
    expected_runtime = {
        "python_implementation": OFFICIAL_PYTHON_IMPLEMENTATION,
        "python_version": OFFICIAL_PYTHON_VERSION,
        "network_allowed_during_model_execution": False,
        "official_fit_tune_select_allowed": False,
        "base_model": None,
    }
    if not isinstance(runtime, Mapping) or dict(runtime) != expected_runtime:
        raise ValueError("R2 runtime binding drift")

    raw = value.get("raw_contract")
    if not isinstance(raw, Mapping):
        raise ValueError("R2 raw contract missing")
    if raw.get("rows") != len(OFFICIAL_SEEDS):
        raise ValueError("R2 raw row inventory drift")
    if raw.get("pairs_per_row") != EXPECTED_PAIRS:
        raise ValueError("R2 raw pair inventory drift")
    if raw.get("records") != len(OFFICIAL_SEEDS) * EXPECTED_PAIRS:
        raise ValueError("R2 raw record inventory drift")
    for key in (
        "raw_before_score",
        "immutable_preserve_before_targets",
        "no_clobber",
        "target_blind",
    ):
        if raw.get(key) is not True:
            raise ValueError(f"R2 raw boundary drift: {key}")
    source_map = raw.get("atomic_idx_source_map")
    expected_map = {
        "artifact": "atomic_idx_source_map.json",
        "schema_version": "1",
        "cluster_key": PRIMARY_BOOTSTRAP_CLUSTER_KEY,
        "target_free": True,
        "pair_assignment": "exactly_once",
        "preserve_with_raw_before_targets": True,
    }
    if not isinstance(source_map, Mapping) or dict(source_map) != expected_map:
        raise ValueError("R2 source-map contract drift")

    scoring = value.get("scoring_contract")
    if not isinstance(scoring, Mapping):
        raise ValueError("R2 scoring contract missing")
    expected_scoring = {
        "metric": "BREU",
        "v4_primary_condition": V4_PRIMARY_CONDITION,
        "reduction_contrast": "C19-v4 primary BREU minus R2 BREU",
        "primary_method": "paired_atomic_idx_cluster_bootstrap",
        "secondary_method": "paired_official_pair_bootstrap_sensitivity",
        "resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "confidence_level": 0.95,
        "quantile_method": "linear_type7",
        "classification": {
            "SURVIVES_FSA_REDUCTION": "primary_ci_lower_gt_0",
            "REDUCED_BY_FSA": "primary_ci_upper_lte_0",
            "INCONCLUSIVE": "primary_ci_contains_0",
            "INVALID_EVIDENCE": "integrity_or_binding_failure",
        },
    }
    if dict(scoring) != expected_scoring:
        raise ValueError("R2 scoring contract drift")

    integrity = value.get("integrity")
    expected_integrity = {
        "fresh_analyst_execution_authorization_required": True,
        "current_handoff_execution_allowed": False,
        "formal_identity_must_be_fresh_and_future": True,
        "started_no_clobber_required": True,
        "retry_after_started": False,
        "r1_transient_outputs_for_design_or_tuning": False,
        "v4_per_example_outputs_for_design_or_tuning": False,
        "preserve_then_independent_refetch_before_targets": True,
    }
    if not isinstance(integrity, Mapping) or dict(integrity) != expected_integrity:
        raise ValueError("R2 integrity contract drift")

    return {
        "spec_id": SPEC_ID,
        "protocol_id": PROTOCOL_ID,
        "formal_identity": None,
        "rows": len(expected_r2_rows()),
        "pairs_per_row": EXPECTED_PAIRS,
        "primary_cluster_key": PRIMARY_BOOTSTRAP_CLUSTER_KEY,
        "official_execution_allowed": False,
        "status": "preformal_contract_checks_pass",
    }


def load_and_validate_contract(path: Path = CONFIG_PATH) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("R2 contract must be a mapping")
    return validate_contract(value)


__all__ = [
    "BOOTSTRAP_LOWER_P",
    "BOOTSTRAP_RESAMPLES",
    "BOOTSTRAP_SEED",
    "BOOTSTRAP_UPPER_P",
    "CHOICES",
    "CONFIG_PATH",
    "EXPECTED_MAINTAIN_PAIRS",
    "EXPECTED_PAIRS",
    "EXPECTED_UPDATE_PAIRS",
    "INPUT_TRACK",
    "MAJORITY_THRESHOLD",
    "MECHANISM_ID",
    "OFFICIAL_PYTHON_IMPLEMENTATION",
    "OFFICIAL_PYTHON_VERSION",
    "OFFICIAL_SEEDS",
    "PACKAGE_ID",
    "PAIR_IID_BOOTSTRAP_DRAWS_PER_RESAMPLE",
    "PARENT_V4_PACKAGE_COMMIT",
    "PRIMARY_BOOTSTRAP_CLUSTER_KEY",
    "PROJECTION_SALT",
    "PROTOCOL_ID",
    "ROW_KIND",
    "SPEC_ID",
    "STATE_ALPHABET",
    "V4_EVIDENCE_COMMIT",
    "V4_PRESERVE_COMMIT",
    "V4_PRIMARY_CONDITION",
    "V4_RAW_SHA256",
    "expected_r2_rows",
    "load_and_validate_contract",
    "validate_contract",
]

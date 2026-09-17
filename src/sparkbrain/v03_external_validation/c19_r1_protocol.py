"""Prospectively fixed pre-START contract for C19-R1.

R1 is a fresh matched reduction object. It does not alter or rerun C19-v4.
The mechanism uses the exact I2 visible representation/readout family from the
v4 package but replaces the persistent coalition gate with a stateless,
label-free certainty arbitration over the two visible steps.
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

PROTOCOL_ID = "c19-r1-revision-authority-protocol-v1"
PLANNED_IDENTITY = "c19-r1-revision-authority-official-v1"
PACKAGE_ID = "c19-r1-revision-authority-package-v1"
PARENT_V4_PACKAGE_COMMIT = "74bfe6b4a39758656f291baaa3f16236e3e71964"
V4_PRESERVE_COMMIT = "d8fcc5216ff24940836972816cb0ec8f11e4ba06"
V4_EVIDENCE_COMMIT = "a0f83318356ced1c84863737803080d0dc69d208"
V4_RAW_SHA256 = "692f8a5dba48f604eb1f5518a8545b80da01e1a00a9e2d2b6b1c0567355d65af"
V4_PRIMARY_CONDITION = "I2_truth_free_symbolic_surface/G1_coalition/E0_global"
INPUT_TRACK = "I2_truth_free_symbolic_surface"
ROW_KIND = "c19_r1_reduction"
MECHANISM_ID = "same-i2-stateless-revision-authority-certainty-v1"

BOOTSTRAP_SEED = 19901
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_DRAWS_PER_RESAMPLE = EXPECTED_PAIRS
BOOTSTRAP_LOWER_P = 0.025
BOOTSTRAP_UPPER_P = 0.975

CONFIG_PATH = Path("configs/external_validation/c19_r1_revision_authority.json")


def expected_r1_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": f"c19-r1:{MECHANISM_ID}:seed-{seed}",
            "row_kind": ROW_KIND,
            "mechanism_id": MECHANISM_ID,
            "input_track": INPUT_TRACK,
            "seed": seed,
        }
        for seed in OFFICIAL_SEEDS
    ]


def validate_contract(value: Mapping[str, Any]) -> dict[str, object]:
    if value.get("schema_version") != "1":
        raise ValueError("R1 schema version drift")
    if value.get("protocol_id") != PROTOCOL_ID:
        raise ValueError("R1 protocol id drift")
    if value.get("planned_identity") != PLANNED_IDENTITY:
        raise ValueError("R1 identity drift")
    if value.get("status") != "prestart_specification_only":
        raise ValueError("R1 contract must remain pre-START")
    if value.get("official_execution_allowed") is not False:
        raise ValueError("R1 current handoff must not enable official execution")

    source = value.get("source_binding")
    if not isinstance(source, Mapping):
        raise ValueError("R1 source binding missing")
    exact_source = {
        "parent_package_commit": PARENT_V4_PACKAGE_COMMIT,
        "v4_preserve_commit": V4_PRESERVE_COMMIT,
        "v4_evidence_commit": V4_EVIDENCE_COMMIT,
        "v4_raw_sha256": V4_RAW_SHA256,
        "implementation_binding_blob": "223642c732563549cecd9fc977504b5db76c5557",
        "truth_free_adapter_blob": "3153fcb61d5872e93d22f30f0f1f808f856bfaeb",
        "v4_protocol_blob": "88e63e0bde27fcca3202173982a982580eb49700",
        "v4_scoring_blob": "55ca473f954b405579e62d4bfbfdc762a974e036",
    }
    if dict(source) != exact_source:
        raise ValueError("R1 exact source/evidence binding drift")

    inputs = value.get("input_binding")
    if not isinstance(inputs, Mapping):
        raise ValueError("R1 input binding missing")
    if inputs.get("expected_pairs") != EXPECTED_PAIRS:
        raise ValueError("R1 pair count drift")
    if inputs.get("expected_update_pairs") != EXPECTED_UPDATE_PAIRS:
        raise ValueError("R1 update slice drift")
    if inputs.get("expected_maintain_pairs") != EXPECTED_MAINTAIN_PAIRS:
        raise ValueError("R1 maintain slice drift")
    if inputs.get("representation") != INPUT_TRACK:
        raise ValueError("R1 must use exact I2 representation")
    if inputs.get("target_use_before_raw_preservation") is not False:
        raise ValueError("R1 target boundary drift")

    mechanism = value.get("mechanism")
    if not isinstance(mechanism, Mapping):
        raise ValueError("R1 mechanism missing")
    if mechanism.get("family") != "same_I2_label_free_stateless_revision_authority":
        raise ValueError("R1 mechanism family drift")
    if mechanism.get("persistent_state") is not False:
        raise ValueError("R1 must be stateless")
    if mechanism.get("cross_pair_state") is not False:
        raise ValueError("R1 must not keep cross-pair state")
    if mechanism.get("fit_tune_select") is not False:
        raise ValueError("R1 fitting/tuning is forbidden")
    if mechanism.get("trainable_parameters") != 0:
        raise ValueError("R1 parameter count drift")
    if mechanism.get("official_seeds") != list(OFFICIAL_SEEDS):
        raise ValueError("R1 seed inventory drift")
    certainty = mechanism.get("certainty")
    if not isinstance(certainty, Mapping):
        raise ValueError("R1 certainty rule missing")
    if certainty.get("definition") != "top1_probability_minus_top2_probability":
        raise ValueError("R1 certainty definition drift")
    if certainty.get("secondary_tie_break") != "top1_probability":
        raise ValueError("R1 certainty secondary tie break drift")
    if certainty.get("thresholds") != []:
        raise ValueError("R1 may not introduce tuned thresholds")

    runtime = value.get("runtime_binding")
    if not isinstance(runtime, Mapping):
        raise ValueError("R1 runtime binding missing")
    if runtime.get("python_implementation") != OFFICIAL_PYTHON_IMPLEMENTATION:
        raise ValueError("R1 Python implementation drift")
    if runtime.get("python_version") != OFFICIAL_PYTHON_VERSION:
        raise ValueError("R1 Python version drift")
    if runtime.get("network_allowed_during_model_execution") is not False:
        raise ValueError("R1 model execution must be network blocked")
    if runtime.get("official_fit_tune_select_allowed") is not False:
        raise ValueError("R1 official tuning is forbidden")
    if runtime.get("base_model") is not None:
        raise ValueError("R1 has no fitted/base model")

    raw = value.get("raw_contract")
    if not isinstance(raw, Mapping):
        raise ValueError("R1 raw contract missing")
    if (
        raw.get("rows"),
        raw.get("pairs_per_row"),
        raw.get("records"),
    ) != (len(OFFICIAL_SEEDS), EXPECTED_PAIRS, len(OFFICIAL_SEEDS) * EXPECTED_PAIRS):
        raise ValueError("R1 raw inventory drift")
    raw_integrity_keys = (
        "raw_before_score",
        "immutable_preserve_before_targets",
        "no_clobber",
        "target_blind",
    )
    for key in raw_integrity_keys:
        if raw.get(key) is not True:
            raise ValueError(f"R1 raw boundary drift: {key}")

    scoring = value.get("scoring_contract")
    if not isinstance(scoring, Mapping):
        raise ValueError("R1 scoring contract missing")
    if scoring.get("metric") != "BREU":
        raise ValueError("R1 metric drift")
    if scoring.get("v4_primary_condition") != V4_PRIMARY_CONDITION:
        raise ValueError("R1 v4 primary binding drift")
    if scoring.get("reduction_contrast") != "C19-v4 primary BREU minus R1 BREU":
        raise ValueError("R1 reduction contrast drift")
    bootstrap = scoring.get("bootstrap")
    if not isinstance(bootstrap, Mapping):
        raise ValueError("R1 bootstrap contract missing")
    if (
        bootstrap.get("resamples"),
        bootstrap.get("draws_per_resample"),
        bootstrap.get("seed"),
        bootstrap.get("lower_p"),
        bootstrap.get("upper_p"),
    ) != (
        BOOTSTRAP_RESAMPLES,
        BOOTSTRAP_DRAWS_PER_RESAMPLE,
        BOOTSTRAP_SEED,
        BOOTSTRAP_LOWER_P,
        BOOTSTRAP_UPPER_P,
    ):
        raise ValueError("R1 bootstrap semantics drift")

    integrity = value.get("integrity")
    if not isinstance(integrity, Mapping):
        raise ValueError("R1 integrity contract missing")
    if integrity.get("retry_after_started") is not False:
        raise ValueError("R1 post-START retry forbidden")
    if integrity.get("fresh_analyst_execution_authorization_required") is not True:
        raise ValueError("R1 needs fresh Analyst execution authority")
    if integrity.get("v4_per_example_outputs_for_design_or_tuning") is not False:
        raise ValueError("R1 must not tune from v4 per-example outputs")
    if integrity.get("current_handoff_execution_allowed") is not False:
        raise ValueError("R1 current handoff is pre-START only")

    return {
        "protocol_id": PROTOCOL_ID,
        "planned_identity": PLANNED_IDENTITY,
        "rows": len(expected_r1_rows()),
        "pairs_per_row": EXPECTED_PAIRS,
        "official_execution_allowed": False,
        "status": "prestart_contract_checks_pass",
    }


def load_and_validate_contract(path: Path = CONFIG_PATH) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("R1 contract must be a mapping")
    return validate_contract(value)


__all__ = [
    "BOOTSTRAP_DRAWS_PER_RESAMPLE",
    "BOOTSTRAP_LOWER_P",
    "BOOTSTRAP_RESAMPLES",
    "BOOTSTRAP_SEED",
    "BOOTSTRAP_UPPER_P",
    "CONFIG_PATH",
    "EXPECTED_MAINTAIN_PAIRS",
    "EXPECTED_PAIRS",
    "EXPECTED_UPDATE_PAIRS",
    "INPUT_TRACK",
    "MECHANISM_ID",
    "OFFICIAL_PYTHON_IMPLEMENTATION",
    "OFFICIAL_PYTHON_VERSION",
    "OFFICIAL_SEEDS",
    "PACKAGE_ID",
    "PARENT_V4_PACKAGE_COMMIT",
    "PLANNED_IDENTITY",
    "PROTOCOL_ID",
    "ROW_KIND",
    "V4_EVIDENCE_COMMIT",
    "V4_PRESERVE_COMMIT",
    "V4_PRIMARY_CONDITION",
    "V4_RAW_SHA256",
    "expected_r1_rows",
    "load_and_validate_contract",
    "validate_contract",
]

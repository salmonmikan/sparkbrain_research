"""Prospectively fixed C19 official-v2 execution/scoring contract.

This module does not change the inherited C19 scientific matrix. It binds the
fresh successor identity and the evaluator/bootstrap semantics fixed by the
Evidence Analyst before STARTED.
"""

from __future__ import annotations

from sparkbrain.v03_external_validation.official_protocol import (
    BASELINES,
    INPUTS,
    OFFICIAL_SEEDS,
    PRIMARY_CONDITION,
    REFERENCE_CONDITION,
    expected_baseline_rows,
    expected_condition_rows,
    expected_row_inventory,
)

PROTOCOL_ID = "c19-external-v2-official-protocol-v2"
PLANNED_IDENTITY = "c19-external-v2-official-v2"
SOURCE_BASE_COMMIT = "66c8eafe9863ed1b2455cc833a3dc498ce7721b0"
INHERITED_FROZEN_PROTOCOL_HEAD = "90c936a7abca7eba0dac1f977753503551e73368"

EXPECTED_PAIRS = 1744
EXPECTED_UPDATE_PAIRS = 1074
EXPECTED_MAINTAIN_PAIRS = 670

EVALUATOR_TARGET_FIELDS = frozenset(
    {
        "pair_index",
        "record_id_hash",
        "source_index",
        "step_index",
        "target_choice_id",
        "update_required",
    }
)
EVALUATOR_JOIN_KEY_FIELDS = (
    "pair_index",
    "record_id_hash",
    "source_index",
    "step_index",
)

BOOTSTRAP_SEED = 19901
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_DRAWS_PER_RESAMPLE = EXPECTED_PAIRS
BOOTSTRAP_CONFIDENCE_LEVEL = 0.95
BOOTSTRAP_LOWER_P = 0.025
BOOTSTRAP_UPPER_P = 0.975
OFFICIAL_PYTHON_IMPLEMENTATION = "CPython"
OFFICIAL_PYTHON_VERSION = "3.11.16"

SEED_AGGREGATION = (
    "recompute per-seed BU_Acc/BM_Acc/BREU then mean the five seed BREU values"
)
PRIMARY_CONTRAST = "primary_condition_minus_reference_condition"

__all__ = [
    "BASELINES",
    "INPUTS",
    "OFFICIAL_SEEDS",
    "PRIMARY_CONDITION",
    "REFERENCE_CONDITION",
    "expected_baseline_rows",
    "expected_condition_rows",
    "expected_row_inventory",
    "PROTOCOL_ID",
    "PLANNED_IDENTITY",
    "SOURCE_BASE_COMMIT",
    "INHERITED_FROZEN_PROTOCOL_HEAD",
    "EXPECTED_PAIRS",
    "EXPECTED_UPDATE_PAIRS",
    "EXPECTED_MAINTAIN_PAIRS",
    "EVALUATOR_TARGET_FIELDS",
    "EVALUATOR_JOIN_KEY_FIELDS",
    "BOOTSTRAP_SEED",
    "BOOTSTRAP_RESAMPLES",
    "BOOTSTRAP_DRAWS_PER_RESAMPLE",
    "BOOTSTRAP_CONFIDENCE_LEVEL",
    "BOOTSTRAP_LOWER_P",
    "BOOTSTRAP_UPPER_P",
    "OFFICIAL_PYTHON_IMPLEMENTATION",
    "OFFICIAL_PYTHON_VERSION",
    "SEED_AGGREGATION",
    "PRIMARY_CONTRAST",
]

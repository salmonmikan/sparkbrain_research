"""Runtime-closed C19 official-v3 protocol identity.

Scientific semantics are inherited unchanged from official-v2.  The new object
exists only because official-v2 was consumed by a post-START runtime dependency
failure before target-blind model execution.
"""

from __future__ import annotations

from sparkbrain.v03_external_validation.official_protocol_v2 import (
    BASELINES,
    BOOTSTRAP_CONFIDENCE_LEVEL,
    BOOTSTRAP_DRAWS_PER_RESAMPLE,
    BOOTSTRAP_LOWER_P,
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    BOOTSTRAP_UPPER_P,
    EVALUATOR_JOIN_KEY_FIELDS,
    EVALUATOR_TARGET_FIELDS,
    EXPECTED_MAINTAIN_PAIRS,
    EXPECTED_PAIRS,
    EXPECTED_UPDATE_PAIRS,
    INHERITED_FROZEN_PROTOCOL_HEAD,
    INPUTS,
    OFFICIAL_PYTHON_IMPLEMENTATION,
    OFFICIAL_PYTHON_VERSION,
    OFFICIAL_SEEDS,
    PRIMARY_CONDITION,
    PRIMARY_CONTRAST,
    REFERENCE_CONDITION,
    SEED_AGGREGATION,
    SOURCE_BASE_COMMIT,
    expected_baseline_rows,
    expected_condition_rows,
    expected_row_inventory,
)

PROTOCOL_ID = "c19-external-v2-official-protocol-v3"
PLANNED_IDENTITY = "c19-external-v2-official-v3"
PACKAGE_ID = "c19-external-v2-official-package-v3"
REQUIRED_TORCH_VERSION = "2.13.0"

__all__ = [
    "BASELINES",
    "BOOTSTRAP_CONFIDENCE_LEVEL",
    "BOOTSTRAP_DRAWS_PER_RESAMPLE",
    "BOOTSTRAP_LOWER_P",
    "BOOTSTRAP_RESAMPLES",
    "BOOTSTRAP_SEED",
    "BOOTSTRAP_UPPER_P",
    "EVALUATOR_JOIN_KEY_FIELDS",
    "EVALUATOR_TARGET_FIELDS",
    "EXPECTED_MAINTAIN_PAIRS",
    "EXPECTED_PAIRS",
    "EXPECTED_UPDATE_PAIRS",
    "INHERITED_FROZEN_PROTOCOL_HEAD",
    "INPUTS",
    "OFFICIAL_PYTHON_IMPLEMENTATION",
    "OFFICIAL_PYTHON_VERSION",
    "OFFICIAL_SEEDS",
    "PACKAGE_ID",
    "PLANNED_IDENTITY",
    "PRIMARY_CONDITION",
    "PRIMARY_CONTRAST",
    "PROTOCOL_ID",
    "REFERENCE_CONDITION",
    "REQUIRED_TORCH_VERSION",
    "SEED_AGGREGATION",
    "SOURCE_BASE_COMMIT",
    "expected_baseline_rows",
    "expected_condition_rows",
    "expected_row_inventory",
]

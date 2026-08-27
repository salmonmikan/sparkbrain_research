"""Strict, source-only contracts for C19 external validation.

The C18 dependency is represented only by a structural adapter protocol.
Keeping this module free of C18 imports prevents an invented checkpoint API
from becoming an accidental execution dependency.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

EXACT_NINE_ARTIFACTS = frozenset(
    {
        "frozen_protocol.json",
        "run_manifest.jsonl",
        "raw_predictions.jsonl",
        "attribution_rows.jsonl",
        "metrics_by_condition.json",
        "paired_statistics.json",
        "baseline_matching.json",
        "failure_examples.jsonl",
        "report.md",
    }
)
AUTONOMOUS_INPUTS = frozenset({"I0_whole_hash", "I1_local_compositional"})
ORACLE_INPUT = "I2_symbolic_oracle"
BASELINE_KINDS = frozenset(
    {
        "direct_stateless",
        "explicit_state_probabilistic",
        "recurrent",
        "transformer",
        "modular_rim_like",
    }
)


def canonical(value: object) -> str:
    return json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _exact_keys(row: Mapping[str, Any], expected: set[str], name: str) -> None:
    if set(row) != expected:
        raise ValueError(f"{name} must have exact keys {sorted(expected)}")


class C18TraceCheckpointAdapter(Protocol):
    """Boundary C18 must satisfy after its accepted public contract exists."""

    def reset(self, *, checkpoint_id: str) -> None: ...

    def step(self, observation: Mapping[str, object]) -> Mapping[str, object]: ...

    def export_trace_checkpoint(self) -> Mapping[str, object]: ...


@dataclass(frozen=True, slots=True)
class FaultAttribution:
    status: str
    dominant_component: str | None
    reason: str

    def to_dict(self) -> dict[str, str | None]:
        return {
            "status": self.status,
            "dominant_component": self.dominant_component,
            "reason": self.reason,
        }


def validate_disabled_preregistration(protocol: Mapping[str, Any]) -> None:
    _exact_keys(
        protocol,
        {
            "artifact_inventory",
            "baseline_kinds",
            "cache_hash_contract",
            "checkpoint_selection",
            "condition_matrix",
            "fresh_seed_contract",
            "official_evaluation_allowed",
            "protocol_id",
            "schema_version",
            "source_commit",
            "trace_checkpoint_contract",
        },
        "C19 preregistration",
    )
    if protocol["schema_version"] != "0.3" or protocol["protocol_id"] != "c19-external-v1":
        raise ValueError("unexpected C19 protocol identity")
    if (
        protocol["official_evaluation_allowed"] is not False
        or protocol["source_commit"] is not None
    ):
        raise ValueError("C19 source preregistration must remain disabled and unpinned")
    if set(protocol["artifact_inventory"]) != EXACT_NINE_ARTIFACTS:
        raise ValueError("C19 requires the exact-nine artifact inventory")
    if set(protocol["baseline_kinds"]) != BASELINE_KINDS:
        raise ValueError("C19 baseline inventory is incomplete")
    cache = protocol["cache_hash_contract"]
    if cache != {
        "cache_sha256": None,
        "content_tracked": False,
        "official_cache_pin_required_before_execution": True,
    }:
        raise ValueError("C19 cache hash contract is not source-only")
    matrix = protocol["condition_matrix"]
    if matrix["inputs"] != ["I0_whole_hash", "I1_local_compositional", ORACLE_INPUT]:
        raise ValueError("C19 input conditions are not frozen")
    if matrix["gates"] != ["G0_probability_margin", "G1_coalition"]:
        raise ValueError("C19 gate conditions are not frozen")
    if matrix["entities"] != ["E0_global", "E1_oracle_entity"]:
        raise ValueError("C19 entity conditions are not frozen")
    trace = protocol["trace_checkpoint_contract"]
    if trace["provider"] != "C18 accepted public contract" or trace["available"] is not False:
        raise ValueError("C19 must not fabricate a C18 trace/checkpoint API")


def validate_baseline_matching(row: Mapping[str, Any]) -> None:
    """Prevent a performance winner claim when matching is incomplete."""

    _exact_keys(
        row,
        {
            "baseline_kind",
            "checkpoint_selection_split",
            "compute_match",
            "data_match",
            "parameter_match",
            "winner_claim_allowed",
        },
        "baseline matching row",
    )
    if row["baseline_kind"] not in BASELINE_KINDS:
        raise ValueError("unknown baseline kind")
    all_matched = all(
        row[key] is True for key in ("compute_match", "data_match", "parameter_match")
    )
    if row["winner_claim_allowed"] != all_matched:
        raise ValueError("winner claims require parameter, data, and compute matching")


def validate_prediction_row(row: Mapping[str, Any]) -> None:
    _exact_keys(
        row,
        {
            "condition_id",
            "entity_count",
            "episode_id_hash",
            "fault_attribution",
            "input_track",
            "oracle_diagnostic",
            "prediction",
            "probabilities",
            "seed",
            "split",
            "step_index",
            "trace_checkpoint_hash",
            "truth",
            "work_counters",
        },
        "raw prediction row",
    )
    if row["input_track"] not in AUTONOMOUS_INPUTS | {ORACLE_INPUT}:
        raise ValueError("unknown input track")
    if row["oracle_diagnostic"] != (row["input_track"] == ORACLE_INPUT):
        raise ValueError("Oracle rows must be diagnostic-only")
    if row["split"] != "synthetic_proxy":
        raise ValueError("source-only C19 may retain only synthetic proxy rows")
    if not isinstance(row["entity_count"], int) or row["entity_count"] < 1:
        raise ValueError("entity_count must be positive")
    if not isinstance(row["probabilities"], Mapping) or not row["probabilities"]:
        raise ValueError("probabilities are required")
    values = list(row["probabilities"].values())
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise ValueError("probabilities must be numeric")
    if not math.isclose(sum(float(value) for value in values), 1.0, abs_tol=1e-9):
        raise ValueError("probabilities must sum to one")


def validate_attribution_row(row: Mapping[str, Any]) -> None:
    _exact_keys(
        row,
        {
            "available",
            "condition_id",
            "dominant_component",
            "entity_count",
            "episode_id_hash",
            "reason",
            "seed",
            "status",
        },
        "attribution row",
    )
    if row["entity_count"] == 1 and row["status"] != "inconclusive":
        raise ValueError("single-entity Belief-R attribution must remain inconclusive")
    if row["status"] == "inconclusive" and row["dominant_component"] is not None:
        raise ValueError("inconclusive attribution cannot name a dominant component")

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
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from sparkbrain.v03_integration import V03Checkpoint, V03TraceEvent, V03TraceSession

EXACT_NINE_ARTIFACT_ORDER = (
    "attribution_rows.jsonl",
    "baseline_matching.json",
    "failure_examples.jsonl",
    "frozen_protocol.json",
    "metrics_by_condition.json",
    "paired_statistics.json",
    "raw_predictions.jsonl",
    "report.md",
    "run_manifest.jsonl",
)
EXACT_NINE_ARTIFACTS = frozenset(EXACT_NINE_ARTIFACT_ORDER)
INPUT_TRACK_ORDER = ("I0_whole_hash", "I1_local_compositional", "I2_symbolic_oracle")
AUTONOMOUS_INPUTS = frozenset(INPUT_TRACK_ORDER[:2])
ORACLE_INPUT = "I2_symbolic_oracle"
GATE_ORDER = ("G0_probability_margin", "G1_coalition")
ENTITY_ORDER = ("E0_global", "E1_oracle_entity")
BASELINE_KIND_ORDER = (
    "direct_stateless",
    "explicit_state_probabilistic",
    "modular_rim_like",
    "recurrent",
    "transformer",
)
BASELINE_KINDS = frozenset(BASELINE_KIND_ORDER)


def canonical(value: object) -> str:
    return json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _exact_keys(row: Mapping[str, Any], expected: set[str], name: str) -> None:
    if set(row) != expected:
        raise ValueError(f"{name} must have exact keys {sorted(expected)}")


def _validate_condition_id(value: object, *, input_track: object | None = None) -> None:
    if not isinstance(value, str):
        raise ValueError("condition_id must be a string")
    segments = value.split("/")
    if (
        len(segments) != 3
        or segments[0] not in INPUT_TRACK_ORDER
        or segments[1] not in GATE_ORDER
        or segments[2] not in ENTITY_ORDER
    ):
        raise ValueError("condition_id must use the frozen input/gate/entity matrix")
    if input_track is not None and segments[0] != input_track:
        raise ValueError("condition_id must begin with the input track")


class C18TraceCheckpointAdapter(Protocol):
    """Boundary C18 must satisfy after its accepted public contract exists."""

    def inspect(self) -> dict[str, Any]: ...

    def record(
        self,
        kind: str,
        payload: Mapping[str, Any],
        *,
        state_delta: Mapping[str, Any],
    ) -> V03TraceEvent: ...

    def checkpoint(self, checkpoint_id: str) -> V03Checkpoint: ...

    def fork(
        self,
        checkpoint: V03Checkpoint,
        *,
        branch_id: str,
        intervention: Mapping[str, Any],
    ) -> V03TraceSession: ...


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
    if protocol["artifact_inventory"] != list(EXACT_NINE_ARTIFACT_ORDER):
        raise ValueError("C19 requires the exact-nine artifact inventory")
    if protocol["baseline_kinds"] != list(BASELINE_KIND_ORDER):
        raise ValueError("C19 baseline inventory is incomplete")
    selection = protocol["checkpoint_selection"]
    _exact_keys(
        selection,
        {"calibration_split", "official_test_fit_or_tuning", "selection_split", "status"},
        "checkpoint selection",
    )
    if selection != {
        "calibration_split": "dev",
        "official_test_fit_or_tuning": False,
        "selection_split": "dev",
        "status": "preregistered",
    }:
        raise ValueError("checkpoint selection and calibration must exclude official test")
    seeds = protocol["fresh_seed_contract"]
    required_seed_keys = {
        "official_seed_range",
        "proxy_seed_range",
        "reserved_test_seed_range",
        "split_seed",
        "bootstrap_seed",
    }
    _exact_keys(seeds, required_seed_keys, "fresh seed contract")
    groups = [
        seeds["official_seed_range"],
        seeds["proxy_seed_range"],
        seeds["reserved_test_seed_range"],
    ]
    values = [value for group in groups for value in group] + [
        seeds["split_seed"],
        seeds["bootstrap_seed"],
    ]
    expected = [5901, 5902, 5903, 5904, 5905, 6901, 6902, 6903, 6904, 6905, 8901, 8902, 7901, 9901]
    if (
        any(isinstance(value, bool) or not isinstance(value, int) for value in values)
        or values != expected
    ):
        raise ValueError("official, proxy, reserved, and split seeds must not overlap")
    cache = protocol["cache_hash_contract"]
    if cache != {
        "cache_sha256": None,
        "content_tracked": False,
        "official_cache_pin_required_before_execution": True,
    }:
        raise ValueError("C19 cache hash contract is not source-only")
    matrix = protocol["condition_matrix"]
    _exact_keys(matrix, {"inputs", "gates", "entities"}, "condition matrix")
    if matrix["inputs"] != list(INPUT_TRACK_ORDER):
        raise ValueError("C19 input conditions are not frozen")
    if matrix["gates"] != list(GATE_ORDER):
        raise ValueError("C19 gate conditions are not frozen")
    if matrix["entities"] != list(ENTITY_ORDER):
        raise ValueError("C19 entity conditions are not frozen")
    trace = protocol["trace_checkpoint_contract"]
    _exact_keys(trace, {"available", "provider", "required_methods"}, "trace contract")
    if (
        trace["provider"] != "V03TraceSession"
        or trace["available"] is not False
        or not isinstance(trace["available"], bool)
        or not isinstance(trace["required_methods"], list)
        or trace["required_methods"] != ["inspect", "record", "checkpoint", "fork"]
    ):
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
    if row["checkpoint_selection_split"] != "dev":
        raise ValueError("baseline checkpoint selection must use preregistered dev")
    _reject_nested_target_leakage(row)
    boolean_keys = ("compute_match", "data_match", "parameter_match", "winner_claim_allowed")
    if any(type(row[key]) is not bool for key in boolean_keys):
        raise ValueError("baseline matching flags must be exact booleans")
    all_matched = all(
        row[key] is True for key in ("compute_match", "data_match", "parameter_match")
    )
    if row["winner_claim_allowed"] is True and not all_matched:
        raise ValueError("winner claims require parameter, data, and compute matching")


_FORBIDDEN_NESTED_TARGET_KEYS = frozenset({"target", "target_label", "truth", "label"})


def _reject_nested_target_leakage(value: object, *, path: str = "row") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in _FORBIDDEN_NESTED_TARGET_KEYS:
                raise ValueError(f"target leakage at {path}.{key}")
            _reject_nested_target_leakage(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_nested_target_leakage(child, path=f"{path}[{index}]")


def validate_prediction_row(row: Mapping[str, Any]) -> None:
    _exact_keys(
        row,
        {
            "condition_id",
            "entity_count",
            "evaluator_only",
            "episode_id_hash",
            "fault_attribution",
            "input_track",
            "oracle_diagnostic",
            "prediction",
            "probabilities",
            "seed",
            "split",
            "step_index",
            "track",
            "trace_checkpoint_hash",
            "truth",
            "work_counters",
        },
        "raw prediction row",
    )
    if row["input_track"] not in AUTONOMOUS_INPUTS | {ORACLE_INPUT}:
        raise ValueError("unknown input track")
    _validate_condition_id(row["condition_id"], input_track=row["input_track"])
    condition_track = row["condition_id"].split("/", 1)[0]
    oracle = condition_track == ORACLE_INPUT
    if type(row["oracle_diagnostic"]) is not bool or type(row["evaluator_only"]) is not bool:
        raise ValueError("Oracle boundary flags must be exact booleans")
    if row["oracle_diagnostic"] != oracle or (row["input_track"] == ORACLE_INPUT) != oracle:
        raise ValueError("Oracle rows must be diagnostic-only")
    if row["evaluator_only"] != oracle:
        raise ValueError("Oracle inputs must remain evaluator-only")
    if row["track"] != ("oracle" if oracle else "autonomous"):
        raise ValueError("track must be derived from the condition input")
    if row["split"] != "synthetic_proxy":
        raise ValueError("source-only C19 may retain only synthetic proxy rows")
    if (
        isinstance(row["entity_count"], bool)
        or not isinstance(row["entity_count"], int)
        or row["entity_count"] < 1
    ):
        raise ValueError("entity_count must be positive")
    if not isinstance(row["probabilities"], Mapping) or not row["probabilities"]:
        raise ValueError("probabilities are required")
    values = list(row["probabilities"].values())
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise ValueError("probabilities must be numeric")
    if not math.isclose(sum(float(value) for value in values), 1.0, abs_tol=1e-9):
        raise ValueError("probabilities must sum to one")
    _reject_nested_target_leakage({key: value for key, value in row.items() if key != "truth"})


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
    _reject_nested_target_leakage(row)
    _validate_condition_id(row["condition_id"])
    if (
        isinstance(row["entity_count"], bool)
        or not isinstance(row["entity_count"], int)
        or row["entity_count"] < 1
    ):
        raise ValueError("entity_count must be a positive integer")
    if row["status"] not in {"attributed", "inconclusive"}:
        raise ValueError("unknown attribution status")
    if type(row["available"]) is not bool:
        raise ValueError("attribution availability must be an exact boolean")
    if row["entity_count"] == 1 and (
        row["status"] != "inconclusive"
        or row["available"] is not False
        or row["dominant_component"] is not None
    ):
        raise ValueError("single-entity Belief-R attribution must remain inconclusive")
    if row["status"] == "attributed" and (
        row["available"] is not True
        or row["dominant_component"] not in {"input", "gate", "state", "objective"}
    ):
        raise ValueError("attributed status requires one registered dominant component")
    if row["status"] == "inconclusive" and (
        row["available"] is not False or row["dominant_component"] is not None
    ):
        raise ValueError("inconclusive attribution must be unavailable and non-dominant")


def autonomous_aggregate_rows(rows: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Fail closed if a diagnostic Oracle row reaches autonomous aggregation."""

    validated = []
    for row in rows:
        validate_prediction_row(row)
        if row["track"] != "autonomous":
            raise ValueError("Oracle rows must be excluded from autonomous aggregation")
        validated.append(row)
    return validated

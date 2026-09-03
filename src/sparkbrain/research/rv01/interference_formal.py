from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from sparkbrain.v06.foundation import digest

from .interference_contract import (
    InterferencePhase,
    InterferenceWorldSpec,
    held_out_worlds,
    world_grid_hash,
)
from .interference_freeze import (
    R01_12D_DEVELOPMENT_GRID_HASH,
    R01_12D_EXECUTION_SOURCE_SHA,
    R01_12D_RESULT_PAYLOAD_HASH,
    R01_12D_SUITE_HASH,
    build_r01_12e_preflight,
)
from .interference_runner import run_interference_world
from .resource_matched_reservoir import run_resource_matched_reservoir_world

SEAL_SCHEMA = "rv01-r01-12-heldout-execution-seal-v1"
CANDIDATE_ID = "rv01-r01-12-interference-heldout-v1"


@dataclass(frozen=True, slots=True)
class ValidatedHeldOutExecutionSeal:
    source_git_sha: str
    held_out_world_grid_hash: str
    preflight_payload_hash: str
    seal_payload_hash: str


class _SealedHeldOutWorldView:
    """Preserve a held-out specification while satisfying internal dev-only guards.

    The existing R01-12B/D runners use ``phase`` only as a capability lock. All
    identity, seed, routes, thresholds, budgets, state serialization, and hashes
    continue to come from the original held-out specification.
    """

    phase = InterferencePhase.DEVELOPMENT

    def __init__(self, original: InterferenceWorldSpec) -> None:
        if original.phase is not InterferencePhase.HELD_OUT:
            raise ValueError("sealed held-out view requires a held-out world")
        original.validate()
        self._original = original

    def __getattr__(self, name: str) -> Any:
        return getattr(self._original, name)

    @property
    def world_id(self) -> str:
        return self._original.world_id

    @property
    def route_count(self) -> int:
        return self._original.route_count

    def validate(self) -> None:
        self._original.validate()

    def state_dict(self) -> dict[str, Any]:
        return self._original.state_dict()

    def specification_hash(self) -> str:
        return self._original.specification_hash()


def _seal_hash(payload: Mapping[str, Any]) -> str:
    value = dict(payload)
    value.pop("seal_payload_hash", None)
    return digest(value)


def validate_held_out_execution_seal(
    payload: Mapping[str, Any],
    *,
    checked_out_source_sha: str,
) -> ValidatedHeldOutExecutionSeal:
    if payload.get("schema") != SEAL_SCHEMA:
        raise RuntimeError("held-out execution seal schema mismatch")
    if payload.get("candidate_id") != CANDIDATE_ID:
        raise RuntimeError("held-out execution candidate mismatch")
    if payload.get("status") != "sealed-not-executed":
        raise RuntimeError("held-out execution seal is not in the sealed state")
    if payload.get("execution_policy") != "one-way-no-rerun":
        raise RuntimeError("held-out execution policy mismatch")
    if payload.get("held_out_capability_executed") is not False:
        raise RuntimeError("seal must precede held-out capability execution")
    if len(checked_out_source_sha) != 40:
        raise ValueError("checked_out_source_sha must be a full Git SHA")
    source_git_sha = str(payload.get("source_git_sha", ""))
    if source_git_sha != checked_out_source_sha:
        raise RuntimeError("checked-out source does not match the execution seal")

    specs = held_out_worlds()
    grid_hash = world_grid_hash(specs)
    if payload.get("held_out_world_grid_hash") != grid_hash:
        raise RuntimeError("held-out world grid does not match the execution seal")
    if payload.get("held_out_world_count") != 50:
        raise RuntimeError("held-out world count mismatch")
    expected = payload.get("expected_held_out_records")
    if expected != {
        "world_count": 50,
        "training_phase_count": 200,
        "field_probe_matrix_record_count": 1000,
        "reservoir_final_probe_record_count": 200,
    }:
        raise RuntimeError("held-out evidence cardinality seal mismatch")
    if payload.get("development_result") != {
        "execution_source_sha": R01_12D_EXECUTION_SOURCE_SHA,
        "world_grid_hash": R01_12D_DEVELOPMENT_GRID_HASH,
        "suite_hash": R01_12D_SUITE_HASH,
        "result_payload_hash": R01_12D_RESULT_PAYLOAD_HASH,
    }:
        raise RuntimeError("fixed R01-12D result anchors do not match the seal")

    preflight_hash = str(payload.get("preflight_payload_hash", ""))
    if len(preflight_hash) != 64:
        raise RuntimeError("preflight payload hash is missing from the seal")
    preflight = build_r01_12e_preflight(source_git_sha=checked_out_source_sha)
    if preflight["preflight_payload_hash"] != preflight_hash:
        raise RuntimeError("checked-out source does not reproduce the sealed preflight")
    if preflight["held_out_world_grid_hash"] != grid_hash:
        raise RuntimeError("reproduced preflight held-out grid mismatch")
    observed_seal_hash = _seal_hash(payload)
    if payload.get("seal_payload_hash") != observed_seal_hash:
        raise RuntimeError("execution seal payload hash mismatch")
    return ValidatedHeldOutExecutionSeal(
        source_git_sha=source_git_sha,
        held_out_world_grid_hash=grid_hash,
        preflight_payload_hash=preflight_hash,
        seal_payload_hash=observed_seal_hash,
    )


def run_sealed_held_out_interference(
    seal_payload: Mapping[str, Any],
    *,
    checked_out_source_sha: str,
) -> dict[str, Any]:
    """Execute the one-way held-out programme after a matching seal exists."""

    seal = validate_held_out_execution_seal(
        seal_payload,
        checked_out_source_sha=checked_out_source_sha,
    )
    specs = held_out_worlds()
    field_results = []
    reservoir_results = []
    for world in specs:
        authorized = _SealedHeldOutWorldView(world)
        field_results.append(run_interference_world(authorized))
        reservoir_results.append(
            run_resource_matched_reservoir_world(authorized)
        )

    field_suite_hash = digest(
        {
            "world_grid_hash": seal.held_out_world_grid_hash,
            "worlds": [
                {"world_id": row.world_id, "semantic_hash": row.semantic_hash}
                for row in field_results
            ],
        }
    )
    reservoir_suite_hash = digest(
        {
            "world_grid_hash": seal.held_out_world_grid_hash,
            "worlds": [
                {"world_id": row.world_id, "semantic_hash": row.semantic_hash}
                for row in reservoir_results
            ],
        }
    )
    return {
        "schema": "rv01-r01-12-heldout-result-v1",
        "candidate_id": CANDIDATE_ID,
        "source_git_sha": seal.source_git_sha,
        "seal_payload_hash": seal.seal_payload_hash,
        "preflight_payload_hash": seal.preflight_payload_hash,
        "held_out_world_grid_hash": seal.held_out_world_grid_hash,
        "held_out_capability_executed": True,
        "field_suite_hash": field_suite_hash,
        "reservoir_suite_hash": reservoir_suite_hash,
        "field_worlds": [row.state_dict() for row in field_results],
        "reservoir_worlds": [row.state_dict() for row in reservoir_results],
    }

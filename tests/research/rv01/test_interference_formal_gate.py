from __future__ import annotations

from pathlib import Path

import pytest

from sparkbrain.research.rv01.interference_contract import held_out_worlds, world_grid_hash
from sparkbrain.research.rv01.interference_formal import (
    CANDIDATE_ID,
    SEAL_SCHEMA,
    _seal_hash,
    _SealedHeldOutWorldView,
    validate_held_out_execution_seal,
)
from sparkbrain.research.rv01.interference_freeze import (
    R01_12D_DEVELOPMENT_GRID_HASH,
    R01_12D_EXECUTION_SOURCE_SHA,
    R01_12D_RESULT_PAYLOAD_HASH,
    R01_12D_SUITE_HASH,
    build_r01_12e_preflight,
)

_SOURCE_SHA = "2" * 40


def _preflight_hash() -> str:
    return str(
        build_r01_12e_preflight(source_git_sha=_SOURCE_SHA)[
            "preflight_payload_hash"
        ]
    )


def _valid_seal() -> dict[str, object]:
    payload: dict[str, object] = {
        "schema": SEAL_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "status": "sealed-not-executed",
        "execution_policy": "one-way-no-rerun",
        "source_git_sha": _SOURCE_SHA,
        "preflight_payload_hash": _preflight_hash(),
        "held_out_world_grid_hash": world_grid_hash(held_out_worlds()),
        "held_out_world_count": 50,
        "held_out_capability_executed": False,
        "expected_held_out_records": {
            "world_count": 50,
            "training_phase_count": 200,
            "field_probe_matrix_record_count": 1000,
            "reservoir_final_probe_record_count": 200,
        },
        "development_result": {
            "execution_source_sha": R01_12D_EXECUTION_SOURCE_SHA,
            "world_grid_hash": R01_12D_DEVELOPMENT_GRID_HASH,
            "suite_hash": R01_12D_SUITE_HASH,
            "result_payload_hash": R01_12D_RESULT_PAYLOAD_HASH,
        },
    }
    payload["seal_payload_hash"] = _seal_hash(payload)
    return payload


def test_valid_seal_can_be_verified_without_executing_capability() -> None:
    seal = _valid_seal()
    validated = validate_held_out_execution_seal(
        seal,
        checked_out_source_sha=_SOURCE_SHA,
    )
    assert validated.source_git_sha == _SOURCE_SHA
    assert validated.preflight_payload_hash == _preflight_hash()
    assert validated.held_out_world_grid_hash == world_grid_hash(held_out_worlds())


def test_source_mismatch_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="checked-out source"):
        validate_held_out_execution_seal(
            _valid_seal(),
            checked_out_source_sha="4" * 40,
        )


def test_unsealed_status_fails_closed() -> None:
    payload = _valid_seal()
    payload["status"] = "review-ready-not-sealed"
    payload["seal_payload_hash"] = _seal_hash(payload)
    with pytest.raises(RuntimeError, match="sealed state"):
        validate_held_out_execution_seal(
            payload,
            checked_out_source_sha=_SOURCE_SHA,
        )


def test_sealed_world_view_changes_only_internal_phase_gate() -> None:
    world = held_out_worlds()[0]
    view = _SealedHeldOutWorldView(world)
    assert view.phase.value == "development"
    assert view.world_id == world.world_id
    assert view.state_dict() == world.state_dict()
    assert view.specification_hash() == world.specification_hash()
    assert view.seed == world.seed
    assert view.routes == world.routes
    assert view.threshold == world.threshold
    assert view.maximum_total_active_edges == world.maximum_total_active_edges


def test_normal_ci_has_no_formal_capability_execution_step() -> None:
    path = Path(__file__).parents[3] / ".github" / "workflows" / "ci.yml"
    source = path.read_text(encoding="utf-8")
    assert "run_rv01_r01_12_formal.py" not in source
    assert "run_sealed_held_out_interference" not in source

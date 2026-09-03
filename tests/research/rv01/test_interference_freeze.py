from __future__ import annotations

from pathlib import Path

from sparkbrain.research.rv01.interference_freeze import (
    CRITICAL_FREEZE_PATHS,
    R01_12D_DEVELOPMENT_GRID_HASH,
    R01_12D_EXECUTION_SOURCE_SHA,
    R01_12D_RESULT_PAYLOAD_HASH,
    R01_12D_SUITE_HASH,
    build_r01_12e_preflight,
)
from sparkbrain.research.rv01.interference_contract import HELD_OUT_SEEDS

_SOURCE_SHA = "1" * 40


def _preflight():
    return build_r01_12e_preflight(source_git_sha=_SOURCE_SHA)


def test_preflight_freezes_exactly_fifty_held_out_specs_without_capability() -> None:
    payload = _preflight()
    assert payload["status"] == "review-ready-not-sealed"
    assert payload["held_out_capability_executed"] is False
    assert payload["source_git_sha"] == _SOURCE_SHA
    assert len(payload["held_out_worlds"]) == 50
    assert len({row["world_id"] for row in payload["held_out_worlds"]}) == 50
    assert len({row["specification_hash"] for row in payload["held_out_worlds"]}) == 50
    assert all(len(row["specification_hash"]) == 64 for row in payload["held_out_worlds"])
    assert len(payload["held_out_world_grid_hash"]) == 64
    assert payload["held_out_seeds"] == list(HELD_OUT_SEEDS)


def test_fixed_r01_12d_development_result_is_a_preflight_dependency() -> None:
    payload = _preflight()
    result = payload["development_result"]
    assert result == {
        "execution_source_sha": R01_12D_EXECUTION_SOURCE_SHA,
        "world_grid_hash": R01_12D_DEVELOPMENT_GRID_HASH,
        "suite_hash": R01_12D_SUITE_HASH,
        "result_payload_hash": R01_12D_RESULT_PAYLOAD_HASH,
    }


def test_expected_held_out_cardinality_is_frozen_before_execution() -> None:
    payload = _preflight()
    assert payload["expected_held_out_records"] == {
        "world_count": 50,
        "training_phase_count": 200,
        "field_probe_matrix_record_count": 1000,
        "reservoir_final_probe_record_count": 200,
    }


def test_world_budgets_are_serialized_in_the_preflight() -> None:
    payload = _preflight()
    for row in payload["held_out_worlds"]:
        assert row["route_count"] >= 3
        assert row["maximum_active_outgoing_edges"] >= 1
        assert row["maximum_total_active_edges"] >= row[
            "maximum_active_outgoing_edges"
        ]


def test_plasticity_comparator_and_evaluator_contracts_are_explicit() -> None:
    payload = _preflight()
    assert payload["plasticity_config"]["minimum_lag_ms"] == 0.5
    assert payload["plasticity_config"]["maximum_lag_ms"] == 6.5
    assert payload["reservoir_config"] == {
        "input_scale": 1.0,
        "leak_rate": 0.8,
        "maximum_abs_readout_weight": 2.0,
        "readout_learning_rate": 0.25,
        "recurrent_scale": 0.75,
        "seed_offset": 12001,
    }
    assert payload["evaluator_contract"]["initial_connection_weight"] == 0.05
    assert payload["evaluator_contract"]["maximum_probe_spikes"] == 512


def test_freeze_critical_source_files_are_hash_bound() -> None:
    payload = _preflight()
    hashes = payload["critical_source_sha256"]
    assert tuple(hashes) == CRITICAL_FREEZE_PATHS
    assert all(len(value) == 64 for value in hashes.values())


def test_preflight_source_does_not_import_capability_runners() -> None:
    path = (
        Path(__file__).parents[3]
        / "src"
        / "sparkbrain"
        / "research"
        / "rv01"
        / "interference_freeze.py"
    )
    source = path.read_text(encoding="utf-8")
    import_section = source.split("R01_12D_EXECUTION_SOURCE_SHA", 1)[0]
    assert "interference_runner" not in import_section
    assert "run_interference_world" not in import_section
    assert "run_resource_matched_reservoir_world" not in import_section


def test_preflight_hash_is_deterministic_for_one_source_sha() -> None:
    first = _preflight()
    second = _preflight()
    assert first == second
    assert len(first["preflight_payload_hash"]) == 64

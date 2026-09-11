from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from sparkbrain.research.rv02_rd003_online import planned_rd003_cells
import sparkbrain.research.rv02_rd004_online as rd004
from sparkbrain.research.rv02_scale import digest


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_rv02_rd004.py"
SPEC = importlib.util.spec_from_file_location("run_rv02_rd004_test", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def minimal_result(**overrides):
    result = {
        "protocol": rd004.RD004_PROTOCOL,
        "status": "incomplete_native_guard_training",
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "gain": 4.0,
        "eligibility_tail_ms": 6.5,
        "washout_ms": 100.0,
        "probe_horizon_ms": 40.0,
        "scientific_status": "not_scored_development_diagnosis",
        "training_schedule": (),
        "training_schedule_hash": digest(()),
        "e1_eligibility_budget": [],
        "es_eligibility_budget": [],
        "learner_states": {"disabled": {"hidden_trace_records": []}},
    }
    result.update(overrides)
    return result


def probe_pair(status: str) -> dict:
    row = {
        "status": status,
        "shared_snapshot_hash": "same",
        "cue_time_ms": 106.5,
    }
    return {"natural": dict(row), "boundary_zero": dict(row)}


def test_rd004_matrix_identity_is_same_exposed_18_cells_as_rd003() -> None:
    assert rd004.planned_rd004_cells() == planned_rd003_cells()
    assert len(rd004.planned_rd004_cells()) == 18


def test_rd004_status_classifier_is_fail_closed() -> None:
    complete = {
        mode: (probe_pair("complete"),)
        for mode in ("disabled", "causal", "shuffled")
    }
    assert rd004._classify_probe_status(complete) == "complete"

    incomplete = {mode: tuple(rows) for mode, rows in complete.items()}
    incomplete["causal"] = (probe_pair("incomplete_native_guard_probe"),)
    assert rd004._classify_probe_status(incomplete) == "incomplete_native_guard_probe"

    unknown = {mode: tuple(rows) for mode, rows in complete.items()}
    unknown["shuffled"] = (probe_pair("unexpected"),)
    assert rd004._classify_probe_status(unknown) == "incomplete_integrity_failure"


def test_offline_verifier_accepts_retained_training_guard_without_scoring() -> None:
    RUNNER.verify_result(minimal_result())


def test_offline_verifier_rejects_parameter_or_budget_drift() -> None:
    with pytest.raises(ValueError, match="gain drifted"):
        RUNNER.verify_result(minimal_result(gain=8.0))

    with pytest.raises(ValueError, match="eligibility budget mismatch"):
        RUNNER.verify_result(
            minimal_result(
                e1_eligibility_budget=[
                    {"time_ms": 1.0, "magnitude": 1.0, "observed_unit_id": 4}
                ]
            )
        )


def test_offline_verifier_rejects_probe_clock_drift() -> None:
    result = minimal_result(
        status="incomplete_integrity_failure",
        probe_snapshots={
            "causal": {
                "source_clock_ms": 10.0,
                "tail_end_ms": 16.5,
                "washout_end_ms": 116.5,
                "cue_time_ms": 117.0,
            }
        },
    )
    with pytest.raises(ValueError, match="cue not anchored"):
        RUNNER.verify_result(result)


def test_source_inventory_binds_new_runner_core_contract_and_tests() -> None:
    inventory = RUNNER.source_inventory(ROOT)
    assert "src/sparkbrain/research/rv02_rd004_online.py" in inventory
    assert "src/sparkbrain/research/rv02_rd004_probe_clock.py" in inventory
    assert "docs/research/RV02_RD004_RELATIVE_PROBE_CLOCK_PREREG.md" in inventory
    assert "scripts/run_rv02_rd004.py" in inventory
    assert "tests/test_rv02_rd004_runner.py" in inventory

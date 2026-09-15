from __future__ import annotations

import importlib.util
from pathlib import Path


def _runner_module():
    path = Path(__file__).parents[1] / "scripts" / "run_v061_a01_md002_p3_candidate_001.py"
    spec = importlib.util.spec_from_file_location("p3_candidate_001_runner", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_p3_candidate_001_manifest_is_prospective_and_execution_disabled() -> None:
    runner = _runner_module()
    contract = runner._contract("a" * 40)

    assert contract["candidate_id"] == (
        "a01-md002-p3-r-only-causal-carrier-candidate-001-v1"
    )
    assert contract["development_only"] is True
    assert contract["held_out_execution_allowed"] is False
    assert contract["formal_execution_allowed"] is False
    assert contract["same_identity_rerun_allowed"] is False

    prepared = contract["prepared_arms"]
    assert len(prepared) == 6
    assert len({row["prospective_execution_id"] for row in prepared}) == 6
    assert all(row["execution_authority"] is False for row in prepared)
    assert all(row["runtime_trace_sha256"] is None for row in prepared)
    assert all(row["capability_result"] is None for row in prepared)
    assert all(row["score"] is None for row in prepared)

    classifier = contract["classifier"]
    assert classifier["version"] == "p3-r-only-development-classifier-v1"
    assert classifier["development_only"] is True
    assert classifier["verdict_order"] == [
        "INVALID",
        "SUPPORTED_R_CAUSAL_CARRIER",
        "BASELINE_FOLLOWING",
        "NO_DIFFERENTIAL_EFFECT",
        "AMBIGUOUS",
    ]

from __future__ import annotations

from scripts.run_v031_brain_lab_artifact import build_artifact


def test_static_brain_lab_artifact_uses_live_runtime_state() -> None:
    artifact = build_artifact()
    assert artifact["status"] == "engineering_static_observation_not_scientific"
    assert artifact["parent"]["observation"]["runtime_origin"] == (
        "live_integrated_v03_runtime"
    )
    assert artifact["parent"]["observation"]["runtime_trace"]["event_hashes"]
    assert artifact["comparison"]["comparison_origin"] == "lab_observer_not_runtime_trace"
    assert artifact["comparison"]["right"]["observation"][
        "causal_evidence_removal"
    ]["trace_origin"] == "lab_counterfactual_observer_not_runtime_trace"

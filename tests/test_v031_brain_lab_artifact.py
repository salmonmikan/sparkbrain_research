from __future__ import annotations

import json
from pathlib import Path

from scripts.run_v031_brain_lab_artifact import build_artifact

ROOT = Path(__file__).resolve().parents[1]


def _canonical(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


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


def test_static_brain_lab_artifact_is_byte_reproducible_and_checked_in() -> None:
    first = _canonical(build_artifact())
    second = _canonical(build_artifact())
    checked = (
        ROOT
        / "artifacts"
        / "v03"
        / "v031_integrated_runtime"
        / "brain_lab_static_observation.json"
    ).read_bytes()
    assert first == second == checked

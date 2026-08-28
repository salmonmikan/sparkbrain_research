from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.v04 import IntegratedV04Brain, V04BrainConfig, pulse_train
from sparkbrain.v04.evaluation import run_reference_experiments
from sparkbrain.v04.visualizer import build_trace_html


def test_temporal_order_produces_distinct_reference_signatures() -> None:
    result = run_reference_experiments()
    row = next(item for item in result["experiments"] if item["name"] == "temporal_order")
    assert row["metrics"]["distinct_cascade_signatures"] == 3


def test_aligned_weak_inputs_outperform_dispersed_inputs() -> None:
    result = run_reference_experiments()
    row = next(item for item in result["experiments"] if item["name"] == "temporal_coincidence")
    metrics = row["metrics"]
    assert metrics["aligned"]["convergence_unit_spikes"] == 1
    assert metrics["dispersed"]["convergence_unit_spikes"] == 0
    assert metrics["aligned_minus_dispersed_spikes"] > 0


def test_repetition_adapts_and_omission_emits_prediction_error() -> None:
    result = run_reference_experiments()
    row = next(item for item in result["experiments"] if item["name"] == "repetition_omission")
    metrics = row["metrics"]
    assert metrics["late_spikes"] < metrics["early_spikes"]
    assert metrics["omission_prediction_error_pulses"] == 1
    assert metrics["omission_spikes"] >= 1


def test_checkpoint_detects_tamper_and_restores_field_continuation(tmp_path: Path) -> None:
    config = V04BrainConfig(enable_expectations=False, enable_plasticity=False)
    brain = IntegratedV04Brain(config)
    brain.ingest_pulses(pulse_train(("A", "B", "C")))
    checkpoint = tmp_path / "brain.json"
    brain.save_checkpoint(checkpoint)
    restored = IntegratedV04Brain.load_checkpoint(checkpoint)
    assert restored.field.state_hash() == brain.field.state_hash()

    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    payload["payload"]["field"]["current_time_ms"] += 1.0
    checkpoint.write_text(json.dumps(payload), encoding="utf-8")
    try:
        IntegratedV04Brain.load_checkpoint(checkpoint)
    except ValueError as exc:
        assert "hash mismatch" in str(exc)
    else:
        raise AssertionError("tampered checkpoint must fail")


def test_visualizer_is_self_contained() -> None:
    brain = IntegratedV04Brain(V04BrainConfig(enable_expectations=False))
    brain.ingest_pulses(pulse_train(("A", "B", "C")))
    page = build_trace_html(brain.trace)
    assert "<canvas" in page
    assert "https://" not in page
    assert "const trace=" in page

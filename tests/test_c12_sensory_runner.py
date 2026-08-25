from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "artifacts" / "v03" / "c12_sensory_field" / "protocol.json"
EXPECTED_OUTPUTS = {
    "ablation_metrics.json",
    "change_recovery_examples.jsonl",
    "goal_bias_adversarial.json",
    "protocol.json",
    "raw_trace.jsonl",
    "report.md",
}


def _run(output: Path, *, protocol: Path = PROTOCOL) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_c12_sensory_field.py"),
            "--root",
            str(ROOT),
            "--protocol",
            str(protocol),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        text=True,
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_c12_runner_is_deterministic_and_meets_preregistered_g04(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_result = _run(first)
    second_result = _run(second)
    assert first_result.returncode == 0, first_result.stderr
    assert second_result.returncode == 0, second_result.stderr
    assert {path.name for path in first.iterdir()} == EXPECTED_OUTPUTS
    assert {path.name for path in second.iterdir()} == EXPECTED_OUTPUTS
    assert {_sha256(first / name) for name in EXPECTED_OUTPUTS} == {
        _sha256(second / name) for name in EXPECTED_OUTPUTS
    }

    metrics = json.loads((first / "ablation_metrics.json").read_text(encoding="utf-8"))
    assert metrics["acceptance_passed"] is True
    assert all(metrics["acceptance"].values())
    full = metrics["conditions"]["full"]
    assert full["metrics"]["predictable_repetition_active_spark_reduction"] >= 0.5
    assert full["metrics"]["predictable_repetition_downstream_work_reduction"] >= 0.5
    assert full["metrics"]["change_or_omission_recall"] >= 0.9
    assert full["metrics"]["goal_relevant_recall_delta"] > 0.0
    assert full["metrics"]["irrelevant_false_activation_increase_percentage_points"] <= 10.0
    assert full["metrics"]["stimulus_specificity_recall"] > 0.0
    for interval in full["paired_intervals"].values():
        assert interval["bootstrap_repetitions"] == 10000
        assert interval["paired_block_count"] == 5


def test_raw_trace_separates_dense_and_active_work_and_keeps_all_channels(
    tmp_path: Path,
) -> None:
    output = tmp_path / "output"
    result = _run(output)
    assert result.returncode == 0, result.stderr
    rows = [
        json.loads(line)
        for line in (output / "raw_trace.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert rows
    assert {row["accepted"] for row in rows} == {False, True}
    required_terms = {
        "magnitude",
        "magnitude_contribution",
        "prediction_error",
        "normalized_novelty",
        "prediction_error_contribution",
        "novelty_contribution",
        "habituation",
        "habituation_contribution",
        "goal_bias_requested",
        "goal_bias_applied",
        "goal_contribution",
        "onset_contribution",
        "threshold",
        "final_salience",
    }
    assert all(required_terms <= set(row) for row in rows)
    assert all(
        row["work_delta"]["channels_inspected"]
        == row["work_delta"]["features_scored"]
        == row["work_delta"]["state_updates"]
        for row in rows
    )
    assert all(
        row["work_delta"]["sparks_emitted"]
        == row["work_delta"]["downstream_active_work"]
        for row in rows
    )
    assert any(row["omission"] and row["accepted"] for row in rows)
    assert any(
        row["goal_bias_requested"] > row["goal_bias_applied"] == 0.35 for row in rows
    )


def test_change_artifact_states_explicit_omission_learning_contract(tmp_path: Path) -> None:
    output = tmp_path / "output"
    result = _run(output)
    assert result.returncode == 0, result.stderr
    examples = [
        json.loads(line)
        for line in (output / "change_recovery_examples.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    full_omissions = [
        row
        for row in examples
        if row["condition_id"] == "full" and row["event_kind"] == "unexpected_omission"
    ]
    assert len(full_omissions) == 5
    assert all(row["recovered"] for row in full_omissions)
    assert all(
        "committed as the latest local value" in row["omission_definition"]
        for row in full_omissions
    )


def test_runner_refuses_nonempty_output_and_too_few_seeds(tmp_path: Path) -> None:
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    marker = occupied / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    result = _run(occupied)
    assert result.returncode != 0
    assert marker.read_text(encoding="utf-8") == "keep"

    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    protocol["seed_list"] = protocol["seed_list"][:4]
    invalid_protocol = tmp_path / "protocol.json"
    invalid_protocol.write_text(json.dumps(protocol), encoding="utf-8")
    result = _run(tmp_path / "short", protocol=invalid_protocol)
    assert result.returncode != 0
    assert "at least five unique seeds" in result.stderr

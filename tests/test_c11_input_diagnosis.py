from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from sparkbrain.learned.model import stable_bucket
from sparkbrain.v03_seed.input_diagnosis import (
    AUTONOMOUS_INPUT_TRACKS,
    DEFAULT_INPUT_TRACK,
    FeatureRecord,
    FrozenPairEvaluator,
    InputRecord,
    StrictSymbolicOracleFrontend,
    WholeHashFrontend,
    create_frontend,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "artifacts" / "v03" / "c11_input_diagnosis"
EXPECTED_OUTPUTS = {
    "protocol.json",
    "frozen_baseline_hashes.json",
    "diagnostic_manifest.json",
    "raw_features.jsonl",
    "raw_predictions.jsonl",
    "metrics_by_input_track.json",
    "failure_examples.jsonl",
    "diagnosis.md",
}


def _symbolic_record(**literal_overrides: object) -> InputRecord:
    literal: dict[str, object] = {
        "predicate": "opens",
        "entity": "red-key|north-door",
        "positive": True,
    }
    literal.update(literal_overrides)
    return InputRecord(
        "oracle",
        "ordinary text is not parsed by the Oracle",
        {"symbolic_event": {"kind": "literal", "literal": literal}},
    )


def _run(output: Path, *, hash_seed: str = "random") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_c11_input_diagnosis.py"),
            "--root",
            str(ROOT),
            "--contracts",
            str(CONTRACTS),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        env={
            **os.environ,
            "PYTHONHASHSEED": hash_seed,
            "PYTHONPATH": str(ROOT / "src"),
        },
        text=True,
        encoding="utf-8",
    )


@pytest.mark.parametrize("text", ["plain text", "猫が扉を開ける", "", "A\u030A"])
@pytest.mark.parametrize("buckets", [2, 17, 128, 1024])
def test_i0_matches_legacy_stable_bucket(text: str, buckets: int) -> None:
    encoded = WholeHashFrontend(buckets=buckets).encode(InputRecord("row", text))
    assert encoded.features == ((f"whole-hash:{stable_bucket(text, buckets)}", 1.0),)


def test_all_tracks_share_one_feature_record_interface() -> None:
    record = _symbolic_record()
    for condition in (*AUTONOMOUS_INPUT_TRACKS, "I2_symbolic_oracle"):
        frontend = create_frontend(condition, allow_oracle=condition == "I2_symbolic_oracle")
        assert isinstance(frontend.encode(record), FeatureRecord)
    assert DEFAULT_INPUT_TRACK in AUTONOMOUS_INPUT_TRACKS


def test_oracle_is_disabled_by_default_and_refuses_plain_text() -> None:
    with pytest.raises(ValueError, match="disabled by default"):
        create_frontend("I2_symbolic_oracle")
    with pytest.raises(ValueError, match="structured symbolic_event"):
        StrictSymbolicOracleFrontend().encode(InputRecord("plain", "text"))


@pytest.mark.parametrize("forbidden", ["truth", "target", "label", "answer", "test-only"])
def test_oracle_rejects_recursive_forbidden_fields(forbidden: str) -> None:
    record = _symbolic_record()
    metadata = dict(record.metadata or {})
    event = dict(metadata["symbolic_event"])
    event["literal"] = {**event["literal"], "nested": {forbidden: "leak"}}
    metadata["symbolic_event"] = event
    with pytest.raises(ValueError, match="forbidden Oracle field"):
        StrictSymbolicOracleFrontend().encode(InputRecord("leak", record.text, metadata))


def test_oracle_rejects_unknown_fields_and_label_shuffle_cannot_change_features() -> None:
    frontend = StrictSymbolicOracleFrontend()
    original = frontend.encode(_symbolic_record())
    shuffled_evaluator_label = "different"
    assert shuffled_evaluator_label == "different"
    assert frontend.encode(_symbolic_record()).feature_hash == original.feature_hash
    with pytest.raises(ValueError, match="exactly entity"):
        frontend.encode(_symbolic_record(comment="unknown"))


def test_pair_evaluator_rejects_cross_track_features() -> None:
    record = _symbolic_record()
    left = create_frontend("I0_whole_hash").encode(record)
    right = create_frontend("I1_local_compositional").encode(record)
    with pytest.raises(ValueError, match="same input condition"):
        FrozenPairEvaluator(similarity_threshold=0.5).evaluate(
            pair_id="P", expected_relation="similar", left=left, right=right
        )


def test_c11_runner_is_deterministic_and_retains_negative_examples(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_result = _run(first, hash_seed="1")
    second_result = _run(second, hash_seed="2")
    assert first_result.returncode == 0, first_result.stderr
    assert second_result.returncode == 0, second_result.stderr
    assert {path.name for path in first.iterdir()} == EXPECTED_OUTPUTS
    assert {path.name for path in second.iterdir()} == EXPECTED_OUTPUTS
    for name in EXPECTED_OUTPUTS:
        assert hashlib.sha256((first / name).read_bytes()).digest() == hashlib.sha256(
            (second / name).read_bytes()
        ).digest()

    metrics = json.loads((first / "metrics_by_input_track.json").read_text(encoding="utf-8"))
    assert metrics["I2_symbolic_oracle"]["accuracy"] == 1.0
    assert metrics["I1_local_compositional"]["mean_similar_pair_similarity"] > metrics[
        "I0_whole_hash"
    ]["mean_similar_pair_similarity"]
    assert metrics["oracle_audit"]["passed"] is True
    diagnosis = (first / "diagnosis.md").read_text(encoding="utf-8")
    assert "**implicated**" in diagnosis
    failures = [
        json.loads(line)
        for line in (first / "failure_examples.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert any(
        row["condition_id"] == "I1_local_compositional"
        and row["family"] == "high_overlap_negation"
        for row in failures
    )


def test_c11_runner_refuses_existing_output(tmp_path: Path) -> None:
    output = tmp_path / "occupied"
    output.mkdir()
    (output / "keep.txt").write_text("do not overwrite", encoding="utf-8")
    result = _run(output)
    assert result.returncode != 0
    assert (output / "keep.txt").read_text(encoding="utf-8") == "do not overwrite"

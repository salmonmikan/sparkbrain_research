from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import sparkbrain.v03_external_validation.readiness as readiness
from sparkbrain.v03_external_validation.contracts import (
    BASELINE_KIND_ORDER,
    EXACT_NINE_ARTIFACT_ORDER,
)
from sparkbrain.v03_external_validation.readiness import (
    BLOCK_REASON,
    C19ReadinessValidationError,
    build_bundle_documents,
    build_frozen_protocol,
    validate_bundle,
    write_blocked_readiness_bundle,
)

ROOT = Path(__file__).parents[1]
SOURCE_COMMIT = "a" * 40


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_frozen_protocol_pins_dependencies_without_reading_official_examples() -> None:
    preregistration_path = ROOT / readiness.INITIAL_PREREGISTRATION
    before = preregistration_path.read_bytes()
    frozen = build_frozen_protocol(root=ROOT, source_commit=SOURCE_COMMIT)

    assert preregistration_path.read_bytes() == before
    assert frozen["official_evaluation_allowed"] is False
    assert frozen["official_data_access"] == {
        "cache_verified": False,
        "examples_read": False,
        "policy": "blocked_before_cache_open",
    }
    assert frozen["belief_r_contract"]["cache_content_read"] is False
    assert frozen["belief_r_contract"]["cache_sha256"] == readiness.BELIEF_R_CACHE_SHA256
    assert frozen["belief_r_contract"]["revision"] == readiness.BELIEF_R_REVISION
    assert frozen["c18_contract"]["accepted_source_commit"] == (
        readiness.C18_ACCEPTED_SOURCE_COMMIT
    )
    assert frozen["c18_contract"]["required_methods"] == [
        "inspect",
        "record",
        "checkpoint",
        "fork",
    ]
    assert frozen["blocker"]["reason_code"] == BLOCK_REASON


def test_exact_nine_blocked_bundle_is_deterministic_and_complete(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"
    left_hashes = write_blocked_readiness_bundle(
        left, root=ROOT, source_commit=SOURCE_COMMIT
    )
    right_hashes = write_blocked_readiness_bundle(
        right, root=ROOT, source_commit=SOURCE_COMMIT
    )

    assert tuple(left_hashes) == EXACT_NINE_ARTIFACT_ORDER
    assert left_hashes == right_hashes
    assert all((left / name).read_bytes() == (right / name).read_bytes() for name in left_hashes)
    assert (left / "raw_predictions.jsonl").read_bytes() == b""
    assert (left / "attribution_rows.jsonl").read_bytes() == b""

    manifest = _jsonl(left / "run_manifest.jsonl")
    matrix = [row for row in manifest if row["row_kind"] == "official_condition"]
    baselines = [row for row in manifest if row["row_kind"] == "baseline"]
    assert len(matrix) == 12 * 5
    assert len(baselines) == len(BASELINE_KIND_ORDER) * 5
    assert all(row["status"] == "blocked" for row in manifest)
    assert all(row["official_examples_read"] is False for row in manifest)
    assert all(row["output_row_count"] == 0 for row in manifest)

    metrics = json.loads((left / "metrics_by_condition.json").read_text(encoding="utf-8"))
    paired = json.loads((left / "paired_statistics.json").read_text(encoding="utf-8"))
    matching = json.loads((left / "baseline_matching.json").read_text(encoding="utf-8"))
    assert metrics["status"] == "not_evaluated"
    assert metrics["autonomous"]["metrics"] is None
    assert metrics["oracle"]["metrics"] is None
    assert paired["comparisons"] is None
    assert paired["executed_resamples"] == 0
    assert matching["winner_claim"] is False
    assert all(
        row[key] is False
        for row in matching["rows"]
        for key in (
            "compute_match",
            "data_match",
            "optimization_match",
            "parameter_match",
            "winner_claim_allowed",
        )
    )


def test_validator_rejects_claim_escalation_and_nonempty_predictions(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    write_blocked_readiness_bundle(output, root=ROOT, source_commit=SOURCE_COMMIT)
    metrics_path = output / "metrics_by_condition.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    metrics["status"] = "supported"
    metrics_path.write_text(json.dumps(metrics), encoding="utf-8")
    with pytest.raises(C19ReadinessValidationError, match="not_evaluated"):
        validate_bundle(output, root=ROOT)

    documents = build_bundle_documents(root=ROOT, source_commit=SOURCE_COMMIT)
    metrics_path.write_bytes(documents[metrics_path.name])
    (output / "raw_predictions.jsonl").write_text("{}\n", encoding="utf-8")
    with pytest.raises(C19ReadinessValidationError, match="zero official predictions"):
        validate_bundle(output, root=ROOT)


def test_validator_rejects_missing_or_extra_artifact(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    write_blocked_readiness_bundle(output, root=ROOT, source_commit=SOURCE_COMMIT)
    (output / "unexpected.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(C19ReadinessValidationError, match="exact-nine"):
        validate_bundle(output, root=ROOT)


def test_invalid_source_commit_and_staging_failure_publish_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    invalid_output = tmp_path / "invalid"
    with pytest.raises(C19ReadinessValidationError, match="full Git commit"):
        write_blocked_readiness_bundle(invalid_output, root=ROOT, source_commit="HEAD")
    assert not invalid_output.exists()

    output = tmp_path / "atomic"

    def reject_staging(_output: Path, *, root: Path) -> dict[str, str]:
        del _output, root
        raise C19ReadinessValidationError("injected validation failure")

    monkeypatch.setattr(readiness, "validate_bundle", reject_staging)
    with pytest.raises(C19ReadinessValidationError, match="injected"):
        write_blocked_readiness_bundle(output, root=ROOT, source_commit=SOURCE_COMMIT)
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


def test_failure_example_contains_only_ids_hashes_and_machine_reason(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    write_blocked_readiness_bundle(output, root=ROOT, source_commit=SOURCE_COMMIT)
    failures = _jsonl(output / "failure_examples.jsonl")
    assert len(failures) == 1
    assert set(failures[0]) == {
        "failure_id",
        "input_hash",
        "reason_code",
        "source_commit_hash",
    }
    assert failures[0]["reason_code"] == BLOCK_REASON


def test_cli_writes_a_valid_bundle_without_dataset_arguments(tmp_path: Path) -> None:
    output = tmp_path / "cli-bundle"
    argv = [
        "scripts/run_c19_external_validation.py",
        "--source-commit",
        SOURCE_COMMIT,
        "--output",
        str(output),
    ]
    bootstrap = (
        "import runpy,sys;"
        "sys.path.insert(0,'src');"
        f"sys.argv={argv!r};"
        "runpy.run_path(sys.argv[0],run_name='__main__')"
    )
    result = subprocess.run(
        [sys.executable, "-c", bootstrap],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "blocked C19 exact-nine bundle" in result.stdout
    assert validate_bundle(output, root=ROOT)

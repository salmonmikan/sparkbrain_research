from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ARTIFACT = (
    Path(__file__).resolve().parents[1] / "artifacts/exploratory/m1-outcome-identity-20261001T1458Z"
)


def test_retained_m1_archive_without_runtime_execution() -> None:
    spec = importlib.util.spec_from_file_location(
        "m1_publication_archive_verifier", ARTIFACT / "verify_bundle.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.verify(ARTIFACT)
    assert result["archive_files_verified"] == 3319
    assert result["readable_copies_verified"] == 43
    assert result["physical_checkpoint_payload_comparisons"] == 2304
    assert result["corrected_cases_independently_recomputed"] == 16
    assert result["total_public_api_attempts"] == 192
    assert result["byte_identical_corrected_non_environment_files"] == 972
    assert result["scientific_credit"] == 0
    assert result["runtime_executed_by_verifier"] is False


def test_publication_verifier_rejects_corrupted_retained_data() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_verify_bundle"],
        cwd=ARTIFACT,
        check=True,
        capture_output=True,
        text=True,
    )


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def update_calls_digest(root: Path) -> None:
    completed = json.loads((root / "COMPLETED.json").read_text())
    completed["calls_sha256"] = hashlib.sha256((root / "calls.jsonl").read_bytes()).hexdigest()
    write_json(root / "COMPLETED.json", completed)


def synthetic_reproduction(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    # These are saved-record fixtures only: no archived driver or runtime is imported.
    artifact, retained = tmp_path / "artifact", tmp_path / "retained"
    artifact.mkdir()
    shutil.copyfile(ARTIFACT / "verify_reproduction.py", artifact / "verify_reproduction.py")
    error = {
        "type": "RuntimeError",
        "message": "identical observation conflict",
        "traceback": (
            'Traceback: File "/original/source/driver.py", line 112\nRuntimeError: conflict'
        ),
    }
    tie = {
        "hypotheses": [
            {"candidate": "alpha", "support": 0.8},
            {"candidate": "beta", "support": 0.8},
        ],
        "confidence": 0.5,
        "margin": 0.0,
        "selected_candidate": None,
    }
    action = {"decision": "abstain", "reason": "predictive_competing_hypotheses_ambiguous"}
    state = {
        "sequence": 3,
        "serialized_components": {"scope/state.json": {"support": 0.8}},
        "traceback": "ordinary state field that must never be normalized",
    }
    rows = [
        {
            "case_id": "exact",
            "call_index": 6,
            "operation": "outcome",
            "exception": error,
            "input": {"receipt_id": "receipt-3", "outcome": -0.8},
            "output": None,
            "before": state,
            "after": state,
            "sequence_delta": 0,
        },
        {
            "case_id": "near-alias",
            "call_index": 6,
            "operation": "outcome",
            "exception": None,
            "input": {"receipt_id": "receipt-3", "outcome": -0.8},
            "output": {"revision": tie},
            "before": state,
            "after": state,
            "sequence_delta": 1,
        },
        {
            "case_id": "near-alias",
            "call_index": 8,
            "operation": "observe",
            "exception": None,
            "input": {"event_id": "event-4", "signal": 0.0},
            "output": action,
            "before": state,
            "after": state,
            "sequence_delta": 0,
        },
    ]
    summaries = [
        {
            "case_id": "exact",
            "probe_exception": error,
            "redelivery_exception": error,
            "fourth_exception": error,
            "fourth_action": None,
            "probe_revision": None,
        },
        {
            "case_id": "near-alias",
            "probe_exception": None,
            "redelivery_exception": None,
            "fourth_exception": None,
            "fourth_action": action,
            "probe_revision": tie,
        },
    ]
    run = retained / "r2-run1"
    write_json(run / "STARTED.json", {"freeze_sha256": "frozen", "scientific_credit": 0})
    write_json(run / "environment.json", {"executable": "/original/python", "pythonhashseed": "1"})
    write_json(run / "summary.json", {"case_count": 2, "cases": summaries})
    write_json(run / "COMPLETED.json", {"fixed_matrix_complete": True, "calls_sha256": "pending"})
    (run / "calls.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
    for row in rows:
        prefix = run / row["case_id"] / f"call-{row['call_index']:02d}"
        write_json(prefix / "record.json", row)
        for side in ("before", "after"):
            write_json(prefix / side / "snapshot.json", state)
            write_json(prefix / side / "save1/scope/state.json", {"support": 0.8})
    for summary in summaries:
        write_json(run / summary["case_id"] / "summary.json", summary)
    update_calls_digest(run)
    shutil.copytree(run, retained / "r2-run37")
    write_json(retained / "r2-run37/environment.json", {"pythonhashseed": "37"})
    manifest = {
        "files": {
            path.relative_to(retained).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in retained.rglob("*")
            if path.is_file()
        }
    }
    write_json(artifact / "review/ARTIFACT_MANIFEST.json", manifest)
    manifest_digest = hashlib.sha256(
        (artifact / "review/ARTIFACT_MANIFEST.json").read_bytes()
    ).hexdigest()
    write_json(artifact / "BUNDLE.json", {"artifact_manifest_sha256": manifest_digest})
    primary, replica = tmp_path / "primary", tmp_path / "replica"
    shutil.copytree(run, primary)
    shutil.copytree(retained / "r2-run37", replica)
    verification = tmp_path / "verification.json"
    write_json(
        verification,
        {
            "run1": {"all_expected_checks_pass": True, "checks": {str(i): True for i in range(29)}},
            "run37": {
                "all_expected_checks_pass": True,
                "checks": {str(i): True for i in range(29)},
            },
            "reproducibility": {"reproducible_all_runtime_records_and_checkpoints": True},
        },
    )
    return artifact, retained, primary, replica, verification


def mutate_saved_records(root: Path, field: str, replacement: object) -> None:
    # Mutate every saved representation of the specified field, leaving physical state intact.
    # This helper intentionally differs from the verifier's tightly scoped normalization.
    def replace(value: object) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == field:
                    value[key] = replacement
                else:
                    replace(item)
        elif isinstance(value, list):
            for item in value:
                replace(item)

    for path in root.rglob("*"):
        if path.name not in {"record.json", "summary.json", "calls.jsonl"}:
            continue
        if path.suffix == ".jsonl":
            rows = [json.loads(line) for line in path.read_text().splitlines()]
            replace(rows)
            path.write_text("".join(json.dumps(row) + "\n" for row in rows))
        else:
            value = json.loads(path.read_text())
            replace(value)
            write_json(path, value)
    update_calls_digest(root)


def run_portable_cli(
    paths: tuple[Path, Path, Path, Path, Path], optimized: bool
) -> subprocess.CompletedProcess:
    artifact, retained, primary, replica, verification = paths
    return subprocess.run(
        [
            sys.executable,
            *(["-O"] if optimized else []),
            str(artifact / "verify_reproduction.py"),
            "--verification",
            str(verification),
            "--primary",
            str(primary),
            "--replica",
            str(replica),
            "--retained-root",
            str(retained),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("optimized", [False, True], ids=["normal", "optimized"])
@pytest.mark.parametrize(
    "condition",
    [
        "matching",
        "relocated_tracebacks",
        "fourth_action_drift",
        "exception_message_drift",
        "invalid_calls_digest",
        "checkpoint_drift",
        "missing_file",
        "environment_only",
    ],
)
def test_portable_reproduction_compares_authenticated_retained_runs(
    tmp_path: Path, condition: str, optimized: bool
) -> None:
    paths = synthetic_reproduction(tmp_path)
    _artifact, _retained, primary, replica, _verification = paths
    if condition == "relocated_tracebacks":
        for root in (primary, replica):
            # Change only declared exception traceback paths, never similarly named state fields.
            for path in root.rglob("*"):
                if path.name in {"record.json", "summary.json", "calls.jsonl"}:
                    path.write_text(path.read_text().replace("/original/source/", "/new/worktree/"))
            update_calls_digest(root)
    elif condition == "fourth_action_drift":
        for root in (primary, replica):
            mutate_saved_records(root, "decision", "act_alpha")
    elif condition == "exception_message_drift":
        for root in (primary, replica):
            mutate_saved_records(root, "message", "a materially different exception")
    elif condition == "invalid_calls_digest":
        write_json(
            primary / "COMPLETED.json", {"fixed_matrix_complete": True, "calls_sha256": "bad"}
        )
    elif condition == "checkpoint_drift":
        write_json(primary / "near-alias/call-08/after/save1/scope/state.json", {"support": 0.9})
    elif condition == "missing_file":
        (primary / "near-alias/call-08/after/snapshot.json").unlink()
    elif condition == "environment_only":
        for root in (primary, replica):
            write_json(
                root / "environment.json", {"executable": "/new/python", "platform": "new-host"}
            )
    # Audit must never rewrite either retained or fresh saved artifacts.
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    completed = run_portable_cli(paths, optimized)
    success = condition in {"matching", "relocated_tracebacks", "environment_only"}
    assert (completed.returncode == 0) is success, completed.stderr
    assert ("portable semantic/state reproduction" in completed.stdout) is success
    assert before == {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    if success:
        result = json.loads(completed.stdout)
        assert result["scientific_credit"] == 0
        assert result["runtime_executed_by_verifier"] is False
        run = result["runs"]["r2-run1"]
        assert run["environment_changed"] is (condition == "environment_only")
        if condition == "relocated_tracebacks":
            assert run["calls_sha256"]["fresh"] != run["calls_sha256"]["retained"]
            assert "COMPLETED.json" in run["declared_provenance_or_json_encoding_differences"]
    else:
        assert "Reproduction verification failed:" in completed.stderr


@pytest.mark.parametrize(
    "condition",
    [
        "manifest_tampering",
        "retained_tampering",
        "extra_file",
        "nested_traceback_drift",
        "malformed_exception",
        "numeric_type_drift",
        "nonliteral_acceptance",
        "failed_check",
        "failed_reproduction",
        "duplicate_json_key",
        "unexpected_completed_field",
    ],
)
def test_portable_reproduction_fails_closed(tmp_path: Path, condition: str) -> None:
    paths = synthetic_reproduction(tmp_path)
    artifact, retained, primary, replica, verification = paths
    if condition == "manifest_tampering":
        with (artifact / "review/ARTIFACT_MANIFEST.json").open("a") as handle:
            handle.write(" ")
    elif condition == "retained_tampering":
        (retained / "r2-run1/STARTED.json").write_text("{}\n")
    elif condition == "extra_file":
        (primary / "undeclared.json").write_text("{}\n")
    elif condition == "nested_traceback_drift":
        for root in (primary, replica):
            mutate_saved_records(root, "traceback", "unapproved state change")
    elif condition == "malformed_exception":
        for root in (primary, replica):
            mutate_saved_records(
                root, "exception", {"type": "RuntimeError", "message": "missing traceback"}
            )
    elif condition == "numeric_type_drift":
        for root in (primary, replica):
            mutate_saved_records(root, "sequence_delta", False)
    elif condition in {"nonliteral_acceptance", "failed_check", "failed_reproduction"}:
        value = json.loads(verification.read_text())
        if condition == "nonliteral_acceptance":
            value["run1"]["all_expected_checks_pass"] = 1
        elif condition == "failed_check":
            value["run1"]["checks"]["0"] = False
        else:
            value["reproducibility"]["reproducible_all_runtime_records_and_checkpoints"] = False
        write_json(verification, value)
    elif condition == "duplicate_json_key":
        path = primary / "exact/call-06/record.json"
        path.write_text(path.read_text().replace("{", '{"output":"masked drift",', 1))
    elif condition == "unexpected_completed_field":
        path = primary / "COMPLETED.json"
        value = json.loads(path.read_text())
        value["unexpected"] = "must remain exact"
        write_json(path, value)
    completed = run_portable_cli(paths, optimized=True)
    assert completed.returncode == 1
    assert "Reproduction verification failed:" in completed.stderr

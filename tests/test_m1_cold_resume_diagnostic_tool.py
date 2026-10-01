"""Outcome-independent harness checks; no M1 runtime execution."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "scripts/m1_cold_resume_diagnostic.py"
SPEC = importlib.util.spec_from_file_location("m1_cold_resume_diagnostic", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def test_exact_bytes_and_inventory_are_required(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "state.json").write_text('{"a":1}\n')
    (b / "state.json").write_text('{"a":1}\n')
    assert TOOL.compare_directories(a, b)["equal"]
    (b / "state.json").write_text('{ "a": 1 }\n')
    assert TOOL.compare_directories(a, b)["changed_files"] == ["state.json"]
    (b / "extra").write_text("x")
    assert TOOL.compare_directories(a, b)["changed_files"] == ["extra", "state.json"]


def test_mismatch_retains_both_payloads(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "state").write_bytes(b"before")
    (b / "state").write_bytes(b"after")
    failure = tmp_path / "failure"
    with pytest.raises(AssertionError, match="serialized state mismatch"):
        TOOL.exact_or_fail(a, b, failure)
    assert (failure / "left/state").read_bytes() == b"before"
    assert (failure / "right/state").read_bytes() == b"after"


def test_rows_do_not_truncate_or_ignore_behavior() -> None:
    row = {"step": 1, "cycle": {"action": "abstain"}, "inspect_hash": "x"}
    assert TOOL.compare_rows([row], [row])["equal"]
    assert not TOOL.compare_rows([row], [])["equal"]
    other = {**row, "cycle": {"action": "act_alpha"}}
    assert TOOL.compare_rows([row], [other])["reason"] == "row_mismatch"


def test_artifact_write_is_no_clobber_and_disk_budget_is_real(tmp_path: Path) -> None:
    p = tmp_path / "artifact.json"
    TOOL.write_json(p, {"x": 1})
    with pytest.raises(FileExistsError):
        TOOL.write_json(p, {"x": 2})
    with pytest.raises(RuntimeError, match="cap exceeded"):
        TOOL.enforce_disk(tmp_path, 1)


def test_missing_checkpoint_is_not_equal_to_missing_checkpoint(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        TOOL.compare_directories(tmp_path / "missing-a", tmp_path / "missing-b")


@pytest.mark.parametrize("mode", ["run", "baseline", "observed", "restore", "secondary"])
def test_cli_existing_output_is_completely_untouched(tmp_path: Path, mode: str) -> None:
    output = tmp_path / "existing"
    output.mkdir()
    (output / "sentinel.bin").write_bytes(b"prior-artifact\x00\xff")
    before = TOOL.inventory(output)
    result = subprocess.run(
        [sys.executable, str(SOURCE), "--mode", mode, "--output", str(output)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0
    assert TOOL.inventory(output) == before
    assert (output / "sentinel.bin").read_bytes() == b"prior-artifact\x00\xff"


def test_summary_separates_byte_behavior_and_execution_failures(tmp_path: Path) -> None:
    status = {"returncode": 1, "timed_out": False}
    error = tmp_path / "ERROR.json"
    TOOL.write_json(error, {"error": "serialized state mismatch: state"})
    assert TOOL.failure_category(status, error) == "serialized_byte_mismatch"
    error.write_bytes(TOOL.canonical({"error": "future transition mismatch at step 8"}))
    assert TOOL.failure_category(status, error) == "future_transition_mismatch"
    assert TOOL.failure_category({"returncode": None, "timed_out": True}, error) == "worker_timeout"
    assert TOOL.failure_category({"returncode": 0, "timed_out": False}, error) is None


def test_cycle_rows_use_the_frozen_json_contract_without_numeric_normalization() -> None:
    live = {"step": 1, "cycle": {"nested": {"centroid": (0.0, 0.45)}}, "inspect_hash": "x"}
    saved = {"step": 1, "cycle": {"nested": {"centroid": [0.0, 0.45]}}, "inspect_hash": "x"}
    assert TOOL.compare_rows([live], [saved])["equal"]
    changed = {**saved, "cycle": {"nested": {"centroid": [0, 0.45]}}}
    assert not TOOL.compare_rows([saved], [changed])["equal"]
    reordered = {**saved, "cycle": {"nested": {"centroid": [0.45, 0.0]}}}
    changed_value = {**saved, "cycle": {"nested": {"centroid": [0.0, 0.46]}}}
    assert not TOOL.compare_rows([saved], [reordered])["equal"]
    assert not TOOL.compare_rows([saved], [changed_value])["equal"]


def test_missing_posix_limits_stops_before_any_runtime_import(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "resource", None)
    monkeypatch.setattr(TOOL, "runtime_imports",
                        lambda: pytest.fail("runtime must not be imported"))
    args = SimpleNamespace(output=tmp_path / "new", mode="baseline", cut=0,
                           reference=None, output_created=False)
    with pytest.raises(RuntimeError, match="requires POSIX"):
        TOOL.worker(args, json.loads(TOOL.PROTOCOL.read_bytes()))
    assert args.output_created is True
    assert (args.output / "STARTED.json").exists()

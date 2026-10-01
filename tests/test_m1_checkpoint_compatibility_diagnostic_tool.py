"""Synthetic harness tests only: never import or execute a SparkBrain runtime."""
from __future__ import annotations

import importlib.util
import inspect
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "scripts/m1_checkpoint_compatibility_diagnostic.py"
SPEC = importlib.util.spec_from_file_location("m1_compatibility_tool", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def synthetic_fixture(root: Path) -> Path:
    root.mkdir(parents=True)
    objects = {
        "predictive/pilot-state.json": {"schema_version": 1, "config": {"context_gate": 0.35},
                                         "reference_brain_state_hash": "semantic-unchanged"},
        "predictive/reference-brain.json": {"schema_version": 1, "state": {"x": 1},
                                             "runtime_state_hash": "semantic-unchanged"},
        "scope/sb002-state.json": {"payload": {"schema_version": 2,
                                               "config": {"minimum_confidence": 0.6},
                                               "router": {"config": {"minimum_confidence": 0.6}}},
                                   "state_hash": "semantic-unchanged"},
        "pilot-state.json": {"schema_version": 1, "predictive_state_hash": "unchanged",
                              "scope_state_hash": "unchanged"},
        "world-state.json": {"index": 7},
    }
    objects["predictive/reference-brain.json"]["payload_hash"] = TOOL.sha(
        TOOL.canonical(objects["predictive/reference-brain.json"]))
    objects["scope/sb002-state.json"]["payload_sha256"] = TOOL.sha(
        TOOL.canonical(objects["scope/sb002-state.json"]["payload"]))
    for name, obj in objects.items():
        TOOL.write_json(root / name, obj)
    TOOL.write_json(root / "manifest.json", {"schema_version": 1,
                                             "state_hash": "semantic-unchanged",
                                             "files": TOOL.inventory(root)})
    return root


def test_import_is_runtime_independent() -> None:
    code = (
        "import builtins,runpy; original=builtins.__import__; "
        "exec(\"def guarded(name,*a,**k):\\n"
        " if name.startswith('sparkbrain'): raise AssertionError(name)\\n"
        " return original(name,*a,**k)\"); "
        "builtins.__import__=guarded; runpy.run_path(" + repr(str(SOURCE)) + ")"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("case", TOOL.load_protocol()["cases"], ids=lambda c: c["case_id"])
def test_mutants_preserve_semantic_hashes_and_only_refresh_declared_digests(
    tmp_path: Path, case: dict,
) -> None:
    original = synthetic_fixture(tmp_path / "original")
    copy = tmp_path / "copy"
    shutil.copytree(original, copy)
    before = TOOL.inventory(original)
    result = TOOL.mutate_input(copy, case)
    assert TOOL.inventory(original) == before
    assert result["before"] == before
    manifest = json.loads((copy / "manifest.json").read_bytes())
    assert manifest["state_hash"] == "semantic-unchanged"
    for name, digest in manifest["files"].items():
        assert TOOL.sha((copy / name).read_bytes()) == digest
    direct = json.loads((copy / "predictive/reference-brain.json").read_bytes())
    assert direct["runtime_state_hash"] == "semantic-unchanged"
    assert direct["payload_hash"] == TOOL.sha(TOOL.canonical(
        {k: v for k, v in direct.items() if k != "payload_hash"}))
    scope = json.loads((copy / "scope/sb002-state.json").read_bytes())
    assert scope["state_hash"] == "semantic-unchanged"
    assert scope["payload_sha256"] == TOOL.sha(TOOL.canonical(scope["payload"]))
    assert scope["payload"]["router"]["config"]["minimum_confidence"] == 0.6
    if case["case_id"] == "C10":
        assert scope["payload"]["config"]["minimum_confidence"] == 0.65
    assert len(result["modified_files"]) <= 2


@pytest.mark.parametrize("mode", ["run", "setup", "case"])
def test_existing_output_is_byte_preserved_for_every_cli_mode(tmp_path: Path, mode: str) -> None:
    (tmp_path / "sentinel").write_bytes(b"old-data\x00\xff")
    before = TOOL.inventory(tmp_path)
    result = subprocess.run([sys.executable, str(SOURCE), "--mode", mode,
                             "--source-commit", "0" * 40, "--output", str(tmp_path)],
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert TOOL.inventory(tmp_path) == before


def test_delegating_wrappers_preserve_descriptor_types_and_restore_on_error() -> None:
    class Fake:
        @staticmethod
        def static(value):
            return value + 1

        @classmethod
        def klass(cls, value):
            return cls.__name__, value

        def method(self):
            raise ValueError("expected")

    originals = {name: inspect.getattr_static(Fake, name) for name in ("static", "klass", "method")}
    events, phase = [], ["primary-load"]
    with pytest.raises(ValueError, match="expected"), TOOL.milestones(
        [(name, Fake, name) for name in originals], events, phase,
    ):
        assert Fake.static(1) == 2
        phase[0] = "save-back"
        assert Fake.klass(2) == ("Fake", 2)
        Fake().method()
    assert all(inspect.getattr_static(Fake, name) is raw for name, raw in originals.items())
    assert TOOL.event_count(events, "static", "primary-load") == 1
    assert TOOL.event_count(events, "klass", "save-back") == 1
    assert events[-1]["event"] == "error"


def test_saveback_failure_cannot_relabel_accepted_load() -> None:
    assert TOOL.disposition("C01", {"returned": True}, {"status": "incomplete"}) == (
        "accepted_control_saveback_incomplete")
    assert TOOL.disposition("C03", {"returned": True}, {"status": "incomplete"}) == (
        "unexpected_acceptance")
    assert TOOL.disposition("C04", {"returned": True}, {"status": "incomplete"}) == (
        "observed_alias_acceptance")
    assert TOOL.disposition("C03", {"returned": False, "error_type": "TimeoutError",
                                    "error": "timed out"}, {}) == "incomplete_load_infrastructure"


def test_posix_limits_are_required_before_runtime_import(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(TOOL, "resource", None)
    with pytest.raises(RuntimeError, match="requires POSIX"):
        TOOL.apply_limits(TOOL.load_protocol())


def test_mutable_input_inventory_detects_write(tmp_path: Path) -> None:
    source = synthetic_fixture(tmp_path / "input")
    before = TOOL.inventory(source)
    (source / "world-state.json").write_bytes(b"changed")
    assert TOOL.inventory(source) != before


def test_preflight_requires_exact_clean_head(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(TOOL, "git", lambda *args: "a" * 40)
    with pytest.raises(ValueError, match="exact checked-out HEAD"):
        TOOL.preflight("b" * 40, TOOL.load_protocol())
    with pytest.raises(ValueError, match="clean committed"):
        TOOL.preflight("a" * 40, TOOL.load_protocol())


def test_incomplete_workers_still_emit_all_ten_planned_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "preflight", lambda *args: {"source_commit": "a" * 40})
    monkeypatch.setattr(TOOL, "runtime_imports", lambda: pytest.fail("no runtime import"))

    def fixture(path):
        synthetic_fixture(path)
        return {"archive_sha256": TOOL.load_protocol()["reused_fixture"]["archive_sha256"],
                "files": TOOL.inventory(path)}

    calls = []

    def failed(command, root, name, timeout):
        calls.append(command)
        return {"name": name, "returncode": 1, "status": "returned"}

    template = synthetic_fixture(tmp_path / "template")
    archive = TOOL.load_protocol()["reused_fixture"]["archive_sha256"]
    frozen = {"retained_fixture": {"archive_sha256": archive, "files": TOOL.inventory(template)}}
    monkeypatch.setattr(TOOL, "load_inputs", lambda: frozen)
    monkeypatch.setattr(TOOL, "retained_fixture", fixture)
    monkeypatch.setattr(TOOL, "capped_subprocess", failed)
    args = SimpleNamespace(output=tmp_path / "new", source_commit="a" * 40, output_created=False)
    TOOL.run(args, TOOL.load_protocol())
    summary = json.loads((args.output / "summary.json").read_bytes())
    assert summary["status"] == "incomplete"
    assert [row["case_id"] for row in summary["cases"]] == [f"C{i:02d}" for i in range(1, 11)]
    assert summary["cases"][1]["status"] == "blocked_setup_failure"
    assert summary["primary_integrated_loads_completed_observed"] == 0
    assert len(calls) == 10  # One setup and nine independent case attempts; C02 is blocked.
    assert (args.output / "protocol.json").read_bytes() == TOOL.PROTOCOL.read_bytes()


def test_file_cap_and_no_clobber_json_are_enforced(tmp_path: Path) -> None:
    target = tmp_path / "x.json"
    TOOL.write_json(target, {"value": 1})
    with pytest.raises(FileExistsError):
        TOOL.write_json(target, {"value": 2})
    with pytest.raises(RuntimeError, match="cap exceeded"):
        TOOL.enforce_output(tmp_path, 1)


@pytest.mark.parametrize("error", ["MemoryError", "OSError", "TimeoutError", "BudgetExceeded"])
def test_alias_infrastructure_errors_are_never_semantic_rejections(error: str) -> None:
    assert TOOL.disposition("C04", {"returned": False, "error_type": error,
                                    "error": "failure"}, {}) == "incomplete_load_infrastructure"


def test_interrupted_saveback_retains_accepted_primary_and_observed_entries(tmp_path: Path) -> None:
    folder = tmp_path / "cases/C01"
    folder.mkdir(parents=True)
    TOOL.write_json(folder / "primary-attempt.json", {"status": "about_to_invoke"})
    TOOL.write_json(folder / "primary-result.json", {"returned": True})
    for name, phase, event in [("integrated_load", "primary-load", "call_intent"),
                               ("direct_reconstruct", "primary-load", "return"),
                               ("integrated_load", "primary-load", "return"),
                               ("direct_reconstruct", "save-back", "call_intent")]:
        TOOL.append_jsonl(folder / "milestones.jsonl", {"name": name, "phase": phase,
                                                        "event": event})
    row = TOOL.collect_case(tmp_path, "C01", {"status": "timed_out", "returncode": -9})
    assert row["primary_load"]["returned"] is True
    assert row["primary_calls_completed_observed"] == 1
    assert row["direct_reconstructions_completed_observed"] == 1
    assert row["save_back"] == {"status": "not_completed", "phase_started": True}
    assert row["observations_may_be_incomplete"] is True
    assert row["status"] == "incomplete_worker"


def test_preparation_failure_retains_every_planned_row(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "preflight", lambda *args: {"source_commit": "a" * 40})
    monkeypatch.setattr(TOOL, "retained_fixture",
                        lambda *args: (_ for _ in ()).throw(OSError("synthetic prep failure")))
    monkeypatch.setattr(TOOL, "runtime_imports", lambda: pytest.fail("no runtime import"))
    args = SimpleNamespace(output=tmp_path / "new", source_commit="a" * 40, output_created=False)
    with pytest.raises(OSError, match="synthetic prep failure"):
        TOOL.run(args, TOOL.load_protocol())
    planned = json.loads((args.output / "planned-matrix.json").read_bytes())
    summary = json.loads((args.output / "summary.json").read_bytes())
    assert len(planned) == len(summary["cases"]) == 10
    assert all(row["status"] == "blocked_controller_failure" for row in summary["cases"])
    assert summary["primary_integrated_loads_completed_observed"] == 0
    assert summary["counts_are_lower_bounds"] is False


def test_stale_mutant_is_rejected_before_runtime_import(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "_BUDGET", None)
    base = synthetic_fixture(tmp_path / "base-fixture")
    reference = tmp_path / "case-inputs/C03"
    shutil.copytree(base, reference)
    before = TOOL.inventory(base)
    TOOL.write_json(tmp_path / "mutations/C03.json", {"before": before, "after": before})
    (reference / "world-state.json").write_bytes(b"stale mutation")
    keys = ("source_commit", "source_tree", "runner_sha256", "protocol_sha256", "inputs_sha256",
            "runtime_source_files_sha256", "schema_assets_sha256", "python", "executable")
    metadata = {key: key for key in keys}
    TOOL.write_json(tmp_path / "STARTED.json", metadata)
    monkeypatch.setattr(TOOL, "preflight", lambda *args: metadata)
    monkeypatch.setattr(TOOL, "apply_limits", lambda *args: None)
    monkeypatch.setattr(TOOL, "load_inputs", lambda: {"retained_fixture": {"files": before}})
    monkeypatch.setattr(TOOL, "runtime_imports", lambda: pytest.fail("no runtime import"))
    args = SimpleNamespace(output=tmp_path / "cases/C03", output_created=False,
                           root=tmp_path, source_commit="a" * 40, mode="case", case_id="C03",
                           reference=reference, deadline=time.monotonic() + 30)
    with pytest.raises(ValueError, match="frozen parent mutation inventory"):
        TOOL.worker(args, TOOL.load_protocol())


def test_bounded_pipe_capture_stops_without_retaining_overflow(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "_BUDGET", (tmp_path, 1024, time.monotonic() + 30))
    result = TOOL.capped_subprocess([sys.executable, "-c", "print('x'*2048)"],
                                    tmp_path, "synthetic", 10)
    assert result["status"] == "budget_exceeded"
    assert result["stdout_stderr_may_be_truncated"] is True
    assert TOOL.retained_bytes(tmp_path) <= 1024


def test_parent_artifact_writes_obey_overall_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "_BUDGET", (tmp_path, 1024, time.monotonic() - 1))
    with pytest.raises(TOOL.BudgetExceeded, match="deadline"):
        TOOL.write_json(tmp_path / "late.json", {})
    assert not (tmp_path / "late.json").exists()


def test_sink_failure_preserves_underlying_return_and_reports_measurement_error() -> None:
    class Fake:
        @staticmethod
        def load():
            return "accepted-session"

    original = inspect.getattr_static(Fake, "load")
    events, errors = [], []

    def sink(event):
        if event["event"] == "return":
            raise OSError("synthetic journal failure")

    with TOOL.milestones([("integrated_load", Fake, "load")], events, ["primary-load"],
                         sink, errors):
        assert Fake.load() == "accepted-session"
        with pytest.raises(TOOL.ObservationFailure, match="before next admitted"):
            Fake.load()
    assert inspect.getattr_static(Fake, "load") is original
    assert errors[0]["error_type"] == "OSError"
    assert TOOL.event_count(events, "integrated_load") == 1
    assert [e["event"] for e in events] == ["call_intent", "return"]


def test_sink_failure_preserves_underlying_exception() -> None:
    class Fake:
        @staticmethod
        def load():
            raise ValueError("underlying loader rejection")

    errors = []

    def sink(event):
        if event["event"] == "error":
            raise OSError("journal failed")

    with TOOL.milestones([("load", Fake, "load")], [], ["primary-load"], sink, errors):
        with pytest.raises(ValueError, match="underlying loader rejection"):
            Fake.load()
    assert errors[0]["error_type"] == "OSError"


def test_pipe_overflow_latches_stop_even_if_retained_bytes_are_small(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(TOOL, "preflight", lambda *args: {"source_commit": "a" * 40})
    template = synthetic_fixture(tmp_path / "template")
    frozen = {"retained_fixture": {
        "archive_sha256": TOOL.load_protocol()["reused_fixture"]["archive_sha256"],
        "files": TOOL.inventory(template)}}
    monkeypatch.setattr(TOOL, "load_inputs", lambda: frozen)

    def fixture(path):
        shutil.copytree(template, path)
        return frozen["retained_fixture"]

    calls = []

    def overflow(command, root, name, timeout):
        calls.append(name)
        return {"name": name, "status": "budget_exceeded", "returncode": -9,
                "stdout_stderr_may_be_truncated": True}

    monkeypatch.setattr(TOOL, "retained_fixture", fixture)
    monkeypatch.setattr(TOOL, "capped_subprocess", overflow)
    args = SimpleNamespace(output=tmp_path / "new", source_commit="a" * 40, output_created=False)
    with pytest.raises(TOOL.BudgetExceeded, match="no later worker admitted"):
        TOOL.run(args, TOOL.load_protocol())
    assert calls == ["setup"]
    summary = json.loads((args.output / "summary.json").read_bytes())
    assert len(summary["cases"]) == 10
    assert all(row["status"] == "blocked_controller_failure" for row in summary["cases"])
    assert summary["output_threshold_exceeded"] is False
    assert summary["status"] == "incomplete"


@pytest.mark.parametrize("phase", ["setup", "save-back"])
def test_final_save_validation_measurement_failure_keeps_actual_outcomes(phase: str) -> None:
    class Fake:
        @staticmethod
        def validate_save():
            return "complete-saved-bytes"

    events, errors = [], []

    def sink(event):
        if event["event"] == "return":
            raise OSError("final validation journal failed")

    with TOOL.milestones([("direct_reconstruct", Fake, "validate_save")],
                         events, [phase], sink, errors):
        assert Fake.validate_save() == "complete-saved-bytes"
    result = {"status": "completed", "primary_load": {"returned": True},
              "save_back": {"status": "completed", "equal": True}}
    TOOL.mark_measurement(result, errors)
    assert result["status"] == "incomplete_instrumentation"
    assert result["primary_load"]["returned"] is True
    assert result["save_back"] == {"status": "completed", "equal": True}
    assert TOOL.event_count(events, "direct_reconstruct", phase) == 1

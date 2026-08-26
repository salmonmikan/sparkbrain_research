"""C16 execution guards and transport tests; never execute official models."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
runner = importlib.import_module("scripts.run_c16_concepts")
release_mode = importlib.import_module("sparkbrain.release").release_mode

PIN = "a" * 40


def protocol() -> dict:
    value = json.loads(runner.DEFAULT_PROTOCOL.read_text(encoding="utf-8"))
    # This explicit synthetic base remains valid after the real pin amendment.
    value.pop("base_commit", None)
    value.pop("base_sha256", None)
    value["source_commit"] = None
    value["runner_execution_allowed"] = False
    return value


def amended() -> dict:
    value = protocol()
    value.update(
        base_commit=runner.BASE_PROTOCOL_COMMIT,
        base_sha256=runner.BASE_PROTOCOL_SHA256,
        source_commit=PIN,
        runner_execution_allowed=True,
    )
    return value


def bundle(value: dict | None = None) -> dict:
    value = protocol() if value is None else value
    return {
        "protocol.json": value,
        "candidate_lineage.jsonl": [],
        "candidate_metrics.json": {
            "failed_seeds": [],
            "engineering_gates": [{"passed": True}],
            "scientific_stage_status": {"CC0": "not_supported"},
        },
        "held_out_utility.json": {},
        "causal_interventions.jsonl": [],
        "matched_controls.json": {},
        "failure_examples.jsonl": [],
        "report.md": "# Synthetic only\n",
    }


def call_run(output: Path) -> dict:
    return runner.run(
        root=ROOT, protocol_path=runner.DEFAULT_PROTOCOL, output=output, source_commit=PIN
    )


def test_protocol_amendment_exact_four_root_fields() -> None:
    base = protocol()
    current = amended()
    runner._validate_protocol_amendment(current, base)
    for key, value in (("unknown", True), ("run_id", "mutated")):
        changed = copy.deepcopy(current)
        changed[key] = value
        with pytest.raises(RuntimeError, match="unauthorized|beyond"):
            runner._validate_protocol_amendment(changed, base)
    changed = copy.deepcopy(current)
    changed["seeds"]["run_seeds"][0] = 99016
    with pytest.raises(RuntimeError, match="beyond"):
        runner._validate_protocol_amendment(changed, base)
    with pytest.raises(RuntimeError, match="unamended"):
        runner._validate_protocol_amendment(current, current)


@pytest.mark.parametrize(
    "path,replacement",
    [
        (("formation", "capacity"), 8.0),
        (("seeds", "bootstrap_seed"), 4366.0),
        (("scope", "sensory_config", "max_active"), 8.0),
        (("formation", "top_k"), True),
    ],
)
def test_protocol_amendment_rejects_python_equal_json_type_changes(path, replacement):
    base = protocol()
    current = amended()
    parent = current
    for key in path[:-1]:
        parent = parent[key]
    original = parent[path[-1]]
    assert original == replacement and type(original) is not type(replacement)
    parent[path[-1]] = replacement
    with pytest.raises(RuntimeError, match="beyond the authorized pin"):
        runner._validate_protocol_amendment(current, base)


def test_disabled_guard_precedes_git_fixture_and_output(tmp_path, monkeypatch) -> None:
    path = tmp_path / runner.PROTOCOL_RELATIVE
    path.parent.mkdir(parents=True)
    path.write_text(runner._canonical(protocol()), encoding="utf-8")

    def forbidden(*args, **kwargs):
        pytest.fail("disabled runner reached Git/fixture/output")

    for name in ("_git", "_git_bytes", "_validate_fixture_hashes", "_validate_output_path"):
        monkeypatch.setattr(runner, name, forbidden)
    output = tmp_path / "absent"
    with pytest.raises(RuntimeError, match="disabled"):
        runner._preflight(root=tmp_path, protocol_path=path, output=output, source_commit=PIN)
    assert not output.exists()


def test_noncanonical_protocol_rejected_before_read(tmp_path) -> None:
    with pytest.raises(RuntimeError, match="canonical path"):
        runner._preflight(
            root=tmp_path,
            protocol_path=tmp_path / "alternative.json",
            output=tmp_path / "out",
            source_commit=PIN,
        )


@pytest.mark.parametrize("payload", [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b"[]"])
def test_strict_json_rejects_duplicate_nonfinite_and_nonobject(payload) -> None:
    with pytest.raises(ValueError):
        runner._decode(payload)


@pytest.mark.parametrize("tamper", ["working", "base", "pin", "root_base"])
def test_protocol_authenticity_fail_closed(tmp_path, monkeypatch, tamper) -> None:
    value = amended()
    if tamper == "pin":
        value["source_commit"] = "b" * 40
    if tamper == "root_base":
        value["base_commit"] = "b" * 40
    path = tmp_path / runner.PROTOCOL_RELATIVE
    path.parent.mkdir(parents=True)
    payload = runner._canonical(value).encode()
    path.write_bytes(payload)
    monkeypatch.setattr(runner, "_git", lambda *args: "")
    monkeypatch.setattr(
        runner,
        "_git_bytes",
        lambda root, *args: (
            b"tampered"
            if tamper == "working" or args[-1].startswith(runner.BASE_PROTOCOL_COMMIT)
            else payload
        ),
    )
    with pytest.raises(RuntimeError, match="bytes|blob hash|registered pin|base pin"):
        runner._preflight(
            root=tmp_path, protocol_path=path, output=tmp_path / "out", source_commit=PIN
        )
    assert not (tmp_path / "out").exists()


@pytest.mark.parametrize(
    "tamper", [None, "missing", "extra", "after", "working", "bytes", "untracked"]
)
def test_source_exact_scope_and_working_pin(tmp_path, monkeypatch, tamper) -> None:
    value = amended()
    paths = value["source_control"]["expected_new_source_and_test_paths"]
    for relative in paths:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"synthetic pinned bytes")
    if tamper == "bytes":
        (tmp_path / paths[0]).write_bytes(b"dirty")

    def git(root, *args):
        if args[0] == "ls-files":
            return "src/shadow.py" if tamper == "untracked" else ""
        if args[:2] == ("diff", "--name-only"):
            if args[2:] == (runner.BASE_PROTOCOL_COMMIT, PIN):
                changed = paths[:-1] if tamper == "missing" else paths
                return "\n".join(changed + (["src/unauthorized.py"] if tamper == "extra" else []))
            if args[2:] == (PIN, "HEAD"):
                return "src/unauthorized.py" if tamper == "after" else ""
            return "src/unauthorized.py" if tamper == "working" else ""
        return ""

    monkeypatch.setattr(runner, "_git", git)
    monkeypatch.setattr(runner, "_git_bytes", lambda *args: b"synthetic pinned bytes")
    if tamper is None:
        runner._validate_source_scope(root=tmp_path, protocol=value, source_commit=PIN)
    else:
        with pytest.raises(RuntimeError, match="source|paths|pin"):
            runner._validate_source_scope(root=tmp_path, protocol=value, source_commit=PIN)


@pytest.mark.skipif(
    release_mode(ROOT) == "archive",
    reason="C16 source-commit hash pins require the retained stage checkout",
)
def test_protected_manifests_and_tamper(tmp_path) -> None:
    value = protocol()["source_control"]
    runner._validate_hash_manifest(ROOT, value["protected_hash_manifest"], count=29)
    runner._validate_hash_manifest(ROOT, value["runtime_source_pins"], count=4)
    target = tmp_path / "protected.txt"
    target.write_bytes(b"protected")
    manifest = {target.name: hashlib.sha256(target.read_bytes()).hexdigest()}
    runner._validate_hash_manifest(tmp_path, manifest, count=1)
    target.write_bytes(b"tampered")
    with pytest.raises(RuntimeError, match="hash mismatch"):
        runner._validate_hash_manifest(tmp_path, manifest, count=1)
    with pytest.raises(RuntimeError, match="cardinality"):
        runner._validate_hash_manifest(tmp_path, manifest, count=2)


def test_thirty_pure_fixture_hashes_and_mismatch() -> None:
    # Hash construction only: never feed official fixtures to a model or sensory field.
    value = protocol()
    runner._validate_fixture_hashes(value)
    value["seeds"]["full_fixture_sha256_by_run_seed_and_split"]["3601"]["train"] = "0" * 64
    with pytest.raises(RuntimeError, match="full fixture hash"):
        runner._validate_fixture_hashes(value)


@pytest.mark.parametrize("tamper", ["extra", "missing", "protocol", "type", "nan", "nested"])
def test_bundle_validation_precedes_writes(tmp_path, monkeypatch, tamper) -> None:
    evaluation = importlib.import_module("sparkbrain.v03_concepts.evaluation")
    value = protocol()
    data = bundle(value)
    if tamper == "extra":
        data["unexpected.json"] = {}
    elif tamper == "missing":
        del data["report.md"]
    elif tamper == "protocol":
        data["protocol.json"] = {}
    elif tamper == "type":
        data["candidate_lineage.jsonl"] = {}
    elif tamper == "nan":
        data["held_out_utility.json"] = {"value": float("nan")}

    def validate(*args):
        if tamper == "nested":
            raise ValueError("synthetic nested schema rejection")

    monkeypatch.setattr(evaluation, "generate_bundle", lambda *args: data)
    monkeypatch.setattr(evaluation, "validate_bundle", validate)
    with pytest.raises((RuntimeError, ValueError)):
        runner._generate(output=tmp_path, protocol=value, source_commit=PIN)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("existing", [False, True])
def test_exact_eight_atomic_publish_and_zero_byte_jsonl(tmp_path, monkeypatch, existing) -> None:
    output = tmp_path / "result"
    if existing:
        output.mkdir()
    value = protocol()
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: value)

    def generate(*, output, **kwargs):
        runner._write_bundle(output, bundle(value))
        return runner._bundle_status(bundle(value))

    monkeypatch.setattr(runner, "_generate_isolated", generate)
    result = call_run(output)
    assert result["engineering_passed"] is True
    assert {item.name for item in output.iterdir()} == runner.EXPECTED_FILES
    for path in output.iterdir():
        if path.suffix == ".jsonl":
            assert path.read_bytes() == b""
        elif path.suffix == ".json":
            assert (
                path.read_bytes()
                == (runner._canonical(json.loads(path.read_bytes())) + "\n").encode()
            )
    assert list(tmp_path.glob(".result.staging-*")) == []


def test_nonempty_output_preserved(tmp_path, monkeypatch) -> None:
    output = tmp_path / "result"
    output.mkdir()
    marker = output / "user.txt"
    marker.write_text("keep", encoding="utf-8")
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: protocol())
    monkeypatch.setattr(runner, "_generate_isolated", lambda **kwargs: pytest.fail("generation"))
    with pytest.raises(RuntimeError, match="new or empty"):
        call_run(output)
    assert marker.read_text(encoding="utf-8") == "keep"


@pytest.mark.parametrize("concurrent_file", [False, True])
def test_publish_replace_failure_restores_empty_or_preserves_concurrent_file(
    tmp_path, monkeypatch, concurrent_file
):
    output = tmp_path / "publish-failure"
    output.mkdir()
    value = protocol()
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: value)

    def generate(*, output, **kwargs):
        runner._write_bundle(output, bundle(value))
        return runner._bundle_status(bundle(value))

    def fail_replace(self, target):
        assert target == output
        assert not output.exists()
        if concurrent_file:
            output.write_bytes(b"concurrent user file")
        raise OSError("synthetic atomic rename failure")

    monkeypatch.setattr(runner, "_generate_isolated", generate)
    monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(OSError, match="atomic rename failure"):
        call_run(output)
    if concurrent_file:
        assert output.read_bytes() == b"concurrent user file"
    else:
        assert output.is_dir()
        assert list(output.iterdir()) == []
    assert list(tmp_path.glob(".publish-failure.staging-*")) == []


def test_publish_revalidates_concurrent_nonempty_output(tmp_path, monkeypatch):
    output = tmp_path / "publish-race"
    output.mkdir()
    value = protocol()
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: value)

    def generate(*, output: Path, **kwargs):
        runner._write_bundle(output, bundle(value))
        (tmp_path / "publish-race" / "user.txt").write_bytes(b"keep concurrent data")
        return runner._bundle_status(bundle(value))

    monkeypatch.setattr(runner, "_generate_isolated", generate)
    with pytest.raises(RuntimeError, match="new or empty"):
        call_run(output)
    assert (output / "user.txt").read_bytes() == b"keep concurrent data"
    assert list(tmp_path.glob(".publish-race.staging-*")) == []


@pytest.mark.parametrize("existing", [False, True])
def test_forced_failure_cleans_staging_preserves_empty_final(
    tmp_path, monkeypatch, existing
) -> None:
    output = tmp_path / "failure"
    if existing:
        output.mkdir()
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: protocol())

    def fail(*, output, **kwargs):
        (output / "partial.json").write_bytes(b"{}")
        raise RuntimeError("injected")

    monkeypatch.setattr(runner, "_generate_isolated", fail)
    with pytest.raises(RuntimeError, match="injected"):
        call_run(output)
    assert output.exists() is existing
    assert list(tmp_path.glob(".failure.staging-*")) == []
    if existing:
        assert list(output.iterdir()) == []


@pytest.mark.parametrize("existing", [False, True])
def test_real_spawn_timeout_does_not_publish(tmp_path, monkeypatch, existing) -> None:
    output = tmp_path / "timeout"
    if existing:
        output.mkdir()
    context = multiprocessing.get_context("spawn")
    workers = []

    def sleeping_process(**kwargs):
        worker = context.Process(target=time.sleep, args=(30,), daemon=True)
        workers.append(worker)
        return worker

    monkeypatch.setattr(
        runner.multiprocessing,
        "get_context",
        lambda method: SimpleNamespace(Pipe=context.Pipe, Process=sleeping_process),
    )
    value = protocol()
    value["failure_and_resource_contract"]["timeout_seconds"] = 0.1
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: value)
    started = time.monotonic()
    with pytest.raises(runner.C16RunTimeoutError, match="deadline"):
        call_run(output)
    assert time.monotonic() - started < 15
    assert workers[0]._closed
    assert output.exists() is existing
    assert list(tmp_path.glob(".timeout.staging-*")) == []


def test_late_exit_and_frozen_escalation(monkeypatch) -> None:
    calls = []
    worker = SimpleNamespace(
        exitcode=None,
        join=lambda seconds: calls.append(("join", seconds)),
        is_alive=lambda: True,
        terminate=lambda: calls.append(("terminate",)),
        kill=lambda: calls.append(("kill",)),
    )
    clock = iter([10.0, 11.0])
    monkeypatch.setattr(runner.time, "monotonic", lambda: next(clock))
    with pytest.raises(runner.C16RunTimeoutError) as error:
        runner._wait_for_worker(worker, deadline=10.5, grace_seconds=5)
    assert error.value.worker_alive
    assert calls == [("join", 0.5), ("terminate",), ("join", 5), ("kill",), ("join", 5)]
    calls.clear()
    clock = iter([10.0, 11.0])
    worker.exitcode = 0
    worker.is_alive = lambda: False
    with pytest.raises(runner.C16RunTimeoutError):
        runner._wait_for_worker(worker, deadline=10.5, grace_seconds=5)
    assert calls == [("join", 0.5)]


@pytest.mark.parametrize("broken_method", ["terminate", "kill", "join", "is_alive"])
def test_process_control_error_quarantines(tmp_path, monkeypatch, broken_method, capsys) -> None:
    def fail(*args):
        raise OSError("synthetic control error")

    worker = SimpleNamespace(
        start=lambda: None,
        exitcode=None,
        join=lambda seconds: None,
        terminate=lambda: None,
        kill=lambda: None,
        is_alive=lambda: True,
    )
    setattr(worker, broken_method, fail)
    pipe = SimpleNamespace(close=lambda: None)
    context = SimpleNamespace(Process=lambda **kwargs: worker, Pipe=lambda **kwargs: (pipe, pipe))
    monkeypatch.setattr(runner.multiprocessing, "get_context", lambda method: context)
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: protocol())
    output = tmp_path / "quarantine"
    with pytest.raises(runner.C16WorkerError) as error:
        call_run(output)
    assert error.value.worker_alive
    stages = list(tmp_path.glob(".quarantine.staging-*"))
    assert len(stages) == 1
    assert str(stages[0].resolve()) in capsys.readouterr().err
    assert not output.exists()


@pytest.mark.parametrize("alive", [False, True])
def test_timeout_cli_124_and_live_worker_atexit_bypass(monkeypatch, alive) -> None:
    def fail(**kwargs):
        raise runner.C16RunTimeoutError("deadline", worker_alive=alive)

    def exit_now(code):
        raise SystemExit(code)

    monkeypatch.setattr(runner, "run", fail)
    monkeypatch.setattr(runner.os, "_exit", exit_now)
    monkeypatch.setattr(sys, "argv", ["runner", "--output", "unused", "--source-commit", PIN])
    if alive:
        with pytest.raises(SystemExit) as result:
            runner.main()
        assert result.value.code == 124
    else:
        assert runner.main() == 124


def test_actual_generation_worker_spawn_importable_without_models() -> None:
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    # Argument binding fails before generation: actual Windows spawn import path only.
    worker = context.Process(target=runner._generation_worker, args=(sender, {}), daemon=True)
    try:
        deadline = time.monotonic() + 10
        worker.start()
        sender.close()
        runner._wait_for_worker(worker, deadline=deadline, grace_seconds=5)
        assert worker.exitcode == 1
        with pytest.raises((EOFError, OSError)):
            receiver.recv()
    finally:
        runner._stop_worker(worker, grace_seconds=5)
        worker.close()
        sender.close()
        receiver.close()


def _synthetic_generation_worker(connection, arguments):
    """Picklable reserved transport worker; no fixture, sensory, or learned call."""
    try:
        data = bundle(arguments["protocol"])
        runner._write_bundle(arguments["output"], data)
        connection.send(runner._bundle_status(data))
    finally:
        connection.close()


def test_spawn_supervisor_receives_small_status_and_publishes(tmp_path, monkeypatch):
    context = multiprocessing.get_context("spawn")

    def synthetic_process(**kwargs):
        kwargs["target"] = _synthetic_generation_worker
        return context.Process(**kwargs)

    monkeypatch.setattr(
        runner.multiprocessing,
        "get_context",
        lambda method: SimpleNamespace(Pipe=context.Pipe, Process=synthetic_process),
    )
    value = protocol()
    value["seeds"]["run_seeds"] = [99016]
    value["failure_and_resource_contract"]["timeout_seconds"] = 15
    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: value)
    output = tmp_path / "spawn-success"
    result = call_run(output)
    assert result["engineering_passed"] is True
    assert len(list(output.iterdir())) == 8


@pytest.mark.parametrize(
    "passed,failed,expected", [(True, [], 0), (False, [], 2), (False, [{"run_seed": 99016}], 2)]
)
def test_completed_result_cli_codes(monkeypatch, passed, failed, expected):
    monkeypatch.setattr(
        runner,
        "run",
        lambda **kwargs: {
            "engineering_passed": passed,
            "failed_seeds": failed,
            "scientific_stage_status": {"CC0": {"status": "not_supported"}},
        },
    )
    monkeypatch.setattr(sys, "argv", ["runner", "--output", "unused", "--source-commit", PIN])
    assert runner.main() == expected


def test_synthetic_canonical_transport_reproducible_across_hash_seeds(tmp_path) -> None:
    # Child processes construct only a synthetic transport bundle, not registered fixtures.
    code = (
        "import sys; from pathlib import Path; "
        "from scripts.run_c16_concepts import _write_bundle, EXPECTED_FILES; "
        "p=Path(sys.argv[1]); p.mkdir(); "
        "b={n: ('synthetic\\n' if n.endswith('.md') else "
        "[{'reserved_seed':99016,'visible':'synthetic'}] if n.endswith('.jsonl') "
        "else {k:k for k in {'z','a','m'}}) for n in EXPECTED_FILES}; _write_bundle(p,b)"
    )
    outputs = []
    for seed in ("17", "37"):
        output = tmp_path / seed
        environment = dict(os.environ, PYTHONHASHSEED=seed, PYTHONPATH=str(ROOT / "src"))
        subprocess.run(
            [sys.executable, "-c", code, str(output)],
            cwd=ROOT,
            env=environment,
            check=True,
            timeout=20,
            capture_output=True,
        )
        outputs.append({path.name: path.read_bytes() for path in output.iterdir()})
    assert set(outputs[0]) == runner.EXPECTED_FILES
    assert outputs[0] == outputs[1]


def all_failed_bundle(monkeypatch):
    evaluation = importlib.import_module("sparkbrain.v03_concepts.evaluation")
    value = protocol()
    value["seeds"]["run_seeds"] = list(range(99016, 99021))
    seen = []

    def fail(protocol, source_commit, seed, location):
        seen.append(seed)
        location["phase"] = "fixture"
        raise ValueError("synthetic failure text must not be retained")

    monkeypatch.setattr(evaluation, "_run_seed", fail)
    data = evaluation.generate_bundle(value, PIN)
    assert seen == value["seeds"]["run_seeds"]
    return value, data


def test_all_failed_seed_bundle_exact_eight_real_validator_and_transport(tmp_path, monkeypatch):
    value, data = all_failed_bundle(monkeypatch)
    runner._validate_bundle(data, value, PIN)
    status = runner._bundle_status(data)
    assert status["engineering_passed"] is False
    assert status["engineering_status"] == "implementation_failure"
    failures = data["candidate_metrics.json"]["failed_seeds"]
    assert len(failures) == 5
    assert all(
        set(row) == set(value["failure_and_resource_contract"]["failed_seed_fields"])
        for row in failures
    )
    for name in ("held_out_utility.json", "matched_controls.json"):
        assert data[name]["failed_seeds"] == failures
    assert data["candidate_metrics.json"]["bank_rows"] == []
    assert data["candidate_metrics.json"]["representation_checkpoints"] == []
    assert data["held_out_utility.json"]["aggregate_rows"] == []
    assert data["matched_controls.json"]["aggregate_comparisons"] == []
    assert all(
        row["status"] == "not_evaluated_implementation_failure"
        for row in status["scientific_stage_status"].values()
    )
    assert "synthetic failure text" not in runner._canonical(data)
    runner._write_bundle(tmp_path, data)
    assert {path.name for path in tmp_path.iterdir()} == runner.EXPECTED_FILES
    assert all(path.stat().st_size == 0 for path in tmp_path.glob("*.jsonl"))


@pytest.mark.parametrize(
    "tamper",
    [
        "unknown",
        "failure_hash",
        "failure_order",
        "common_failures",
        "aggregate",
        "grade",
        "engineering",
        "report",
        "nonfinite",
    ],
)
def test_actual_validator_rejects_failure_schema_and_derived_tamper(monkeypatch, tamper):
    value, data = all_failed_bundle(monkeypatch)
    metrics = data["candidate_metrics.json"]
    if tamper == "unknown":
        metrics["unknown"] = True
    elif tamper == "failure_hash":
        metrics["failed_seeds"][0]["error_hash"] = "0" * 64
    elif tamper == "failure_order":
        metrics["failed_seeds"].reverse()
    elif tamper == "common_failures":
        data["held_out_utility.json"]["failed_seeds"] = []
    elif tamper == "aggregate":
        data["held_out_utility.json"]["aggregate_rows"] = [{}]
    elif tamper == "grade":
        metrics["scientific_stage_status"]["CC0"]["status"] = "supported"
    elif tamper == "engineering":
        gate = metrics["engineering_gates"][0]
        gate["passed"] = not gate["passed"]
    elif tamper == "report":
        data["report.md"] += "invented result"
    elif tamper == "nonfinite":
        data["matched_controls.json"]["aggregate_comparisons"] = [{"effect": float("nan")}]
    with pytest.raises((RuntimeError, ValueError)):
        runner._validate_bundle(data, value, PIN)

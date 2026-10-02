"""Model-free orchestration checks; no SparkBrain/runtime import or model construction."""

from __future__ import annotations

import copy
import importlib.abc
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "retention_runner_test", ROOT / "scripts/run_plasticity_retention.py"
)
assert SPEC and SPEC.loader
R = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R)


class BlockRuntime(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("test must not import SparkBrain")
        return None


@pytest.fixture(autouse=True)
def no_runtime():
    blocker = BlockRuntime()
    sys.meta_path.insert(0, blocker)
    yield
    sys.meta_path.remove(blocker)


def test_published_inputs_are_independently_pinned():
    protocol, inputs, jobs, prefixes = R.check_preparation()
    assert sum(j["pairs"] for j in jobs["jobs"]) == 768
    assert sum(j["pairs"] for j in jobs["jobs"] if j["family"] == "v05") == 512
    totals = {
        k: sum(R.call_limits(j)[k] for j in jobs["jobs"]) for k in R.call_limits(jobs["jobs"][0])
    }
    assert totals == {
        "wrapper_load": 26,
        "wrapper_init": 26,
        "v05_init": 36,
        "native_load": 18,
        "predict": 768,
        "outcome": 768,
        "v05_episode": 512,
        "apply": 512,
        "v05_outcome": 512,
    }
    assert protocol["execution_authorized"] is False
    assert len(inputs["streams"]) == 6 and len(prefixes["prefixes"]) == 6
    with pytest.raises(RuntimeError, match="not admitted"):
        R.predecessor()


def test_tampered_preparation_rejected_before_runtime(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "PROTOCOL", tmp_path / "protocol.json")
    R.PROTOCOL.write_text("{}")
    with pytest.raises(RuntimeError, match="independent protocol"):
        R.check_preparation()


def test_unapproved_gate_rejects_without_any_model(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "verify_freeze", lambda path: {})
    monkeypatch.setattr(R, "git", lambda *args: b"head\n")
    (tmp_path / "manifest.json").write_text("{}")
    digest = R.S.sha(tmp_path / "manifest.json")
    paths = []
    for kind, flag in (
        ("review", "source_review_approved"),
        ("publication", "verified_published"),
        ("approval", "approved_for_execution"),
    ):
        path = tmp_path / (kind + ".json")
        path.write_text(
            json.dumps(
                {
                    flag: kind != "approval",
                    "source_commit": "head",
                    "manifest_sha256": digest,
                    "output_root": str(R.S.PLANNED_OUTPUT),
                    "ceiling_pairs": 768,
                    "record_url": "test-only",
                    "recorded_by": "test-only",
                }
            )
        )
        paths.append(path)
    with pytest.raises(RuntimeError, match="execution not approved"):
        R.gate(tmp_path, *paths)


def test_actual_loaded_modules_require_frozen_origin(monkeypatch, tmp_path):
    # Restrict inventory to one synthetic module; no runtime imports.
    module = type(sys)("synthetic_unbound")
    module.__file__ = str(tmp_path / "unbound.py")
    (tmp_path / "unbound.py").write_text("pass\n")
    monkeypatch.setattr(R.sys, "modules", {"synthetic_unbound": module})
    with pytest.raises(RuntimeError, match="outside frozen origins"):
        R.loaded_bindings({"sources": {}}, {"stdlib_path": str(tmp_path / "stdlib")})


def test_supervisor_direct_invocation_denied(monkeypatch, tmp_path):
    monkeypatch.setattr(R.S, "validate_output_roots", lambda path: None)
    with pytest.raises(RuntimeError, match="inherited driver supervision"):
        R.S.accept_supervision(None, {}, tmp_path)


def envelope(job, directory):
    return {
        "schema": "retention-supervision-1",
        "parent_pid": 123,
        "job_sha256": R.S.digest(job),
        "directory": str(directory.resolve()),
        "output_root": str(R.S.PLANNED_OUTPUT),
        "cpu_limit": 3,
        "wall_limit": 5,
        "issued_monotonic": 10,
        "wall_stop_monotonic": 15,
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("parent_pid", 124),
        ("job_sha256", "bad"),
        ("cpu_limit", 17),
        ("wall_limit", float("inf")),
        ("wall_stop_monotonic", 16),
    ],
)
def test_supervisor_rejects_unbound_envelope(field, value, tmp_path):
    job = {"cpu_limit": 3, "wall_limit": 5}
    header = envelope(job, tmp_path)
    header[field] = value
    with pytest.raises(RuntimeError):
        R.S.validate_supervisor_envelope(header, job, tmp_path, parent_pid=123, now=11)


def test_supervisor_accepts_bounded_exact_envelope(tmp_path):
    job = {"cpu_limit": 3, "wall_limit": 5}
    assert R.S.validate_supervisor_envelope(
        envelope(job, tmp_path), job, tmp_path, parent_pid=123, now=11
    ) == (3, 4)


def test_worker_body_with_synthetic_memory_only(monkeypatch, tmp_path):
    protocol, inputs, jobs, prefixes = R.check_preparation()
    plan = next(j for j in jobs["jobs"] if j["arm"] == "H")
    prefix = tmp_path / "prefix"
    prefix.mkdir()
    original = {
        "arm": "H",
        "counts": [0, 0],
        "memory": [],
        "prototypes": [],
        "pending": None,
        "receipts": {str(i): 0 for i in range(64)},
    }
    (prefix / "wrapper.json").write_text(json.dumps(original))

    class NoBrain:
        def __init__(self):
            raise AssertionError("no fake brain construction either")

        @classmethod
        def load_checkpoint(cls, path):
            raise AssertionError("no brain load")

        def process_episode(self):
            raise AssertionError("no episode")

        def learn_outcome(self):
            raise AssertionError("no brain outcome")

    class FakeMemory:
        def __init__(self):
            self.brain = None
            self.__dict__.update(copy.deepcopy(original))

        @classmethod
        def load(cls, path):
            return cls()

        def state(self):
            return {k: getattr(self, k) for k in original}

        def predict(self, obs):
            self.pending = {"id": obs["occurrence_id"]}
            return {
                "p1": 0.5,
                "native": None,
                "occurrence_id": obs["occurrence_id"],
                "input_sha256": R.S.digest(obs),
                "query_time_ms": obs["start_ms"] + 72,
            }

        def outcome(self, key, value):
            self.receipts[key] = value
            self.pending = None
            return True

    monkeypatch.setattr(
        R, "predecessor", lambda: SimpleNamespace(Model=FakeMemory, IntegratedV05Brain=NoBrain)
    )
    monkeypatch.setattr(R, "verify_freeze", lambda path: {"sources": {}})
    monkeypatch.setattr(R, "loaded_bindings", lambda *args: {"synthetic": "test-only"})
    monkeypatch.setattr(R, "verify_prefix", lambda *args: prefix)
    monkeypatch.setattr(
        R, "validate_job", lambda *args: (plan, inputs["streams"][plan["stream"]], prefix)
    )
    monkeypatch.setattr(R, "_MODEL_ADMISSION", False)
    monkeypatch.setattr(R.sys, "path", list(sys.path))
    freeze = tmp_path / "freeze"
    freeze.mkdir()
    for name in ("manifest", "dependencies"):
        (freeze / (name + ".json")).write_text("{}")
    directory = tmp_path / "job"
    directory.mkdir()
    job = {
        "plan": plan,
        "freeze": str(freeze),
        "binding": {"manifest_sha256": R.S.sha(freeze / "manifest.json")},
        "record_paths": {},
    }
    writer = R.C.OutputWriter(tmp_path, terminal_limit=131072)
    ledger = R.C.CallLedger(lambda row: None, R.call_limits(plan))
    result = R.worker_body(job, directory, writer, ledger, {})
    assert result["completed_pairs"] == 32
    assert ledger.returns["predict"] == ledger.returns["outcome"] == 32
    assert ledger.returns["v05_init"] == 0
    assert len(R.read_jsonl(directory / "predictions.jsonl")) == 32
    assert len(R.read_jsonl(directory / "receipts.jsonl")) == 32


def test_validate_rows_rejects_short_or_unbound_inputs(tmp_path):
    _, inputs, jobs, _ = R.check_preparation()
    job = next(j for j in jobs["jobs"] if j["arm"] == "H")
    directory = tmp_path / "jobs" / job["job_id"]
    directory.mkdir(parents=True)
    for name in ("predictions", "receipts"):
        (directory / (name + ".jsonl")).write_text("{}\n")
    with pytest.raises(RuntimeError, match="completeness"):
        R.validate_rows(job, tmp_path, inputs)


def test_dummy_subprocess_capture_overflow_is_failure(monkeypatch, tmp_path):
    # A plain stdlib writer exercises supervision/capture; this is not a model worker.
    original = subprocess.Popen

    def dummy(*args, **kwargs):
        # Do not lower AS below the possibly large pytest parent before exec.
        kwargs.pop("preexec_fn")
        return original(
            [sys.executable, "-S", "-B", "-c", "import os; os.write(1,b'x'*70000)"], **kwargs
        )

    monkeypatch.setattr(R.subprocess, "Popen", dummy)
    costs = []
    writer = R.C.OutputWriter(tmp_path, terminal_limit=524288)
    job = {"plan": {"job_id": "synthetic-overflow"}, "cpu_limit": 1, "wall_limit": 3}
    with pytest.raises(RuntimeError, match="capture allowance"):
        R.launch_worker(job, tmp_path, writer, costs)
    assert len(costs) == 1
    cost = costs[0]
    assert cost["capture_retained_bytes"]["stdout"] == 65536
    assert cost["known_discarded_bytes"]["stdout"] > 0
    assert cost["unread_pipe_bytes"] == "unknown after failure"
    assert cost["worker_peak_rss_kib"] > 0


def test_dummy_subprocess_wall_timeout_is_failure(monkeypatch, tmp_path):
    original = subprocess.Popen

    def dummy(*args, **kwargs):
        # Do not lower AS below the possibly large pytest parent before exec.
        kwargs.pop("preexec_fn")
        return original([sys.executable, "-S", "-B", "-c", "import time; time.sleep(10)"], **kwargs)

    monkeypatch.setattr(R.subprocess, "Popen", dummy)
    writer = R.C.OutputWriter(tmp_path, terminal_limit=524288)
    costs = []
    job = {"plan": {"job_id": "synthetic-timeout"}, "cpu_limit": 1, "wall_limit": 0.3}
    with pytest.raises(TimeoutError, match="wall allowance"):
        R.launch_worker(job, tmp_path, writer, costs)
    assert costs[0]["timed_out"] is True
    assert costs[0]["exit_code"] < 0


def test_freeze_test_mode_does_not_import_model(monkeypatch, tmp_path):
    monkeypatch.setattr(R.S, "validate_execution_environment", lambda: None)
    monkeypatch.setattr(R.S, "dependency_inventory", lambda: {"synthetic": True})
    source = tmp_path / "source.txt"
    source.write_text("frozen synthetic source")
    monkeypatch.setattr(R, "ROOT", tmp_path)
    monkeypatch.setattr(R, "sources", lambda: [source])
    result = R.freeze(tmp_path / "freeze")
    assert result["model_calls"] == 0
    manifest = R.verify_freeze(tmp_path / "freeze")
    assert manifest["status"] == "UNEXECUTED"
    source.write_text("changed")
    with pytest.raises(RuntimeError, match="source inventory"):
        R.verify_freeze(tmp_path / "freeze")


def test_first_observables_ignore_only_nonobservable_whole_state_hash():
    row = {
        "p1": 0.5,
        "native": None,
        "assembly_id": None,
        "mature": False,
        "raw_result": {
            "state_hash": "C",
            "emitted_pulses": [],
            "v04_result": {"spikes": []},
            "patterns": [],
            "assembly_activations": [],
            "prediction": {"value": None},
        },
    }
    changed = copy.deepcopy(row)
    changed["raw_result"]["state_hash"] = "L"
    assert R.first_observables(row) == R.first_observables(changed)
    changed["raw_result"]["v04_result"]["spikes"] = [{"unit_id": 2, "time_ms": 3}]
    assert R.first_observables(row) != R.first_observables(changed)


def test_runtime_environment_check_never_treats_regular_pytest_as_execution():
    with pytest.raises(RuntimeError):
        R.S.validate_execution_environment()


def test_os_limits_match_registered_resources(monkeypatch):
    calls = []
    monkeypatch.setattr(
        R.S.resource, "setrlimit", lambda kind, values: calls.append((kind, values))
    )
    R.S.process_limits(3)
    assert calls == [
        (R.S.resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2)),
        (R.S.resource.RLIMIT_CORE, (0, 0)),
        (R.S.resource.RLIMIT_CPU, (3, 3)),
    ]


@pytest.mark.parametrize("remaining", [0, 3, 15.9, 16])
def test_child_admission_requires_full_cpu_headroom(monkeypatch, remaining):
    monkeypatch.setattr(R.S.signal, "getitimer", lambda kind: (remaining, 0))
    with pytest.raises(RuntimeError, match="headroom"):
        with R.S.reserve_child_cpu(16):
            raise AssertionError("child must not be admitted")


def test_child_cpu_reserved_before_launch_then_unused_portion_refunded(monkeypatch):
    remaining, calls = [20.0], []
    child = [10.0]
    monkeypatch.setattr(R.S.signal, "getitimer", lambda kind: (remaining[0], 0))

    def set_timer(kind, value):
        remaining[0] = value
        calls.append(value)

    monkeypatch.setattr(R.S.signal, "setitimer", set_timer)
    monkeypatch.setattr(R.S, "child_cpu", lambda: child[0])
    with R.S.reserve_child_cpu(16):
        assert remaining[0] == 4
        remaining[0] -= 0.5  # Concurrent driver work is still charged.
        child[0] += 8
    assert calls == [4, 11.5]
    assert remaining[0] == 20 - 0.5 - 8


def test_expired_parent_timer_is_not_revived_by_child_refund(monkeypatch):
    remaining = [20.0]
    monkeypatch.setattr(R.S.signal, "getitimer", lambda kind: (remaining[0], 0))
    monkeypatch.setattr(
        R.S.signal, "setitimer", lambda kind, value: remaining.__setitem__(0, value)
    )
    monkeypatch.setattr(R.S, "child_cpu", lambda: 0)
    with pytest.raises(TimeoutError):
        with R.S.reserve_child_cpu(16):
            remaining[0] = 0
            raise TimeoutError("parent timer expired")
    assert remaining[0] == 0


def test_selector_setup_interrupt_reaps_before_cpu_refund(monkeypatch, tmp_path):
    events, remaining, waited_cpu = [], [20.0], [0.0]

    class FakeStream:
        def fileno(self):
            return 100

        def close(self):
            events.append("close")

    fake = SimpleNamespace(pid=12345, returncode=None, stdout=FakeStream(), stderr=FakeStream())

    class BrokenSelector:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def register(self, *args):
            raise TimeoutError("selector setup interrupted")

    def reap(pid, options):
        events.append("wait4")
        waited_cpu[0] = 8
        return pid, 9, SimpleNamespace(ru_utime=8, ru_stime=0, ru_maxrss=100)

    monkeypatch.setattr(R.subprocess, "Popen", lambda *args, **kwargs: fake)
    monkeypatch.setattr(R.selectors, "DefaultSelector", BrokenSelector)
    monkeypatch.setattr(R.os, "set_blocking", lambda *args: None)
    monkeypatch.setattr(R.os, "kill", lambda *args: events.append("kill"))
    monkeypatch.setattr(R.os, "wait4", reap)
    monkeypatch.setattr(R.S, "deadline", lambda *args: R.contextlib.nullcontext())
    monkeypatch.setattr(R.S, "child_cpu", lambda: waited_cpu[0])
    monkeypatch.setattr(R.S.signal, "getitimer", lambda kind: (remaining[0], 0))
    monkeypatch.setattr(
        R.S.signal, "setitimer", lambda kind, value: remaining.__setitem__(0, value)
    )
    writer = R.C.OutputWriter(tmp_path, terminal_limit=524288)
    costs = []
    with pytest.raises(TimeoutError, match="selector setup"):
        with R.S.reserve_child_cpu(16):
            R.launch_worker(
                {
                    "plan": {"job_id": "synthetic-setup-interrupt"},
                    "cpu_limit": 16,
                    "wall_limit": 20,
                },
                tmp_path,
                writer,
                costs,
            )
    assert events == ["kill", "wait4", "close", "close"]
    assert remaining[0] == 12
    assert costs[0]["worker_cpu_seconds"] == 8


@pytest.mark.parametrize("exhausted", [False, True])
def test_failed_driver_closure_uses_only_remaining_budget(monkeypatch, tmp_path, exhausted):
    clocks = {"cpu": 0.0, "wall": 100.0}
    admitted = []
    output = tmp_path / "synthetic-driver"
    monkeypatch.setattr(R, "BOOT_WALL", 100.0)
    monkeypatch.setattr(R.S, "validate_execution_environment", lambda: None)
    monkeypatch.setattr(R.S, "validate_output_roots", lambda *args, **kwargs: None)
    monkeypatch.setattr(R.S, "process_limits", lambda *args: None)
    monkeypatch.setattr(R.sys, "addaudithook", lambda *args: None)
    monkeypatch.setattr(R.S, "cpu_clock", lambda: clocks["cpu"])
    monkeypatch.setattr(R.time, "monotonic", lambda: clocks["wall"])

    def deadline(cpu, wall):
        admitted.append((cpu, wall))
        return R.contextlib.nullcontext()

    def failed_gate(*args):
        clocks.update(cpu=361.0 if exhausted else 359.8, wall=581.0 if exhausted else 579.7)
        raise RuntimeError("synthetic pre-model gate failure")

    monkeypatch.setattr(R.S, "deadline", deadline)
    monkeypatch.setattr(R, "gate", failed_gate)
    args = SimpleNamespace(
        output=output, freeze=tmp_path, review=tmp_path, publication=tmp_path, approval=tmp_path
    )
    assert R.driver(args) == 1
    if exhausted:
        assert len(admitted) == 1
        assert not (output / "result.json").exists()
    else:
        assert admitted[-1] == pytest.approx((0.2, 0.3))
        assert R.S.read(output / "result.json")["error_type"] == "ResourceClosureBudget"


def synthetic_gate_records(monkeypatch, tmp_path):
    """Nonexistent commit and fake freeze; these cannot authorize a study run."""
    directory = tmp_path / "synthetic-freeze"
    directory.mkdir()
    (directory / "manifest.json").write_text("{}")
    pin = R.S.sha(directory / "manifest.json")
    monkeypatch.setattr(R, "ROOT", tmp_path)
    monkeypatch.setattr(R, "sources", lambda: [])
    monkeypatch.setattr(R, "verify_freeze", lambda path: {})

    def fake_git(*args):
        if args == ("rev-parse", "HEAD"):
            return ("a" * 40 + "\n").encode()
        return (tmp_path / args[1].split(":", 1)[1]).read_bytes()

    monkeypatch.setattr(R, "git", fake_git)
    paths = []
    for kind, flag in (
        ("review", "source_review_approved"),
        ("publication", "verified_published"),
        ("approval", "approved_for_execution"),
    ):
        path = tmp_path / ("synthetic-" + kind + ".json")
        path.write_text(
            json.dumps(
                {
                    flag: True,
                    "source_commit": "a" * 40,
                    "manifest_sha256": pin,
                    "output_root": str(R.S.PLANNED_OUTPUT),
                    "ceiling_pairs": 768,
                    "record_url": "synthetic://pytest-only",
                    "recorded_by": "SYNTHETIC TEST: NO EXECUTION AUTHORITY",
                },
                indent=3,
            )
            + "\n\n"
        )
        paths.append(path)
    return directory, paths


def test_gate_binds_original_authority_bytes_not_reserialized_json(monkeypatch, tmp_path):
    directory, paths = synthetic_gate_records(monkeypatch, tmp_path)
    binding = R.gate(directory, *paths)
    assert set(binding["record_files"]) == {"review", "publication", "approval"}
    for kind, path in zip(("review", "publication", "approval"), paths, strict=True):
        item = binding["record_files"][kind]
        assert item == {
            "path": "authority-records/" + kind + ".json",
            "sha256": R.S.sha(path),
            "bytes": path.stat().st_size,
        }
        assert item["sha256"] != R.C.digest(binding["records"][kind])
    assert R._MODEL_ADMISSION is False


@pytest.mark.parametrize(
    "key,value",
    [
        ("record_url", {}),
        ("recorded_by", "  "),
        ("ceiling_pairs", 768.0),
        ("approved_for_execution", 1),
    ],
)
def test_gate_rejects_ambiguous_authority_fields(monkeypatch, tmp_path, key, value):
    directory, paths = synthetic_gate_records(monkeypatch, tmp_path)
    record = json.loads(paths[2].read_text())
    record[key] = value
    paths[2].write_text(json.dumps(record))
    with pytest.raises(RuntimeError):
        R.gate(directory, *paths)

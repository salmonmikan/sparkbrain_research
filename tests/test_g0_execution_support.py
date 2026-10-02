"""SOURCE-ONLY / SYNTHETIC_MODEL_FREE: never import or construct SparkBrain."""
from __future__ import annotations

import gc
import json
import random
import stat
import subprocess
import sys
import threading
import weakref
from pathlib import Path

import pytest

from scripts import g0_execution_support as support

ROOT = Path(__file__).resolve().parents[1]


class SyntheticResource:
    pass


def sample(**changes):
    return {"cpu_seconds": 0, "wall_seconds": 0, "address_space_bytes": 0, **changes}


def budget(**changes):
    return support.ResourceBudget(sampler=lambda: sample(**changes))


def synthetic_function(root, relative, source, name, namespace=None):
    """Compile a standard-library-only stand-in with declared synthetic provenance."""
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source)
    values = {"__name__": "synthetic_model_free", **(namespace or {})}
    exec(compile(source, str(path), "exec"), values)
    return values[name]


def test_import_and_static_contract_checks_never_import_runtime():
    code = f'''import sys
class BlockRuntime:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("SparkBrain import attempted")
sys.meta_path.insert(0, BlockRuntime())
from scripts import g0_execution_support as s
root = s.Path({str(ROOT)!r})
contract = s.read_json(s.confined_path(root, s.CONTRACT, "contract"))
expected = {{**contract["runtime_sources_sha256"], **contract["runtime_schema_sha256"]}}
matching = all(s.digest(s.confined_path(root, name, "source").read_bytes()) == sha
               for name, sha in expected.items())
if matching:
    assert s.verify(root)["runtime_execution_authorized"] is False
else:
    try:
        s.verify(root)
    except ValueError:
        pass
    else:
        raise AssertionError("changed historical runtime was incorrectly admitted")
assert not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules)
'''
    result = subprocess.run([sys.executable, "-B", "-s", "-c", code], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("value", [object(), Path("."), b"bytes", {1: "key"},
                                    float("nan"), float("inf"), ValueError("bad")])
def test_logs_reject_nonprimitive_values(value):
    with pytest.raises(support.AdmissionError, match="primitives"):
        support.primitive(value)


def test_primitive_copy_does_not_alias():
    original = {"items": [{"value": 1}]}
    copied = support.primitive(original)
    original["items"][0]["value"] = 2
    assert copied == {"items": [{"value": 1}]}


def test_duplicate_json_rejected(tmp_path):
    target = tmp_path / "record.json"
    target.write_text('{"identity":1,"identity":2}')
    with pytest.raises(support.AdmissionError, match="duplicate"):
        support.read_json(target)


@pytest.mark.parametrize("kind", ["root", "ancestor", "file", "directory"])
def test_inventory_rejects_every_symlink_route(tmp_path, kind):
    ordinary = tmp_path / "ordinary"
    ordinary.mkdir()
    (ordinary / "source.txt").write_text("synthetic")
    if kind == "file":
        (ordinary / "alias.txt").symlink_to(ordinary / "source.txt")
        root, relative = ordinary, "alias.txt"
    elif kind == "directory":
        (ordinary / "alias").symlink_to(ordinary, target_is_directory=True)
        root, relative = ordinary, "alias/source.txt"
    else:
        alias = tmp_path / "alias"
        alias.symlink_to(ordinary, target_is_directory=True)
        if kind == "ancestor":
            (ordinary / "child").mkdir()
            (ordinary / "child" / "source.txt").write_text("synthetic")
            root = alias / "child"
        else:
            root = alias
        relative = "source.txt"
    with pytest.raises(ValueError, match="symlink"):
        support.source_inventory(root, [relative])


def test_inventory_rejects_escape_and_duplicate(tmp_path):
    with pytest.raises(ValueError, match="escapes"):
        support.source_inventory(tmp_path, ["../secret"])
    with pytest.raises(support.AdmissionError, match="duplicate"):
        support.source_inventory(tmp_path, ["x", "x"])


@pytest.mark.parametrize("key", list(support.LIMITS))
def test_each_resource_cap_blocks_before_mock_dynamics(tmp_path, key):
    current = sample()
    cap = support.LIMITS[key] - support.RESERVES[key]
    b = support.ResourceBudget(sampler=lambda: current)
    if key == "output_bytes":
        b.output_bytes = cap
    else:
        current[key] = cap
    steps = []
    model = synthetic_function(tmp_path, "mock.py", "def act():\n    steps.append(1)\n", "act",
                               {"steps": steps})
    monitor = support.PassiveCallMonitor(tmp_path, {"act": 1}, b,
                                        targets={"act": ("mock.py", "act")},
                                        allowed_functions=set())
    with pytest.raises(support.BudgetExceeded, match="cap"):
        with monitor:
            model()
    assert steps == []
    assert monitor.counts["act"] == 0
    assert b.failure is not None


@pytest.mark.parametrize("name,cap", list(support.CALL_CAPS.items()))
def test_every_call_ceiling_blocks_before_next_mock_body(tmp_path, name, cap):
    steps = []
    model = synthetic_function(tmp_path, "mock.py",
                               "def act(self=sentinel):\n    steps.append(1)\n", "act",
                               {"steps": steps, "sentinel": SyntheticResource()})
    monitor = support.PassiveCallMonitor(tmp_path, {name: cap}, budget(),
                                        targets={name: ("mock.py", "act")},
                                        allowed_functions=set())
    with pytest.raises(support.BudgetExceeded, match="before body"):
        if name == "registry_guard":
            # Abstract counter behavior, separate from the native allocator feature test.
            for _ in range(cap + 1):
                monitor.before(name)
                model(SyntheticResource())
        else:
            with monitor:
                for _ in range(cap + 1):
                    model(SyntheticResource())
    assert len(steps) == cap
    assert monitor.counts[name] == cap
    with pytest.raises(support.BudgetExceeded):
        monitor.check()


def test_unknown_call_route_blocks_before_body(tmp_path):
    steps = []
    model = synthetic_function(tmp_path, "src/sparkbrain/synthetic.py",
                               "def unknown():\n    steps.append(1)\n", "unknown", {"steps": steps})
    monitor = support.PassiveCallMonitor(tmp_path, {}, budget(), targets={},
                                        allowed_functions=set())
    with pytest.raises(support.BudgetExceeded, match="unknown runtime call"):
        with monitor:
            model()
    assert steps == []


def test_counter_profiles_new_owner_thread_before_body(tmp_path):
    steps, failures = [], []
    model = synthetic_function(tmp_path, "mock.py", "def act():\n    steps.append(1)\n", "act",
                               {"steps": steps})
    monitor = support.PassiveCallMonitor(tmp_path, {"act": 1}, budget(),
                                        targets={"act": ("mock.py", "act")},
                                        allowed_functions=set())

    def owner():
        try:
            model()
            model()
        except support.BudgetExceeded as exc:
            failures.append(str(exc))

    main_id = threading.get_ident()
    with monitor:
        thread = threading.Thread(target=owner)
        thread.start()
        thread.join()
    assert steps == [1]
    assert failures and monitor.snapshot()["threads_seen"] != [main_id]
    assert sys.getprofile() is None and threading.getprofile() is None


def test_terminal_stop_bypasses_native_style_rollback(tmp_path):
    steps, rollbacks = [], []
    model = synthetic_function(tmp_path, "mock.py", "def act():\n    steps.append(1)\n", "act",
                               {"steps": steps})
    monitor = support.PassiveCallMonitor(tmp_path, {"act": 0}, budget(),
                                        targets={"act": ("mock.py", "act")},
                                        allowed_functions=set())
    with pytest.raises(support.BudgetExceeded):
        with monitor:
            try:
                model()
            except Exception:
                rollbacks.append(1)
    assert steps == rollbacks == []


def test_ancillary_random_not_counted_as_model_resource(tmp_path):
    monitor = support.PassiveCallMonitor(tmp_path, {"model_rng": 0}, budget(),
                                        targets={}, allowed_functions=set())
    with monitor:
        random.Random(0)
    assert monitor.counts["model_rng"] == 0


def test_owned_rng_birth_counted_and_unknown_route_rejected(tmp_path):
    source = ("class IntegratedV03Brain:\n    def _initialize_runtime(self):\n"
              "        return random.Random(0)\n")
    cls = synthetic_function(tmp_path, "src/sparkbrain/v03/runtime.py", source,
                             "IntegratedV03Brain", {"random": random})
    owner = cls()
    key = ("src/sparkbrain/v03/runtime.py", "IntegratedV03Brain._initialize_runtime")
    monitor = support.PassiveCallMonitor(tmp_path, {"model_rng": 1}, budget(),
                                        targets={}, allowed_functions={key})
    with pytest.raises(support.BudgetExceeded, match="before body"):
        with monitor:
            owner._initialize_runtime()
            owner._initialize_runtime()
    assert monitor.counts["model_rng"] == 1
    unknown = synthetic_function(tmp_path, "src/sparkbrain/unknown.py",
                                 "def birth():\n    return random.Random(0)\n", "birth",
                                 {"random": random})
    monitor = support.PassiveCallMonitor(tmp_path, {"model_rng": 1}, budget(), targets={},
                                        allowed_functions={("src/sparkbrain/unknown.py", "birth")})
    with pytest.raises(support.BudgetExceeded, match="unknown model RNG"):
        with monitor:
            unknown()


def test_profile_captures_native_file_bytes_before_temporary_deletion(tmp_path):
    from tempfile import TemporaryDirectory

    source = '''class SyntheticCheckpoint:
    @staticmethod
    def save(path):
        path.write_bytes(b"synthetic checkpoint bytes")
        return "synthetic_digest"
'''
    cls = synthetic_function(tmp_path, "mock.py", source, "SyntheticCheckpoint")
    b = budget()
    writer = support.ExclusiveEvidenceWriter(tmp_path / "evidence", support.IDENTITY, b)
    monitor = support.PassiveCallMonitor(tmp_path, {"direct_checkpoint_save": 1}, b, writer,
                                        targets={"direct_checkpoint_save":
                                                 ("mock.py", "SyntheticCheckpoint.save")},
                                        allowed_functions=set())
    with monitor:
        with TemporaryDirectory(dir=tmp_path) as directory:
            path = Path(directory) / "raw.json"
            cls.save(path)
    assert not path.exists()
    captured = tmp_path / "evidence/native-checkpoint-0001-raw.json"
    assert captured.read_bytes() == b"synthetic checkpoint bytes"
    assert monitor.counts["direct_checkpoint_save"] == 1


def test_profile_does_not_retain_objects_or_frames(tmp_path):
    class Synthetic:
        pass

    seen = weakref.WeakKeyDictionary()
    model = synthetic_function(tmp_path, "mock.py", "def act(value):\n    return 1\n", "act")
    monitor = support.PassiveCallMonitor(tmp_path, {"act": 1}, budget(),
                                        targets={"act": ("mock.py", "act")},
                                        allowed_functions=set())
    value = Synthetic()
    ref = weakref.ref(value)
    seen[value] = 1
    with monitor:
        model(value)
    del value
    gc.collect()
    assert ref() is None and len(seen) == 0
    support.canonical(monitor.snapshot())


def test_evidence_is_exclusive_and_verdict_follows_raw(tmp_path):
    writer = support.ExclusiveEvidenceWriter(tmp_path / "out", support.IDENTITY, budget())
    with pytest.raises(FileExistsError):
        support.ExclusiveEvidenceWriter(tmp_path / "out", support.IDENTITY, budget())
    with pytest.raises(support.AdmissionError, match="durable raw"):
        writer.verdict("verdict.json", {"equal": True}, raw_names=["raw.json"])
    writer.raw_json("raw.json", {"left": [1], "right": [1]})
    with pytest.raises(FileExistsError):
        writer.raw_json("raw.json", {"replaced": True})
    writer.verdict("verdict.json", {"equal": True}, raw_names=["raw.json"])
    writer.terminal("SYNTHETIC_ONLY", {"real_g0_executed": False})
    terminal = json.loads((tmp_path / "out/TERMINAL.json").read_bytes())
    assert [item["kind"] for item in terminal["records"]] == ["start", "raw_json", "verdict"]
    with pytest.raises(support.AdmissionError, match="closed"):
        writer.raw_bytes("late", b"late")


@pytest.mark.parametrize("name", ["../escape", "/absolute", "nested/file", "..", ""])
def test_evidence_leaf_names_confined(tmp_path, name):
    writer = support.ExclusiveEvidenceWriter(tmp_path / "out", support.IDENTITY, budget())
    with pytest.raises(support.AdmissionError, match="leaf"):
        writer.raw_bytes(name, b"x")


def test_output_cap_preserves_raw_and_terminal_reserve(tmp_path):
    b = budget()
    writer = support.ExclusiveEvidenceWriter(tmp_path / "out", support.IDENTITY, b)
    writer.raw_bytes("already.raw", b"retained")
    b.output_bytes = support.LIMITS["output_bytes"] - support.RESERVES["output_bytes"] - 1
    with pytest.raises(support.BudgetExceeded, match="output cap"):
        writer.raw_bytes("not-written.raw", b"xx")
    writer.terminal("PARTIAL_FAILURE", {"reason": b.failure})
    assert (tmp_path / "out/already.raw").read_bytes() == b"retained"
    assert not (tmp_path / "out/not-written.raw").exists()
    result = json.loads((tmp_path / "out/TERMINAL.json").read_bytes())
    assert result["partial_evidence_retained"] is True
    assert b.output_bytes <= support.LIMITS["output_bytes"]


@pytest.mark.parametrize("key", list(support.LIMITS))
def test_finalization_never_exceeds_hard_caps(tmp_path, key):
    current = sample()
    b = support.ResourceBudget(sampler=lambda: current)
    writer = support.ExclusiveEvidenceWriter(tmp_path / "out", support.IDENTITY, b)
    writer.raw_bytes("partial", b"already durable")
    if key == "output_bytes":
        b.output_bytes = support.LIMITS[key]
    else:
        current[key] = support.LIMITS[key]
    with pytest.raises(support.BudgetExceeded):
        writer.terminal("PARTIAL_FAILURE")
    assert (tmp_path / "out/partial").read_bytes() == b"already durable"
    assert not (tmp_path / "out/TERMINAL.json").exists()


def test_no_resource_cap_top_up():
    limits = {**support.LIMITS, "cpu_seconds": 601}
    with pytest.raises(support.AdmissionError, match="expanded"):
        support.ResourceBudget(limits=limits)


def test_unsupported_and_forged_permits_reject_without_limits(tmp_path, monkeypatch):
    with pytest.raises(support.AdmissionError, match="external authority"):
        support.ExecutionPermit()
    forged = object.__new__(support.ExecutionPermit)
    with pytest.raises(support.AdmissionError, match="unissued"):
        support.require_execution_permit(forged)
    with pytest.raises(support.AdmissionError, match="unissued"):
        support.install_runtime_limits(forged)
    with pytest.raises(support.AdmissionError, match="independent external"):
        support.authorize_execution(tmp_path, "none", "none", "0" * 64, None)


def test_gate_rejects_synthetic_approval_even_with_positive_callback(tmp_path, monkeypatch):
    from types import SimpleNamespace

    # Isolate this synthetic gate fixture from unrelated full-suite runtime imports.
    monkeypatch.setattr(support, "sys", SimpleNamespace(modules={}))
    synthetic = {"freeze": {}, "freeze_sha256": "a" * 64, "source_inventory_sha256": "b" * 64}
    monkeypatch.setattr(support, "verify_preparation", lambda *args: synthetic)
    approval = {"schema": "g0-published-execution-approval-v1", "identity": support.IDENTITY,
                "freeze_sha256": "a" * 64, "source_inventory_sha256": "b" * 64,
                "limits": support.LIMITS, "reserves": support.RESERVES,
                "call_caps": support.CALL_CAPS, "actual_execution_authorized": True,
                "synthetic": True}
    raw = support.canonical(approval)
    (tmp_path / "synthetic.json").write_bytes(raw)
    with pytest.raises(support.AdmissionError, match="synthetic"):
        support.authorize_execution(tmp_path, "synthetic-freeze", "synthetic.json",
                                    support.digest(raw), lambda record: True)


@pytest.mark.parametrize("field,value", [("identity", "consumed-pr182"),
                                         ("limits", {"cpu_seconds": 1000}),
                                         ("call_caps", {}),
                                         ("contract_sha256", "wrong"),
                                         ("runtime_execution_authorized", True)])
def test_freeze_cannot_change_identity_caps_contract_or_self_authorize(field, value):
    freeze = {"schema": "g0-execution-freeze-v1", "identity": support.IDENTITY,
              "limits": support.LIMITS, "reserves": support.RESERVES,
              "call_caps": support.CALL_CAPS, "runtime_python_files": 157,
              "runtime_schema_files": 15, "contract_sha256": support.CONTRACT_SHA256,
              "runtime_execution_authorized": False, field: value}
    with pytest.raises(support.AdmissionError):
        support._fixed_envelope(freeze)


def test_actual_parent_timeout_not_boolean_claim():
    # This source-only test only reads /proc; no timeout/model/limits route is launched.
    with pytest.raises(support.AdmissionError, match="actual parent"):
        support.verify_timeout_parent("0" * 64)


def test_passive_birth_ids_include_shells_and_allow_weak_cleanup(tmp_path):
    # These are synthetic stand-ins with source tags, never imported runtime classes.
    raw = type("IntegratedV03Brain", (), {"__module__": "sparkbrain.v03.runtime"})
    producer = type("IntegratedV05Brain", (), {"__module__": "sparkbrain.v05.brain"})
    construct = synthetic_function(
        tmp_path, "scripts/g0_joint_ownership.py",
        "def _construct(cls):\n    clone = object.__new__(cls)\n    return clone\n", "_construct")
    monitor = support.PassiveCallMonitor(tmp_path, {"rawbrain_shell": 2, "v05_shell": 1},
                                        budget(), targets={})
    with monitor:
        first = construct(raw)
        second = construct(producer)
        first_id = id(first)
        ref = weakref.ref(first)
        del first
        gc.collect()
        third = construct(raw)
    assert ref() is None
    snapshot = monitor.snapshot()
    assert [item["birth_id"] for item in snapshot["births"]] == [1, 2, 3]
    assert snapshot["counts"] == snapshot["returned"] == {"rawbrain_shell": 2, "v05_shell": 1}
    assert snapshot["births"][0]["runtime_id"] == first_id
    assert {id(second), id(third)} == set(snapshot["live_resource_ids"])
    assert snapshot["pending_shells"] == []
    support.canonical(snapshot)
    del second, third
    gc.collect()
    assert monitor.snapshot()["live_resource_ids"] == []


def test_source_bound_class_bodies_and_registry_guard_are_admitted(tmp_path):
    import importlib.util

    relative = "src/sparkbrain/v032/runtime.py"
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_text("import threading\n_LOCK_REGISTRY_GUARD = threading.Lock()\n"
                      "class Synthetic:\n    marker = 1\n")
    spec = importlib.util.spec_from_file_location("synthetic_model_free_import", target)
    module = importlib.util.module_from_spec(spec)
    monitor = support.PassiveCallMonitor(tmp_path, {"registry_guard": 1}, budget(), targets={})
    try:
        support.require_passive_lock_api()
    except support.AdmissionError:
        with pytest.raises(support.AdmissionError, match="unsupported passive lock allocator"):
            with monitor:
                spec.loader.exec_module(module)
        assert not hasattr(module, "Synthetic")
        return
    with monitor:
        spec.loader.exec_module(module)
    assert module.Synthetic.marker == 1
    snapshot = monitor.snapshot()
    assert snapshot["counts"] == snapshot["returned"] == {"registry_guard": 1}
    assert snapshot["births"][0]["runtime_id"] == id(module._LOCK_REGISTRY_GUARD)


def test_native_load_raw_is_durable_before_failed_decode(tmp_path):
    source = ("class SyntheticCheckpoint:\n    @staticmethod\n"
              "    def _load_bytes(raw):\n        raise ValueError('synthetic decode failure')\n")
    cls = synthetic_function(tmp_path, "mock.py", source, "SyntheticCheckpoint")
    b = budget()
    writer = support.ExclusiveEvidenceWriter(tmp_path / "out", support.IDENTITY, b)
    monitor = support.PassiveCallMonitor(tmp_path, {"direct_checkpoint_load_bytes": 1}, b, writer,
                                        targets={"direct_checkpoint_load_bytes":
                                                 ("mock.py", "SyntheticCheckpoint._load_bytes")},
                                        allowed_functions=set())
    with monitor:
        with pytest.raises(ValueError, match="synthetic decode failure"):
            cls._load_bytes(b"not valid synthetic checkpoint JSON")
    assert (tmp_path / "out/native-load-input-0001.json").read_bytes() == (
        b"not valid synthetic checkpoint JSON")
    assert monitor.counts["direct_checkpoint_load_bytes"] == 1
    assert monitor.returned["direct_checkpoint_load_bytes"] == 0
    assert any(item["kind"] == "call_exception" for item in monitor.events)


def test_public_json_read_rejects_symlink(tmp_path):
    target = tmp_path / "ordinary.json"
    target.write_text("{}")
    alias = tmp_path / "alias.json"
    alias.symlink_to(target)
    with pytest.raises(ValueError, match="symlink"):
        support.read_json(alias)


def synthetic_freeze(tmp_path, monkeypatch):
    """Explicit synthetic structural fixture; never capable of minting runtime authority."""
    monkeypatch.setattr(support, "verify", lambda root: {"synthetic": True})
    paths = {
        support.CONTRACT: support.canonical({"runtime_sources_sha256": {},
                                            "runtime_schema_sha256": {},
                                            "reuse_sources_sha256": {}}),
        "scripts/g0_execution_support.py": b"# synthetic fixture\n",
        "scripts/g0_joint_ownership.py": b"# synthetic fixture\n",
        "scripts/verify_g0_joint_source_contract.py": b"# synthetic fixture\n",
        "scripts/run_g0_joint_eligibility.py": b"# synthetic fixture\n",
        "scripts/launch_g0_joint_eligibility.py": b"# synthetic fixture\n",
        "tests/test_g0_joint_launcher.py": b"# synthetic fixture\n",
        "scripts/v05_history_export_probe.py": b"# synthetic fixture\n",
        "tests/test_g0_execution_support.py": b"# synthetic fixture\n",
        "tests/test_g0_joint_eligibility_runner.py": b"# synthetic fixture\n",
        "tests/test_g0_joint_ownership.py": b"# synthetic fixture\n",
        "tests/test_g0_joint_source_contract.py": b"# synthetic fixture\n",
        "tests/test_g0_execution_protocol.py": b"# synthetic fixture\n",
        "docs/research/assembly_m1_g0_execution_preparation_20261002.md": b"Synthetic only.\n",
    }
    inputs_path = f"{support.ARTIFACT_ROOT}/inputs.json"
    protocol_path = f"{support.ARTIFACT_ROOT}/protocol.json"
    inputs = support.canonical({"synthetic": True})
    protocol = {"synthetic": True, "identity": support.IDENTITY,
                "call_caps": support.protocol_call_caps(), "limits": support.LIMITS,
                "reserves": support.RESERVES,
                "inputs": {"path": inputs_path, "sha256": support.digest(inputs)}}
    paths[inputs_path] = inputs
    paths[protocol_path] = support.canonical(protocol)
    for name, raw in paths.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    (tmp_path / "src/sparkbrain").mkdir(parents=True)
    freeze = {"schema": "g0-execution-freeze-v1", "identity": support.IDENTITY,
              "limits": support.LIMITS, "reserves": support.RESERVES,
              "call_caps": support.CALL_CAPS, "runtime_python_files": 157,
              "runtime_schema_files": 15, "contract_sha256": support.CONTRACT_SHA256,
              "runtime_execution_authorized": False, "environment": {"synthetic": True},
              "timeout_executable_sha256": "0" * 64,
              "source_files_sha256": {name: support.digest(raw) for name, raw in paths.items()},
              "protocol": {"path": protocol_path, "sha256": support.digest(paths[protocol_path])},
              "inputs": {"path": inputs_path, "sha256": support.digest(inputs)}}
    (tmp_path / "synthetic-freeze.json").write_bytes(support.canonical(freeze))
    return freeze


@pytest.mark.parametrize("target", ["protocol", "inputs"])
def test_gate_rejects_inventoried_but_wrong_literal_file(tmp_path, monkeypatch, target):
    freeze = synthetic_freeze(tmp_path, monkeypatch)
    original = tmp_path / freeze[target]["path"]
    (tmp_path / "wrong.json").write_bytes(original.read_bytes())
    freeze[target]["path"] = "wrong.json"
    freeze["source_files_sha256"]["wrong.json"] = support.digest(original.read_bytes())
    (tmp_path / "synthetic-freeze.json").write_bytes(support.canonical(freeze))
    with pytest.raises(support.AdmissionError,
                       match="canonical prospective path|literal binding differs"):
        support.verify_preparation(tmp_path, "synthetic-freeze.json", check_environment=False)


def test_gate_rejects_protocol_to_input_misbinding(tmp_path, monkeypatch):
    freeze = synthetic_freeze(tmp_path, monkeypatch)
    path = tmp_path / freeze["protocol"]["path"]
    protocol = support.read_json(path)
    protocol["inputs"]["sha256"] = "0" * 64
    path.write_bytes(support.canonical(protocol))
    sha = support.digest(path.read_bytes())
    freeze["protocol"]["sha256"] = sha
    freeze["source_files_sha256"][freeze["protocol"]["path"]] = sha
    (tmp_path / "synthetic-freeze.json").write_bytes(support.canonical(freeze))
    with pytest.raises(support.AdmissionError, match="literal binding differs"):
        support.verify_preparation(tmp_path, "synthetic-freeze.json", check_environment=False)


@pytest.mark.parametrize("change", ["source", "missing", "bytecode", "environment"])
def test_static_gate_rejects_source_inventory_bytecode_and_environment_changes(
        tmp_path, monkeypatch, change):
    freeze = synthetic_freeze(tmp_path, monkeypatch)
    if change == "source":
        (tmp_path / "scripts/g0_joint_ownership.py").write_text("# changed\n")
    elif change == "missing":
        del freeze["source_files_sha256"]["scripts/g0_joint_ownership.py"]
        (tmp_path / "synthetic-freeze.json").write_bytes(support.canonical(freeze))
    elif change == "bytecode":
        (tmp_path / "src/sparkbrain/rogue.pyc").write_bytes(b"synthetic bytecode")
    else:
        monkeypatch.setattr(support, "environment_snapshot", lambda root: {"synthetic": "changed"})
    with pytest.raises(support.AdmissionError):
        support.verify_preparation(tmp_path, "synthetic-freeze.json",
                                   check_environment=change == "environment")


def test_synthetic_static_validation_never_mints_authority(tmp_path, monkeypatch):
    before = {name for name in sys.modules
              if name == "sparkbrain" or name.startswith("sparkbrain.")}
    synthetic_freeze(tmp_path, monkeypatch)
    result = support.verify_preparation(tmp_path, "synthetic-freeze.json", check_environment=False)
    assert result["runtime_execution_authorized"] is False
    assert result["source_contract"] == {"synthetic": True}
    after = {name for name in sys.modules
             if name == "sparkbrain" or name.startswith("sparkbrain.")}
    assert after == before


def test_delayed_admission_includes_timeout_parent_in_terminal_reserve(monkeypatch):
    # No actual timeout is launched. A synthetic verified-parent clock starts earlier.
    b = budget()
    b._wall_start = 900.0
    b._sampler = lambda: sample(wall_seconds=support.time.monotonic() - b._wall_start)
    monkeypatch.setattr(support.time, "monotonic", lambda: 1000.0)
    b.bind_timeout_parent({"started_monotonic_seconds": 200.0})
    assert b.sample()["wall_seconds"] == 800.0
    monkeypatch.setattr(support.time, "monotonic", lambda: 1055.0)
    with pytest.raises(support.BudgetExceeded, match="wall_seconds"):
        b.check()
    assert b.finish()["wall_seconds"] == 855.0
    monkeypatch.setattr(support.time, "monotonic", lambda: 1100.0)
    with pytest.raises(support.BudgetExceeded, match="wall_seconds"):
        b.check()


def test_identity_reservation_is_durable_across_different_output_directories(tmp_path, monkeypatch):
    # Explicit synthetic in-memory harness: bypass admission only, never import runtime.
    monkeypatch.setattr(support, "require_execution_permit", lambda *args: None)
    ledger = tmp_path / "synthetic-ledger.json"
    ledger.write_bytes(support.canonical({"synthetic": True}))
    reservation = tmp_path / (support.IDENTITY + ".STARTED.json")

    def synthetic_permit(output):
        permit = object.__new__(support.ExecutionPermit)
        support._PERMITS[permit] = {
            "root": tmp_path, "output_directory": output, "consumed": False,
            "identity_ledger_path": ledger,
            "identity_ledger_sha256": support.digest(ledger.read_bytes()),
            "identity_reservation": reservation, "execution_nonce": "SYNTHETIC_TEST_ONLY",
            "approval_sha256": "synthetic_not_authority",
            "verified": {"freeze_sha256": "synthetic_not_authority"},
        }
        return permit

    first_output = tmp_path / "first"
    first = synthetic_permit(first_output)
    with pytest.raises(support.AdmissionError, match="destination"):
        support.consume_execution_permit(first, tmp_path / "wrong", budget=budget())
    assert support.consume_execution_permit(first, first_output, budget=budget()) == first_output
    assert reservation.exists()
    with pytest.raises(support.AdmissionError, match="already consumed"):
        support.consume_execution_permit(first, first_output, budget=budget())
    second = synthetic_permit(tmp_path / "different-output")
    with pytest.raises(FileExistsError):
        support.consume_execution_permit(second, second.output_directory, budget=budget())
    assert not second.output_directory.exists()


def test_changed_identity_ledger_blocks_reservation(tmp_path, monkeypatch):
    monkeypatch.setattr(support, "require_execution_permit", lambda *args: None)
    ledger = tmp_path / "synthetic-ledger.json"
    ledger.write_bytes(b"synthetic original ledger")
    old_digest = support.digest(ledger.read_bytes())
    ledger.write_bytes(b"synthetic changed ledger")
    permit = object.__new__(support.ExecutionPermit)
    output = tmp_path / "out"
    reservation = tmp_path / "synthetic-reservation"
    support._PERMITS[permit] = {
        "output_directory": output, "consumed": False,
        "identity_ledger_path": ledger, "identity_ledger_sha256": old_digest,
        "identity_reservation": reservation,
    }
    with pytest.raises(support.AdmissionError, match="ledger changed"):
        support.consume_execution_permit(permit, output, budget=budget())
    assert not reservation.exists() and not output.exists()


def test_late_native_mappings_must_be_covered_by_frozen_code(tmp_path, monkeypatch):
    system_library = tmp_path / "synthetic-system.so"
    system_library.write_bytes(b"synthetic stand-in ELF bytes, not executable")
    system_sha = support.digest(system_library.read_bytes())
    environment = {"native_code_sha256": {"/synthetic/declared-extension.so": "extension-hash"},
                   "system_libraries_sha256": {str(system_library): system_sha},
                   "executable": "/synthetic/python", "executable_sha256": "python-hash"}
    mapped = {str(system_library): system_sha, "/synthetic/python": "python-hash"}
    monkeypatch.setattr(support, "mapped_code_snapshot", lambda: mapped)
    assert support.verify_mapped_libraries(environment) == mapped
    mapped["/synthetic/declared-extension.so"] = "extension-hash"
    assert support.verify_mapped_libraries(environment) == mapped
    mapped["/synthetic/unfrozen.so"] = "unknown-hash"
    with pytest.raises(support.AdmissionError, match="new or changed"):
        support.verify_mapped_libraries(environment)
    del mapped["/synthetic/unfrozen.so"]
    system_library.write_bytes(b"changed synthetic system library")
    with pytest.raises(support.AdmissionError, match="system library changed"):
        support.verify_mapped_libraries(environment)


@pytest.mark.parametrize("resource_name,key,required", [
    ("RLIMIT_CPU", "cpu_seconds", 600),
    ("RLIMIT_AS", "address_space_bytes", 1 << 30),
    ("RLIMIT_FSIZE", "output_bytes", 256 << 20),
])
def test_insufficient_inherited_limits_never_consume_identity(
        tmp_path, monkeypatch, resource_name, key, required):
    import resource

    target = getattr(resource, resource_name)
    monkeypatch.setattr(resource, "getrlimit", lambda name: (
        (required - 1, required - 1) if name == target else
        (resource.RLIM_INFINITY, resource.RLIM_INFINITY)))
    installed = []
    monkeypatch.setattr(resource, "setrlimit", lambda *args: installed.append(args))
    monkeypatch.setattr(support, "require_execution_permit", lambda *args: None)
    permit = object.__new__(support.ExecutionPermit)
    reservation = tmp_path / "synthetic-reservation"
    output = tmp_path / "synthetic-output"
    support._PERMITS[permit] = {"consumed": False, "identity_reservation": reservation}
    evidence_budget = budget()
    with pytest.raises(support.AdmissionError, match="inherited hard limit.*" + key):
        support.consume_execution_permit(permit, output, budget=evidence_budget)
    assert support._PERMITS[permit]["consumed"] is False
    assert evidence_budget.output_bytes == 0
    assert not reservation.exists() and not output.exists()
    assert installed == []


@pytest.mark.parametrize("inherited", ["exact", "higher", "unlimited"])
def test_limit_preflight_keeps_exact_frozen_pairs_without_installing(monkeypatch, inherited):
    import resource

    exact = {resource.RLIMIT_CPU: 600, resource.RLIMIT_AS: 1 << 30,
             resource.RLIMIT_FSIZE: 256 << 20, resource.RLIMIT_CORE: 0}

    def getrlimit(identifier):
        hard = exact[identifier]
        if inherited == "higher":
            hard += 1000
        elif inherited == "unlimited":
            hard = resource.RLIM_INFINITY
        return hard, hard

    installed = []
    monkeypatch.setattr(resource, "getrlimit", getrlimit)
    monkeypatch.setattr(resource, "setrlimit", lambda *args: installed.append(args))
    result = support.preflight_runtime_limits()
    assert result["read_only"] is True
    assert installed == []
    assert {row["resource_id"]: row["required_hard"] for row in result["resources"]} == exact
    assert all(row["required_soft"] == row["required_hard"] for row in result["resources"])


def test_present_launcher_and_test_must_both_be_frozen(tmp_path, monkeypatch):
    freeze = synthetic_freeze(tmp_path, monkeypatch)
    del freeze["source_files_sha256"]["scripts/launch_g0_joint_eligibility.py"]
    (tmp_path / "synthetic-freeze.json").write_bytes(support.canonical(freeze))
    with pytest.raises(support.AdmissionError, match="incomplete"):
        support.verify_preparation(tmp_path, "synthetic-freeze.json", check_environment=False)


def synthetic_completed_lifecycle():
    """Pure invented primitive ledger for completion validation; no runtime observations."""
    returns = support.expected_lifecycle_returns()
    births = []
    for name, count in support.expected_lifecycle_birth_counts().items():
        for _ in range(count):
            index = len(births) + 1
            births.append({"birth_id": index, "name": name, "runtime_id": 1000 + index,
                           "type": support.BIRTH_TYPES[name],
                           "source_route": list(support.lifecycle_birth_routes(name)[0]),
                           "thread": 1})
    guard = next(row["runtime_id"] for row in births if row["name"] == "registry_guard")
    events = []

    def event(kind, name, **data):
        events.append({"sequence": len(events) + 1, "kind": kind, "name": name,
                       "thread": 1, **data})

    for name, count in support.CALL_CAPS.items():
        for attempt in range(1, count + 1):
            event("call_attempt", name, attempt=attempt)
            event("call_return" if attempt <= returns[name] else "call_exception", name)
    for row in births:
        event("resource_birth", row["name"],
              **{key: value for key, value in row.items() if key != "name"})
    return {"counts": dict(support.CALL_CAPS), "caps": dict(support.CALL_CAPS),
            "returned": returns, "failure": None, "pending_calls": [], "pending_shells": [],
            "births": births, "events": events, "live_resource_ids": [guard], "threads_seen": [1],
            "ancillary_rngs": 0, "counts_before_body": True,
            "protocol_counts": support.protocol_call_caps()}


def test_primitive_completed_lifecycle_reconciles_returns_births_and_lifetimes():
    result = support.validate_completed_lifecycle(synthetic_completed_lifecycle())
    assert result["validated"] is True
    assert result["normal_returns"]["m1_apply_outcome"] == 4
    assert result["exceptional_exits"]["m1_apply_outcome"] == 2
    assert result["birth_counts"] == support.expected_lifecycle_birth_counts()
    assert result["model_resources_live"] == 0


@pytest.mark.parametrize("change", [
    "missing_returns", "short_return", "extra_return", "missing_births", "duplicate_birth_id",
    "nonmonotonic_birth_id", "wrong_resource_type", "unknown_birth_route", "model_still_live",
    "guard_dead", "sticky_failure", "pending_call", "pending_shell", "missing_events",
    "missing_attempt_event", "wrong_attempt_sequence", "missing_return_event", "extra_exception",
    "changed_birth_event", "wrong_birth_count", "unknown_event", "wrong_event_sequence",
    "boolean_count", "invalid_thread", "wrong_ancillary_count",
])
def test_malformed_completion_ledgers_cannot_pass(change):
    value = synthetic_completed_lifecycle()
    if change == "missing_returns":
        del value["returned"]
    elif change == "short_return":
        value["returned"]["facade_init"] -= 1
    elif change == "extra_return":
        value["returned"]["m1_apply_outcome"] += 1
    elif change == "missing_births":
        del value["births"]
    elif change == "duplicate_birth_id":
        value["births"][1]["birth_id"] = value["births"][0]["birth_id"]
    elif change == "nonmonotonic_birth_id":
        value["births"][0]["birth_id"] = 2
    elif change == "wrong_resource_type":
        value["births"][0]["type"] = "synthetic.unknown"
    elif change == "unknown_birth_route":
        value["births"][0]["source_route"] = ["synthetic.py", "unknown"]
    elif change == "model_still_live":
        value["live_resource_ids"].append(value["births"][0]["runtime_id"])
    elif change == "guard_dead":
        value["live_resource_ids"] = []
    elif change == "sticky_failure":
        value["failure"] = "synthetic profiler failure"
    elif change == "pending_call":
        value["pending_calls"] = [{"name": "synthetic"}]
    elif change == "pending_shell":
        value["pending_shells"] = [{"name": "synthetic"}]
    elif change == "missing_events":
        del value["events"]
    elif change in {"missing_attempt_event", "missing_return_event"}:
        kind = "call_attempt" if change == "missing_attempt_event" else "call_return"
        index = next(i for i, row in enumerate(value["events"]) if row["kind"] == kind)
        del value["events"][index]
        for index, row in enumerate(value["events"], 1):
            row["sequence"] = index
    elif change == "wrong_attempt_sequence":
        value["events"][0]["attempt"] += 1
    elif change == "extra_exception":
        row = next(row for row in value["events"] if row["kind"] == "call_return")
        row["kind"] = "call_exception"
    elif change == "changed_birth_event":
        row = next(row for row in value["events"] if row["kind"] == "resource_birth")
        row["runtime_id"] += 1
    elif change == "wrong_birth_count":
        value["births"].pop()
    elif change == "unknown_event":
        value["events"][0]["kind"] = "invented"
    elif change == "wrong_event_sequence":
        value["events"][0]["sequence"] = 2
    elif change == "boolean_count":
        value["returned"]["v03_init"] = True
    elif change == "invalid_thread":
        value["threads_seen"] = [["invalid"]]
    elif change == "wrong_ancillary_count":
        value["ancillary_rngs"] = 1
    with pytest.raises(support.AdmissionError):
        support.validate_completed_lifecycle(value)


def test_unreviewed_lock_allocator_rejects_before_synthetic_module_execution(tmp_path, monkeypatch):
    from types import SimpleNamespace

    # Simulate the changed allocator API without replacing the process's threading module.
    monitor = support.PassiveCallMonitor(tmp_path, {"registry_guard": 1}, budget(),
                                        targets={}, allowed_functions=set())
    monkeypatch.setattr(support, "threading", SimpleNamespace(Lock=type("UnreviewedLock", (), {})))
    reached = []
    with pytest.raises(support.AdmissionError, match="unsupported passive lock allocator"):
        with monitor:
            reached.append("body")
    assert reached == []


def test_limit_installation_uses_exact_pairs_with_only_synthetic_os_backends(monkeypatch):
    import resource
    from types import SimpleNamespace

    installed, hooks = [], []
    monkeypatch.setattr(support, "require_execution_permit", lambda permit: None)
    monkeypatch.setattr(support, "verify_timeout_parent", lambda *args: {"synthetic": True})
    monkeypatch.setattr(resource, "getrlimit", lambda identifier:
                        (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    monkeypatch.setattr(resource, "setrlimit", lambda identifier, pair: installed.append(
        (identifier, pair)))
    monkeypatch.setattr(support, "sys", SimpleNamespace(
        dont_write_bytecode=True, flags=SimpleNamespace(no_user_site=1),
        addaudithook=lambda hook: hooks.append(hook)))
    permit = SimpleNamespace(freeze={"timeout_executable_sha256": "SYNTHETIC_NOT_AUTHORITY"})
    result = support.install_runtime_limits(permit)
    assert installed == [(resource.RLIMIT_CPU, (600, 600)),
                         (resource.RLIMIT_AS, (1 << 30, 1 << 30)),
                         (resource.RLIMIT_FSIZE, (256 << 20, 256 << 20)),
                         (resource.RLIMIT_CORE, (0, 0))]
    assert len(hooks) == 1
    assert result["inherited_limits"]["frozen_envelope_preserved"] is True


@pytest.mark.parametrize("resource_name,key,required", [
    ("RLIMIT_CPU", "cpu_seconds", 600),
    ("RLIMIT_AS", "address_space_bytes", 1 << 30),
    ("RLIMIT_FSIZE", "output_bytes", 256 << 20),
])
@pytest.mark.parametrize("shortfall", ["zero", "just_below"])
def test_insufficient_soft_limits_never_consume_or_charge_identity(
        tmp_path, monkeypatch, resource_name, key, required, shortfall):
    import resource

    target = getattr(resource, resource_name)
    soft = 0 if shortfall == "zero" else required - 1
    monkeypatch.setattr(resource, "getrlimit", lambda name: (
        (soft, resource.RLIM_INFINITY) if name == target else
        (resource.RLIM_INFINITY, resource.RLIM_INFINITY)))
    installed = []
    monkeypatch.setattr(resource, "setrlimit", lambda *args: installed.append(args))
    monkeypatch.setattr(support, "require_execution_permit", lambda *args: None)
    permit = object.__new__(support.ExecutionPermit)
    reservation = tmp_path / "synthetic-reservation"
    output = tmp_path / "synthetic-output"
    support._PERMITS[permit] = {"consumed": False, "identity_reservation": reservation}
    evidence_budget = budget()
    with pytest.raises(support.AdmissionError, match="inherited soft limit.*" + key):
        support.consume_execution_permit(permit, output, budget=evidence_budget)
    assert support._PERMITS[permit]["consumed"] is False
    assert evidence_budget.output_bytes == 0
    assert not reservation.exists() and not output.exists()
    assert installed == []


@pytest.mark.parametrize("resource_name,required", [
    ("RLIMIT_CPU", 600), ("RLIMIT_AS", 1 << 30), ("RLIMIT_FSIZE", 256 << 20),
])
@pytest.mark.parametrize("boundary", ["exact", "soft_exact_hard_unlimited", "unlimited"])
def test_each_healthy_soft_hard_boundary_is_read_only(
        monkeypatch, resource_name, required, boundary):
    import resource

    target = getattr(resource, resource_name)
    pair = {"exact": (required, required),
            "soft_exact_hard_unlimited": (required, resource.RLIM_INFINITY),
            "unlimited": (resource.RLIM_INFINITY, resource.RLIM_INFINITY)}[boundary]
    monkeypatch.setattr(resource, "getrlimit", lambda name: pair if name == target else
                        (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    installed = []
    monkeypatch.setattr(resource, "setrlimit", lambda *args: installed.append(args))
    result = support.preflight_runtime_limits()
    row = next(row for row in result["resources"] if row["resource_id"] == target)
    assert (row["inherited_soft"], row["inherited_hard"]) == pair
    assert (row["required_soft"], row["required_hard"]) == (required, required)
    assert installed == []


@pytest.mark.parametrize("bad", ["boolean", "float", "negative", "wrong_shape", "list_pair",
                                 "soft_above_hard", "soft_unlimited_hard_finite", "read_error"])
def test_invalid_or_unavailable_limit_metadata_never_consumes_identity(tmp_path, monkeypatch, bad):
    import resource

    pairs = {"boolean": (True, resource.RLIM_INFINITY),
             "float": (600.0, resource.RLIM_INFINITY),
             "negative": (-2, resource.RLIM_INFINITY), "wrong_shape": (600,),
             "list_pair": [600, 600], "soft_above_hard": (601, 600),
             "soft_unlimited_hard_finite": (resource.RLIM_INFINITY, 600)}

    def getrlimit(identifier):
        if bad == "read_error":
            raise OSError("synthetic getrlimit failure")
        return pairs[bad]

    monkeypatch.setattr(resource, "getrlimit", getrlimit)
    installed = []
    monkeypatch.setattr(resource, "setrlimit", lambda *args: installed.append(args))
    monkeypatch.setattr(support, "require_execution_permit", lambda *args: None)
    permit = object.__new__(support.ExecutionPermit)
    reservation = tmp_path / "synthetic-reservation"
    output = tmp_path / "synthetic-output"
    support._PERMITS[permit] = {"consumed": False, "identity_reservation": reservation}
    evidence_budget = budget()
    with pytest.raises(support.AdmissionError, match="metadata|unavailable"):
        support.consume_execution_permit(permit, output, budget=evidence_budget)
    assert support._PERMITS[permit]["consumed"] is False
    assert evidence_budget.output_bytes == 0
    assert not reservation.exists() and not output.exists()
    assert installed == []


@pytest.mark.parametrize("resource_name,required", [
    ("RLIMIT_CPU", 600), ("RLIMIT_AS", 1 << 30),
    ("RLIMIT_FSIZE", 256 << 20), ("RLIMIT_CORE", 0),
])
@pytest.mark.parametrize("soft_boundary", ["below", "exact", "above", "unlimited"])
@pytest.mark.parametrize("hard_boundary", ["below", "exact", "above", "unlimited"])
def test_complete_inherited_limit_matrix_before_reservation_and_exact_mock_install(
        tmp_path, monkeypatch, resource_name, required, soft_boundary, hard_boundary):
    import resource
    from types import SimpleNamespace

    # Core's lowest finite valid value is zero. Its "below" case is invalid metadata,
    # not a negative usable limit; -1 is reserved by this backend for unlimited.
    values = {"below": required - 1 if required else -2, "exact": required,
              "above": required + 1, "unlimited": resource.RLIM_INFINITY}
    soft, hard = values[soft_boundary], values[hard_boundary]
    target = getattr(resource, resource_name)
    monkeypatch.setattr(resource, "getrlimit", lambda identifier: (soft, hard)
                        if identifier == target else
                        (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    installed = []
    monkeypatch.setattr(resource, "setrlimit", lambda identifier, pair:
                        installed.append((identifier, pair)))
    monkeypatch.setattr(support, "require_execution_permit", lambda permit: None)
    permit = object.__new__(support.ExecutionPermit)
    reservation = tmp_path / "synthetic-reservation"
    output = tmp_path / "synthetic-output"
    support._PERMITS[permit] = {"consumed": False, "identity_reservation": reservation}
    evidence_budget = budget()
    infinity = resource.RLIM_INFINITY
    healthy = (
        (soft == infinity or soft >= required)
        and (hard == infinity or hard >= required)
        and (hard == infinity or (soft != infinity and soft <= hard))
    )
    if not healthy:
        with pytest.raises(support.AdmissionError):
            support.consume_execution_permit(permit, output, budget=evidence_budget)
        assert support._PERMITS[permit]["consumed"] is False
        assert evidence_budget.output_bytes == 0
        assert not reservation.exists() and not output.exists()
        assert installed == []
        return
    admitted = support.preflight_runtime_limits()
    row = next(row for row in admitted["resources"] if row["resource_id"] == target)
    assert (row["inherited_soft"], row["inherited_hard"]) == (soft, hard)
    assert installed == []
    hooks = []
    monkeypatch.setattr(support, "verify_timeout_parent", lambda *args: {"synthetic": True})
    monkeypatch.setattr(support, "sys", SimpleNamespace(
        dont_write_bytecode=True, flags=SimpleNamespace(no_user_site=1),
        addaudithook=lambda hook: hooks.append(hook)))
    fake = SimpleNamespace(freeze={"timeout_executable_sha256": "SYNTHETIC_NOT_AUTHORITY"})
    support.install_runtime_limits(fake)
    assert installed == [(resource.RLIMIT_CPU, (600, 600)),
                         (resource.RLIMIT_AS, (1 << 30, 1 << 30)),
                         (resource.RLIMIT_FSIZE, (256 << 20, 256 << 20)),
                         (resource.RLIMIT_CORE, (0, 0))]
    assert len(hooks) == 1
    assert not reservation.exists() and not output.exists()
    assert evidence_budget.output_bytes == 0


def synthetic_reservation_fixture(tmp_path, monkeypatch):
    import resource

    monkeypatch.setattr(support, "require_execution_permit", lambda permit: None)
    monkeypatch.setattr(resource, "getrlimit", lambda identifier:
                        (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    ledger = tmp_path / "synthetic-ledger.json"
    ledger.write_bytes(support.canonical({"synthetic": True}))
    reservation = tmp_path / "synthetic-reservation.json"
    output = tmp_path / "synthetic-output"
    permit = object.__new__(support.ExecutionPermit)
    support._PERMITS[permit] = {
        "root": tmp_path, "output_directory": output, "consumed": False,
        "identity_ledger_path": ledger,
        "identity_ledger_sha256": support.digest(ledger.read_bytes()),
        "identity_reservation": reservation, "execution_nonce": "SYNTHETIC_TEST_ONLY",
        "approval_sha256": "synthetic_not_authority",
        "verified": {"freeze_sha256": "synthetic_not_authority"},
    }
    return permit, budget(), output, reservation


def test_exclusive_reservation_open_failure_does_not_consume_identity(tmp_path, monkeypatch):
    permit, evidence_budget, output, reservation = synthetic_reservation_fixture(
        tmp_path, monkeypatch)
    original_open = support.os.open

    def denied_open(path, flags, mode=0o777):
        if Path(path) == reservation:
            raise PermissionError("synthetic exclusive open failure")
        return original_open(path, flags, mode)

    monkeypatch.setattr(support.os, "open", denied_open)
    with pytest.raises(PermissionError, match="synthetic exclusive open"):
        support.consume_execution_permit(permit, output, budget=evidence_budget)
    assert support._PERMITS[permit]["consumed"] is False
    assert not reservation.exists() and not output.exists()
    # Conservatively charged attempted bytes are not an identity reservation.
    assert evidence_budget.output_bytes > 0


@pytest.mark.parametrize("stage", ["write", "flush", "fsync"])
def test_postcreate_marker_failure_is_consumed_and_partial_marker_cannot_be_reused(
        tmp_path, monkeypatch, stage):
    permit, evidence_budget, output, reservation = synthetic_reservation_fixture(
        tmp_path, monkeypatch)
    original_fdopen = support.os.fdopen
    handles = []

    class FailedHandle:
        def __init__(self, descriptor, mode):
            self.handle = original_fdopen(descriptor, mode)
            handles.append(self.handle)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.handle.close()

        def close(self):
            self.handle.close()

        def write(self, data):
            if stage == "write":
                self.handle.write(data[:7])
                raise OSError("synthetic marker write failure")
            return self.handle.write(data)

        def flush(self):
            self.handle.flush()
            if stage == "flush":
                raise OSError("synthetic marker flush failure")

        def fileno(self):
            return self.handle.fileno()

    monkeypatch.setattr(support.os, "fdopen", FailedHandle)
    if stage == "fsync":
        original_fsync = support.os.fsync

        def failed_fsync(descriptor):
            if stat.S_ISREG(support.os.fstat(descriptor).st_mode):
                raise OSError("synthetic marker fsync failure")
            return original_fsync(descriptor)
        monkeypatch.setattr(support.os, "fsync", failed_fsync)
    with pytest.raises(OSError, match="synthetic marker " + stage):
        support.consume_execution_permit(permit, output, budget=evidence_budget)
    assert support._PERMITS[permit]["consumed"] is True
    assert handles and all(handle.closed for handle in handles)
    raw = reservation.read_bytes()
    assert raw and not output.exists()
    assert evidence_budget.output_bytes >= len(raw)
    with pytest.raises(support.AdmissionError, match="already consumed"):
        support.consume_execution_permit(permit, output, budget=evidence_budget)
    other = object.__new__(support.ExecutionPermit)
    other_output = tmp_path / "synthetic-other-output"
    support._PERMITS[other] = {**support._PERMITS[permit], "consumed": False,
                              "output_directory": other_output}
    with pytest.raises(FileExistsError):
        support.consume_execution_permit(other, other_output, budget=budget())
    assert reservation.read_bytes() == raw
    assert not other_output.exists()


class SyntheticDurabilityProbe:
    """Real temporary descriptors with bounded, local fault injection; never model code."""

    def __init__(self, monkeypatch, target, stage=None, consumed=None):
        self.target, self.stage, self.consumed = target, stage, consumed
        self.events, self.opened = [], set()
        self.descriptors = {}
        self.created = False
        self.file_closed = False
        original_open = support.os.open
        original_close = support.os.close
        original_fsync = support.os.fsync
        original_fdopen = support.os.fdopen
        probe = self

        def fail(label):
            if probe.stage == label:
                raise OSError("synthetic durability failure: " + label)

        def phase():
            return "after" if probe.file_closed else "before"

        def opened(path, flags, mode=0o777):
            is_directory = bool(flags & support.os.O_DIRECTORY)
            if is_directory and probe.created:
                if probe.consumed is not None:
                    assert probe.consumed() is True
                fail("dir_open_" + phase())
            descriptor = original_open(path, flags, mode)
            kind = "dir" if is_directory else "file"
            probe.descriptors[descriptor] = kind
            probe.opened.add(descriptor)
            probe.events.append((kind + "_open", str(path)))
            if Path(path) == probe.target:
                probe.created = True
            return descriptor

        def closed(descriptor):
            kind = probe.descriptors[descriptor]
            original_close(descriptor)
            probe.opened.discard(descriptor)
            probe.events.append((kind + "_close", None))
            if kind == "dir" and probe.created:
                fail("dir_close_" + phase())

        def synced(descriptor):
            kind = probe.descriptors[descriptor]
            probe.events.append((kind + "_fsync", None))
            if kind == "dir" and probe.created:
                fail("dir_fsync_" + phase())
            if kind == "file":
                fail("file_fsync")
            original_fsync(descriptor)

        class Handle:
            def __init__(self, descriptor, mode):
                probe.events.append(("fdopen", None))
                fail("fdopen")
                self.descriptor = descriptor
                self.handle = original_fdopen(descriptor, mode)

            def write(self, raw):
                probe.events.append(("file_write", None))
                if probe.stage in {"write", "short_write"}:
                    size = self.handle.write(raw[:7])
                    fail("write")
                    return size
                return self.handle.write(raw)

            def flush(self):
                probe.events.append(("file_flush", None))
                self.handle.flush()
                fail("flush")

            def fileno(self):
                return self.handle.fileno()

            def close(self):
                self.handle.close()
                probe.opened.discard(self.descriptor)
                probe.file_closed = True
                probe.events.append(("file_close", None))
                fail("file_close")

        monkeypatch.setattr(support.os, "open", opened)
        monkeypatch.setattr(support.os, "close", closed)
        monkeypatch.setattr(support.os, "fsync", synced)
        monkeypatch.setattr(support.os, "fdopen", Handle)


@pytest.mark.parametrize("kind", ["reservation", "evidence"])
@pytest.mark.parametrize("stage", ["dir_open_before", "dir_fsync_before", "dir_close_before",
                                   "fdopen", "write", "short_write", "flush", "file_fsync",
                                   "file_close", "dir_open_after", "dir_fsync_after",
                                   "dir_close_after"])
def test_postcreate_durability_failures_close_descriptors_and_never_acknowledge(
        tmp_path, monkeypatch, kind, stage):
    if kind == "reservation":
        permit, b, output, target = synthetic_reservation_fixture(tmp_path, monkeypatch)
        consumed = lambda: support._PERMITS[permit]["consumed"]  # noqa: E731
        operation = lambda: support.consume_execution_permit(permit, output, budget=b)  # noqa: E731
        writer = None
    else:
        writer = support.ExclusiveEvidenceWriter(tmp_path / "evidence", support.IDENTITY, budget())
        target = writer.path / "incomplete.raw"
        consumed = None
        operation = lambda: writer.raw_bytes(target.name, b"synthetic primitive bytes")  # noqa: E731
    probe = SyntheticDurabilityProbe(monkeypatch, target, stage, consumed)
    with pytest.raises(OSError, match="durability failure|short durable evidence write"):
        operation()
    assert target.exists()
    assert probe.opened == set()
    if kind == "reservation":
        assert support._PERMITS[permit]["consumed"] is True
        assert not output.exists()
        with pytest.raises(support.AdmissionError, match="already consumed"):
            operation()
    else:
        assert not any(row["name"] == target.name for row in writer.records)
        assert writer.write_attempts[-1]["complete"] is False
        with pytest.raises(support.AdmissionError, match="durable raw"):
            writer.verdict("forbidden-verdict.json", {"synthetic": True}, raw_names=[target.name])
        with pytest.raises(FileExistsError):
            operation()
    assert probe.opened == set()


@pytest.mark.parametrize("kind", ["reservation", "evidence"])
def test_directory_is_durable_before_payload_and_after_file_sync(tmp_path, monkeypatch, kind):
    if kind == "reservation":
        permit, b, output, target = synthetic_reservation_fixture(tmp_path, monkeypatch)
        consumed = lambda: support._PERMITS[permit]["consumed"]  # noqa: E731
        operation = lambda: support.consume_execution_permit(permit, output, budget=b)  # noqa: E731
    else:
        writer = support.ExclusiveEvidenceWriter(tmp_path / "evidence", support.IDENTITY, budget())
        target = writer.path / "durable.raw"
        consumed = None
        operation = lambda: writer.raw_bytes(target.name, b"synthetic bytes")  # noqa: E731
    probe = SyntheticDurabilityProbe(monkeypatch, target, consumed=consumed)
    operation()
    start = next(index for index, event in enumerate(probe.events)
                 if event == ("file_open", str(target)))
    sequence = [event[0] for event in probe.events[start:]]
    assert sequence == ["file_open", "dir_open", "dir_fsync", "dir_close", "fdopen",
                        "file_write", "file_flush", "file_fsync", "file_close",
                        "dir_open", "dir_fsync", "dir_close"]
    assert target.read_bytes()
    assert probe.opened == set()


@pytest.mark.parametrize("stage", ["open", "fsync", "close"])
def test_provisioning_failure_precedes_reservation_and_byte_charge(tmp_path, monkeypatch, stage):
    permit, b, output, target = synthetic_reservation_fixture(tmp_path, monkeypatch)
    original_open, original_fsync, original_close = (
        support.os.open, support.os.fsync, support.os.close)
    opened = set()

    def open_directory(path, flags, mode=0o777):
        if flags & support.os.O_DIRECTORY and stage == "open":
            raise OSError("synthetic provisioning open")
        descriptor = original_open(path, flags, mode)
        opened.add(descriptor)
        return descriptor

    def sync_directory(descriptor):
        if stage == "fsync":
            raise OSError("synthetic provisioning fsync")
        original_fsync(descriptor)

    def close_directory(descriptor):
        original_close(descriptor)
        opened.discard(descriptor)
        if stage == "close":
            raise OSError("synthetic provisioning close")

    monkeypatch.setattr(support.os, "open", open_directory)
    monkeypatch.setattr(support.os, "fsync", sync_directory)
    monkeypatch.setattr(support.os, "close", close_directory)
    with pytest.raises(OSError, match="synthetic provisioning " + stage):
        support.consume_execution_permit(permit, output, budget=b)
    assert support._PERMITS[permit]["consumed"] is False
    assert b.output_bytes == 0
    assert not target.exists() and not output.exists()
    assert opened == set()


def test_provisioning_syncs_only_directory_and_parent_under_declared_boundary(
        tmp_path, monkeypatch):
    directory = tmp_path / "new-reservation-directory"
    directory.mkdir()
    synchronized = []
    monkeypatch.setattr(support, "fsync_directory", lambda path: synchronized.append(path))
    support.fsync_directory_provisioning(directory)
    assert synchronized == [directory.parent, directory]
    assert "Older directory ancestors are trusted" in support.FILESYSTEM_DURABILITY_BOUNDARY
    assert "ephemeral-storage loss" in support.FILESYSTEM_DURABILITY_BOUNDARY
    assert "not permission to retry" in support.FILESYSTEM_DURABILITY_BOUNDARY


@pytest.mark.parametrize("directory_kind", ["parent", "output"])
@pytest.mark.parametrize("stage", ["open", "fsync", "close"])
def test_new_evidence_directory_sync_failure_is_retained_and_never_started(
        tmp_path, monkeypatch, directory_kind, stage):
    output = tmp_path / "synthetic-new-output"
    target_directory = tmp_path if directory_kind == "parent" else output
    state = {"created": False}
    opened, targeted = set(), set()
    original_mkdir, original_open = support.os.mkdir, support.os.open
    original_close, original_fsync = support.os.close, support.os.fsync
    b = budget()

    def mkdir(path, mode=0o777, **kwargs):
        original_mkdir(path, mode, **kwargs)
        if Path(path) == output:
            state["created"] = True

    def open_directory(path, flags, mode=0o777):
        applies = state["created"] and Path(path) == target_directory
        if applies and stage == "open":
            raise OSError("synthetic new directory open")
        descriptor = original_open(path, flags, mode)
        opened.add(descriptor)
        if applies:
            targeted.add(descriptor)
        return descriptor

    def sync_directory(descriptor):
        if descriptor in targeted and stage == "fsync":
            raise OSError("synthetic new directory fsync")
        original_fsync(descriptor)

    def close_directory(descriptor):
        applies = descriptor in targeted
        original_close(descriptor)
        opened.discard(descriptor)
        targeted.discard(descriptor)
        if applies and stage == "close":
            raise OSError("synthetic new directory close")

    monkeypatch.setattr(support.os, "mkdir", mkdir)
    monkeypatch.setattr(support.os, "open", open_directory)
    monkeypatch.setattr(support.os, "fsync", sync_directory)
    monkeypatch.setattr(support.os, "close", close_directory)
    with pytest.raises(OSError, match="synthetic new directory " + stage):
        support.ExclusiveEvidenceWriter(output, support.IDENTITY, b)
    assert output.is_dir()
    assert not (output / "STARTED.json").exists()
    assert b.output_bytes == 0
    assert opened == set()
    state["created"] = False
    with pytest.raises(FileExistsError):
        support.ExclusiveEvidenceWriter(output, support.IDENTITY, b)
    assert opened == set()


@pytest.mark.parametrize("stage", ["file_close", "dir_open_after",
                                   "dir_fsync_after", "dir_close_after"])
def test_complete_looking_success_bytes_do_not_acknowledge_failed_terminal_sync(
        tmp_path, monkeypatch, stage):
    writer = support.ExclusiveEvidenceWriter(tmp_path / "evidence", support.IDENTITY, budget())
    writer.raw_bytes("earlier.raw", b"durable synthetic raw evidence")
    target = writer.path / "TERMINAL.json"
    probe = SyntheticDurabilityProbe(monkeypatch, target, stage)
    with pytest.raises(OSError, match="synthetic durability failure"):
        writer.terminal("SUCCESS", {"synthetic_only": True, "real_g0_executed": False})
    manifest = json.loads(target.read_bytes())
    assert manifest["status"] == "SUCCESS"
    assert "launcher status" in manifest["terminal_acknowledgment"]
    assert writer.closed is False
    assert writer.write_attempts[-1]["complete"] is False
    assert not any(row["kind"] == "terminal" for row in writer.records)
    assert (writer.path / "earlier.raw").read_bytes() == b"durable synthetic raw evidence"
    assert probe.opened == set()
    with pytest.raises(FileExistsError):
        writer.terminal("SUCCESS", {"synthetic_only": True})
    assert writer.closed is False
    assert probe.opened == set()


class SyntheticBudgetAdvancingWriter:
    """Simulate a charged durable write that crosses a soft cap before returning."""

    def __init__(self, b, current, key, advance_when):
        self.budget, self.current, self.key = b, current, key
        self.advance_when = advance_when
        self.records = []

    def log(self, name, raw, value=None):
        self.budget.reserve_output(len(raw))
        self.records.append({"name": name, "bytes": len(raw), "value": value})
        if self.advance_when(name, value):
            boundary = self.budget.limits[self.key] - self.budget.reserves[self.key]
            if self.key == "output_bytes":
                self.budget.output_bytes = boundary
            else:
                self.current[self.key] = boundary

    def raw_json(self, name, value):
        self.log(name, support.canonical(value), support.primitive(value))

    def raw_bytes(self, name, raw):
        self.log(name, raw)


@pytest.mark.parametrize("key", list(support.LIMITS))
def test_manual_before_rechecks_after_durable_attempt_logging(tmp_path, key):
    current = sample()
    b = support.ResourceBudget(sampler=lambda: current)
    writer = SyntheticBudgetAdvancingWriter(
        b, current, key, lambda name, value: value is not None and value["kind"] == "call_attempt")
    monitor = support.PassiveCallMonitor(tmp_path, {"act": 1}, b, writer,
                                        targets={}, allowed_functions=set())
    following = []
    with pytest.raises(support.BudgetExceeded):
        monitor.before("act")
        following.append("mock dynamics")
    assert following == []
    assert monitor.counts["act"] == 1
    assert writer.records[0]["value"]["kind"] == "call_attempt"
    assert b.failure is not None


@pytest.mark.parametrize("key", list(support.LIMITS))
def test_predecode_raw_capture_cannot_cross_budget_then_enter_decoder(tmp_path, key):
    current, steps = sample(), []
    b = support.ResourceBudget(sampler=lambda: current)
    writer = SyntheticBudgetAdvancingWriter(
        b, current, key, lambda name, value: name.startswith("native-load-input-"))
    decode = synthetic_function(tmp_path, "mock.py",
                                "def decode(raw):\n    steps.append('decode body')\n    return 1\n",
                                "decode", {"steps": steps})
    monitor = support.PassiveCallMonitor(
        tmp_path, {"direct_checkpoint_load_bytes": 1}, b, writer,
        targets={"direct_checkpoint_load_bytes": ("mock.py", "decode")}, allowed_functions=set())
    with pytest.raises(support.BudgetExceeded):
        with monitor:
            decode(b"synthetic checkpoint input")
    assert steps == []
    assert any(row["name"].startswith("native-load-input-") for row in writer.records)
    assert monitor.counts["direct_checkpoint_load_bytes"] == 1
    assert monitor.returned["direct_checkpoint_load_bytes"] == 0
    assert b.failure is not None


@pytest.mark.parametrize("key", list(support.LIMITS))
@pytest.mark.parametrize("phase", ["return_event", "checkpoint_capture"])
def test_return_logging_cannot_cross_budget_then_resume_caller_dynamics(tmp_path, key, phase):
    current, steps = sample(), []
    b = support.ResourceBudget(sampler=lambda: current)

    def advance(name, value):
        if phase == "checkpoint_capture":
            return name.startswith("native-checkpoint-")
        return value is not None and value["kind"] == "call_return"

    writer = SyntheticBudgetAdvancingWriter(b, current, key, advance)
    save = synthetic_function(
        tmp_path, "mock.py", "def save(path):\n    steps.append('save body')\n"
        "    path.write_bytes(b'synthetic checkpoint bytes')\n    return 'synthetic digest'\n",
        "save", {"steps": steps})
    target = tmp_path / "temporary-checkpoint.json"
    monitor = support.PassiveCallMonitor(tmp_path, {"direct_checkpoint_save": 1}, b, writer,
                                        targets={"direct_checkpoint_save": ("mock.py", "save")},
                                        allowed_functions=set())
    with pytest.raises(support.BudgetExceeded):
        with monitor:
            save(target)
            steps.append("following caller dynamics")
    assert steps == ["save body"]
    assert target.read_bytes() == b"synthetic checkpoint bytes"
    assert monitor.returned["direct_checkpoint_save"] == 1
    assert b.failure is not None


def test_shell_return_trace_logging_rechecks_before_next_caller_line(tmp_path):
    current, steps = sample(), []
    b = support.ResourceBudget(sampler=lambda: current)
    writer = SyntheticBudgetAdvancingWriter(
        b, current, "wall_seconds",
        lambda name, value: value is not None and value["kind"] == "resource_birth")
    cls = type("IntegratedV03Brain", (), {"__module__": "sparkbrain.v03.runtime"})
    construct = synthetic_function(
        tmp_path, "scripts/g0_joint_ownership.py", "def _construct(cls):\n"
        "    clone = object.__new__(cls)\n    steps.append('following shell dynamics')\n"
        "    return clone\n", "_construct", {"steps": steps})
    monitor = support.PassiveCallMonitor(tmp_path, {"rawbrain_shell": 1}, b, writer, targets={})
    with pytest.raises(support.BudgetExceeded):
        with monitor:
            construct(cls)
    assert steps == []
    assert monitor.returned["rawbrain_shell"] == 1
    assert len(monitor.births) == 1
    assert b.failure is not None


def test_uncharged_profile_and_trace_callbacks_do_not_resample_budget(tmp_path, monkeypatch):
    from types import SimpleNamespace

    sampled = []

    def sampler():
        sampled.append(1)
        return sample()

    b = support.ResourceBudget(sampler=sampler)
    monitor = support.PassiveCallMonitor(tmp_path, {}, b, targets={}, allowed_functions=set())
    monkeypatch.setattr(monitor, "_profile_inner", lambda *args: None)
    monitor._profile(object(), "call", None)
    frame = SimpleNamespace(f_code=SimpleNamespace(
        co_filename=str(tmp_path / "scripts/g0_joint_ownership.py"), co_qualname="_construct"))
    monitor._trace(frame, "line", None)
    assert sampled == []


def test_postlog_admission_check_is_finite_and_does_not_log_recursively(tmp_path):
    sampled, current = [], sample()

    def sampler():
        sampled.append(1)
        return current

    b = support.ResourceBudget(sampler=sampler)
    writer = SyntheticBudgetAdvancingWriter(
        b, current, "wall_seconds", lambda name, value: value["kind"] == "call_attempt")
    monitor = support.PassiveCallMonitor(tmp_path, {"act": 1}, b, writer,
                                        targets={}, allowed_functions=set())
    with pytest.raises(support.BudgetExceeded):
        monitor.before("act")
    assert len(sampled) == 3  # initial admission, writer byte charge, one post-log admission
    assert len(writer.records) == len(monitor.events) == 1


@pytest.mark.parametrize("key", list(support.LIMITS))
@pytest.mark.parametrize("terminal", [False, True])
def test_post_io_budget_exhaustion_leaves_complete_bytes_unacknowledged(
        tmp_path, monkeypatch, key, terminal):
    current = sample()
    b = support.ResourceBudget(sampler=lambda: current)
    writer = support.ExclusiveEvidenceWriter(tmp_path / "evidence", support.IDENTITY, b)
    target = writer.path / ("TERMINAL.json" if terminal else "unacknowledged.raw")
    original = support.exclusive_durable_write

    def durable_then_exhausted(path, raw, **kwargs):
        original(path, raw, **kwargs)
        boundary = b.limits[key] if terminal else b.limits[key] - b.reserves[key]
        if key == "output_bytes":
            b.output_bytes = boundary
        else:
            current[key] = boundary

    monkeypatch.setattr(support, "exclusive_durable_write", durable_then_exhausted)
    with pytest.raises(support.BudgetExceeded):
        if terminal:
            writer.terminal("SUCCESS", {"synthetic_only": True, "real_g0_executed": False})
        else:
            writer.raw_bytes(target.name, b"complete synthetic bytes")
    assert target.exists()
    if terminal:
        assert json.loads(target.read_bytes())["status"] == "SUCCESS"
    else:
        assert target.read_bytes() == b"complete synthetic bytes"
    assert writer.closed is False
    assert writer.write_attempts[-1]["complete"] is False
    assert not any(row["name"] == target.name for row in writer.records)
    assert b.failure is not None

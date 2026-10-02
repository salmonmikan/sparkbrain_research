"""Model-free adversarial checks; never evidence of native eligibility or execution."""

from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import os
import random
import subprocess
import sys
import sysconfig
import threading
import types
from pathlib import Path

import pytest

from scripts import m1_path_admission as admission

ROOT = Path(__file__).resolve().parents[1]
SHA = "a" * 64


@pytest.fixture(autouse=True)
def forbid_native_imports(monkeypatch):
    original = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name == "sparkbrain" or name.startswith("sparkbrain."):
            raise AssertionError("these tests must never import SparkBrain")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded)


def binding(path):
    return {"path": path, "sha256": SHA}


def freeze():
    """Schema-only synthetic values, explicitly not a source/runtime freeze."""
    return {
        "schema": "m1-path-execution-freeze-v1",
        "identity": admission.IDENTITY,
        "source_commit": admission.SOURCE_COMMIT,
        "runtime_execution_authorized": False,
        "source_contract": binding(admission.CONTRACT),
        "source_files_sha256": {"synthetic.py": SHA},
        "inputs": binding(admission.ARTIFACT_ROOT + "/inputs.jsonl"),
        "teaching": {
            "evaluator": binding(admission.ARTIFACT_ROOT + "/evaluator.json"),
            "subset_sha256": SHA,
        },
        "configuration": {"synthetic": True},
        "environment": {
            "schema": "m1-path-python-environment-v1",
            "implementation": "CPython",
            "version": "3.11.0 (synthetic source-only fixture)",
            "executable": "/synthetic/python",
            "executable_sha256": SHA,
            "prefix": "/synthetic",
            "base_prefix": "/synthetic",
            "platform": "linux",
            "machine": "synthetic",
            "cache_tag": "synthetic",
            "flags": {"dont_write_bytecode": 1, "no_user_site": 1},
            "sys_path": ["/synthetic"],
            "environment_sha256": SHA,
            "dependency_roots": ["/synthetic/lib"],
            "stdlib": {
                "root": "/synthetic/lib",
                "sources_sha256": dict.fromkeys(admission.STDLIB_ROUTE_SOURCES, SHA),
            },
            "dependency_inventory_sha256": SHA,
            "dependency_files": 1,
            "native_code_sha256": {},
            "mapped_code_sha256": {"/synthetic/python": SHA},
            "external_import_archives": {},
            "venv_configuration_sha256": None,
        },
        "gates": {key: binding("synthetic/" + key + ".json") for key in admission.GATE_NAMES},
        "limits": dict.fromkeys(admission.RESOURCE_KEYS, 2),
        "finalization_reserves": dict.fromkeys(admission.RESOURCE_KEYS, 1),
        "launcher": {
            "implementation": binding("synthetic/launcher.py"),
            "authority_verifier": "verify_authority",
            "runtime_verifier": "verify_runtime",
            "hard_wall_executable": "/synthetic/timeout",
            "hard_wall_sha256": SHA,
            **dict.fromkeys(
                (
                    "offline",
                    "fresh_process",
                    "no_bytecode",
                    "no_user_site",
                    "sanitize_environment",
                    "raw_before_verdict",
                    "exclusive_output",
                    "partial_evidence_retained",
                    "no_retry",
                ),
                True,
            ),
        },
        "ownership": dict.fromkeys(
            (
                "dedicated_serial_owner",
                "owner_thread_cleanup",
                "reverse_allocation_cleanup",
                "zero_live_resources_at_success",
                "no_model_references_escape",
            ),
            True,
        ),
        "one_shot": {
            "identity": admission.IDENTITY,
            "durable_exclusive_reservation": True,
            "reserve_before_native_import": True,
            "failure_consumes_identity": True,
        },
    }


def test_import_is_inert_and_never_imports_native():
    code = """
import builtins, sys
original = builtins.__import__
def guarded(name, *a, **kw):
    if name == 'sparkbrain' or name.startswith('sparkbrain.'):
        raise AssertionError('native import')
    return original(name, *a, **kw)
builtins.__import__ = guarded
from scripts import m1_path_admission as a
assert a.APPROVED_FREEZE_SHA256 is None
assert not any(n == 'sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules)
assert sys.getprofile() is None and sys.gettrace() is None
"""
    result = subprocess.run(
        [sys.executable, "-B", "-s", "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_public_construction_forgery_and_all_launch_entries_fail_closed(tmp_path):
    assert admission.APPROVED_FREEZE_SHA256 is None
    with pytest.raises(admission.AdmissionError):
        admission.Permit()
    forged = object.__new__(admission.Permit)
    with pytest.raises(admission.AdmissionError, match="unissued"):
        _ = forged.root
    with pytest.raises(AttributeError):
        forged.root = tmp_path
    with pytest.raises(admission.AdmissionError, match="cannot be copied"):
        copy.copy(forged)
    for value in (None, object(), forged, {"approved": True}):
        with pytest.raises(admission.AdmissionError, match="no reviewed execution freeze"):
            admission.require_permit(value)
        with pytest.raises(admission.AdmissionError, match="no reviewed execution freeze"):
            admission.claim_owner(value, {"approved": True}, lambda _: True)
    with pytest.raises(admission.AdmissionError, match="no reviewed execution freeze"):
        admission.authorize_execution(
            tmp_path, "missing.json", "approval.json", SHA, lambda _: True
        )
    assert list(tmp_path.iterdir()) == []


def test_schema_only_success_is_detached_and_not_authority():
    source = freeze()
    checked = admission.validate_freeze_schema(source)
    assert checked == source and checked is not source
    checked["limits"]["wall_seconds"] = 999
    assert source["limits"]["wall_seconds"] == 2
    assert admission.APPROVED_FREEZE_SHA256 is None


@pytest.mark.parametrize("key", sorted(admission.FREEZE_KEYS))
def test_every_top_level_gate_is_mandatory(key):
    value = freeze()
    del value[key]
    with pytest.raises(admission.AdmissionError):
        admission.validate_freeze_schema(value)


@pytest.mark.parametrize(
    "edit",
    [
        lambda f: f.update(runtime_execution_authorized=True),
        lambda f: f.update(native_execution_enabled=True),
        lambda f: f.update(source_commit="old-source"),
        lambda f: f["gates"].pop("g0"),
        lambda f: f["gates"].update(constructor_census={"status": "eligible"}),
        lambda f: f["limits"].update(cpu_seconds=True),
        lambda f: f["limits"].update(cpu_seconds=0),
        lambda f: f["finalization_reserves"].update(cpu_seconds=2),
        lambda f: f["finalization_reserves"].update(cpu_seconds=0),
        lambda f: f["limits"].update(unknown=1),
        lambda f: f["launcher"].update(no_retry=False),
        lambda f: f["launcher"].update(authority_verifier="arbitrary.lambda"),
        lambda f: f["ownership"].update(owner_thread_cleanup=False),
        lambda f: f["ownership"].update(owner_thread_cleanup=1),
        lambda f: f["one_shot"].update(reserve_before_native_import=False),
        lambda f: f["one_shot"].update(reserve_before_native_import=1),
        lambda f: f["source_contract"].update(path="../contract.json"),
        lambda f: f["inputs"].update(path="alternate-inputs.jsonl"),
        lambda f: f["teaching"].update(subset_sha256="missing"),
        lambda f: f["environment"].pop("dependency_inventory_sha256"),
        lambda f: f["environment"]["flags"].update(dont_write_bytecode=False),
        lambda f: f["environment"].update(mapped_code_sha256={}),
    ],
)
def test_unknown_missing_false_or_unbounded_fields_are_rejected(edit):
    value = freeze()
    edit(value)
    with pytest.raises(admission.AdmissionError):
        admission.validate_freeze_schema(value)


@pytest.mark.parametrize(
    "raw", [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b"\xff", b"{"]
)
def test_json_rejects_duplicate_nonfinite_and_malformed_values(raw):
    with pytest.raises(admission.AdmissionError):
        admission.parse_json(raw)


def test_json_refuses_conversion_hooks():
    class Hook:
        def __str__(self):
            raise AssertionError("conversion hook must never be invoked")

    with pytest.raises(admission.AdmissionError):
        admission.canonical({"value": Hook()})


def write_json(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = admission.canonical(value)
    path.write_bytes(raw)
    return {"path": name, "sha256": admission.digest(raw)}


def bind_stdlib_fixture(value, directory):
    """Bind explicit fixture/host files without representing a real environment snapshot."""
    value["environment"]["dependency_roots"] = [str(directory)]
    value["environment"]["stdlib"] = {
        "root": str(directory),
        "sources_sha256": {
            name: admission.digest((directory / name).read_bytes())
            for name in admission.STDLIB_ROUTE_SOURCES
        },
    }


def synthetic_stdlib_fixture(root, value):
    """Source-shaped supported-version ASTs, never imported or executed."""
    sources = {
        "enum.py": "class Enum:\n    def __init__(self, *args, **kwargs): pass\n",
        "random.py": "class Random:\n    def __init__(self, x=None): pass\n",
        "threading.py": "def RLock(*args, **kwargs): pass\n",
        "dataclasses.py": "def _init_fn(*args, **kwargs): pass\n",
        "copy.py": "def deepcopy(x, memo=None): pass\n"
        "def _reconstruct(x, memo, func, args): pass\n"
        "def _deepcopy_dict(x, memo): pass\n",
        "copyreg.py": "def __newobj__(cls, *args): pass\n",
        "tempfile.py": "class _RandomNameSequence:\n    def rng(self): pass\n",
    }
    directory = root / "declared-stdlib"
    directory.mkdir()
    for name, source in sources.items():
        (directory / name).write_text(source)
    bind_stdlib_fixture(value, directory)


def gate_fixture(root):
    value = freeze()
    synthetic_stdlib_fixture(root, value)
    raw = write_json(root, "raw.json", {"synthetic": True})
    terminal = write_json(
        root, "terminal.json", {"identity": "assembly-m1-g0-v1-20261002", "status": "SUCCESS"}
    )
    contract = source_shaped_census_contract(root, value)
    old_runtime = {**contract["runtime_sources_sha256"], "src/sparkbrain/example.py": "b" * 64}
    per_type = {
        name: {"init": 0, "shell": 0}
        for name in set(contract["allocation_type_sources"])
        | {"random:Random", "_thread:lock", "_thread:RLock"}
    }
    per_type["sparkbrain.example:Example"]["init"] = 1
    per_type["random:Random"]["init"] = 29
    per_type["_thread:RLock"]["init"] = 28
    per_type["_thread:lock"]["shell"] = 1
    for name, count in contract["import_enum_initializations"].items():
        per_type[name]["init"] = count
    common = {
        "source_contract_sha256": SHA,
        "inputs_sha256": value["inputs"]["sha256"],
        "configuration_sha256": admission.digest(admission.canonical(value["configuration"])),
        "raw_evidence": [raw],
    }
    gates = {
        "g0": {
            "status": "SUCCESS",
            "runtime_sources_sha256": old_runtime,
            "terminal": terminal,
        },
        "source_delta_reconciliation": {
            "status": "RECONCILED",
            "from_runtime_sources_sha256": old_runtime,
            "to_runtime_sources_sha256": contract["runtime_sources_sha256"],
            "changed_paths": ["src/sparkbrain/example.py"],
            "g0_evidence_sha256": None,
            "review_reference": "synthetic test only",
        },
        "three_observation_eligibility": {
            "status": "OBSERVED_ELIGIBLE",
            "observations_per_arm": 3,
            "arms": {
                arm: {
                    "fullgraph_verified": True,
                    "checkpoint_roundtrip_verified": True,
                    "evidence": [raw],
                }
                for arm in ("S", "R")
            },
        },
        "constructor_census": {
            "status": "REVIEWED_DERIVATION_WITH_OBSERVED_ELIGIBILITY",
            "observed_eligibility_per_type": per_type,
            "prospective_type_caps": copy.deepcopy(per_type),
            "derivation_reference": "synthetic-only",
            "derived_success_counts": admission.PROSPECTIVE_SUCCESS_COUNTS,
            "prospective_rollback_additions": admission.PROSPECTIVE_ROLLBACK_ADDITIONS,
            "unobserved_routes": [],
            "observed_routes": [
                {
                    "type": "sparkbrain.example:Example",
                    "path": "src/sparkbrain/example.py",
                    "qualname": "Example.__init__",
                    "kind": "init",
                    "count": 1,
                }
            ],
        },
    }
    for name, count in contract["import_enum_initializations"].items():
        gates["constructor_census"]["observed_routes"].append(
            {
                "type": name,
                "path": "stdlib/enum.py",
                "qualname": "Enum.__init__",
                "kind": "init",
                "count": count,
            }
        )
    from scripts.m1_path_census_evidence import RESOURCE_ROUTE_SUCCESS, RESOURCE_TYPES

    for name, path, qualname, count in RESOURCE_ROUTE_SUCCESS:
        typename, kind = RESOURCE_TYPES[name]
        gates["constructor_census"]["observed_routes"].append(
            {"type": typename, "path": path, "qualname": qualname, "kind": kind, "count": count}
        )
    for name, gate in gates.items():
        gate.update(common)
        gate["schema"] = "m1-path-" + name.replace("_", "-") + "-v1"
        if name == "constructor_census":
            refresh_profiler_evidence(root, value, gate)
        if name == "source_delta_reconciliation":
            gate["g0_evidence_sha256"] = value["gates"]["g0"]["sha256"]
        value["gates"][name] = write_json(root, name + ".json", gate)
    return value, contract, gates


def test_synthetic_gate_validation_does_not_issue_permit(tmp_path):
    value, contract, _ = gate_fixture(tmp_path)
    admission._inspect_gates(tmp_path, value, contract)
    assert admission.APPROVED_FREEZE_SHA256 is None


def set_synthetic_observed_count(census, name, kind, count):
    """Keep synthetic raw-route totals consistent so cap checks are isolated."""
    census["observed_eligibility_per_type"][name][kind] = count
    census["observed_routes"] = [
        row for row in census["observed_routes"] if (row["type"], row["kind"]) != (name, kind)
    ]
    if count:
        census["observed_routes"].append(
            {
                "type": name,
                "path": (
                    "src/sparkbrain/example.py"
                    if kind == "init"
                    else "scripts/g0_joint_ownership.py"
                ),
                "qualname": ("Example.__init__" if kind == "init" else "_construct"),
                "kind": kind,
                "count": count,
            }
        )


@pytest.mark.parametrize(
    "name",
    [
        "sparkbrain.example:Example",
        "sparkbrain.v032.contracts:V032StepResult",
        "random:Random",
        "_thread:RLock",
        "_thread:lock",
    ],
)
@pytest.mark.parametrize("kind", ["init", "shell"])
def test_observed_count_above_prospective_type_cap_fails_closed(tmp_path, name, kind):
    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    set_synthetic_observed_count(census, name, kind, 2)
    census["prospective_type_caps"][name][kind] = 1
    value["gates"]["constructor_census"] = write_json(tmp_path, "constructor_census.json", census)
    with pytest.raises(admission.AdmissionError, match="exceeds prospective type cap") as error:
        admission._inspect_gates(tmp_path, value, contract)
    assert name + ":" + kind in str(error.value)


@pytest.mark.parametrize("kind", ["init", "shell"])
@pytest.mark.parametrize("count", [0, 1])
def test_observed_count_equal_to_prospective_type_cap_is_accepted(tmp_path, kind, count):
    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    name = "sparkbrain.example:Example"
    set_synthetic_observed_count(census, name, kind, count)
    census["prospective_type_caps"][name][kind] = count
    refresh_profiler_evidence(tmp_path, value, census)
    value["gates"]["constructor_census"] = write_json(tmp_path, "constructor_census.json", census)
    admission._inspect_gates(tmp_path, value, contract)
    assert admission.APPROVED_FREEZE_SHA256 is None


@pytest.mark.parametrize("transient", ["SensoryChannelDecision", "V032StepResult"])
@pytest.mark.parametrize("field", ["observed_eligibility_per_type", "prospective_type_caps"])
def test_allocation_caps_include_transient_nonretained_types(tmp_path, transient, field):
    value, contract, gates = gate_fixture(tmp_path)
    name = "sparkbrain.v032.contracts:" + transient
    assert name in contract["allocation_type_sources"]
    assert transient not in contract["files"]["src/sparkbrain/example.py"]["classes"]
    del gates["constructor_census"][field][name]
    value["gates"]["constructor_census"] = write_json(
        tmp_path, "constructor_census.json", gates["constructor_census"]
    )
    with pytest.raises(admission.AdmissionError, match=field):
        admission._inspect_gates(tmp_path, value, contract)


def test_retained_graph_inventory_never_substitutes_for_allocation_inventory(tmp_path):
    value, contract, _ = gate_fixture(tmp_path)
    del contract["allocation_type_sources"]
    with pytest.raises(admission.AdmissionError, match="allocation-type source inventory"):
        admission._inspect_gates(tmp_path, value, contract)


@pytest.mark.parametrize("field", ["observed_eligibility_per_type", "prospective_type_caps"])
@pytest.mark.parametrize("kind", ["init", "shell"])
def test_excluded_allocators_require_zero_counts_and_caps(tmp_path, field, kind):
    value, contract, gates = gate_fixture(tmp_path)
    gates["constructor_census"][field]["sparkbrain.example:InheritedOnly"][kind] = 1
    value["gates"]["constructor_census"] = write_json(
        tmp_path, "constructor_census.json", gates["constructor_census"]
    )
    with pytest.raises(admission.AdmissionError, match="excluded constructor requires zero"):
        admission._inspect_gates(tmp_path, value, contract)


@pytest.mark.parametrize(
    "excluded",
    [
        None,
        "not-a-list",
        ["sparkbrain.unknown:Missing"],
        ["sparkbrain.example:InheritedOnly"] * 2,
        ["sparkbrain.example:InheritedOnly", "sparkbrain.example:Example"],
    ],
)
def test_excluded_constructor_inventory_is_mandatory_unique_and_sorted(tmp_path, excluded):
    value, contract, _ = gate_fixture(tmp_path)
    if excluded is None:
        del contract["excluded_constructor_types"]
    else:
        contract["excluded_constructor_types"] = excluded
    with pytest.raises(admission.AdmissionError, match="excluded constructor inventory"):
        admission._inspect_gates(tmp_path, value, contract)


@pytest.mark.parametrize(
    "name,count",
    [
        ("sparkbrain.model:SparkKind", 7),
        ("sparkbrain.model:EventKind", 5),
        ("sparkbrain.v03_seed.revision:TransitionKind", 4),
    ],
)
@pytest.mark.parametrize("field", ["observed_eligibility_per_type", "prospective_type_caps"])
def test_enum_imports_require_source_derived_init_floor(tmp_path, name, count, field):
    value, contract, gates = gate_fixture(tmp_path)
    assert contract["import_enum_initializations"][name] == count
    gates["constructor_census"][field][name]["init"] = count - 1
    value["gates"]["constructor_census"] = write_json(
        tmp_path, "constructor_census.json", gates["constructor_census"]
    )
    with pytest.raises(admission.AdmissionError, match="enum initialization coverage"):
        admission._inspect_gates(tmp_path, value, contract)


@pytest.mark.parametrize(
    "edit",
    [
        lambda c: c.pop("import_enum_initializations"),
        lambda c: c["import_enum_initializations"].pop("sparkbrain.model:SparkKind"),
        lambda c: c["import_enum_initializations"].update({"sparkbrain.model:SparkKind": True}),
        lambda c: c["import_enum_initializations"].update({"sparkbrain.model:SparkKind": 0}),
        lambda c: c["import_enum_initializations"].update({"sparkbrain.example:InheritedOnly": 1}),
        lambda c: c["excluded_constructor_types"].append("sparkbrain.model:SparkKind"),
    ],
)
def test_enum_allowance_is_narrow_complete_and_not_excluded(tmp_path, edit):
    value, contract, _ = gate_fixture(tmp_path)
    edit(contract)
    with pytest.raises(admission.AdmissionError):
        admission._inspect_gates(tmp_path, value, contract)


@pytest.mark.parametrize(
    "name,edit",
    [
        ("g0", lambda g: g.update(status="SOURCE_ONLY_PASS")),
        ("source_delta_reconciliation", lambda g: g.update(changed_paths=[])),
        ("source_delta_reconciliation", lambda g: g.update(g0_evidence_sha256="c" * 64)),
        ("three_observation_eligibility", lambda g: g.update(observations_per_arm=2)),
        (
            "three_observation_eligibility",
            lambda g: g["arms"]["S"].update(fullgraph_verified=False),
        ),
        ("constructor_census", lambda g: g.update(unobserved_routes=["unmeasured"])),
        ("constructor_census", lambda g: g["observed_eligibility_per_type"].pop("random:Random")),
        ("constructor_census", lambda g: g["observed_routes"][0].update(count=2)),
        ("constructor_census", lambda g: g.update(raw_evidence=[])),
    ],
)
def test_actual_evidence_gate_failures_are_terminal(tmp_path, name, edit):
    value, contract, gates = gate_fixture(tmp_path)
    edit(gates[name])
    value["gates"][name] = write_json(tmp_path, name + ".json", gates[name])
    with pytest.raises(admission.AdmissionError):
        admission._inspect_gates(tmp_path, value, contract)


def test_evidence_symlink_and_hash_changes_are_rejected(tmp_path):
    path = tmp_path / "raw.json"
    path.write_bytes(b"{}")
    sha = admission.digest(b"{}")
    with pytest.raises(admission.AdmissionError, match="bytes differ"):
        admission._read_binding(tmp_path, {"path": "raw.json", "sha256": SHA}, "raw")
    (tmp_path / "alias.json").symlink_to(path)
    with pytest.raises(ValueError, match="symlink"):
        admission._read_binding(tmp_path, {"path": "alias.json", "sha256": sha}, "raw")


def synthetic_registry_root(tmp_path, monkeypatch):
    source = b"class Example:\n    def __init__(self):\n        self.value = None\n"
    path = tmp_path / "src" / "fixture_runtime.py"
    path.parent.mkdir()
    path.write_bytes(source)
    module = types.ModuleType("fixture_runtime")
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    monkeypatch.setitem(sys.modules, "fixture_runtime", module)
    contract = {
        "files": {
            "src/fixture_runtime.py": {
                "sha256": hashlib.sha256(source).hexdigest(),
                "classes": {
                    "Example": {"slot_fields": [], "dict_fields": ["value"], "source_hooks": []}
                },
            }
        }
    }
    bound = write_json(tmp_path, admission.CONTRACT, contract)
    monkeypatch.setattr(admission, "verify", lambda root: {"contract_sha256": bound["sha256"]})
    monkeypatch.setattr(admission, "require_permit", lambda permit: permit)
    # This synthetic seam never creates/loads a model and never issues a Permit.
    permit = types.SimpleNamespace(root=tmp_path)
    return permit, module, path


def test_new_binder_uses_populate_not_historical_g0_verifier(tmp_path, monkeypatch):
    from scripts.g0_joint_ownership import SourceRegistry

    permit, module, _ = synthetic_registry_root(tmp_path, monkeypatch)

    def forbidden(*args, **kwargs):
        raise AssertionError("historical binder must not be reused")

    monkeypatch.setattr(SourceRegistry, "from_verified_source", forbidden)
    result = admission.bind_source_registry(permit, (module.Example, random.Random))
    assert result.domain == "VERIFIED_SOURCE_PREPARATION"
    assert result.spec(module.Example).dict_fields == ("value",)
    assert result.spec(random.Random).dict_fields == ("gauss_next",)


@pytest.mark.parametrize("change", ["missing", "duplicate", "path", "hash", "binding"])
def test_binder_rejects_incomplete_duplicate_or_changed_classes(tmp_path, monkeypatch, change):
    permit, module, path = synthetic_registry_root(tmp_path, monkeypatch)
    classes = (module.Example, random.Random)
    if change == "missing":
        classes = (module.Example,)
    elif change == "duplicate":
        classes += (module.Example,)
    elif change == "path":
        module.__file__ = str(tmp_path / "wrong.py")
    elif change == "hash":
        path.write_bytes(path.read_bytes() + b"# changed\n")
    elif change == "binding":
        module.Example = None
    with pytest.raises(admission.AdmissionError):
        admission.bind_source_registry(permit, classes)


@pytest.mark.skipif(
    sys.version_info >= (3, 14), reason="research admission supports CPython 3.11–3.13"
)
def test_unknown_import_root_never_scans_private_tree(tmp_path, monkeypatch):
    admission.sysconfig.get_paths()  # Resolve interpreter metadata before isolating sys.path.
    monkeypatch.setattr(sys, "path", [str(tmp_path / "private")])
    monkeypatch.setattr(
        admission, "_tree_inventory", lambda _: pytest.fail("must reject before scan")
    )
    with pytest.raises(admission.AdmissionError, match="unknown import root"):
        admission.environment_snapshot(ROOT)


def test_new_native_mapping_must_already_be_in_full_inventory(monkeypatch):
    environment = {
        "executable": "/python",
        "executable_sha256": SHA,
        "native_code_sha256": {"/extension.so": SHA},
        "mapped_code_sha256": {"/libc.so": SHA},
    }
    monkeypatch.setattr(admission, "mapped_code_snapshot", lambda: {"/extension.so": SHA})
    admission.verify_mapped_libraries(environment)
    monkeypatch.setattr(admission, "mapped_code_snapshot", lambda: {"/unknown.so": SHA})
    with pytest.raises(admission.AdmissionError, match="new or changed"):
        admission.verify_mapped_libraries(environment)


def test_internal_synthetic_permit_lifecycle_is_thread_affine_and_irrevocable(
    tmp_path, monkeypatch
):
    # This is a model-free capability-state fixture, never the public admission path.
    permit = object.__new__(admission.Permit)
    authority = tmp_path / "authority.json"
    authority.write_bytes(b"{}")
    verified = {"freeze_sha256": SHA, "freeze": {"fixture": True}}
    record = {
        "root": tmp_path,
        "verified": verified,
        "freeze_relative": "fixture.json",
        "authority_relative": "authority.json",
        "authority_sha256": admission.digest(b"{}"),
        "state": "ISSUED",
        "pid": os.getpid(),
        "owner": threading.current_thread(),
        "issuer": threading.current_thread(),
        "claim_attempted": False,
    }
    admission._PERMITS[permit] = record
    monkeypatch.setattr(admission, "APPROVED_FREEZE_SHA256", SHA)
    monkeypatch.setattr(admission, "verify_preparation", lambda *args, **kw: verified)
    with pytest.raises(admission.AdmissionError, match="inactive"):
        admission.require_permit(permit)
    record["state"] = "ACTIVE"
    assert admission.require_permit(permit) is permit
    detached = permit.freeze
    detached["fixture"] = False
    assert permit.freeze["fixture"] is True
    foreign = []

    def on_foreign_thread():
        try:
            admission.require_permit(permit)
        except admission.AdmissionError:
            foreign.append("rejected")

    thread = threading.Thread(target=on_foreign_thread)
    thread.start()
    thread.join()
    assert foreign == ["rejected"]
    authority.write_bytes(b"changed")
    with pytest.raises(admission.AdmissionError, match="authority changed"):
        admission.require_permit(permit)
    assert record["state"] == "POISONED"
    authority.write_bytes(b"{}")
    with pytest.raises(admission.AdmissionError, match="inactive"):
        admission.require_permit(permit)
    admission.close_permit(permit)
    assert record["state"] == "CLOSED"


def test_failed_owner_claim_cannot_be_retried(tmp_path, monkeypatch):
    permit = object.__new__(admission.Permit)
    record = {
        "pid": os.getpid(),
        "state": "ISSUED",
        "claim_attempted": False,
        "issuer": threading.current_thread(),
        "owner": None,
    }
    admission._PERMITS[permit] = record
    monkeypatch.setattr(admission, "APPROVED_FREEZE_SHA256", SHA)
    with pytest.raises(admission.AdmissionError, match="dedicated owner thread"):
        admission.claim_owner(permit, {}, lambda _: True)
    assert record["state"] == "POISONED"
    with pytest.raises(admission.AdmissionError, match="already claimed/poisoned"):
        admission.claim_owner(permit, {}, lambda _: True)


def test_arbitrary_callbacks_are_not_independent_authority(tmp_path):
    with pytest.raises(admission.AdmissionError, match="exact reviewed binding"):
        admission._verify_callback(tmp_path, freeze(), lambda _: True, "authority_verifier")


@pytest.mark.parametrize("version", ["3.10.9", "3.14.0", "4.0.0"])
def test_declared_unreviewed_python_version_is_rejected(version):
    proposal = freeze()
    proposal["environment"]["version"] = version
    with pytest.raises(admission.AdmissionError, match="CPython 3.11 through 3.13"):
        admission.validate_freeze_schema(proposal)


def test_actual_unreviewed_interpreter_rejected_before_environment_scan(monkeypatch):
    with monkeypatch.context() as patch:
        patch.setattr(admission.sys, "version_info", (3, 14, 0))
        with pytest.raises(admission.AdmissionError, match="CPython 3.11 through 3.13"):
            admission.environment_snapshot(ROOT)


def source_shaped_census_contract(root, value):
    from scripts.m1_path_census_evidence import CALL_PLAN, PROPOSAL
    from scripts.verify_g0_joint_source_contract import class_spec

    plan = admission.parse_json((ROOT / CALL_PLAN).read_bytes())
    sources = {
        "src/sparkbrain/example.py": """
class Example:
    def __init__(self):
        self.value = 1
class InheritedOnly(ValueError):
    pass
""",
        "src/sparkbrain/v032/contracts.py": """
from dataclasses import dataclass
@dataclass
class SensoryChannelDecision:
    value: int = 1
@dataclass
class V032StepResult:
    value: int = 1
""",
        "src/sparkbrain/model.py": "from enum import StrEnum\n"
        + "\n".join(
            "class "
            + name
            + "(StrEnum):\n"
            + "\n".join(f'    MEMBER_{index} = "member-{index}"' for index in range(count))
            for name, count in (("SparkKind", 7), ("EventKind", 5))
        ),
        "src/sparkbrain/v03_seed/revision.py": "from enum import StrEnum\n"
        "class TransitionKind(StrEnum):\n"
        + "\n".join(f'    MEMBER_{i} = "member-{i}"' for i in range(4)),
        "src/sparkbrain/v03/runtime.py": """
class IntegratedV03Brain:
    def __init__(self):
        self.value = 1
    def _initialize_runtime(self):
        return None
""",
        "src/sparkbrain/v03_seed/sensory_field.py": """
import copy
from dataclasses import dataclass
@dataclass(slots=True)
class _FeatureState:
    value: int = 1
class AdaptiveSensoryField:
    def observe_with_trace(self):
        working_states = copy.deepcopy(self._states)
        return working_states
""",
        "src/sparkbrain/v032/runtime.py": """
class IntegratedV032Brain:
    def __init__(self):
        self.value = 1
def _shared_step_lock():
    return None
""",
        "src/sparkbrain/v05/topology.py": "def layered_reservoir_topology():\n    return None\n",
        "src/sparkbrain/v032/checkpoint.py": """
_BRAIN = "sparkbrain.v03.runtime:IntegratedV03Brain"
_CLASSES = frozenset({_BRAIN, "sparkbrain.example:Example",
                     "sparkbrain.v032.contracts:SensoryChannelDecision"})
_OBJECT_ATTRS = {"sparkbrain.example:Example": frozenset({"value"})}
def _decode(node):
    return node
class DirectCheckpointManager:
    @staticmethod
    def _load_bytes(raw):
        return raw
""",
        "scripts/g0_joint_ownership.py": "def _construct(value):\n    return value\n",
        "scripts/m1_path_census.py": (ROOT / "scripts/m1_path_census.py").read_text(),
    }
    for path in ("scripts/m1_path_inputs.py", "scripts/m1_path_native.py"):
        sources[path] = (ROOT / path).read_text()
    # Stand-in AST declarations cover the exact reviewed routes without importing
    # or executing any actual model. These bodies do not represent native behavior.
    for path, qualname in plan["call_targets"].values():
        tree = ast.parse(sources.get(path, ""))
        parts = qualname.split(".")
        if len(parts) == 2:
            cls, method = parts
            owners = [
                node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == cls
            ]
            if not owners:
                owner = ast.parse(f"class {cls}:\n    pass\n").body[0]
                tree.body.append(owner)
            else:
                owner = owners[0]
            if not any(
                isinstance(node, ast.FunctionDef) and node.name == method for node in owner.body
            ):
                owner.body.append(ast.parse(f"def {method}(self):\n    return None\n").body[0])
        else:
            assert len(parts) == 1
            if not any(
                isinstance(node, ast.FunctionDef) and node.name == qualname for node in tree.body
            ):
                tree.body.append(ast.parse(f"def {qualname}():\n    return None\n").body[0])
        sources[path] = ast.unparse(tree) + "\n"
    runtime, preparation, allocations, graph = {}, {}, {}, {}
    for path, text in sources.items():
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
        sha = admission.digest(file.read_bytes())
        (runtime if path.startswith("src/") else preparation)[path] = sha
        if not path.startswith("src/"):
            continue
        for node in ast.parse(text).body:
            if isinstance(node, ast.ClassDef):
                name = path[4:-3].replace("/", ".") + ":" + node.name
                allocations[name] = {"path": path, "sha256": sha, "witness": class_spec(node)}
                if node.name in {
                    "Example",
                    "IntegratedV03Brain",
                    "IntegratedV032Brain",
                    "_FeatureState",
                }:
                    graph.setdefault(path, {"sha256": sha, "classes": {}})["classes"][node.name] = (
                        class_spec(node)
                    )
    for path in (PROPOSAL, plan["inputs"]["path"], plan["teaching"]["evaluator"]["path"]):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / path).read_bytes())
        preparation[path] = admission.digest(target.read_bytes())
    value["inputs"] = {key: plan["inputs"][key] for key in ("path", "sha256")}
    value["teaching"] = copy.deepcopy(plan["teaching"])
    value["configuration"] = copy.deepcopy(plan["configuration"])
    plan["runtime_sources_sha256"] = runtime
    plan["support_sources_sha256"] = {
        name: preparation[name] for name in plan["support_sources_sha256"]
    }
    plan_binding = write_json(root, CALL_PLAN, plan)
    preparation[CALL_PLAN] = plan_binding["sha256"]
    value["_synthetic_plan"] = plan
    value["_synthetic_plan_binding"] = plan_binding
    value["source_files_sha256"].update({**runtime, **preparation})
    return {
        "runtime_sources_sha256": runtime,
        "preparation_sources_sha256": preparation,
        "files": graph,
        "eligibility_call_plan": plan_binding,
        "allocation_type_sources": allocations,
        "excluded_constructor_types": ["sparkbrain.example:InheritedOnly"],
        "import_enum_initializations": {
            "sparkbrain.model:SparkKind": 7,
            "sparkbrain.model:EventKind": 5,
            "sparkbrain.v03_seed.revision:TransitionKind": 4,
        },
    }


def refresh_profiler_evidence(root, value, census, *, events=None, snapshot=None):
    """Package source-shaped synthetic records; never represent them as native observations."""
    from scripts.m1_path_census_evidence import RESOURCE_ROUTES, RESOURCE_TYPES

    plan = value["_synthetic_plan"]
    caps = {**plan["successful_calls"], **dict.fromkeys(RESOURCE_ROUTES, 0)}
    if events is None:
        events = []
        type_counts = {
            name: {"init": 0, "shell": 0} for name in census["observed_eligibility_per_type"]
        }
        births = 0

        def event(kind, **details):
            events.append({"sequence": len(events) + 1, "kind": kind, "thread": 17, **details})

        for row in census["observed_routes"]:
            name, kind, route = row["type"], row["kind"], [row["path"], row["qualname"]]
            resource = next(
                (
                    key
                    for key, pair in RESOURCE_TYPES.items()
                    if pair == (name, kind) and tuple(route) in RESOURCE_ROUTES[key]
                ),
                None,
            )
            for _ in range(row["count"]):
                if resource:
                    caps[resource] += 1
                    event("call_attempt", name=resource, route=route, count=caps[resource])
                type_counts[name][kind] += 1
                event(
                    "type_attempt",
                    type=name,
                    allocation=kind,
                    route=route,
                    count=type_counts[name][kind],
                )
                if resource:
                    event("call_return", name=resource)
                births += 1
                event(
                    "type_birth",
                    type=name,
                    allocation=kind,
                    route=route,
                    birth=births,
                    runtime_id=123,
                )  # Deliberate legal address reuse.
        for name, route in plan["call_targets"].items():
            for count in range(1, caps[name] + 1):
                event("call_attempt", name=name, route=route, count=count)
                event("call_return", name=name)
        snapshot = {
            "call_attempts": caps,
            "call_returns": caps,
            "types": {
                name: {**row, "init_return": row["init"], "shell_return": row["shell"]}
                for name, row in type_counts.items()
            },
            "pending_calls": 0,
            "pending_shells": 0,
            "failure": None,
            "events": events,
        }
    else:
        caps = dict(snapshot["call_attempts"])
    event_bindings = [
        write_json(root, f"profile/census-{i:07d}.json", row) for i, row in enumerate(events, 1)
    ]
    snapshot_binding = write_json(root, "profile/snapshot.json", snapshot)
    terminal = {
        "schema": "m1-path-passive-census-terminal-v1",
        "status": "SUCCESS",
        "source_contract_sha256": value["source_contract"]["sha256"],
        "eligibility_call_plan": value["_synthetic_plan_binding"],
        "snapshot": snapshot_binding,
        "events": event_bindings,
        "event_count": len(events),
        "final_sequence": len(events),
        "closed": True,
        "pending_calls": 0,
        "pending_shells": 0,
        "failure": None,
    }
    terminal_binding = write_json(root, "profile/terminal.json", terminal)
    declared = value["environment"]["stdlib"]
    stdlib_sources = {
        name: {"path": str(Path(declared["root"]) / name), "sha256": sha}
        for name, sha in declared["sources_sha256"].items()
    }
    census["profiler_evidence"] = {
        "schema": "m1-path-passive-census-evidence-v1",
        "eligibility_plan": value["_synthetic_plan_binding"],
        "census_implementation": {
            "path": "scripts/m1_path_census.py",
            "sha256": value["source_files_sha256"]["scripts/m1_path_census.py"],
        },
        "stdlib_sources": stdlib_sources,
        "call_targets": {
            name: route for name, route in plan["call_targets"].items() if name in caps
        },
        "call_caps": caps,
        "events": event_bindings,
        "snapshot": snapshot_binding,
        "terminal": terminal_binding,
    }
    census["raw_evidence"] = [*event_bindings, snapshot_binding, terminal_binding]


def replace_observed_route(census, name, kind, path, qualname, count=1):
    set_synthetic_observed_count(census, name, kind, count)
    for row in census["observed_routes"]:
        if (row["type"], row["kind"]) == (name, kind):
            row.update(path=path, qualname=qualname)
    census["prospective_type_caps"][name][kind] = count


def save_census(root, value, census):
    value["gates"]["constructor_census"] = write_json(root, "constructor_census.json", census)


@pytest.mark.parametrize(
    "name,kind,path,qualname",
    [
        ("sparkbrain.example:Example", "init", "src/sparkbrain/example.py", "Example.__init__"),
        (
            "sparkbrain.v032.contracts:SensoryChannelDecision",
            "init",
            "src/sparkbrain/v032/contracts.py",
            "SensoryChannelDecision.__init__[dataclass-generated]",
        ),
        ("sparkbrain.example:Example", "shell", "scripts/g0_joint_ownership.py", "_construct"),
        ("sparkbrain.example:Example", "shell", "src/sparkbrain/v032/checkpoint.py", "_decode"),
        (
            "sparkbrain.v032.contracts:SensoryChannelDecision",
            "shell",
            "src/sparkbrain/v032/checkpoint.py",
            "_decode",
        ),
        (
            "sparkbrain.v03.runtime:IntegratedV03Brain",
            "shell",
            "src/sparkbrain/v032/checkpoint.py",
            "DirectCheckpointManager._load_bytes",
        ),
        ("random:Random", "init", "scripts/g0_joint_ownership.py", "_construct"),
        ("random:Random", "init", "src/sparkbrain/v032/checkpoint.py", "_decode"),
        (
            "random:Random",
            "init",
            "src/sparkbrain/v03/runtime.py",
            "IntegratedV03Brain._initialize_runtime",
        ),
        ("random:Random", "init", "src/sparkbrain/v05/topology.py", "layered_reservoir_topology"),
        ("_thread:RLock", "init", "src/sparkbrain/v032/runtime.py", "_shared_step_lock"),
        ("_thread:lock", "shell", "src/sparkbrain/v032/runtime.py", "<module>"),
    ],
)
def test_raw_census_accepts_exact_supported_source_routes(tmp_path, name, kind, path, qualname):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    replace_observed_route(census, name, kind, path, qualname)
    refresh_profiler_evidence(tmp_path, value, census)
    save_census(tmp_path, value, census)
    _validate_raw_census_evidence(tmp_path, value, contract, census)


@pytest.mark.parametrize(
    "name,kind,path,qualname",
    [
        (
            "sparkbrain.v032.contracts:V032StepResult",
            "init",
            "src/sparkbrain/example.py",
            "Example.__init__",
        ),
        ("sparkbrain.example:Example", "shell", "src/sparkbrain/example.py", "Example.__init__"),
        (
            "sparkbrain.example:Example",
            "init",
            "src/sparkbrain/v05/topology.py",
            "layered_reservoir_topology",
        ),
        ("sparkbrain.example:Example", "init", "synthetic/census.py", "fabricated"),
        ("sparkbrain.example:Example", "init", "src/sparkbrain/example.py", "Missing.__init__"),
        (
            "sparkbrain.example:Example",
            "init",
            "src/sparkbrain/example.py",
            "Example.__init__[dataclass-generated]",
        ),
        (
            "sparkbrain.v03.runtime:IntegratedV03Brain",
            "shell",
            "src/sparkbrain/v032/checkpoint.py",
            "_decode",
        ),
        (
            "sparkbrain.v032.runtime:IntegratedV032Brain",
            "shell",
            "scripts/g0_joint_ownership.py",
            "_construct",
        ),
        (
            "sparkbrain.v032.contracts:V032StepResult",
            "shell",
            "src/sparkbrain/v032/checkpoint.py",
            "_decode",
        ),
        ("random:Random", "shell", "scripts/g0_joint_ownership.py", "_construct"),
    ],
)
def test_fabricated_route_totals_cannot_attest_unsupported_sources(
    tmp_path, name, kind, path, qualname
):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    replace_observed_route(census, name, kind, path, qualname)
    refresh_profiler_evidence(tmp_path, value, census)
    save_census(tmp_path, value, census)
    with pytest.raises(admission.AdmissionError, match="outside exact source support"):
        _validate_raw_census_evidence(tmp_path, value, contract, census)


def read_profile(root, census):
    profile = census["profiler_evidence"]
    snapshot = admission.parse_json((root / profile["snapshot"]["path"]).read_bytes())
    return copy.deepcopy(snapshot["events"]), snapshot


@pytest.mark.parametrize(
    "change",
    [
        "sequence_gap",
        "sequence_duplicate",
        "cumulative_count",
        "birth_without_attempt",
        "birth_sequence",
        "unexpected_field",
        "exception",
        "unknown_kind",
        "wrong_thread",
        "missing_tail",
        "snapshot_pending",
        "snapshot_failure",
        "snapshot_totals",
        "raw_summary_route",
        "resource_ancillary",
        "unbound_ancillary",
        "terminal_pending",
    ],
)
def test_raw_profiler_event_and_terminal_integrity_fail_closed(tmp_path, change):
    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    events, snapshot = read_profile(tmp_path, census)
    if change == "sequence_gap":
        events[0]["sequence"] = 2
    elif change == "sequence_duplicate":
        events[1]["sequence"] = 1
    elif change == "cumulative_count":
        events[0]["count"] = 2
    elif change == "birth_without_attempt":
        events[0] = {**events[1], "sequence": 1}
    elif change == "birth_sequence":
        events[1]["birth"] = 2
    elif change == "unexpected_field":
        events[0]["unexpected"] = True
    elif change == "exception":
        events[0] = {"sequence": 1, "thread": 17, "kind": "init_exception", "name": "Example"}
    elif change == "unknown_kind":
        events[0]["kind"] = "made_up"
    elif change == "wrong_thread":
        events[1]["thread"] = 18
    elif change == "missing_tail":
        events.pop()
    elif change == "snapshot_pending":
        snapshot["pending_calls"] = 1
    elif change == "snapshot_failure":
        snapshot["failure"] = "poisoned"
    elif change == "snapshot_totals":
        snapshot["types"]["sparkbrain.example:Example"]["init_return"] = 0
    elif change == "raw_summary_route":
        events[0]["route"] = events[1]["route"] = ["scripts/g0_joint_ownership.py", "_construct"]
        events[0]["allocation"] = events[1]["allocation"] = "shell"
        snapshot["types"]["sparkbrain.example:Example"] = {
            "init": 0,
            "shell": 1,
            "init_return": 0,
            "shell_return": 1,
        }
    elif change in {"resource_ancillary", "unbound_ancillary"}:
        route = (
            ["scripts/g0_joint_ownership.py", "_construct"]
            if change == "resource_ancillary"
            else ["synthetic/census.py", "unknown"]
        )
        events.append(
            {"sequence": len(events) + 1, "thread": 17, "kind": "ancillary_rng", "route": route}
        )
    if change != "missing_tail":
        snapshot["events"] = events
    refresh_profiler_evidence(tmp_path, value, census, events=events, snapshot=snapshot)
    if change == "terminal_pending":
        profile = census["profiler_evidence"]
        terminal = admission.parse_json((tmp_path / profile["terminal"]["path"]).read_bytes())
        terminal["pending_shells"] = 1
        profile["terminal"] = write_json(tmp_path, "profile/terminal.json", terminal)
        census["raw_evidence"][-1] = profile["terminal"]
    save_census(tmp_path, value, census)
    with pytest.raises(admission.AdmissionError):
        admission._inspect_gates(tmp_path, value, contract)


def test_raw_event_hash_and_source_hash_are_both_bound(tmp_path):
    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    event = tmp_path / census["profiler_evidence"]["events"][0]["path"]
    original = event.read_bytes()
    event.write_bytes(original + b" ")
    with pytest.raises(admission.AdmissionError, match="bytes differ"):
        admission._inspect_gates(tmp_path, value, contract)
    event.write_bytes(original)
    source = tmp_path / "src/sparkbrain/example.py"
    source.write_text(source.read_text() + "# stale source\n")
    with pytest.raises(admission.AdmissionError, match="bytes differ"):
        admission._inspect_gates(tmp_path, value, contract)


def test_duplicate_or_truncated_event_manifest_cannot_override_terminal(tmp_path):
    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    census["profiler_evidence"]["events"].pop()
    save_census(tmp_path, value, census)
    with pytest.raises(admission.AdmissionError, match="terminal"):
        admission._inspect_gates(tmp_path, value, contract)


@pytest.mark.skipif(sys.version_info >= (3, 14), reason="PassiveCensus supports CPython 3.11–3.13")
def test_real_passive_census_standin_dataclass_enum_recording_validates(tmp_path, monkeypatch):
    from scripts.m1_path_census import PassiveCensus, source_functions
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    names = census["prospective_type_caps"]
    names["sparkbrain.v032.contracts:SensoryChannelDecision"]["init"] = 1

    class Budget:
        def check(self):
            return {}

        def poison(self, reason):
            raise AssertionError(reason)

    class Writer:
        def raw_json(self, name, row):
            return None

        def raw_bytes(self, name, row):
            raise AssertionError("no checkpoint/model execution in this fixture")

    modules = {}
    for name in (
        "sparkbrain.model",
        "sparkbrain.v03_seed.revision",
        "sparkbrain.example",
        "sparkbrain.v032.contracts",
    ):
        module = types.ModuleType(name)
        monkeypatch.setitem(sys.modules, name, module)
        modules[name] = module
    profile = PassiveCensus(
        tmp_path,
        targets={},
        call_caps=dict.fromkeys(("model_rng", "topology_rng", "model_lock", "registry_guard"), 0),
        type_caps=names,
        allowed_functions=source_functions(tmp_path, list(contract["runtime_sources_sha256"])),
        budget=Budget(),
        writer=Writer(),
    )
    profile.install()
    try:
        for name, module in modules.items():
            path = tmp_path / ("src/" + name.replace(".", "/") + ".py")
            exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
        modules["sparkbrain.example"].Example()
        modules["sparkbrain.v032.contracts"].SensoryChannelDecision()
    finally:
        profile.close()
    snapshot = profile.snapshot()
    census["observed_eligibility_per_type"] = {
        name: {"init": row["init"], "shell": row["shell"]}
        for name, row in snapshot["types"].items()
    }
    from collections import Counter

    routes = Counter(
        (event["type"], *event["route"], event["allocation"])
        for event in snapshot["events"]
        if event["kind"] == "type_attempt"
    )
    census["observed_routes"] = [
        {"type": key[0], "path": key[1], "qualname": key[2], "kind": key[3], "count": count}
        for key, count in routes.items()
    ]
    bind_stdlib_fixture(value, Path(sysconfig.get_path("stdlib")))
    refresh_profiler_evidence(tmp_path, value, census, events=snapshot["events"], snapshot=snapshot)
    save_census(tmp_path, value, census)
    _validate_raw_census_evidence(tmp_path, value, contract, census)
    assert any(
        row["qualname"].endswith("[dataclass-generated]") for row in census["observed_routes"]
    )
    assert any(row["path"] == "stdlib/enum.py" for row in census["observed_routes"])


def test_feature_state_copyreg_shell_has_one_exact_source_bound_route(tmp_path):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    replace_observed_route(
        census,
        "sparkbrain.v03_seed.sensory_field:_FeatureState",
        "shell",
        "stdlib/copyreg.py",
        "__newobj__",
    )
    refresh_profiler_evidence(tmp_path, value, census)
    save_census(tmp_path, value, census)
    _validate_raw_census_evidence(tmp_path, value, contract, census)


@pytest.mark.parametrize(
    "name,kind,qualname",
    [
        ("sparkbrain.example:Example", "shell", "__newobj__"),
        ("sparkbrain.v03_seed.sensory_field:_FeatureState", "init", "__newobj__"),
        ("sparkbrain.v03_seed.sensory_field:_FeatureState", "shell", "__newobj_ex__"),
    ],
)
def test_copyreg_allowance_never_expands_type_allocation_or_function(
    tmp_path, name, kind, qualname
):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    replace_observed_route(census, name, kind, "stdlib/copyreg.py", qualname)
    refresh_profiler_evidence(tmp_path, value, census)
    save_census(tmp_path, value, census)
    with pytest.raises(admission.AdmissionError, match="outside exact source support"):
        _validate_raw_census_evidence(tmp_path, value, contract, census)


@pytest.mark.parametrize("source", ["copy.py", "copyreg.py"])
def test_copyreg_shell_requires_both_stdlib_source_bindings(tmp_path, source):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    del census["profiler_evidence"]["stdlib_sources"][source]
    save_census(tmp_path, value, census)
    with pytest.raises(admission.AdmissionError, match="stdlib source bindings"):
        _validate_raw_census_evidence(tmp_path, value, contract, census)


@pytest.mark.parametrize(
    "change",
    [
        "other_input",
        "extra_args",
        "other_target",
        "custom_new",
        "custom_reduce",
        "inherited",
        "alias_copy",
    ],
)
def test_feature_copy_support_requires_exact_native_ast_witness(tmp_path, change):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence
    from scripts.verify_g0_joint_source_contract import class_spec

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    relative = "src/sparkbrain/v03_seed/sensory_field.py"
    path = tmp_path / relative
    source = path.read_text()
    if change == "other_input":
        source = source.replace("copy.deepcopy(self._states)", "copy.deepcopy(self.other)")
    elif change == "extra_args":
        source = source.replace("copy.deepcopy(self._states)", "copy.deepcopy(self._states, {})")
    elif change == "other_target":
        source = source.replace("working_states =", "other_states =")
    elif change == "custom_new":
        source = source.replace(
            "    value: int = 1",
            "    value: int = 1\n    def __new__(cls):\n        return object.__new__(cls)",
        )
    elif change == "custom_reduce":
        source = source.replace(
            "    value: int = 1",
            "    value: int = 1\n    def __reduce_ex__(self, protocol):\n        return None",
        )
    elif change == "inherited":
        source = source.replace("class _FeatureState:", "class _FeatureState(object):")
    else:
        source = source.replace("import copy", "import copy as alias")
    path.write_text(source)
    sha = admission.digest(path.read_bytes())
    contract["runtime_sources_sha256"][relative] = sha
    value["source_files_sha256"][relative] = sha
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            contract["allocation_type_sources"][
                "sparkbrain.v03_seed.sensory_field:" + node.name
            ] = {"path": relative, "sha256": sha, "witness": class_spec(node)}
    with pytest.raises(admission.AdmissionError, match="feature-state|sensory copy"):
        _validate_raw_census_evidence(tmp_path, value, contract, census)


def test_exact_probe_census_is_software_only_and_mandatory_blocks_remain(tmp_path):
    from scripts.m1_path_census_evidence import CONDITIONAL_UNMET, MANDATORY_UNMET

    value, contract, _ = gate_fixture(tmp_path)
    report = admission._inspect_gates(tmp_path, value, contract)
    assert report["runtime_execution_authorized"] is False
    assert report["mandatory_unmet_obligations"] == list(MANDATORY_UNMET)
    assert "weak_registry_object_birth_census" in report["mandatory_unmet_obligations"]
    assert report["conditional_unmet_coverage"] == list(CONDITIONAL_UNMET)
    with pytest.raises(admission.AdmissionError, match="fixed mandatory unmet obligations"):
        admission._verify_gates(tmp_path, value, contract)
    assert admission.APPROVED_FREEZE_SHA256 is None


def rebind_synthetic_plan(root, value, contract, census, plan):
    from scripts.m1_path_census_evidence import CALL_PLAN

    bound = write_json(root, CALL_PLAN, plan)
    contract["eligibility_call_plan"] = bound
    contract["preparation_sources_sha256"][CALL_PLAN] = bound["sha256"]
    value["source_files_sha256"][CALL_PLAN] = bound["sha256"]
    census["profiler_evidence"]["eligibility_plan"] = bound


@pytest.mark.parametrize(
    "change",
    [
        "empty_map",
        "partial_map",
        "substituted_route",
        "wrong_floor",
        "missing_zero",
        "pilot_counts",
        "extra_target",
        "erase_mandatory",
        "erase_conditional",
        "claim_registry_covered",
        "noncanonical_row",
        "boolean_row",
        "changed_row_hash",
        "different_runtime",
        "different_config",
        "missing_support",
        "proposal_substitution",
        "authorized_flag",
        "wrong_identity",
        "wrong_resource_split",
        "self_digest",
    ],
)
def test_reviewed_plan_cannot_be_redefined_by_caller_even_with_rebound_file_hash(tmp_path, change):
    from scripts.m1_path_census_evidence import _validate_eligibility_plan

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    plan = copy.deepcopy(value["_synthetic_plan"])
    if change == "empty_map":
        plan["call_targets"] = {}
    elif change == "partial_map":
        del plan["call_targets"]["m1_observe"]
    elif change == "substituted_route":
        plan["call_targets"]["m1_observe"] = plan["call_targets"]["m1_outcome"]
    elif change == "wrong_floor":
        plan["successful_calls"]["m1_observe"] = 5
    elif change == "missing_zero":
        del plan["successful_calls"]["producer_learn_outcome"]
    elif change == "pilot_counts":
        plan["successful_calls"]["producer_process"] = 68
        plan["successful_calls"]["m1_observe"] = 14
    elif change == "extra_target":
        plan["call_targets"]["unreviewed"] = ["scripts/g0_joint_ownership.py", "_construct"]
    elif change == "erase_mandatory":
        plan["mandatory_unmet_obligations"] = []
    elif change == "erase_conditional":
        plan["conditional_unmet_coverage"] = []
    elif change == "claim_registry_covered":
        plan["mandatory_unmet_obligations"].remove("weak_registry_object_birth_census")
    elif change == "noncanonical_row":
        plan["inputs"]["selected_indices"][66] = 67
    elif change == "boolean_row":
        plan["inputs"]["selected_indices"][1] = True
    elif change == "changed_row_hash":
        plan["inputs"]["selected_rows_sha256"][0] = SHA
    elif change == "different_runtime":
        plan["runtime_sources_sha256"]["src/sparkbrain/example.py"] = SHA
    elif change == "different_config":
        plan["configuration"] = {"different": True}
    elif change == "missing_support":
        del plan["support_sources_sha256"]["scripts/m1_path_native.py"]
    elif change == "proposal_substitution":
        plan["proposal"]["sha256"] = SHA
    elif change == "authorized_flag":
        plan["runtime_execution_authorized"] = True
    elif change == "wrong_identity":
        plan["identity"] = admission.IDENTITY
    elif change == "wrong_resource_split":
        plan["resource_route_success_calls"][0]["count"] = 28
    else:
        plan["source_contract_sha256"] = SHA
    rebind_synthetic_plan(tmp_path, value, contract, census, plan)
    with pytest.raises(admission.AdmissionError):
        _validate_eligibility_plan(tmp_path, value, contract, census)


@pytest.mark.parametrize(
    "change",
    [
        "missing_plan",
        "unbound_plan",
        "empty_targets",
        "partial_targets",
        "substituted_target",
        "missing_zero_cap",
        "missing_resource_cap",
        "low_cap",
        "boolean_cap",
    ],
)
def test_profiler_requires_exact_source_bound_plan_map_and_all_counter_keys(tmp_path, change):
    from scripts.m1_path_census_evidence import _validate_eligibility_plan

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    profile = census["profiler_evidence"]
    if change == "missing_plan":
        del contract["eligibility_call_plan"]
    elif change == "unbound_plan":
        profile["eligibility_plan"] = {"path": "arbitrary.json", "sha256": SHA}
    elif change == "empty_targets":
        profile["call_targets"] = {}
    elif change == "partial_targets":
        del profile["call_targets"]["m1_observe"]
    elif change == "substituted_target":
        profile["call_targets"]["m1_observe"] = profile["call_targets"]["m1_outcome"]
    elif change == "missing_zero_cap":
        del profile["call_caps"]["producer_learn_outcome"]
    elif change == "missing_resource_cap":
        del profile["call_caps"]["registry_guard"]
    elif change == "low_cap":
        profile["call_caps"]["m1_observe"] = 5
    else:
        profile["call_caps"]["producer_init"] = True
    with pytest.raises(admission.AdmissionError):
        _validate_eligibility_plan(tmp_path, value, contract, census)


@pytest.mark.parametrize(
    "counter,count", [("m1_observe", 5), ("producer_process", 68), ("producer_learn_outcome", 1)]
)
def test_complete_raw_attempt_return_vector_must_equal_reviewed_probe_exposure(
    tmp_path, counter, count
):
    from scripts.m1_path_census_evidence import validate_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    events, snapshot = read_profile(tmp_path, census)
    route = census["profiler_evidence"]["call_targets"][counter]
    events = [
        event
        for event in events
        if not (event["kind"].startswith("call_") and event["name"] == counter)
    ]
    for current in range(1, count + 1):
        events.extend(
            [
                {
                    "kind": "call_attempt",
                    "thread": 17,
                    "name": counter,
                    "route": route,
                    "count": current,
                },
                {"kind": "call_return", "thread": 17, "name": counter},
            ]
        )
    for sequence, event in enumerate(events, 1):
        event["sequence"] = sequence
    snapshot["events"] = events
    snapshot["call_attempts"][counter] = snapshot["call_returns"][counter] = count
    refresh_profiler_evidence(tmp_path, value, census, events=events, snapshot=snapshot)
    census["profiler_evidence"]["call_caps"][counter] = max(
        count, value["_synthetic_plan"]["successful_calls"][counter]
    )
    with pytest.raises(admission.AdmissionError, match="exact successful eligibility call vector"):
        validate_census_evidence(tmp_path, value, contract, census)


def test_type_only_recording_is_not_a_probe_even_when_raw_events_are_valid(tmp_path):
    from scripts.m1_path_census_evidence import (
        _validate_raw_census_evidence,
        validate_census_evidence,
    )

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    events, snapshot = read_profile(tmp_path, census)
    ordinary = set(census["profiler_evidence"]["call_targets"])
    events = [
        event
        for event in events
        if not (event["kind"].startswith("call_") and event["name"] in ordinary)
    ]
    for sequence, event in enumerate(events, 1):
        event["sequence"] = sequence
    snapshot["events"] = events
    for field in ("call_attempts", "call_returns"):
        snapshot[field] = {
            key: count for key, count in snapshot[field].items() if key not in ordinary
        }
    refresh_profiler_evidence(tmp_path, value, census, events=events, snapshot=snapshot)
    _validate_raw_census_evidence(tmp_path, value, contract, census)
    with pytest.raises(
        admission.AdmissionError, match="complete exact eligibility native call map"
    ):
        validate_census_evidence(tmp_path, value, contract, census)


@pytest.mark.parametrize("declared_version", ["3.11.9", "3.12.7", "3.13.0"])
def test_static_declared_stdlib_inspection_is_independent_of_host_314(
    tmp_path, monkeypatch, declared_version
):
    import enum

    from scripts.m1_path_census import PassiveCensus

    value, contract, gates = gate_fixture(tmp_path)
    value["environment"]["version"] = declared_version + " (synthetic AST-only fixture)"
    with monkeypatch.context() as patch:
        patch.setattr(sys, "version_info", (3, 14, 0))
        patch.setattr(enum.Enum, "__init__", object.__init__)
        patch.setattr(
            sysconfig, "get_path", lambda *_: pytest.fail("static inspection used host sysconfig")
        )
        report = admission._inspect_gates(tmp_path, value, contract)
        assert report["mandatory_unmet_obligations"]
        with pytest.raises(admission.AdmissionError, match="fixed mandatory unmet obligations"):
            admission._verify_gates(tmp_path, value, contract)
        with pytest.raises(admission.AdmissionError, match="CPython 3.11 through 3.13"):
            admission.environment_snapshot(tmp_path)
        with pytest.raises(ValueError, match="CPython 3.11 through 3.13"):
            PassiveCensus(
                tmp_path,
                targets={},
                call_caps={},
                type_caps={},
                allowed_functions=set(),
                budget=None,
                writer=None,
            )
        # Host portability must not bypass the static route checks on that host.
        census = gates["constructor_census"]
        replace_observed_route(
            census, "sparkbrain.example:Example", "init", "stdlib/enum.py", "Enum.__init__"
        )
        refresh_profiler_evidence(tmp_path, value, census)
        save_census(tmp_path, value, census)
        with pytest.raises(admission.AdmissionError, match="outside exact source support"):
            admission._inspect_gates(tmp_path, value, contract)
    assert admission.APPROVED_FREEZE_SHA256 is None


@pytest.mark.parametrize(
    "change",
    [
        "missing_binding",
        "missing_root",
        "missing_hash_map",
        "extra_binding_field",
        "missing_enum_source",
        "missing_ancillary_source",
        "extra_source",
        "traversal_source",
        "bad_hash",
        "relative_root",
        "traversal_root",
        "noncanonical_root",
        "double_slash_root",
        "uninventoried_root",
        "environment_hash_rebound",
        "profile_hash_rebound",
        "profile_path_rebound",
        "profile_path_traversal",
        "extra_profile_source",
        "missing_profile_ancillary_source",
        "stale_source_bytes",
        "root_symlink",
        "source_symlink",
        "missing_python_enum_init",
        "declared_314",
        "declared_other_implementation",
    ],
)
def test_declared_stdlib_bindings_fail_closed_before_event_acceptance(tmp_path, change):
    from scripts.m1_path_census_evidence import _validate_raw_census_evidence

    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    environment = value["environment"]
    declared = environment["stdlib"]
    hashes = declared["sources_sha256"]
    profile = census["profiler_evidence"]["stdlib_sources"]
    directory = Path(declared["root"])
    if change == "missing_binding":
        del environment["stdlib"]
    elif change == "missing_root":
        del declared["root"]
    elif change == "missing_hash_map":
        del declared["sources_sha256"]
    elif change == "extra_binding_field":
        declared["host_fallback"] = True
    elif change == "missing_enum_source":
        del hashes["enum.py"]
    elif change == "missing_ancillary_source":
        del hashes["tempfile.py"]
    elif change == "extra_source":
        hashes["unreviewed.py"] = SHA
    elif change == "traversal_source":
        hashes["../enum.py"] = hashes.pop("enum.py")
    elif change == "bad_hash":
        hashes["enum.py"] = True
    elif change in {"relative_root", "traversal_root", "noncanonical_root", "double_slash_root"}:
        declared["root"] = {
            "relative_root": "declared-stdlib",
            "traversal_root": str(directory / ".." / directory.name),
            "noncanonical_root": str(directory) + "/",
            "double_slash_root": "/" + str(directory),
        }[change]
        environment["dependency_roots"] = [declared["root"]]
    elif change == "uninventoried_root":
        environment["dependency_roots"] = [str(tmp_path)]
    elif change == "environment_hash_rebound":
        hashes["enum.py"] = SHA
    elif change == "profile_hash_rebound":
        profile["enum.py"]["sha256"] = SHA
    elif change == "profile_path_rebound":
        alternate = tmp_path / "enum.py"
        alternate.write_bytes((directory / "enum.py").read_bytes())
        profile["enum.py"]["path"] = str(alternate)
    elif change == "profile_path_traversal":
        profile["enum.py"]["path"] = str(directory / ".." / directory.name / "enum.py")
    elif change == "extra_profile_source":
        profile["unreviewed.py"] = dict(profile["enum.py"])
    elif change == "missing_profile_ancillary_source":
        del profile["tempfile.py"]
    elif change == "stale_source_bytes":
        (directory / "enum.py").write_text("class Enum: pass\n")
    elif change == "root_symlink":
        alias = tmp_path / "stdlib-alias"
        alias.symlink_to(directory, target_is_directory=True)
        declared["root"] = str(alias)
        environment["dependency_roots"] = [str(alias)]
        for name, binding in profile.items():
            binding["path"] = str(alias / name)
    elif change == "source_symlink":
        target = directory / "enum.py"
        alternate = tmp_path / "aliased-enum.py"
        target.rename(alternate)
        target.symlink_to(alternate)
    elif change == "missing_python_enum_init":
        (directory / "enum.py").write_text("class Enum: pass\n")
        hashes["enum.py"] = admission.digest((directory / "enum.py").read_bytes())
        profile["enum.py"]["sha256"] = hashes["enum.py"]
    elif change == "declared_314":
        environment["version"] = "3.14.0"
    elif change == "declared_other_implementation":
        environment["implementation"] = "PyPy"
    with pytest.raises(ValueError):
        _validate_raw_census_evidence(tmp_path, value, contract, census)


def test_live_snapshot_binds_exact_stdlib_sources_from_full_inventory(tmp_path, monkeypatch):
    value = freeze()
    synthetic_stdlib_fixture(tmp_path, value)
    expected = value["environment"]["stdlib"]
    inventory = {**expected["sources_sha256"], "other_dependency.py": SHA}
    monkeypatch.setattr(sys, "version_info", (3, 13, 0))
    monkeypatch.setattr(sys, "path", [expected["root"]])
    monkeypatch.setattr(admission.platform, "python_implementation", lambda: "CPython")
    monkeypatch.setattr(sysconfig, "get_path", lambda _: expected["root"])
    monkeypatch.setattr(admission, "_tree_inventory", lambda _: inventory)
    monkeypatch.setattr(admission, "mapped_code_snapshot", lambda: {"/synthetic/python": SHA})
    snapshot = admission.environment_snapshot(tmp_path)
    assert snapshot["stdlib"] == expected
    assert snapshot["dependency_files"] == len(inventory)
    assert snapshot["dependency_inventory_sha256"] == admission.digest(
        admission.canonical({expected["root"]: inventory})
    )
    del inventory["enum.py"]
    with pytest.raises(admission.AdmissionError, match="stdlib route sources are missing"):
        admission.environment_snapshot(tmp_path)

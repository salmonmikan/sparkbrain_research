"""Model-free adversarial checks; never evidence of native eligibility or execution."""

from __future__ import annotations

import builtins
import copy
import hashlib
import os
import random
import subprocess
import sys
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


def gate_fixture(root):
    value = freeze()
    raw = write_json(root, "raw.json", {"synthetic": True})
    terminal = write_json(
        root, "terminal.json", {"identity": "assembly-m1-g0-v1-20261002", "status": "SUCCESS"}
    )
    contract = {
        "runtime_sources_sha256": {"src/sparkbrain/example.py": SHA},
        "files": {"src/sparkbrain/example.py": {"classes": {"Example": {}}}},
        "allocation_type_sources": {
            "sparkbrain.example:Example": {
                "path": "src/sparkbrain/example.py",
                "sha256": SHA,
                "witness": {},
            },
            "sparkbrain.example:InheritedOnly": {
                "path": "src/sparkbrain/example.py",
                "sha256": SHA,
                "witness": {},
            },
            "sparkbrain.v032.contracts:SensoryChannelDecision": {
                "path": "src/sparkbrain/v032/contracts.py",
                "sha256": SHA,
                "witness": {},
            },
            "sparkbrain.v032.contracts:V032StepResult": {
                "path": "src/sparkbrain/v032/contracts.py",
                "sha256": SHA,
                "witness": {},
            },
        },
        "excluded_constructor_types": ["sparkbrain.example:InheritedOnly"],
        "import_enum_initializations": {
            "sparkbrain.model:SparkKind": 7,
            "sparkbrain.model:EventKind": 5,
            "sparkbrain.v03_seed.revision:TransitionKind": 4,
        },
    }
    for name in contract["import_enum_initializations"]:
        contract["allocation_type_sources"][name] = {
            "path": "src/" + name.split(":")[0].replace(".", "/") + ".py",
            "sha256": SHA,
            "witness": {},
        }
    per_type = {
        name: {"init": 0, "shell": 0}
        for name in set(contract["allocation_type_sources"])
        | {"random:Random", "_thread:lock", "_thread:RLock"}
    }
    per_type["sparkbrain.example:Example"]["init"] = 1
    for name, count in contract["import_enum_initializations"].items():
        per_type[name]["init"] = count
    common = {
        "source_contract_sha256": SHA,
        "inputs_sha256": SHA,
        "configuration_sha256": admission.digest(admission.canonical(value["configuration"])),
        "raw_evidence": [raw],
    }
    gates = {
        "g0": {
            "status": "SUCCESS",
            "runtime_sources_sha256": {"src/sparkbrain/example.py": "b" * 64},
            "terminal": terminal,
        },
        "source_delta_reconciliation": {
            "status": "RECONCILED",
            "from_runtime_sources_sha256": {"src/sparkbrain/example.py": "b" * 64},
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
    for name, gate in gates.items():
        gate.update(common)
        gate["schema"] = "m1-path-" + name.replace("_", "-") + "-v1"
        if name == "source_delta_reconciliation":
            gate["g0_evidence_sha256"] = value["gates"]["g0"]["sha256"]
        value["gates"][name] = write_json(root, name + ".json", gate)
    return value, contract, gates


def test_synthetic_gate_validation_does_not_issue_permit(tmp_path):
    value, contract, _ = gate_fixture(tmp_path)
    admission._verify_gates(tmp_path, value, contract)
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
                "path": "synthetic/census.py",
                "qualname": "synthetic_route",
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
        admission._verify_gates(tmp_path, value, contract)
    assert name + ":" + kind in str(error.value)


@pytest.mark.parametrize("kind", ["init", "shell"])
@pytest.mark.parametrize("count", [0, 1])
def test_observed_count_equal_to_prospective_type_cap_is_accepted(tmp_path, kind, count):
    value, contract, gates = gate_fixture(tmp_path)
    census = gates["constructor_census"]
    name = "sparkbrain.example:Example"
    set_synthetic_observed_count(census, name, kind, count)
    census["prospective_type_caps"][name][kind] = count
    value["gates"]["constructor_census"] = write_json(tmp_path, "constructor_census.json", census)
    admission._verify_gates(tmp_path, value, contract)
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
        admission._verify_gates(tmp_path, value, contract)


def test_retained_graph_inventory_never_substitutes_for_allocation_inventory(tmp_path):
    value, contract, _ = gate_fixture(tmp_path)
    del contract["allocation_type_sources"]
    with pytest.raises(admission.AdmissionError, match="allocation-type source inventory"):
        admission._verify_gates(tmp_path, value, contract)


@pytest.mark.parametrize("field", ["observed_eligibility_per_type", "prospective_type_caps"])
@pytest.mark.parametrize("kind", ["init", "shell"])
def test_excluded_allocators_require_zero_counts_and_caps(tmp_path, field, kind):
    value, contract, gates = gate_fixture(tmp_path)
    gates["constructor_census"][field]["sparkbrain.example:InheritedOnly"][kind] = 1
    value["gates"]["constructor_census"] = write_json(
        tmp_path, "constructor_census.json", gates["constructor_census"]
    )
    with pytest.raises(admission.AdmissionError, match="excluded constructor requires zero"):
        admission._verify_gates(tmp_path, value, contract)


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
        admission._verify_gates(tmp_path, value, contract)


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
        admission._verify_gates(tmp_path, value, contract)


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
        admission._verify_gates(tmp_path, value, contract)


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
        admission._verify_gates(tmp_path, value, contract)


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


@pytest.mark.skipif(sys.version_info >= (3, 14),
                    reason="research admission supports CPython 3.11–3.13")
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

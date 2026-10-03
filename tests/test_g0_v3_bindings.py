"""SOURCE_ONLY / SYNTHETIC_MODEL_FREE: v3 wiring never grants run authority.

Every approval-shaped record below is a temporary, labeled negative-test fixture.
Admission always rejects before permit issuance. Runtime wiring uses inert stand-ins
and no SparkBrain source import, constructor, ledger, reservation or research run.
"""
from __future__ import annotations

import dataclasses
import importlib.machinery
import importlib.util
import json
import runpy
import sys
import threading
import time
import types
import weakref
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest
import test_g0_joint_eligibility_runner as standins
from test_g0_execution_support import synthetic_completed_lifecycle

from scripts import g0_execution_objects as objects
from scripts import g0_execution_support as support
from scripts import launch_g0_joint_eligibility as launcher
from scripts import launch_g0_v3_eligibility as wrapper
from scripts import run_g0_joint_eligibility as runner

ROOT = Path(__file__).resolve().parents[1]
V3 = objects.G0_V3
OLD = objects.HISTORICAL_G0
BINDING = objects.object_binding(V3)
MISSING = object()
PRELAUNCH_FLAGS = (
    "verified_before_target_python_start", "full_published_tree_verified",
    "no_undeclared_importables", "namespace_and_path_precedence_verified",
    "aliases_and_extensions_verified", "trusted_startup_hooks_verified",
    "quiescent_source_and_environment",
)


@pytest.fixture(autouse=True)
def no_native_imports(monkeypatch):
    """Install before each test in addition to the pre-pytest process tripwire."""
    class BlockNative:
        def find_spec(self, fullname, path=None, target=None):
            if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
                raise AssertionError("native import forbidden in v3 source-only tests")

    before = {name: module for name, module in sys.modules.items()
              if name == "sparkbrain" or name.startswith("sparkbrain.")}
    monkeypatch.setattr(sys, "meta_path", [BlockNative(), *sys.meta_path])
    yield
    after = {name: module for name, module in sys.modules.items()
             if name == "sparkbrain" or name.startswith("sparkbrain.")}
    assert after.keys() == before.keys()
    assert all(after[name] is module for name, module in before.items())


def budget():
    return support.ResourceBudget(sampler=lambda: {
        "cpu_seconds": 0.0, "wall_seconds": 0.0, "address_space_bytes": 0,
    })


def save(root, relative, value):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(support.canonical(value))
    return support.digest(path.read_bytes())


def forbid(*args, **kwargs):
    pytest.fail("crossed a forbidden native/authority/reservation boundary")


def inert_prelaunch_shape(root, commit, inventory):
    """Invented structural metadata; no pre-startup verification was performed."""
    return {
        "schema": "g0-prelaunch-materialization-attestation-v1", **BINDING,
        "source_root": str(root), "published_commit": commit,
        "runtime_origin_commit": V3.runtime_origin_commit,
        "source_inventory_sha256": inventory,
        "proof_sha256": support.digest(b"SYNTHETIC SHAPE ONLY, NO EXTERNAL ATTESTATION"),
        "reference": "SYNTHETIC SHAPE ONLY, NOT A GENUINE PRELAUNCH PROOF",
        **dict.fromkeys(PRELAUNCH_FLAGS, True),
    }


@pytest.fixture
def prepared_tree(tmp_path, monkeypatch):
    """Structural fixture only: source verification is deliberately replaced."""
    monkeypatch.setattr(support, "verify_object_source", lambda root, object_spec: {
        "synthetic": True, "runtime_execution_authorized": False,
        "contract_sha256": object_spec.contract_sha256,
    })
    relatives = [
        "scripts/g0_execution_support.py", "scripts/g0_joint_ownership.py",
        "scripts/verify_g0_joint_source_contract.py", "scripts/run_g0_joint_eligibility.py",
        "scripts/v05_history_export_probe.py", "scripts/launch_g0_joint_eligibility.py",
        "scripts/g0_execution_objects.py", V3.launcher_relative,
        "tests/test_g0_execution_support.py", "tests/test_g0_joint_eligibility_runner.py",
        "tests/test_g0_joint_ownership.py", "tests/test_g0_joint_source_contract.py",
        "tests/test_g0_execution_protocol.py", "tests/test_g0_joint_launcher.py",
        "tests/test_g0_execution_objects.py", "tests/test_g0_v3_bindings.py",
        "tests/test_g0_v3_environment.py", "tests/test_g0_v3_environment_regressions.py",
        "scripts/g0_prelaunch/materialization_verifier.py",
        "scripts/g0_prelaunch/published_baseline_inventory.json",
        "scripts/g0_prelaunch/README.md", "tests/test_g0_prelaunch_verifier.py",
        "docs/research/assembly_m1_g0_execution_preparation_20261002.md",
        "docs/research/assembly_m1_g0_v2_proposal_20261002.md",
        "docs/research/assembly_m1_g0_v3_proposal_20261003.md",
        "tests/test_g0_v2_bindings.py",
        V3.artifact_root + "/proposal.json",
    ]
    inventory = {name: save(tmp_path, name, {"synthetic": True}) for name in relatives}
    inventory[V3.contract_relative] = save(tmp_path, V3.contract_relative, {
        "runtime_sources_sha256": {}, "runtime_schema_sha256": {},
        "reuse_sources_sha256": {}, "synthetic": True,
    })
    inventory[V3.inputs_relative] = save(tmp_path, V3.inputs_relative, {"synthetic": True})
    inputs = {"path": V3.inputs_relative, "sha256": inventory[V3.inputs_relative]}
    protocol = {"identity": V3.identity, **BINDING, "synthetic": True,
                "runtime_origin_commit": V3.runtime_origin_commit,
                "call_caps": support.protocol_call_caps(), "limits": support.LIMITS,
                "reserves": support.RESERVES, "inputs": inputs}
    inventory[V3.protocol_relative] = save(tmp_path, V3.protocol_relative, protocol)
    freeze = {"schema": "g0-execution-freeze-v1", "identity": V3.identity, **BINDING,
              "runtime_origin_commit": V3.runtime_origin_commit,
              "limits": support.LIMITS, "reserves": support.RESERVES,
              "call_caps": support.CALL_CAPS, "runtime_python_files": 157,
              "runtime_schema_files": 15, "contract_sha256": V3.contract_sha256,
              "runtime_execution_authorized": False,
              "environment": {"synthetic": True, "system_libraries_sha256": {}},
              "timeout_executable_sha256": "0" * 64, "source_files_sha256": inventory,
              "inputs": inputs,
              "protocol": {"path": V3.protocol_relative,
                           "sha256": inventory[V3.protocol_relative]}}
    save(tmp_path, V3.freeze_relative, freeze)
    (tmp_path / "src/sparkbrain").mkdir(parents=True)
    return tmp_path, freeze, protocol


def verify_fixture(root):
    return support.verify_preparation(root, V3.freeze_relative,
                                      check_environment=False, object_spec=V3)


def test_v3_static_preparation_returns_only_bound_non_authority(prepared_tree):
    root, _, _ = prepared_tree
    result = verify_fixture(root)
    assert result["identity"] == V3.identity
    assert result["execution_object_sha256"] == objects.object_digest(V3)
    assert result["runtime_execution_authorized"] is False
    assert result["scientific_credit"] == 0
    assert not support._PERMITS


@pytest.mark.parametrize("record", ["freeze", "protocol"])
@pytest.mark.parametrize("field,value", [
    ("execution_object_sha256", MISSING),
    ("execution_object_sha256", objects.object_digest(OLD)),
    ("identity", OLD.identity),
    ("runtime_origin_commit", OLD.runtime_origin_commit),
])
def test_preparation_rejects_missing_or_cross_object_records(prepared_tree, record, field, value):
    root, freeze, protocol = prepared_tree
    target = freeze if record == "freeze" else protocol
    if value is MISSING:
        target.pop(field)
    else:
        target[field] = value
    if record == "protocol":
        sha = save(root, V3.protocol_relative, protocol)
        freeze["protocol"]["sha256"] = sha
        freeze["source_files_sha256"][V3.protocol_relative] = sha
    save(root, V3.freeze_relative, freeze)
    with pytest.raises(support.AdmissionError):
        verify_fixture(root)


@pytest.mark.parametrize("key", ["protocol", "inputs"])
def test_preparation_rejects_historical_literal_namespace(prepared_tree, key):
    root, freeze, _ = prepared_tree
    freeze[key]["path"] = getattr(OLD, key + "_relative")
    save(root, V3.freeze_relative, freeze)
    with pytest.raises(support.AdmissionError,
                       match="canonical prospective path|literal binding differs"):
        verify_fixture(root)


def test_preparation_rejects_historical_freeze_path_before_reads(tmp_path):
    with pytest.raises(support.AdmissionError, match="freeze path"):
        support.verify_preparation(tmp_path, OLD.freeze_relative, object_spec=V3)


@pytest.fixture
def negative_authority(tmp_path, monkeypatch):
    """Admission-shaped negative fixtures; final authority is unconditionally denied."""
    # Exercise downstream synthetic gates in an explicitly fresh fixture namespace.
    # Full-suite collection may already have native modules; never remove or mutate
    # those ambient objects, and never relax the production preload rejection.
    monkeypatch.setattr(support, "sys", SimpleNamespace(modules={}, platform=sys.platform))
    verified = {"freeze_sha256": "a" * 64, "source_inventory_sha256": "b" * 64}
    calls = []

    def preparation(root, relative, *, checkpoint, object_spec):
        assert root == tmp_path and relative == V3.freeze_relative and object_spec is V3
        calls.append("synthetic preparation only")
        return verified

    monkeypatch.setattr(support, "verify_preparation", preparation)
    monkeypatch.setattr(support, "ResourceBudget", lambda: SimpleNamespace(check=lambda: None))
    identity_record = {"state": "UNCONSUMED", **BINDING,
                       "reservation_directory": str(tmp_path)}
    ledger = {"classification": "SYNTHETIC_TEST_NOT_AN_AUTHORITY_LEDGER",
              "identities": {V3.identity: identity_record}}
    ledger_path = tmp_path / "SYNTHETIC_NEGATIVE_TEST_LEDGER.json"
    ledger_sha = save(tmp_path, ledger_path.name, ledger)
    approval = {
        "classification": "SYNTHETIC_NEGATIVE_TEST_NOT_AN_APPROVAL",
        "schema": "g0-published-execution-approval-v1", "identity": V3.identity, **BINDING,
        "execution_object_enabled": True, **verified,
        "limits": support.LIMITS, "reserves": support.RESERVES, "call_caps": support.CALL_CAPS,
        # Gate-shape literals are never evidence of authority: the independent
        # callback below always denies, even if every earlier structural check passes.
        "actual_execution_authorized": True, "synthetic": False,
        "publication": {"reference": "SYNTHETIC_NOT_PUBLISHED", "commit": "c" * 40,
                        "exact_source_sha256": verified["source_inventory_sha256"]},
        "review": {"reference": "SYNTHETIC_NOT_REVIEWED", "unresolved_findings": 0,
                   "freeze_sha256": verified["freeze_sha256"]},
        "user_approval": {"reference": "SYNTHETIC_NOT_APPROVED"},
        "output_directory": str(tmp_path / "NEVER_CREATED_OUTPUT"),
        "execution_nonce": "SYNTHETIC_MUST_NEVER_EXECUTE", "identity_previously_consumed": False,
        "identity_ledger": {"path": str(ledger_path), "sha256": ledger_sha,
                            "reference": "SYNTHETIC_NOT_AUTHORITATIVE"},
        "prelaunch_materialization": inert_prelaunch_shape(
            tmp_path, "c" * 40, verified["source_inventory_sha256"]),
    }
    permits_before = set(support._PERMITS)
    yield tmp_path, approval, ledger, calls
    assert set(support._PERMITS) == permits_before
    assert not (tmp_path / "NEVER_CREATED_OUTPUT").exists()
    assert not list(tmp_path.glob("*.STARTED.json"))


@pytest.mark.parametrize("name", ["sparkbrain", "sparkbrain.synthetic_ambient"])
def test_real_admission_rejects_inert_preloaded_runtime_before_preparation(
        tmp_path, monkeypatch, name):
    """The real gate still rejects preloads; only negative fixtures isolate sys."""
    ambient = sys.modules.get(name, MISSING)
    with monkeypatch.context() as isolated:
        isolated.setitem(sys.modules, name, types.ModuleType(name))
        isolated.setattr(support, "verify_preparation", forbid)
        isolated.setattr(support, "confined_path", forbid)
        with pytest.raises(support.AdmissionError, match="fresh frozen runtime imports"):
            support.authorize_execution(
                tmp_path, V3.freeze_relative, V3.approval_relative,
                "0" * 64, forbid, object_spec=V3)
    assert sys.modules.get(name, MISSING) is ambient
    assert not list(tmp_path.iterdir())


def reject_fixture(fixture, *, callback=forbid):
    root, approval, ledger, _ = fixture
    approval["identity_ledger"]["sha256"] = save(
        root, "SYNTHETIC_NEGATIVE_TEST_LEDGER.json", ledger)
    sha = save(root, V3.approval_relative, approval)
    return support.authorize_execution(root, V3.freeze_relative, V3.approval_relative,
                                       sha, callback, object_spec=V3)


@pytest.mark.parametrize("field,value", [
    ("execution_object_sha256", MISSING),
    ("execution_object_sha256", objects.object_digest(OLD)),
    ("identity", OLD.identity), ("execution_object_enabled", MISSING),
    ("execution_object_enabled", False), ("execution_object_enabled", 1),
])
def test_approval_object_binding_rejects_before_authority(negative_authority, field, value):
    _, approval, _, _ = negative_authority
    if value is MISSING:
        approval.pop(field)
    else:
        approval[field] = value
    with pytest.raises(support.AdmissionError):
        reject_fixture(negative_authority)


@pytest.mark.parametrize("change", ["missing_binding", "historical_binding", "historical_identity",
                                   "consumed", "missing_identity"])
def test_ledger_crossbinding_rejects_without_permit_or_reservation(negative_authority, change):
    _, _, ledger, _ = negative_authority
    record = ledger["identities"][V3.identity]
    if change == "missing_binding":
        record.pop("execution_object_sha256")
    elif change == "historical_binding":
        record["execution_object_sha256"] = objects.object_digest(OLD)
    elif change == "historical_identity":
        ledger["identities"] = {OLD.identity: record}
    elif change == "consumed":
        record["state"] = "CONSUMED"
    else:
        ledger["identities"] = {}
    with pytest.raises(support.AdmissionError):
        reject_fixture(negative_authority)


def test_structurally_bound_test_records_still_cannot_issue_authority(negative_authority):
    denied = []

    def deny(record):
        assert record["classification"] == "SYNTHETIC_NEGATIVE_TEST_NOT_AN_APPROVAL"
        denied.append(True)
        return False

    with pytest.raises(support.AdmissionError, match="not independently verified"):
        reject_fixture(negative_authority, callback=deny)
    assert denied == [True]


@pytest.mark.parametrize("cross", ["freeze", "approval"])
def test_authorize_rejects_cross_namespace_before_preparation(tmp_path, monkeypatch, cross):
    monkeypatch.setattr(support, "verify_preparation", forbid)
    with pytest.raises(support.AdmissionError, match="path differs"):
        support.authorize_execution(
            tmp_path, OLD.freeze_relative if cross == "freeze" else V3.freeze_relative,
            OLD.approval_relative if cross == "approval" else V3.approval_relative,
            "0" * 64, forbid, object_spec=V3)


def fake_permit(monkeypatch, record):
    """An internal malformed-record fixture, never issued through admission."""
    permits = weakref.WeakKeyDictionary()
    permit = object.__new__(support.ExecutionPermit)
    permits[permit] = record
    monkeypatch.setattr(support, "_PERMITS", permits)
    return permit


@pytest.mark.parametrize("spec", [MISSING, None, objects.ExecutionObject(*V3)])
def test_internal_permit_missing_or_unsealed_descriptor_never_falls_back(monkeypatch, spec):
    record = {"classification": "SYNTHETIC_MALFORMED_INTERNAL_RECORD", **BINDING}
    if spec is not MISSING:
        record["object_spec"] = spec
    permit = fake_permit(monkeypatch, record)
    monkeypatch.setattr(support, "verify_preparation", forbid)
    with pytest.raises(support.AdmissionError, match="sealed execution object"):
        support.require_execution_permit(permit)
    with pytest.raises(support.AdmissionError, match="sealed execution object"):
        _ = permit.object_spec


@pytest.mark.parametrize("binding", [MISSING, objects.object_digest(OLD)])
def test_internal_v3_permit_rejects_missing_or_cross_digest(monkeypatch, binding):
    record = {"object_spec": V3}
    if binding is not MISSING:
        record["execution_object_sha256"] = binding
    permit = fake_permit(monkeypatch, record)
    monkeypatch.setattr(support, "verify_preparation", forbid)
    with pytest.raises(support.AdmissionError, match="object binding"):
        support.require_execution_permit(permit)
    with pytest.raises(AttributeError):
        permit.object_spec = OLD


@pytest.mark.parametrize("change", ["missing_spec", "historical_spec", "copied_spec",
                                   "missing_digest", "historical_digest"])
def test_runtime_receipt_rejects_object_mismatch_and_poison_before_native_work(
        tmp_path, monkeypatch, change):
    b = budget()
    record = {"root": tmp_path, "consumed": True, "budget": b, "object_spec": V3, **BINDING}
    permit = fake_permit(monkeypatch, record)
    token = object.__new__(support._RuntimeAdmission)
    admitted = {"permit": permit, "root": tmp_path, "budget": b, "thread": threading.get_ident(),
                "phase": "prepared", "object_spec": V3, **BINDING}
    if change == "missing_spec":
        admitted.pop("object_spec")
    elif change == "historical_spec":
        admitted["object_spec"] = OLD
    elif change == "copied_spec":
        admitted["object_spec"] = objects.ExecutionObject(*V3)
    elif change == "missing_digest":
        admitted.pop("execution_object_sha256")
    else:
        admitted["execution_object_sha256"] = objects.object_digest(OLD)
    receipts = weakref.WeakKeyDictionary()
    receipts[token] = admitted
    monkeypatch.setattr(support, "_RUNTIME_ADMISSIONS", receipts)
    monkeypatch.setattr(support, "file_digest", forbid)
    with pytest.raises(support.AdmissionError, match="object"):
        support.advance_runtime_admission(permit, token, b, "importing")
    assert admitted["phase"] == "failed"


@pytest.mark.parametrize("stage", ["consume", "orchestrate"])
def test_cross_output_rejects_before_reservation_or_writer(tmp_path, monkeypatch, stage):
    permit = fake_permit(monkeypatch, {
        "object_spec": V3, **BINDING, "root": tmp_path,
        "output_directory": tmp_path / "AUTHORIZED_SYNTHETIC_ONLY", "consumed": False,
    })
    monkeypatch.setattr(support, "require_execution_permit", lambda *args, **kwargs: None)
    monkeypatch.setattr(support, "preflight_runtime_limits", lambda: {})
    monkeypatch.setattr(support, "exclusive_durable_write", forbid)
    monkeypatch.setattr(support, "ExclusiveEvidenceWriter", forbid)
    if stage == "consume":
        with pytest.raises(support.AdmissionError, match="destination"):
            support.consume_execution_permit(permit, tmp_path / "WRONG", budget=budget())
    else:
        monkeypatch.setattr(support, "consume_execution_permit", forbid)
        with pytest.raises(runner.BindingError, match="target"):
            runner.execute_reviewed(permit, tmp_path / "WRONG")
    assert list(tmp_path.iterdir()) == []
    assert support._PERMITS[permit]["consumed"] is False


@pytest.mark.parametrize("component", ["registry", "writer"])
@pytest.mark.parametrize("binding", [MISSING, "historical", "copied"])
def test_engine_rejects_missing_or_cross_object_before_constructor(component, binding):
    registry = runner.SourceRegistry(())
    registry.execution_object_sha256 = objects.object_digest(V3)
    writer = standins.MemoryWriter()
    writer._object_spec = V3
    if component == "registry":
        if binding is MISSING:
            del registry.execution_object_sha256
        else:
            registry.execution_object_sha256 = (objects.object_digest(OLD)
                                                 if binding == "historical" else "0" * 64)
    elif binding is MISSING:
        del writer._object_spec
    else:
        writer._object_spec = OLD if binding == "historical" else objects.ExecutionObject(*V3)
    runtime = standins.ModelFreeRuntime()
    with pytest.raises(runner.BindingError, match=component + " execution object"):
        runner.ExecutionEngine(runtime, registry, None, writer, standins.NoLimitBudget(),
                               standins.input_plan(), object_spec=V3)
    assert runtime.calls == [] and writer.rows == {}


@pytest.mark.parametrize("binding", [MISSING, objects.object_digest(OLD)])
def test_lifecycle_missing_or_cross_object_rejected(binding):
    value = synthetic_completed_lifecycle()
    if binding is not MISSING:
        value["execution_object_sha256"] = binding
    with pytest.raises(support.AdmissionError, match="object binding"):
        support.validate_completed_lifecycle(value, object_spec=V3)


def test_synthetic_completed_lifecycle_is_bound_to_selected_object():
    result = support.validate_completed_lifecycle(
        {**synthetic_completed_lifecycle(), **BINDING}, object_spec=V3)
    assert result["execution_object_sha256"] == objects.object_digest(V3)
    assert result["validated"] is True
    with pytest.raises(support.AdmissionError, match="object binding"):
        support.validate_completed_lifecycle({**synthetic_completed_lifecycle(), **BINDING})


@pytest.mark.parametrize("kwargs", [
    {"call_plan": {}}, {"call_plan": {**support.CALL_CAPS, "producer_process": 999}},
    {"targets": {}}, {"allowed_functions": set()},
])
def test_v3_monitor_disallows_caller_cap_and_route_overrides(tmp_path, kwargs):
    kwargs = dict(kwargs)
    call_plan = kwargs.pop("call_plan", None)
    with pytest.raises(support.AdmissionError, match="cannot be overridden"):
        support.PassiveCallMonitor(tmp_path, call_plan, budget(), object_spec=V3, **kwargs)


def test_v3_monitor_missing_contract_has_no_synthetic_source_fallback(tmp_path):
    path = tmp_path / "src/sparkbrain/inert.py"
    path.parent.mkdir(parents=True)
    path.write_text("# Synthetic source must not admit missing v3 contract\n")
    with pytest.raises((ValueError, OSError)):
        support.PassiveCallMonitor(tmp_path, None, budget(), object_spec=V3)
    assert sys.getprofile() is None and threading.getprofile() is None


def test_v3_monitor_rejects_historical_writer_before_source_scan(tmp_path):
    writer = object.__new__(support.ExclusiveEvidenceWriter)
    writer._object_spec = OLD
    with pytest.raises(support.AdmissionError, match="different execution object"):
        support.PassiveCallMonitor(tmp_path, None, budget(), writer, object_spec=V3)
    assert list(tmp_path.iterdir()) == []


def inert_module(relative, root=ROOT, *, name=None):
    canonical_name = relative.removesuffix(".py").replace("/", ".")
    path = str(root / relative)
    loader = importlib.machinery.SourceFileLoader(canonical_name, path)
    module = types.ModuleType(name or canonical_name)
    module.__file__ = path
    module.__loader__ = loader
    module.__spec__ = importlib.util.spec_from_loader(canonical_name, loader, origin=path)
    return module


def test_v3_reviewed_launch_requires_actual_active_wrapper(monkeypatch):
    with pytest.raises(support.AdmissionError, match="active fixed wrapper"):
        launcher._guarded_root(str(ROOT), object_spec=V3, entry_module=wrapper,
                               require_active=True)
    with pytest.raises(support.AdmissionError, match="fixed successor wrapper"):
        launcher._guarded_root(str(ROOT), object_spec=V3, require_active=True)
    with pytest.raises(support.AdmissionError, match="origin"):
        launcher._guarded_root(str(ROOT), object_spec=V3, entry_module=launcher,
                               require_active=True)
    active = inert_module(V3.launcher_relative, name="__main__")
    monkeypatch.setitem(sys.modules, "__main__", active)
    assert launcher._guarded_root(str(ROOT), object_spec=V3, entry_module=active,
                                  require_active=True) == ROOT


@pytest.mark.parametrize("mutation", ["spec_name", "loader_name", "loader_path", "spec_origin",
                                     "file", "loader_instance", "module_name", "fake_main"])
def test_fixed_wrapper_rejects_loader_spec_name_and_path_aliases(monkeypatch, mutation):
    active = inert_module(V3.launcher_relative, name="__main__")
    monkeypatch.setitem(sys.modules, "__main__", active)
    if mutation == "spec_name":
        active.__spec__.name = "scripts.launch_g0_joint_eligibility"
    elif mutation == "loader_name":
        active.__loader__.name = "scripts.alias"
    elif mutation == "loader_path":
        active.__loader__.path = str(ROOT / "scripts/../scripts/launch_g0_v3_eligibility.py")
    elif mutation == "spec_origin":
        active.__spec__.origin = str(ROOT / OLD.launcher_relative)
    elif mutation == "file":
        active.__file__ = str(ROOT / "scripts/../scripts/launch_g0_v3_eligibility.py")
    elif mutation == "loader_instance":
        active.__loader__ = importlib.machinery.SourceFileLoader(
            active.__spec__.name, active.__file__)
    elif mutation == "module_name":
        active.__name__ = "scripts.alias"
    else:
        monkeypatch.setitem(sys.modules, "__main__", types.ModuleType("__main__"))
    with pytest.raises(support.AdmissionError, match="origin|active fixed wrapper"):
        launcher._guarded_root(str(ROOT), object_spec=V3, entry_module=active, require_active=True)


def test_wrapper_passes_fixed_singleton_and_its_own_entry_module(monkeypatch):
    seen = []

    def core(argv, *, object_spec, entry_module):
        seen.append((argv, object_spec, entry_module))
        return 17

    monkeypatch.setattr(launcher, "main", core)
    assert wrapper.main(["--check-source"]) == 17
    assert seen == [(["--check-source"], V3, wrapper)]


def native_export_fixture():
    prototype = SimpleNamespace(ordered_units=(1,), relative_bins=(0,), unit_ids=(1,),
                                spike_count=1, source_kind="synthetic")
    bank = SimpleNamespace(config=SimpleNamespace(mature_episodes=1, similarity_threshold=0.5),
                           candidates={"synthetic": SimpleNamespace(
                               prototype=prototype, episode_ids={"one"}, occurrences=1)},
                           suppressed=set())
    brain = SimpleNamespace(assemblies=bank, pending_activation=None,
                            config=SimpleNamespace(min_pattern_spikes=1))
    result = SimpleNamespace(patterns=[], assembly_activations=[], end_ms=72.0)
    observation = {"occurrence_id": "SYNTHETIC_ONLY", "start_ms": 0.0}
    return bank, brain, result, observation


def test_dictionary_and_export_use_v3_pin_without_changing_native_coordinates():
    bank, brain, result, observation = native_export_fixture()
    old = runner.freeze_dictionary(bank)
    current = runner.freeze_dictionary(bank, object_spec=V3)
    assert current["binding"]["source_pin"] == V3.runtime_origin_commit
    assert current["binding"]["execution_object_sha256"] == objects.object_digest(V3)
    assert old["binding"]["source_pin"] == OLD.runtime_origin_commit
    assert "execution_object_sha256" not in old["binding"]
    assert old["coordinates"] == current["coordinates"]
    assert old["binding"]["dictionary_sha256"] == current["binding"]["dictionary_sha256"]
    exported, _ = runner.export_native(brain, result, observation, current, forbid, object_spec=V3)
    assert exported["accepted"] is True
    assert exported["binding"] == current["binding"]
    assert exported["features"] == [0.0]


@pytest.mark.parametrize("field", ["source_pin", "execution_object_sha256"])
def test_v3_export_withholds_cross_object_dictionary_binding(field):
    bank, brain, result, observation = native_export_fixture()
    dictionary = runner.freeze_dictionary(bank, object_spec=V3)
    dictionary["binding"][field] = (OLD.runtime_origin_commit if field == "source_pin"
                                     else objects.object_digest(OLD))
    exported, audit = runner.export_native(
        brain, result, observation, dictionary, forbid, object_spec=V3)
    assert exported["accepted"] is False
    assert exported["features"] == [] and exported["status"] == "binding_error"
    assert "binding_error" in audit["withheld_reasons"]


@dataclasses.dataclass
class InertPulse:
    metadata: dict

    def as_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class InertResult:
    end_ms: float = 72.0

    def as_dict(self):
        return dataclasses.asdict(self)


def test_native_runtime_adapter_forwards_permit_object_into_export(monkeypatch):
    """Call only adapter code against inert dataclasses, never native producer code."""
    calls = []
    produced = InertResult()

    def process(pulses, **kwargs):
        calls.append((pulses, kwargs))
        return produced

    producer = SimpleNamespace(process_episode=process)
    similarity = object()
    runtime = object.__new__(runner.NativeRuntime)
    runtime.permit = SimpleNamespace(object_spec=V3)
    runtime.modules = {
        "sparkbrain.v04.contracts": SimpleNamespace(SignalPulse=InertPulse),
        "sparkbrain.v05.assemblies": SimpleNamespace(pattern_similarity=similarity),
    }
    root = {"producer": producer, "clock": {}, "dictionary": {"synthetic": True}}
    observation = {"pulses": [{"metadata": {"nested": [1]}}],
                   "occurrence_id": "SYNTHETIC", "start_ms": 0.0}
    exported = {"synthetic": [1]}
    audited = {"synthetic_audit": [2]}
    exports = []

    def capture(brain, result, row, dictionary, match, *, object_spec):
        exports.append(object_spec)
        assert (brain, result, row, dictionary, match) == (
            producer, produced, observation, root["dictionary"], similarity)
        return exported, audited

    monkeypatch.setattr(runner, "export_native", capture)
    outward = runtime.process(root, observation, acquisition=False)
    assert exports == [V3] and root["clock"] == {"decision_ms": 72.0}
    assert calls[0][1] == {"episode_id": "SYNTHETIC", "learn_assembly": False,
                           "learn_field": False, "explore_action": False, "metadata": {}}
    assert calls[0][0][0].metadata is not outward["caller_pulses"][0].metadata
    exported["synthetic"].append(9)
    audited["synthetic_audit"].append(9)
    assert outward["raw"]["export"] == {"synthetic": [1]}
    assert outward["raw"]["matching"] == {"synthetic_audit": [2]}
    runtime.process(root, observation, acquisition=True)
    assert exports == [V3]


@pytest.mark.parametrize("change", ["equal_tuple", "generation", "other_owner"])
def test_case10_exact_owner_pointer_guard_rejects_fault_time_change(change):
    runtime = standins.ModelFreeRuntime()
    registry = runner.SourceRegistry(())
    registry.execution_object_sha256 = objects.object_digest(V3)
    writer = standins.MemoryWriter()
    writer._object_spec = V3
    engine = runner.ExecutionEngine(runtime, registry, None, writer, standins.NoLimitBudget(),
                                    standins.input_plan(), object_spec=V3)
    ordinary = runtime.outcome

    def mutate(root, receipt, *, fault=False):
        if fault:
            old = engine.pointer
            if change == "equal_tuple":
                engine.pointer = tuple([old[0], old[1]])
                assert engine.pointer == old and engine.pointer is not old
            elif change == "generation":
                engine.pointer = (old[0], old[1] + 1)
            else:
                engine.pointer = (engine.live["candidate-02"], old[1])
        return ordinary(root, receipt, fault=fault)

    runtime.outcome = mutate
    with pytest.raises(runner.InvariantError, match="fault changed owner pointer"):
        engine.execute()
    witness = writer.rows["fault-owner-boundary.json"]
    assert witness["exact_owner_pointer_and_generation_preserved"] is False
    assert witness["native_rollback_equivalence"] == "not_tested"
    assert "candidate-12-publication.json" not in writer.rows
    assert 10 in engine.candidates
    engine.abort_cleanup()


def test_v3_orchestrator_threads_object_through_complete_model_free_path(tmp_path, monkeypatch):
    """Full software orchestration, with authority/import/limits/monitor all inert."""
    output = tmp_path / "SYNTHETIC_MODEL_FREE_OUTPUT"
    source = tmp_path / "synthetic-source"
    source.mkdir()
    protocol = json.loads((ROOT / V3.protocol_relative).read_bytes())
    plan = json.loads((ROOT / V3.inputs_relative).read_bytes())
    inventory = {
        V3.protocol_relative: save(source, V3.protocol_relative, protocol),
        V3.inputs_relative: save(source, V3.inputs_relative, plan),
    }
    save(source, V3.freeze_relative, {"synthetic": True, **BINDING})
    save(source, V3.approval_relative, {"synthetic": True, "actual_execution_authorized": False})
    permit = SimpleNamespace(
        object_spec=V3, root=source, output_directory=output,
        freeze_path=source / V3.freeze_relative, approval_path=source / V3.approval_relative,
        freeze={"environment": {"synthetic": True, "system_libraries_sha256": {}},
                "source_files_sha256": inventory})
    runtime = standins.ModelFreeRuntime()
    registry = runner.SourceRegistry(())
    registry.execution_object_sha256 = objects.object_digest(V3)
    calls = []
    real_budget = support.ResourceBudget
    real_writer = support.ExclusiveEvidenceWriter
    real_engine = runner.ExecutionEngine

    class SyntheticBudget(real_budget):
        def __init__(self):
            super().__init__(sampler=lambda: {
                "cpu_seconds": 0.0, "wall_seconds": 0.0, "address_space_bytes": 0,
            })

    class SyntheticMonitor:
        def __init__(self, root, caps, budget, writer, *, object_spec):
            assert root == source and caps == support.CALL_CAPS and object_spec is V3
            assert writer._object_spec is V3
            calls.append("monitor-v3")
            self.budget = budget

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def check(self):
            self.budget.check()

        def snapshot(self):
            return {"synthetic": True, **BINDING, "counts": dict(support.CALL_CAPS)}

    def writer(destination, identity, b, *, object_spec):
        assert destination == output and identity == V3.identity and object_spec is V3
        calls.append("writer-v3")
        return real_writer(destination, identity, b, object_spec=object_spec)

    def engine(*args, object_spec):
        assert object_spec is V3 and args[1] is registry
        calls.append("engine-v3")
        return real_engine(*args, object_spec=object_spec)

    def gate(value, *, checkpoint):
        assert value is permit
        checkpoint()
        calls.append("synthetic-gate-no-authority")

    def consume(value, destination, *, budget):
        assert value is permit and destination == output
        calls.append("synthetic-consume-no-reservation")

    def load(value, *, admission, budget):
        assert value is permit and admission == "SYNTHETIC_NO_NATIVE_ADMISSION"
        calls.append("synthetic-loader-no-native-imports")
        return runtime, registry, {}

    def lifecycle(snapshot, *, object_spec):
        assert snapshot["synthetic"] is True and object_spec is V3
        assert snapshot["execution_object_sha256"] == objects.object_digest(V3)
        calls.append("lifecycle-v3")
        return {"synthetic": True, **BINDING, "validated": True}

    monkeypatch.setattr(sys, "pycache_prefix", None)
    monkeypatch.setattr(support, "ResourceBudget", SyntheticBudget)
    monkeypatch.setattr(support, "require_execution_permit", gate)
    monkeypatch.setattr(support, "consume_execution_permit", consume)
    monkeypatch.setattr(support, "runtime_admission", lambda *args: nullcontext(
        "SYNTHETIC_NO_NATIVE_ADMISSION"))
    monkeypatch.setattr(support, "install_runtime_limits", lambda *args, **kwargs: {
        "synthetic_no_limits_installed": True, "started_monotonic_seconds": time.monotonic(),
    })
    monkeypatch.setattr(support, "verify_mapped_libraries", lambda *args, **kwargs: {
        "synthetic_no_native_library_admission": True,
    })
    monkeypatch.setattr(support, "ExclusiveEvidenceWriter", writer)
    monkeypatch.setattr(support, "PassiveCallMonitor", SyntheticMonitor)
    monkeypatch.setattr(support, "validate_completed_lifecycle", lifecycle)
    monkeypatch.setattr(runner, "load_real_runtime", load)
    monkeypatch.setattr(runner, "native_resource_boundary", lambda owner, modules: None)
    monkeypatch.setattr(runner, "ExecutionEngine", engine)
    terminal = runner.execute_reviewed(permit, output)
    assert terminal["failure"] is None
    assert terminal["identity"] == V3.identity
    assert terminal["execution_object_sha256"] == objects.object_digest(V3)
    assert terminal["scientific_credit"] == 0
    result = terminal["result"]
    assert result["identity"] == V3.identity and result["actual"] == runner.EXPECTED
    assert result["execution_object_sha256"] == objects.object_digest(V3)
    assert result["runtime_domain"] == "SYNTHETIC_MODEL_FREE"
    assert result["native_rollback_equivalence"] == "not_tested"
    assert set(calls) == {
        "writer-v3", "monitor-v3", "engine-v3", "lifecycle-v3",
        "synthetic-gate-no-authority", "synthetic-consume-no-reservation",
        "synthetic-loader-no-native-imports",
    }
    assert calls.count("synthetic-gate-no-authority") == 2
    saved = json.loads((output / "TERMINAL.json").read_bytes())
    assert saved["status"] == "SUCCESS" and saved["details"] == terminal
    assert saved["identity"] == V3.identity
    assert saved["execution_object_sha256"] == objects.object_digest(V3)
    for record in saved["records"] + saved["write_attempts"]:
        assert record["execution_object_sha256"] == objects.object_digest(V3)
    launch = json.loads((output / "launch-environment.json").read_bytes())
    assert launch["identity"] == V3.identity and launch["execution_object_sha256"] == (
        objects.object_digest(V3))
    copies = json.loads((output / "source-copy-index.json").read_bytes())
    assert {record["source"] for record in copies} == set(inventory)
    assert json.loads((output / "literal-inputs.json").read_bytes()) == plan
    pointer = json.loads((output / "fault-owner-boundary.json").read_bytes())
    assert pointer["exact_owner_pointer_and_generation_preserved"] is True
    assert pointer["native_rollback_equivalence"] == "not_tested"
    assert not list(tmp_path.glob("*.STARTED.json"))


def test_real_module_wrapper_selects_v3_only_while_active_main(monkeypatch):
    """Run only the inert wrapper source; the reviewed gate cannot grant authority."""
    seen = []

    def reviewed(args, *, object_spec, entry_module):
        assert object_spec is V3
        assert entry_module is sys.modules["__main__"]
        assert entry_module.__name__ == "__main__"
        assert launcher._guarded_root(args.root, object_spec=object_spec,
                                      entry_module=entry_module, require_active=True) == ROOT
        seen.append(object_spec)
        return {"failure": None, "synthetic_no_execution": True}

    monkeypatch.setattr(launcher, "_run_reviewed", reviewed)
    monkeypatch.delitem(sys.modules, wrapper.__name__)
    monkeypatch.setattr(sys, "argv", ["synthetic-wrapper", "--run-reviewed",
                                      "--approval-sha256", "a" * 64,
                                      "--approval-object-sha256", "b" * 64,
                                      "--published-commit", "c" * 40,
                                      "--source-inventory-sha256", "d" * 64])
    with pytest.raises(SystemExit) as stopped:
        runpy.run_module(wrapper.__name__, run_name="__main__", alter_sys=True)
    assert stopped.value.code == 0 and seen == [V3]


def native_origin_fixture(root, kind):
    name = {"package": "sparkbrain", "module": "sparkbrain.v05.synthetic",
            "config_only": "sparkbrain.v04.synthetic_config"}[kind]
    relative = "src/" + name.replace(".", "/")
    relative += "/__init__.py" if kind == "package" else ".py"
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Inert synthetic origin bytes: never imported or executed\n")
    module = inert_module(relative, root, name=name)
    module.__spec__.name = name
    module.__loader__.name = name
    if kind == "package":
        module.__path__ = [str(path.parent)]
    return name, module, path


@pytest.mark.parametrize("kind", ["package", "module", "config_only"])
def test_native_origin_pure_check_accepts_exact_inert_source_shapes(tmp_path, kind):
    name, module, _ = native_origin_fixture(tmp_path, kind)
    ambient = sys.modules.get(name, MISSING)
    runner.verify_native_module_origin(tmp_path, name, module)
    assert sys.modules.get(name, MISSING) is ambient


@pytest.mark.parametrize("kind", ["package", "module", "config_only"])
@pytest.mark.parametrize("change", ["module_name", "spec_name", "loader_name", "loader_path",
                                   "spec_origin", "file", "loader_identity", "missing_spec",
                                   "loader_subclass", "spec_subclass", "module_subclass",
                                   "wrong_package_shape"])
def test_native_origin_rejects_inert_package_config_and_module_aliases(tmp_path, kind, change):
    name, module, path = native_origin_fixture(tmp_path, kind)
    ambient = sys.modules.get(name, MISSING)
    alias = str(path.parent / ".." / path.parent.name / path.name)
    if change == "module_name":
        module.__name__ = name + "_alias"
    elif change == "spec_name":
        module.__spec__.name = name + "_alias"
    elif change == "loader_name":
        module.__loader__.name = name + "_alias"
    elif change == "loader_path":
        module.__loader__.path = alias
    elif change == "spec_origin":
        module.__spec__.origin = alias
    elif change == "file":
        module.__file__ = alias
    elif change == "loader_identity":
        module.__loader__ = importlib.machinery.SourceFileLoader(name, str(path))
    elif change == "missing_spec":
        del module.__spec__
    elif change == "loader_subclass":
        class DerivedLoader(importlib.machinery.SourceFileLoader):
            pass
        loader = DerivedLoader(name, str(path))
        module.__loader__ = module.__spec__.loader = loader
    elif change == "spec_subclass":
        class DerivedSpec(importlib.machinery.ModuleSpec):
            pass
        module.__spec__ = DerivedSpec(name, module.__loader__, origin=str(path))
    elif change == "module_subclass":
        class DerivedModule(types.ModuleType):
            pass
        replacement = DerivedModule(name)
        vars(replacement).update(vars(module))
        module = replacement
    elif kind == "package":
        del module.__path__
    else:
        module.__path__ = [str(path.parent)]
    with pytest.raises((runner.BindingError, ValueError, OSError)):
        runner.verify_native_module_origin(tmp_path, name, module)
    assert sys.modules.get(name, MISSING) is ambient


@pytest.mark.parametrize("field", [
    "schema", "execution_object_sha256", "source_root", "published_commit",
    "runtime_origin_commit", "source_inventory_sha256", "proof_sha256", "reference",
    *PRELAUNCH_FLAGS,
])
def test_prelaunch_exact_schema_rejects_every_missing_field_without_authority(tmp_path, field):
    proof = inert_prelaunch_shape(tmp_path, "c" * 40, "b" * 64)
    proof.pop(field)
    with pytest.raises(support.AdmissionError, match="prelaunch"):
        support.verify_prelaunch_materialization(
            tmp_path, {"prelaunch_materialization": proof}, "c" * 40, "b" * 64,
            object_spec=V3)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("field,value", [
    ("schema", "unreviewed-schema"),
    ("execution_object_sha256", objects.object_digest(OLD)),
    ("source_root", "/SYNTHETIC_WRONG_ROOT"),
    ("published_commit", "d" * 40),
    ("runtime_origin_commit", OLD.runtime_origin_commit),
    ("source_inventory_sha256", "d" * 64),
    ("proof_sha256", "A" * 64), ("proof_sha256", "g" * 64),
    ("proof_sha256", "a" * 63), ("proof_sha256", None),
    ("reference", ""), ("reference", " \t\n"), ("reference", 7),
    ("unreviewed_extra_field", True),
])
def test_prelaunch_rejects_crossbindings_or_malformed_proof(tmp_path, field, value):
    proof = inert_prelaunch_shape(tmp_path, "c" * 40, "b" * 64)
    proof[field] = value
    with pytest.raises(support.AdmissionError, match="prelaunch"):
        support.verify_prelaunch_materialization(
            tmp_path, {"prelaunch_materialization": proof}, "c" * 40, "b" * 64,
            object_spec=V3)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("flag", PRELAUNCH_FLAGS)
@pytest.mark.parametrize("value", [False, 1, "true"])
def test_prelaunch_requires_exact_true_for_every_external_prerequisite(tmp_path, flag, value):
    proof = inert_prelaunch_shape(tmp_path, "c" * 40, "b" * 64)
    proof[flag] = value
    with pytest.raises(support.AdmissionError, match="prelaunch"):
        support.verify_prelaunch_materialization(
            tmp_path, {"prelaunch_materialization": proof}, "c" * 40, "b" * 64,
            object_spec=V3)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("commit,inventory", [
    ("C" * 40, "b" * 64), ("c" * 39, "b" * 64), (None, "b" * 64),
    ("c" * 40, "B" * 64), ("c" * 40, "b" * 63), ("c" * 40, None),
])
def test_prelaunch_rejects_malformed_external_pins_even_when_record_matches(
        tmp_path, commit, inventory):
    proof = inert_prelaunch_shape(tmp_path, commit, inventory)
    with pytest.raises(support.AdmissionError, match="exact published commit/inventory pins"):
        support.verify_prelaunch_materialization(
            tmp_path, {"prelaunch_materialization": proof}, commit, inventory, object_spec=V3)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("value", [MISSING, None, [], "SYNTHETIC_NOT_ATTESTATION"])
def test_v3_missing_prelaunch_record_never_inherits_historical_exemption(tmp_path, value):
    approval = {} if value is MISSING else {"prelaunch_materialization": value}
    with pytest.raises(support.AdmissionError, match="prelaunch"):
        support.verify_prelaunch_materialization(
            tmp_path, approval, "c" * 40, "b" * 64, object_spec=V3)
    support.verify_prelaunch_materialization(tmp_path, approval, "c" * 40, "b" * 64)
    assert list(tmp_path.iterdir()) == []


def test_prelaunch_inert_shape_validation_does_not_create_authority(tmp_path):
    before = set(support._PERMITS)
    proof = inert_prelaunch_shape(tmp_path, "c" * 40, "b" * 64)
    assert support.verify_prelaunch_materialization(
        tmp_path, {"prelaunch_materialization": proof}, "c" * 40, "b" * 64,
        object_spec=V3) is None
    assert set(support._PERMITS) == before and list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("change", ["missing", "object", "root", "commit", "inventory"])
def test_authorize_checks_prelaunch_before_ledger_or_callback(
        negative_authority, monkeypatch, change):
    root, approval, _, _ = negative_authority
    proof = approval["prelaunch_materialization"]
    if change == "missing":
        approval.pop("prelaunch_materialization")
    elif change == "object":
        proof["execution_object_sha256"] = objects.object_digest(OLD)
    elif change == "root":
        proof["source_root"] = str(root / "wrong")
    elif change == "commit":
        proof["published_commit"] = "d" * 40
    else:
        proof["source_inventory_sha256"] = "d" * 64
    original = support.confined_path

    def guarded(source, relative, label, **kwargs):
        if label == "identity ledger":
            pytest.fail("prelaunch rejection must precede identity ledger access")
        return original(source, relative, label, **kwargs)

    monkeypatch.setattr(support, "confined_path", guarded)
    with pytest.raises(support.AdmissionError, match="prelaunch"):
        reject_fixture(negative_authority)


@pytest.mark.parametrize("change", ["missing", "object", "root", "commit", "inventory"])
def test_launch_binding_checks_prelaunch_against_exact_external_pins(prepared_tree, change):
    root, freeze, _ = prepared_tree
    inventory = freeze["source_files_sha256"]
    inventory_sha = support.digest(support.canonical(inventory))
    commit = "c" * 40
    proof = inert_prelaunch_shape(root, commit, inventory_sha)
    approval = {
        "classification": "SYNTHETIC_NOT_APPROVAL", **BINDING,
        "launcher": {"path": V3.launcher_relative, "sha256": inventory[V3.launcher_relative]},
        "freeze_sha256": support.digest((root / V3.freeze_relative).read_bytes()),
        "source_inventory_sha256": inventory_sha,
        "publication": {"commit": commit, "exact_source_sha256": inventory_sha},
        "materialized_source": {
            "schema": launcher.PROVENANCE_SCHEMA, "source_root": str(root),
            "published_commit": commit, "source_inventory_sha256": inventory_sha,
            "materialization": "independently_verified_published_tree",
            "local_git_head_is_source_authority": False, "reference": "SYNTHETIC_ONLY",
        },
        "prelaunch_materialization": proof,
    }
    assert launcher._verify_launch_bindings(
        root, approval, commit, inventory_sha, object_spec=V3) is None
    if change == "missing":
        approval.pop("prelaunch_materialization")
    elif change == "object":
        proof["execution_object_sha256"] = objects.object_digest(OLD)
    elif change == "root":
        proof["source_root"] = str(root / "wrong")
    elif change == "commit":
        proof["published_commit"] = "d" * 40
    else:
        proof["source_inventory_sha256"] = "d" * 64
    with pytest.raises(support.AdmissionError, match="prelaunch"):
        launcher._verify_launch_bindings(root, approval, commit, inventory_sha, object_spec=V3)
    assert not list(root.glob("*.STARTED.json"))


@pytest.mark.parametrize("spec,wrong", [(V3, OLD), (OLD, V3)])
def test_explicit_identity_cannot_contradict_matching_object_digest(spec, wrong):
    value = {"identity": wrong.identity, "execution_object_sha256": objects.object_digest(spec)}
    with pytest.raises(support.AdmissionError, match="object binding"):
        support._require_object_binding(value, spec)
    value["identity"] = spec.identity
    support._require_object_binding(value, spec)


@pytest.mark.parametrize("kind", ["subclass", "standin"])
@pytest.mark.parametrize("spec", [MISSING, OLD, objects.ExecutionObject(*V3)])
def test_v3_monitor_cannot_evade_writer_binding_via_subclass_or_standin(tmp_path, kind, spec):
    if kind == "subclass":
        class InertWriter(support.ExclusiveEvidenceWriter):
            pass
        writer = object.__new__(InertWriter)
    else:
        writer = SimpleNamespace()
    if spec is not MISSING:
        writer._object_spec = spec
    with pytest.raises(support.AdmissionError,
                       match="writer belongs to a different execution object"):
        support.PassiveCallMonitor(tmp_path, None, budget(), writer, object_spec=V3)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("target", ["approval", "ledger", "prelaunch"])
def test_sibling_v2_binding_cannot_admit_v3(negative_authority, target):
    root, approval, ledger, _ = negative_authority
    sibling = objects.object_digest(objects.G0_V2)
    if target == "approval":
        approval["execution_object_sha256"] = sibling
    elif target == "ledger":
        ledger["identities"][V3.identity]["execution_object_sha256"] = sibling
    else:
        approval["prelaunch_materialization"]["execution_object_sha256"] = sibling
    with pytest.raises(support.AdmissionError):
        reject_fixture(negative_authority)
    assert not list(root.glob("*.STARTED.json"))


@pytest.mark.parametrize("component", ["registry", "writer"])
def test_sibling_v2_cannot_supply_v3_engine_components(component):
    registry = runner.SourceRegistry(())
    registry.execution_object_sha256 = objects.object_digest(V3)
    writer = standins.MemoryWriter()
    writer._object_spec = V3
    if component == "registry":
        registry.execution_object_sha256 = objects.object_digest(objects.G0_V2)
    else:
        writer._object_spec = objects.G0_V2
    runtime = standins.ModelFreeRuntime()
    with pytest.raises(runner.BindingError):
        runner.ExecutionEngine(runtime, registry, None, writer, standins.NoLimitBudget(),
                               standins.input_plan(), object_spec=V3)
    assert runtime.calls == [] and writer.rows == {}


def test_sibling_v2_permit_digest_rejects_v3_without_reads(monkeypatch):
    permit = fake_permit(monkeypatch, {
        "object_spec": V3, **objects.object_binding(objects.G0_V2),
    })
    monkeypatch.setattr(support, "verify_preparation", forbid)
    with pytest.raises(support.AdmissionError, match="object binding"):
        support.require_execution_permit(permit)


def test_sibling_v2_wrapper_cannot_launch_v3():
    from scripts import launch_g0_v2_eligibility as sibling_wrapper

    with pytest.raises(support.AdmissionError, match="origin"):
        launcher._guarded_root(str(ROOT), object_spec=V3, entry_module=sibling_wrapper,
                               require_active=True)

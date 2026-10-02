"""Inert source-only object boundaries; no native runtime imports or construction.

Synthetic class declarations below contain only ``pass`` or literal ``__slots__``.
Their module names/source metadata exercise the binder, not SparkBrain behavior.
Nothing in this suite creates execution approval or empirical G0 evidence.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import random
import shutil
import sys
import types
from pathlib import Path

import pytest

from scripts import g0_execution_objects as objects
from scripts import verify_g0_joint_source_contract as legacy
from scripts.g0_joint_ownership import OwnershipError, SourceRegistry

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = (objects.HISTORICAL_G0, objects.G0_V2)
FIELDS = (
    "identity", "artifact_root", "contract_relative", "contract_sha256",
    "runtime_origin_commit", "launcher_relative",
)


@pytest.fixture
def current_sources(tmp_path):
    """Copy only contract-listed bytes; never import or alter the source checkout."""
    root = tmp_path / "current-source"
    contract_relative = objects.G0_V2.contract_relative
    contract = json.loads((ROOT / contract_relative).read_bytes())
    relatives = {contract_relative}
    for key in ("runtime_sources_sha256", "runtime_schema_sha256", "reuse_sources_sha256"):
        relatives.update(contract[key])
    relatives.update(contract["files"])
    for relative in sorted(relatives):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    return root


@pytest.fixture
def source_shaped_classes(current_sources, monkeypatch):
    """Bind inert storage shapes with no execution of any native source node."""
    contract = json.loads((current_sources / objects.G0_V2.contract_relative).read_bytes())
    classes = []
    for relative, record in contract["files"].items():
        module_name = relative.removeprefix("src/").removesuffix(".py").replace("/", ".")
        source = str(current_sources / relative)
        loader = importlib.machinery.SourceFileLoader(module_name, source)
        module = types.ModuleType(module_name)
        module.__file__ = source
        module.__loader__ = loader
        module.__spec__ = importlib.util.spec_from_loader(module_name, loader, origin=source)
        declarations = []
        for name, witness in record["classes"].items():
            fields = witness["slot_fields"]
            body = [ast.Pass()]
            if fields:
                body = [ast.Assign(
                    targets=[ast.Name(id="__slots__", ctx=ast.Store())],
                    value=ast.Tuple(elts=[ast.Constant(value=field) for field in fields],
                                    ctx=ast.Load()),
                )]
            declarations.append(ast.ClassDef(
                name=name, bases=[], keywords=[], body=body, decorator_list=[],
            ))
        inert_ast = ast.fix_missing_locations(ast.Module(body=declarations, type_ignores=[]))
        # This AST was built above from inert class/storage literals, not parsed
        # or compiled from native source code. The loader is never executed.
        exec(compile(inert_ast, source, "exec"), vars(module))
        monkeypatch.setitem(sys.modules, module_name, module)
        classes.extend(vars(module)[name] for name in record["classes"])
    monkeypatch.setattr(objects, "verify_object_source", lambda root, object_spec: {
        "contract_sha256": object_spec.contract_sha256,
    })
    assert len(classes) == 101
    return current_sources, tuple(classes) + (random.Random,), contract


def bind(fixture, classes=None, root=None):
    source, expected, _ = fixture
    return objects.bind_object_registry(
        source if root is None else root,
        expected if classes is None else classes,
        objects.G0_V2,
    )


@pytest.mark.parametrize("spec", OBJECTS)
def test_exact_immutable_closed_execution_object(spec):
    assert type(spec) is objects.ExecutionObject
    assert tuple(spec._fields) == FIELDS
    assert all(type(getattr(spec, field)) is str for field in FIELDS)
    assert objects.require_object(spec) is spec
    assert not hasattr(spec, "__dict__")
    for field in FIELDS:
        with pytest.raises((AttributeError, TypeError)):
            setattr(spec, field, "forged")
        with pytest.raises((AttributeError, TypeError)):
            object.__setattr__(spec, field, "forged")
    assert objects.require_object(spec) is spec


@pytest.mark.parametrize("spec", OBJECTS)
def test_object_descriptor_digest_is_canonical_and_complete(spec):
    raw = (json.dumps(spec._asdict(), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False) + "\n").encode()
    assert objects.object_digest(spec) == hashlib.sha256(raw).hexdigest()
    assert objects.object_digest(spec) == objects.object_digest(spec)
    assert objects.object_digest(objects.HISTORICAL_G0) != objects.object_digest(objects.G0_V2)


@pytest.mark.parametrize("spec", OBJECTS)
def test_object_paths_keep_historical_and_successor_namespaces_separate(spec):
    for property_name, filename in (
        ("freeze_relative", "freeze.json"),
        ("protocol_relative", "protocol.json"),
        ("inputs_relative", "inputs.json"),
        ("approval_relative", "independent-execution-approval.json"),
    ):
        assert getattr(spec, property_name) == f"{spec.artifact_root}/{filename}"
    other = objects.G0_V2 if spec is objects.HISTORICAL_G0 else objects.HISTORICAL_G0
    assert spec.identity != other.identity
    assert spec.artifact_root != other.artifact_root
    assert spec.contract_relative != other.contract_relative
    assert spec.contract_sha256 != other.contract_sha256


@pytest.mark.parametrize("spec", OBJECTS)
@pytest.mark.parametrize("replacement", ["copy", "deepcopy", "constructor", "subclass", "mapping"])
def test_value_equal_objects_never_grant_object_identity(spec, replacement):
    if replacement == "copy":
        forged = copy.copy(spec)
    elif replacement == "deepcopy":
        forged = copy.deepcopy(spec)
    elif replacement == "constructor":
        forged = objects.ExecutionObject(*spec)
    elif replacement == "mapping":
        forged = spec._asdict()
    else:
        class Derived(objects.ExecutionObject):
            pass
        forged = Derived(*spec)
    assert forged is not spec
    with pytest.raises((ValueError, TypeError)):
        objects.require_object(forged)
    with pytest.raises((ValueError, TypeError)):
        objects.object_digest(forged)


@pytest.mark.parametrize("field", FIELDS)
def test_mutated_descriptor_copy_is_rejected_at_all_public_gates(field, tmp_path):
    forged = objects.G0_V2._replace(**{field: "forged"})
    for operation in (
        lambda: objects.require_object(forged),
        lambda: objects.object_digest(forged),
        lambda: objects.verify_object_source(tmp_path, forged),
        lambda: objects.bind_object_registry(tmp_path, (), forged),
    ):
        with pytest.raises((ValueError, TypeError)):
            operation()


@pytest.mark.parametrize("forged", [None, "assembly-m1-g0-v2-20261002", (), object()])
def test_unknown_object_types_fail_closed(forged):
    with pytest.raises((ValueError, TypeError)):
        objects.require_object(forged)


def test_historical_default_source_verifier_is_unchanged(historical_sources):
    expected = legacy.verify(historical_sources)
    assert objects.verify_object_source(historical_sources) == expected
    assert objects.verify_object_source(historical_sources, objects.HISTORICAL_G0) == expected


def test_historical_registry_default_delegates_without_successor_reinterpretation(monkeypatch):
    calls = []
    sentinel = object()

    def delegate(cls, root, loaded_classes):
        calls.append((cls, root, loaded_classes))
        return sentinel

    monkeypatch.setattr(SourceRegistry, "from_verified_source", classmethod(delegate))
    assert objects.bind_object_registry(ROOT, ()) is sentinel
    assert objects.bind_object_registry(ROOT, (), objects.HISTORICAL_G0) is sentinel
    assert calls == [(SourceRegistry, ROOT, ()), (SourceRegistry, ROOT, ())]


def test_current_source_verifies_only_for_its_explicit_successor_object():
    result = objects.verify_object_source(ROOT, objects.G0_V2)
    assert result["contract_sha256"] == objects.G0_V2.contract_sha256
    assert result["runtime_python_files"] == 157
    assert result["runtime_schema_files"] == 15
    assert result["class_witnesses"] == 101
    assert result["runtime_execution_authorized"] is False
    assert result["scientific_credit"] == 0
    with pytest.raises(ValueError):
        objects.verify_object_source(ROOT)


@pytest.mark.parametrize("change", [
    "changed_python", "extra_python", "missing_python", "changed_schema", "extra_schema",
    "changed_reuse", "changed_contract",
])
def test_successor_source_dependency_drift_fails_closed(current_sources, change):
    contract = json.loads((current_sources / objects.G0_V2.contract_relative).read_bytes())
    if change == "changed_contract":
        target = current_sources / objects.G0_V2.contract_relative
    elif change == "changed_reuse":
        target = current_sources / next(iter(contract["reuse_sources_sha256"]))
    elif change in ("changed_schema", "extra_schema"):
        target = current_sources / next(iter(contract["runtime_schema_sha256"]))
        if change == "extra_schema":
            target = target.parent / "unreviewed.json"
    else:
        target = current_sources / next(iter(contract["runtime_sources_sha256"]))
        if change == "extra_python":
            target = target.parent / "unreviewed.py"
    if change == "missing_python":
        target.unlink()
    else:
        target.write_bytes((target.read_bytes() if target.exists() else b"") + b"\n")
    with pytest.raises(ValueError):
        objects.verify_object_source(current_sources, objects.G0_V2)


@pytest.mark.parametrize("location", ["root", "src", "schemas", "contract", "source"])
def test_successor_source_and_ancestors_reject_symlink_aliases(current_sources, location):
    if location == "root":
        alias = current_sources.parent / "alias"
        alias.symlink_to(current_sources, target_is_directory=True)
        supplied = alias
    else:
        relative = {
            "src": "src",
            "schemas": "schemas",
            "contract": objects.G0_V2.contract_relative,
            "source": "src/sparkbrain/v032/runtime.py",
        }[location]
        original = current_sources / relative
        target = current_sources / "relocated"
        directory = original.is_dir()
        original.rename(target)
        original.symlink_to(target, target_is_directory=directory)
        supplied = current_sources
    with pytest.raises(ValueError):
        objects.verify_object_source(supplied, objects.G0_V2)


def test_successor_registry_contains_exact_inert_shapes_and_object_binding(source_shaped_classes):
    root, classes, contract = source_shaped_classes
    registry = bind(source_shaped_classes)
    assert type(registry) is SourceRegistry
    assert registry.domain == "VERIFIED_SOURCE_PREPARATION"
    assert registry.source_root == root
    assert registry.contract_sha256 == objects.G0_V2.contract_sha256
    assert registry.execution_object_sha256 == objects.object_digest(objects.G0_V2)
    assert set(registry._specs) == set(classes)
    for cls in classes:
        spec = registry.spec(cls)
        assert spec.cls is cls
        if cls is random.Random:
            assert spec.dict_fields == ("gauss_next",)
            continue
        relative = "src/" + cls.__module__.replace(".", "/") + ".py"
        witness = contract["files"][relative]["classes"][cls.__name__]
        slots = tuple(witness["slot_fields"])
        assert spec.slot_fields == slots
        assert spec.dict_fields == (None if slots else tuple(witness["dict_fields"]))


@pytest.mark.parametrize("change", [
    "missing_class", "duplicate_class", "missing_random", "duplicate_random",
    "unknown_class", "class_instance", "random_subclass", "class_subclass",
])
def test_successor_registry_requires_closed_complete_class_multiset(source_shaped_classes, change):
    _, expected, _ = source_shaped_classes
    classes = list(expected)
    if change == "missing_class":
        classes.pop(0)
    elif change == "duplicate_class":
        classes.append(classes[0])
    elif change == "missing_random":
        classes.remove(random.Random)
    elif change == "duplicate_random":
        classes.append(random.Random)
    elif change == "unknown_class":
        classes[0] = type("Unknown", (), {})
    elif change == "class_instance":
        classes[0] = object()
    elif change == "random_subclass":
        classes[-1] = type("RandomSubclass", (random.Random,), {})
    else:
        classes[0] = type("Derived", (classes[0],), {})
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes, tuple(classes))


@pytest.mark.parametrize("change", [
    "module_binding", "nested_qualname", "module_name", "module_type", "no_spec",
    "spec_origin", "spec_name", "module_internal_name", "loader_type",
    "loader_subclass", "loader_name",
    "loader_path", "spec_loader", "divergent_loader", "file_path",
])
def test_successor_registry_rejects_forged_module_origin_and_loaders(
    source_shaped_classes, monkeypatch, change,
):
    root, classes, _ = source_shaped_classes
    cls = classes[0]
    module = sys.modules[cls.__module__]
    if change == "module_binding":
        monkeypatch.setattr(module, cls.__name__, object())
    elif change == "nested_qualname":
        cls.__qualname__ = "Nested." + cls.__name__
    elif change == "module_name":
        monkeypatch.setattr(cls, "__module__", "unreviewed.module")
    elif change == "module_type":
        monkeypatch.setitem(sys.modules, cls.__module__, types.SimpleNamespace(**vars(module)))
    elif change == "no_spec":
        monkeypatch.setattr(module, "__spec__", None)
    elif change == "spec_origin":
        monkeypatch.setattr(module.__spec__, "origin", str(root / "unreviewed.py"))
    elif change == "spec_name":
        monkeypatch.setattr(module.__spec__, "name", "unreviewed.module")
    elif change == "module_internal_name":
        monkeypatch.setattr(module, "__name__", "unreviewed.module")
    elif change == "loader_type":
        monkeypatch.setattr(module, "__loader__", object())
    elif change == "loader_subclass":
        class DerivedLoader(importlib.machinery.SourceFileLoader):
            pass
        loader = DerivedLoader(module.__name__, module.__file__)
        monkeypatch.setattr(module, "__loader__", loader)
        monkeypatch.setattr(module.__spec__, "loader", loader)
    elif change == "loader_name":
        monkeypatch.setattr(module.__loader__, "name", "unreviewed.module")
    elif change == "loader_path":
        monkeypatch.setattr(module.__loader__, "path", str(root / "unreviewed.py"))
    elif change == "spec_loader":
        monkeypatch.setattr(module.__spec__, "loader", object())
    elif change == "divergent_loader":
        loader = importlib.machinery.SourceFileLoader(module.__name__, module.__file__)
        monkeypatch.setattr(module.__spec__, "loader", loader)
    else:
        monkeypatch.setattr(module, "__file__", str(root / "unreviewed.py"))
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes)


@pytest.mark.parametrize("alias_location", ["root", "module", "origin", "loader"])
def test_successor_registry_never_normalizes_aliased_source_paths(
    source_shaped_classes, monkeypatch, alias_location,
):
    root, classes, _ = source_shaped_classes
    module = sys.modules[classes[0].__module__]
    if alias_location == "root":
        alias = root.parent / "root_alias"
        alias.symlink_to(root, target_is_directory=True)
        supplied = alias
    else:
        alias = root / "class_alias.py"
        alias.symlink_to(module.__file__)
        supplied = root
        if alias_location == "module":
            monkeypatch.setattr(module, "__file__", str(alias))
        elif alias_location == "origin":
            monkeypatch.setattr(module.__spec__, "origin", str(alias))
        else:
            monkeypatch.setattr(module.__loader__, "path", str(alias))
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes, root=supplied)


@pytest.mark.parametrize("change", ["source", "contract"])
def test_successor_registry_rechecks_bytes_after_verification(source_shaped_classes, change):
    root, classes, _ = source_shaped_classes
    target = (root / objects.G0_V2.contract_relative if change == "contract"
              else Path(sys.modules[classes[0].__module__].__file__))
    target.write_bytes(target.read_bytes() + b"\n")
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes)


@pytest.mark.parametrize("change", ["list", "tuple_subclass", "metaclass"])
def test_successor_registry_rejects_nonexact_entry_container_and_class_types(
    source_shaped_classes, change,
):
    _, classes, _ = source_shaped_classes
    if change == "list":
        supplied = list(classes)
    elif change == "tuple_subclass":
        class DerivedTuple(tuple):
            pass
        supplied = DerivedTuple(classes)
    else:
        class DerivedMeta(type):
            pass
        supplied = (DerivedMeta("Fake", (), {}), *classes[1:])
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes, supplied)


@pytest.mark.parametrize("change", ["storage", "allocation", "inheritance"])
def test_successor_registry_preserves_population_storage_and_allocation_guards(
    source_shaped_classes, monkeypatch, change,
):
    _, expected, _ = source_shaped_classes
    original = expected[0]
    module = sys.modules[original.__module__]
    attributes = {"__module__": original.__module__}
    bases = ()
    if change == "storage":
        attributes["__slots__"] = ("unreviewed_storage",)
    elif change == "allocation":
        def forbidden_new(cls):
            raise AssertionError("inert allocator must never execute")
        attributes["__new__"] = staticmethod(forbidden_new)
    else:
        bases = (type("UnreviewedBase", (), {}),)
    replacement = type(original.__name__, bases, attributes)
    monkeypatch.setattr(module, original.__name__, replacement)
    classes = (replacement, *expected[1:])
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes, classes)


def test_successor_registry_rejects_equal_bytes_bound_to_another_root(source_shaped_classes):
    root, _, _ = source_shaped_classes
    other = root.parent / "other-root"
    shutil.copytree(root, other)
    with pytest.raises(OwnershipError):
        bind(source_shaped_classes, root=other)


def test_historical_descriptor_keeps_original_identity_and_source_pin():
    spec = objects.HISTORICAL_G0
    assert spec.identity == "assembly-m1-g0-v1-20261002"
    assert spec.artifact_root == "artifacts/research/assembly_m1_g0_v1_20261002"
    assert spec.contract_relative == legacy.CONTRACT
    assert spec.contract_sha256 == legacy.CONTRACT_SHA256
    assert spec.runtime_origin_commit == "b9caed4797c9cd8217361b6e523864aabdd4cbcc"
    assert spec.launcher_relative == "scripts/launch_g0_joint_eligibility.py"


def test_successor_descriptor_is_explicitly_current_and_separately_named():
    spec = objects.G0_V2
    assert spec.identity == "assembly-m1-g0-v2-20261002"
    assert spec.artifact_root == "artifacts/research/assembly_m1_g0_v2_20261002"
    assert spec.contract_relative == spec.artifact_root + "/source_contract.json"
    assert spec.runtime_origin_commit == "d3ad56dce4256634ce62c69acecd1de65fcd9fb7"
    assert spec.launcher_relative == "scripts/launch_g0_v2_eligibility.py"
    assert hashlib.sha256((ROOT / spec.contract_relative).read_bytes()).hexdigest() == (
        spec.contract_sha256
    )


def test_only_successor_records_add_the_explicit_object_binding():
    assert objects.object_binding(objects.HISTORICAL_G0) == {}
    assert objects.object_binding(objects.G0_V2) == {
        "execution_object_sha256": objects.object_digest(objects.G0_V2),
    }
    with pytest.raises(ValueError):
        objects.object_binding(copy.copy(objects.G0_V2))


def test_complete_successor_class_set_has_no_caller_order_dependency(source_shaped_classes):
    _, classes, _ = source_shaped_classes
    registry = bind(source_shaped_classes, tuple(reversed(classes)))
    assert set(registry._specs) == set(classes)

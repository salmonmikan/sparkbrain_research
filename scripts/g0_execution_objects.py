"""Two fixed G0 source objects; imports and source checks confer no run authority.

Tuple-backed descriptors contain only immutable strings. Their digest excludes the
protocol/freeze/approval and this module's bytes, avoiding every back-edge in the
source-contract -> descriptor -> protocol -> outer-freeze dependency graph.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.machinery
import inspect
import json
import random
import stat
import sys
import types
from pathlib import Path
from typing import Any, NamedTuple

from scripts import verify_g0_joint_source_contract as legacy


class ExecutionObject(NamedTuple):
    identity: str
    artifact_root: str
    contract_relative: str
    contract_sha256: str
    runtime_origin_commit: str
    launcher_relative: str

    @property
    def freeze_relative(self) -> str:
        return self.artifact_root + "/freeze.json"

    @property
    def protocol_relative(self) -> str:
        return self.artifact_root + "/protocol.json"

    @property
    def inputs_relative(self) -> str:
        return self.artifact_root + "/inputs.json"

    @property
    def approval_relative(self) -> str:
        return self.artifact_root + "/independent-execution-approval.json"


HISTORICAL_G0 = ExecutionObject(
    "assembly-m1-g0-v1-20261002", "artifacts/research/assembly_m1_g0_v1_20261002",
    legacy.CONTRACT, legacy.CONTRACT_SHA256, "b9caed4797c9cd8217361b6e523864aabdd4cbcc",
    "scripts/launch_g0_joint_eligibility.py",
)
G0_V2 = ExecutionObject(
    "assembly-m1-g0-v2-20261002", "artifacts/research/assembly_m1_g0_v2_20261002",
    "artifacts/research/assembly_m1_g0_v2_20261002/source_contract.json",
    "61b9025247ff89909e6cf2f2f326f09b1cff050b27c66d3b0dc0ac770cbe9278",
    "d3ad56dce4256634ce62c69acecd1de65fcd9fb7", "scripts/launch_g0_v2_eligibility.py",
)


def require_object(object_spec: ExecutionObject) -> ExecutionObject:
    if object_spec is not HISTORICAL_G0 and object_spec is not G0_V2:
        raise ValueError("execution object must be an exact source-defined singleton")
    return object_spec


def object_digest(object_spec: ExecutionObject) -> str:
    spec = require_object(object_spec)
    raw = (json.dumps(spec._asdict(), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False) + "\n").encode()
    return hashlib.sha256(raw).hexdigest()


def object_binding(object_spec: ExecutionObject) -> dict[str, str]:
    """Historical default records retain their exact schema; v2 is always cross-bound."""
    spec = require_object(object_spec)
    return {} if spec is HISTORICAL_G0 else {"execution_object_sha256": object_digest(spec)}


def verify_object_source(root: Path, object_spec: ExecutionObject = HISTORICAL_G0,
                         ) -> dict[str, Any]:
    spec = require_object(object_spec)
    if spec is HISTORICAL_G0:
        return legacy.verify(root)
    root = legacy.source_root(root)
    raw = legacy.confined_path(root, spec.contract_relative, "object contract").read_bytes()
    if hashlib.sha256(raw).hexdigest() != spec.contract_sha256:
        raise ValueError("object source contract digest mismatch")
    contract = json.loads(raw)
    if (contract["runtime_execution_authorized"] is not False
            or contract["scientific_credit"] != 0
            or contract["source_commit"] != spec.runtime_origin_commit):
        raise ValueError("object source-only/origin boundary differs")
    for key, directory, suffix, size in (
            ("runtime_sources_sha256", "src/sparkbrain", ".py", 157),
            ("runtime_schema_sha256", "schemas", ".json", 15)):
        actual = {}
        pending = [legacy.confined_path(root, directory, "runtime dependency", directory=True)]
        while pending:
            for path in sorted(pending.pop().iterdir()):
                info = legacy.path_metadata(path, "runtime dependency")
                if stat.S_ISDIR(info.st_mode):
                    pending.append(path)
                elif path.name.endswith(suffix):
                    relative = path.relative_to(root).as_posix()
                    checked = legacy.confined_path(root, relative, "runtime dependency")
                    actual[relative] = hashlib.sha256(checked.read_bytes()).hexdigest()
        if len(actual) != size or actual != contract[key]:
            raise ValueError("complete object runtime dependency inventory mismatch: " + key)
    for relative, expected in contract["reuse_sources_sha256"].items():
        path = legacy.confined_path(root, relative, "reuse source")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("reuse source digest mismatch")
    count = 0
    for relative, record in contract["files"].items():
        raw = legacy.confined_path(root, relative, "source").read_bytes()
        if hashlib.sha256(raw).hexdigest() != record["sha256"]:
            raise ValueError("source digest mismatch: " + relative)
        tree = ast.parse(raw, filename=relative)
        for name, expected in record["classes"].items():
            matches = [node for node in tree.body if isinstance(node, ast.ClassDef)
                       and node.name == name]
            if (len(matches) != 1 or legacy.class_spec(matches[0]) != expected
                    or expected["source_hooks"]):
                raise ValueError("source class witness mismatch: " + relative + ":" + name)
            count += 1
    if count != 101:
        raise ValueError("complete object class witness count mismatch")
    return {"classification": "SOURCE_ONLY_NON_EVIDENTIARY",
            "status": "SOURCE_BINDINGS_VERIFIED_REAL_G0_NOT_EXECUTED",
            "contract_sha256": spec.contract_sha256, "source_commit": contract["source_commit"],
            "source_files": len(contract["files"]), "class_witnesses": count,
            "runtime_python_files": 157, "runtime_schema_files": 15,
            "reuse_source_files": len(contract["reuse_sources_sha256"]),
            "runtime_execution_authorized": False, "scientific_credit": 0,
            **object_binding(spec)}


def bind_object_registry(root: Path, loaded_classes: tuple[type, ...],
                         object_spec: ExecutionObject = HISTORICAL_G0) -> Any:
    """Bind an exact complete already-loaded class set; never load a runtime module."""
    from scripts.g0_joint_ownership import OwnershipError, SourceRegistry, TypeSpec

    spec = require_object(object_spec)
    if spec is HISTORICAL_G0:
        return SourceRegistry.from_verified_source(root, loaded_classes)
    try:
        root = legacy.source_root(root)
        verified = verify_object_source(root, spec)
        raw = legacy.confined_path(root, spec.contract_relative, "object contract").read_bytes()
        if hashlib.sha256(raw).hexdigest() != verified["contract_sha256"]:
            raise ValueError("object contract changed after verification")
        contract = json.loads(raw)
    except (OSError, ValueError, KeyError) as error:
        raise OwnershipError(f"object source verification failed: {error}") from None
    expected = {(path, name) for path, record in contract["files"].items()
                for name in record["classes"]}
    if (type(loaded_classes) is not tuple or len(expected) != 101
            or len(loaded_classes) != 102
            or any(type(cls) is not type for cls in loaded_classes)
            or len(set(loaded_classes)) != 102
            or sum(cls is random.Random for cls in loaded_classes) != 1):
        raise OwnershipError("object registry requires every exact class and Random once")
    seen, specs = set(), []
    for loaded in loaded_classes:
        if loaded is random.Random:
            specs.append(TypeSpec(random.Random, "stdlib:random.Random:exact-state-v1",
                                  ("gauss_next",)))
            continue
        name = loaded.__module__
        module = sys.modules.get(name)
        relative = "src/" + name.replace(".", "/") + ".py"
        key = (relative, loaded.__name__)
        if (key not in expected or key in seen or type(module) is not types.ModuleType
                or loaded.__qualname__ != loaded.__name__
                or vars(module).get(loaded.__name__) is not loaded):
            raise OwnershipError("loaded class is not its exact expected module-level binding")
        try:
            path = legacy.confined_path(root, relative, "loaded source")
            module_spec = vars(module).get("__spec__")
            if (type(module_spec) is not importlib.machinery.ModuleSpec
                    or type(module_spec.loader) is not importlib.machinery.SourceFileLoader
                    or vars(module).get("__loader__") is not module_spec.loader
                    or vars(module).get("__name__") != name
                    or module_spec.name != name
                    or module_spec.loader.name != name
                    or module_spec.loader.path != str(path)
                    or vars(module).get("__file__") != str(path)
                    or module_spec.origin != str(path)
                    or inspect.getsourcefile(loaded) != str(path)):
                raise ValueError("loaded class source origin differs from guarded root")
            record = contract["files"][relative]
            if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
                raise ValueError("loaded class source bytes changed after verification")
        except (OSError, TypeError, ValueError):
            raise OwnershipError("loaded class source origin/hash differs") from None
        witness = record["classes"][loaded.__name__]
        slots = tuple(witness["slot_fields"])
        specs.append(TypeSpec(loaded, f"{relative}:{loaded.__name__}@{record['sha256']}",
                              None if slots else tuple(witness["dict_fields"]), slots))
        seen.add(key)
    if seen != expected:
        raise OwnershipError("object registry class coverage differs")
    bound = object.__new__(SourceRegistry)
    bound.domain = "VERIFIED_SOURCE_PREPARATION"
    bound.source_root = root
    bound.contract_sha256 = spec.contract_sha256
    bound.execution_object_sha256 = object_digest(spec)
    bound._populate(tuple(specs))
    return bound

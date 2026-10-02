"""Verify the new repaired-source candidate without importing any SparkBrain module."""
from __future__ import annotations

import ast
import hashlib
import json
import stat
from pathlib import Path

from scripts.verify_g0_joint_source_contract import (
    class_spec,
    confined_path,
    path_metadata,
    source_root,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "artifacts/research/assembly_m1_path_v1_20261002/source_contract.json"
CONTRACT_SHA256 = "a9f7d5cb19879333b02b3fc8de61127e0bd2399bf033661ef293330669a05301"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root: Path, relative: str, suffix: str) -> dict[str, str]:
    pending = [confined_path(root, relative, "dependency", directory=True)]
    result = {}
    while pending:
        for path in sorted(pending.pop().iterdir()):
            info = path_metadata(path, "dependency")
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
            elif path.name.endswith(suffix):
                name = path.relative_to(root).as_posix()
                result[name] = digest(confined_path(root, name, "dependency"))
    return result


def verify(root: Path = ROOT) -> dict:
    root = source_root(root)
    raw = confined_path(root, CONTRACT, "prospective source contract").read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONTRACT_SHA256:
        raise ValueError("prospective source contract digest changed")
    contract = json.loads(raw)
    if (contract["runtime_execution_authorized"] is not False
            or contract["source_commit"] != "46bbd9b8b28c2404c73f028f8736ed83c3b5c3fe"
            or contract["scientific_credit"] != 0):
        raise ValueError("source-only candidate boundary changed")
    for key, directory, suffix in (("runtime_sources_sha256", "src/sparkbrain", ".py"),
                                   ("runtime_schema_sha256", "schemas", ".json")):
        if inventory(root, directory, suffix) != contract[key]:
            raise ValueError("complete runtime dependency inventory changed")
    for name, sha in contract["preparation_sources_sha256"].items():
        if digest(confined_path(root, name, "preparation input/source")) != sha:
            raise ValueError("preparation input/source changed: " + name)
    witnesses = 0
    for name, row in contract["files"].items():
        path = confined_path(root, name, "class source")
        if digest(path) != row["sha256"]:
            raise ValueError("class source changed")
        classes = {node.name: node for node in ast.parse(path.read_bytes()).body
                   if isinstance(node, ast.ClassDef)}
        for cls, expected in row["classes"].items():
            if cls not in classes or class_spec(classes[cls]) != expected:
                raise ValueError("exact class witness changed")
            if expected["source_hooks"]:
                raise ValueError("unreviewed object hook")
            witnesses += 1
    actual_allocations = {}
    excluded_constructors = []
    enum_initializations = {}
    for name, sha in contract["runtime_sources_sha256"].items():
        path = confined_path(root, name, "allocation source")
        module = name.removeprefix("src/").removesuffix(".py").replace("/", ".")
        module = module.removesuffix(".__init__")
        for node in ast.parse(path.read_bytes()).body:
            if isinstance(node, ast.ClassDef):
                type_name = module + ":" + node.name
                actual_allocations[type_name] = {
                    "path": name, "sha256": sha, "witness": class_spec(node)}
                is_enum = (len(node.bases) == 1 and isinstance(node.bases[0], ast.Name)
                           and node.bases[0].id == "StrEnum")
                if is_enum:
                    enum_initializations[type_name] = sum(
                        len(member.targets) for member in node.body
                        if isinstance(member, ast.Assign))
                if node.bases and not is_enum and not any(
                    isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and member.name == "__init__" for member in node.body
                ):
                    excluded_constructors.append(type_name)
    if actual_allocations != contract["allocation_type_sources"]:
        raise ValueError("complete allocation-type source inventory changed")
    if enum_initializations != contract["import_enum_initializations"]:
        raise ValueError("import enum initializer allowance changed")
    if sorted(excluded_constructors) != contract["excluded_constructor_types"]:
        raise ValueError("excluded constructor scope changed")
    # A repaired allowlist entry is necessary, not a live graph compatibility proof.
    codec = confined_path(root, "src/sparkbrain/v032/checkpoint.py", "codec").read_text()
    if '"sparkbrain.v03_seed.concepts:_MutableConcept"' not in codec:
        raise ValueError("required concept registry repair missing")
    return {"status": "SOURCE_ONLY_CANDIDATE_VERIFIED_NATIVE_BLOCKED",
            "contract_sha256": CONTRACT_SHA256, "class_witnesses": witnesses,
            "runtime_python_files": len(contract["runtime_sources_sha256"]),
            "allocation_type_witnesses": len(actual_allocations),
            "runtime_execution_authorized": False, "scientific_credit": 0,
            "unresolved_gates": contract["unresolved_gates"]}


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True, indent=2))

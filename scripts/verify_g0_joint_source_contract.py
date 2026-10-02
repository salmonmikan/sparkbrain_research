"""Source-only G0 schema audit. Never imports or constructs SparkBrain objects."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "artifacts/research/g0_joint_ownership_preparation_20261002/source_contract.json"
CONTRACT_SHA256 = "281e71fd1bbc11d9d705e6a02524f4071d39573ce0bc36b040da1de40a04e7c8"
COPY_HOOKS = {
    "__copy__", "__deepcopy__", "__reduce__", "__reduce_ex__",
    "__getstate__", "__setstate__", "__del__",
}


def class_spec(node: ast.ClassDef) -> dict[str, Any]:
    """Extract narrow source witnesses, not a whole-program field-completeness proof."""
    decorators = [
        value for value in node.decorator_list
        if isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name) and value.func.id == "dataclass"
    ]
    slots = bool(decorators and any(
        keyword.arg == "slots" and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is True for keyword in decorators[0].keywords
    ))
    if decorators:
        fields = {
            value.target.id for value in node.body
            if isinstance(value, ast.AnnAssign) and isinstance(value.target, ast.Name)
        }
    else:
        fields = {
            value.attr for value in ast.walk(node)
            if isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name)
            and value.value.id == "self" and isinstance(value.ctx, ast.Store)
        }
    hooks = [
        value.name for value in node.body
        if isinstance(value, (ast.FunctionDef, ast.AsyncFunctionDef))
        and value.name in COPY_HOOKS
    ]
    return {
        "dict_fields": [] if slots else sorted(fields),
        "slot_fields": sorted(fields) if slots else [],
        "source_hooks": hooks,
        "start_line": node.lineno,
        "end_line": node.end_lineno,
    }


def verify(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve(strict=True)
    contract_path = (root / CONTRACT).resolve(strict=True)
    if not contract_path.is_relative_to(root):
        raise ValueError("contract escapes root")
    raw = contract_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONTRACT_SHA256:
        raise ValueError("source contract digest mismatch")
    contract = json.loads(raw)
    if contract["runtime_execution_authorized"] is not False or contract["scientific_credit"] != 0:
        raise ValueError("source-only boundary changed")
    for key, directory, pattern in (
        ("runtime_sources_sha256", "src/sparkbrain", "*.py"),
        ("runtime_schema_sha256", "schemas", "*.json"),
    ):
        actual = {}
        component = root
        for name in Path(directory).parts:
            component /= name
            if component.is_symlink():
                raise ValueError("runtime dependency symlink is unsupported")
        if any(item.is_symlink() for item in (root / directory).rglob("*")):
            raise ValueError("runtime dependency symlink is unsupported")
        for item in sorted((root / directory).rglob(pattern)):
            resolved = item.resolve(strict=True)
            if not resolved.is_relative_to(root):
                raise ValueError("runtime dependency escapes root")
            digest = hashlib.sha256(item.read_bytes()).hexdigest()
            actual[item.relative_to(root).as_posix()] = digest
        if actual != contract[key]:
            raise ValueError(f"complete runtime dependency inventory mismatch: {key}")
    for path, expected in contract["reuse_sources_sha256"].items():
        source = (root / path).resolve(strict=True)
        if not source.is_relative_to(root):
            raise ValueError("reuse source escapes root")
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError("reuse source digest mismatch")
    count = 0
    for path, record in contract["files"].items():
        source = (root / path).resolve(strict=True)
        if not source.is_relative_to(root):
            raise ValueError("source escapes root")
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError(f"source digest mismatch: {path}")
        module = ast.parse(data, filename=path)
        for name, expected in record["classes"].items():
            matches = [node for node in module.body if isinstance(node, ast.ClassDef)
                       and node.name == name]
            if len(matches) != 1 or class_spec(matches[0]) != expected:
                raise ValueError(f"source class witness mismatch: {path}:{name}")
            if expected["source_hooks"]:
                raise ValueError("custom source copy hook is not supported")
            count += 1
    return {
        "classification": "SOURCE_ONLY_NON_EVIDENTIARY",
        "status": "SOURCE_BINDINGS_VERIFIED_REAL_G0_NOT_EXECUTED",
        "contract_sha256": CONTRACT_SHA256,
        "source_commit": contract["source_commit"],
        "source_files": len(contract["files"]),
        "class_witnesses": count,
        "runtime_python_files": len(contract["runtime_sources_sha256"]),
        "runtime_schema_files": len(contract["runtime_schema_sha256"]),
        "reuse_source_files": len(contract["reuse_sources_sha256"]),
        "runtime_execution_authorized": False,
        "scientific_credit": 0,
        "limits": "AST witnesses bind selected source bytes; they do not prove live graph coverage",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

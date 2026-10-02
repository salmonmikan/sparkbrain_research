"""Model-free source binding for G0; never imports or constructs SparkBrain.

A successful audit verifies source facts, not snapshot eligibility or execution clearance.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
from typing import Any

CLASSIFICATION = "SOURCE_ONLY_NONCANONICAL_NON_EVIDENTIARY"
PROTOCOL = "artifacts/research/assembly_m1_g0_20261002/source_contract.json"
# Pin the entire logical contract, including its fact inventory and future-case metadata.
CONTRACT_SHA256 = "079605ca4f42f8229d54052ebfe7058da137d98e36cc299f0593ea5031d8e26c"
REQUIRED_BLOCKERS = {
    "producer_oracle_missing_m1_types",
    "facade_lock_and_global_registry",
    "checkpoint_loses_reference_topology",
    "joint_commit_and_rollback_unverified",
}


def canonical(value: Any) -> str:
    return json.dumps(value, allow_nan=False, sort_keys=True, separators=(",", ":"))


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def _finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"nonfinite JSON number: {value}")
    return result


def read_contract(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
        parse_constant=_reject_constant,
        parse_float=_finite_float,
    )
    if not isinstance(value, dict):
        raise ValueError("contract must be a JSON object")
    return value


def resolve_symbol(tree: ast.Module, dotted: str) -> ast.AST:
    current: ast.AST = tree
    for name in dotted.split("."):
        matches = [
            node for node in getattr(current, "body", [])
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == name
        ]
        if len(matches) != 1:
            raise ValueError(f"missing/ambiguous symbol: {dotted}")
        current = matches[0]
    return current


def verify(root: Path, contract: dict[str, Any] | None = None) -> dict[str, Any]:
    root = root.resolve()
    if contract is None:
        contract = read_contract(root / PROTOCOL)
    if set(contract) != {
        "schema", "classification", "scientific_credit", "runtime_execution_authorized",
        "source_commit", "files", "facts", "blockers", "future_case_ids",
    }:
        raise ValueError("unexpected contract fields")
    if (
        type(contract["schema"]) is not int or contract["schema"] != 1
        or contract["classification"] != CLASSIFICATION
        or type(contract["scientific_credit"]) is not int
        or contract["scientific_credit"] != 0
        or contract["runtime_execution_authorized"] is not False
        or set(contract["blockers"]) != REQUIRED_BLOCKERS
    ):
        raise ValueError("invalid source-only/blocked boundary")
    files = contract["files"]
    if not isinstance(files, dict) or not files:
        raise ValueError("missing source inventory")
    trees: dict[str, ast.Module] = {}
    sources: dict[str, str] = {}
    for relative, expected in files.items():
        if not isinstance(relative, str) or not relative.endswith(".py"):
            raise ValueError("invalid source path")
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or path == root:
            raise ValueError("source path escapes checkout")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"source drift: {relative}")
        sources[relative] = data.decode("utf-8")
        trees[relative] = ast.parse(sources[relative], filename=relative)
    facts = []
    seen = set()
    for fact in contract["facts"]:
        if set(fact) != {"id", "path", "symbol", "required_tokens", "interpretation"}:
            raise ValueError("invalid fact fields")
        if fact["id"] in seen or fact["path"] not in trees:
            raise ValueError("duplicate fact or unbound source")
        seen.add(fact["id"])
        node = resolve_symbol(trees[fact["path"]], fact["symbol"])
        segment = ast.get_source_segment(sources[fact["path"]], node)
        if not segment or not all(token in segment for token in fact["required_tokens"]):
            raise ValueError(f"source fact changed: {fact['id']}")
        facts.append({
            "id": fact["id"], "path": fact["path"], "symbol": fact["symbol"],
            "start_line": node.lineno, "end_line": node.end_lineno,
            "interpretation": fact["interpretation"],
        })
    if not facts:
        raise ValueError("missing source facts")
    if hashlib.sha256(canonical(contract).encode()).hexdigest() != CONTRACT_SHA256:
        raise ValueError("source contract differs from the complete pinned inventory")
    return {
        "classification": CLASSIFICATION,
        "scientific_credit": 0,
        "source_binding_verified": True,
        "source_commit": contract["source_commit"],
        "file_count": len(files),
        "facts": facts,
        "g0_status": "BLOCKED_SOURCE_CONTRACT_GAP",
        "runtime_execution_authorized": False,
        "real_model_imports_by_this_auditor": 0,
        "real_model_constructions_by_this_auditor": 0,
        "real_dynamics_calls_by_this_auditor": 0,
        "blockers": contract["blockers"],
        "limitations": (
            "Hashes, AST ranges and literal source tokens are inspected. The commit ID is "
            "declared provenance; this auditor does not query Git. This is not a "
            "whole-program proof, runtime graph inventory, checkpoint certificate or G0 pass."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(canonical(verify(args.root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

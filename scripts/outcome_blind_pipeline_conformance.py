from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from outcome_blind_fixed_scorer import score_preserved_raw
from outcome_blind_raw_generator import generate_raw


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _write_durable(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _verify_hash(path: Path, expected: str) -> None:
    observed = sha256_file(path)
    if observed != expected:
        raise ValueError(f"frozen hash mismatch for {path}: {observed} != {expected}")


def verify_frozen_contract(*, repo_root: Path, contract: dict[str, Any]) -> None:
    for relative_path, expected_sha256 in contract["frozen_sha256"].items():
        _verify_hash(repo_root / relative_path, expected_sha256)
    if contract["synthetic_only"] is not True:
        raise ValueError("contract is not synthetic-only")
    if contract["analysis_choices"]["transform"] != "identity":
        raise ValueError("transform changed")
    if contract["analysis_choices"]["comparator"] != "none":
        raise ValueError("comparator changed")


def run_conformance(
    *,
    repo_root: Path,
    contract_path: Path,
    output_root: Path,
) -> dict[str, Any]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    verify_frozen_contract(repo_root=repo_root, contract=contract)

    fixture_path = repo_root / contract["fixture_path"]
    plan_path = repo_root / contract["analysis_plan_path"]
    staging_raw = output_root / "staging" / "raw.json"

    generate_raw(
        fixture_path=fixture_path,
        output_path=staging_raw,
        seed=contract["runtime"]["seed"],
    )

    raw_bytes = staging_raw.read_bytes()
    raw_sha256 = sha256_bytes(raw_bytes)
    preserve_root = output_root / contract["preserve_namespace"]
    preserved_raw = preserve_root / "raw.json"
    _write_durable(preserved_raw, raw_bytes)

    raw_manifest = {
        "schema_version": 1,
        "stage": "DURABLE_RAW_ONLY_PRESERVE_DIGEST",
        "raw_sha256": raw_sha256,
        "raw_schema_version": contract["raw_schema_version"],
        "contract_generation": contract["contract_generation"],
        "analysis_plan_sha256": contract["frozen_sha256"][contract["analysis_plan_path"]],
        "scorer_sha256": contract["frozen_sha256"][contract["scorer_path"]],
        "synthetic_fixture_sha256": contract["frozen_sha256"][contract["fixture_path"]],
    }
    raw_manifest_path = preserve_root / "raw_manifest.json"
    _write_durable(
        raw_manifest_path,
        (json.dumps(raw_manifest, sort_keys=True, separators=(",", ":")) + "\n").encode(),
    )

    staging_raw.unlink()
    result = score_preserved_raw(
        preserved_raw_path=preserved_raw,
        expected_raw_sha256=raw_sha256,
        plan_path=plan_path,
    )

    scored_manifest = {
        "schema_version": 1,
        "stage": "SCORED_PRESERVE_LINEAGE",
        "contract_generation": contract["contract_generation"],
        "raw_preserve_path": str(preserved_raw.relative_to(output_root)),
        "raw_manifest_path": str(raw_manifest_path.relative_to(output_root)),
        "raw_sha256": raw_sha256,
        "score": result,
        "source_sha256": contract["frozen_sha256"][contract["pipeline_path"]],
        "scorer_sha256": contract["frozen_sha256"][contract["scorer_path"]],
        "workflow_git_blob": contract["workflow_git_blob"],
        "package_git_blob": contract["package_git_blob"],
    }
    scored_path = output_root / contract["scored_preserve_namespace"] / "scored_manifest.json"
    _write_durable(
        scored_path,
        (json.dumps(scored_manifest, sort_keys=True, separators=(",", ":")) + "\n").encode(),
    )

    reopened = json.loads(scored_path.read_text(encoding="utf-8"))
    if reopened["raw_sha256"] != sha256_file(preserved_raw):
        raise ValueError("scored preserve lineage does not bind exact preserved raw")

    return {
        "status": "PASS",
        "raw_sha256": raw_sha256,
        "preserved_raw": str(preserved_raw),
        "raw_manifest": str(raw_manifest_path),
        "scored_manifest": str(scored_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    result = run_conformance(
        repo_root=repo_root,
        contract_path=args.contract,
        output_root=args.output_root,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent structural verifier for preserved Family-B Generation-1 raw evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CANDIDATE_ID = "a01-family-b-distributed-field-trace-gen1-v1"
RAW_SCHEMA = "v061-a01-family-b-gen1-raw-v1"
MANIFEST_SCHEMA = "v061-a01-family-b-gen1-manifest-v1"
NULL_IDS = {
    "explicit_memory": "v061-a01-bgen1-explicit-eligibility-return-address-null-v1",
    "recurrent_trace": "v061-a01-bgen1-resource-matched-recurrent-causal-trace-null-v1",
    "belief_state": "v061-a01-bgen1-explicit-latent-cause-belief-null-v1",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path.name} must be an object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_preserved_raw_bundle(
    root: Path,
    *,
    expected_source_sha: str,
    expected_run_id: str,
    expected_owner_claim: str,
    expected_acquisition_claim: str,
) -> None:
    raw_path = root / "raw.json"
    digest_path = root / "raw.sha256"
    manifest_path = root / "candidate_manifest.json"
    runtime_path = root / "runtime_contract.json"
    metadata_path = root / "_execution_metadata" / "execution_metadata.json"

    for path in (raw_path, digest_path, manifest_path, runtime_path, metadata_path):
        _require(path.is_file(), f"missing preserved artifact: {path.name}")
    _require(not (root / "scored.json").exists(), "raw preserve must predate scoring")

    digest_parts = digest_path.read_text(encoding="utf-8").strip().split()
    _require(len(digest_parts) == 2 and digest_parts[1] == "raw.json", "raw digest format")
    _require(digest_parts[0] == _sha256(raw_path), "raw digest mismatch")

    raw = _load(raw_path)
    manifest = _load(manifest_path)
    metadata = _load(metadata_path)
    runtime = _load(runtime_path)

    _require(raw.get("schema") == RAW_SCHEMA, "raw schema mismatch")
    _require(raw.get("candidate_id") == CANDIDATE_ID, "raw candidate mismatch")
    _require(raw.get("source_sha") == expected_source_sha, "raw source mismatch")
    _require(raw.get("acquisition_claim_sha") == expected_acquisition_claim, "raw claim mismatch")
    _require(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema mismatch")
    _require(manifest.get("candidate_id") == CANDIDATE_ID, "manifest candidate mismatch")
    _require(manifest.get("source_sha") == expected_source_sha, "manifest source mismatch")
    _require(manifest.get("same_identity_rerun_allowed") is False, "manifest rerun drift")
    _require(runtime.get("same_identity_rerun_allowed") is False, "runtime rerun drift")
    _require(runtime.get("execution_admission_required") is True, "runtime admission drift")

    _require(metadata.get("candidate_id") == CANDIDATE_ID, "metadata candidate mismatch")
    _require(
        metadata.get("frozen_source_git_sha") == expected_source_sha,
        "metadata source mismatch",
    )
    _require(metadata.get("workflow_run_id") == expected_run_id, "metadata run mismatch")
    _require(metadata.get("execution_owner_claim_commit") == expected_owner_claim, "owner mismatch")
    _require(
        metadata.get("acquisition_claim_commit") == expected_acquisition_claim,
        "acquire mismatch",
    )
    _require(metadata.get("same_identity_rerun_allowed") is False, "metadata rerun drift")

    candidate = raw.get("candidate")
    nulls = raw.get("nulls")
    _require(isinstance(candidate, dict), "candidate measurement missing")
    _require(isinstance(nulls, dict), "null measurements missing")
    _require(set(nulls) == set(NULL_IDS), "null set mismatch")
    for key, null_id in NULL_IDS.items():
        value = nulls[key]
        _require(isinstance(value, dict), f"null payload missing: {key}")
        _require(value.get("null_id") == null_id, f"null identity mismatch: {key}")

    checks = candidate.get("checks")
    _require(isinstance(checks, dict) and checks, "candidate checks missing")
    _require(
        set(checks)
        == {
            "circulation_external_required",
            "lineage_swap_anonymous_selectivity",
            "contradiction_correction",
            "f_only_transfer",
            "bounded_plurality",
            "dedup_checkpoint",
        },
        "candidate check set drift",
    )
    _require(
        all(isinstance(value, bool) for value in checks.values()),
        "candidate checks must be booleans",
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--expected-source-sha", required=True)
    parser.add_argument("--expected-run-id", required=True)
    parser.add_argument("--expected-owner-claim", required=True)
    parser.add_argument("--expected-acquisition-claim", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    verify_preserved_raw_bundle(
        Path(args.root),
        expected_source_sha=str(args.expected_source_sha),
        expected_run_id=str(args.expected_run_id),
        expected_owner_claim=str(args.expected_owner_claim),
        expected_acquisition_claim=str(args.expected_acquisition_claim),
    )


if __name__ == "__main__":
    main()

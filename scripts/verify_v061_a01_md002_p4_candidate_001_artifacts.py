#!/usr/bin/env python3
"""Independent read-only verifier for A01 MD-002 P4 candidate-001 artifacts.

This verifier intentionally does not import the candidate acquisition or scoring
entrypoints.  It validates only already-materialized artifact structure,
bindings, checksums, and raw trace completeness.  It never writes files and it
cannot acquire or score candidate outcomes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CANDIDATE_ID = "a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1"
CONTRACT_SCHEMA = "v061-a01-md002-p4-selective-resolution-candidate-v2"
RAW_SCHEMA = "v061-a01-md002-p4-selective-resolution-raw-v2"
RUNTIME_SCHEMA = "v061-a01-md002-p4-candidate-runtime-v1"
EXPECTED_PYTHON = "Python 3.11.16"
EXPECTED_EXECUTION_IDS = (
    "p4-separate-confirmation",
    "p4-merged-confirmation",
    "p4-merged-separating-confirmation-a",
    "p4-merged-separating-confirmation-b",
    "p4-merged-separating-contradiction-a",
    "p4-merged-separating-contradiction-b",
    "p4-merged-absence",
    "p4-merged-replay",
)


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _require_git_sha(value: Any, name: str) -> str:
    text = str(value)
    _require(
        len(text) == 40 and all(char in "0123456789abcdef" for char in text),
        f"{name} must be a lowercase 40-character Git SHA",
    )
    return text


def _verify_checksum_manifest(root: Path, relative_path: str) -> None:
    manifest_path = root / relative_path
    _require(manifest_path.is_file(), f"missing checksum manifest: {relative_path}")
    for line in manifest_path.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        _require(len(parts) == 2, f"invalid checksum row in {relative_path}")
        expected, filename = parts
        filename = filename.lstrip("* ")
        candidate = Path(filename)
        _require(
            not candidate.is_absolute() and ".." not in candidate.parts,
            f"unsafe checksum path in {relative_path}: {filename}",
        )
        target = root / candidate
        _require(target.is_file(), f"checksum target missing: {filename}")
        _require(
            _file_sha256(target) == expected,
            f"checksum mismatch: {filename}",
        )


def _verify_contract(contract: Any, expected_source_sha: str) -> dict[str, Any]:
    _require(isinstance(contract, dict), "contract must be an object")
    contract = dict(contract)
    _require(contract.get("schema") == CONTRACT_SCHEMA, "contract schema mismatch")
    _require(contract.get("candidate_id") == CANDIDATE_ID, "contract candidate mismatch")
    _require(contract.get("source_sha") == expected_source_sha, "contract source mismatch")
    digest = contract.get("contract_sha256")
    _require(isinstance(digest, str), "contract digest missing")
    unhashed = dict(contract)
    unhashed.pop("contract_sha256", None)
    _require(_canonical_sha256(unhashed) == digest, "contract digest mismatch")

    prospective = contract.get("prospective_execution_ids")
    _require(isinstance(prospective, dict), "prospective execution map missing")
    _require(set(prospective) == set(EXPECTED_EXECUTION_IDS), "execution ID set mismatch")
    for execution_id in EXPECTED_EXECUTION_IDS:
        _require(
            prospective.get(execution_id) == f"{CANDIDATE_ID}:{execution_id}:once",
            f"prospective identity mismatch: {execution_id}",
        )

    matrix = contract.get("execution_matrix")
    _require(isinstance(matrix, list), "execution matrix missing")
    matrix_ids = [row.get("execution_id") for row in matrix if isinstance(row, dict)]
    _require(
        len(matrix) == len(EXPECTED_EXECUTION_IDS)
        and set(matrix_ids) == set(EXPECTED_EXECUTION_IDS),
        "execution matrix mismatch",
    )
    return contract


def _verify_manifest(root: Path, expected_source_sha: str) -> dict[str, Any]:
    manifest = _read_json(root / "candidate_manifest.json")
    _require(isinstance(manifest, dict), "candidate manifest must be an object")
    _require(manifest.get("candidate_id") == CANDIDATE_ID, "manifest candidate mismatch")
    _require(manifest.get("source_sha") == expected_source_sha, "manifest source mismatch")
    contract = _verify_contract(manifest.get("contract"), expected_source_sha)
    _require(
        manifest.get("contract_sha256") == contract["contract_sha256"],
        "manifest contract digest mismatch",
    )
    return contract


def _verify_runtime(root: Path) -> None:
    runtime = _read_json(root / "runtime_contract.json")
    _require(isinstance(runtime, dict), "runtime contract must be an object")
    _require(runtime.get("schema") == RUNTIME_SCHEMA, "runtime schema mismatch")
    _require(runtime.get("candidate_id") == CANDIDATE_ID, "runtime candidate mismatch")
    _require(runtime.get("python_version") == "3.11.16", "runtime Python mismatch")
    _require(runtime.get("development_only") is True, "runtime must remain development-only")
    _require(runtime.get("held_out_execution_allowed") is False, "held-out execution enabled")
    _require(runtime.get("formal_execution_allowed") is False, "formal execution enabled")
    _require(runtime.get("same_identity_rerun_allowed") is False, "rerun unexpectedly enabled")


def _verify_trace_row(
    row: dict[str, Any],
    contract: dict[str, Any],
    execution_id: str,
) -> None:
    trace = row.get("retained_runtime_trace")
    boundaries = row.get("retained_boundary_events")
    _require(isinstance(trace, list) and trace, f"{execution_id}: retained trace missing")
    _require(isinstance(boundaries, list) and boundaries, f"{execution_id}: boundaries missing")
    trace_digest = row.get("retained_runtime_trace_sha256")
    _require(
        isinstance(trace_digest, str) and _canonical_sha256(trace) == trace_digest,
        f"{execution_id}: retained trace digest mismatch",
    )

    trace_boundaries = [
        item.get("event")
        for item in trace
        if isinstance(item, dict) and item.get("type") == "md002-p4-boundary-event"
    ]
    _require(
        trace_boundaries == boundaries,
        f"{execution_id}: retained boundary coverage mismatch",
    )

    condition_spec = row.get("condition_spec")
    _require(isinstance(condition_spec, dict), f"{execution_id}: condition spec missing")
    if condition_spec.get("boundary_mode") != "merged":
        return

    observation = row.get("merged_ancestry_observation")
    _require(isinstance(observation, dict), f"{execution_id}: merged observation missing")
    _require(
        observation.get("runtime_trace_sha256") == trace_digest,
        f"{execution_id}: observation trace digest mismatch",
    )
    _require(
        observation.get("runtime_trace") == trace,
        f"{execution_id}: observation trace bytes mismatch",
    )
    merged_ids = row.get("merged_source_proposal_ids")
    _require(
        isinstance(merged_ids, list) and len(set(merged_ids)) >= 2,
        f"{execution_id}: merged ancestry is not plural",
    )
    _require(
        set(observation.get("boundary_source_proposal_ids", [])) == set(merged_ids),
        f"{execution_id}: merged ancestry observation mismatch",
    )
    _require(
        len(set(observation.get("active_lineages_before", []))) >= 2,
        f"{execution_id}: active lineage plurality missing before evidence",
    )

    if condition_spec.get("requires_later_separation"):
        selected = row.get("trace_derived_selected_lineage")
        _require(isinstance(selected, dict), f"{execution_id}: trace selection missing")
        proposal_id = selected.get("proposal_id")
        path_map = contract.get("fixture", {}).get("path_map", {})
        _require(proposal_id in path_map, f"{execution_id}: selected proposal not frozen")
        _require(
            selected.get("path_id") == path_map[proposal_id].get("path_id"),
            f"{execution_id}: selected path binding mismatch",
        )
        external = row.get("external_evidence")
        _require(isinstance(external, dict), f"{execution_id}: external evidence missing")
        parents = set(external.get("parent_event_ids", []))
        _require(
            selected.get("parent_boundary_event_id") in parents,
            f"{execution_id}: selected boundary is not an external parent",
        )
        _require(
            selected.get("parent_boundary_event_id")
            in set(row.get("expired_historical_boundary_ids", [])),
            f"{execution_id}: selected historical boundary was not expired",
        )


def _verify_raw(
    root: Path,
    contract: dict[str, Any],
    expected_source_sha: str,
) -> None:
    raw = _read_json(root / "raw.json")
    _require(isinstance(raw, dict), "raw artifact must be an object")
    _require(raw.get("schema") == RAW_SCHEMA, "raw schema mismatch")
    _require(raw.get("candidate_id") == CANDIDATE_ID, "raw candidate mismatch")
    _require(raw.get("source_sha") == expected_source_sha, "raw source mismatch")
    _require(raw.get("contract") == contract, "raw contract differs from manifest")
    _require(
        raw.get("contract_sha256") == contract["contract_sha256"],
        "raw contract digest mismatch",
    )
    observations = raw.get("observations")
    _require(isinstance(observations, list), "raw observations must be a list")
    _require(len(observations) == len(EXPECTED_EXECUTION_IDS), "raw observation count mismatch")
    by_id = {
        str(row.get("condition_id")): row
        for row in observations
        if isinstance(row, dict)
    }
    _require(set(by_id) == set(EXPECTED_EXECUTION_IDS), "raw condition set mismatch")
    _require(len(by_id) == len(observations), "duplicate raw condition ID")

    expected_prospective = contract["prospective_execution_ids"]
    for execution_id in EXPECTED_EXECUTION_IDS:
        row = by_id[execution_id]
        _require(
            row.get("prospective_execution_id") == expected_prospective[execution_id],
            f"{execution_id}: prospective identity mismatch",
        )
        _require(isinstance(row.get("proposal_rows"), list), f"{execution_id}: proposals missing")
        _require(isinstance(row.get("path_map"), dict), f"{execution_id}: path map missing")
        _require(isinstance(row.get("pre"), dict), f"{execution_id}: pre state missing")
        _require(isinstance(row.get("post"), dict), f"{execution_id}: post state missing")
        _require(isinstance(row.get("changed_path_ids"), list), f"{execution_id}: changed paths missing")
        _require(isinstance(row.get("consistency_state"), dict), f"{execution_id}: consistency missing")
        _require(isinstance(row.get("ledger_state"), dict), f"{execution_id}: ledger missing")
        _verify_trace_row(row, contract, execution_id)


def _verify_metadata(
    root: Path,
    expected_source_sha: str,
    expected_run_id: str,
    expected_owner_claim: str,
) -> None:
    metadata = _read_json(root / "_execution_metadata" / "execution_metadata.json")
    _require(isinstance(metadata, dict), "execution metadata must be an object")
    _require(metadata.get("candidate_id") == CANDIDATE_ID, "metadata candidate mismatch")
    _require(metadata.get("frozen_source_git_sha") == expected_source_sha, "metadata source mismatch")
    _require(str(metadata.get("workflow_run_id")) == expected_run_id, "metadata run mismatch")
    _require(
        metadata.get("execution_owner_claim_commit") == expected_owner_claim,
        "metadata owner claim mismatch",
    )
    _require(metadata.get("same_identity_rerun_allowed") is False, "metadata rerun enabled")
    _require(metadata.get("held_out_executed") is False, "metadata says held-out executed")
    _require(metadata.get("formal_execution_allowed") is False, "metadata says formal enabled")
    _require(
        metadata.get("execution_authority_identity")
        == "A01_MD002_USER_AUTHORIZATION_2026-09-12",
        "metadata authority mismatch",
    )


def verify_raw_bundle(
    root: Path,
    *,
    expected_source_sha: str,
    expected_run_id: str,
    expected_owner_claim: str,
) -> None:
    """Fail closed unless an already-preserved raw bundle is complete and bound."""

    _require(root.is_dir(), "artifact root does not exist")
    source_sha = _require_git_sha(expected_source_sha, "expected source SHA")
    _require_git_sha(expected_owner_claim, "expected owner claim")
    _require(expected_run_id.isdigit(), "expected workflow run ID must be numeric")

    required = (
        "candidate_manifest.json",
        "runtime_contract.json",
        "raw.json",
        "raw.sha256",
        "_execution_metadata/binding.sha256",
        "_execution_metadata/python_version.txt",
        "_execution_metadata/source_sha.txt",
        "_execution_metadata/execution_metadata.json",
    )
    for relative in required:
        _require((root / relative).is_file(), f"missing required artifact: {relative}")

    _require(
        (root / "_execution_metadata" / "source_sha.txt").read_text().strip() == source_sha,
        "source SHA file mismatch",
    )
    _require(
        (root / "_execution_metadata" / "python_version.txt").read_text().strip()
        == EXPECTED_PYTHON,
        "Python version file mismatch",
    )
    _verify_checksum_manifest(root, "_execution_metadata/binding.sha256")
    _verify_checksum_manifest(root, "raw.sha256")
    contract = _verify_manifest(root, source_sha)
    _verify_runtime(root)
    _verify_metadata(root, source_sha, expected_run_id, expected_owner_claim)
    _verify_raw(root, contract, source_sha)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--expected-source-sha", required=True)
    parser.add_argument("--expected-run-id", required=True)
    parser.add_argument("--expected-owner-claim", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    verify_raw_bundle(
        Path(args.root),
        expected_source_sha=str(args.expected_source_sha),
        expected_run_id=str(args.expected_run_id),
        expected_owner_claim=str(args.expected_owner_claim),
    )
    print("P4 raw artifact bundle verification: PASS")


if __name__ == "__main__":
    main()

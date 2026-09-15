from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.verify_v061_a01_md002_p4_candidate_001_artifacts import (
    CANDIDATE_ID,
    CONTRACT_SCHEMA,
    EXPECTED_EXECUTION_IDS,
    RAW_SCHEMA,
    RUNTIME_SCHEMA,
    _canonical_sha256,
    verify_raw_bundle,
)

SOURCE_SHA = "1" * 40
OWNER_SHA = "2" * 40
RUN_ID = "123456"


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_bundle(root: Path) -> None:
    path_map = {
        "proposal-a": {"path_id": "path-a", "target": "world:x"},
        "proposal-b": {"path_id": "path-b", "target": "world:y"},
    }
    prospective = {
        execution_id: f"{CANDIDATE_ID}:{execution_id}:once"
        for execution_id in EXPECTED_EXECUTION_IDS
    }
    matrix = [
        {
            "execution_id": execution_id,
            "base_condition_id": execution_id.rsplit("-a", 1)[0].rsplit("-b", 1)[0],
        }
        for execution_id in EXPECTED_EXECUTION_IDS
    ]
    contract = {
        "schema": CONTRACT_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": SOURCE_SHA,
        "prospective_execution_ids": prospective,
        "execution_matrix": matrix,
        "fixture": {"path_map": path_map},
    }
    contract["contract_sha256"] = _canonical_sha256(contract)
    manifest = {
        "candidate_id": CANDIDATE_ID,
        "source_sha": SOURCE_SHA,
        "contract_sha256": contract["contract_sha256"],
        "contract": contract,
    }
    runtime = {
        "schema": RUNTIME_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "python_version": "3.11.16",
        "development_only": True,
        "held_out_execution_allowed": False,
        "formal_execution_allowed": False,
        "same_identity_rerun_allowed": False,
    }

    observations = []
    for execution_id in EXPECTED_EXECUTION_IDS:
        separating = "merged-separating" in execution_id
        merged = execution_id != "p4-separate-confirmation"
        selected_proposal = "proposal-b" if execution_id.endswith("-b") else "proposal-a"
        selected_boundary = f"history-{selected_proposal}"
        boundaries = [
            {
                "event_id": "merged-boundary",
                "source_proposal_ids": ["proposal-a", "proposal-b"],
            }
        ]
        if separating:
            boundaries.insert(
                0,
                {
                    "event_id": selected_boundary,
                    "source_proposal_ids": [selected_proposal],
                },
            )
        trace = [
            {"type": "md002-p4-boundary-event", "event": event}
            for event in boundaries
        ]
        if separating:
            trace.append(
                {"type": "md002-p4-expired-boundary", "event_id": selected_boundary}
            )
        trace.extend(
            [
                {
                    "type": "md002-p4-active-lineages",
                    "phase": "before",
                    "proposal_ids": ["proposal-a", "proposal-b"],
                },
                {
                    "type": "md002-p4-active-lineages",
                    "phase": "after",
                    "proposal_ids": ["proposal-a", "proposal-b"],
                },
            ]
        )
        trace_digest = _canonical_sha256(trace)
        observation = {
            "condition_id": execution_id,
            "prospective_execution_id": prospective[execution_id],
            "condition_spec": {
                "boundary_mode": "merged" if merged else "separate",
                "requires_later_separation": separating,
            },
            "proposal_rows": [
                {"proposal_id": "proposal-a"},
                {"proposal_id": "proposal-b"},
            ],
            "path_map": path_map,
            "retained_boundary_events": boundaries,
            "retained_runtime_trace": trace,
            "retained_runtime_trace_sha256": trace_digest,
            "merged_ancestry_observation": (
                {
                    "boundary_source_proposal_ids": ["proposal-a", "proposal-b"],
                    "active_lineages_before": ["proposal-a", "proposal-b"],
                    "active_lineages_after": ["proposal-a", "proposal-b"],
                    "runtime_trace": trace,
                    "runtime_trace_sha256": trace_digest,
                }
                if merged
                else None
            ),
            "merged_source_proposal_ids": ["proposal-a", "proposal-b"],
            "expired_historical_boundary_ids": [selected_boundary] if separating else [],
            "external_evidence": (
                {"parent_event_ids": ["merged-boundary", selected_boundary]}
                if separating
                else None
            ),
            "trace_derived_selected_lineage": (
                {
                    "parent_boundary_event_id": selected_boundary,
                    "proposal_id": selected_proposal,
                    "path_id": path_map[selected_proposal]["path_id"],
                    "target": path_map[selected_proposal]["target"],
                }
                if separating
                else None
            ),
            "pre": {},
            "post": {},
            "changed_path_ids": [],
            "consistency_state": {},
            "ledger_state": {},
        }
        observations.append(observation)

    raw = {
        "schema": RAW_SCHEMA,
        "candidate_id": CANDIDATE_ID,
        "source_sha": SOURCE_SHA,
        "contract_sha256": contract["contract_sha256"],
        "contract": contract,
        "observations": observations,
    }
    metadata = {
        "candidate_id": CANDIDATE_ID,
        "frozen_source_git_sha": SOURCE_SHA,
        "workflow_run_id": RUN_ID,
        "execution_owner_claim_commit": OWNER_SHA,
        "execution_authority_identity": "A01_MD002_USER_AUTHORIZATION_2026-09-12",
        "same_identity_rerun_allowed": False,
        "held_out_executed": False,
        "formal_execution_allowed": False,
    }

    _write_json(root / "candidate_manifest.json", manifest)
    _write_json(root / "runtime_contract.json", runtime)
    _write_json(root / "raw.json", raw)
    _write_json(root / "_execution_metadata" / "execution_metadata.json", metadata)
    (root / "_execution_metadata" / "python_version.txt").write_text("Python 3.11.16\n")
    (root / "_execution_metadata" / "source_sha.txt").write_text(f"{SOURCE_SHA}\n")
    (root / "raw.sha256").write_text(f"{_sha256(root / 'raw.json')}  raw.json\n")
    binding_names = (
        "candidate_manifest.json",
        "runtime_contract.json",
        "_execution_metadata/python_version.txt",
        "_execution_metadata/source_sha.txt",
    )
    (root / "_execution_metadata" / "binding.sha256").write_text(
        "".join(f"{_sha256(root / name)}  {name}\n" for name in binding_names)
    )


def test_independent_verifier_accepts_complete_bound_raw_bundle(tmp_path: Path) -> None:
    _build_bundle(tmp_path)
    verify_raw_bundle(
        tmp_path,
        expected_source_sha=SOURCE_SHA,
        expected_run_id=RUN_ID,
        expected_owner_claim=OWNER_SHA,
    )


def test_independent_verifier_rejects_trace_digest_tampering(tmp_path: Path) -> None:
    _build_bundle(tmp_path)
    raw_path = tmp_path / "raw.json"
    raw = json.loads(raw_path.read_text())
    raw["observations"][1]["retained_runtime_trace_sha256"] = "0" * 64
    _write_json(raw_path, raw)
    (tmp_path / "raw.sha256").write_text(f"{_sha256(raw_path)}  raw.json\n")

    with pytest.raises(ValueError, match="retained trace digest mismatch"):
        verify_raw_bundle(
            tmp_path,
            expected_source_sha=SOURCE_SHA,
            expected_run_id=RUN_ID,
            expected_owner_claim=OWNER_SHA,
        )

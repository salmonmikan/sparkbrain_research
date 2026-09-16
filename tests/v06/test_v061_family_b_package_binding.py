from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    FAMILY_B_GEN1_PROPOSAL,
    PRE_P4_FAMILY_SOURCE_SHA,
)
from sparkbrain.evaluation.v061_family_b_readiness import (
    EXPECTED_BELIEF_STATE_NULL_ID,
    EXPECTED_PROPOSAL_SPECIFICATION_HASH,
)

ROOT = Path(__file__).resolve().parents[2]
BINDING_PATH = ROOT / "docs" / "V061_A01_FAMILY_B_GEN1_PACKAGE_BINDING.json"
EXPECTED_IMPLEMENTATION_HEAD_SHA = "421145d60645b2f3b0d4c46c69ef314a9fc4de74"
EXPECTED_PROTOCOL_BUNDLE_SOURCE_STAGE = "post-p4-generation1-contract"
EXPECTED_SOURCE_PATHS = frozenset(
    {
        "src/sparkbrain/evaluation/v061_family_b_distributed_field_trace.py",
        "src/sparkbrain/evaluation/v061_family_b_readiness.py",
        "src/sparkbrain/evaluation/v061_family_b_readiness_harness.py",
    }
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content, usedforsecurity=False).hexdigest()


def test_family_b_package_binding_matches_exact_source_contract_and_input_bytes() -> None:
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    source_path = ROOT / binding["mechanism_source_path"]
    contract_path = ROOT / binding["mechanism_contract_path"]
    input_path = ROOT / binding["readiness_input_path"]

    assert binding["proposal_id"] == FAMILY_B_GEN1_PROPOSAL.proposal_id
    assert (
        binding["proposal_specification_sha256"]
        == EXPECTED_PROPOSAL_SPECIFICATION_HASH
    )
    assert (
        binding["protocol_bundle_source_sha"]
        == FAMILY_B_GEN1_PROPOSAL.protocol_bundle_source_sha
    )
    assert (
        binding["protocol_bundle_source_stage"]
        == EXPECTED_PROTOCOL_BUNDLE_SOURCE_STAGE
    )
    assert binding["pre_p4_family_source_sha"] == PRE_P4_FAMILY_SOURCE_SHA
    assert binding["implementation_head_sha"] == EXPECTED_IMPLEMENTATION_HEAD_SHA
    assert binding["belief_state_null_id"] == EXPECTED_BELIEF_STATE_NULL_ID
    assert _sha256(source_path) == binding["mechanism_source_sha256"]
    assert _sha256(contract_path) == binding["mechanism_contract_sha256"]
    assert _git_blob_sha(contract_path) == binding["mechanism_contract_git_blob"]
    assert _sha256(input_path) == binding["readiness_input_sha256"]
    assert _git_blob_sha(input_path) == binding["readiness_input_git_blob"]
    assert binding["readiness_input_id"] == "v061-a01-bgen1-readiness-input-v1"
    assert binding["execution_admitted"] is False

    source_blobs = binding["source_git_blobs"]
    assert frozenset(source_blobs) == EXPECTED_SOURCE_PATHS
    for relative_path, expected_blob in source_blobs.items():
        assert _git_blob_sha(ROOT / relative_path) == expected_blob

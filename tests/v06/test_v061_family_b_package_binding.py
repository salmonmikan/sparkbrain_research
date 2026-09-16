from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    FAMILY_B_GEN1_PROPOSAL,
)
from sparkbrain.evaluation.v061_family_b_readiness import (
    EXPECTED_PROPOSAL_SPECIFICATION_HASH,
)

ROOT = Path(__file__).resolve().parents[2]
BINDING_PATH = ROOT / "docs" / "V061_A01_FAMILY_B_GEN1_PACKAGE_BINDING.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content, usedforsecurity=False).hexdigest()


def test_family_b_package_binding_matches_exact_source_and_input_bytes() -> None:
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    source_path = ROOT / binding["mechanism_source_path"]
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
    assert _sha256(source_path) == binding["mechanism_source_sha256"]
    assert _sha256(input_path) == binding["readiness_input_sha256"]
    assert _git_blob_sha(input_path) == binding["readiness_input_git_blob"]
    assert binding["readiness_input_id"] == "v061-a01-bgen1-readiness-input-v1"
    assert binding["execution_admitted"] is False

    source_blobs = binding["source_git_blobs"]
    assert source_blobs
    for relative_path, expected_blob in source_blobs.items():
        assert _git_blob_sha(ROOT / relative_path) == expected_blob

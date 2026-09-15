from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_p4_candidate_v3_manifest_preflight_is_counterbalanced(tmp_path: Path) -> None:
    output = tmp_path / "manifest.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_v061_a01_md002_p4_candidate_001_v3.py",
            "manifest",
            "--source-sha",
            "0" * 40,
            "--output",
            str(output),
        ],
        check=True,
    )
    manifest = json.loads(output.read_text())
    contract = manifest["contract"]
    assert manifest["candidate_id"] == (
        "a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1"
    )
    assert contract["schema"] == (
        "v061-a01-md002-p4-selective-resolution-candidate-v2"
    )
    assert contract["classifier"]["version"] == (
        "p4-selective-resolution-development-classifier-v2"
    )
    assert set(contract["prospective_execution_ids"]) == {
        "p4-separate-confirmation",
        "p4-merged-confirmation",
        "p4-merged-separating-confirmation-a",
        "p4-merged-separating-confirmation-b",
        "p4-merged-separating-contradiction-a",
        "p4-merged-separating-contradiction-b",
        "p4-merged-absence",
        "p4-merged-replay",
    }
    separating = {
        (row["evidence_sign"], row["selected_lineage_arm"])
        for row in contract["execution_matrix"]
        if row["selected_lineage_arm"] is not None
    }
    assert separating == {
        ("confirmation", "a"),
        ("confirmation", "b"),
        ("contradiction", "a"),
        ("contradiction", "b"),
    }
    assert contract["same_identity_rerun_allowed"] is False
    assert contract["formal_execution_allowed"] is False
    assert contract["held_out_execution_allowed"] is False
    assert "classification" not in manifest


def test_p4_candidate_v3_contract_binds_trace_and_strict_ttl(tmp_path: Path) -> None:
    output = tmp_path / "manifest.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_v061_a01_md002_p4_candidate_001_v3.py",
            "manifest",
            "--source-sha",
            "f" * 40,
            "--output",
            str(output),
        ],
        check=True,
    )
    contract = json.loads(output.read_text())["contract"]
    binding = contract["retained_trace_binding"]
    assert "complete retained runtime trace" in binding["digest"]
    assert "ProvenanceLedger" in binding["active_lineage_source"]
    assert "strictly greater" in contract["ttl_rule"]

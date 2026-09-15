from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_p4_candidate_manifest_preflight_does_not_execute_candidate(tmp_path: Path) -> None:
    output = tmp_path / "manifest.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_v061_a01_md002_p4_candidate_001.py",
            "manifest",
            "--source-sha",
            "0" * 40,
            "--output",
            str(output),
        ],
        check=True,
    )
    manifest = json.loads(output.read_text())
    assert (
        manifest["candidate_id"]
        == "a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1"
    )
    contract = manifest["contract"]
    assert contract["development_only"] is True
    assert contract["formal_execution_allowed"] is False
    assert contract["held_out_execution_allowed"] is False
    assert contract["same_identity_rerun_allowed"] is False
    assert tuple(contract["prospective_execution_ids"]) == (
        "p4-separate-confirmation",
        "p4-merged-confirmation",
        "p4-merged-separating-confirmation",
        "p4-merged-separating-contradiction",
        "p4-merged-absence",
        "p4-merged-replay",
    )
    assert contract["classifier"]["version"] == (
        "p4-selective-resolution-development-classifier-v1"
    )
    assert "classification" not in manifest

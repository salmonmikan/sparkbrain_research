from __future__ import annotations

import subprocess
import sys


def test_superseded_p4_entrypoint_cannot_acquire_or_manifest() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_v061_a01_md002_p4_candidate_001.py",
            "manifest",
            "--source-sha",
            "0" * 40,
            "--output",
            "/tmp/should-not-exist.json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "superseded pre-STARTED P4 entrypoint" in (
        result.stdout + result.stderr
    )

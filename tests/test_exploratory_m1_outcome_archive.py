from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "artifacts/exploratory/m1-outcome-identity-20261001T1458Z"
)


def test_retained_m1_archive_without_runtime_execution() -> None:
    spec = importlib.util.spec_from_file_location(
        "m1_publication_archive_verifier", ARTIFACT / "verify_bundle.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.verify(ARTIFACT)
    assert result["archive_files_verified"] == 3319
    assert result["readable_copies_verified"] == 43
    assert result["physical_checkpoint_payload_comparisons"] == 2304
    assert result["corrected_cases_independently_recomputed"] == 16
    assert result["total_public_api_attempts"] == 192
    assert result["byte_identical_corrected_non_environment_files"] == 972
    assert result["scientific_credit"] == 0
    assert result["runtime_executed_by_verifier"] is False


def test_publication_verifier_rejects_corrupted_retained_data() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_verify_bundle"],
        cwd=ARTIFACT,
        check=True,
        capture_output=True,
        text=True,
    )

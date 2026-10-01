"""Data-only archive checks; never run the M1 diagnostic from CI."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "scripts/verify_m1_cold_resume_artifacts.py"
SPEC = importlib.util.spec_from_file_location("verify_m1_cold_resume_artifacts", SOURCE)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def test_retained_results_recalculate_without_runtime_execution() -> None:
    result = TOOL.verify(TOOL.DEFAULT)
    assert result["total_primary_commits"] == 198
    assert result["resumed_transitions"] == 96
    assert result["scientific_credit"] == 0


def test_transport_tampering_is_rejected(tmp_path: Path) -> None:
    source = TOOL.DEFAULT / "corrected.parts"
    dest = tmp_path / "parts"
    shutil.copytree(source, dest)
    part = dest / "part-000.b64"
    part.write_bytes(part.read_bytes() + b"A")
    with pytest.raises(ValueError, match="digest mismatch"):
        TOOL.read_bundle(dest)


def test_optimized_python_cannot_silently_disable_verification() -> None:
    result = subprocess.run([sys.executable, "-O", str(SOURCE)],
                            capture_output=True, text=True, check=False)
    assert result.returncode != 0
    assert "requires Python without -O" in result.stderr

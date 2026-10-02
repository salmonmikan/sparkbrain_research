"""Byte-level failure preservation checks; no experiment, model or baseline evaluation."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "failure_bytes", ROOT / "scripts/verify_retention_preflight_failure.py"
)
assert SPEC and SPEC.loader
TOOL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)


def test_preserved_failure_and_sources_repack_exactly():
    report = TOOL.verify(TOOL.ARTIFACT)
    assert report["archive_files"] == 204
    assert report["source_files_verified"] == 193
    assert report["canonical_repack_matches"] is True
    assert report["runtime_model_method_calls"] == 0


@pytest.mark.parametrize("path", ["result.json", "evidence.part000.b64", "independent_audit.json"])
def test_changed_preserved_evidence_rejects(tmp_path, path):
    target = tmp_path / "evidence"
    shutil.copytree(TOOL.ARTIFACT, target)
    selected = target / path
    selected.write_bytes(selected.read_bytes() + b" ")
    with pytest.raises(RuntimeError):
        TOOL.verify(target)

"""Pinned publication checks only: no producer or scientific runner imports."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_v05_owned_state_evidence", ROOT / "scripts/verify_v05_owned_state_evidence.py"
)
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def materialize(tmp_path):
    for name in ("transport_manifest.json", "evidence-000.b64", "evidence-001.b64"):
        shutil.copyfile(VERIFY.ARTIFACT / name, tmp_path / name)
    return tmp_path


def test_published_negative_boundary():
    result = VERIFY.verify()
    assert result["status"] == "verified_coverage_block"
    assert result["raw_files"] == 47 and result["graph_files"] == 16
    assert result["prefix_patterns"] == result["prefix_candidates"] == 0
    assert result["model_execution"] is False


def test_reject_corrupt_part(tmp_path):
    root = materialize(tmp_path)
    with (root / "evidence-000.b64").open("ab") as stream:
        stream.write(b"bad")
    with pytest.raises(ValueError, match="part hash/size"):
        VERIFY.verify(root)


def test_reject_archive_rebinding(tmp_path):
    root = materialize(tmp_path)
    path = root / "transport_manifest.json"
    data = json.loads(path.read_text())
    data["archive_sha256"] = "0" * 64
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="original archive"):
        VERIFY.verify(root)


def test_reject_part_path_escape(tmp_path):
    root = materialize(tmp_path)
    path = root / "transport_manifest.json"
    data = json.loads(path.read_text())
    data["parts"][0]["path"] = "../elsewhere"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="transport parts"):
        VERIFY.verify(root)

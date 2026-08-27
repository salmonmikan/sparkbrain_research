from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sparkbrain.release_candidate import (
    CANDIDATE_MANIFEST_SCHEMA,
    build_canonical_reproduction_manifest,
    validate_canonical_reproduction_manifest,
    validate_network_client_boundary,
)


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def fixture(root: Path) -> str:
    (root / "src" / "sparkbrain").mkdir(parents=True)
    (root / "src" / "sparkbrain" / "runtime.py").write_text("import json\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "result.md").write_text("evidence\n", encoding="utf-8")
    git(root, "init", "--quiet")
    git(root, "config", "user.name", "fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "add", "--all")
    git(root, "commit", "--quiet", "-m", "fixture")
    return git(root, "rev-parse", "HEAD")


def test_manifest_uses_real_commit_and_rejects_bool_and_payload_drift(tmp_path: Path) -> None:
    revision = fixture(tmp_path)
    manifest = build_canonical_reproduction_manifest(
        tmp_path, source_revision=revision, paths=["docs/result.md"]
    )
    assert manifest["schema_version"] == CANDIDATE_MANIFEST_SCHEMA
    assert validate_canonical_reproduction_manifest(tmp_path, manifest) == []
    manifest["file_count"] = True
    manifest["total_bytes"] = False
    manifest["files"][0]["size"] = True
    problems = validate_canonical_reproduction_manifest(tmp_path, manifest)
    assert "candidate manifest file_count mismatch" in problems
    assert "candidate manifest total_bytes mismatch" in problems
    assert any("size must be" in problem for problem in problems)


@pytest.mark.parametrize("source", ["import httpx\n", "__import__('socket')\n"])
def test_network_boundary_scans_package_and_fails_closed(tmp_path: Path, source: str) -> None:
    fixture(tmp_path)
    (tmp_path / "src" / "sparkbrain" / "runtime.py").write_text(source, encoding="utf-8")
    assert validate_network_client_boundary(tmp_path)

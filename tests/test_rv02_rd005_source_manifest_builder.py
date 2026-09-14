from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import scripts.build_rv02_rd005_source_manifest as builder
import sparkbrain.research.rv02_rd005_development_package as package


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "rd005-test@example.invalid")
    _git(repo, "config", "user.name", "RD005 Test")
    (repo / "source.txt").write_text("source\n", encoding="utf-8")
    (repo / "builder.txt").write_text("builder\n", encoding="utf-8")
    _git(repo, "add", "source.txt", "builder.txt")
    _git(repo, "commit", "-m", "fixture")
    return repo


def _patch_required_paths(
    monkeypatch: pytest.MonkeyPatch,
    paths: set[str],
) -> None:
    required = frozenset(paths)
    monkeypatch.setattr(builder, "RD005_REQUIRED_SOURCE_PATHS", required)
    monkeypatch.setattr(package, "RD005_REQUIRED_SOURCE_PATHS", required)


def test_builder_binds_exact_clean_head_and_all_declared_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = _init_repo(tmp_path)
    _patch_required_paths(monkeypatch, {"source.txt"})
    monkeypatch.setattr(builder, "_EXTRA_PROVENANCE_PATHS", frozenset({"builder.txt"}))

    manifest = builder.build_source_manifest(repo)

    assert manifest.source_git_sha == _git(repo, "rev-parse", "HEAD")
    assert {entry.path for entry in manifest.entries} == {"source.txt", "builder.txt"}
    assert len(manifest.manifest_sha256) == 64


def test_builder_rejects_modified_tracked_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = _init_repo(tmp_path)
    _patch_required_paths(monkeypatch, {"source.txt"})
    monkeypatch.setattr(builder, "_EXTRA_PROVENANCE_PATHS", frozenset({"builder.txt"}))
    (repo / "source.txt").write_text("changed\n", encoding="utf-8")

    with pytest.raises(ValueError, match="clean tracked checkout"):
        builder.build_source_manifest(repo)


def test_builder_rejects_nested_path_as_repository_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = _init_repo(tmp_path)
    nested = repo / "nested"
    nested.mkdir()
    _patch_required_paths(monkeypatch, {"source.txt"})
    monkeypatch.setattr(builder, "_EXTRA_PROVENANCE_PATHS", frozenset({"builder.txt"}))

    with pytest.raises(ValueError, match="Git top-level"):
        builder.build_source_manifest(nested)


def test_builder_rejects_missing_bound_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = _init_repo(tmp_path)
    _patch_required_paths(monkeypatch, {"source.txt", "missing.txt"})
    monkeypatch.setattr(builder, "_EXTRA_PROVENANCE_PATHS", frozenset({"builder.txt"}))

    with pytest.raises(ValueError, match="source path is missing"):
        builder.build_source_manifest(repo)

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from sparkbrain.research.rv01_r01_16_development_package import (
    R01_16_REQUIRED_SOURCE_PATHS,
    R0116SourceManifest,
    R0116SourceManifestEntry,
)
from sparkbrain.research.rv01_r01_16_source_binding import (
    verify_r01_16_source_checkout,
)

SOURCE_BINDING_PATH = "src/sparkbrain/research/rv01_r01_16_source_binding.py"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _fixture_repo(tmp_path: Path) -> tuple[Path, R0116SourceManifest]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "fixture")
    _git(root, "config", "user.email", "fixture@example.invalid")

    paths = sorted(R01_16_REQUIRED_SOURCE_PATHS | {SOURCE_BINDING_PATH})
    for path in paths:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"fixture bytes for {path}\n", encoding="utf-8")

    _git(root, "add", "--all")
    _git(root, "commit", "--quiet", "-m", "fixture source")
    source_sha = _git(root, "rev-parse", "HEAD")
    manifest = R0116SourceManifest(
        source_git_sha=source_sha,
        entries=tuple(
            R0116SourceManifestEntry(
                path=path,
                sha256=hashlib.sha256((root / path).read_bytes()).hexdigest(),
            )
            for path in paths
        ),
    )
    return root, manifest


def test_r01_16_source_checkout_verifies_exact_clean_git_and_file_bytes(
    tmp_path: Path,
) -> None:
    root, manifest = _fixture_repo(tmp_path)

    verified = verify_r01_16_source_checkout(root, manifest)

    assert verified.source_git_sha == manifest.source_git_sha
    assert verified.source_manifest_sha256 == manifest.manifest_sha256
    assert verified.verified_paths == tuple(sorted(row.path for row in manifest.entries))
    assert verified.state_dict()["execution_authority_granted"] is False


def test_r01_16_source_checkout_rejects_wrong_git_identity(tmp_path: Path) -> None:
    root, manifest = _fixture_repo(tmp_path)

    with pytest.raises(ValueError, match="source Git SHA mismatch"):
        verify_r01_16_source_checkout(
            root,
            replace(manifest, source_git_sha="a" * 40),
        )


def test_r01_16_source_checkout_rejects_modified_tracked_source(tmp_path: Path) -> None:
    root, manifest = _fixture_repo(tmp_path)
    target = root / sorted(R01_16_REQUIRED_SOURCE_PATHS)[0]
    target.write_text("tampered after manifest\n", encoding="utf-8")

    with pytest.raises(ValueError, match="modified tracked files"):
        verify_r01_16_source_checkout(root, manifest)


def test_r01_16_source_checkout_requires_verifier_itself_in_manifest(
    tmp_path: Path,
) -> None:
    root, manifest = _fixture_repo(tmp_path)
    without_verifier = replace(
        manifest,
        entries=tuple(row for row in manifest.entries if row.path != SOURCE_BINDING_PATH),
    )

    with pytest.raises(ValueError, match="bind the source verifier itself"):
        verify_r01_16_source_checkout(root, without_verifier)

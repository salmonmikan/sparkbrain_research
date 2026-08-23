from __future__ import annotations

import json
import subprocess
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from sparkbrain import release

REVISION = "a" * 40


def _write_archive_fixture(root: Path) -> dict[str, object]:
    (root / "docs").mkdir(parents=True)
    (root / "docs/result.md").write_text("evidence\n", encoding="utf-8")
    (root / "pyproject.toml").write_text(
        '[project]\nname = "fixture"\nversion = "1.2.3"\n', encoding="utf-8"
    )
    manifest = release.build_release_manifest(
        root,
        generated_at="2026-08-24T00:00:00+00:00",
        source_revision=REVISION,
        paths=["docs/result.md", "pyproject.toml"],
    )
    release.write_release_manifest(root / release.MANIFEST_PATH, manifest)
    metadata = release.build_release_metadata(root, root / release.MANIFEST_PATH)
    release.write_release_metadata(root / release.RELEASE_METADATA_PATH, metadata)
    return manifest


def _write_revision_artifacts(root: Path, revision: str) -> None:
    release_dir = root / "artifacts/release"
    release_dir.mkdir(parents=True, exist_ok=True)
    (release_dir / "evidence_map.json").write_text(
        json.dumps({"source_revision": revision}), encoding="utf-8"
    )
    (release_dir / "provenance.json").write_text(
        json.dumps({"source_revision": revision}), encoding="utf-8"
    )


def test_archive_mode_uses_metadata_and_never_calls_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = _write_archive_fixture(tmp_path)

    def forbidden_git(*args: object, **kwargs: object) -> object:
        raise AssertionError("archive mode called Git")

    monkeypatch.setattr(release.subprocess, "run", forbidden_git)
    assert release.release_mode(tmp_path) == "archive"
    assert release.source_revision(tmp_path) == REVISION
    assert release.tracked_release_paths(tmp_path) == ["docs/result.md", "pyproject.toml"]
    assert release.validate_source_revision(
        tmp_path, {"source_revision": REVISION}, label="fixture"
    ) == []
    assert release.verify_release_manifest(
        tmp_path, manifest, require_complete_tracked_tree=True
    ) == []


def test_archive_manifest_copy_detects_omitted_bound_path(tmp_path: Path) -> None:
    manifest = _write_archive_fixture(tmp_path)
    manifest["files"] = manifest["files"][1:]
    problems = release.verify_release_manifest(
        tmp_path, manifest, require_complete_tracked_tree=True
    )
    assert any(problem.startswith("release manifest omits archive files:") for problem in problems)


def test_archive_mode_rejects_missing_or_malformed_metadata(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "fixture"\nversion = "1.2.3"\n', encoding="utf-8"
    )
    with pytest.raises(RuntimeError, match="archive source revision unavailable"):
        release.source_revision(tmp_path)
    (tmp_path / release.RELEASE_METADATA_PATH).write_text(
        json.dumps({"source_revision": "not-a-revision"}), encoding="utf-8"
    )
    with pytest.raises(RuntimeError, match="full lowercase Git SHA"):
        release.source_revision(tmp_path)


def test_release_metadata_binds_manifest_hash_count_version_and_revision(
    tmp_path: Path,
) -> None:
    _write_archive_fixture(tmp_path)
    metadata_path = tmp_path / release.RELEASE_METADATA_PATH
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["manifest_sha256"] = "0" * 64
    metadata["file_count"] = 999
    metadata["package_version"] = "9.9.9"
    metadata["source_revision"] = "b" * 40
    release.write_release_metadata(metadata_path, metadata)
    problems = release.validate_release_metadata(tmp_path)
    assert "release metadata manifest_sha256 does not match PACKAGE_MANIFEST.json" in problems
    assert "release metadata file_count does not match PACKAGE_MANIFEST.json" in problems
    assert "release metadata package_version does not match pyproject.toml" in problems
    assert "release metadata source_revision does not match PACKAGE_MANIFEST.json" in problems


def test_archive_completeness_rejects_missing_unexpected_cache_and_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = _write_archive_fixture(tmp_path)
    (tmp_path / "docs/result.md").unlink()
    (tmp_path / "unexpected.txt").write_text("unexpected", encoding="utf-8")
    cache = tmp_path / "pkg/__pycache__"
    cache.mkdir(parents=True)
    (cache / "module.pyc").write_bytes(b"cache")
    (tmp_path / "data/external").mkdir(parents=True)
    original_tree = release._archive_tree_paths

    def tree_with_symlink(root: Path) -> tuple[set[str], list[str]]:
        paths, problems = original_tree(root)
        return paths, [*problems, "archive tree contains symlink: docs/link.md"]

    monkeypatch.setattr(release, "_archive_tree_paths", tree_with_symlink)
    problems = release.verify_release_manifest(
        tmp_path, manifest, require_complete_tracked_tree=True
    )
    assert "missing or non-regular release file: docs/result.md" in problems
    assert any("archive tree contains forbidden paths:" in problem for problem in problems)
    assert "archive tree contains forbidden directory: data/external" in problems
    assert any("archive tree is missing manifest files:" in problem for problem in problems)
    assert any("archive tree contains unexpected files:" in problem for problem in problems)
    assert "archive tree contains symlink: docs/link.md" in problems


def test_release_revision_consistency_rejects_cross_file_mismatch(tmp_path: Path) -> None:
    _write_archive_fixture(tmp_path)
    _write_revision_artifacts(tmp_path, "b" * 40)
    problems = release.validate_release_revision_consistency(tmp_path)
    assert any(
        problem.startswith("release source_revision values do not match:")
        for problem in problems
    )
    assert release.validate_source_revision(
        tmp_path, {"source_revision": "b" * 40}, label="evidence map"
    ) == ["evidence map source_revision does not match release metadata"]


def test_repository_mode_keeps_git_ancestry_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".git").write_text("gitdir: fixture", encoding="utf-8")
    calls: list[list[str]] = []

    def fake_run(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        return SimpleNamespace(returncode=1, stdout="", stderr="not an ancestor")

    monkeypatch.setattr(release.subprocess, "run", fake_run)
    assert release.release_mode(tmp_path) == "repository"
    assert release.validate_source_revision(
        tmp_path, {"source_revision": REVISION}, label="fixture"
    ) == ["fixture source_revision is not an ancestor of HEAD"]
    assert calls == [["git", "merge-base", "--is-ancestor", REVISION, "HEAD"]]


def test_repository_git_failure_is_reported_without_traceback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".git").mkdir()

    def missing_git(*args: object, **kwargs: object) -> object:
        raise FileNotFoundError("git executable missing")

    monkeypatch.setattr(release.subprocess, "run", missing_git)
    problems = release.validate_source_revision(
        tmp_path, {"source_revision": REVISION}, label="fixture"
    )
    assert problems == [
        "fixture source_revision ancestry check failed: git executable missing"
    ]


def test_repository_completeness_failure_is_a_problem_not_an_exception(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "tracked.txt").write_text("tracked", encoding="utf-8")
    manifest = release.build_release_manifest(
        tmp_path,
        generated_at="fixed",
        source_revision=REVISION,
        paths=["tracked.txt"],
    )

    def failed_git(*args: object, **kwargs: object) -> object:
        raise subprocess.CalledProcessError(128, ["git", "ls-files"])

    monkeypatch.setattr(release.subprocess, "run", failed_git)
    problems = release.verify_release_manifest(
        tmp_path, manifest, require_complete_tracked_tree=True
    )
    assert len(problems) == 1
    assert problems[0].startswith("repository release completeness check failed:")


def test_release_archive_includes_hash_binding_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_archive_fixture(tmp_path)
    monkeypatch.setattr(release, "project_license_selected", lambda root: True)
    monkeypatch.setattr(release, "validate_release_tree", lambda root, require_public=True: [])
    output = tmp_path.parent / f"{tmp_path.name}-release.zip"
    result = release.build_release_archive(
        tmp_path, output, source_date_epoch=1_700_000_000
    )
    try:
        with zipfile.ZipFile(output) as archive:
            assert release.MANIFEST_PATH in archive.namelist()
            assert release.RELEASE_METADATA_PATH in archive.namelist()
        assert result["archive"] == str(output)
    finally:
        output.unlink(missing_ok=True)
        output.with_suffix(output.suffix + ".sha256").unlink(missing_ok=True)

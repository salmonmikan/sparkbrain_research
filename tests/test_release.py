from __future__ import annotations

from pathlib import Path

from sparkbrain.release import (
    build_release_manifest,
    project_license_selected,
    verify_release_manifest,
)


def test_release_manifest_is_stable_and_detects_tampering(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "result.md").write_text("evidence\n", encoding="utf-8")
    manifest = build_release_manifest(
        tmp_path,
        generated_at="2026-08-23T00:00:00+00:00",
        source_revision="a" * 40,
        paths=["docs/result.md", "PACKAGE_MANIFEST.json"],
    )

    assert manifest["file_count"] == 1
    assert manifest["files"][0]["path"] == "docs/result.md"
    assert verify_release_manifest(tmp_path, manifest) == []

    (tmp_path / "docs" / "result.md").write_text("changed\n", encoding="utf-8")
    problems = verify_release_manifest(tmp_path, manifest)
    assert "size mismatch: docs/result.md" in problems
    assert "sha256 mismatch: docs/result.md" in problems


def test_release_manifest_rejects_parent_traversal(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("not in release", encoding="utf-8")
    try:
        build_release_manifest(
            tmp_path,
            generated_at="fixed",
            source_revision="fixed",
            paths=["../outside.txt"],
        )
    except ValueError as exc:
        assert "unsafe release path" in str(exc)
    else:
        raise AssertionError("parent traversal was accepted")


def test_unselected_project_license_blocks_release(tmp_path: Path) -> None:
    (tmp_path / "LICENSE_NOT_SELECTED.md").write_text("pending", encoding="utf-8")
    assert not project_license_selected(tmp_path)
    (tmp_path / "LICENSE_NOT_SELECTED.md").unlink()
    (tmp_path / "LICENSE").write_text("selected by owner", encoding="utf-8")
    assert project_license_selected(tmp_path)

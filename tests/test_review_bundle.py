from __future__ import annotations

import hashlib
import json
import stat
import warnings
import zipfile
from pathlib import Path

import pytest

from scripts.build_review_bundle import (
    ARCHIVE_ROOT,
    PRIVATE_NOTICE,
    RELEASE_METADATA,
    REVIEW_MANIFEST,
    SOURCE_MANIFEST,
    build_review_bundle,
    validate_review_bundle,
)

SOURCE_EPOCH = 1_700_000_000
NESTED_RELEASE = "archive/v0.2/sparkbrain_research_v0_2.zip"


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _make_root(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    (root / "docs").mkdir(parents=True)
    (root / "archive/v0.2").mkdir(parents=True)
    (root / "docs/result.md").write_text("evidence\n", encoding="utf-8")
    (root / "docs/日本語.md").write_text("再現可能\n", encoding="utf-8")
    (root / NESTED_RELEASE).write_bytes(b"old nested release")
    (root / "pyproject.toml").write_text(
        '[project]\nname = "sparkbrain-research"\nversion = "0.2.1"\n',
        encoding="utf-8",
    )
    rows = []
    for relative, artifact_class in (
        (NESTED_RELEASE, "package-metadata"),
        ("docs/result.md", "documentation"),
        ("docs/日本語.md", "documentation"),
        ("pyproject.toml", "package-metadata"),
    ):
        content = (root / relative).read_bytes()
        rows.append(
            {
                "path": relative,
                "size": len(content),
                "sha256": _sha256(content),
                "artifact_class": artifact_class,
            }
        )
    manifest = {
        "manifest_schema_version": "3",
        "source_revision": "a" * 40,
        "file_count": len(rows),
        "files": rows,
    }
    (root / SOURCE_MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    source_bytes = (root / SOURCE_MANIFEST).read_bytes()
    (root / RELEASE_METADATA).write_text(
        json.dumps(
            {
                "release_metadata_schema_version": "1",
                "source_revision": "a" * 40,
                "generated_at": "2026-08-24T00:00:00+00:00",
                "package_version": "0.2.1",
                "manifest_sha256": _sha256(source_bytes),
                "file_count": len(rows),
            }
        ),
        encoding="utf-8",
    )
    return root


def _rewrite_entry(path: Path, target: str, replacement: bytes) -> None:
    rewritten = path.with_suffix(".rewritten.zip")
    with (
        zipfile.ZipFile(path) as source,
        zipfile.ZipFile(rewritten, "w", compression=zipfile.ZIP_DEFLATED) as destination,
    ):
        for info in source.infolist():
            content = replacement if info.filename == target else source.read(info.filename)
            destination.writestr(info, content)
    path.unlink()
    rewritten.replace(path)


def test_review_bundle_is_deterministic_exact_and_unicode_safe(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    first_result = build_review_bundle(root, first, source_date_epoch=SOURCE_EPOCH)
    second_result = build_review_bundle(root, second, source_date_epoch=SOURCE_EPOCH)

    assert first.read_bytes() == second.read_bytes()
    assert first_result["sha256"] == second_result["sha256"]
    assert validate_review_bundle(first) == []
    assert (
        first.with_suffix(".zip.sha256")
        .read_text(encoding="ascii")
        .startswith(first_result["sha256"])
    )

    manifest_name = f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST}"
    with zipfile.ZipFile(first) as archive:
        manifest = json.loads(archive.read(manifest_name).decode("utf-8"))
        listed = {row["path"] for row in manifest["files"]}
        assert set(archive.namelist()) == listed | {manifest_name}
        assert manifest_name not in listed
        assert f"{ARCHIVE_ROOT}/docs/日本語.md" in listed
        assert f"{ARCHIVE_ROOT}/{SOURCE_MANIFEST}" in listed
        assert f"{ARCHIVE_ROOT}/{RELEASE_METADATA}" in listed
        assert f"{ARCHIVE_ROOT}/{PRIVATE_NOTICE}" in listed
        assert f"{ARCHIVE_ROOT}/{NESTED_RELEASE}" not in listed
        assert manifest["excluded_source_manifest_paths"] == [NESTED_RELEASE]
        for info in archive.infolist():
            assert info.date_time == (2023, 11, 14, 22, 13, 20)
            assert stat.S_IMODE(info.external_attr >> 16) == 0o644


@pytest.mark.parametrize("unsafe", ["../outside.txt", "C:/outside.txt", "//host/share.txt"])
def test_builder_rejects_unsafe_source_paths(tmp_path: Path, unsafe: str) -> None:
    root = _make_root(tmp_path)
    manifest_path = root / SOURCE_MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][0]["path"] = unsafe
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="unsafe review bundle path"):
        build_review_bundle(root, tmp_path / "unsafe.zip", source_date_epoch=SOURCE_EPOCH)


def test_builder_rejects_duplicate_manifest_paths(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    manifest_path = root / SOURCE_MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"].append(dict(manifest["files"][0]))
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate source manifest path"):
        build_review_bundle(root, tmp_path / "duplicate.zip", source_date_epoch=SOURCE_EPOCH)


def test_builder_rejects_source_symlink(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _make_root(tmp_path)
    original = Path.is_symlink

    def marked_symlink(path: Path) -> bool:
        if path == root / "docs/result.md":
            return True
        return original(path)

    monkeypatch.setattr(Path, "is_symlink", marked_symlink)
    with pytest.raises(ValueError, match="does not allow symlinks"):
        build_review_bundle(root, tmp_path / "symlink.zip", source_date_epoch=SOURCE_EPOCH)


def test_validator_rejects_duplicate_traversal_and_symlink_entries(tmp_path: Path) -> None:
    archive_path = tmp_path / "invalid.zip"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr("../outside.txt", b"unsafe")
            archive.writestr("duplicate.txt", b"one")
            archive.writestr("duplicate.txt", b"two")
            symlink = zipfile.ZipInfo("link")
            symlink.create_system = 3
            symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(symlink, b"target")

    problems = validate_review_bundle(archive_path)
    assert any("unsafe review bundle path" in problem for problem in problems)
    assert any("duplicate ZIP entries" in problem for problem in problems)
    assert any("ZIP symlink is not allowed" in problem for problem in problems)


@pytest.mark.parametrize(
    "member",
    [
        "outside-root.txt",
        f"{ARCHIVE_ROOT}/.pytest_cache/state",
        f"{ARCHIVE_ROOT}/data/external/private.txt",
    ],
)
def test_validator_rejects_outside_root_cache_and_external_entries(
    tmp_path: Path, member: str
) -> None:
    archive_path = tmp_path / "forbidden.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(member, b"forbidden")

    problems = validate_review_bundle(archive_path)
    assert any(
        "outside the review archive root" in problem
        or "forbidden review ZIP entry" in problem
        for problem in problems
    )


def test_validator_detects_content_tampering(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    archive_path = tmp_path / "review.zip"
    build_review_bundle(root, archive_path, source_date_epoch=SOURCE_EPOCH)
    target = f"{ARCHIVE_ROOT}/docs/result.md"
    _rewrite_entry(archive_path, target, b"tampered\n")

    assert any(
        "review bundle sha256 mismatch" in problem
        for problem in validate_review_bundle(archive_path)
    )


def test_validator_detects_crc_corruption(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    archive_path = tmp_path / "review.zip"
    build_review_bundle(root, archive_path, source_date_epoch=SOURCE_EPOCH)
    content = bytearray(archive_path.read_bytes())
    with zipfile.ZipFile(archive_path) as archive:
        target = archive.getinfo(f"{ARCHIVE_ROOT}/docs/result.md")
        offset = target.header_offset + len(target.FileHeader())
    content[offset] ^= 0xFF
    archive_path.write_bytes(content)

    assert any(
        "CRC validation failed" in problem for problem in validate_review_bundle(archive_path)
    )


def test_builder_refuses_overwrite(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    output = tmp_path / "review.zip"
    output.write_bytes(b"existing")
    with pytest.raises(FileExistsError, match="must not already exist"):
        build_review_bundle(root, output, source_date_epoch=SOURCE_EPOCH)

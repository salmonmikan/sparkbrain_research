from __future__ import annotations

import json
import os
import zipfile
from pathlib import Path

import pytest

from sparkbrain.release_v03 import (
    ARCHIVE_ROOT,
    REVIEW_MANIFEST_NAME,
    SOURCE_MANIFEST_NAME,
    build_private_review_bundle,
    validate_private_review_bundle,
    validate_source_manifest,
)


def _fixture(root: Path) -> list[str]:
    (root / "docs").mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        "[project]\nname = 'sparkbrain-research'\nversion = '0.3.0'\n", encoding="utf-8"
    )
    (root / "README.md").write_text("review source\n", encoding="utf-8")
    (root / "docs" / "result.md").write_text("negative result retained\n", encoding="utf-8")
    return ["README.md", "docs/result.md", "pyproject.toml"]


def test_private_review_bundle_is_deterministic_and_no_git_verifiable(tmp_path: Path) -> None:
    root = tmp_path / "source"
    paths = _fixture(root)
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    for output in (first, second):
        build_private_review_bundle(
            root,
            source_revision="a" * 40,
            paths=paths,
            output=output,
            source_date_epoch=1_700_000_000,
        )
        assert validate_private_review_bundle(output) == []
    assert first.read_bytes() == second.read_bytes()
    assert first.with_suffix(".zip.sha256").read_text(encoding="ascii").split()[0] == (
        second.with_suffix(".zip.sha256").read_text(encoding="ascii").split()[0]
    )
    extracted = tmp_path / "no-git"
    with zipfile.ZipFile(first) as archive:
        archive.extractall(extracted)
    review_root = extracted / ARCHIVE_ROOT
    assert not (review_root / ".git").exists()
    source_manifest = json.loads((review_root / SOURCE_MANIFEST_NAME).read_text(encoding="utf-8"))
    assert validate_source_manifest(review_root, source_manifest) == []


def test_private_review_bundle_rejects_source_and_checksum_tampering(tmp_path: Path) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    build_private_review_bundle(
        root,
        source_revision="b" * 40,
        paths=_fixture(root),
        output=output,
        source_date_epoch=1_700_000_000,
    )
    rewritten = tmp_path / "rewritten.zip"
    with zipfile.ZipFile(output) as source, zipfile.ZipFile(rewritten, "w") as target:
        for info in source.infolist():
            content = source.read(info.filename)
            if info.filename == f"{ARCHIVE_ROOT}/docs/result.md":
                content = b"tampered\n"
            target.writestr(info, content)
    rewritten.replace(output)
    assert any("hash mismatch" in problem for problem in validate_private_review_bundle(output))
    output.with_suffix(".zip.sha256").write_text("0" * 64 + "  review.zip\n", encoding="ascii")
    assert any("checksum mismatch" in problem for problem in validate_private_review_bundle(output))


def test_private_review_bundle_keeps_license_blocker_and_refuses_existing_output(
    tmp_path: Path,
) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    paths = _fixture(root)
    build_private_review_bundle(
        root,
        source_revision="c" * 40,
        paths=paths,
        output=output,
        source_date_epoch=1_700_000_000,
    )
    with zipfile.ZipFile(output) as archive:
        manifest = json.loads(archive.read(f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST_NAME}"))
    assert manifest["license_status"] == "owner-decision-pending"
    with pytest.raises(ValueError, match="already exists"):
        build_private_review_bundle(
            root,
            source_revision="c" * 40,
            paths=paths,
            output=output,
            source_date_epoch=1_700_000_000,
        )


def test_private_review_bundle_preserves_corrective_package_version(tmp_path: Path) -> None:
    root = tmp_path / "source"
    paths = _fixture(root)
    (root / "pyproject.toml").write_text(
        "[project]\nname = 'sparkbrain-research'\nversion = '0.3.1'\n", encoding="utf-8"
    )
    output = tmp_path / "review.zip"
    build_private_review_bundle(
        root,
        source_revision="3" * 40,
        paths=paths,
        output=output,
        source_date_epoch=1_700_000_000,
    )
    with zipfile.ZipFile(output) as archive:
        review = json.loads(archive.read(f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST_NAME}"))
        source = json.loads(archive.read(f"{ARCHIVE_ROOT}/{SOURCE_MANIFEST_NAME}"))
    assert review["package_version"] == "0.3.1"
    assert source["package_version"] == "0.3.1"
    assert validate_private_review_bundle(output) == []


def test_private_review_bundle_refuses_existing_checksum_without_publishing_zip(
    tmp_path: Path,
) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    checksum = output.with_suffix(".zip.sha256")
    checksum.write_bytes(b"competitor-checksum")

    with pytest.raises(ValueError, match="already exists"):
        build_private_review_bundle(
            root,
            source_revision="d" * 40,
            paths=_fixture(root),
            output=output,
            source_date_epoch=1_700_000_000,
        )
    assert not output.exists()
    assert checksum.read_bytes() == b"competitor-checksum"


def test_private_review_bundle_never_removes_a_racing_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    original_link = os.link

    def racing_link(source: str | Path, target: str | Path) -> None:
        if Path(target) == output:
            output.write_bytes(b"competitor")
        original_link(source, target)

    monkeypatch.setattr("sparkbrain.release_v03.os.link", racing_link)
    with pytest.raises(FileExistsError):
        build_private_review_bundle(
            root,
            source_revision="d" * 40,
            paths=_fixture(root),
            output=output,
            source_date_epoch=1_700_000_000,
        )
    assert output.read_bytes() == b"competitor"
    assert not list(tmp_path.glob(".v03-private-review-*.zip"))


def test_private_review_bundle_rolls_back_its_zip_on_checksum_publish_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    checksum = output.with_suffix(".zip.sha256")
    original_link = os.link

    def racing_link(source: str | Path, target: str | Path) -> None:
        if Path(target) == checksum:
            checksum.write_bytes(b"competitor-checksum")
        original_link(source, target)

    monkeypatch.setattr("sparkbrain.release_v03.os.link", racing_link)
    with pytest.raises(FileExistsError):
        build_private_review_bundle(
            root,
            source_revision="e" * 40,
            paths=_fixture(root),
            output=output,
            source_date_epoch=1_700_000_000,
        )
    assert not output.exists()
    assert checksum.read_bytes() == b"competitor-checksum"
    assert not list(tmp_path.glob(".v03-private-review-*.zip"))
    assert not list(tmp_path.glob(".v03-private-review-*.zip.sha256"))


def test_private_review_bundle_rolls_back_both_files_on_validation_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    checksum = output.with_suffix(".zip.sha256")
    monkeypatch.setattr(
        "sparkbrain.release_v03.validate_private_review_bundle",
        lambda _path: ["injected validation failure"],
    )

    with pytest.raises(ValueError, match="injected validation failure"):
        build_private_review_bundle(
            root,
            source_revision="f" * 40,
            paths=_fixture(root),
            output=output,
            source_date_epoch=1_700_000_000,
        )
    assert not output.exists()
    assert not checksum.exists()
    assert not list(tmp_path.glob(".v03-private-review-*.zip"))
    assert not list(tmp_path.glob(".v03-private-review-*.zip.sha256"))


def test_private_review_bundle_rollback_preserves_replaced_competitor_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "source"
    output = tmp_path / "review.zip"
    checksum = output.with_suffix(".zip.sha256")

    def replace_before_failure(_path: Path) -> list[str]:
        replacement_zip = tmp_path / "competitor.zip"
        replacement_checksum = tmp_path / "competitor.zip.sha256"
        replacement_zip.write_bytes(b"competitor-zip")
        replacement_checksum.write_bytes(b"competitor-checksum")
        os.replace(replacement_zip, output)
        os.replace(replacement_checksum, checksum)
        return ["injected validation failure"]

    monkeypatch.setattr(
        "sparkbrain.release_v03.validate_private_review_bundle", replace_before_failure
    )
    with pytest.raises(ValueError, match="injected validation failure"):
        build_private_review_bundle(
            root,
            source_revision="1" * 40,
            paths=_fixture(root),
            output=output,
            source_date_epoch=1_700_000_000,
        )
    assert output.read_bytes() == b"competitor-zip"
    assert checksum.read_bytes() == b"competitor-checksum"
    assert not list(tmp_path.glob(".v03-private-review-*.zip"))
    assert not list(tmp_path.glob(".v03-private-review-*.zip.sha256"))

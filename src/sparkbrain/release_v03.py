"""Deterministic, no-Git-verifiable private v0.3 review bundles.

This module deliberately does not create a public archive.  It packages only a
caller-selected source snapshot with a self-contained manifest so reviewers can
verify it after extraction without Git metadata.  The owner license blocker is
part of the immutable review contract.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import time
import tomllib
import zipfile
from collections import Counter
from collections.abc import Iterable
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

ARCHIVE_ROOT = "sparkbrain_research_v0_3"
SOURCE_MANIFEST_NAME = "SOURCE_MANIFEST.json"
REVIEW_MANIFEST_NAME = "REVIEW_BUNDLE_MANIFEST.json"
PRIVATE_NOTICE_NAME = "PRIVATE_REVIEW_NOTICE.txt"
SOURCE_MANIFEST_SCHEMA = "sparkbrain-v03-source-manifest-v1"
REVIEW_MANIFEST_SCHEMA = "sparkbrain-v03-private-review-v1"
SUPPORTED_PRIVATE_REVIEW_VERSIONS = frozenset({"0.3.0", "0.3.1"})
PRIVATE_NOTICE = (
    b"PRIVATE CHATGPT REVIEW BUNDLE\n"
    b"This archive is for private review, not a public release.\n"
    b"The project license remains an owner decision.\n"
    b"REVIEW_BUNDLE_MANIFEST.json is the content authority for this archive.\n"
)
FORBIDDEN_PREFIXES = (".git/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/", ".venv/")


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _path(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("release path must be a string")
    normalized = value.replace("\\", "/")
    posix = PurePosixPath(normalized)
    windows = PureWindowsPath(value)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or ".." in posix.parts
        or normalized in {"", "."}
        or normalized.startswith(FORBIDDEN_PREFIXES)
        or normalized == "data/external"
        or normalized.startswith("data/external/")
    ):
        raise ValueError("unsafe release path")
    return posix.as_posix()


def _revision(value: Any) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 40
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("source_revision must be a full lowercase Git SHA")
    return value


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _package_version(root: Path) -> str:
    try:
        payload = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"project metadata is unreadable: {exc}") from exc
    version = payload.get("project", {}).get("version")
    if not isinstance(version, str) or version not in SUPPORTED_PRIVATE_REVIEW_VERSIONS:
        raise ValueError("private v0.3 bundle requires a supported v0.3 package version")
    return version


def build_source_manifest(
    root: Path, *, source_revision: str, paths: Iterable[str]
) -> dict[str, Any]:
    revision = _revision(source_revision)
    selected = sorted(_path(path) for path in paths)
    if not selected or len(selected) != len(set(selected)):
        raise ValueError("release source paths must be non-empty and unique")
    rows = []
    for relative in selected:
        absolute = root / relative
        if absolute.is_symlink() or not absolute.is_file():
            raise ValueError(f"release source is not a regular file: {relative}")
        content = absolute.read_bytes()
        rows.append({"path": relative, "size": len(content), "sha256": _sha256(content)})
    return {
        "schema_version": SOURCE_MANIFEST_SCHEMA,
        "package_version": _package_version(root),
        "source_revision": revision,
        "files": rows,
        "file_count": len(rows),
        "total_bytes": sum(row["size"] for row in rows),
    }


def validate_source_manifest(root: Path, manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["source manifest must be a JSON object"]
    required = {
        "schema_version",
        "package_version",
        "source_revision",
        "files",
        "file_count",
        "total_bytes",
    }
    problems: list[str] = []
    if set(manifest) != required:
        problems.append("source manifest fields do not match fixed schema")
    if manifest.get("schema_version") != SOURCE_MANIFEST_SCHEMA:
        problems.append("unsupported source manifest schema version")
    if manifest.get("package_version") not in SUPPORTED_PRIVATE_REVIEW_VERSIONS:
        problems.append("source manifest package_version must be a supported v0.3 version")
    try:
        _revision(manifest.get("source_revision"))
    except ValueError as exc:
        problems.append(str(exc))
    files = manifest.get("files")
    if not isinstance(files, list):
        return [*problems, "source manifest files must be an array"]
    paths: list[str] = []
    total = 0
    for index, row in enumerate(files):
        if not isinstance(row, dict) or set(row) != {"path", "size", "sha256"}:
            problems.append(f"source manifest files[{index}] has invalid fields")
            continue
        try:
            relative = _path(row["path"])
        except ValueError:
            problems.append(f"source manifest files[{index}] has unsafe path")
            continue
        paths.append(relative)
        if relative != row["path"]:
            problems.append(f"source manifest files[{index}] path is not canonical")
        if not _plain_int(row["size"]) or row["size"] < 0:
            problems.append(f"source manifest files[{index}] size must be a non-negative integer")
            continue
        total += row["size"]
        if not _valid_sha256(row["sha256"]):
            problems.append(f"source manifest files[{index}] sha256 must be lowercase SHA-256")
            continue
        absolute = root / relative
        if absolute.is_symlink() or not absolute.is_file():
            problems.append(f"source manifest file is missing or non-regular: {relative}")
            continue
        content = absolute.read_bytes()
        if row["size"] != len(content):
            problems.append(f"source manifest size mismatch: {relative}")
        if row["sha256"] != _sha256(content):
            problems.append(f"source manifest sha256 mismatch: {relative}")
    if not paths:
        problems.append("source manifest files must be non-empty")
    if paths != sorted(paths):
        problems.append("source manifest paths must be sorted")
    if len(paths) != len(set(paths)):
        problems.append("source manifest paths must be unique")
    if not _plain_int(manifest.get("file_count")) or manifest["file_count"] != len(files):
        problems.append("source manifest file_count mismatch")
    if not _plain_int(manifest.get("total_bytes")) or manifest["total_bytes"] != total:
        problems.append("source manifest total_bytes mismatch")
    return sorted(set(problems))


def _zip_entry(archive: zipfile.ZipFile, name: str, content: bytes, epoch: int) -> None:
    info = zipfile.ZipInfo(name, date_time=tuple(time.gmtime(max(epoch, 315532800))[:6]))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, content, compresslevel=9)


def _zip_layout(archive: zipfile.ZipFile) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    infos = archive.infolist()
    names = [info.filename for info in infos]
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        problems.append(f"duplicate ZIP entries: {duplicates}")
    for info in infos:
        if info.is_dir() or stat.S_ISLNK(info.external_attr >> 16):
            problems.append(f"ZIP entry must be a regular file: {info.filename}")
        try:
            safe = _path(info.filename)
        except ValueError:
            problems.append(f"unsafe ZIP entry path: {info.filename}")
            continue
        if safe != info.filename or not safe.startswith(f"{ARCHIVE_ROOT}/"):
            problems.append(f"ZIP entry has an invalid archive root: {info.filename}")
    try:
        damaged = archive.testzip()
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        problems.append(f"ZIP CRC validation failed: {exc}")
    else:
        if damaged is not None:
            problems.append(f"ZIP CRC validation failed: {damaged}")
    return problems, names


def validate_private_review_bundle(path: Path) -> list[str]:
    if path.is_symlink() or not path.is_file():
        return ["private review bundle must be a regular file"]
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"private review ZIP is unreadable: {exc}"]
    with archive:
        problems, names = _zip_layout(archive)
        manifest_path = f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST_NAME}"
        source_path = f"{ARCHIVE_ROOT}/{SOURCE_MANIFEST_NAME}"
        notice_path = f"{ARCHIVE_ROOT}/{PRIVATE_NOTICE_NAME}"
        try:
            review_raw = archive.read(manifest_path)
            source_raw = archive.read(source_path)
            notice = archive.read(notice_path)
            review = json.loads(review_raw.decode("utf-8"))
            source = json.loads(source_raw.decode("utf-8"))
        except (
            KeyError,
            RuntimeError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            zipfile.BadZipFile,
        ) as exc:
            return [*problems, f"private review manifest is unreadable: {exc}"]
        if review_raw != _canonical_json(review) or source_raw != _canonical_json(source):
            problems.append("private review JSON is not canonical")
        expected_review_fields = {
            "schema_version",
            "bundle_type",
            "source_manifest",
            "source_manifest_sha256",
            "source_revision",
            "package_version",
            "private_notice",
            "private_notice_sha256",
            "license_status",
        }
        if not isinstance(review, dict) or set(review) != expected_review_fields:
            problems.append("private review manifest fields do not match fixed schema")
            return sorted(set(problems))
        expected_values = {
            "schema_version": REVIEW_MANIFEST_SCHEMA,
            "bundle_type": "private-review",
            "source_manifest": SOURCE_MANIFEST_NAME,
            "private_notice": PRIVATE_NOTICE_NAME,
            "license_status": "owner-decision-pending",
        }
        for field, expected in expected_values.items():
            if review.get(field) != expected:
                problems.append(f"private review manifest {field} mismatch")
        if review.get("package_version") not in SUPPORTED_PRIVATE_REVIEW_VERSIONS:
            problems.append("private review manifest package_version mismatch")
        if review.get("source_manifest_sha256") != _sha256(source_raw):
            problems.append("private review source manifest hash mismatch")
        if review.get("private_notice_sha256") != _sha256(notice) or notice != PRIVATE_NOTICE:
            problems.append("private review notice mismatch")
        if review.get("source_revision") != source.get("source_revision"):
            problems.append("private review source revision mismatch")
        source_fields = {
            "schema_version",
            "package_version",
            "source_revision",
            "files",
            "file_count",
            "total_bytes",
        }
        if not isinstance(source, dict) or set(source) != source_fields:
            problems.append("private review source manifest fields do not match fixed schema")
            return sorted(set(problems))
        if source.get("schema_version") != SOURCE_MANIFEST_SCHEMA:
            problems.append("private review source manifest schema mismatch")
        try:
            _revision(source.get("source_revision"))
        except ValueError:
            problems.append("private review source manifest revision is invalid")
        if source.get("package_version") not in SUPPORTED_PRIVATE_REVIEW_VERSIONS:
            problems.append("private review source manifest package version mismatch")
        if review.get("package_version") != source.get("package_version"):
            problems.append("private review package version does not match source manifest")
        files = source.get("files") if isinstance(source, dict) else None
        expected_names = {manifest_path, source_path, notice_path}
        if not isinstance(files, list):
            problems.append("private review source manifest files must be an array")
        else:
            paths: list[str] = []
            total_bytes = 0
            for row in files:
                if not isinstance(row, dict) or set(row) != {"path", "size", "sha256"}:
                    problems.append("private review source manifest row is invalid")
                    continue
                try:
                    relative = _path(row["path"])
                except ValueError:
                    problems.append("private review source manifest row has unsafe path")
                    continue
                paths.append(relative)
                if relative != row["path"] or not _plain_int(row["size"]) or row["size"] < 0:
                    problems.append("private review source manifest row has invalid fields")
                    continue
                total_bytes += row["size"]
                if not _valid_sha256(row["sha256"]):
                    problems.append("private review source manifest row has invalid sha256")
                    continue
                member = f"{ARCHIVE_ROOT}/{relative}"
                expected_names.add(member)
                try:
                    content = archive.read(member)
                except (KeyError, RuntimeError, zipfile.BadZipFile) as exc:
                    problems.append(f"private review source file is unreadable: {relative}: {exc}")
                    continue
                if row.get("size") != len(content) or row.get("sha256") != _sha256(content):
                    problems.append(f"private review source file hash mismatch: {relative}")
            if paths != sorted(paths) or len(paths) != len(set(paths)):
                problems.append("private review source manifest paths must be sorted and unique")
            if source.get("file_count") != len(files):
                problems.append("private review source manifest file_count mismatch")
            if source.get("total_bytes") != total_bytes:
                problems.append("private review source manifest total_bytes mismatch")
        if set(names) != expected_names or len(names) != len(expected_names):
            problems.append("private review manifest does not exactly match ZIP contents")
    checksum_path = path.with_suffix(path.suffix + ".sha256")
    try:
        checksum = checksum_path.read_bytes()
    except OSError as exc:
        problems.append(f"private review checksum is unreadable: {exc}")
    else:
        expected_checksum = f"{sha256_file(path)}  {path.name}\n".encode("ascii")
        if checksum != expected_checksum:
            problems.append("private review checksum mismatch")
    return sorted(set(problems))


def _publish_no_clobber(staging: Path, destination: Path) -> None:
    """Atomically publish a staged file without replacing an existing path."""

    os.link(staging, destination)


def _unlink_published_if_ours(staging: Path, destination: Path) -> None:
    """Rollback only while the destination still names the staged file."""

    try:
        is_ours = os.path.samefile(staging, destination)
    except OSError:
        return
    if is_ours:
        destination.unlink(missing_ok=True)


def build_private_review_bundle(
    root: Path,
    *,
    source_revision: str,
    paths: Iterable[str],
    output: Path,
    source_date_epoch: int,
) -> dict[str, str]:
    if not _plain_int(source_date_epoch):
        raise ValueError("source_date_epoch must be an integer")
    checksum_output = output.with_suffix(output.suffix + ".sha256")
    if (
        output.exists()
        or output.is_symlink()
        or checksum_output.exists()
        or checksum_output.is_symlink()
    ):
        raise ValueError("private review output already exists")
    source = build_source_manifest(root, source_revision=source_revision, paths=paths)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=".v03-private-review-", suffix=".zip", dir=output.parent, delete=False
    ) as temporary:
        staging = Path(temporary.name)
    staging_checksum: Path | None = None
    published_bundle = False
    published_checksum = False
    try:
        review = {
            "schema_version": REVIEW_MANIFEST_SCHEMA,
            "bundle_type": "private-review",
            "source_manifest": SOURCE_MANIFEST_NAME,
            "source_manifest_sha256": _sha256(_canonical_json(source)),
            "source_revision": source["source_revision"],
            "package_version": source["package_version"],
            "private_notice": PRIVATE_NOTICE_NAME,
            "private_notice_sha256": _sha256(PRIVATE_NOTICE),
            "license_status": "owner-decision-pending",
        }
        with zipfile.ZipFile(
            staging, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for row in source["files"]:
                _zip_entry(
                    archive,
                    f"{ARCHIVE_ROOT}/{row['path']}",
                    (root / row["path"]).read_bytes(),
                    source_date_epoch,
                )
            _zip_entry(
                archive,
                f"{ARCHIVE_ROOT}/{SOURCE_MANIFEST_NAME}",
                _canonical_json(source),
                source_date_epoch,
            )
            _zip_entry(
                archive,
                f"{ARCHIVE_ROOT}/{PRIVATE_NOTICE_NAME}",
                PRIVATE_NOTICE,
                source_date_epoch,
            )
            _zip_entry(
                archive,
                f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST_NAME}",
                _canonical_json(review),
                source_date_epoch,
            )
        checksum = f"{sha256_file(staging)}  {output.name}\n".encode("ascii")
        with tempfile.NamedTemporaryFile(
            prefix=".v03-private-review-",
            suffix=".zip.sha256",
            dir=output.parent,
            delete=False,
        ) as temporary:
            staging_checksum = Path(temporary.name)
            temporary.write(checksum)
        _publish_no_clobber(staging, output)
        published_bundle = True
        _publish_no_clobber(staging_checksum, checksum_output)
        published_checksum = True
        problems = validate_private_review_bundle(output)
        if problems:
            raise ValueError("published private review validation failed: " + "; ".join(problems))
    except BaseException:
        if published_checksum and staging_checksum is not None:
            _unlink_published_if_ours(staging_checksum, checksum_output)
        if published_bundle:
            _unlink_published_if_ours(staging, output)
        staging.unlink(missing_ok=True)
        if staging_checksum is not None:
            staging_checksum.unlink(missing_ok=True)
        raise
    staging.unlink()
    if staging_checksum is None:
        raise RuntimeError("private review checksum staging was not created")
    staging_checksum.unlink()
    return {
        "review": str(output),
        "sha256": sha256_file(output),
        "checksum_file": str(checksum_output),
    }

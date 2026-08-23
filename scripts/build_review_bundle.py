from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import stat
import tempfile
import tomllib
import zipfile
import zlib
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = "sparkbrain_research_v0_2"
SOURCE_MANIFEST = "PACKAGE_MANIFEST.json"
RELEASE_METADATA = "RELEASE_METADATA.json"
REVIEW_MANIFEST = "REVIEW_BUNDLE_MANIFEST.json"
PRIVATE_NOTICE = "PRIVATE_REVIEW_NOTICE.txt"
REVIEW_SCHEMA_VERSION = "sparkbrain-review-bundle-v1"
EXCLUDED_SOURCE_PATHS = {"archive/v0.2/sparkbrain_research_v0_2.zip"}
FORBIDDEN_SOURCE_PREFIXES = (
    ".git/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".venv/",
    "data/external/",
)


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError(f"unsafe review bundle path: {value!r}")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(value)
    if (
        path.is_absolute()
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or ".." in path.parts
        or normalized in {"", "."}
    ):
        raise ValueError(f"unsafe review bundle path: {value!r}")
    return path.as_posix()


def _zip_info(name: str, timestamp: tuple[int, int, int, int, int, int]) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=timestamp)
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def _package_version(root: Path) -> str:
    payload = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    version = payload.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("pyproject.toml must declare project.version")
    return version


def _notice_bytes() -> bytes:
    return (
        b"PRIVATE CHATGPT REVIEW BUNDLE\n"
        b"This archive is for private review, not a public release.\n"
        b"The project license remains an owner decision.\n"
        b"REVIEW_BUNDLE_MANIFEST.json is the content authority for this archive.\n"
    )


def _selected_source_rows(root: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = source.get("files")
    if not isinstance(rows, list):
        raise ValueError("PACKAGE_MANIFEST.json files must be an array")
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"PACKAGE_MANIFEST.json files[{index}] must be an object")
        relative = _safe_relative_path(row.get("path"))
        if relative in seen:
            raise ValueError(f"duplicate source manifest path: {relative}")
        seen.add(relative)
        if relative in EXCLUDED_SOURCE_PATHS:
            continue
        if relative.startswith(FORBIDDEN_SOURCE_PREFIXES):
            raise ValueError(f"forbidden review source path: {relative}")
        path = root / Path(relative)
        if path.is_symlink():
            raise ValueError(f"review bundle does not allow symlinks: {relative}")
        if not path.is_file():
            raise ValueError(f"missing or non-regular review source file: {relative}")
        content = path.read_bytes()
        if row.get("size") != len(content):
            raise ValueError(f"source manifest size mismatch: {relative}")
        if row.get("sha256") != _sha256_bytes(content):
            raise ValueError(f"source manifest sha256 mismatch: {relative}")
        artifact_class = row.get("artifact_class")
        if not isinstance(artifact_class, str) or not artifact_class:
            raise ValueError(f"source manifest artifact_class is invalid: {relative}")
        selected.append(
            {
                "path": f"{ARCHIVE_ROOT}/{relative}",
                "size": len(content),
                "sha256": _sha256_bytes(content),
                "artifact_class": artifact_class,
                "content": content,
            }
        )
    return selected


def _manifest_row(path: str, content: bytes, artifact_class: str) -> dict[str, Any]:
    return {
        "path": path,
        "size": len(content),
        "sha256": _sha256_bytes(content),
        "artifact_class": artifact_class,
    }


def validate_review_bundle(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"review ZIP is unreadable: {exc}"]
    with archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
        if duplicates:
            problems.append(f"duplicate ZIP entries: {duplicates}")
        for info in infos:
            try:
                safe = _safe_relative_path(info.filename)
            except ValueError as exc:
                problems.append(str(exc))
                continue
            if safe != info.filename:
                problems.append(f"non-canonical ZIP entry path: {info.filename}")
            archive_prefix = f"{ARCHIVE_ROOT}/"
            if not safe.startswith(archive_prefix):
                problems.append(f"ZIP entry is outside the review archive root: {info.filename}")
            else:
                inner = safe[len(archive_prefix) :]
                if inner.startswith(FORBIDDEN_SOURCE_PREFIXES):
                    problems.append(f"forbidden review ZIP entry: {info.filename}")
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                problems.append(f"ZIP symlink is not allowed: {info.filename}")
            if info.is_dir():
                problems.append(f"ZIP directory entry is not allowed: {info.filename}")
        try:
            damaged = archive.testzip()
        except (OSError, RuntimeError, zipfile.BadZipFile, zlib.error) as exc:
            problems.append(f"ZIP CRC validation failed: {exc}")
        else:
            if damaged is not None:
                problems.append(f"ZIP CRC validation failed: {damaged}")

        manifest_name = f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST}"
        if names.count(manifest_name) != 1:
            problems.append("review bundle manifest must appear exactly once")
            return problems
        try:
            manifest = json.loads(archive.read(manifest_name).decode("utf-8"))
        except (
            KeyError,
            RuntimeError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            zipfile.BadZipFile,
            zlib.error,
        ) as exc:
            problems.append(f"review bundle manifest is unreadable: {exc}")
            return problems
        if manifest.get("schema_version") != REVIEW_SCHEMA_VERSION:
            problems.append("unsupported review bundle manifest schema version")
        rows = manifest.get("files")
        if not isinstance(rows, list):
            problems.append("review bundle manifest files must be an array")
            return problems
        seen: set[str] = set()
        contents: dict[str, bytes] = {}
        total_bytes = 0
        for index, row in enumerate(rows):
            required = {"path", "size", "sha256", "artifact_class"}
            if not isinstance(row, dict) or set(row) != required:
                problems.append(f"review files[{index}] has invalid fields")
                continue
            if not isinstance(row["artifact_class"], str) or not row["artifact_class"]:
                problems.append(f"review files[{index}] has invalid artifact_class")
            try:
                relative = _safe_relative_path(row["path"])
            except ValueError as exc:
                problems.append(f"review files[{index}] has invalid path: {exc}")
                continue
            if relative == manifest_name:
                problems.append("review manifest must not list itself")
            if relative in seen:
                problems.append(f"duplicate review manifest path: {relative}")
                continue
            seen.add(relative)
            if names.count(relative) != 1:
                problems.append(f"missing or duplicate review ZIP entry: {relative}")
                continue
            try:
                content = archive.read(relative)
            except (KeyError, RuntimeError, zipfile.BadZipFile, zlib.error) as exc:
                problems.append(f"review ZIP entry is unreadable: {relative}: {exc}")
                continue
            contents[relative] = content
            if row["size"] != len(content):
                problems.append(f"review bundle size mismatch: {relative}")
            if row["sha256"] != _sha256_bytes(content):
                problems.append(f"review bundle sha256 mismatch: {relative}")
            total_bytes += len(content)
        expected_names = seen | {manifest_name}
        if set(names) != expected_names:
            problems.append("review manifest does not exactly match ZIP contents")
        if manifest.get("file_count") != len(rows):
            problems.append("review bundle manifest file_count mismatch")
        if manifest.get("uncompressed_bytes_excluding_manifest") != total_bytes:
            problems.append("review bundle manifest total byte count mismatch")
        source_name = f"{ARCHIVE_ROOT}/{SOURCE_MANIFEST}"
        metadata_name = f"{ARCHIVE_ROOT}/{RELEASE_METADATA}"
        if source_name in contents:
            source_bytes = contents[source_name]
            if manifest.get("source_manifest_sha256") != _sha256_bytes(source_bytes):
                problems.append("review bundle source manifest hash mismatch")
        else:
            problems.append("review bundle omits PACKAGE_MANIFEST.json")
        if metadata_name in contents:
            try:
                metadata = json.loads(contents[metadata_name].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                problems.append(f"review bundle release metadata is unreadable: {exc}")
            else:
                if metadata.get("manifest_sha256") != manifest.get("source_manifest_sha256"):
                    problems.append("review bundle release metadata manifest hash mismatch")
                if metadata.get("source_revision") != manifest.get("source_revision"):
                    problems.append("review bundle release metadata revision mismatch")
                if metadata.get("package_version") != manifest.get("package_version"):
                    problems.append("review bundle release metadata package version mismatch")
        else:
            problems.append("review bundle omits RELEASE_METADATA.json")
    return problems


def build_review_bundle(
    root: Path, output: Path, *, source_date_epoch: int
) -> dict[str, str | int]:
    root = root.resolve()
    output = output.resolve()
    checksum_path = output.with_suffix(output.suffix + ".sha256")
    if output.exists() or checksum_path.exists():
        raise FileExistsError("review bundle output and checksum path must not already exist")
    source_bytes = (root / SOURCE_MANIFEST).read_bytes()
    source = json.loads(source_bytes.decode("utf-8"))
    source_revision = source.get("source_revision")
    if (
        not isinstance(source_revision, str)
        or re.fullmatch(r"[0-9a-f]{40}", source_revision) is None
    ):
        raise ValueError("PACKAGE_MANIFEST.json source_revision must be a full lowercase Git SHA")
    source_rows = _selected_source_rows(root, source)
    metadata_bytes = (root / RELEASE_METADATA).read_bytes()
    metadata = json.loads(metadata_bytes.decode("utf-8"))
    if metadata.get("manifest_sha256") != _sha256_bytes(source_bytes):
        raise ValueError(
            "RELEASE_METADATA.json manifest_sha256 does not match PACKAGE_MANIFEST.json"
        )
    if metadata.get("source_revision") != source_revision:
        raise ValueError(
            "RELEASE_METADATA.json source_revision does not match PACKAGE_MANIFEST.json"
        )
    package_version = _package_version(root)
    if metadata.get("package_version") != package_version:
        raise ValueError("RELEASE_METADATA.json package_version does not match pyproject.toml")

    package_manifest_path = f"{ARCHIVE_ROOT}/{SOURCE_MANIFEST}"
    release_metadata_path = f"{ARCHIVE_ROOT}/{RELEASE_METADATA}"
    notice_path = f"{ARCHIVE_ROOT}/{PRIVATE_NOTICE}"
    notice = _notice_bytes()
    payload = [
        *source_rows,
        {
            **_manifest_row(package_manifest_path, source_bytes, "package-metadata"),
            "content": source_bytes,
        },
        {
            **_manifest_row(release_metadata_path, metadata_bytes, "package-metadata"),
            "content": metadata_bytes,
        },
        {
            **_manifest_row(notice_path, notice, "documentation"),
            "content": notice,
        },
    ]
    payload.sort(key=lambda row: row["path"])
    payload_names = [row["path"] for row in payload]
    if len(payload_names) != len(set(payload_names)):
        raise ValueError("review bundle generated paths collide with source manifest paths")
    timestamp_value = max(source_date_epoch, 315532800)
    date = datetime.datetime.fromtimestamp(timestamp_value, tz=datetime.UTC)
    timestamp = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    manifest = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "bundle_type": "private-chatgpt-review",
        "archive_root": ARCHIVE_ROOT,
        "generated_at": date.isoformat(),
        "package_version": package_version,
        "source_revision": source_revision,
        "source_manifest": SOURCE_MANIFEST,
        "source_manifest_sha256": _sha256_bytes(source_bytes),
        "excluded_source_manifest_paths": sorted(EXCLUDED_SOURCE_PATHS),
        "license_status": "owner-decision-pending",
        "manifest_self_excluded": True,
        "file_count": len(payload),
        "uncompressed_bytes_excluding_manifest": sum(row["size"] for row in payload),
        "files": [
            {key: row[key] for key in ("path", "size", "sha256", "artifact_class")}
            for row in payload
        ],
    }
    manifest_bytes = _canonical_json(manifest)
    manifest_name = f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST}"

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=output.parent, prefix=f".{output.name}.", suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
        with zipfile.ZipFile(
            temporary_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            members = [*payload, {"path": manifest_name, "content": manifest_bytes}]
            for row in sorted(members, key=lambda item: item["path"]):
                archive.writestr(_zip_info(row["path"], timestamp), row["content"])
        problems = validate_review_bundle(temporary_path)
        if problems:
            raise ValueError("review bundle validation failed: " + "; ".join(problems))
        checksum = _sha256_file(temporary_path)
        os.replace(temporary_path, output)
        temporary_path = None
        checksum_path.write_text(f"{checksum}  {output.name}\n", encoding="ascii", newline="\n")
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return {
        "archive": str(output),
        "sha256": checksum,
        "checksum_file": str(checksum_path),
        "manifest": f"{ARCHIVE_ROOT}/{REVIEW_MANIFEST}",
        "file_count_excluding_manifest": len(payload),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a deterministic private review bundle")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-date-epoch", type=int, required=True)
    args = parser.parse_args()
    try:
        result = build_review_bundle(ROOT, args.output, source_date_epoch=args.source_date_epoch)
    except (FileExistsError, OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Fail-closed candidate/review archive primitives for the future v0.3 release.

This module intentionally does not select a public license, alter package metadata, or
publish an official release.  It is a source-only foundation that C20 can wire to the
final, accepted v0.3 evidence after C11--C19 have closed.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import tempfile
import time
import zipfile
from collections.abc import Iterable
from pathlib import Path, PurePosixPath
from typing import Any


CANDIDATE_MANIFEST_NAME = "CANDIDATE_RELEASE_MANIFEST.json"
REVIEW_MANIFEST_NAME = "REVIEW_BUNDLE_MANIFEST.json"
CANDIDATE_MANIFEST_SCHEMA = "sparkbrain-candidate-release-v1"
REVIEW_MANIFEST_SCHEMA = "sparkbrain-review-bundle-v1"
CANONICAL_REPRODUCTION_SCHEMA = "sparkbrain-canonical-reproduction-v1"
NETWORK_MODULE_PREFIXES = ("http", "requests", "socket", "urllib")


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"unsafe candidate path: {value!r}")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or normalized in {"", "."}:
        raise ValueError(f"unsafe candidate path: {value!r}")
    return path.as_posix()


def _require_revision(value: Any) -> str:
    if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("source_revision must be a full lowercase Git SHA")
    return value


def build_canonical_reproduction_manifest(
    root: Path, *, source_revision: str, paths: Iterable[str]
) -> dict[str, Any]:
    """Create deterministic evidence identity without runtime duration/platform fields."""

    revision = _require_revision(source_revision)
    selected = sorted(_safe_relative_path(path) for path in paths)
    if len(selected) != len(set(selected)):
        raise ValueError("candidate manifest paths must be unique")

    files: list[dict[str, Any]] = []
    total_bytes = 0
    for relative in selected:
        absolute = root / relative
        if absolute.is_symlink() or not absolute.is_file():
            raise ValueError(f"candidate input is not a regular file: {relative}")
        size = absolute.stat().st_size
        total_bytes += size
        files.append({"path": relative, "sha256": sha256_file(absolute), "size": size})

    return {
        "file_count": len(files),
        "files": files,
        "schema_version": CANONICAL_REPRODUCTION_SCHEMA,
        "source_revision": revision,
        "total_bytes": total_bytes,
    }


def validate_canonical_reproduction_manifest(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["candidate manifest must be a JSON object"]
    expected = {"file_count", "files", "schema_version", "source_revision", "total_bytes"}
    problems: list[str] = []
    if set(manifest) != expected:
        problems.append("candidate manifest fields do not match fixed schema")
    if manifest.get("schema_version") != CANONICAL_REPRODUCTION_SCHEMA:
        problems.append("unsupported candidate manifest schema version")
    try:
        _require_revision(manifest.get("source_revision"))
    except ValueError as exc:
        problems.append(str(exc))
    rows = manifest.get("files")
    if not isinstance(rows, list):
        return [*problems, "candidate manifest files must be an array"]

    paths: list[str] = []
    total_bytes = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "size"}:
            problems.append(f"candidate manifest files[{index}] has invalid fields")
            continue
        try:
            path = _safe_relative_path(row.get("path"))
        except ValueError as exc:
            problems.append(f"candidate manifest files[{index}] {exc}")
            continue
        paths.append(path)
        if not isinstance(row.get("size"), int) or row["size"] < 0:
            problems.append(f"candidate manifest files[{index}] size must be a non-negative integer")
        else:
            total_bytes += row["size"]
        checksum = row.get("sha256")
        if not isinstance(checksum, str) or len(checksum) != 64 or any(
            char not in "0123456789abcdef" for char in checksum
        ):
            problems.append(f"candidate manifest files[{index}] sha256 must be lowercase SHA-256")

    if paths != sorted(paths):
        problems.append("candidate manifest file paths must be sorted")
    if len(paths) != len(set(paths)):
        problems.append("candidate manifest file paths must be unique")
    if manifest.get("file_count") != len(rows):
        problems.append("candidate manifest file_count mismatch")
    if manifest.get("total_bytes") != total_bytes:
        problems.append("candidate manifest total_bytes mismatch")
    return problems


def validate_network_client_boundary(paths: Iterable[Path]) -> list[str]:
    """Reject source files that import a runtime network client, before packaging."""

    problems: list[str] = []
    for path in paths:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            problems.append(f"network boundary could not parse {path}: {exc}")
            continue
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if name.split(".")[0] in NETWORK_MODULE_PREFIXES:
                    problems.append(f"network client import is forbidden: {path}:{name}")
    return sorted(set(problems))


def _zip_write(archive: zipfile.ZipFile, name: str, data: bytes, source_date_epoch: int) -> None:
    timestamp = max(source_date_epoch, 315532800)  # ZIP cannot represent dates before 1980.
    info = zipfile.ZipInfo(name)
    info.date_time = tuple(time.gmtime(timestamp)[:6])
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compresslevel=9)


def _checksum_text(path: Path) -> bytes:
    return f"{sha256_file(path)}  {path.name}\n".encode("ascii")


def _validate_candidate_archive(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("candidate ZIP CRC validation failed")
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("candidate ZIP members must be unique")
        if CANDIDATE_MANIFEST_NAME not in names:
            raise ValueError("candidate ZIP is missing its manifest")
        if names[-1] != CANDIDATE_MANIFEST_NAME or names[:-1] != sorted(names[:-1]):
            raise ValueError("candidate ZIP payload members must be sorted and manifest must be last")
        manifest = json.loads(archive.read(CANDIDATE_MANIFEST_NAME))
        problems = validate_canonical_reproduction_manifest(manifest)
        if problems:
            raise ValueError("candidate manifest validation failed: " + "; ".join(problems))
        expected = [row["path"] for row in manifest["files"]]
        if names != [*expected, CANDIDATE_MANIFEST_NAME]:
            raise ValueError("candidate ZIP members do not match its manifest")
        for row in manifest["files"]:
            content = archive.read(row["path"])
            if len(content) != row["size"] or _sha256_bytes(content) != row["sha256"]:
                raise ValueError(f"candidate ZIP payload does not match manifest: {row['path']}")
    return manifest


def _validate_review_archive(path: Path, candidate_path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("review ZIP CRC validation failed")
        names = archive.namelist()
        expected_names = [candidate_path.name, f"{candidate_path.name}.sha256", REVIEW_MANIFEST_NAME]
        if names != expected_names:
            raise ValueError("review ZIP members do not match the fixed review schema")
        review = json.loads(archive.read(REVIEW_MANIFEST_NAME))
        expected_fields = {"candidate_sha256", "candidate_zip", "schema_version"}
        if not isinstance(review, dict) or set(review) != expected_fields:
            raise ValueError("review manifest fields do not match fixed schema")
        if review.get("schema_version") != REVIEW_MANIFEST_SCHEMA:
            raise ValueError("unsupported review manifest schema version")
        if review.get("candidate_zip") != candidate_path.name:
            raise ValueError("review manifest candidate ZIP name mismatch")
        candidate_bytes = candidate_path.read_bytes()
        if archive.read(candidate_path.name) != candidate_bytes:
            raise ValueError("review ZIP candidate payload mismatch")
        if review.get("candidate_sha256") != _sha256_bytes(candidate_bytes):
            raise ValueError("review manifest candidate SHA-256 mismatch")
        if archive.read(f"{candidate_path.name}.sha256") != _checksum_text(candidate_path):
            raise ValueError("review ZIP candidate checksum mismatch")


def build_candidate_and_review_archives(
    root: Path,
    *,
    source_revision: str,
    paths: Iterable[str],
    candidate_output: Path,
    review_output: Path,
    source_date_epoch: int,
    network_boundary_paths: Iterable[Path] = (),
) -> dict[str, str]:
    """Stage, validate, then publish paired archives or roll back every published output."""

    if candidate_output.parent != review_output.parent:
        raise ValueError("candidate and review outputs must share a parent for transactional publish")
    if candidate_output == review_output:
        raise ValueError("candidate and review outputs must be distinct")
    outputs = (
        candidate_output,
        candidate_output.with_suffix(candidate_output.suffix + ".sha256"),
        review_output,
        review_output.with_suffix(review_output.suffix + ".sha256"),
    )
    if any(path.exists() or path.is_symlink() for path in outputs):
        raise ValueError("candidate/review output already exists")
    network_problems = validate_network_client_boundary(network_boundary_paths)
    if network_problems:
        raise ValueError("network boundary failed: " + "; ".join(network_problems))

    manifest = build_canonical_reproduction_manifest(
        root, source_revision=source_revision, paths=paths
    )
    parent = candidate_output.parent
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".candidate-release-staging-", dir=parent))
    published: list[Path] = []
    try:
        staged_candidate = staging / candidate_output.name
        with zipfile.ZipFile(staged_candidate, "w") as archive:
            for row in manifest["files"]:
                _zip_write(archive, row["path"], (root / row["path"]).read_bytes(), source_date_epoch)
            _zip_write(archive, CANDIDATE_MANIFEST_NAME, _canonical_json(manifest), source_date_epoch)
        _validate_candidate_archive(staged_candidate)
        staged_candidate_checksum = staging / f"{candidate_output.name}.sha256"
        staged_candidate_checksum.write_bytes(_checksum_text(staged_candidate))

        staged_review = staging / review_output.name
        review_manifest = {
            "candidate_sha256": sha256_file(staged_candidate),
            "candidate_zip": candidate_output.name,
            "schema_version": REVIEW_MANIFEST_SCHEMA,
        }
        with zipfile.ZipFile(staged_review, "w") as archive:
            _zip_write(archive, candidate_output.name, staged_candidate.read_bytes(), source_date_epoch)
            _zip_write(
                archive,
                f"{candidate_output.name}.sha256",
                staged_candidate_checksum.read_bytes(),
                source_date_epoch,
            )
            _zip_write(archive, REVIEW_MANIFEST_NAME, _canonical_json(review_manifest), source_date_epoch)
        _validate_review_archive(staged_review, staged_candidate)
        staged_review_checksum = staging / f"{review_output.name}.sha256"
        staged_review_checksum.write_bytes(_checksum_text(staged_review))

        for staged, destination in zip(
            (staged_candidate, staged_candidate_checksum, staged_review, staged_review_checksum), outputs
        ):
            if destination.exists() or destination.is_symlink():
                raise FileExistsError(f"candidate/review output appeared during publish: {destination}")
            os.replace(staged, destination)
            published.append(destination)
    except BaseException:
        for path in reversed(published):
            path.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return {"candidate": str(candidate_output), "review": str(review_output)}

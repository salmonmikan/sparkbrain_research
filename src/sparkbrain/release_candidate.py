"""Fail-closed source-only candidate/review release primitives for C20 integration.

Each publication is a unique Windows directory renamed from validated staging.  The group
directory contains both ZIP/checksum pairs and its binding manifest; no external pointer is
published. A process kill before/within rename is not recoverable and must not be reported as a
successful release.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
import zipfile
from collections.abc import Iterable
from pathlib import Path, PurePosixPath
from typing import Any

CANDIDATE_MANIFEST_NAME = "CANDIDATE_RELEASE_MANIFEST.json"
REVIEW_MANIFEST_NAME = "REVIEW_BUNDLE_MANIFEST.json"
RELEASE_GROUP_MANIFEST_NAME = "RELEASE_GROUP_MANIFEST.json"
CANDIDATE_MANIFEST_SCHEMA = "sparkbrain-candidate-release-v1"
REVIEW_MANIFEST_SCHEMA = "sparkbrain-review-bundle-v2"
RELEASE_GROUP_SCHEMA = "sparkbrain-release-group-v1"
NETWORK_PREFIXES = {"aiohttp", "http", "httpx", "requests", "socket", "urllib", "urllib3"}


def _json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _path(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("unsafe candidate path")
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts or str(path) in {"", "."}:
        raise ValueError("unsafe candidate path")
    return path.as_posix()


def _revision(value: Any) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 40
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise ValueError("source_revision must be a full lowercase Git SHA")
    return value


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError(
            "repository revision validation failed: " + (result.stderr.strip() or "git failed")
        )
    return result.stdout.strip()


def _bound_revision(root: Path, revision: str, base: str | None) -> None:
    _git(root, "cat-file", "-e", f"{revision}^{{commit}}")
    target = base or _git(root, "rev-parse", "HEAD")
    _git(root, "cat-file", "-e", f"{_revision(target)}^{{commit}}")
    _git(root, "merge-base", "--is-ancestor", revision, target)


def _git_blob(root: Path, revision: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{relative}"], cwd=root, capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(f"payload path is not bound to source_revision: {relative}")
    return result.stdout


def _bound_payload(root: Path, revision: str, paths: Iterable[str]) -> None:
    for relative in paths:
        clean = _git(root, "hash-object", "--path", relative, "--", relative)
        expected = _git(root, "rev-parse", f"{revision}:{relative}")
        if clean != expected:
            raise ValueError(f"payload content is not bound to source_revision: {relative}")


def build_canonical_reproduction_manifest(
    root: Path, *, source_revision: str, paths: Iterable[str], revision_base: str | None = None
) -> dict[str, Any]:
    revision = _revision(source_revision)
    selected = sorted(_path(path) for path in paths)
    if len(selected) != len(set(selected)):
        raise ValueError("candidate manifest paths must be unique")
    _bound_revision(root, revision, revision_base)
    _bound_payload(root, revision, selected)
    files = []
    for relative in selected:
        source = root / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"candidate input is not a regular file: {relative}")
        blob = _git_blob(root, revision, relative)
        files.append(
            {"path": relative, "size": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
        )
    return {
        "schema_version": CANDIDATE_MANIFEST_SCHEMA,
        "source_revision": revision,
        "files": files,
        "file_count": len(files),
        "total_bytes": sum(row["size"] for row in files),
    }


def validate_canonical_reproduction_manifest(
    root: Path, manifest: Any, *, revision_base: str | None = None
) -> list[str]:
    if not isinstance(manifest, dict):
        return ["candidate manifest must be a JSON object"]
    expected = {"schema_version", "source_revision", "files", "file_count", "total_bytes"}
    problems: list[str] = []
    if set(manifest) != expected:
        problems.append("candidate manifest fields do not match fixed schema")
    if manifest.get("schema_version") != CANDIDATE_MANIFEST_SCHEMA:
        problems.append("unsupported candidate manifest schema version")
    try:
        _bound_revision(root, _revision(manifest.get("source_revision")), revision_base)
    except ValueError as exc:
        problems.append(str(exc))
    rows = manifest.get("files")
    if not isinstance(rows, list):
        return [*problems, "candidate manifest files must be an array"]
    paths: list[str] = []
    total = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"path", "size", "sha256"}:
            problems.append(f"candidate manifest files[{index}] has invalid fields")
            continue
        try:
            paths.append(_path(row["path"]))
        except ValueError:
            problems.append(f"candidate manifest files[{index}] has unsafe path")
            continue
        if not _plain_int(row["size"]) or row["size"] < 0:
            problems.append(
                f"candidate manifest files[{index}] size must be a non-negative integer"
            )
        else:
            total += row["size"]
        if (
            not isinstance(row["sha256"], str)
            or len(row["sha256"]) != 64
            or any(c not in "0123456789abcdef" for c in row["sha256"])
        ):
            problems.append(f"candidate manifest files[{index}] sha256 must be lowercase SHA-256")
    if paths != sorted(paths):
        problems.append("candidate manifest file paths must be sorted")
    if len(paths) != len(set(paths)):
        problems.append("candidate manifest file paths must be unique")
    if not _plain_int(manifest.get("file_count")) or manifest["file_count"] != len(rows):
        problems.append("candidate manifest file_count mismatch")
    if not _plain_int(manifest.get("total_bytes")) or manifest["total_bytes"] != total:
        problems.append("candidate manifest total_bytes mismatch")
    if not problems:
        try:
            _bound_payload(root, manifest["source_revision"], paths)
        except ValueError as exc:
            problems.append(str(exc))
    return problems


def validate_network_client_boundary(root: Path) -> list[str]:
    package = root / "src" / "sparkbrain"
    if not package.is_dir():
        raise ValueError("network boundary requires src/sparkbrain package root")
    sources = sorted(package.rglob("*.py"))
    if not sources:
        raise ValueError("network boundary found no package Python sources")
    problems: list[str] = []
    for path in sources:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            problems.append(f"network boundary could not parse {path}: {exc}")
            continue
        for node in ast.walk(tree):
            names = (
                [a.name for a in node.names]
                if isinstance(node, ast.Import)
                else [node.module]
                if isinstance(node, ast.ImportFrom) and node.module
                else []
            )
            if any(name.split(".")[0] in NETWORK_PREFIXES for name in names):
                problems.append(f"network client import is forbidden: {path}")
            if isinstance(node, ast.Call) and (
                (isinstance(node.func, ast.Name) and node.func.id == "__import__")
                or (isinstance(node.func, ast.Attribute) and node.func.attr == "import_module")
            ):
                target = (
                    node.args[0].value
                    if node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    else None
                )
                if target is None or target.split(".")[0] in NETWORK_PREFIXES:
                    problems.append(f"unproven or network dynamic import is forbidden: {path}")
    return sorted(set(problems))


def _zip(archive: zipfile.ZipFile, name: str, data: bytes, epoch: int) -> None:
    info = zipfile.ZipInfo(name)
    info.date_time = tuple(time.gmtime(max(epoch, 315532800))[:6])
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compresslevel=9)


def build_candidate_and_review_archives(
    root: Path,
    *,
    source_revision: str,
    paths: Iterable[str],
    release_directory: Path,
    source_date_epoch: int,
    revision_base: str | None = None,
) -> dict[str, str]:
    if release_directory.exists() or release_directory.is_symlink():
        raise ValueError("candidate release directory already exists")
    network = validate_network_client_boundary(root)
    if network:
        raise ValueError("network boundary failed: " + "; ".join(network))
    manifest = build_canonical_reproduction_manifest(
        root, source_revision=source_revision, paths=paths, revision_base=revision_base
    )
    release_directory.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".candidate-release-staging-", dir=release_directory.parent)
    )
    try:
        candidate = staging / "candidate.zip"
        with zipfile.ZipFile(candidate, "w") as archive:
            for row in manifest["files"]:
                _zip(
                    archive,
                    row["path"],
                    _git_blob(root, manifest["source_revision"], row["path"]),
                    source_date_epoch,
                )
            _zip(archive, CANDIDATE_MANIFEST_NAME, _json(manifest), source_date_epoch)
        if validate_canonical_reproduction_manifest(root, manifest, revision_base=revision_base):
            raise ValueError("candidate manifest validation failed")
        candidate_hash = f"{sha256_file(candidate)}  {candidate.name}\n".encode()
        (staging / "candidate.zip.sha256").write_bytes(candidate_hash)
        review = staging / "review.zip"
        review_manifest = {
            "schema_version": REVIEW_MANIFEST_SCHEMA,
            "candidate_zip": candidate.name,
            "candidate_sha256": sha256_file(candidate),
        }
        with zipfile.ZipFile(review, "w") as archive:
            _zip(archive, candidate.name, candidate.read_bytes(), source_date_epoch)
            _zip(archive, "candidate.zip.sha256", candidate_hash, source_date_epoch)
            _zip(archive, REVIEW_MANIFEST_NAME, _json(review_manifest), source_date_epoch)
        (staging / "review.zip.sha256").write_bytes(
            f"{sha256_file(review)}  {review.name}\n".encode()
        )
        group = {
            "schema_version": RELEASE_GROUP_SCHEMA,
            "files": {p.name: sha256_file(p) for p in sorted(staging.iterdir())},
        }
        (staging / RELEASE_GROUP_MANIFEST_NAME).write_bytes(_json(group))
        if os.name != "nt":
            raise OSError("candidate group publish requires Windows no-replace directory rename")
        if release_directory.exists() or release_directory.is_symlink():
            raise FileExistsError(
                f"candidate release directory already exists: {release_directory}"
            )
        os.rename(staging, release_directory)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "release_directory": str(release_directory),
        "candidate": str(release_directory / "candidate.zip"),
        "review": str(release_directory / "review.zip"),
    }

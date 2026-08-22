from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Iterable
from pathlib import Path, PurePosixPath
from typing import Any

MANIFEST_SCHEMA_VERSION = "2"
MANIFEST_PATH = "PACKAGE_MANIFEST.json"
EXCLUDED_PREFIXES = (
    ".git/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".venv/",
    "data/external/",
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _safe_relative_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or normalized in {"", "."}:
        raise ValueError(f"unsafe release path: {value!r}")
    return path.as_posix()


def _is_release_path(path: str) -> bool:
    return path != MANIFEST_PATH and not path.startswith(EXCLUDED_PREFIXES)


def tracked_release_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    paths = [
        _safe_relative_path(item)
        for item in result.stdout.decode("utf-8").split("\0")
        if item
    ]
    return sorted(path for path in paths if _is_release_path(path))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_release_manifest(
    root: Path,
    *,
    generated_at: str,
    source_revision: str,
    paths: Iterable[str] | None = None,
) -> dict[str, Any]:
    selected = tracked_release_paths(root) if paths is None else sorted(
        _safe_relative_path(path) for path in paths if _is_release_path(path)
    )
    if len(selected) != len(set(selected)):
        raise ValueError("release manifest paths must be unique")

    files: list[dict[str, Any]] = []
    total_bytes = 0
    for relative in selected:
        absolute = root / Path(relative)
        if absolute.is_symlink():
            raise ValueError(f"release manifest does not allow symlinks: {relative}")
        if not absolute.is_file():
            raise FileNotFoundError(f"tracked release file is missing: {relative}")
        size = absolute.stat().st_size
        total_bytes += size
        files.append({"path": relative, "size": size, "sha256": sha256_file(absolute)})

    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": generated_at,
        "source_revision": source_revision,
        "manifest_excludes": [MANIFEST_PATH],
        "file_count": len(files),
        "uncompressed_bytes_excluding_manifest": total_bytes,
        "files": files,
    }


def write_release_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(_canonical_json(manifest), encoding="utf-8", newline="\n")


def verify_release_manifest(root: Path, manifest: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if manifest.get("manifest_schema_version") != MANIFEST_SCHEMA_VERSION:
        problems.append("unsupported release manifest schema version")
    rows = manifest.get("files")
    if not isinstance(rows, list):
        return [*problems, "release manifest files must be an array"]

    seen: set[str] = set()
    total_bytes = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"path", "size", "sha256"}:
            problems.append(f"files[{index}] must contain only path, size, and sha256")
            continue
        try:
            relative = _safe_relative_path(row["path"])
        except (TypeError, ValueError) as exc:
            problems.append(f"files[{index}] has invalid path: {exc}")
            continue
        if not _is_release_path(relative):
            problems.append(f"files[{index}] is excluded from release: {relative}")
            continue
        if relative in seen:
            problems.append(f"duplicate release path: {relative}")
            continue
        seen.add(relative)
        absolute = root / Path(relative)
        if absolute.is_symlink() or not absolute.is_file():
            problems.append(f"missing or non-regular release file: {relative}")
            continue
        actual_size = absolute.stat().st_size
        if row["size"] != actual_size:
            problems.append(f"size mismatch: {relative}")
        actual_hash = sha256_file(absolute)
        if row["sha256"] != actual_hash:
            problems.append(f"sha256 mismatch: {relative}")
        total_bytes += actual_size

    if manifest.get("file_count") != len(rows):
        problems.append("release manifest file_count mismatch")
    if manifest.get("uncompressed_bytes_excluding_manifest") != total_bytes:
        problems.append("release manifest total byte count mismatch")
    return problems


def project_license_selected(root: Path) -> bool:
    return (root / "LICENSE").is_file() and not (root / "LICENSE_NOT_SELECTED.md").exists()

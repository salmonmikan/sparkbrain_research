#!/usr/bin/env python3
"""Build an exact, execution-disabled source manifest for RV02 RD005.

The builder is intentionally source-preparation only. It binds the current clean
Git checkout and SHA-256 digests for the RD005 construction implementation,
reviewed matrix/preregistration boundary, all RD005-specific tests, the canonical
package-plan preflight, and this builder itself. It does not construct D1, open
capability output, score an outcome, create STARTED, or grant execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from sparkbrain.research.rv02_rd005_development_package import (
    RD005_REQUIRED_SOURCE_PATHS,
    RD005SourceManifest,
    RD005SourceManifestEntry,
)

_BUILDER_PATH = "scripts/build_rv02_rd005_source_manifest.py"
_MATRIX_PATH = "docs/research/RV02_RD005_PLANNED_MATRIX_92505.md"
_BOUND_CONSTRUCTION_PATH = "src/sparkbrain/research/rv02_rd005_bound_construction.py"
_EXTRA_PROVENANCE_PATHS = frozenset(
    {_BUILDER_PATH, _MATRIX_PATH, _BOUND_CONSTRUCTION_PATH}
)


def _git(repo_root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(f"RD005 source-manifest preparation requires git: {exc}") from exc
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise RuntimeError(f"RD005 source-manifest preparation failed: {detail}")
    return result.stdout.strip()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _discover_rd005_test_paths(root: Path) -> frozenset[str]:
    test_root = root / "tests"
    paths = frozenset(
        path.relative_to(root).as_posix()
        for path in sorted(test_root.glob("test_rv02_rd005_*.py"))
        if path.is_file()
    )
    if not paths:
        raise ValueError("RD005 source boundary contains no tests/test_rv02_rd005_*.py files")
    return paths


def _require_git_tracked(root: Path, relative_path: str) -> None:
    try:
        _git(root, "ls-files", "--error-unmatch", "--", relative_path)
    except RuntimeError as exc:
        raise ValueError(f"RD005 source path is not tracked by Git: {relative_path}") from exc


def build_source_manifest(repo_root: Path) -> RD005SourceManifest:
    """Return the exact RD005 source manifest for one clean Git checkout."""

    root = repo_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("RD005 repository root must be a directory")

    git_root = Path(_git(root, "rev-parse", "--show-toplevel")).resolve(strict=True)
    if git_root != root:
        raise ValueError(
            "RD005 repository root does not equal the checkout Git top-level: "
            f"expected {root}, got {git_root}"
        )

    head = _git(root, "rev-parse", "HEAD")
    if len(head) != 40 or any(char not in "0123456789abcdef" for char in head):
        raise ValueError("RD005 source HEAD must be a 40-character lowercase Git SHA")

    tracked_status = _git(root, "status", "--porcelain", "--untracked-files=no")
    if tracked_status:
        raise ValueError("RD005 source-manifest preparation requires a clean tracked checkout")

    paths = sorted(
        RD005_REQUIRED_SOURCE_PATHS
        | _EXTRA_PROVENANCE_PATHS
        | _discover_rd005_test_paths(root)
    )
    entries: list[RD005SourceManifestEntry] = []
    for relative_path in paths:
        candidate = root / relative_path
        try:
            resolved = candidate.resolve(strict=True)
        except FileNotFoundError as exc:
            raise ValueError(f"RD005 source path is missing: {relative_path}") from exc
        if not resolved.is_relative_to(root):
            raise ValueError(f"RD005 source path escapes repository root: {relative_path}")
        if not resolved.is_file():
            raise ValueError(f"RD005 source path is not a regular file: {relative_path}")
        _require_git_tracked(root, relative_path)
        entries.append(
            RD005SourceManifestEntry(
                path=relative_path,
                sha256=hashlib.sha256(resolved.read_bytes()).hexdigest(),
            )
        )

    manifest = RD005SourceManifest(source_git_sha=head, entries=tuple(entries))
    manifest.validate()
    return manifest


def _write_fresh(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(raw)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an exact SHA-256 source manifest for prospective RV02 RD005."
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--digest-output", type=Path)
    args = parser.parse_args(argv)

    manifest = build_source_manifest(args.repo_root)
    raw = _canonical_json(manifest.state_dict())
    if args.output is None:
        print(raw.decode("utf-8"), end="")
    else:
        _write_fresh(args.output, raw)
    if args.digest_output is not None:
        _write_fresh(args.digest_output, f"{manifest.manifest_sha256}\n".encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_source_manifest", "main"]

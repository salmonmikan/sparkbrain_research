#!/usr/bin/env python3
"""Preserve C19-R2 target-blind raw, manifest, and target-free source map atomically."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_destination(raw: str) -> Path:
    dest = Path(raw)
    if dest.is_absolute() or ".." in dest.parts or raw in {"", "."}:
        raise SystemExit("destination must be a non-root relative repository path")
    return dest


def _remote_branch_sha(remote: str, branch: str) -> str | None:
    result = _git("ls-remote", "--exit-code", "--heads", remote, branch, check=False)
    if result.returncode == 2:
        return None
    if result.returncode != 0:
        raise SystemExit(f"unable to inspect remote branch {remote}/{branch}: {result.stderr.strip()}")
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise SystemExit(f"ambiguous remote branch resolution for {remote}/{branch}")
    return lines[0].split()[0]


def preserve(
    *,
    payload: Path,
    manifest: Path,
    source_map: Path,
    base_commit: str,
    branch: str,
    destination: Path,
    remote: str,
    commit_message: str,
) -> dict[str, str]:
    files = (payload, manifest, source_map)
    if not all(path.is_file() for path in files):
        raise SystemExit("payload, manifest, and source map must all be regular files")
    if len({path.name for path in files}) != 3:
        raise SystemExit("R2 preservation filenames must be distinct")
    _git("cat-file", "-e", f"{base_commit}^{{commit}}")
    if _remote_branch_sha(remote, branch) is not None:
        raise SystemExit(f"remote preservation branch already exists: {branch}")

    digests = {path.name: _sha256(path) for path in files}
    _git("switch", "--create", branch, base_commit)
    destination.mkdir(parents=True, exist_ok=True)
    staged_paths: list[str] = []
    for path in files:
        dest = destination / path.name
        if dest.exists():
            raise SystemExit(f"destination collision: {dest}")
        shutil.copyfile(path, dest)
        if _sha256(dest) != digests[path.name]:
            raise SystemExit(f"copied-byte digest mismatch: {path.name}")
        staged_paths.append(str(dest))

    _git("add", "--", *staged_paths)
    staged = set(_git("diff", "--cached", "--name-only").stdout.splitlines())
    if staged != set(staged_paths):
        raise SystemExit(f"unexpected staged R2 preservation paths: {sorted(staged)}")
    _git("commit", "-m", commit_message)
    preservation_commit = _git("rev-parse", "HEAD").stdout.strip()
    _git("push", remote, f"HEAD:refs/heads/{branch}")
    remote_sha = _remote_branch_sha(remote, branch)
    if remote_sha != preservation_commit:
        raise SystemExit("remote R2 preservation ref mismatch")
    return {
        "base_commit": base_commit,
        "branch": branch,
        "destination": destination.as_posix(),
        "payload_sha256": digests[payload.name],
        "manifest_sha256": digests[manifest.name],
        "source_map_sha256": digests[source_map.name],
        "preservation_commit": preservation_commit,
        "remote": remote,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--source-map", required=True, type=Path)
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--commit-message", default="preserve(c19-r2): retain target-blind raw and source map")
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    result = preserve(
        payload=args.payload,
        manifest=args.manifest,
        source_map=args.source_map,
        base_commit=args.base_commit,
        branch=args.branch,
        destination=_validate_destination(args.destination),
        remote=args.remote,
        commit_message=args.commit_message,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

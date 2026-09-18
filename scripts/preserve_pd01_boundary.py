#!/usr/bin/env python3
"""Preserve PD0.1 target-blind raw, manifest, and target-free input inventory atomically."""

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    args = parser.parse_args()
    files = (args.raw, args.manifest, args.inventory)
    if not all(path.is_file() for path in files):
        raise SystemExit("PD01 preservation inputs must be regular files")
    if args.destination.is_absolute() or ".." in args.destination.parts:
        raise SystemExit("PD01 destination must be a safe relative path")
    if _remote_branch_sha("origin", args.branch) is not None:
        raise SystemExit("PD01 preservation branch already exists")
    _git("cat-file", "-e", f"{args.base_commit}^{{commit}}")
    digests = {path.name: _sha256(path) for path in files}
    _git("switch", "--create", args.branch, args.base_commit)
    args.destination.mkdir(parents=True, exist_ok=False)
    staged: list[str] = []
    for path in files:
        dest = args.destination / path.name
        shutil.copyfile(path, dest)
        if _sha256(dest) != digests[path.name]:
            raise SystemExit("PD01 copied-byte digest mismatch")
        staged.append(str(dest))
    _git("add", "--", *staged)
    if set(_git("diff", "--cached", "--name-only").stdout.splitlines()) != set(staged):
        raise SystemExit("PD01 unexpected preservation paths")
    _git("commit", "-m", "preserve(pd01): retain target-blind formal raw")
    preservation_commit = _git("rev-parse", "HEAD").stdout.strip()
    _git("push", "origin", f"HEAD:refs/heads/{args.branch}")
    if _remote_branch_sha("origin", args.branch) != preservation_commit:
        raise SystemExit("PD01 remote preservation ref mismatch")
    result = {
        "preservation_commit": preservation_commit,
        "branch": args.branch,
        "base_commit": args.base_commit,
        "destination": args.destination.as_posix(),
        "raw_sha256": digests[args.raw.name],
        "manifest_sha256": digests[args.manifest.name],
        "inventory_sha256": digests[args.inventory.name],
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
